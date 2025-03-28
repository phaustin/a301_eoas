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

(week11:earthcare)=
# Reading earth data


```{code-cell} ipython3
from pathlib import Path
import xarray as xr
import numpy as np
import pyproj
from matplotlib import pyplot as plt
import datetime
import pytz
```

```{code-cell} ipython3
data_dir = Path().home() / 'repos/a301/satdata/earthcare'
radar_filepaths = list(data_dir.glob("**/*.h5"))
filepaths=dict()
for filepath in radar_filepaths:
    relpath = filepath.relative_to(data_dir)
    casename = relpath.parts[0]
    filepaths[casename]=filepath
    
```

```{code-cell} ipython3
def sort_keys(the_case):
    number = the_case[4:]
    return int(number)

```

```{code-cell} ipython3
sorted_keys = list(filepaths.keys())
sorted_keys.sort(key=sort_keys)
casenum = 'case5'
#sorted_keys
```

```{code-cell} ipython3
cpr_data = xr.open_dataset(filepaths[casenum], engine='h5netcdf', group='/ScienceData/Data',
                            decode_times=True,  phony_dims='access')
cpr_meta = xr.open_dataset(filepaths[casenum], engine='h5netcdf', group='/ScienceData/Geo',
                           decode_times=True, phony_dims='access')
```

```{code-cell} ipython3
def find_times(filepath):
    cpr_meta = xr.open_dataset(filepath, engine='h5netcdf', group='/ScienceData/Geo',
                           decode_times=False, phony_dims='access')
    times = cpr_meta['profileTime'].data
    start_time = datetime.datetime(2000,1,1,0,0,0)
    the_times =[start_time + datetime.timedelta(seconds=item) for item in times]
    the_times = [item.replace(tzinfo = pytz.utc) for item in the_times]
    return the_times[0],the_times[-1]
```

## Print the case times

```{code-cell} ipython3
for casename in sorted_keys:
    filepath = filepaths[casename]
    start, stop = find_times(filepath)
    print(casename, start, stop)
```

```{code-cell} ipython3
times = cpr_meta['profileTime'].data
start_time = datetime.datetime(2000,1,1,0,0,0)
the_times =[start_time + datetime.timedelta(seconds=item) for item in times]
the_times = [item.replace(tzinfo = pytz.utc) for item in the_times]
the_times[-1],the_times[0]
```

```{code-cell} ipython3
cpr_meta = xr.open_dataset(filepaths['case2'], engine='h5netcdf', group='/ScienceData/Geo',
                            phony_dims='access')
the_times = cpr_meta['profileTime'].data
the_times[-1],the_times[0]
```

## get binheights

```{code-cell} ipython3

def get_binheights(cpr_meta):
    the_bins = cpr_meta.binHeight[...]
    the_bins = the_bins[0,:].data
    diff_bins = np.diff(the_bins)
    del_y = float(np.nanmean(diff_bins))
    new_y = [float(the_bins[0])]
    for count,old_y in enumerate(the_bins[1:]):
        if np.isnan(old_y):
            new_y.append(float(new_y[count]) + del_y)
        else:
            new_y.append(float(old_y))
    return np.array(new_y)

yheights = get_binheights(cpr_meta)
```

## Get reflectivity

```{code-cell} ipython3
radar = np.flipud(cpr_data['radarReflectivityFactor'].T)
#plt.imshow(cpr_data['radarReflectivityFactor'])
out = 10*np.log10(radar)
distance.shape
yheights.shape
```

```{code-cell} ipython3
ax[0]
```

```{code-cell} ipython3
fig, ax = plt.subplots(1, 1, figsize=(12, 5))
plt.pcolormesh(out,ax=ax,y=yheights,x=distance) 
```

```{code-cell} ipython3

```

```{code-cell} ipython3
great_circle=pyproj.Geod(ellps='WGS84')
meters2km = 1.e-3
def calc_distance(lonvec,latvec):
    distance=[0]
    startlon,startlat = lonvec[0],latvec[0]
    for lon,lat in zip(lonvec[1:],latvec[1:]):
        azi12,azi21,step= great_circle.inv(startlon,startlat,lon,lat)
        distance.append(distance[-1] + step)
        startlon,startlat = lon, lat
    distance=np.array(distance)*meters2km
    return distance
```

```{code-cell} ipython3
cpr_new = cpr_data.rename_dims({'phony_dim_0':'time','phony_dim_1': 'height'})
```

```{code-cell} ipython3
meta_new  = cpr_meta.rename_dims({'phony_dim_0':'time','phony_dim_1': 'height'})
height = cpr_meta['binHeight'].data[0,::-1]
lonvec = cpr_meta['longitude'].data
latvec = cpr_meta['latitude'].data
distance = calc_distance(lonvec, latvec)
coords = dict(distance=("time", distance),height=("height",height))
cpr_meta = cpr_meta.assign_coords(coords=coords)
cpr_data = cpr_data.assign_coords(coords=coords)
```

