/**
 * Sender Component
 * Captures and broadcasts screen
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  joinAsSender,
  startStreaming,
  stopStreaming,
  sendOffer,
  sendIceCandidate,
  onReceiverJoined,
  onStreamingStatus,
  getSocket
} from '../services/socketService';
import styles from './Sender.module.css';

export default function SenderComponent() {
  const [isStreaming, setIsStreaming] = useState(false);
  const [receivers, setReceivers] = useState(0);
  const [fps, setFps] = useState(0);
  const videoRef = useRef(null);
  const pcRef = useRef(null);

  useEffect(() => {
    joinAsSender();
    
    onReceiverJoined(() => {
      setReceivers(prev => Math.min(prev + 1, 3));
    });

    onStreamingStatus((data) => {
      setFps(data.fps);
    });

    return () => {
      if (isStreaming) {
        handleStopStreaming();
      }
    };
  }, []);

  const createPeerConnection = async () => {
    const pc = new RTCPeerConnection({
      iceServers: [
        { urls: 'stun:stun.l.google.com:19302' },
        { urls: 'stun:stun1.l.google.com:19302' }
      ]
    });

    pc.onicecandidate = (event) => {
      if (event.candidate) {
        sendIceCandidate(event.candidate);
      }
    };

    return pc;
  };

  const handleStartStreaming = async () => {
    try {
      // Get display media
      const stream = await navigator.mediaDevices.getDisplayMedia({
        video: {
          cursor: 'always',
          displaySurface: 'monitor'
        }
      });

      // Display in preview
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }

      // Create peer connection
      pcRef.current = await createPeerConnection();

      // Add track to peer
      stream.getTracks().forEach(track => {
        pcRef.current.addTrack(track, stream);
      });

      // Create and send offer
      const offer = await pcRef.current.createOffer();
      await pcRef.current.setLocalDescription(offer);
      sendOffer(offer);

      // Listen for answer
      const socket = getSocket();
      socket.once('answer', async (data) => {
        const answer = new RTCSessionDescription(data);
        await pcRef.current.setRemoteDescription(answer);
      });

      startStreaming();
      setIsStreaming(true);
    } catch (error) {
      console.error('Error starting stream:', error);
      alert('Failed to start streaming: ' + error.message);
    }
  };

  const handleStopStreaming = async () => {
    if (videoRef.current && videoRef.current.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }

    if (pcRef.current) {
      pcRef.current.close();
      pcRef.current = null;
    }

    stopStreaming();
    setIsStreaming(false);
    setReceivers(0);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>📡 X-Share Sender</h1>
        <div className={styles.stats}>
          <span>📹 FPS: {fps}</span>
          <span>👥 Receivers: {receivers}/3</span>
        </div>
      </div>

      <div className={styles.previewSection}>
        <video
          ref={videoRef}
          autoPlay
          muted
          className={styles.preview}
        />
        {!isStreaming && <div className={styles.placeholder}>
          Click "Start Sharing" to begin broadcasting
        </div>}
      </div>

      <div className={styles.controls}>
        <button
          className={`${styles.button} ${isStreaming ? styles.stop : styles.start}`}
          onClick={isStreaming ? handleStopStreaming : handleStartStreaming}
        >
          {isStreaming ? '⏹️ Stop Sharing' : '▶️ Start Sharing'}
        </button>
      </div>

      <div className={styles.info}>
        <p>💡 Share your screen with up to 3 receivers</p>
        <p>⚡ Low latency WebRTC streaming</p>
      </div>
    </div>
  );
}
