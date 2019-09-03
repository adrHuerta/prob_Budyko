import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import salem
import pickle

sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.3, rc={"lines.linewidth": 1})

# datasets
annual_ae = pickle.load(open("./data/processed/AE/ae_products.pkl", "rb"))

# shp vert
shp = pd.read_pickle("./data/processed/SHP/sph_ver.pkl")

# ALL AE PRODUCTS

fig = plt.figure(figsize=(18, 15))

grid = AxesGrid(fig, 111,
                nrows_ncols=(2, 3),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=0.5,
                cbar_size=.25
                )

for i in range(6):
    ax = grid[i]
    i_product = list(annual_ae.keys())[i]
    smap = annual_ae[i_product].salem.get_map(data=annual_ae[i_product], cmap="hsv")
    smap.set_lonlat_contours(interval=0)
    smap.set_shapefile(shape=shp, linewidth=1)
    smap.visualize(ax=ax, addcbar=False)
    ax.set_title(i_product, fontsize=18)
    ax.set_axis_off()

im = ax.imshow(np.random.uniform(0, 2500, [16, 16]), cmap="hsv", alpha=0)

cbar = ax.cax.colorbar(im)
cbar.solids.set(alpha=1)

fig.savefig("./output/figures/02_AEproducts.png", bbox_inches='tight')
plt.close()

# HOW SIMILAR ARE ALL AE PRODUCTS?

def Tind(xrf, xrr):
    fv = xrf.to_dataframe().ae.values.tolist()
    rv = xrr.to_dataframe().ae.values.tolist()
    res = pd.DataFrame(
        {'fv': fv,
         'rv': rv
         }).dropna(axis=0, how="all")

    std_f = np.sqrt( (res.fv - res.fv.mean()).pow(2).sum()/len(res.fv) )
    std_r = np.sqrt( (res.rv - res.rv.mean()).pow(2).sum()/len(res.rv) )
    std_fr = ( (res.fv - res.fv.mean() ) * ( res.rv - res.rv.mean() ) ).sum()/len(res.rv)

    R_stat = std_fr/(std_f*std_r)
    BIAS_stat = res.fv.mean() - res.rv.mean()
    MSE_stat = (res.fv - res.rv).pow(2).sum()/len(res.rv)
    return ((1 + R_stat)/2) * (1 - MSE_stat/(np.power(BIAS_stat, 2) + np.power(std_f, 2) + np.power(std_fr, 2)))

dfT = np.zeros((6, 6))

for i in range(6):
    for j in range(6):
        dfT[i, j] = Tind(xrf=annual_ae[list(annual_ae.keys())[i]],
                         xrr=annual_ae[list(annual_ae.keys())[j]])

dfT = pd.DataFrame(dfT,
                   index=annual_ae.keys(),
                   columns=annual_ae.keys())

fig, ax = plt.subplots(figsize=(10, 4))
ax = sns.heatmap(dfT, vmin=0.75, vmax=1, cmap="hot")
fig.savefig("./output/figures/03_Tindex_AEproducts.png", bbox_inches='tight')
plt.close()
