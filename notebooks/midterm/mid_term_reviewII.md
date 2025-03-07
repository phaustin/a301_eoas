(mid-review2)=

# Midterm review questions II

## D1. Schwartzchild with changing temperature

From {ref}`week5-schwartzA`

1. Equation {eq}`vary` allows you to find the radiance at
   height $z_T$ if given enough information about the atmosphere.

   $$
   L^\uparrow (\tau_T) = L^\uparrow (0) \, t_{tot} + \int_0^{z_T} t(\tau_T, \tau^\prime) B(\tau^\prime)\, d\tau^\prime
   $$ (vary)

   1. Draw a sketch of the layer, and label $L^\uparrow (0)$,
      $z_T$, $t_{tot}$, $t(\tau_T,\tau^\prime)$,
      $d\tau^\prime$, $B(\tau^\prime)$, where
      $z^\prime= z_T/2$

   2. Use the definition of the transmissivity
      $t(\tau_T, \tau^\prime)$ to prove that

      $$
      \int_0^{z_T} t(\tau_T,\tau^\prime) B(\tau^\prime)\, d\tau^\prime = \int_0^{z_T} B(t^\prime)\, dt^\prime
      $$ (eq_orig)

## D2 Beer's law

From {ref}`week1-beerslaw`

1. A 5 km thick ozone layer absorbs 30% of the ultraviolet sunlight that
   passes through it when the sun is directly overhead.

   1. What is the vertical optical thickness of the layer in the
      ultraviolet? (UV radiation is not reflected, only
      absorbed/transmitted)
   2. What is the value of the absorptivity at 4pm, when the sun is
      $60^\circ$ away from the zenith?
   3. Find the solid angle subtended by the sun when viewed from the earth (i.e. -- what is area/r^2 for the sun?)
   4. If the UV solar flux is 200 $W\,m^{-2}$ for overhead sun, what is the value of
      the radiance and the flux at 4pm?

## D3 Hydrostatic equation

From {ref}`hydro` and the {ref}`week6:weighting_funs` notebook.

1. A 10 km thick layer of an an atmosphere has constant temperature
   $T_{atm}$=280 K, a pressure/density scale height of
   $H=8\ km$ and is filled with a gas with a mass absorption
   coefficient of $k_\lambda$ = 0.2 at a wavelength of 10 .
   Underneath this layer is a black surface with a temperature of 290 K.
   The atmosphere is in hydrostatic equilibrium, the gas has a constant
   mixing ratio and a density at the surface of $\rho_0 = 10^{-3}\ kg\,m^{-3}$. Find:

   1. The vertical optical depth of the layer
   2. The layer transmission for radiance going straight up.
   3. The radiance, in at the top of the layer due to the surface and
      atmosphere.
   4. The brightness temperature $T_b$ (K) that a satellite would
      measure at $\lambda$=10 if there were no
      absorption/emission above 10 km. (see Planck function curves on
      next page).
