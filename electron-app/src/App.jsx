/**
 * Main App Component
 * Mode selection and routing
 */

import React, { useState, useEffect } from 'react';
import SenderComponent from './components/Sender';
import ReceiverComponent from './components/Receiver';
import { initSocket } from './services/socketService';
import styles from './App.module.css';

function App() {
  const [mode, setMode] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [serverUrl, setServerUrl] = useState('http://localhost:5000');

  useEffect(() => {
    // Initialize Socket.IO connection
    const socket = initSocket(serverUrl);
    
    socket.on('connect', () => {
      setIsConnected(true);
      console.log('Connected to broadcast server');
    });

    socket.on('disconnect', () => {
      setIsConnected(false);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  if (!isConnected) {
    return (
      <div className={styles.loadingScreen}>
        <div className={styles.loadingContent}>
          <h1>🔗 X-Share</h1>
          <p className={styles.connecting}>Connecting to server...</p>
          <div className={styles.spinner}></div>
          <p className={styles.hint}>Make sure Python server is running on {serverUrl}</p>
        </div>
      </div>
    );
  }

  if (!mode) {
    return (
      <div className={styles.modeSelectScreen}>
        <div className={styles.modeContent}>
          <h1>🚀 X-Share</h1>
          <p className={styles.subtitle}>Professional NDI-like Screen Sharing</p>
          
          <div className={styles.modeButtons}>
            <button
              className={`${styles.modeButton} ${styles.sender}`}
              onClick={() => setMode('sender')}
            >
              <div className={styles.icon}>📡</div>
              <h2>Broadcast Your Screen</h2>
              <p>Share your screen with up to 3 receivers</p>
            </button>

            <button
              className={`${styles.modeButton} ${styles.receiver}`}
              onClick={() => setMode('receiver')}
            >
              <div className={styles.icon}>📺</div>
              <h2>Receive Screen Stream</h2>
              <p>View shared screens from other users</p>
            </button>
          </div>

          <p className={styles.version}>X-Share v1.0.0</p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.appContainer}>
      <div className={styles.appHeader}>
        <button
          className={styles.backButton}
          onClick={() => setMode(null)}
          title="Back to mode selection"
        >
          ← Change Mode
        </button>
        <span className={`${styles.serverStatus} ${isConnected ? styles.online : styles.offline}`}>
          {isConnected ? '🟢' : '🔴'} {isConnected ? 'Online' : 'Offline'}
        </span>
      </div>

      <div className={styles.appContent}>
        {mode === 'sender' && <SenderComponent />}
        {mode === 'receiver' && <ReceiverComponent />}
      </div>
    </div>
  );
}

export default App;
