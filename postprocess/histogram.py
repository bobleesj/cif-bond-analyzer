import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os
import util.folder

def plot_histograms(unique_pairs_distances, directory_path):
    """
    Generates and saves histograms for the distribution of distances for each unique atomic pair.

    Parameters:
    - unique_pairs_distances: A dictionary with keys as atomic pairs and values as lists of distances.
    - directory_path: The path to the directory where the histogram image will be saved.
    """

    # Prepare the subplots grid. It's a square grid that has enough cells to hold all histograms.
    grid_size = int(len(unique_pairs_distances)**0.5)
    if grid_size**2 < len(unique_pairs_distances):
        grid_size += 1

    # Set the figure size
    plt.figure(figsize=(15, 10))

    # Go through each unique pair
    for i, (pair, distances) in enumerate(unique_pairs_distances.items()):
        distances = [float(dist) for dist in distances]  # Convert distances to float

        # Compute the mean and standard deviation of the distances
        mean_value = np.mean(distances)
        std_value = np.std(distances)

        # Create a new subplot for each histogram
        plt.subplot(grid_size, grid_size, i + 1)
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
    