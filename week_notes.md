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

## Week 7

###  Day 19 Monday

- mid-term

### Day 20 Wednesday

Went over

- {ref}`week7:false_color`

#### Do for Friday

- Read Stull Chapter 8 through p. 239
- Start on Assignment 5a due Friday March 7:

  - Write a function that takes 3 tif files and returns a rioxarray false color image. Use it
to make a band 5,4,3 false color png file of your scene and upload the ipynb file

### Day 21 Friday

- {ref}`mid2024:sol`

- New version of {ref}`week4:clip_bands` that correctly saves the channel data as floating point
  numbers.  You'll need to rewrite your `clip_image` function using the approach
  of version 0.2 of the notebook in the week4 folder: see {ref}`clip:create_arrays`
  
  - See [the 9 rules of debugging](https://medium.com/@abhinav.ittekot/9-golden-rules-for-debugging-8e94d879e3db)
  
- New notebook: {ref}`week7:fmask`

  - the [Fmask algorithm](https://www.sciencedirect.com/science/article/pii/S0034425719302172)

#### Do for Monday


- Assignment 5b due Friday March 7

  - Write a function that takes an image and its fmask and returns a new image
    with all cloudy pixels set to np.nan.  Make a notebook that uses this function
    to plot a partly cloudy scene.


### Day 23 Monday

## Week 8

- {ref}`week8:install_part1`
- {ref}`week8:goes_true_color`

### Day 24 Wednesday

- {ref}`week8:goes_landsat`

#### Do for Friday

Read Stull Chapter 8 through p. 248 on weather radar

### Day 25 Friday

- New {ref}`week8:goes_landsat` with bug fixed
- New v0.2 of [a301_lib.py](https://github.com/phaustin/a301_lib/blob/main/src/a301_lib.py)
- {ref}`week8:goes_landsat_rio`
- {ref}`assign6`

#### For Monday

- Work on {ref}`assign6`
- Read {ref}`week8:radar` along with the Stull weather radar pages

## Week 9

### Day 26 Monday

- Working with bounding boxes

  - {ref}`week9:clip_demo`

- A land classification dataset
 
  - {ref}`week9:land_classes`
  
- More on the Schwartzchild equation: the diffuse flux approximation

  - {ref}`week9:diffusivity`
  - {ref}`week9:pydiffuse`

#### For Wednesday

- Get the land cover tif for your Landsat region
- work on {ref}`assign6`

Read:

- {ref}`week9:diffusivity`
- {ref}`week9:pydiffuse`

### Day 27 Wednesday

- {ref}`week9:diffusivity`
- {ref}`week9:pydiffuse`
- {ref}`week9:marshall`

#### Github part 1: ssh keys

You need to be able to pull and push files from your computer to the github server. Github
does this using [public key cryptography](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

1) log onto your github acount
2) clone [a301_lib](https://github.com/phaustin/a301_lib)
3) open a terminal and generate an ssh key  named a301key by doing:

   `ssh-keygen -f a301key`
   
4) move both your private key (a301key) and your public key (a301key.pub) into ~/.ssh
5) upload the a301key.pub to github following their instructions
6) download the ssh config file from our [gdrive installation folder](https://drive.google.com/file/d/1BlpJIw7Hr-uIAtjVk2VQli7WsVpyaqey/view?usp=drive_link)
7) if `~/.ssh/config` exists, add the lines from the gdrive file to your config file
8) if you don't have an ssh config, copy the gdrive config file to `~/.ssh`
9) test  your keys by doing:

   ```
   ssh a301git
   ```
   
10) clone the `a301_lib` repository by doing

   ```
   cd ~/repos
   git clone a301git:youraccountname/a301_lib
   ```
   
  
### Day 28 Friday

- {ref}`week10:false_color_examples`

#### Github part 2: packages

1) log into your github account
2) fork [https://github.com/phaustin/a301_extras](https://github.com/phaustin/a301_extras)
3) git clone a301git:youraccountname/a301_extras
4) checkout a working branch with your initials (mine are pha)
   ```
   git checkoout -b pha
   ```
5) install with

   ```
   pip install -e . --upgrade
   ```
6) test with

   ```
   python test_imports.py
   ```
   
7) add a new python file with your functions to the src/ folder

8) commit it to git with

   ```
   git add src/newfile.py
   git commit -am 'added new function'
   git push
   ```
   
#### For Monday

Read Stull through p. 255 on Doppler radar


## Week 10


