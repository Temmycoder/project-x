"""
Configuration file for X-Share
"""

# Server Configuration
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000
SERVER_SECRET_KEY = 'ndi-screen-share-2026-secret'

# Stream Configuration
STREAM_FPS = 30
STREAM_QUALITY = 1.0  # 0.5 = 50% quality, use for slower machines
STREAM_BITRATE = 5000  # kbps, adaptive based on network

# Virtual Camera Configuration
VCAM_ENABLED = True
VCAM_WIDTH = 1920
VCAM_HEIGHT = 1080
VCAM_FPS = 30

# WebRTC Configuration
MAX_RECEIVERS_PER_SENDER = 3
ICE_SERVERS = [
    {'urls': 'stun:stun.l.google.com:19302'},
    {'urls': 'stun:stun1.l.google.com:19302'},
    {'urls': 'stun:stun2.l.google.com:19302'},
]

# Network Configuration
ENABLE_CORS = True
CORS_ORIGINS = "*"

# Logging Configuration
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = 'x-share.log'

# Development
DEBUG_MODE = False
ELECTRON_DEV = False
