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
    
    async def receive_from_ws(self, ws):
        while True:
            try:
                result_str = await ws.recv()
                result_json = json.loads(result_str)
                if result_json["message_type"] == "PartialTranscript":
                    print(f"Partial transcript received: ", result_json["text"])
                elif result_json['message_type'] == "FinalTranscript":
                    print(f"Final transcript received: ", result_json["text"])
                    await ws.close()
                    return True
            except websockets.exceptions.ConnectionClosedError as e:
                print(e)
                assert e.code == 4008
                break
            except Exception as e:
                assert False, "Not a websocket 4008 error"
    
    async def send_to_ws_from_mic(self, ws):
        stream = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=self.FRAMES_PER_BUFFER
        )
        while True:
            try:
                data = stream.read(self.FRAMES_PER_BUFFER)
                data = base64.b64encode(data).decode("utf-8")
                json_data = json.dumps({"audio_data":str(data)})
                await ws.send(json_data)
            except websockets.exceptions.ConnectionClosedError as e:
                print(e)
                assert e.code == 4008
                break
            except websockets.exceptions.ConnectionClosed as e:
                print("websocket closed")
                return True
            except Exception as e:
                assert False, "Not a websocket 4008 error"
            await asyncio.sleep(0.01)
       
        return True
    
    def start_ws(self):
        async def start_ws_async():
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
                    self.receive_from_ws(ws)
                )
    
        asyncio.run(start_ws_async())

if __name__ == "__main__":
    stt_manager = STTManager()
    stt_manager.start_ws()