---
jupytext:
  cell_metadata_filter: -all
  encoding: '# -*- coding: utf-8 -*-'
  formats: ipynb,md:myst,py:percent
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.7
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# A301 midterm

Name (Last, First):

Student Number:


Instructions: Answer all questions, clearly labeling each answer, showing all your work on the exam booklet.

For partial credit: If you're stuck on one part of a multipart question and need to move on, you can invent a reasonable set of numbers so that you can answer subsequent questions for full credit. Just be very clear in explaining what you're doing.

Closed book, equation sheet provided, calculators ok

+++

## Q1) (12) 

A satellite orbiting at an altitude of 36000 km observes the
surface in the $CO_2$ absorption band with a wavelength
range of 14 μm  $< λ < 16$ μm.
    
###  Q1a) (4 points) 

The atmosphere is 20 km thick, and has a density scale height of
$H_\rho$ = 9 km and a surface air density of
$\rho_{air}$ = 1.1 $kg\,m^{-3}$. The $CO_2$ mass
absorption coefficient is
$k_λ$ = 0.15 $m^2\,kg^{-1}$ at
λ = 15 μm and its mixing ratio is $4 \times 10^{−4}\,kg\,kg^{-1}$.
Find the:

- the atmosphere’s vertical optical thickness
    $τ_λ$ in the $CO_2$ band

- the atmosphere’s transmittance $t_\lambda$ in the $CO_2$
    band

for a pixel directly beneath the satellite.

+++

### Q1b (4 points)
 
If the surface is a blackbody with a temperature of 290 K, and
        the atmosphere has an constant temperature of 270 K, find the

-   monochromatic radiance observed by the satellite at 15
        μm in ($W\,m^{-2}\,\mu m^{-1}\,sr^{-1}$)

-   the brightness temperature of the pixel in Kelvins for that
        radiance

+++

### Q1c (4 points)

- Given a pixel size $10\ km^2$, find:

    -   the imager field of view in steradians

    -   the flux, in $W\,m^{-2}$ at the satellite for the wavelength range between
        14-16 $\mu m$

+++

## Q2 (8 points)

+++

- For the same atmosphere as Question 1, find the heating/cooling rate, in degrees K/day,
  showing all your work.

+++

<div class="page-break"></div>


## Q3 (6 points)

Starting with the Schwartzchild equation

$$
  dL_\lambda = -L_\lambda\, d\tau/\mu  + B_{\lambda}(z) d\tau/\mu
$$

Derive the integrated solution for an isothermal layer:

$$
  L_\lambda(\tau/\mu)= B_\lambda(T_{skin}) \hat{t}_{tot}
             +  (1 - \exp(-\tau/\mu) )B_\lambda(T)
$$

stating all your assumptions.

+++

## Planck curves

```{figure} figures/a301_radiance_planck.png
---
width: 100%
---
Planck function
```
