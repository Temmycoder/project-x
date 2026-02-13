# 🚀 X-Share - Professional NDI-like Screen Sharing

A cross-platform desktop application for broadcasting your screen over the internet using WebRTC. Works on **Windows and Mac** with support for up to **3 simultaneous receivers**.

![X-Share](https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![Electron](https://img.shields.io/badge/Electron-Latest-blue?style=flat-square)
![WebRTC](https://img.shields.io/badge/WebRTC-P2P-green?style=flat-square)

## ✨ Features

- 📡 **Screen Broadcasting** - Share your entire screen in real-time
- 👥 **Multiple Receivers** - Up to 3 devices can receive simultaneously
- 🎯 **Low Latency** - WebRTC for peer-to-peer streaming
- 💻 **Cross-Platform** - Works on Windows and macOS
- 🎨 **Modern UI** - Beautiful, intuitive interface
- 📹 **Virtual Camera** - Outputs stream as virtual camera (Windows/Mac)
- 🔧 **Easy Setup** - Single-click launcher

## 📋 Requirements

### System Requirements

- **Windows 10+** or **macOS 10.15+**
- **4GB RAM minimum**
- **Broadband internet** for online streaming

### Software Dependencies

- **Python 3.8+**
- **Node.js 16+** (for Electron development)
- **pip** (Python package manager)

## 📦 Project Structure

```
project-x/
├── backend/
│   ├── server.py              # Main Flask/Socket.IO server
│   ├── requirements.txt        # Python dependencies
│   └── streamer/
│       ├── screen_capture.py   # Screen capture module
│       ├── webrtc_handler.py   # WebRTC peer management
│       └── virtual_camera.py   # Virtual camera output
│
├── electron-app/
│   ├── main.js                # Electron main process
│   ├── preload.js             # IPC bridge
│   ├── package.json           # Electron dependencies
│   └── src/
│       ├── App.jsx            # Main React component
│       ├── index.js           # React entry point
│       └── components/
│           ├── Sender.jsx     # Sender UI
│           ├── Receiver.jsx   # Receiver UI
│           └── services/
│               └── socketService.js  # Socket.IO client
│
└── README.md                  # This file
```

## 🚀 Quick Start

### Option 1: Development Mode

#### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### 2. Install Node Dependencies

```bash
cd electron-app
npm install
```

#### 3. Start Python Server

```bash
# From project-x/backend directory
python server.py
```

Server runs on `http://localhost:5000`

#### 4. Start Electron App (New Terminal)

```bash
# From project-x/electron-app directory
npm run dev
```

This will start:

- React dev server (port 3000)
- Electron app connected to React

### Option 2: Packaged Release (Recommended)

#### Build for Windows

```bash
cd electron-app
npm run build:win
```

Creates installer in `dist/` folder

#### Build for macOS

```bash
cd electron-app
npm run build:mac
```

## 🎮 Usage Guide

### As a Sender (Broadcasting)

1. **Launch X-Share** → Select **"Broadcast Your Screen"**
2. Click **"▶️ Start Sharing"** button
3. Choose which display to share
4. Share the **Sender ID** with receivers (shown in top left)
5. Monitor **FPS** and **Receiver Count** in real-time
6. Click **"⏹️ Stop Sharing"** when done

### As a Receiver (Watching)

1. **Launch X-Share** → Select **"Receive Screen Stream"**
2. Wait for senders to become available
3. Click on a sender from the **Available Senders** list
4. Stream appears in main video area
5. Click **"🔌 Disconnect"** to stop receiving

## 🔧 Configuration

### Modify Server Port

Edit `backend/server.py`:

```python
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=YOUR_PORT, debug=False)
```

### Adjust Stream Quality

In `backend/streamer/screen_capture.py`:

```python
# Change FPS and scale
screen_capture = ScreenCapture(fps=60, scale=0.75)
```

### Change Server Address

In `electron-app/src/App.jsx`:

```javascript
const [serverUrl, setServerUrl] = useState("http://your-server-ip:5000");
```

## 🌐 Network Configuration

### Local Network Only

No setup needed - works automatically on same WiFi/LAN

### Over Internet (Port Forwarding)

1. **Router Port Forwarding**:
   - Forward port **5000** to your machine's local IP
   - Example: `192.168.1.100:5000`

2. **Firewall Rules**:
   - Allow Python and Electron through firewall
   - Windows: Add exceptions in Windows Defender

3. **Share Public Address**:
   - Get your public IP: https://whatismyipaddress.com
   - Share: `http://YOUR_PUBLIC_IP:5000`

4. **Security** (Optional):
   - Use VPN for secure connection
   - Add authentication to `server.py`

## 🐛 Troubleshooting

### "Connection Refused"

- ✅ Ensure Python server is running
- ✅ Check port 5000 is not in use: `netstat -ano | findstr :5000`
- ✅ Firewall not blocking port

### No Displays Found

- ✅ Check screen capture permissions
- **macOS**: Settings → Privacy & Security → Screen Recording → Allow X-Share

### Slow Performance

- ✅ Reduce quality: `scale=0.5` in `screen_capture.py`
- ✅ Lower FPS: `fps=15`
- ✅ Check network latency
- ✅ Close other bandwidth-heavy apps

### Virtual Camera Not Showing

- ✅ Install `pyvirtualcam` drivers
- **Windows**: May require obs-virtualcam
- **macOS**: May require manual driver installation

## 📊 Performance Tips

| Setting      | FPS | Quality | Latency | CPU      |
| ------------ | --- | ------- | ------- | -------- |
| **Ultra**    | 60  | 1080p   | 50ms    | High     |
| **High**     | 30  | 1080p   | 100ms   | Med      |
| **Balanced** | 30  | 720p    | 100ms   | Low      |
| **Low**      | 15  | 480p    | 150ms   | Very Low |

## 🔐 Security Notes

- **Local Network**: Broadcasts on LAN without encryption
- **Internet**: Recommend using VPN or firewall rules
- **Future**: Add JWT authentication to `server.py`

## 📚 Architecture

### Communication Flow

```
Sender App → Socket.IO → Python Server → WebRTC → Receiver App
                ↓
          Frame Buffer → Virtual Camera
```

### WebRTC Components

- **ICE Servers**: Google STUN for NAT traversal
- **VP8/H264**: Video codec negotiation
- **Adaptive Bitrate**: Automatic quality adjustment

## 🛠️ Development

### Add Custom Features

#### Add Authentication

Edit `backend/server.py`:

```python
@socketio.on('authenticate')
def handle_auth(data):
    token = data.get('token')
    # Verify token
    emit('auth_success')
```

#### Custom Codec Selection

Edit `backend/streamer/webrtc_handler.py`:

```python
# Force H264
pc.addTransceiver("video", {"send": RTCRtpTransceiver("H264")})
```

#### Add Recording

```python
from av import open as av_open

output = av_open('recording.mp4', 'w')
```

## 📄 License

MIT License - See LICENSE file

## 👨‍💻 Support

- 📧 Email: support@x-share.dev
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

## 🎯 Roadmap

- [ ] Recording functionality
- [ ] Multi-monitor support
- [ ] Custom bitrate control
- [ ] Mobile receiver app
- [ ] Cloud server hosting
- [ ] Browser-based receiver
- [ ] Audio streaming
- [ ] Speech-to-text overlay

## ⭐ Credits

Built with ❤️ using:

- **Python**: Flask, aiortc, Socket.IO
- **Electron**: React, Modern JavaScript
- **WebRTC**: Real-time P2P streaming

---

**Made with passion for seamless screen sharing** 🚀
