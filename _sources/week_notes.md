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

## Week 4

### Day 10 Monday

- More on optical depth: linking the mean free path to $\tau = 1$
  - {ref}`week4:tau2`
- New notebook -- how to write several clipped images given a bounding box
  - {ref}`week4:clip_bands`
- Assignment 3 due next Tuesday midnight
  - {ref}`assign3`

#### Do for Wednesday

- Do Wallace and Hobbs problem 4.44 with pencil and paper
- Start on {ref}`assign3`
- Read Wallace and Hobbs through p. 133

### Day 11 Wednesday

- Discussion: what happened to $\cos \theta$ in problem 4.31?:

  $$
  d E=\pi r^2 I d \omega
  $$
  
- If you're interested/motivated, try {ref}`pixi_install`
- Finish: {ref}`week4:tau2`
- Finish: {ref}`week4:clip_bands`
- In-class coding:

  Write a function with the following signature:

  ```
  def find_latlon(geotiff,column,row):
      '''
      Given the path to a geotiff file, use the geotiff crs and affine transform
      to return the longitude and latitude of the center of the pixel at
      (row, column)

      Parameters
      ----------

      geotiff: pathlib.Path
         path to a local geotiff file

      row: float
         row of the pixel in the raster
      column: float
         column of the pixel in the raster

      Returns
      -------

      lonlat: (float, float)
        longitude and latitude of the pixel center
   ```

#### Do for Friday

- Test find_latlon on one of your clipped images
- Read WH through p. 132  -- especially eq. 4.37

### Day 12 Friday

- Introduce {ref}`notebook_index`
- {ref}`assign2a_solution`
- Finish `find_latlon` 

#### Do for Monday

- Work on Assignment 3
- As part of  assignment 4, we'll write a `clip_image` function which takes a geotiff and a bounding box and writes out a clipped geotiff


## Week 5

### Day 13 Monday

- Note the new {ref}`mid-review1b`
- Go over {ref}`assign2b_solution`
- My version of {ref}`week5:rowcol2latlon`

### Do for Wednesday

- Read Stull Chapter 8 pp. 219-226 together with:

  - {ref}`week5-schwartzA`
  - work on your version of `clip_image`.  We want it to take a geotiff and two
    slice objects (desired rows and columns) and write a new, smaller geotiff
    with the raster selected using those two slices.
    
###  Day 14 Wednesday

Topics:

- {ref}`assign4` due midnight next Wednesday
- {ref}`assign2c_solution`
- In-class: {ref}`mid-review1b` problem A.1 and A.2
- Continue with {ref}`week5-schwartzA`
- {ref}`hydro`
- {ref}`week5:add_palette`
    
###  Day 15 Friday

- [Environment Canada Meteorology Scholarships](https://portal.scholarshippartners.ca/welcome/Meteorology-Awards/)
- {ref}`sec:bacartopy`
- Introduce {ref}`mid-review2`
- Go over Wallace and Hobbs Figure 4.24 -- Beer's law
- Continue with {ref}`week5-schwartzA`

#### Do for Monday

- Work on {ref}`assign4` and other midterm practice problems
- Upload assignment 3 fixed images if you were having cartopy problems

## Week 6

###  Day 16 Monday

- [2022 mid-term](https://drive.google.com/file/d/12ZDN8NZzgafeCMDTy4t0u-w80o3-foNT/view?usp=sharing)
- {ref}`assign3_solution`
- {ref}`week6:scale_heights`
- {ref}`week6:weighting_funs`

#### Do for Wednesday

- Work on {ref}`assign4` and other midterm practice problems

###  Day 17 Wednesday

- {ref}`heating-rate`
- Assignment 4 questions
- Midterm review questions

#### Do for Friday

- Midterm review

###  Day 18 Friday

- [radiation in the news](https://www.washingtonpost.com/climate-environment/2025/02/14/global-warming-acceleration-clouds/)
- {ref}`mid-review1-sol`
- {ref}`mid-review2-sols`
- {ref}`assign4-2laysol`

- All Assignment 4 solutions: {ref}`assign4_solution`


