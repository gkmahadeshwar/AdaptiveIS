# adaptiveIS

## Project Overview

**adaptiveIS** is a our Python implementation for flexible applications **importance sampling** methods.  
It compares the following methods on both **toy datasets** and real-world **options pricing** data, evaluated with convergence rate and stability.

This project focuses on three major types of importance sampling:
- **Importance Sampling (IS)**: Sampling based on a user-defined starting distribution.
- **Adaptive Importance Sampling (AIS)**: Sampling based on a user-defined starting distribution, which is reweighted through each iteration.


---

## Features

- Implementation of IS and AIS
- Application on 1D toy example
- Implementation of "Hard-mixture" AIS
- Implementation to estimate a fair price in options trading based on Black-Scholes equation

---

## Project Structure
'''
adaptiveIS/
.
├── adaptiveIS
│   ├── __init__.py
│   ├── iv_surface_plot.py
│   └── surface_estimation.py
├── Numerical_final_presentation_GKM_JZ_FINAL.pdf
├── OptionTrading.csv
├── options_pricing_final.ipynb
├── Importance_Sampling.ipynb
├── plots
├── environment.yml
└── README.md
'''
