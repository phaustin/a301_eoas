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

# Assignment 2: solutions

WH 4.21, 4.25, 4.30, 4.31, 4.32, 4.39

+++

## Question 4.21 

Show that for small perturbations in the Earth's radiation balance

$$
\frac{\delta T_E}{T_E}=\frac{1}{4} \frac{\delta F_E}{F_E}
$$

where $T_E$ is the Earth's equivalent blackbody temperature and $F_E$ is the flux density of radiation emitted from the top of its atmosphere. [Hint: Take the logarithm of the Stefan-Boltzmann law (4.12) and then take the differential.] Use this relationship to estimate the change in equivalent blackbody temperature that would occur in response to (a) the seasonal variations in the sun-Earth distance due to the eccentricity of the Earth's orbit (presently $\sim 3.5 \%$ ) and (b) an increase in the Earth's albedo from 0.305 to 0.315 .

+++

### 4.21 Answer

+++

4.21) Some definitions:

Note -- I'll use $d$ instead of $\delta$ to denote a small change, except I'll write $\delta d$ since $dd$ looks strange.

+++

- $A$: albedo
- $Q$: power output of the sun (W)
- $d$: sun-earth distance (m)
- $S_0=\frac{Q}{4 \pi d^2}$: Solar constant ($W/m^2$)

The emitted flux $F_E$ and the equivalent temperature $T_E$ are related by

$$
F_e=\frac{S_0}{4}(1-A)=\sigma T_e^4
$$ (albedo)

We want to find the differentials $d T_E$ and $d F_E$.

Take the hint:

$$
\ln F_e = \ln \sigma T_E^4 = \ln \sigma + 4 \ln T_E
$$

and take the differential of both sides

$$
\frac{dF_E}{F_E} = 0 + 4 \frac{dT_E}{T_E}
$$ (lndiff)

+++

and from {eq}`albedo` if we change the albedo, the change in $F_E$ due to an albedo change:

$$
dF_E = -\frac{S_0}{4}(dA)
$$

Divide both sides by $F_E = \frac{S_0}{4}(1-A)$

$$
\frac{dF_E}{F_E} = -\frac{dA}{1 - A} = 4 \frac{dT_E}{T_E}
$$ (diffalb)

Now calculate the relative change in $F_E$ due to a change in the earth-sun distance $d$, recalling that $S_0=\frac{Q}{4 \pi d^2}$

$$
dF_E =  d S_0 \frac{(1 - A)}{4} = \delta \left ( \frac{Q}{4 \pi d^2} \right ) \frac{(1 - A)}{4}  = -2 \left ( \frac{Q}{4 \pi d^3} \right ) \frac{(1 - A)}{4} \delta d
$$

Divide both sides by $F_E = \frac{S_0}{4}(1-A)$:

$$
\frac{dF_E}{F_E} =  -2 \frac{\delta d}{d} = 4 \frac{dT_E}{T_E}
$$ (dchange)

+++

#### Alternative derivation of {eq}`lndiff`

+++

If you don't like the $\ln$ approach above in {eq}`lndiff`, dividing by $F_E$ also works for $dT_E$ in that case:

$$
\begin{gathered}
d F_e=4 \sigma T_e^3 d T_e
\end{gathered}
$$

divide both sides by $F_E = \sigma T_E^4$

$$
\frac{d F_E}{F_E}=\frac{4 \sigma T_e^3}{\sigma T_e^4} d T_E = 4 \frac{dT_E}{T_E}
$$

+++

### Q 4.21a 

If the earth-Sun distance changes by 3.5\%, what is the change in $T_E$?

#### Answer

Use {eq}`dchange` with $\frac{\delta d}{d}$ = 0.035.  That gives:

$$
 \frac{dT_E}{T_E} =   -\frac{2}{4}  \frac{\delta d}{d} = -0.0175
$$

+++

### Q 4.21b

Find $ \frac{dT_E}{T_E}$ for an increase in the Earth’s albedo from 0.305 to 0.315

#### Answer

Use {eq}`diffalb`:

$$
\frac{dT_E}{T_E} = \frac{1}{4} \frac{dF_E}{F_E} = -\frac{dA}{4(1 - A)} 
$$

$ d A=0.305 \rightarrow 0.315=+0.01$

$$
 \frac{d T_e}{T_e}=\frac{-0.01}{4(1-0.305)}=\frac{-0.01}{4 \times 0.695} = -0.0036
$$

So if $T_e=255 \mathrm{~K}$ then this change in albedo will produce
$-0.0036 \times 255\ K = -0.9\ K$ cooling

+++

## Question 4.25

Show that for radiation with very long wavelengths, the Planck monochromatic intensity $B_λ (T)$ is linearly proportional to absolute temperature. This is referred to as the Rayleigh-Jeans limit.

