from typing import TypedDict

class WeatherResponse(TypedDict):
    city: str
    temperature_c: float
    humidity_percent: int
    wind_speed_kph: float
    conditions: str

def get_current_weather(city: str, units: str = "metric") -> WeatherResponse:
    """Return a weather response for a city.

    This example demonstrates a signature and response shape for documentation.
    It does not call a real weather service.
    """
    return {
        "city": city,
        "temperature_c": 22.5,
        "humidity_percent": 58,
        "wind_speed_kph": 11.2,
        "conditions": "Partly cloudy",
    }
