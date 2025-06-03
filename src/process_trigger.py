import pandas as pd

def find_rising_edges(trigger_path):
    """
    Reads a trigger signal file and detects the timestamps of rising edges.
    A rising edge is defined as a transition from 0 to 1 in a TTL digital signal.

    Parameters:
        trigger_path (str): Path to the trigger signal file (tab-separated .txt)

    Returns:
        pd.Series: A pandas Series containing timestamps where rising edges occur.
    """
    # Read the trigger signal file
    df = pd.read_csv(trigger_path, sep="\t")

    # Detect rising edges: where the previous value is 0 and current value is 1
    rising_edges = df[(df["signal"].shift(1) == 0) & (df["signal"] == 1)]

    # Return just the timestamps
    return rising_edges["timestamp"].reset_index(drop=True)