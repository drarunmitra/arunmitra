---
title: "A Quasi-Experimental Trial of the NutriAide App for Anaemia in Pregnancy"
subtitle: "Does app-based dietary self-monitoring improve anaemia outcomes over standard antenatal care?"
excerpt: "A quasi-experimental trial testing whether the NutriAide mobile app — daily dietary logging plus reminders — improves haemoglobin in anaemic pregnant women beyond routine iron supplementation and counselling. The app showed no significant advantage, with app adherence a key limiting factor."
date: 2025-11-20
author: "Arun Mitra"
draft: false
layout: single
categories:
  - Nutrition
  - Maternal Health
  - Data Science
tags:
  - anaemia in pregnancy
  - mHealth
  - NutriAide
  - quasi-experimental
  - R
---

## Background

Anaemia in pregnancy is a major problem in India — NFHS-5 puts the prevalence at 52.2% — and adherence to routine iron–folic acid (IFA) supplementation is often poor because of side effects. Mobile-health (mHealth) tools that support dietary awareness and supplement reminders have been proposed as a way to improve behaviour and outcomes. This study tested whether the **NutriAide** app (developed by the National Institute of Nutrition), used for daily dietary self-logging, adds measurable benefit over standard antenatal care in anaemic pregnant women.

## Approach

Conducted as an ICMR Short-Term Studentship project (ref. STS2024-3Y-03247), this was a **quasi-experimental trial** in the antenatal clinic of a tertiary-care Obstetrics & Gynaecology department over two months. **59 pregnant women** with mild-to-moderate anaemia (haemoglobin 8–10 g/dL) in the second or early third trimester, who owned smartphones, were allocated to an intervention group (n = 30) — NutriAide app for daily food logging plus WhatsApp reminders, on top of routine IFA and a diet chart — or a control group (n = 29) receiving IFA and the diet chart alone. Haemoglobin and serum iron, ferritin, folate and B12 were measured at baseline and after the intervention. I led the data analysis in R 4.3.2 (paired/Welch comparisons, group summaries).

## What we found

- Haemoglobin improved in **both** groups over two months — but the app group did **not** do better than standard care.
- Mean haemoglobin rise was **1.26 ± 0.95 g/dL (intervention) vs 1.92 ± 1.42 g/dL (control)** — no significant difference (p = 0.10); end-of-study haemoglobin was actually higher in the control group (11.49 vs 10.54 g/dL, p = 0.022).
- **App adherence was the key limitation:** only 60% (18/30) installed NutriAide, and of those just 66.7% (12) ever logged a meal.
- Conclusion: app-based dietary self-monitoring did not outperform routine supplementation and counselling within this short, small study.

## Outputs & impact

This completed studentship analysis is a candid **null result**: the NutriAide app showed no significant advantage over standard antenatal anaemia care, with poor engagement, a short two-month follow-up, small sample, and unmeasured confounders (e.g., parenteral iron) limiting any effect. It offers a useful design lesson for future mHealth nutrition trials — larger, multi-centre samples, longer follow-up, and real-time adherence tracking — alongside a reproducible R analysis pipeline. The manuscript and dissemination are in preparation.
