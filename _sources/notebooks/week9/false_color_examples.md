---
jupytext:
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

(week9:false_color_examples)=
# Landsat 8 false color examples

In the {ref}`week7:false_color` notebook we showed how to make a false color composite with Landsat 8 bands 5, 4, 3 mapped to 
red, blue and green (color infrared)

In this notebook we move that code into a function called `make_false_color`, and show a Vancouver scene with some different band combinations

Still to be done -- including the full cloud/water/missing data mask in the false color image

```{code-cell} ipython3
import xarray
import rioxarray
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from skimage import exposure, img_as_ubyte
from IPython.display import Image
from pathlib import Path
#from false_color import make_false_color
```

## Understanding Landsat band location

The figure below shows average reflectances for various surface types. Compare some of thse
reflectance values with the landsat band locations in microns

1) coastal aerosol: 0.44
2) blue: 0.47
3) green: 0.55
4) red:  0.65
5) near-ir:  0.86
6) swir1  1.6
7) swir2: 2.2

+++

```{figure} figures/hou_reflectance.png
:name: fig:reflectance_spectra
:width: 80%

Reflectance spectra
```

+++

## Landsat bands by surface type

+++

```{figure} figures/landsat8_bands.png
:name: landsat_8_bands![landsat8_bands.png](attachment:9454ecea-8cba-488a-87ec-110fb2b5d57f.png)
:width: 80%

Landsat 8 band wavelengths
```

+++

## Landsat false color combinations

+++

```{figure} figures/arc_gis_bands.png
:width: 80%
:name: landsat_8_bands


```

+++

### Specific examples

- see [this website](https://www.nv5geospatialsoftware.com/Learn/Blogs/Blog-Details/the-many-band-combinations-of-landsat-8) for images that demonstrate the combinations
- see [this goes2go demo](https://blaylockbk.github.io/goes2go/_build/html/user_guide/notebooks/DEMO_rgb_recipes.html) for mulitple GOES band combinations

+++

## Make a false color landsat image

Under construction while I figure out fmask clipping

```{code-cell} ipython3
:user_expressions: []

bands={'B01':'Coastal_Aerosol',
        'B02':'Blue',
        'B03':'Green',
        'B04':'Red',
        'B05':'NIR',
        'B06':'SWIR1',
        'B07':'SWIR2',
        'B09':'Cirrus',
        'B10':'TIRS1',
        'B11':'TIRS2'}
```

```{code-cell} ipython3
data_dir = Path().home() / 'repos/a301/satdata/landsat'
all_tifs = list(data_dir.glob('**/week4*clipped_*.tif'))
scene_dict = {}
for key,bandname in bands.items():
    band_tif = None
    for the_tif in all_tifs:
        if str(the_tif).find(bandname) > -1:
            print(f"reading {key}:{the_tif}")
            scene_dict[key] = rioxarray.open_rasterio(the_tif, mask_and_scale=True)
            continue
   
    
```

### Create an xarray dataset from the band dictionary

```{code-cell} ipython3
ds_allbands = xarray.Dataset(data_vars=scene_dict,
               coords=scene_dict['B02'].coords,attrs=scene_dict['B02'].attrs)
ds_allbands
```

## To be done

make fully masked false color image

```{code-cell} ipython3
def make_false_color(the_ds, band_names):
    """
    given a landsat dataset created by get_landsat_datascene, return
    a histogram-equalized false color image with rgb mapped
    to the bands in the order they appear in the list band_names

    example usage:

    landsat_654 = make_false_color(the_ds,['B06','B05','B04'])

    Parameters
    ----------

    the_ds: xarray.DataSet
       output og get_landsat_datascene -- must contain at least 3 bands and Fmask
    band_names: list[str]
       list of strings with the names of the bands to be mapped to red, green and blue
    
```
