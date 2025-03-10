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

(assign6)=
# Assignment 6

Upload a pdf and a notebook for the following problems:

## Q1 Planck wavenumber

Planck's law as a function of wavelength:

$$
B_\lambda(\lambda, T)=\frac{2 h c^2}{\lambda^5} \frac{1}{e^{h c /\left(\lambda k_{\mathrm{B}} T\right)}-1}
$$ (planck)


Use change of variables to rewrite {eq}`planck` in terms of wavenumber $\tilde{\nu} = 1/\lambda$ and show that it is:

$$
B_{\tilde{\nu}}(\tilde{\nu}, T)=2 h c^2 \tilde{\nu}^3 \frac{1}{e^{h c \tilde{\nu} /\left(k_{\mathrm{B}} T\right)}-1}
$$ (planck_wn)

## Q2 Stefan-Boltzman

Integrate {eq}`planck_wn` to find the Stefan-Boltzman equation given that 

$$
\int_0^\infty \frac{u^3}{(e^u -1 )} du = \frac{\pi^4}{15} 
$$ (planck_int)
([Riemann zeta function](https://en.wikipedia.org/wiki/Riemann_zeta_function))

i.e. show that:

$$
\int_0^\infty B_{\nu} d\nu = \frac{\sigma}{\pi} T^4
$$

where 

$$
\sigma=\frac{2 \pi^4 k^4}{15 c^2 h^3}
$$

## Q3 Wien's law

Show that the maximum value for {eq}`planck` occurs at:

$$
\lambda_{max} \propto \frac{1}{T}
$$
([Wien's law](https://en.wikipedia.org/wiki/Wien%27s_displacement_law))


## Q4  Radar Rainrate

Integrate $Z=\int D^6 n(D) dD$ on paper, assuming a Marshall Palmer size distribution and show that it integrates to:

$$
Z \approx 300 RR^{1.5}
$$

with Z in $mm^6\,m^{-3}$ and RR in mm/hr.  It's helpful to know that:

$$
\int^\infty_0 x^n \exp( -a x) dx = n! / a^{n+1}
$$

## Q5 Radar Rainrate Python

Repeat using numerical integration in python (i.e. np.diff and np.sum) and show that the  result agrees.

