# Code Analysis

This is a **WebRTC screen sharing application** with a sender-receiver architecture using Socket.IO for signaling.

## How it works:

**Sender** (`sender.html`):

- Captures screen using `getDisplayMedia()`
- Creates an RTCPeerConnection and sends video tracks to receiver
- Emits an offer through Socket.IO when "Share" button is clicked
- Receives ICE candidates and answer from receiver

**Receiver** (`receiver.html`):

- Waits for incoming offer from sender
- Creates RTCPeerConnection to receive remote tracks
- Displays shared screen in a `<video>` element
- Sends answer and ICE candidates back to sender

**Server** (`server.js`):

- Node.js/Express with Socket.IO
- Routes signaling messages (offer/answer/ICE candidates) between sender and receiver
- Tracks which socket is sender and which is receiver
- Cleans up when either peer disconnects

## Key flow:

1. Receiver connects and signals "ready"
2. Sender clicks share → captures screen → creates offer
3. Server relays offer to receiver
4. Receiver creates answer → server relays back to sender
5. Both exchange ICE candidates for connection
6. WebRTC peer connection established → video streams

It's a simple **1-to-1 screen sharing solution** using WebRTC P2P with Socket.IO as the signaling channel.
