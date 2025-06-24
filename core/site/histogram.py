"""Plot histograms for atomic pair dists from dict and save the
plots."""

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator


def get_histogram_config():
    """Configure the maximum number of histograms per image."""

    max_columns = 4
    histograms_per_image = 16
    bin_width = 0.10  # Å

    config = {
        "histograms_per_image": histograms_per_image,
        "max_columns": max_columns,
        "bin_width": bin_width,
    }

    return config


def get_colors_category_mappings():
    """Get colors and atomic mixing mapping info."""
    categories_colors = {
        "deficiency_with_atomic_mixing": "#d62728",  # brick red
        "full_occupancy_atomic_mixing": "#ff7f0e",  # safety orange
        "deficiency_without_atomic_mixing": "#2ca02c",  # cooked asparagus green
        "full_occupancy": "#1f77b4",  # muted blue
    }

    categories_mapping = {
        "deficiency_with_atomic_mixing": "Deficiency with atomic mixing",
        "full_occupancy_atomic_mixing": "Full occupancy with atomic mixing",
        "deficiency_without_atomic_mixing": "Deficiency without atomic mixing",
        "full_occupancy": "Full occupancy",
    }

    return categories_colors, categories_mapping


def draw_histograms(site_pair_dict, element_pair_dict, dir_path):
    """Draw histograms using site pair and element pair dicts."""
    all_distances = get_distances_from_site_pair(site_pair_dict)
    config = get_histogram_config()
    bin_width = config["bin_width"]
    bins = get_bins_from_distances(bin_width, all_distances)

    plot_histograms(
        site_pair_dict,
        dir_path,
        bins,
        all_distances,
        "histogram_site_pair",
    )
    plot_histograms(
        element_pair_dict,
        dir_path,
        bins,
        all_distances,
        "histogram_element_pair",
    )


def get_distances_from_site_pair(data):
    """Get all distances from the site pair dict."""
    element_pairs = list(data.items())

    all_distances = []
    for _, records in element_pairs:
        for infos in records.values():
            for info in infos:
                all_distances.append(float(info["dist"]))

    return all_distances


def get_bins_from_distances(bin_width, all_distances):
    """Get bin information from bin width and distances."""
    data_range = max(all_distances) - min(all_distances)
    bin_size = int(np.ceil(data_range / bin_width))
    bins = np.linspace(min(all_distances), max(all_distances), bin_size + 1)
    return bins


def get_dist_fig_text(all_distances):
    min_dist = np.round(min(all_distances), 2)
    max_dist = np.round(max(all_distances), 2)
    return f"Distance range: {min_dist}-{max_dist} Å"


def plot_histograms(data, dir_path, bins, all_distances, output_filename):
    (
        categories_colors,
        categories_mapping,
    ) = get_colors_category_mappings()
    config = get_histogram_config()
    histograms_per_image = config["histograms_per_image"]
    max_columns = config["max_columns"]

    # Specify the desired order for legend

    ordered_keys = [
        "full_occupancy",
        "full_occupancy_atomic_mixing",
        "deficiency_with_atomic_mixing",
        "deficiency_without_atomic_mixing",
    ]

    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=categories_colors[cat])
        for cat in ordered_keys
    ]

    legend_labels = [categories_mapping[cat] for cat in ordered_keys]
    dist_fig_text = get_dist_fig_text(all_distances)

    num_pairs = len(data)
    total_images = np.ceil(num_pairs / histograms_per_image).astype(int)
    data_pairs = list(data.items())
    # Calculate the number of rows based on the maximum histograms per image
    num_rows = np.ceil(histograms_per_image / max_columns).astype(int)
    sheet_size = (
        max_columns * 4,
        num_rows * 3,
    )  # Fixed sheet size

    single_histogram_dir = os.path.join(
        dir_path,
        "output",
        "single_histogram",
        output_filename,
    )
    os.makedirs(single_histogram_dir, exist_ok=True)

    for image_num in range(total_images):
        start_index = image_num * histograms_per_image
        end_index = min(
            (image_num + 1) * histograms_per_image,
            num_pairs,
        )
        current_pairs = data_pairs[start_index:end_index]

        fig, axes = plt.subplots(num_rows, max_columns, figsize=sheet_size)
        axes = np.atleast_2d(axes).flatten()

        for i, (pair_key, records) in enumerate(current_pairs):
            ax = axes[i]
            ax.set_title(pair_key)

            stacked_data = []
            labels = []
            for cat in ordered_keys:
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
                ax.yaxis.set_major_locator(MaxNLocator(integer=True))

                # Individual histogram figure with same format
                single_fig, single_ax = plt.subplots(figsize=(4, 3))
                single_ax.hist(
                    stacked_data,
                    bins=bins,
                    color=[categories_colors[cat] for cat in labels],
                    stacked=True,
                    edgecolor="black",
                )
                single_ax.set_title(pair_key)
                single_ax.set_xlabel("Distance (Å)")
                single_ax.set_ylabel("Count")
                single_ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                single_fig.tight_layout(rect=[0, 0, 1, 1])
                single_fig.savefig(
                    os.path.join(
                        single_histogram_dir,
                        f"{pair_key}.png",
                    ),
                    dpi=150,
                )
                plt.close(single_fig)

            else:
                ax.set_visible(False)

        # Hide unused axes
        for i in range(len(current_pairs), len(axes)):
            axes[i].set_visible(False)

        # Adjust the y-axis tick interval based on the max_count
        for ax in axes:
            ax.yaxis.set_major_locator(
                MaxNLocator(nbins=4, integer=True)
            )  # Adjust 'nbins' as needed

        # Code for the composite figure remains the same
        fig.legend(
            legend_handles,
            legend_labels,
            loc="lower center",
            ncol=len(legend_labels),
            bbox_to_anchor=(0.5, 0.02),
        )

        bin_width = str(get_histogram_config()["bin_width"])
        bin_width_text = f", Bin width: {bin_width} Å"
        plt.figtext(
            0.5,
            0.02,
            dist_fig_text + bin_width_text,
            ha="center",
            va="top",
        )
        plt.tight_layout(rect=[0, 0.05, 1, 1])

        output_dir = os.path.join(dir_path, "output")
        os.makedirs(output_dir, exist_ok=True)
        fig.savefig(
            os.path.join(
                output_dir,
                f"{output_filename}_{image_num + 1}.png",
            ),
            dpi=150,
        )
        plt.close(fig)
