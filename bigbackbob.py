import threading
import time
import numpy as np

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

# Import Pyjnius to access Android APIs.
from jnius import autoclass

# Audio and detection parameters.
SAMPLE_RATE = 44100
WHISTLE_FREQ_LOW = 1000    # Lower bound for whistle (Hz)
WHISTLE_FREQ_HIGH = 3000   # Upper bound for whistle (Hz)
AMPLITUDE_THRESHOLD = 1000  # Threshold for frequency amplitude (tweak as needed)
MIN_TIME_BETWEEN_WHISTLES = 1.0  # seconds

# Access Android classes.
AudioRecord = autoclass('android.media.AudioRecord')
AudioFormat = autoclass('android.media.AudioFormat')
MediaRecorder = autoclass('android.media.MediaRecorder')

# Set up audio parameters.
CHANNEL_CONFIG = AudioFormat.CHANNEL_IN_MONO
ENCODING = AudioFormat.ENCODING_PCM_16BIT
AUDIO_SOURCE = MediaRecorder.AudioSource.MIC

# Get minimum buffer size.
min_buffer_size = AudioRecord.getMinBufferSize(SAMPLE_RATE, CHANNEL_CONFIG, ENCODING)
# Choose a buffer size (in shorts) that’s large enough.
BUFFER_SIZE = max(min_buffer_size, 2048)


class WhistleDetector(threading.Thread):
    def __init__(self, whistle_callback):
        threading.Thread.__init__(self)
        self.whistle_callback = whistle_callback
        self.running = True
        self.last_whistle_time = 0

        # Initialize AudioRecord.
        self.recorder = AudioRecord(
            AUDIO_SOURCE,
            SAMPLE_RATE,
            CHANNEL_CONFIG,
            ENCODING,
            BUFFER_SIZE * 2  # buffer size in bytes (16 bits = 2 bytes per sample)
        )
        self.recorder.startRecording()

    def run(self):
        while self.running:
            try:
                # Create a bytearray buffer to hold raw audio (16-bit PCM)
                buf = bytearray(BUFFER_SIZE * 2)
                # Read audio data into the buffer.
                # Note: On Android, AudioRecord.read fills the byte array with raw bytes.
                shorts_read = self.recorder.read(buf, 0, len(buf))
                if shorts_read <= 0:
                    continue

                # Convert byte data to numpy array of int16.
                audio_data = np.frombuffer(buf, dtype=np.int16)

                # Compute FFT on the audio data.
                fft_data = np.fft.rfft(audio_data)
                freqs = np.fft.rfftfreq(len(audio_data), 1.0 / SAMPLE_RATE)
                magnitude = np.abs(fft_data)

                # Look for peaks in the whistle frequency range.
                indices = np.where((freqs >= WHISTLE_FREQ_LOW) & (freqs <= WHISTLE_FREQ_HIGH))[0]
                if indices.size > 0 and np.max(magnitude[indices]) > AMPLITUDE_THRESHOLD:
                    current_time = time.time()
                    if current_time - self.last_whistle_time > MIN_TIME_BETWEEN_WHISTLES:
                        self.last_whistle_time = current_time
                        # Invoke the callback when a whistle is detected.
                        self.whistle_callback()
            except Exception as e:
                print("Error during audio processing:", e)

    def stop(self):
        self.running = False
        self.recorder.stop()
        self.recorder.release()


class WhistleApp(App):
    def build(self):
        self.whistle_count = 0
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.label = Label(text="Whistles detected: 0", font_size='30sp')
        self.layout.add_widget(self.label)
        self.quit_button = Button(text="Quit", size_hint=(1, 0.2))
        self.quit_button.bind(on_press=self.stop_app)
        self.layout.add_widget(self.quit_button)

        # Start the whistle detector thread.
        self.detector = WhistleDetector(self.increment_counter)
        self.detector.daemon = True
        self.detector.start()

        return self.layout

    def increment_counter(self):
        # Schedule UI update on the main thread.
        Clock.schedule_once(lambda dt: self._increment_counter(), 0)

    def _increment_counter(self):
        self.whistle_count += 1
        self.label.text = f"Whistles detected: {self.whistle_count}"

    def stop_app(self, instance):
        self.detector.stop()
        self.stop()


if __name__ == '__main__':
    WhistleApp().run()
