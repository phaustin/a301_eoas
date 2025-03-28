---
jupytext:
  formats: ipynb,md:myst
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

(assign7)=
# Assignment 7

## Classification part 1

- Make a jupyter notebook that reproduces the false color examples
  in{ref}`week10:false_color_examples` for your scene (you'll need to rerun  {ref}`week4:clip_bands` version 3 to get the clipped fmask, and rerun {ref}`week2:hls` to download all of the HLS tifs for bands 1,2,3,4,5,6,7,9,10,11,fmask if you don't have them).
- Choose one band combination that looks interesting, and compare it with the land classification you created using {ref}`week9:land_classes` for your image with the same bounding box and pixel size -- comment on an y similarities and differences you can find.  Is the classification accurate?

### Stull Radar problem

Answer the following questions in a Jupyter notebook, using a function to define the radar equation.

1. Suppose a Nexrad radar (Stull p.~246)  is
   receiving a signal with returned power Pr = -58 dBm.  Using the radar
   equation find the precipitation rate under the assumption that
   there is no attenuation and that it is a rainstorm (i.e. liquid water)
   100 km away from the radar.

2. Now keep everything the same, but make the mistake of guessing that it's a snowstorm,
   which means that K2=0.208 and we use the snowfall Z-RR relation
   of $Z=2000*RR^2$.  What is the new incorrect  precip rate?
   
3. Now assume it's rain, but make the mistake of guessing that there's a factor of La=2
   attenuation between the target and the rainstorm.  What is the new precip rate?

Nexrad coefficients:

```
    #coefficents for nexrad
    R1=2.17e-10#range factor, km, Stull 8.25
    Pt=750.e3 #transmitted power, W, stull p. 246
    b=14255 #equipment factor, Stull 8.26
```
