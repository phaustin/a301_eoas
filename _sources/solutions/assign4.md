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

(assign4)=
# Assignment 4

## Q1 - Q3
- From {ref}`mid-review1b` do problems A.4, B.4, C.1

## Q4

For the following set of layers:

:::{figure} images/two_layer.png
:name: twolayer
:scale: 50

Two grey layers over a black surface
:::


1) Write down a system of three equations in three unknowns for the equilibrium case where the fluxes at each level are in balance.
2) Write a python function that returns the three layer temperatures  $T_g,\ T_1,\ T_2$ given $\epsilon_1$, $\epsilon_2$ and $I_0$.  Hand in notebook that uses that function to solve for $\epsilon_1=0.8$, $\epsilon_2 = 0.4$ and $I_0 = 240\ W\,m^{-2}$ 
3) Possible helpful `numpy.linalg.solve` video from [Kindson the Genius](https://www.youtube.com/watch?v=lMI63LrKNnA)

