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

(sec:vancartopy)=
# Mapping Vancouver with cartopy

+++

**This cell sets up the datum and the LAEA projection, with the tangent point at the North Pole and the central meridian at -90 degrees west of Greenwich**

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

In {ref}`week8:output_bounds` we wrote the 

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

```{code-cell} ipython3
:trusted: true

goes_bounds
```

```{code-cell} ipython3
:trusted: true

bbox_keys = [('ll_lon','ur_lon','ur_lon','ll_lon','ll_lon'),
                ('ll_lat','ll_lat','ur_lat','ur_lat','ll_lat')]
```

```{code-cell} ipython3
:trusted: true

lons, lats = bbox_keys
goes_lons_coords = [goes_bounds[key] for key in lons]
goes_lats_coords = [goes_bounds[key] for key in lats]
ls_lons_coords = [goes_bounds[key] for key in lons]
ls_lats_coords = [landsat_bounds[key] for key in lats]
```

```{code-cell} ipython3
:trusted: true

# silence geojson warnings
import warnings
warnings.filterwarnings("ignore")
projection = ccrs.PlateCarree()
fig, ax = plt.subplots(1, 1, figsize=(6, 6), subplot_kw={"projection": projection})
#
# set the plot extent to be bigger than geh bounding box
#
xmin, xmax = -123.6,-123.
ymin, ymax = 49,49.6
extent = [xmin,xmax,ymin,ymax]
ax.set_extent(extent)
ax.gridlines(linewidth=2)
ax.plot(goes_lons_coords,goes_lats_coords,'r',label='goes')
ax.plot(ls_lons_coords,ls_lats_coords,'g',label='landsat')
ax.add_feature(cartopy.feature.GSHHSFeature(scale="auto", levels=[1, 2, 3]))
ax.legend(loc='best');
```

## Redo in GOES coordinates

```{code-cell} ipython3
:trusted: true

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
save_dir = Path.home() / "repos/a301/satdata/goes" 
full_path = save_dir / the_path
goesC = xr.open_dataset(full_path,mode = 'r',mask_and_scale = True)
c3 = goesC.metpy.parse_cf('CMI_C03')
cartopy_crs = c3.metpy.cartopy_crs
```

```{code-cell} ipython3
:trusted: true

cartopy_crs.globe.semiminor_axis
```

```{code-cell} ipython3
:trusted: true

goesC.goes_imager_projection.semi_minor_axis
```

```{code-cell} ipython3
:trusted: true


```

## Construct the cartopy crs

Take the falues from the pyproj.CRS goes_crs we just read in.
Follow [goes2go FieldOfViewAccessor](https://github.com/blaylockbk/goes2go/blob/main/goes2go/accessors.py#L90)

```{code-cell} ipython3
:trusted: true

goes_coeffs = goes_crs.to_dict()
goes_coeffs
```

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

```{code-cell} ipython3
:trusted: true

globe=ccrs.Globe(ellipse=None, **globe_kwargs)
cartopy_crs = ccrs.Geostationary(**crs_kwargs,globe=globe)
```

```{code-cell} ipython3
:trusted: true


```

```{code-cell} ipython3
:trusted: true

latlon_crs = pyproj.CRS.from_epsg(4326)
transformer = pyproj.Transformer.from_crs(latlon_crs,goes_crs,always_xy =True)
```

```{code-cell} ipython3
:trusted: true

goes_x, goes_y = transformer.transform(goes_lons_coords, goes_lats_coords)
minx, miny = float(np.min(goes_x)), float(np.min(goes_y))
maxx, maxy = float(np.max(goes_x)), float(np.max(goes_y))
```

```{code-cell} ipython3
:trusted: true

# silence geojson warnings
import warnings
warnings.filterwarnings("ignore")
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

```{code-cell} ipython3
:trusted: true

cartopy_crs.proj4_params
```

```{code-cell} ipython3
:trusted: true

dir(cartopy_crs.globe)
```

```{code-cell} ipython3
:trusted: true

cartopy_globe = cartopy_crs.proj4_params
cartopy_globe
```

```{code-cell} ipython3
:trusted: true

cartopy_test = ccrs.CRS(**cartopy_globe)
```

```{code-cell} ipython3
:trusted: true


```
