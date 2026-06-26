---
title: "Normative Heart Rate Variability Across Age and Gender in Healthy South Indian Adults"
subtitle: "Region-specific reference values for resting HRV from an apex tertiary care centre"
excerpt: "A cross-sectional study establishing region-specific normative reference values for resting heart rate variability (HRV) in 249 healthy South Indian adults, characterising how cardiac autonomic function varies with age and gender. Published in Annals of Neurosciences."
date: 2026-06-01
author: "Arun Mitra"
draft: false
layout: single
categories:
  - Physiology
  - Cardiac Autonomic Function
  - Data Science
tags:
  - heart rate variability
  - autonomic function
  - normative values
  - ageing
  - gender
  - R
links:
- icon: doi
  icon_pack: ai
  name: Paper (Annals of Neurosciences)
  url: https://doi.org/10.1177/09727531261454450
---

## Background

Heart rate variability (HRV) — the beat-to-beat fluctuation in heart rate — is a widely used, non-invasive index of cardiac autonomic regulation, and its time- and frequency-domain measures shift with age, sex, and environment. Most reference values in clinical and research use are derived from Western populations, yet autonomic function differs across regions and ethnic groups. This study set out to establish region-specific normative HRV values for a predominantly South Indian population and to characterise how those values vary with age and gender.

## Approach

This was a cross-sectional observational study at an apex tertiary care centre in southern India. Five-minute resting ECG recordings were obtained from 272 healthy adults aged 18–80 (predominantly from Telangana and Andhra Pradesh); after excluding 23 recordings for artefacts or poor signal quality, **249 participants** were analysed (mean age 42 ± 15 years; 130 male, 119 female). Standard time- and frequency-domain HRV indices were derived per Task Force guidelines in LabChart, and participants were grouped by age (<30, 30–59, 60+). I contributed the data and statistical analysis — conducted in R (with JASP) using Welch t-tests, one-way ANOVA, and Games–Howell post-hoc tests, with a formal power analysis (`pwr`/`pwrss`). The study was led by Dr. Anish Singhal, with senior author Dr. Nitin Ashok John and colleagues.

## What we found

- **Age:** overall HRV and parasympathetic indices (SDRR, RMSSD, pRR50%) declined with age, most markedly after the 30s, while the LF/HF ratio rose — a shift toward sympathetic predominance. ANOVA showed significant age effects on SDRR, RMSSD, pRR50%, LF nu, HF nu, LF/HF and total power.
- **Gender:** males showed higher sympathetic tone (higher LF nu and LF/HF, lower resting heart rate), while females showed greater parasympathetic activity (higher RMSSD, pRR50% and HF nu).
- At n = 249 the study was well powered (>0.90) to detect age main effects and to fit full age-plus-sex models for moderate-to-large effects.
- Resting SDRR was markedly lower than Western Task Force norms, underscoring the need for region-specific reference values.

## Outputs & impact

The work is published in *Annals of Neurosciences* ([doi:10.1177/09727531261454450](https://doi.org/10.1177/09727531261454450)). It provides age- and gender-stratified normative HRV reference values for healthy South Indian adults — a practical baseline for interpreting autonomic testing in clinical and research settings across the region.
