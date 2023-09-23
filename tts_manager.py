import asyncio
import websockets
import json
import base64
from pydub import AudioSegment
from pydub.playback import play
import io

class TTSManager:

    def __init__(self):
        self.ELEVENLABS_API_KEY = json.load(open("creds.json", "r"))["elevenlabs_api_key"]
        self.ELEVENLABS_MODEL = 'eleven_monolingual_v1'
        self.ELEVENLABS_VOICE_ID = 'CYw3kZ02Hs0563khs1Fj'
        self.ELEVENLABS_URI = f"wss://api.elevenlabs.io/v1/text-to-speech/{self.ELEVENLABS_VOICE_ID}/stream-input?model_id={self.ELEVENLABS_MODEL}"

    async def generate_tts(self, text):
        async with websockets.connect(self.ELEVENLABS_URI) as websocket:

            # Initialize the connection
            bos_message = {
                "text": " ",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": True
                },
                "xi_api_key": self.ELEVENLABS_API_KEY
            }
            await websocket.send(json.dumps(bos_message))

            # Generate the text
            input_message = {
                "text": text + " ", # input must end with space
                "try_trigger_generation": True
            }
            await websocket.send(json.dumps(input_message))

            # Send EOS message with an empty string
            await websocket.send(json.dumps({"text": ""}))

            # Yield MP3 chunks until the connection is closed
            while True:
                try:
                    response = await websocket.recv()
                    data = json.loads(response)
                    print("Server response:", data)

                    if data["audio"]:
                        chunk = base64.b64decode(data["audio"])
                        yield chunk
                    else:
                        print("No audio data in the response")
                        break
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed")
                    break
    
    def generate_tts_sync(self, text):
        async def get_tts_chunks(text):
            print("Generating TTS...")
            data = b""
            async for chunk in self.generate_tts(text):
                data += chunk
            print("TTS generated")
            return data
        return asyncio.get_event_loop().run_until_complete(get_tts_chunks(text))

    def start_terminal_interface(self):
        print("Starting TTS. Type quit to exit.")
        while True:
            text = input("Text: ")

            if text.lower() == "quit":
                print("Quitting TTS")
                break

            segment = AudioSegment.from_file(io.BytesIO(self.generate_tts_sync(text)), format="mp3")
            play(segment)

if __name__ == "__main__":
    tts_manager = TTSManager()
    tts_manager.start_terminal_interface()
