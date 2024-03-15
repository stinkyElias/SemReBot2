import os
# os.environ['HF_HOME']='/home/stinky/models'
os.environ['HF_HOME']='/home/carla/elias/models'

import torch
torch.cuda.empty_cache()

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

device = 'cuda:0'
model_id = 'mistralai/Mistral-7B-Instruct-v0.2'

tokenizer = AutoTokenizer.from_pretrained(model_id)

nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

print("Memory allocated 0: %d" % torch.cuda.memory_allocated())
print("Max memory allocated 0: %d" % torch.cuda.max_memory_allocated())

model_nf4 = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=nf4_config)

print("Memory allocated 1: %d" % torch.cuda.memory_allocated())
print("Max memory allocated 1: %d" % torch.cuda.max_memory_allocated())


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

encodeds = tokenizer.apply_chat_template(messages, return_tensors='pt')

model_inputs = encodeds.to(device)
# model.to(device)

print("Memory allocated 2: %d" % torch.cuda.memory_allocated())
print("Max memory allocated 2: %d" % torch.cuda.max_memory_allocated())

generated_ids = model_nf4.generate(model_inputs, pad_token_id=tokenizer.eos_token_id, max_new_tokens=100, do_sample=True)
decoded = tokenizer.batch_decode(generated_ids)

print("Memory allocated 3: %d" % torch.cuda.memory_allocated())
print("Max memory allocated 3: %d" % torch.cuda.max_memory_allocated())

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