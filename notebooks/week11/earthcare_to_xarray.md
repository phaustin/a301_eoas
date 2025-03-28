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

(week11:earthcare_xarray)=
# Convert earthcare to xarray

This notebook does a quick inspection of one of the earthcare cases, with
plots of the radar reflectivity and doppler velocity.  The earthcare data
is stored in [hdf5](https://docs.h5py.org/en/stable/) format, which is also
the underlying data format for netcdf.  Unlike netcdf, the files don't supply
dimensions or coordinates, so we have to figure out those ourselves.

+++

## Installation

- Download a case folder from the satdata/earthcare folder on our
[gdrive folder](https://drive.google.com/drive/folders/1-D6y9MlE8LZRLZg-qRCxPZSgar8kGjBT?usp=drive_link)

- fetch and rebase from upstream/main to get this notebook in week11

```{code-cell} ipython3
from pathlib import Path
import xarray as xr
import numpy as np
import pyproj
from matplotlib import pyplot as plt
import datetime
import pytz
import pyproj
```

## Find the case files

Organize them in a dictionary keyed by the case name, which
is at the start of the relative file path.  pathlib has a function that
finds the relative path, and also can break the folder path into 
its various parts

```{code-cell} ipython3
data_dir = Path().home() / 'repos/a301/satdata/earthcare'
radar_filepaths = list(data_dir.glob("**/*.h5"))
filepaths=dict()
for filepath in radar_filepaths:
    relpath = filepath.relative_to(data_dir)
    casename = relpath.parts[0]
    filepaths[casename]=filepath
relpath
```

```{code-cell} ipython3
def sort_keys(the_case):
    number = the_case[4:]
    return int(number)
```

```{code-cell} ipython3
sorted_keys = list(filepaths.keys())
sorted_keys.sort(key=sort_keys)
casenum = 'case4'
#sorted_keys
```

## Read the data and metadata

These are netcdf files, so no dimensions or coordinates, we'll need to
create these.  Start by naming the time and height dimensions

```{code-cell} ipython3
def get_binheight(the_bins, index=0):
    """
    the radar bin heights are stored for every radar pulse.  If the terrain is
    roughly level, these should be the same pulse to pulse, so just use the
    first one

    Some radar height bins are missing, so fill those in by finding the average
    distance between bins and using that as an increment

    Questions -- what does [...] accomplish here? Why all the float() calls?
    """
    the_bins = the_bins[:,index].data
    diff_bins = np.diff(the_bins)
    del_y = float(np.nanmean(diff_bins))
    new_y = [float(the_bins[0])]
    for count,old_y in enumerate(the_bins[1:]):
        if np.isnan(old_y):
            new_y.append(float(new_y[count]) + float(del_y))
        else:
            new_y.append(float(old_y))
    return np.array(new_y)

def find_times(filepath):
    """
    times are stored as seconds after Jan 1, 2000
    use the datetime.timedelta function to increment from
    that start time

    Also set the timezone as utc
    """
    cpr_meta = xr.open_dataset(filepath, engine='h5netcdf', group='/ScienceData/Geo',
                           decode_times=False, phony_dims='access')
    times = cpr_meta['profileTime'].data
    start_time = datetime.datetime(2000,1,1,0,0,0)
    the_times =[start_time + datetime.timedelta(seconds=item) for item in times]
    the_times = [item.replace(tzinfo = pytz.utc) for item in the_times]
    return the_times

great_circle=pyproj.Geod(ellps='WGS84')
meters2km = 1.e-3
def calc_distance(lonvec,latvec):
    distance=[0]
    startlon,startlat = lonvec[0],latvec[0]
    for lon,lat in zip(lonvec[1:],latvec[1:]):
        azi12,azi21,step= great_circle.inv(startlon,startlat,lon,lat)
        distance.append(distance[-1] + step)
        startlon,startlat = lon, lat
    distance=np.array(distance)*meters2km
    return distance

def ec_to_xarray(ec_filepath):
    #
    # read the h5 files into xarray dataarrays
    # 
    cpr_data = xr.open_dataset(ec_filepath, engine='h5netcdf', group='/ScienceData/Data',
                                decode_times=False,  phony_dims='access')
    cpr_data = cpr_data.rename_dims({'phony_dim_0':'distance','phony_dim_1': 'height'})
    cpr_meta = xr.open_dataset(ec_filepath, engine='h5netcdf', group='/ScienceData/Geo',
                               decode_times=False, phony_dims='access')
    cpr_meta = cpr_meta.rename_dims({'phony_dim_0':'distance','phony_dim_1': 'height'})
    lonvec = cpr_meta['longitude']
    latvec = cpr_meta['latitude']
    distance = calc_distance(lonvec.data, latvec.data)
    the_times = find_times(ec_filepath)
    binHeights = cpr_meta.binHeight[...].T
    heights = get_binheight(binHeights,0)
    coords = dict(height=("height",heights),
              distance = ("distance",distance))
    velocity = cpr_data['dopplerVelocity'].T
    radar = cpr_data['radarReflectivityFactor'].T
    dbZ = 10*np.log10(radar)
    attrs=dict(history = f"written by ec_to_xarray on {str(datetime.datetime.now())}")
    var_dict = dict(dbZ = dbZ , velocity=velocity,binHeights=binHeights,
                   longitude=lonvec, latitude=latvec,time=the_times)
    ds_earthcare = xr.Dataset(data_vars=var_dict,
        coords=coords,attrs=attrs)
    print(f"{binHeights.dims=},{binHeights.shape=}")
    print(f"{velocity.dims=},{velocity.shape=}")
    print(f"{dbZ.dims=},{dbZ.shape=}")
    return ds_earthcare
    

    
    
```

```{code-cell} ipython3

```

### print the case times

```{code-cell} ipython3
for casename in sorted_keys:
    filepath = filepaths[casename]
    check_times = find_times(filepath)
    print(casename, check_times[0], check_times[-1])
```

## plot the radar reflectivity

```{code-cell} ipython3
filepaths[casenum]
radar_ds = ec_to_xarray(filepaths[casenum])
radar_ds
```

```{code-cell} ipython3

```

```{code-cell} ipython3
def set_new_height(ds,target_index):
    """
    replace the height coordinate with a new height
    """
    height_array = ds['binHeights']
    bin_height = get_binheight(height_array,target_index)
    print(bin_height[-1])
    ds = ds.assign_coords({'height': bin_height})
    return ds
    
```

```{code-cell} ipython3
radar_ds.coords['height'].data[-1]
```

```{code-cell} ipython3
new_index = np.argmin(np.abs(radar_ds.distance.data - 1000))
new_index
```

```{code-cell} ipython3
radar_ds = set_new_height(radar_ds,new_index)
radar_ds.coords['height'].data[-1]
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1,figsize=(12,3))
radar_ds['dbZ'].plot(ax = ax, x="distance",y="height",vmin=-3,vmax=25);
ax.set_xlim(1000,5000)
ax.set_xlabel("distance (km)")
ax.set_ylabel("height (m)")
ax.set_title(casenum);
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1,figsize=(12,3))
radar_ds['velocity'].plot(ax = ax, x="distance",y="height",vmin=-3,vmax=3);
ax.set_xlabel("distance (km)")
ax.set_ylabel("height (m)")
ax.set_xlim(1000,5000)
ax.set_title(casenum);
```

```{code-cell} ipython3
radar_ds.where(radar_ds.coords['distance'] > 1000.)
```

```{code-cell} ipython3
start_index = radar_ds = radar_ds.isel(radar_ds.distance > 1000, drop = True)
radar_ds.isel(distance=hit)
```

```{code-cell} ipython3

```
