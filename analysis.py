"""
Energy Consumption of Old vs. Modern Appliances — Refrigerator case study
Group 1 · Descriptive Statistics · Universidad Europea · 2026

This single script:
  1. Downloads the ENERGY STAR certified refrigerators dataset (U.S. EPA).
  2. Cleans it and defines "Older" (certified 2014-2017) vs "Modern" (2023-2026).
  3. Computes univariate + bivariate descriptive statistics.
  4. Runs statistical inference (CI, one-sample t, two-sample Welch t,
     Mann-Whitney U).
  5. Saves all figures into ./figures/.

Requirements: pandas, numpy, scipy, matplotlib, requests
    pip install pandas numpy scipy matplotlib requests
"""

import os
import io
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# ---------------------------------------------------------------------------
# 0. Setup
# ---------------------------------------------------------------------------
DATA_URL = "https://data.energystar.gov/api/views/p5st-her9/rows.csv?format=true"
CSV_PATH = "energystar_fridges.csv"
FIG_DIR  = "figures"
os.makedirs(FIG_DIR, exist_ok=True)
plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 140, "font.size": 10})

# ---------------------------------------------------------------------------
# 1. Download data (only once)
# ---------------------------------------------------------------------------
if not os.path.exists(CSV_PATH):
    print("Downloading ENERGY STAR dataset ...")
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
    "US Federal Standard (kWh/yr)",
    "Percent Less Energy Use than US Federal Standard",
    "Capacity (Total Volume) (ft3)",
    "Adjusted Volume (ft3)",
    "Height (in)",
    "Width (in)",
]
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df["Date Certified"] = pd.to_datetime(df["Date Certified"], errors="coerce")
df["YearCert"] = df["Date Certified"].dt.year

def era(y):
    if y <= 2017:  return "Older (2014-2017)"
    if y >= 2023:  return "Modern (2023-2026)"
    return "Mid"

df["Era"] = df["YearCert"].apply(era)

sub = (df[df["Era"] != "Mid"]
         .dropna(subset=["Annual Energy Use (kWh/yr)",
                         "Capacity (Total Volume) (ft3)"])
         .copy())

older  = sub[sub["Era"] == "Older (2014-2017)"]
modern = sub[sub["Era"] == "Modern (2023-2026)"]
older_e  = older["Annual Energy Use (kWh/yr)"]
modern_e = modern["Annual Energy Use (kWh/yr)"]

# ---------------------------------------------------------------------------
# 3. Univariate descriptive stats
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

describe(older_e,  "Older  (2014-2017)")
describe(modern_e, "Modern (2023-2026)")

# ---------------------------------------------------------------------------
# 4. Bivariate descriptive stats
# ---------------------------------------------------------------------------
m_num = modern[["Annual Energy Use (kWh/yr)",
                "Capacity (Total Volume) (ft3)",
                "Adjusted Volume (ft3)",
                "US Federal Standard (kWh/yr)",
                "Percent Less Energy Use than US Federal Standard"]].dropna()

print("\nPearson correlation matrix (modern cohort):")
print(m_num.corr().round(3))

cov_ec = np.cov(m_num["Annual Energy Use (kWh/yr)"],
                m_num["Capacity (Total Volume) (ft3)"])[0, 1]
print(f"\nCov(Energy, Capacity) = {cov_ec:.2f}")

slope, intercept, r, p, se = stats.linregress(
    m_num["Capacity (Total Volume) (ft3)"],
    m_num["Annual Energy Use (kWh/yr)"])
print(f"OLS: Energy = {intercept:.2f} + {slope:.2f}*Capacity  "
      f"r={r:.3f}  R2={r**2:.3f}  p={p:.2e}")

# ---------------------------------------------------------------------------
# 5. Inference
# ---------------------------------------------------------------------------
# 5.1 CI for modern mean
ci95 = stats.t.interval(0.95, len(modern_e) - 1,
                        loc=modern_e.mean(), scale=stats.sem(modern_e))
print(f"\n95% CI for modern mean: [{ci95[0]:.2f}, {ci95[1]:.2f}]")

# 5.2 One-sample vs 1981 AHAM baseline (1278 kWh/yr)
t1, p1 = stats.ttest_1samp(modern_e, 1278, alternative="less")
print(f"One-sample t vs 1278: t={t1:.2f}, p={p1:.2e}")

# 5.3 Two-sample Welch, one-sided: older > modern
t2, p2 = stats.ttest_ind(older_e, modern_e,
                         equal_var=False, alternative="greater")
diff   = older_e.mean() - modern_e.mean()
se_d   = np.sqrt(older_e.var(ddof=1)/len(older_e)
               + modern_e.var(ddof=1)/len(modern_e))
df_w   = (older_e.var(ddof=1)/len(older_e)
         + modern_e.var(ddof=1)/len(modern_e))**2 / (
         (older_e.var(ddof=1)/len(older_e))**2/(len(older_e)-1)
       + (modern_e.var(ddof=1)/len(modern_e))**2/(len(modern_e)-1))
ci_d   = stats.t.interval(0.95, df_w, loc=diff, scale=se_d)
pooled = np.sqrt(((len(older_e)-1)*older_e.var(ddof=1)
                + (len(modern_e)-1)*modern_e.var(ddof=1))
               / (len(older_e) + len(modern_e) - 2))
d_cohen = diff / pooled
print(f"Welch t: t={t2:.3f}  p(one-sided)={p2:.2e}  "
      f"diff={diff:.2f}  95%CI=[{ci_d[0]:.2f},{ci_d[1]:.2f}]  "
      f"d={d_cohen:.3f}")

