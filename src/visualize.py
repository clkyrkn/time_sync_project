import pandas as pd
import matplotlib.pyplot as plt

def improved_plot_signals(trigger_path, measurement_path, result_path, channel="ch1", zoom=True):
    """
    Enhanced visualization of signal synchronization:
    - Trigger signal plotted as a TTL square wave using step plot
    - Raw measurement data plotted transparently
    - Mean values plotted as discrete dots
    - Standard deviation visualized as error bars

    Parameters:
        trigger_path (str): Path to the trigger signal file (tab-separated .txt)
        measurement_path (str): Path to the measurement data file (tab-separated .txt)
        result_path (str): Path to the result file containing mean and std values
        channel (str): The measurement channel to visualize (e.g., "ch1")
        zoom (bool): Whether to zoom in on the first 10 ms of data
    """
    # Load data
    trigger = pd.read_csv(trigger_path, sep="\t")
    measurement = pd.read_csv(measurement_path, sep="\t")
    result_df = pd.read_csv(result_path)

    # Column names for mean and std
    mean_col = f"{channel}_mean"
    std_col = f"{channel}_std"

    # Initialize plot
    plt.figure(figsize=(12, 6))

    # Plot raw measurement signal
    plt.plot(measurement["timestamp"], measurement[channel], label=f"{channel} (raw)", color='red', alpha=0.4)

    # Plot trigger as square wave
    plt.step(trigger["timestamp"], trigger["signal"] * 5, label="Trigger (scaled)", color='gray', linewidth=0.7, where='post')

    # Calculate the center of each interval (midpoint between start and end)
    interval_center = (result_df["interval_start"] + result_df["interval_end"]) / 2

    # Plot the mean value as dots at the center of each interval
    plt.scatter(interval_center, result_df[mean_col],
                label="Mean per interval", color='black', s=10, zorder=3)

    # Plot the standard deviation as vertical error bars centered on each interval
    plt.errorbar(interval_center, result_df[mean_col],
                yerr=result_df[std_col], fmt='none', ecolor='blue',
                elinewidth=1, capsize=2, label="Standard deviation")

    # Axis labels and plot settings
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title(f"{channel}: Raw Signal, Trigger, Mean & Std Deviation")
    plt.legend()
    plt.grid(True)

    if zoom:
        plt.xlim(0, 0.01)  # zoom into first 10 ms

    plt.tight_layout()
    plt.show()
