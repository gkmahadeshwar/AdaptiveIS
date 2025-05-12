import pandas as pd
import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

def black_scholes_price(S, K, T, r, sigma, option_type):
    if T <= 0 or S <= 0 or K <= 0 or sigma <= 0:
        return 0.0

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
        
    return price

def implied_volatility(price, S, K, T, option_type, r=0.01):
    def bs_error(sigma):
        return black_scholes_price(S, K, T, r, sigma, option_type) - price

    try:
        # Check if the root is bracketed in the interval
        low_val = bs_error(1e-6)
        high_val = bs_error(5.0)

        # If no sign change, no root in interval
        if low_val * high_val > 0:
            return np.nan

        # Try solving with Brent's method
        implied_vol = brentq(bs_error, 1e-6, 5.0, maxiter=500)
        return implied_vol

    except Exception as e:
        return np.nan

def compute_iv_surface(df, r=0.01):
    df = df.copy()

    # Use BidAsk as MidPrice
    df['MidPrice'] = df['BidAsk']

    # Parse and compute time to maturity
    df['Date'] = pd.to_datetime(df['Time']).dt.date
    df['ExpirationDate'] = pd.to_datetime(df['Exp']).dt.date
    df['T'] = (pd.to_datetime(df['ExpirationDate']) - pd.to_datetime(df['Date'])).dt.days / 365.0
    df = df[df['T'] > 1e-4]

    # Normalize option type (C/P → 'call', 'put')
    df['C/P'] = df['C/P'].str.lower()
    # Filter valid values
    df = df.dropna(subset=['MidPrice', 'Strike', 'Spot', 'T'])
    df = df[(df['MidPrice'] > 0) & (df['Strike'] > 0) & (df['Spot'] > 0)]
    # Compute implied volatility (safe apply)
    def safe_iv(row):
        try:
            return implied_volatility(
                price=row['MidPrice'],
                S=row['Spot'],
                K=row['Strike'],
                T=row['T'],
                option_type=row['C/P'],
                r=r
            )
        except:
            return np.nan

    df['IV'] = df.apply(safe_iv, axis=1)
    df = df.dropna(subset=['IV'])

    # Add moneyness and log-moneyness
    df['moneyness'] = df['Strike'] / df['Spot']
    df['log_moneyness'] = np.log(df['moneyness'])
    log_moneyness_std = df['log_moneyness'].std()
    df['atm_weight'] = np.exp(- (df['log_moneyness'] ** 2) / (2 * log_moneyness_std**2))

    return df
