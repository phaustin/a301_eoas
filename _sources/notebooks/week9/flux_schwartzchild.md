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

(week9:diffusivity)=

# Integrating the Schwartzchild equation 

To calculate the radiative flux passing through an atmospheric layer we need to know the optical depth as a function
of wavelength, height and direction and the temperature as a function of height. That means we need to do
three separate integrations with respect to $\lambda$, $\tau$, and $\theta$, assuming that the radiance is
independent of azimuth $\phi$.

## Integration over wavelength

Typically this integration is done over a set of intervals (perhaps 30-40) with different values of the absorption coefficient $k_\lambda$ for each of the absorbing gasses (assumed independent). We also need to integrate the
Planck function over wavelength. From {ref}`assign6` we know that:

$$
\int_0^\infty B_{\lambda} d\lambda = \frac{\sigma}{\pi} T^4
$$

Below we'll also define $\overline{\tau}$ as the average over a wavelength interval $\Delta \lambda$

$$
\overline{\tau} = \frac{\int_{\Delta \lambda} \tau_\lambda d\lambda}{\Delta \lambda}
$$

## Integration over optical depth

For slant paths start by rewriting {eq}`schwart2` in {ref}`week5-schwartzA` to account for $\mu = \cos \theta$

$$
   dL_\lambda= \left ( -L_\lambda + B_\lambda (T_{layer} ) \right ) \frac{d\tau_\lambda}{\mu}
$$ (schwart3)

For constant temperature  we know how to solve this.  Since $\mu$ isn't related to temperature we can just repeat the change of variables trick in {ref}`schwartz:change` and get the zenith-angle dependent version.

$$
L_\lambda = L_{\lambda 0} \exp( -\tau_{\lambda}/\mu  ) + B_\lambda (T_{layer})(1- \exp( -\tau_{\lambda} /\mu))
$$ (rep_constant)



For height dependent temperature in r {eq}`integ1` we used an integrating factor of $\exp(\tau)$.  You should convince yourself that if
we do the same thing for {eq}`schwart3` but with an integrating factor of $\exp(\tau/\mu)$ we
get:

$$
L_\lambda = B_\lambda(T_{skin}) \exp(-\tau/\mu)  +     \int_0^{\tau} \exp\left(  - (\tau -\tau^\prime)/\,\mu \right ) B_\lambda(T) d \tau^\prime / \mu 
$$ (fluxtrans4)

and defining the slant trasmission:

$$
t_s = \exp\left(  - (\tau -\tau^\prime)/\,\mu \right )
$$
{eq}`fluxtrans4` simplifies to 

$$
L_\lambda = B_\lambda(T_{skin}) t_s(\tau)  +     \int_0^{\tau}  B_\lambda(T) d ts(\tau,\tau^\prime) / \mu 
$$ (fluxtrans4b)
just like {eq}`calc4`.

## Integration over zenith angle: no atmosphere

We can’t integrate {eq}`fluxtrans4` over $\mu$ analytically, but the integrals are easy
to do numerically. As we'll show in a {ref}`week9:pydiffuse`, the following “diffusivity”
approximation is quite good:

$$
t_f =  \int_0^1 \mu \exp \left ( \frac{(\tau - \tau^\prime)}{\mu} \right ) d\mu
    =  \exp \left (-1.66 (\tau - \tau^\prime) \right )
$$ (diffusivity)

So that the transmissivity for flux is the same as the transmissivity for radiance except that the effective thickness of the atmosphere is increased by a factor of 1.666.

Where does this factor of 1.66 come from?

-   In the {ref}`sec:week1-flux-from-radiance` notes we turned blackbody isotropic radiance
    into a flux by taking the normal component and integrating over the hemisphere:

    $$
    \begin{align}
      F_\lambda&= \int_0^{2 \pi} \int_0^{\pi/2} \cos \theta\, L_\lambda \sin \theta d\theta d\phi \\
               &= 2 \pi  \int_0^1 \mu \, L_\lambda  d\mu
     \end{align}
    $$ (allangles2)

    assuming no dependence of $L_\lambda$ on $\phi$ and $\theta$ we can take $L_\lambda$ out
    of the integral and substituting $\mu= \cos \theta$ write:

    $$
    F_\lambda=  2 \pi L_\lambda \int_0^1 \mu  d\mu  = 2 \pi \frac{\mu^2}{2} \Bigg \rvert_0^1 = 2 \pi  L_\lambda \frac{ 1}{ 2}
      = \pi L_\lambda
    $$ (allangles2b)

+++

### now add an atmosphere

Once we add the atmopsheric transmissivity, we have a much more difficult integral:

Getting the flux using $L_\lambda$ from  {eq}`fluxtrans4` looks like this:

$$
 F_\uparrow &= \int_0^{2 \pi} \int_0^{\pi/2} \cos \theta\,
 L_\lambda \sin \theta d\theta d\phi \\
 &=  2\pi \int_0^1 \mu L_\lambda d \mu \notag\\
 &= 2 \pi B_{\lambda 0}(T_s) \int_0^1 \mu  \exp(-\tau/\mu) d\mu \nonumber\\
 &+ 2 \pi \int_0^1
 \int_0^{\tau} \exp\left( -\frac{(\tau - \tau^\prime)}{\mu} \right ) B_\lambda(T)\,d\tau^\prime  d\mu
$$ (allangmu)

Comparing these two terms with {eq}`fluxtrans4`, note that the $1/\mu$ has been cancelled from the second term in {eq}`allangmu`, but the structure is otherwise the same for both flux and radiance.

