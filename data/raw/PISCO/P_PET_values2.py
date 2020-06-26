import xarray as xr
import numpy as np
import pickle

lat_new = np.arange(-18.5, 0.2, 0.01)
lon_new = np.arange(-81.5, -68.25, 0.01)

p = "./data/raw/PISCO/p.nc"
p = xr.open_dataset(p, decode_times=False).\
    drop("z_bnds").\
    rename({"z":"time"}).\
    assign_coords(time = list(range(1981,2017))). \
    sel(time=slice(2000, 2014)).\
    mean(dim="time")

p = p.where((-81.5 < p.longitude) &
                          (p.longitude < -68.25) &
                          (-18.5 < p.latitude) &
                          (p.latitude < 0.2), drop=True).\
    reindex(latitude=lat_new, longitude=lon_new, method="nearest").p


pet = "./data/raw/PISCO/pet.nc"
pet = xr.open_dataset(pet, decode_times=False).\
    drop("time_bnds").\
    assign_coords(time = list(range(1981,2017))). \
    sel(time=slice(2000, 2014)).\
    mean(dim="time")

pet = pet.where((-81.5 < pet.longitude) &
                          (pet.longitude < -68.25) &
                          (-18.5 < pet.latitude) &
                          (pet.latitude < 0.2), drop=True).\
    reindex(latitude=lat_new, longitude=lon_new, method="nearest").pet

pickle.dump(p, open("./data/processed/PISCO/p.pkl", "wb"))
pickle.dump(pet, open("./data/processed/PISCO/pet.pkl", "wb"))