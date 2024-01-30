import torch
torch.cuda.empty_cache()

from transformers import pipeline
from transformers.utils import is_flash_attn_2_available

asr_pipeline = pipeline(
    'automatic-speech-recognition',
    model='openai/whisper-large-v3',
    torch_dtype=torch.float16,
    device='cuda:0',
    model_kwargs={'attn_implementation': 'flash_attention_2'} if is_flash_attn_2_available() else {'attn_implementation': 'sdpa'},
)

print("Generating output...")
output = asr_pipeline(
    '/cluster/work/eliashk/semantic-robot/stt/audio_files/speech.wav',
    chunk_length_s=30,
    batch_size=24,
    return_timestamps=True,
)

print(output['text'])
print(asr_pipeline.model.get_memory_footprint())