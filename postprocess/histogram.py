import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os

def plot_histograms(unique_pairs_distances, directory_path):
    """
    Generates and saves histograms for the distribution of distances for each unique atomic pair.

    Parameters:
    - unique_pairs_distances: A dictionary with keys as atomic pairs and values as lists of distances.
    - directory_path: The path to the directory where the histogram image will be saved.
    """

    # Determine the number of histograms to be plotted
    num_pairs = len(unique_pairs_distances)

    # Set the maximum number of columns as 4
    max_columns = 4

    # Calculate the number of rows based on the number of pairs and maximum columns
    num_rows = -(-num_pairs // max_columns)  # Ceiling division to ensure we have enough rows

    # Adjust the figure size to allow for extending the size vertically. Each subplot is approximately 4x3 inches.
    plt.figure(figsize=(max_columns * 4, num_rows * 3))

    # Go through each unique pair
    for i, (pair, distances) in enumerate(unique_pairs_distances.items()):
        distances = [float(dist) for dist in distances]  # Convert distances to float

        # Compute the mean and standard deviation of the distances
        mean_value = np.mean(distances)
        std_value = np.std(distances)

        # Create a new subplot for each histogram
        plt.subplot(num_rows, max_columns, i + 1)
        plt.hist(distances, bins=20, color='steelblue', edgecolor='black')
        plt.axvline(x=mean_value, color='red', linestyle='dashed', label=f"Mean: {mean_value:.4f}\nStd Dev: {std_value:.4f}")
        lower_bound = mean_value - 3 * std_value
        upper_bound = mean_value + 3 * std_value
        plt.xlim([lower_bound, upper_bound])

        # Set x-axis tick size to exactly 4 tickers
        plt.gca().xaxis.set_major_locator(ticker.LinearLocator(numticks=5))
        plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%1.3f'))  # Display up to third decimal place

        # Ensure y-axis has integer ticks
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        plt.xlabel(f"Distance (Å): {pair[0].strip()}-{pair[1].strip()}")
        plt.ylabel("Count")
        plt.legend()

    plt.tight_layout(pad=3.0)  # Increase padding
    file_path = os.path.join(directory_path, "output", "histograms.png")
    plt.savefig(file_path, dpi=300)
    print(f"\n{os.path.basename(file_path)} saved")
