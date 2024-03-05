import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import os


def plot_histograms_from_data(data, directory_path):
    # Define the color mapping for atomic site categories
    categories_colors = {
        "deficiency": "#d62728",             # brick red
        "full_occupancy_atomic_mixing": "#ff7f0e",  # safety orange
        "deficiency_no_atomic_mixing": "#2ca02c",   # cooked asparagus green
        "full_occupancy": "#1f77b4",         # muted blue
    }

    # Prepare for plotting
    num_pairs = len(data)
    max_columns = 4
    num_rows = np.ceil(num_pairs / max_columns).astype(int)
    plt.figure(figsize=(max_columns * 4, num_rows * 3))

    # Collect all distances to establish global bins
    all_distances = [
        record['Distance'] for pair in data.values() for record in pair
    ]
    bins = np.linspace(min(all_distances), max(all_distances), 21)

    # Iterate over each atomic pair and its list of records
    for i, (pair, records) in enumerate(data.items(), start=1):
        # Create a subplot for each atomic pair
        ax = plt.subplot(num_rows, max_columns, i)

        # Prepare the data for the histogram
        stacked_data = []
        labels = []
        for category in categories_colors.keys():
            category_distances = [
                record['Distance'] for record in records if record['Atomic Site'] == category
            ]
            if category_distances:
                stacked_data.append(category_distances)
                labels.append(category)

        # Plot the stacked histogram
        if stacked_data:
            ax.hist(
                stacked_data,
                bins=bins,
                color=[categories_colors[cat] for cat in labels],
                label=labels,
                stacked=True,
                edgecolor='black'
            )

        ax.set_title(f"Distances for {pair}")
        ax.set_xlabel("Distance (Å)")
        ax.set_ylabel("Count")
        ax.legend(loc='upper right')

    plt.tight_layout()

    # Save the figure
    plt.savefig(os.path.join(directory_path, "output", "atomic_pair_histograms.png"), dpi=300)
    plt.close()
