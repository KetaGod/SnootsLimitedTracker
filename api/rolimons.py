import requests

def get_rolimons_data():
    url = "https://www.rolimons.com/itemapi/itemdetails"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json().get("items", {})
    return {}
