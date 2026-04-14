"""
Energy Consumption of Old vs. Modern Appliances — Clothes Washers
Group 1 · Descriptive Statistics · Universidad Europea · 2026

Downloads the ENERGY STAR Certified Residential Clothes Washers dataset,
cleans it, defines "Older" (available on market <= 2017) vs "Modern"
(available on market >= 2022), and runs the full descriptive + inferential
analysis. All figures are written to ./figures/.

Requirements: pandas, numpy, scipy, matplotlib, requests
"""

import os
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# ---------------------------------------------------------------------------
# 0. Setup
# ---------------------------------------------------------------------------
DATA_URL = "https://data.energystar.gov/api/views/bghd-e2wd/rows.csv?accessType=DOWNLOAD"
CSV_PATH = "energystar_washers.csv"
FIG_DIR  = "figures"
os.makedirs(FIG_DIR, exist_ok=True)
plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 140, "font.size": 10})

# ---------------------------------------------------------------------------
# 1. Download data (only once)
# ---------------------------------------------------------------------------
if not os.path.exists(CSV_PATH):
    print("Downloading ENERGY STAR clothes washers dataset ...")
    r = requests.get(DATA_URL, timeout=60)
    r.raise_for_status()
    with open(CSV_PATH, "wb") as f:
        f.write(r.content)

df = pd.read_csv(CSV_PATH)
print(f"Raw dataset: {df.shape[0]} rows, {df.shape[1]} columns")

# ---------------------------------------------------------------------------
# 2. Cleaning & feature engineering
# ---------------------------------------------------------------------------
num_cols = [
    "Annual Energy Use (kWh/yr)",
    "Volume (cu. ft.)",
    "Integrated Modified Energy Factor (IMEF)",
    "Integrated Water Factor (IWF)",
    "Annual Water Use (gallons/yr)",
]
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df["Date Available On Market"] = pd.to_datetime(df["Date Available On Market"], errors="coerce")
df["YearAvail"] = df["Date Available On Market"].dt.year

# keep residential, drop combo all-in-one
df = df[df["Intended Market"] == "Residential"].copy()
df = df[df["Special Type"] != "Combination All-in-One Washer/Dryer"].copy()
df = df.dropna(subset=["Annual Energy Use (kWh/yr)", "Volume (cu. ft.)", "YearAvail"])
print(f"Cleaned: {df.shape[0]} residential washers, years "
      f"{int(df['YearAvail'].min())}-{int(df['YearAvail'].max())}")

def era(y):
    if y <= 2017:  return "Older (<=2017)"
    if y >= 2022:  return "Modern (>=2022)"
    return "Mid"

df["Group"] = df["YearAvail"].apply(era)
older  = df[df["Group"] == "Older (<=2017)"]
modern = df[df["Group"] == "Modern (>=2022)"]
older_e  = older["Annual Energy Use (kWh/yr)"]
modern_e = modern["Annual Energy Use (kWh/yr)"]
print(f"Older n={len(older_e)}, Modern n={len(modern_e)}")

# ---------------------------------------------------------------------------
# 3. Univariate descriptive statistics
# ---------------------------------------------------------------------------
def describe(x, name):
    print(f"\n--- {name}  (n={len(x)}) ---")
    print(f"  mean   = {x.mean():.2f}")
    print(f"  median = {x.median():.2f}")
    print(f"  std    = {x.std(ddof=1):.2f}")
    print(f"  var    = {x.var(ddof=1):.2f}")
    print(f"  IQR    = {np.percentile(x,75) - np.percentile(x,25):.2f}")
    print(f"  CV     = {x.std()/x.mean():.3f}")
    print(f"  skew   = {stats.skew(x):.3f}")
    print(f"  kurt   = {stats.kurtosis(x):.3f}")
    print(f"  min/max= {x.min():.0f} / {x.max():.0f}")

describe(df["Annual Energy Use (kWh/yr)"], "All washers — Annual Energy")
describe(older_e, "Older — Annual Energy")
describe(modern_e, "Modern — Annual Energy")

# ---------------------------------------------------------------------------
# 4. Bivariate descriptive statistics
# ---------------------------------------------------------------------------
num_sub = df[["Annual Energy Use (kWh/yr)",
              "Volume (cu. ft.)",
              "Integrated Modified Energy Factor (IMEF)",
              "Integrated Water Factor (IWF)",
              "Annual Water Use (gallons/yr)"]]
print("\nPearson correlation matrix:")
print(num_sub.corr().round(3))
print("\nSpearman correlation matrix:")
print(num_sub.corr(method="spearman").round(3))

slope, intercept, r, p, se = stats.linregress(df["Volume (cu. ft.)"],
                                              df["Annual Energy Use (kWh/yr)"])
