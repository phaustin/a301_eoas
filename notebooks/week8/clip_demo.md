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

(week9:stanleypark)=
# Clipping issues: What happened to Stanley Park?
 In the {ref}`week8:goes_landsat_rio` notebook we wound up with a cropped image
 that shaved off the western and eastern sides of our specified bounding box.
 As explained in that notebook, that was because we selected the bounding box corners in lon/lat coords (or equivalently, UTM), but executed `rioxarray.clip_box` in geostationary coordinates.  In this notebook I make two plots, one showing the bounding box in lon/lat coordinates, and one showing it in geostationary coordinates.  The second plot shows that, because lines of constant longitude are not the same as lines of constant geostationary x values, the clipped bounds differ significantly in the two scenes.

```{code-cell} ipython3
:trusted: true

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy
import json
import pyproj
from pathlib import Path
import xarray as xr
from goes2go.data import goes_nearesttime
import numpy as np
```

## Read in bounds for landsat and goes

I've modified {ref}`week8:output_bounds` to save the pyproj geostationary crs
and the lon/lat bounding boxes out to json files.  Read these in
so we can start with the same coordinates.

```{code-cell} ipython3
:trusted: true

with open("goes_crs.json","r") as infile:
    text_crs = infile.read()
    goes_crs = pyproj.CRS(text_crs)
with open("goes_bounds.json","r") as infile:
    goes_bounds = json.load(infile)
with open("landsat_bounds.json","r") as infile:
    landsat_bounds = json.load(infile)
```

```{code-cell} ipython3
:trusted: true

goes_bounds
```

### Make a counterclockwise set of coordinates

We want to show the bounding box on a map in the two coordinate systems.
The x,y keys below start in the ll corner and go around the bounding box counter clockwise. There are 5 values so we return to where we started.

```{code-cell} ipython3
:trusted: true

bbox_keys = [('ll_lon','ur_lon','ur_lon','ll_lon','ll_lon'),
                ('ll_lat','ll_lat','ur_lat','ur_lat','ll_lat')]
```

### Find the x,y coorinates for each crs

Use these keys in a list comprehension to
group the x and y  values together so we can use pyproj.Transformer

```{code-cell} ipython3
:trusted: true

lons, lats = bbox_keys
goes_lons_coords = [goes_bounds[key] for key in lons]
goes_lats_coords = [goes_bounds[key] for key in lats]
ls_lons_coords = [landsat_bounds[key] for key in lons]
ls_lats_coords = [landsat_bounds[key] for key in lats]
```

## First Plot: the bounding boxes in lon/lat coords

Note that in the lon/lat projection the GOES boundary box is actually
bigger than the landsat bounding box and includes Stanley Park on the east
and Keats Island on the West

```{code-cell} ipython3
:trusted: true

# silence geojson warnings
import warnings
warnings.filterwarnings("ignore")
projection = ccrs.PlateCarree()
fig, ax = plt.subplots(1, 1, figsize=(6, 6), 
                       subplot_kw={"projection": projection})
#
# set the plot extent to be bigger than geh bounding box
#
xmin, xmax = -123.6,-123.  #longitude degrees east
ymin, ymax = 49,49.6  #latitude degrees north
extent = [xmin,xmax,ymin,ymax]
ax.set_extent(extent)
ax.gridlines(linewidth=2)
ax.plot(goes_lons_coords,goes_lats_coords,'r',label='goes')
ax.plot(ls_lons_coords,ls_lats_coords,'g',label='landsat')
ax.add_feature(cartopy.feature.GSHHSFeature(scale="auto", levels=[1, 2, 3]))
ax.legend(loc='best');
```

## Redo in geostationary coordinates

Now try this again, but in a coordinate system where the vertical
and horizontal lines are geostationary x and geostationary y instead
of longitude and latitude.

+++

### Construct the cartopy crs for GOES

Remember that cartopy is much older than pyproj, and it has its own
way of constructing a geostationary coordinate system, so we can't use
a format like wkt (well known text).

