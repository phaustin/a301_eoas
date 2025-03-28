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

# earth care cpr

## imports

```{code-cell} ipython3
import h5py
from pyhdf.SD import SD
from pyhdf.SD import SDC
import numpy as np
import matplotlib.pyplot as plt
import pytz
```

```{code-cell} ipython3
# from sat_lib.cloudsat import read_cloudsat_var
```

```{code-cell} ipython3
import netCDF4
import xarray as xr
from pathlib import Path
```

```{code-cell} ipython3
from satpy import Scene
```

### file i/o

```{code-cell} ipython3
import os
from glob import glob

# os.getcwd(), os.listdir()
```

```{code-cell} ipython3
def apply_metadata_names(metadata,
                         measurements):

    measurements_dims = measurements.rename(dims_mapping)

    return measurements_dims
```

```{code-cell} ipython3
data_dir = Path().home() / 'repos/a301/satdata/earthcare'
radar_filepaths = list(data_dir.glob("**/*.h5"))
good_paths=dict()
for filepath in radar_filepaths:
    relpath = filepath.relative_to(data_dir)
    casename = relpath.parts[0]
    good_paths[casename]=filepath
```

radar_filepaths = Path().glob("**/*h5")
radar_filepaths = list(radar_filepaths)
good_paths = [filename for filename in radar_filepaths
              if (filename.parts[0] == 'data' and str(filename).find('CPR') > 0)]
keys = [filename.parts[1] for filename in good_paths]
good_paths = dict(zip(keys,good_paths))
good_paths.keys()

```{code-cell} ipython3
def sort_keys(the_case):
    number = the_case[4:]
    return int(number)
sorted_keys = list(good_paths.keys())
sorted_keys.sort(key=sort_keys)
sorted_keys
```

```{code-cell} ipython3
cpr_data = xr.open_dataset(good_paths['case4'], engine='h5netcdf', group='/ScienceData/Data', phony_dims='access')
cpr_meta = xr.open_dataset(good_paths['case4'], engine='h5netcdf', group='/ScienceData/Geo', phony_dims='access')
# cpr_meta.binHeight[0, :10].max() - cpr_meta.binHeight[0, :10].min()
```

## Get binheights

```{code-cell} ipython3
def get_binheight(cpr_meta):
    the_bins = cpr_meta.binHeight[...]

the_bins = cpr_meta.binHeight[...]
the_bins = the_bins[0,:].data
diff_bins = np.diff(the_bins)
del_y = np.nanmean(diff_bins)
new_y = [the_bins[0]]
for count,old_y in enumerate(the_bins[1:]):
    if np.isnan(old_y):
        new_y.append(float(new_y[count]) + float(del_y))
    else:
        new_y.append(float(old_y))
new_y = new_y[::-1]
print(len(the_bins),len(new_y))
print(new_y)   
```

## Check times

```{code-cell} ipython3
import datetime
from timezonefinder import TimezoneFinder
tf = TimezoneFinder()

def get_first_last(filepath):
    meta_file = xr.open_dataset(filepath, engine='h5netcdf', group='/ScienceData/Geo', phony_dims='access')
    lon = meta_file['longitude'][0].to_dict()['data']
    lat = meta_file['latitude'][0].to_dict()['data']
    first_time = meta_file['profileTime'][0].to_dict()['data']
    first_time = first_time.replace(tzinfo = pytz.utc)
    timezone_str =  tf.timezone_at(lng=lon, lat=lat)
    timezone = pytz.timezone(timezone_str)
    first_time = first_time.replace(tzinfo = timezone)
    timestr = first_time.strftime("local time: %Y/%b/%d %H:%M")
    latlon = f"{lat:.0f},{lon:.0f}"
    return timestr, latlon, timezone_str
```

```{code-cell} ipython3
for the_key in sorted_keys:
    test = get_first_last(good_paths[the_key])
    print(test)
```

```{code-cell} ipython3
# times = cpr_meta['profileTime']
# bins = cpr_meta['binHeight']
# #fig, ax = plt.subplots(1,1)
# # plt.imshow(cpr_meta['binHeight'].data)
# rows, cols = bins.shape
# for row in range(10):
#     print("++++++++++")
#     print(bins[row,:].data)
```

