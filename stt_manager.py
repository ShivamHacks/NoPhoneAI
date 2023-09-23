import sys
import json
import assemblyai as aai
from mic_stream import MicStream

class STTManager:

    def __init__(self, sample_rate: int = 44_100):
        self.transcription_callback = None
        aai.settings.api_key = json.load(open("creds.json", "r"))["assemblyai_api_key"]
        self.transcriber = aai.RealtimeTranscriber(
            on_data=self.on_data,
            on_error=self.on_error,
            sample_rate=sample_rate,
            on_open=self.on_open, # optional
            on_close=self.on_close, # optional
        )
        self.transcriber.connect()
    
    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        print("STT Ready, session ID:", session_opened.session_id)

    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        # TODO: measure time between real time STT and final transcript prediction
        if isinstance(transcript, aai.RealtimeFinalTranscript):
            print(transcript.text, end="\r\n")
            if self.transcription_callback is not None:
                self.transcription_callback(transcript.text)
        else:
            print(transcript.text, end="\r")

    def on_error(self, error: aai.RealtimeError):
        print("STT error occured:", error)

    def on_close(self):
        print("STT closing Session")

    def start_stream(self, stream):
        # Note that calling this is blocking
        self.transcriber.stream(stream)

    def set_transcription_callback(self, transcription_callback):
        self.transcription_callback = transcription_callback

if __name__ == "__main__":
    stt_manager = STTManager()

    def transcription_callback(text):
        if "quit" in text.lower():
            print("Exiting STT")
            sys.exit() # TODO: not working
    
    stt_manager.set_transcription_callback(transcription_callback)
    stt_manager.start_stream(MicStream())