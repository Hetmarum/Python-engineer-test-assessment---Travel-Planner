import requests


def fetch_artwork(artwork_id: int):
    url = f"https://api.artic.edu/api/v1/artworks/{artwork_id}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        return None

    data = response.json()
    return data.get("data")