print(f"\nRegression Energy ~ Volume: Energy = {intercept:.2f} + "
      f"{slope:.2f}*Volume  r={r:.3f}  R2={r**2:.3f}  p={p:.2e}")

# ---------------------------------------------------------------------------
# 5. Inference & hypothesis tests
# ---------------------------------------------------------------------------
# CI for modern mean
ci95 = stats.t.interval(0.95, len(modern_e) - 1,
                        loc=modern_e.mean(), scale=stats.sem(modern_e))
print(f"\n95% CI for modern mean energy: [{ci95[0]:.2f}, {ci95[1]:.2f}]")

# Welch's t (one-sided: older > modern)
t, p_w = stats.ttest_ind(older_e, modern_e,
                         equal_var=False, alternative="greater")
diff = older_e.mean() - modern_e.mean()
se_d = np.sqrt(older_e.var(ddof=1)/len(older_e)
             + modern_e.var(ddof=1)/len(modern_e))
dfW  = (older_e.var(ddof=1)/len(older_e)
       + modern_e.var(ddof=1)/len(modern_e))**2 / (
       (older_e.var(ddof=1)/len(older_e))**2/(len(older_e)-1)
     + (modern_e.var(ddof=1)/len(modern_e))**2/(len(modern_e)-1))
ci_d = stats.t.interval(0.95, dfW, loc=diff, scale=se_d)
pooled = np.sqrt(((len(older_e)-1)*older_e.var(ddof=1)
                + (len(modern_e)-1)*modern_e.var(ddof=1))
               / (len(older_e) + len(modern_e) - 2))
d_cohen = diff / pooled
print(f"\nWelch's t (Older>Modern): t={t:.3f}  df={dfW:.1f}  "
      f"p(one-sided)={p_w:.4g}")
print(f"  diff={diff:.2f}  95% CI=[{ci_d[0]:.2f},{ci_d[1]:.2f}]  "
      f"Cohen d={d_cohen:.3f}")
u, p_u = stats.mannwhitneyu(older_e, modern_e, alternative="greater")
print(f"  Mann-Whitney U={u:.0f}  p={p_u:.4g}")

# Front vs Top load
fl = df[df["Load Configuration"] == "Front Load"]["Annual Energy Use (kWh/yr)"]
tl = df[df["Load Configuration"] == "Top Load"]["Annual Energy Use (kWh/yr)"]
t_fl, p_fl = stats.ttest_ind(tl, fl, equal_var=False)
print(f"\nFront vs Top Load: Front n={len(fl)} mean={fl.mean():.1f}, "
      f"Top n={len(tl)} mean={tl.mean():.1f}, "
      f"t={t_fl:.2f}  p={p_fl:.3e}")

# ---------------------------------------------------------------------------
# 6. Figures
# ---------------------------------------------------------------------------
# Fig 1 — histogram all models
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.hist(df["Annual Energy Use (kWh/yr)"], bins=30, color="#2E86AB",
        edgecolor="white", alpha=0.85)
ax.axvline(df["Annual Energy Use (kWh/yr)"].mean(), color="red", ls="--",
           label=f"Mean = {df['Annual Energy Use (kWh/yr)'].mean():.0f}")
ax.axvline(df["Annual Energy Use (kWh/yr)"].median(), color="orange", ls="--",
           label=f"Median = {df['Annual Energy Use (kWh/yr)'].median():.0f}")
ax.set(xlabel="Annual Energy Use (kWh/yr)", ylabel="Frequency",
       title="Fig.1 — Annual Energy Use (all 351 residential washers)")
ax.legend(); plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig1_hist_all.png"); plt.close()

# Fig 2 — boxplot overall
fig, ax = plt.subplots(figsize=(5, 4.2))
bp = ax.boxplot(df["Annual Energy Use (kWh/yr)"], patch_artist=True,
                showmeans=True, tick_labels=["All washers"])
bp["boxes"][0].set_facecolor("#2E86AB")
ax.set(ylabel="Annual Energy Use (kWh/yr)",
       title="Fig.2 — Boxplot of Annual Energy Use")
plt.tight_layout(); plt.savefig(f"{FIG_DIR}/fig2_box_all.png"); plt.close()

# Fig 3 — histogram of volume
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.hist(df["Volume (cu. ft.)"], bins=20, color="#81B29A", edgecolor="white")
ax.set(xlabel="Drum Volume (cu. ft.)", ylabel="Frequency",
       title="Fig.3 — Drum Volume distribution")
plt.tight_layout(); plt.savefig(f"{FIG_DIR}/fig3_hist_volume.png"); plt.close()

# Fig 4 — bar chart Load Configuration
fig, ax = plt.subplots(figsize=(5, 4.2))
cnt = df["Load Configuration"].value_counts()
ax.bar(cnt.index, cnt.values, color=["#3D405B", "#E07A5F"])
for i, v in enumerate(cnt.values):
    ax.text(i, v + 3, str(v), ha="center")
