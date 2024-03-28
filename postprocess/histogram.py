"""
Plot histograms for atomic pair dists from dict and save the plots.
(Refactoring will occcur once test results are confirmed)
"""

import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

def get_histogram_config():
    """
    Configure the maximum number of histograms per image.
    """

    max_columns = 4
    histograms_per_image = 16
    bin_width = 0.10 # Å

    return histograms_per_image, max_columns, bin_width


def get_colors_category_mappings():
    """
    Get colors and atomic mixing mapping info.
    """
    categories_colors = {
        "1": "#d62728",  # brick red
        "2": "#ff7f0e",  # safety orange
        "3": "#2ca02c",  # cooked asparagus green
        "4": "#1f77b4",  # muted blue
    }

    categories_mapping = {
        "1": "Deficiency with atomic mixing",
        "2": "Full occupancy with atomic mixing",
        "3": "Deficiency without atomic mixing",
        "4": "Full occupancy",
    }

    return categories_colors, categories_mapping

def get_bins_from_distances(bin_width, all_distances):
    data_range = max(all_distances) - min(all_distances)
    bin_size = int(np.ceil(data_range / bin_width))
    bins = np.linspace(min(all_distances), max(all_distances), bin_size + 1)
    return bins


def plot_histograms(data, directory_path, output_filename):
    categories_colors, categories_mapping = get_colors_category_mappings()
    histograms_per_image, max_columns, bin_width = get_histogram_config()

    # Specify the desired order for legend
    ordered_keys = ["4", "2", "1", "3"]
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=categories_colors[cat])
        for cat in ordered_keys
    ]
    legend_labels = [categories_mapping[cat] for cat in ordered_keys]

    num_pairs = len(data)
    total_images = np.ceil(num_pairs / histograms_per_image).astype(int)
    element_pairs = list(data.items())

    all_distances = []
    for _, records in element_pairs:
        for infos in records.values():
            for info in infos:
                all_distances.append(float(info["dist"]))
    
    bins = get_bins_from_distances(bin_width, all_distances)
    # If bin_size is 20, then it evenly divides into 20 within the range
    # bins = np.linspace(min(all_distances), max(all_distances), bin_size)

    for image_num in range(total_images):
        start_index = image_num * histograms_per_image
        end_index = min((image_num + 1) * histograms_per_image, num_pairs)
        current_pairs = element_pairs[start_index:end_index]

        num_rows = np.ceil(histograms_per_image / max_columns).astype(int)
        fig, axes = plt.subplots(
            num_rows, max_columns, figsize=(max_columns * 4, num_rows * 3)
        )
        axes = axes.flatten()

        max_count = 0  # Keep track of the maximum count for y-tick adjustment
        for i in range(histograms_per_image):
            if i < len(current_pairs):
                pair_key, records = current_pairs[i]
                ax = axes[i]
                ax.set_title(pair_key)

                stacked_data = []
                labels = []
                for cat, color in categories_colors.items():
                    category_distances = [
                        float(info["dist"])
                        for infos in records.values()
                        for info in infos
                        if info["mixing"] == cat
                    ]
                    if category_distances:
                        stacked_data.append(category_distances)
                        labels.append(cat)
                        max_count = max(
                            max_count, len(category_distances)
                        )  # Update max_count

                if stacked_data:
                    ax.hist(
                        stacked_data,
                        bins=bins,
                        color=[categories_colors[cat] for cat in labels],
                        label=[categories_mapping[cat] for cat in labels],
                        stacked=True,
                        edgecolor="black",
                    )
                ax.set_xlabel("Distance (Å)")
                ax.set_ylabel("Count")
                ax.yaxis.set_major_locator(MaxNLocator(integer=True))

            else:
                axes[i].set_visible(False)

        # Adjust the y-axis tick interval based on the max_count
        for ax in axes:
            ax.yaxis.set_major_locator(
                MaxNLocator(nbins=4, integer=True)
            )  # Adjust 'nbins' as needed

        fig.legend(
            legend_handles,
            legend_labels,
            loc="lower center",
            ncol=len(legend_labels),
            bbox_to_anchor=(0.5, 0.02),
        )
        plt.tight_layout(rect=[0, 0.05, 1, 1])

        output_dir = os.path.join(directory_path, "output")
        os.makedirs(output_dir, exist_ok=True)
        fig.savefig(
            os.path.join(output_dir, f"{output_filename}_{image_num + 1}.png"),
            dpi=150,
        )
        plt.close(fig)


def plot_element_pair_histograms(data, directory_path):
    plot_histograms(data, directory_path, "histogram_element_pair")


def plot_site_pair_histograms(data, directory_path):
    plot_histograms(data, directory_path, "histogram_site_pair")
