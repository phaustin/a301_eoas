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

# GOES stability indices

+++

Another GOES level 2 product is ""ABI-L2-DSI", which stands for "Advanced Baseline Imager, Level 2, Derived Stability Indices"

+++

## Some review

Stability indices are a shorthand proxy for CAPE, the convective available potential energy that lifts surface air upward into the atmosphere.

- A list of indices: [from NOAA](https://www.weather.gov/lmk/indices).  

- Remember how cape is calculated, for example, here's an [ATSC 405 notebook](https://phaustin.github.io/a405_2024/notebooks/worksheets/cape_part1.html)

- How do you do this with the GOES channels?  Recall our {ref}`week6:weighting_funs` notebook and Stull Section 8.2.4.  The GOES-R satellite series has 7 channels with different weight functions you can look at
[at this link](https://cimss.ssec.wisc.edu/goes-wf/plot-viewer/#/plot-viewer/plot/model/abi18/default/20250323_1200Z/50,240).  For each pixel, the GOES postprocessing software fits temperature and vapor soundings to best reproduce those 7 radiance measurements, much like Roland does in that section.  This produces temperature and vapor values at 105 separate pressure levels, which are used to calculate the CAPE and the indices below.


+++

https://cimss.ssec.wisc.edu/goes-wf/plot-viewer/#/plot-viewer/plot/model/abi18/default/20250323_1200Z/50,240

+++

## Simple RGB Figure
At the most simple level, here is how to produce an RGB from the GOES ABI data.

```{code-cell} ipython3
from goes2go.data import goes_nearesttime
import matplotlib.pyplot as plt 
from datetime import datetime
from pathlib import Path
import xarray
```

```{code-cell} ipython3
# Get an ABI Dataset
save_dir = Path.home() / "repos/a301/satdata/goes" 
writeit = False
if writeit:
    g = goes_nearesttime(
        datetime(2020, 6, 25, 18), satellite="goes16",product="ABI-L2-DSI", domain='C', 
          return_as="xarray", save_dir = save_dir, download = True, overwrite = False
    )
    the_path = g.path[0]
else:
    the_path = ("noaa-goes16/ABI-L2-DSIC/2020/177/18/"
                "OR_ABI-L2-DSIC-M6_G16_s20201771801172_e20201771803545_c20201771805311.nc")
    full_path = save_dir / the_path
    g = xarray.open_dataset(full_path,mode = 'r',mask_and_scale = True)
```

## CAPE

```{code-cell} ipython3
g['CAPE'].plot.imshow();
```

## Lifted Index

```{code-cell} ipython3
g['LI'].plot.imshow();
```

## Total totals

```{code-cell} ipython3
g['TT'].plot.imshow();
```

## Showalter Index

```{code-cell} ipython3
g['SI'].plot.imshow();
```

## K-Index

```{code-cell} ipython3
g['KI'].plot.imshow()
```

```{code-cell} ipython3

```