```{code-cell} ipython3
import copy
from matplotlib import cm
from matplotlib.colors import Normalize

for the_case in sorted_keys:
    filepath = good_paths[the_case]
    with xr.open_dataset(filepath, engine='h5netcdf', group='/ScienceData/Data', phony_dims='access') as cpr_data:
        # cpr_meta = xr.open_dataset(radar_filepaths[ii], engine='h5netcdf', group='/ScienceData/Geo', phony_dims='access')
        # cpr_data['phony_dim_0'] = cpr_meta['profileTime']
        # cpr_data['phony_dim_1'] = cpr_meta['binHeight'][-1, :]

        # cpr_data = cpr_data.rename({'phony_dim_0': 'profileTime'})  # , 'phony_dim_1': 'binHeight'})
        
        fig, ax = plt.subplots(2, 1, figsize=(12, 5))
        vmin=-5
        vmax=5
        the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
        cmap_ref=copy.copy(cm.coolwarm)
        cmap_ref.set_over('w')
        cmap_ref.set_under('0.5')
        cmap_ref.set_bad('0.75') #75% grey
        cpr_data['dopplerVelocity'].T.plot.pcolormesh(ax=ax[0], yincrease=False, norm=the_norm, cmap=cmap_ref);
        ax[0].set_title(the_case)
        vmin=-25
        vmax=20
        the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
        cmap_ref=copy.copy(cm.viridis)
        cmap_ref.set_over('w')
        cmap_ref.set_under('0.5')
        cmap_ref.set_bad('0.75') #75% grey
        
        # fig, ax = plt.subplots(1, 1, figsize=(12, 5))
        dbZ = 10*np.log10(cpr_data['radarReflectivityFactor'])
        # dbZ = cpr_data['radarReflectivityFactor']
        
        dbZ.T.plot.pcolormesh(ax=ax[1], yincrease=False, norm=the_norm, cmap=cmap_ref);
```

### quick-look h5py
- identify groupnames for xarray

```{code-cell} ipython3
# loading and visualizing radar with hdf5

with h5py.File(good_paths[the_case], 'r') as hdf5:
    print(hdf5.keys())
    header_key = list(hdf5.keys())[0]
    science_key = list(hdf5.keys())[1]  # holds the measurements
    print(science_key)
    print(header_key)

    # query nested groups
    data = list(hdf5[science_key])  # list the measurement names
    print(type(data), data)

    cpr_data = hdf5['/ScienceData/Data']
    cpr_meta = hdf5['/ScienceData/Data'].keys()
    print(cpr_meta)
    # cpr_header = hdf5['/HeaderData/VariableProductHeader']
    print(cpr_data)

    # print(list(cpr_header.keys()))
    epsilon = 1e-1

    doppler_velocity = hdf5['/ScienceData/Data/dopplerVelocity']
    rr_factor = hdf5['/ScienceData/Data/radarReflectivityFactor']

    
    # print(dset[:, 0])

    # time = hdf5['ScienceData/time'][:]
    # altitude = hdf5['ScienceData/height'][:]
    # time, altitude

    # fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 6))
    # ax1.pcolormesh(np.log10(np.abs(doppler_velocity)), shading='auto', cmap='viridis')
    # # ax1.yaxis.set_inverted(True)
    # ax2.pcolormesh(np.log10(np.abs(rr_factor)), shading='auto', cmap='viridis')
    # ax2.yaxis.set_inverted(True)
    # ax3.pcolormesh(np.log10(np.abs(crosspolar_backscatter[:, :].T)), shading='auto', cmap='viridis')
    # ax3.yaxis.set_inverted(True)
```

### loading and visualizing lidar

```{code-cell} ipython3

```

```{code-cell} ipython3
first_pixel = 2000
second_pixel = 200

with h5py.File(atl_file[0], 'r') as hdf5:
    print(hdf5.keys())
    header_key = list(hdf5.keys())[0]
    science_key = list(hdf5.keys())[1]  # holds the measurements
    print(science_key)
    
    # Getting the data
    data = list(hdf5[science_key])  # list the measurement names
    # print(data)

    mie_backscatter = hdf5['ScienceData/mie_attenuated_backscatter']  # add the desired name to group to access array
    rayleigh_backscatter = hdf5['ScienceData/rayleigh_attenuated_backscatter']
    crosspolar_backscatter = hdf5['ScienceData/crosspolar_attenuated_backscatter']
    layer_temperature = hdf5['ScienceData/layer_temperature']
    print(mie_backscatter.shape)

    epsilon = 1e-1

    # print(dset[:, 0])

    time = hdf5['ScienceData/time'][:]
    altitude = hdf5['ScienceData/height'][:]
    time, altitude

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 6))
    ax1.pcolormesh(np.log10(np.abs(mie_backscatter[:, :].T)), shading='auto', cmap='viridis')
    ax1.yaxis.set_inverted(True)
    ax2.pcolormesh(np.log10(np.abs(rayleigh_backscatter[:, :].T)), shading='auto', cmap='viridis')
    ax2.yaxis.set_inverted(True)
    ax3.pcolormesh(np.log10(np.abs(crosspolar_backscatter[:, :].T)), shading='auto', cmap='viridis')
    ax3.yaxis.set_inverted(True)
    ax4.pcolormesh(layer_temperature[:, :].T, shading='auto', cmap='viridis')
    ax4.yaxis.set_inverted(True)

    plt.show()
```
