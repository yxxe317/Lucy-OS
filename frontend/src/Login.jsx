import { useState } from 'react'
import axios from 'axios'
import { Sparkles, LogIn, UserPlus, User, Lock } from 'lucide-react'
import './Login.css'  // ✅ ADD THIS LINE

const API_URL = "http://127.0.0.1:8000";

export default function Login({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const endpoint = isRegister ? '/auth/register' : '/auth/login'
      const res = await axios.post(`${API_URL}${endpoint}`, {
        username,
        password
      })

      if (res.data.success) {
        onLogin(res.data)
      } else {
        setError(res.data.message || 'Authentication failed')
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Connection error')
    } finally {
      setLoading(false)
    }
  }

  const handleQuickLogin = async () => {
    setLoading(true)
    setError('')
    try {
      const res = await axios.post(`${API_URL}/auth/login`, {
        username: 'Comander',
        password: 'admin'
      })
      if (res.data.success) {
        onLogin(res.data)
      }
    } catch (err) {
      setError('Quick login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container-compact">
      <div className="login-card-compact">
        <div className="login-header-compact">
          <div className="login-logo-compact">
            <Sparkles size={32} />
          </div>
          <h1 className="login-title-compact">LUCY OMNI</h1>
          <p className="login-subtitle-compact">v21.0 Omni Edition</p>
          <p className="login-description-compact">Next-Gen AI Assistant System</p>
        </div>

        <div className="login-tabs-compact">
          <button 
            className={!isRegister ? 'active' : ''} 
            onClick={() => setIsRegister(false)}
          >
            <LogIn size={18} /> Login
          </button>
          <button 
            className={isRegister ? 'active' : ''} 
            onClick={() => setIsRegister(true)}
          >
            <UserPlus size={18} /> Register
          </button>
        </div>

        <form onSubmit={handleSubmit} className="login-form-compact">
          <div className="input-group-compact">
            <User size={18} className="input-icon" />
            <input
              type="text"
              className="input-compact"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              autoComplete="username"
            />
          </div>

          <div className="input-group-compact">
            <Lock size={18} className="input-icon" />
            <input
              type="password"
              className="input-compact"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
            />
          </div>

          {error && (
            <div className="error-message-compact">
              ⚠️ {error}
            </div>
          )}

          <button 
            type="submit" 
            className="login-btn-compact"
            disabled={loading}
          >
            {loading ? 'Processing...' : (isRegister ? 'Create Account' : 'Sign In')} →
          </button>
        </form>

        <div className="quick-access-compact">
          <p>Quick Access:</p>
          <button onClick={handleQuickLogin} className="quick-user-compact">
            <User size={14} /> Use 'Comander'
          </button>
        </div>
      </div>
    </div>
  )
}