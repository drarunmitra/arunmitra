---
title: "Tuberculosis Notification & Differentiated Care in Goa"
subtitle: "Epidemiological analysis of TB notification and comorbidity data under the NTEP"
excerpt: "Analysis of TB notification registers, differentiated-care models, and comorbidity patterns in Goa, where the TB death rate has run well above the national average."
date: 2025-06-01
author: "Arun Mitra"
draft: false
layout: single
categories:
  - Epidemiology
  - Tuberculosis
  - Data Science
tags:
  - tuberculosis
  - differentiated care
  - surveillance
  - R
links:
- icon: doi
  icon_pack: ai
  name: Paper (TODO_journal)
  url: TODO_doi
---

<!-- TODO_confirm_date -->

## Background

India's National Tuberculosis Elimination Programme (NTEP) has set an ambitious elimination target, yet Goa has reported a persistently high TB death rate, around 9% in 2023 against roughly 4.2% nationally. Diabetes, alcohol use, and loss to follow-up are commonly cited as drivers, but concrete local evidence has been limited. This project applies data-science and epidemiological methods to NTEP (Ni-kshay) records to characterise TB notification, comorbidity, and differentiated-care patterns in the state.

## Approach

The analysis draws on patient-level notification data from the Ni-kshay database for the 2021-2023 treatment cohorts, exported as CSV for secondary analysis. Work was carried out in R using the tidyverse, with structured exploratory data analysis of notification registers and comorbidity records (`eda_notification_data.R`, `eda_comorbidity_data.R`), followed by epidemiological analysis and differentiated-care stratification (`epidemiological_analysis.R`). Treatment outcomes were framed as a binary died-versus-survived endpoint, with socio-demographics, comorbidities, addictions, and adverse drug reactions as candidate factors.

## What we found

- TB notification and comorbidity registers were cleaned, harmonised, and profiled to support stratified, differentiated-care analysis.
- Exploratory analysis characterised the distribution of comorbidities (including diabetes) and addictions across the notified cohort.
- Detailed associations with mortality and differentiated-care outcomes are in progress. <!-- TODO_findings -->

## Outputs & impact

The project delivers a reproducible R/tidyverse pipeline for ingesting and analysing Ni-kshay notification and comorbidity data, and a stratification scheme aligned with differentiated TB care models. It lays the groundwork for prediction algorithms targeting avoidable TB deaths in Goa and for evidence-informed prioritisation of high-risk patients under the NTEP. This work is in progress.
