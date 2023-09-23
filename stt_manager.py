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
        self.mic_opened = False
        self.ws_open = False
        self.transcript_callback = None
        self.listening_on_mic = False
    
    def start_stt_websocket_thread(self):
        websocket.enableTrace(False)
        auth_header = {"Authorization": f"{self.ASSEMBLYAI_API_KEY}" }
        self.ws = websocket.WebSocketApp(
            f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={self.SAMPLE_RATE}",
            header=auth_header,
            on_message=self.on_ws_message,
            on_open=self.on_ws_open,
            on_error=self.on_ws_error,
            on_close=self.on_ws_close
        )
        Thread(target=self.ws.run_forever).start()

    def close_stt_websocket(self):
        if self.ws_open:
            self.ws.close()

    def on_ws_message(self, ws, message):
        transcript = json.loads(message)
        text = transcript['text']
        if transcript["message_type"] == "PartialTranscript":
            print(f"Partial transcript received: {text}")
        elif transcript['message_type'] == 'FinalTranscript':
            print(f"Final transcript received: {text}")
            if self.transcript_callback is not None:
                self.transcript_callback(text)

    def on_ws_error(self, ws, error):
        print(error)

    def on_ws_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed")
        self.ws_open = False

    def on_ws_open(self, ws):
        print("WebSocket opened")
        self.ws_open = True
    
    def listen_on_mic(self, final_transcript_callback=None):
        print("Opening mic")
        self.listening_on_mic = True
        self.open_stt_websocket()
        self.mic_stream = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.SAMPLE_RATE,
            input=True,
            frames_per_buffer=self.FRAMES_PER_BUFFER
        )

        def transcript_callback(text):
            print("Received result: " + text)
            self.listening_on_mic = False
            self.mic_stream.close()
            self.close_stt_websocket()
            if final_transcript_callback is not None:
                final_transcript_callback(text)
        self.transcript_callback = transcript_callback

        # TODO: self.mic_stream.is_active() is not working
        while self.listening_on_mic:
            print("mic open")
            if not self.ws_open:
                # Wait until websocket is open
                continue
            data = self.mic_stream.read(self.FRAMES_PER_BUFFER)
            data = base64.b64encode(data).decode("utf-8")
            json_data = json.dumps({"audio_data":str(data)})
            self.ws.send(json_data)
        
        print("Listen on mic complete")

    def start_mic_loop(self):
        print("Starting STT. Type quit to exit.")
        while True:
            text = input("Quit (y/N): ")
            if text.lower() == "y":
                break
            self.listen_on_mic()


if __name__ == "__main__":
    stt_manager = STTManager()
    #stt_manager.start_mic_loop()
    stt_manager.start_stt_websocket_thread()
    stt_manager.close_stt_websocket()