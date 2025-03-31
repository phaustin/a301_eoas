---
jupytext:
  cell_metadata_filter: -all
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
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

(week11:stull_radar_solution)=
# Assign7 Radar Problems -- solution

Reference:
 [Stull Chapter 8](https://www.eoas.ubc.ca/books/Practical_Meteorology/prmet102/Ch08-satellite_radar-v102b.pdf)

 
Answer the following questions in a Jupyter notebook, using a function to define the radar equation.

1. Suppose a Nexrad radar (Stull p.~246)  is
   receiving a signal with returned power Pr = -58 dBm.  Using the radar
   equation find the precipitation rate under the assumption that
   there is no attenuation and that it is a rainstorm (i.e. liquid water)
   100 km away from the radar.

2. Now keep everything the same, but make the mistake of guessing that it's a snowstorm,
   which means that K2=0.208 and we use the snowfall Z-RR relation
   of $Z=2000*RR^2$.  What is the new incorrect  precip rate?
   
3. Now assume it's rain, but make the mistake of guessing that there's a factor of La=2
   attenuation between the target and the rainstorm.  What is the new precip rate?

Nexrad coefficients:

```
    #coefficents for nexrad
    R1=2.17e-10#range factor, km, Stull 8.25
    Pt=750.e3 #transmitted power, W, stull p. 246
    b=14255 #equipment factor, Stull 8.26
```

```{code-cell} ipython3
import numpy as np
from numpy import log10
from numpy.testing import assert_almost_equal
```

## Question 1


Q1: Suppose a Nexrad radar (Stull p.~246)  is
receiving a signal with returned power Pr = -58 dBm.  Using the radar
equation find the precipitation rate under the assumption that
there is no attenuation and that it is a rainstorm (i.e. liquid water)
100 km away from the radar.

+++

### Question 1 answer


#### Radar functions

Here is the radar equation: Stull 8.28

```{code-cell} ipython3
def finddbz(Pr,K2,La,R,R1=None,Pt=None,b=None):
   """calculate dbZ using Stull 8.28
      with Pr the returned power in Watts
   """
   dbZ=10.*log10(Pr/Pt) + 20.*log10(R/R1) - \
       10.*log10(K2/La**2.) - 10.*log10(b)
   return dbZ
```

and here is the rain rate equation: Stull 8.29

```{code-cell} ipython3
def findRR_rain(dbZ):
   """
    find the rain rate in mm/hr using Stull 8.29
    dbZ:  reflectivity in dbZ referenced to 1 mm^6/m^3
   """
   #given that for rain Z=300*RR**1.4
   #a1_rain=(1/300.)**(1/1.4) = 0.017
   #a2_rain=1/1.4  = 0.714
   Z=10**(dbZ/10.)
   a1_rain=0.017  
   a2_rain=0.714  
   RR=a1_rain*Z**a2_rain
   return RR
```

and here are the Nexrad radar constants from Stull p. 246, converted into a dictionary called nexrad

```{code-cell} ipython3
# stull p. 246 sample appliation
# given

#coefficents for nexrad
R1=2.17e-10#range factor, km, Stull 8.25
Pt=750.e3 #transmitted power, W, stull p. 246
b=14255 #equipment factor, Stull 8.26

nexrad=dict(R1=R1,Pt=Pt,b=b)
```

#### Set coefficients for problem 1

We're assuming -58 dBm so need to convert that to watts.  Range is 100 km, no attenuation.

```{code-cell} ipython3
K2=0.93  #stull p. 245
Pr=10**(-5.8)*1.e-3  #dBm=-58, convert from mWatts to Watts
La=1  # no attenuation
R=100.  #km
```

#### Question 1 dbZ

```{code-cell} ipython3
dbZ=finddbz(Pr,K2,La,R,**nexrad)
print(f"calculated dbZ is {dbZ=:6.1f} referenced to 1 mm^6/m^3")
```

#### Question 1 rain rate

```{code-cell} ipython3
RR=findRR_rain(dbZ)
print(f"calculate rain rate is {RR=:6.1f} mm/hour")
```

## Question 2

 Now keep everything the same, but make the mistake of guessing that it's a snowstorm,
   which means that K2=0.208 and we use the snowfall Z-RR relation
   of $Z=2000*RR^2$.  What is the new incorrect  precip rate?

+++

### Question 2 answer

+++

#### Radar functions

```{code-cell} ipython3
def findRR_snow(dbZ):
   """
    find the rain rate in mm/hr Environment Canada's relation for snow
    dbZ:  reflectivity in dbZ referenced to 1 mm^6/m^3
   """
   #given that for snow Z=2000*RR**2. 
   a1_snow=0.02236   #(1/2000.)**(1./2.)
   a2_snow=0.5   #RR=(1/2000)**(1./2.)*Z**(1/2.)
   Z=10**(dbZ/10.)
   RR=a1_snow*Z**a2_snow
   return RR
```

#### Assume K2 for snow

```{code-cell} ipython3
K2=0.208 #p. 245
dbZ=finddbz(Pr,K2,La,R,**nexrad)
RR=findRR_snow(dbZ)
```

#### Q2 dbZ assuming snow

```{code-cell} ipython3
print(f"calculated dbZ is {dbZ=:6.1f} referenced to 1 mm^6/m^3")
```

#### Q2 RR assuming snow

```{code-cell} ipython3
print(f"calculate rain rate is {RR=:6.1f} mm/hour")
```

## Question 3

Now assume it’s rain, but make the mistake of guessing that there’s a factor of La=2 attenuation between the target and the rainstorm. What is the new precip rate?

+++

### Question 3 answer

+++

#### Assume K2 for liquid, la=2

```{code-cell} ipython3
K2=0.93 #p. 245
La=2.
dbZ=finddbz(Pr,K2,La,R,**nexrad)
RR=findRR_rain(dbZ)
```

#### dbZ assuming attenuation

```{code-cell} ipython3
print(f"calculated dbZ is {dbZ=:6.1f} referenced to 1 mm^6/m^3")
```

#### Rain rate assuming attenuation

```{code-cell} ipython3
print(f"calculate rain rate is {RR=:6.1f} mm/hour")
```
