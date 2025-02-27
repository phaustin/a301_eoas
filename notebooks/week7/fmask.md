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
in.  In this notebook we use a mask file downloaded from NASA (`HLS.L30.T10UDV.2015165T190019.v2.0.Fmask.tif`) using {ref}`week2:hls`

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

Here's how to list the individual bit order for each number in the mask

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

How do we find the water pixels for the clipped scene.  We want to find
all pixels in the mask with their bit 5 set to 1.  We can do that by
creating a mask with only the bit 5 set to 1, then doing a `bitwise_and` with
the masked values.  That will turn the water pixels into decimal 32 (2**5), and
all other pixels into 0.

```{code-cell} ipython3
fifth_bit_on = 0b00100000
#
# construct and array of the right shape filled with
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

```{code-cell} ipython3
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.imshow(water_mask)
ax2.hist(water_mask.flat);
```

### Inverting the mask

Now that we know where the water is, we want to assign all those pixels
as np.nan, and all land pixels as 1.  We can do this using np.where. The
next cell assigns all the land pixels the value 1, and all other pixels
the value np.nan

```{code-cell} ipython3
land_mask = np.where(water_mask == 0,1,np.nan)
plt.imshow(land_mask);
```

## Using the mask

Now that we have the land_mask, we multiply the data by the mask
to remove water pixels, like this

```{code-cell} ipython3
xarray_dict[var].data = xarray_dict[var].data*land_mask
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

```{code-cell} ipython3
for key,array in xarray_dict.items():
    if key=='fmask':
        continue
    array.data = array.data*land_mask
```

### Give the bands shorter names

Makes it easier to type

```{code-cell} ipython3
b2, b3, b4, b5 = xarray_dict['blue'],xarray_dict['green'], xarray_dict['red'], xarray_dict['nir']
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

## Histogram equalization

The mask creates a new problem though -- histogram equalization won't work with
nans.  Get around this by turning the nans into zeros.  np.isnan finds the nans
then we use where as before to replace them with zeros.


```{code-cell} ipython3
stretch_input = dict()
for key,value in xarray_dict.items():
    if key == 'fmask':
        continue
    data = value.data
    filled_data = np.where(np.isnan(data), 0, data)
    value.data = filled_data
    stretch_input[key] = value
```

```{code-cell} ipython3
stretch_input['nir'].plot.imshow();
```

### Here's the cumulative distribution for band 5

If we stretch the band 5 values to this cumulative distribution, 50% of the data range (0-125) is going to get essentially
100% of the levels between 0-1.

```{code-cell} ipython3
b2, b3, b4, b5 = xarray_dict['blue'],xarray_dict['green'], xarray_dict['red'], xarray_dict['nir']
```

```{code-cell} ipython3
from skimage import exposure
#
# want 256 levels from 0-255
#
bins=256
img_cdf, bins = exposure.cumulative_distribution(b5.data.ravel(), bins)
plt.plot(img_cdf)
plt.grid(True);
```

### Stretching step 1: stretch the data in each band and save to a dictionary with the band name as key

To do the histogram stretch we'll use  the [scikit-image equalization module](https://scikit-image.org/docs/dev/auto_examples/color_exposure/plot_equalize.html).  It uses our boolean mask
to ignore np.nan values when it calculates the distribution.

```{code-cell} ipython3
stretched_dict = dict()
keys = ['b2','b3','b4','b5']
images = [b2, b3, b4, b5]
for key, image in zip(keys,images):
    stretched_dict[key] = exposure.equalize_hist(image.data)
```

### Before and after stretching

Pretty dramatic difference

```{code-cell} ipython3
fig, (ax1, ax2) = plt.subplots(1,2)
ax1.imshow(b3);
ax2.imshow(stretched_dict['b3']);
```

### Stretching step 2: check the stretched histograms

Redo the histogram plots to show the stretched distributions.  Note that they still contain information
about the correlation between bands, but the distributions are much broader than their unstretched versions.  Also note that in each of the joint plot there are clusters of pixels that share similar values in the two bands.  These clusters correspond to similar surface types (water, grass fields, golf courses, concrete pavement etc.)

```{code-cell} ipython3
fig = sns.jointplot(
    x=stretched_dict['b3'].ravel(),
    y=stretched_dict['b4'].ravel(),
    xlim=(0, 1),
    ylim=(0.0, 1),
    kind="hex",
    color="#4CB391"
)
fig.fig.suptitle("stretched green (band 3) vs red (band 4)");
axes = fig.fig.get_axes()
axes[0].set(xlabel = "stretched band 3 reflectivity",
            ylabel = "stretched band 4 reflectivity");
```

```{code-cell} ipython3
fig = sns.jointplot(
    x=stretched_dict['b4'].ravel(),
    y=stretched_dict['b5'].ravel(),
    xlim=(0, 1),
    ylim=(0.0, 1),
    kind="hex",
    color="#4CB391"
)
fig.fig.suptitle("stretched red (band 4) vs near ir (band 5)");
axes = fig.fig.get_axes()
axes[0].set(xlabel = "stretched band 4 reflectivity",
            ylabel = "stretched band 5 reflectivity");
