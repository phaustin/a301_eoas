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

(assign2b_solution)=
# Assignment 2: solutions part B

 4.25,  4.32, 4.39

+++

## Question 4.25

Show that for radiation with very long wavelengths, the Planck monochromatic intensity $B_λ (T)$ is linearly proportional to absolute temperature. This is referred to as the Rayleigh-Jeans limit.

### Answer

Recall WH 4.10:

$$
B_\lambda(T)=\frac{c_1 \lambda^{-5}}{\pi\left(e^{c_2 / \lambda T}-1\right)}
$$ (eq:planck)

In the limit $\lambda \rightarrow \infty$ the term $c_2 / \lambda T$ gets increasing small.  We can use the fact that 

$$
e^x  = 1+\frac{x^1}{1!}+\frac{x^2}{2!}+\frac{x^3}{3!}+ \ldots
$$
to get the small x approximation by keeping only the first order term:

$$
e^x  \approx 1+ x
$$ (eq:small)

Inserting {eq}`eq:small` into {eq}`eq:planck` gives:

$$
B_\lambda(T) \approx \frac{c_1 \lambda^{-5} \lambda T}{\pi  c_2 } = \frac{c_1 \lambda^{-4} T}{\pi  c_2 } 
$$ (eq:rj)

which is the Rayleigh-Jean approximation.

+++

## Question 4.32

Show that the approach in Exercise 4.5 in the text, when applied {numref}`p4_31` yields a temperature of

$$
T_s=T_E\left[\frac{1}{4}\left(\frac{6371}{8371}\right)^2\right]^{1 / 4}=158 \mathrm{~K}
$$


Explain why this approach underestimates the temperature of the satellite. Show that the answer obtained with this approach converges to the exact solution in the previous exercise as the distance between the satellite and the center of the Earth becomes large in comparison to the radius of the Earth $R_E$. [Hint: show that as $d / R_E \rightarrow \infty$, the arc of solid angle subtended by the Earth approaches $\pi R_E^2 / d^2$.]

```{code-cell} ipython3

```
