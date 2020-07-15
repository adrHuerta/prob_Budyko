import pandas as pd
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.3, rc={"lines.linewidth": 1})

# results

shp = pd.read_pickle("./data/processed/SHP/UH.pkl")
val = pickle.load(open("./scripts/to_output/data_val.pkl", "rb"))

bdk_shp = shp.merge(val["Basin"], on='ID',  how='outer')
bdk_shp2 = shp.merge(val["Basin2"], on='ID',  how='outer')

"""
val = {"Peru":Ei_peru_scale,
       "Nivel":Ei_nivel_scale,
       "Basin":bdk_val}
"""
# predicted Ei at Peru and Nivel scale

fig14, ((ax15, ax16), (ax17, ax18)) = plt.subplots(2, 2, figsize=(8, 5))

sns.distplot(val["Peru"]["Ei_values"], kde=False, bins=15, ax=ax15)
ax15.set_xlim(0, 1)
ax15.set_ylim(0, 20)
ax15.set_title("Perú")
ax15.set_xlabel("AE/P predecido")
ax15.set_ylabel("Frecuencia")
ax15.scatter(x=val["Peru"]["Ei_values"].median(), y=2, color='r', marker="X", s=100)
ax15.scatter(x=val["Peru"]["Ei_median"].Ei, y=2, color='b', marker=".", s=100)

sns.distplot(val["Nivel"]["Ei_values_pac"], kde=False, bins=7, ax=ax16)
ax16.set_xlim(0, 1)
ax16.set_ylim(0, 20)
ax16.set_title("Pacífico")
ax16.set_xlabel("AE/P predecido")
ax16.set_ylabel("Frecuencia")
ax16.scatter(x=val["Nivel"]["Ei_values_pac"].median(), y=2, color='r', marker="X", s=100)
ax16.scatter(x=val["Nivel"]["Ei_median"].Ei.Pacífico, y=2, color='b', marker=".", s=100)

sns.distplot(val["Nivel"]["Ei_values_amz"], kde=False, bins=15, ax=ax17)
ax17.set_xlim(0, 1)
ax17.set_ylim(0, 20)
ax17.set_title("Amazonas")
ax17.set_xlabel("AE/P predecido")
ax17.set_ylabel("Frecuencia")
ax17.scatter(x=val["Nivel"]["Ei_values_amz"].median(), y=2, color='r', marker="X", s=100)
ax17.scatter(x=val["Nivel"]["Ei_median"].Ei.Amazonas, y=2, color='b', marker=".", s=100)

sns.distplot(val["Nivel"]["Ei_values_tit"], kde=False, bins=5, ax=ax18)
ax18.set_xlim(0, 1)
ax18.set_ylim(0, 20)
ax18.set_title("Titicaca")
ax18.set_xlabel("AE/P predecido")
ax18.set_ylabel("Frecuencia")
ax18.scatter(x=val["Nivel"]["Ei_values_tit"].median(), y=2, color='r', marker="X", s=100)
ax18.scatter(x=val["Nivel"]["Ei_median"].Ei.Titicaca, y=2, color='b', marker=".", s=100)

plt.tight_layout()

fig14.savefig("./output/figures/09_proBK_val.png", bbox_inches='tight', dpi=200)
plt.close()

# predicted Ei at basin scale with nivels

# mean, max and min error value at basin scale (abs because there are + and - values)
bdk_shp[bdk_shp.Ei.notna()].Ei.abs().mean()
bdk_shp[bdk_shp.Ei.notna()].Ei.max()
bdk_shp[bdk_shp.Ei.notna()].Ei.min()

plt.rc('grid', linestyle=":", color='black', alpha=.5)
fig13, ax14 = plt.subplots(figsize=(5,6))

cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["indianred","white","dodgerblue"])
cmap.set_under('darkred')

