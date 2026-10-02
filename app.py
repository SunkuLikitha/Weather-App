import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

CITY_ALIASES = {"bangalore": "Bengaluru"}

WEATHER_CODE_DETAILS = {
    0: ("Clear sky", "sun"),
    1: ("Mainly clear", "partly-cloudy"),
    2: ("Partly cloudy", "partly-cloudy"),
    3: ("Cloudy", "cloud"),
    45: ("Fog", "fog"),
    48: ("Fog", "fog"),
    51: ("Drizzle", "drizzle"),
    53: ("Drizzle", "drizzle"),
    55: ("Drizzle", "drizzle"),
    56: ("Freezing drizzle", "drizzle"),
    57: ("Freezing drizzle", "drizzle"),
    61: ("Rain", "rain"),
    63: ("Rain", "rain"),
    65: ("Heavy rain", "rain"),
    66: ("Freezing rain", "rain"),
    67: ("Freezing rain", "rain"),
    71: ("Snow", "snow"),
    73: ("Snow", "snow"),
    75: ("Heavy snow", "snow"),
    77: ("Snow grains", "snow"),
    80: ("Rain showers", "rain"),
    81: ("Rain showers", "rain"),
    82: ("Heavy rain showers", "rain"),
    85: ("Snow showers", "snow"),
    86: ("Heavy snow showers", "snow"),
    95: ("Thunderstorm", "thunderstorm"),
    96: ("Thunderstorm with hail", "thunderstorm"),
    99: ("Thunderstorm with hail", "thunderstorm"),
}


def get_weather_details(weather_code, is_day):
    description, icon = WEATHER_CODE_DETAILS.get(
        weather_code,
        ("Weather unavailable", "cloud"),
    )
    if weather_code == 0 and not is_day:
        icon = "moon"
    return description, icon


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/weather")
def get_weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "Please enter a city name.", "code": "empty_city"}), 400

    search_city = CITY_ALIASES.get(city.casefold(), city)

    try:
        geocoding_response = requests.get(
            GEOCODING_API_URL,
            params={
                "name": search_city,
                "count": 10,
                "language": "en",
                "format": "json",
            },
            timeout=10,
        )
        geocoding_response.raise_for_status()
        locations = geocoding_response.json().get("results", [])
        if not locations:
            return jsonify({
                "error": f"We couldn't find {city}. Check the spelling and try again.",
                "code": "city_not_found",
            }), 404

        location = locations[0]
        weather_response = requests.get(
            WEATHER_API_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": (
                    "temperature_2m,relative_humidity_2m,apparent_temperature,"
                    "weather_code,wind_speed_10m,surface_pressure,is_day"
                ),
                "temperature_unit": "celsius",
                "wind_speed_unit": "ms",
                "timezone": "auto",
            },
            timeout=10,
        )
        weather_response.raise_for_status()
        current = weather_response.json()["current"]

        weather_code = int(current["weather_code"])
        condition, icon = get_weather_details(weather_code, current["is_day"] == 1)
        result = {
            "city": location["name"],
            "country": location.get("country", ""),
            "temperature": round(current["temperature_2m"]),
            "condition": condition,
            "feels_like": round(current["apparent_temperature"]),
            "humidity": current["relative_humidity_2m"],
            "wind_speed": round(current["wind_speed_10m"], 1),
            "pressure": round(current["surface_pressure"]),
            "icon": icon,
        }
    except requests.exceptions.Timeout:
        return jsonify({
            "error": "The weather lookup timed out. Please try again.",
            "code": "timeout",
        }), 504
    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Could not connect to Open-Meteo. Check your internet connection and try again.",
            "code": "network_error",
        }), 503
    except requests.exceptions.RequestException:
        return jsonify({
            "error": "Open-Meteo could not provide weather data right now. Please try again later.",
            "code": "api_error",
        }), 502
    except (KeyError, TypeError, ValueError):
        return jsonify({
            "error": "Open-Meteo returned an unexpected response. Please try again later.",
            "code": "invalid_response",
        }), 502

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)