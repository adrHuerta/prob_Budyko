import numpy as np
import pandas as pd
import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.3, rc={"lines.linewidth": 1.5})

VI_peru = xr.open_dataset("./scripts/to_output/VI_peru_scale.nc", decode_times=False)
VI_peru_u = xr.open_dataset("./scripts/to_output/VI_peru_scale_u.nc", decode_times=False)

# VI at Peru scale

fig, (ax22, ax33) = plt.subplots(2, 1, figsize=(7, 5))
cs2 = ax22.contour(VI_peru.P.values, VI_peru.PE.values, VI_peru.VI.values, levels= np.arange(-20, 81, 20),
                   colors=('k',), linestyles=('-',),linewidths=(1,))
cs = ax22.contourf(VI_peru.P.values, VI_peru.PE.values, VI_peru.VI.values, levels=25, vmax=180, vmin =-180, cmap="PiYG_r")
plt.clabel(cs2, fmt = '%2.1d', colors = 'k', fontsize=14) #contour line labels
cbar = fig.colorbar(cs, shrink=0.8, extend='both', ax=ax22)
ax22.set_ylabel(r'$\Delta$PE (%)')
ax22.set_ylim(0, 50)
ax22.set_xlim(-50, 50)

cs3 = ax33.contourf(VI_peru_u.P.values, VI_peru_u.PE.values, VI_peru_u.VI.values, levels=15, vmax=60, vmin=15, cmap="Purples_r")
cbar3 = fig.colorbar(cs3, shrink=0.8, extend='both', ax=ax33)
ax33.set_xlabel(r'$\Delta$P (%)')
ax33.set_ylabel(r'$\Delta$PE (%)')
ax33.set_ylim(0, 50)
ax33.set_xlim(-50, 50)

plt.tight_layout()

fig.savefig("./output/figures/12_VI_PERU_scale.png", bbox_inches='tight')
plt.close()


# VI at basin scale using Nivel

VI_basin = pickle.load(open("./scripts/to_output/VI_basin_scale_using_nivel.pkl", "rb"))
VI_basin_u = pickle.load(open("./scripts/to_output/VI_basin_scale_using_nivel_u.pkl", "rb"))

PE_new = np.round(np.arange(0, 50.1, 0.1), 1)
P_new = np.round(np.arange(-50., 50.1, 0.1), 1)

VI_basin = [i.reindex(PE=PE_new, P=P_new, method="nearest") for i in VI_basin]
VI_basin_u = [i.reindex(PE=PE_new, P=P_new, method="nearest") for i in VI_basin_u]

res1 = [VI.where((VI.PE == 20) & (VI.P == -20), drop=True).values.mean() for VI in VI_basin]
res2 = [VI.where(VI.PE == 20, drop=True).where(VI > 24, drop=True).where(VI < 26, drop=True).P.values.mean() for VI in VI_basin]
res2_pos = [np.where((np.array(VI.where(VI.PE == 20, drop=True).values.tolist()[0]) > 24) &
                     (np.array(VI.where(VI.PE == 20, drop=True).values.tolist()[0]) < 26)) for VI in VI_basin]

res1_u = [VI.where((VI.PE == 20) & (VI.P == -20), drop=True).values.mean() for VI in VI_basin_u]
res2_u = []
for i in range(len(VI_basin_u)):
    VIu_i = np.array(VI_basin_u[i].where(VI_basin_u[i].PE == 20, drop=True).values.tolist()[0])
    res2_u.append( np.round(np.mean( VIu_i[res2_pos[i]]), 3))

"""
fig, ax22 = plt.subplots(figsize=(6, 2))
VI_basin[0].plot()
fig, ax23 = plt.subplots(figsize=(6, 2))
VI_basin[9].plot()
"""

# spatial VI according to PE and P variations

shp = pd.read_pickle("./data/processed/SHP/UH.pkl")
bdk_cal = pd.read_pickle("./scripts/to_output/data_bk.pkl").dropna(axis=0)
bdk_cal["VI"] = res1
bdk_cal["VI_u"] = res1_u

