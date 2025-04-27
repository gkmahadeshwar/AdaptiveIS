import numpy as np
import pandas as pd

def regular_importance_sampling(df, n_samples, random_state=42):
    """Uniform random sampling"""
    sampled_df = df.sample(n=n_samples, random_state=random_state)
    return sampled_df

def adaptive_importance_sampling(df, n_samples, importance_col, random_state=42, clip_quantile=0.999):
    """
    Adaptive importance sampling from a specified importance column.
    
    Args:
        df (pd.DataFrame): Your input data
        n_samples (int): Number of samples to draw
        importance_col (str): Name of the column to base importance weights on
        random_state (int): Seed for reproducibility
        clip_quantile (float): To avoid overskewed weighting (clip very large weights)
    
    Returns:
        pd.DataFrame: Sampled dataframe
    """
    df = df.copy()
    
    # Normalize the specified column for importance weights
    weights = df[importance_col].values.clip(min=0)
    weights = weights / weights.sum()

    # Optionally clip heavy peaks
    max_weight = np.quantile(weights, clip_quantile)
    weights = np.clip(weights, 0, max_weight)
    weights /= weights.sum()

    sampled_indices = np.random.choice(
        df.index,
        size=n_samples,
        replace=False,
        p=weights
    )
    sampled_df = df.loc[sampled_indices].copy()
    return sampled_df

def sequential_importance_sampling(df, n_batches, batch_size, importance_col, random_state=42):
    """
    Sequential sampling based on a dynamic importance column.
    
    Args:
        df (pd.DataFrame): Input data
        n_batches (int): Number of sampling rounds
        batch_size (int): Number of samples per round
        importance_col (str): Column to define sampling importance
        random_state (int): Seed
    
    Returns:
        pd.DataFrame: Combined sampled dataframe across all batches
    """
    df = df.copy()
    samples = []
    np.random.seed(random_state)

    for _ in range(n_batches):
        weights = df[importance_col].values.clip(min=0)
        if weights.sum() == 0:
            break
        weights = weights / weights.sum()
        
        sampled_indices = np.random.choice(
            df.index,
            size=min(batch_size, df.shape[0]),
            replace=False,
            p=weights
        )
        sampled_batch = df.loc[sampled_indices].copy()
        samples.append(sampled_batch)

        # Remove sampled points
        df.drop(index=sampled_indices, inplace=True)

        if df.empty:
            break

    return pd.concat(samples, ignore_index=True)