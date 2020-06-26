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

v = np.arange(0, 81, 5)
u_v = np.arange(10, 60, 5)

fig, (ax22, ax33) = plt.subplots(2, 1, figsize=(7, 5))
cs2 = ax22.contour(VI_peru.P.values, VI_peru.PE.values, VI_peru.VI.values, levels= np.arange(-200, 81, 25),
                   colors=('k',), linestyles=('-',),linewidths=(1,), alpha=.5)
cs = ax22.contourf(VI_peru.P.values, VI_peru.PE.values, VI_peru.VI.values, v, cmap="Spectral_r")
plt.clabel(cs2, fmt = '%2.1d', colors = 'k', fontsize=14) #contour line labels
cbar = fig.colorbar(cs, shrink=0.8, extend='both', ax=ax22)
ax22.set_ylabel(r'$\Delta$PE (%)')
ax22.set_ylim(0, 50)
ax22.set_xlim(-50, 50)

cs3 = ax33.contourf(VI_peru_u.P.values, VI_peru_u.PE.values, VI_peru_u.VI.values, u_v, cmap="Purples_r")
cbar3 = fig.colorbar(cs3, shrink=0.8, extend='both', ax=ax33)
ax33.set_xlabel(r'$\Delta$P (%)')
ax33.set_ylabel(r'$\Delta$PE (%)')
ax33.set_ylim(0, 50)
ax33.set_xlim(-50, 50)

plt.tight_layout()
fig.savefig("./output/figures/12_VI_PERU_scale.png", bbox_inches='tight', dpi=200)
plt.close()


# VI at basin scale using Nivel

shp = pd.read_pickle("./data/processed/SHP/UH.pkl")
bdk_cal = pd.read_pickle("./scripts/to_output/data_bk.pkl").dropna(axis=0)

VI_nivel = pickle.load(open("./scripts/to_output/VI_nivel_scale.pkl", "rb"))
VI_nivel_u = pickle.load(open("./scripts/to_output/VI_nivel_scale_u.pkl", "rb"))

v = np.arange(0, 91, 5)
u_v = np.arange(10, 60, 5)

#amazonas
fig3 = plt.figure(constrained_layout=True, figsize = (8, 4.5))
gs = fig3.add_gridspec(2, 2, width_ratios = [1, .35],  height_ratios = [.6, .4])

f3_ax0 = fig3.add_subplot(gs[:-1, 0])
cs2 = f3_ax0.contour(VI_nivel[0].P.values, VI_nivel[0].PE.values, VI_nivel[0].VI.values, levels= np.arange(-200, 81, 25),
                   colors=('k',), linestyles=('-',),linewidths=(1,), alpha=.5)
cs = f3_ax0.contourf(VI_nivel[0].P.values, VI_nivel[0].PE.values, VI_nivel[0].VI.values,  v, cmap="Spectral_r")
plt.clabel(cs2, fmt = '%2.1d', colors = 'k', fontsize=14) #contour line labels
fig3.colorbar(cs, shrink=0.8, extend='both', ax=f3_ax0)
f3_ax0.set_ylabel(r'$\Delta$PE (%)')
f3_ax0.set_ylim(0, 50)
f3_ax0.set_xlim(-50, 50)

f3_ax1 = fig3.add_subplot(gs[-1:, 0])
cs3 = f3_ax1.contourf(VI_nivel_u[0].P.values, VI_nivel_u[0].PE.values, VI_nivel_u[0].VI.values, u_v, cmap="Purples_r")
fig3.colorbar(cs3, shrink=0.8, extend='both', ax=f3_ax1)
f3_ax1.set_xlabel(r'$\Delta$P (%)')
f3_ax1.set_ylabel(r'$\Delta$PE (%)')
f3_ax1.set_ylim(0, 50)
f3_ax1.set_xlim(-50, 50)

f3_ax2 = fig3.add_subplot(gs[:, 1])
shp.plot(color = "gray", vmin=0, vmax=1, legend=True, linewidth=0.1, ax=f3_ax2)
shp.merge(bdk_cal[bdk_cal.Nivel == "Amazonas"], on='ID').plot(ax=f3_ax2, color="green")
f3_ax2.axis('off')

