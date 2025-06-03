from src.process_trigger import find_rising_edges
from src.process_measurement import compute_mean_per_interval
from src.sync_signals import check_sync_quality
from src.visualize import plot_signals
from src.live_xy_plot import run_live_xy_plot

import os

# -------------------------------------------------------------
# Configuration: Set to True for jitter test, False for standard test
# -------------------------------------------------------------
USE_JITTER = True  # ← Only change this line to switch mode

# -------------------------------------------------------------
# File paths based on test mode
# -------------------------------------------------------------
trigger_path = "data/synthetic_trigger_data.txt"
measurement_path = "data/synthetic_measurement_data.txt"

if USE_JITTER:
    output_path = "data/results/mean_measurements_jitter.csv"
    print("Running jitter test processing...")
else:
    output_path = "data/results/mean_measurements.csv"
    print("Running standard test processing...")

# -------------------------------------------------------------
# Step 1: Detect rising edges in trigger signal
# -------------------------------------------------------------
print("Step 1: Detecting rising edges...")
rising_ts = find_rising_edges(trigger_path)
print(f"Found {len(rising_ts)} rising edges.")

# -------------------------------------------------------------
# Step 2: Analyze jitter between trigger intervals
# -------------------------------------------------------------
print("Step 2: Analyzing jitter between trigger intervals...")
check_sync_quality(rising_ts, None)

# -------------------------------------------------------------
# Step 3: Compute mean and standard deviation per interval
# -------------------------------------------------------------
print("Step 3: Computing statistics for measurement intervals...")
mean_df = compute_mean_per_interval(measurement_path, rising_ts)
print(f"Computed values for {len(mean_df)} intervals.")

# -------------------------------------------------------------
# Step 4: Save results to output file
# -------------------------------------------------------------
print("Step 4: Saving results to file...")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
mean_df.to_csv(output_path, index=False)
print(f"Results saved to: {output_path}")

# -------------------------------------------------------------
# Step 5: Plot the signals for visual confirmation
# -------------------------------------------------------------
print("Step 5: Plotting raw signal, trigger, and mean...")
plot_signals(trigger_path, measurement_path, mean_df, channel="ch1")

# -------------------------------------------------------------
# Step 6 (Optional): Run live x/y visualization
# -------------------------------------------------------------
print("Step 6 (Optional): Running live x/y plot from ch1 and ch2...")
run_live_xy_plot(measurement_path, x_channel="ch1", y_channel="ch2", update_interval=500)