import xarray as xr
import numpy as np
import pandas as pd
from cdo import *
cdo = Cdo()

# potential evapotranspiration estimation
# from daily to annual values
tx = "./data/raw/PISCO/PISCOdtx_v1.1.nc"
tn = "./data/raw/PISCO/PISCOdtn_v1.1.nc"

tx = xr.open_dataset(tx, decode_times=False)
tn = xr.open_dataset(tn, decode_times=False)

lat = np.tile(tx["latitude"].values, (145, 1)).transpose()

dates = pd.date_range('1981-01-01', "2016-12-31", freq='D')
dates = [int(i.strftime("%j")) for i in dates]

for i in range(0, 13149):
    itx = tx.tx.isel(time=i)
    itn = tn.tn.isel(time=i)
    itime = dates[i]
    delta = np.sin((2 * np.pi * itime / 365) - 1.405) * 0.4093
    d_r = 1 + 0.033 * np.cos(2 * np.pi * itime/ 365)
    W_s = np.arccos(-np.tan(np.radians(lat)) * np.tan(delta))
    Re = 15.392 * d_r * (
                W_s * np.sin(np.radians(lat)) * np.sin(delta) + np.cos(np.radians(lat)) * np.cos(delta) * np.sin(
            W_s))
    a_hg = np.sqrt((itx - itn)) * ((itx + itn) / 2 + 17.8) * Re * 0.0023
    a_hg.name = "pet"
    a_hg.to_netcdf('./data/raw/PISCO/results/results-%05d.nc' % i, mode='w')


pet = cdo.cat(input="./data/raw/PISCO/results/*.nc")
"""
cdo.sellonlatbox(-73.5, -70, -15, -12.5, input=pet, output="/home/adrian/Desktop/goyburo/pet.nc")
"""
pet = cdo.yearsum(input=pet, output="./data/raw/PISCO/pet.nc")

cdo.cleanTempDir()

# precipitation
# from daily to annual values

cdo.yearsum(input="./data/raw/PISCO/PISCOpd.nc",
            output="./data/raw/PISCO/p.nc")
cdo.cleanTempDir()
"""
-70, -73.5
-12.5, 15
"""