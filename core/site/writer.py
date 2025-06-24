import os


def write_summary_and_missing_pairs_with_element_dict(
    dist_mix_pair_dict,
    missing_pairs,
    text_filename,
    dir_path,
):
    """Writes a summary of unique atomic pairs, including counts and
    distances, and a list of missing pairs to a file."""

    file_path = os.path.join(dir_path, "output", text_filename)

    # Step 1: Collect data
    data = []
    for pair, files in dist_mix_pair_dict.items():
        distances = []
        for file_infos in files.values():
            for info in file_infos:  # Access each list in the dictionary
                distances.append(float(info["dist"]))
        distances = sorted(distances)
        count = len(distances)
        dists = ", ".join(f"{distance:.3f}" for distance in distances)
        data.append((pair, count, dists))

    # Step 2: Sort the data first by count (descending) then by pair name
    sorted_data = sorted(data, key=lambda x: (-x[1], x[0]))

    # Step 3: Write sorted data to file
    with open(file_path, "w", encoding="utf-8") as file:
        # print("\nMissing pairs:")
        file.write("Summary:\n")
        for pair, count, dists in sorted_data:
            file.write(f"Pair: {pair}, Count: {count}, Distances: {dists}\n")

        file.write("\nMissing pairs:\n")
        missing_pairs_sorted = sorted(
            missing_pairs,
            key=lambda x: (x[0][0], x[0], x[1]),
        )
        for pair in missing_pairs_sorted:
            atom_1, atom_2 = pair
            file.write(f"{atom_1}-{atom_2}\n")

    print(f"\nSummary and missing pairs saved to {file_path}")