### Day 29 Monday 

- Continue with false color notebook

- {ref}`week10:false_color_examples`

#### Working with google Collab and Gemini -- class demo

- [register for google earth engine -- create the project `ee-a301`](https://developers.google.com/earth-e]ngine/guides/access)
- [demonstration collab notebook](https://github.com/phaustin/a301_eoas/blob/main/notebooks/week10/read_landsat_ee.ipynb)

#### Assignment 7 -- due Monday March24 at midnight

- {ref}`assign7`

#### For Wednesday

- Read the [NOAA Doppler notes](https://drive.google.com/file/d/1893L784j7aXhY14_aFlXgbjS97uzaBai/view?usp=drive_link) through page 3.20

### Day 30 Wednesday

#### Assignment 6 solutions

- {ref}`assign6_solution`

#### Github part 3: merging changes from upstream (revised from Monday)


To get the new changes from my repository: [https://github.com/phaustin/a301_extras.git](https://github.com/phaustin/a301_extras.git) you need
to add it to the list of repositories you can pull code from.  By tradition, your own remote github
repository is called `origin` and the main remote repository that is the source of official releases is
called `upstream`.

To add a remote repository:

- First verify your remote is correct

  - cd `~/repos/a301_extras`
  - git remote -vv

    This should print something like:

    ```
    origin	yourgithubid:yourgithubid/a301_extras (fetch)
    origin	yourgithubid:yourgithubid/a301_extras (push)
    ```
  
- Next, add my repository as a remote

  - git remote add upstream https://github.com/phaustin/a301_extras.git
  - git remote -vv

  Now this should print
  
  ```
  origin	yourgithubid:yourgithubid/a301_extras (fetch)
  origin	yourgithubid:yourgithubid/a301_extras (push)
  upstream	https://github.com/phaustin/a301_extras.git (fetch)
  upstream	https://github.com/phaustin/a301_extras.git (push)
  ```

- make sure you're on your own main branch 
  - `git branch` shows an asterisk next to your current branch 
  - `git branch -a` lists both local and remote branches.
  - `git branch -vv` (for "very verbose") shows your current commits
  - `git remote -vv` shows where your origin branch is on github.
  
- move to your main branch  
  
  ```
  git checkout main
  git branch -a
  ```
  which should print out all your branches
  
- fetch the changes I've made to the official main branch on upstream
  ```
  git fetch upstream
  ```
- update your main branch with my changes using rebase
  ```
  git rebase upstream/main
  ```
- push your new rebased main to your github remote
  ```
  git push
  git branch -vv
  ```
  which should show you your updated local branch
  
- you'll need to continue working on your personal branch (which we named with your initials), rebase it on the new main branch
  ```
  git checkout yourinitials
  git rebase origin/main
  git push
  git branch -vv
  ```

  
- On github you should see a new week10 folder on your personal branch that should look like mine:

  - [https://github.com/phaustin/a301_extras/tree/main/notebooks/week10](https://github.com/phaustin/a301_extras/tree/main/notebooks/week10)  -- you'll be able to edit and track changes in this notebook on collab
    
- If instead you are done with your personal branch, delete it from github and 
  delete it from your local repository
  ```
  git push -d origin yourinitials
  git checkout main
  git branch -d yourinitials
  git branch -vv
  ```

####  Github and Collab

- To edit my week10 Collab notebook first log into collab:

  - go to [https://colab.research.google.com/](https://colab.research.google.com/)
  - click on `open collab` and then from the `file` dropdown click on `open notebook`
  - click on the github tab, and enter your github username
  - select the `a301_extras` repository, and your personal branch
  - select `read_landsat_ee.ipynb`
  - now any changes you save will appear as github commits to this file
  - Alternatively, you could copy the file to your google drive, or upload it, but then you couldn't
    track/recover changes
  - work through read_landsat_ee.ipynb
    
#### Doppler notes

- Two short reviews on phase and the unit circle
  - {ref}`phasor_examples`
  - {ref}`phase_shiftb`

##### Read for Friday

-  [my doppler notes](https://drive.google.com/file/d/13rMkduBy7Q68DW5UVXUdkgo48AmbmMDW/view?usp=drive_link)
   (note my disagreement with Stull Figure 8.32, which doesn't show a phase shift in the reflected wave.  See [slide 6 of these slides](https://www.amherst.edu/system/files/media/1172/Lecture36%2520slides.pdf).  It won't matter
   for pulse-pair doppler radar however, because we are comparing two pulses that have both been reflected off of water drops.
   
   
### Day 31 Friday

- Important concepts from Stull 8.3.1 and 8.3.2
  - Size of radar sample volume
  - Maximum unambiguous range (MUR)
  - Z-RR relationship
  - Radar equation
  - bright band
  
- Review my {ref}`week8:radar` questions
- Review [my doppler notes](https://drive.google.com/file/d/13rMkduBy7Q68DW5UVXUdkgo48AmbmMDW/view?usp=drive_link)
- Compare the Nexrad radar (700,000 Watts, 8.5 meter diameter dish) with
  the [Earthcare satellite](https://drive.google.com/file/d/1ZQ_uq4SIm_phs9y-doRlhA8uNSwxKv4q/view?usp=drive_link)
  
#### Do for Monday

- Finish - {ref}`assign7`

## Week 11

### Day 32 Monday

- {ref}`assign5_solution`
- {ref}`week11:goesrgb2`
- {ref}`week11:stability`


#### Do for Wednesday

- Start on the [Assignment 8 doppler problem](https://drive.google.com/file/d/1OrIQnwRJGdkDhQyKtjNVtlctEZH0EgJc/view?usp=drive_link) using the [NOAA Doppler notes](https://drive.google.com/file/d/1893L784j7aXhY14_aFlXgbjS97uzaBai/view?usp=drive_link)


### Day 33 Wednesday

- Go over how to approach the the [Assignment 8 doppler problem](https://drive.google.com/file/d/1OrIQnwRJGdkDhQyKtjNVtlctEZH0EgJc/view?usp=drive_link)
  using the first guess/second guess phasor discussion from the [NOAA Doppler notes](https://drive.google.com/file/d/1893L784j7aXhY14_aFlXgbjS97uzaBai/view?usp=drive_link)

- Introduce the earthcare cases:  {ref}`week11:earthcare` 

#### Do for Friday

Use code in the {ref}`week8:goes_landsat_rio` notebook to find a GOES 16 image that is taken
as close as possible to your earthcare radar segment.  Plot the truecolor image using the
goes2go rgb module, clip it to a reasonable lat, lon square and overlay your earthcare
groundtrack

### Day 34 Friday

- {ref}`week11:earthcare_xarray`
- {ref}`week11:stull_radar_solution`
- {ref}`week11:phasor_notes2`


## Week 12

### Day 35 Monday

- {ref}`final-guide`
- [Practice final 2014](https://drive.google.com/file/d/17jhwpTbpT21fCBCqhatxccmA_tm8NJD9/view?usp=drive_link)
- [Practice final 2022](https://drive.google.com/file/d/1P--fLrVzcd18l8QSxjjs7YbyMv9889fC/view?usp=drive_link)
- {ref}`assign7_solution`
- {ref}`week12:goes_earthcare`
- {ref}`week12:assign8`

### Day 36 Wednesday

- {ref}`week12:goes_temperature`

### Day 37 Friday

- FYI: Interesting links we didn't have time for
  - [Developing a classifier using random forests with sentinel 2
](https://projectpythia.org/eo-datascience-cookbook/notebooks/templates/classification.html)
  - [Synthetic aperture radar SAR with sentinel 1](https://projectpythia.org/eo-datascience-cookbook/notebooks/courses/microwave-remote-sensing.html)
  - [SAR flood detection with sentinel 1](https://projectpythia.org/eo-datascience-cookbook/notebooks/courses/microwave-remote-sensing.html)
  
  - And a good intro to [stac and open data cube (odc)](https://www.geocorner.net/post/are-you-still-downloading-satellite-images-stop-and-stac-part-2)

  - [odc-geo xarray plugin](https://odc-geo.readthedocs.io/en/latest/intro-xr.html)

- Go over {ref}`final_2014_answers`

### For Monday

Send me an email on canvas with your preferred start day and time for your 4 day window. Needs to be between Monday April 7 and Tuesday April 15.

## Week 13

- Go over {ref}`assign8_doppler_solution`
- Go over {ref}`assign8_goes_solution2`
- Added the [2010 final exam](  https://drive.google.com/file/d/1_uypEFfAluDzxdt2_Eu07lYfJj7aafFa/view?usp=drive_link)

### do by Wednesday

- hand in your update Assignment 8 part b satellite notebook for partial credit (and to get ready for the takehome exam)
- send me your start time for the takehome via canvas email

### do before final

- post your solutions to final exam practice questions on piazza



