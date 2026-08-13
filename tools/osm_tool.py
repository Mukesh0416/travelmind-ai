# import requests


# def search_location(place: str):
#     url = "https://nominatim.openstreetmap.org/search"

#     params = {
#         "q": place,
#         "format": "json",
#         "limit": 5,
#     }

#     headers = {
#         "User-Agent": "TravelMind-AI/1.0"
#     }

#     response = requests.get(
#         url,
#         params=params,
#         headers=headers,
#         timeout=10,
#     )

#     response.raise_for_status()

#     return response.json()


import requests


def search_location(place: str):

    print("Searching:", place)

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": place,
        "format": "json",
        "limit": 5,
    }

    headers = {
        "User-Agent": "TravelMind-AI/1.0"
    }

    print("Sending request...")

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10,
    )

    print("Response received:", response.status_code)

    response.raise_for_status()

    print("Converting JSON...")

    return response.json()