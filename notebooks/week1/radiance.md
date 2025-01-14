(radiance)=

# Solid angle and radiance

My notes on Wallace and Hobbs Chapter 4, pp. 113-117.  The purpose of this note is to introduce a basic measurement of electromagnetic radiation, the **monochromatic radiance** or **monochromatic intensity**, introduced on pp. 114 of Wallace and Hobbs.   In the literature, there is no clear agreement about symbols.  Wikipedia uses [the letter L](https://en.wikipedia.org/wiki/Radiance) while Wallace and Hobbs use the letter I.   Regardless, it has the units of "watts per meter squared per micron bin width per steradian field of view".  Below I try to untangle this, thinking in terms of how a satellite actually would measure $I_\lambda$.

Wallace and Hobbs also show how the radiance is related to the **irradiance**, or **radiant flux**.   Stull defines this quantity in terms of the monochromatic radiant flux emitted from a black surface:

$$
F_\lambda{ }^*=\frac{c_1}{\lambda^5 \cdot\left[\exp \left(c_2 /(\lambda \cdot T)\right)-1\right]}
$$
Note that both $I_\lambda$ and $F_\lambda$ are vectors, and in this case the direction of propagation of $F_\lambda$, called the **zenith angle** $\theta$, is perpendicular to the emitting surface.

Note that there's nothing special about the blackbody emission, they are just photons in space.   Wallace and Hobbs show how to find the radiant flux given the radiance by integrating over a hemisphere:

$$
F_\lambda=\int_{2 \pi} I_\lambda \cos \theta d \omega
$$

To measure $F$, you could use a photo diode to count the number of
photons per second hitting a sensor, recording the wavelength of each
photon. To get the photon energy use Stull eq. 2.12

$$
\nu = c/\lambda
$$

where $\nu$ is the frequency and c is the speed of light, and then use
Planck's constant (h) to convert frequency in Hz ($s^{-1}$) to
energy in Joules

$$
energy = h \nu
$$

where $h=6.62607 \times 10^{-34}$ $J\,s$. Summing all
the photon energies and dividing by the sensor area would give you the
flux E.  Spreading that flux coming in at zenith angle $\theta$ over a surface that absorbs/reflects the photons would give you the irradiance  $F$.

Below we'll go through each of these terms.

## The $\cos \theta$ effect

To see why the zenith angle matters to the irradiance, consider this figure:

::: {figure} ../figures/costheta.png
:width: 60%
:name: costheta
:alt: pha
The surface area depends on zenith angle
:::

This is why shadows are longer for a setting sun.  The photons need to be spread over a larger area as the zenith angle $\theta$ increases towards 90 degrees.

## Monochromatic Radiance vs. total flux


In the real world, instruments only measure photons that arrive within a limited
field of view (i.e. the field of view of the telescope). The sensor also samples a limited
range of wavelengths, both because the photo diode doesn't respond
equally to all wavelengths and because we are interested in particular
wavelength ranges.  The figure below shows the field of view for a typical
airborne scanning radiometer:

::: {figure} ../figures/c5_1.png
:width: 70%
:name: whiskbroom
:alt: pha
Whiskbroom scanner
:::


The photons reaching the sensor through the telescope are separated into
particular wavelength regions using a filter wheel or a beam splitter:


::: {figure} ../figures/c5_5.png
:width: 70%
:name: filters
:alt: pha
Waveband filters
:::

## Field of view

**Planar angle**

Dealing with the fact that the telescope only sees photons coming from a
specific set of angles means that we need a way to define those angles.
In one dimension, we define an angle using radians:

$$
\phi = \frac{l}{r}
$$

where $l$ is the arclength along a circle of radius $r$ that
defines the angle.

In the case that $l$=$r$ the angle is 1 radian:

:::{figure} ../figures/Radian.png
:name: radian

Definition of planar angle
:::

The differential version of this is:

$$
d\phi = \frac{dl}{r}
$$

### solid angle

A pixel has two dimensions, which makes things more complicated.
Consider the following spherical coordinate system:

:::{figure} ../figures/spherical.png
:width: 70%
:name: spherical_coords
:alt: pha
Spherical coordinates
:::

$\theta$ is called the "zenith angle", and $\phi$ is called
the "azimuth angle". Image our sensor is looking up in the direction
given by $\Omega$

Suppose the telescope has a field of view that's defined by a small
angle $d\phi$ in the azimuthal direction and $d\theta$ in
the zenith direction (these two angles would be equal if the field of
view was a circular cone). A distance $r$ away from the telescope,
the arclength in the zenith direction is $r d\theta$ by the
definition of the planar angle. For the azimuth direction though, the
planar angle is defined by the radius $r \sin \theta$, which gives
the distance from the vertical axis to the surface of the sphere of
radius $r$. That means that the area seen by the telescope at
radius r is:

$$
dA = width \times height = r \sin \theta d\phi \times r d\theta = r^2  \sin \theta d\theta d \phi
$$

:::{figure} ../figures/solid_angle.png
:name: solid_angle

Definition of solid angle
:::

Now that we know $dA$ we can define the solid angle
$d\omega$ (steradians) by analogy with the planar angle:

Planar angle:

$$
d\phi = \frac{dl}{r}
$$

measured in radians

Solid angle:

$$
d\omega = \frac{dA}{r^2} = \frac{r^2 \sin \theta d\theta  d\phi}{r^2} = \sin \theta d\theta  d\phi
$$ (domegaA)

measured in steradians


## Monochromatic flux

Handling the fact that we are only receiving photons in a specific
wavelength range $\Delta \lambda$ is straight forward: we just
divide the measured flux $F$ by the wavelength range to get
$F_\lambda$, the monochromatic flux:

$$
F_\lambda\ (W\,m^{-2}\,\mu m^{-1}) = \frac{ F}{\Delta \lambda}
$$

and if I take $\lim{\Delta \lambda \to 0}$

$$
dF = F_\lambda d \lambda
$$

so we can define $\Delta F$ as the portion of the flux that
is being transmitted by photons with wavelengths between
$\lambda \to \lambda + \Delta \lambda$


## Monochromatic radiance

So if we know the monochromatic flux, and we know the
field of view $\Delta \omega$ of the telescope, then we can get
the monochromatic radiance $I_\lambda$ by:

$$
I_\lambda = \frac{\Delta F_\lambda}{\Delta \lambda \Delta \omega}
$$ (Llambda)

units: $W\,m^{-2}\,\mu m^{-1}\,sr^{-1}$.

The monochromatic radiance $I_\lambda$ is the variable that the
Modis thermal sensors deliver.

Switching to differentials again, we've got:

$$
dF_\lambda = I_\lambda d\lambda d\omega
$$ (dF)

Note that both $dF_\lambda$ and $I_\lambda$ have a direction
associated with them -- their direction of propagation, which is
perpendicular to the surface the photons are passing through.

Note that $dF$ assumes that all the energy is contained in the small solid
angle $d \omega$, which is true for satellites because they are using
a telescope to focus on a small pixel.  If we want to instead measure all the energy
crossing a surface from all directions, we need to integrate over all zenith and azimuth angles.

## Some definitions

* The *irradiance* or *radiant flux* **F** is defined as the energy
(Joules) crossing a unit surface (1 $m^2$) in unit time (1 second)
so it has units of $W\,m^{-2}$.

* The *radiance* or *radiant intensity* is defined as the as the energy
(Joules) crossing a unit surface (1 $m^2$) in unit time (1 second) over
a unit solid angle, wo it has units of $W\,m^{-2}\,sr^{-1}$
