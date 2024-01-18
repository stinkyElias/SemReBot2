import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 1    # mono
RATE = 44100    # Hz
CHUNK = 512     # frames per buffer

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

frames = []

try:
    while True:
        data = stream.read(CHUNK)
        frames.append(data)

except KeyboardInterrupt:
    pass

stream.stop_stream()
stream.close()
audio.terminate()

sound_file = wave.open("test.wav", "wb")
sound_file.setnchannels(CHANNELS)  
sound_file.setsampwidth(audio.get_sample_size(FORMAT))
sound_file.setframerate(RATE)
sound_file.writeframes(b''.join(frames))
sound_file.close()  