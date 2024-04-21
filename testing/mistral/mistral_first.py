import os
import torch
import json
import gc
import sys

test_set = int(sys.argv[1])

if sys.argv[2] == '4bit':
    _4bit = True
    _8bit = False
    half_precision = False
    full_precision = False

    results_file = 'mistral_results_4bit.txt'
    precision = '4-bit'
    test_set_file = 'test_set.jsonl'
elif sys.argv[2] == '8bit':
    _4bit = False
    _8bit = True
    half_precision = False
    full_precision = False

    results_file = 'mistral_results_8bit.txt'
    precision = '8-bit'
    test_set_file = 'test_set.jsonl'
elif sys.argv[2] == 'half':
    _4bit = False
    _8bit = False
    half_precision = True
    full_precision = False

    results_file = 'mistral_results_half_precision.txt'
    precision = 'half precision'
    test_set_file = 'test_set.jsonl'
elif sys.argv[2] == 'full':
    _4bit = False
    _8bit = False
    half_precision = False
    full_precision = True

    results_file = 'mistral_results_full_precision.txt'
    precision = 'full precision'
    test_set_file = 'test_set.jsonl'
elif sys.argv[2] == '4bit-specific':
    _4bit = True
    _8bit = False
    half_precision = False
    full_precision = False

    results_file = 'mistral_results_4bit_specific.txt'
    precision = '4-bit specific'
    test_set_file = 'test_set_specific.jsonl'    

if sys.argv[3] == 'idun':
    idun = True
elif sys.argv[3] == 'local':
    idun = False

if idun and _4bit:
    os.environ['HF_HOME'] = '/cluster/work/eliashk/models/mistral/4-bit'
elif idun and _8bit:
    os.environ['HF_HOME'] = '/cluster/work/eliashk/models/mistral/8-bit'
elif idun and half_precision:
    os.environ['HF_HOME'] = '/cluster/work/eliashk/models/mistral/half_precision'
elif idun and full_precision:
    os.environ['HF_HOME'] = '/cluster/work/eliashk/models/mistral/full_precision'

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

device = 'cuda'
model_id = 'mistralai/Mistral-7B-Instruct-v0.2'
tokenizer = AutoTokenizer.from_pretrained(model_id)

with open('shot_set.jsonl', 'r') as infile:
    shot_data = json.load(infile)

domains, inputs, outputs = [], [], []

for i in range(len(shot_data['shots'])):
    domains.append(shot_data['shots'][i]['domain'])
    inputs.append(shot_data['shots'][i]['input'])
    outputs.append(shot_data['shots'][i]['output'])

with open(test_set_file, 'r') as infile:
    test_data = json.load(infile)

test_domains, commands, solutions, num_instances, num_predicates, num_goals = [], [], [], [], [], []

for i in range(len(test_data['tests'])):
    test_domains.append(test_data['tests'][i]['domain'])
    commands.append(test_data['tests'][i]['command'])
    solutions.append(test_data['tests'][i]['solution'])
    num_instances.append(test_data['tests'][i]['num_instances'])
    num_predicates.append(test_data['tests'][i]['num_predicates'])
    num_goals.append(test_data['tests'][i]['num_goals'])

device_name = torch.cuda.get_device_properties(device).name
device_capacity = round(torch.cuda.get_device_properties(device).total_memory/(1024**2), 0)

header =      f"               Mistral Large Language Model {precision} test             \n"
underline =    "===========================================================================\n"
device_info = f"  Test completed on device {device_name} with {device_capacity} MB memory  \n" 

if not os.path.exists(results_file):
    with open(results_file, 'a') as outfile:
        outfile.write(header)
        outfile.write(underline)
        outfile.write(device_info)
        outfile.write(underline)

nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

nf8_config = BitsAndBytesConfig(
    load_in_8bit=True,
)

allocated, model_input_size, inference_times, model_outputs = [], [], [], []

