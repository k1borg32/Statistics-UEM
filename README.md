# Energy Consumption of Old vs. Modern Appliances

> **Applied Statistics · Group 1 · Universidad Europea · 2026**
> Topic: *Energy consumption of old vs. modern appliances.*
> Hypothesis: *"Modern appliances consume less energy than older ones."*

This repository contains **two independent case studies** that test the same
hypothesis on two different appliance categories, both sourced from the
U.S. EPA **ENERGY STAR** open-data catalogue:

| # | Appliance | Sample size | Report | Presentation | Code |
|---|-----------|------------:|--------|--------------|------|
| 1 | **Refrigerators** | 4 591 models (2014-2026) + historical 1972-2013 | [refrigerators/REPORT.md](refrigerators/REPORT.md) | [refrigerators/PRESENTATION.md](refrigerators/PRESENTATION.md) | [refrigerators/analysis.py](refrigerators/analysis.py) |
| 2 | **Residential Clothes Washers** | 351 models (2014-2026) | [washers/REPORT.md](washers/REPORT.md) | [washers/PRESENTATION.md](washers/PRESENTATION.md) | [washers/analysis.py](washers/analysis.py) |

Both studies reach the same headline conclusion: **modern appliances do consume
significantly less energy than older ones**, with effect sizes and p-values
reported inside each report.

---

## Repository layout

```
STATISTICS/
├── README.md                     ← this file
├── requirements.txt              ← Python dependencies for both studies
│
├── refrigerators/                ← Study 1 — Refrigerators
│   ├── REPORT.md                 ← full written report
│   ├── PRESENTATION.md           ← 10-slide in-class deck
│   ├── analysis.py               ← reproducible script (downloads data + figures)
│   ├── energystar_fridges.csv    ← raw data (EPA ENERGY STAR, p5st-her9)
│   ├── subset.csv                ← cleaned Older vs Modern sub-sample
│   └── figures/                  ← 7 PNG charts (Fig. 1 – Fig. 7)
│       ├── fig1_hist_modern.png
│       ├── fig2_box_era.png
│       ├── fig3_scatter_cap_energy.png
│       ├── fig4_trend_year.png
│       ├── fig5_history.png
│       ├── fig6_density.png
│       └── fig7_pctless.png
│
└── washers/                      ← Study 2 — Clothes Washers
    ├── REPORT.md                 ← full written report
    ├── PRESENTATION.md           ← 12-slide in-class deck
    ├── analysis.py               ← reproducible script (downloads data + figures)
    ├── energystar_washers.csv    ← raw data (EPA ENERGY STAR, bghd-e2wd)
    └── figures/                  ← 10 PNG charts (Fig. 1 – Fig. 10)
        ├── fig1_hist_all.png
        ├── fig2_box_all.png
        ├── fig3_hist_volume.png
        ├── fig4_bar_load.png
        ├── fig5_density_era.png
        ├── fig6_box_era.png
        ├── fig7_scatter_vol_load.png
        ├── fig8_imef_energy.png
        ├── fig9_water_energy.png
        └── fig10_trend_year.png
```

---

## Quick results at a glance

### Refrigerators
* Modern (2023-2026) mean **390 kWh/yr** vs older (2014-2017) mean **433 kWh/yr**.
* Welch's one-sided t = 4.86, **p = 7.5 × 10⁻⁷** → reject H₀.
* Compared to the 1981 AHAM baseline of 1 278 kWh/yr → **−69.5 %**.
* Energy–Capacity relationship: `Energy = 162 + 16.8·Capacity` (R² = 0.73).

### Clothes Washers
* Modern (≥ 2022) mean **112.7 kWh/yr** vs older (≤ 2017) mean **123.5 kWh/yr**.
* Welch's one-sided t = 1.92, **p = 0.030** → reject H₀.
* Mann-Whitney p = 0.015 confirms the result non-parametrically.
* Front-load vs Top-load: 104 vs 157 kWh/yr (p ≈ 10⁻²³) — load type is the
  single strongest driver of energy use.

---

## How to reproduce the analyses

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run a study

Each folder is self-contained: the analysis script downloads its own dataset
the first time it runs and writes all figures into the local `figures/`
sub-folder.

```bash
# Refrigerators
cd refrigerators
python analysis.py

# Clothes washers
cd ../washers
python analysis.py
```

Each script prints the full set of descriptive statistics, correlation
matrices, regression output and hypothesis-test results (t, df, p, CI, Cohen's
d, Mann-Whitney U) to stdout and regenerates the PNG figures that are embedded
in the corresponding `REPORT.md`.

### 3. Read the reports

Open `refrigerators/REPORT.md` or `washers/REPORT.md` in any Markdown viewer
(VS Code, Obsidian, GitHub). Figures are referenced with relative paths and
render inline.

---

## Data sources

* **ENERGY STAR Certified Residential Refrigerators** — EPA, resource
  `p5st-her9` — <https://catalog.data.gov/dataset/energy-star-certified-residential-refrigerators>
* **ENERGY STAR Certified Residential Clothes Washers** — EPA, resource
  `bghd-e2wd` — <https://catalog.data.gov/dataset/energy-star-certified-residential-clothes-washers>
* Historical refrigerator averages 1972-2013 — AHAM / U.S. DOE:
  <https://appliance-standards.org/sites/default/files/refrigerator_graph_Nov_2016.pdf>
* EU product registry (reference only, not used in analysis) — EPREL:
  <https://eprel.ec.europa.eu>

---

## Deliverables (per professor's brief)

> *DO NOT deliver code.*

The graded deliverables are:
1. The **written report** — `refrigerators/REPORT.md` and/or `washers/REPORT.md`.
2. The **in-class presentation** — `refrigerators/PRESENTATION.md` and/or
   `washers/PRESENTATION.md`.

The Python scripts and CSV files are included in the repo only for
reproducibility and are **not** part of the graded submission.

---

## Authors

Group 1 — Applied Statistics — Universidad Europea — 2026.
