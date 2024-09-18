import threading
import pyaudio
import wave

class Recorder:
    def __init__(self) -> None:
        self.rate = 16000
        self.chunk = 1024
        self.audio = pyaudio.PyAudio()
        self.channels = 1
        self.format = pyaudio.paInt16
        self.output_file = "./sound/user_response.wav"
        self.frames = []
        self.stream = None
        self.recording_thread = None
        self.recording = threading.Event()  # Use threading.Event for synchronization

    def _record(self):
        self.frames = []
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        print("Recording started...")

        while self.recording.is_set():  # Use threading.Event to control recording
            data = self.stream.read(self.chunk)
            self.frames.append(data)

        self.stream.stop_stream()
        self.stream.close()
        self.save_wav()

    def start(self):
        if not self.recording.is_set():  # Check if recording is already in progress
            self.recording.set()
            self.recording_thread = threading.Thread(target=self._record)
            self.recording_thread.start()
        else:
            print("Recording is already in progress")

    def stop(self):
        if self.recording.is_set():  # Check if recording is active
            self.recording.clear()  # Stop the recording loop
            self.recording_thread.join()  # Wait for the recording to finish
            self.audio.terminate()  # Clean up audio resources
            print("Recording stopped")
        else:
            print("No active recording to stop.")

    def save_wav(self):
        with wave.open(self.output_file, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b"".join(self.frames))

        print(f"Recording saved to {self.output_file}")