fig3.savefig("./output/figures/12_VI_Nivel_scale_Amazon.png",
             bbox_inches='tight',
             dpi = 200)
plt.close()

#Pacifico
fig3 = plt.figure(constrained_layout=True, figsize = (8, 4.5))
gs = fig3.add_gridspec(2, 2, width_ratios = [1, .35],  height_ratios = [.6, .4])

f3_ax0 = fig3.add_subplot(gs[:-1, 0])
cs2 = f3_ax0.contour(VI_nivel[1].P.values, VI_nivel[1].PE.values, VI_nivel[1].VI.values, levels= np.arange(-200, 81, 25),
                   colors=('k',), linestyles=('-',),linewidths=(1,), alpha=.5)
cs = f3_ax0.contourf(VI_nivel[1].P.values, VI_nivel[1].PE.values, VI_nivel[1].VI.values, v, cmap="Spectral_r")
plt.clabel(cs2, fmt = '%2.1d', colors = 'k', fontsize=14) #contour line labels
fig3.colorbar(cs, shrink=0.8, extend='both', ax=f3_ax0)
f3_ax0.set_ylabel(r'$\Delta$PE (%)')
f3_ax0.set_ylim(0, 50)
f3_ax0.set_xlim(-50, 50)

f3_ax1 = fig3.add_subplot(gs[-1:, 0])
cs3 = f3_ax1.contourf(VI_nivel_u[1].P.values, VI_nivel_u[1].PE.values, VI_nivel_u[1].VI.values, u_v, cmap="Purples_r")
fig3.colorbar(cs3, shrink=0.8, extend='both', ax=f3_ax1)
f3_ax1.set_xlabel(r'$\Delta$P (%)')
f3_ax1.set_ylabel(r'$\Delta$PE (%)')
f3_ax1.set_ylim(0, 50)
f3_ax1.set_xlim(-50, 50)

f3_ax2 = fig3.add_subplot(gs[:, 1])
shp.plot(color = "gray", vmin=0, vmax=1, legend=True, linewidth=0.1, ax=f3_ax2)
shp.merge(bdk_cal[bdk_cal.Nivel == "Pacífico"], on='ID').plot(ax=f3_ax2, color="red")

f3_ax2.axis('off')

fig3.savefig("./output/figures/12_VI_Nivel_scale_Pacific.png",
             bbox_inches='tight',
             dpi = 200)
plt.close()

#Titicaca
fig3 = plt.figure(constrained_layout=True, figsize = (8, 4.5))
gs = fig3.add_gridspec(2, 2, width_ratios = [1, .35],  height_ratios = [.6, .4])

f3_ax0 = fig3.add_subplot(gs[:-1, 0])
cs2 = f3_ax0.contour(VI_nivel[2].P.values, VI_nivel[2].PE.values, VI_nivel[2].VI.values, levels= np.arange(-200, 81, 25),
                   colors=('k',), linestyles=('-',),linewidths=(1,), alpha=.5)
cs = f3_ax0.contourf(VI_nivel[2].P.values, VI_nivel[2].PE.values, VI_nivel[2].VI.values, v, cmap="Spectral_r")
plt.clabel(cs2, fmt = '%2.1d', colors = 'k', fontsize=14) #contour line labels
fig3.colorbar(cs, shrink=0.8, extend='both', ax=f3_ax0)
f3_ax0.set_ylabel(r'$\Delta$PE (%)')
f3_ax0.set_ylim(0, 50)
f3_ax0.set_xlim(-50, 50)

f3_ax1 = fig3.add_subplot(gs[-1:, 0])
cs3 = f3_ax1.contourf(VI_nivel_u[2].P.values, VI_nivel_u[2].PE.values, VI_nivel_u[2].VI.values, u_v, cmap="Purples_r")
fig3.colorbar(cs3, shrink=0.8, extend='both', ax=f3_ax1)
f3_ax1.set_xlabel(r'$\Delta$P (%)')
f3_ax1.set_ylabel(r'$\Delta$PE (%)')
f3_ax1.set_ylim(0, 50)
f3_ax1.set_xlim(-50, 50)

