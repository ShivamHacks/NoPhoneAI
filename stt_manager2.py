import websockets
import asyncio
import base64
import pyaudio
import json
 
FRAMES_PER_BUFFER = 3200

# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
 
async def send_receive():
   print(f'Connecting websocket to url ${URL}')
   async with websockets.connect(
       URL,
       extra_headers=(("Authorization", json.load(open("creds.json", "r"))["assemblyai_api_key"]),),
       ping_interval=5,
       ping_timeout=20
   ) as _ws:
       await asyncio.sleep(0.1)
       print("Receiving SessionBegins ...")
       session_begins = await _ws.recv()
       print(session_begins)
       print("Sending messages ...")
       async def send():
           stream = pyaudio.PyAudio().open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=FRAMES_PER_BUFFER
            )
           while True:
               try:
                   data = stream.read(FRAMES_PER_BUFFER)
                   data = base64.b64encode(data).decode("utf-8")
                   json_data = json.dumps({"audio_data":str(data)})
                   await _ws.send(json_data)
               except websockets.exceptions.ConnectionClosedError as e:
                   print(e)
                   assert e.code == 4008
                   break
               except Exception as e:
                   assert False, "Not a websocket 4008 error"
               await asyncio.sleep(0.01)
          
           return True
      
       async def receive():
           while True:
               try:
                   result_str = await _ws.recv()
                   print(json.loads(result_str))
               except websockets.exceptions.ConnectionClosedError as e:
                   print(e)
                   assert e.code == 4008
                   break
               except Exception as e:
                   assert False, "Not a websocket 4008 error"
      
       send_result, receive_result = await asyncio.gather(send(), receive())

asyncio.run(send_receive())