ax.set(ylabel="Number of models",
       title="Fig.4 — Load Configuration")
plt.tight_layout(); plt.savefig(f"{FIG_DIR}/fig4_bar_load.png"); plt.close()

# Fig 5 — density by era
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.hist(older_e, bins=20, color="#E07A5F", alpha=0.55, density=True,
        label=f"Older (n={len(older_e)})")
ax.hist(modern_e, bins=20, color="#81B29A", alpha=0.55, density=True,
        label=f"Modern (n={len(modern_e)})")
ax.set(xlabel="Annual Energy Use (kWh/yr)", ylabel="Density",
       title="Fig.5 — Density: Older vs Modern washers")
ax.legend(); plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig5_density_era.png"); plt.close()

# Fig 6 — boxplot by era
fig, ax = plt.subplots(figsize=(6.5, 4.2))
bp = ax.boxplot([older_e, modern_e],
                tick_labels=[f"Older\nn={len(older_e)}",
                             f"Modern\nn={len(modern_e)}"],
                patch_artist=True, showmeans=True)
for patch, col in zip(bp["boxes"], ["#E07A5F", "#81B29A"]):
    patch.set_facecolor(col)
ax.set(ylabel="Annual Energy Use (kWh/yr)",
       title="Fig.6 — Annual Energy Use by Era")
plt.tight_layout(); plt.savefig(f"{FIG_DIR}/fig6_box_era.png"); plt.close()

# Fig 7 — scatter Energy vs Volume coloured by Load Config
fig, ax = plt.subplots(figsize=(7, 4.5))
for cfg, col in zip(["Front Load", "Top Load"], ["#3D405B", "#E07A5F"]):
    sub = df[df["Load Configuration"] == cfg]
    ax.scatter(sub["Volume (cu. ft.)"], sub["Annual Energy Use (kWh/yr)"],
               alpha=0.55, s=22, color=col, label=cfg)
xs = np.linspace(df["Volume (cu. ft.)"].min(),
                 df["Volume (cu. ft.)"].max(), 100)
ax.plot(xs, intercept + slope*xs, color="black", ls="--", lw=1.5,
        label=f"OLS  y={intercept:.1f}+{slope:.1f}x  r={r:.2f}")
ax.set(xlabel="Drum Volume (cu. ft.)",
       ylabel="Annual Energy Use (kWh/yr)",
       title="Fig.7 — Energy vs Volume by Load Configuration")
ax.legend(); plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig7_scatter_vol_load.png"); plt.close()

# Fig 8 — IMEF vs Energy
fig, ax = plt.subplots(figsize=(7, 4.5))
imef_df = df.dropna(subset=["Integrated Modified Energy Factor (IMEF)"])
ax.scatter(imef_df["Integrated Modified Energy Factor (IMEF)"],
           imef_df["Annual Energy Use (kWh/yr)"],
           alpha=0.5, s=22, color="#6A994E")
r_im = imef_df["Integrated Modified Energy Factor (IMEF)"].corr(
       imef_df["Annual Energy Use (kWh/yr)"])
ax.set(xlabel="Integrated Modified Energy Factor (IMEF)",
       ylabel="Annual Energy Use (kWh/yr)",
       title=f"Fig.8 — IMEF vs Annual Energy (r = {r_im:.2f})")
plt.tight_layout(); plt.savefig(f"{FIG_DIR}/fig8_imef_energy.png"); plt.close()

# Fig 9 — Annual Water vs Annual Energy
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.scatter(df["Annual Water Use (gallons/yr)"],
           df["Annual Energy Use (kWh/yr)"],
           alpha=0.5, s=22, color="#2E86AB")
r_w = df["Annual Water Use (gallons/yr)"].corr(
       df["Annual Energy Use (kWh/yr)"])
ax.set(xlabel="Annual Water Use (gallons/yr)",
       ylabel="Annual Energy Use (kWh/yr)",
       title=f"Fig.9 — Water vs Energy (r = {r_w:.2f})")
plt.tight_layout(); plt.savefig(f"{FIG_DIR}/fig9_water_energy.png"); plt.close()

# Fig 10 — trend by year of availability (mean + 95% CI)
agg = (df.groupby("YearAvail")["Annual Energy Use (kWh/yr)"]
         .agg(["mean", "std", "count"]).dropna())
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.errorbar(agg.index, agg["mean"],
            yerr=agg["std"]/np.sqrt(agg["count"])*1.96,
            marker="o", color="#2E86AB", capsize=3)
ax.set(xlabel="Year of Market Availability",
       ylabel="Mean Annual Energy Use (kWh/yr)",
       title="Fig.10 — Mean Energy Use by Market Year (95% CI)")
ax.grid(alpha=0.3); plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig10_trend_year.png"); plt.close()

print("\nAll figures written to", FIG_DIR)
