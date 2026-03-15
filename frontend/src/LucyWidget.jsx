import { useState, useEffect } from 'react'
import './App.css'

export default function LucyWidget({ isSpeaking, emotion }) {
  const [visible, setVisible] = useState(true)
  const [position, setPosition] = useState({ x: 20, y: 20 })
  const [isDragging, setIsDragging] = useState(false)
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 })

  // Get current emotion state
  const currentEmotion = emotion || 'neutral'

  const handleMouseDown = (e) => {
    setIsDragging(true)
    setDragOffset({
      x: e.clientX - position.x,
      y: e.clientY - position.y
    })
  }

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (isDragging) {
        setPosition({
          x: e.clientX - dragOffset.x,
          y: e.clientY - dragOffset.y
        })
      }
    }

    const handleMouseUp = () => {
      setIsDragging(false)
    }

    if (isDragging) {
      window.addEventListener('mousemove', handleMouseMove)
      window.addEventListener('mouseup', handleMouseUp)
    }

    return () => {
      window.removeEventListener('mousemove', handleMouseMove)
      window.removeEventListener('mouseup', handleMouseUp)
    }
  }, [isDragging, dragOffset])

  if (!visible) return null

  return (
    <div 
      className={`lucy-widget ${currentEmotion} ${isSpeaking ? 'speaking' : ''}`}
      style={{ left: position.x, top: position.y }}
      onMouseDown={handleMouseDown}
    >
      <div className="lucy-avatar">
        {/* Emotion rings */}
        <div className={`avatar-ring ${isSpeaking ? 'active' : ''}`}></div>
        <div className={`avatar-ring-2 ${isSpeaking ? 'active' : ''}`}></div>
        
        {/* Face */}
        <div className={`avatar-face ${currentEmotion}`}>
          {/* Eyes */}
          <div className={`eye left ${currentEmotion}`}>
            <div className="pupil"></div>
          </div>
          <div className={`eye right ${currentEmotion}`}>
            <div className="pupil"></div>
          </div>
          
          {/* Eyebrows */}
          <div className={`eyebrow left ${currentEmotion}`}></div>
          <div className={`eyebrow right ${currentEmotion}`}></div>
          
          {/* Mouth - changes shape based on emotion */}
          <div className={`mouth ${currentEmotion} ${isSpeaking ? 'talk' : ''}`}></div>
          
          {/* Blush for happy/excited */}
          {(currentEmotion === 'happy' || currentEmotion === 'excited') && (
            <>
              <div className="blush left"></div>
              <div className="blush right"></div>
            </>
          )}
          
          {/* Sweat drop for confused/nervous */}
          {(currentEmotion === 'confused' || currentEmotion === 'concerned') && (
            <div className="sweat"></div>
          )}
        </div>
      </div>
      
      {/* Emotion label */}
      <div className="emotion-label">
        {getEmotionText(currentEmotion)}
      </div>
      
      {/* Controls */}
      <div className="widget-controls">
        <button className="control-btn" onClick={() => setVisible(false)}>×</button>
      </div>

      {isSpeaking && (
        <div className="speaking-indicator">
          <span>Lucy is speaking...</span>
        </div>
      )}
    </div>
  )
}

// Helper function for emotion text
function getEmotionText(emotion) {
  const texts = {
    neutral: 'Ready',
    happy: 'Happy 😊',
    thinking: 'Thinking 🤔',
    surprised: 'Surprised 😮',
    confused: 'Confused 😕',
    concerned: 'Concerned 😢',
    excited: 'Excited 🤩',
    error: 'Error ⚠️'
  }
  return texts[emotion] || 'Ready'
}