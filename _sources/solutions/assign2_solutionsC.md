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

(assign2c_solution)=
# Assignment 2: solutions part C


## Question 4.39 

Consider the radiation balance of an atmosphere with a large number of layers, each of which is isothermal, transparent to solar radiation, and absorbs the fraction of longwave radiation incident on it from above or below. (a) Show that the flux density of the radiation emitted by the topmost layer is αF/(2-α) where F is the flux density of the planetary radiation emitted to space. By applying the Stefan-Boltzmann law (4.12) to an infinitesimally thin topmost layer, show that the radiative equilibrium temperature at the top of the atmosphere, sometimes referred to as the skin temperature, is given by

(Were it not for the presence of stratospheric ozone, the temperature of the 20- to 80-km layer in the Earth's atmosphere would be close to the skin temperature.)

$$
T_L=\left(\frac{1}{2}\right)^{1 / 4} T_E
$$

### Answer

Here's the setup:

:::{figure} images/wh_4_39_setup.png
:name: grey_layers_wh
:scale: 55
Wallace and Hobbs problem 4.39: A thin grey layer
:::

Red arrows denote longwave radiation, and the yellow arrow is solar radiation. The arrow labeled $F$ is the flux arriving from the sun, the unknown arrows are $L$, the flux emitted by the layer and $G$ the flux arriving from below the layer.  There are two equations because at both the top and bottom of the layer the fluxes have to be exactly equal, or the layer would be heating or cooling.   Traditionally, downward arrows are given a positive sign, and negative arrows are given a positive sign.  To solve the problem, use the two equations to solve for $L$ in terms of $F$ and show that

$$
L = \frac{\alpha}{2 - \alpha} F
$$

The two equations are:

- Balance at the top and bottom of the layer
  
$$
F &- (1 - \alpha) G - L = 0 \\
F &- G + L = 0
$$

- Add and subtract the two equations

$$
2F &- (2 - \alpha)G =0 \\
\alpha G &- 2L = 0
$$

- Rearrange

$$
G &= \frac{2F}{2 - \alpha} \\
L & = \frac{G}{2} = \frac{\alpha  }{2 - \alpha} F 
$$ (two)

To get Wallace and Hobbs answer, recognize that the definition of the equilibrium temperature $T_E$ is the temperature a blackbody would need to balance $F$, that is:

$$
F = \sigma T_E^4
$$

and by Kirchoff's law

$$
L = \epsilon \sigma T_L^4 = \alpha \sigma T_L^4
$$

So {eq}`two` becomes:

$$
L = \alpha \sigma T_L^4 = \frac{\alpha  }{2 - \alpha} F 
$$

and canceling the $\alpha$:

$$
\sigma T_L^4 = \frac{ 1  }{2 - \alpha} F  = \frac{F}{2} = \frac{\sigma T_E^4}{2}
$$
in the limit $\alpha \rightarrow 0$


 
