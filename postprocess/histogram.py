"""
Plot histograms for atomic pair dists from dict and save the plots.
(Refactoring will occcur once test results are confirmed)
"""

import os
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
import numpy as np
import os

def plot_histograms_from_label_dict(data, directory_path):
    """
    Plot histograms for atomic pair dists from dict and save the plots.
    """
    categories_colors = {
        "1": "#d62728",
        "2": "#ff7f0e",
        "3": "#2ca02c",
        "4": "#1f77b4",
    }

    categories_mapping = {
        "1": "Deficiency",
        "2": "Full occupancy & atomic mixing",
        "3": "Deficiency & noatomic mixing",
        "4": "Full occupancy",
    }

    # Calculate total number of images
    num_pairs = len(data)
    histograms_per_image = 16
    total_images = np.ceil(num_pairs / histograms_per_image).astype(int)
    pair_list = list(data.items())

    for image_num in range(total_images):
        start_index = image_num * histograms_per_image
        end_index = min((image_num + 1) * histograms_per_image, num_pairs)
        current_pairs = pair_list[start_index:end_index]

        # Prepare for plotting
        num_rows = np.ceil(len(current_pairs) / 4).astype(int)
        plt.figure(figsize=(16, num_rows * 3))

        # Collect all distances to establish global bins
        distances = []
        for _, pair_info in current_pairs:
            for sub_key in pair_info:
                distances.append(float(pair_info[sub_key]["dist"]))
        
        all_distances = sorted(distances)
        bins = np.linspace(min(all_distances), max(all_distances), 21)

        for i, (atomic_pair, pair_info) in enumerate(current_pairs, start=1):
            ax = plt.subplot(num_rows, 4, i)
            ax.set_title(atomic_pair)

            stacked_data = []
            labels = []
            for cat, _ in categories_colors.items():
                category_distances = [
                    float(info["dist"])
                    for sub_key, info in pair_info.items()
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
            ax.legend(loc="upper right")

        plt.tight_layout()
        plt.savefig(
            os.path.join(directory_path, "output", f"histogram_label_pair_{image_num + 1}.png"),
            dpi=150,
        )
        plt.close()


def plot_histograms_from_element_dict(data, directory_path):
    """
    Plot histograms for atomic pair distances from dict and save the plots.
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

    # Calculate total number of images needed
    num_pairs = len(data)
    histograms_per_image = 16
    total_images = np.ceil(num_pairs / histograms_per_image).astype(int)
    element_pairs = list(data.items())

    for image_num in range(total_images):
        start_index = image_num * histograms_per_image
        end_index = min((image_num + 1) * histograms_per_image, num_pairs)
        current_pairs = element_pairs[start_index:end_index]

        # Prepare for plotting
        max_columns = 4
        num_rows = np.ceil(len(current_pairs) / max_columns).astype(int)
        plt.figure(figsize=(max_columns * 4, num_rows * 3))

        # Collect all distances to establish global bins
        distances = []
        for _, records in current_pairs:
            for infos in records.values():
                for info in infos:
                    distances.append(float(info["dist"]))
        
        all_distances = sorted(distances)
        bins = np.linspace(min(all_distances), max(all_distances), 21)

        for i, (atomic_pair, records) in enumerate(current_pairs, start=1):
            ax = plt.subplot(num_rows, max_columns, i)
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
            ax.legend(loc="upper right")

        plt.tight_layout()
        output_dir = os.path.join(directory_path, "output")
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(
            os.path.join(output_dir, f"histogram_element_{image_num + 1}.png"), dpi=150
        )
        plt.close()