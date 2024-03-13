import os
os.environ['HF_HOME'] = '/home/stinky/models'

import torch

from transformers import pipeline
from transformers.utils import is_flash_attn_2_available

pipe = pipeline(
    'automatic-speech-recognition',
    model='openai/whisper-large-v3',
    torch_dtype=torch.float16,
    device='cpu',
    model_kwargs={"attn_implementation": "flash_attention_2"} if is_flash_attn_2_available() else {"attn_implementation": "sdpa"},
)