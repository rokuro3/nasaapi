#%%
import os
import fsspec

import pandas as pd
import xarray as xr

from datetime import datetime

filepath = 'https://nasa-power.s3.us-west-2.amazonaws.com/syn1deg/temporal/power_syn1deg_monthly_temporal_lst.zarr'
filepath_mapped = fsspec.get_mapper(filepath)
ds = xr.open_zarr(filepath_mapped, consolidated=True)

# different ways to slice the data
#%%
ds_single_point = ds.ALLSKY_SFC_LW_DWN.sel(lat=39, lon=-77, method='nearest').load()
ds_single_time = ds.ALLSKY_SFC_LW_DWN.sel(time=datetime(2022, 12, 31)).load()
ds_time_series = ds.ALLSKY_SFC_LW_DWN.sel(time=pd.date_range(datetime(2019, 12, 31), datetime(2020, 12, 31), freq='1Y')).load()
ds_region = ds.ALLSKY_SFC_LW_DWN.sel(lat=slice(35, 45), lon=slice(-85, -75)).load()

output = r'' # if none the location of the script is where the files will be outputted.

# export region as NetCDF4
ds_region.to_netcdf(path=os.path.join(output, "region.nc"))

# export as CSV
df_region = ds_region.to_dataframe()
df_region.to_csv(os.path.join(output, "region.csv"))