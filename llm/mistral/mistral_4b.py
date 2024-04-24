import os
os.environ['HF_HOME']='/home/stinky/models'
# os.environ['HF_HOME']='/home/carla/elias/models'

import torch
<<<<<<< HEAD
import json
import gc
import sys

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

device = 'cuda'
=======
torch.cuda.empty_cache()

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

device = 'cuda:0'
>>>>>>> main
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

<<<<<<< HEAD
model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=nf4_config)
=======
model_nf4 = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=nf4_config)
>>>>>>> main

print("Memory allocated AFTER loading model: %d MB" % (torch.cuda.memory_allocated()/(1024**2)))
print("Max memory allocated AFTER loading model: %d MB\n" % (torch.cuda.max_memory_allocated()/(1024**2)))

<<<<<<< HEAD
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
=======

question = 'Move the new pallet from the unload zone to shelf 2 and recharge at the charging station.'

messages = [
        {'role': 'user', 'content': 'You will be receiving a natural language input from me, and you will return a text based on the input and on the format that I will show you three examples of. You will act based on a PDDL domain file.'},
        {'role': 'assistant', 'content': 'I understand. Give me the domain.pddl'},
        {'role': 'user', 'content': '(define (domain warehouse)(:types robot zone pallet)(:predicates(robot_available ?robot - robot)(robot_at ?robot - robot ?zone - zone)(pallet_at ?pallet - pallet ?zone - zone)(is_pallet ?pallet - pallet)(pallet_not_moved ?pallet - pallet)(is_unload_zone ?zone - zone)(is_reol_zone ?zone - zone))'},
        {'role': 'assistant', 'content': 'I see. This is the types and predicates in the domain.pddl.'},
        {'role': 'user', 'content': 'Yes. I will show you an example, and you will see the format of the input and the output. Only answer in the same format as this example.'},
        {'role': 'assistant', 'content': 'Understood, I will learn from the coming example and see how I shall respond. Only special characters I can use is "|", "(", ")" and "_".'},
        {'role': 'user', 'content': 'Prompt: A new shipment arrived. Please move the new pallet from the unload zone to reol 1. Afterwards, wait at reol 2. -> Correct output: set instance pallet_1 pallet|set predicate pallet_at pallet_1 unload_zone|set predicate pallet_not_moved pallet_1|set goal pallet_at pallet_1 reol_1|set goal robot_at tars reol_2|'},
        {'role': 'assistant', 'content': 'I understand the format. I will respond in the same format. Please give me the input.'},
        {'role': 'user', 'content': question},
    ]

>>>>>>> main
encodeds = tokenizer.apply_chat_template(messages, return_tensors='pt')

model_inputs = encodeds.to(device)
# model.to(device)

print("Memory allocated BEFORE inference: %d MB" % (torch.cuda.memory_allocated()/(1024**2)))
print("Max memory allocated BEFORE inference: %d MB\n" % (torch.cuda.max_memory_allocated()/(1024**2)))

<<<<<<< HEAD
generated_ids = model_nf4.generate(model_inputs, pad_token_id=tokenizer.eos_token_id, max_new_tokens=1000, do_sample=True)
=======
generated_ids = model_nf4.generate(model_inputs, pad_token_id=tokenizer.eos_token_id, max_new_tokens=100, do_sample=True)
>>>>>>> main
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