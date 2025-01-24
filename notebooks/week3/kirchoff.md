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

(week3:kirchoff)=
# Kirchoff worksheet

## Introduction

In section 4.3.4 on p. 120 Wallace and Hobbs present the following definitions:

$$
\varepsilon_\lambda&=\frac{I_\lambda(\text { emitted })}{B_\lambda(T)} \\
\alpha_\lambda&=\frac{I_\lambda(\text { absorbed })}{I_\lambda(\text { incident })} \\
R_\lambda&=\frac{I_\lambda(\text { reflected })}{I_\lambda(\text { incident })} \\
T_\lambda&=\frac{I_\lambda(\text { transmitted })}{I_\lambda(\text { incident })} \\
$$

The absorptivity, reflectivity and transmissivity are related via conservation of energy.  Every photon that arrives in a layer of gas, solid or liquid has to be either absorb, reflected, or transmitted, so:

$$
\alpha_\lambda + R_\lambda + T_\lambda = 1
$$

## Monochromatic emissivity $\epsilon_\lambda$

Kirchoff's law says that  “good absorbers are good emitters” or more exactly:

$$
\alpha_\lambda = \epsilon_\lambda 
$$
for any gas, liquid or solid in thermodynamic equilibrium.

To see why this has to be true, consider {numref}`kirchoff`, where a blackbody (surface A) is facing a surface B at the same temperature, with absorptivity and emissivity that violate Kirchoff’s law (there is a vacuum between the two plates). 

:::{figure} ./images/kirchoff.png
:name: kirchoff
:scale: 100

Demonstration of Kirchoff’s law
:::


## Worksheet question


Suppose the reflectivity on for wall A is $\alpha_l =0.7$, so  $\alpha_l \neq \epsilon_l$ and Kirchoff's law is violated.  Find the net flux at wall A if this is true.   Why is this physically impossiblea?  Note that $\sigma 280^4$ is a flux, not a radiance, but that doesn't matter for this proof  (why not)?


