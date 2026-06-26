---
title: "Where India Misses Tuberculosis"
subtitle: "A sub-national map of the TB burden–notification gap"
excerpt: "A spatial epidemiology compendium that estimates India's tuberculosis case-detection gap at district and sub-district level, comparing modelled incidence against Ni-kshay notifications. It maps where TB cases are being missed and unpacks the drivers of that geographic inequality."
date: 2025-11-01
author: "Arun Mitra"
draft: false
layout: single
categories:
  - Tuberculosis
  - Spatial Analysis
  - Epidemiology
tags:
  - tuberculosis
  - case detection
  - spatial epidemiology
  - small-area estimation
  - BYM2
  - R
links:
- icon: doi
  icon_pack: ai
  name: Paper (TODO_journal)
  url: TODO_doi
- icon: github
  icon_pack: fab
  name: Code
  url: https://github.com/drarunmitra/tb-notification-gap-india
---
<!-- TODO_confirm_date -->

## Background

India carries the world's largest tuberculosis burden, and a central challenge for the National TB Elimination Programme is the gap between the TB cases that occur and the cases that are actually notified. National coverage figures hide enormous local variation: some districts notify nearly everyone they should, while others miss a large share of their true burden. This project asks *where* India misses tuberculosis — at a resolution fine enough to be actionable — and *why*.

## Approach

The work is built as a reproducible research compendium in R (4.4.1). It compares modelled TB incidence against annualised Ni-kshay notifications to produce relative under-notification surfaces at district and sub-district level. Methods include small-area estimation and ecological modelling with spatial smoothing (BYM2 via `INLA`), kernel-based surfaces (`sparr`), and raster covariate assembly (`sf`, `terra`) drawing on WorldPop population rasters, the MAP motorised friction surface, the National TB Prevalence Survey, the India TB Report, and NACO databases. Sensitivity analyses propagate uncertainty, apply multiple imputation, and test the robustness of candidate drivers.

## What we found

- The case-detection gap is highly uneven across India, with distinct sub-national clusters of severe under-notification (TODO_findings for specific districts/magnitudes).
- Accessibility (travel friction) and programme/health-system covariates emerge as candidate drivers of the gap.
- Mapping the gap at sub-district resolution reveals priority pockets that national or even state-level figures obscure.

## Outputs & impact

The compendium produces gap-estimate tables and figures (`out/`) with full methodology in Quarto manuscripts, released under MIT (code) and CC-BY-4.0 (derived data) licences with a `CITATION.cff`. By turning notification data into an interpretable, uncertainty-aware map of *missed* TB, the work offers the elimination programme evidence-ready intelligence for targeting active case-finding where it is most needed. The associated manuscript is in preparation (TODO_journal).
