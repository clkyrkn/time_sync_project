import pandas as pd

def compute_mean_per_interval(measurement_path, rising_timestamps):
    """
    For each interval defined by two consecutive rising edge timestamps,
    compute the mean and standard deviation of voltage values from the measurement data.

    Parameters:
        measurement_path (str): Path to the measurement data file (tab-separated .txt)
        rising_timestamps (pd.Series): Series of timestamps marking rising edges

    Returns:
        pd.DataFrame: A DataFrame containing average and standard deviation values per interval,
                      as well as interval start and end times.
    """
    # Read the measurement data
    df = pd.read_csv(measurement_path, sep="\t")

    results = []

    for i in range(len(rising_timestamps) - 1):
        start = rising_timestamps[i]
        end = rising_timestamps[i + 1]

        # Extract data within this trigger interval
        interval_data = df[(df["timestamp"] >= start) & (df["timestamp"] < end)]

        # Skip empty intervals (important for clean statistics)
        if interval_data.empty:
            continue

        # Compute mean and std across channels
        mean = interval_data[["ch1", "ch2", "ch3", "ch4"]].mean()
        std = interval_data[["ch1", "ch2", "ch3", "ch4"]].std()

        # Handle any potential NaNs (e.g. std on single-value intervals)
        std = std.fillna(0)

        # Build result row
        result = {
            "interval_start": start,
            "interval_end": end,
            **{f"{col}_mean": mean[col] for col in mean.index},
            **{f"{col}_std": std[col] for col in std.index}
        }

        results.append(result)

    return pd.DataFrame(results)
