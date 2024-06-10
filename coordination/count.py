def nth_shortest_distance_count(connections: dict, label, index: int) -> int:
    # Check if label exists in connections dictionary
    if label not in connections:
        raise ValueError("Label not found in connections.")

    # Extract distances for the specified label
    distances = [dist for _, dist, _, _ in connections[label]]

    # Convert distances to a set to remove duplicates, then convert back to a list and sort it
    unique_sorted_distances = sorted(set(distances))

    # Check if the index is within the range of available unique distances
    if index >= len(unique_sorted_distances):
        raise ValueError(
            "Index is out of range for the number of unique distances available."
        )

    # Identify the nth shortest distance from the unique and sorted list
    nth_distance = unique_sorted_distances[index]
    print("Sorted unique distances:", unique_sorted_distances)
    print(f"The {index + 1}-th shortest unique distance is: {nth_distance}")

    # Count occurrences of the nth shortest distance in the original list of distances
    count_nth_distance = distances.count(nth_distance)

    return count_nth_distance
