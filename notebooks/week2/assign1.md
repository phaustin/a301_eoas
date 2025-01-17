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

(sec:assign1)=
# Assignment 1, brightness temperatures

- Download assign1.ipynb from the [week2 folder](https://drive.google.com/drive/folders/1-Ja2wVKVIjkZb7Gx_rfc14J_aBYiknuw?usp=sharing)

- For this assignment you're asked to write a function to calculate the "brightness temperature", defined as the temperature a blackbody would need to have to emit an observed monochromatic radiance $I_\lambda$:

$$
  B_\lambda(T_b) = I_{\lambda\,observed}
$$
  


Fill in the notebooks cells indicated below and upload your notebook to canvas.

+++

## Question 1

In the cell below, write a function that calculates the blackbody radiance.  You can/should just adapt the code from {ref}`sec:planck_sol` so that it evaluates W&H 4.10:
  
  $$
  B_\lambda(T)=\frac{c_1 \lambda^{-5}}{\pi\left(e^{c_2 / \lambda T}-1\right)}
  $$


  Your function should have the following name and signature

+++

```python
def calc_Blambda(wavel, Temp):
    """
    Calculate the blackbody radiance (W&H 4.10)

    Parameters
    ----------

      wavel: float or array
           wavelength (meters)

      Temp: float
           temperature (K)

    Returns
    -------

    Blambda:  float or arr
           monochromatic blackbody radiance (W/m^2/m/sr)
    """
```

```{code-cell} ipython3
###  Question 1
###  your Blambda function here
###
```

## Question 2
### brightness temperature function

In the cell below, write a new function to compute the brightness temperature  $T_{bright}$.  It should have the following name and signature

```python
def calc_Tbright(wavel, I):
    """
    Calculate the brightness temperature
    
    Parameters
    ----------
      wavel: float
           wavelength (meters)
      I: float or array
           radiance (W/m^2/m/sr)
    
    Returns
    -------
    Tbright:  float or arr
           brightness temperature (K)
    """

```

```{code-cell} ipython3
### Question 2 answer
### your version of calc_Tbright here
###
```

## Question 3

Test your function by executing a round trip for some wavelength and temperature.  In the cell below, define a wavelength `wavelen` and a temperture `the_temp` and use them to calculate blackbody radiance `Iblack` with your function `calc_Blambda`.   Then calculate a brightness temperature `Tbright` using `calc_Tbright` and make sure it is equal to `the_temp` using the function [numpy.testing.assert_almost_equal](https://numpy.org/doc/2.1/reference/generated/numpy.testing.assert_almost_equal.html)

Something like:

`np.testing.assert_almost_equal(the_temp, Tbright)`

```{code-cell} ipython3
### Question 3 answer
#
# your question 3 solution here
#
```
