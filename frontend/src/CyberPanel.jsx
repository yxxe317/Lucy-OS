import { useState } from 'react'
import axios from 'axios'
import { Shield, AlertTriangle, CheckCircle, FileText, Lock, BookOpen, Activity } from 'lucide-react'
import './App.css'

const API_URL = "http://127.0.0.1:8000";

export default function CyberPanel({ onSpeak }) {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [logContent, setLogContent] = useState('')
  const [logAnalysis, setLogAnalysis] = useState(null)
  const [password, setPassword] = useState('')
  const [passwordResult, setPasswordResult] = useState(null)
  const [incidentType, setIncidentType] = useState('malware_detection')
  const [playbook, setPlaybook] = useState(null)
  const [loading, setLoading] = useState(false)

  const analyzeLogs = async () => {
    setLoading(true)
    try {
      const res = await axios.post(`${API_URL}/cyber/analyze-logs`, { log_content: logContent })
      setLogAnalysis(res.data)
      if (onSpeak && res.data.findings_count > 0) {
        onSpeak(`Found ${res.data.findings_count} potential security issues in logs.`)
      }
    } catch (err) {
      alert('Analysis failed: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const checkPasswordStrength = async () => {
    try {
      const res = await axios.post(`${API_URL}/cyber/check-password`, { password })
      setPasswordResult(res.data)
    } catch (err) {
      alert('Check failed')
    }
  }

  const generatePlaybook = async () => {
    setLoading(true)
    try {
      const res = await axios.post(`${API_URL}/cyber/incident-playbook`, { incident_type: incidentType })
      setPlaybook(res.data.playbook)
    } catch (err) {
      alert('Failed to generate playbook')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="cyber-panel">
      <div className="cyber-sidebar">
        <h3>🛡️ Cyber Command</h3>
        
        <div className="cyber-tabs">
          <button className={activeTab === 'dashboard' ? 'active' : ''} onClick={() => setActiveTab('dashboard')}>
            <Activity size={16} /> Dashboard
          </button>
          <button className={activeTab === 'logs' ? 'active' : ''} onClick={() => setActiveTab('logs')}>
            <FileText size={16} /> Log Analyzer
          </button>
          <button className={activeTab === 'password' ? 'active' : ''} onClick={() => setActiveTab('password')}>
            <Lock size={16} /> Password Check
          </button>
          <button className={activeTab === 'incident' ? 'active' : ''} onClick={() => setActiveTab('incident')}>
            <AlertTriangle size={16} /> Incident Response
          </button>
          <button className={activeTab === 'training' ? 'active' : ''} onClick={() => setActiveTab('training')}>
            <BookOpen size={16} /> Training
          </button>
        </div>

        <div className="cyber-status-card">
          <Shield size={40} color="#00ff88" />
          <h4>Defense Status</h4>
          <p className="status-good">All Systems Secure</p>
        </div>
      </div>

      <div className="cyber-main">
        {activeTab === 'dashboard' && (
          <div className="cyber-dashboard">
            <h4>🛡️ Security Overview</h4>
            <div className="cyber-stats-grid">
              <div className="cyber-stat-card">
                <Shield size={32} color="#00f0ff" />
                <h3>Secure</h3>
                <p>System Status</p>
              </div>
              <div className="cyber-stat-card">
                <AlertTriangle size={32} color="#ffaa00" />
                <h3>0</h3>
                <p>Active Threats</p>
              </div>
              <div className="cyber-stat-card">
                <CheckCircle size={32} color="#00ff88" />
                <h3>Ready</h3>
                <p>Defense Modules</p>
              </div>
            </div>
            <p className="cyber-disclaimer">🔒 Defensive Security Tools Only - Educational Purpose</p>
          </div>
        )}

        {activeTab === 'logs' && (
          <div className="cyber-section">
            <h4>📄 Log Analyzer</h4>
            <textarea
              value={logContent}
              onChange={(e) => setLogContent(e.target.value)}
              placeholder="Paste log content here for analysis..."
              className="cyber-textarea"
            />
            <button onClick={analyzeLogs} disabled={loading} className="cyber-btn">
              Analyze Logs
            </button>
            
            {logAnalysis && (
              <div className="cyber-results">
                <h5>Analysis Results:</h5>
                <p>Risk Score: {logAnalysis.risk_score}/100</p>
                <p>Findings: {logAnalysis.findings_count}</p>
                {logAnalysis.findings?.map((f, i) => (
                  <div key={i} className="cyber-finding">
                    <span className={`severity-${f.severity}`}>{f.severity.toUpperCase()}</span>
                    <span>{f.threat}</span>
                    <span className="recommendation">{f.recommendation}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'password' && (
          <div className="cyber-section">
            <h4>🔒 Password Strength Evaluator</h4>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password to check"
              className="cyber-input"
            />
            <button onClick={checkPasswordStrength} className="cyber-btn">
              Check Strength
            </button>
            
            {passwordResult && (
              <div className="cyber-results">
                <h5>Strength: {passwordResult.strength}</h5>
                <p>Score: {passwordResult.score}/100</p>
                <ul>
                  {passwordResult.feedback.map((f, i) => (
                    <li key={i}>{f}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {activeTab === 'incident' && (
          <div className="cyber-section">
            <h4>🚨 Incident Response Playbook</h4>
            <select
              value={incidentType}
              onChange={(e) => setIncidentType(e.target.value)}
              className="cyber-select"
            >
              <option value="malware_detection">Malware Detection</option>
              <option value="phishing_attack">Phishing Attack</option>
              <option value="data_breach">Data Breach</option>
            </select>
            <button onClick={generatePlaybook} disabled={loading} className="cyber-btn">
              Generate Playbook
            </button>
            
            {playbook && (
              <div className="cyber-results">
                <h5>Response Steps:</h5>
                <ol>
                  {playbook.steps.map((step, i) => (
                    <li key={i}>{step}</li>
                  ))}
                </ol>
                <h5>Recommended Tools:</h5>
                <p>{playbook.tools.join(', ')}</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'training' && (
          <div className="cyber-section">
            <h4>📚 Cybersecurity Training</h4>
            <p>Select a topic to learn:</p>
            <div className="training-topics">
              <div className="training-topic">Network Security Fundamentals</div>
              <div className="training-topic">Secure Coding Practices</div>
              <div className="training-topic">Incident Response Procedures</div>
              <div className="training-topic">Phishing Awareness</div>
              <div className="training-topic">Encryption Basics</div>
            </div>
            <p className="cyber-disclaimer">⚠️ Educational Purpose Only - Do not use on systems you don't own</p>
          </div>
        )}
      </div>
    </div>
  )
}