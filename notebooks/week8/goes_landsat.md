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

(week8:goes_landsat)=
# Combining goes and landsat data using rioxarray

- 2025/March/7: fixed {ref}`crs_bug`


## Introduction

This notebook shows how to clip landsat and goes images to the same bounding box.  This could be useful to provide largescale atmospheric context, to
check the data, or to fill in missing data (although the pixel sizes
are completely different (3 km for GOES and 30 m for Landsat)

New material:

1) I read the GOES image and crop it to a bounding box using the [satpy module](https://satpy.readthedocs.io/en/latest/)

2) I create a set of python objects to hold the image extent, a point on the image and the bounding box using the [pydantic module]([pydantic library](https://realpython.com/python-pydantic/)

3) I define a new function `find_bounds` that uses `type hints` to specify the required types for function parameters.  This extra safety isn't particularly useful for short programs using Jupyter notebooks, but it is very helpful when writing code that will be put in a library and used by other people.  Not required for your assignments, see [this type checking guide](https://realpython.com/python-type-checking/) for more information.

### To install

- you'll need to install satpy and pydantic into the a301 environment

  ```
  conda install pydantic
  conda install satpy

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
from a301_lib import make_pal
import pyproj
import pydantic
from goes2go.data import goes_nearesttime
from datetime import datetime
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

## Make some data container objects

The [pydantic library](https://realpython.com/python-pydantic/) provides
a way to create new python types that enforce the order and the type
of their internal data.   This helps document the code and avoids errors
caused by passing the wrong variables into a function.

```{code-cell} ipython3
from pydantic import BaseModel

class Row_col_offsets(BaseModel):
    """
    row/col offsets needed to define
    rows and column ranges in a region
    """
    west: int
    south: int
    east: int
    north: int

class Clip_point(BaseModel):
    """
    a location within the clipped region 
    in geodetic coordinates
    """
    lon: float
    lat: float

class Bounding_box(BaseModel):
    """
    bounding box for rioxarray.clip_box in map coordinates
    """
    xmin: float
    ymin: float
    xmax: float
    ymax: float

class Cartopy_extent(BaseModel):
    """
    cartopy plotting extent in map coords
    """
    xmin: float
    xmax: float
    ymin: float
    ymax: float
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

#### Why parameter typing is helpful

In the box below, the class `Clip_point` cannot convert the string 'cinco' to a float,
and will raise an exception.  Passing integers or strings that can be
converted to float will succeed.  This becomes much  more helpful
when you are trying to use someone's large library with complex parameters.

```{code-cell} ipython3
# try this 
a = 'cinco'
b = '5'
c = 5
d = 5.
#bad = Clip_point(lon = c, lat = a)
ok = Clip_point(lon = d, lat = b)
```

### The find_bounds function


The function below has a signature with 3 required parameters (scene_ds, offsets, image_point)
and one optional parameter (scene_crs).  Each parameter is followed by a *type hint*, which
tells you the type of the parameter being passed.  It is only a hint -- the code will run
even if you pass the wrong type, but you can run a separate type checking
program that will catch type mismatches when you call `find_bounds` in 
your code.

```{code-cell} ipython3
def find_bounds(
    scene_ds: xr.DataArray,
    offsets: Row_col_offsets,
    image_point: Clip_point,
    scene_crs: pyproj.CRS | None = None ) -> Bounding_box: 
    """
    Given a point in x,y map coordinates and
    a set of row, column offsets, return a
    bounding box that can be used by rio.clip_box to clip
    the image

    Parameters
    ----------
    scene_ds: rioxarray DataArray
    offsets: west, south, east, north
    image_point: lon, lat for point in image
    scene_crs: Optional -- point in scene, if missing use scene_ds.rio.crs

    Returns
    -------

    bounds: west, south, east, north bounds for rio.clip_box
    """ 
    if scene_crs is None:
        #
        # turn the rasterio CRS into a pyproj.CRS
        #
        scene_crs = pyproj.CRS(scene_ds.rio.crs)
    #
    # step 1: find the image point in utm coords
    # need to transform the latlon point to x,y utm zone 10
    #
    full_affine = scene_ds.rio.transform()
    p_latlon = CRS.from_epsg(4326)
    transform = Transformer.from_crs(p_latlon, scene_crs)
    image_x, image_y = transform.transform(image_point.lat, image_point.lon)
    #
    # step 2: find the row and column of the image point
    #
    image_col, image_row = ~full_affine * (image_x, image_y)
    image_col, image_row = int(image_col), int(image_row)
    #
    # step 3 find the top, bottom, left and right rows and columns
    # given the specified offsets
    #
    col_left, col_right = (image_col + offsets.west, image_col + 
                           offsets.east)
    row_bot, row_top = image_row + offsets.south, image_row + offsets.north
    row_max, col_max = scene_ds.shape
    #
    # step 4: sanity check to make sure we haven't gone outside the image
    #
    if (col_left < 0 or col_right > (col_max -1) or
         row_top < 0 or row_bot > (row_max -1)):
        raise ValueError((f"bounds error with "
                          f"{(col_left, col_right, row_bot, row_top)=}"
                          f"\n{scene_ds.shape=}"))
    #
    # step 5: find the x,y corners of the bounding box
    #
    ul_x, ul_y = full_affine * (col_left, row_top)
    lr_x, lr_y = full_affine * (col_right, row_bot)
    #
    # step 6 create a new instance of the Bounding_box object and return it
    #
    bounds = Bounding_box(xmin=ul_x,ymin=lr_y,xmax=lr_x,ymax=ul_y)
    return bounds
```

(landsat_goes_find_bounds)=
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

### Read the image with satpy

```{code-cell} ipython3
from satpy import Scene
goes_2023 = Scene(reader= "abi_l2_nc", filenames = list([str(full_path)]))
```

### Get the veggie band (nir)

```{code-cell} ipython3
goes_2023.load(['C03'])
```

```{code-cell} ipython3
c3 = goes_2023['C03']
cartopy_crs = c3.area.to_cartopy_crs()
original_extent = cartopy_crs.bounds
goes_crs = pyproj.CRS(cartopy_crs)
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

(crs_bug)=
### Bug! copied the wrong CRS

need the clipped crs, not the full scene.  The bug was in the next line below

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

##  Verdict: still not a match 

With the bug fixed we've got the correct area, but the landsat image is 30 km x 24 km and the cropped GOES image is
only 16 km x 18 km.  In the next notebook: {ref}`week8:goes_landsat_rio` we show why there's a
discrepancy.

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
