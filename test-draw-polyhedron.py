import os
import imageio.v3 as iio
from postprocess import polyhedron


# Example usage
json_file_path = "20240518_polyhedron_test/shortest_dist_CN/URhIn.json"
dir_path = "incremental_polyhedron_plots"

polyhedron.draw_incremental_polyhedrons(json_file_path, dir_path, dpi=300)

gif_dir = os.path.join(dir_path, "gif")

# Create gif directory if it doesn't exist
os.makedirs(gif_dir, exist_ok=True)

# Dictionary to store images based on their prefixes
images_dict = {"Rh2": [], "U1": [], "Rh1": [], "In1": []}

# Get sorted list of files
filenames = sorted(os.listdir(dir_path))

# Separate and sort images based on prefixes and step numbers
for filename in filenames:
    if filename.endswith(".png"):
        prefix = filename.split("_")[0]
        if prefix in images_dict:
            step_number = polyhedron.get_step_number(filename)
            if step_number is not None:
                images_dict[prefix].append(
                    (step_number, os.path.join(dir_path, filename))
                )

# Create GIFs for each prefix
for prefix, image_list in images_dict.items():
    if image_list:
        # Sort images based on step numbers
        image_list.sort()
        images = [iio.imread(filepath) for _, filepath in image_list]
        gif_filename = os.path.join(gif_dir, f"{prefix}_polyhedron.gif")
        iio.imwrite(gif_filename, images, duration=500, loop=0)
        print(f"Saved GIF: {gif_filename}")

print("GIF creation complete.")
