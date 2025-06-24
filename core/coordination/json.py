import json

from cifkit import CifEnsemble

from core.coordination.util import compute_delta
from core.prompts.progress import prompt_file_saved


def save_json_for_connections(
    cif_ensemble: CifEnsemble, output_dir: str
) -> None:
    """Save the coordination number connections for a set of CIF files
    in JSON format."""
    CN_json = {}
    for cif in cif_ensemble.cifs:
        connections = cif.CN_connections_by_best_methods
        file_name = cif.file_name_without_ext
        CN_json[file_name] = {}

        for label, connection_data in connections.items():
            CN_json[file_name][label] = []
            neighbor_count = 1
            for connection in connection_data:
                other_label = connection[0]
                distance = connection[1]
                delta = compute_delta(label, other_label, distance)
                sorted_label_pair = tuple(sorted((label, other_label)))
                # Mixing info
                mixing_info_per_label = cif.mixing_info_per_label_pair

                CN_json[file_name][label].append(
                    {
                        "connected_label": other_label,
                        "distance": distance,
                        "delta": delta,
                        "mixing": mixing_info_per_label[sorted_label_pair],
                        "neighbor": neighbor_count,
                    }
                )
                neighbor_count += 1

    json_path = f"{output_dir}/CN_connections.json"
    with open(json_path, "w") as json_file:
        json.dump(CN_json, json_file, indent=4)

    prompt_file_saved(json_path)