I'll take the values from the `pyproj.CRS goes_crs` we read in from `goes_crs.json` above 
and rename them so they will be accepted by the cartopy.CRS constructor.

Follow [goes2go FieldOfViewAccessor](https://github.com/blaylockbk/goes2go/blob/main/goes2go/accessors.py#L90).crs

```{code-cell} ipython3
:trusted: true

#
# here's what we have from the json file
#
goes_coeffs = goes_crs.to_dict()
goes_coeffs
```

### move the pyproj params over to cartopy

Note that pyproj ignores `semiminor_axis`, which I have to
fill in from reading a goes image and dumping its metadata.  This
might explain why the x,y coordinates are slightly different from
goes2go and satpy.  The next cell does the translation from pyproj arguments
to cartopy arguments.

```{code-cell} ipython3
:trusted: true

#
# had to copy semiminor_axis from a goes2go dataset
# it's not included in the pyproj CRS
#
globe_kwargs = dict(semimajor_axis = goes_coeffs['a'],
                    semiminor_axis=6356752.3141,
                    inverse_flattening = goes_coeffs['rf'])
crs_kwargs = dict(central_longitude = goes_coeffs['lon_0'],
                  satellite_height = goes_coeffs['h'],
                  sweep_axis = 'x')
```

### Call the cartopy.CRS constructors

cartopy uses the workd `globe` for what we've been calling the `datum`

```{code-cell} ipython3
:trusted: true

globe=ccrs.Globe(ellipse=None, **globe_kwargs)
cartopy_crs = ccrs.Geostationary(**crs_kwargs,globe=globe)
```

### Transform the boundary coords

Transform the lat/lon boundary into geostationary x,y from [epsg 4326](https://epsg.io/4326)

```{code-cell} ipython3
:trusted: true

# epsg 4326 is simple geodetic latlon
# we need the always_xy = True because the 4326 default order is lat,lon for some reason
# unlike the other coordinate systems, and that's an accident waiting to happen
latlon_crs = pyproj.CRS.from_epsg(4326)
transformer = pyproj.Transformer.from_crs(latlon_crs,goes_crs,always_xy =True)
goes_x, goes_y = transformer.transform(goes_lons_coords, goes_lats_coords)
```

## Second plot: the bounding box in geostationary coordinates

```{code-cell} ipython3
:trusted: true

projection = cartopy_crs
fig, ax = plt.subplots(1, 1, figsize=(6, 6), 
                       subplot_kw={"projection": projection})
ax.gridlines(linewidth=2)
ax.plot(goes_x,goes_y,'g',label='goes')
ll_x,ll_y = goes_x[0], goes_y[0]
ur_x, ur_y = goes_x[2], goes_y[2]
ax.plot(ll_x,ll_y,'ro',markersize=15,label = 'lower_left')
ax.plot(ur_x,ur_y,'bo',markersize=15,label = 'upper_right')
ax.plot((ll_x,ll_x),(ll_y,ur_y),'r-')
ax.plot((ur_x,ur_x),(ll_y,ur_y),'b-')
ax.add_feature(cartopy.feature.GSHHSFeature(scale="auto", levels=[1, 2, 3]))
fig.legend(bbox_to_anchor=(0.5, 0.25, 0.5, 0.5));
```

## Summary

Compare with {ref}`week8:resampled_goes` to see why the Stanly Park and Keats Island get clipped.
From the cell above it's clear that the lower left and upper right corners of
the bounding box do not give the expected west and east boundaries, which are
created along lines of constant longitude, not lines of constant geostationary.x.  

Bottom line, if we want to clip along UTM Zone10 or lon/lat boundaries, we
have to resample the goes image into that coordinate system, then clip.  Alternatively, we need to make the bounding box big enough to get the lower left and upper right corners to span the desired longitude range in geostationary coordinates.

```{code-cell} ipython3
:trusted: true


```
