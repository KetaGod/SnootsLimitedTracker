import requests

def get_user_id(username):
    url = "https://users.roblox.com/v1/usernames/users"
    payload = {
        "usernames": [username],
        "excludeBannedUsers": False
    }

    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        data = res.json()
        if data["data"]:
            return data["data"][0]["id"]
        else:
            print(f"Username '{username}' not found.")
            return None
    except requests.RequestException as e:
        print(f"Error fetching user ID: {e}")
        return None

def get_limited_inventory(user_id):
    url = f"https://inventory.roblox.com/v1/users/{user_id}/assets/collectibles?sortOrder=Asc&limit=100"
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json().get("data", [])
    except requests.RequestException as e:
        print(f"Error fetching inventory for user {user_id}: {e}")
        return []