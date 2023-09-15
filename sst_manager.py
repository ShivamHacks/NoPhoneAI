import websocket
import base64
import pyaudio
import json
from threading import Thread

class STTManager:

    def __init__(self):
        self.ASSEMBLYAI_API_KEY = json.load(open("creds.json", "r"))["assemblyai_api_key"]
        self.FRAMES_PER_BUFFER = 3200
        self.SAMPLE_RATE = 16000
        self.open_mic = False
    
    def setup_speech(self):
        websocket.enableTrace(False)
        auth_header = {"Authorization": f"{self.ASSEMBLYAI_API_KEY}" }
        self.ws = websocket.WebSocketApp(
            f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={self.SAMPLE_RATE}",
            header=auth_header,
            on_message=self.on_message,
            on_open=self.on_open,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.run_forever()

    def on_message(self, ws, message):
        transcript = json.loads(message)
        text = transcript['text']
        if transcript["message_type"] == "PartialTranscript":
            print(f"Partial transcript received: {text}")
        elif transcript['message_type'] == 'FinalTranscript':
            print(f"Final transcript received: {text}")

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed")

    def on_open(self, ws):
        print("WebSocket opened")
        if not self.open_mic:
            return
        
        stream = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.SAMPLE_RATE,
            input=True,
            frames_per_buffer=self.FRAMES_PER_BUFFER
        )

        def send_data():
            while True:
                data = stream.read(self.FRAMES_PER_BUFFER)
                data = base64.b64encode(data).decode("utf-8")
                json_data = json.dumps({"audio_data":str(data)})
                self.ws.send(json_data)

        Thread(target=send_data).start()
    
    def start_mic_transcription(self):
        self.open_mic = True


if __name__ == "__main__":
    stt_manager = STTManager()
    stt_manager.start_mic_transcription()
    stt_manager.setup_speech()