### Answer

+++

## Question 4.30

A small, perfectly black, spherical satellite is in orbit around the Earth at an altitude of 2000 km as depicted in Fig. 4.37. What angle does the Earth subtend when viewed from the satellite?

### Answer

The setup is shown in {numref}`small_planet`

+++

:::{figure} images/small_planet.png
:name: small_planet
:scale: 60

Satellite problem setup
:::

+++


$$
\begin{aligned}
& \phi=\sin ^{-1}\left(\frac{6370}{8370}\right)=0.864\ \mathrm{rad} \approx 49\ deg \\
&\omega = \int_0^{2 \pi} \int_0^\theta \sin \theta^\prime d \theta^\prime d \phi^\prime=\left.2 \pi(-\cos \theta)\right|_0 ^{0.864} \\
&\omega =2 \pi(1-\cos (0.864))=2.21\ \mathrm{sr}
\end{aligned}
$$


+++

### But what is the flux?

Question 4.31 requires the flux to the satellite if the radiance $I$ is independent of
direction (isotropic).  If the radiance is $I$ in all directions, we have to find the component of each element $I d\omega$ in the
direction of the satellite, which means we need to include $\cos \theta$

$$
\begin{aligned}
F &= \int_0^{2 \pi} \int_0^\theta I \cos \theta^\prime \sin \theta^\prime d \theta^\prime d \phi^\prime=\left.2 \pi \left (-\frac{(\cos \theta)^2}{2} \right )\right|_0 ^{0.864} \\
F &= I\,2 \pi \left (\frac{1 - (\cos \theta)^2}{2} \right )= 1.87 I
\end{aligned}
$$

In Q4.31 Wallace and Hobbs neglect $\cos \theta$, which overestimates
the flux as $2.21 I$ and introduces an error of about 20%.

```{code-cell} ipython3
import numpy  as np
theta = 0.864
cos2=np.cos(theta)**2.
print(f"{cos2=:.3f}")
result = 2*np.pi*(1 - cos2)/2.
print( f"{result=:.3f}" )
error = (result - 2.21)/result*100
print(f"{error=:.2f}%")
```

## Question 4.31

If the Earth radiates as a blackbody at an equivalent blackbody temperature $T_E=255 \mathrm{~K}$, calculate the radiative equilibrium temperature of the satellite when it is in the Earth's shadow.

### Answer

Figure {numref}`zoom_out` shows a section of solid angle at a latitude of about 45 deg on the satellite.  How many Watts is arriving at that area?  We know that the flux (arrow) $F$ is arriving at an angle to the surface so we need to find the projection of the surface normal
to the flux.  By the definition of solid angle, the surface area of the pixel is:

$$
dA = r^2 d\omega
$$
where $r$ is the radius of the satellite.



+++

:::{figure} images/zoom_out.png
:name: zoom_out
:scale: 10

Demonstration of Kirchoff’s law
:::

+++

:::{figure} images/zoom_in.png
:name: zoom_in
:scale: 10

Solid angle of a piece of the satellite surfas at 45 deg latitude
:::

+++



+++



+++


[Hint: Let $d E$ be the amount of radiation flux imparted to the satellite by the flux density $d E$ received within the infinitesimal element of solid angle $d \omega$.] Then,

$$
d E=\pi r^2 I d \omega
$$

where $r$ is the radius of the satellite and $I$ is the intensity of the radiation emitted by the Earth, i.e., the flux density of blackbody radiation, as given by (4.12), divided by $\pi$. Integrate the above expression over the arc of solid angle subtended by the Earth, as computed in the previous exercise, noting that the radiation is isotropic, to obtain the total energy absorbed by the satellite per unit time

$$
Q=2.21 r^2 \sigma T_E^4
$$


Finally, show that the temperature of the satellite is given by

$$
T_s=T_E\left(\frac{2.21}{4 \pi}\right)^{1 / 4}
$$

+++

### Answer

+++

## Question 4.32

Show that the approach in Exercise 4.5 in the text, when applied to the previous exercise, yields a temperature of

$$
T_s=T_E\left[\frac{1}{4}\left(\frac{6371}{8371}\right)^2\right]^{1 / 4}=158 \mathrm{~K}
$$


Explain why this approach underestimates the temperature of the satellite. Show that the answer obtained with this approach converges to the exact solution in the previous exercise as the distance between the satellite and the center of the Earth becomes large in comparison to the radius of the Earth $R_E$. [Hint: show that as $d / R_E \rightarrow \infty$, the arc of solid angle subtended by the Earth approaches $\pi R_E^2 / d^2$.]

```{code-cell} ipython3

```