bins = [-np.inf, 0,  10, 20, 50, np.inf]
bins_u = [-np.inf, 20, 30, 40, 50, np.inf]
bdk_cal['VI'] = pd.cut(bdk_cal["VI"], bins=bins)
bdk_cal['VI_u'] = pd.cut(bdk_cal["VI_u"], bins=bins_u)

to_plot = shp.merge(bdk_cal[["VI", "VI_u", "ID"]], on='ID', how="outer")


cmap = mpl.colors.ListedColormap(["dodgerblue" ,"lightskyblue", "mistyrose", "lightsalmon",'crimson'])

fig, (ax22, ax33) = plt.subplots(1, 2, figsize=(8, 6), dpi=150)

ax = to_plot[to_plot.VI.notna()].plot("VI", ax=ax22, cmap=cmap, legend=True)
to_plot[to_plot.VI.isna()].plot(ax=ax22, color="lightgrey")
leg = ax.get_legend()
leg.set_bbox_to_anchor((.1, .1, .2, .2))
for i in range(5):
    leg.get_texts()[i].set_text(["< 0", "0-10", "10-20", "20-50", ">50"][i])
ax22.axis('off')
ax22.set_ylim(-18.5,0)
ax22.set_xlim(-81.3,-68.7)
ax22.grid(False)
ax22.set_title(r'$\bf{Vulnerabilidad}$' + "\n" + "PE = 20% & P = -20%")

ax = to_plot[to_plot.VI_u.notna()].plot("VI_u", ax=ax33, cmap=cmap, legend=True)
to_plot[to_plot.VI_u.isna()].plot(ax=ax33, color="lightgrey")
leg = ax.get_legend()
leg.set_bbox_to_anchor((.1, .1, .2, .2))
for i in range(5):
    leg.get_texts()[i].set_text(["10-20", "20-30", "30-40", "40-50", ">50"][i])
ax33.axis('off')
ax33.set_ylim(-18.5,0)
ax33.set_xlim(-81.3,-68.7)
ax33.grid(False)
ax33.set_title(r'$\bf{Incertidumbre}$' + "\n" + "PE = 20% & P = -20%")

plt.tight_layout()

fig.savefig("./output/figures/13_VI_f(PE,P).png", bbox_inches='tight')
plt.close()

# spatial P according to PE and VI variations

shp = pd.read_pickle("./data/processed/SHP/UH.pkl")
bdk_cal = pd.read_pickle("./scripts/to_output/data_bk.pkl").dropna(axis=0)
bdk_cal["VI"] = res2
bdk_cal["VI_u"] = res2_u

bdk_cal = bdk_cal.dropna(axis=0)
bins = [-np.inf, -20, -10, 0, np.inf]
bins_u = [-np.inf, 20, 30, 40, 50, np.inf]

bdk_cal['VI'] = pd.cut(bdk_cal["VI"], bins=bins)
bdk_cal['VI_u'] = pd.cut(bdk_cal["VI_u"], bins=bins_u)

to_plot = shp.merge(bdk_cal[["VI", "VI_u", "ID"]], on='ID', how="outer")

cmap = mpl.colors.ListedColormap(["dodgerblue" ,"lightskyblue", "mistyrose", "lightsalmon",'crimson'])

fig, (ax22, ax33) = plt.subplots(1, 2, figsize=(8, 6), dpi=150)

ax = to_plot[to_plot.VI.notna()].plot("VI", ax=ax22, cmap=cmap, legend=True)
to_plot[to_plot.VI.isna()].plot(ax=ax22, color="lightgrey")
leg = ax.get_legend()
leg.set_bbox_to_anchor((.1, .1, .2, .2))
for i in range(4):
    leg.get_texts()[i].set_text([">20", "10-20", "0-10", "<0"][i])
ax22.axis('off')
ax22.set_ylim(-18.5,0)
ax22.set_xlim(-81.3,-68.7)
ax22.grid(False)
ax22.set_title(r'$\bf{Cambio}$' + "\n" + "PE = 20% & VI = 25%")

