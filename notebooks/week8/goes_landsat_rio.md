---
jupytext:
  formats: md:myst,ipynb
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
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

(week8:goes_landsat_rio)=
# Combining goes and landsat data

The cropping function for satpy left something to be desired -- it covered less than half of the clipped
landsat scene



- Download goes_landsat.ipynb from the [week8 folder](https://drive.google.com/drive/folders/1-Ja2wVKVIjkZb7Gx_rfc14J_aBYiknuw?usp=sharing)
  
- You'll also need to copy the band 5 hls tif files in the [vancouver_2023](https://drive.google.com/drive/folders/1UwTc4MnneI2eZ6rHqKFzF4YdRRbQi4sS?usp=sharing) folder into a new folder on your drive called `~/repos/a301/satdata/landsat/vancouver_2023`

```{code-cell} ipython3
from pathlib import Path
import json

import cartopy
import numpy as np
from matplotlib import pyplot as plt
from pyproj import CRS, Transformer
import rioxarray
import xarray as xr
from cartopy import crs as ccrs
from a301_lib import (
    make_pal,
    Row_col_offsets,
    Clip_point,
    Bounding_box,
    Cartopy_extent,
    find_bounds
    )
    
import pyproj
import pydantic
from goes2go.data import goes_nearesttime
from datetime import datetime
import affine
```

## Get the original hls tif files from disk

This cell finds all the 3660 x 3660 landsat tifs we downloaded in the satdata/landsat/vancouver folder.  We can use the `*` wildcard
so we don't have to type in long filenames, and the `**` wildcard so we look in all subfolders.  If you're interested  here's
the [wikipedia entry on globbing](https://en.wikipedia.org/wiki/Glob_(programming)#:~:text=6%20References-,Origin,command%3A%20%2Fetc%2Fglob.)

```{code-cell} ipython3
data_dir = Path().home() / 'repos/a301/satdata/landsat'
the_tifs = list(data_dir.glob('**/vancouver_2023/HLS.L30*tif'))
print(the_tifs)
```

## Read band 5 into a dictionary

Note on the next cell:

- Because we set `masked_and_scale=True`, all `-9999` values are changed to `np.nan` and the data is multiplied by the scale factor and converted from `int16` to `float32`

```{code-cell} ipython3
band_dict={}
for tif_path in the_tifs:
    if 'Fmask' in str(tif_path):
        hls_band = rioxarray.open_rasterio(tif_path,
                                           mask_and_scale=False)
        band_name = 'fmask'
    else:
        hls_band = rioxarray.open_rasterio(tif_path,
                                           mask_and_scale=True)
        band_name = hls_band.long_name
    hls_band = hls_band.squeeze()
    print(f"{band_name=}")
    band_dict[band_name] = hls_band
    if 'unit' in hls_band.attrs:
        print(f"{hls_band.unit=}")
```

```{code-cell} ipython3
landsat_nir = band_dict['NIR']
landsat_crs = pyproj.CRS(landsat_nir.rio.crs)
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1,figsize = (6,6))
vmin = 0.0
vmax = 0.5
pal_dict = make_pal(vmin=vmin,vmax=vmax)
landsat_nir.plot.imshow(ax=ax,
                    norm = pal_dict['norm'],
                    cmap = pal_dict['cmap'],
                    extend = "both");
```

```{code-cell} ipython3
a=band_dict['NIR']
np.unique(np.diff(a.x))
```

## Define the image point and offsets

To make the bounding box, we add column and row offsets
to a point that we want in our image, in this case EOSC

```{code-cell} ipython3
ubc_lon = -123.2460 #degrees West
ubc_lat = 49.2606  # degrees North
image_point = Clip_point(lon = ubc_lon, lat = ubc_lat)
#
# remember that rows increase downwards
# make a 1000 row by 800 column (30 km x 24 km) clipped image
#
#
offsets = Row_col_offsets(west = -500,
                south =300,
                east =  300,
                north = -700)
nir = band_dict['NIR']
```

## Find bounds and clip

```{code-cell} ipython3
landsat_bbox = find_bounds(nir, offsets, image_point, scene_crs = landsat_crs)
print(landsat_bbox)
```

```{code-cell} ipython3
bounds_list = list(dict(landsat_bbox).values())
clipped_ds = landsat_nir.rio.clip_box(*bounds_list)
clipped_ds.shape
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1,figsize = (6,6))
clipped_ds.plot.imshow(ax=ax,
                    norm = pal_dict['norm'],
                    cmap = pal_dict['cmap'],
                    extend = "both");
```

## Get GOES image

```{code-cell} ipython3
save_dir = Path.home() / "repos/a301/satdata/goes" 
```

### Read the landsat overpass time

```{code-cell} ipython3
landsat_nir.SENSING_TIME
```

### Get the coincident GOES 18 image

```{code-cell} ipython3
getdata = False
if getdata:
    g = goes_nearesttime(
        datetime(2023, 8, 24, 19), satellite="goes18",product="ABI-L2-MCMIP", domain='C', 
          return_as="xarray", save_dir = save_dir, download = True, overwrite = False
    )
    the_path = g.path[0]
else:
    the_path = ("noaa-goes18/ABI-L2-MCMIPC/2023/236/19/"
                "OR_ABI-L2-MCMIPC-M6_G18_s20232361901177"
                "_e20232361903550_c20232361904064.nc")
```

```{code-cell} ipython3
full_path = save_dir / the_path
```

### Read the image with goes2go

```{code-cell} ipython3
goesC = xr.open_dataset(full_path,mode = 'r',mask_and_scale = True)
```

### Get the veggie band (nir)

```{code-cell} ipython3
c3 = goesC.metpy.parse_cf('CMI_C03')
cartopy_crs = c3.metpy.cartopy_crs
goes_crs = pyproj.CRS(cartopy_crs)
goes_coords = dict(c3.coords)
resolutionx = np.mean(np.diff(c3.x))
resolutiony = np.mean(np.diff(c3.y))
print(resolutionx, resolutiony)
attrs = c3.attrs
```

### create the affine transform

```{code-cell} ipython3
ul_x = c3.x[0].data
ul_y = c3.y[0].data
lr_x = c3.y[-1].data
lr_y = c3.y[-1].data
new_affine = affine.Affine(resolutionx, 0.0, ul_x, 0.0, resolutiony, ul_y)
new_affine
```

```{code-cell} ipython3
c3.plot.hist();
```

### Copy the data to a rioxarray

```{code-cell} ipython3
def make_new_rioxarray(
    dataset:np.ndarray,
    coords: dict,
    dims: tuple,
    crs: pyproj.CRS,
    transform: affine.Affine,
    attrs: dict | None = None) -> xr.DataArray:
    """
    create a new rioxarray from an ndarray plus components

    Parameters
    ----------

    rio_da: xarray DataArray
       a DataArray with rasterio metadata
    crs: optional pyproj crs
       a crs which is able to return its epsg code
       if it's missing, the crs from rio_da will be copied

    Returns
    -------

    clipped_da: xarray.DataArray
      a DataArray with metadata and data copied from rio_da
    
    
    """
    #
    # NASA hls files have bad crs, so allow for an override parameter
    #
    if crs is None:
        crs = rio_da.rio.crs
    clipped_da=xr.DataArray(rio_da.data,coords=rio_da.coords,
                            dims=rio_da.dims)
    clipped_da.rio.write_crs(crs, inplace=True)
    clipped_da.rio.write_transform(rio_da.rio.transform(), inplace=True)
    clipped_da=clipped_da.assign_attrs(rio_da.attrs)
    clipped_da = clipped_da.rio.set_nodata(np.float32(np.nan))
    return clipped_da
```

```{code-cell} ipython3
np.unique(np.diff(c3.x))
```

```{code-cell} ipython3
c3.plot.hist();
```

```{code-cell} ipython3
fig = plt.figure(figsize=(15, 12))
lc = ccrs.LambertConformal(central_longitude= -137)
ax = fig.add_subplot(1, 1, 1, projection=lc)


ax.imshow(
    c3.data,
    origin="upper",
    extent=original_extent,
    transform=cartopy_crs,
    interpolation="none",
    vmin =0,
    vmax=30,
    alpha=0.6
)
ax.set_extent([-170, -110, 10, 55], crs=ccrs.PlateCarree())
ax.coastlines(resolution="50m", color="black", linewidth=1)
ax.add_feature(ccrs.cartopy.feature.STATES);
```

## Transform the landsat bounds to GOES coords

We what to clip to the same region as our clipped landsat scene

```{code-cell} ipython3
clipped_ds.shape
```

### Bug! copied the wrong CRS

need the clipped crs, not the full scene

```{code-cell} ipython3
# -> bad: landsat_crs  = nir.rio.crs
xmin,ymin,xmax,ymax = clipped_ds.rio.bounds()
print(f"{(xmax - xmin)=}")
print(f"{(ymax - ymin)=}")
transform = Transformer.from_crs(landsat_crs, goes_crs)
xmin_goes,ymin_goes = transform.transform(xmin,ymin)
xmax_goes,ymax_goes = transform.transform(xmax,ymax)
print(f"{(xmax_goes - xmin_goes)=}")
print(f"{(ymax_goes - ymin_goes)=}")
bounds_goes = xmin_goes,ymin_goes,xmax_goes,ymax_goes
#
# now crop to these bounds
#
cropped_ds=goes_2023.crop(xy_bbox = bounds_goes)
cropped_c3 = cropped_ds['C03']
xmin,ymin,xmax,ymax = cropped_c3.area.area_extent
cropped_c3.shape
```

##  Verdict: still not great

Sub-optimal -- correct area, but the landsat image is 30 km x 24 km and the cropped GOES image is
only 16 km x 18 km -- way to conservative.  We'll try switching to rioxarray in the next notebook

```{code-cell} ipython3
cropped_c3.shape, clipped_ds.shape
```

### Plot the cropped goes image

```{code-cell} ipython3
extent_cartopy = xmin,xmax,ymin,ymax
fig2, ax = plt.subplots(1, 1, figsize=(10,10), 
                        subplot_kw={"projection": cartopy_crs})
cs = ax.imshow(
    cropped_c3.data,
    origin="upper",
    extent=extent_cartopy,
    transform=cartopy_crs,
    alpha=1,
    vmin=0,
    vmax=30
)
ax.set_extent(extent_cartopy,crs=cartopy_crs)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="auto", 
                                            levels=[1, 2, 3],edgecolor='red'));
```

### Next step

Resample the GOES image to the Landsat grid for a pixel by pixel comparison
