import pandas as pd
import matplotlib.pyplot as plt

def plot_signals(trigger_path, measurement_path, result_df, channel="ch1", zoom=True):
    """
    Plots raw measurement, trigger signal, and mean per interval for a given channel.

    Parameters:
        trigger_path (str): Path to the trigger data file
        measurement_path (str): Path to the measurement data file
        result_df (pd.DataFrame): Mean/std data per interval
        channel (str): Channel to plot (e.g. 'ch1')
        zoom (bool): If True, zoom into the first few milliseconds
    """
    # Load the data
    trigger = pd.read_csv(trigger_path, sep="\t")
    measurement = pd.read_csv(measurement_path, sep="\t")

    plt.figure(figsize=(12, 6))

    # Plot raw measurement
    plt.plot(measurement["timestamp"], measurement[channel], label=f"{channel} (raw)", alpha=0.5, color='red')

    # Plot trigger signal (scaled for visibility)
    plt.plot(trigger["timestamp"], trigger["signal"] * 5, label="Trigger (scaled)", color='gray', linewidth=0.5)

    # Plot calculated mean values per interval
    plt.step(result_df["interval_start"], result_df[f"{channel}_mean"], label="Mean per interval", color='black', linewidth=1.5)

    # Labels and formatting
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title(f"{channel}: Raw vs Mean vs Trigger")
    plt.legend()
    plt.grid(True)

    # Optional zoom for better visibility
    if zoom:
        plt.xlim(0, 0.005)  # Zoom into first 5 milliseconds

    plt.tight_layout()
    plt.show()
