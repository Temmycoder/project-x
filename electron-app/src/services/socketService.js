/**
 * Socket.IO Service
 * Handles all socket communication
 */

import io from 'socket.io-client';

let socket = null;

export const initSocket = (serverUrl) => {
  socket = io(serverUrl, {
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    reconnectionAttempts: 10,
    transports: ['websocket', 'polling']
  });

  socket.on('connect', () => {
    console.log('Connected to server');
  });

  socket.on('disconnect', () => {
    console.log('Disconnected from server');
  });

  socket.on('error', (error) => {
    console.error('Socket error:', error);
  });

  return socket;
};

export const getSocket = () => {
  return socket;
};

export const joinAsSender = () => {
  if (socket) {
    socket.emit('join_as_sender');
  }
};

export const joinAsReceiver = (senderId) => {
  if (socket) {
    socket.emit('join_as_receiver', { sender_id: senderId });
  }
};

export const startStreaming = () => {
  if (socket) {
    socket.emit('start_streaming');
  }
};

export const stopStreaming = () => {
  if (socket) {
    socket.emit('stop_streaming');
  }
};

export const sendOffer = (offer) => {
  if (socket) {
    socket.emit('offer', {
      type: offer.type,
      sdp: offer.sdp
    });
  }
};

export const sendIceCandidate = (candidate) => {
  if (socket) {
    socket.emit('ice_candidate', {
      candidate: candidate
    });
  }
};

export const onAnswer = (callback) => {
  if (socket) {
    socket.on('answer', callback);
  }
};

export const onIceCandidate = (callback) => {
  if (socket) {
    socket.on('ice_candidate', callback);
  }
};

export const onStreamingStatus = (callback) => {
  if (socket) {
    socket.on('stream_status', callback);
  }
};

export const onReceiverJoined = (callback) => {
  if (socket) {
    socket.on('receiver_joined', callback);
  }
};

export const onSenderDisconnected = (callback) => {
  if (socket) {
    socket.on('sender_disconnected', callback);
  }
};
