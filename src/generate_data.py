import numpy as np
import pandas as pd
import os

def generate_trigger_signal(frequency=20000, duration_sec=1):
    """
    Generates a TTL trigger signal (0/1 square wave) for the given frequency and duration.

    Parameters:
        frequency (int): Frequency of the trigger signal in Hz (e.g., 20000)
        duration_sec (float): Total duration in seconds (e.g., 1.0)

    Returns:
        pd.DataFrame: Trigger signal with 'timestamp' and 'signal' columns
    """
    t = np.arange(0, duration_sec, 1 / (2 * frequency))  # two samples per period
    signal = np.tile([0, 1], len(t) // 2)
    if len(signal) < len(t):
        signal = np.append(signal, 0)
    return pd.DataFrame({'timestamp': t, 'signal': signal})

def generate_measurement_signal(trigger_frequency=20000, measurement_frequency=200000, duration_sec=1, num_channels=4):
    """
    Generates measurement signal that stays constant for each 50 µs period, matching trigger frequency.
    Each period has a different random voltage value between 0–5V.

    Parameters:
        trigger_frequency (int): Frequency of the trigger signal in Hz
        measurement_frequency (int): Sampling rate of the measurement signal in Hz
        duration_sec (float): Duration of the data in seconds
        num_channels (int): Number of voltage channels to generate

    Returns:
        pd.DataFrame: Measurement signal with 'timestamp' and one column per channel
    """
    total_samples = int(duration_sec * measurement_frequency)
    samples_per_period = int(measurement_frequency / trigger_frequency)

    # Create timestamp vector
    t = np.arange(total_samples) / measurement_frequency

    # Generate per-channel stepwise constant signals
    data = []
    num_periods = int(np.ceil(total_samples / samples_per_period))

    for ch in range(num_channels):
        # Generate random value per period, repeat it for that period
        period_values = np.random.uniform(0, 5, size=num_periods)
        repeated = np.repeat(period_values, samples_per_period)[:total_samples]
        data.append(repeated)

    df = pd.DataFrame(np.array(data).T, columns=[f"ch{i+1}" for i in range(num_channels)])
    df["timestamp"] = t

    # DEBUG: Show sample values
    print(df.head(20))  # Optional: See the first 20 rows for debugging
    return df

def save_synthetic_data(base_path="data"):
    """
    Generates and saves both trigger and measurement signals to the specified data path.
    """
    trigger_df = generate_trigger_signal()
    measurement_df = generate_measurement_signal()

    os.makedirs(base_path, exist_ok=True)
    trigger_df.to_csv(os.path.join(base_path, "synthetic_trigger_data.txt"), sep="\t", index=False)
    measurement_df.to_csv(os.path.join(base_path, "synthetic_measurement_data.txt"), sep="\t", index=False)

    print(f"Synthetic data saved to: {base_path}/")

if __name__ == "__main__":
    save_synthetic_data()
