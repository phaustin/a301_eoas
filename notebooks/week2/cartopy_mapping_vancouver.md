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

- Download cartopy_mapping_buenos_aires.ipynb from the [week5 folder](https://drive.google.com/drive/folders/1-Ja2wVKVIjkZb7Gx_rfc14J_aBYiknuw?usp=sharing)


+++

## Create the UTM zone 21S CRS

Google says that Buenos Aires in in zone 22 South, which has an epsg code of 32721.


```{code-cell} ipython3
:trusted: true

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy
```

**Use matplotlib to draw the map and add a coastline**

```{code-cell} ipython3
:trusted: true

# silence geojson warnings
import warnings
warnings.filterwarnings("ignore")
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw={"projection": projection})
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="coarse", levels=[1, 2, 3]));
```

*  zoom in on vancouver

The next step is to pick an bounding box in map coordinates (the "extent") to limit the map area

The idea is to reduce the extent of the map to a region that is only a fraction
of the original full globe.  The strategy is to find a point in your swath and
get it's x,y coords, then use that to set the corners of the map so that
you have your region of interest

```{code-cell} ipython3
:trusted: true

#
# pick a bounding box in map coordinates
# (we know from the next cell that vancouver is located
# at x,y = -2_422_235, -3_721_768  so pick a bounding box
# based on that define abox that is 3200 km wide and 1600 km tall
#
xleft, xright = -4_000_000, -800_000
ybot, ytop = -4_700_000, -3_100_000
```

* Use the transform_point method to get x,y on this projection

This is how we put Vancouver (in lon,lat coords) on the map (in LAEA x,y coords)

We use the `projection.transform_point` method to get the lat/lon of Vancouver into map coordinates

```{code-cell} ipython3
:trusted: true

fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw={"projection": projection})
#
# clip with 0,0 in the center:  [xleft, xright, ybot, ytop]
#
new_extent = [xleft, xright, ybot, ytop]
ax.set_extent(new_extent, projection)
#
# the simple lon,lat projection is called "geodetic"
# transform this from geodetic into the projection ccrs.LambertAzimuthalEqualArea
# defined above
#
geodetic = ccrs.Geodetic()
van_x, van_y = projection.transform_point(van_lon, van_lat, geodetic)
ax.plot(van_x, van_y, "ro", markersize=10)
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="coarse", levels=[1, 2, 3]))
print(f"Vancouver map x, y: {van_x:.0f}, {van_y:.0f} meters");
```

## Now plot a location of your choice

As discussed in class, pick a point on the earth you're interested in, at least 1000 km away from Vancouver with
a coastline of more than 100 km.   Make a LAEA map with your point located with a red dot.  You will probably need to
define a new LAEA map projection with a better central lat/lon than the North Pole.

```{code-cell} ipython3
:trusted: true


```
