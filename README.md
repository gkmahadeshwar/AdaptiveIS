# adaptiveIS

## Project Overview

**adaptiveIS** is a Python package for flexible and reusable **importance sampling** methods.  
It provides tools to apply sampling strategies to both **toy datasets** and real-world **options trading (IV Surface)** data.

This project focuses on three major types of importance sampling:
- **Vanilla Importance Sampling**: Uniform random sampling across all data points.
- **Adaptive Importance Sampling**: Sampling based on a user-defined importance score (e.g., liquidity, premiums, spent).
- **Sequential Importance Sampling**: Adaptive sampling across rounds, progressively updating after each round.

The package allows easy plug-and-play usage for custom datasets in research and prototyping.

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