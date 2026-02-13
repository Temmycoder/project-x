"""Virtual camera output for Windows/Mac"""
import pyvirtualcam
import numpy as np
from PIL import Image
import threading
from typing import Optional
import time

class VirtualCamera:
    """Creates and manages virtual camera output"""
    
    def __init__(self, width: int = 1920, height: int = 1080, fps: int = 30):
        self.width = width
        self.height = height
        self.fps = fps
        self.camera = None
        self.is_running = False
        self.current_frame = None
        self.lock = threading.Lock()
        
    def start(self) -> bool:
        """Start virtual camera"""
        try:
            self.camera = pyvirtualcam.Camera(
                width=self.width,
                height=self.height,
                fps=self.fps,
                fmt=pyvirtualcam.PixelFormat.BGR
            )
            self.is_running = True
            print(f"Virtual camera started: {self.width}x{self.height} @ {self.fps}fps")
            return True
        except Exception as e:
            print(f"Error starting virtual camera: {e}")
            return False
    
    def send_frame(self, frame: np.ndarray):
        """Send frame to virtual camera"""
        if not self.is_running or self.camera is None:
            return
        
        try:
            # Ensure frame is correct size
            if frame.shape[:2] != (self.height, self.width):
                frame = np.array(
                    Image.fromarray(frame).resize(
                        (self.width, self.height),
                        Image.Resampling.LANCZOS
                    )
                )
            
            with self.lock:
                self.camera.send(frame)
        except Exception as e:
            print(f"Error sending frame to virtual camera: {e}")
    
    def stop(self):
        """Stop virtual camera"""
        if self.camera:
            self.is_running = False
            self.camera.close()
            print("Virtual camera stopped")
