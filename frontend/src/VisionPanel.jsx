import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import { Upload, Eye, X, Image as ImageIcon } from 'lucide-react'

const API_URL = "http://127.0.0.1:8000";

export default function VisionPanel({ onAnalyze }) {
  const [images, setImages] = useState([])
  const [selectedImage, setSelectedImage] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [analysis, setAnalysis] = useState('')
  const [question, setQuestion] = useState('What do you see in this image?')
  const fileInputRef = useRef(null)

  // ✅ FIX 1: Define loadImages BEFORE useEffect
  const loadImages = async () => {
    try {
      const res = await axios.get(`${API_URL}/vision/images`)
      setImages(res.data.images || [])
    } catch (error) {
      console.error("Failed to load images")
    }
  }

  // ✅ FIX 2: Now useEffect can call loadImages
  useEffect(() => {
    loadImages()
  }, [])

  const handleFileSelect = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)

      const res = await axios.post(`${API_URL}/vision/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      if (res.data.status === 'success') {
        alert(`✅ Image uploaded: ${file.name}`)
        loadImages()
      }
    } catch (error) {
      alert("❌ Upload failed: " + error.message)
    } finally {
      setUploading(false)
    }
  }

  const selectImage = (img) => {
    setSelectedImage(img)
    setAnalysis('')
  }

  const analyzeImage = async () => {
    if (!selectedImage) return

    setAnalyzing(true)
    try {
      const res = await axios.post(`${API_URL}/vision/analyze`, {
        filename: selectedImage.name,
        question: question
      })

      if (res.data.status === 'success') {
        setAnalysis(res.data.analysis)
        if (onAnalyze) {
          onAnalyze(res.data.analysis)
        }
      } else {
        setAnalysis("Error analyzing image")
      }
    } catch (error) {
      setAnalysis("Error: " + error.message)
    } finally {
      setAnalyzing(false)
    }
  }

  return (
    <div className="vision-panel">
      <div className="vision-sidebar">
        <h3>🖼️ Images</h3>
        <button className="upload-btn" onClick={() => fileInputRef.current?.click()} disabled={uploading}>
          <Upload size={16} /> {uploading ? 'Uploading...' : 'Upload Image'}
        </button>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileSelect}
          accept="image/*"
          style={{ display: 'none' }}
        />

        <div className="image-list">
          {images.map((img, idx) => (
            <div
              key={idx}
              className={`image-item ${selectedImage?.name === img.name ? 'selected' : ''}`}
              onClick={() => selectImage(img)}
            >
              <ImageIcon size={16} />
              <span>{img.name}</span>
            </div>
          ))}
          {images.length === 0 && (
            <p className="empty-msg">No images yet. Upload one!</p>
          )}
        </div>
      </div>

      <div className="vision-main">
        {selectedImage ? (
          <>
            <div className="image-preview">
              <img 
                src={`${API_URL}/vision/image/${selectedImage.name}?t=${Date.now()}`} 
                alt={selectedImage.name}
              />
              <button className="close-btn" onClick={() => setSelectedImage(null)}>
                <X size={20} />
              </button>
            </div>

            <div className="analyze-section">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask about this image..."
                className="question-input"
              />
              <button 
                onClick={analyzeImage} 
                disabled={analyzing || !selectedImage}
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
          </>
        ) : (
          <div className="no-selection">
            <ImageIcon size={64} color="#555" />
            <p>Select an image to analyze</p>
            <p style={{fontSize: '0.8rem', color: '#444'}}>Or upload a new one</p>
          </div>
        )}
      </div>
    </div>
  )
}