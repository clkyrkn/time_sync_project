import pandas as pd

def compute_mean_per_interval(measurement_path, rising_timestamps):
    """
    For each interval defined by two consecutive rising edge timestamps,
    compute the mean and standard deviation of voltage values from the measurement data.

    Parameters:
        measurement_path (str): Path to the measurement data file (tab-separated .txt)
        rising_timestamps (pd.Series): Series of timestamps marking rising edges

    Returns:
        pd.DataFrame: DataFrame with average and standard deviation values per interval,
                      along with start and end times.
    """
    # Read the measurement data
    df = pd.read_csv(measurement_path, sep="\t")

    results = []

    # Iterate over intervals defined by rising edges
    for i in range(len(rising_timestamps) - 1):
        start = rising_timestamps[i]
        end = rising_timestamps[i + 1]

        # Filter data within the current interval
        interval_data = df[(df["timestamp"] >= start) & (df["timestamp"] < end)]

        # Compute mean and std for each channel
        mean = interval_data[["ch1", "ch2", "ch3", "ch4"]].mean()
        std = interval_data[["ch1", "ch2", "ch3", "ch4"]].std()

        # Combine into one row
        result = {
            "interval_start": start,
            "interval_end": end,
            **{f"{col}_mean": mean[col] for col in mean.index},
            **{f"{col}_std": std[col] for col in std.index}
        }

        results.append(result)

    return pd.DataFrame(results)
