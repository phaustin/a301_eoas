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

## Integration over zenith angle

We can’t integrate {eq}`fluxtrans4` over $\mu$ analytically, but the integrals are easy
to do numerically. As we'll show in a {ref}`week9:pydiffuse`, the following “diffusivity”
approximation is quite good:

$$
t_f =  \int_0^1 \mu \exp \left ( \frac{(\tau - \tau^\prime)}{\mu} \right ) d\mu
    =  \exp \left (-1.66 (\tau - \tau^\prime) \right )
$$ (diffusivity)

where $t_f$ is called the **flux transmissivity**.

This gives a the upward flux version of {eq}`rep_constant`:

$$
F_{\lambda \uparrow} = \pi L_{\lambda 0} \exp( -1.66 \tau_{\lambda T}  ) + \pi B_\lambda (T_{layer})(1- \exp( -1.66\tau_{\lambda T} ))
$$

And if we then integrate this over all wavelengths we get the **broadband flux equation**:

$$
F_{\lambda \uparrow} = \sigma T_0^4 \exp( -1.66 \overline{\tau}_{\lambda T}  ) + \sigma T_{layer}^4(1- \exp( -1.66 \overline{\tau}_{\lambda T} ))
$$

+++

### Temperature changing with height

To summarize: define the “diffusivity approximation” as: replace the vertical optical thickness $\tau$ by
$\frac{5}{3} \tau$ and multiply blackbody radiances by $\pi$.  But what about the case where temperature is
changing with height?

-   Start with the equation for the upward radiance with $\mu=1$ which we saw in {eq}$calc1$:

    $$
    L_\lambda(\tau)= B_\lambda(T_{skin})( \exp(-\tau) +    \int_0^{\tau} \exp\left(  - (\tau -\tau^\prime) \right )
    B_\lambda(T)\, d\tau^\prime
    $$

-   Add the fact that the photons that travel along a slant path have lower transmissivity.
    In fact: they travel a distance $\Delta s = \Delta z/\cos \theta = \Delta z/\mu$ which
    is Stull’s $\Delta s$ in his equation 2.31b

    $$
    L_\lambda(\tau,\mu)= B_\lambda(T_{skin})( \exp(-\tau/\mu) +    \int_0^{\tau} \exp\left(  - (\tau -\tau^\prime)/\mu \right )
      B_\lambda(T)\, \frac{d\tau^\prime}{\mu}
    $$ (newslant)

-   So define a new transmission for the slant path:

-   and use it to rewrite {eq}`newslant`:

    $$
    L_\lambda(\tau,\mu)= B_\lambda(T_{skin}) \hat{t}_{stot}  +    \int_0^{\tau} B_\lambda(T)\,d\hat{t_s}
    $$ (newslant2)

+++

#### Integrating over $\mu=\cos \theta$

-   In the {ref}`sec:week1-flux-from-radiance` notes we turned blackbody isotropic radiance
    into a flux by taking the normal component and integrating over the hemisphere, in {eq}`flux_final`:

    $$
    \begin{align}
      F_\lambda&= \int_0^{2 \pi} \int_0^{\pi/2} \cos \theta\, L_\lambda \sin \theta d\theta d\phi \\
               &= 2 \pi  \int_0^1 \mu \, L_\lambda  d\mu
     \end{align}
    $$ (allangles2)

    assuming no dependence on $\phi$ and substituting $\mu= \cos \theta$

    $$
    F_\lambda=  2 \pi L_\lambda \int_0^1 \mu  d\mu  = 2 \pi \frac{\mu^2}{2} \Bigg \rvert_0^1 = 2 \pi  L_\lambda \frac{ 1}{ 2}
      = \pi L_\lambda
    $$ (allangles2)

+++



+++

## Radiance into flux

So do this to {eq}`Luptrans`

$$
\begin{gather}
 F_\uparrow = \int_0^{2 \pi} \int_0^{\pi/2} \cos \theta\,
 L_\lambda \sin \theta d\theta d\phi =  2\pi \int_0^1 \mu L_\lambda d \mu \notag\\
 = 2 \pi B_{\lambda 0}(T_s) \int_0^1 \mu  \exp(-\tau/\mu) d\mu \nonumber\\
 + 2 \pi \int_0^1
 \int_0^{\tau} \exp\left( -\frac{(\tau - \tau^\prime)}{\mu} \right ) B_\lambda(T)\,d\tau^\prime d\mu
\end{gather}
$$ (allanglesmu})

The difference
is that now our expression for $L_\lambda(\tau,\mu, \phi)$ depends on
the zenith angle $\theta$, so that the integral is more difficult (actually
it’s impossible to do analytically).

+++



+++

### Flux transmissivity


-   To make progress, first swap the limits of integration (ok because the layers  
    are plane parallel)

$$
\begin{gather}
      F_\uparrow =   \pi B_{\lambda 0}(T_s)\, 2 \int_0^1 \mu  \exp(-\tau/\mu) d\mu
      +      \nonumber\\
     \int_0^{\tau} \pi B_\lambda(T)\, 2 \int_0^1 \exp\left( -\frac{(\tau - \tau^\prime)}{\mu}
     \right ) \, d\mu\, d\tau^\prime
 \end{gather}
$$ (allanglesmuswapII)

(Remember that $T$ does depend on $z$, and therefore $B_\lambda(T)$ has to stay inside the $\tau^\prime$ integral.)

+++

-   Look what happens to this equation if we define $t_f$, the flux transmissivity as:

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
$$ (allangles2B)

+++

### Exponential integrals


-   But how do we get values for $t_f$ and $dt_f$ if we can’t do

the integration? – Use python to evaluate

$$
t_f=  2 \int_0^1 \mu  \exp(-(\tau - \tau^\prime)/\mu) d\mu = 2 E_3(\tau)
$$ (fluxtrans2)

exactly.

-   We wouldn’t be any further ahead except that, it turns out to
    a very good approximation:

$$
t_f(\tau) = 2 E_3(\tau) \approx \exp \left (- \frac{5}{3} \tau \right )
$$ (expapprox0)

In words, that means that the flux sees a layer that is effectively 5/3 times
thicker, compared with the layer faced by photons pointed at $\mu=1$ (straight up).
Be sure you understand why this make physical sense.

+++

### Fluxes continued

$$
\begin{gather}
   t_f(\tau) = 2 E_3(\tau) \approx \exp \left (- \frac{5}{3} \tau \right ) = \\
   \exp \left (- \tau/(3/5) \right )
   =\exp \left (- \tau/\cos 53^\circ \right ) \\
   = \exp \left (- \tau/ \overline{\mu} \right )
 \end{gather}
$$ (expapprox2)

-   So you if you like you can think of the flux as if it was a radiance

going through the layer at an angle of $53^\circ$.

or rewriting {eq}`allangles2B`

Or just think of it as passing though a layer that’s
1.66 times thicker than $\tau$.

$$
F_\uparrow = \pi  B_{\lambda 0}(T_s) \, t_f(0,1.66\tau)
   +  \int_0^{\tau}  \pi \, B_\lambda(T)\,d t_f(1.66\tau^\prime,1.66\tau)
$$ (allangles3)

+++
