---
jupytext:
  formats: ipynb,md:myst
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

```{code-cell} ipython3
import matplotlib.pyplot as plt
from numpy import pi
import numpy as np
```

```{code-cell} ipython3
fig1, axis1 =plt.subplots(1,1, subplot_kw=dict(polar=True))
theta=np.array([0.,0.])*pi/180.;
rho=np.array([0.,1.]);
line1=axis1.plot(theta,rho,'b-',linewidth=3);
point1=axis1.plot(0,1,'bo');
```

```{code-cell} ipython3
theta=np.array([30.,30.])*pi/180.;
rho=np.array([0,1]);
line1=axis1.plot(theta,rho,'c-',lw=4);
point1=axis1.plot(theta[0],1,'co')
display(fig1)
```

```{code-cell} ipython3
theta=np.array([60.,60.])*pi/180.;
rho=np.array([0,1]);
line1=axis1.plot(theta,rho,'g-',lw=4);
point1=axis1.plot(theta[0],1,'go')
display(fig1)
```

```{code-cell} ipython3
theta=np.array([90.,90.])*pi/180.;
rho=np.array([0,1]);
line1=axis1.plot(theta,rho,'k-',lw=4);
point1=axis1.plot(theta[0],1,'ko');
axis1.set_title('phase shifts of 0, 30, 60, 90 degrees')
display(fig1)
```

```{code-cell} ipython3

```
