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
import pyproj
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

```{code-cell} ipython3
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
```

```{code-cell} ipython3
import datetime
from timezonefinder import TimezoneFinder
tf = TimezoneFinder()

def get_var(filepath,varname,group='Data'):
    groupname = f"/ScienceData/{group}"
    ds = xr.open_dataset(filepath, 
                          engine='h5netcdf', group=groupname, phony_dims='access')
    vec_out = ds[varname].data
    return vec_out
    
def get_first_last(filepath):
    meta_file = xr.open_dataset(filepath, engine='h5netcdf', group='/ScienceData/Geo', phony_dims='access')
    lon = meta_file['longitude'].data
    midindex = int(len(lon)/2)
    start_lon = meta_file['longitude'][0].to_dict()['data']
    start_lat = meta_file['latitude'][0].to_dict()['data']
    stop_lon = meta_file['longitude'][-1].to_dict()['data']
    stop_lat = meta_file['latitude'][-1].to_dict()['data']
    mid_lon = meta_file['longitude'][midindex].to_dict()['data']
    mid_lat = meta_file['latitude'][midindex].to_dict()['data']
    first_time = meta_file['profileTime'][0].to_dict()['data']
    last_time = meta_file['profileTime'][-1].to_dict()['data']
    mid_time = last_time = meta_file['profileTime'][midindex].to_dict()['data']
    def format_time(the_time,lat,lon):
        the_time = the_time.replace(tzinfo = pytz.utc)
        timezone_str =  tf.timezone_at(lng=lon, lat=lat)
        timezone = pytz.timezone(timezone_str)
        the_time = the_time.replace(tzinfo = timezone)
        timestr = the_time.strftime("local time: %Y/%b/%d %H:%M")
        return timestr
    start_latlon = f"{start_lat:.0f},{start_lon:.0f}"
    stop_latlon = f"{stop_lat:.0f},{stop_lon:.0f}"
    return (format_time(mid_time,mid_lat,mid_lon),
            start_latlon, stop_latlon)
```

```{code-cell} ipython3
def sort_keys(the_case):
    number = the_case[4:]
    return int(number)
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
radar_filepaths = Path().glob("**/*h5")
radar_filepaths = list(radar_filepaths)
good_paths = [filename for filename in radar_filepaths
              if (filename.parts[0] == 'data' and str(filename).find('CPR') > 0)]
keys = [filename.parts[1] for filename in good_paths]
good_paths = dict(zip(keys,good_paths))
sorted_keys = list(good_paths.keys())
sorted_keys.sort(key=sort_keys)
ds_dict ={}
for key, filepath in good_paths.items():
    ds_data = xr.open_dataset(filepath, engine='h5netcdf', group='/ScienceData/Data', phony_dims='access')
    ds_data = ds_data.rename_dims({'phony_dim_0':'time','phony_dim_1': 'height'})
    ds_meta = xr.open_dataset(filepath, engine='h5netcdf', group='/ScienceData/Geo', phony_dims='access')
    ds_meta = ds_meta.rename_dims({'phony_dim_0':'time','phony_dim_1': 'height'})
    height = ds_meta['binHeight'].data[0,::-1]
    lonvec = ds_meta['longitude'].data
    latvec = ds_meta['latitude'].data
    distance = calc_distance(lonvec, latvec)
    coords = dict(distance=("time", distance),height=("height",height))
    ds_meta = ds_meta.assign_coords(coords=coords)
    ds_data = ds_data.assign_coords(coords=coords)
    ds_dict[key] = dict(data = ds_data, meta = ds_meta)
```

```{code-cell} ipython3

```

```{code-cell} ipython3
np.nanmean(np.diff(ds_dict['case2']['data'].coords['height']))
```

```{code-cell} ipython3
# cpr_data = xr.open_dataset(good_paths['case2'], engine='h5netcdf', group='/ScienceData/Data', phony_dims='access')
# cpr_meta = xr.open_dataset(good_paths['case2'], engine='h5netcdf', group='/ScienceData/Geo', phony_dims='access')
# cpr_meta.binHeight[0, :10].max() - cpr_meta.binHeight[0, :10].min()
```

## Check times

+++

## get the track distance in km

```{code-cell} ipython3
case = 'case14'
lonvec = get_var(good_paths[case],'longitude','Geo')
latvec = get_var(good_paths[case],'latitude','Geo')
heights = get_var(good_paths[case],'binHeight','Geo')
heights.shape
```

## add coordinates

+++

### distance

```{code-cell} ipython3
distance = calc_distance(lonvec,latvec)
distance
```

```{code-cell} ipython3
### height
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

for the_case in sorted_keys[:1]:
    cpr_data = ds_dict[the_case]['data']
    print(cpr_data.coords)
    fig, ax = plt.subplots(2, 1, figsize=(12, 5))
    vmin=-5
    vmax=5
    the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
    cmap_ref=copy.copy(cm.coolwarm)
    cmap_ref.set_over('w')
    cmap_ref.set_under('0.5')
    cmap_ref.set_bad('0.75') #75% grey
    doppler_vel = np.fliplr(cpr_data['dopplerVelocity'].data)
    cpr_data['dopplerVelocity'].data = doppler_vel
    cpr_data['dopplerVelocity'].T.plot.pcolormesh(ax=ax[0],x='distance',y='height',
                                                  yincrease=True, 
                                                  norm=the_norm, cmap=cmap_ref);
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
