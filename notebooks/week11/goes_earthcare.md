---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.6
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(week11:goes_earthcare)=
# goes-earthcare overlay

```{code-cell} ipython3
from pathlib import Path
import xarray as xr
import numpy as np
import pyproj
from matplotlib import pyplot as plt
import datetime
import pytz
import pandas as pd
from pyproj import CRS, Transformer
import affine
from a301_extras.sat_lib import make_new_rioxarray
import cartopy.crs as ccrs
import cartopy.feature as cfeature
```

## open the earthcare radar file

```{code-cell} ipython3
data_dir = Path().home() / 'repos/a301/satdata/earthcare'
radar_filepath = list(data_dir.glob("**/*.nc"))[0]
radar_ds = xr.open_dataset(radar_filepath)
radar_ds
```

### get the time and bounding box corners

```{code-cell} ipython3
midpoint = int(len(radar_ds['time'])/2.)
midtime = radar_ds['time'][midpoint].data

#datetime.datetime(midtime)
timestamp = pd.to_datetime(midtime)
timestamp
```

```{code-cell} ipython3
lats = radar_ds['latitude']
lons = radar_ds['longitude']
ymin, ymax = np.min(lats.data),np.max(lats.data)
xmin, xmax = np.min(lons.data),np.max(lons.data)
(xmin,ymin,xmax,ymax)
```

## Find the nearest GOES image

+++

### Function get_goes

```{code-cell} ipython3
from goes2go import goes_nearesttime
save_dir = Path.home() / "repos/a301/satdata/earthcare"
def get_goes(timestamp, satellite="goes16", product="ABI-L2-MCMIP",domain="C",
             download=True, save_dir=None):
    g = goes_nearesttime(
        timestamp, satellite=satellite,product=product, domain=domain, 
          return_as="xarray", save_dir = save_dir, download = download, overwrite = False
    )
    the_path = g.path[0]
    return the_path
```

## Get the cloudtop height

