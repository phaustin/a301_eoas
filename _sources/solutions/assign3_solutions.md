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

(assign3_solution)=
# Assignment 3: solutions

WH 4.43, 4.46, 4.47

+++

## Question 4.43


Consider radiation with wavelength λ and zero zenith angle passing through a gas with an absorption coefficient of $k_\lambda$ = 0.01 $m^2\,kg^{-1}$. What fraction of the beam is absorbed in passing through a layer containing 1 $kg\,m^{-2}$ of the gas? What mass of gas would the layer have to contain in order to absorb half the incident radiation?

+++

### 4.43 Answer

The equation: use eq. 4.31 for constant absorption coefficient, which can come out of the integral.  Since they don't mention
a mixing ratio $r$, we can assume that it's the only gas, so $r$=1.  Also $\theta = 0$ so $\sec \theta = 1$.  Assume the setup is that the
radiation is coming down in a direct beam from above (sunlight), so we can define the mass above z as $M\ (kg\,m^{-2}$) where:

$$
M = \int_z^\infty \rho dz
$$

Then Beer's law says:

$$
\tau = k_\lambda \int_z^{\infty}  \rho  d z = k_\lambda M
$$

$$
\frac{I_{\lambda}}{I_{\lambda \infty}} = \exp(-\tau) = \exp \left ( -k_\lambda  M \right )
$$

with $\sec \theta$=1 and  and absorption coefficient $k_\lambda$ both constant with $z$

The numbers:

$$
k_\lambda M = 0.01\  m^2\,kg^{-1} \times 1\ kg\,m^{-2} = 0.01
$$

$$
\frac{I_{\lambda}}{I_{\lambda \infty}} = \exp(-0.01) = 0.37
$$

Column mass needed for 0.5 absorption:

$$
0.5 &= \exp( -0.01 \times M ) \\
\ln(0.5) & = -0.01 \times M \\
 M  &= -0.69/-0.01  = 69\ kg\,m^{-2}
$$

```{code-cell} ipython3
import numpy as np
print(f"{np.exp(-0.01)=:.2f}")
print(f"{np.log(0.5)=:.2f}")
```

## Question 4.46


Consider a hypothetical planetary atmosphere comprised entirely of the gas in Exercise 4.43. The atmospheric pressure at the surface of the planet is 1000 hPa , the lapse rate is isothermal, the scale height is 10 km , and the gravitational acceleration is 10 $m\,s^{-2}$. Estimate the height and pressure of the level of unit normal optical depth.

### 4.46 Answer

+++

Again, the mass of the column as $M = \int \rho dz$

$$
\tau = \int_z^\infty k_\lambda \rho dz = k_\lambda \int_z^\infty  \rho dz= k_\lambda M = 1 \\
M = 1/k_\lambda = 1/0.01 = 100\ kg\,m^{-2}
$$

Hydrostatic equation:

$$
\int_{p}^0 dp^\prime &= -\int_0^z \rho g dz^\prime \\
 -p &=  -g \int_z^\infty \rho dz^\prime = - g M = 10 \times 100 = -1000\ Pa\\
 p &= 1000\ Pa
$$

Height at 1000 Pa given $p_0 = 10^5\ Pa$ and H = 10 km

$$
p &= p_0 \exp(-z/H) \\
1000 &= 10^5 \exp(-z/H) \\
\ln(10^{-2}) &= -z/H = -z/10\ km \\
-4.6 \times 10 &= - z \\
z &= 46\ km
$$

```{code-cell} ipython3
np.log(1.e-2)
```

## Question 4.47



(a) What percentage of the incident monochromatic intensity with wavelength λ and zero zenith angle is absorbed in passing through the layer of the atmosphere extending from an optical depth τ_λ=0.2 to τ_λ=4.0 ?
(b) What percentage of the outgoing monochromatic intensity to space with wavelength λ and zero zenith angle is emitted from the layer of the atmosphere extending from an optical depth τ_λ=0.2 to τ_λ=4.0 ?
(c) In an isothermal atmosphere, through how many scale heights would the layer in (a) and (b) extend?

Here's the setup:


:::{figure} images/wh_4_47.png
:name: figure_447
:scale: 60

Setup for Problem 4.47
:::


### 4.47 Answer

+++

**a)** As with {ref}`week4:tau2`, to find the amount absorbed we just need to take the difference between the amount arriving at
$\tau = 0.2$ and the amount that makes it to  $\tau = 4$.  So if the fraction absorbed is $f$, then

$$
f = \frac{I_0 \exp(-0.20 ) - I_0\exp(-4)}{I_0} = .818 - .18  = 0.8 = 80\%
$$

```{code-cell} ipython3
np.exp(-0.2), np.exp(-4)
```

**b)** Assume that the layer is thick enough so that for the entire layer, emissivity $\epsilon$ = 1, i.e. the total optical depth $\tau_T$ is very large.  Also assume that we're again dealing with an isothermal layer.  Then the question can be phrased as "what's the emissivity of
the part of the atmosphere between $\tau = 0.2$ and $\tau = 4$?".  If we call that emissivity $\epsilon_L$, then for an isothermal atmosphere
the emitted radiance is going to be $\epsilon_L B_\lambda$.

First find the emissivity between $\tau = 0$ and $\tau = 4$.  We know that emissivity = absorptivity, and without reflection
absorptivity = 1 - transmissivity.  So the emissivity from $\tau = 0 \rightarrow 4$ is:

$$
\epsilon_{0-4} = 1 - \exp(-4)
$$
and the emissivity from $0-0.2$ is 

$$
\epsilon_{0-0.2} = 1 - \exp(-0.2)
$$

So the total emitted from $\tau = 0 \rightarrow 4$ is $\epsilon_{0-4} B_\lambda$ and the amount emitted from $\tau = 0\rightarrow0.2$ is $\epsilon_{0-0.2} B_\lambda$.  The fraction f emitted is just the difference between those two amounts divided by the total
blackbody emission $B_\lambda$:

$$
f = \frac{ (1 - \exp(-4)) B_\lambda - (1 - \exp(-0.2))B_\lambda}{B_\lambda} = 0.818 - 0.18 = 0.8
$$

i.e., just another way of saying that 1 - transmissivity = absorptivity = emissivity

+++

**c)** Assume the density scale height is $H$, so that

$$
\rho(z) = \rho_0 \exp(-z/H)
$$

From part a) the defintion of the optical depth is

$$
\tau = k_\lambda \int_z^{\infty}  \rho  d z = k_\lambda \int_z^{\infty}  \rho_0 \exp(-z/H)  d z
$$

Integrating this:

$$
\tau = -H k_\lambda \rho_0 \exp(-z/H) \big |_z^\infty =  k_\lambda \rho_0 \left ( 0 - (-H \exp(-z/H)) \right ) = k_\lambda \rho_0 H \exp(-z/H)
$$

If we say that $\tau_1 = 4$ occurs at height $z_1$ and $\tau_2 = 0.2$ occurs at heigh $z_2$, then

$$
\frac{\tau_2}{\tau_1} = \frac{0.2}{4} = \frac{k_\lambda \rho_0 H\exp(-z_2/H)}{k_\lambda \rho_0 H \exp(-z_1/H)} = \exp \left ( -\frac{(z_2 - z_1 ) }{H} \right )
$$

Take the log of both sides:

$$
\ln(0.05) = -3 = -\frac{(z_2 - z_1 ) }{H}
$$

So the difference between the heights is 3 scale heights.

```{code-cell} ipython3
np.log(0.05)
```

```{code-cell} ipython3

```
