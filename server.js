const express = require("express");
const app = express();
const http = require("http").createServer(app);
const io = require("socket.io")(http);

app.use(express.static("public"));

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

  socket.on("disconnect", () => {
    if (socket === sender) sender = null;
    if (socket === receiver) receiver = null;
  });
});

http.listen(3000, () => console.log("Server running on port 3000"));