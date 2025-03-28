(phasors)=

# Notes on phasors

How do radars measure the phase $\phi$ of a returning pulse?

1. The radar measures the returned pulse by converting voltages into digital data with an
   analog to digital converter. This only gives us a single piece of information (called the "in-phase" signal which is $\cos \phi$ ), which
   isn't enough to get both the amplitude and phase of the return. We need to make a second measurement
   so we can read off the phase angle $\phi$

2. How do you get the second (Quadrature) component of the phasor? A schematic is shown on
   in [this radar tutorial](http://www.radartutorial.eu/10.processing/sp06.en.html) The details
   aren't too important, but the essential facts are that the pulse is split and sent into two circuits, one
   that passes the signal through unshifted (and measures $cos(\phi)$, and one that electonically adds a +90 degree
   phase shift, to move the pulse into another quadrant on the phasor diagram (which is why it's
   called the quadrature component). As the diagram in the above web page indicates, this phase shifted component records $-\sin(\phi)$. Remember that $d \cos(x)/dx = -\sin(x)$ -- this means that adding a phase shift of 90 degrees is the same as taking the derivative of the cosine.

   Consider this specific example:

   ```{image} figures/phase_shift90.png
   :scale: 80
   ```

   The dotted wave is the in-phase returning pulse which is recorded with a voltage of 0.866 in the A-D converter (where
   we've normalized the voltage so it goes betwee -1 and 1 in some units). Without more information, this single measurement
   is consistent with a phase shift of either +30 degrees or -30 degrees, since cos(+30deg)=cos(-30deg) = 0.866.
   The quadrature wave arrives at the converter with a 90 degree phase shift, which means that it records a voltage
   of -0.5. Turning this into an angle requires the following trig relation:

   $$
   \cos(\phi + \pi/2) = -sin(\phi)
   $$

   so if $\cos(\phi)= 0.866$ (the in-phase measurement) and
   $\cos(\phi + \pi/2) = -sin(\phi) = -0.5$ (the quadrature measurement)
   then we know $sin(\phi) = 0.5$ and the phasor has to lie in the
   northeast quadrant, as shown here by the green line, with the black line showing
   the 90 degree phase shift:

   ```{image} figures/myshift.png
   :scale: 80
   ```

(pulse-pair-problem)=

## Doppler pulse-pair problem

- A cloud radar operates at $\lambda$ =10 cm with a PRF of 600 $s^{-1}$
  This figure shows the in-phase (coherence) plots of two wavetrains returning from a pulse pair
  separated by 1/600th of a second.

  ```{image} figures/final_phase.png
  :scale: 30
  ```

  1. Find the values of I ($\cos(\phi)$) and Q ($-\sin(\phi)$) for the two pulses, and use them to find the phase angle for each pulse. Draw the two phase angles on a phasor plot.
  2. Calculate a *first guess* radial velocity with direction, plus two other
     velocities that are also consistent with this pulse pair, explaining your reasoning.

- Hint -- I found this equation in the {ref}`doppler`

  $$
  \frac{ \phi_2 - \phi_1}{2 \pi} = \frac{2d }{\lambda}
  = \frac{-2 T_r M_r }{\lambda} = \frac{ -2M_r}{\lambda PRF}
  $$ (phi2)

  to be useful.

## Extra -- euler notation

Not required but kind of interesting. Remember in grade 12 (?) you learned about
the [euler notation](http://www.mathsisfun.com/algebra/eulers-formula.html) for
complex numbers.

- Some trigonometry facts:

  $$
  \exp(x) = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^4}{4!} + \ldots

  \exp(ix)= 1 + ix - \frac{x^2}{2!} - i\frac{x^3}{3!} + \frac{x^4}{4!} + \ldots

  \cos(x) = 1 - \frac{x^2}{2!} + \frac{x^4}{4!}  + \ldots

  \sin(x) = x - \frac{x^3}{3!} + \frac{x^5}{5!}  + \ldots

  \text{so this means: }

  \exp(ix) = cos(x) + i sin(x)
  $$

- Some facts about complex numbers

  - Any complex number can be written in either cartesian or euler form:

    $$
    \text{Cartesian: }

    I = x + iy

    \text{Euler: }

    I=A \exp(i \phi) = A\cos( \phi) + Ai\sin(\phi)

    \text{where: }

    A^2 = x^2 + y^2

    \text{and: }

    \phi = \arctan(y/x)
    $$

- Put these together:

  $$
  i=\exp \left (i \frac{\pi}{2} \right )

  \frac{d \exp(i\phi)}{d\phi} = i \exp(i\phi) = \exp\left (i\frac{\pi}{2} \right ) \exp(i\phi) = \exp \left (i \left ( \phi + \frac{\pi}{2} \right ) \right )
  $$

  so adding a positive phase shift of $\pi/2$ is the same thing as taking the derivitive. To get the phase of the pulse
  in the proper quadrant, you measure two real voltages at the A-D converter: $I=A\cos(\phi)$, which is called the **in-phase** component, and
  $Q= -A\cos(\phi + \frac{\pi}{2}) = A \sin(\phi)$ which is called the **quadrature** component. This is equivalent
  to finding the real part of $I$ and the real part of its derivitive, which gives it a unique quadrant location.

(pulse-pair-solution)=

## Doppler pulse-pair problem solution

- Repeat the figure for the problem:

  ```{image} figures/final_phase.png
  :scale: 30
  ```

- For pulse 1 I read I = $\cos(\phi)$ = -1, so we know that the phase angle for the pulse $\pm \pi$.

- If I take the derivitive of pulse 1 by adding a phase shift of $\pi/2$ I get $\cos(\phi + \pi/2) = Q = -\sin(\phi)$ = 0,
  so $\sin(\phi)$ = 0 which is consistent with $\phi = \pm \pi$ for pulse 1.

- For pulse 2 I have I= $\cos(\phi)$ = +0.5, so $\phi$ is either 60 degrees or 300 degrees.

- If I take the derivitive of pulse 2 by adding a phase shift of $\pi/2$ I get $\cos(\phi + \pi/2) = Q = -\sin(\phi)$ = +0.866,
  so $\sin(\phi)$ = -0.866 and $\phi =$ 300 degrees for pulse 2.

- Here is pulse 1 (cyan) and pulse 2 (green) on the phasor

  ```{image} figures/wednesday_pair.png
  :scale: 80
  ```

- The first guess velocity goes to the smallest phase angle, which is the increase from 180 to 300 degrees = 120 degress.
  So the first guess velocity is positive (away from the radar). From (10) in
  my [Doppler notes] we know that with $\lambda$ =10 cm and PRF = 600 Hz:

  $$
  M_{rmax} = \frac{\lambda PRF}{4} = \frac{0.1 * 600}{4} = 15\ m/s
  $$

  This is the speed corresponding to a 180 degree phase shift, so a +120 degree (counter-clockwise) phase shift
  would be $120/180 \times (15\ m/s)$ = -10 m/s towards the radar. Two other possibilites are
  that the phase shift is really -240 degrees (from -180 to -420), so that the velocity would be
  $240/180 \times (15\ m/s)$ = 20 m/s away from the radar, or (360 + 120 = 480) degrees, so that the velocity
  would be $480/180 \times (15\ m/s)$ = 40 m/s into the radar.

(doppler-sol)=

## Doppler problem solution

```{image} figures/final_doppler_0_0.png
```

1. The attached color Doppler image shows a velocity pattern measured by
   Doppler radar with a wavelength of $\lambda=10$ cm and a PRF of
   2200 Hz. Using the space below the figure, plot the wind direction
   (with wind from the east at 90 degrees and wind from the west at 270
   degrees) and the wind speed as functions of height, Assume that the
   outer range ring is at vertical elevation of 24 km and that the radar
   is at sea level, and pretend that the wind speed is in m/s, not
   knots. (so the blue colors start at -51 m/s and go in steps of 7 m/s
   towards zero then on to speeds of +51 m/s in the yellow).

1) Answer -- range rings at elevations of 12 km and 24 km, so wind is
   blowing west to east with a maximum at 18 km of about 30 m/s
2) Now assume that the the PRF is reduced to 1100 Hz. Describe
   qualitatively what the radar image would look like if it was not
   corrected for aliasing. You can draw contour lines on the map and
   verbally describe the color patterns inside the ring.

2. Answer: first find mrmax and MUR for the two PRFs

```python
the_lambda=0.1
c=3.e8
PRF=2200
mrmax=the_lambda*PRF/4.
MUR=c/(2.*PRF)*1.e-3
print("At a PRF of {} Hz, the mrmax is {} m/s and the MUR is {} km".format(PRF,mrmax,MUR))
```

```{eval-rst}
.. parsed-literal::

    At a PRF of 2200 Hz, the mrmax is 55.0 m/s and the MUR is 68.1818181818 km

```

```python
PRF=1100
mrmax=the_lambda*PRF/4.
MUR=c/(2.*PRF)*1.e-3
print("At a PRF of {} Hz, the mrmax is {} m/s and the MUR is {} km".format(PRF,mrmax,MUR))
```

```{eval-rst}
.. parsed-literal::

    At a PRF of 1100 Hz, the mrmax is 27.5 m/s and the MUR is 136.363636364 km

```

So there will be aliasing once the wind speed exceeds 27.5 m/s. The
maxium wind speed of 30 m/s is to produce a phase angle of:

```python
delta_phi=30/27.5*180.
print("phase angle for 30 m/s is {} degrees".format(delta_phi))
print("radar will display this as {} degrees in opposite direction".format((360. - delta_phi)))
print("the magnitude of the aliased velocity will be {} m/s".format((360. - delta_phi)/180.*mrmax))
```

```{eval-rst}
.. parsed-literal::

    phase angle for 30 m/s is 196.363636364 degrees
    radar will display this as 163.636363636 degrees in opposite direction
    the magnitude of the aliased velocity will be 25.0 m/s

```

So the diagram will change color from blue to red or from red to blue at
the 27.5 m/s isoline with the displayed windspeed decreasing from 27.5
to 25 m/s as it actually increases from 27.5 to 30 m/s

3. Find the smallest phase angle (magnitude and direction) between two
   pulses when the radial wind speed is 30 m/s and the PRF is at i) 1100
   Hz and ii) 2200 Hz

```python
text="""At 2200 Hz, the mrmax is 55 m/s and the smallest phase angle for 30 ms is: {:5.2f} degrees
        At 1110 Hz, the mrmax is 27.5 m/s and the smallest phase angle for 30 m/s is {:5.2f} degrees
     """
print(text.format((30/55.*180.),(360. - (30./27.5*180.))))
print(98.18*np.pi/180.)
print(163.64*np.pi/180.)
```

```{eval-rst}
.. parsed-literal::

    At 2200 Hz, the mrmax is 55 m/s and the smallest phase angle for 30 ms is: 98.18 degrees
            At 1110 Hz, the mrmax is 27.5 m/s and the smallest phase angle for 30 m/s is 163.64 degrees

    1.71356425961
    2.85605678796

```

4. Find the maximum unambiguous range for this radar when the PRF is at
   i) 1100 Hz and ii) 2200 Hz.

As calculated above, at 2200 Hz the MUR is 68.1 km and at 1100 Hz the
MUR is 136.6 km
