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

(assign2b_solution)=
# Assignment 2: solutions part B

 4.25,  4.32

+++ {"jp-MarkdownHeadingCollapsed": true}

## Question 4.25

Show that for radiation with very long wavelengths, the Planck monochromatic intensity $B_λ (T)$ is linearly proportional to absolute temperature. This is referred to as the Rayleigh-Jeans limit.

### Answer

Recall WH 4.10:

$$
B_\lambda(T)=\frac{c_1 \lambda^{-5}}{\pi\left(e^{c_2 / \lambda T}-1\right)}
$$ (eq:planck)

In the limit $\lambda \rightarrow \infty$ the term $c_2 / \lambda T$ gets increasing small.  We can use the fact that 

$$
e^x  = 1+\frac{x^1}{1!}+\frac{x^2}{2!}+\frac{x^3}{3!}+ \ldots
$$
to get the small x approximation by keeping only the first order term:

$$
e^x  \approx 1+ x
$$ (eq:small)

Inserting {eq}`eq:small` into {eq}`eq:planck` gives:

$$
B_\lambda(T) \approx \frac{c_1 \lambda^{-5} \lambda T}{\pi  c_2 } = \frac{c_1 \lambda^{-4} T}{\pi  c_2 } 
$$ (eq:rj)

which is the Rayleigh-Jean approximation.

+++

## Question 4.32

Show that the approach in Exercise 4.5 in the text, when applied {numref}`p4_31` yields a temperature of

$$
T_s=T_E\left[\frac{1}{4}\left(\frac{6371}{8371}\right)^2\right]^{1 / 4}=158 \mathrm{~K}
$$


Explain why this approach underestimates the temperature of the satellite. Show that the answer obtained with this approach converges to the exact solution in the previous exercise as the distance between the satellite and the center of the Earth becomes large in comparison to the radius of the Earth $R_E$. [Hint: show that as $d / R_E \rightarrow \infty$, the arc of solid angle subtended by the Earth approaches $\pi R_E^2 / d^2$.]

+++

### Answer

First redo E4.5 for this case:

- radius of earth = $R_E$ = 6371 km
- radius of satellite orbit = $d$ = 8371 km
- power in Watts from the earth = $P_E = 4\pi R_E^2 \sigma T_E^4$ W
- area of sphere that power is spread over = $4\pi d^2$ $km^2$
- flux $F_E$ at satellite = $P_E$/area = $\left ( \frac{R_E^2}{d^2} \right ) \sigma T_E^4$
- The flux is intercepted by the satellite across a disk of area $\pi r^2$ where $r$ is the radius
  of the satellite.  As in Q4.31, it assumed to be radiated away over all of the satellite, so in
  equilbrium the new version of {eq}`eq:equil` is:

$$
4 \pi r^2 \sigma T_s^4  &= \pi r^2 F_E = \pi r^2 \left ( \frac{R_E^2}{d^2}  \right ) \sigma T_E^4 \\
T_S^4 &= 0.145\, \sigma T_E^4 
$$

compared to the previous exact result from 6.31:

$$
4 \pi r^2 \sigma T_s^4  &= \pi r^2 \times 1.87 \left ( \frac{  \sigma T_E^4}{\pi} \right ) \\
 T_s^4  &=   \frac{1.87}{4 \pi} T_E^4 = 0.1488\,  T_E^4 
$$ 
The reason the flux at the satellite is slightly larger for the exact solution is because the approximation
assumes a direct beam, with the flux completely perpendicular to the satellite, where the wider solid angle
in the exact answer captures energy that's arriving from the full field of view.

- We want to show that our  exact version of the flux from {eq}`eq:exact`

  $$
  F_E = \int_0^{2 \pi} \int_0^\theta I \cos \theta^\prime \sin \theta^\prime d \theta^\prime d \phi^\prime
  $$ (eq:fullflux)

  converges to the approximate version we're using in this problem

  $$
  F_E = \left ( \frac{R_E^2}{d^2} \right ) \sigma T_E^4
  $$
  in the limit $R_E/d \rightarrow 0$

  First recall that, in the limit of $\theta \approx 0$,  $\sin \theta \approx \theta$ and $\cos \theta \approx 1$,
  which implies that $\sin^{-1} \theta = \theta$.  Since we know from
  {numref}`q4_30` that $\sin \theta = R_E/d$, we've got

  $$
  \theta \approx R_E/d
  $$

  Now use these approximations to integrate {eq}`eq:fullflux` with the blackbody radiance $I = \frac{\sigma T_E^4}{\pi}$

  $$
  F_E &= 2 \pi \int_0^{R_E/d} \frac{\sigma T_E^4}{\pi} \times 1 \times  \theta^\prime d \theta^\prime \\
      &= 2 \sigma T_E^4 \frac{(\theta^\prime)^2}{2} \Big |_0^{R_E/d} = \left ( \frac{R_E^2}{d^2} \right ) \sigma T_E^4
  $$ 

```{code-cell} ipython3
import numpy as np
6370/8370
```

```{code-cell} ipython3
re = 6387
rs = 8387
(re**2./rs**2.)/4.
```

```{code-cell} ipython3

```
