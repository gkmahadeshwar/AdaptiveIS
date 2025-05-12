# adaptiveIS

## Project Overview

**adaptiveIS** is a our Python implementation for flexible applications **importance sampling** methods.  
It compares the following methods on both **toy datasets** and real-world **options trading (IV Surface)** data, evaluated with convergence rate and numerical stability.

This project focuses on three major types of importance sampling:
- **Vanilla Importance Sampling**: Uniform random sampling across all data points.
- **Adaptive Importance Sampling**: Sampling based on a user-defined importance score (e.g., liquidity, premiums, spent).
- **Sequential Importance Sampling**: Adaptive sampling across rounds, progressively updating after each round.


---

## Features

- Reusable functions across arbitrary datasets.
- Adaptive sampling driven by financial data (e.g., options trading volume, money spent).
- Sequential update mechanism for progressive learning or active data collection.
- Emphasis on smooth implied volatility (IV) surface estimation for options datasets.
- Extendable design for 2D or general nD importance functions.

---

## Project Structure

adaptiveIS/
├── __init__.py
├── surface_estimation.py       
├── importance_sampling.py       
│
│environment.yml              
│README.md                     