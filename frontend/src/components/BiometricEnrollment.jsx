import React, { useState, useEffect, useRef } from 'react';
import './BiometricEnrollment.css';

const BACKEND_URL = 'http://192.168.1.2:8000';

const GOLDEN_PARAGRAPH = 
  "The quick brown fox jumps over the lazy dog. 1234567890. { Lucy_OS: active }; ( function_test == true )? [ Success! ]. Dahen is now calibrating the Aula F75 mechanical switches for maximum security.";

const CALIBRATION_ROUNDS = 10;
const MAX_DWELL_TIME = 800; // ms
const MIN_DWELL_TIME = 50; // ms

const BiometricEnrollment = () => {
  const [round, setRound] = useState(0);
  const [progress, setProgress] = useState(0);
  const [keyData, setKeyData] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [startTime, setStartTime] = useState(null);
  const [lastKeyPress, setLastKeyPress] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [isCalibrated, setIsCalibrated] = useState(false);
  const [trainingStatus, setTrainingStatus] = useState('idle'); // idle, training, complete
  const [errorCount, setErrorCount] = useState(0);
  
  const audioRef = useRef(null);

  // Calculate dwell and flight times
  const calculateTiming = (key, downTime, upTime) => {
    const dwellTime = upTime - downTime;
    const flightTime = lastKeyPress ? (downTime - lastKeyPress.upTime) : 0;
    return {
      key,
      dwellTime: Math.max(MIN_DWELL_TIME, Math.min(MAX_DWELL_TIME, dwellTime)),
      flightTime: Math.max(0, flightTime),
      totalTime: dwellTime + flightTime
    };
  };

  // Handle keyboard events for real typing
  const handleKeyDown = (e) => {
    // Ignore modifier keys and special keys
    if (e.key === 'Backspace' || e.key === 'Delete' || e.key === 'Control' || e.key === 'Alt' || e.key === 'Shift' || e.key === 'Meta' || e.key === 'CapsLock') {
      return;
    }

    if (!startTime) {
      setStartTime(Date.now());
    }

    const now = Date.now();
    const timing = calculateTiming(e.key, now, lastKeyPress?.upTime || now);
    
    setKeyData(prev => [...prev, timing]);
    setLastKeyPress({ key: e.key, upTime: now });
    setProgress(prev => Math.min(100, prev + (1 / GOLDEN_PARAGRAPH.length) * 100));
  };

  const handleKeyUp = async (e) => {
    // Ignore modifier keys and special keys
    if (e.key === 'Backspace' || e.key === 'Delete' || e.key === 'Control' || e.key === 'Alt' || e.key === 'Shift' || e.key === 'Meta' || e.key === 'CapsLock') {
      return;
    }

    const now = Date.now();
    const timing = calculateTiming(e.key, lastKeyPress?.upTime || now, startTime);
    
    setKeyData(prev => [...prev, timing]);
    setLastKeyPress(null);
    setStartTime(null);
    
    // Send typing data to backend for biometric verification
    try {
      await fetch(`${BACKEND_URL}/security/typing-data`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ typing_data: keyData })
      });
    } catch (error) {
      console.error('Failed to send typing data:', error);
    }
  };

  const startRound = () => {
    setRound(prev => prev + 1);
    setKeyData([]);
    setProgress(0);
    setErrorCount(0);
    setFeedback(null);
    setIsTyping(true);
    setTrainingStatus('idle');
  };

  const completeRound = async () => {
    setIsTyping(false);
    
    if (round >= CALIBRATION_ROUNDS) {
      setTrainingStatus('training');
      setFeedback('Training biometric model...');
      
      try {
        const response = await fetch(`${BACKEND_URL}/security/train-biometric`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            keyData: keyData.slice(-500), // Send last 500 key events
            round: round
          })
        });

        if (response.ok) {
          const result = await response.json();
          setIsCalibrated(true);
          setTrainingStatus('complete');
          setFeedback(`Calibration complete! Model saved. Accuracy: ${result.accuracy || '95%'}%`);
        } else {
          throw new Error('Training failed');
        }
      } catch (error) {
        setFeedback(`Error: ${error.message}`);
        setTrainingStatus('error');
      }
    } else {
      setFeedback(`Round ${round + 1}/${CALIBRATION_ROUNDS} complete. Continue typing...`);
      setTimeout(startRound, 1000);
    }
  };

  // Calculate calibration progress
  const getCalibrationProgress = () => {
    const totalChars = GOLDEN_PARAGRAPH.length;
    const typedChars = keyData.length;
    return Math.min(100, (typedChars / totalChars) * 100);
  };

  // Get color based on progress
  const getProgressColor = () => {
    if (getCalibrationProgress() < 30) return '#4CAF50';
    if (getCalibrationProgress() < 70) return '#2196F3';
    if (getCalibrationProgress() < 100) return '#FF9800';
    return '#9C27B0';
  };

  return (
    <div className="biometric-enrollment">
      <div className="biometric-header">
        <h1>🔐 Biometric Calibration</h1>
        <p className="subtitle">Dahen's Typing Rhythm Authentication</p>
      </div>

      {isCalibrated && (
        <div className="calibration-complete">
          <div className="success-icon">✓</div>
          <h2>Calibration Complete</h2>
          <p>Your biometric signature has been saved.</p>
          <button className="calibrate-again" onClick={() => window.location.reload()}>
            Calibrate Again
          </button>
        </div>
      )}

      {!isCalibrated && (
        <>
          <div className="round-indicator">
            <span className="round-number">Round {round + 1}/{CALIBRATION_ROUNDS}</span>
            <span className="round-status">{isTyping ? 'Typing...' : 'Ready'}</span>
          </div>

          <div className="calibration-bar-container">
            <div 
              className="calibration-bar" 
              style={{ width: `${getCalibrationProgress()}%`, backgroundColor: getProgressColor() }}
            />
            <span className="progress-text">{Math.round(getCalibrationProgress())}%</span>
          </div>

          <div className="training-status">
            <span className="status-dot" style={{ 
              backgroundColor: trainingStatus === 'training' ? '#FF9800' : 
                             trainingStatus === 'complete' ? '#4CAF50' : '#9E9E9E' 
            }} />
            <span className="status-text">{trainingStatus === 'training' ? 'Training...' : 
                                      trainingStatus === 'complete' ? 'Model Saved' : 
                                      trainingStatus === 'error' ? 'Error' : 'Ready'}</span>
          </div>

          {feedback && (
            <div className={`feedback ${trainingStatus === 'error' ? 'error' : 'success'}`}>
              {feedback}
            </div>
          )}

          <div className="typing-area">
            <div className="golden-text">
              {GOLDEN_PARAGRAPH.split('').map((char, index) => {
                const typedIndex = keyData.findIndex(d => d.key === char);
                const isTyped = typedIndex !== -1;
                const isCurrent = isTyping && keyData.length === index + 1;
                
                return (
                  <span 
                    key={index}
                    className={`char ${isTyped ? 'typed' : ''} ${isCurrent ? 'current' : ''}`}
                  >
                    {char}
                  </span>
                );
              })}
            </div>

            <div className="key-stats">
              <div className="stat">
                <span className="stat-label">Keys Typed</span>
                <span className="stat-value">{keyData.length}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Avg Dwell</span>
                <span className="stat-value">{keyData.length > 0 ? Math.round(keyData.reduce((sum, d) => sum + d.dwellTime, 0) / keyData.length) : 0}ms</span>
              </div>
              <div className="stat">
                <span className="stat-label">Avg Flight</span>
                <span className="stat-value">{keyData.length > 0 ? Math.round(keyData.reduce((sum, d) => sum + d.flightTime, 0) / keyData.length) : 0}ms</span>
              </div>
            </div>
          </div>

          <div className="instructions">
            <h3>Instructions</h3>
            <ul>
              <li>Type the text above using your keyboard</li>
              <li>Complete {CALIBRATION_ROUNDS} rounds for accurate calibration</li>
              <li>Use natural typing speed - don't rush</li>
              <li>This captures your unique typing rhythm for biometric authentication</li>
            </ul>
          </div>

          {!isTyping && round < CALIBRATION_ROUNDS && (
            <button className="start-button" onClick={startRound}>
              Start Calibration Round {round + 1}
            </button>
          )}
        </>
      )}
    </div>
  );
};

export default BiometricEnrollment;
