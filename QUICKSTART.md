# 🚀 X-Share Quick Start Guide

## ⚡ 30 Second Setup

### Windows

```bash
# 1. Run setup script
setup.bat

# 2. Terminal 1: Start Python server
cd backend
python server.py

# 3. Terminal 2: Start Electron app
cd electron-app
npm run dev
```

### macOS/Linux

```bash
# 1. Run setup script
chmod +x setup.sh
./setup.sh

# 2. Terminal 1: Start Python server
cd backend
python3 server.py

# 3. Terminal 2: Start Electron app
cd electron-app
npm run dev
```

## 🎮 First Time Use

### Sending Your Screen (Machine A)

1. Launch X-Share → Click **"Broadcast Your Screen"**
2. Click **"▶️ Start Sharing"**
3. Choose display to share
4. Copy your **Sender ID** (shown at top)

### Receiving Stream (Machine B)

1. Launch X-Share → Click **"Receive Screen Stream"**
2. Wait for sender to appear in list
3. Enter sender ID or click from list
4. Click sender name to connect
5. Stream displays in main area

## 📊 Connection Status

| Status    | Meaning                 |
| --------- | ----------------------- |
| 🟢 Green  | Connected and streaming |
| 🟡 Yellow | Connecting...           |
| 🔴 Red    | Disconnected            |

## 🌍 Network Modes

### Same WiFi (Easiest)

- Automatic discovery
- No configuration needed
- Works out of the box

### Over Internet

1. Forward port 5000 on router
2. Get public IP: https://whatismyipaddress.com
3. Share: `http://YOUR_IP:5000`

### Behind VPN

- Use VPN app on both machines
- Share sender ID through VPN connection
- Works transparently

## 🛠️ Common Issues Quick Fix

### "Can't Connect"

```
Check: Is Python server running?
python server.py
```

### Screen Won't Share

```
macOS: Settings → Security & Privacy → Screen Recording → Allow X-Share
Windows: Check Windows Defender Firewall
```

### Slow Performance

```
Edit: backend/streamer/screen_capture.py
Change: ScreenCapture(fps=15, scale=0.5)
```

### No Receivers Show Up

```
Check: Both machines on same network
Check: Firewall allows port 5000
Check: Server running on correct IP
```

## 📱 Advanced Usage

### Multi-Monitor Sharing

```python
# Edit backend/server.py
monitor_id = 2  # Change monitor
screen_capture.start_capture(monitor_id=monitor_id)
```

### Adjust Stream Quality

```python
# backend/streamer/screen_capture.py
# Ultra Quality (uses more bandwidth)
screen_capture = ScreenCapture(fps=60, scale=1.0)

# Balanced
screen_capture = ScreenCapture(fps=30, scale=1.0)

# Low Bandwidth
screen_capture = ScreenCapture(fps=15, scale=0.5)
```

### Custom Server Port

```python
# backend/server.py
socketio.run(app, port=8000)  # Change from 5000

# electron-app/src/App.jsx
setServerUrl('http://localhost:8000')
```

## 💾 Files That Matter

| Path                       | Purpose                  |
| -------------------------- | ------------------------ |
| `backend/server.py`        | Main streaming server    |
| `backend/streamer/`        | Stream encoding/decoding |
| `electron-app/src/App.jsx` | Main UI                  |
| `electron-app/main.js`     | Electron launcher        |

## 🔐 Security Checklist

- [ ] Running on trusted network
- [ ] Firewall configured
- [ ] Strong WiFi password
- [ ] VPN enabled for internet streaming
- [ ] No sensitive data in background

## 📞 Need Help?

### Check Logs

```bash
# Python server logs
tail -f backend/x-share.log

# Electron logs
tail -f ~/.config/X-Share/logs
```

### Debug Mode

```python
# In backend/server.py
DEBUG_MODE = True
LOG_LEVEL = 'DEBUG'
```

### Test Connection

```bash
# Check server is running
curl http://localhost:5000

# Check port is open
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # macOS/Linux
```

---

**Ready to share? Click "▶️ Start Sharing" now!** 🎬
