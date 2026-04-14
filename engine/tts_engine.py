# engine/tts_engine.py
from gtts import gTTS
import pygame
import os
import time

class TTSManager:
    def __init__(self):
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()

    def speak(self, text):
        if not text:
            return
            
        print(f"[Speaking]: {text}")
        tts_file = "temp_voice.mp3"
        
        try:
            # Create gTTS object with Hindi ('hi')
            # It handles English words within Hindi sentences naturally.
            tts = gTTS(text=text, lang='hi', slow=False)
            tts.save(tts_file)

            # Play the file
            pygame.mixer.music.load(tts_file)
            pygame.mixer.music.play()

            # Wait for audio to finish playing
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Unload music so we can delete/overwrite the file later
            pygame.mixer.music.unload()
            os.remove(tts_file)
            
        except Exception as e:
            print(f"TTS Error: {e}")