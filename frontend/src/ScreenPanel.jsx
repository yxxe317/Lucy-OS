import { useState, useEffect } from 'react'
import axios from 'axios'
import { Monitor, Camera, Eye, Trash2, Download } from 'lucide-react'
import './App.css'

const API_URL = "http://127.0.0.1:8000";

export default function ScreenPanel() {
  const [screenshots, setScreenshots] = useState([])
  const [selectedScreenshot, setSelectedScreenshot] = useState(null)
  const [capturing, setCapturing] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [analysis, setAnalysis] = useState('')
  const [question, setQuestion] = useState('What do you see on this screen?')
  const [screenInfo, setScreenInfo] = useState(null)

  useEffect(() => {
    loadScreenInfo()
    loadScreenshots()
  }, [])

  const loadScreenInfo = async () => {
    try {
      const res = await axios.get(`${API_URL}/screen/info`)
      setScreenInfo(res.data)
    } catch (error) {
      console.error("Failed to load screen info")
    }
  }

  const loadScreenshots = async () => {
    try {
      const res = await axios.get(`${API_URL}/screen/screenshots`)
      setScreenshots(res.data.screenshots || [])
    } catch (error) {
      console.error("Failed to load screenshots")
    }
  }

  const captureScreen = async () => {
    setCapturing(true)
    try {
      const res = await axios.post(`${API_URL}/screen/capture`, {})
      if (res.data.status === 'success') {
        alert(`✅ Screenshot captured: ${res.data.filename}`)
        loadScreenshots()
      }
    } catch (error) {
      alert("❌ Capture failed: " + error.message)
    } finally {
      setCapturing(false)
    }
  }

  const selectScreenshot = (shot) => {
    setSelectedScreenshot(shot)
    setAnalysis('')
  }

  const analyzeScreen = async () => {
    if (!selectedScreenshot) return

    setAnalyzing(true)
    try {
      const res = await axios.post(`${API_URL}/screen/analyze`, {
        filename: selectedScreenshot.name,
        question: question
      })

      if (res.data.status === 'success') {
        setAnalysis(res.data.analysis)
      } else {
        setAnalysis("Error analyzing screen")
      }
    } catch (error) {
      setAnalysis("Error: " + error.message)
    } finally {
      setAnalyzing(false)
    }
  }

  const deleteScreenshot = async (filename) => {
    if (!confirm('Delete this screenshot?')) return
    
    // Note: Need to add delete endpoint to backend
    alert("Delete functionality coming soon!")
  }

  const downloadScreenshot = (filename) => {
    window.open(`${API_URL}/screen/image/${filename}`, '_blank')
  }

  return (
    <div className="screen-panel">
      <div className="screen-sidebar">
        <h3>🖥️ Screen</h3>
        
        {screenInfo && (
          <div className="screen-info-card">
            <Monitor size={24} color="#00f0ff" />
            <div>
              <div className="stat-value">{screenInfo.width}x{screenInfo.height}</div>
              <div className="stat-label">Screen Resolution</div>
            </div>
          </div>
        )}

        <button 
          className="capture-btn" 
          onClick={captureScreen} 
          disabled={capturing}
        >
          <Camera size={16} /> {capturing ? 'Capturing...' : 'Take Screenshot'}
        </button>

        <div className="screenshot-list">
          <h4>Recent Screenshots</h4>
          {screenshots.map((shot, idx) => (
            <div
              key={idx}
              className={`screenshot-item ${selectedScreenshot?.name === shot.name ? 'selected' : ''}`}
              onClick={() => selectScreenshot(shot)}
            >
              <img 
                src={`${API_URL}/screen/image/${shot.name}`} 
                alt={shot.name}
              />
              <span>{shot.name}</span>
            </div>
          ))}
          {screenshots.length === 0 && (
            <p className="empty-msg">No screenshots yet</p>
          )}
        </div>
      </div>

      <div className="screen-main">
        {selectedScreenshot ? (
          <>
            <div className="screenshot-preview">
              <img 
                src={`${API_URL}/screen/image/${selectedScreenshot.name}`} 
                alt={selectedScreenshot.name}
              />
            </div>

            <div className="analyze-section">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask about this screen..."
                className="question-input"
              />
              <button 
                onClick={analyzeScreen} 
                disabled={analyzing}
                className="analyze-btn"
              >
                <Eye size={16} /> {analyzing ? 'Analyzing...' : 'Analyze'}
              </button>
            </div>

            {analysis && (
              <div className="analysis-result">
                <h4>👁️ Lucy's Analysis:</h4>
                <p>{analysis}</p>
              </div>
            )}

            <div className="screenshot-actions">
              <button onClick={() => downloadScreenshot(selectedScreenshot.name)}>
                <Download size={16} /> Download
              </button>
              <button onClick={() => deleteScreenshot(selectedScreenshot.name)}>
                <Trash2 size={16} /> Delete
              </button>
            </div>
          </>
        ) : (
          <div className="no-selection">
            <Monitor size={64} color="#555" />
            <p>Take a screenshot to analyze</p>
            <p style={{fontSize: '0.8rem', color: '#444'}}>Lucy can see and understand your screen!</p>
          </div>
        )}
      </div>
    </div>
  )
}