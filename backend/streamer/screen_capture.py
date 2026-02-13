"""Screen capture module for cross-platform support"""
import mss
import numpy as np
from PIL import Image
import asyncio
import threading
from typing import Optional

class ScreenCapture:
    """Captures screen frames at specified intervals"""
    
    def __init__(self, fps: int = 30, scale: float = 1.0):
        self.fps = fps
        self.scale = scale
        self.frame_interval = 1.0 / fps
        self.current_frame = None
        self.is_capturing = False
        self.lock = threading.Lock()
        self.sct = mss.mss()
        
    def get_monitor_info(self):
        """Get available monitors"""
        monitors = self.sct.monitors
        return [
            {
                'id': i, 
                'width': m['width'], 
                'height': m['height'],
                'left': m['left'],
                'top': m['top']
            } 
            for i, m in enumerate(monitors[1:], 1)
        ]
    
    def capture_frame(self, monitor_id: int = 1) -> Optional[np.ndarray]:
        """Capture a single frame"""
        try:
            monitor = self.sct.monitors[monitor_id]
            screenshot = self.sct.grab(monitor)
            
            # Convert to numpy array
            frame = np.array(screenshot)
            
            # Apply scaling if needed
            if self.scale != 1.0:
                height, width = frame.shape[:2]
                new_width = int(width * self.scale)
                new_height = int(height * self.scale)
                frame = np.array(Image.fromarray(frame).resize(
                    (new_width, new_height), Image.Resampling.LANCZOS
                ))
            
            return frame
        except Exception as e:
            print(f"Error capturing frame: {e}")
            return None
    
    def start_capture(self, monitor_id: int = 1):
        """Start continuous capture loop"""
        self.is_capturing = True
        threading.Thread(
            target=self._capture_loop, 
            args=(monitor_id,),
            daemon=True
        ).start()
    
    def _capture_loop(self, monitor_id: int):
        """Background capture loop"""
        while self.is_capturing:
            frame = self.capture_frame(monitor_id)
            if frame is not None:
                with self.lock:
                    self.current_frame = frame
            
            asyncio.sleep(self.frame_interval)
    
    def get_current_frame(self) -> Optional[np.ndarray]:
        """Get the current captured frame"""
        with self.lock:
            return self.current_frame.copy() if self.current_frame is not None else None
    
    def stop_capture(self):
        """Stop the capture loop"""
        self.is_capturing = False
