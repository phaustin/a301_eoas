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

(week7:fmask)=
# Using fmask to mask water pixels


## Intoduction


- Download the `fmask.ipynb` notebook from week7 in our
[gdrive folder](https://drive.google.com/drive/folders/1-D6y9MlE8LZRLZg-qRCxPZSgar8kGjBT?usp=drive_link)

- Download the folder `downloads/vancouver/week7` containing the clipped tif files produced by v0.2 of {ref}`week4:clip_bands` and a new fmask file  `~/repos/a301/satdata/landsat/vancouver`



In {ref}`week7:false_color` we created false color images using 3 bands.  One problem with
those images is that half of the scene was water, which we aren't particularly interested
in.  In this notebook we use a mask file downloaded from NASA (`HLS.L30.T10UDV.2015165T190019.v2.0.Fmask.tif`) using {ref}`week2:hls` to remove all the water pixels.  It cleans up the joint histograms significantly.

## Read in the clipped image

Copy some code from {ref}`week7:false_color`

```{code-cell} ipython3
import xarray
import rioxarray
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from skimage import exposure, img_as_ubyte
from IPython.display import Image
from a301_lib import make_pal
```

### Add the fmask to the list

```{code-cell} ipython3
data_dir = Path().home() / 'repos/a301/satdata/landsat/vancouver'
blue = list(data_dir.glob('**/*Blue*tif'))[0]
red = list(data_dir.glob('**/*Red*tif'))[0]
green = list(data_dir.glob('**/*Green*tif'))[0]
nir =  list(data_dir.glob('**/*NIR*tif'))[0]
fmask =  list(data_dir.glob('**/*Fmask*tif'))[0]
band_dict = dict(zip(('red','green','nir','blue','fmask'),(red,green,nir,blue,fmask)))
```

```{code-cell} ipython3
xarray_dict={}
for key,filename in band_dict.items():
    print(key)
    xarray_dict[key] = rioxarray.open_rasterio(filename,mask_and_scale=True);
    xarray_dict[key] = xarray_dict[key].squeeze()
```

## Clip fmask to the same bounding box

Copy some code from {ref}`week4:clip_bands`

```{code-cell} ipython3
clipped_tif = xarray_dict['blue']
clipped_transform = clipped_tif.rio.transform()
nrows, ncols = clipped_tif.shape
ul_x, ul_y = clipped_transform * (0, 0)
lr_x, lr_y = clipped_transform * (ncols, nrows)
bounding_box = (ul_x, lr_y, lr_x, ul_y)
print(f"{bounding_box=}")
fmask = xarray_dict['fmask'].rio.clip_box(*bounding_box)
```

### fmask data

This scene has 6 unique fmask values

```{code-cell} ipython3
fmask.plot.hist(figsize=(6,6));
```

### fmask image

```{code-cell} ipython3
fmask.plot.imshow();
```

## decoding fmask values

So what is the meaning of these six numbers?  The values are given in the
[hls landsat user guide](https://lpdaac.usgs.gov/documents/1698/HLS_User_Guide_V2.pdf) on page 17

:::{figure} ./images/fmask_table.png
:name: fmask_table
:scale: 60

hls landsat fmask values
:::

+++

The full scene before clipping acually has 35 values:

```{code-cell} ipython3
len(np.unique(xarray_dict['fmask'].data))
```

Here's how to list the individual bit order for each number in the mask.  We need to convert the floating point values to unsigned, 8 bit integers (`uint8`)
and then unpack the 8 bits using the numpy function `unpackbits`

```{code-cell} ipython3
# var = xarray_dict['fmask'].data
var = fmask.data
vals = np.unique(var)
vals = vals.astype('uint8')
for item in vals:
    print(f"{item:03d}",np.unpackbits(item))
```

Comparing with the table, you should recognize that 96, 160, and 224 all have their
bit 5 (counting from the right) set to 1, indicating water.  The difference between the three is whether they have clean air (01 in bits 6,7), moderate aerosols (10) or high aerosols (11).

+++

## finding all water pixels

How do we find the water pixels for the clipped scene?  We want to find
all pixels in the mask with their bit 5 set to 1.  We can do that by
creating a mask with *only* the bit 5 set to 1, then doing a `bitwise_and` with
the masked values.  That will turn the water pixels into decimal 32 (2**5), and
all other pixels into 0, because only (1 and 1) is 1, and all other bit postions
with and to zero.

```{code-cell} ipython3
fifth_bit_on = 0b00100000
#
# construct an array of the right shape filled with
# the water bit
#
a_array = np.full(fmask.data.shape,fifth_bit_on)
#
# turn the fmask values into unsigned bytes
#
var_bytes = fmask.data.astype('uint8')
#
# do the bitwise_and to get a mask
#
water_mask = np.bitwise_and(var_bytes,a_array)
```

### plot the water_mask

As expected, water=32, everything else is 0.

```{code-cell} ipython3
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.imshow(water_mask)
ax2.hist(water_mask.flat);
```

### Inverting the water mask

Now that we know where the water is, we want to assign all those pixels
as np.nan, and all land pixels as 1.  We can do this using np.where. The
next cell assigns all the land pixels the value 1, and all other pixels
the value np.nan

```{code-cell} ipython3
land_mask = np.where(water_mask == 0,1,np.nan)
```

```{code-cell} ipython3
plt.imshow(land_mask);
```

## Using the mask

Now that we have the land_mask, we multiply the data by the mask
to remove water pixels, like this:

```{code-cell} ipython3
varname = 'nir'
xarray_dict[varname].data = xarray_dict[varname].data*land_mask
```

```{code-cell} ipython3
vmin = 0.0
vmax = 0.5
pal_dict = make_pal(vmin=vmin,vmax=vmax)
fig, ax = plt.subplots(1,1)
var = 'nir'
xarray_dict[var].plot.imshow(ax=ax,
                    norm = pal_dict['norm'],
                    cmap = pal_dict['cmap'],
                    extend = "both")
ax.set(title=f"{xarray_dict[var].long_name}");
```

#### Mask the remain bands

Do this to every band except fmask

```{code-cell} ipython3
for key,array in xarray_dict.items():
    if key=='fmask':
        continue
    array.data = array.data*land_mask
```

### Give the bands shorter names

Makes it easier to type

```{code-cell} ipython3
b2, b3, b4, b5 = (xarray_dict['blue'],xarray_dict['green'], 
                   xarray_dict['red'], xarray_dict['nir'])
```

## Plotting joint histograms

Compare the masked joint histograms with the ones we found in {ref}`false_color_joint`.  They are much cleaner.

```{code-cell} ipython3
fig = sns.jointplot(
    x=b3.data.ravel(),
    y=b4.data.ravel(),
    xlim=(0, 0.125),
    ylim=(0.0, 0.125),
    kind="hex",
    color="#4CB391",
    gridsize=100
)
fig.fig.suptitle("green (band 3) vs red (band 4)");
axes = fig.fig.get_axes()
axes[0].set(xlabel = "band 3 reflectivity",
            ylabel = "band 4 reflectivity");
```

Note that the plot below looks funny because there are many water pixels with low reflectivity.  We'll mask
these out in the next notebook

```{code-cell} ipython3
fig = sns.jointplot(
    x=b4.data.ravel(),
    y=b5.data.ravel(),
    kind="hex",
    xlim=(0, 0.125),
    ylim=(0.0, 0.5),
    color="#4CB391",
    gridsize=100
)
fig.fig.suptitle("red (band 4) vs near ir (band 5)");
axes = fig.fig.get_axes()
axes[0].set(xlabel = "band 4 reflectivity",
            ylabel = "band 5 reflectivity");
```

## Caveat

Histogram equalization won't work with masked scenes, since `exposure.equalize_hist` won't work with nans.  That's not a real problem though, because equalization if more about getting a qualitative instead of a quantitimpression.

+++

## Assignment 5 part 2:  make a cloud mask function

Due next Friday

Write a function that takes an image and its fmask and returns a new image
with all cloudy pixels set to np.nan.  Make a notebook that uses this function
to plot a partly cloudy scene.

```{code-cell} ipython3

```
