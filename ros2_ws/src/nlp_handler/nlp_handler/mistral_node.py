import os
os.environ['HF_HOME'] = '/home/stinky/models'

import rclpy
import torch

from rclpy.node import Node
from std_msgs.msg import String
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from transformers import BitsAndBytesConfig

class MistralNode(Node):
    def __init__(self) -> None:
        super().__init__('mistral_node')

        self.declare_parameters(
            namespace='',
            parameters=[
                ('model_name', ''),
                ('device', ''),
            ]
        )

        model_name_ = self.get_parameter('model_name').get_parameter_value().string_value
        self.device_ = self.get_parameter('device').get_parameter_value().string_value

        self.publisher_ = self.create_publisher(String, 'mistral_output', 10)
        self.subscriber_ = self.create_subscription(String, 'whisper_output', self.get_command_callback, 10)

        self.tokenizer_ = AutoTokenizer.from_pretrained(model_name_)

        nf4_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
        )

        try:
            self.model = AutoModelForCausalLM.from_pretrained(model_name_, config=nf4_config)

            self.get_logger().info("Loaded model %s to device %s" % (model_name_, self.device_))
            self.get_logger().info("Node mistral_node has current state active. Waiting for natural language input.")

        except:
            self.get_logger().error("Failed to load model %s" % model_name_)
            raise Exception("Failed to load model %s" % model_name_)
    
    def get_command_callback(self, msg):
        pub_msg = String()
        
        self.get_logger().info("Received command:\n %s" % msg.data)

        # pre-prompt
        messages = [
            {'role': 'user', 'content': 'You will be receiving a natural language input from me, and you will return a text based on the input and on the format that I will show you three examples of. You will act based on a PDDL domain file.'},
            {'role': 'assistant', 'content': 'I understand. Give me the domain.pddl'},
            {'role': 'user', 'content': '(define (domain warehouse)(:types robot zone pallet)(:predicates(robot_available ?robot - robot)(robot_at ?robot - robot ?zone - zone)(pallet_at ?pallet - pallet ?zone - zone)(is_pallet ?pallet - pallet)(pallet_not_moved ?pallet - pallet)(is_unload_zone ?zone - zone)(is_reol_zone ?zone - zone))'},
            {'role': 'assistant', 'content': 'I see. This is the types and predicates in the domain.pddl.'},
            {'role': 'user', 'content': 'Yes. I will show you an example, and you will see the format of the input and the output. Only answer in the same format as this example.'},
            {'role': 'assistant', 'content': 'Understood, I will learn from the coming example and see how I shall respond. Only special characters I can use is "|", "(", ")" and "_".'},
            {'role': 'user', 'content': 'Prompt: A new shipment arrived. Please move the new pallet from the unload zone to reol 1. Afterwards, wait at reol 2. -> Correct output: set instance pallet_1 pallet|set predicate pallet_at pallet_1 unload_zone|set predicate pallet_not_moved pallet_1|set goal pallet_at pallet_1 reol_1|set goal robot_at tars reol_2|'},
            {'role': 'assistant', 'content': 'I understand the format. I will respond in the same format. Please give me the input.'},
            {'role': 'user', 'content': msg.data},
        ]

        self.get_logger().info("Generating response...")
        encodeds = self.tokenizer_.apply_chat_template(messages, return_tensors='pt')
        model_inputs = encodeds.to(self.device_)

        generated_ids = self.model.generate(model_inputs,
                                            pad_token_id=self.tokenizer_.eos_token_id,
                                            max_new_tokens=100,
                                            do_sample=True)
        
        decoded = self.tokenizer_.batch_decode(generated_ids)

        output_tokens = decoded[0]
        end_token = "[/INST]"

        end_tag_index = output_tokens.rfind(end_token)
        end_of_sentence = -4
        sliced_output = output_tokens[end_tag_index + len(end_token):end_of_sentence]

        delimiter = '|'
        last_delimiter = sliced_output.rfind(delimiter)
        sliced_output = sliced_output[:last_delimiter + 1]
        self.get_logger().info("Generated response.")

        pub_msg.data = sliced_output

        self.publisher_.publish(pub_msg)
        self.get_logger().info("Published response:\n %s" % pub_msg.data)

def main(args=None):
    torch.cuda.empty_cache()
    rclpy.init(args=args)

    mistral_node = MistralNode()

    rclpy.spin(mistral_node)

    mistral_node.destroy_node()
    rclpy.shutdown()
    torch.cuda.empty_cache()

if __name__ == '__main__':
    main()

        