---
jupytext:
  cell_metadata_filter: all
  formats: ipynb,md:myst
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

(sec:bacartopy)=
# Cartopy mapping Buenos Aires

In order to run this notebook go to [the download folder](https://drive.google.com/drive/folders/1-Ja2wVKVIjkZb7Gx_rfc14J_aBYiknuw) and get

- week5/cartopy_mapping_buenos_aires.ipynb
- week5/a301_lib.py
- buenos_aires/*B02.tif

the band2 (blue) tif needs to be in `~/repos/a301/satdata/landsat/buenos_aires/.`

## Introduction

This notebook shows how to turn a Landsat Zone North UTM crs into a Zone South crs so that we can use cartopy.  Basically, all we need to do is to add a "false northing" of 10,000,000 meters to the upper left corner of the raster image, as it is defined in the affine transform that is stored in the geotiff metadata.  Once we have the Zone 21S transform, we can use it
to find the image extent that cartopy needs to plot the raster along with the coastline.

## Example

Use Buenos Aires as a specifc test.

Google says Buenos Aires in in UTM zone 21 South, with an epgs code of 32721

lat = -34.6037 deg S
lon = -58.3816 deg W

We want to put an image on a map, with this Landsat scene 

:::{figure} figures/buenos_aires.jpg
:name: ba_browse
:scale: 50

Landsat browse image of Buenos Aires
:::

+++

## Import libraries

+++

The file `a301_lib.py` is a new python module containing course code.
For week 5 it  contains `rowcol2latlon` from {ref}`week5:rowcol2latlon` and
`make_pal` from {ref}`week5:add_palette`.  We use the `make_pal` function below

```{code-cell} ipython3
:trusted: true

from a301_lib import make_pal
```

```{code-cell} ipython3
:trusted: true

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy
from pathlib import Path
import rioxarray
import affine

from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
import warnings
```

silence weird cartopy geojson warnings  (doesn't seem to help)

```{code-cell} ipython3
:trusted: true

warnings.filterwarnings("ignore")
```

## Set up the UTM CRS for Zone 21S

+++

Here is the center of buenos aires

```{code-cell} ipython3
:trusted: true

ba_lat = -34.6037 # deg N
ba_lon = -58.3816 # deg E
```

### The epsg code for Zone 21S is 32721

```{code-cell} ipython3
:trusted: true

geodetic = ccrs.Geodetic()
the_crsS = ccrs.epsg(32721)
ba_x, ba_yS = the_crsS.transform_point(ba_lon, ba_lat, geodetic)
print(f"{ba_x=:.0f}, {ba_yS=:.0f}")
```

## Repeat this for UTM Zone 21N

This has an epsg code of 32621

```{code-cell} ipython3
:trusted: true

the_crsN = ccrs.epsg(32621)
ba_x, ba_yN = the_crsN.transform_point(ba_lon, ba_lat, geodetic)
print(f"{ba_x=:.0f}, {ba_yN=:.0f}")
```

## False northing

Zone 21 North has negative y values south of the equator.   To eliminate this, someone decided to create a new zone,
Zone 21 South, by adding 10,000,000 meters to every y value south of the equator, the "false northing".

You can see this when you subtract the y for Buenos Aires in 201N from the y in 21S:

```{code-cell} ipython3
:trusted: true

print(f"false northing: {(ba_yS - ba_yN)=:.0f} meters")
```

### Zone 21S ends at 80 deg S

see the [epsg website](https://epsg.io/32721)

What is the most southern y point in Zone 21N  coordinates?

Note that the x coords are identical in both projections, but

sp_yS - sp_yN = 10,000,000

```{code-cell} ipython3
:trusted: true

sp_lon = -57. # zone 21 central meridian 57 deg W
sp_lat = -80  #farthest south point
sp_x, sp_yN = the_crsN.transform_point(sp_lon, sp_lat, geodetic)
print(f"{(sp_x,sp_yN)=}")
```

### How about Zone 21S

```{code-cell} ipython3
:trusted: true

sp_x, sp_yS = the_crsS.transform_point(sp_lon, sp_lat, geodetic)
print(f"{(sp_x,sp_yS)=}")
print(f"{(sp_yS - sp_yN)=}")
```

### How about the equator?

```{code-cell} ipython3
:trusted: true

eq_lon = -57. # zone 21 central meridian 57 deg W
eq_lat = 0  #farthest north point
eq_x, eq_yS = the_crsS.transform_point(eq_lon, eq_lat, geodetic)
print(f"{(eq_x,eq_yS)=}")
eq_x, eq_yN = the_crsN.transform_point(eq_lon, eq_lat, geodetic)
print(f"{(eq_x,eq_yN)=}")
```

So there's a 10 million meter discontinuity when you change zones at the equator.  NASA
decided this was a problem, and did away with the false northing, permitting negative y values for Zone 21N.  Cartopy disagreed, and
requires positive y values in each utm zone.

+++

## Draw a Buenos Aires map with the_CRSS south CRS

follow {ref}`sec:vancartopy`

make it 50 x 50 km with BA in the center

```{code-cell} ipython3
:trusted: true

#
# pick a bounding box in map coordinates
# set the extent for 25 km in each direction from BA
#
half_width = 25*1.e3  # 50,000 m
xleft, xright = ba_x - half_width, ba_x + half_width
ybot, ytop =  ba_yS - half_width, ba_yS + half_width
extent = [xleft, xright, ybot, ytop]
```

```{code-cell} ipython3
:trusted: true

fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw={"projection": the_crsS})
ax.set_extent(extent, the_crsS)
ax.plot(ba_x, ba_yS, "ko", markersize=10)
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="auto", edgecolor = "red", levels=[1, 2, 3]));
```

## Now overlay a landsat image

We need to take the affine transform from the landsat image and change it from zone 21N to 21S.  To do that
we need to rewrite the upper-left corner Y value by adding 10,000,000 meters to it.

```{code-cell} ipython3
:trusted: true

data_dir = Path().home() / 'repos/a301/satdata/landsat/buenos_aires'
the_tif = list(data_dir.glob('**/HLS.L30*B02.tif'))[0]
print(the_tif)
```

### Grab the affine transform

Recall from {ref}`week3:map_landsat` that the [affine transform](https://www.perrygeo.com/python-affine-transforms.html) handles
the conversion from x, y to row, column and back.  The transform stored in the landsat images is written with Z 21N.  We need
to turn that transform into 21S by add 10,000,000 m to the y value of the upper left corner.

The layout for the transform is:

```
a = width of a pixel
b = row rotation (typically zero)
c = x-coordinate of the upper-left corner of the upper-left pixel
d = column rotation (typically zero)
e = height of a pixel (typically negative)
f = y-coordinate of the of the upper-left corner of the upper-left pixel
```
So f is the value we need to change.

First grab the blue band for the scene

```{code-cell} ipython3
:trusted: true

hls_band = rioxarray.open_rasterio(the_tif,masked=True)
hls_band = hls_band.squeeze()
hls_band = hls_band*hls_band.scale_factor
```

#### Now get the transform for Zone 21N

```{code-cell} ipython3
:trusted: true

n_tf = hls_band.rio.transform()
print(f"{n_tf.f=}")
```

```{code-cell} ipython3
:trusted: true

hls_band.plot.hist();
```

### Change the transform by adding the false northing

We just need to add the northing to the f component and put the pieces
back together.

```{code-cell} ipython3
:trusted: true

northing = 1.e7  #10 million m
s_tf = affine.Affine(n_tf.a, n_tf.b, n_tf.c, n_tf.d, n_tf.e, n_tf.f + northing)
s_tf
```

### Use the modified transform to get the extent for cartopy in the 21S crs

+++

Find the corners like we did in {ref}`bounding_box`

```{code-cell} ipython3
:trusted: true

nrows, ncols = hls_band.rio.shape
```

```{code-cell} ipython3
:trusted: true

ur_x, ur_y = s_tf*(0,0)
lr_x, lr_y = s_tf*(nrows,ncols)
```

```{code-cell} ipython3
:trusted: true

image_extent = [ur_x, lr_x, lr_y, ur_y]
```

## Use the new make_pal

```{code-cell} ipython3
:trusted: true

help(make_pal)
```

```{code-cell} ipython3
:trusted: true

vmin = 0.0
vmax = 0.1
pal_dict = make_pal(vmin=vmin,vmax=vmax)
pal_dict
```

```{code-cell} ipython3
:trusted: true

fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw={"projection": the_crsS})
cs = ax.imshow(
    hls_band.data,
    origin="upper",
    norm = pal_dict['norm'],
    cmap = pal_dict['cmap'],
    extent=image_extent,
    transform=the_crsS
)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="auto", levels=[1, 2, 3],edgecolor='red'))
fig.colorbar(cs,extend='both');
```

```{code-cell} ipython3
:trusted: true


```
