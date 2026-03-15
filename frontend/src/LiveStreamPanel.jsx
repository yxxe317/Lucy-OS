import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import { Monitor, Play, Square, Circle, StopCircle, Download, Eye, Volume2, VolumeX, Mic, MicOff, Maximize2, Minimize2, Trash2 } from 'lucide-react'
import './App.css'

const API_URL = "http://127.0.0.1:8000";

export default function LiveStreamPanel({ onSpeak }) {
  const [isStreaming, setIsStreaming] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const [currentFrame, setCurrentFrame] = useState(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [analysis, setAnalysis] = useState('')
  const [question, setQuestion] = useState('What do you see on my screen?')
  const [chatMessages, setChatMessages] = useState([])
  const [recordings, setRecordings] = useState([])
  const [autoSpeak, setAutoSpeak] = useState(true)
  const [isMuted, setIsMuted] = useState(false)
  const [fps, setFps] = useState(5)
  
  const frameIntervalRef = useRef(null)
  const chatEndRef = useRef(null)
  const streamViewerRef = useRef(null)

  useEffect(() => {
    loadRecordings()
    return () => stopStream()
  }, [])

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" })
    }
  }, [chatMessages])

  const loadRecordings = async () => {
    try {
      const res = await axios.get(`${API_URL}/stream/recordings`)
      setRecordings(res.data.recordings || [])
    } catch (error) {
      console.error("Failed to load recordings")
    }
  }

  const startStream = async () => {
    try {
      const stream = await navigator.mediaDevices.getDisplayMedia({
        video: { cursor: "always", width: { ideal: 1920 }, height: { ideal: 1080 } },
        audio: false
      })
      
      const res = await axios.post(`${API_URL}/stream/start`, { fps })
      
      if (res.data.status === 'started') {
        setIsStreaming(true)
        setSessionId(res.data.session_id)
        
        frameIntervalRef.current = setInterval(async () => {
          try {
            const frameRes = await axios.get(`${API_URL}/stream/frame`)
            if (frameRes.data.frame) {
              setCurrentFrame(frameRes.data.frame)
            }
          } catch (error) {
            console.error("Frame capture error:", error)
          }
        }, 1000 / fps)
        
        if (res.data.auto_greeting) {
          addChatMessage('lucy', res.data.auto_greeting)
          setAnalysis(res.data.auto_greeting)
          if (autoSpeak && onSpeak && !isMuted) {
            onSpeak(res.data.auto_greeting)
          }
        }
        
        addSystemMessage(`✅ Stream started: ${res.data.session_id}`)
      }
    } catch (error) {
      console.error("Stream error:", error)
      alert("❌ Failed to start stream: " + error.message)
    }
  }

  const stopStream = async () => {
    if (frameIntervalRef.current) {
      clearInterval(frameIntervalRef.current)
      frameIntervalRef.current = null
    }
    try {
      await axios.post(`${API_URL}/stream/stop`)
      setIsStreaming(false)
      setSessionId(null)
      setCurrentFrame(null)
      addSystemMessage('⏹️ Stream stopped')
    } catch (error) {
      console.error("Stop stream error:", error)
    }
  }

  const startRecording = async () => {
    try {
      await axios.post(`${API_URL}/stream/record/start`)
      setIsRecording(true)
      addSystemMessage('🔴 Recording started')
    } catch (error) {
      alert("❌ Failed to start recording")
    }
  }

  const stopRecording = async () => {
    try {
      const res = await axios.post(`${API_URL}/stream/record/stop`)
      setIsRecording(false)
      addSystemMessage(`⏹️ Recording saved (${res.data.frames} frames)`)
      loadRecordings()
    } catch (error) {
      alert("❌ Failed to stop recording")
    }
  }

  const analyzeScreen = async () => {
    if (!isStreaming || !question.trim()) return
    
    setAnalyzing(true)
    try {
      const res = await axios.post(`${API_URL}/stream/analyze`, { 
        question,
        auto_speak: autoSpeak && !isMuted
      })
      
      if (res.data.status === 'success') {
        addChatMessage('user', question)
        addChatMessage('lucy', res.data.analysis)
        setAnalysis(res.data.analysis)
        
        if (res.data.spoke && autoSpeak && onSpeak && !isMuted) {
          addSystemMessage('🔊 Lucy spoke the analysis')
          onSpeak(res.data.analysis)
        }
      }
    } catch (error) {
      setAnalysis("Error: " + error.message)
      addChatMessage('system', '❌ Error: ' + error.message)
    } finally {
      setAnalyzing(false)
    }
  }

  const addChatMessage = (sender, text) => {
    setChatMessages(prev => [...prev, { sender, text, timestamp: new Date().toISOString() }])
  }

  const addSystemMessage = (text) => {
    setChatMessages(prev => [...prev, { sender: 'system', text, timestamp: new Date().toISOString() }])
  }

  const downloadRecording = (filename) => {
    window.open(`${API_URL}/stream/recording/${filename}`, '_blank')
    addSystemMessage(`📥 Downloading: ${filename}`)
  }

  const deleteRecording = async (filename) => {
    if (!window.confirm(`Delete ${filename}?`)) return
    try {
      await axios.delete(`${API_URL}/stream/recording/${filename}`)
      addSystemMessage(`🗑️ Deleted: ${filename}`)
      loadRecordings()
    } catch (error) {
      alert("❌ Failed to delete recording")
    }
  }

  const toggleFullscreen = () => {
    if (!streamViewerRef.current) return
    if (!document.fullscreenElement) {
      streamViewerRef.current.requestFullscreen().catch(err => console.error(err))
    } else {
      document.exitFullscreen()
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      analyzeScreen()
    }
  }

  return (
    <div className="livestream-panel">
      {/* Sidebar */}
      <div className="stream-sidebar">
        <h3>📹 Live Stream</h3>
        
        <div className="stream-status">
          <div className={`status-dot ${isStreaming ? 'live' : 'offline'}`}></div>
          <span>{isStreaming ? 'LIVE' : 'OFFLINE'}</span>
        </div>

        {!isStreaming ? (
          <button className="start-stream-btn" onClick={startStream}>
            <Play size={16} /> Start Screen Share
          </button>
        ) : (
          <>
            <button className="stop-stream-btn" onClick={stopStream}>
              <StopCircle size={16} /> Stop Stream
            </button>
            {!isRecording ? (
              <button className="start-record-btn" onClick={startRecording}>
                <Circle size={16} /> Start Recording
              </button>
            ) : (
              <button className="stop-record-btn" onClick={stopRecording}>
                <Square size={16} /> Stop Recording
              </button>
            )}
          </>
        )}

        <div className="stream-settings">
          <label>FPS: {fps}</label>
          <select value={fps} onChange={(e) => setFps(Number(e.target.value))} disabled={isStreaming}>
            <option value={3}>3 FPS</option>
            <option value={5}>5 FPS</option>
            <option value={10}>10 FPS</option>
            <option value={15}>15 FPS</option>
          </select>

          <label>
            <input type="checkbox" checked={autoSpeak} onChange={(e) => setAutoSpeak(e.target.checked)} />
            🔊 Auto-Speak
          </label>

          <label>
            <input type="checkbox" checked={isMuted} onChange={(e) => setIsMuted(e.target.checked)} />
            {isMuted ? <VolumeX size={14} /> : <Volume2 size={14} />} Muted
          </label>
        </div>

        <div className="stream-info">
          <p><strong>Session:</strong> {sessionId || 'N/A'}</p>
          <p><strong>Recording:</strong> {isRecording ? 'Yes' : 'No'}</p>
          <p><strong>FPS:</strong> {fps}</p>
        </div>

        <div className="recordings-list">
          <h4>📁 Recordings</h4>
          {recordings.length > 0 ? (
            recordings.map((rec, idx) => (
              <div key={idx} className="recording-item">
                <div className="recording-info">
                  <span className="recording-name">{rec.name}</span>
                  <span className="recording-size">{rec.size || 'N/A'}</span>
                </div>
                <div className="recording-actions">
                  <button className="download-btn" onClick={() => downloadRecording(rec.name)}>
                    <Download size={14} />
                  </button>
                  <button className="delete-btn" onClick={() => deleteRecording(rec.name)}>
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            ))
          ) : (
            <p className="empty-msg">No recordings yet</p>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="stream-main">
        {/* Stream Viewer */}
        <div className="stream-viewer" ref={streamViewerRef}>
          {currentFrame ? (
            <>
              <img src={`data:image/jpeg;base64,${currentFrame}`} alt="Live Screen" className="stream-frame" />
              {isRecording && (
                <div className="recording-indicator">
                  <Circle size={12} className="recording-dot" />
                  <span>REC</span>
                </div>
              )}
              <div className="stream-overlay">
                <button className="overlay-btn" onClick={toggleFullscreen}>
                  <Maximize2 size={18} />
                </button>
                <button className="overlay-btn" onClick={() => setIsMuted(!isMuted)}>
                  {isMuted ? <VolumeX size={18} /> : <Volume2 size={18} />}
                </button>
              </div>
            </>
          ) : (
            <div className="no-stream">
              <Monitor size={64} color="#555" />
              <h3>No Stream Active</h3>
              <p>Click "Start Screen Share" to begin</p>
              <p className="hint">Lucy will see your screen in real-time!</p>
            </div>
          )}
          {isStreaming && (
            <div className="live-badge">
              <Circle size={8} className="live-dot" />
              LIVE
            </div>
          )}
        </div>

        {/* Chat */}
        <div className="stream-chat">
          <div className="chat-header">
            <h4>💬 Live Chat with Lucy</h4>
            <div className="chat-stats">
              <span>{chatMessages.length} messages</span>
            </div>
          </div>
          
          <div className="chat-messages">
            {chatMessages.length > 0 ? (
              chatMessages.map((msg, idx) => (
                <div key={idx} className={`chat-message ${msg.sender}`}>
                  <div className="message-avatar">
                    {msg.sender === 'user' && '👤'}
                    {msg.sender === 'lucy' && '🤖'}
                    {msg.sender === 'system' && '⚙️'}
                  </div>
                  <div className="message-content">
                    <div className="chat-bubble">{msg.text}</div>
                    <div className="chat-time">
                      {new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="empty-chat">
                <MessageCircle size={40} color="#555" />
                <p>No messages yet</p>
                <p className="hint">Ask Lucy about your screen!</p>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          <div className="chat-input-area">
            <div className="input-wrapper">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask Lucy about your screen..."
                disabled={!isStreaming || analyzing}
                className="chat-input"
              />
              {analyzing && (
                <div className="analyzing-indicator">
                  <div className="spinner"></div>
                  <span>Analyzing...</span>
                </div>
              )}
            </div>
            <button onClick={analyzeScreen} disabled={!isStreaming || analyzing || !question.trim()} className="analyze-btn">
              <Eye size={16} /> {analyzing ? '...' : 'Analyze'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}