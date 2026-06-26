---
title: "Geo-Spatial Analysis of Acute Ischemic Stroke Reperfusion Treatment in India"
subtitle: "An assessment of the distribution of and access to reperfusion-capable stroke centres"
excerpt: "Nationwide geospatial and spatial-epidemiological analysis quantifying how much of India's population can reach an intravenous thrombolysis (IVT)- or endovascular thrombectomy (EVT)-capable stroke centre within the critical treatment window, exposing stark regional disparities in time-sensitive reperfusion care."
date: 2025-06-01
author: "Arun Mitra"
draft: false
layout: single
categories:
  - Epidemiology
  - Spatial Analysis
  - Stroke
tags:
  - spatial epidemiology
  - health equity
  - stroke
  - R
  - GIS
links:
- icon: doi
  icon_pack: ai
  name: Paper (International Journal of Stroke)
  url: https://doi.org/10.1177/17474930241312598
---

## Background

Acute ischaemic stroke is a time-critical emergency in which reperfusion therapy, intravenous thrombolysis (IVT) and endovascular thrombectomy (EVT), must be delivered within a narrow therapeutic window to salvage brain tissue. In a country as large and geographically heterogeneous as India, the practical benefit of these treatments depends not only on whether capable centres exist but on whether patients can physically reach them in time. This study asks a simple but consequential question: what share of India's population actually lives within a one-hour drive of a stroke centre equipped to deliver IVT or EVT, and how does that access vary across regions?

## Approach

I contributed the data-science analysis at the AMC Data Science Lab, AMCHSS, SCTIMST. The study was led by Dr. Kaiz S. Asif with a large international author group, conducted in partnership with the All India Mission Thrombectomy Regional Committees, and included senior stroke and data-science investigators such as Dr. Dileep Yavagal, Dr. P.N. Sylaja, Dr. Biju Soman, Dr. Adrija Roy, and Dr. M.V. Padma Srivastava, among others. We geolocated IVT- and EVT-capable stroke facilities nationwide and built a network-based, drive-time accessibility model rather than relying on simple straight-line buffers. Using spatial-epidemiological methods in R (sf and allied geospatial tooling), we intersected drive-time catchments with gridded population data to estimate the population covered within one-hour isochrones and to compute median drive times by region.

## What we found

- Only about 26.3% of India's population has an IVT-capable stroke centre within a one-hour drive.
- Only about 20.6% of the population lives within a one-hour drive of an EVT-capable centre.
- Access is sharply unequal across regions: South India is comparatively well served, while large parts of the country, especially the Northeast, are severely underserved, with median drive times to reperfusion-capable care exceeding seven hours.
- The geography of access, not just the count of facilities, is the binding constraint on equitable time-sensitive stroke care.

## Outputs & impact

The work was published in the *International Journal of Stroke* (2025; 20(6):708–720, [doi:10.1177/17474930241312598](https://doi.org/10.1177/17474930241312598)) and is already being cited in the stroke literature (for example in *Stroke*, 2026); it was accompanied by a public press release highlighting the access gap for time-critical stroke care. By mapping where reperfusion-capable services are reachable and where they are not, the analysis provides a concrete evidence base for prioritising new stroke-centre placement, referral-network design, and pre-hospital triage policy. The reproducible geospatial workflow is intended to be extensible to other time-sensitive emergency services and to subnational planning.