```

## Write the false color image into 3-dimensional array called "band_values"

We need to fill a new array of shape [3,nrows,ncols] and dtype=unsigned integer (byte)
with the
bands in the correct order -- red, blue, green.  The cell below does this
using the `img_as_ubyte` function, which scales and converts the floating point reflectivities to "unsigned bytes"
which are postive 8 bit numbers with range 0-255. The
output array needs to have the same number of rows and columns as the original image. I'll use
b3.shape to get those.

```{code-cell} ipython3
nrows, ncols = b3.shape
band_values = np.empty([3, nrows, ncols], dtype=np.uint8)
for index, key in enumerate(['b5', 'b4', 'b3']):
    stretched = stretched_dict[key]
    band_values[index, :, :] = img_as_ubyte(stretched)
```

#### Note that we've lost our missing values

There's no way to write an np.nan as a missing value in a datatype that can only take on
values between 0 and 255, so all missing values have been converted to 0

+++

### Stretched band 5 (nir)

```{code-cell} ipython3
fig, ax = plt.subplots(1,1,figsize=(12,8))
ax.imshow(band_values[0, :, :]);
```

### Create the dataArray

Now that I have 3 bands scaled from 0-255, I can write them out as
a png file, with new tags.  Recall from the {ref}`week8:zoom_landsat` that I need
to supply the array, dimensions, coordinates and attributes.

For the coordinate dictionary, I can borrow the 'x' and 'y' coordinates from band 3.

```{code-cell} ipython3
dims = ('band','y','x')
coords={'band':('band',[5,4,3]),
        'x': ('x',b3.x.data),
        'y': ('y',b3.y.data)}
```

### Add attributes

I'll keep some of the old attributes from the original `bands_543` dataset, and
add two new ones: history and landsat_rgb_bands.

```{code-cell} ipython3
band_names=['B05','B04','B03']
keep_attrs = ['cloud_cover','date','day','target_lat','target_lon']
all_attrs = xarray_dict['red'].attrs
attr_dict = {key: value for key, value in all_attrs.items() if key in keep_attrs}
attr_dict['history']="written by false_color.md"
attr_dict["landsat_rgb_bands"] = band_names
```

### Create the falsecolor dataArray

Just copy this from the `zoom_landsat` notebook

```{code-cell} ipython3
false_color=xarray.DataArray(band_values,coords=coords,
                            dims=dims,
                            attrs=attr_dict)
false_color.rio.write_crs(b3.rio.crs, inplace=True)
false_color.rio.write_transform(b3.rio.transform(), inplace=True);
```

```{code-cell} ipython3
false_color
```

The final image -- the imshow function interprets any array with shape [3, nrows, ncols] as
a false color image and presents it with rgb colors.

+++

#### False color bands 5,4,3

```{code-cell} ipython3
false_color.plot.imshow(figsize=(6,9));
```

### Save as a png file

Now that we have a standard 24 bit color 3 channel array we can create either a png or a jpg file that can be viewed with a browser.

If the filename ends in png, rioxarray will save it in the standard png format.

```{code-cell} ipython3
png_filename = data_dir / "vancouver_543.png"
false_color.rio.to_raster(png_filename)
```

### Read it back in to check

Here's the finished product -- read back in from the png file

```{code-cell} ipython3
Image(filename=png_filename,width=300)
```

## Repeat with the red, green, blue

Try a true color image, note that simple stretching doesn't really work to make photo-realistic picture

```{code-cell} ipython3
#
# just repeat replacing nir b5 with blue b2
#
nrows, ncols = b3.shape
band_values = np.empty([3, nrows, ncols], dtype=np.uint8)
for index, key in enumerate(['b4', 'b3', 'b2']):
    stretched = stretched_dict[key]
    band_values[index, :, :] = img_as_ubyte(stretched)
```

```{code-cell} ipython3
true_color=xarray.DataArray(band_values,coords=coords,
                            dims=dims,
                            attrs=attr_dict)
true_color.rio.write_crs(b3.rio.crs, inplace=True)
true_color.rio.write_transform(b3.rio.transform(), inplace=True);
```

#### bands 4,3,2 -- looking strange

```{code-cell} ipython3
true_color.plot.imshow(figsize=(6,9));
```

#### compare with the Nasa browse image

Question: what's the difference between `DataArray.plot.imshow` and `IPython.display.Image`

```{code-cell} ipython3
browse_jpg = list(data_dir.glob("**/*vancouver*jpg"))[0]
Image(browse_jpg,width=300)
```

## Summary

False color images have advantages and disadvantages.  They make it easy to see subtle differences between image regions, but the cost is that the stretched histograms now don't connect directly to the original radiances.

+++

## Assignment 5 part 1:  create a false color image for your scene

Due next Friday

Write a function that takes 3 tif files and returns a rioxarray false color image. Use it
to make a band 5,4,3 false color png file of your scene

```{code-cell} ipython3

```
