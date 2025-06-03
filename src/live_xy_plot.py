import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def run_live_xy_plot(measurement_path="data/synthetic_measurement_data.txt", x_channel="ch1", y_channel="ch2", update_interval=500):
    """
    Displays a live x-y plot that updates every 0.5 seconds (default).
    Each point is taken from the latest value in the measurement data.

    Parameters:
        measurement_path (str): Path to the measurement data file
        x_channel (str): Channel name for x-axis
        y_channel (str): Channel name for y-axis
        update_interval (int): Update time in milliseconds (default = 500 ms)
    """
    # Load data
    df = pd.read_csv(measurement_path, sep="\t")

    # Set up plot
    fig, ax = plt.subplots()
    scatter, = ax.plot([], [], 'bo')

    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_xlabel(f"{x_channel} (V)")
    ax.set_ylabel(f"{y_channel} (V)")
    ax.set_title("Live x/y Voltage Plot")
    plt.grid(True)
    plt.tight_layout()

    # Define update function WITH ACCESS to df and scatter
    def update(frame):
        if frame >= len(df):
            return scatter,
        x = df[x_channel].iloc[frame]
        y = df[y_channel].iloc[frame]
        scatter.set_data([x], [y])  # use lists
        return scatter,

    # Create animation
    ani = animation.FuncAnimation(fig, update, frames=len(df), interval=update_interval, blit=True)

    # Show the animation
    plt.show()
