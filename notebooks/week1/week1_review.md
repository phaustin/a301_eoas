---
jupytext:
  formats: md:myst,ipynb
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

(week1-review)=
# Week 1 review questions/answers

1. On page 39, Stull asserts the inverse square law:

$$
F_2 = F_1 \left ( \frac{R_1^2}{R_2^2} \right )
$$ 

Prove this using conservation of energy (i.e. conservation of Joules)

*Answer*: The total power, in Watts, passing through a hemisphere at $R_1$ is

$$
P_1=F_1 \times 2 \pi R_1^2
$$

If $P_1$ is conserved then at distance $R_2$ the new flux is:

$$
F_2 = \frac{P_1}{2\pi R_2^2} = \frac{F_1 \times 2 \pi R_1^2}{2\pi R_2^2}
$$

+++

2. Suppose a 10 cm x 10 cm piece of white paper with a visible
   reflectivity of 80% is pinned to a wall and illuminated by visible
   light with a flux of 100 $W\,m^{-2}$. If the paper reflects
   evenly in all directions (isotropic, not glossy), what is the flux
   from the paper 3 meters from the wall? What about 6 meters from the
   wall?   

```{code-cell} ipython3
import numpy as np
area = 0.1*0.1 #m^2
reflect=0.8
incident_flux = 100 #W/m^2
reflect_power = 0.8*incident_flux*area
R1 =3  #meters
reflect_flux_3 = reflect_power/(2*np.pi*R1**2.) #W/m^2
R2=6 #meters
reflect_flux_6 = reflect_power/(2*np.pi*R2**2.) #W/m^2
print(f"Reflected flux at {R1:0.2f} meters = {reflect_flux_3:0.2g} W/m^2")
print(f"Reflected flux at {R2:0.2f} meters = {reflect_flux_6:0.2g} W/m^2")
```

3. Stull defines the direct beam transmissivity as:

   $$
   t = \frac{F}{F_{i}} = \exp(-\tau)
   $$

   Suppose I have two pieces of translucent glass that absorb but don't
   reflect light, and their indvidual transmissivities are $t_1$ and
   $t_2$. Use conservation of energy to prove that if we stack the
   two pieces, the combined transmissivity will be $t_1 \times t_2$,
   which means that the combined optical depth will be
   $\tau_1 + \tau_2$ (i.e. optical depths add). Note that I had to
   assume no reflection so that photons wouldn't bounce back and forth
   between the two plates. 


4. Suppose you have a radiometer with a zoom telescope that can focus on 1 $km^2$ pixel at any distance.   If the surface is emitting radiance $I$ in all directions into a hemisphere, find both $F$ and $I$ at 10 km above the surface, and at 100 km above the surface, assuming you can use the parallel beam approximation.

5. In the answer to 1) you should have found that I is independent of distance from the surface. Explain why {eq}`flux_short` doesn't  violate the inverse square law for flux F.

6. Find the solid angle for a 1 $km^2$ pixel viewed from 800 km, and compare that result to $Area/R^2$.

7. Change of variables:  Do W&H Exercise 4.13 to prove relationship 4.4