number_of_max_new_tokens = 250  # default

generated_knowledge = 'instance tars robot|instance charging_station zone|instance unload_zone zone|instance shelf_1 zone|instance shelf_2 zone|instance shelf_3 zone|instance shelf_4 zone|predicate robot_availabletars|predicate is_recharge_zone charging_station|predicate is_unload_zone unload_zone|predicate is_shelf_zone shelf_1|predicate is_shelf_zone shelf_2|predicate is_shelf_zone shelf_3|predicate is_shelf_zone shelf_4|'
system_prompt = 'As a PDDL assistant, your task is to outline the available instances, predicates, and goals based on the provided domain and command. Answer in the format shown after ### Output ###.'
system_prompt_specific = f'You are the robot tars, an automatic forklift that will move pallets around a warehouse. Your task is to outline the available instances, predicates, and goals based on the provided domain and command. Answer in the format shown after ### Output ###. This is the domain: {test_domains[0]}.'

messages_list = [
                 [ # short and precise
                    {'role': 'user', 'content': system_prompt + f' Here is a domain: {domains[0]}, and command {inputs[0]}. ### Output ### {outputs[0]}.'},
                    {'role': 'assistant', 'content': 'Understood. Awaiting new domain and command.'},
                 ],
                 [ # medium detailed
                    {'role': 'user', 'content': system_prompt},
                    {'role': 'assistant', 'content': 'Understood, please give me a domain and command.'},
                    {'role': 'user', 'content': f'Here is a domain {domains[0]}, and command {inputs[0]}.'},
                    {'role': 'assistant', 'content': 'Thank you. What is the desired output?'},
                    {'role': 'user', 'content': f'### Output ### {outputs[0]}'},
                    {'role': 'assistant', 'content': 'Understood. I will generate an output based on a domain and command.'}
                 ],
                 [ # long and detailed
                    {'role': 'user', 'content': system_prompt},
                    {'role': 'assistant', 'content': 'Absolutely, I am ready to assist. Please provide the complete details of the domain and the specific command you wish to evaluate. This will enable me to accurately generate the necessary PDDL structures and outputs.'},
                    {'role': 'user', 'content': f'The domain under consideration is {domains[0]}, accompanied by the corresponding command {inputs[0]}. Please align the output format as described in the template provided.'},
                    {'role': 'assistant', 'content': ' I have received the information regarding the domain and command. To proceed accurately, could you please confirm the exact format for the output? This will ensure that the results are generated in complete alignment with your expectations and requirements for the PDDL environment.'},
                    {'role': 'user', 'content': f'The required output format should adhere to the following structure: ### Output ### {outputs[0]}'},
                    {'role': 'assistant', 'content': 'Your specifications have been meticulously noted. I am now fully prepared to process the subsequent set of data. Please provide the next domain and its associated command so that I can continue to deliver outputs that meet the high standards of accuracy and detail required.'},
                 ],

                 [  # user specific, short and precise, no generated knowledge
                    {'role': 'user', 'content': system_prompt_specific + f' Here is a command {commands[0]}. ### Output ### {solutions[0]}.'},
                    {'role': 'assistant', 'content': 'Understood. Awaiting new domain and command.'},
                 ],

                 [ # user specific, medium detailed, no generated knowledge
                    {'role': 'user', 'content': system_prompt_specific},
                    {'role': 'assistant', 'content': 'Understood, please give me a command.'},
                    {'role': 'user', 'content': f'Here is a command {commands[0]}.'},
                    {'role': 'assistant', 'content': 'Thank you. What is the desired output?'},
                    {'role': 'user', 'content': f'### Output ### {solutions[0]}'},
                    {'role': 'assistant', 'content': 'Understood. I will generate an output based on the domain and command.'}
                 ],

                 [ # user specific, long and detailed, no generated knowledge
                    {'role': 'user', 'content': system_prompt_specific},
                    {'role': 'assistant', 'content': 'As tars, I am ready to assist. Please provide the complete details of the specific command you wish to evaluate. This will enable me to accurately generate the necessary PDDL structures and outputs.'},
                    {'role': 'user', 'content': f'The command under consideration is {commands[0]}. Please align the output format as described in the template provided.'},
                    {'role': 'assistant', 'content': ' I have received the information regarding the domain and command. To proceed accurately, could you please confirm the exact format for the output? This will ensure that the results are generated in complete alignment with your expectations and requirements for the PDDL environment.'},
                    {'role': 'user', 'content': f'The required output format should adhere to the following structure: ### Output ### {solutions[0]}'},
                    {'role': 'assistant', 'content': 'Your specifications have been meticulously noted. I am now fully prepared to process the subsequent set of data. Please provide the next command so that I can continue to deliver outputs that meet the high standards of accuracy and detail required.'},
                 ],

                 [  # user specific, short and precise, generated knowledge
                    {'role': 'user', 'content': system_prompt_specific + f'At all times, these instances and predicates are true: {generated_knowledge}. You do not have to repeat them in your output.' + f' Here is a command {commands[0]}. ### Output ### {solutions[0]}.'},
                    {'role': 'assistant', 'content': 'Understood. Awaiting new domain and command.'},
                 ],

                 [ # user specific, medium detailed, generated knowledge
                    {'role': 'user', 'content': system_prompt_specific + f'At all times, these instances and predicates are true: {generated_knowledge}. You do not have to repeat them in your output.' },
                    {'role': 'assistant', 'content': 'Understood, please give me a command.'},
                    {'role': 'user', 'content': f'Here is a command {commands[0]}.'},
                    {'role': 'assistant', 'content': 'Thank you. What is the desired output?'},
                    {'role': 'user', 'content': f'### Output ### {solutions[0]}'},
                    {'role': 'assistant', 'content': 'Understood. I will generate an output based on the domain and command.'}
                 ],

                 [ # user specific, long and detailed, generated knowledge
                    {'role': 'user', 'content': system_prompt_specific + f'At all times, these instances and predicates are true: {generated_knowledge}. You do not have to repeat them in your output.' },
                    {'role': 'assistant', 'content': 'As tars, I am ready to assist. Please provide the complete details of the specific command you wish to evaluate. This will enable me to accurately generate the necessary PDDL structures and outputs.'},
                    {'role': 'user', 'content': f'The command under consideration is {commands[0]}. Please align the output format as described in the template provided.'},
                    {'role': 'assistant', 'content': ' I have received the information regarding the domain and command. To proceed accurately, could you please confirm the exact format for the output? This will ensure that the results are generated in complete alignment with your expectations and requirements for the PDDL environment.'},
                    {'role': 'user', 'content': f'The required output format should adhere to the following structure: ### Output ### {solutions[0]}'},
                    {'role': 'assistant', 'content': 'Your specifications have been meticulously noted. I am now fully prepared to process the subsequent set of data. Please provide the next command so that I can continue to deliver outputs that meet the high standards of accuracy and detail required.'},
                 ],
]

