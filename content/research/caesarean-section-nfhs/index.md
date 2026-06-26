---
title: "Exploring Spatial Clusters of Caesarean Sections across India"
subtitle: "Insights from National Family Health Survey data — a spatial epidemiological analysis"
excerpt: "Spatial epidemiological analysis of National Family Health Survey (NFHS) data identifying geographic clusters and hotspots of caesarean-section rates across India."
date: 2026-02-20
author: "Arun Mitra"
draft: false
layout: single
categories:
  - Reproductive Health
  - Epidemiology
  - Spatial Analysis
  - Data Science
tags:
  - caesarean section
  - NFHS
  - spatial clustering
  - survey data
  - R
links:
- icon: doi
  icon_pack: ai
  name: Paper (PLOS Global Public Health)
  url: https://doi.org/10.1371/journal.pgph.0006070
- icon: doi
  icon_pack: ai
  name: Preprint (medRxiv)
  url: https://doi.org/10.1101/2025.04.15.25325862
---

## Background

Caesarean section rates in India have risen substantially, raising concerns about both under-provision in underserved populations and over-medicalisation in others. These rates are not uniform across the country, and understanding their geographic patterning is essential for targeted policy. The National Family Health Survey (NFHS) provides large, nationally representative data well suited to mapping where caesarean delivery is unusually common or uncommon. This study uses NFHS data and spatial analysis to identify geographic clusters of caesarean-section rates across India.

## Approach

The analysis applies spatial epidemiological methods to NFHS-4 (2015-16) and NFHS-5 (2019-21) survey data in R. Caesarean-section prevalence was estimated at the district level, and spatial cluster detection was used to locate statistically significant high-prevalence (hotspot) and low-prevalence (coldspot) clusters across the country. The work was led by Arun Mitra with co-authors Durgesh Prasad Sahoo, N. Agarwal, Biju Soman, and Shreyas Patil.

## What we found

- The national caesarean rate rose from 17.2% in NFHS-4 to 21.5% in NFHS-5.
- Caesarean-section rates show significant spatial clustering rather than a uniform national pattern (Global Moran's I and Getis-Ord, p < 0.01), with distinct high- and low-prevalence geographic clusters across India.
- Zonal extremes (NFHS-5) ranged from the South zone highest (~39.5%) to the East zone lowest (~14.7%).
- State extremes ran from Telangana highest (~60.7%) to Nagaland lowest (~5.8%).
- A marked disparity was evident between public- and private-sector facilities.

## Outputs & impact

The work is published in *PLOS Global Public Health* ([10.1371/journal.pgph.0006070](https://doi.org/10.1371/journal.pgph.0006070)), with an earlier version available as a medRxiv preprint. By revealing where caesarean delivery is concentrated geographically, the analysis provides an evidence base for spatially targeted interventions addressing both under- and over-use of caesarean section.
