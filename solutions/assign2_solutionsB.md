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
$$

In the limit $\lambda \rightarrow \infty$ the term $c_2 / \lambda T$ gets increasing small.  We can use the fact that 

$$
e^3  = 1+\frac{3^1}{1!}+\frac{3^2}{2!}+\frac{3^3}{3!}+ \ldots
$$

+++

## Question 4.32

Show that the approach in Exercise 4.5 in the text, when applied to the previous exercise, yields a temperature of

$$
T_s=T_E\left[\frac{1}{4}\left(\frac{6371}{8371}\right)^2\right]^{1 / 4}=158 \mathrm{~K}
$$


Explain why this approach underestimates the temperature of the satellite. Show that the answer obtained with this approach converges to the exact solution in the previous exercise as the distance between the satellite and the center of the Earth becomes large in comparison to the radius of the Earth $R_E$. [Hint: show that as $d / R_E \rightarrow \infty$, the arc of solid angle subtended by the Earth approaches $\pi R_E^2 / d^2$.]

```{code-cell} ipython3

```
