# dir = '/home/stinky/models'
dir = '/home/carla/elias/models'

import os
os.environ['HF_HOME'] = dir

import torch

from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from transformers.utils import is_flash_attn_2_available

# whisper
pipe = pipeline(
    'automatic-speech-recognition',
    model='openai/whisper-large-v3',
    torch_dtype=torch.float16,
    device='cpu',
    model_kwargs={"attn_implementation": "flash_attention_2"} if is_flash_attn_2_available() else {"attn_implementation": "sdpa"},
)

# mistral
model_id = 'mistralai/Mistral-7B-Instruct-v0.2'

tokenizer = AutoTokenizer.from_pretrained(model_id)

nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

model_nf4 = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=nf4_config)

print("Models saved to ", dir)