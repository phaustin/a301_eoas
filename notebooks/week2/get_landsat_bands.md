---
jupytext:
  formats: md:myst,ipynb
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

(week2:hls)=
# Landsat 1: Dowloading Landsat and Sentinel data from NASA

- Download get_landsat_bands.ipynb from the [week2 folder](https://drive.google.com/drive/folders/1-Ja2wVKVIjkZb7Gx_rfc14J_aBYiknuw?usp=sharing)


## Introduction 

This notebook goes over the procedure to locate and download 30 meter resolution
Landsat and Sentinel data using NASA's Harmonized Landsat and Sentinel-2  dataset.
These two satellites have very similar radiometer bands, fly in similar orbits and
have similar resolutions and swath widths.  NASA (Landsat) and the European Space Agency (ESA)
have collaborated on a common dataset that gives corrected surface reflectivity and brightness
temperatures for the two satellites.

## Overview/objectives

In the first few sections, we'll go over how to select a Landsat scene for a particular place and range of dates, and look at the true-color browse image.  This image is available as jpg file without having to
authenticate with an earthdata id.  

Then we'll download a band 5, near-infrared geotif file, where tif stands for "tagged image format".  Here is the [tif wikipedia article](https://en.wikipedia.org/wiki/TIFF). Unlike the jpg format, tif files don't use lossy compression, and contain arbitrary metadata about the image.

Python modules introduced below:

- earthaccess, to send credentials to NASA
- pystac_client, to search the image catalog for satellites, locations and dates
- rioxarray, to read the tif image into memory and store as an xarray.DataArray object
- xarray.DataArray, to access the metadata, make histograms and image plots
- matplotlib.Normalize, to enhance image contrast for plotting specific ranges of reflectivities

We'll go into more detail on xarray and matplotlib/cartopy in future notebooks.

By the end of this notebook you should have a saved tif file of your landsat, band 5 image, and a good idea of what the reflective patterns of the image are.

## Installation

This notebook requires three additions to the a301 environment.  To install them, do

```
conda install earthaccess pystac-client shapely
```

+++

## Authentication

To get NASA to give you your image, you'll need your username and password that you created at [https://urs.earthdata.nasa.gov/](https://urs.earthdata.nasa.gov)

You need to authenticate as described in: [https://earthaccess.readthedocs.io/en/latest/howto/authenticate](https://earthaccess.readthedocs.io/en/latest/howto/authenticate/)

The following steps create a `~/.netrc` file, which  keeps your username and password for future use:

1. open a terminal and activate the a301 environment
2. type `python -i` to get an interactive python session
3. type `import earthaccess`
4. type `auth = earthaccess.login(strategy="interactive", persist=True)` to create an authorization object and write the information into a netrc file for future reference.

Then the next time you need to download or search HLS data you should just be able to do:

```{code-cell} ipython3
import earthaccess
auth = earthaccess.login(strategy="netrc")
```

```{code-cell} ipython3
auth.authenticated
```

and your credentials will be read in from the netrc file.

You can search the catalog without logging in, but once you ask for data, the earthaccess object will write a new file called "cookies.txt" in the directory  you started jupyterlab in.

+++

##  Doing an image search using pystac_client

STAC is an acronym for "Spatio-temporal asset catalog", which is a standard way of cataloging
GIS resources in the cloud.  A STAC catalog hold metadata, including web addresses, for geotiff
files like those uploaded by the [NASA harmonized landsat-sentinel project](https://www.earthdata.nasa.gov/learn/articles/hls-cloud-efforts) (HLS) to Amazon Web Services.

+++

We get the url for the stac catalog from the "Common Metadata Repository" stored on at [NASA CMR page](https://nasa-openscapes.github.io/2021-Cloud-Hackathon/tutorials/02_Data_Discovery_CMR-STAC_API.html). The HLS project catalog is called "LPCLOUD"  (for land processes cloud and is available at [https://cmr.earthdata.nasa.gov/stac/LPCLOUD](https://cmr.earthdata.nasa.gov/stac/LPCLOUD).  This is called a "stac endpoint" and will receive
and process requests sent to it by the pystac Client.

+++

We'll also need the [shapely](https://towardsdatascience.com/geospatial-adventures-step-1-shapely-e911e4f86361) library to specify a point on the earth that we want to be included in our search. In addition, we need to specify a date range to search.

```{code-cell} ipython3
import numpy
from pathlib  import Path
import inspect

from matplotlib import pyplot as plt
import numpy as np
from copy import copy

import rioxarray
from pystac_client import Client
from shapely.geometry import Point
```

Use shapely to create a point object holding the location of UBC.  Also create a datetime object showing the range of days you're interested in searching for images.

```{code-cell} ipython3
hls_lon, hls_lat = -58.3816, -34.607
center_point = Point(hls_lon, hls_lat)
van_lon, van_lat = -123.120, 49.2827
center_point = Point(van_lon, van_lat)
#june_2015 = "2015-06-01/2015-06-30"
summer_2023 = "2023-06-01/2023-08-31"
```

```{code-cell} ipython3
# connect to the STAC endpoint
cmr_api_url = "https://cmr.earthdata.nasa.gov/stac/LPCLOUD" 
client = Client.open(cmr_api_url)
```

### set up the search

The pystac client object takes the search parameters as the following keywords:

```{code-cell} ipython3
search = client.search(
    collections=["HLSL30.v2.0"],
    intersects=center_point,
    datetime= summer_2023
) 
# uncomment below to see gory details
# help(search)
```

### get the metadata for search items

This search should find 4 scenes -- 2 of which have 4% cloud cover.

```{code-cell} ipython3
items = search.item_collection()
for index, the_scene in enumerate(items):
    print(f"\n\n{index=}\nproperties: {the_scene.properties}")
# items
```

### Get the assets for scene 1 (June 14, 2015)

Once we decide on the scene, we can access its assets.  It contains the href (url) for
each of the landsat bands (except Band 8) -- here are their wavelengths:  [Landsat Bands](https://landsat.gsfc.nasa.gov/satellites/landsat-8/landsat-8-bands/)

What happened to band 8? It is in a wavelength range that is only measured by the Sentinel MSI scanner, not the Landsat OLI scanner.  The channel comparisons are given here:
[harmonized channels](https://lpdaac.usgs.gov/data/get-started-data/collection-overview/missions/harmonized-landsat-sentinel-2-hls-overview/)

If we had found a Sentinel image instead, we would be missing the thermal channels in Landsat bands 10 and 11.

There are also geotiffs for the 

- Solar Azimuth Angle (SAA) 
- Solar Zenith Angle (SZA)
- Sensor Azimuth Angle (VAA)
- Sensor Zenith Angle (VZA)

and a jpg image file called 'browse' which is a 1000 x 1000 pixel true color image for the scene.  This image is created by mapping bands 2, 3 and 4 to the blue, green and red values in the browse jpg image file file.

The filenames below show that the June 14 scene was taken by Landsat -- Landsat filenames begin with HLS.L30, Sentinel with HLS.S30.  The number 30 is the pixel size in meters:  30 meters high by 30 meters wide

```{code-cell} ipython3
hls_scene = items[6]
hls_scene.assets
```

### Download and display the true-color browse image

You can see the browse image by clicking on the asset href above. We can also use rioxarray to download the browse image from its url.  The browse image is stored as a red green blue jpg file:  [wikipedia page on jpg](https://en.wikipedia.org/wiki/JPEG)

```{code-cell} ipython3
hls_browse = rioxarray.open_rasterio(hls_scene.assets['browse'].href)
```

`hls_browse` is an [xarray DataArray](https://docs.xarray.dev/en/stable/generated/xarray.DataArray.htm).  In this case it's a simple 3 dimensional array with shape (3,1000,1000) holding the integer brightness levels (0-255), along with x,y values for each pixel.   These are just values of the pixel centers between 0-1000, since the browse image has no coordinate reference system attached.

```{code-cell} ipython3
type(hls_browse)
```

```{code-cell} ipython3
hls_browse
```

and we can plot it using imshow

```{code-cell} ipython3
fig, ax = plt.subplots(1,1,figsize=(10,10))
hls_browse.plot.imshow(ax=ax, origin = 'upper')
ax.set_title('June 14, 2015, Landsat 8');
```

## Working with the Band5 geotiff

Landsat Band5 in the near-infrared spans wavelengths between  0.845–0.885 $\mu m$ which are invisible to the human eye. This is a wavelength region where vegetation is very reflective,
because the leaves want to absorb red photons for photosynthesis and reflect slightly longer near-ir photons so they don't get absorbed and 
raise the leaf temperature.  This difference between red (Band4) and near-infrared (Band 5) is called the ["red edge"](https://agrio.app/Red-Edge-reflectance-monitoring-for-early-plant-stress-detection/).  

If you have managed to get your earthdata login into the `~/.netrc` file you should be able to download and save band 5 as shown below:

```{code-cell} ipython3
band_name="B05"
hls_scene.assets[band_name].href
```

### set the cookie file name as an environmental variable

We got the browse image for free, but the actual bands require authorization. The nasa earthdata site will put an encrypted token into the file `cookies.txt` in the current directory ('.') when we ask for band data.

```{code-cell} ipython3
import os
os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"
```

### Read the band 5 raster

The next cell reads in the raster.  By setting `masked=True` we are telling rasterio to look up the `_FillValue` tag in the
geotiff, and replace all pixels that have that value to `np.nan`.

#### Use a local file if available

This step is the one that requires authentication.  NASA counts the number of downloads your account makes in a day, and
will deny access if you exceed a threshold (about 50 downloads).  At the bottom of the notebook in section {ref}`sec:writeout` we write band 5 to disk if the variable `writeit` is set to `True`.  If you want to use that file instead, set the variable `from_disk` to `True`

```{code-cell} ipython3
data_dir = Path().home() / 'repos/a301/satdata/landsat'
band_name = 5
data_dir.mkdir(exist_ok=True, parents=True)
disk_file = data_dir / f"hls_landsat8_{band_name}.tif"
has_file = disk_file.exists()

from_disk = True
if from_disk:
    if not has_file:
        raise IOError(f"can't find {disk_file}, rerun with from_disk=False and writeit=True") 
    hls_band5 = rioxarray.open_rasterio(disk_file,masked=True)
else:
    # go to NASA
    hls_band5 = rioxarray.open_rasterio(hls_scene.assets['B05'].href,masked=True)
```

### List all attributes

Unlike the browse image, the actual band 5 tif has metadata.  xarray DataArray objects store metadata as "attributes".  Here are all the attributes we fetched from the tif file.

```{code-cell} ipython3
hls_band5.attrs
```

The most important are the coordinate reference system for the image (UTM zone 10N), the coordinates of the upper left corner (not the center) (ULX, ULY), the pixel size (SPATIAL_RESOLUTION), cloud_coverage (4%), and the scale_factor we need to multiply by to get surface refectance from the packed data values.

The DataArray also has three indexes, the first is just the number 1 (only 1 band in the tif), the next 2 are the x,y values of the center of each pixel in UTM 10N coordiates. Note that the  y array gets smaller as the index increases -- the image is scanned from top to bottom.

```{code-cell} ipython3
hls_band5.indexes
```

### Machine readable crs

The `HORIZONTAL_CS_NAME` attribute is for humans.  To use the image CRS with a program like cartopy we need a more detailed version.  This is supplied by an accessor function added to xarray by rioxarray, with outputs the crs in "well known text (WKT)" format:

```{code-cell} ipython3
hls_band5.rio.crs
```

### Image  coverage

Here are two ways of finding the image width in km.  The first way gives 109.77 km

```{code-cell} ipython3
((hls_band5.x[-1] - hls_band5.x[0])/1000.)
```

The second gives 109.80 km.  

#### Explain why the two estimates are correct but different.

```{code-cell} ipython3
hls_band5.NCOLS*30./1000.
```

### Scaling the image

The cell below removes the useless unit index and converts the image from (1,3660,3660) to (3660,3660), then scales the array.
Note that by doing arithemetic on the image, we lose all the metadata, but we keep the indexes.

```{code-cell} ipython3
hls_raster = hls_band5.squeeze()
hls_raster = hls_raster*hls_band5.scale_factor
hls_raster.attrs, hls_raster.indexes
```

```{code-cell} ipython3
hls_raster.attrs = hls_band5.attrs
hls_raster.x[0]
```

### Histogram the raster

Make sure the scaled band5 reflectance is in the range 0-1

```{code-cell} ipython3
hls_raster
```

```{code-cell} ipython3
#hls_raster.plot.hist();
# ls_band5.plot.hist()
from matplotlib import pyplot as plt
#plt.hist(hls_raster.data.flat)
```

### Plot it using a grey palette

We can use the Normalize object to adjust the maximum range we want to assign colors to.  In this case,
we don't want to waste colors on the very few pixels with reflectances higher than 0.8.  We'll use a grey scale colormap.  Note that the DataArray object
knows how to use the x and y indexes to label the axis tick marks in map coordinates.

```{code-cell} ipython3
pal = copy(plt.get_cmap("Greys_r"))
pal.set_bad("0.75")  # color 75% grey np.nan cells
pal.set_over("w")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
vmin = 0.0  #anything under this is colored black
vmax = 0.8  #anything over this is colored white
from matplotlib.colors import Normalize
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1, figsize=(10,10))
hls_raster.plot(ax=ax, cmap=pal, norm = the_norm)
ax.set_title(f"Landsat band {band_name}");
```

(sec:writeout)=
### Write out the raster as a geotiff

Save the original tif to disk so you don't need to go back to NASA

```{code-cell} ipython3
writeit=False
if writeit:
    hls_band5.rio.to_raster(disk_file)
    #check if write worked
    hls_band5 = rioxarray.open_rasterio(disk_file,masked=True)
    print(f"checking read, here is the crs: {hls_band5.rio.crs}")
```

## What's next

+++

Now that we can get landsat and sentinel scenes, we need to be able to 
subset to a particular part of the image, apply the cloud mask to remove cloudy
pixels and use channel ratios to infer surface properties.  That's the topic for the
next few notebooks.


### For Monday's class
For Monday, copy this notebook and edit it to download and save a new tif containing band 4 (red) for your location.

```
!python --version
```
