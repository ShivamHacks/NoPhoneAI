from pydub import AudioSegment
from pydub.playback import play
import io
import asyncio

from chat_manager import ChatManager
from stt_manager3 import STTManager
from tts_manager import TTSManager

chat_manager = ChatManager()
stt_manager = STTManager()
tts_manager = TTSManager()

tts_queue = asyncio.Queue(maxsize=-1) # infinite queue
async def process_tts_queue():
    while True:
        text = await tts_queue.get()
        print("Generating TTS...")
        stt_manager.set_read_from_mic(False)
        voice_response = await tts_manager.get_tts_bytes(text)
        segment = AudioSegment.from_file(io.BytesIO(voice_response), format="mp3")
        play(segment)
        await asyncio.sleep(3)
        stt_manager.set_read_from_mic(True)

def process_stt(text):
    if text == "":
        return
    response = chat_manager.run(text)
    print("Chat: " + response)
    tts_queue.put_nowait(response)

print("Starting localE2E")

chat_manager.setup_chat(
    "John",
    "Walgreens",
    "Check if they have dayquill in stock",
    True
)
stt_manager.set_read_from_mic(True)
stt_manager.set_stt_callback(process_stt)

async def main():
    await asyncio.gather(
        stt_manager.start_ws_async(close_stt_on_text=False),
        process_tts_queue()
    )

asyncio.run(main())