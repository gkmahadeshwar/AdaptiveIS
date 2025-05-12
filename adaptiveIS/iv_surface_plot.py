import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

def plot_iv_surface(df, option_type, strike_col='Strike', maturity_col='T', iv_col='IV', title=None, 
                    figsize=(10, 5), elev=30, azim=-135):
    """
    Plots the IV surface: IV as a function of Strike and Time to Maturity T.
    
    Args:
        df (pd.DataFrame): DataFrame containing strike, T, and IV
        strike_col (str): Name of the column containing strike prices
        maturity_col (str): Column with time to maturity (in years)
        iv_col (str): Column with implied volatilities
        title (str): Plot title
        figsize (tuple): Figure size
        elev (float): Elevation angle for 3D plot
        azim (float): Azimuth angle for 3D plot
    """
    df = df.copy()
    df = df[df['C/P'].str.lower() == option_type]
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')

    x = df[strike_col]
    y = df[maturity_col]
    z = df[iv_col]

    ax.scatter(x, y, z, c=z, cmap='viridis', s=20)
    
    ax.set_xlabel(strike_col)
    ax.set_ylabel("Time to Maturity (Years)")
    ax.set_zlabel("Implied Volatility")
    if title:
        ax.set_title(title)
    else:
        ax.set_title(f"Implied Volatility Surface for {option_type}")
    ax.view_init(elev=elev, azim=azim)

    plt.tight_layout()
    plt.show()