# tools/automation.py
import datetime
import requests
from config import WEATHER_API_KEY

def get_weather(location="Delhi"):
    """Fetches real-time weather using OpenWeatherMap."""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()
        
        if response.get("cod") != 200:
            return f"Maaf kijiye, {location} ka weather nahi mil pa raha hai."

        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        return f"{location} में अभी तापमान {temp}°C है और मौसम {desc} है।"
    except Exception as e:
        return "Weather check karne mein error aaya."

def get_time(args=None):
    now = datetime.datetime.now().strftime("%I:%M %p")
    return f"अभी समय {now} हो रहा है।"

def turn_on_light(room="living room"):
    # This would normally call a Smart Home API (Tuya/Yeelight)
    # For now, we simulate the success.
    return f"Ji, {room} ki light on kar di gayi hai."

# Registry
TOOL_REGISTRY = {
    "get_weather": get_weather,
    "get_time": get_time,
    "turn_on_light": turn_on_light
}