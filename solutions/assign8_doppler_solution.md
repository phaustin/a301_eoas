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

(assign8_doppler_solution)=
# Assignment 8 doppler solution

+++

## Q1 

The attached color Doppler image shows a velocity pattern measured by Doppler radar with a wavelength of λ = 10 cm and a PRF of 2200 Hz. Using the space below the figure, plot the wind direction (with wind from the east at 90 degrees and wind from the west at 270 degrees) and the wind speed as functions of height, Assume that the outer range ring is at vertical elevation of 24 km and that the radar is at sea level, and pretend that the wind speed is in m/s, not knots. (so the blue colors start at -51 m/s and go in steps of 7 m/s towards zero then on to speeds of +51 m/s in the yellow).

+++

### Q1 Answer

This is similar to Stull Figure 8.38a, with the wind blowing into the radar (minus, blue/green) from the west/left and away from the radar (positive, yellow/read) on the right (east).  There is a maximum in the windspeed at an altitude of about 12 km with a spped of 51 m/s, falling to zero at the surface and about 24 m/s at 24 km.



+++

:::{figure} ./images/doppler_assign8.jpg
:name: doppler_fig
:scale: 100

Doppler velocity plot
:::

+++

## Question 2

Now assume that the the PRF is reduced to 1100 Hz. Describe qualitatively what the radar image would look like if it was not corrected for aliasing. You can draw contour lines on the map and verbally describe the color patterns inside the ring

+++

### Question 2 answer

From the equation sheet we know that:

$$
M_{r\,max} = \lambda \cdot \mathrm{PRF}/4
$$

So with the PRF at 2200 Hz, the maximum unambiguous velocity is 55 m/s.  Once the PRF is reduced to 1100 Hz, you would get aliasing for speeds above 27.5 m/s.  On the left, shades above green on the pallette would switch to orange/yellow and on the right the reverse would happen.

```{code-cell} ipython3
0.1*2200/4.
```

## Question 3

Find the smallest phase angle (magnitude and direction) between two pulses when the radial wind speed is 30 m/s and the PRF is at i) 1100 Hz and ii) 2200 Hz

+++

### Question 3 answer

From the equation sheet we know that 

$$
\frac{\Delta \phi} {2 \pi} = \frac{ 2d}{\lambda} = \frac{ -2 T_r M_r}{\lambda} 
$$ (delphi)

Note that if 

$$
M_r = M_{r\,max} = \lambda \cdot \mathrm{PRF}/4
$$

the {eq}`delphi` reduces to

$$
\frac{\Delta \phi} { \pi} =1
$$
That is, the maximum velocity is just enough to rotate the phasor through an angle of 180 degrees.

i) At 1100 Hz using {eq}`delphi` gives a phase difference of -196 degrees away from the radar.  That angle  would not be reported however, because of aliasing due to the fact that the phasor has rotated through more than 180 degrees.  The radar would incorrectly report the smaller postive phase difference of 360 - 196 = 164 degrees.  This would be interpreted as a speed of (164/180)*27.5 = 25 m/s towards the radar.

ii) At 2200 Hz {eq}`delphi` gives a phase difference of -98 degrees away from the radar. This is a smaller magnitude than 180 degrees so this would be intrepreted correctly as (98.5/180)*55 = 30 m/s away from the radar.

```{code-cell} ipython3
import numpy as np
Tr = 1/1100
Mr = 30
the_lambda = 0.1
del_phi = -4*np.pi*Tr*Mr/the_lambda
del_phi_deg = np.rad2deg(del_phi)
print(f"for 1100 Hz: {del_phi_deg=:0.1f} degrees")
del_phi_wrong = 360 + del_phi_deg
print(f"incorrect angle: {del_phi_wrong=:.1f}")
print(f"incorrect velocity {(del_phi_wrong/180)*27.5=:.1f} m/s towards the radar\n\n")
Tr = 1/2200
del_phi = -4*np.pi*Tr*Mr/the_lambda
del_phi_deg = np.rad2deg(del_phi)
print(f"correct angle for 2200 Hz: {del_phi_deg=:.1f} degrees")
print(f"correct velocity {(-del_phi_deg/180)*55=:.1f} m/s away from the radar")
```

## Question 4

+++

Find the maximum unambiguous range for this radar when the PRF is at i) 1100 Hz and ii) 2200 Hz

The equation:

$$
  MUR = \frac{c}{2 \cdot \mathrm{PRF}}
$$

See cell below

```{code-cell} ipython3
c=3e8  #m/s
prf = 1100
mur = c/(2*prf*1.e3)
print(f"at {prf} Hz the {mur=:.3g} km")
prf = 2200
mur = c/(2*prf*1.e3)
print(f"at {prf} Hz the {mur=:.3g} km")
```

```{code-cell} ipython3

```
