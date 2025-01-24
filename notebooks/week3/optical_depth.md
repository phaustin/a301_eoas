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

(week3:tau)=
# Optical depth and heating rate

## Notes on optical depth and the greenhouse effect

We need to connect the layer model showing Wallace and Hobbs Figure 4.9 p. 122 with Beer's law and optical depth.

:::{figure} images/wh_2layer.png
:name: black_layers
:scale: 70

Wallace and Hobbs Figure 4.9: two black layers
:::

In {numref}`black_layers` the absorptivity $\alpha$ and emissivity $\epsilon$ are both 1, and the transmissivity $T$ is 0, because the layers are black. But we know that in general the atmosphere is at least partially transparent in the longwave (we can measure the surface temperature from satellites), so that the flux
transmissivity from Week 1 {eq}`beers-flux`:

$$
\frac{F_{out}}{F_{in}} = \exp(-\tau)
$$ (ftrans)
is greater than 0.  In fact if we average across all wavelengths and the depth of the atmosphere atmosphere, $T \approx 0.2$ so $\epsilon \approx 0.8$)

Wallace and Hobbs make two changes to {eq}`ftrans`:  

1. They use radiance instead of flux

   {eq}`ftrans` only works for "direct beam" flux.  Later in the course we'll see how it has to be modified for the more general case of photons coming from all directions (specifically, we need to get to Wallace and Hobbs equation 4.44 on page 136).  Wallace and Hobbs equation 4.17 is always true though:
   
   $$
   d I_\lambda=-I_\lambda \rho r k_\lambda d s = -I_\lambda \rho r k_\lambda dz/\cos \theta =  -I_\lambda \, d\tau/\cos \theta
   $$
   where $\rho$ is the air density ($kg\,m^{-3}$), $r$ is the gas mixing ratio (kg gas/kg air) and $k_\lambda$ is the mass absorption coefficient ($m^{2}\,kg^{-1}$).

   To get the flux equation {eq}`ftrans` for the direct beam (like the solar beam), just multiply by the small field of view $\Delta \omega$, since in that case $F = I \Delta \omega$.

2. they allow for "slant paths" where the beam is moving at an angle $\theta$ from the vertical, and so covering a longer distance.  For {eq}`ftrans` we need to limit ourselves to straight up and down with $\theta = 0$.


## Optical depth and the greybody approximation

So if the real atmosphere is semi-transparent, how do we modify  {numref}`black_layers`  to be more accurate?   We use the "greybody" approximation.  If we know the optical depth $\tau$, then we know the transmissivity $T = \exp(-\tau)$.   If we can neglect reflectivity $R$ (a good approximation in the longwave), then Wallace and Hobbs equation 4.14 gets simpler:

Conservation of energy:

$$
\alpha + R + T = 1
$$

becomes

$$
\alpha + T &= \alpha + \exp(-\tau) = 1 \\
\epsilon &= \alpha = (1 - \exp(-\tau)) 
$$
where we have used Kirchoff's law that $\alpha = \epsilon$.  So we're in a position to calculate absorption and emission for any part of the atmosphere, as long as we know it's composition, density and temperature.

## The grey layer in Wallace and Hobbs problem 4.39

Wallace and Hobbs problem 4.39 describes the folowing grey layer:

:::{figure} images/wh_4_39_setup.png
:name: grey_layers
:scale: 70

Wallace and Hobbs problem 4.39: A thin grey layer
:::

Red arrows denote longwave radiation, and the yellow arrow is solar radiation. The arrow labeled $F$ is the flux arriving from the sun, the unkown arrows are $L$, the flux emitted by the layer and $G$ the flux arriving from below the layer.  There are two equations because at both the top and bottom of the layer the fluxes have to be exactly equal, or the layer would be heating or cooling.   Traditionally, downward arrows are given a positive sign, and negative arrows are given a positive sign.  To solve the problem, use the two equations to solve for $L$ in terms of $F$ and show that

$$
L = \frac{\alpha}{2 - \alpha} F
$$

To get Wallace and Hobbs answer, recognize that the definition of the equilibrium temperature $T_E$ is the temperature a blackbody would need to balance $F$, that is:

$$
F = \sigma T_E^4
$$

and by Kirchoff's law

$$
L = \epsilon \sigma T_L^4 = \alpha \sigma T_L^4
$$


## Summary

1. Given values for gas density, mixing ratio and the absorption coefficient we can compute the optical depth along a path.

2. Once we know the optical depth, and in the absense of reflection, we can get the transmivity $T$, the absorptivity $\alpha$ and the emissivity $\epsilon$

3. We can then use that information to calculate the energy transfer between more realistic atmospheric layers, which will allows us to get the greenhouse effect later in the course.

