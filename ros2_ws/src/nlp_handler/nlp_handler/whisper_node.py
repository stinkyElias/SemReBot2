import os
os.environ['HF_HOME'] = '/home/stinky/models'

import rclpy
import torch

from rclpy.node import Node
from std_msgs.msg import String, Int8
from transformers import pipeline
from transformers.utils import is_flash_attn_2_available

class WhisperNode(Node):
    # STT model parameters
    model_name_='openai/whisper-large-v3'
    device_='cuda:0' if torch.cuda.is_available() else 'cpu'
    
    def __init__(self) -> None:
        super().__init__('whisper_node')
        
        self.publisher_ = self.create_publisher(String, 'whisper_output', 10)
        self.subscriber_ = self.create_subscription(Int8, 'whisper_input', self.get_command_callback, 10)
        
        # load whisper model
        try:
            self.asr_pipeline_ = pipeline(
                'automatic-speech-recognition',
                model=self.model_name_,
                torch_dtype=torch.float16,
                device=self.device_,
                model_kwargs={'attn_implementation': 'flash_attention_2'} if is_flash_attn_2_available() else {'attn_implementation': 'sdpa'},
            )
            
            self.get_logger().info("Loaded model %s" % self.model_name_)
        except:
            self.get_logger().error("Failed to load model %s" % self.model_name_)
            raise Exception("Failed to load model %s" % self.model_name_)

    def get_command_callback(self, incoming_msg: Int8) -> None:
        try:
            if incoming_msg.data == 1:
                audio_data = '/home/stinky/ros2_ws/src/nlp_handler/audio_files/1.wav'
            elif incoming_msg.data == 2:
                audio_data = '/home/stinky/ros2_ws/src/nlp_handler/audio_files/2.wav'
            elif incoming_msg.data == 3:
                audio_data = '/home/stinky/ros2_ws/src/nlp_handler/audio_files/3.wav'
            elif incoming_msg.data == 4:
                audio_data = '/home/stinky/ros2_ws/src/nlp_handler/audio_files/4.wav'
        except:
            self.get_logger().error("No such audio file %i." % incoming_msg.data)
            return
        
        self.get_logger().info("Transcribing audio file %i.wav" % incoming_msg.data)
        output = self.asr_pipeline_(
            audio_data,
            chunk_length_s=30,
            batch_size=24,
            return_timestamps=True,
        )
        self.get_logger().info("Transcription complete.")

        msg = String()
        msg.data = output['text']

        self.publisher_.publish(msg)
        self.get_logger().info("Publishing transcribed audio.")
           
    
def main(args=None):
    rclpy.init(args=args)
    whisper_node = WhisperNode()
    
    rclpy.spin(whisper_node)
    
    whisper_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
