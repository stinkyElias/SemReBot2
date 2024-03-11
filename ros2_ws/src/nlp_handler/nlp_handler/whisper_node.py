import rclpy
import torch
import pyaudio
import tty
import termios
import sys
import threading
import select
import os
import numpy as np

from rclpy.node import Node
from std_msgs.msg import String
from transformers import pipeline
from transformers.utils import is_flash_attn_2_available

# os.environ['HF_HOME'] = '/home/stinky/ros2_ws/src/nlp_handler/models'

class WhisperNode(Node):
    # STT model parameters
    model_name_='openai/whisper-large-v3'
    task_='automatic-speech-recognition'
    torch_dtype_=torch.float16
    device_='cuda:0'
    model_kwargs_={'attn_implementation': 'flash_attention_2'} if is_flash_attn_2_available() else {'attn_implementation': 'sdpa'}
    
    #PyAudio parameters
    format_ = pyaudio.paInt16
    channels_ = 1               # mono
    rate_ = 16000                # Hz. 16000 is the sample rate of Whisper
    chunk_ = 512                 # frames per buffer
    # recording_duration_ = 10     # seconds
    
    # recording paramters
    is_recoding_ = False
    
    def __init__(self) -> None:
        super().__init__('whisper_node')
        
        self.publisher_ = self.create_publisher(String, 'whisper_output', 10)
        
        # load whisper model
        try:
            asr_pipeline_ = pipeline(
                self.task_,
                model=self.model_name_,
                torch_dtype=self.torch_dtype_,
                device=self.device_,
                model_kwargs=self.model_kwargs_,
            )
            
            self.get_logger().info("Loaded model %s" % self.model_name_)
        except:
            self.get_logger().error("Failed to load model %s" % self.model_name_)
            raise Exception("Failed to load model %s" % self.model_name_)
        
        # initialize PyAudio
        try:
            audio_ = pyaudio.PyAudio()
            stream_ = audio_.open(format=self.format_, channels=self.channels_, rate=self.rate_, input=True, frames_per_buffer=self.chunk_)
            frames_ = []
            
            self.get_logger().info("Initialized PyAudio")
        except:
            self.get_logger().error("Failed to initialize PyAudio")
            raise Exception("Failed to initialize PyAudio")
    
    def record_audio(self):
        self.get_logger().info("Recording audio...")
        
        self.is_recoding_ = True
        while self.is_recoding_:
            data = self.stream_.read(self.chunk_)
            self.frames_.append(data)
    
    def stop_recording(self):
        self.is_recording_ = False
        
        # self.stream_.stop_stream()
        # self.stream_.close()
        # self.audio_.terminate()
            

   

def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    
    return key

def get_keyboard_input():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
    
def main(args=None):
    rclpy.init(args=args)
    whisper_node = WhisperNode()
    
    spinner_thread = threading.Thread(target=rclpy.spin, args=(whisper_node,), daemon=True)
    spinner_thread.start()
    
    whisper_node.get_logger().info("Press 't' followed by 'Enter' to start recording audio.")
    while True:
        if get_keyboard_input():
            pressed_key = sys.stdin.readline().strip()
            if pressed_key == 't':
                whisper_node.record_audio()
            else:
                break
    
    rclpy.shutdown()
    spinner_thread.join()

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