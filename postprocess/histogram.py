"""Plot histograms for atomic pair dists from dict and save the plots."""

import os
import matplotlib.pyplot as plt
import numpy as np


def plot_histograms_from_data(data, directory_path):
    """
    Plot histograms for atomic pair dists from dict and save the plots.
    """
    # Define the color mapping for atomic site categories

    categories_colors = {
        "1": "#d62728",  # brick red
        "2": "#ff7f0e",  # safety orange
        "3": "#2ca02c",  # cooked asparagus green
        "4": "#1f77b4",  # muted blue
    }

    # Prepare for plotting
    num_pairs = len(data)
    max_columns = 4
    num_rows = np.ceil(num_pairs / max_columns).astype(int)
    plt.figure(figsize=(max_columns * 4, num_rows * 3))

    # Collect all distances to establish global bins
    distances = []
    for key in data:
        for sub_key in data[key]:
            distances.append(float(data[key][sub_key]["dist"]))

    all_distances = sorted(distances)
    bins = np.linspace(min(all_distances), max(all_distances), 21)

    # Iterate over each atomic pair and its list of records
    for i, (atomic_pair, pair_info) in enumerate(data.items(), start=1):
        # Create a subplot for each atomic pair
        ax = plt.subplot(num_rows, max_columns, i)
        ax.set_title(atomic_pair)

        # Prepare the data for the histogram
        stacked_data = []
        labels = []
        for category, _ in categories_colors.items():
            category_distances = [
                float(pair_info["dist"]) for sub_key, 
                pair_info in pair_info.items() if pair_info["mixing"] == category
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

        ax.set_title(atomic_pair)
        ax.set_xlabel("Distance (Å)")
        ax.set_ylabel("Count")
        ax.legend(loc='upper right')

    plt.tight_layout()
    plt.savefig(os.path.join(
        directory_path,
        "output", "atomic_pair_histograms.png"), dpi=150)

    plt.close()
