import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.3, rc={"lines.linewidth": 1})

# results

bdk_cal = pd.read_pickle("./scripts/to_output/data_bk.pkl")
shp = pd.read_pickle("./data/processed/SHP/UH.pkl")
bdk_shp = shp.merge(bdk_cal, on='ID')


# RAW BUDYKO CURVE

fig, ax = plt.subplots(figsize=(8,4))
sns.scatterplot("Ai", "Ei", data=bdk_cal, hue="Nivel",
                s=50, palette=["red", "seagreen", "blue"], linewidth=0.1)
ax.set_xlabel("Índice de aridez")
ax.set_ylabel("Índice de evaporación")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles[1:], labels=labels[1:], markerscale=1.5)
plt.close()

# RAW BUDYKO CURVE: ZOOM

fig, ax = plt.subplots(figsize=(8,4))
sns.scatterplot("Ai", "Ei", data=bdk_cal, hue="Nivel",
                s=50, palette=["red","seagreen","blue"], linewidth=0.1)
ax.plot(np.arange(0,1.1,.1), np.arange(0,1.1,.1), "black", linewidth=1)
ax.plot(np.arange(1,601,1), np.repeat(1,600), "black", linewidth=1)
ax.set_xlim(-5,10)#600
ax.set_ylim(0,5)
ax.set_xlabel("Índice de aridez")
ax.set_ylabel("Índice de evaporación")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles[1:], labels=labels[1:], markerscale=1.5)
plt.close()

# BUDYKO CURVE: SUPPLY AND ENERGY LAW

fig, ax = plt.subplots(figsize=(8,4))
sns.scatterplot("Ai", "Ei", data=bdk_cal[bdk_cal.omega.notna()], hue="Nivel",
                s=75, palette=["red","seagreen","blue"], linewidth=0.1)
ax.plot(np.arange(0,1.1,.1), np.arange(0,1.1,.1), "black", linewidth=1.5)
ax.plot(np.arange(1,601,1), np.repeat(1,600), "black", linewidth=1.5)
ax.set_xlim(0,7)
ax.set_ylim(0,1.1)
ax.set_xlabel("Índice de aridez")
ax.set_ylabel("Índice de evaporación")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles[1:], labels=labels[1:], markerscale=1.5)
plt.close()


# OMEGA BOXPLOT

fig1, ax1 = plt.subplots(figsize=(4,4))
ax1 = sns.boxplot(y='omega', x="Nivel", data=bdk_cal, palette=["red","seagreen","blue"])
ax1.set_xlabel('')
ax1.set_ylabel(r'$\omega$')

fig1.savefig("./output/figures/08_omega_boxplot.png", bbox_inches='tight')
plt.close()

# BASIN PLOT, BUDYKO WITH NO LAWS AND OMEGA BOXPLOT

fig4 = plt.figure(figsize=(10,7))

ax8 = plt.subplot2grid((2, 2), (0, 1), colspan=2)

sns.scatterplot("Ai", "Ei", data=bdk_cal, hue="Nivel",
                s=50, palette=["red","seagreen","blue"], linewidth=0.1, ax=ax8)
ax8.plot(np.arange(0,1.1,.1), np.arange(0,1.1,.1), "black", linewidth=1)
ax8.plot(np.arange(1,601,1), np.repeat(1,600), "black", linewidth=1)
ax8.set_xlim(0,10)#600
ax8.set_ylim(0,1.1)
ax8.set_xlabel("Índice de aridez")
ax8.set_ylabel("Índice de evaporación")
handles, labels = ax8.get_legend_handles_labels()
ax8.legend(handles=handles[1:], labels=labels[1:], markerscale=1.5)

ax9 = plt.subplot2grid((2, 2), (1, 1), colspan=2)

sns.boxplot(y='omega', x="Nivel", data=bdk_cal, palette=["red","seagreen","blue"], ax=ax9)
ax9.set_xlabel('')
ax9.set_ylabel(r'$\omega$')

ax10 = plt.subplot2grid((2, 2), (0, 0), rowspan=2)

bdk_shp[bdk_shp.Nivel_y == "Pacífico"].plot(color="red", linewidth=0.1, ax=ax10)
bdk_shp[bdk_shp.Nivel_y == "Amazonas"].plot(color="seagreen", linewidth=0.1, ax=ax10)
bdk_shp[bdk_shp.Nivel_y == "Titicaca"].plot(color="blue", linewidth=0.1, ax=ax10)
ax10.axis('off')
ax10.set_ylim(-18.5, 0)
ax10.set_xlim(-81.3, -68.7)
ax10.grid(False)
ax10.set_title("Categoria de Cuencas (N:231)")

plt.tight_layout()
plt.close()

# RAW SPATIAL Ai / Ei DISTRIBUTION WITH no LIMITS

fig2, (ax2, ax3) = plt.subplots(2, 1, figsize=(4, 6), dpi=150)
cmap = mpl.cm.get_cmap('jet')
cmap.set_over('black')

ax2 = bdk_shp.plot("Ei", cmap="jet", vmin=0, vmax=1, legend=False, linewidth=0.1, ax=ax2)
scatter = ax2.collections[0]
plt.colorbar(scatter, ax=ax2, extend='max')
#ax2.axis('off')
ax2.set_ylim(-18.5,0)
ax2.set_xlim(-81.3,-68.7)
#ax2.grid(False)
ax2.set_title("Índice de evaporación")

