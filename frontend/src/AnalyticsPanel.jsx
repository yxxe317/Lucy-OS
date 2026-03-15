import { useState, useEffect } from 'react'
import axios from 'axios'
import { Shield, AlertTriangle, CheckCircle, Activity, FileText, TrendingUp } from 'lucide-react'
import './App.css'

const API_URL = "http://127.0.0.1:8000";

export default function AnalyticsPanel({ onSpeak }) {
  const [dashboard, setDashboard] = useState(null)
  const [alerts, setAlerts] = useState([])
  const [compliance, setCompliance] = useState(null)
  const [activeTab, setActiveTab] = useState('overview')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadDashboard()
    loadAlerts()
    loadCompliance()
  }, [])

  const loadDashboard = async () => {
    try {
      const res = await axios.get(`${API_URL}/security/dashboard`)
      setDashboard(res.data)
    } catch (err) { console.error('Failed to load dashboard') }
  }

  const loadAlerts = async () => {
    try {
      const res = await axios.get(`${API_URL}/security/alerts`)
      setAlerts(res.data.alerts || [])
    } catch (err) { console.error('Failed to load alerts') }
  }

  const loadCompliance = async () => {
    try {
      const res = await axios.get(`${API_URL}/security/compliance`)
      setCompliance(res.data)
    } catch (err) { console.error('Failed to load compliance') }
  }

  const createAlert = async () => {
    const severity = prompt('Severity (low/medium/high/critical):', 'medium')
    const description = prompt('Description:')
    if (!severity || !description) return
    
    try {
      await axios.post(`${API_URL}/security/alert`, { severity, description })
      alert('✅ Alert created')
      loadAlerts()
      loadDashboard()
    } catch (err) {
      alert('Failed: ' + err.message)
    }
  }

  const resolveAlert = async (id) => {
    try {
      await axios.post(`${API_URL}/security/alert/${id}/resolve`)
      alert('✅ Alert resolved')
      loadAlerts()
      loadDashboard()
    } catch (err) {
      alert('Failed: ' + err.message)
    }
  }

  return (
    <div className="analytics-panel">
      <div className="analytics-sidebar">
        <h3>📊 Security Analytics</h3>
        
        <div className="analytics-tabs">
          <button className={activeTab === 'overview' ? 'active' : ''} onClick={() => setActiveTab('overview')}>
            <Activity size={16} /> Overview
          </button>
          <button className={activeTab === 'alerts' ? 'active' : ''} onClick={() => setActiveTab('alerts')}>
            <AlertTriangle size={16} /> Alerts
          </button>
          <button className={activeTab === 'compliance' ? 'active' : ''} onClick={() => setActiveTab('compliance')}>
            <FileText size={16} /> Compliance
          </button>
        </div>

        <div className="analytics-status-card">
          <Shield size={40} color={dashboard?.risk_score < 30 ? '#00ff88' : '#ffaa00'} />
          <h4>Threat Level</h4>
          <p className={dashboard?.risk_score < 30 ? 'status-good' : 'status-warning'}>
            {dashboard?.risk_score < 30 ? 'LOW' : 'ELEVATED'}
          </p>
        </div>
      </div>

      <div className="analytics-main">
        {activeTab === 'overview' && dashboard && (
          <div className="analytics-dashboard">
            <h4>🛡️ Security Overview</h4>
            
            <div className="analytics-metrics-grid">
              <div className="analytics-metric-card">
                <Shield size={32} color="#00f0ff" />
                <h3>{dashboard.risk_score}</h3>
                <p>Risk Score (0-100)</p>
              </div>
              <div className="analytics-metric-card">
                <AlertTriangle size={32} color="#ffaa00" />
                <h3>{dashboard.alerts_unresolved}</h3>
                <p>Unresolved Alerts</p>
              </div>
              <div className="analytics-metric-card">
                <CheckCircle size={32} color="#00ff88" />
                <h3>{dashboard.compliance_score}%</h3>
                <p>Compliance Score</p>
              </div>
              <div className="analytics-metric-card">
                <TrendingUp size={32} color="#bc13fe" />
                <h3>{dashboard.logs_processed}</h3>
                <p>Logs Processed</p>
              </div>
            </div>

            {/* Simple Timeline Visualization */}
            <div className="analytics-timeline">
              <h5>Risk Trend (7 Days)</h5>
              <div className="timeline-bars">
                {dashboard.timeline.map((day, i) => (
                  <div key={i} className="timeline-bar-container">
                    <div 
                      className="timeline-bar" 
                      style={{height: `${day.risk}%`, background: day.risk > 40 ? '#ff4444' : '#00ff88'}}
                    ></div>
                    <span className="timeline-label">{day.date.split('-')[2]}</span>
                  </div>
                ))}
              </div>
            </div>

            <button onClick={createAlert} className="analytics-btn">
              + Create Manual Alert
            </button>
          </div>
        )}

        {activeTab === 'alerts' && (
          <div className="analytics-section">
            <h4>🚨 Security Alerts</h4>
            <div className="alerts-list">
              {alerts.map((alert) => (
                <div key={alert.id} className={`alert-item ${alert.status}`}>
                  <div className="alert-header">
                    <span className={`severity-badge ${alert.severity}`}>{alert.severity.toUpperCase()}</span>
                    <span className="alert-status">{alert.status}</span>
                  </div>
                  <p className="alert-description">{alert.description}</p>
                  <div className="alert-meta">
                    <span>{alert.created_at?.split('T')[0]}</span>
                    {alert.status === 'open' && (
                      <button onClick={() => resolveAlert(alert.id)} className="resolve-btn">Resolve</button>
                    )}
                  </div>
                </div>
              ))}
              {alerts.length === 0 && <p className="empty">No alerts</p>}
            </div>
          </div>
        )}

        {activeTab === 'compliance' && compliance && (
          <div className="analytics-section">
            <h4>📋 Compliance Report ({compliance.framework})</h4>
            <div className="compliance-score">
              <div className="score-circle">
                <svg viewBox="0 0 36 36">
                  <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#333" strokeWidth="3"/>
                  <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#00ff88" strokeWidth="3" strokeDasharray={`${compliance.score}, 100`}/>
                </svg>
                <div className="score-number">{compliance.score}%</div>
              </div>
            </div>
            
            <div className="controls-list">
              {compliance.controls.map((control, i) => (
                <div key={i} className="control-item">
                  <span className="control-id">{control.id}</span>
                  <span className="control-name">{control.name}</span>
                  <span className={`control-status ${control.status}`}>{control.status}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}