"""
Plot histograms for atomic pair dists from dict and save the plots.
(Refactoring will occcur once test results are confirmed)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np


def get_histogram_config():
    """
    Configure the maximum number of histograms per image.
    """

    max_columns = 4
    histograms_per_image = 16

    return histograms_per_image, max_columns


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
        "1": "Deficiency",
        "2": "Full occupancy & atomic mixing",
        "3": "Deficiency & no atomic mixing",
        "4": "Full occupancy",
    }

    return categories_colors, categories_mapping


def plot_element_pair_histograms(data, directory_path):
    """
    Plot histograms for atomic pair distances from dict and save the plots.
    """
    # Prepare the legend handles manually, in the desired order
    (
        categories_colors,
        categories_mapping,
    ) = get_colors_category_mappings()
    histograms_per_image, max_columns = get_histogram_config()

    # Sort the categories based on the keys in reverse order
    ordered_keys = sorted(categories_colors.keys(), reverse=True)
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=categories_colors[cat])
        for cat in ordered_keys
    ]
    legend_labels = [categories_mapping[cat] for cat in ordered_keys]

    # Calculate total number of images needed
    num_pairs = len(data)
    total_images = np.ceil(num_pairs / histograms_per_image).astype(int)
    element_pairs = list(data.items())

    for image_num in range(total_images):
        start_index = image_num * histograms_per_image
        end_index = min((image_num + 1) * histograms_per_image, num_pairs)
        current_pairs = element_pairs[start_index:end_index]

        # Prepare for plotting with a fixed grid of subplots
        num_rows = np.ceil(histograms_per_image / max_columns).astype(int)
        fig, axes = plt.subplots(
            num_rows,
            max_columns,
            figsize=(max_columns * 4, num_rows * 3),
        )
        axes = axes.flatten()

        # Collect all distances to establish global bins
        distances = []
        for _, records in current_pairs:
            for infos in records.values():
                for info in infos:
                    distances.append(float(info["dist"]))

        all_distances = sorted(distances)
        bins = np.linspace(min(all_distances), max(all_distances), 21)

        # Plot data on the corresponding subplot, leave the rest empty
        for i in range(histograms_per_image):
            if i < len(current_pairs):
                atomic_pair, records = current_pairs[i]
                ax = axes[i]
                ax.set_title(atomic_pair)

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
                ax.yaxis.set_major_locator(mticker.MultipleLocator(1))
            else:
                axes[i].set_visible(False)

        # Create the global legend with manual handles
        fig.legend(
            legend_handles,
            legend_labels,
            loc="lower center",
            ncol=len(legend_labels),
            bbox_to_anchor=(0.5, 0.02),
        )

        # Adjust layout
        plt.tight_layout(rect=[0, 0.05, 1, 1])

        # Save the figure
        output_dir = os.path.join(directory_path, "output")
        os.makedirs(output_dir, exist_ok=True)
        fig.savefig(
            os.path.join(
                output_dir,
                f"histogram_element_pair_{image_num + 1}.png",
            ),
            dpi=150,
        )
        plt.close(fig)


def plot_site_pair_histograms(data, directory_path):
    """
    Plot histograms for atomic pair distances from dict and save the plots.
    """
    # Prepare the legend handles manually, in the desired order
    (
        categories_colors,
        categories_mapping,
    ) = get_colors_category_mappings()
    histograms_per_image, max_columns = get_histogram_config()

    # Sort the categories based on the keys in reverse order
    ordered_keys = sorted(categories_colors.keys(), reverse=True)
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=categories_colors[cat])
        for cat in ordered_keys
    ]
    legend_labels = [categories_mapping[cat] for cat in ordered_keys]

    # Calculate total number of images needed
    num_pairs = len(data)
    total_images = np.ceil(num_pairs / histograms_per_image).astype(int)
    element_pairs = list(data.items())

    for image_num in range(total_images):
        start_index = image_num * histograms_per_image
        end_index = min((image_num + 1) * histograms_per_image, num_pairs)
        current_pairs = element_pairs[start_index:end_index]

        # Prepare for plotting with a fixed grid of subplots
        num_rows = np.ceil(histograms_per_image / max_columns).astype(int)
        fig, axes = plt.subplots(
            num_rows,
            max_columns,
            figsize=(max_columns * 4, num_rows * 3),
        )
        axes = axes.flatten()

        # Collect all distances to establish global bins
        distances = []
        for _, records in current_pairs:
            for infos in records.values():
                for info in infos:
                    distances.append(float(info["dist"]))

        all_distances = sorted(distances)
        bins = np.linspace(min(all_distances), max(all_distances), 21)

        # Plot data on the corresponding subplot, leave the rest empty
        for i in range(histograms_per_image):
            if i < len(current_pairs):
                atomic_pair, records = current_pairs[i]
                ax = axes[i]
                ax.set_title(atomic_pair)

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
                ax.yaxis.set_major_locator(mticker.MultipleLocator(1))
            else:
                axes[i].set_visible(False)

        # Create the global legend with manual handles
        fig.legend(
            legend_handles,
            legend_labels,
            loc="lower center",
            ncol=len(legend_labels),
            bbox_to_anchor=(0.5, 0.02),
        )

        # Adjust layout
        plt.tight_layout(rect=[0, 0.05, 1, 1])

        # Save the figure
        output_dir = os.path.join(directory_path, "output")
        os.makedirs(output_dir, exist_ok=True)
        fig.savefig(
            os.path.join(
                output_dir, f"histogram_site_pair_{image_num + 1}.png"
            ),
            dpi=150,
        )
        plt.close(fig)