ax3 = bdk_shp.plot("Ai", cmap="jet", vmin=0, vmax=10, legend=False, linewidth=0.1, ax=ax3)
scatter = ax3.collections[0]
plt.colorbar(scatter, ax=ax3, extend='max')
#ax3.axis('off')
ax3.set_ylim(-18.5,0)
ax3.set_xlim(-81.3,-68.7)
#ax3.grid(False)
ax3.set_title("Índice de aridez")
plt.tight_layout()

fig2.savefig("./output/figures/05_Ai_Ei_spatial.png", bbox_inches='tight', dpi=200)
plt.close()

# SPATIAL Ai / Ei / omega DISTRIBUTION WITH LAWS

plt.rc('grid', linestyle=":", color='black', alpha=.25)
fig3, (ax4, ax5, ax6) = plt.subplots(1, 3, figsize=(10.5, 3.7), dpi=150)

ax4.set_axisbelow(False)
ax4 = bdk_shp[bdk_shp.omega.notna()].plot("Ei", cmap="jet", vmin=0, vmax=1, legend=True, linewidth=0.1, ax=ax4)
bdk_shp[bdk_shp.omega.isna()].plot(ax=ax4, color="lightgrey")#hatch="//""
#ax4.axis('off')
ax4.set_ylim(-18.5, 0.25)
ax4.set_xlim(-82, -68.5)
ax4.set_title("Índice de evaporación")

ax5.set_axisbelow(False)
ax5 = bdk_shp[bdk_shp.omega.notna()].plot("Ai", cmap="jet", vmin=0, vmax=10, legend=True, linewidth=0.1, ax=ax5)
bdk_shp[bdk_shp.omega.isna()].plot(ax=ax5, color="lightgrey")#hatch="//""
#ax5.axis('off')
ax5.set_ylim(-18.5, 0.25)
ax5.set_xlim(-82, -68.5)
ax5.grid(True)
ax5.set_title("Índice de aridez")

ax6.set_axisbelow(False)
ax6 = bdk_shp[bdk_shp.omega.notna()].plot("omega", cmap="jet", legend=True, linewidth=0.1, ax=ax6)
bdk_shp[bdk_shp.omega.isna()].plot(ax=ax6, color="lightgrey")#hatch="//""
#ax6.axis('off')
ax6.set_ylim(-18.5, 0.25)
ax6.set_xlim(-82, -68.5)
ax6.grid(True, zorder=2)
ax6.set_title(r'Omega - $\omega$')
plt.tight_layout()

fig3.savefig("./output/figures/06_Ai_Ei_Omega_spatial.png", bbox_inches='tight')
plt.close()


# omega hist and budyko curve with limits

fig5 = plt.figure(figsize=(8, 5))

ax9 = plt.subplot2grid((2, 3), (0, 0), colspan=3)
sns.scatterplot("Ai", "Ei", data=bdk_cal[bdk_cal.omega.notna()], hue="Nivel",
                s=80, palette=["red", "seagreen", "blue"], linewidth=0.1, ax=ax9)
ax9.plot(np.arange(0,1.1,.1), np.arange(0,1.1,.1), "black", linewidth=1.5)
ax9.plot(np.arange(1,601,1), np.repeat(1,600), "black", linewidth=1.5)
ax9.set_xlim(0, 6.5)#600
ax9.set_ylim(0, 1.1)
ax9.set_xlabel("Índice de aridez")
ax9.set_ylabel("Índice de evaporación")
handles, labels = ax9.get_legend_handles_labels()
ax9.legend(handles=handles[1:], labels=labels[1:], markerscale=1.5)

ax10 = plt.subplot2grid((2, 3), (1, 0), rowspan=2)
sns.distplot(bdk_cal.dropna(axis=0)[bdk_cal.Nivel == "Pacífico"].omega,
             kde=False, color="red", bins=5, hist_kws={"alpha": .8, "linewidth": 0.5}, ax=ax10)
ax10.plot([2.6, 2.6], [0, 20], "--", color="black")
ax10.set_xlim(0, 7)
ax10.set_ylim(0, 20)
ax10.set_xlabel(r'$\omega$')
ax10.set_ylabel("Frecuencia")


ax11 = plt.subplot2grid((2, 3), (1, 1), rowspan=2)
sns.distplot(bdk_cal.dropna(axis=0)[bdk_cal.Nivel == "Amazonas"].omega,
             kde=False,color="green", bins=15, hist_kws={"alpha": .8, "linewidth": 0.5}, ax=ax11)
ax11.plot([2.6, 2.6], [0, 20], "--", color="black")
ax11.set_xlim(0, 7)
ax11.set_ylim(0, 20)
ax11.set_xlabel(r'$\omega$')
ax11.set_ylabel("Frecuencia")

ax12 = plt.subplot2grid((2, 3), (1, 2), rowspan=2)
sns.distplot(bdk_cal.dropna(axis=0)[bdk_cal.Nivel == "Titicaca"].omega,
             kde=False,color="blue", bins=4, hist_kws={"alpha": .8, "linewidth": 0.5}, ax=ax12)
ax12.plot([2.6, 2.6], [0, 20], "--", color="black")
ax12.set_xlim(0, 7)
ax12.set_ylim(0, 20)
ax12.set_xlabel(r'$\omega$')
ax12.set_ylabel("Frecuencia")

plt.tight_layout()

fig5.savefig("./output/figures/07_Curve_and_omega.png", bbox_inches='tight', dpi=200)
plt.close()