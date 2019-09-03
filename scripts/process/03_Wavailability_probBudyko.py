import numpy as np
import pandas as pd
import salem
import pickle

# actual evapotranspiration, potential evapotranspiration and precipitation

annual_p = pickle.load(open("./data/processed/PISCO/p.pkl", "rb"))
annual_pet = pickle.load(open("./data/processed/PISCO/pet.pkl", "rb"))
annual_ae = pickle.load(open("./data/processed/AE/ae_mean.pkl", "rb"))

# shp basins

shp = pd.read_pickle("./data/processed/SHP/UH.pkl")

#

data_AE = []
data_P = []
data_PET = []

for i in range(len(shp)):

    subx = shp.iloc[i:i + 1]

    AE = (annual_ae.salem.subset(shape=subx)).salem.roi(shape=subx).mean().values.tolist()
    P = (annual_p.salem.subset(shape=subx)).salem.roi(shape=subx).mean().values.tolist()
    PET = (annual_pet.salem.subset(shape=subx)).salem.roi(shape=subx).mean().values.tolist()

    data_AE.append(np.round(AE, 2))
    data_P.append(np.round(P, 2))
    data_PET.append(np.round(PET, 2))

data_bk = pd.DataFrame(np.column_stack([shp[["ID", "Nivel"]], data_AE, data_P, data_PET]),
                       columns=["ID", "Nivel", "AE", "P", "PE"]).\
    assign(Ai=lambda x: pd.to_numeric(x.PE/x.P),
           Ei=lambda x: pd.to_numeric(x.AE/x.P),
           AE_PE=lambda x: pd.to_numeric(x.AE-x.PE))

def calib_budyko(EI, AI, ae_pet):
    """
        res = []
    for j in np.arange(1,20,.01):
        model = 1 + (b) - np.power((1 + np.power(b, j)), 1 / j)
        res.append(np.sqrt(np.mean((model - (a)) ** 2)))
    return(np.arange(1,20,.01)[res.index(min(res))])
    """

    if pd.isnull(AI):
        return AI
    elif EI > 1:        # water limit (arid) supply limit
        return np.nan
    elif ae_pet > 0:    # energy limit
        return np.nan
    else:
        res = pd.DataFrame({"range": np.arange(1, 20, .1)})
        res["model_value"] = res.apply(lambda x: 1 + (AI) - np.power((1 + np.power(AI, x.range)), 1 / x.range), axis=1)
        res["sqrt"] = res.apply(lambda x: np.sqrt(np.mean((x.model_value - (EI)) ** 2)), axis=1)
        return float(res[res.sqrt == res.sqrt.min()].range.values)

data_bk["omega"] = data_bk.apply(lambda x: calib_budyko(AI=x.Ai, EI=x.Ei, ae_pet=x.AE_PE), axis=1)
data_bk.to_pickle("./scripts/to_output/data_bk.pkl")