This variable is in the `ABI-L2-ACHAC` product, at 10 km resolution.  It is available every 60 minutes. The
full description is [here](https://www.star.nesdis.noaa.gov/goesr/docs/ATBD/Cloud_Height.pdf)

```{code-cell} ipython3
download_dict = dict(satellite="goes16",product = "ABI-L2-ACHAC",save_dir=save_dir)
```

```{code-cell} ipython3
writeit = False
if writeit:
    the_path = get_goes(timestamp,**download_dict)
else:
    the_path = ('noaa-goes16/ABI-L2-ACHAC/2024/348/22/OR_ABI-L2-ACHAC-M6_G16_s20243482251172'
                '_e20243482253545_c20243482256029.nc'
               )
full_path = save_dir / the_path
```

```{code-cell} ipython3
goes_ct = xr.open_dataset(full_path,mode = 'r',mask_and_scale = True)
type(goes_ct)
```

## calculate the projection coordinates

The x and y coordinates for the Dataset `goes_ct` are in radians.  The function `parse_cf` (where `CF` stands
for `climate and forecast`) extracts a dataset variable as a DataArray and converts those x and y values to meters in the geostationary CRS by multiplying by the height of the satellite. It also sets the `grid_mapping` attribute
to `goes_imager_projection` which allows goes2go to produce the geostationary CRS using `cloud_ct.metpy.pyproj_crs` or `cloud_ct.metpy.cartopy_crs`. The CF conventions
are documented [here](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.7/cf-conventions.html#_geostationary_projection) ).

```{code-cell} ipython3
cloud_top = goes_ct.metpy.parse_cf('HT')
type(cloud_top)
```

```{code-cell} ipython3
cloud_top.plot.imshow()
```

## Get the 11 micron thermal band

This is [channel 14](https://www.noaa.gov/jetstream/goes_east) in the
moisture and cloud product.  The brightness temperatures will have 2 km resolution,
but no atmospheric correction

```{code-cell} ipython3
download_dict = dict(satellite="goes16",
                     product = "ABI-L2-MCMIPC",save_dir=save_dir)
```

```{code-cell} ipython3
writeit = False
if writeit:
    the_path = get_goes(timestamp,**download_dict)
else:
    the_path = ('noaa-goes16/ABI-L2-MCMIPC/2024/348/22/OR_ABI-L2-MCMIPC-M6_G16_s20243482251172_'
                'e20243482253545_c20243482254074.nc'
               )
full_path = save_dir / the_path
```

```{code-cell} ipython3
goes_mc = xr.open_dataset(full_path,mode = 'r',mask_and_scale = True)
chan_14 = goes_mc.metpy.parse_cf('CMI_C14')
```

## Calculate the affine transforms

+++

### Function get_affine

```{code-cell} ipython3
def get_affine(goes_da):
    resolutionx = np.mean(np.diff(goes_da.x))
    resolutiony = np.mean(np.diff(goes_da.y))
    ul_x = goes_da.x[0].data
    ul_y = goes_da.y[0].data
    goes_transform = affine.Affine(resolutionx, 0.0, ul_x, 0.0, resolutiony, ul_y)
    return goes_transform
    
```

```{code-cell} ipython3
cloud_top_affine = get_affine(cloud_top)
chan_14_affine = get_affine(chan_14)
chan_14_affine, cloud_top_affine
```

## convert  cloud_top  to a rioxarray

+++

Use make_new_rioxarray introduced in {ref}`week8:goes_landsat_rio`

```python
def make_new_rioxarray(
    rawdata: np.ndarray,
    coords: dict,
    dims: tuple,
    crs: pyproj.CRS,
    transform: affine.Affine,
    attrs: dict | None = None,
    missing: float | None = None,
    name: str | None = "name_here") -> xr.DataArray:
    """
    create a new rioxarray from an ndarray plus components

    Parameters
    ----------

    rawdata: numpy array
    crs: pyproj crs for scene
    coords: xarray coordinate dict
    dims: x and y dimension names from coords
    transform: scene affine transform
    attrs: optional attribute dictionary
    missing: optional missing value
    name: optional variable name, defaults to "name_here"

    Returns
    -------

    rio_da: a new rioxarray
    """
```

+++

### Set cloud top height attributes

```{code-cell} ipython3
attribute_names=['long_name','standard_name','units','grid_mapping']
attributes ={name:item for name,item in cloud_top.attrs.items()
             if name in attribute_names}
attributes['history'] = f"written by goes_earthcare.ipynb on {datetime.datetime.now()}"
attributes['start'] = goes_ct.attrs['time_coverage_start']
attributes['end'] = goes_ct.attrs['time_coverage_end']
attributes['dataset'] = goes_ct.attrs['dataset_name']
attributes['title'] = 'cloud layer height'
attributes
```

```{code-cell} ipython3
the_dims = ('y','x')
goes_crs = cloud_top.metpy.pyproj_crs
coords_cloud_top = dict(x=cloud_top.x,y=cloud_top.y)
cloud_top_da = make_new_rioxarray(cloud_top,
                                  coords_cloud_top,
                                  the_dims,
                                  goes_crs,
                                  cloud_top_affine,
                                  attrs = attributes,
                                  missing=np.float32(np.nan),
                                  name = 'ht')
                                                                   
```

```{code-cell} ipython3
attribute_names=['long_name','standard_name','units','grid_mapping']
attributes ={name:item for name,item in chan_14.attrs.items()
             if name in attribute_names}
attributes['history'] = f"written by goes_earthcare.ipynb on {datetime.datetime.now()}"
attributes['start'] = goes_mc.attrs['time_coverage_start']
attributes['end'] = goes_mc.attrs['time_coverage_end']
attributes['dataset'] = goes_mc.attrs['dataset_name']
attributes['title'] = 'chan_14'
attributes
```

## convert chan_14 to a rioxarray

+++

### set chan_14 attributes

```{code-cell} ipython3
the_dims = ('y','x')
goes_crs = cloud_top.metpy.pyproj_crs
coords_chan_14 = dict(x=chan_14.x,y=chan_14.y)
chan_14_da = make_new_rioxarray(chan_14,
                                  coords_chan_14,
                                  the_dims,
                                  goes_crs,
                                  chan_14_affine,
                                  attrs = attributes,
                                  missing=np.float32(np.nan),
                                  name = 'chan_14')
                                  
```

```{code-cell} ipython3
chan_14_da.plot.imshow()
```

## crop the images

We want to crop the images to the radar track.  To do that, we first need to get
the bounding box in geostationary coordinates, so we can use the `rio.clip_box` function.
We did this in week 8 in {ref}`week8:goes_clip_bounds`

```{code-cell} ipython3
xmin,ymin,xmax,ymax
```

### Transform the bounds from lat/lon to geostationary crs

```{code-cell} ipython3
#
# transform bounds from lat,lon to goes crs
#
latlon_crs = pyproj.CRS.from_epsg(4326)
transform = Transformer.from_crs(latlon_crs, goes_crs,always_xy=True)
xmin_goes,ymin_goes = transform.transform(xmin,ymin)
xmax_goes,ymax_goes = transform.transform(xmax,ymax)
print(f"{(xmax_goes - xmin_goes)=} m")
print(f"{(ymax_goes - ymin_goes)=} m")
bounds_goes = xmin_goes,ymin_goes,xmax_goes,ymax_goes
```

### Crop using clip_box

```{code-cell} ipython3
#
# now crop to these bounds using clip_box
#
clipped_cloud_top=cloud_top_da.rio.clip_box(*bounds_goes)
clipped_chan_14 = chan_14_da.rio.clip_box(*bounds_goes)
```

```{code-cell} ipython3
clipped_cloud_top.plot.imshow()
```

```{code-cell} ipython3
clipped_chan_14.plot.imshow()
```

## Make cartopy plots with radar ground track

Borrow code from {ref}`week8:cartopy_goes`

```{code-cell} ipython3
extent = (xmin_goes,xmax_goes,ymin_goes,ymax_goes)
cartopy_crs = cloud_top.metpy.cartopy_crs
fig,ax = plt.subplots(1,1,figsize=(10,8), subplot_kw={"projection":cartopy_crs})
clipped_chan_14.plot.imshow(
    ax = ax,
    origin="upper",
    extent= extent,
    transform=cartopy_crs,
    interpolation="nearest",
    vmin=220,
    vmax=285
);
ax.coastlines(resolution="50m", color="black", linewidth=2)
ax.add_feature(ccrs.cartopy.feature.STATES,edgecolor="red")
```

```{code-cell} ipython3
fig,ax = plt.subplots(1,1,figsize=(10,8), subplot_kw={"projection":cartopy_crs})
clipped_cloud_top.plot.imshow(
    ax = ax,
    origin="upper",
    extent= extent,
    transform=cartopy_crs,
    interpolation="nearest"
);
ax.coastlines(resolution="50m", color="black", linewidth=2)
ax.add_feature(ccrs.cartopy.feature.STATES,edgecolor="red");
```

## Add the groundtrack

```{code-cell} ipython3
goes_x, goes_y =  transform.transform(lons, lats)
hit = lats > 35
```

```{code-cell} ipython3
ax.plot(goes_x[hit],goes_y[hit],'w-')
display(fig)
```

```{code-cell} ipython3

```
