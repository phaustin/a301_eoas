---
jupytext:
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

(assign7_solution)=
# Assign7 Classification problem -- solution

- Make a jupyter notebook that reproduces the false color examples
  in{ref}`week10:false_color_examples` for your scene (you'll need to rerun  {ref}`week4:clip_bands` version 3 to get the clipped fmask, and rerun {ref}`week2:hls` to download all of the HLS tifs for bands 1,2,3,4,5,6,7,9,10,11,fmask if you don't have them).
- Choose one band combination that looks interesting, and compare it with the land classification you created using {ref}`week9:land_classes` for your image with the same bounding box and pixel size -- comment on any similarities and differences you can find.  Is the classification accurate?

```{code-cell} ipython3
import xarray
import rioxarray
from matplotlib import pyplot as plt
import numpy as np
from skimage import exposure, img_as_ubyte
from IPython.display import Image
from pathlib import Path
from numpy.typing import NDArray
from rasterio.enums import Resampling
import seaborn as sns
```

## False color bands for Vancouver

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
        'B11':'TIRS2',
        'fmask':'fmask'}
```

### Read all bands into a dictionary

Use the `bands` dictionary to identify the band by its name (Blue, Green, etc)
and store it in `scene_dict`.  Masking fmask would convert it from 8 bit to float, so we
need to special-case the fmask file.

```{code-cell} ipython3
data_dir = Path().home() / 'repos/a301/satdata/landsat'
all_tifs = list(data_dir.glob('**/week10*clipped_*.tif'))
scene_dict = {}
for key,bandname in bands.items():
    band_tif = None
    for the_tif in all_tifs:
        if str(the_tif).find(bandname) > -1:
            print(f"reading {key}:{the_tif}")
            if key == 'fmask':
                scene_dict[key] = rioxarray.open_rasterio(the_tif)
            else:
                scene_dict[key] = rioxarray.open_rasterio(the_tif, mask_and_scale=True)
            continue
   
    
```

### Create an xarray dataset from the band dictionary

(make_dataset2)=
#### make_dataset function

```{code-cell} ipython3
from a301_extras.sat_lib import (make_dataset,
                                 make_bool_mask,
                                 make_false_color)
ds_allbands = make_dataset(scene_dict)
```

```{code-cell} ipython3
ds_allbands
```

### Make the mask

```{code-cell} ipython3
bool_image = make_bool_mask(scene_dict['fmask'])
plt.imshow(bool_image.squeeze())
```

## Urban swir-2, swir-1, red

concrete and bare soil have approximately constant reflectivities between 1.6 and 2.2 microns,
while vegetation reflects more in swir-1 than swir-2.  This combination distinguishes between
types of urban development.  Less contrast for turbid/fresh water.  See: [band764 detail](https://eos.com/make-an-analysis/shortwave-infrared/)

```{code-cell} ipython3
urban = make_false_color(ds_allbands, band_names=["B07","B06","B04"])
fig5, ax5 = plt.subplots(1,1,figsize=(6,9))
urban.plot.imshow(ax=ax5);
ax5.set(title="Urban 764");
```

## Read in the classification and resample

The land use/land classification process assigns a category between 0-11 for the following 9 categories
(they have combined former categories 3 and 6 in the the category 11 (rangeland).

$$
\begin{array}{|ll|}
\hline 0 & \text { No data } \\
\hline 1 & \text { Water } \\
\hline 2 & \text { Trees } \\
\hline 4 & \text { Flooded Vegetation }  \\
\hline 5 & \text { Crops }  \\
\hline 7 & \text { Built Area }  \\
\hline 8 & \text { Bare Ground }  \\
\hline 9 & \text { Snow/lce } \\
\hline 10 & \text { Clouds }  \\
\hline 11 & \text { Rangeland }  \\
\hline
\end{array}
$$

+++

### get the bounds from band7

```{code-cell} ipython3
the_tif = list(data_dir.glob('**/vancouver_2023/10U*2023*tif'))[0]
print(the_tif)
```

### get the classification file

```{code-cell} ipython3
band7 = ds_allbands['B07'].squeeze()
bounds = band7.rio.bounds()
land_class = rioxarray.open_rasterio(the_tif)
land_class = land_class.squeeze()
```

## resample to band 7 grid

```{code-cell} ipython3
matched_class = land_class.rio.reproject_match(band7,
                                                  resampling=Resampling.mode)
```

```{code-cell} ipython3
matched_class.plot.imshow();
```

```{code-cell} ipython3
matched_class.plot.hist()
```

## Discussion

The classifier appeaars to be doing a good job of distinguishing the concrete runways as built, and the
mowed grass around the runways as rangeland. for the YVR runways. It also picks out the UBC golf course as
rangeland, but seems to also classify some sandy areas as rangeland around Iona spit. Not sure what's going
on with the crop classification in Point Grey. Would need to look at
[sentinel msi bands](https://lpdaac.usgs.gov/data/get-started-data/collection-overview/missions/harmonized-landsat-sentinel-2-hls-overview/#hls-spectral-bands) which are used to develop the classifier to see if they
are making some other kind of distinction in their bands 5-7 which landsat doesn't have

```{code-cell} ipython3
hit_built = matched_class.data == 7
hit_range = matched_class.data ==11
band6 = ds_allbands['B06'].squeeze()
band4 = ds_allbands['B04'].squeeze()
```

```{code-cell} ipython3
band7.shape
```

```{code-cell} ipython3
band7_built = band7.data[hit_built]
band6_built = band6.data[hit_built]
band4_built = band4.data[hit_built]
band7_range = band7.data[hit_range]
band6_range = band6.data[hit_range]
band4_range = band4.data[hit_range]
```

### Jointplot for built pixels bands 6,7

```{code-cell} ipython3
fig = sns.jointplot(
    x=band6_built,
    y=band7_built,
    kind="hex",
    xlim=(0.08, 0.3),
    ylim=(0.0, 0.24),
    color="#4CB391",
    gridsize=100,
)
fig.set_axis_labels("band 6 built", "band 7 built");
```

### Joint plot for range pixels, bands 6 and 7

```{code-cell} ipython3
fig = sns.jointplot(
    x=band6_range,
    y=band7_range,
    kind="hex",
    xlim=(0.08, 0.3),
    ylim=(0.0, 0.24),
    color="#4CB391",
    gridsize=100,
)
fig.set_axis_labels("band 6 range", "band 7 range");
```

### Jointplot for built pixels bands 4,7

```{code-cell} ipython3
fig = sns.jointplot(
    x=band4_built,
    y=band7_built,
    kind="hex",
    xlim=(0.0, 0.15),
    ylim=(0.0, 0.24),
    color="#4CB391",
    gridsize=100,
)
fig.set_axis_labels("band 4 range", "band 7 range");
```

### Joint plot for range pixels bands 4, 7

```{code-cell} ipython3
fig = sns.jointplot(
    x=band4_range,
    y=band7_range,
    kind="hex",
    xlim=(0.0, 0.15),
    ylim=(0.0, 0.24),
    color="#4CB391",
    gridsize=100,
)
fig.set_axis_labels("band 4 range", "band 7 range");
```

```{code-cell} ipython3

```
