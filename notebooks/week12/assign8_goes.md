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

(week12:goes_earthcare)=
# goes-earthcare overlay

## Introduction

This notebook 

- reads in the netcdf file container the Earthcare case you saved in {ref}`week11:earthcare_xarray`
- finds the closest GOES 16 or GOES 18 image and extracts the cloud top height and the channel 14 (11 micron) brightness temperature
- crops the GOES image to the region of the Earthcare radar groundtrack
- plots the groundtrack on top of the GOES heights

This sets up the second problem in {ref}`week12:assign8`

## Installation

- fetch and rebase to pick up the week12 folder with this ipynb file
- `pip install -r requirements.txt`  to install the newest version of the `a301_extras` library

## open the earthcare radar file

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
import rioxarray
import xarray as xr
```

```{code-cell} ipython3
data_dir = Path().home() / 'repos/a301/satdata/earthcare'
radar_filepath = list(data_dir.glob("**/*.nc"))[0]
radar_ds = xr.open_dataset(radar_filepath)
radar_ds
```

### Get the radar ground track

```{code-cell} ipython3
latvec = radar_ds.latitude
lonvec = radar_ds.longitude
```

## open clipped ht file

```{code-cell} ipython3
ht_filepath = list(data_dir.glob("**/*.tif"))[0]
ht_filepath
```

```{code-cell} ipython3
goes_ht = rioxarray.open_rasterio(ht_filepath).squeeze()
goes_ht.plot.imshow();
```

```{code-cell} ipython3
goes_ht.attrs
```

## get row,column from lat,lon

+++

### Function get_rowcol

reuse code from {ref}`(week12:goes_earthcare` and {ref}`week12:goes_temperature`

```{code-cell} ipython3
affine_transform = goes_ht.rio.transform()
goes_crs = goes_ht.rio.crs
latlon_crs = pyproj.CRS.from_epsg(4326)
goes_latlon_xy = Transformer.from_crs(latlon_crs, goes_crs,always_xy=True)
x_goes,y_goes = goes_latlon_xy.transform(lonvec,latvec)
```

```{code-cell} ipython3
def get_rowcol(affine_transform,x_coords,y_coords):
    image_col, image_row = ~affine_transform * (x_coords,y_coords)
    image_col = np.round(image_col).astype(np.int32)
    image_row = np.round(image_row).astype(np.int32)
    return image_col,image_row
```

```{code-cell} ipython3
track_col, track_row = get_rowcol(affine_transform,x_goes,y_goes)
```

## Sample goes heights along track

```{code-cell} ipython3
the_heights = []
for row, col in zip(track_col, track_row):
    the_heighs.append(goes_ht
```

```{code-cell} ipython3
xmin_goes,ymin_goes = goes_latlon_xy.transform(xmin,ymin)
xmax_goes,ymax_goes = goes_latlon_xy.transform(xmax,ymax)
extent = (xmin_goes,xmax_goes,ymin_goes,ymax_goes)
```

```{code-cell} ipython3
import cartopy
wkt_string = goes_ht.attrs['cartopy_crs']
cartopy_crs = ccrs.Projection(wkt_string)
cartopy_crs.to_dict()
```

```{code-cell} ipython3
def make_cartopy_crs(wkt_string):
goes_coeffs = goes_da.rio.crs.to_dict()
      print(goes_coeffs) 
      globe_kwargs = dict(semimajor_axis = goes_coeffs['a'],
                    semiminor_axis=6356752.3141,
                   inverse_flattening = goes_coeffs['rf'])
      crs_kwargs = dict(central_longitude = goes_coeffs['lon_0'],
                 satellite_height = goes_coeffs['h'],
                  sweep_axis = 'x')
   
     globe=ccrs.Globe(ellipse=None, **globe_kwargs)
     cartopy_crs = ccrs.Geostationary(**crs_kwargs,globe=globe)
     return cartopy_crs
```

```{code-cell} ipython3
extent = (xmin_goes,xmax_goes,ymin_goes,ymax_goes)
cartopy_crs = make_cartopy_crs(goes_ht)
fig,ax = plt.subplots(1,1,figsize=(10,8),subplot_kw={'projection':cartopy_crs})
goes_ht.plot.imshow(
    ax = ax,
    origin="upper",
    extent= extent,
    transform=cartopy_crs,
    interpolation="nearest",
    vmin=220,
    vmax=285
);
# ax.coastlines(resolution="50m", color="black", linewidth=2)
# ax.add_feature(ccrs.cartopy.feature.STATES,edgecolor="red")
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

+++

goes_x, goes_y =  transform.transform(lons, lats)
hit = lats > 0

+++

ax.plot(goes_x[hit],goes_y[hit],'w-')
display(fig)

```{code-cell} ipython3

```
