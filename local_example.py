import time
from chat_manager import ChatManager
from stt_manager import STTManager
from tts_manager import TTSManager
from mic_stream import MicStream

chat_manager = ChatManager()
chat_manager.setup_chat_from_terminal()

tts_manager = TTSManager()
mic_stream = MicStream()
mic_stream.pause()

def measure_time(name, func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    print(f"Time({name}) = {end - start}")
    return result

def transcription_callback(text):
    mic_stream.pause()
    response = measure_time("chat", chat_manager.run, text)
    tts_manager.tts(response)
    mic_stream.start()

stt_manager = STTManager()
stt_manager.set_transcription_callback(transcription_callback)
mic_stream.start()
stt_manager.start_stream(mic_stream)
