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
    #annual_q[i] = annual_q[i] * 1000*365*24*60*60 / shp[shp.Basin == i].Area.tolist()
    annual_q[i] = annual_q[i] * 86400*1000*30.41*12 / shp[shp.Basin == i].Area.tolist()
    # https://www.researchgate.net/post/How_to_convert_discharge_m3_s_to_mm_of_discharge
    #print(annual_q[i] * 1000 * 24 * 30 * 3600 / shp[shp.Basin == i].Area.tolist())
    #annual_q[i] * 36*24*12*3 / list((shp[shp.Basin == i].Area / 10**6))

ae_mean = pd.DataFrame(annual_q.apply(lambda x: np.nanmean(x)), columns=["q"]).rename_axis('Basin').reset_index()
ae_mean = shp.merge(ae_mean, on="Basin")

ae_mean.to_pickle("./data/processed/Q/q.pkl")


## FIGURE

import matplotlib.pyplot as plt
plt.rc('grid', linestyle=":", color='black', alpha=.5)

shp_p = shp_p[shp_p["Basins"].isin(ae_mean.Basin.to_list())]
shp_p2 = shp_p[shp_p["Basins"].isin(ae_mean.Basin.to_list())]
shp_p2.YVAL.iloc[3] = shp_p2.YVAL.iloc[3] + .8
shp_p2.XVAL.iloc[3] = shp_p2.XVAL.iloc[3] - .7
shp_p2.V_NOM_ESTA.iloc[0] = "ARDILLA"
n_stat = ae_mean.Basin.sort_values().reset_index().Basin + " - " + shp_p2.sort_values("Basins").reset_index().V_NOM_ESTA

shp_vert = pd.read_pickle("/home/adrian/Documents/wa_budyko_datasets/shapefiles/sph_ver.pkl")

fig, ax22 = plt.subplots(figsize=(6, 8))

ax = shp_vert.plot(ax=ax22, edgecolor='black', color='whitesmoke', linewidth=1.2)
ae_mean.plot("Basin", ax=ax22, legend=True, edgecolor='black', cmap="tab20", linewidth=1)
shp_p.plot("Basins", ax=ax22, legend=False, color="black", markersize=25)
leg = ax.get_legend()
leg.set_bbox_to_anchor((.01, .18, .34, .2))
for i in range(0,len(n_stat)):
    leg.get_texts()[i].set_text(n_stat.iloc[i])
    leg.get_texts()[i].set_fontsize(8.5)
leg.get_frame().set_edgecolor('white')
ax22.set_ylim(-18.5, 0.25)
ax22.set_xlim(-82, -68.5)
ax22.grid(True)
for line in range(0,shp_p2.shape[0]):
         ax22.text(shp_p2.XVAL.iloc[line] - 0.1, shp_p2.YVAL.iloc[line] - 0.5, shp_p2.Basins.iloc[line],
         size=8, bbox=dict(boxstyle="round", ec=(1, 1, 1), fc=(1, 1, 1),
         facecolor='white', alpha=0.65), weight='bold')
plt.tight_layout()

fig.savefig("./output/figures/00_evaluation_basins.png",
            bbox_inches='tight', dpi=200)
plt.close()


fig, ax22 = plt.subplots(figsize=(8, 4))

p1 = annual_q.plot(ax=ax22)
ax22.set_ylim([0, 140])
ax22.set_ylabel("Caudal (mm/año)")
ax22.set_xlabel("")
p1.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)
plt.tight_layout()

fig.savefig("./output/figures/00_q_basins.png",
            bbox_inches='tight', dpi=200)
plt.close()

