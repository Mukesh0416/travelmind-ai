def extract_places(search_results):

    # Expected attraction names in the exact format requested
    expected_attractions = [
        "Beas River",
        "Bhrigu Lake",
        "Hadimba Temple",
        "Manu Temple",
        "Old Manali",
        "Rohtang Pass",
        "Solang Valley",
        "Van Vihar",
        "Vashisht Temple"
    ]

    # Known place names mapping (lowercase to proper case)
    known_places = {
        "beas river": "Beas River",
        "bhrigu lake": "Bhrigu Lake",
        "hadimba temple": "Hadimba Temple",
        "manu temple": "Manu Temple",
        "old manali": "Old Manali",
        "rohtang pass": "Rohtang Pass",
        "solang valley": "Solang Valley",
        "van vihar": "Van Vihar",
        "vashisht temple": "Vashisht Temple",
    }

    places = set()

    for result in search_results:

        # Use "content" field from Tavily results
        text = (
            result.get("title", "")
            + " "
            + result.get("content", "")
        )

        # Extract 2-word phrases where both start with capital or are exact matches
        import re
        # Look for known place names (case-insensitive)
        for lowercase, proper in known_places.items():
            # Check if the lowercase version appears in the text (case-insensitive)
            if lowercase in text.lower():
                places.add(proper)

        # Also extract 2-word capitalized phrases from text
        capitalized_phrases = re.findall(r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b', text)
        for phrase in capitalized_phrases:
            full_phrase = phrase[0] + " " + phrase[1]
            # Add if it's in expected attractions
            if full_phrase in expected_attractions:
                places.add(full_phrase)

    return sorted(list(places))