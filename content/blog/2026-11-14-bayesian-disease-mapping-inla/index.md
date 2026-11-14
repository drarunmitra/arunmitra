---
title: "Bayesian disease mapping in R with INLA"
subtitle: "A short, practical guide for district-level health data"
author: Arun Mitra
date: '2026-11-14'
categories:
  - spatial epidemiology
  - R
tags:
  - INLA
  - disease mapping
  - Bayesian
  - spatial
description: "How to fit a BYM2 disease-mapping model with R-INLA: build the neighbour graph, set priors, map relative risks and exceedance probabilities, and avoid common mistakes."
excerpt: "A step-by-step guide to fitting a BYM2 disease-mapping model with R-INLA, from the neighbour graph to relative-risk and exceedance maps."
draft: false
layout: standard
show_title_as_headline: no
image_alt: "Banner image: a stylised district map shaded in graded blues and reds beside a smooth bell-shaped posterior curve, with a few linked neighbour nodes between districts"
---

District-level counts of disease are noisy. A district with 4 cases and an expected count of 2 looks twice as risky as one with 400 cases and an expected count of 200, yet the first number tells us far less. Bayesian disease mapping fixes this by letting each district borrow strength from its neighbours. INLA (Integrated Nested Laplace Approximation) fits these models in seconds, not hours, which makes it a good first tool for health data.

This post shows the core workflow for a Poisson model with a BYM2 spatial term. The code is a template: swap in your own `sf` object. I have not run it on your data, so read the warnings and check each step.

## What you need

- An `sf` object with one row per district (or block, or state), with a column of observed counts.
- An expected count for each area. The usual choice is indirect standardisation, which multiplies the age-specific rates of the whole study region by each district's age-specific population.
- R packages `INLA`, `sf`, `spdep`, `ggplot2` and `dplyr`.

`INLA` is not on CRAN. Install it from the INLA site:

```r
install.packages(
  "INLA",
  repos = c(getOption("repos"), INLA = "https://inla.r-inla-download.org/R/stable"),
  dep = TRUE
)
```

## Step 1: build the neighbour graph

BYM2 treats two districts as neighbours if they share a border. `spdep` finds the neighbours, and `nb2INLA` writes them in the format INLA reads.

```r
library(sf)
library(spdep)
library(INLA)

districts <- st_read("districts.gpkg")        # your boundaries
nb <- poly2nb(districts)                      # queen contiguity by default
nb2INLA("districts.adj", nb)
g <- inla.read.graph("districts.adj")
```

Check `nb` before you go on. `poly2nb` warns when a district has no neighbours, which happens with islands. An area with no neighbours cannot borrow strength from anyone, and the model will treat it as its own island. Link it to its nearest mainland district by hand, or accept the result and say so in your methods.

## Step 2: set up the model

INLA needs a numeric index for the spatial term.

```r
districts$id <- seq_len(nrow(districts))

formula <- cases ~ 1 +
  f(id,
    model = "bym2",
    graph = g,
    scale.model = TRUE,
    constr = TRUE,
    hyper = list(
      phi  = list(prior = "pc", param = c(0.5, 2/3)),
      prec = list(prior = "pc.prec", param = c(1, 0.01))
    )
  )

fit <- inla(
  formula,
  family = "poisson",
  data = districts,
  E = expected,
  control.predictor = list(compute = TRUE),
  control.compute = list(dic = TRUE, waic = TRUE)
)
```

Three choices matter here.

- **`bym2`** splits the area effect into a structured part (spatial smoothing) and an unstructured part (district-specific noise). The mixing parameter `phi` tells you how much of the variation is spatial. A value near 1 means neighbours look alike. A value near 0 means the variation is mostly local noise.
- **`scale.model = TRUE`** scales the spatial term so that the prior on the precision means the same thing whatever your map looks like. Leave it on.
- **Penalised complexity (PC) priors** are set in terms you can reason about. `param = c(0.5, 2/3)` for `phi` says there is a two-thirds probability that less than half of the variation is spatial. `param = c(1, 0.01)` for the precision says there is a 1% chance that the standard deviation exceeds 1. These are sensible defaults for a log relative risk. Change them if you know your outcome varies far more than that, and say what you used.

## Step 3: get relative risks and exceedance probabilities

When you give INLA an `E` term, the fitted values are the area relative risks, that is, the risk compared with what you expected.

```r
districts$RR <- fit$summary.fitted.values$mean
districts$RR_low <- fit$summary.fitted.values$`0.025quant`
districts$RR_high <- fit$summary.fitted.values$`0.975quant`

# probability that the relative risk is above 1
districts$p_exceed <- sapply(
  fit$marginals.fitted.values,
  function(m) 1 - inla.pmarginal(1, m)
)
```

The exceedance probability is often more useful than the point estimate. A district with a relative risk of 1.3 and an exceedance probability of 0.55 is a very different finding from one with 1.3 and 0.98.

## Step 4: map it

```r
library(ggplot2)

ggplot(districts) +
  geom_sf(aes(fill = RR), colour = "white", linewidth = 0.1) +
  scale_fill_gradient2(midpoint = 1, trans = "log",
                       low = "#2c7bb6", mid = "white", high = "#d7191c",
                       name = "Relative risk") +
  theme_void()
```

Put the exceedance map next to it, with breaks at 0.2 and 0.8. A map of relative risks alone invites readers to over-read the red districts.

## Things that go wrong

- **Expected counts that are wrong.** The model smooths toward the expected count. If your age standardisation is off, every map you draw is off by the same amount.
- **Two data sources for the numerator and denominator.** Cases from a surveillance system and population from the census can disagree about district boundaries. Check that they refer to the same boundaries and the same year.
- **Reading the map as causal.** This is an ecological analysis. A district-level pattern does not tell you about the individuals in it.
- **Not checking sensitivity.** Refit with another prior on `phi` and with a plain unstructured model. Compare DIC and WAIC (`fit$dic$dic`, `fit$waic$waic`) and check that your story survives.
- **Old INLA versions.** The package changes between releases. Record `packageVersion("INLA")` in your analysis log.

## Where to read more

- Riebler A, Sorbye SH, Simpson D, Rue H. An intuitive Bayesian spatial model for disease mapping that accounts for scaling. *Statistical Methods in Medical Research*. 2016. This is the paper behind BYM2.
- Moraga P. *Spatial Statistics for Data Science: Theory and Practice with R*. This is free online and has a worked INLA chapter.
- Blangiardo M, Cameletti M. *Spatial and Spatio-temporal Bayesian Models with R-INLA*.

I use this workflow for the spatial work on maternal and child health and tuberculosis notification described on the [Research](/research/) page. If you want to try it on your own data and get stuck, my contact details are on the [Contact](/contact/) page.
