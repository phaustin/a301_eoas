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

(heating-rate)=

+++

# Finding the heating rate of the atmosphere

How does a climate model calculate the temperature change at every vertical level during a timestep? Wallace and Hobbs present
the **heating rate equation** (eq. 4.52 on p. 136) which relates the change in temperature to the net flux divergence $Q_r$ across
a layer infinitesimal thickness:

$$
\rho c_p \frac{d T}{d t}= \frac{dF_n}{d z} = Q_r
$$
where $F_n$ = $F_\downarrow + F_\uparrow$, with the convention that downward flux is positive (heating) and upward flux is
negative (cooling)

They solve this with an approximation to get eq. 4.56:

$$
\left(\frac{d T}{d t}\right)_\nu=-\frac{\pi}{c_p} k_\nu r B_\nu(z) \frac{e^{-\tau_\nu / \bar{\mu}}}{\bar{\mu}}
$$ (wh_dTdt)
note that there is a typo below this equation, since $\overline{\mu} \neq 1.66$. As they say on p. 136 eq. 4.47

$$
\frac{1}{\bar{\mu}} \equiv \sec 53^{\circ}=1.66
$$

After the break we'll derive {eq}`wh_dTdt` and use it, but for the midterm we will instead ignore that equation and calculate the heating rate
the way a global climate model does.  We will still use the fact that you can 
convert the Schwartzchild equation for radiance into an equation for flux by multiplying the vertical optical thickness $\tau$ by a factor
of 1.66, effectively make the atmosphere $66\%$ thicker for flux than for radiance.

+++



+++

## Schwartzchild equation for flux

Here's what the diffusivity approximation look like in practice.  First remember the Schwartzchild equation for flux:

$$
L_\lambda(\tau_T)= B_\lambda(T_{skin}) \exp(-\tau_T) +    \int_0^{\tau_T} B_\lambda(T)\, d\hat{t}
$$ (main)

where $\hat{t}(\tau_T) = \exp(-\tau_T)$ is the total transmissivity of a layer with optical thickness $\tau_T$ and
$\hat{t} = \exp \left (-(\tau_T - \tau) \right )$ is the transmissivity of the atmosphere from the top of the layer (where the optical depth=$\tau_T$), to a height at which the optical depth= $\tau$.

Here’s the picture, note that we're using a coordinate system where $\tau$ increases with height:

:::{figure} figures/schwartzchild.png
:name: schwartzchild_rep
:scale: 40
:::

If $T$ is constant with height then integrating {eq}`main` is simple:

$$
\begin{aligned}
      L_\lambda(\tau_T) &= B_\lambda(T_{skin}) \exp(-\tau_T) +    B_\lambda(T) \int_0^{\tau_T} \, d\hat{t}\\
        &= B_\lambda(T_{skin}) \exp(-\tau_T) +    B_\lambda(T)(\hat{t}(\tau_T) - \hat{t}(0) ) \\
        &= B_\lambda(T_{skin}) \exp(-\tau_T) +    B_\lambda(T)(1 - \exp(-\tau_T) )
  \end{aligned}
$$ (main2)

+++

For fluxes, we have a new flux transmission, $\hat{t}_f = \exp(-1.666 \tau)$ So using that:

$$
\begin{aligned}
      F_\lambda(\tau_T) &= F_{bb \lambda}(T_{skin}) \exp(-1.66 \tau_T) +    F_\lambda(T) \int_0^{\tau_T} \, d\hat{t}\\
        &= F_\lambda(T_{skin}) \exp(-1.66 \tau_T) +    F_\lambda(T)(\hat{t}_f(\tau_T) - \hat{t}(0) ) \\
        &= F_\lambda(T_{skin}) \exp(-1.666 \tau_T) +    F_\lambda(T)(1 - \exp(-1.666\tau_T) )
  \end{aligned}
$$ (main3)

+++

## Net flux

This gives us the net upward flux at the top of the layer.  We can
do the same integration the top of the atmosphere down and from $\theta=\pi/2$ to $\theta = \pi$ and 
get the downard flux passing through that level. 
Finally, we can integrate over all wavelengths to the the total net flux entering and leaving the layer.

The final result will be a picture that looks like this:

:::{figure} figures/layer_budget.png
:scale: 110
:::

To get the heating rate in $W\,m^{-2}$ for the layer above, use the following convention:

1.  Downward fluxes are positive (heating), upward fluxes are negative (cooling)

2.  The net flux $F_n = F_\uparrow + F_\downarrow$

3.  The heating rate is then defined as:

    $$
    \Delta F_n = F_{nTop} - F_{nBot} = \left ( (60 - 20) - (80 - 25) \right )= (40 - 55) = -15\ W\,m^{-2}
    $$

In other words, the layer is cooling at a rate of -15 $W\,m^{-2}$, because less energy is
entering from the top of the layer than is exiting from below.

+++

## Temperature change

To turn the radiative heating rate into a rate of temperature change, we need to use the first law of thermodynamics
(see Stull equation 3.4a):

$$
\frac{dH}{dt} = \Delta F_n
$$

where $H$ (units: $Joules/m^2$) is called the *enthalpy* (note that the units work out to $W/m^2$). The enthalpy of
a 1 $m^2$ column of thickness $\Delta z$ is related to the temperature T via the **heat capacity at constant pressure** $c_p$
(units: $J\,kg^{-1}\,K^{-1}$ and the density $\rho$ ($kg\,m^{-3}$):

$$
H=\rho\, c_p\, \Delta z\, T
$$

We define the **specific enthalpy** *h* as the enthalpy/unit mass = $h=H/(\rho \Delta z)$ where we are implicitly assuming that
our column is 1 $m^2$

Putting these two equations together gives the heating rate, $Q_r$ (units: K/second):

+++

$$
\rho c_p \Delta z \frac{dT}{dt} &= \Delta F_n\\
Q_r = \frac{dT}{dt} &= \frac{1}{\rho c_p} \frac{\Delta F_n}{\Delta z} = \frac{1}{\rho c_p} \frac{dF_n}{dz}
$$ (heating)

+++

## Summary

So the recipe for advancing the model 1 timestep:

1) calculate the optical depth $\tau$ in every layer
2) start from the surface and for each layer, calculate the flux transmittance, using $1.66 \tau$ for the optical depth
3) use the Schwartzchild equation with constant temperature to calculate the upward flux leaving the top of the layer, given the flux
   from below and the emission from the layer
4) repeat starting at the top of the atmosphere and moving downward
5) find the net flux $F_n$ at each level, and the heating rate $Q_r$ across each layer
6) use {eq}`heating` to get the rate of change of temperature, and increase or decrease the temperature by

   $$
   \Delta T = Q_r \Delta t
   $$
   where the timestep $\Delta t$ is typically 20 minutes.


```
