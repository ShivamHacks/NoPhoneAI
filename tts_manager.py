import json
from elevenlabs import generate, stream, set_api_key

class TTSManager:

    def __init__(self):
        set_api_key(json.load(open("creds.json", "r"))["elevenlabs_api_key"])

    def tts(self, text):
        audio_stream = generate(
            text=text,
            stream=True
        )
        stream(audio_stream)

    def start_terminal_interface(self):
        print("Starting TTS. Type quit to exit.")
        while True:
            text = input("Text: ")

            if text.lower() == "quit":
                print("Quitting TTS")
                break
        
            self.tts(text)

if __name__ == "__main__":
    tts_manager = TTSManager()
    tts_manager.start_terminal_interface()