const express = require("express");
const app = express();
const http = require("http").createServer(app);
const io = require("socket.io")(http);
const fs = require("fs");
const path = require("path");

app.use(express.static("public"));

// Ensure frames folder exists for debug/output
const framesDir = path.join(__dirname, "public", "frames");
fs.mkdirSync(framesDir, { recursive: true });

let sender = null;
let receiver = null;

io.on("connection", socket => {

  socket.on("join", role => {
    if (role === "sender") sender = socket;
    if (role === "receiver") {
      receiver = socket;
      sender?.emit("receiver-ready");
    }
  });

  socket.on("offer", offer => receiver?.emit("offer", offer));
  socket.on("answer", answer => sender?.emit("answer", answer));

  socket.on("ice", candidate => {
    if (socket === sender) receiver?.emit("ice", candidate);
    else sender?.emit("ice", candidate);
  });

  // Receive periodic frames (JPEG blobs) from the receiver and save the latest one
  // Throttle writes to disk to avoid IO overload
  let lastFrameTime = 0;
  const FRAME_INTERVAL_MS = 100; // ~10 FPS

  socket.on("frame", data => {
    const now = Date.now();
    if (now - lastFrameTime < FRAME_INTERVAL_MS) return;
    lastFrameTime = now;
    const filePath = path.join(framesDir, "latest.jpg");
    fs.writeFile(filePath, data, err => { if (err) console.error("Error writing frame", err); });
  });

  socket.on("disconnect", () => {
    if (socket === sender) sender = null;
    if (socket === receiver) receiver = null;
  });
});

http.listen(3000, () => console.log("Server running on port 3000"));