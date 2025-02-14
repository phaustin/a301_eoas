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

(assign4-2laysol)=
# Assignment 4 two layer solution

## Q4

For the following set of layers:

:::{figure} figures/two_layer.png
:name: twolayer
:scale: 50

Two grey layers over a black surface
:::


1) Write down a system of three equations in three unknowns for the equilibrium case where the fluxes at each level are in balance.
2) Write a python function that returns the three layer temperatures  $T_g,\ T_1,\ T_2$ given $\epsilon_1$, $\epsilon_2$ and $I_0$.  Hand in notebook that uses that function to solve for $\epsilon_1=0.8$, $\epsilon_2 = 0.4$ and $I_0 = 240\ W\,m^{-2}$ 
3) Possible helpful `numpy.linalg.solve` video from [Kindson the Genius](https://www.youtube.com/watch?v=lMI63LrKNnA)

+++

## Solution

The three equations:

Here is the energy budget (heating rate) for each layer where F means flux (positive downward

- layer 2 budget
   - heating2 = abs2\*Tr1\*Fg + abs2\*F1 - 2\*F2
- layer 1 budget
   - heating1 = abs1\*Fg - 2\*F1 + abs1*F2
- Ground budget
   - heatingg = Sol - Fg + F1 + Tr1*F2

or you could write the flux for each level (downward positive)

- level 2 flux
  - F2 = Sol - Tr2\*Tr1\*Fg - Tr2\*F1
  - F1 = Sol - Tr1\*Fg + F2
  - Fg = Sol + Tr1\*F2 + F1
    
  
Convince yourself that these two systems are identical -- i.e. that the heating rate for layer 2 is given by subtracting the flux through level 1 from the flux through level 2

```python
do_two_matrix(Sol=341.,albedo=0.3,epsilon1=0.55,epsilon2=0.55)         
          -- this solves the two layer model numerically
```

```{code-cell} ipython3
import numpy as np
from scipy import linalg


sigma=5.67e-8  #W/m^2/K^4

def do_two_matrix(Sol=240,albedo=0.0,epsilon1=0.8,epsilon2=0.4):
    """
       do_two_matrix(Sol=341.,albedo=0.3,epsilon1=0.55,epsilon2=0.55)
       returns [Fg,F1,F2]   -- layer fluxes in W/m^2
    """   
    Sol=Sol*(1-albedo)
    abs1=epsilon1
    abs2=epsilon2
    Tr1=1. - abs1
    Tr2=1. - abs2
    #layer 2 budget
    #dF2/dt = abs2*Tr1*Fg + abs2*F1 - 2*F2
    #layer 1 budget
    #dF1/dt = abs1*Fg - 2*F1 + abs1*F2
    #Ground budget
    #dFg/dt = Sol - Fg + F1 + Tr1*F2
    the_array=[[abs2*Tr1, abs2, -2.], \
               [abs1, -2., abs1],\
               [-1., 1., Tr1]]
    the_array=np.array(the_array)
    rhs=[0,0,-Sol]
    the_inv=linalg.inv(the_array)
    fluxes=np.dot(the_inv,rhs)
    return fluxes

def find_temps(fluxes,epsilon1=0.8,epsilon2=0.4):
    """
       find_temps(fluxes,epsilon1=0.55,epsilon2=0.55)
       fluxes=(Fg,F1,F2)
       returns (Tg,T1,T2)
    """
    Tg=(fluxes[0]/sigma)**0.25
    T1=(fluxes[1]/(sigma*epsilon1))**0.25
    T2=(fluxes[2]/(sigma*epsilon2))**0.25
    return (Tg,T1,T2)   
```

```{code-cell} ipython3
numeric_fluxes=do_two_matrix()
print(f"numeric temperatues: {find_temps(numeric_fluxes)}")
```

```{code-cell} ipython3

```

```{code-cell} ipython3

```
