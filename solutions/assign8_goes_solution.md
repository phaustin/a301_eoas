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

(assign8_goes_solution)=
# Assignment 8 GOES heights solution


- upload a notebook that
  -  overlays your radar cases's ground track on the nearest GOES cloud height image using the code in {ref}`week12:goes_earthcare`
  - Add a function that locates image row/column values along the radar lat/lon coordinates
    of the GOES height image. Use it to produce a height/distance plot that shows the
    radar reflectivity image  with the colocated GOES HT heights overlaid as a line on the image.  Do
    GOES and earthcare agree on the location of cloudtop?

## Installation

- fetch and rebase to pick up the week12 folder with this ipynb file
- `pip install -r requirements.txt`  to install the newest version of the `a301_extras` library

## open the earthcare radar file

Use the file written by {ref}`week11:earthcare_xarray`

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
casenum = radar_ds.attrs['casenum']
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

## get row,column from lat,lon

+++

### Function get_rowcol

reuse code from {ref}`week12:goes_earthcare` and {ref}`week12:goes_temperature`

```{code-cell} ipython3
affine_transform = goes_ht.rio.transform()
goes_crs = goes_ht.rio.crs
latlon_crs = pyproj.CRS.from_epsg(4326)
goes_latlon_xy = Transformer.from_crs(latlon_crs, goes_crs,always_xy=True)
x_goes,y_goes = goes_latlon_xy.transform(lonvec,latvec)
```

```{code-cell} ipython3
def get_rowcol(affine_transform,x_coords,y_coords):
    image_row, image_col = ~affine_transform * (x_coords,y_coords)
    image_col = np.round(image_col).astype(np.int32)
    image_row = np.round(image_row).astype(np.int32)
    return image_col,image_row
```

```{code-cell} ipython3
track_col, track_row = get_rowcol(affine_transform,x_goes,y_goes)
```

## Sample GOES heights along track

```{code-cell} ipython3
the_heights = []
for row, col in zip(track_col, track_row):
    the_heights.append(goes_ht[row,col].data)
```

## Add to the radar reflectivity plot

```{code-cell} ipython3
fig, ax = plt.subplots(1,1,figsize=(12,3))
radar_ds['dbZ'].plot(ax = ax, x="distance",y="height",vmin=-3,vmax=25);
ax.plot(radar_ds['distance'],the_heights,'r-')
ax.set_ylim(0,15000)
ax.set_xlabel("distance (km)")
ax.set_ylabel("height (m)")
ax.set_title(f"{casenum}");
```

## To debug: check against image

+++

### Make groundtrack heights stand out

```{code-cell} ipython3
for row, col in zip(track_col, track_row):
    goes_ht[row,col]=20000
```

```{code-cell} ipython3
xmin = -145
xmax = -85.
ymax = 70
ymin = 20
xmin_goes,ymin_goes = goes_latlon_xy.transform(xmin,ymin)
xmax_goes,ymax_goes = goes_latlon_xy.transform(xmax,ymax)
extent = (xmin_goes,xmax_goes,ymin_goes,ymax_goes)
```

```{code-cell} ipython3
def make_cartopy_crs(wkt_string):
    bad_cartopy_crs = ccrs.Projection(wkt_string)
    terms=bad_cartopy_crs.to_dict()
    globe_kwargs = dict(semimajor_axis = terms['a'],
                  semiminor_axis=6356752.3141,
                 inverse_flattening = terms['rf'])
    crs_kwargs = dict(central_longitude = terms['lon_0'],
                    satellite_height = terms['h'],
                 sweep_axis = 'x')
    globe=ccrs.Globe(ellipse=None, **globe_kwargs)
    cartopy_crs = ccrs.Geostationary(**crs_kwargs,globe=globe)
    return cartopy_crs
```

```{code-cell} ipython3
wkt_string = goes_ht.attrs['cartopy_crs']
extent = (xmin_goes,xmax_goes,ymin_goes,ymax_goes)
cartopy_crs = make_cartopy_crs(wkt_string)
fig,ax = plt.subplots(1,1,figsize=(10,8),subplot_kw={'projection':cartopy_crs})
goes_ht.plot.imshow(
    ax = ax,
    origin="upper",
    extent= extent,
    transform=cartopy_crs,
    interpolation="nearest",
    vmin=0,
    vmax=16000
);
ax.coastlines(resolution="50m", color="black", linewidth=2)
ax.add_feature(ccrs.cartopy.feature.STATES,edgecolor="red")
```

```{code-cell} ipython3

```
