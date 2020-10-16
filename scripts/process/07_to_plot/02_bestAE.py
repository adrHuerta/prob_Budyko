import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from adjustText import adjust_text

sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.3, rc={"lines.linewidth": 1})

# results

resWB = pickle.load(open("./scripts/to_output/resWB.pkl", "rb"))
resBK = pickle.load(open("./scripts/to_output/resBK.pkl", "rb"))

# BUDYKO CURVE FOR ALL DATASET

df_WB = resWB["resDF"].groupby("Basin").mean()
df_WB["ET_BK"] = resBK["resBK"].groupby("Basin").mean().ET_BK
df_WB["Ei_WB"] = df_WB["ET_WB"]/df_WB["PP"]
df_WB["Ei_BK"] = df_WB["ET_BK"]/df_WB["PP"]
df_WB["Ai"] = df_WB["PET"]/df_WB["PP"]
df_WB["Basin"] = df_WB.index

df_ET_m = resWB["resDF"]
df_ET_m["Ei"] = df_ET_m["ET_m_values"]/df_ET_m["PP"]
df_ET_m["Ai"] = df_ET_m["PET"]/df_ET_m["PP"]


fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8)) = plt.subplots(2, 4, figsize=(8, 3), dpi=300, sharey=True, sharex=True)

def budyko_curve_plot(data, X, Y, title, ax):
    sns.scatterplot(X, Y, data=data, s=15, linewidth=0.5, color="skyblue", edgecolor="black", alpha=.75, ax=ax)
    ax.plot(np.arange(0,1.1,.1), np.arange(0,1.1,.1), "black", linewidth=1, alpha = .5)
    ax.plot(np.arange(1,12,1), np.repeat(1,11), "black", linewidth=1, alpha = .5)
    ax.set_xlim(0, 8.5)#600
    ax.set_ylim(0, 1.5)
    ax.set_title(title, color = "black", size = 10)
    ax.xaxis.set_tick_params(labelsize = 7, pad = -3)
    ax.yaxis.set_tick_params(labelsize = 7, pad = -3)
    ax.set_xlabel("")
    ax.set_ylabel("")
    texts = [ax.text(data[X].values[i], data[Y].values[i], data["Basin"].values[i], size = 4, fontweight='bold', alpha = .6) for i in range(len(df_WB["Basin"]))]
    adjust_text(texts, arrowprops={"arrowstyle":'-', "color":'red', "alpha":.75, "lw":.15}, expand_text=(2, 2), only_move={'objects': 'xy', 'points': 'xy', 'text': 'y'}, ax = ax)

budyko_curve_plot(data = df_WB, X = "Ai", Y = "Ei_WB", title = "Balance Hídrico", ax = ax1)
budyko_curve_plot(data = df_WB, X = "Ai", Y = "Ei_BK", title = "Budyko Determinístico", ax = ax2)
budyko_curve_plot(data = df_ET_m[df_ET_m["ET_m"] == "GLEAM"], X = "Ai", Y = "Ei", title = "GLEAM", ax = ax3)
budyko_curve_plot(data = df_ET_m[df_ET_m["ET_m"] == "MODIS16"], X = "Ai", Y = "Ei", title = "MODIS16", ax = ax4)
budyko_curve_plot(data = df_ET_m[df_ET_m["ET_m"] == "PROMEDIO"], X = "Ai", Y = "Ei", title = "PROMEDIO", ax = ax5)
budyko_curve_plot(data = df_ET_m[df_ET_m["ET_m"] == "SSEBop"], X = "Ai", Y = "Ei", title = "SSEBop", ax = ax6)
budyko_curve_plot(data = df_ET_m[df_ET_m["ET_m"] == "TerraClimate"], X = "Ai", Y = "Ei", title = "TerraClimate", ax = ax7)
budyko_curve_plot(data = df_ET_m[df_ET_m["ET_m"] == "P-LSH"], X = "Ai", Y = "Ei", title = "P-LSH", ax = ax8)

fig.text(0.5, 0.03, 'Índice de aridez', ha='center', size = 8)
fig.text(0.08, 0.5, 'Índice de evaporación', va='center', rotation='vertical', size = 8)

plt.savefig("./output/figures/04_05_curve_all_data.png",
            pad_inches = 0,  bbox_inches='tight')
plt.close()

# BIAS BY BASIN AND MODEL

resBIAS_WB = pd.pivot_table(resWB["resDF"], values="BIAS", index=["Basin"], columns=["ET_m"])
resBIAS_BK = pd.pivot_table(resBK["resBK"], values="BIAS", index=["Basin"], columns=["ET_m"])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8))

ax1 = sns.heatmap(resBIAS_WB, vmax=180, vmin=-180, cmap="PiYG", ax=ax1)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0)
ax1.set_title("Balance Hidrico", fontsize=15)
ax1.set_ylabel("")
ax1.set_xlabel("")

ax2 = sns.heatmap(resBIAS_BK, vmax=180, vmin=-180, cmap="PiYG", ax=ax2)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
ax2.set_title("Budyko", fontsize=15)
ax2.set_ylabel("")
ax2.set_xlabel("")

plt.tight_layout()

fig.savefig("./output/figures/04_BIAS_by_basin.png", bbox_inches='tight', dpi = 200)
plt.close()

# WHICH PRODUCT IS THE BEST: RANKING

res_RRMSE = pd.concat([resWB["rWB"], resBK["rWB"],
                       resWB["rRMSE"], resBK["rRMSE"],
                       resBIAS_WB.apply(lambda x: x.median(), axis=0), resBIAS_BK.apply(lambda x: x.median(), axis=0)],
                      axis=1)
res_RRMSE.columns = ["r_BH", "r_BK", "RMSE_BH", "RMSE_BK", "BIAS_BH", "BIAS_BK"]

res_RRMSE.round(2).to_csv("./output/tables/Table_r_rmse_bias_by_AEproduct.csv")

rank = [pd.Series(res_RRMSE.sort_values(by="r_BH", ascending=False).index),
        pd.Series(res_RRMSE.sort_values(by="r_BK", ascending=False).index),
        pd.Series(res_RRMSE.sort_values(by="RMSE_BH", ascending=True).index),
        pd.Series(res_RRMSE.sort_values(by="RMSE_BK", ascending=True).index),
        pd.Series(res_RRMSE.BIAS_BH.abs().sort_values().index),
        pd.Series(res_RRMSE.BIAS_BK.abs().sort_values().index)]
rank = pd.concat(rank, axis=1)
rank.apply(lambda x: x.mode(), axis=1)

