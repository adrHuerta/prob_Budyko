import xarray as xr
import pandas as pd
import numpy as np
import glob
import salem
import pickle

lat_new = np.arange(-18.5, 0.2, 0.01)
lon_new = np.arange(-81.5, -68.25, 0.01)

shp = "./data/raw/AE/Sudamérica.shp"
shp = salem.read_shapefile(shp).\
    to_crs({"init": "epsg:4326"}).iloc[11:12]

#zhang2015

ae_zhang = xr.concat([xr.open_dataset(f) for f in glob.glob('./data/raw/AE/Zhang/Peru/*.nc')],
               dim='time'). \
    rename({"longitude": "lon", "latitude": "lat"}). \
    assign_coords(time=list(range(1982, 2014)))

ae_zhang = ae_zhang.where((-81.5 < ae_zhang.lon) &
                          (ae_zhang.lon < -68.25) &
                          (-18.5 < ae_zhang.lat) &
                          (ae_zhang.lat < 0.2), drop=True).\
    reindex(lat=lat_new, lon=lon_new, method="nearest")

#gleam

ae_gleam = xr.open_dataset("./data/raw/AE/GLEAM/E_1980_2018_GLEAM_v3.3a_YR.nc", decode_times=False). \
    rename({"E": "ae"}).\
    drop("time_bnds").\
    assign_coords(time=list(range(1980, 2019)))

ae_gleam = ae_gleam.where((-81.5 < ae_gleam.lon) &
                          (ae_gleam.lon < -68.25) &
                          (-18.5 < ae_gleam.lat) &
                          (ae_gleam.lat < 0.2), drop=True).\
    reindex(lat=lat_new, lon=lon_new, method="nearest")

#terraclimate

ae_tc = xr.open_dataset("./data/raw/AE/TerraClimate/agg_terraclimate_aet_1980_CurrentYear_GLOBE.nc", decode_times=False).\
    rename({"aet": "ae"}).\
    assign_coords(time=pd.date_range('1980-01-01', "2017-12-31",freq='M')).\
    resample(time="A").sum(). \
    assign_coords(time=list(range(1980, 2018)))

ae_tc = ae_tc.where((-81.5 < ae_tc.lon) &
                          (ae_tc.lon < -68.25) &
                          (-18.5 < ae_tc.lat) &
                          (ae_tc.lat < 0.2), drop=True).\
    reindex(lat=lat_new, lon=lon_new, method="nearest")

#ssebop

ae_ssebop = xr.open_dataset("./data/raw/AE/SSEBop/ae_SSEBop_03_16.nc"). \
    rename({"variable": "ae", "longitude": "lon", "latitude": "lat", "z": "time"}). \
    drop("crs").\
    assign_coords(time=list(range(2003, 2017)))

ae_ssebop = ae_ssebop.where((-81.5 < ae_ssebop.lon) &
                          (ae_ssebop.lon < -68.25) &
                          (-18.5 < ae_ssebop.lat) &
                          (ae_ssebop.lat < 0.2), drop=True).\
    reindex(lat=lat_new, lon=lon_new, method="nearest")

#MODIS16

ae_modis16 = xr.open_dataset("./data/raw/AE/MODIS16/MODIS16_AE_2000_2014.nc"). \
    rename({"__xarray_dataarray_variable__": "ae", "longitude": "lon", "latitude": "lat"}). \
    assign_coords(time=list(range(2000, 2015)))

ae_modis16 = ae_modis16.where((-81.5 < ae_modis16.lon) &
                          (ae_modis16.lon < -68.25) &
                          (-18.5 < ae_modis16.lat) &
                          (ae_modis16.lat < 0.2), drop=True).\
    reindex(lat=lat_new, lon=lon_new, method="nearest")

#Average

ae_mean = (ae_ssebop + ae_ssebop + ae_zhang + ae_gleam + ae_tc) / 5

#climatological values

ae_ssebop_c = ae_ssebop.sel(time=slice(2000, 2015)).\
    ae.\
    mean(dim="time").\
    salem.roi(shape=shp)

ae_zhang_c = ae_zhang.sel(time=slice(2000, 2015)).\
    ae.\
    mean(dim="time").\
    salem.roi(shape=shp)

ae_gleam_c = ae_gleam.sel(time=slice(2000, 2014)).\
    ae.\
    mean(dim="time").\
    salem.roi(shape=shp).\
    transpose()

ae_tc_c = ae_tc.sel(time=slice(2000, 2014)).\
    ae.\
    mean(dim="time").\
    salem.roi(shape=shp)

ae_modis16_c = ae_modis16.sel(time=slice(2000, 2015)).\
    ae.\
    mean(dim="time").\
    salem.roi(shape=shp)

ae_mean_c = ae_mean.sel(time=slice(2000, 2014)).\
    ae.\
    mean(dim="time").\
    salem.roi(shape=shp)

mean_ae = {"GLEAM": ae_gleam_c,
           "MODIS16": ae_modis16_c,
           "MEAN": ae_mean_c,
           "SSEBop": ae_ssebop_c,
           "TerraClimate": ae_tc_c,
           "Zhang": ae_zhang_c}

pickle.dump(mean_ae, open("./data/processed/AE/ae_products.pkl", "wb"))
pickle.dump(ae_gleam_c, open("./data/processed/AE/ae_gleam.pkl", "wb"))
pickle.dump(ae_mean_c, open("./data/processed/AE/ae_mean.pkl", "wb"))