ax = to_plot[to_plot.VI_u.notna()].plot("VI_u", ax=ax33, cmap=cmap, legend=True)
to_plot[to_plot.VI_u.isna()].plot(ax=ax33, color="lightgrey")
leg = ax.get_legend()
leg.set_bbox_to_anchor((.1, .1, .2, .2))
for i in range(5):
    leg.get_texts()[i].set_text(["10-20", "20-30", "30-40", "40-50", ">50"][i])
ax33.axis('off')
ax33.set_ylim(-18.5,0)
ax33.set_xlim(-81.3,-68.7)
ax33.grid(False)
ax33.set_title(r'$\bf{Incertidumbre}$' + "\n" + "PE = 20% & VI = 25%")

plt.tight_layout()

fig.savefig("./output/figures/14_P_f(PE,VI).png", bbox_inches='tight')
plt.close()


################
#using both datasets

fig, ((ax22, ax33), (ax44, ax55)) = plt.subplots(2, 2, figsize=(18, 10), dpi=150)

cmap = mpl.colors.ListedColormap(["dodgerblue" ,"lightskyblue", "mistyrose", "lightsalmon",'crimson'])

ax = to_plot[to_plot.VI.notna()].plot("VI", ax=ax22, cmap=cmap, legend=True)
to_plot[to_plot.VI.isna()].plot(ax=ax22, color="lightgrey")
leg = ax.get_legend()
leg.set_bbox_to_anchor((.1, .1, .2, .2))
for i in range(5):
    leg.get_texts()[i].set_text(["< 0", "0-10", "10-20", "20-50", ">50"][i])
ax22.axis('off')
ax22.set_ylim(-18.5,0)
ax22.set_xlim(-81.3,-68.7)
ax22.grid(False)
ax22.set_title(r'$\bf{Vulnerabilidad}$' + "\n" + "PE = 20% & P = -20%")

ax = to_plot[to_plot.VI_u.notna()].plot("VI_u", ax=ax33, cmap=cmap, legend=True)
to_plot[to_plot.VI_u.isna()].plot(ax=ax33, color="lightgrey")
leg = ax.get_legend()
leg.set_bbox_to_anchor((.1, .1, .2, .2))
for i in range(5):
    leg.get_texts()[i].set_text(["10-20", "20-30", "30-40", "40-50", ">50"][i])
ax33.axis('off')
ax33.set_ylim(-18.5,0)
ax33.set_xlim(-81.3,-68.7)
ax33.grid(False)
ax33.set_title(r'$\bf{Incertidumbre}$' + "\n" + "PE = 20% & P = -20%")

cmap = mpl.colors.ListedColormap(["dodgerblue" ,"lightskyblue", "mistyrose", "lightsalmon",'crimson'])

ax = to_plot[to_plot.VI.notna()].plot("VI", ax=ax44, cmap=cmap, legend=True)
to_plot[to_plot.VI.isna()].plot(ax=ax44, color="lightgrey")
leg = ax.get_legend()
leg.set_bbox_to_anchor((.1, .1, .2, .2))
for i in range(4):
    leg.get_texts()[i].set_text([">20", "10-20", "0-10", "<0"][i])
ax44.axis('off')
ax44.set_ylim(-18.5,0)
ax44.set_xlim(-81.3,-68.7)
ax44.grid(False)
ax44.set_title(r'$\bf{Cambio}$' + "\n" + "PE = 20% & VI = 25%")

ax = to_plot[to_plot.VI_u.notna()].plot("VI_u", ax=ax55, cmap=cmap, legend=True)
to_plot[to_plot.VI_u.isna()].plot(ax=ax55, color="lightgrey")
leg = ax.get_legend()
leg.set_bbox_to_anchor((.1, .1, .2, .2))
for i in range(5):
    leg.get_texts()[i].set_text(["10-20", "20-30", "30-40", "40-50", ">50"][i])
ax55.axis('off')
ax55.set_ylim(-18.5,0)
ax55.set_xlim(-81.3,-68.7)
ax55.grid(False)
ax55.set_title(r'$\bf{Incertidumbre}$' + "\n" + "PE = 20% & VI = 25%")

plt.tight_layout()
fig.savefig("/home/adrian/Documents/wa_budyko_datasets/figures/13_VI_P_change.png", bbox_inches='tight')
plt.close()
######################

