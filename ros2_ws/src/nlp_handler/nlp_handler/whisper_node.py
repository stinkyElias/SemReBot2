import os
os.environ['HF_HOME'] = '/home/stinky/models'

import rclpy
import torch

from rclpy.node import Node
from std_msgs.msg import String, Int8
from transformers import pipeline
from transformers.utils import is_flash_attn_2_available

class WhisperNode(Node):   
    def __init__(self) -> None:
        super().__init__('whisper_node')

        self.declare_parameters(
            namespace='',
            parameters=[
                ('model_name', ''),
                ('audio_dir', ''),
                ('data_type', ''),
                ('device', ''),
                ('chunk_length', 0),
                ('batch_size', 0)
            ]
        )

        self.model_name_ = self.get_parameter('model_name').get_parameter_value().string_value
        self.audio_dir_ = self.get_parameter('audio_dir').get_parameter_value().string_value
        dtype = self.get_parameter('data_type').get_parameter_value().string_value
        
        self.publisher_ = self.create_publisher(String, 'whisper_output', 10)
        self.subscriber_ = self.create_subscription(Int8, 'whisper_input', self.get_command_callback, 10)

        dtype_map = {
            'float16': torch.float16,
            'float32': torch.float32,
            'float64': torch.float64,
        }

        torch_dtype = dtype_map.get(dtype, torch.float16)

        device_ = self.get_parameter('device').get_parameter_value().string_value if torch.cuda.is_available() else 'cpu'

        try:
            self.asr_pipeline_ = pipeline(
                'automatic-speech-recognition',
                model=self.model_name_,
                torch_dtype=torch_dtype,
                device=device_,
                model_kwargs={'attn_implementation': 'flash_attention_2'} if is_flash_attn_2_available() else {'attn_implementation': 'sdpa'},
            )
            
            self.get_logger().info("Loaded model %s to device %s" % (self.model_name_, device_))
            self.get_logger().info("Node whisper_node has current state active. Waiting for audio input.")

        except:
            self.get_logger().error("Failed to load model %s" % self.model_name_)
            raise Exception("Failed to load model %s" % self.model_name_)

    def get_command_callback(self, incoming_msg: Int8) -> None:
        try:
            if incoming_msg.data == 1:
                audio_data = os.path.join(self.audio_dir_, str(incoming_msg.data) + '.wav')
            elif incoming_msg.data == 2:
                audio_data = os.path.join(self.audio_dir_, str(incoming_msg.data) + '.wav')
            elif incoming_msg.data == 3:
                audio_data = os.path.join(self.audio_dir_, str(incoming_msg.data) + '.wav')
            elif incoming_msg.data == 4:
                audio_data = os.path.join(self.audio_dir_, str(incoming_msg.data) + '.wav')
        except:
            self.get_logger().error("No such audio file %i.wav" % incoming_msg.data)
            return
        
        self.get_logger().info("Transcribing audio file %i.wav" % incoming_msg.data)
        output = self.asr_pipeline_(
            audio_data,
            chunk_length_s=self.get_parameter('chunk_length').get_parameter_value().integer_value,
            batch_size=self.get_parameter('batch_size').get_parameter_value().integer_value,
            return_timestamps=True,
        )
        self.get_logger().info("Transcription complete.")

        msg = String()
        msg.data = output['text']

        self.publisher_.publish(msg)
        self.get_logger().info("Publishing transcribed audio.")
           
    
def main(args=None):
    torch.cuda.empty_cache()
    rclpy.init(args=args)
    whisper_node = WhisperNode()
    
    rclpy.spin(whisper_node)
    
    whisper_node.destroy_node()
    rclpy.shutdown()
    torch.cuda.empty_cache()

if __name__ == '__main__':
    main()
