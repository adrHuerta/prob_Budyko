import numpy as np
import pandas as pd
import salem
import pickle

# actual evapotranspiration and precipitation

annual_p = pickle.load(open("./data/processed/PISCO/p.pkl", "rb"))
annual_pet = pickle.load(open("./data/processed/PISCO/pet.pkl", "rb"))
annual_ae = pickle.load(open("./data/processed/AE/ae_products.pkl", "rb"))

# Q and basins

shp = pd.read_pickle("./data/processed/Q/q.pkl")

# masking by basin, computing area values of p and statistics
resDF = []
resPP = []
for i in range(len(shp)):

    subx = shp.iloc[i: i + 1]

    PP = (annual_p.salem.subset(shape=subx)).salem.roi(shape=subx).mean().values.tolist()
    PET = (annual_pet.salem.subset(shape=subx)).salem.roi(shape=subx).mean().values.tolist()
    #(annual_p.salem.subset(shape=subx)).salem.roi(shape=subx).plot()
    ET_wb = np.round(PP - float(subx.q.values), 2)

    resET = []
    for j in annual_ae.keys():
        res = (annual_ae[j].salem.subset(shape=subx)).salem.roi(shape=subx).mean().values.tolist()
        res = np.round(res, 2)
        resET.append(res)

    resET = pd.DataFrame(resET)
    resET.columns = ["ET_m_values"]
    resET["ET_m"] = annual_ae.keys()
    resET["ET_WB"] = ET_wb
    resET["PET"] = PET
    resET["PP"] = PP
    resET["Basin"] = subx.Basin.iloc[0]

    resDF.append(resET)
    resPP.append(PP)

resDF = pd.concat(resDF).reset_index()
resDF["BIAS"] = resDF.apply(lambda x: x.ET_m_values - x.ET_WB, axis=1)

resWB = {"resDF":resDF,
       "rWB":resDF.groupby("ET_m").\
           apply(lambda x: x.ET_m_values.corr(x.ET_WB, method='spearman')),
       "rRMSE":resDF.groupby("ET_m").\
           apply(lambda x: np.sqrt(np.sum(np.power((x.ET_m_values - x.ET_WB), 2)) / len(x.ET_m_values)))}

pickle.dump(resWB, open("./scripts/to_output/resWB.pkl", "wb"))

###

table_q_area_basin = shp.drop("geometry", axis=1)
table_q_area_basin["p"] =  resPP
table_q_area_basin["Area"] = table_q_area_basin["Area"]/1000000
table_q_area_basin.to_csv("./output/tables/Table_Q_AREA_BASIN.csv")