ax14 = bdk_shp[bdk_shp.Ei.notna()].plot("Ei", cmap=cmap, vmin=-30, vmax=30, legend=False, linewidth=0.1, ax=ax14)
bdk_shp[bdk_shp.Ei.isna()].plot(ax=ax14, color="lightgrey")
scatter = ax14.collections[0]
plt.colorbar(scatter, ax=ax14, extend='min')
#ax14.axis('off')
ax14.set_ylim(-18.5, 0.25)
ax14.set_xlim(-82, -68.5)
#ax14.grid(False)
#ax14.set_title("Error (%)")

fig13.savefig("./output/figures/10_proBK_basin_by_nivel.png", bbox_inches='tight', dpi=200)
plt.close()

# predicted Ei at basin scale without nivels

fig15, ax20 = plt.subplots(figsize=(5,6))

cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["indianred","white","dodgerblue"])
cmap.set_under('darkred')

ax20 = bdk_shp2[bdk_shp2.Ei.notna()].plot("Ei", cmap=cmap, vmin=-30, vmax=30, legend=False, linewidth=0.1, ax=ax20)
bdk_shp2[bdk_shp2.Ei.isna()].plot(ax=ax20, color="lightgrey")
scatter = ax20.collections[0]
plt.colorbar(scatter, ax=ax20, extend='min')
ax20.axis('off')
ax20.set_ylim(-18.5,0)
ax20.set_xlim(-81.3,-68.7)
ax20.grid(False)
#ax20.set_title("Error (%)")

fig15.savefig("./output/figures/11_proBK_basin.png", bbox_inches='tight')
plt.close()

# table of error

Data = {'PE/P': [val["Peru"]["Ei_median"].Ai, val["Nivel"]["Ei_median"].Ai.Pacífico,
                 val["Nivel"]["Ei_median"].Ai.Amazonas, val["Nivel"]["Ei_median"].Ai.Titicaca],
        'Observado (AE/P)': [val["Peru"]["Ei_median"].Ei, val["Nivel"]["Ei_median"].Ei.Pacífico,
                             val["Nivel"]["Ei_median"].Ei.Amazonas, val["Nivel"]["Ei_median"].Ei.Titicaca],
        'Proyectado_5': [val["Peru"]["Ei_values"].quantile(0.05), val["Nivel"]["Ei_values_pac"].quantile(0.05),
                         val["Nivel"]["Ei_values_amz"].quantile(0.05), val["Nivel"]["Ei_values_tit"].quantile(0.05)],
        'Proyectado_50': [val["Peru"]["Ei_values"].quantile(0.5), val["Nivel"]["Ei_values_pac"].quantile(0.5),
                         val["Nivel"]["Ei_values_amz"].quantile(0.5), val["Nivel"]["Ei_values_tit"].quantile(0.5)],
        'Proyectado_95': [val["Peru"]["Ei_values"].quantile(0.95), val["Nivel"]["Ei_values_pac"].quantile(0.95),
                         val["Nivel"]["Ei_values_amz"].quantile(0.95), val["Nivel"]["Ei_values_tit"].quantile(0.95)],
        'Error': [((val["Peru"]["Ei_median"].Ei - val["Peru"]["Ei_values"].quantile(0.5))/val["Peru"]["Ei_median"].Ei)*100,
                  ((val["Nivel"]["Ei_median"].Ei.Pacífico - val["Nivel"]["Ei_values_pac"].quantile(0.5))/val["Nivel"]["Ei_median"].Ei.Pacífico)*100,
                  ((val["Nivel"]["Ei_median"].Ei.Amazonas - val["Nivel"]["Ei_values_amz"].quantile(0.5))/val["Nivel"]["Ei_median"].Ei.Amazonas)*100,
                  ((val["Nivel"]["Ei_median"].Ei.Titicaca - val["Nivel"]["Ei_values_tit"].quantile(0.5))/val["Nivel"]["Ei_median"].Ei.Titicaca)*100]
        }

pd.DataFrame(Data, columns = ['PE/P', 'Observado (AE/P)',"Proyectado_5", "Proyectado_50", "Proyectado_95", "Error"],
             index=["Peru", "Pacífico", "Amazonas", "Titicaca"]).\
    to_csv("./output/tables/Table_of_bias.csv")