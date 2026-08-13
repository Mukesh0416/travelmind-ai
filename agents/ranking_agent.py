POPULAR_ATTRACTIONS = {
    "Solang Valley": 10,
    "Rohtang Pass": 9,
    "Hadimba Temple": 8,
    "Old Manali": 8,
    "Manu Temple": 7,
    "Van Vihar": 6,
    "Beas River": 6,
}


def ranking_agent(attractions):

    ranked = sorted(
        attractions,
        key=lambda x: POPULAR_ATTRACTIONS.get(x, 0),
        reverse=True,
    )

    return ranked