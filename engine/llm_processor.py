# engine/llm_processor.py
import json
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME

class IntentProcessor:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL_NAME,
            generation_config={
                "response_mime_type": "application/json",
            },
            system_instruction=(
                "You are 'Vani', a helpful Hinglish Voice Assistant. "
                "Analyze input and return JSON. "
                "Available Tools: "
                "- get_weather(location): Returns weather info. "
                "- get_time(): Returns current time. "
                "- turn_on_light(room): Controls smart lights. "
                "- get_news(category): Returns top news headlines. Categories: 'business', 'entertainment', 'health', 'science', 'sports', 'technology', 'general'. "
                "JSON Schema: {'plan': [{'tool': str, 'args': {}}], 'reply': str}"
            )
        )

    def process(self, text):
        try:
            response = self.model.generate_content(text)
            # Gemini returns a string in response.text which we parse as JSON
            return json.loads(response.text)
        except Exception as e:
            print(f"LLM Error: {e}")
            return {"plan": [], "reply": "Maaf kijiye, main samajh nahi paayi."}