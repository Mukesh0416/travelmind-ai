from tools.weather_tool import get_weather


from tools.weather_tool import get_weather


def weather_agent(state):

    latitude = state["location"]["latitude"]

    longitude = state["location"]["longitude"]

    weather = get_weather(latitude, longitude)

    state["weather"] = {
        "temperature": weather["current"]["temperature_2m"],
        "humidity": weather["current"]["relative_humidity_2m"],
        "wind_speed": weather["current"]["wind_speed_10m"],
    }

    state["next_agent"] = "search"

    return state