(week1-flux-from-radiance)=

# Finding the flux given the radiance

## Law of the cosine -- using power

Unless the sun is directly overhead, the flux  $F$ on a level
surface is going to be less than the flux perpendicular to the
solar beam. The figure below shows the geometry:

:::{figure} ../figures/shadow.png
:name: shadow
:scale: 35

$\cos \theta$ effect
:::

Assuming that the y dimension (into and out of the screen) has unit
length, then if flux $F_1$ $(W\,m^{-2})$ is incident
on surface 1, power flowing through surface 1 is:

$P_1 = F_1 \times A_1$ Watts

If we assume a direct beam of sunlight (so no inverse-square spreading),
then all of that power passes through surface 2, and so the flux
perpendicular to surface 2 is:

$F_2 = P_1/A_2 = P_1/(A_1 /cos \theta) = F_1 \cos \theta$

This is the main reason why it's cooler at sunset than at noon. It is
also the reason your shadow can be taller than you.

(moving)=

## Moving between flux and radiance

We saw in the {ref}`radiance` reading
that in the case that we have a very narrow beam of solid angle $d\omega$, the flux and radiance vectors are related by:

$$
dF_\lambda = I_\lambda d\omega
$$
where we are writing $dF$ to indicate that you need to integrate this equation over a (possibly imaginary) flat surface to get the flux.  This is just Wallace and Hobbs equation 4.5 without the integral signs, in the particular case that we are looking straight down at the surface, i.e. $\theta =0$ an $\cos \theta$ = 1.


A good way to think about this to ask yourself how a satellite would
measure the radiance I in some direction. It would need to:

1. measure the power P reaching its sensor that has area A
2. Calculate the flux F= P/A
3. Divide that flux by the wavelength range of its filter (say
   $\Delta \lambda = 1\ \mu m$) to get the monochromatic
   flux:

$$
F_\lambda = \frac{F}{\Delta \lambda}
$$

4. Multiply the monochromatic radiance by the field of view of the
   telescope $\Delta \omega$ to get the relationship between
   the monochromatic irradiance and radiance for a narrow beam:

$$
F_\lambda = I_\lambda \Delta \omega
$$ (flrel)


Repeating this figure from the {ref}`radiance` reading: 

:::{figure} ../figures/I_F.png
:name: I_F
:scale: 50

Relationship between I and F
:::

So how would you calculate the flux F crossing through the bottom
of this triangle if you knew the radiance I at every angle? Now you need
to use the law of the cosines to move from the perpendicular surface
with area $dA_1$ to the surface you are interested in with larger
area $dA_2 = dA_1/\cos \theta$:

$$
dF_2 = \cos \theta dF_1 = \cos \theta I d\omega
$$ (cosflux)

To get the flux from every angle requires that you integrate over
a hemisphere. That means you need to integrate over all azimuths, so
$\phi = 0 \to 2\pi$ and over 90 degrees of zenith, so that
$\theta = 0 \to \pi/2$, which is done in Wallace and Hobbs exercise 4.3 
on page 113:

$$
F_2 = \int dF_2 = \int_0^{2\pi} \int_0^{\pi/2} \cos \theta \, I \, d \omega =\int_0^{2\pi} \int_0^{\pi/2} I \cos \theta  \sin \theta \, d\theta \, d \phi
$$ (fluxrel)

Note that you always do this integral over a plane surface containing the sensor.  That is, if you are interested in emission from the earth's surface, you need to turn {numref}`I_F` upside down, and look downward at the source of the radiation.


### Two approximations to {eq}`fluxrel`

Equation {eq}`fluxrel` is the formal definition of $F$ and is always correct.  There are two simplifications that are extremely useful:

#### Parallel beam approximation (W&H p. 116)

$$
F=I \times \Delta \omega
$$

This holds when:

- the $\Delta \omega$, the total solid angle of interest is very small, so that $I$ can be moved out of the integral because it doesn't vary
- the beam is directly parallel to the surface of interest, so that $\theta \approx 0$ and $\cos \theta \approx 1$
- In this case it's typical that the approximation $\Delta \omega = A/R^2$ is good enough  (we'll do a problem on this)

(final-form)=

#### Isotropic radiance: $F = \pi B$

This is Wallace and Hobbs Exersize 4.3 on page 116.  Here we're using the WH notation for the Planck function radiance:  the letter $B$ ($W\,m^{-2}\,sr^{-1}$)

A common case in this course is thermal emission or diffuse reflection, which is characterized
by photons coming isotropically from all directions. In the thermal case the 
surface emitted radiance $B^*$ is independent of
$(\phi, \theta)$ and can be taken outside of the integral. With
that simplification, we're down to trigonometric integrals from first
year calculus:

$$
F_2 = F^* = \int_0^{2\pi}\int_0^{\pi/2} B \cos \theta  \sin \theta \, d\theta \, d \phi = 2 \pi B
      \int_0^{\pi/2} \cos \theta  \sin \theta\, d\theta = 2\pi B \left( \frac{1}{2} \right)  = \pi B
$$ (flux_final)

where we've continued to use an asterisk to denote that this is the
radiation coming from a black surface, immediately above the surface.

More generally if we know $I$ anywhere in space and know that it
is independent of direction, then the irriadiance at that point is going
to be:

$$
F = \pi I
$$ (flux_short)


## Worksheet questions

1) Suppose you have a radiometer with a zoom telescope that can focus on 1 $km^2$ pixel at any distance.   If the surface is emitting radiance $I$ in all directions into a hemisphere, find both $F$ and $I$ at 10 km above the surface, and at 100 km above the surface, assuming you can use the parallel beam.

2) In the answer to 1) you should have found that I is independent of distance from the surface. Explain why {eq}`flux_short` doesn't  violate the inverse square law for flux F.

3) Find the solid angle for a 1 $km^2$ pixel viewed from 800 km, and compare that result to $Area/R^2$.

4) Change of variables:  Do W&H Exercise 4.13 to prove relationship 4.4

