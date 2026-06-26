---
title: "Anxiety & Depression Among Pregnant Women at a Tertiary Centre"
subtitle: "GAD-7 and PHQ-9 screening for common perinatal mental health disorders in Telangana"
excerpt: "A cross-sectional screening study of antenatal anxiety and depression at a tertiary care centre in Telangana, using GAD-7 and PHQ-9 within a reproducible Quarto pipeline."
date: 2025-04-01
author: "Arun Mitra"
draft: false
layout: single
categories:
  - Maternal Health
  - Mental Health
  - Epidemiology
tags:
  - perinatal mental health
  - GAD-7
  - PHQ-9
  - screening
  - R
links:
- icon: doi
  icon_pack: ai
  name: Paper (TODO_journal)
  url: TODO_doi
---

<!-- TODO_confirm_date -->

## Background

Common mental health disorders in pregnancy, particularly anxiety and depression, are frequently under-detected in routine antenatal care despite their consequences for maternal and child outcomes. This collaborator-led clinical study screened pregnant women attending a tertiary care centre in Telangana to estimate the burden of antenatal anxiety and depression and to characterise the referral cascade for those screening positive.

## Approach

A cross-sectional design was used, with anxiety screened via the GAD-7 and depression via the PHQ-9, scored into standard severity bands (minimal, mild, moderate, moderately severe, severe). A referral criterion flagged participants with moderate-or-greater anxiety or depression, and onward attendance with a psychiatrist was tracked. Arun led the analysis in R, using `gtsummary` for descriptive tables within a fully reproducible Quarto pipeline (`results_manuscript.qmd`).

## What we found

- Descriptive epidemiology covered sociodemographics (age, income, education, family type, Kuppuswamy socioeconomic status) and trimester distribution across the screened cohort.
- Prevalence of any anxiety and any depressive symptoms, severity distributions, and anxiety-depression comorbidity were estimated; exact figures to be confirmed from the final dataset. <!-- TODO_findings -->
- The first trimester showed the highest rates of moderate-to-severe anxiety and major depression. <!-- TODO_findings -->
- A referral cascade was constructed, quantifying the share of screen-positive women who actually attended psychiatric assessment. <!-- TODO_findings -->

## Outputs & impact

The study provides tertiary-centre estimates of antenatal mental health burden in Telangana and highlights gaps between screening, referral, and psychiatric follow-up that routine antenatal services could close. Outputs include a reproducible Quarto analysis and publication-ready `gtsummary` tables and figures summarising prevalence and the referral cascade.
