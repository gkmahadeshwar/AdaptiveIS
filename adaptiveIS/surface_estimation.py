import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import norm

def black_scholes_price(S, K, T, r, sigma, option_type):
    """Compute Black-Scholes price for a call or put option."""
    if T <= 0:
        return max(0, S - K) if option_type == "call" else max(0, K - S)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type.lower() == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type.lower() == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return price

def implied_volatility(price, S, K, T, r, option_type):
    """Solve for implied volatility using numerical methods."""
    if price <= 0 or S <= 0 or K <= 0 or T <= 0:
        return np.nan
    try:
        return brentq(
            lambda sigma: black_scholes_price(S, K, T, r, sigma, option_type) - price,
            1e-6, 5
        )
    except:
        return np.nan

def compute_iv_surface(df, r=0.01):
    """
    Compute implied volatility surface.
    
    Args:
        df (pd.DataFrame): DataFrame with Strike, StockPrice, ExpirationDate, Date, OptionType, Spent
        r (float): Risk-free rate

    Returns:
        df (pd.DataFrame): Same DataFrame but now with computed IVs
    """
    df = df.copy()

    # Calculate time to maturity T
    df['T'] = (pd.to_datetime(df['ExpirationDate']) - pd.to_datetime(df['Date'])).dt.days / 365
    df = df[df['T'] > 0]

    # Assume Spent is the total money spent for 100 contracts (standard format),
    # divide accordingly if needed. Here simplified.
    df['MidPrice'] = df['Spent'] / 100  

    # Calculate IV
    df['IV'] = df.apply(lambda row: implied_volatility(
        price=row['MidPrice'],
        S=row['StockPrice'],
        K=row['Strike'],
        T=row['T'],
        r=r,
        option_type=row['OptionType']
    ), axis=1)

    return df.dropna(subset=['IV'])