import os
os.environ['HF_HOME'] = '/home/stinky/models'
# result_dir = '/home/stinky/ros2_ws/results'

import rclpy
import torch
import gc

from rclpy.lifecycle import LifecycleNode, LifecycleState, TransitionCallbackReturn
from std_msgs.msg import String, Int8
from transformers import pipeline
from transformers.utils import is_flash_attn_2_available

class WhisperNode(LifecycleNode):   
    def __init__(self, node_name) -> None:
        super().__init__(node_name)

        self.node_name = node_name
        self.publisher_ = None
        self.subscriber_ = None

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

        self.get_logger().info("Current state unconfigured [1]")
        
    def on_configure(self, state: LifecycleState) -> TransitionCallbackReturn:
        self.model_name_ = self.get_parameter('model_name').get_parameter_value().string_value
        self.audio_dir_ = self.get_parameter('audio_dir').get_parameter_value().string_value
        dtype = self.get_parameter('data_type').get_parameter_value().string_value
        
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
            
            self.get_logger().info(f"Loaded model {self.model_name_} to device {device_}")
            # self.get_logger().info("Current state inactive [2]")
            return TransitionCallbackReturn.SUCCESS

        except Exception as e:
            self.get_logger().error(f"Failed to load model {self.model_name_} to device {device_}: {e}")
            return TransitionCallbackReturn.ERROR
        
    def on_cleanup(self, state: LifecycleState) -> TransitionCallbackReturn:      
        try:
            del self.asr_pipeline_
            gc.collect()
            torch.cuda.empty_cache()

            # self.get_logger().info("Current state unconfigured [1]")
            return TransitionCallbackReturn.SUCCESS
        
        except Exception as e:
            self.get_logger().error(f"Failed to cleanup model {self.model_name_}: {e}")
            return TransitionCallbackReturn.ERROR
    
    def on_activate(self, state: LifecycleState) -> TransitionCallbackReturn:
        self.publisher_ = self.create_lifecycle_publisher(String,
                                                          'command',
                                                          10)
        self.subscriber_ = self.create_subscription(Int8,
                                                    'speech',
                                                    self.get_command_callback,
                                                    10)

        # self.get_logger().info("Current state active [3]")
        return super().on_activate(state)
    
    def on_deactivate(self, state: LifecycleState) -> TransitionCallbackReturn:       
        self.destroy_lifecycle_publisher(self.publisher_)
        self.destroy_subscription(self.subscriber_)

        # self.get_logger().info("Current state inactive [2]")
        return super().on_deactivate(state)
    
    def on_shutdown(self, state: LifecycleState) -> TransitionCallbackReturn:
        try:
            del self.asr_pipeline_
            gc.collect()
            torch.cuda.empty_cache()

            self.destroy_lifecycle_publisher(self.publisher_)
            self.destroy_subscription(self.subscriber_)

            # self.get_logger().info("Current state finalized [4]")
            return TransitionCallbackReturn.SUCCESS
        
        except Exception as e:
            self.get_logger().error(f"Failed to cleanup model {self.model_name_}: {e}")
            return TransitionCallbackReturn.ERROR
        
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
        self.get_logger().info("Transcription complete")

        msg = String()
        msg.data = output['text']

        # # write to file
        # with open(os.path.join(result_dir, 'results.txt'), 'a') as f:
        #     f.write('\n====================================================================\n')
        #     f.write(f'Transcription {str(incoming_msg.data)}:\n' + output['text'] + '\n')

        self.publisher_.publish(msg)

        torch.cuda.empty_cache()
           
    
def main(args=None):
    torch.cuda.empty_cache()

    rclpy.init(args=args)
    whisper_node = WhisperNode('whisper')


    
    rclpy.spin(whisper_node)
    
    whisper_node.destroy_node()
    rclpy.shutdown()

    torch.cuda.empty_cache()

if __name__ == '__main__':
    main()
