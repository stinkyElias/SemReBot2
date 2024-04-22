import os
os.environ['HF_HOME']='/home/stinky/models'
# os.environ['HF_HOME']='/home/carla/elias/models'

import torch
import json
import gc
import sys

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

device = 'cuda'
model_id = 'mistralai/Mistral-7B-Instruct-v0.2'

tokenizer = AutoTokenizer.from_pretrained(model_id)

nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

print("Memory allocated BEFORE loading model: %d MB" % (torch.cuda.memory_allocated()/(1024**2)))
print("Max memory allocated BEFORE loading model: %d MB\n" % (torch.cuda.max_memory_allocated()/(1024**2)))

model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=nf4_config)

print("Memory allocated AFTER loading model: %d MB" % (torch.cuda.memory_allocated()/(1024**2)))
print("Max memory allocated AFTER loading model: %d MB\n" % (torch.cuda.max_memory_allocated()/(1024**2)))

with open('shots.jsonl', 'r') as infile:
    data = json.load(infile)

domains, commands, solutions = [], [], []

for item in data:
    domains.append(data['shots'][item]['domain'])
    commands.append(data[item]['command'])
    solutions.append(data[item]['solution'])

generated_knowledge = 'instance tars robot|instance charging_station zone|instance unload_zone zone|instance shelf_1 zone|instance shelf_2 zone|instance shelf_3 zone|instance shelf_4 zone|predicate robot_availabletars|predicate is_recharge_zone charging_station|predicate is_unload_zone unload_zone|predicate is_shelf_zone shelf_1|predicate is_shelf_zone shelf_2|predicate is_shelf_zone shelf_3|predicate is_shelf_zone shelf_4|'
system_prompt = f'You are the robot tars, an automatic forklift that will move pallets around a warehouse. Your task is to outline the available instances, predicates, and goals based on the provided domain and command. Answer in the format shown after ### Output ###. This is the domain: {domains[0]}.'

messages = [{'role': 'user', 'content': system_prompt + f'At all times, these instances and predicates are true: {generated_knowledge}. You do not have to repeat them in your output.' + f' Here is a command {commands[0]}. ### Output ### {solutions[0]}.'},
           {'role': 'assistant', 'content': 'Understood. Awaiting new domain and command.'},
]
encodeds = tokenizer.apply_chat_template(messages, return_tensors='pt')

model_inputs = encodeds.to(device)
# model.to(device)

print("Memory allocated BEFORE inference: %d MB" % (torch.cuda.memory_allocated()/(1024**2)))
print("Max memory allocated BEFORE inference: %d MB\n" % (torch.cuda.max_memory_allocated()/(1024**2)))

generated_ids = model_nf4.generate(model_inputs, pad_token_id=tokenizer.eos_token_id, max_new_tokens=1000, do_sample=True)
decoded = tokenizer.batch_decode(generated_ids)

print("Memory allocated AFTER inference: %d MB" % (torch.cuda.memory_allocated()/(1024**2)))
print("Max memory allocated AFTER inference: %d MB\n" % (torch.cuda.max_memory_allocated()/(1024**2)))

# # Remove the pre-prompts and end-of-sentence token
output_tokens = decoded[0]
end_token = "[/INST]"

# # Find last occurence of end_tag in output
end_tag_index = output_tokens.rfind(end_token)
end_of_sentence = -4
sliced_output = output_tokens[end_tag_index + len(end_token):end_of_sentence]

torch.cuda.empty_cache()

delimiter = '|'

# start from the back of sliced_output and find the last occurence of delimiter
last_delimiter = sliced_output.rfind(delimiter)
# slice the string from the last occurence of delimiter to the end
sliced_output = sliced_output[:last_delimiter + 1]

print(sliced_output)