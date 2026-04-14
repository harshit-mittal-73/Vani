# main.py
import pvporcupine
from pvrecorder import PvRecorder
import speech_recognition as sr
from config import PICOVOICE_API_KEY, WAKE_WORD_PATH, STT_LANGUAGE
from engine.llm_processor import IntentProcessor
from engine.tts_engine import TTSManager  # Added
from tools.automation import TOOL_REGISTRY

def listen_for_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Vani]: Sunn rahi hoon...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=7, phrase_time_limit=10)
            return recognizer.recognize_google(audio, language=STT_LANGUAGE)
        except:
            return None

def main():
    porcupine = pvporcupine.create(access_key=PICOVOICE_API_KEY, keyword_paths=[WAKE_WORD_PATH])
    recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
    brain = IntentProcessor()
    speaker = TTSManager() # Added

    print("--- Vani is Ready (Namaste Vani) ---")
    recorder.start()

    try:
        while True:
            pcm = recorder.read()
            if porcupine.process(pcm) >= 0:
                print("\n[Vani]: Ji?")
                recorder.stop()
                
                # Feedback audio for wake word
                speaker.speak("जी?") 
                
                user_query = listen_for_speech()
                if user_query:
                    print(f"You: {user_query}")
                    
                    result = brain.process(user_query)
                    
                    # 1. Speak the LLM's natural reply
                    speaker.speak(result['reply'])

                    # 2. Execute Tools and speak their results
                    for action in result.get("plan", []):
                        tool_name = action['tool']
                        args = action.get('args', {})
                        
                        func = TOOL_REGISTRY.get(tool_name)
                        if func:
                            print(f"[System]: Running {tool_name}...")
                            output = func(**args) if args else func()
                            # Speak the tool's result (e.g., "Mumbai mein temperature...")
                            speaker.speak(output)

                recorder.start()
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        recorder.delete()
        porcupine.delete()

if __name__ == "__main__":
    main()