(heating-rate)=

# Finding the heating rate of the atmosphere

## Review

Now that we have the diffusivity approximation from {ref}`assign6a`, we can solve the Schwartzchild equation for fluxes. First remember what it looks like for radiance:

$$
L_\lambda(\tau_T)= B_\lambda(T_{skin}) \exp(-\tau_T) +    \int_0^{\tau_T} B_\lambda(T)\, d\hat{t}
$$ (main)

where $\exp(-\tau_T)$ is the total transmissivity of an atmosphere with optical thickness $\tau_T$ and $\hat{t}$ is the transmissivity of the atmosphere from the top of the atmosphere (where the optical depth=0, to a height at which the optical depth= $\tau$.

Here's the picture:

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

For fluxes, we have a new flux transmission, `\hat{t}_f` = `\exp(-1.666 \tau)` So using that:

$$
\begin{aligned}
      F_\lambda(\tau_T) &= F_{bb \lambda}(T_{skin}) \exp(-1.66 \tau_T) +    F_\lambda(T) \int_0^{\tau_T} \, d\hat{t}\\
        &= F_\lambda(T_{skin}) \exp(-1.66 \tau_T) +    F_\lambda(T)(\hat{t}_f(\tau_T) - \hat{t}(0) ) \\
        &= F_\lambda(T_{skin}) \exp(-1.666 \tau_T) +    F_\lambda(T)(1 - \exp(-1.666\tau_T) )
  \end{aligned}
$$ (main3)

## Net flux

If we want to know whether the atmosphere is heating or cooling at a particular place, however, we need
to convert the monochromatic radiance $L_\lambda$ into the corresponding broadband flux $F$ by:

1. Integrating $\cos \theta L_\lambda d\omega$ over a hemisphere to get the monochromatic flux $F_\lambda$
   as in {ref}`moving` equation (1):

   $$
   \begin{aligned}
   F_{\lambda \uparrow} &= \int dF_\lambda = \int_0^{2\pi} \int_0^{\pi/2} \cos \theta \, L_\lambda \, d \omega =\int_0^{2\pi} \int_0^{\pi/2} L_\lambda \cos \theta  \sin \theta \, d\theta \ \, d \phi  \\
   &= \int_0^{2\pi} \int_0^1 L_\lambda  \mu d \mu\ \, d \phi
   \end{aligned}
   $$ (fluxrel)

   where the arrow $\uparrow$ reminds us we have integrated over all upward pointing radiances

2. Integrating $F_\lambda$ over all wavelengths to get $F$. If we can do that, then we can get
   an energy budget for a layer that looks like this:

   :::{figure} figures/layer_budget.png
   :scale: 110
   :::

To get the heating rate in $W\,m^{-2}$ for the layer above, use the following convention:

1. Downward fluxes are positive (heating), upward fluxes are negative (cooling)

2. The net flux $F_n = F_\uparrow + F_\downarrow$

3. The heating rate is then defined as:

   $$
   \Delta F_n = F_{nTop} - F_{nBot} = (60 - 20) - (80 - 25) = 40 - 55 = -15\ W\,m^{-2}
   $$

In other words, the layer is cooling at a rate of -15 $W\,m^{-2}$, because more energy is
exiting from top of the layer than is entering from below.

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

$$
\begin{aligned}

\rho c_p \Delta z \frac{dT}{dt} &= \Delta F_n\\

Q_r = \frac{dT}{dt} &= \frac{1}{\rho c_p} \frac{\Delta F_n}{\Delta z} = \frac{1}{\rho c_p} \frac{dF_n}{dz}
\end{aligned}
$$
