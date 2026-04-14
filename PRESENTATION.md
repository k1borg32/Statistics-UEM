# PRESENTATION SLIDES — Group 1
## Energy Consumption of Old vs. Modern Appliances
### (Refrigerators case study)

---

### Slide 1 — Title
**Energy Consumption of Old vs. Modern Appliances**
Group 1 · Descriptive Statistics · Universidad Europea · 2026
*Hypothesis: modern refrigerators consume less energy than older ones.*

---

### Slide 2 — Motivation
* Refrigerators run 24/7 → biggest single residential electricity load.
* EU energy labels & U.S. NAECA standards promised huge savings.
* Question: **did the promise materialise in real products?**

---

### Slide 3 — Data
* **ENERGY STAR U.S. EPA registry** — 4 591 certified fridges, 2014–2026.
  Annual kWh, capacity, standard baseline, certification date.
* **AHAM / DOE historical averages** — shipment-weighted means 1972-2013.
* Working sample: 464 "older" (2014-2017) + 2 621 "modern" (2023-2026).

---

### Slide 4 — Univariate picture
Modern fridges: mean **390 kWh/yr** · median 347 · SD 164 · right-skewed.
Older cohort: mean **433 kWh/yr** · median 398.
Insert **Fig. 1 (histogram)** + **Fig. 2 (boxplot by era)**.

---

### Slide 5 — The 50-year story
Insert **Fig. 5** — from 2 000 kWh (1972) → ~390 kWh (2025).
**−80 % in 50 years while volume grew ~20 %.**

---

### Slide 6 — Bivariate view
* Correlation Energy ↔ Capacity = 0.86.
* Regression: Energy = 162 + 16.8 × Capacity (R² = 0.73).
* Manufacturers cluster 10 % under the federal standard.
Insert **Fig. 3 (scatter)**.

---

### Slide 7 — Statistical Inference
95 % CI for modern-fridge mean: **[384, 396] kWh/yr**.
Versus the 1981 AHAM baseline of 1 278 kWh → one-sample t = −278, p ≈ 0.
⇒ Modern units are **69.5 % below the 1981 population mean**.

---

### Slide 8 — Hypothesis Test (old vs modern cohort)
H₀: µ_old ≤ µ_modern · H₁: µ_old > µ_modern · α = 0.05
Welch's t (one-sided): **t = 4.86, p = 7.5 × 10⁻⁷**
Diff = 42.4 kWh/yr, 95 % CI [25, 60]; Mann-Whitney confirms (p = 10⁻⁵).
**Reject H₀.**

---

### Slide 9 — Conclusions
1. Modern fridges **really do** consume significantly less energy.
2. −70 % vs 1981, −10 % vs 2014-2017, with *higher* capacity.
3. ~42 kWh/yr × 150 M U.S. fridges ≈ 6.3 TWh/yr saved per decade.
4. Standards (not marketing) are the main driver.

---

### Slide 10 — Q&A
*Thank you.*
