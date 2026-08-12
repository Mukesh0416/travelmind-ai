from tools.weather_tool import get_weather


def weather_agent(latitude: float, longitude: float):
    weather = get_weather(latitude, longitude)

    return {
        "temperature": weather["current"]["temperature_2m"],
        "humidity": weather["current"]["relative_humidity_2m"],
        "wind_speed": weather["current"]["wind_speed_10m"],
    }