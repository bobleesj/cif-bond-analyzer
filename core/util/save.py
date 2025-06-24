import json


def save_to_json(data, json_file_path):
    """Save data to a JSON file and confirm the action."""
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Data has been saved to {json_file_path}.")
