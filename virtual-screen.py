import cv2
import numpy as np
from flask import Flask, Response
import threading
import pyvirtualcam
from PIL import Image, ImageDraw
import time

app = Flask(__name__)

# Create a virtual screen (blank initially)
screen_width = 1920
screen_height = 1080
current_frame = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

def generate_frames():
    """Generate video frames for HTTP streaming"""
    while True:
        # Convert frame to JPEG
        ret, buffer = cv2.imencode('.jpg', current_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return """
    <html>
        <head>
            <title>Virtual Screen</title>
            <style>
                body { margin: 0; background: #000; }
                img { width: 100%; height: 100vh; object-fit: contain; }
            </style>
        </head>
        <body>
            <img src="/video_feed">
        </body>
    </html>
    """

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def run_virtual_camera():
    """Create virtual camera for projection"""
    with pyvirtualcam.Camera(width=screen_width, height=screen_height, fps=30) as cam:
        print(f"Virtual camera created: {cam.device}")
        while True:
            # Send current frame to virtual camera
            cam.send(current_frame)
            cam.sleep_until_next_frame()

if __name__ == '__main__':
    # Start virtual camera in background thread
    cam_thread = threading.Thread(target=run_virtual_camera, daemon=True)
    cam_thread.start()
    
    # Start HTTP server
    print(f"Virtual screen running!")
    print(f"1. Project to this PC using Windows+P")
    print(f"2. View stream at: http://[YOUR-IP]:5000")
    print(f"3. Virtual camera available for apps like Zoom/Teams")
    
    app.run(host='0.0.0.0', port=5000, threaded=True)