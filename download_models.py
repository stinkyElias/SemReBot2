'''
This script downloads and initializes models for automatic speech recognition and language modeling.
To run, specify the directory where the models should be saved as an argument (string!).
If no argument is provided, the models will be saved to the default directory '~/semrebot2_models'.
'''

import os
import sys

try:
    # Try to get the user-specified directory
    output_dir = os.path.expanduser(os.path.join('~/', str(sys.argv[1])))
except IndexError:
    # If no argument is provided, use the default directory
    output_dir = os.path.expanduser('~/semrebot2_models')

os.environ['HF_HOME'] = output_dir

import torch

from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from transformers.utils import is_flash_attn_2_available

### Download models ###

# large whisper with flash attention
pipe = pipeline(
    'automatic-speech-recognition',
    model='openai/whisper-large-v3',
    torch_dtype=torch.float16,
    device='cpu',
    model_kwargs={"attn_implementation": "flash_attention_2"} if is_flash_attn_2_available() else {"attn_implementation": "sdpa"},
)

# mistral 7B instruct in 4-bit precision
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