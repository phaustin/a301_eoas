---
jupyter:
  jupytext:
    formats: md,ipynb
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.6
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

(sec:planck_sol)=
# Plotting the Planck function - solution

- Download planck_sol.ipynb from the [week2 folder](https://drive.google.com/drive/folders/1-Ja2wVKVIjkZb7Gx_rfc14J_aBYiknuw?usp=sharing)


```python
import numpy as np
from matplotlib import pyplot as plt
```

## Write a function to compute Stull 2.13

```python
import numpy as np
#
# get Stull's c_1 and c_2 from fundamental constants
#
# c=2.99792458e+08  #m/s -- speed of light in vacuum
# h=6.62606876e-34  #J s  -- Planck's constant
# k=1.3806503e-23  # J/K  -- Boltzman's constant

def Flambda(wavel, Temp):
    """
    Calculate the blackbody radiant exitence (Stull 2.13)

    Parameters
    ----------

      wavel: float or array
           wavelength (meters)

      Temp: float
           temperature (K)

    Returns
    -------

    Flambda:  float or arr
           monochromatic radiant exitence (W/m^2/m)
    """
    c, h, k = 299_792_458.0, 6.626_070_04e-34, 1.380_648_52e-23
    c1 = 2.0 * h * c ** 2.0
    c2 = h * c / k
    Flambda_val = c1 * np.pi / (wavel ** 5.0 * (np.exp(c2 / (wavel * Temp)) - 1))
    return Flambda_val
```

## run the function for a single temperature

```python
npoints = 10000
Temp = 255  # K
wavelengths = np.linspace(0.1, 500.0, npoints) * 1.0e-6  # meters
Fstar = Flambda(wavelengths, Temp)
fig, ax = plt.subplots(1, 1, figsize=(7, 7))
#
#  change wavelength to microns and flux to W/m^2/micron
#
ax.plot(wavelengths * 1.0e6, Fstar * 1.0e-6)
ax.set(xlim=[0, 50])
ax.grid(True)
ax.set(
    xlabel="wavelength (m)",
    ylabel=r"$F_\lambda^*\ (W\,m^{-2}\,\mu m^{-1}$)",
    title=f"Monochromatic blackbody flux at Temp={Temp} K",
);
```

## Convert flux to radiance

This uses the reading {ref}`sec:week1-flux-from-radiance`

```python
# convert isotropic flux to radiance
Blambda = Fstar / np.pi
fig, ax = plt.subplots(1, 1, figsize=(8, 8))
#convert wavelength from meters to microns
ax.plot(wavelengths * 1.0e6, Blambda * 1.0e-6)
ax.set(xlim=[0, 50])
ax.grid(True)
ax.set(
    xlabel="wavelength ($\mu m$)",
    ylabel="$B_\lambda\ (W\,m^{-2}\,sr^{-1}\,\mu m^{-1}$)",
    title=f"Monochromatic blackbody radiance at Temp={Temp} K",
);
```

## Reproduce W&H figure 4.6

In the cell below add lines and change the axis limits to reproduce the high temperature emission spectrum in the W&H figure

```python
temps =[5000, 6000, 7000] #K
# convert isotropic flux to radiance
npoints=1000
wavelengths = np.linspace(0.01,2,npoints)*1.e-6  #meters
fig, ax = plt.subplots(1, 1, figsize=(8, 8))
for the_temp in temps:
    Fstar = Flambda(wavelengths, the_temp)
    Blambda = Fstar / np.pi
    #convert wavelength from meters to microns
    #convert radiance to megawatts per meter^2 per micron bin width per sr
    ax.plot(wavelengths * 1.0e6, Blambda*1.e-12,label=f"{the_temp} K")
    ax.set(xlim=[0., 2])
ax.grid(True)
ax.legend()
ax.set(
    xlabel="wavelength ($\mu m$)",
    ylabel="$B_\lambda\ (MW\,m^{-2}\,sr^{-1}\,\mu m^{-1}$)",
    title=f"Monochromatic blackbody radiance vs temperature"
);
```

```python

```
