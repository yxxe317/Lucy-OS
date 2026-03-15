import { useState, useEffect } from 'react'
import axios from 'axios'
import { Heart, Save, User, Smile, Frown, Meh, Sparkles, Volume2, MessageSquare, Zap, RefreshCw } from 'lucide-react'
import './App.css'

const API_URL = "http://127.0.0.1:8000";

export default function PersonalityPanel({ onSpeak }) {
  const [activeTab, setActiveTab] = useState('overview')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState({ text: '', type: '' })
  
  // Personality Settings
  const [personality, setPersonality] = useState({
    style: 'friendly',
    tone: 'friendly',
    verbosity: 'medium',
    humor: true,
    emojis: true
  })
  
  // Stats
  const [stats, setStats] = useState({
    totalInteractions: 0,
    positiveFeedback: 0,
    negativeFeedback: 0,
    averageResponseLength: 0
  })
  
  // Profile
  const [profile, setProfile] = useState({
    username: '',
    memberSince: '',
    lastActive: ''
  })

  useEffect(() => {
    loadPersonality()
    loadStats()
    loadProfile()
  }, [])

  const getToken = () => {
    const token = localStorage.getItem('token')
    return token?.trim() || ''
  }

  const loadPersonality = async () => {
    try {
      const token = getToken()
      if (!token) {
        console.warn('No token found for loading personality')
        return
      }
      
      const res = await axios.get(`${API_URL}/users/personality`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      if (res.data.success && res.data.personality) {
        setPersonality(res.data.personality)
      }
    } catch (error) {
      console.error('Failed to load personality:', error)
      // Use defaults on error
      setPersonality({
        style: 'friendly',
        tone: 'friendly',
        verbosity: 'medium',
        humor: true,
        emojis: true
      })
    }
  }

  const loadStats = async () => {
    try {
      const token = getToken()
      if (!token) return
      
      const res = await axios.get(`${API_URL}/users/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      if (res.data.success && res.data.stats) {
        setStats(res.data.stats)
      }
    } catch (error) {
      console.error('Failed to load stats')
    }
  }

  const loadProfile = async () => {
    try {
      const token = getToken()
      const username = localStorage.getItem('username')
      
      setProfile({
        username: username || 'User',
        memberSince: '2026',
        lastActive: new Date().toLocaleDateString()
      })
    } catch (error) {
      console.error('Failed to load profile')
    }
  }

  const savePersonality = async () => {
    setLoading(true)
    setMessage({ text: '', type: '' })
    
    try {
      const token = getToken()
      if (!token) {
        setMessage({ text: '❌ Not authenticated. Please login again.', type: 'error' })
        setLoading(false)
        return
      }
      
      console.log('📤 Saving personality:', personality)
      
      const res = await axios.post(`${API_URL}/users/personality`, {
        personality: {
          style: personality.style,
          tone: personality.tone,
          verbosity: personality.verbosity,
          humor: personality.humor,
          emojis: personality.emojis
        }
      }, {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      
      console.log('📥 Response:', res.data)
      
      if (res.data.success) {
        setMessage({ text: '✅ Personality saved successfully!', type: 'success' })
        if (onSpeak) {
          onSpeak('Personality settings saved successfully!')
        }
        setTimeout(() => setMessage({ text: '', type: '' }), 3000)
      } else {
        setMessage({ text: '⚠️ ' + (res.data.message || 'Failed to save'), type: 'error' })
      }
    } catch (error) {
      console.error('❌ Save error:', error)
      console.error('Response data:', error.response?.data)
      
      const errorMsg = error.response?.data?.message || error.message || 'Failed to save personality'
      setMessage({ text: `❌ Error: ${errorMsg}`, type: 'error' })
    } finally {
      setLoading(false)
    }
  }

  const resetPersonality = () => {
    setPersonality({
      style: 'friendly',
      tone: 'friendly',
      verbosity: 'medium',
      humor: true,
      emojis: true
    })
    setMessage({ text: '🔄 Reset to defaults. Click Save to apply.', type: 'success' })
    setTimeout(() => setMessage({ text: '', type: '' }), 3000)
  }

  const getEmotionIcon = () => {
    switch(personality.tone) {
      case 'friendly': return <Smile size={20} color="#00ff88" />
      case 'serious': return <Meh size={20} color="#888" />
      case 'playful': return <Smile size={20} color="#ff8800" />
      case 'empathetic': return <Heart size={20} color="#bc13fe" />
      case 'enthusiastic': return <Sparkles size={20} color="#00f0ff" />
      default: return <Meh size={20} />
    }
  }

  return (
    <div className="personality-panel">
      {/* Sidebar */}
      <div className="personality-sidebar">
        <h3><Heart size={20} /> Personality</h3>
        
        <div className="settings-tabs">
          <button className={activeTab === 'overview' ? 'active' : ''} onClick={() => setActiveTab('overview')}>
            <User size={16} /> Overview
          </button>
          <button className={activeTab === 'style' ? 'active' : ''} onClick={() => setActiveTab('style')}>
            <Sparkles size={16} /> Style
          </button>
          <button className={activeTab === 'tone' ? 'active' : ''} onClick={() => setActiveTab('tone')}>
            {getEmotionIcon()} Tone
          </button>
          <button className={activeTab === 'feedback' ? 'active' : ''} onClick={() => setActiveTab('feedback')}>
            <MessageSquare size={16} /> Feedback
          </button>
        </div>

        <div className="user-info-card">
          <User size={48} />
          <h4>{profile.username}</h4>
          <p>Member since: {profile.memberSince}</p>
          <p className="interactions">{stats.totalInteractions} interactions</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="personality-main">
        {message.text && (
          <div className={`settings-message ${message.type}`}>
            {message.text}
          </div>
        )}

        {/* OVERVIEW TAB */}
        {activeTab === 'overview' && (
          <div className="settings-section">
            <h4><User size={20} /> Personality Overview</h4>
            
            <div className="stats-grid">
              <div className="stat-box">
                <div className="stat-value">{personality.style}</div>
                <div className="stat-label">Communication Style</div>
              </div>
              <div className="stat-box">
                <div className="stat-value">{personality.tone}</div>
                <div className="stat-label">Tone</div>
              </div>
              <div className="stat-box">
                <div className="stat-value">{personality.verbosity}</div>
                <div className="stat-label">Verbosity</div>
              </div>
              <div className="stat-box">
                <div className="stat-value">{personality.emojis ? '✅' : '❌'}</div>
                <div className="stat-label">Emojis</div>
              </div>
            </div>

            <div className="profile-info">
              <h3><Zap size={16} /> Quick Settings</h3>
              <div className="info-grid">
                <div className="info-item">
                  <span className="info-label">Humor</span>
                  <span className="info-value">{personality.humor ? 'Enabled' : 'Disabled'}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Style</span>
                  <span className="info-value">{personality.style}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Tone</span>
                  <span className="info-value">{personality.tone}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Verbosity</span>
                  <span className="info-value">{personality.verbosity}</span>
                </div>
              </div>
            </div>

            <div className="form-actions">
              <button className="save-btn" onClick={savePersonality} disabled={loading}>
                <Save size={16} /> {loading ? 'Saving...' : 'Save Changes'}
              </button>
              <button className="cancel-btn" onClick={resetPersonality}>
                <RefreshCw size={16} /> Reset
              </button>
            </div>
          </div>
        )}

        {/* STYLE TAB */}
        {activeTab === 'style' && (
          <div className="settings-section">
            <h4><Sparkles size={20} /> Communication Style</h4>
            
            <div className="edit-form">
              <div className="form-group">
                <label>Style</label>
                <select
                  value={personality.style}
                  onChange={(e) => setPersonality({ ...personality, style: e.target.value })}
                >
                  <option value="professional">Professional</option>
                  <option value="casual">Casual</option>
                  <option value="friendly">Friendly</option>
                  <option value="technical">Technical</option>
                  <option value="creative">Creative</option>
                </select>
                <p className="form-hint">How Lucy communicates with you</p>
              </div>

              <div className="form-group">
                <label>Verbosity</label>
                <select
                  value={personality.verbosity}
                  onChange={(e) => setPersonality({ ...personality, verbosity: e.target.value })}
                >
                  <option value="brief">Brief (Short responses)</option>
                  <option value="medium">Medium (Balanced)</option>
                  <option value="detailed">Detailed (Comprehensive)</option>
                </select>
                <p className="form-hint">Length of Lucy's responses</p>
              </div>

              <div className="form-group checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    checked={personality.humor}
                    onChange={(e) => setPersonality({ ...personality, humor: e.target.checked })}
                  />
                  Enable Humor
                </label>
                <p className="form-hint">Lucy will use jokes and witty remarks</p>
              </div>

              <div className="form-group checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    checked={personality.emojis}
                    onChange={(e) => setPersonality({ ...personality, emojis: e.target.checked })}
                  />
                  Use Emojis
                </label>
                <p className="form-hint">Add emojis to responses</p>
              </div>
            </div>

            <div className="form-actions">
              <button className="save-btn" onClick={savePersonality} disabled={loading}>
                <Save size={16} /> {loading ? 'Saving...' : 'Save Style'}
              </button>
            </div>
          </div>
        )}

        {/* TONE TAB */}
        {activeTab === 'tone' && (
          <div className="settings-section">
            <h4><Heart size={20} /> Tone & Emotion</h4>
            
            <div className="edit-form">
              <div className="form-group">
                <label>Tone</label>
                <select
                  value={personality.tone}
                  onChange={(e) => setPersonality({ ...personality, tone: e.target.value })}
                >
                  <option value="friendly">Friendly 😊</option>
                  <option value="serious">Serious 😐</option>
                  <option value="playful">Playful 😄</option>
                  <option value="empathetic">Empathetic 🤗</option>
                  <option value="enthusiastic">Enthusiastic 🎉</option>
                </select>
                <p className="form-hint">Lucy's emotional tone</p>
              </div>
            </div>

            <div className="form-actions">
              <button className="save-btn" onClick={savePersonality} disabled={loading}>
                <Save size={16} /> {loading ? 'Saving...' : 'Save Tone'}
              </button>
            </div>
          </div>
        )}

        {/* FEEDBACK TAB */}
        {activeTab === 'feedback' && (
          <div className="settings-section">
            <h4><MessageSquare size={20} /> Feedback & Stats</h4>
            
            <div className="feedback-section">
              <h3>Response Feedback</h3>
              <div className="feedback-bars">
                <div className="feedback-bar">
                  <span>Positive</span>
                  <div className="bar-bg">
                    <div 
                      className="bar-fill positive" 
                      style={{ width: `${stats.totalInteractions > 0 ? (stats.positiveFeedback / stats.totalInteractions) * 100 : 50}%` }}
                    ></div>
                  </div>
                  <span>{stats.positiveFeedback}</span>
                </div>
                <div className="feedback-bar">
                  <span>Negative</span>
                  <div className="bar-bg">
                    <div 
                      className="bar-fill negative" 
                      style={{ width: `${stats.totalInteractions > 0 ? (stats.negativeFeedback / stats.totalInteractions) * 100 : 10}%` }}
                    ></div>
                  </div>
                  <span>{stats.negativeFeedback}</span>
                </div>
              </div>
            </div>

            <div className="interests-section">
              <h3><Volume2 size={16} /> Voice Settings</h3>
              <div className="info-grid">
                <div className="info-item">
                  <span className="info-label">Total Interactions</span>
                  <span className="info-value">{stats.totalInteractions}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Avg Response Length</span>
                  <span className="info-value">{stats.averageResponseLength} chars</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Last Active</span>
                  <span className="info-value">{profile.lastActive}</span>
                </div>
              </div>
            </div>

            <div className="form-actions">
              <button className="save-btn" onClick={loadStats}>
                <RefreshCw size={16} /> Refresh Stats
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}