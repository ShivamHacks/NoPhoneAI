import websockets
import asyncio
import base64
import pyaudio
import json

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
        self.ASSEMBLYAI_URL = f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={self.SAMPLE_RATE}"
        self.stt_callback = None
        self.stream = None
    
    def set_stt_callback(self, callback):
        self.stt_callback = callback
    
    def set_read_from_mic(self, read_from_mic):
        if self.stream is None:
            return
        if read_from_mic:
            print("starting stream")
            self.stream.start_stream()
        else:
            print("stopping stream")
            self.stream.stop_stream()
    
    async def receive_from_ws(self, ws, close_stt_on_text=False):
        while True:
            print("recv")
            try:
                result_str = await ws.recv()
                result_json = json.loads(result_str)
                if result_json["message_type"] == "PartialTranscript":
                    print(f"Partial transcript received: ", result_json["text"])
                elif result_json['message_type'] == "FinalTranscript":
                    print(f"Final transcript received: ", result_json["text"])
                    if close_stt_on_text:
                        await ws.close()
                        break
                    if self.stt_callback is not None:
                        self.stt_callback(result_json["text"])
            except websockets.exceptions.ConnectionClosedError as e:
                print(e)
                assert e.code == 4008
                break
            except Exception as e:
                assert False, "Not a websocket 4008 error"
        
        return True
    
    async def send_to_ws_from_mic(self, ws):
        self.stream = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=self.FRAMES_PER_BUFFER
        )
        self.stream.start_stream()
        while True:
            if not self.stream.is_active():
                print("mic closed")
                await asyncio.sleep(0.01)
                continue
            try:
                data = self.stream.read(self.FRAMES_PER_BUFFER)
                data = base64.b64encode(data).decode("utf-8")
                json_data = json.dumps({"audio_data":str(data)})
                await ws.send(json_data)
            except websockets.exceptions.ConnectionClosedError as e:
                print(e)
                assert e.code == 4008
                break
            except websockets.exceptions.ConnectionClosed as e:
                print("websocket closed")
                break
            except Exception as e:
                assert False, "Not a websocket 4008 error"
            await asyncio.sleep(0.01)
       
        return True
    
    async def start_ws_async(self, close_stt_on_text=False):
        print(f'Connecting websocket to url ${self.ASSEMBLYAI_URL}')
        async with websockets.connect(
            self.ASSEMBLYAI_URL,
            extra_headers=(("Authorization", self.ASSEMBLYAI_API_KEY),),
            ping_interval=5,
            ping_timeout=20
        ) as ws:
            await asyncio.sleep(0.1)
            print("Receiving SessionBegins ...")
            session_begins = await ws.recv()
            print(session_begins)
            print("Sending messages ...")
            send_result, receive_result = await asyncio.gather(
                self.send_to_ws_from_mic(ws),
                self.receive_from_ws(ws, close_stt_on_text)
            )

    def start_ws(self, close_stt_on_text=False):
        asyncio.run(self.start_ws_async(close_stt_on_text))

if __name__ == "__main__":
    stt_manager = STTManager()
    stt_manager.start_ws(close_stt_on_text=True)