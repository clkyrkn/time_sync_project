# Software-Based Time Synchronization Project

This project implements a software-based approach to synchronize a high-speed measurement signal with a trigger signal. It includes the generation of synthetic test data, analysis and visualization tools, and a live view module for real-time signal inspection.

---

## Purpose

- Simulate a real-time measurement setup with a **trigger signal** and a **measurement signal**.
- Synchronize measurement data based on trigger timestamps (rising edges).
- Compute **mean and standard deviation** of measurements within each trigger period.
- Visualize results and test **jitter sensitivity**.
- Display a **live x/y plot** of two selected measurement channels.

---

## Folder Structure

```
Benedikt/
├── main.py
├── data/
│   ├── synthetic_trigger_data.txt
│   ├── synthetic_measurement_data.txt
│   └── results/
│       ├── mean_measurements.csv
│       └── mean_measurements_jitter.csv
└── src/
    ├── generate_data.py
    ├── generate_variable_data.py
    ├── process_trigger.py
    ├── process_measurement.py
    ├── sync_signals.py
    ├── visualize.py
    └── live_xy_plot.py
```

---

## Modules Overview

### `main.py`
Main entry point. Controls the full synchronization pipeline.  
Set `USE_JITTER = True/False` to switch between normal and jitter tests.

### `generate_data.py`
Creates synthetic trigger and measurement signals at fixed 20 kHz frequency.

### `generate_variable_data.py`
Creates jitter test data with varying trigger frequencies (18–22 kHz).

### `process_trigger.py`
Detects **rising edges** in the trigger signal and returns time stamps.

### `process_measurement.py`
Computes **mean and standard deviation** for each trigger-defined interval.

### `sync_signals.py`
Analyzes **jitter** between trigger intervals for validation and debugging.

### `visualize.py`
Plots the **raw signal**, **trigger**, and **computed mean** values on the same chart.

### `live_xy_plot.py`
Creates a **live animated x/y plot** using `ch1` and `ch2` values, updated every 0.5s.

---

## Test Scenarios

### Standard Test
- Fixed 20 kHz trigger signal.
- Each 50 µs contains constant measurement values.
- Standard deviation should be **0**.
- Result saved to `mean_measurements.csv`.

### Jitter Test
- Trigger frequency varies randomly between 18–22 kHz.
- Measurement values change in sync with jittered trigger.
- Tests the robustness of the synchronization algorithm.
- Result saved to `mean_measurements_jitter.csv`.
