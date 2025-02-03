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

(week3:image_zoom)=

# Zooming an image

- Download zoom_landsat.ipynb from the [week3 folder](https://drive.google.com/drive/folders/1-Ja2wVKVIjkZb7Gx_rfc14J_aBYiknuw?usp=sharing)


We need to be able to select a small region of a landsat image to work with.  This notebook:downloaded in the week3 folder in the [google drive]


1. zooms in on a 400 pixel wide x 600 pixel high subscene centered on EOS South, using pyproj and the affine transform to map from lon,lat to x,y in UTM zone 10N to row, column in the landsat imag

2. Plots coastlines in the UTM-10N crs

3. Calculates the new affine transform for the subcene, and writes the image out to a 1 Mbyte tiff file using rasterio

4. Repeats the write operation using rioxarray instead of rasterio

- Notable new features
  - Use the [pyproj module](https://pyproj4.github.io/pyproj/stable/examples.html) to find x,y from lat, lon
  - Use numpy slice objects to slice the rows and columns from the image
  - use rioxarray `clip_box` to clip the desired rows and columns from the image
  - use rasterio and rioxarray `to_raster` to write a new clipped tif file

```{code-cell} ipython3
import copy
import pprint
from pathlib import Path

import cartopy
import numpy as np
import numpy.random
import rasterio
from affine import Affine
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from pyproj import CRS, Transformer
import rioxarray
from cartopy import crs as ccrs
```

## Get the tiff files and calculate band 5 reflectance

```{code-cell} ipython3
data_dir = Path().home() / 'repos/a301/satdata/landsat'
band_name = 5
data_dir.mkdir(exist_ok=True, parents=True)
disk_file = data_dir / f"hls_landsat8_{band_name}.tif"
has_file = disk_file.exists()

if not has_file:
    raise IOError(f"can't find {disk_file}, rerun with the week2 get_landsat_scene notebook") 
hls_band5 = rioxarray.open_rasterio(disk_file,masked=True)
```

## Save the crs and the affine transform for the full iamge

We need to keep both full_affine (the affine transform for the full scene, and the coordinate reference system for pyproj (called p_utl below).  

Complication -- as before, cartopy can't use the pyproj p_utm, so need to do a convertion for cartopy_crs.

```{code-cell} ipython3
full_affine = hls_band5.rio.transform()
hls_crs = hls_band5.rio.crs.to_wkt()
b5_refl = hls_band5.data.squeeze()*hls_band5.scale_factor
```

## Convert to cartopy crs for map plot

As in {ref}`week3:map_landsat` we've got to jump th rough hoops to get the correct cartopy crs. The problem is that hls forgot to put the epsg code in their tif file.

```{code-cell} ipython3
hls_crs
```

```{code-cell} ipython3
proj_crs = CRS.from_wkt(hls_crs)
pyproj_epsg = proj_crs.to_epsg(min_confidence=60)
print(f"{pyproj_epsg=}")
cartopy_crs = ccrs.epsg(pyproj_epsg)
proj_code = cartopy_crs.to_epsg()
proj_code
```

```{code-cell} ipython3
plt.imshow(b5_refl);
```

### Pick a random selection  of 1000 pixels to histogram

Don't need 3660 x 3660 pixels to get a feeling for the distribution

```{code-cell} ipython3
subset = np.random.randint(0, high=len(b5_refl.flat), size=1000, dtype="l")
plt.hist(b5_refl.flat[subset])
plt.title("band 5 reflectance whole scene")
```

## Locate UBC on the map

We need to project the center of campus from lon/lat to UTM 10N x,y using pyproj.Transformer and our crs (which in this case is UTM).  We can transform from lat,lon (p_lonlat) to x,y (p_utm) to anchor us to a known point in the map coordinates.

+++

### Alert!! the epsg:4326 projection order is (lat, lon) (yikes)

see [this stack exchage](https://gis.stackexchange.com/questions/434038/order-of-latitude-and-longitude-in-epsg4326).  Most projections are (lon, lat) which
maps more logically to (x, y).  Compare the axis order on these two crs:

```{code-cell} ipython3
CRS.from_epsg(proj_code)
```

```{code-cell} ipython3
CRS.from_epsg(4326)
```

```{code-cell} ipython3
p_utm = CRS.from_epsg(proj_code)
p_latlon = CRS.from_epsg(4326)
transform = Transformer.from_crs(p_latlon, p_utm)
ubc_lon = -123.2460 
ubc_lat = 49.2606
ubc_x, ubc_y = transform.transform(ubc_lat, ubc_lon)
ubc_x,ubc_y
```

```{code-cell} ipython3
lon, lat = transform(ubc_x, ubc_y, inverse=True)
```

For more on epsg:4326 see [Justyna Jurkowska's](https://8thlight.com/insights/geographic-coordinate-systems-101#:~:text=EPSG%3A4326%2C%20also%20known%20as,Google%20Earth%20and%20GSP%20systems) blog entry.

+++

## Locate UBC on the image

Now we need to use the affine transform to go between x,y and
col, row on the image.  The next cell creates two slice objects that extend  on either side of the center point.  The tilde (~) in front of the transform indicates that we're going from x,y to col,row, instead of col,row to x,y.  (See [this blog entry](http://www.perrygeo.com/python-affine-transforms.html) for reference.)  Remember that row 0 is the top row, with rows decreasing downward to the south.  To demonstrate, the cell below uses the tranform to calculate the x,y coordinates of the (0,0) corner.

```{code-cell} ipython3
full_ul_xy = np.array(full_affine * (0, 0))
print(f"orig ul corner x,y (km)={full_ul_xy*1.e-3}")
```

(sec:slice)=
## Slice the array

Make our subscene 400 pixels wide and 600 pixels tall, using UBC as a reference point.
We need to find the right rows and columns on the image to save for the subscene.  Do this by working outward from UBC by a certain number of pixels in each direction, using the inverse of the full_affine transform to go from x,y to col,row

```{code-cell} ipython3
b5_refl.shape[0] - 2230
```

```{code-cell} ipython3
ubc_x, ubc_y = full_affine * (ubc_row, ubc_col)
ubc_x, ubc_y
```

```{code-cell} ipython3
ubc_col, ubc_row = ~full_affine * (ubc_x, ubc_y)
ubc_col, ubc_row = int(ubc_col), int(ubc_row)
offset_col = 200
offset_row = 300
l_col_offset = -offset_col
r_col_offset = +offset_col
b_row_offset = +offset_row
t_row_offset = -offset_row
col_slice = slice(ubc_col + l_col_offset, ubc_col + r_col_offset)
row_slice = slice(ubc_row + t_row_offset, ubc_row + b_row_offset)
section = b5_refl[row_slice, col_slice]
ubc_ul_xy = full_affine * (col_slice.start, row_slice.start)
ubc_lr_xy = full_affine * (col_slice.stop, row_slice.stop)
ubc_ul_xy, ubc_lr_xy
```

```{code-cell} ipython3
print(section.shape)
```

```{code-cell} ipython3
ubc_col, ubc_row
```

```{code-cell} ipython3
ubc_x, ubc_y
```

```{code-cell} ipython3
full_affine*(ubc_col, ubc_row)
```

```{code-cell} ipython3
upper_left_col = ubc_col + l_col_offset
upper_left_row = ubc_row + t_row_offset
print(upper_left_row, upper_left_col)
```

# Plot the raw band 5 image, clipped to reflectivities below 0.6

This is a simple check that we got the right section.  Note that matplotlib ignores the `figsize=(10,10)` argument in plt.subplots and keeps the correct aspect ratio for the image.  I have to make a copy of the palette so my changes "stick"

```{code-cell} ipython3
vmin = 0.0
vmax = 0.6
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
palette = "viridis"
pal = copy.copy(plt.get_cmap(palette))
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("w")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
cs = ax.imshow(section, cmap=pal, norm=the_norm, origin="upper")
fig.colorbar(cs, extend = 'both');
```

## put this on a map

Note that the origin is switched to "lower" in the x,y coordinate system below,
since y increases upwards.  The coastline is very crude, but at least indicates we've got the coords roughly correct.  See the "high_res_map" notebook for a better coastline.

```{code-cell} ipython3
fig2, ax = plt.subplots(1, 1, figsize=(10,10), subplot_kw={"projection": cartopy_crs})
#
# extent is distance betweenn sides, but the affine transform gives location of pixel centers
# for these tiny pixels it doesn't make a noticeable difference
#
edge_offset = 15 #pxiels are 30 meters wide, so edges are 1/2 a pixel away from centers
image_extent = [ubc_ul_xy[0] - edge_offset, ubc_lr_xy[0] + edge_offset, ubc_lr_xy[1] - edge_offset, ubc_ul_xy[1] + edge_offset]
ax.set_extent(image_extent, crs=cartopy_crs);
cs = ax.imshow(
    section,
    cmap=pal,
    norm=the_norm,
    origin="upper",
    extent=image_extent,
    transform=cartopy_crs,
    alpha=1,
)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="auto", levels=[1, 2, 3],edgecolor='red'))
# shape_project = cartopy.crs.Geodetic()
# ax.add_geometries(
#     df_coast["geometry"], shape_project, facecolor="none", edgecolor="red", lw=2
# )
#ax.coastlines(resolution="10m", color="red", lw=2)
ax.plot(ubc_x, ubc_y, "ro", markersize=25)
fig2.colorbar(cs, extend = 'both');
```

##  Use  rasterio  to write a new tif file

### Set the affine transform for the scene

We can write this clipped image back out to a much smaller tiff file if we can come up with the new affine transform for the smaller scene.  Referring again [to the writeup](http://www.perrygeo.com/python-affine-transforms.html) we need:

    a = width of a pixel
    b = row rotation (typically zero)
    c = x-coordinate of the upper-left corner of the upper-left pixel
    d = column rotation (typically zero)
    e = height of a pixel (typically negative)
    f = y-coordinate of the of the upper-left corner of the upper-left pixel

which will gives:

new_affine=Affine(a,b,c,d,e,f)

In addition, need to add a third dimension to the section array, because
rasterio expects [band,x,y] for its writer.  Do this with np.newaxis in the next cell

```{code-cell} ipython3
image_height, image_width = section.shape
ul_x, ul_y = ubc_ul_xy[0], ubc_ul_xy[1]
new_affine = Affine(30.0, 0.0, ul_x, 0.0, -30.0, ul_y)
out_section = section[np.newaxis, ...]
print(out_section.shape)
```

### Now write this out to band5_clipped_rasterio.tif

Note that the new file does have the utm zone 10 epsg code, since we use the pyproj utm and not the one we got from hls_band5.rio.crs

```{code-cell} ipython3
filename = 'band5_clipped_rasterio.tif'
tif_filename = data_dir / filename
#
# remove the file if it already exists
#
if tif_filename.exists():
    tif_filename.unlink()
num_chans = 1
with rasterio.open(
    tif_filename,
    "w",
    driver="GTiff",
    height=image_height,
    width=image_width,
    count=num_chans,
    dtype=out_section.dtype,
    crs=p_utm,
    transform=new_affine,
    nodata=0.0,
) as dst:
    dst.write(out_section)
    section_profile = dst.profile

print(f"section profile: {pprint.pformat(section_profile)}")
```

## Repeat the write with rioxarray

We can also write a geotiff with rioxarray.  To do that we first need to create the DataArray, then
add the attributes, coordinates, affine transform and crs, and then write it out using the `to_raster()` method

+++

(zoom_landsat_array)=
### Create the DataArray

In {numref}`sec:slice` we used slices to clip the subscene around UBC.  For rioxarray, we can use 
[clip_box](https://corteva.github.io/rioxarray/stable/rioxarray.html#rioxarray.raster_array.RasterArray.clip_box) to do
the same thing.  We need to provide the bounding box x and y edges we want to clip to, these are
given by (ubc_ul_xy, ubc_lr_xy).  clip_box wants them in the following order:

```
(ul_x, lr_y, lr_x, ul_y)
```

Below we unpack the x,y pairs and then put them into the right order.

```{code-cell} ipython3
ul_x, ul_y = ubc_ul_xy
lr_x, lr_y = ubc_lr_xy
bounding_box = (ul_x, lr_y, lr_x, ul_y)
print(f"{bounding_box=}")
```

In the call below I'm using the `*` operator to [unpack the tuple](https://www.w3schools.com/python/python_tuples_unpack.asp)

```{code-cell} ipython3
da_band5 = hls_band5.rio.clip_box(*bounding_box)
```

#### Check the shape, attributes and coordinates

clip_box clips the data, but it also clips the x,y coordinates so that we can still automatically
label our image with x and y tick marks

```{code-cell} ipython3
da_band5
```

### check the image

```{code-cell} ipython3
fig, ax = plt.subplots(1,1, figsize=(6,6))
da_band5.plot(ax=ax)
ax.set_title(f"Landsat band {band_name}");
```

(week3:write_clipped)=
### add the transform and the crs

```{code-cell} ipython3
da_band5.data.dtype
```

```{code-cell} ipython3
da_band5.rio.write_crs(p_utm, inplace=True)
da_band5.rio.write_transform(new_affine, inplace=True);
```

### change some attributes

We need to adjust some of the attributions for the new subscene.  To do this, copy the exiting attributes into
a dictionary and rewrite the parts you want to change, adding any extras.

```{code-cell} ipython3
new_attrs = da_band5.attrs
new_attrs['ULX']= ul_x
new_attrs['ULY'] = ul_y
band, nrows, ncols = da_band5.shape
new_attrs['NROWS'] = nrows
new_attrs['NCOLS'] = ncols
new_attrs['history'] = "written by the zoom_landsat notebook"
da_band5.rio.update_attrs(new_attrs, inplace = True);
```

#### check the attributes

```{code-cell} ipython3
da_band5.attrs['history']
```

### Write out the new geotiff

```{code-cell} ipython3
filename = 'band5_clipped_rio.tif'
filename = data_dir / filename
#
# remove the file if it already exists
#
if tif_filename.exists():
    tif_filename.unlink()
da_band5.rio.to_raster(filename)
```

### read it back in to check

```{code-cell} ipython3
has_file = filename.exists()
if not has_file:
    raise IOError(f"can't find {filename}, something went wrong above") 
small_band5 = rioxarray.open_rasterio(filename,masked=True)
fig, ax = plt.subplots(1,1, figsize=(6,6))
small_band5.plot(ax=ax)
ax.set_title(f"Landsat band {band_name}");
```

#### note that we now have the correct epsg code

Because we used the pyproj `p_utm` crs in our raster write we've fixed the missing epsg code problem.

```{code-cell} ipython3
small_band5.rio.crs
```

```{code-cell} ipython3

```
