import requests
from config import UNSPLASH_ACCESS_KEY


def search_image(query):

    url = "https://api.unsplash.com/search/photos"

    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }

    params = {
        "query": query,
        "per_page": 1
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    data = response.json()

    if data.get("results"):
        return data["results"][0]["urls"]["regular"]

    return None