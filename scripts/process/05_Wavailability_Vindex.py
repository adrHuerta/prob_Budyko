import pandas as pd
import numpy as np
import xarray as xr
import pickle
from pandarallel import pandarallel
pandarallel.initialize()

# results

bdk_cal = pd.read_pickle("./scripts/to_output/data_bk.pkl").dropna(axis=0)

def func(x):
    return 1 + x.Ai_sp - np.power(1 + np.power(x.Ai_sp, x.omega), 1 / x.omega)

# VI at Peru scale using pandas

omega_vi = bdk_cal.omega.to_list()
code_vi = list(bdk_cal.index)
nivel_vi = bdk_cal.Nivel.to_list()
pet_space = (np.linspace(0, 50, 100) / 100).round(3)
p_space = (np.linspace(-50, 50, 100) / 100).round(2)

omega_series = pd.Series(np.repeat(omega_vi, len(pet_space)*len(p_space)), name="omega")
nivel_series = pd.Series(np.repeat(nivel_vi, len(pet_space)*len(p_space)), name="nivel")
code_series = pd.Series(np.repeat(code_vi, len(pet_space)*len(p_space)), name="code")
pet_series = pd.Series(np.tile(np.tile(pet_space, len(pet_space)), len(omega_vi)), name="PE")
p_series = pd.Series(np.tile(np.repeat(p_space, len(p_space)), len(omega_vi)), name="P")
data_all = pd.concat([nivel_series, code_series, omega_series, pet_series, p_series],  axis=1)

df_vi = data_all

p_hist = bdk_cal.P.median()
ae_hist = bdk_cal.AE.median()
pet_hist = bdk_cal.PE.median()
wa_hist = p_hist - ae_hist

df_vi["PET_sp"] = (pet_hist + pet_hist*df_vi.PE)
df_vi["P_sp"] = (p_hist + p_hist*df_vi.P)
df_vi["Ai_sp"] = (df_vi.PET_sp / df_vi.P_sp)
df_vi["Ei"] = df_vi.parallel_apply(func, axis=1)
df_vi["AE_sp"] = df_vi["Ei"] * df_vi["P_sp"]
df_vi["WA_model"] = df_vi["P_sp"] - df_vi["AE_sp"]
df_vi["VI"] = np.round((wa_hist-df_vi["WA_model"]) / wa_hist * 100, 3)

df_vi = np.round(df_vi.groupby(["PE", "P"]).VI.median(), 3)
df_vi = df_vi.to_xarray()
df_vi.PE.values = np.round(np.linspace(0, 50, 100), 1)
df_vi.P.values = np.round(np.linspace(-50, 50, 100), 1)

df_vi.to_netcdf("./scripts/to_output/VI_peru_scale.nc")


# VI at basin scale using Nivel

omega_vi = bdk_cal.omega.to_list()
code_vi = list(bdk_cal.index)
nivel_vi = bdk_cal.Nivel.to_list()
pet_space = (np.linspace(0, 50, 100) / 100).round(3)
p_space = (np.linspace(-50, 50, 100) / 100).round(2)

omega_series = pd.Series(np.repeat(omega_vi, len(pet_space)*len(p_space)), name="omega")
nivel_series = pd.Series(np.repeat(nivel_vi, len(pet_space)*len(p_space)), name="nivel")
code_series = pd.Series(np.repeat(code_vi, len(pet_space)*len(p_space)), name="code")
pet_series = pd.Series(np.tile(np.tile(pet_space, len(pet_space)), len(omega_vi)), name="PE")
p_series = pd.Series(np.tile(np.repeat(p_space, len(p_space)), len(omega_vi)), name="P")
data_all = pd.concat([nivel_series, code_series, omega_series, pet_series, p_series],  axis=1)

h_res = []
for h in range(0,len(bdk_cal)):

    df_vi = data_all[data_all.nivel == bdk_cal.Nivel.iloc[h]] # analysis by Nivel
    #df_vi = data_all #  analysis by all
    p_hist = bdk_cal.P.iloc[h]
    pet_hist = bdk_cal.PE.iloc[h]
    ae_hist = bdk_cal.AE.iloc[h]
    wa_hist = p_hist - ae_hist

    df_vi["PET_sp"] = (pet_hist + pet_hist*df_vi.PE)
    df_vi["P_sp"] = (p_hist + p_hist*df_vi.P)
    df_vi["Ai_sp"] = (df_vi.PET_sp / df_vi.P_sp)
    df_vi["Ei"] = df_vi.parallel_apply(func, axis=1)
    df_vi["AE_sp"] = df_vi["Ei"] * df_vi["P_sp"]
    df_vi["WA_model"] = df_vi["P_sp"] - df_vi["AE_sp"]
    df_vi["VI"] = np.round((wa_hist - df_vi["WA_model"]) / wa_hist * 100, 3)
    df_vi = np.round(df_vi.groupby(["PE", "P"]).VI.median(), 3)
    df_vi = df_vi.to_xarray()
    df_vi.PE.values = np.round(np.linspace(0, 50, 100), 1)
    df_vi.P.values = np.round(np.linspace(-50, 50, 100), 1)
    h_res.append(df_vi)

pickle.dump(h_res, open("./scripts/to_output/VI_basin_scale_using_nivel.pkl", "wb"))