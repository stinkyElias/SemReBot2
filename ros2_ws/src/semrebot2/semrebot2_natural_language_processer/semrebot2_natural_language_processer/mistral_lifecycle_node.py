import os
os.environ['HF_HOME'] = '/home/stinky/models'
<<<<<<< HEAD
# result_dir = '/home/stinky/ros2_ws/results'
=======
>>>>>>> main

import rclpy
import torch
import gc
import re
<<<<<<< HEAD
import json
=======
>>>>>>> main

from rclpy.lifecycle import LifecycleNode, LifecycleState, TransitionCallbackReturn
from std_msgs.msg import String
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
<<<<<<< HEAD
from ament_index_python.packages import get_package_share_directory
=======
from transformers import BitsAndBytesConfig
>>>>>>> main

class MistralNode(LifecycleNode):
    def __init__(self, node_name) -> None:
        super().__init__(node_name)

        self.node_name = node_name
        self.publisher_ = None
        self.subscriber_ = None
        self.domain = None

<<<<<<< HEAD
        self.commands, self.solutions = [], []
        self.data = None

=======
>>>>>>> main
        self.declare_parameters(
            namespace='',
            parameters=[
                ('model_name', ''),
                ('device', ''),
            ]
        )
        self.get_logger().info("Current state unconfigured [1]")

    def on_configure(self, state: LifecycleState) -> TransitionCallbackReturn:
        model_name_ = self.get_parameter('model_name').get_parameter_value().string_value
        self.device_ = self.get_parameter('device').get_parameter_value().string_value

        self.tokenizer_ = AutoTokenizer.from_pretrained(model_name_)

        nf4_config = BitsAndBytesConfig(
            load_in_4bit=True,  
            bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        
        # Read domain file and extract only the available types and predicates
        home_dir = os.path.expanduser('~')
        domain_dir = os.path.join(home_dir, 'ros2_ws/src/semrebot2/semrebot2_task_controller/pddl/domain.pddl')

        with open(domain_dir, 'r') as file:
            data = file.read()
        
        domain = data.replace('\n', ' ').replace('\r', ' ')
        domain = ' '.join(domain.split())

        types_start = domain.find(':types')
        types_end = domain.find(')', types_start)

        predicates_start = domain.find(':predicates')

        match = re.search('\)\s*\)', domain[predicates_start:])
        
        if match:
            predicates_end = predicates_start + match.start() + 1
        else:
            self.get_logger().error(f"Couldn't read domain.pddl due to mismatch in expected predicates syntax")

            return TransitionCallbackReturn.ERROR

        types = domain[types_start:types_end + 1]
        predicates = domain[predicates_start:predicates_end + 1]

        self.domain = '(' + types + ' (' + predicates + ')'

<<<<<<< HEAD
        self.get_logger().info(f"domain.pddl successfully extracted")

        # Load shots for few-shot prompting
        shot_dir = os.path.join(home_dir, 'ros2_ws/src/semrebot2/semrebot2_natural_language_processer/config/shots.jsonl')
        
        with open(shot_dir, 'r') as infile:
            self.data = json.load(infile)
        
        for i in range(len(self.data['shots'])):
            self.commands.append(self.data['shots'][i]['command'])
            self.solutions.append(self.data['shots'][i]['solution'])

        if self.commands and self.solutions:
            self.get_logger().info(f"Successfully loaded {len(self.commands)} commands and {len(self.solutions)} solutions for prompting")
        else:
            self.get_logger().error(f"Failed to load commands and solutions")

            return TransitionCallbackReturn.ERROR
=======
        self.get_logger().info(f"Types and predicates successfully extracted from domain.pddl: {self.domain}")
>>>>>>> main

        # Load the model to memory
        try:
            self.model = AutoModelForCausalLM.from_pretrained(model_name_,
                                                              quantization_config=nf4_config)

            self.get_logger().info(f"Loaded model {model_name_} to device {self.device_}")

            return TransitionCallbackReturn.SUCCESS
        
        except Exception as e:
            self.get_logger().error(f"Failed to load model {model_name_} to device {self.device_}: {e}")       
            return TransitionCallbackReturn.ERROR
    
    def on_cleanup(self, state: LifecycleState) -> TransitionCallbackReturn:
        try:
            del self.model
            gc.collect()
            torch.cuda.empty_cache()
        
            return TransitionCallbackReturn.SUCCESS
        
        except Exception as e:
            self.get_logger().error(f"Failed to cleanup model {self.model_name_}: {e}")
            return TransitionCallbackReturn.ERROR
    
    def on_activate(self, state: LifecycleState) -> TransitionCallbackReturn:
        self.publisher_ = self.create_lifecycle_publisher(String,
                                                          'pddl_command',
                                                          10)
        self.subscriber_ = self.create_subscription(String,
                                                    'command',
                                                    self.get_command_callback,
                                                    10)

        return super().on_activate(state)
    
    def on_deactivate(self, state: LifecycleState) -> TransitionCallbackReturn:
        self.destroy_lifecycle_publisher(self.publisher_)
        self.destroy_subscription(self.subscriber_)

        return super().on_deactivate(state)

    def on_shutdown(self, state: LifecycleState) -> TransitionCallbackReturn:
        try:
            del self.model
            gc.collect()
            torch.cuda.empty_cache()

            self.destroy_lifecycle_publisher(self.publisher_)
            self.destroy_subscription(self.subscriber_)

            return TransitionCallbackReturn.SUCCESS
        
        except Exception as e:
            self.get_logger().error(f"Failed to cleanup model {self.model_name_}: {e}")
            return TransitionCallbackReturn.ERROR


    def get_command_callback(self, msg):
        pub_msg = String()
        
        # pre-prompt
<<<<<<< HEAD
        generated_knowledge = 'instance tars robot|instance charging_station zone|instance unload_zone zone|instance shelf_1 zone|instance shelf_2 zone|instance shelf_3 zone|instance shelf_4 zone|predicate robot_availabletars|predicate is_recharge_zone charging_station|predicate is_unload_zone unload_zone|predicate is_shelf_zone shelf_1|predicate is_shelf_zone shelf_2|predicate is_shelf_zone shelf_3|predicate is_shelf_zone shelf_4|'
        system_prompt = f'You are the robot tars, an automatic forklift that will move pallets around a warehouse. Your task is to outline the available instances, predicates, and goals based on the provided domain and command. Answer in the format shown after ### Output ###. This is the domain: {self.domain}.'

        messages = [
            {'role': 'user', 'content': system_prompt + f'At all times, these instances and predicates are true: {generated_knowledge}. You do not have to repeat them in your output.' + f' Here is a command {self.commands[0]}. ### Output ### {self.solutions[0]}.'},
            {'role': 'assistant', 'content': 'Understood. Awaiting new domain and command.'},
        ]

        for i in range(1, len(self.data['shots'])):
            messages.append({'role': 'user', 'content': f'Command: {self.commands[i]}'})
            messages.append({'role': 'assistant', 'content': f'### Output ### {self.solutions[i]}'})

        messages.append({'role': 'user', 'content': f'Command: {msg.data}'})

=======
        messages = [
            {'role': 'user',        'content': 'You will receive a natural language prompt and create text based on the prompt and a domain from domain.pddl.'},
            {'role': 'assistant',   'content': 'I understand. Give me the domain.pddl'},
            {'role': 'user',        'content': 'domain.pddl: ' + self.domain},
            {'role': 'assistant',   'content': 'Thank you. This is the types and predicates in the domain.pddl.'},
            {'role': 'user',        'content': 'Yes. I will show you an example, and you will see the format of a prompt and the only accepted format to answer in. Only answer in the same format as this example.'},
            {'role': 'assistant',   'content': 'Understood, I will learn from the coming example and see how I shall respond.'},
            {'role': 'user',        'content': 'Prompt: "A new shipment arrived. Please move the new pallet from the unload zone to reol 1. Afterwards, wait at reol 2". From this prompt, the only correct answer would be: set instance pallet_1 pallet|set predicate pallet_at pallet_1 unload_zone|set predicate pallet_not_moved pallet_1|set goal pallet_at pallet_1 reol_1|set goal robot_at tars reol_2|'},
            {'role': 'assistant',   'content': 'I understand the format. I will respond in the same format, only setting instances, predicates and goals delimited by "|". Please give me the prompt.'},
            {'role': 'user',        'content': 'Prompt: ' + msg.data},
        ]

>>>>>>> main
        encodeds = self.tokenizer_.apply_chat_template(messages, return_tensors='pt')
        model_inputs = encodeds.to(self.device_)

        self.get_logger().info("Generating response")
        generated_ids = self.model.generate(model_inputs,
                                            pad_token_id=self.tokenizer_.eos_token_id,
<<<<<<< HEAD
                                            max_new_tokens=1000,
=======
                                            max_new_tokens=100,
>>>>>>> main
                                            do_sample=True)
        
        decoded = self.tokenizer_.batch_decode(generated_ids)

<<<<<<< HEAD
        start_token = '[/INST]'
        start_tag_index = decoded[0].rfind(start_token)
        decoded[0] = decoded[0][start_tag_index+len(start_token):]

        end_token = '</s>'
        end_tag_index = decoded[0].rfind(end_token)
        decoded[0] = decoded[0][:end_tag_index]

        delimiter = '|'
        last_delimiter_index = decoded[0].rfind(delimiter)
        decoded[0] = decoded[0][:last_delimiter_index+len(delimiter)]

        output_token = '### Output ###'
        output_tag_index = decoded[0].find(output_token)
        decoded[0] = decoded[0][output_tag_index+len(output_token)+1:]

        first_instance = decoded[0].find('instance ')
        first_predicate = decoded[0].find('predicate ')
        first_goal = decoded[0].find('goal ')

        if first_instance != -1 and (first_predicate == -1 or first_instance < first_predicate) and (first_goal == -1 or first_instance < first_goal):
            decoded[0] = decoded[0][first_instance:]
        elif first_predicate != -1 and (first_goal == -1 or first_predicate < first_goal):
            decoded[0] = decoded[0][first_predicate:]
        elif first_goal != -1:
            decoded[0] = decoded[0][first_goal:]

        for i in range(len(decoded[0])):
            if decoded[0][i] == delimiter:
                j = i+1
                
                while j < len(decoded[0]) and decoded[0][j].isspace():
                    j += 1

                if j < len(decoded[0]) and decoded[0][j] not in ['i', 'p', 'g']:
                    decoded[0] = decoded[0][:i+len(delimiter)]
                    break

        pub_msg.data = decoded[0]

        # # write to file
        # with open(os.path.join(result_dir, 'results.txt'), 'a') as outfile:
        #     outfile.write(f'Mistral: \n{pub_msg.data}\n\n')

        self.publisher_.publish(pub_msg)
        self.get_logger().info(f"Generated response")

        # training_msg = String()
        # training_msg.data = "instance pallet_1 pallet|predicate pallet_at pallet_1 unload_zone|predicate pallet_not_moved pallet_1|goal pallet_at pallet_1 shelf_1|instance pallet_2 pallet|predicate pallet_at pallet_2 unload_zone|predicate pallet_not_moved pallet_2|goal pallet_at pallet_2 shelf_2|"
=======
        output_tokens = decoded[0]
        end_token = "[/INST]"

        end_tag_index = output_tokens.rfind(end_token)
        end_of_sentence = -4
        sliced_output = output_tokens[end_tag_index + len(end_token):end_of_sentence]

        delimiter = '|'
        last_delimiter = sliced_output.rfind(delimiter)
        sliced_output = sliced_output[:last_delimiter + 1]

        # remove newlines
        sliced_output = sliced_output.replace('\n', '')
        # remove leading whitespaces
        sliced_output = sliced_output.strip()

        pub_msg.data = sliced_output

        self.publisher_.publish(pub_msg)
        self.get_logger().info(f"Generated response:\n {pub_msg.data}")

        # training_msg = String()
        # training_msg.data = "set instance pallet_2 pallet|set predicate pallet_at pallet_2 unload_zone|set predicate pallet_not_moved pallet_2|set goal pallet_at pallet_2 shelf_2|set goal robot_at tars charging_station|"

>>>>>>> main
        # self.publisher_.publish(training_msg)

        torch.cuda.empty_cache()

def main(args=None):
    torch.cuda.empty_cache()

    rclpy.init(args=args)
    mistral_node = MistralNode('mistral')

    rclpy.spin(mistral_node)

    mistral_node.destroy_node()
    rclpy.shutdown()

    torch.cuda.empty_cache()

if __name__ == '__main__':
    main()

        