# src/utils.py
import json

def load_problem_data(filepath):
    """Loads the scheduling problem data from a JSON file."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        print("Problem data loaded successfully.")
        return data
    except FileNotFoundError:
        print(f" Error: The file {filepath} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {filepath} is not a valid JSON file.")
        return None