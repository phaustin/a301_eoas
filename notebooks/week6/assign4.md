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

"""
   layers.py provides two functions:
      do_two(Sol=341.,epsilon=0.55,albedo=0.3)
         -- this solves the two layer model analytically

      do_two_matrix(Sol=341.,albedo=0.3,epsilon1=0.55,epsilon2=0.55)         
          -- this solves the two layer model numerically
"""
      
import numpy as np
from scipy import linalg

#show the difference between importing and running this
#module by printing the module namespace
#
sigma=5.67e-8  #W/m^2/K^4

def do_two(Sol=341.,epsilon=0.55,albedo=0.3):
    """
       do_two(Sol=341.,epsilon=0.55,albedo=0.3)
       returns [Fg,F1,F2]   -- layer fluxes in W/m^2
    """
    Sol=341.
    epsilon=0.55
    Fg=(1-albedo)*Sol/(1-epsilon/2*(1+epsilon*(1-epsilon)/2)/ \
                         (1-epsilon*epsilon/4)-(1-epsilon)*epsilon/2*((1-epsilon)+ \
                        epsilon/2)/(1-epsilon*epsilon/4))
    F2=Fg*epsilon/2*((1-epsilon)+epsilon/2)/(1-epsilon*epsilon/4)
    F1=Fg*epsilon/2*(1+epsilon*(1-epsilon)/2)/(1-epsilon*epsilon/4)
    #check balances
    TOA= Sol*(1 - albedo) - F2  - (1-epsilon)*F1 - (1-epsilon)**2.*Fg
    Lay1=Sol*(1 - albedo) + F2 - F1 - (1 - epsilon)*Fg
    Ground=Sol*(1 - albedo) + F1 + (1-epsilon)*F2 - Fg
    return (Fg,F1,F2)

def do_two_matrix(Sol=341.,albedo=0.3,epsilon1=0.55,epsilon2=0.55):
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

def find_temps(fluxes,epsilon1=0.55,epsilon2=0.55):
    """
       find_temps(fluxes,epsilon1=0.55,epsilon2=0.55)
       fluxes=(Fg,F1,F2)
       returns (Tg,T1,T2)
    """
    Tg=(fluxes[0]/sigma)**0.25
    T1=(fluxes[1]/(sigma*epsilon1))**0.25
    T2=(fluxes[2]/(sigma*epsilon2))**0.25
    return (Tg,T1,T2)   

# the following boiler plate runs test code when
# layers.py is executed from the command line and it's namespace
# is "__main__", but not when it is imported
# by other code and it's namespace is "layers"

if __name__=="__main__":
    analytic_fluxes=do_two()
    numeric_fluxes=do_two_matrix()
    print(f"analytic temperatures: {find_temps(analytic_fluxes)}")
    print(f"numeric temperatues: find_temps(numeric_fluxes)}")

