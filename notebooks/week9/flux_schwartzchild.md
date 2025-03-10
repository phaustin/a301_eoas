---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: pandoc
      format_version: 3.6.2
      jupytext_version: 1.16.6
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  nbformat: 4
  nbformat_minor: 5
---

::: {#d9641126-63a8-454e-84e7-95cc6fc12884 .cell .markdown}
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

## Integration over optical depth

For slant paths start by rewriting {eq}`schwart2` in {ref}`week5-schwartzA` to account for $\mu = \cos \theta$

\$\$

\$\$

# The diffusivity approximation

From the {ref}`heating` notes we have the heating rate equation {eq}`temprate` used by cloudsat:

$$
\frac{dT}{dt} = \frac{1}{\rho c_p} \frac{dE_{net}}{dz}
$$

But how do we get `E_{net}` if the satellites only measure radiance `L`? Graphically, this is the
situation we know how to solve, from {ref}`week4_schwartz` notes:

:::{figure} figures/schwartzchild.png
:name: schwartzchild2
:scale: 35
:::

::: {#1c4280dd-70ef-40fd-94bc-d4213ea72b83 .cell .markdown}
But this only works for photons that are going straight up or straight down.
For the flux, we need to count
every photon at going up at any zenith angle $\mu = \cos \theta$. Our situation is more like this:

:::{figure} figures/diffuse_flux.png
:name: diffuse
:scale: 55
:::

Where does that leave us? Surprisingly, moving from radiance to flux is reasonably approximated by simply increasing the optical thickness of the layer, to take into account the fact
that almost all photons have further to travel through the layer than those that are
going straight up. Specifically for a constant temperature layer we found {eq}`rad_constant`:

$$
L_\lambda = L_{\lambda 0} \exp( -\tau_{\lambda T}  ) + B_\lambda (T_{layer})(1- \exp( -\tau_{\lambda T} ))
$$ (rep_constant)

## Accounting for slant paths

Nothing in the derivation of {eq}`rad_constant` prevents us from
setting the zenith angle for the photon paths
to something besides $\cos \theta = 0\ (\mu = 1)$. Step 1 is to remember the relationship between
$L$ and $E$. For upward flux we integrate over the upward facing hemisphere:

$$
\begin{align}
        E&= \int_0^{2 \pi} \int_0^{\pi/2} \cos \theta\, L \sin \theta d\theta d\phi \\
        &\text{or changing variables $\mu=\cos \theta$ integrating over azimuth $\phi$}: \\
        E&= 2\pi\int_0^{1}  \mu  L d\mu
\end{align}
$$ (allangles2)

For {eq}`rad_constant` we took $L$ out of the integral and got $E=\pi L$, but this isn't an option now, because the transmissivity depends on $\mu$. Specifically, with $\mu \neq 1$ we have new
definitions for the **slant transmissivity** $\hat{t}_s$:

$$
\begin{align}
        \hat{t_s} &= \exp \left ( \frac{(\tau - \tau^\prime)}{\mu} \right ) \\
   d\hat{t_s} &=\frac{d \hat{t_s}(\tau^\prime,\tau)}{d\tau^\prime} d\tau^\prime =
        \exp\left( -\frac{(\tau -
   \tau^\prime)}{\mu} \right ) \frac{1}{\mu} d\tau^\prime
 \end{align}
$$ (fluxtrans4)

We can't integrate this transmission over $\mu$ analytically, but the integrals are easy
to do numerically. As you'll show in a separate notebook, the following "diffusivity"
approximation is quite good:

$$
\hat{t}_f =  \int_0^1 \mu \exp \left ( \frac{(\tau - \tau^\prime)}{\mu} \right ) d\mu
    =  \exp \left (-1.66 (\tau - \tau^\prime) \right )
$$ (diffusivity)

where $\hat{t_f}$ is called the **flux transmissivity**.

This gives a the upward flux version of {eq}`rep_constant`:

$$
E_{\lambda \uparrow} = \pi L_{\lambda 0} \exp( -1.66 \tau_{\lambda T}  ) + \pi B_\lambda (T_{layer})(1- \exp( -1.66\tau_{\lambda T} ))
$$

And if we then integrate this over all wavelengths we get the **broadband flux equation**:

$$
E_{\lambda \uparrow} = \sigma T_0^4 \exp( -1.66 \overline{\tau}_{\lambda T}  ) + \sigma T_{layer}^4(1- \exp( -1.66 \overline{\tau}_{\lambda T} ))
$$

This is called the "diffusivity approximation": replace the vertical optical thickness $\tau$ by
$\frac{5}{3} \tau$ and multiply blackbody radiances by $\pi$.

-   Start with the equation for the upward radiance with $\mu=1$ which we saw in {eq}$calc1$:

    $$
    L_\lambda(\tau)= B_\lambda(T_{skin})( \exp(-\tau) +    \int_0^{\tau} \exp\left(  - (\tau -\tau^\prime) \right )
    B_\lambda(T)\, d\tau^\prime
    $$

-   Add the fact that the photons that travel along a slant path have lower transmissivity.
    In fact: they travel a distance $\Delta s = \Delta z/\cos \theta = \Delta z/\mu$ which
    is Stull's $\Delta s$ in his equation 2.31b

    $$
    L_\lambda(\tau,\mu)= B_\lambda(T_{skin})( \exp(-\tau/\mu) +    \int_0^{\tau} \exp\left(  - (\tau -\tau^\prime)/\mu \right )
      B_\lambda(T)\, \frac{d\tau^\prime}{\mu}
    $$ (newslant)

-   So define a new transmission for the slant path:

-   and use it to rewrite {eq}`newslant`:

    $$
    L_\lambda(\tau,\mu)= B_\lambda(T_{skin}) \hat{t}_{stot}  +    \int_0^{\tau} B_\lambda(T)\,d\hat{t_s}
    $$ (newslant2)

### Integrating over $\mu=\cos \theta$

-   In the {ref}`week2_flux_from_radiance` notes we turned blackbody isotropic radiance
    into a flux by taking the normal component and integrating over the hemisphere, in {eq}`flux_final`:

    $$
    \begin{align}
      E_\lambda&= \int_0^{2 \pi} \int_0^{\pi/2} \cos \theta\, I_\lambda \sin \theta d\theta d\phi \\
               &= 2 \pi  \int_0^1 \mu \, I_\lambda  d\mu
     \end{align}
    $$ (allangles2)

    assuming no dependence on $\phi$ and substituting $\mu= \cos \theta$

    $$
    E_\lambda=  2 \pi L_\lambda \int_0^1 \mu  d\mu  = 2 \pi \frac{\mu^2}{2} \Bigg \rvert_0^1 = 2 \pi  I_\lambda \frac{ 1}{ 2}
      = \pi L_\lambda
    $$ (allangles2)

## Radiance into flux

So do this to {eq}`Luptrans`

$$
\begin{gather}
 E_\uparrow = \int_0^{2 \pi} \int_0^{\pi/2} \cos \theta\,
 I_\lambda \sin \theta d\theta d\phi =  2\pi \int_0^1 \mu I_\lambda d \mu \notag\\
 = 2 \pi B_{\lambda 0}(T_s) \int_0^1 \mu  \exp(-\tau/\mu) d\mu \nonumber\\
 + 2 \pi \int_0^1
 \int_0^{\tau} \exp\left( -\frac{(\tau - \tau^\prime)}{\mu} \right ) B_\lambda(T)\,d\tau^\prime d\mu
\end{gather}
$$ (allanglesmu})

The difference
is that now our expression for $L_\lambda(\tau,\mu, \phi)$ depends on
the zenith angle $\theta$, so that the integral is more difficult (actually
it's impossible to do analytically).

Flux transmissivity
==================+

-   To make progress, first swap the limits of integration (ok because the layers\
    are plane parallel)

$$
\begin{gather}
      E_\uparrow =   \pi B_{\lambda 0}(T_s)\, 2 \int_0^1 \mu  \exp(-\tau/\mu) d\mu
      +      \nonumber\\
     \int_0^{\tau} \pi B_\lambda(T)\, 2 \int_0^1 \exp\left( -\frac{(\tau - \tau^\prime)}{\mu}
     \right ) \, d\mu\, d\tau^\prime
 \end{gather}
$$ (allanglesmuswapII)

(Remember that $T$ does depend on $z$, and therefore $B_\lambda(T)$ has to stay inside the $\tau^\prime$ integral.)

## Flux transmissivity cont

-   Look what happens to this equation if we define $t_f$, the ,

as:

$$
Tr_f=  2 \int_0^1 \mu  \exp(-(\tau - \tau^\prime)/\mu) d\mu
$$ (fluxtrans)

and differentiating wrt $\tau^\prime$:

$$
dTr_f=  2 \int_0^1  \exp(-(\tau - \tau^\prime)/\mu) d\mu d\tau^\prime
$$ (fluxtransb)

Plug these into {eq}`allanglesmuswapII` and get:

$$
E_\uparrow = \pi  B_{\lambda 0}(T_s) \, Tr_f(0,\tau)
    +  \int_0^{\tau}  \pi \, B_\lambda(T)\,d Tr_f(\tau^\prime,\tau)
$$ (allangles2B)

Exponential integrals
====================+

-   But how do we get values for $Tr_f$ and $dTr_f$ if we can't do

the integration? -- Use python to evaluate

$$
Tr_f=  2 \int_0^1 \mu  \exp(-(\tau - \tau^\prime)/\mu) d\mu = 2 E_3(\tau)
$$ (fluxtrans2)

exactly.

-   We wouldn't be any further ahead except that, it turns out to
    a very good approximation:

$$
Tr_f(\tau) = 2 E_3(\tau) \approx \exp \left (- \frac{5}{3} \tau \right )
$$ (expapprox0)

In words, that means that the flux sees a layer that is effectively 5/3 times
thicker, compared with the layer faced by photons pointed at $\mu=1$ (straight up).
Be sure you understand why this make physical sense.

Repeat the Schwartzchild problem

-   A 100 m thick nocturnal cloud layer with a temperature of 270 K floats

over a 300 K surface. The volume absorption coefficient of the cloud
is $\beta_a=0.01\  (m^{-1})$, and the downward longwave flux density from the
air above the cloud is 100 wm. Assuming that there is no absorption between
the surface and the cloud base

-   Find the total flux transmission of the cloud
-   Find the upward and downward monochromatic fluxes

$E_\lambda~ ( (W\,m^{-2}\mu m^{-1})$)
at a height $z=75$ m above cloud base and a wavelength of 10 mu m, assuming that
the downward flux at cloud top is $E_{10\,\mu m}= 12\  (W\,m^{-2}\mu m^{-1})$

## Python

-   href{/home/phil/public_html/courses/atsc301/repos/expint3.py}%

{expint3.py} plots 2 times the exact exponential integral calculated by
python and compares it to the approximation

$$
Tr_f(\tau) = 2 E_3(\tau) \approx \exp \left (- \frac{5}{3} \tau \right )
$$ (expapprox)

Not too shabby for such a simple approximation

## Fluxes continued

$$
\begin{gather}
   Tr_f(\tau) = 2 E_3(\tau) \approx \exp \left (- \frac{5}{3} \tau \right ) = \\
   \exp \left (- \tau/(3/5) \right )
   =\exp \left (- \tau/\cos 53^\circ \right ) \\
   = \exp \left (- \tau/ \overline{\mu} \right )
 \end{gather}
$$ (expapprox2)

-   So you if you like you can think of the flux as if it was a radiance

going through the layer at an angle of $53^\circ$.

or rewriting {eq}`allangles2B`

Or just think of it as passing though a layer that's
1.66 times thicker than $\tau$.

$$
E_\uparrow = \pi  B_{\lambda 0}(T_s) \, Tr(0,1.66\tau)
   +  \int_0^{\tau}  \pi \, B_\lambda(T)\,d Tr(1.66\tau^\prime,1.66\tau)
$$ (allangles3)

This is the approximation that we use for the day 17 problem.
:::
:::