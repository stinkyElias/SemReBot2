import os
# os.environ['HF_HOME']='/home/stinky/Documents/semantic-robot/ros2_ws/src/nlp_handler/models'
os.environ['HF_HOME']='/home/stinky/ros2_ws/src/nlp_handler/models'

import torch
torch.cuda.empty_cache()
import pyaudio
import time
import numpy as np

from transformers import pipeline
from transformers.utils import is_flash_attn_2_available

# Load Insanely Fast Whisper
# print("Loading model...")
asr_pipeline = pipeline(
    'automatic-speech-recognition',
    model='openai/whisper-large-v3',
    torch_dtype=torch.float16,
    device='cuda:0',
    model_kwargs={'attn_implementation': 'flash_attention_2'} if is_flash_attn_2_available() else {'attn_implementation': 'sdpa'},
)
# print("Finished loading model.")

# # Initialize PyAudio
# FORMAT = pyaudio.paInt16
# CHANNELS = 1    # mono
# RATE = 44100    # Hz. 16000 is the sample rate of Whisper
# CHUNK = 512     # frames per buffer
# RECORDING_DURATION = 5  # seconds

# audio = pyaudio.PyAudio()
# stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
# frames = []

# print("Recording audio...")
# start_time = time.time()
# try:
#     while time.time() - start_time < RECORDING_DURATION:
#         data = stream.read(CHUNK)
#         frames.append(data)

# except KeyboardInterrupt:
#     pass

# stream.stop_stream()
# stream.close()
# audio.terminate()
# print("Finished recording audio.")

# audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
audio_data = 'audio_files/speech.wav'

# Transcribe audio
output = asr_pipeline(
    audio_data,
    chunk_length_s=30,
    batch_size=24,
    return_timestamps=True,
)

print(output['text'])