msg_idx = int(sys.argv[4])
messages = messages_list[msg_idx]

range_start = 1
range_end = 5

# endre range så vi får med alle shotsa
for i in range(range_start, range_end+1):
    number_of_examples = i+1
    
    if _4bit:
        model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=nf4_config)
    elif _8bit:
        model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=nf8_config)
    elif half_precision:
        model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.float16)
    elif full_precision:
        model = AutoModelForCausalLM.from_pretrained(model_id)

    allocated.append(round(torch.cuda.memory_allocated(device)/(1024**2), 5))

    if len(messages) > 2:
        del messages[-1:]

        if msg_idx == 0:
            messages.append({'role': 'user', 'content': f'Here is a new example. Domain: {domains[i]}, command: {inputs[i]}. ### Output ### {outputs[0]}.'})
            messages.append({'role': 'assistant', 'content': 'Understood. Awaiting new domain and command.'})
        
        if msg_idx == 1:
            messages.append({'role': 'user', 'content': f'Here is a domain {domains[i]}, and command {inputs[i]}.'})
            messages.append({'role': 'assistant', 'content': 'Thank you. What is the desired output?'})
            messages.append({'role': 'user', 'content': f'### Output ### {outputs[i]}'})
            messages.append({'role': 'assistant', 'content': 'Understood. I will generate an output based on a domain and command.'})
        
        if msg_idx == 2:
            messages.append({'role': 'user', 'content': f'The domain under consideration is {domains[i]}, accompanied by the corresponding command {inputs[i]}. Please align the output format as described in the template provided.'})
            messages.append({'role': 'assistant', 'content': ' I have received the information regarding the domain and command. To proceed accurately, could you please confirm the exact format for the output? This will ensure that the results are generated in complete alignment with your expectations and requirements for the PDDL environment.'})
            messages.append({'role': 'user', 'content': f'The required output format should adhere to the following structure: ### Output ### {outputs[i]}'})
            messages.append({'role': 'assistant', 'content': 'Your specifications have been meticulously noted. I am now fully prepared to process the subsequent set of data. Please provide the next domain and its associated command so that I can continue to deliver outputs that meet the high standards of accuracy and detail required.'})

        if msg_idx == 3 or msg_idx == 6:
            messages.append({'role': 'user', 'content': f'Here is a new example. Command: {commands[i]}. ### Output ### {solutions[0]}.'})
            messages.append({'role': 'assistant', 'content': 'Understood. Awaiting new command.'})
        
        if msg_idx == 4 or msg_idx == 7:
            messages.append({'role': 'user', 'content': f'Here is the command {commands[i]}.'})
            messages.append({'role': 'assistant', 'content': 'Thank you. What is the desired output?'})
            messages.append({'role': 'user', 'content': f'### Output ### {solutions[i]}'})
            messages.append({'role': 'assistant', 'content': 'Understood. I will generate an output based on a command.'})
        
        if msg_idx == 5 or msg_idx == 8:
            messages.append({'role': 'user', 'content': f'The command under consideration is {commands[i]}. Please align the output format as described in the template provided.'})
            messages.append({'role': 'assistant', 'content': ' I have received the information regarding the domain and command. To proceed accurately, could you please confirm the exact format for the output? This will ensure that the results are generated in complete alignment with your expectations and requirements for the PDDL environment.'})
            messages.append({'role': 'user', 'content': f'The required output format should adhere to the following structure: ### Output ### {solutions[i]}'})
            messages.append({'role': 'assistant', 'content': 'Your specifications have been meticulously noted. I am now fully prepared to process the subsequent set of data. Please provide the next command so that I can continue to deliver outputs that meet the high standards of accuracy and detail required.'})


    if msg_idx == 0:
        messages.append({'role': 'user', 'content': f'Domain: {test_domains[test_set]}, command: {commands[test_set]}. Give me the output.'})
        prompt = 1
    
    elif msg_idx == 1:
        messages.append({'role': 'user', 'content': f'Here is a domain {test_domains[test_set]}, and command {commands[test_set]}. Give me the output.'})
        prompt = 2

    elif msg_idx == 2:
        messages.append({'role': 'user', 'content': f'The domain under consideration is {test_domains[test_set]}, accompanied by the corresponding command {commands[test_set]}. Give me the output.'})
        prompt = 3
    
    elif msg_idx == 3:
        messages.append({'role': 'user', 'content': f'Command: {commands[i+1]}. Give me the output.'})
        prompt = 1
        generated_knowledge_bool = False
    
    elif msg_idx == 4:
        messages.append({'role': 'user', 'content': f'Here is the command {commands[i+1]}. Give me the output.'})
        prompt = 2
        generated_knowledge_bool = False
    
    elif msg_idx == 5:
        messages.append({'role': 'user', 'content': f'The command under consideration is {commands[i+1]}. Give me the output.'})
        prompt = 3
        generated_knowledge_bool = False
    
    elif msg_idx == 6:
        messages.append({'role': 'user', 'content': f'Command: {commands[i+1]}. Give me the output.'})
        prompt = 1
        generated_knowledge_bool = True
    
    elif msg_idx == 7:
        messages.append({'role': 'user', 'content': f'Here is the command {commands[i+1]}. Give me the output.'})
        prompt = 2
        generated_knowledge_bool = True
    
    elif msg_idx == 8:
        messages.append({'role': 'user', 'content': f'The command under consideration is {commands[i+1]}. Give me the output.'})
        prompt = 3
        generated_knowledge_bool = True

    # start timer
    start = torch.cuda.Event(enable_timing=True)
    start.record()

    # inference
    encodeds = tokenizer.apply_chat_template(messages, return_tensors='pt')
    model_inputs = encodeds.to(device)

    model_input_size.append(round((model_inputs.element_size()*model_inputs.nelement())/(1024**2), 5))    # MB
    
    with torch.no_grad():
        generated_ids = model.generate(
            model_inputs,
            pad_token_id=tokenizer.eos_token_id,
            max_new_tokens=number_of_max_new_tokens,
            do_sample=True,
        )
        
    decoded = tokenizer.batch_decode(generated_ids)

    end = torch.cuda.Event(enable_timing=True)
    end.record()
    
    torch.cuda.synchronize()

    # compute inference time
    timer = start.elapsed_time(end)/1000
    inference_times.append(timer)

    '''
    Format the output string - remove the last 4 characters which are the end token,
    then remove everything after the last delimiter and
    remove everything before the first occurence of "instance" or "### Output ### ".
    Finally, remove newlines in output
    '''
    output_tokens = decoded[0]
    end_token = '[/INST]'

    end_tag_index = output_tokens.rfind(end_token)
    end_of_sentence = -4
    sliced_output = output_tokens[end_tag_index + len(end_token):end_of_sentence]

    delimiter = '|'
    last_delimiter = sliced_output.rfind(delimiter)
    model_output = sliced_output[:last_delimiter+1]

    # check if the model output contains "### Output ### " and delete everything before it.
    # if not found, delete everything before first "instance"
    output_flag = '### Output ### '
    expected_output_index = model_output.find(output_flag)
    
    if expected_output_index != -1:
        model_output = model_output[expected_output_index + len(output_flag):]
    else:
        model_output = model_output[model_output.find('instance'):]

    # remove newlines in output
    model_output = model_output.replace('\n', ' ')
    model_output = model_output.replace('\t', ' ')
    model_output = model_output.replace('\r', ' ')
    model_output = model_output.replace('  ', ' ')

    model_outputs.append(model_output)

    # write the results to file
    result = {
        'Model': model_id + f' --- {precision}',
        'Max new tokens': number_of_max_new_tokens,
        'Prompt number': prompt,
        'Test set #': i + 1,
        'Number of examples': number_of_examples,
        'Inference time [s]': inference_times[-1],
        'GPU memory loaded [MB]': allocated[-1],
        'Model input size [MB]': model_input_size[-1],
        'Sliced output': model_outputs[-1],
        'Solution': solutions[test_set],
        'Labeled': 'No',
        'Generated knowledge': generated_knowledge_bool,
    }

    with open(results_file, 'a') as outfile:
        for key, value in result.items():
            outfile.write(f'{key:<25}: {value}\n')
        outfile.write(underline)

    print(f'Mistral 7B instruct {precision} finished on test {test_set + 1} with {number_of_examples} examples and prompt {prompt}. No label.')

    # delete model to free up GPU memory
    del model
    del model_inputs
    del generated_ids
    torch.cuda.empty_cache()
    gc.collect()

# clean up
torch.cuda.empty_cache()
gc.collect()