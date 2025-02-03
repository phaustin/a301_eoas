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

(week5:rowcol2latlon)=
# Getting lat,lon from row, column

- Download rowcol2latlon.ipynb from the [week5 folder](https://drive.google.com/drive/folders/1-Ja2wVKVIjkZb7Gx_rfc14J_aBYiknuw?usp=sharing)


## Introduction

The function `rowcol2latlon` defined below takes the name of a tiffile and a row,column pair
for the raster and returns the latitude and longitude of that pixel.  It uses the
[pyproj.CRS](https://pyproj4.github.io/pyproj/stable/api/crs/crs.html#id2) object to hold the coordinate reference system and the [pyproj.Transformer](https://pyproj4.github.io/pyproj/stable/api/transformer.html#pyproj.transformer.Transformer)
object to do
the transform.

```{code-cell} ipython3
from pathlib import Path
from pyproj import Transformer, CRS
import rioxarray
```

```{code-cell} ipython3
data_dir = Path().home() / 'repos/a301/satdata/landsat'
tif_filename = data_dir / 'vancouver' / f"week4_clipped_TIRS2.tif"
print(f"{tif_filename=}")
```

## transforming lat/lon to utm


Here is how we did this using the code from - {ref}`week3:image_zoom`.


```{code-cell} ipython3
# zone 10 UTM
proj_code = 32610
#
# we want to go from x,y in utm zone 10 to lat,lon
# first, get x,y from lat, lon, the show you can reverse that
#
p_utm = CRS.from_epsg(proj_code)
p_latlon = CRS.from_epsg(4326)
transform = Transformer.from_crs(p_latlon, p_utm)
ubc_lon = -123.2460 
ubc_lat = 49.2606
ubc_x, ubc_y = transform.transform(ubc_lat, ubc_lon)
print(f"{ubc_x=:.2f} m, {ubc_y:.2f}")
```

## doing the inverse: utm to lat/lon

To go the other direction, just reverse the parameters in the Transformer call

```{code-cell} ipython3
# zone 10 UTM
proj_code = 32610
#
# we want to go from x,y in utm zone 10 to lat,lon
# first, get x,y from lat, lon, the show you can reverse that
#
p_utm = CRS.from_epsg(proj_code)
p_latlon = CRS.from_epsg(4326)
transform = Transformer.from_crs(p_latlon, p_utm)
ubc_lon = -123.2460 
ubc_lat = 49.2606
ubc_x, ubc_y = transform.transform(ubc_lat, ubc_lon)
print(f"{ubc_x=:.2f} m, {ubc_y:.2f}")
```

### Now do x,y to lat/lon

Just reverse the arguments to the Transformer

```{code-cell} ipython3
transform = Transformer.from_crs(p_utm, p_latlon)
ubc_lat, ubc_lon = transform.transform(ubc_x, ubc_y) 
print(f"{ubc_lon=:.3f} m, {ubc_lat:.3f}")
```

### wrap this in a function

```{code-cell} ipython3
def rowcol2latlon(tiffile,row,col):
    """
    return the latitude and longitude of a row and column in a geotif

    Parameters
    ----------

    tiffile: Path object
        path to a clipped tiffile
    row: float
       row of the pixel
    col: float
       column of the pixel

    Returns
    -------

    (lon, lat):  (float, float)
       longitude (deg east) and latitude (deg north) on
       a WGS84 datum
    
    """
    has_file = tiffile.exists()
    if not has_file:
        raise IOError(f"can't find {filename}, something went wrong above") 
    the_band = rioxarray.open_rasterio(tif_filename,masked=True)
    epsg_code = the_band.rio.crs.to_epsg()
    p_utm = CRS.from_epsg(epsg_code)
    p_latlon = CRS.from_epsg(4326)
    affine_transform = the_band.rio.transform()
    x, y = affine_transform*(row, col)
    crs_transform = Transformer.from_crs(p_utm, p_latlon)
    lat, lon = transform.transform(x,y) 
    return (lon, lat)

lon, lat = rowcol2latlon(tif_filename,0,0)
print(f"{lon=:.1f} deg,{lat=:.1f} deg")
```

## Two gotchas to watch out for

+++

- Don't confuse the pyproj transformer.Transform with
  the affine transform -- two completely different things
- pyproj has an alternate way of doing coordinate transforms using
  a Proj object and a transform (lower case t) method.  These are
  in lots of examples on the web, but have been superseded by
  Transformer.transform
  

```{code-cell} ipython3

```
