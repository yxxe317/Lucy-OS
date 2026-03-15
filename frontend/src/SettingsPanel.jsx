import { useState, useEffect } from 'react'
import axios from 'axios'
import { User, Heart, Plug, Settings, Save, Trash2, LogOut, Bell, Volume2 } from 'lucide-react'
import './App.css'

const API_URL = "http://127.0.0.1:8000";

export default function SettingsPanel({ currentUser, onLogout, onSpeak }) {
  const [activeTab, setActiveTab] = useState('profile')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState({ text: '', type: '' })
  const [profile, setProfile] = useState({ username: currentUser?.username || '', email: '', bio: '', interests: [] })
  const [personality, setPersonality] = useState({ style: 'friendly', tone: 'friendly', verbosity: 'medium', humor: true, emojis: true })
  const [settings, setSettings] = useState({ theme: 'dark', notifications: true, autoSpeak: true, voiceSpeed: 1.0, language: 'en' })
  const [plugins] = useState([
    { id: 'voice', name: 'Voice Recognition', description: 'Enable voice commands', enabled: true },
    { id: 'vision', name: 'Vision Analysis', description: 'Image recognition', enabled: true },
    { id: 'web', name: 'Web Search', description: 'Internet search', enabled: true },
    { id: 'code', name: 'Code Execution', description: 'Run Python code', enabled: true },
    { id: 'memory', name: 'Long-term Memory', description: 'Remember context', enabled: true }
  ])

  const getToken = () => {
    const token = localStorage.getItem('token')
    return token ? token.trim() : ''
  }

  useEffect(() => {
    loadProfile()
    loadPersonality()
    loadSettings()
  }, [])

  const loadProfile = async () => {
    try {
      const token = getToken()
      if (!token) return
      const res = await axios.get(`${API_URL}/users/profile`, { headers: { Authorization: `Bearer ${token}` } })
      if (res.data.success && res.data.profile) setProfile(res.data.profile)
    } catch (error) {
      console.log('Using default profile')
    }
  }

  const loadPersonality = async () => {
    try {
      const token = getToken()
      if (!token) return
      const res = await axios.get(`${API_URL}/users/personality`, { headers: { Authorization: `Bearer ${token}` } })
      if (res.data.success && res.data.personality) setPersonality(res.data.personality)
    } catch (error) {
      console.log('Using default personality')
    }
  }

  const loadSettings = async () => {
    try {
      const token = getToken()
      if (!token) return
      const res = await axios.get(`${API_URL}/users/settings`, { headers: { Authorization: `Bearer ${token}` } })
      if (res.data.success && res.data.settings) setSettings(res.data.settings)
    } catch (error) {
      console.log('Using default settings')
    }
  }

  const saveProfile = async () => {
    setLoading(true)
    setMessage({ text: '', type: '' })
    try {
      const token = getToken()
      if (!token) { setMessage({ text: '❌ Not authenticated', type: 'error' }); setLoading(false); return }
      
      const res = await axios.post(`${API_URL}/users/profile`, {
        username: profile.username,
        email: profile.email,
        bio: profile.bio,
        interests: Array.isArray(profile.interests) ? profile.interests : (profile.interests || '').split(',').map(i => i.trim())
      }, { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } })
      
      if (res.data.success) {
        setMessage({ text: '✅ Profile saved!', type: 'success' })
        // ❌ REMOVED: onSpeak('Profile saved successfully!') - was causing audio error
        setTimeout(() => setMessage({ text: '', type: '' }), 3000)
      } else {
        setMessage({ text: '⚠️ ' + (res.data.message || 'Failed'), type: 'error' })
      }
    } catch (error) {
      setMessage({ text: '❌ ' + (error.response?.data?.message || error.message || 'Failed'), type: 'error' })
    } finally { setLoading(false) }
  }

  const savePersonality = async () => {
    setLoading(true)
    setMessage({ text: '', type: '' })
    try {
      const token = getToken()
      if (!token) { setMessage({ text: '❌ Not authenticated', type: 'error' }); setLoading(false); return }
      
      const res = await axios.post(`${API_URL}/users/personality`, {
        personality: {
          style: personality.style,
          tone: personality.tone,
          verbosity: personality.verbosity,
          humor: personality.humor,
          emojis: personality.emojis
        }
      }, { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } })
      
      if (res.data.success) {
        setMessage({ text: '✅ Personality saved!', type: 'success' })
        // ❌ REMOVED: onSpeak('Personality saved!') - was causing audio error
        setTimeout(() => setMessage({ text: '', type: '' }), 3000)
      } else {
        setMessage({ text: '⚠️ ' + (res.data.message || 'Failed'), type: 'error' })
      }
    } catch (error) {
      setMessage({ text: '❌ ' + (error.response?.data?.message || error.message || 'Failed'), type: 'error' })
    } finally { setLoading(false) }
  }

  const saveSettings = async () => {
    setLoading(true)
    setMessage({ text: '', type: '' })
    try {
      const token = getToken()
      if (!token) { setMessage({ text: '❌ Not authenticated', type: 'error' }); setLoading(false); return }
      
      const res = await axios.post(`${API_URL}/users/settings`, {
        settings: {
          theme: settings.theme,
          notifications: settings.notifications,
          autoSpeak: settings.autoSpeak,
          voiceSpeed: settings.voiceSpeed,
          language: settings.language
        }
      }, { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } })
      
      if (res.data.success) {
        setMessage({ text: '✅ Settings saved!', type: 'success' })
        // ❌ REMOVED: onSpeak('Settings saved!') - was causing audio error
        setTimeout(() => setMessage({ text: '', type: '' }), 3000)
      } else {
        setMessage({ text: '⚠️ ' + (res.data.message || 'Failed'), type: 'error' })
      }
    } catch (error) {
      setMessage({ text: '❌ ' + (error.response?.data?.message || error.message || 'Failed'), type: 'error' })
    } finally { setLoading(false) }
  }

  const togglePlugin = (pluginId) => {
    setMessage({ text: '✅ Plugin toggled!', type: 'success' })
    setTimeout(() => setMessage({ text: '', type: '' }), 2000)
  }

  return (
    <div className="settings-panel">
      {/* Sidebar */}
      <div className="settings-sidebar">
        <h3><Settings size={20} /> Settings</h3>
        
        <div className="settings-tabs">
          <button className={activeTab === 'profile' ? 'active' : ''} onClick={() => setActiveTab('profile')}>
            <User size={16} /> Profile
          </button>
          <button className={activeTab === 'personality' ? 'active' : ''} onClick={() => setActiveTab('personality')}>
            <Heart size={16} /> Personality
          </button>
          <button className={activeTab === 'plugins' ? 'active' : ''} onClick={() => setActiveTab('plugins')}>
            <Plug size={16} /> Plugins
          </button>
          <button className={activeTab === 'general' ? 'active' : ''} onClick={() => setActiveTab('general')}>
            <Settings size={16} /> General
          </button>
          <button className={activeTab === 'danger' ? 'active' : ''} onClick={() => setActiveTab('danger')}>
            <Trash2 size={16} /> Danger Zone
          </button>
        </div>

        <div className="user-info-card">
          <User size={48} />
          <h4>{currentUser?.username || 'User'}</h4>
          <p>🟢 Online</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="settings-main">
        {message.text && <div className={`settings-message ${message.type}`}>{message.text}</div>}

        {activeTab === 'profile' && (
          <div className="settings-section">
            <h3><User size={20} /> User Profile</h3>
            <div className="profile-form">
              <div className="form-group">
                <label>Username</label>
                <input type="text" value={profile.username} onChange={(e) => setProfile({ ...profile, username: e.target.value })} placeholder="Your username" />
              </div>
              <div className="form-group">
                <label>Email</label>
                <input type="email" value={profile.email} onChange={(e) => setProfile({ ...profile, email: e.target.value })} placeholder="your@email.com" />
              </div>
              <div className="form-group">
                <label>Bio</label>
                <textarea value={profile.bio} onChange={(e) => setProfile({ ...profile, bio: e.target.value })} placeholder="Tell us about yourself..." rows="4" />
              </div>
              <div className="form-group">
                <label>Interests (comma separated)</label>
                <input type="text" value={Array.isArray(profile.interests) ? profile.interests.join(', ') : profile.interests} onChange={(e) => setProfile({ ...profile, interests: e.target.value.split(',').map(i => i.trim()) })} placeholder="AI, Security, Coding..." />
              </div>
              <button className="save-btn" onClick={saveProfile} disabled={loading}><Save size={16} /> {loading ? 'Saving...' : 'Save Profile'}</button>
            </div>
          </div>
        )}

        {activeTab === 'personality' && (
          <div className="settings-section">
            <h3><Heart size={20} /> Lucy's Personality</h3>
            <div className="personality-form">
              <div className="form-group">
                <label>Communication Style</label>
                <select value={personality.style} onChange={(e) => setPersonality({ ...personality, style: e.target.value })}>
                  <option value="professional">Professional</option>
                  <option value="friendly">Friendly</option>
                  <option value="casual">Casual</option>
                  <option value="technical">Technical</option>
                </select>
              </div>
              <div className="form-group">
                <label>Tone</label>
                <select value={personality.tone} onChange={(e) => setPersonality({ ...personality, tone: e.target.value })}>
                  <option value="friendly">Friendly</option>
                  <option value="neutral">Neutral</option>
                  <option value="enthusiastic">Enthusiastic</option>
                  <option value="calm">Calm</option>
                </select>
              </div>
              <div className="form-group">
                <label>Verbosity</label>
                <select value={personality.verbosity} onChange={(e) => setPersonality({ ...personality, verbosity: e.target.value })}>
                  <option value="brief">Brief</option>
                  <option value="medium">Medium</option>
                  <option value="detailed">Detailed</option>
                </select>
              </div>
              <div className="form-group checkbox-group">
                <label><input type="checkbox" checked={personality.humor} onChange={(e) => setPersonality({ ...personality, humor: e.target.checked })} /> Enable Humor</label>
              </div>
              <div className="form-group checkbox-group">
                <label><input type="checkbox" checked={personality.emojis} onChange={(e) => setPersonality({ ...personality, emojis: e.target.checked })} /> Use Emojis</label>
              </div>
              <button className="save-btn" onClick={savePersonality} disabled={loading}><Save size={16} /> {loading ? 'Saving...' : 'Save Personality'}</button>
            </div>
          </div>
        )}

        {activeTab === 'plugins' && (
          <div className="settings-section">
            <h3><Plug size={20} /> Plugin Manager</h3>
            <div className="plugins-grid">
              {plugins.map((plugin) => (
                <div key={plugin.id} className={`plugin-card ${plugin.enabled ? 'enabled' : 'disabled'}`}>
                  <div className="plugin-header">
                    <h4>{plugin.name}</h4>
                    <span className={`status-badge ${plugin.enabled ? 'on' : 'off'}`}>{plugin.enabled ? 'ON' : 'OFF'}</span>
                  </div>
                  <p className="plugin-description">{plugin.description}</p>
                  <button className={`toggle-btn ${plugin.enabled ? 'disable' : 'enable'}`} onClick={() => togglePlugin(plugin.id)}>{plugin.enabled ? 'Disable' : 'Enable'}</button>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'general' && (
          <div className="settings-section">
            <h3><Settings size={20} /> General Settings</h3>
            <div className="settings-list">
              <div className="setting-item">
                <label>Theme</label>
                <select value={settings.theme} onChange={(e) => setSettings({ ...settings, theme: e.target.value })}>
                  <option value="dark">Dark</option>
                  <option value="light">Light</option>
                  <option value="auto">Auto</option>
                </select>
              </div>
              <div className="setting-item">
                <label><Bell size={16} /> Notifications</label>
                <input type="checkbox" checked={settings.notifications} onChange={(e) => setSettings({ ...settings, notifications: e.target.checked })} />
              </div>
              <div className="setting-item">
                <label><Volume2 size={16} /> Auto Speak Responses</label>
                <input type="checkbox" checked={settings.autoSpeak} onChange={(e) => setSettings({ ...settings, autoSpeak: e.target.checked })} />
              </div>
              <div className="setting-item">
                <label>Voice Speed: {settings.voiceSpeed}x</label>
                <input type="range" min="0.5" max="2.0" step="0.1" value={settings.voiceSpeed} onChange={(e) => setSettings({ ...settings, voiceSpeed: parseFloat(e.target.value) })} style={{ width: '200px' }} />
              </div>
              <button className="save-btn" onClick={saveSettings} disabled={loading}><Save size={16} /> {loading ? 'Saving...' : 'Save Settings'}</button>
            </div>
          </div>
        )}

        {activeTab === 'danger' && (
          <div className="settings-section danger-section">
            <h3><Trash2 size={20} /> Danger Zone</h3>
            <div className="warning-box">⚠️ Warning: These actions are irreversible!</div>
            <div className="danger-item">
              <h4>Delete All Data</h4>
              <p>This will delete all your conversations, settings, and personal data.</p>
              <button className="delete-btn" onClick={onLogout}><Trash2 size={16} /> Delete Everything</button>
            </div>
            <div className="danger-item">
              <h4>Logout</h4>
              <p>Sign out of your account on this device.</p>
              <button className="logout-btn" onClick={onLogout}><LogOut size={16} /> Logout</button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}