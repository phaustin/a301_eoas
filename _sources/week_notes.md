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

* [Instructions for Macs](https://www.dropbox.com/scl/fi/ribiztx2t2vzmbsxvnxyi/python-setup_macos_2024.pdf?rlkey=miqlz5fxeg6sqoiatp57461bz&st=5tu7kgwk&dl=0)
* [Instructions for Windows](https://www.dropbox.com/scl/fi/1zlod8dyqzj0qp23ge0hm/python-setup_windows_2024.pdf?rlkey=pwe8m5grzewselmhsk8bpzvef&st=7w0sp8h7&dl=0)

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
- For Assignment 1 (posted this evening, do next Monday at midnight)
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
- [download folder](https://www.dropbox.com/scl/fo/25w66p7nimcsm04dr1ce9/AOzTXQwlajVjByVQ7xWlgcA?rlkey=aup2jh41qqaposch0pn1fx0ed&st=609jtnta&dl=0)

#### Do for Friday

- Read Chapters 1 and 2 of [Understanding map projections](https://drive.google.com/file/d/1araPnZwMui9tBTPyLO_UHVC2DDEIdZ0p/view?usp=sharing)
- Finish {ref}`sec:cartopy` and {ref}`sec:vancartopy`

### Day 6 Friday

- Go over how to use rioxarray to plot a Landsat/Sentinel image of your choice:
  The notebook: {ref}`week2:hls`
