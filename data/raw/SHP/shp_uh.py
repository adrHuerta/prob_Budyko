import salem

shp = "./data/raw/SHP/UH.shp"

shp = salem.read_shapefile(shp).\
    to_crs({"init": "epsg:4326"}).\
    sort_values("ID")

shp["NIVEL1"] = shp["NIVEL1"].apply(lambda x: int(x))
shp["Nivel"] = shp["NIVEL1"].apply(lambda x: "Titicaca" if x == 0.0 else "Pacífico" if x == 1.0 else "Amazonas")
shp = shp[(shp.NOMBRE != "Lago Titicaca")]
shp.groupby("Nivel").count()

shp = shp.drop(['NIVEL1',"AREA_KM2",'OBJECTID', 'NOMB_UH_N1',
      'NIVEL2', 'NIVEL3', 'NIVEL4', 'NIVEL5',
      'NIVEL6', 'NIVEL7','NOMB_UH_N2', 'NOMB_UH_N3',
      'NOMB_UH_N4', 'NOMB_UH_N5', 'NOMB_UH_N6', 'NOMB_UH_N7', 'CODIGO',
      'ORDEN', 'Shape_Leng', 'Shape_Area',
      'min_x', 'max_x', 'min_y', 'max_y'], axis=1)

shp.to_pickle("./data/processed/SHP/UH.pkl")


shdf = salem.read_shapefile("./data/raw/SHP/vertientes.shp").\
    to_crs({"init": "epsg:4326"})
shdf.to_pickle("./data/processed/SHP/sph_ver.pkl")


## figure

import matplotlib as mpl
import matplotlib.pyplot as plt
plt.rc('grid', linestyle=":", color='black', alpha=.5)

cmap = mpl.colors.ListedColormap(["green", "red", "blue"])

fig, ax22 = plt.subplots(figsize=(6, 8))

ax = shp.plot("Nivel", ax=ax22, cmap=cmap, legend=True, linewidth=0.8, edgecolor='black')
leg = ax.get_legend()
leg.set_bbox_to_anchor((.0, .0, .4, .2))
leg.get_frame().set_edgecolor('white')
for i in range(3):
    leg.get_texts()[i].set_text(["Amazonas (84)", "Pacífico (127)", "Titicaca (18)"][i])
ax22.set_ylim(-18.5, 0.25)
ax22.set_xlim(-82, -68.5)
ax22.grid(True)

fig.savefig("./output/figures/00_vertientes.png", bbox_inches='tight', dpi=200)
plt.close()