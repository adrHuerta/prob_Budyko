import numpy as np
import pandas as pd
import salem

## runoff and basins

annual_q = pd.read_csv("./data/raw/Q/Qmensual2.csv")
annual_q['Index'] = pd.to_datetime(annual_q['Index'], format="%Y-%m-%d")
annual_q = annual_q.set_index("Index", drop=True). \
               resample('Y'). \
               agg(lambda x: np.round(x.values.mean(), 2))['2000-01-01':'2014-12-31']

q_selected = annual_q.isnull().sum()[annual_q.isnull().sum() <= 6].index.tolist()
q_selected.remove("CON")
len(q_selected)

annual_q = annual_q[q_selected]
annual_q.columns

shp = salem.read_shapefile("./data/raw/Q/shape_basins_piscopV2.shp")
shp_p = salem.read_shapefile("./data/raw/Q/est_t3.shp")

adr = pd.DataFrame(shp)
shp["Area"] = (shp.to_crs({'init': 'epsg:32717'}).area)  # / 1000
shp = shp[shp["Basin"].isin(q_selected)].drop(['min_x', 'max_x', 'min_y', 'max_y'], axis=1)

annual_q = annual_q[shp.Basin.to_list()]
annual_q.shape

# from Q/s to mm
for i in annual_q.columns:
    #    annual_q[i] = annual_q[i] * 1000*365*24*60*60 / shp[shp.Basin == i].Area.tolist()
    annual_q[i] = annual_q[i] * 1000 * 24 * 30 * 3600 / shp[shp.Basin == i].Area.tolist()

ae_mean = pd.DataFrame(annual_q.apply(lambda x: np.nanmean(x)), columns=["q"]).rename_axis('Basin').reset_index()
ae_mean = shp.merge(ae_mean, on="Basin")

ae_mean.to_pickle("./data/processed/Q/q.pkl")
