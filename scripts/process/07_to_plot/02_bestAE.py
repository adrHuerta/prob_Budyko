import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.3, rc={"lines.linewidth": 1})

# results

resWB = pickle.load(open("./scripts/to_output/resWB.pkl", "rb"))
resBK = pickle.load(open("./scripts/to_output/resBK.pkl", "rb"))

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

fig.savefig("./output/figures/04_BIAS_by_basin.png", bbox_inches='tight')
plt.close()

# WHICH PRODUCT IS THE BEST: RANKING

res_RRMSE = pd.concat([resWB["rWB"], resBK["rWB"],
                       resWB["rRMSE"], resBK["rRMSE"],
                       resBIAS_WB.apply(lambda x: x.median(), axis=0), resBIAS_BK.apply(lambda x: x.median(), axis=0)],
                      axis=1)
res_RRMSE.columns = ["r_BH", "r_BK", "RMSE_BH", "RMSE_BK", "BIAS_BH", "BIAS_BK"]

res_RRMSE.to_csv("./output/tables/Table_r_rmse_bias_by_AEproduct.csv")

rank = [pd.Series(res_RRMSE.sort_values(by="r_BH", ascending=False).index),
        pd.Series(res_RRMSE.sort_values(by="r_BK", ascending=False).index),
        pd.Series(res_RRMSE.sort_values(by="RMSE_BH", ascending=True).index),
        pd.Series(res_RRMSE.sort_values(by="RMSE_BK", ascending=True).index),
        pd.Series(res_RRMSE.BIAS_BH.abs().sort_values().index),
        pd.Series(res_RRMSE.BIAS_BK.abs().sort_values().index)]
rank = pd.concat(rank, axis=1)
rank.apply(lambda x: x.mode(), axis=1)
"""
by hand: GLEAM:3, MEAN:8, MODIS16:12, TerraClimate:14, Zhang:20, SSEBop:28 
"""