```{code-cell} ipython3
plt.plot(lonvec,latvec)
```

```{code-cell} ipython3
test = np.float64(cpr_meta['profileTime'].data)
test
```

```{code-cell} ipython3
cpr_meta
```

```{code-cell} ipython3
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
    dims: x and y dimension names from coorcds
    transform: scene affine transform
    attrs: optional attribute dictionary
    missing: optional missing value
    name: optional variable name, defaults to "name_here"

    Returns
    -------

    rio_da: a new rioxarray
    """
    rio_da=xr.DataArray(rawdata.data,coords=coords,
                            dims=dims,name=name)
    rio_da.rio.write_crs(crs, inplace=True)
    rio_da.rio.write_transform(transform, inplace=True)
    if attrs is not None:
        rio_da=rio_da.assign_attrs(attrs)
    if missing is not None:
        rio_da = rio_da.rio.set_nodata(missing)
    return rio_da
```

## clip to lat lon box

+++

## Simple RGB Figure
At the most simple level, here is how to produce an RGB from the GOES ABI data.

```{code-cell} ipython3
from goes2go.data import goes_nearesttime
import matplotlib.pyplot as plt 
from datetime import datetime
from pathlib import Path
import xarray
```

```{code-cell} ipython3
# Get an ABI Dataset
save_dir = Path.home() / "repos/a301/satdata/goes" 
writeit = False
if writeit:
    g = goes_nearesttime(
        datetime(2020, 6, 25, 18), satellite="goes16",product="ABI-L2-MCMIP", domain='C', 
          return_as="xarray", save_dir = save_dir, download = True, overwrite = False
    )
    the_path = g.path[0]
else:
    the_path = ("noaa-goes16/ABI-L2-MCMIPC/2020/177/18/"
                "OR_ABI-L2-MCMIPC-M6_G16_s20201771801172_e20201771803551_c20201771804104.nc")
    full_path = save_dir / the_path
    g = xarray.open_dataset(full_path,mode = 'r',mask_and_scale = True)
# Create RGB and plot
image = g.rgb.TrueColor()
image.plot.imshow();
```

### keywords for cartopy plotting

+++

## Read earthcare


```{code-cell} ipython3
g.rgb.imshow_kwargs
```

## All available RGB recipes

```{code-cell} ipython3
from goes2go.data import goes_nearesttime
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
```

```{code-cell} ipython3
writeit = False
if writeit:
    G16 = goes_nearesttime('2024-06-25 18',satellite=16,save_dir=save_dir)
    print(G16.path[0])
else:
    the_path = ("noaa-goes16/ABI-L2-MCMIPC/2024/177/18"
                "/OR_ABI-L2-MCMIPC-M6_G16_s20241771801172_e20241771803557_c20241771804062.nc")
    full_path = save_dir / the_path
    G16 = xarray.open_dataset(full_path,mode = 'r',mask_and_scale = True)
if writeit:
    G18 = goes_nearesttime('2024-06-25 18',satellite=18,save_dir=save_dir)
    print(G18.path[0])
else:
    the_path = ("noaa-goes16/ABI-L2-MCMIPC/2024/177/18"
                "/OR_ABI-L2-MCMIPC-M6_G16_s20241771801172_e20241771803557_c20241771804062.nc")
    full_path = save_dir / the_path
    G18 = xarray.open_dataset(full_path,mode = 'r',mask_and_scale = True)
```

```{code-cell} ipython3

```

```{code-cell} ipython3
rgb_products = [i for i in dir(G16.rgb) if i[0].isupper()]

for product in rgb_products:

    fig = plt.figure(figsize=(15, 12))
    ax18 = fig.add_subplot(1, 2, 1, projection=G18.rgb.crs)
    ax16 = fig.add_subplot(1, 2, 2, projection=G16.rgb.crs)

    for ax, G in zip([ax18, ax16], [G18, G16]):
        RGB = getattr(G.rgb, product)()

        #common_features('50m', STATES=True, ax=ax)
        ax.imshow(RGB, **G.rgb.imshow_kwargs)
        ax.set_title(f"{G.orbital_slot} {product}", loc='left', fontweight='bold')
        ax.set_title(f"{G.t.dt.strftime('%H:%M UTC %d-%b-%Y').item()}", loc="right")
    plt.subplots_adjust(wspace=0.01)
    #plt.savefig(f'../docs/_static/{product}', bbox_inches='tight')
```

```{code-cell} ipython3

```