+++

### Flux transmissivity


-   To make progress, first swap the limits of integration:


$$
\begin{gather}
      F_{\lambda \uparrow} =   \pi B_{\lambda 0}(T_s)\, 2 \int_0^1 \mu  \exp(-\tau/\mu) d\mu
      +      \nonumber\\
     \int_0^{\tau} \pi B_\lambda(T)\, 2 \int_0^1 \exp\left( -\frac{(\tau - \tau^\prime)}{\mu}
     \right ) \, d\mu\, d\tau^\prime
 \end{gather}
$$ (allanglesmuswapII)

(Remember that $T$ does depend on $z$, and therefore $B_\lambda(T)$ has to stay inside the $\tau^\prime$ integral.)

+++

-   Look what happens to this equation if we define $t_f$, the *flux transmissivity* as:

$$
t_f=  2 \int_0^1 \mu  \exp(-(\tau - \tau^\prime)/\mu) d\mu
$$ (fluxtrans)

and differentiating wrt $\tau^\prime$:

$$
dt_f=  2 \int_0^1  \exp(-(\tau - \tau^\prime)/\mu) d\mu d\tau^\prime
$$ (fluxtransb)


Plug these into {eq}`allanglesmuswapII` and get:

$$
F_\uparrow = \pi  B_{\lambda 0}(T_s) \, t_f(0,\tau)
    +  \int_0^{\tau}  \pi \, B_\lambda(T)\,d t_f(\tau^\prime,\tau)
$$ (allangles2c)

+++

### Exponential integrals

#### calculating $t_f$

-   But how do we get values for $t_f$ and $dt_f$ if we can’t do
    the integration? 
    
    – In {ref}`week9:pydiffuse` we use python to evaluate:

    $$
    t_f=  2 \int_0^1 \mu  \exp(-(\tau - \tau^\prime)/\mu) d\mu = 2 E_3(\tau)
    $$ (fluxtrans2)

-   As we show there, it turns out to  a very good approximation:

    $$
    t_f(\tau) = 2 E_3(\tau) \approx \exp \left (- 1.666 \tau \right )
    $$ (expapprox0)

#### calculating $dt_f$


It turns out that $\frac{dE_3}{d\tau^\prime} = -E_2(\tau^\prime)$ (see [wikipedia](https://en.wikipedia.org/wiki/Exponential_integral)).  

In assignment 7 you'll show that 

$$
\frac{dt_f(\tau,\tau^\prime)}{d\tau^\prime} = 2E_2(\tau,\tau^\prime) \approx 1.666\exp(-1.666(\tau - \tau^\prime))
$$(dtf)

In words, that means that the flux sees a layer that is effectively 5/3 times
thicker, compared with the radiance case  at $\mu=1$ (straight up/down), for both the flux transmission
and the weighting function $dt_f$. Be sure you understand why this make physical sense.

+++

### Matching with Wallace and Hobbs eq. 4.46

Convince yourself that Wallace and Hobbs eq. 4.46

$$
T_\nu^f \simeq e^{-\tau_\nu / \bar{\mu}}
$$
where

$$
\frac{1}{\bar{\mu}} \equiv \sec 53^{\circ}=1.66
$$

is identical to {eq}`expapprox0`

and that their equation 4.56:

$$
\left(\frac{d T}{d t}\right)_\nu=-\frac{\pi}{c_p} k_\nu r B_\nu(z) \frac{e^{-\tau_\nu / \bar{\mu}}}{\bar{\mu}}
$$

is actually:

$$
\left(\frac{d T}{d t}\right)_\nu=-\frac{\pi}{c_p} k_\nu r B_\nu(z) dt_f
$$

+++

## Summary

+++

Bottom line:  the longwave radiation code in a climate model:

- Calculates $\Delta \tau_\lambda$, the optical thickness for every model layer $n$ and for 30-40 different wavelengths

- Uses the temperature and the Planck function to get $B_\lambda (T_n)$ in each layer and wavelength

- Starts from the lowest model level for the upward flux, and the highest model level
  for the downward flux, and finds $F_{\lambda \uparrow}$ and $F_{\lambda \downarrow}$
  for each layer and wavelength using the angle-integrated Schwartzchild equation.  Integrating {eq}`allangles2c` across layer $n$ assuming constant $T_{layer}$ we get the upward flux through the top of layer $n$ as:

    $$
    F_{\lambda \uparrow n} = F_{\lambda \uparrow n-1}
        +   B_\lambda(T_n)(1 - t_f(\Delta \tau_n))
    $$ (allangles2Bmodel)


    and the downward flux (downward negative) though the bottom of layer $n$ is: 

    $$
    F_{\lambda \downarrow n} = F_{\lambda \downarrow n+1}
        -  B_\lambda(T_n)(1 - t_f(\Delta \tau_n))
    $$ (allangles2Bmodelc)

- Gets the net flux $F_{net, n} = F_{\uparrow n} + F_{\downarrow n }$ through every  level by summing over all wavelengths

- Gets the heating rate in K/second for each layer

  $$
  \frac{dT_n}{dt} = -\frac{1}{\rho c_p} \frac{dF_{net\,n}}{dz}
  $$

- Update each layer temperature for the timestep (say $\Delta t = 20$ minutes)

  $$
  \frac{dT_{t+1,n}}{dt} = T_{t,n} \Delta t
  $$

```{code-cell} ipython3

```
