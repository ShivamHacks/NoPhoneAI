import time
import pyaudio

class MicStream:
    def __init__(self, sample_rate: int = 44_100,):
        self.pyaudio = pyaudio.PyAudio()
        self.sample_rate = sample_rate

        self.chunk_size = int(self.sample_rate * 0.1)
        self.stream = self.pyaudio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        self.open = True

    def __iter__(self):
        return self

    def __next__(self):
        if not self.open:
            raise StopIteration
        try:
            return self.stream.read(self.chunk_size)
        except KeyboardInterrupt:
            raise StopIteration
        
    def pause(self):
        print("Pausing mic input")
        self.open = False
        if self.stream.is_active():
            self.stream.stop_stream()

    def start(self):
       print("Starting mic input")
       self.stream.start_stream()
       self.open = True

    def close(self):
        self.pause()
        self.stream.close()
        self.pyaudio.terminate()
