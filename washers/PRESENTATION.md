# PRESENTATION SLIDES — Group 1
## Energy Consumption of Old vs. Modern Clothes Washers

---

### Slide 1 — Title & Objectives
**Energy Consumption of Old vs. Modern Clothes Washers**
Group 1 · Descriptive Statistics · Universidad Europea · 2026
*Hypothesis: modern residential clothes washers consume less energy than older ones.*

---

### Slide 2 — Motivation
* Washers are a top-5 household electricity consumer.
* They use both electricity **and** hot water (heated by the boiler).
* Efficiency standards (IMEF) promise savings — do they deliver?

---

### Slide 3 — Dataset
* **ENERGY STAR Certified Residential Clothes Washers** (EPA / data.energystar.gov, `bghd-e2wd`).
* 361 raw rows → 351 after cleaning (combo washer/dryers removed).
* Market-available years: 2014 – 2026.

---

### Slide 4 — Variables
* Annual Energy Use (kWh/yr) — target
* Volume (ft³) — size
* IMEF — efficiency metric (higher better)
* IWF & Annual Water Use — water efficiency
* Load Configuration — Front / Top
* Date Available On Market — era

---

### Slide 5 — Older vs Modern Cohorts
* Older: ≤ 2017 → **n = 40**
* Modern: ≥ 2022 → **n = 171**
* Mid (2018-2021) excluded to avoid overlap.

---

### Slide 6 — Univariate Overview
* Overall mean = 122 kWh/yr, median = 110, SD = 41, right-skewed (skew 1.6).
* Front-loads dominate (66 %).
* Show **Fig. 1 (histogram all)** + **Fig. 4 (bar load config)**.

---

### Slide 7 — Older vs Modern (Univariate)
* Mean 123.5 → 112.7 kWh/yr (−9 %).
* Median 120 → 106; IQR tighter for Modern.
* Show **Fig. 5 (density)** + **Fig. 6 (boxplot)**.

---

### Slide 8 — Bivariate Relationships
* Correlation matrix: Energy-Water 0.67, Energy-IMEF −0.48, Energy-Volume 0.41.
* Show **Fig. 7 (scatter Volume × Load)** and **Fig. 8 (IMEF × Energy)**.

---

### Slide 9 — Main Hypothesis Test
* Welch's t (one-sided): **t = 1.92, df = 65, p = 0.030**.
* Mean diff = 10.8 kWh/yr, 95 % CI [−0.5, +22.1]; Cohen d = 0.31.
* Mann-Whitney p = 0.015.
* **Reject H₀ at α = 0.05.**

---

### Slide 10 — Secondary Tests
* **Front-load vs Top-load**: 104 vs 157 kWh/yr, t = 12.0, p ≈ 10⁻²³.
* **IMEF between eras**: p = 0.46 (no difference).
* ⇒ Energy gain comes from product mix (more front-loaders, smaller drums), not from higher IMEF.

---

### Slide 11 — Conclusions
1. Modern washers do consume significantly less energy (~9 %).
2. The lever is water use and load configuration, not IMEF.
3. Product evolution + stricter standards explain the result.

---

### Slide 12 — Limitations & Q&A
* Only ENERGY STAR certified models — the effect vs truly old washers is larger.
* Lab-cycle kWh, not metered household usage.
* Cut-offs (2017 / 2022) set empirically from the year distribution.
*Thank you — questions?*