f3_ax2 = fig3.add_subplot(gs[:, 1])
shp.plot(color = "gray", vmin=0, vmax=1, legend=True, linewidth=0.1, ax=f3_ax2)
shp.merge(bdk_cal[bdk_cal.Nivel == "Titicaca"], on='ID').plot(ax=f3_ax2, color="blue")
f3_ax2.axis('off')

fig3.savefig("./output/figures/12_VI_Nivel_scale_Titicaca.png", bbox_inches='tight',
             dpi = 200)
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
names_01 = to_plot[(to_plot.VI == to_plot.VI.cat.categories[4]) & (to_plot.VI_u == to_plot.VI_u.cat.categories[0])].NOMBRE


cmap = mpl.colors.ListedColormap(["dodgerblue" ,"lightskyblue", "mistyrose", "lightsalmon",'crimson'])
plt.rc('grid', linestyle=":", color='black', alpha=.25)

fig, (ax22, ax33) = plt.subplots(1, 2, figsize=(8, 6), dpi=150)

ax22.set_axisbelow(False)
ax = to_plot[to_plot.VI.notna()].plot("VI", ax=ax22, cmap=cmap, legend=True)
to_plot[to_plot.VI.isna()].plot(ax=ax22, color="lightgrey")
leg = ax.get_legend()
leg.set_bbox_to_anchor((.18, .12, .2, .2))
for i in range(5):
    leg.get_texts()[i].set_text(["< 0", "0-10", "10-20", "20-50", ">50"][i])
#ax22.axis('off')
ax22.set_ylim(-18.5, 0.25)
ax22.set_xlim(-82, -68.5)
#ax22.grid(False)
ax22.set_title(r'$\bf{Vulnerabilidad}$' + "\n" + "PE = 20% & P = -20%")

ax33.set_axisbelow(False)
ax = to_plot[to_plot.VI_u.notna()].plot("VI_u", ax=ax33, cmap=cmap, legend=True)
to_plot[to_plot.VI_u.isna()].plot(ax=ax33, color="lightgrey")
leg = ax.get_legend()
leg.set_bbox_to_anchor((.18, .12, .2, .2))
for i in range(5):
    leg.get_texts()[i].set_text(["10-20", "20-30", "30-40", "40-50", ">50"][i])
#ax33.axis('off')
ax33.set_ylim(-18.5, 0.25)
ax33.set_xlim(-82, -68.5)
#ax33.grid(False)
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
bins = [-np.inf, -20, -10, 0, np.inf] # 0 for 5
bins_u = [-np.inf, 20, 30, 40, 50, np.inf]

bdk_cal['VI'] = pd.cut(bdk_cal["VI"], bins=bins)
bdk_cal['VI_u'] = pd.cut(bdk_cal["VI_u"], bins=bins_u)

to_plot = shp.merge(bdk_cal[["VI", "VI_u", "ID"]], on='ID', how="outer")
names_02 = to_plot[(to_plot.VI == to_plot.VI.cat.categories[3]) & (to_plot.VI_u != to_plot.VI_u.cat.categories[2]) & (to_plot.VI_u != to_plot.VI_u.cat.categories[2])].NOMBRE

cmap = mpl.colors.ListedColormap(["dodgerblue" ,"lightskyblue", "mistyrose", "lightsalmon",'crimson'])
plt.rc('grid', linestyle=":", color='black', alpha=.25)

fig, (ax22, ax33) = plt.subplots(1, 2, figsize=(8, 6), dpi=150)

ax22.set_axisbelow(False)
ax = to_plot[to_plot.VI.notna()].plot("VI", ax=ax22, cmap=cmap, legend=True)
to_plot[to_plot.VI.isna()].plot(ax=ax22, color="lightgrey")
leg = ax.get_legend()
leg.set_bbox_to_anchor((.18, .12, .2, .2))
for i in range(4):
    leg.get_texts()[i].set_text([">20", "10-20", "0-10", "<0"][i])
