---
jupytext:
  cell_metadata_filter: -all
  notebook_metadata_filter: -all
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(midterm-topics)=
# Study topics for midterm

## Not on test

- No questions about python, programming, gis, coordinate transforms etc.

## Topic focus for the test

1. Calculating radiances and fluxes from atmospheric conditions:

   1. Find optical depth and transmisson profiles given a hydrostatic atmosphere with
      a specified scale height
   2. Calculate broadband ($\sigma\,T^4 / \pi$) and monochromatic radiances and fluxes
   3. Calculate the flux observed by a satellite through an atmosphere of known properties
   4. Convert between radiance and brightness temperature
   5. Calculate heating/cooling rates for a layer
   6. Calculate field of view in steradians and find the flux through a field of view
      given an isotropic source of radiation 

2. Calcuate atmospheric/solar properties from radiation measurements

   1. Use Beer's law to estimate the solar flux as a function of optical depth

3. Derivations/equations

   1. Integrate the hydrostatic equation to find the pressure or mass of a column
      as a function of height
   2. Integrate the radiance over a hemisphere to find the flux leaving a surface
   3. Integrate the Schwartzchild equation with a constant temperature profile to find the
      radiance or the flux for a  layer
   4. Show that the radiance is independent of distance, while the flux obeys an inverse
      square law
   5. Derive the heating rate equation
   6. Use change of variables to solve an integral
   7. Use a Taylor series to approximate a change in a quantity to first order



