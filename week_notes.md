(sec:weekly)=
# Week notes

## Week 1

### Getting started

* {ref}`syllabus`

### Some of our satellites

* [Landsat](https://landsat.gsfc.nasa.gov/satellites/landsat-9/)

* [GOES](https://www.goes-r.gov/products/baseline-cloud-moisture-imagery.html)

* [The A-train](https://atrain.nasa.gov/)

* [Earthcare](https://earth.esa.int/eogateway/missions/earthcare/description)

### Installing python on your laptop

* [Instructions for Macs and Windows in "Installation"](https://drive.google.com/drive/folders/1-Ja2wVKVIjkZb7Gx_rfc14J_aBYiknuw?usp=sharing)

#### Do for Wednesday's class:

* Sign up for piazza using the link on [canvas](https://canvas.ubc.ca/courses/158920)

* Read [Stull Chapter 2, pp. 34-40](https://www.eoas.ubc.ca/books/Practical_Meteorology/prmet102/Ch02-radiation-v102b.pdf)

* Read my extra notes on the material covered on pp. 38-39: {ref}`week1-beerslaw`

### Day 2 Wednesday

- Learning objectives

  - Explain the relationship between the monochromatic radiance and the monochromatic irradiance
  - Why are both variables necessary?
  - How would you measure them with a satellite radiometer?
 
* Reading: {ref}`week1-beerslaw` and {ref}`radiance`

#### Do for Friday's class

- Read
  
  - All of {ref}`week1-beerslaw` and {ref}`radiance`
  - [Stull](https://www.eoas.ubc.ca/books/Practical_Meteorology/prmet102/Ch02-radiation-v102b.pdf) pp. 34-43
  - [WH Chapter 4](https://gw2jh3xr2c.search.serialssolutions.com/?sid=sersol&SS_jc=TC0000517195&title=Atmospheric%20Science%3A%20An%20Introductory%20Survey) pp. 113-118
 
### Day 3 Friday

- Note syllabus change: Midterm is now Monday, Feb. 24 -- {ref}`syllabus`
- [Thermodynamic humour](https://m.xkcd.com/3032/)
- Go over {ref}`sec:week1-flux-from-radiance`


#### Do for Monday

- Read Wallace and Hobbs Section 4.3
- Download and run {ref}`sec:planck` and modify it to reproduce Wallace and Hobbs Figure 4.6


## Week 2

### Day 4 Monday

- Select [office hours](https://whenisgood.net/xj4khmm/results/4sfd25r) -- 11am Wed?
- Go over {ref}`week1-review`
- Get accounts on the [NASA earthdata website](https://urs.earthdata.nasa.gov/home)

#### Do for Wednesday

- Finish reading Wallace and Hobbs Section 4.3
- For Assignment 1 (posted this evening, do next Tuesday at 5 pm)
  - Unwrap the Planck function for temperature T and code this in Python.  That is, given W&H equation 4.4:
  
  $$
  B_\lambda(T)=\frac{c_1 \lambda^{-5}}{\pi\left(e^{c_2 / \lambda T}-1\right)}
  $$
  
  Solve for the "brightness temperature" $T_b$ such that, given a radiance $I_\lambda$:
  
  $$
  B_\lambda(T_b) = I_\lambda
  $$
  
  i.e.  find the temperature that a black body would need to have to emit $I_\lambda$ at wavelength $\lambda$
  
  Check your work by "round tripping"  -- find the radiance at a temperture $T$ using the Planck function, then insert that temperture into your brightness temperature function to make sure you get back that radiance.
  
### Day 5 Wednesday

#### Review/Announcements

- {ref}`sec:assign1` is posted on canvas, due Tuesday, Jan 21 at 5pm

- Review {ref}`sec:planck_sol`

- Review: $\cos \theta$ for stream flow

- [ESSA career fair registration (Tuesday evening Jan 21)](https://docs.google.com/forms/d/e/1FAIpQLSft_f1UuDeSllvymipSk1xeUPTqhlOEDEJk1n7TbQr7bGEzuQ/viewform)
 
Today we shift from radiation to mapping, and cover some notebooks about the use of the cartopy mapping package.


#### Making maps

- [Another xkcd classic: map projections](https://xkcd.com/977/)
- Reading for Friday: Chapters 1 and 2 of [Understanding map projections](https://drive.google.com/file/d/1araPnZwMui9tBTPyLO_UHVC2DDEIdZ0p/view?usp=sharing)
- In class: {ref}`sec:cartopy`
- In class: {ref}`sec:vancartopy`
- [download folder](


#### Do for Friday

- Read Chapters 1 and 2 of [Understanding map projections](https://drive.google.com/file/d/1araPnZwMui9tBTPyLO_UHVC2DDEIdZ0p/view?usp=sharing)
- Finish {ref}`sec:cartopy` and {ref}`sec:vancartopy`

### Day 6 Friday

- Go over how to use rioxarray to plot a Landsat/Sentinel image of your choice:
  The notebook: {ref}`week2:hls`

#### Do for Monday

- Download a band 4 (red) tif file for your scene


## Week 3

### Day 7 Monday

- Go over {ref}`windows_install`
- Put an image on a map with {ref}`week3:map_landsat`

#### Do for Wednesday

- New consolidated review page started at {ref}`week-review`
- start on [Assignment 2](https://canvas.ubc.ca/courses/158920/assignments/2088849)
- Review Wallace and Hobbs Section 4.3.5 and 4.3.6 on Kirchoff's law and the greenhouse effect
- Read Wallace and Hobbs Section 4.4

### Day 8 Wednesday

- {ref}`asign1:planck_solution`
- Fixed the bug in {ref}`week3_bug`
- New notebook on clipping an image region: {ref}`week3:image_zoom`
- In-class worksheet: {ref}`week3:kirchoff`

#### Do for Friday

- Clip an interesting region and make sure your coastlines are correct
- Write the region to a new geotiff
- Read Wallace and Hobbs Section 4.5

### Day 9 Friday

- I've added the rioxarray `to_raster` example to show how to write a geotif with rioxarray in {ref}`week3:image_zoom`
- Do the {ref}`week3:kirchoff`
- Go over {ref}`week3:tau` with the setup for Wallace and Hobbs Problem 4.39

#### Do for Monday

- Finish Assignment 1
- Write out clipped geotifs for your band 4 and band 5 images



