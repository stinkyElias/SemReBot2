import os
os.environ['HF_HOME'] = '/home/stinky/ros2_ws/src/nlp_handler/models'

import rclpy
import torch
import pyaudio
import tty
import termios
import sys
import threading
import select
import time
import numpy as np

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
            asr_pipeline_ = pipeline(
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

    def get_command_callback(self, msg: Int8) -> None:
        if msg.data == 1:
            audio_data = '/home/stinky/ros2_ws/src/nlp_handler/audio_files/1.wav'
        elif msg.data == 2:
            audio_data = '/home/stinky/ros2_ws/src/nlp_handler/audio_files/2.wav'
        elif msg.data == 3:
            audio_data = '/home/stinky/ros2_ws/src/nlp_handler/audio_files/3.wav'
        elif msg.data == 4:
            audio_data = '/home/stinky/ros2_ws/src/nlp_handler/audio_files/4.wav'
        else:
            self.get_logger().error("No such audio file.")
        
        # Transcribe audio
        output = self.asr_pipeline_(
            audio_data,
            chunk_length_s=30,
            batch_size=24,
            return_timestamps=True,
        )

        self.publisher_.publish(output['text'])
        self.get_logger().info("Publishing transcribed audio.")

        '''
        # initialize PyAudio
        try:
            audio_ = pyaudio.PyAudio()
            stream_ = audio_.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=512)
            frames_ = []
            
            self.get_logger().info("Initialized PyAudio")
        except:
            self.get_logger().error("Failed to initialize PyAudio")
            raise Exception("Failed to initialize PyAudio")
        
        print("Recording audio...")
        start_time = time.time()

        try:
            while time.time() - start_time < 5:
                data = stream_.read(512)
                frames_.append(data)

        except KeyboardInterrupt:
            pass

        stream_.stop_stream()
        stream_.close()
        audio_.terminate()
        print("Finished recording audio.")

        audio_data = np.frombuffer(b''.join(frames_), dtype=np.int16)
        '''

        
            
    
def main(args=None):
    rclpy.init(args=args)
    whisper_node = WhisperNode()
    
    rclpy.spin(whisper_node)
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()

'''
if __name__ == '__main__':
    old_settings = termios.tcgetattr(sys.stdin)
    
    if sys.platform != 'win32':
        try:
            tty.setcbreak(sys.stdin.fileno())
            main()
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    else:
        raise Exception("Node 'whisper_node' cannot be run on Windows. Please run on a Unix-based system.")
'''