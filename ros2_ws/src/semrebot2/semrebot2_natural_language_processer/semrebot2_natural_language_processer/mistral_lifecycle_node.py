import os
os.environ['HF_HOME'] = '/home/stinky/models'

import rclpy
import torch
import gc
import re
import jsonl

from rclpy.lifecycle import LifecycleNode, LifecycleState, TransitionCallbackReturn
from std_msgs.msg import String
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from ament_index_python.packages import get_package_share_directory

class MistralNode(LifecycleNode):
    def __init__(self, node_name) -> None:
        super().__init__(node_name)

        self.node_name = node_name
        self.publisher_ = None
        self.subscriber_ = None
        self.domain = None

        self.commands, self.solutions = [], []
        self.data = None

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
        package_dir = get_package_share_directory('semrebot2_natural_language_processer')
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

        self.get_logger().info(f"domain.pddl successfully extracted")

        # Load shots for few-shot prompting
        shot_dir = os.path.join(package_dir, 'config', 'shots.jsonl')
        
        with open(shot_dir, 'r') as infile:
            self.data = jsonl.load(infile)
        
        for i in range(len(data['shots'])):
            self.commands.append(data['shots'][i]['command'])
            self.solutions.append(data['shots'][i]['solution'])
        
        if self.commands and self.solutions:
            self.get_logger().info(f"Successfully loaded {len(self.commands)} commands and {len(self.solutions)} solutions")
        else:
            self.get_logger().error(f"Failed to load commands and solutions")

            return TransitionCallbackReturn.ERROR

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
        generated_knowledge = 'instance tars robot|instance charging_station zone|instance unload_zone zone|instance shelf_1 zone|instance shelf_2 zone|instance shelf_3 zone|instance shelf_4 zone|predicate robot_availabletars|predicate is_recharge_zone charging_station|predicate is_unload_zone unload_zone|predicate is_shelf_zone shelf_1|predicate is_shelf_zone shelf_2|predicate is_shelf_zone shelf_3|predicate is_shelf_zone shelf_4|'
        system_prompt = f'You are the robot tars, an automatic forklift that will move pallets around a warehouse. Your task is to outline the available instances, predicates, and goals based on the provided domain and command. Answer in the format shown after ### Output ###. This is the domain: {domains[0]}.'

        messages = [
            {'role': 'user', 'content': system_prompt + f'At all times, these instances and predicates are true: {generated_knowledge}. You do not have to repeat them in your output.' + f' Here is a command {commands[0]}. ### Output ### {solutions[0]}.'},
            {'role': 'assistant', 'content': 'Understood. Awaiting new domain and command.'},
        ]

        for i in range(1, len(self.data['shots'])):
            messages.append({'role': 'user', 'content': f'Command: {self.commands[i]}'})
            messages.append({'role': 'assistant', 'content': f'### Output ### {self.solutions[i]}'})

        messages.append({'role': 'user', 'content': f'Command: {msg.data}'})

        encodeds = self.tokenizer_.apply_chat_template(messages, return_tensors='pt')
        model_inputs = encodeds.to(self.device_)

        self.get_logger().info("Generating response")
        generated_ids = self.model.generate(model_inputs,
                                            pad_token_id=self.tokenizer_.eos_token_id,
                                            max_new_tokens=1000,
                                            do_sample=True)
        
        decoded = self.tokenizer_.batch_decode(generated_ids)

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

        pub_msg.data = decoded[0]

        self.publisher_.publish(pub_msg)
        self.get_logger().info(f"Generated response:\n {pub_msg.data}")

        training_msg = String()
        training_msg.data = "instance pallet_1 pallet|predicate pallet_at pallet_1 unload_zone|predicate pallet_not_moved pallet_1|goal pallet_at pallet_1 shelf_1|instance pallet_2 pallet|predicate pallet_at pallet_2 unload_zone|predicate pallet_not_moved pallet_2|goal pallet_at pallet_2 shelf_2|"
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

        