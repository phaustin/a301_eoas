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

(week4:clip_bands)=
# Clipping multiple bands-- v0.2


2025/Feb/27: Fixed a problem where the datatype of the clipped arrays was changed from float32 to int16 when creating geotiffs.  See {ref}`clip:create_arrays` for the new code.

## Introduction

We are going to need to look at bands 2, 3, 4, 5, 9, 10 and 11.  This notebook uses the clipped band we wrote in
{ref}`week3:image_zoom` to get the clipping box, then reads in each of these bands, clips to the same box
and writes them out to new smaller geotifs.

- Download clip_bands.ipynb from the [week4 folder](https://drive.google.com/drive/folders/1-Ja2wVKVIjkZb7Gx_rfc14J_aBYiknuw?usp=sharing)
- You'll also need to copy the 5 NASA hls tif files in the [vancouver](https://drive.google.com/drive/folders/1UwTc4MnneI2eZ6rHqKFzF4YdRRbQi4sS?usp=sharing) folder into a new folder on your drive called `~/repos/a301/satdata/landsat/vancouver`

```{code-cell} ipython3
import copy
import pprint
from pathlib import Path
from osgeo import gdal
import json

import cartopy
import numpy as np
import numpy.random
import rasterio
from affine import Affine
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from pyproj import CRS, Transformer
import rioxarray
import xarray as xr
from cartopy import crs as ccrs
from a301_lib import make_pal
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

## Examine the geotif metadata

### Using gdalinfo from the terminal

It turns out that rioxarray only copies part of the metadata into the `DataArray`.  To get all the metadata, we can use the underlying [gdal module](https://gdal.org/en/stable/programs/gdalinfo.html). Do the following:

- open a terminal
- cd to the folder holding the geotiff
- type `gdalinfo your_tif_name_here.tif`

For a shorter summary, you can use the `rasterio` command line tool `rio`:

- `rio info you_tif_name_here.tif`

### Using the python gdal api

We can also do that from inside python.  To get all the information for the first tif, do:

```{code-cell} ipython3
info = gdal.Info(the_tifs[1], format='json')
info.keys()
```

### Dump all the metadata

You can print the  `info` dictionary to see the full gdal metadata dictionary.
Scanning through it, will see that the `metadata` key has two sub-keys:

```{code-cell} ipython3
print(f"{info['metadata'].keys()=}")
```

And looking at the first key shows all of the metadata that rioxarray transfers to the DataArray attributes.  these are the entries that we'll need to change for our clipped, scaled image.  We need to change `NCOLS, NROWS, ULX, ULY and scale_factor` when we write the clipped geotif.  Descriptions of each of the metadata items are in the [hls user guide](https://lpdaac.usgs.gov/documents/1007/HLS_User_Guide_V15_provisional.pdf)

```{code-cell} ipython3
print(f"{info['metadata'][''].keys()=}")
```

We want to check the `long_name` key in particular, to make sure we are looking at the right wavelength:

```{code-cell} ipython3
print(f"{info['metadata']['']['long_name']=}")
```

The exact wavelength range for each hls landsat band is given in the [spectral band table](https://lpdaac.usgs.gov/data/get-started-data/collection-overview/missions/harmonized-landsat-sentinel-2-hls-overview/#hls-spectral-bands)

+++

## Read the bands into a dictionary

We're ready to read all of the bands into a dictionary, keyed by the band `long_name`.  All the band names are listed in the
[spectral band table](https://lpdaac.usgs.gov/data/get-started-data/collection-overview/missions/harmonized-landsat-sentinel-2-hls-overview/#hls-spectral-bands). Note one complication -- the `unit` attribute is only present for brightness temperatures, not reflectivities.

Note on the next cell:

- Because we set `masked_and_scale=True`, all `-9999` values are changed to `np.nan` and the data is multiplied by the scale factor and converted from `int16` to `float32`

```{code-cell} ipython3
band_dict={}
for tif_path in the_tifs:
    #
    # skip fmask for now
    #
    if 'Fmask' in str(tif_path):
        continue
    hls_band = rioxarray.open_rasterio(tif_path,mask_and_scale=True)
    band_name = hls_band.long_name
    print(f"{band_name=}")
    band_dict[band_name] = hls_band
    if 'unit' in hls_band.attrs:
        print(f"{hls_band.unit=}")
```

### check the dtype of the data and missing data

```{code-cell} ipython3
band_dict['Green'].dtype, band_dict['Green'].rio.nodata
```

## Read the clipped week3 band 5 bounding box

Next we want to get the affine transform from week 3 clipped band file, so we can set the same bounding box for all tifs

+++

(bounding_box)=
### Create the bounding box using the upper left and lower right corners

This should be identical to the bounding box we found in {ref}`zoom_landsat_array`, which was:

`bounding_box=(476100.0, 5447460.0, 488100.0, 5465460.0)`

We can get them using the clipped affine transform.  Again, we search for the file using wild cards.  We just want
the first file we find, which means we need convert the python generator returned by glob into a list we can index.

```{code-cell} ipython3
filename =  list(data_dir.glob('**/band5_clipped*'))[0]
print(filename)
clipped_5 = rioxarray.open_rasterio(filename,masked=True)
clipped_transform = clipped_5.rio.transform()
clipped_transform
```

```{code-cell} ipython3
band, nrows, ncols = clipped_5.shape
nrows, ncols
```

```{code-cell} ipython3
ul_x, ul_y = clipped_transform * (0, 0)
lr_x, lr_y = clipped_transform * (ncols, nrows)
bounding_box = (ul_x, lr_y, lr_x, ul_y)
print(f"{bounding_box=}")
```

### Get the pyproj crs to copy to output tif

We want the improved crs we wrote out in {ref}`week3:image_zoom` for the band5 clipped tif, since  it includes the epsg code

```{code-cell} ipython3
good_crs = clipped_5.rio.crs
print(f"{good_crs.to_epsg()=}")
```

(clip:create_arrays)=
## Create new clipped arrays

Fixed in version 0.2:  Just copying all the metadata from the original NASA files led to issues with missing data values and the ouput datatype for the data. To fix this, create the rioxarray DataArrays from scratch with
only those attributes that are consistent with the new mask_and_scaled array.
We'll add more attributes in {ref}`change_attrs` below. In particular note
that ULX, ULY, NROWS and NCOLS have not been updated from the original full scene.

```{code-cell} ipython3
def make_new_array(rio_da,crs=None):
    """
    transfer data into from rio_da into a fresh DataArray, copying only the selected metadata
    from rio_da.  This avoids copying old metadata from the original hls tif file

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
band_clipped = {}
for key, value in band_dict.items():
    the_array = value.rio.clip_box(*bounding_box)
    new_clipped = make_new_array(the_array,crs = good_crs)
    band_clipped[key]=new_clipped
```

```{code-cell} ipython3
var='TIRS1'
band_clipped[var].rio.nodata, band_clipped[var].attrs
```

## Check the brightness temperature in band 11

```{code-cell} ipython3
print(band_clipped[key].rio.nodata)
```

```{code-cell} ipython3
key = 'TIRS2'
fig, ax = plt.subplots(1,1)
band_clipped[key].plot.hist(ax = ax)
ax.set_title(f"band {key} ({band_dict[key].unit})")
```

## Write the clipped geotiffs

Put these into the vancouver folder.  We can copy code from {ref}`week3:write_clipped`

+++

(change_attrs)=
### change some attributes

We need to adjust some of the attributions for the new subscene.  To do this, copy the exiting attributes into
a dictionary and rewrite the parts you want to change, adding any extras.

```{code-cell} ipython3
band_clipped['Red'].dtype,band_clipped['Red'].rio.nodata
```

```{code-cell} ipython3
value.rio.set_nodata(np.float32(np.nan),inplace=True)
type(value.rio._nodata)
```

```{code-cell} ipython3
for key, value in band_clipped.items():
    new_attrs = copy.deepcopy(value.attrs)
    new_attrs['ULX']= ul_x
    new_attrs['ULY'] = ul_y
    band, nrows, ncols = value.shape
    new_attrs['NROWS'] = nrows
    new_attrs['NCOLS'] = ncols
    new_attrs['FillValue'] = np.nan
    new_attrs['history'] = "v0.2 -- written by the week4 clip_bands notebook"
    value.rio.update_attrs(new_attrs, inplace = True)
    #
    # update_attrs seems to destroy the rio.nodata attribute
    #
    value.rio.set_nodata(np.float32(np.nan),inplace=True);
```

#### check the attributes

```{code-cell} ipython3
value.attrs['history'],value.dtype,value.rio.nodata
```

### Write out the new geotiffs

```{code-cell} ipython3
band_clipped['Blue'][0,-1,-10:]
```

```{code-cell} ipython3
for key, value in band_clipped.items():
    band_name = value.long_name
    tif_filename = data_dir / 'vancouver' / f"week4_clipped_{band_name}.tif"
    #
    # remove the file if it already exists
    #
    if tif_filename.exists():
        tif_filename.unlink()
    value.rio.to_raster(tif_filename)
value = band_clipped['Blue']
print(value.data[0,-1,-10:])
print(f"{(value.dtype, value.rio.nodata,value.rio.crs.to_epsg())=}")
```

### read one back in to check

```{code-cell} ipython3
tif_filename = list(data_dir.glob("**/*week4*NIR.tif"))[0]
print(f"{tif_filename=}")
has_file = tif_filename.exists()
if not has_file:
    raise IOError(f"can't find {filename}, something went wrong above") 
small_band = rioxarray.open_rasterio(tif_filename,mask_and_scale=True)
print(f"{small_band.data[0,-1,-10:]=}")
small_band = small_band.squeeze()
band_name = small_band.long_name
print(f"{(band_name, small_band.dtype)=}")
fig, ax = plt.subplots(1,1, figsize=(6,6))
vmin, vmax = 0.,0.5
pal_dict = make_pal(vmin=vmin,vmax=vmax)
small_band.plot.imshow(ax=ax,
                    norm = pal_dict['norm'],
                    cmap = pal_dict['cmap'],
                    extend = "both")
ax.set_title(f"Landsat band {band_name}");
```

```{code-cell} ipython3
small_band.attrs['history']
```

#### note that we now have the correct epsg code

Because we used the pyproj `good_crs` in our raster write we've fixed the missing epsg code problem.

```{code-cell} ipython3
small_band.rio.crs.to_epsg(), small_band.rio.nodata,small_band.dtype
```

#### Check the metadata

Write all the metadata out to a file for a detailed check

```{code-cell} ipython3
info = gdal.Info(tif_filename, format='json')
print(f"{tif_filename=}")
with open('dump.json','w') as fp:
    json.dump(info,fp,indent=4)
```

```{code-cell} ipython3

```
