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

(week5:add_palette)=
# Adding a palette to an axis

- Download add_palette.ipynb from the [week5 folder](https://drive.google.com/drive/folders/1-Ja2wVKVIjkZb7Gx_rfc14J_aBYiknuw?usp=sharing)


## Introduction

Plotting images with complicated palettes is a pain.  If you have a palette you like, and would
like to use over and over again, you can wrap that palette in a function, as shown below.

```{code-cell} ipython3
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
import rioxarray
```

## Get the blue band

```{code-cell} ipython3
data_dir = Path().home() / 'repos/a301/satdata/landsat'
tif_file = data_dir.glob("**/*B02.tif") 
tif_file = list(tif_file)[0]
has_file = tif_file.exists()
print(f"{tif_file=}")
if not has_file:
    raise IOError(f"can't find {tif_file}") 
hls_blue = rioxarray.open_rasterio(tif_file,masked=True)
hls_blue=hls_blue.squeeze()
hls_blue = hls_blue*hls_blue.scale_factor
```

## Step 1 Histogram the image

The histogram shows that most of the pixels are very dark, but there are a few bright
clouds.  We're going to see very little  information from this raw image with a default palette

```{code-cell} ipython3
hls_blue.plot.hist();
```

## Step 2: Make a default plot

As expected, not good

```{code-cell} ipython3
fig, ax = plt.subplots(1, 1, figsize=(4, 4))
hls_blue.plot.imshow(ax=ax);
```

## Step 3: Normalized palette

Create a normalized palette  with values for the over and under colors
and minimum and maximum values.  This looks better.

```{code-cell} ipython3
vmin, vmax = 0., 0.05
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
palette = "viridis"
pal = plt.get_cmap(palette)
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("w")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
fig, ax = plt.subplots(1, 1, figsize=(4, 4))
hls_blue.plot.imshow(ax=ax, cmap=pal, norm=the_norm, origin="upper",extend = "both");
```

## Step 5: create a function

But that's a lot of work to make one picture.  We can create an importable function called `make_pal` to encapsulate some of that.

```{code-cell} ipython3
def make_pal(vmin = None, vmax = None, palette = "viridis"):
    the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
    pal = plt.get_cmap(palette)
    pal.set_bad("0.75")  # 75% grey for out-of-map cells
    pal.set_over("w")  # color cells > vmax red
    pal.set_under("k")  # color cells < vmin black
    return the_norm, pal

vmin, vmax = 0,0.1
the_norm, pal = make_pal(vmin, vmax)
fig, ax = plt.subplots(1, 1, figsize=(4, 4))
hls_blue.plot.imshow(ax=ax, cmap=pal, norm=the_norm, origin="upper",extend = "both");
```

## Step 6: pass a dictionary using keyword expansion

If we don't like typing all those parameters into imshow, we could return
a dictionary and use it as below.  The problem with this is that a new
user reading the code would have trouble figuring out what imshow actually needs for arguments,
because they wouldn't see the code for `make_pal`, which would be imported from
a library.

```{code-cell} ipython3
def make_pal(ax,vmin = None, vmax = None, palette = "viridis"):
    the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
    pal = plt.get_cmap(palette)
    pal.set_bad("0.75")  # 75% grey for out-of-map cells
    pal.set_over("w")  # color cells > vmax red
    pal.set_under("k")  # color cells < vmin black
    out_dict=dict(ax=ax,cmap=pal,norm=the_norm, origin="upper",
                  extend = "both")
    return out_dict

vmin, vmax = 0,0.1
fig, ax = plt.subplots(1, 1, figsize=(4, 4))
pal_dict = make_pal(ax,vmin, vmax)
#
# pretty simple
#
hls_blue.plot.imshow(**pal_dict);
```

```{code-cell} ipython3

```
