"""Main streaming server with Socket.IO signaling"""
import os
import json
import asyncio
import numpy as np
from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from aiortc import RTCSessionDescription
import logging

from streamer.screen_capture import ScreenCapture
from streamer.webrtc_handler import WebRTCHandler
from streamer.virtual_camera import VirtualCamera

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'ndi-screen-share-2026'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize components
screen_capture = ScreenCapture(fps=30)
webrtc_handler = WebRTCHandler()
virtual_camera = VirtualCamera(width=1920, height=1080, fps=30)

# Store connected clients
clients = {
    'senders': {},
    'receivers': {}
}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect(auth):
    """Handle client connection"""
    client_id = request.sid
    logger.info(f"Client connected: {client_id}")
    emit('connected', {'data': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    client_id = request.sid
    logger.info(f"Client disconnected: {client_id}")
    
    # Cleanup if sender
    if client_id in clients['senders']:
        del clients['senders'][client_id]
        socketio.emit('sender_disconnected', 
                     {'sender_id': client_id}, 
                     to='receivers')
    
    # Cleanup if receiver
    if client_id in clients['receivers']:
        del clients['receivers'][client_id]

@socketio.on('join_as_sender')
def handle_sender_join():
    """Handle sender joining"""
    client_id = request.sid
    clients['senders'][client_id] = {
        'id': client_id,
        'status': 'idle',
        'receivers': []
    }
    logger.info(f"Sender joined: {client_id}")
    emit('sender_ready', {'sender_id': client_id})

@socketio.on('join_as_receiver')
def handle_receiver_join(data):
    """Handle receiver joining"""
    client_id = request.sid
    sender_id = data.get('sender_id')
    
    # Limit to 3 receivers per sender
    if sender_id in clients['senders']:
        if len(clients['senders'][sender_id]['receivers']) >= 3:
            emit('error', {'message': 'Max 3 receivers allowed'})
            return
        
        clients['senders'][sender_id]['receivers'].append(client_id)
    
    clients['receivers'][client_id] = {
        'id': client_id,
        'sender_id': sender_id
    }
    
    logger.info(f"Receiver joined: {client_id} for sender: {sender_id}")
    socketio.emit('receiver_joined', 
                 {'receiver_id': client_id}, 
                 to=sender_id)

@socketio.on('offer')
async def handle_offer(data):
    """Handle WebRTC offer"""
    sender_id = request.sid
    offer = RTCSessionDescription(sdp=data['sdp'], type=data['type'])
    
    # Create peer connection and get answer
    answer = await webrtc_handler.handle_offer(sender_id, offer)
    
    emit('answer', {
        'sdp': answer.sdp,
        'type': answer.type
    }, to=sender_id)

@socketio.on('ice_candidate')
async def handle_ice(data):
    """Handle ICE candidate"""
    client_id = request.sid
    candidate = data.get('candidate')
    
    await webrtc_handler.add_ice_candidate(client_id, candidate)

@socketio.on('start_streaming')
def handle_start_streaming():
    """Start capturing and streaming"""
    sender_id = request.sid
    screen_capture.start_capture(monitor_id=1)
    virtual_camera.start()
    
    clients['senders'][sender_id]['status'] = 'streaming'
    logger.info(f"Sender {sender_id} started streaming")
    
    emit('streaming_started')

@socketio.on('stop_streaming')
def handle_stop_streaming():
    """Stop streaming"""
    sender_id = request.sid
    screen_capture.stop_capture()
    virtual_camera.stop()
    
    if sender_id in clients['senders']:
        clients['senders'][sender_id]['status'] = 'idle'
    
    logger.info(f"Sender {sender_id} stopped streaming")
    emit('streaming_stopped')

def frame_capture_loop():
    """Background loop to capture and distribute frames"""
    while True:
        frame = screen_capture.get_current_frame()
        
        if frame is not None:
            # Send to virtual camera
            virtual_camera.send_frame(frame)
            
            # Send to WebRTC peers
            webrtc_handler.add_frame(frame)
            
            # Emit frame count for monitoring
            socketio.emit('stream_status', {
                'fps': screen_capture.fps,
                'peers': webrtc_handler.get_peer_count(),
                'frame_received': True
            }, to='senders')
        
        asyncio.sleep(1 / 30)  # 30fps

if __name__ == '__main__':
    # Start frame capture loop
    import threading
    threading.Thread(target=frame_capture_loop, daemon=True).start()
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