u, pu = stats.mannwhitneyu(older_e, modern_e, alternative="greater")
print(f"Mann-Whitney U={u:.0f}  p={pu:.2e}")

# ---------------------------------------------------------------------------
# 6. Figures
# ---------------------------------------------------------------------------

# Fig 1 — histogram of modern energy use
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.hist(modern_e, bins=40, color="#2E86AB", edgecolor="white", alpha=0.85)
ax.axvline(modern_e.mean(),   color="red",    ls="--",
           label=f"Mean = {modern_e.mean():.0f}")
ax.axvline(modern_e.median(), color="orange", ls="--",
           label=f"Median = {modern_e.median():.0f}")
ax.set(xlabel="Annual Energy Use (kWh/yr)", ylabel="Frequency",
       title="Fig.1 — Modern ENERGY STAR fridges (2023-2026)")
ax.legend(); plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig1_hist_modern.png"); plt.close()

# Fig 2 — boxplot by era
fig, ax = plt.subplots(figsize=(7, 4.2))
bp = ax.boxplot([older_e, modern_e],
                tick_labels=[f"Older (2014-2017)\nn={len(older_e)}",
                             f"Modern (2023-2026)\nn={len(modern_e)}"],
                patch_artist=True, showmeans=True)
for patch, col in zip(bp["boxes"], ["#E07A5F", "#81B29A"]):
    patch.set_facecolor(col)
ax.set(ylabel="Annual Energy Use (kWh/yr)",
       title="Fig.2 — Annual Energy Use by Era")
plt.tight_layout(); plt.savefig(f"{FIG_DIR}/fig2_box_era.png"); plt.close()

# Fig 3 — scatter Capacity vs Energy with regression line
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.scatter(m_num["Capacity (Total Volume) (ft3)"],
           m_num["Annual Energy Use (kWh/yr)"],
           alpha=0.25, s=12, color="#3D405B")
xs = np.linspace(m_num["Capacity (Total Volume) (ft3)"].min(),
                 m_num["Capacity (Total Volume) (ft3)"].max(), 100)
ax.plot(xs, intercept + slope*xs, color="red", lw=2,
        label=f"y = {intercept:.1f} + {slope:.2f}x  r={r:.3f}")
ax.set(xlabel="Capacity (ft³)", ylabel="Annual Energy Use (kWh/yr)",
       title="Fig.3 — Capacity vs Energy (modern)")
ax.legend(); plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig3_scatter_cap_energy.png"); plt.close()

# Fig 4 — mean energy by certification year (95% CI)
agg = (df.groupby("YearCert")["Annual Energy Use (kWh/yr)"]
         .agg(["mean", "std", "count"]).dropna())
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.errorbar(agg.index, agg["mean"],
            yerr=agg["std"]/np.sqrt(agg["count"])*1.96,
            marker="o", color="#2E86AB", capsize=3)
ax.set(xlabel="Year of ENERGY STAR Certification",
       ylabel="Mean Annual Energy Use (kWh/yr)",
       title="Fig.4 — Trend of Mean Energy Use (95% CI)")
ax.grid(alpha=0.3); plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig4_trend_year.png"); plt.close()

# Fig 5 — 50-year historical trend (AHAM/DOE + our sample)
hist_years = [1972, 1981, 1990, 1994, 2000, 2009, 2013]
hist_kwh   = [2000, 1278,  900,  670,  650,  450,  444]
our_years  = [2023, 2025]
our_kwh    = [df[df["YearCert"] == y]["Annual Energy Use (kWh/yr)"].mean()
              for y in our_years]
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.plot(hist_years, hist_kwh, "o-", color="#E07A5F",
        lw=2, ms=8, label="AHAM / DOE historical")
ax.plot(our_years, our_kwh, "s-", color="#2E86AB",
        lw=2, ms=9, label="ENERGY STAR (our sample)")
for x, y in zip(hist_years + our_years, hist_kwh + our_kwh):
    ax.annotate(f"{y:.0f}", (x, y), xytext=(5, 8),
                textcoords="offset points", fontsize=8)
ax.set(xlabel="Year", ylabel="Average Annual Energy Use (kWh/yr)",
       title="Fig.5 — 50-year trend")
ax.grid(alpha=0.3); ax.legend(); plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig5_history.png"); plt.close()

# Fig 6 — density: older vs modern
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.hist(older_e,  bins=30, color="#E07A5F", alpha=0.55,
        density=True, label="Older (2014-2017)")
ax.hist(modern_e, bins=30, color="#81B29A", alpha=0.55,
        density=True, label="Modern (2023-2026)")
ax.set(xlabel="Annual Energy Use (kWh/yr)", ylabel="Density",
       title="Fig.6 — Energy distribution: older vs modern")
ax.legend(); plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig6_density.png"); plt.close()

# Fig 7 — % less energy than federal standard (modern)
pct = pd.to_numeric(modern["Percent Less Energy Use than US Federal Standard"],
                    errors="coerce").dropna()
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.hist(pct, bins=40, color="#6A994E", edgecolor="white")
ax.axvline(pct.mean(), color="red", ls="--",
           label=f"Mean = {pct.mean():.1f}%")
ax.set(xlabel="% less energy than U.S. Federal Standard",
       ylabel="Frequency",
       title="Fig.7 — Efficiency margin of modern fridges")
ax.legend(); plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig7_pctless.png"); plt.close()

print("\nAll figures written to", FIG_DIR)
