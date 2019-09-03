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
      'NOMBRE', 'ORDEN', 'Shape_Leng', 'Shape_Area',
      'min_x', 'max_x', 'min_y', 'max_y'], axis=1)

shp.to_pickle("./data/processed/SHP/UH.pkl")


shdf = salem.read_shapefile("./data/raw/SHP/vertientes.shp").\
    to_crs({"init": "epsg:4326"})

shdf.plot()

shdf.to_pickle("./data/processed/SHP/sph_ver.pkl")