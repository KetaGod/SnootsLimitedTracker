import matplotlib.pyplot as plt
from utils.storage import get_history

def show_graph(username):
    history = get_history(username)
    if not history:
        return

    timestamps = [entry["timestamp"] for entry in history]
    rap_values = [entry["rap"] for entry in history]
    total_values = [entry["value"] for entry in history]

    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, rap_values, label="RAP", color="#9D00FF", marker="o")
    plt.plot(timestamps, total_values, label="Value", color="cyan", marker="x")
    plt.xticks(rotation=45)
    plt.title(f"{username}'s RAP and Value History")
    plt.xlabel("Time")
    plt.ylabel("RAP / Value")
    plt.tight_layout()
    plt.legend()
    plt.grid(True)
    plt.show()
