from chat_manager import ChatManager
from stt_manager import STTManager
from tts_manager import TTSManager
from mic_stream import MicStream

chat_manager = ChatManager()
chat_manager.setup_chat_from_terminal()

tts_manager = TTSManager()
mic_stream = MicStream()

def transcription_callback(text):
    mic_stream.pause()
    response = chat_manager.run(text)
    tts_manager.tts(response)
    mic_stream.start()

stt_manager = STTManager()
stt_manager.set_transcription_callback(transcription_callback)
stt_manager.start_stream(mic_stream)
