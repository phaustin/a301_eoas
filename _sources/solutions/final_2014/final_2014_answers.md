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

(final_2014_answers)=
# 2014 final solutions

+++

## 2014 final question 3

See {ref}`week11:phasor_notes2`

+++ {"jupyter": {"outputs_hidden": false}}

A cloud radar operates at $\lambda=10\ cm$ with a PRF of 600 $s^{-1}$.
This figure shows the in-phase (coherence) plots of two wavetrains returning from a pulse pair
separated by 1/600th of a second.


:::{figure} ./phase_shift_final.png
:name: phase_shift
:scale: 100

Doppler pulse pair
:::

+++ {"jupyter": {"outputs_hidden": false}}

a) (4)  Find the values of I and Q for the two pulses, and draw them on
a phasor plot.  The values at x = 0 are 0.707 for pulse 1 and -0.866 for pulse 2

```{code-cell} ipython3
---
jupyter:
  outputs_hidden: false
---
import numpy as np
from numpy import pi,exp,cos,deg2rad,rad2deg
import matplotlib.pyplot as plt
```

```{code-cell} ipython3
---
jupyter:
  outputs_hidden: false
---
phi1, phi2 = rad2deg(np.arccos(0.707)), rad2deg(np.arccos(-0.866))
phi1, phi2
```

At this point we know they are both on the right side (postive cosine), but
we don't know whether they are in the top or bottom quadrant, because we 
don't know the sin.

+++

## Now phase shift by 90 degrees


```{code-cell} ipython3
Q1, Q2 = -np.sin(deg2rad(phi1)), -np.sin(deg2rad(phi2))
Q1, Q2
```

So `sin(phi1) = 0.707` and `sin(phi2) = 0.5`

This means that both angles are in the upper quadrant, and
phi1 = 45 degrees and phi2 = 150 degrees

+++ {"jupyter": {"outputs_hidden": false}}

see 

b) (4)  Calculate a "first guess" radial velocity with direction, plus two other 
velocities that are also consistent with this pulse pair, explaining your reasoning.

+++

10 cm = 0.1 m
positive angles are into the radar, negative angles are away from the radar

```{code-cell} ipython3
mrmax=0.1*600./4.
#smallest angle is 150 - 45.
angle=150 - 45.
vel1 = (150. - 45.)/180.*15  #8.75 m/s into the radar
print(f"{vel1=} m/s")
#second guess
angle2= angle - 360
vel2 = (angle2)/180.*15 #away from the radar
print(f"{vel2=} m/s")
```

+++ {"jupyter": {"outputs_hidden": false}}

c) (5) Derive the doppler equation for the maximum unambiguous velocity with the help of a phasor diagram.

$$
\frac{\Delta \phi} {2 \pi} = \frac{ 2d}{\lambda} = \frac{ -2 T_r M_r}{\lambda} 
$$

+++ {"jupyter": {"outputs_hidden": false}}



+++ {"jupyter": {"outputs_hidden": false}}



+++ {"jupyter": {"outputs_hidden": false}}



+++

## Code

```{code-cell} ipython3
---
jupyter:
  outputs_hidden: false
---
thetime=np.arange(0.,2.5*pi,0.05)
thewave=thetime
four5=45.*pi/180.
thirty=30*pi/180.
sixty=2.*thirty
onefifty=5.*thirty


fig1,axis1=plt.subplots(1,1)
axis1.plot(thewave,np.cos(thetime + four5),'k-',lw=5,label='pulse 1')
axis1.plot(thewave,np.cos(thetime + onefifty),'k+',lw=5,label='pulse 2')
axis1.set_xlabel('horizontal position (one wavelength=2pi)')
axis1.set_ylabel('amplitude')
axis1.set_title(' ')
pos=[0.,0.25*pi,0.5*pi,0.75*pi,1.*pi,1.25*pi,1.5*pi,1.75*pi,2*pi,2.25*pi]
labels=['0','pi/4','pi/2','3pi/4','pi','5pi/4','6pi/4','7pi/4','2pi','9pi/4']
axis1.grid()
axis1.set_xticks(pos)
axis1.set_xticklabels(labels)
axis1.legend(loc='best')
fig1.savefig('phase_shift_final.png')
```

```{code-cell} ipython3
---
jupyter:
  outputs_hidden: false
---
#pulse1
I=0.707
Q= -(0.707) # = 0.707
#pulse2
I=-0.866
Q=-(-0.5) #=0.5
#first angle= +45
#pulse2=150 degrees
mrmax=0.1*600./4.
```

```{code-cell} ipython3
---
jupyter:
  outputs_hidden: false
---
mrmax
```

```{code-cell} ipython3
np.cos(150/180.*np.pi)
np.cos(240/180.*np.pi)
```

```{code-cell} ipython3
---
jupyter:
  outputs_hidden: false
---
#smallest angle is 150 - 45.
(150. - 45.)/180.*15  #8.75 m/s into the radar
angle=150 - 45.
#second guess
angle2=360. - angle
(angle2)/180.*15 #away from the radar
```
