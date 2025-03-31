

(final-guide)=
# Study guide for final exam


1. Calculating radiative fluxes from atmospheric conditions:

   1. Find optical depth and transmisson profiles given a hydrostatic atmosphere with
      a specified scale height
   2. Calculate the equilibrium temperature profile of a multilayer atmosphere with known
      transmission
   3. Calculate the flux observed by a satellite through an atmosphere of know properties
   4. Convert between radiance and brightness temperature
   5. Calculate heating/cooling rates given atmospheric fluxes

2. Calcuate atmospheric/solar properties from radiation measurements

   1. Use Beer's law to estimate the solar flux as a function of optical depth
   2. Use high resolution spectral measurements to estimate temperatures in the stratosphere and
      at the surface
   3. Use weighting functions and measurements at multiple wavelengths to infer temperature at
      different heights
   4. Calculate flux/radiance/brightness temperature in specific wavelength ranges  given optical depths and atmosphere and surface temperatures

3. Radar:

   1. Find possible radial velocities given doppler I and Q values
   2. Find pulse pair phase shifts given I and Q values
   3. Find the wind direction as a function of height from a radar display of radial wind speeds
   4. Calculate maximum unambiguous velocities and ranges given the PRF and radar wavelength
   5. Find the rain rate from a Z-R relationship
   6. Find Z from a cloud droplet size distribution

4. Derivations/equations

   1. Integrate the hydrostatic equation to find the pressure as a function of height
   2. Integrate the Schwartzchild equation with a constant temperature profile to find the
      radiance or the flux for a layer
   3. Integrate the Schwartzchild equation with a varying temprature profile
   4. Derive the MUR and Mrmax equations
   5. Derive the heating rate equation
   6. Use change of variables to solve an integral
   7. Use differentials to estimate small changes to a function

5. Python programming

   - Be able to explain and use all the functions in [a301_extras](https://phaustin.github.io/a301_extras/full_listing.html)
   - be able to explain the work flow in a program that crops an image or compares
     to images of different resolutions/CRSs as in Assignment 8

7. Essay/short answer

   - Vocabulary/definitions from Understanding Map Projections/programs -- datum, CRS, geoid, affine transform
   - What is the bright band? Why is it bright?
   - What is aliasing, how does it limit radar observations of reflectivity and velocity?
   - Choose 2 band combinations from GOES or Landsat false color images and discuss what wavelengths are used and what they reveal about the land surface or the airmass in a particular pixel -- i.e. how are the different for built/vegetated environments or warm/moist/cold/dry air etc.
   
