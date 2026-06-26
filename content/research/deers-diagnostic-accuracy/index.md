---
title: "Diagnostic Accuracy of the DEERS Endometrial Imaging Test"
subtitle: "Validation against histopathology across 309 paired cases"
excerpt: "A retrospective diagnostic-accuracy study comparing DEERS imaging classifications with histopathology, showing reliable detection of normal tissue but poor sensitivity for malignancy."
date: 2025-03-01
author: "Arun Mitra"
draft: false
layout: single
categories:
  - Diagnostics
  - Epidemiology
  - Data Science
tags:
  - diagnostic accuracy
  - ROC
  - endometrial pathology
  - validation
  - R
links:
- icon: doi
  icon_pack: ai
  name: Paper (TODO_journal)
  url: TODO_doi
---

<!-- TODO_confirm_date -->

## Background

Endometrial cancer requires early and accurate diagnosis, but the gold standard, histopathological examination (HPE) of an endometrial biopsy, is invasive and uncomfortable. The DEERS imaging test (Diseases of Endometrium – Evaluation and Risk Scoring) is a novel technology offering real-time visualization and classification of endometrial tissue. This study rigorously evaluates its diagnostic performance against HPE.

## Approach

This retrospective analytical study was conducted at a tertiary care hospital in Telangana among 309 women with abnormal uterine bleeding. It compared 309 paired samples, matching DEERS classifications (Normal, Benign, Complex Hyperplasia, Malignancy) against the HPE gold standard. A four-class categorical agreement was assessed via confusion matrix, overall accuracy, and Cohen's kappa, alongside three clinically relevant binary scenarios (Normal vs Abnormal, Malignancy vs all others, Benign vs malignant/pre-malignant). Analysis used R with `tidyverse`, `yardstick`, `pROC`, and `janitor`, reporting sensitivity, specificity, kappa, and ROC/AUC.

## What we found

- Overall four-class accuracy was 73.5% with moderate agreement (Cohen's kappa 0.503).
- DEERS identified normal tissue well (sensitivity ~81%) and distinguished normal from abnormal with fair discrimination (AUC 0.774, accuracy 77.7%).
- Sensitivity for malignancy was extremely poor at 9.1%, missing 10 of 11 malignant cases, with several misclassified as complex hyperplasia.
- For benign versus malignant/pre-malignant lesions, AUC was 0.775 but sensitivity only 28.2%, indicating poor categorical separation of higher-risk pathology.

## Outputs & impact

The study concludes that DEERS is a reasonable tool for confirming normal endometrium but is unreliable as a standalone cancer-screening test because of a high risk of false negatives for malignancy. The findings caution against using it as a primary diagnostic tool and identify where its categorical thresholds need refinement. Outputs include a reproducible R diagnostic-accuracy pipeline, confusion matrices, and ROC analyses.
