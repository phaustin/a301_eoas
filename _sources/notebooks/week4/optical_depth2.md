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

(week4:tau2)=
# Optical depth II: mean free path

## Introduction

Recall the definiton of the vertical optical depth defined by {eq}`eq:whtau` and Stull Chapter 2 p. 43 or WH eq 4.17 p. 123:

$$
d\tau_\lambda = \rho \, r \, k_\lambda dz
$$
where $\rho$ is the air density ($kg\,m^{-3}$), $r$ is the gas mixing ratio (kg gas/kg air) and $k_\lambda$ is the mass absorption coefficient at wavelength $\lambda$ ($m^{2}\,kg^{-1}$).

Stull eq. 2.32 on p. 43 also defines the volume absorption coefficient $\gamma$ ($m^2/m^3$):

$$
\gamma_\lambda = \rho\,r\,k_\lambda
$$

With that definiton we can go back to our {eq}`eq:difflux` from week 1 and rewrite

$$
\frac{dI}{I} = -n b ds
$$
where $s\ (m)$ is the distance travelled (the path length),
$n\ (\#/m^3)$ is the number denstiy of absorbing
particles and $b\ (m^2)/molecule$ is the absorption cross section per molecule.
Using $\gamma_\lambda$ Beer's law becomes:


$$
\frac{dI}{I} = -\gamma ds
$$ (eq:newdf)

and if we're pointing straight up, $ds = dz$ so we can integrate {eq}`eq:newdf`
to get

$$
I(z) = I_i \exp (-\gamma z)
$$ (eq:gammaI)
with the big assumption that the mass absorption coefficient $\gamma$ is independent of $z$.

## Photon lifetimes

So given {eq}`eq:gammaI`, what is the probability that a photon is absorbed across a distance $\Delta z$?

Let's call that probability $p(z) dz$.  Where $p(z)$ is a probability distribution that satisfies the condition that:

$$
\int_0^\infty p(z) dz =1
$$
that is, 100% of all photons are absorbed over an infinite path.  What about a shorter path?
For a path of length $\Delta z$, this is going to just be the difference between the fraction
that reached $z$ and the fraction that reaches $z + \Delta z$.

$$
\int_z^{z+\Delta z} p(z) d z \approx p(z) \Delta z  =\exp \left ( -\gamma z\ \right )-\exp \left ( -\gamma (z+\Delta z) \right )
$$
where we've assumed that $p(z)$ is approximately constant over $\Delta z$ and can be taken out of the integral.

Finally, divide by $\Delta z$ and take the limit $\Delta z \rightarrow 0$ and get

$$
p(z)  = \left [ \exp \left ( -\gamma z\ \right )-\exp \left ( -\gamma (z+\Delta z) \right ) \right ] / \Delta z = - \frac{d}{dz} \exp ( -\gamma z) = \gamma \exp ( -\gamma z )
$$ (eq:pz)


## Mean free path

Finally, if we know the probability $p(z)$ that a photon is going to be absorbed after travelling a distance $z$, we can find the average distance that a photon travels before it is absorbed.  The definition of the that average from statistics is just:

$$
\overline{z} = \int_0^\infty z\,p(z)\,dz 
$$
and using {eq}`eq:pz` that is just:

$$
\overline{z}  = \int_0^\infty z \gamma \exp (- \gamma z ) \,dz = \frac{1}{\gamma} 
$$

## Unit optical depth

We have shown that the volume absorption coefficient $\gamma$ gives a measure for how far a photon can travel through the atmosphere before being absorbed.  What is the optical depth that corresponds to that distance?  Do the integration between $z=0$ and $z=\overline{z} = 1/\gamma$, again assuming that $\gamma$ is independent of $z$:

$$
\tau = \int_0^\overline{z} \gamma dz = \gamma \times \overline{z} = \gamma \times \frac{1}{\gamma} = 1
$$

So on average, the photons can travel through an optical depth of 1 before being absorbed.

## Conclusion

How good is the assumption that $\gamma$ is independent of height?  In the atmosphere, not very good, because the gas density $\rho(z)$ decreases exponentially with height.  This is the subject of
Walace and Hobbs problem 4.44 and the next lecture.
