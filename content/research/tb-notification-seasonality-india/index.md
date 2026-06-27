---
title: "Seasonality of Tuberculosis Notification in India"
subtitle: "Disease signal versus public-sector reporting artefact"
excerpt: "A longitudinal analysis of monthly TB notifications across 747 Indian districts that separates genuine seasonal disease patterns from administrative reporting artefacts. By comparing public and private sectors, it asks how much of TB's apparent seasonality is signal and how much is the rhythm of the reporting system itself."
date: 2025-11-01
author: "Arun Mitra"
draft: false
layout: single
categories:
  - Tuberculosis
  - Epidemiology
  - Time Series
tags:
  - tuberculosis
  - seasonality
  - time series
  - STL decomposition
  - negative binomial
  - R
links:
- icon: database
  icon_pack: fas
  name: Data & code (Zenodo)
  url: https://doi.org/10.5281/zenodo.20665380
- icon: github
  icon_pack: fab
  name: Code
  url: https://github.com/drarunmitra/tb-notification-seasonality-india
---

## Background

Tuberculosis notifications in India rise and fall over the year, and that seasonality is often read as a property of the disease — transmission, reactivation, or care-seeking shifting with the seasons. But notifications are produced by a reporting system, not just by biology. Campaign drives, working-day patterns, and public-sector reporting behaviour can imprint their own rhythm on the data. This study asks whether India's apparent TB seasonality is a disease signal or, in part, a reporting artefact.

## Approach

The analysis is a longitudinal ecological study of monthly TB notifications across 747 districts (2022–2025), implemented in R. It contrasts the public and private sectors to separate genuine seasonal disease patterns from administrative spikes. Methods include seasonal-trend decomposition (STL) and negative-binomial regression with population and working-day offsets, harmonic terms, climate covariates (NASA POWER), and calendar/campaign indicators. Core packages: `dplyr`, `sf`, `tsibble`, `fable`, `glmmTMB`, and `ggplot2`, with WorldPop denominators, Local Government Directory district geometry, and 2011 Census sociodemographic indicators.

## What we found

- Seasonal variance can be partitioned into harmonic, climate, and calendar/campaign components — and several month-on-month movements reverse once reporting structure is adjusted for.
- Public- versus private-sector contrasts expose where apparent seasonality is driven by reporting behaviour rather than disease.
- Geographic heterogeneity in reporting artefacts means seasonality is not a single national story but a patchwork across districts.

## Outputs & impact

Archived code and district-level data are released on Zenodo ([doi:10.5281/zenodo.20665380](https://doi.org/10.5281/zenodo.20665380)) under an MIT licence, with the manuscript currently under review. Distinguishing disease signal from reporting artefact matters for programme planning: it guards against misreading administrative spikes as epidemiological trends and helps target when and where active case-finding and reporting support are most useful.
