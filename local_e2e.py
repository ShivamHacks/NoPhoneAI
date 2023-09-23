from pydub import AudioSegment
from pydub.playback import play
import io
import asyncio

from chat_manager import ChatManager
from stt_manager import STTManager
from tts_manager import TTSManager

chat_manager = ChatManager()
stt_manager = STTManager()
tts_manager = TTSManager()

def process_stt(text):
    stt_manager.set_listening(False)
    print("STT: " + text)
    response = chat_manager.run(text)
    print("Chat: " + response)
    voice_response = tts_manager.generate_tts_sync(response)
    segment = AudioSegment.from_file(io.BytesIO(voice_response), format="mp3")
    play(segment)
    stt_manager.set_listening(True)

print("Starting localE2E")

chat_manager.setup_chat(
    "John",
    "Walgreens",
    "Check if they have dayquill in stock",
    True
)
stt_manager.add_transcript_callback(process_stt)
stt_manager.setup_speech()
stt_manager.set_listening(True)
