import numpy as np
import pandas as pd
import salem
import pickle

# actual evapotranspiration, potential evapotranspiration and precipitation

annual_p = pickle.load(open("./data/processed/PISCO/p.pkl", "rb"))
annual_pet = pickle.load(open("./data/processed/PISCO/pet.pkl", "rb"))
annual_ae = pickle.load(open("./data/processed/AE/ae_products.pkl", "rb"))

# Q and basins

shp = pd.read_pickle("./data/processed/Q/q.pkl")

# masking by basin, computing area values of p and statistics
resBK = []
for i in range(len(shp)):

    subx = shp.iloc[i: i + 1]

    PP = (annual_p.salem.subset(shape=subx)).salem.roi(shape=subx).mean().values.tolist()
    PET = (annual_pet.salem.subset(shape=subx)).salem.roi(shape=subx).mean().values.tolist()
    ET_bdk = np.round((1 + PET/PP - np.power(1 + np.power(PET/PP, 2.6), 1/2.6)) * PP, 2)

    resET = []
    for j in annual_ae.keys():
        res = (annual_ae[j].salem.subset(shape=subx)).salem.roi(shape=subx).mean().values.tolist()
        res = np.round(res, 2)
        resET.append(res)

    resET = pd.DataFrame(resET)
    resET.columns = ["ET_m_values"]
    resET["ET_m"] = annual_ae.keys()
    resET["ET_BK"] = ET_bdk
    resET["Basin"] = subx.Basin.iloc[0]

    resBK.append(resET)

resBK = pd.concat(resBK).reset_index()
resBK["BIAS"] = resBK.apply(lambda x: x.ET_m_values - x.ET_BK, axis=1)

resBK = {"resBK":resBK,
       "rWB":resBK.groupby("ET_m").\
           apply(lambda x: x.ET_m_values.corr(x.ET_BK, method='spearman')),
       "rRMSE":resBK.groupby("ET_m").\
           apply(lambda x: np.sqrt(np.sum(np.power((x.ET_m_values - x.ET_BK), 2)) / len(x.ET_m_values)))}

pickle.dump(resBK, open("./scripts/to_output/resBK.pkl", "wb"))