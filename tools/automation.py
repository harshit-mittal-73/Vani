# tools/automation.py
import datetime
import requests
from config import WEATHER_API_KEY, NEWS_API_KEY, GNEWS_API_KEY

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

# tools/automation.py
    """Fetches top headlines with a fallback mechanism."""
    try:
        # Strategy 1: Try top headlines for India with category
        url = f"https://newsapi.org/v2/top-headlines?country=in&category={category}&apiKey={NEWS_API_KEY}"
        response = requests.get(url).json()

        articles = response.get("articles", [])

        # Strategy 2: If no articles, try a general search for 'India' + category keywords
        if not articles or response.get("totalResults") == 0:
            print(f"[System]: No specific headlines for {category}. Trying search...")
            fallback_url = f"https://newsapi.org/v2/everything?q=India%20{category}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
            response = requests.get(fallback_url).json()
            articles = response.get("articles", [])

        if not articles:
            return "Maaf kijiye, mujhe abhi koi taaja khabar nahi mili. Shaitad server down hai."

        # Pick top 3 and clean them
        headlines = []
        for a in articles[:3]:
            title = a['title'].split(" - ")[0] # Remove source name from title for cleaner speech
            headlines.append(title)
            
        news_summary = "Aaj ki badi khabrein ye hain: " + "। ".join(headlines)
        return news_summary

    except Exception as e:
        print(f"News Tool Error: {e}")
        return "News fetch karne mein technical dikkat aa rahi hai."

def get_news(category="general"):
    """Fetches top headlines in Hindi using GNews API."""
    try:
        # lang='hi' ensures headlines are in Hindi script
        # country='in' targets Indian news sources
        url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=hi&country=in&max=3&apikey={GNEWS_API_KEY}"
        
        response = requests.get(url)
        data = response.json()

        if "articles" not in data or not data["articles"]:
            return "Maaf kijiye, mujhe abhi Hindi mein koi khabar nahi mili."

        articles = data["articles"]
        headlines = []
        
        for a in articles:
            # We take the title; GNews titles in Hindi are usually very clean
            headlines.append(a['title'])
            
        news_summary = "Hindi mein aaj ki badi khabrein ye hain: " + "। ".join(headlines)
        return news_summary

    except Exception as e:
        print(f"GNews Error: {e}")
        return "News system mein kuch dikkat aa rahi hai."
# Registry
TOOL_REGISTRY = {
    "get_weather": get_weather,
    "get_time": get_time,
    "turn_on_light": turn_on_light,
    "get_news": get_news
}