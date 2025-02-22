(mid-review1-sol)=
# Midterm Solutions: midterm sample questions I

## A. Beers law

Stull page 2.43 and the {ref}`week1-beerslaw` reading:

### A1

1. Prove that for a thin non-reflecting layer the change in emissivity
   = change in optical thickness, i.e. prove that:

   $$
   \Delta e_\lambda \approx  \Delta \tau_\lambda
   $$ (thin1)

   **Answer:**

   Assuming no reflection, we know that the absorptivity is:

   $a_\lambda = 1 - t_\lambda = 1 - \exp(-\tau)$

   and from Kirchoff’s law:

   $e_\lambda = a_\lambda$

   so take the differential:

   $d e_\lambda = da_\lambda = \exp(-\tau) d\tau$

   but for a thin layer we are expanding about
   (tau=0,exp(-tau) = 1) so

   $d e_\lambda \approx d\tau$ or going to finite differences

   $\Delta e_\lambda \approx \Delta \tau$

### A2

2. Repeat the problem above, but for a layer with an optical depth of $\tau_\lambda=1$.
   How does that change {eq}`thin1` ?

   **Answer:**

   Now the relationship has to be:

   $\Delta e_\lambda \approx \exp(-\tau) \Delta \tau$

   which makes sense because we are adding a thin layer $\Delta \tau$ onto
   an existing layer of thickness $\tau$, so the amount of light reaching
   the thin layer is going to be reduced by the transmittance $\exp( -\tau )$

### A3


3. Suppose you put ozone molecules in a 1 km long tunnel and measure an optical thickness of
   0.5 using an ultraviolet laser. You know that the ozone mixing ratio is 1 g/kg and the air
   density is 1 kg/$m^3$. What is the extinction coefficient $k$ in $m^2/kg$?

   **Answer:**

   $$
   \kappa_\lambda = \frac{\tau}{\rho_{air} r_{mix} \Delta z}
   $$

   Plugging in the numbers gives $k_\lambda = 0.5\ m^2/kg$

   **Answer:**

   For the slant path we would need to replace the vertical optical thickness:

   $$
   d \tau =  \kappa_\lambda \rho_g dz
   $$

   with the slant path optical thickness $\tau_s$:

   $$
   d \tau_s =  \kappa_\lambda \rho_g ds = \kappa_\lambda \rho_g dz/\cos \theta
   = \kappa_\lambda \rho_g dz/\mu
   $$

   Once we made that change, everything would work as before, just with a
   smaller transmittance due to the longer slant path for $\mu < 1$.

(mid_a4_solution)=
### A4

4. Find the narrow beam transmissivity, absorptivity and emissivity for a series of
   stacked layers of equal transmissivities and temperatures in a direction perpendicular to the layers.

   **Answer**
   
   First, note that temperature is a red herring, since we are assuming that the optical properties
   of the material oare independent of temperature.
   
   If we assume the layers are not reflective, then every photon either has to be absorbed or
   transmitted as it goes through the layers.  The radiance through layer 1 is:
   
   $$
   L_1 = L_0 \exp(-\tau)
   $$
   
   while the radiance through layer 2 is 
   
   $$
   L_2 = L_1 \exp(-\tau) = L_0 \exp(-\tau) \exp(-\tau) = L_0 \exp(-2 \tau)
   $$
   and so on.
   
   So if the number of layers is N, then the transmissivity is $\exp(-N \tau)$. If reflectivity
   is zero that means the absorptivity is $1 - \exp(-N \tau)$ and by Kirchoff's law
   that is also the emissivity.


## Solid angle and radiance

From {ref}`radiance` reading:

### B1

1. Calculate the solid angle subtended by a cone with an angular width of
   $\Delta \theta$ =20 degrees.

   **Answer**

   $$
   \omega = \int_0^{2\pi} \int_0^{10} \sin \theta d\theta d\phi = -2\pi (\cos(10) - \cos(0))
     = 2\pi (1 - \cos(10)) = 2\pi(1 - 0.985) = 0.0954\ sr
   $$(solid)


### B2

2. A laser pointer subtends the same solid angle as the sun: $7 \times 10^{-5}$ sr. You shine it at a wall that is 10 meters away. What is the radius of the circular dot?

   **Answer:**

   $$
   \begin{aligned}
      r=10\ m \\
      A/r^2= 7 \times 10{-5}\ sr \\
      A=7 \times 10^{-3}\ m^2 = \pi R^2\\
      R=(.007/(\pi))^{0.5} \approx 5\ cm
   \end{aligned}
   $$

### B3

3. What is the angle of the cone if $\omega = 7. \times 10^{-5}\ sr$?

   **Answer:**

   R= 0.05 m at 10 m, $\theta = \tan^{-1}(0.05/10) \approx 0.005$ radians or about 0.3 degrees

