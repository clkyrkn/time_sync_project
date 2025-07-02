import numpy as np
import pandas as pd
import os

# -------------------------------------------------------------
# Configuration: Set to True to make measurement constant per trigger period
# -------------------------------------------------------------
USE_CONSTANT_MEASUREMENT = True  # ← Change this to False for random noisy signal

def generate_trigger_signal(frequency=20000, duration_sec=1):
    """
    Generates a TTL trigger signal (0/1 square wave) at the given frequency and duration.

    Parameters:
        frequency (int): Trigger signal frequency in Hz
        duration_sec (float): Duration in seconds

    Returns:
        pd.DataFrame: Trigger signal with 'timestamp' and 'signal' columns
    """
    t = np.arange(0, duration_sec, 1 / (2 * frequency))
    signal = np.tile([0, 1], len(t) // 2)
    if len(signal) < len(t):
        signal = np.append(signal, 0)
    return pd.DataFrame({'timestamp': t, 'signal': signal})

def generate_measurement_signal(trigger_frequency=20000, measurement_frequency=200000,
                                duration_sec=1, num_channels=4):
    """
    Generates measurement data for each channel.

    If USE_CONSTANT_MEASUREMENT is True:
        - Each trigger period will contain a constant value
    Else:
        - Each sample point will have a random value (noisy)

    Returns:
        pd.DataFrame: Measurement data with 'timestamp' and channel columns
    """
    total_samples = int(duration_sec * measurement_frequency)
    samples_per_period = int(measurement_frequency / trigger_frequency)
    num_periods = int(np.ceil(total_samples / samples_per_period))
    t = np.arange(total_samples) / measurement_frequency

    data = []
    for ch in range(num_channels):
        if USE_CONSTANT_MEASUREMENT:
            # Same value for all samples in a trigger period
            values = np.repeat(np.random.uniform(0, 5, size=num_periods), samples_per_period)
            values = values[:total_samples]
        else:
            # Different random value at every sample point
            values = np.random.uniform(0, 5, size=total_samples)
        data.append(values)

    df = pd.DataFrame(np.array(data).T, columns=[f"ch{i+1}" for i in range(num_channels)])
    df["timestamp"] = t

    # Debug check
    print(df[["timestamp", "ch1"]].head(20))  # verify visually

    return df

def save_synthetic_data(base_path="data"):
    """
    Generates and saves both trigger and measurement signals to files.
    """
    trigger_df = generate_trigger_signal()
    measurement_df = generate_measurement_signal()

    os.makedirs(base_path, exist_ok=True)
    trigger_df.to_csv(os.path.join(base_path, "synthetic_trigger_data.txt"), sep="\t", index=False)
    measurement_df.to_csv(os.path.join(base_path, "synthetic_measurement_data.txt"), sep="\t", index=False)

    print("Synthetic data saved to:", base_path)

if __name__ == "__main__":
    save_synthetic_data()
