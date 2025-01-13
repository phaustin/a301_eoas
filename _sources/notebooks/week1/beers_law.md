(week1-beerslaw)=
# Beers and inverse squared laws

Comments/derivations for the material in  Stull p. 38-39

(differences)=

## Differences, differentials and derivatives

1. What is a derivative?

- According to
  [wikipedia](https://en.wikipedia.org/wiki/Derivative), a
  derivative is defined as:

  The derivative of a function of a real variable measures the
  sensitivity to change of a quantity (a function value or dependent
  variable) which is determined by another quantity (the independent
  variable).

2. What is the derivative of $F = \sigma T^4$ with respect to T?

$$
\frac{dF}{dT} = \frac{d \sigma T^4}{dT} = 4 \sigma T^3
$$

Does that mean that you are free to treat dF/dT as a fraction, and
cancel dT in the denominator to write:

$$
dF = \frac{d \sigma T^4}{dT} dT = 4 \sigma T^3 dT
$$

Scientists (and mathematicians) do this all the time, but that isn't how
derivatives work -- dF/dT is a function, not a fraction. So what is
really going on?

3. Instead, we need to treat the differentials dF and dT as limits, not
   numbers. We know that the following is true: given a small
   temperature difference $\Delta T$ the flux difference
   $\Delta F$ is aproximately:

$$
\Delta F \approx  \frac{dF}{dT} \Delta T =  4 \sigma T^3 \Delta T
$$

i.e. -- change in x times slope = change in y.

This equation in words is called a "first order Taylor series expansion"
of the function $F = \sigma T^4$. It is not exact, but it gets
better as $\Delta T$ gets smaller. We can make it exact by writing
out the whole Taylor series expansion which is a power series with an
infinite number of terms. (See the Wikipedia entry
[here](https://en.wikipedia.org/wiki/Taylor_series))

4. What is a differential?

Roughly, the differentials dF and dT represent limits that are evaluated
by integration:

$dT = \lim{\  \Delta T \to 0}$, so that
$\int dT = T$ and

$$
dF = \lim_{ \Delta T \to 0} \Delta F
$$

So if we take the $\lim{\  \Delta T \to 0}$ we can write

$$
dF = \frac{d \sigma T^4}{dT} dT = 4 \sigma T^3 dT
$$

Note that this is just doing the steps in Stull p. 38 in the opposite
order. He starts with my last equation and winds up with 3). The
advantage of the alternative approach we're using here is that we don't
need to treat the function $\frac{dF}{dT}$ as if it can be ripped
apart to get $dF$ and $dT$. If you really care, I recommend
reading [this
answer](http://math.stackexchange.com/questions/23902/what-is-the-practical-difference-between-a-differential-and-a-derivative)
to a question about differentials. This is also closely related to the
[chain rule](https://en.wikipedia.org/wiki/Chain_rule) for
derivatives of functions.

By taking the limit as $\Delta T$ approaches 0 we've turned a
*difference equation* for the number $\Delta F$ (which we can
solve in python) into a *differential equation* for the differential
$dF$ (which we can integrate using calculus).

(beers-law-diff)=

## Beers law -- using differentials

Both physics (Maxwell's equations) and observations show that when a
narrow beam of photons are travelling through a material (like air or
water) of constant composition, the flux obeys "Beer's law":

$$
F(s) = F_i \exp (-n b s)
$$

where $s\ (m)$ is the distance travelled (the path length),
$n\ (\#/m^3)$ is the number denstiy of reflecting/absorbing
particles and $b\ (m^2)$ is the extinction cross section due to
both absorption and scattering. You can think of $b$ as the
*target size* of the particles (molecules, smoke particles etc.) which
may be much different than the physical size of the particle because of
quantum mechanical and wave interference effects.

To get the differential version of Beers law, take the derivitive and
use the limit argument we went through above and get:

$$
dF = F_i (-nb) \exp(-nbs) ds =  (-nb) F ds
$$

or

$$
\frac{dF}{F} = -n b ds
$$

If we define the differential optical depth as:

$$
d\tau = n b ds
$$


Then we ge:

$$
\frac{dF^\prime}{F^\prime} = d \ln F^\prime = -d \tau^\prime
$$ (diffbeers)

and integrating from $\tau^\prime=0,\ F^\prime=F_i$ to
$\tau^\prime = \tau,F^\prime = F$ gives:

$$
\int_{F_i}^F  d \ln F^\prime = -\int_0^\tau d\tau^\prime
$$

$$
\ln \left ( \frac{F}{F_i} \right ) = - \tau
$$

$$
F = F_i \exp (-\tau)
$$

which is stull 2.31c. An important point is that the extinction cross
section $b$ can vary enormously over small wavlength ranges
(called "absorption bands") where the cross section can increase by a
factor of 100,000. This is why small concentrations of carbon dioxide
have such large impacts on climate.

Also note that now that we have the differential form of Beer's law, we
don't have to assume that $n$ or $b$ are constant, we can
make them depend on position and just do the (more complicated) integral
to get $\tau$

## Inverse Square Law: In-class problem in energy conservation

On page 39, Stull asserts the inverse square law:

$$
F_2 = F_1^* \left ( \frac{R_1^2}{R_2^2} \right )
$$

1. Prove this using conservation of energy (i.e. conservation of Joules)

2. Suppose a 10 cm x 10 cm piece of white paper with a visible
   reflectivity of 80% is pinned to a wall and illuminated by visible
   light with a flux of 100 $W\,m^{-2}$. If the paper reflects
   evenly in all directions (isotropic, not glossy), what is the flux
   from the paper 3 meters from the wall? What about 6 meters from the
   wall?  




3. Stull defines the direct beam transmissivity as:

   $$
   t = \frac{F}{F_{i}} = \exp(-\tau)
   $$

   Suppose I have two pieces of translucent glass that absorb but don't
   reflect light, and their indvidual transmissivities are $t_1$ and
   $t_2$. Use conservation of energy to prove that if we stack the
   two pieces, the combined transmissivity will be $t_1 \times t_2$,
   which means that the combined optical depth will be
   $\tau_1 + \tau_2$ (i.e. optical depths add). Note that I had to
   assume no reflection so that photons wouldn't bounce back and forth
   between the two plates. 
