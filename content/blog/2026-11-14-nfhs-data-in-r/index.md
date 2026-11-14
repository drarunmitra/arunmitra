---
title: "Working with NFHS data in R"
subtitle: "From the raw survey file to a weighted state estimate"
author: Arun Mitra
date: '2026-11-14'
categories:
  - data science
  - R
tags:
  - NFHS
  - DHS
  - survey analysis
  - R
description: "How to get the India National Family Health Survey (NFHS) data, read it in R, declare the survey design, and produce correctly weighted estimates with confidence intervals."
excerpt: "A practical guide to NFHS microdata in R: access, variable names, survey weights, the survey design object, and weighted state estimates with confidence intervals."
draft: false
layout: standard
show_title_as_headline: no
image_alt: "Banner image: rows of a survey table flowing into a weighted bar chart, beside a simple outline of India with a few state regions highlighted"
---

The National Family Health Survey (NFHS) is the main source of population-level data on health, nutrition and family welfare in India. It is a household survey with a complex design. If you treat it as a simple random sample, your estimates and your confidence intervals will both be wrong. This post covers the steps I follow, from getting the files to a weighted estimate by state.

## Getting the data

NFHS microdata are distributed by the DHS Program.

1. Register at [dhsprogram.com](https://dhsprogram.com) and describe your project.
2. Request the India datasets for the survey round you need.
3. Download the files in Stata format (`.dta`).

You will see several files per round, one for each unit of analysis:

| File | One row per | Use for |
|------|-------------|---------|
| Individual recode (IR) | woman aged 15 to 49 | women's health, fertility, contraception |
| Births recode (BR) | child ever born | delivery care, birth outcomes |
| Children's recode (KR) | child under 5 | immunisation, child nutrition and illness |
| Household recode (HR) | household | housing, water, sanitation, assets |
| Men's recode (MR) | man | men's health and behaviour |

The file names depend on the round. Check the download page and the codebook that comes with the data.

**A rule of the data agreement:** you may not share the microdata. For a reproducible project, share your code and a script that tells readers how to download the files themselves. I keep the data in a folder that is excluded from Git.

## Reading the file

```r
library(haven)
library(dplyr)

br <- read_dta("data/your_births_file.DTA")
```

`read_dta` keeps the value labels from Stata. Use `haven::as_factor()` to turn a coded column into labelled categories, and `haven::zap_labels()` when you want plain numbers.

## The four variables that define the design

Every DHS-style file has the same core design variables:

| Variable | Meaning |
|----------|---------|
| `v005` | sample weight, stored as an integer and scaled by one million |
| `v021` | primary sampling unit (PSU) |
| `v022` | sample strata |
| `v024` | state |

Divide `v005` by 1,000,000 to get the weight.

```r
br <- br |>
  mutate(wt = v005 / 1e6)
```

**A warning about weights.** The weights in a state-level file are made for estimates within a state. If you pool several states to get a national figure, read the survey's final report and the DHS guidance on weights before you do it. Pooling state weights without adjustment can give a wrong national estimate.

## Declare the survey design

```r
library(survey)
options(survey.lonely.psu = "adjust")

des <- svydesign(
  ids     = ~v021,
  strata  = ~v022,
  weights = ~wt,
  data    = br,
  nest    = TRUE
)
```

`nest = TRUE` is needed because PSU numbers are only unique within a stratum. The `lonely.psu` option tells R what to do when a stratum has a single PSU, which happens when you subset to a small group.

## A worked example: caesarean delivery by state

The births recode has `m17` (delivery by caesarean) and `b19` (age of the child in months). Restrict the analysis to births in the last five years.

```r
br <- br |>
  mutate(
    csection = case_when(m17 == 1 ~ 1, m17 == 0 ~ 0),
    recent   = b19 < 60
  )

des <- svydesign(ids = ~v021, strata = ~v022, weights = ~wt,
                 data = br, nest = TRUE)

# subset the design, not the data frame
des_recent <- subset(des, recent)

est <- svyby(
  ~csection, ~v024, des_recent, svymean,
  na.rm = TRUE, vartype = c("se", "ci")
)
```

The point to notice is `subset(des, recent)`. If you filter the data frame before you declare the design, R forgets that the full sample existed, and the standard errors come out wrong. Always subset the design object.

Multiply the proportions by 100 and report them with their confidence intervals. For a state with few births, check the number of unweighted cases too. A state estimate on 40 births is not one to put in a headline.

## Mistakes I see often

- **Using unweighted means.** `mean(br$csection)` gives the average in the sample, not in the population.
- **Treating "don't know" as data.** Codes such as 8, 9 or 99 often mean "don't know" or "missing". Recode them before you analyse.
- **Comparing rounds without care.** District boundaries and some definitions change between NFHS rounds. Check the codebook before you compare a district over time.
- **Reporting a 95% interval from too few clusters.** The effective sample size is closer to the number of PSUs than to the number of rows.
- **Forgetting to cite the DHS Program.** The data agreement asks for it.

## Linking to maps

India files include a district code, usually `sdist`. Check the codebook for your round. You can match it to a district boundary file and use the resulting estimates in a map. District estimates from a survey designed for state-level precision have wide intervals, so smooth them with a model before you draw conclusions. My [post on Bayesian disease mapping with INLA](/blog/2026-11-14-bayesian-disease-mapping-inla/) shows one way.

My own analysis of spatial clusters of caesarean section in NFHS data is described on the [Research](/research/caesarean-section-nfhs/) page.
