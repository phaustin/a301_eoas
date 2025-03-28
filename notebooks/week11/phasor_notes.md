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


(week11:phasor_notes2)=
# Notes on phasors 

How do radars measure the phase $\phi$ of a returning pulse?

1.  The radar measures the returned pulse by converting voltages into digital data with an
    analog to digital converter. This only gives us a single piece of information (called the "in-phase" signal which is $\cos \phi$ ), which
    isn't enough to get both the amplitude and phase of the return. We need to make a second measurement
    so we can read off the phase angle $\phi$

2.  How do you get the second (Quadrature) component of the phasor? A schematic is shown on
    in [this radar tutorial](https://www.radartutorial.eu/10.processing/sp06.en.html) The details
    aren't too important, but the essential facts are that the pulse is split and sent into two circuits, one
    that passes the signal through unshifted (and measures $cos(\phi)$, and one that electonically adds a +90 degree
    phase shift, to move the pulse into another quadrant on the phasor diagram (which is why it's
    called the quadrature component). As the diagram in the above web page indicates, this phase shifted component records $-\sin(\phi)$. Remember that $d \cos(x)/dx = -\sin(x)$ -- this means that adding a phase shift of 90 degrees is the same as taking the derivative of the cosine.

    Consider this specific example:

:::{figure} ./figures/phase_shift90.png
:name: phase90
:scale: 80

90 degree phase shift
:::

The dotted wave is the in-phase returning pulse which is recorded with a voltage of 0.866 in the A-D converter (where
we've normalized the voltage so it goes between -1 and 1 in some units). Without more information, this single measurement
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

:::{figure} ./figures/myshift.png
:name: secondphase
:scale: 80

Quadrature
:::



## Practice dopper problem

-   A cloud radar operates at $\lambda$ =10 cm with a PRF of 600 $s^{-1}$
    This figure shows the in-phase (coherence) plots of two wavetrains returning from a pulse pair
    separated by 1/600th of a second.

:::{figure} ./figures/final_phase.png
:name: Dopler problem
:scale: 30

Quadrature
:::

1.  Find the values of I ($\cos(\phi)$) and Q ($-\sin(\phi)$) for the two pulses, and use them to find the phase angle for each pulse. Draw the two phase angles on a phasor plot.
2.  Calculate a *first guess* radial velocity with direction, plus two other
    velocities that are also consistent with this pulse pair, explaining your reasoning.

-   Hint -- I found equation (9) in the [doppler notes](https://drive.google.com/file/d/13rMkduBy7Q68DW5UVXUdkgo48AmbmMDW/view)

    $$
    \frac{ \phi_2 - \phi_1}{2 \pi} = \frac{2d }{\lambda}
    = \frac{-2 T_r M_r }{\lambda} = \frac{ -2M_r}{\lambda PRF}
    $$ (phi2)

    to be useful.
:::


## Derivatives and Euler notation

Not required but potentially usefull. Remember in grade 12 (?) you learned about
the [euler notation](https://www.mathsisfun.com/algebra/eulers-formula.html) for
complex numbers.

-   Some trigonometry facts:

$$
\exp(x) = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^4}{4!} + \ldots

\exp(ix)= 1 + ix - \frac{x^2}{2!} - i\frac{x^3}{3!} + \frac{x^4}{4!} + \ldots

\cos(x) = 1 - \frac{x^2}{2!} + \frac{x^4}{4!}  + \ldots

\sin(x) = x - \frac{x^3}{3!} + \frac{x^5}{5!}  + \ldots

\text{so this means: }

\exp(ix) = cos(x) + i sin(x)
$$

-   Some facts about complex numbers

    -   Any complex number can be written in either cartesian or euler form:


- Cartesian

$$
I = x + iy
$$

- Euler

$$
I=A \exp(i \phi) = A\cos( \phi) + Ai\sin(\phi)
$$

where $A^2 = x^2 + y^2$ and $\phi = \arctan(y/x)$

In other words -- a phasor diagram is just the same as a complex number [Argand plot](https://mathworld.wolfram.com/ArgandDiagram.html).

-   Put these together:

$$
 i&=\exp \left (i \frac{\pi}{2} \right ) \\
 \frac{d \exp(i\phi)}{d\phi} &= i \exp(i\phi) = \exp\left (i\frac{\pi}{2} \right ) \exp(i\phi) = \exp \left (i \left ( \phi + \frac{\pi}{2} \right ) \right ) \\
$$

so adding a positive phase shift of $\pi/2$ is the same thing as taking the derivative. To get the phase of the pulse in the proper quadrant, you measure two real voltages at the A-D converter: $I=A\cos(\phi)$, which is called the **in-phase** component, and
$Q= -A\cos(\phi + \frac{\pi}{2}) = A \sin(\phi)$ which is called the **quadrature** component. This is equivalent
to finding the real part of $I$ and the real part of its derivative, which gives it a unique quadrant location.


