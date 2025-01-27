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

(week-review)=
# Weekly review 

(week1-review)=
## Week 1

### Key week1 topics

1. Definitions of solid angle/field of view, irradiance, radiance
2. Explanation of how a satellite sensor measures radiance
3. Conservation of radiance in a vacuum
4. Derivation of Beer's law and optical depth (we'll return to this in more detail later)
5. Calculating flux from radiance for two cases: 

   - the parallel beam approximation ($I$ contained in a narrow field of view  e.g. solar direct beam) 
   - isotropic radiance ($I$ independent of direction e.g. diffuse reflection or thermal emission) 




### Week 1 Study question solutions

1. On page 39, Stull asserts the inverse square law:

    $$
    F_2 = F_1 \left ( \frac{R_1^2}{R_2^2} \right )
    $$ 

    Prove this using conservation of energy (i.e. conservation of Joules)

    **Answer**: The total power, in Watts, passing through a hemisphere at $R_1$ is

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
   $$ (week1_beers)

   Suppose I have two pieces of translucent glass that absorb but don't
   reflect light, and their indvidual transmissivities are $t_1$ and
   $t_2$. Use conservation of energy to prove that if we stack the
   two pieces, the combined transmissivity will be $t_1 \times t_2$,
   which means that the combined optical depth will be
   $\tau_1 + \tau_2$ (i.e. optical depths add). Note that I had to
   assume no reflection so that photons wouldn't bounce back and forth
   between the two plates.

   **Answer**:  From {eq}`week1_beers` we know that the flux exiting plate 1 is:
   
   $$
   F_1 = F_i \exp(-\tau_1)
   $$
   
   Because we know it is a direct beam (i.e. tiny solid angle $\Delta \omega$) there is no spherical
   spreading and $F_2$ is just

   $$
   F_2 = F_1 \exp(-\tau_2) = F_i \exp(-\tau_1) \exp(-\tau_2) = F_i \exp(-(\tau_1 + \tau_2))
   $$

+++

4. Suppose you have a radiometer with a zoom telescope that can focus on 1 $km^2$ pixel at any distance.   If the surface is emitting radiance $I$ in all directions into a hemisphere, find both $F$ and $I$ at 10 km above the surface, and at 100 km above the surface, assuming you can use the parallel beam approximation.

    **Answer**
    
    Since we are using the parallel beam approximation, we can assume that:
    
    $$
    F = I \Delta \omega
    $$
    for at nadir ($\theta = 0$).
    
    In each case, we make the approximation that
    
    $$
    \Delta \omega \approx  \frac{area}{R^2}
    $$  (approx_omega)
    
    Since $I$ is independent of distance in a vacuum,  $F$ obeys the inverse square law, that is the flux decreases as $1/R^2$
    
    New question -- how accurate is {eq}`approx_omega`  in each case?

+++

5. In the answer to 4. you should have found that I is independent of distance from the surface.
   Explain why, in the case of isotropic emission/reflection over a plane surface


   $$
   F = \pi I
   $$
   doesn't  violate the inverse square law for flux F.

   **Answer**  In contrast to the parallel beam case, over an infinite flat surface there is always more surface area to fill the
   sensor field of view as the sensor moves away from the surface.  Therefore the power reacing the sensor increases by the area in the image
   which increases by the $R^2$ as the sensor moves away.

+++

8. Find the solid angle for a 1 $km^2$ pixel viewed from 800 km, and compare that result to $Area/R^2$.

   We need to integrate the definition of the solid angle {eq}`domegaA`
  
   $$
   \int d\omega   = \int_0^{2\pi}  \int_0^\theta \sin \theta d\theta  d\phi
   $$
   
   We know that $\sin \theta$ is rise/run  $\approx$ 0.5 km/800 km.  

   Google tells me that the arcsin of 0.5/800 is 0.000654 radians.
   
   Make the variable substitution suggested in class:
   
   $$
   \begin{aligned}
   \mu &= \cos \theta \\
   d\mu &= -\sin \theta d\theta \\
   \int d\omega  & = \int_0^{2\pi}  \int_\mu^1 d\mu  d\phi \\
   \omega &= 2\pi \times (1 - \mu)  = 2\pi \times 1.95312519 \times 10^{-7} = 1.227 \times 10^{-6} \ sr
   \end{aligned}
   $$
   
   Compare this to $area/R^2$ = $1/800^2$ = $1.5625 \times 10^{-6}$ sr
   
   New question -- what is a more accurate area for the circular pixel in this case?  Does this make the approximation better?
+++

9. Change of variables:  Do W&H Exercise 4.13 to prove relationship 4.4

   $$
   \nu &=  \lambda^{-1} \\
   d\nu &=  (-\lambda^{-2}) d\lambda \\
   I_\nu d\nu &= -I_\lambda d\lambda \\
   I_\nu d\nu &= I_\lambda \lambda^2 d\nu \\
   I_\nu &= \lambda^2 I_\lambda
   $$

   What's going on with the minus sign?  This is because integration over $\lambda$ and $\nu$ proceed in opposite directions. If $\Delta \lambda = \lambda_2 - \lambda_1$ is positive then $\Delta \nu =  \nu_2 - \nu_1$ is negative, and you would flip the limits of integration, which produces a cancelling minus sign.
   
   
(week2-review)=
## Week 2

### Key week2 topics

1. The $\cos \theta$ law for flux
2. The derivation and use of the brightness temperature
3. GIS concepts:  datum, map projection
4. Software: making maps with cartopy, reading geotiff raster data with rioxarray


## Week 3

### Key week3 topics

1. Stefan- Boltzman: WH p. 119
2. Kirchoff's law: WH p. 121 and problem 4.35
3. Greenhouse effect and energy balance: WH p 122, Figure 4.9
3. Beer's law: WH p. 122 eq. 4.16
4. Optical depth, transmissivity, grey layers: WH p. 130 eq. 4.32
5. Clipping Landsat scenes with a bounding box

