import pandas as pd
import numpy as np

def analyze_jitter(rising_timestamps):
    """
    Calculates jitter between consecutive trigger rising edges.

    Parameters:
        rising_timestamps (pd.Series): List of rising edge timestamps

    Returns:
        pd.Series: Differences between consecutive rising edges (expected to be constant if no jitter)
    """
    diffs = rising_timestamps.diff().dropna()
    jitter = diffs - diffs.mean()
    return jitter

def check_sync_quality(rising_timestamps, measurement_df, verbose=True):
    """
    Verifies if measurement timestamps align well with trigger intervals.

    Parameters:
        rising_timestamps (pd.Series): Trigger rising edge timestamps
        measurement_df (pd.DataFrame): Measurement data with timestamps
        verbose (bool): Print summary or not

    Returns:
        dict: Summary of time alignment stats
    """
    expected_interval = rising_timestamps.diff().dropna().mean()
    actual_intervals = rising_timestamps.diff().dropna()

    jitter_stats = {
        "expected_interval_sec": expected_interval,
        "mean_jitter_sec": actual_intervals.std(),
        "max_jitter_sec": actual_intervals.max() - expected_interval,
        "min_jitter_sec": expected_interval - actual_intervals.min(),
    }

    if verbose:
        print("Jitter Analysis Summary:")
        for k, v in jitter_stats.items():
            print(f"  {k}: {v:.9f} sec")

    return jitter_stats
