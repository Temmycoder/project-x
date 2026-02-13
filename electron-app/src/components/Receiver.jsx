/**
 * Receiver Component
 * Displays broadcasted screen
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  joinAsReceiver,
  getSocket,
  sendIceCandidate,
  onSenderDisconnected
} from '../services/socketService';
import styles from './Receiver.module.css';

export default function ReceiverComponent() {
  const [senderList, setSenderList] = useState([]);
  const [selectedSenderId, setSelectedSenderId] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const videoRef = useRef(null);
  const pcRef = useRef(null);

  useEffect(() => {
    const socket = getSocket();
    
    // Listen for available senders
    socket.on('sender_ready', (data) => {
      setSenderList(prev => {
        if (!prev.find(s => s.id === data.sender_id)) {
          return [...prev, { id: data.sender_id, status: 'available' }];
        }
        return prev;
      });
    });

    onSenderDisconnected((data) => {
      setSenderList(prev => prev.filter(s => s.id !== data.sender_id));
      if (selectedSenderId === data.sender_id) {
        handleDisconnect();
      }
    });

    return () => {
      if (isConnected) {
        handleDisconnect();
      }
    };
  }, [selectedSenderId, isConnected]);

  const createPeerConnection = async () => {
    const pc = new RTCPeerConnection({
      iceServers: [
        { urls: 'stun:stun.l.google.com:19302' },
        { urls: 'stun:stun1.l.google.com:19302' }
      ]
    });

    pc.ontrack = (event) => {
      console.log('Received track:', event.track);
      if (videoRef.current) {
        videoRef.current.srcObject = event.streams[0];
      }
    };

    pc.onicecandidate = (event) => {
      if (event.candidate) {
        sendIceCandidate(event.candidate);
      }
    };

    pc.onconnectionstatechange = () => {
      console.log('Connection state:', pc.connectionState);
      if (pc.connectionState === 'disconnected' || pc.connectionState === 'failed') {
        handleDisconnect();
      }
    };

    return pc;
  };

  const handleConnectToSender = async (senderId) => {
    try {
      setSelectedSenderId(senderId);
      
      // Create peer connection
      pcRef.current = await createPeerConnection();

      // Join as receiver
      joinAsReceiver(senderId);

      // Listen for offer from sender
      const socket = getSocket();
      socket.once('offer', async (data) => {
        const offer = new RTCSessionDescription(data);
        await pcRef.current.setRemoteDescription(offer);

        const answer = await pcRef.current.createAnswer();
        await pcRef.current.setLocalDescription(answer);

        // Send answer back (will be handled by socket on sender side)
        socket.emit('answer', {
          type: answer.type,
          sdp: answer.sdp
        }, senderId);
      });

      // Listen for ICE candidates
      socket.on('ice_candidate', async (data) => {
        if (data.candidate) {
          try {
            await pcRef.current.addIceCandidate(data.candidate);
          } catch (err) {
            console.error('Error adding ICE candidate:', err);
          }
        }
      });

      setIsConnected(true);
    } catch (error) {
      console.error('Error connecting to sender:', error);
      alert('Failed to connect: ' + error.message);
    }
  };

  const handleDisconnect = () => {
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    if (pcRef.current) {
      pcRef.current.close();
      pcRef.current = null;
    }

    setIsConnected(false);
    setSelectedSenderId(null);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>📺 X-Share Receiver</h1>
        <span className={`${styles.status} ${isConnected ? styles.connected : ''}`}>
          {isConnected ? '🟢 Connected' : '⚫ Waiting...'}
        </span>
      </div>

      <div className={styles.mainContent}>
        <div className={styles.videoSection}>
          <video
            ref={videoRef}
            autoPlay
            className={styles.video}
          />
          {!isConnected && (
            <div className={styles.videoPlaceholder}>
              Select a sender to receive stream
            </div>
          )}
        </div>

        <div className={styles.senderList}>
          <h3>Available Senders</h3>
          {senderList.length === 0 ? (
            <p className={styles.noSenders}>No senders available</p>
          ) : (
            <div className={styles.senderItems}>
              {senderList.map((sender) => (
                <button
                  key={sender.id}
                  className={`${styles.senderItem} ${
                    selectedSenderId === sender.id ? styles.active : ''
                  }`}
                  onClick={() => handleConnectToSender(sender.id)}
                  disabled={isConnected && selectedSenderId !== sender.id}
                >
                  <span className={styles.senderInfo}>
                    <span className={styles.senderName}>Sender</span>
                    <span className={styles.senderId}>{sender.id.substring(0, 8)}</span>
                  </span>
                  {selectedSenderId === sender.id && (
                    <span className={styles.badge}>📡</span>
                  )}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {isConnected && (
        <button className={styles.disconnectBtn} onClick={handleDisconnect}>
          🔌 Disconnect
        </button>
      )}
    </div>
  );
}