#ax22.axis('off')
ax22.set_ylim(-18.5, 0.25)
ax22.set_xlim(-82, -68.5)
#ax22.grid(False)
ax22.set_title(r'$\bf{Cambio}$' + "\n" + "PE = 20% & VI = 25%")

ax33.set_axisbelow(False)
ax = to_plot[to_plot.VI_u.notna()].plot("VI_u", ax=ax33, cmap=cmap, legend=True)
to_plot[to_plot.VI_u.isna()].plot(ax=ax33, color="lightgrey")
leg = ax.get_legend()
leg.set_bbox_to_anchor((.18, .12, .2, .2))
for i in range(5):
    leg.get_texts()[i].set_text(["10-20", "20-30", "30-40", "40-50", ">50"][i])
#ax33.axis('off')
ax33.set_ylim(-18.5, 0.25)
ax33.set_xlim(-82, -68.5)
#ax33.grid(False)
ax33.set_title(r'$\bf{Incertidumbre}$' + "\n" + "PE = 20% & VI = 25%")

plt.tight_layout()

fig.savefig("./output/figures/14_P_f(PE,VI).png", bbox_inches='tight')
plt.close()

"""
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
"""

# new figure:

from matplotlib.patches import Patch

shp = pd.read_pickle("./data/processed/SHP/UH.pkl")

names_basin = names_01.tolist() + names_02.tolist()
basin_in_danger = list(set([x for x in names_basin if names_basin.count(x) > 1]))

basin_in_danger_but_no_too_much = list(set(names_basin))
basin_in_danger_but_no_too_much = [x for x in basin_in_danger_but_no_too_much if x not in basin_in_danger]

shp_not_used = shp[~shp.ID.isin(bdk_cal.ID)]
shp_used = shp[shp.ID.isin(bdk_cal.ID)]
plt02 = shp[shp.NOMBRE.isin(basin_in_danger_but_no_too_much)]
plt01 = shp[shp.NOMBRE.isin(basin_in_danger)]


fig, ax = plt.subplots(dpi = 300)

shp_not_used.plot(ax = ax, linewidth = .5, color="lightgrey", edgecolor="lightgrey")
shp_used.plot(ax = ax, color="lightskyblue", linewidth = .5, edgecolor="lightgrey")
plt02.plot(ax = ax, color="lightcoral", linewidth = .5, edgecolor="lightgrey")
plt01.plot(ax = ax, color="maroon", linewidth = .5, edgecolor="lightgrey")
shp.dissolve(by = "Nivel").boundary.plot(ax = ax, linewidth = .5, edgecolor="black")
ax.set_xlim(-81.5, -68.45)#600
ax.set_ylim(-18.5, 0)
ax.axis('on')
ax.grid(which='minor', alpha=0.2, linestyle=':')
ax.grid(which='major', alpha=0.5, linestyle='--')
ax.xaxis.set_tick_params(labelsize = 7, pad = -3)
ax.yaxis.set_tick_params(labelsize = 7, pad = -3)

legend_elements = [Patch(facecolor='lightgrey', edgecolor='lightgrey', label='No datos'),
                   Patch(facecolor='lightskyblue', edgecolor='lightskyblue', label='No vulnerable'),
                   Patch(facecolor='lightcoral', edgecolor='lightcoral', label='Vulnerable (+)'),
                   Patch(facecolor='maroon', edgecolor='maroon', label='Vulnerable (++)')]

ax.legend(handles=legend_elements, prop={'size': 8}, loc = 3)

texts = [ax.text(plt01.centroid.x.iloc[i]-0.1, plt01.centroid.y.iloc[i]-0.1, i + 1, size = 4, fontweight='bold', color = "black",
                 bbox=dict(facecolor='white', edgecolor='white', boxstyle='round,pad=0.05')) for i in range(len(plt01.NOMBRE))]

plt.tight_layout()
fig.savefig("./output/figures/14_susceptible_basins.png", bbox_inches='tight')
plt.close()
