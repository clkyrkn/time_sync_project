import numpy as np
import pandas as pd
import os

def generate_variable_trigger_signal(f_min=18000, f_max=22000, duration_sec=1):
    """
    Generates a trigger signal with varying frequency between f_min and f_max.

    Parameters:
        f_min (int): Minimum frequency in Hz
        f_max (int): Maximum frequency in Hz
        duration_sec (float): Total duration in seconds

    Returns:
        pd.DataFrame: DataFrame with columns ['timestamp', 'signal']
    """
    timestamps = []
    signal = []
    t = 0.0
    state = 0

    while t < duration_sec:
        freq = np.random.uniform(f_min, f_max)
        period = 1 / freq
        timestamps.append(t)
        signal.append(state)
        state = 1 - state
        t += period / 2  # toggle every half period

    return pd.DataFrame({'timestamp': timestamps, 'signal': signal})

def generate_variable_measurement_signal(trigger_df, measurement_frequency=200000, num_channels=4):
    """
    Generates measurement data synchronized to variable trigger intervals.
    Each interval has constant random voltage values.

    Parameters:
        trigger_df (pd.DataFrame): Trigger data with timestamps and signal (0/1)
        measurement_frequency (int): Sampling rate of the measurement signal
        num_channels (int): Number of measurement channels

    Returns:
        pd.DataFrame: DataFrame with 'timestamp' and channel voltage columns
    """
    rising_edges = trigger_df[(trigger_df["signal"].shift(1) == 0) & (trigger_df["signal"] == 1)]["timestamp"].values

    timestamps = []
    data = [[] for _ in range(num_channels)]

    for i in range(len(rising_edges) - 1):
        start = rising_edges[i]
        end = rising_edges[i + 1]
        n_samples = int((end - start) * measurement_frequency)
        if n_samples <= 0:
            continue

        interval_timestamps = np.linspace(start, end, n_samples, endpoint=False)
        for ch in range(num_channels):
            value = np.random.uniform(0, 5)
            data[ch].extend([value] * n_samples)
        timestamps.extend(interval_timestamps)

    df = pd.DataFrame({f"ch{i+1}": data[i] for i in range(num_channels)})
    df["timestamp"] = timestamps
    return df

def save_variable_synthetic_data(base_path="data"):
    """
    Creates and saves variable-frequency trigger and matching measurement data.
    """
    trigger_df = generate_variable_trigger_signal()
    measurement_df = generate_variable_measurement_signal(trigger_df)

    os.makedirs(base_path, exist_ok=True)
    trigger_df.to_csv(os.path.join(base_path, "synthetic_trigger_data.txt"), sep="\t", index=False)
    measurement_df.to_csv(os.path.join(base_path, "synthetic_measurement_data.txt"), sep="\t", index=False)

    print("Variable synthetic data generated and saved to:", base_path)

if __name__ == "__main__":
    save_variable_synthetic_data()
