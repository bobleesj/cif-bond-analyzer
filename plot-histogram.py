import os
import json
import click
from click import echo
from core.site import histogram
from core.util import prompt, folder


from core.prompts.progress import prompt_folder_progress
from core.prompts.intro import prompt_plot_histograms_intro


def plot_histogram():
    """
    Produce histogram sheets and single histograms
    """

    prompt_plot_histograms_intro()
    # 1. Customize the bin width if needed
    echo("Would you like to customize the histogram width?")
    is_custom_design = click.confirm("(Default: Y)", default=True)

    if is_custom_design:
        min_x = click.prompt(
            "(1/3) Enter the minimum value for the x-axis",
            type=float,
        )
        max_x = click.prompt(
            "(2/3) Enter the maximum value for the x-axis",
            type=float,
        )

        bin_width = click.prompt(
            "(3/3) Enter the bin width",
            type=float,
        )

    # 2. Choose folders contianing .json
    script_path = os.path.dirname(os.path.abspath(__file__))
    dir_names_with_json = folder.get_json_dir_names(script_path)
    selected_dirs = prompt.get_user_input_folder_processing(
        dir_names_with_json, ".json"
    )
    num_selected_dirs = len(selected_dirs)

    if not dir_names_with_json:
        click.echo("No folders containing .json files were found.")
        return

    # 3. Plot
    for idx, dir_name in enumerate(selected_dirs.values(), start=1):
        dir_path = os.path.join(script_path, dir_name, "output")
        prompt_folder_progress(idx, dir_name, num_selected_dirs)
        element_pair_dict = None
        site_pair_dict = None

        for file_name in os.listdir(dir_path):
            if file_name.endswith("_element_pairs.json") or file_name.endswith(
                "_site_pairs.json"
            ):
                json_file_path = os.path.join(dir_path, file_name)
                echo(f"Processing {os.path.basename(json_file_path)}")

                with open(json_file_path, "r") as json_file:
                    data = json.load(json_file)
                if "_element_pairs.json" in file_name:
                    element_pair_dict = data
                elif "_site_pairs.json" in file_name:
                    site_pair_dict = data

        # Ensure that both dictionaries are not None before proceeding
        histogram_output_dir = os.path.join(script_path, dir_name)
        if site_pair_dict is not None and element_pair_dict is not None:
            if not is_custom_design:
                histogram.draw_histograms(
                    site_pair_dict,
                    element_pair_dict,
                    histogram_output_dir,
                )

            if is_custom_design:
                distances = [min_x, max_x]
                bins = histogram.get_bins_from_distances(bin_width, distances)

                histogram.plot_histograms(
                    site_pair_dict,
                    histogram_output_dir,
                    bins,
                    distances,
                    "histogram_site_pair",
                )
                histogram.plot_histograms(
                    element_pair_dict,
                    histogram_output_dir,
                    bins,
                    distances,
                    "histogram_element_pair",
                )

    echo("\nCongratulations! All histograms are re-generated.")


if __name__ == "__main__":
    plot_histogram()
