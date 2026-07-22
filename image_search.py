def search_image(query):
    import requests

    url = "https://api.unsplash.com/search/photos"

    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }

    params = {
        "query": query,
        "per_page": 1
    }

    response = requests.get(url, headers=headers, params=params)

    print("=" * 50)
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    print("=" * 50)

    if response.status_code != 200:
        return None

    data = response.json()

    if len(data["results"]) > 0:
        print("IMAGE URL:", data["results"][0]["urls"]["regular"])
        return data["results"][0]["urls"]["regular"]

    print("No image found")
    return None