"""WebRTC handler for peer connections and streaming"""
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaStreamTrack
import av
import numpy as np
from typing import Dict, Optional
import asyncio
from collections import deque

class FrameSource(MediaStreamTrack):
    """Custom media track that provides frames"""
    kind = "video"
    
    def __init__(self, frame_buffer: deque, fps: int = 30):
        super().__init__()
        self.frame_buffer = frame_buffer
        self.fps = fps
        self.pts = 0
        self.time_base = av.open_codec_context(
            {"video": "libx264"}, format="rawvideo", mode="w"
        ).streams.video[0].time_base if False else av.time.TimeBase(1, fps)
        
    async def recv(self):
        """Get next frame from buffer"""
        frame = None
        if self.frame_buffer:
            frame = self.frame_buffer.popleft()
        
        if frame is None:
            # Return blank frame if no data
            frame = np.zeros((720, 1280, 3), dtype=np.uint8)
        
        # Convert numpy array to av.VideoFrame
        img_frame = av.VideoFrame.from_ndarray(frame, format="bgr24")
        img_frame.pts = self.pts
        img_frame.time_base = self.time_base
        self.pts += 1
        
        await asyncio.sleep(1 / self.fps)
        return img_frame

class WebRTCHandler:
    """Manages WebRTC peer connections"""
    
    def __init__(self):
        self.peers: Dict[str, RTCPeerConnection] = {}
        self.frame_buffer = deque(maxlen=10)
        
    async def create_peer(self, peer_id: str) -> RTCPeerConnection:
        """Create a new peer connection"""
        pc = RTCPeerConnection()
        self.peers[peer_id] = pc
        
        # Add video track
        video_track = FrameSource(self.frame_buffer)
        pc.addTrack(video_track)
        
        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            print(f"Connection state change: {pc.connectionState}")
            if pc.connectionState == "failed":
                await self.close_peer(peer_id)
        
        return pc
    
    async def handle_offer(self, peer_id: str, offer: RTCSessionDescription) -> RTCSessionDescription:
        """Handle WebRTC offer from peer"""
        if peer_id not in self.peers:
            pc = await self.create_peer(peer_id)
        else:
            pc = self.peers[peer_id]
        
        await pc.setRemoteDescription(offer)
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        
        return answer
    
    async def add_ice_candidate(self, peer_id: str, candidate):
        """Add ICE candidate"""
        if peer_id in self.peers:
            await self.peers[peer_id].addIceCandidate(candidate)
    
    async def close_peer(self, peer_id: str):
        """Close a peer connection"""
        if peer_id in self.peers:
            await self.peers[peer_id].close()
            del self.peers[peer_id]
    
    def add_frame(self, frame: np.ndarray):
        """Add frame to buffer for streaming"""
        try:
            self.frame_buffer.append(frame)
        except:
            pass
    
    async def close_all(self):
        """Close all peer connections"""
        for peer_id in list(self.peers.keys()):
            await self.close_peer(peer_id)
    
    def get_peer_count(self) -> int:
        """Get number of connected peers"""
        return len(self.peers)
