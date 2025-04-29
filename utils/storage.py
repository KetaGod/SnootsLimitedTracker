import json
import os
import csv
from datetime import datetime

DATA_FILE = "prev_data.json"

def load_previous_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_current_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def ensure_user_dir(username):
    folder = f"data/{username}"
    os.makedirs(folder, exist_ok=True)
    return folder

def append_to_history(username, total_rap, total_value):
    folder = ensure_user_dir(username)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"timestamp": timestamp, "rap": total_rap, "value": total_value}

    json_path = os.path.join(folder, "history.json")
    history = []
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            history = json.load(f)
    history.append(entry)
    with open(json_path, "w") as f:
        json.dump(history, f, indent=2)

    csv_path = os.path.join(folder, "history.csv")
    write_header = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["timestamp", "rap", "value"])
        if write_header:
            writer.writeheader()
        writer.writerow(entry)

def get_history(username):
    path = f"data/{username}/history.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
        return []