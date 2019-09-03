import pandas as pd
import numpy as np
import pickle

# results

bdk_cal = pd.read_pickle("./scripts/to_output/data_bk.pkl").dropna(axis=0)

#  Ei at peru scale

ai_peru = bdk_cal["Ai"].median()

Ei_peru_scale = {"Ei_median":bdk_cal[["Ei","Ai"]].median(),
                 "Ei_values":bdk_cal.apply(lambda x: 1 + ai_peru - np.power(1 + np.power(ai_peru, x.omega), 1/x.omega),
                                                axis=1)}

#  Ei at nivel scale

ai_pc = bdk_cal.groupby("Nivel", sort=False).Ai.median().Pacífico
ai_az = bdk_cal.groupby("Nivel", sort=False).Ai.median().Amazonas
ai_ti = bdk_cal.groupby("Nivel", sort=False).Ai.median().Titicaca

Ei_nivel_scale = {"Ei_median": bdk_cal.groupby("Nivel", sort=False)[["Ei", "Ai"]].median(),
                  "Ei_values_pac": bdk_cal[bdk_cal.Nivel == "Pacífico"].apply(
                      lambda x: 1 + ai_pc - np.power(1 + np.power(ai_pc, x.omega), 1 / x.omega), axis=1),
                  "Ei_values_amz": bdk_cal[bdk_cal.Nivel == "Amazonas"].apply(
                      lambda x: 1 + ai_az - np.power(1 + np.power(ai_az, x.omega), 1 / x.omega), axis=1),
                  "Ei_values_tit": bdk_cal[bdk_cal.Nivel == "Titicaca"].apply(
                      lambda x: 1 + ai_ti - np.power(1 + np.power(ai_ti, x.omega), 1 / x.omega), axis=1)}


#  Ei at basin scale

Ei_basin_bias_pc = []
Ei_basin_bias_az = []
Ei_basin_bias_ti = []

data_pc = bdk_cal[bdk_cal.Nivel == "Pacífico"]
for j in range(len(data_pc)):

    ei = data_pc.Ei.iloc[j]
    ai = data_pc.Ai.iloc[j]
    ei_model = data_pc.apply(lambda x: 1 + ai - np.power(1 + np.power(ai, x.omega), 1 / x.omega), axis=1)
    Ei_basin_bias_pc.append(((ei-ei_model)/ei).mean()*100)


data_az = bdk_cal[bdk_cal.Nivel == "Amazonas"]
for j in range(len(data_az)):
    ei = data_az.Ei.iloc[j]
    ai = data_az.Ai.iloc[j]
    ei_model = data_az.apply(lambda x: 1 + ai - np.power(1 + np.power(ai, x.omega), 1 / x.omega), axis=1)
    Ei_basin_bias_az.append(((ei - ei_model) / ei).mean() * 100)

data_ti = bdk_cal[bdk_cal.Nivel == "Titicaca"]
for j in range(len(data_ti)):
    ei = data_ti.Ei.iloc[j]
    ai = data_ti.Ai.iloc[j]
    ei_model = data_ti.apply(lambda x: 1 + ai - np.power(1 + np.power(ai, x.omega), 1 / x.omega), axis=1)
    Ei_basin_bias_ti.append((((ei - ei_model) / ei)*100).median())

Ei_basin_bias = Ei_basin_bias_pc + Ei_basin_bias_az+ Ei_basin_bias_ti
bdk_val = bdk_cal[["ID","Nivel", "Ei"]]
bdk_val["Ei"] = Ei_basin_bias


#  Ei at basin scale using all data

data = bdk_cal
Ei_basin = []
for j in range(len(data)):

    ei = data.Ei.iloc[j]
    ai = data.Ai.iloc[j]
    ei_model = data.apply(lambda x: 1 + ai - np.power(1 + np.power(ai, x.omega), 1 / x.omega), axis=1)
    Ei_basin.append(((ei-ei_model)/ei).mean()*100)

bdk_val2 = bdk_cal[["ID","Nivel", "Ei"]]
bdk_val2["Ei"] = Ei_basin

val = {"Peru":Ei_peru_scale,
       "Nivel":Ei_nivel_scale,
       "Basin":bdk_val,
       "Basin2":bdk_val2}

pickle.dump(val, open("./scripts/to_output/data_val.pkl", "wb"))