(mid_b4_solution)=
### B4


4. A satellite orbits 800 km above the earth and has a telescope with a field of view
   that covers 1 $km^2$ directly below it (i.e. at nadir). If that 1 $km^2$ is ocean with
   an emissivity $\epsilon =1$ at a temperature
   of 280 K, calculate the surface flux in $W\,m^{-2}$ reaching the satellite between 10-11 microns,
   assuming no atmospheric absorption or emission.

   **Answer:**
   
   We can use the parallel beam approximation for small solid angles:
   
   $$
   \Delta \omega = \frac{A}{R^2} = \frac{1}{800^2} = 1.56 \times 10^{-6}\ sr
   $$

   From the [Planck diagram](https://drive.google.com/file/d/12ZDN8NZzgafeCMDTy4t0u-w80o3-foNT/view)
   I get a radiance from the 280 K ocean of about 7 $W\,m^2\,\mu m^{-1}\,sr^{-1}$ at a wavelength
   of 10.5 $\mu m$

   So putting that together gives:

   $$
   F_{sat} = L_{sea} \times \Delta \omega \times \Delta \lambda =  7 \times 1.56 \times 10^{-6} \times 1 = 
   1 \times 10^{-5}\ W\,m^{-2}
   $$

```python
1/800**2., 7*1.56e-6
```

### B5

5. Suppose that a satellite's orbit changes from a height of 800 km to a height of 600 km
   above the surface. If the telescope field of view stays the same, prove that
   the radiance stays constant.

   **Answer**:

   Suppose that at a height of 800 km the satellite sees a circular area of 1 $km^2$ in a single
   pixel. If the surface is emitting a flux of $E_{fsc}\ W/m^2$ then the those photons will
   be emitted into a hemisphere of radius $h=800\ km$, and the flux at the satellite
   will be power/area = $E_{sfc} \times 1\ km^2\ Watts/(2 \pi h^2\ meters^2)$.

   Note that the flux
   will increase the altitude $h$ decreases, because of the $1/h^2$ factor.

   Now suppose the satellite descends to h=600 km. Again, if the power emitted by the surface stayed the same,
   then the flux reaching the satellite would
   increase by a factor $(800/600)^2$ because the same Watts are being distributed over a smaller
   hemisphere. The power emitted by the surface is reduced however, because the pixel is smaller.
   The pixel radius before was $R=800 \tan(\theta)\ km$, where $\theta$ is the half-angle of the cone
   field of view of the telescope. At 600 km altitude, $R=600\,\tan(\theta)$, and since the pixel
   area is $\pi R^2= \pi h^2 (\tan\theta)^2$ and $E_{sfc}$ hasn't changed, the emitted power is lower by $(600/800)^2$, exactly
   counteracting the inverse squared increase in the flux due to bringing the satellite closer to the surface. Since the flux at the
   satellite is the same, and the field of view is the same, the radiance hasn't changed.

## Schwartzchild equation

From Stull p. 224 and the {ref}`week5-schwartzA` reading:

(mid_c1_solution)=
### C1

1. Show that $e_\lambda$ = $a_\lambda$ for a gas that absorbs and transmits but doesn't reflect.
   (hint: put the gas between two black plates, assume that the gas and the plates are at the
   same temperature and show that the 2nd law is violated if $e_\lambda \neq a_\lambda$

   **Answer:**

   Suppose the gas has absorptivity a and emissivity ε and they are new equal to each other.
   The it will be transmitting $(1 - a)\sigma T^4$ from the right wall to the left wall,
   and emitting $\epsilon \sigma T^4$ to the left wall, while the (black) left wall will
   be emitting $\sigma T^4$. The temperature of the wall will change because the balance
   will be:

   $$
   \begin{aligned}
   \sigma T^4 &= \epsilon \sigma T^4 + (1 - a) \sigma T^4 \\
   & \text{so:}\\
   1 &= 1 + (\epsilon - a)
   \end{aligned}
   $$

   i.e. the flux at the wall will be unbalanced, and the temperature
   will change in violation of the 2nd law, unless ε=a for the gas.

### C2

2. Integrate the Schwartzchild equation

   $$
        dL_{\lambda,absorption} + dL_{\lambda,emission}  = -L_\lambda\, d\tau_\lambda + B_\lambda (T_{layer})\, d\tau_\lambda
   $$

   across a constant temperature layer of thickness $\Delta \tau_\lambda$ over a surface
   emitting radiance $L_{\lambda 0}$
   and show that the radiance at the top of a constant temperature layer is given by:

   $$
   L_\lambda = L_{\lambda 0} \exp( -\Delta \tau_\lambda  ) + B_\lambda (1- \exp( -\Delta \tau_\lambda))
   $$

   **Answer:**

   See the section "Adding emission to Beers law" in the {ref}`week5-schwartzA` notes.

