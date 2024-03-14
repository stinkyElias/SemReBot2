import os
os.environ['HF_HOME'] = '/home/stinky/models'

import rclpy
import torch
torch.cuda.empty_cache()

from rclpy.node import Node
from std_msgs.msg import String
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

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

            self.get_logger().info("Loaded model %s" % model_name_)
            self.get_logger().info("Node mistral_node has current state active. Waiting for natural language input.")
        except:
            self.get_logger().error("Failed to load model %s" % model_name_)
            raise Exception("Failed to load model %s" % model_name_)
    
    def get_command_callback(self, msg):
        self.get_logger().info("Received command:\n %s" % msg.data)

def main(args=None):
    rclpy.init(args=args)

    mistral_node = MistralNode()

    rclpy.spin(mistral_node)

    mistral_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

        