import { useState, useEffect } from 'react'
import axios from 'axios'
import { Shield, Activity, AlertTriangle, Users, FileText, Award, Clock, CheckCircle } from 'lucide-react'
import './App.css'

const API_URL = "http://127.0.0.1:8000";

export default function SOCPanel({ onSpeak }) {
  const [dashboard, setDashboard] = useState(null)
  const [scenarios, setScenarios] = useState([])
  const [incidents, setIncidents] = useState([])
  const [certifications, setCertifications] = useState(null)
  const [activeTab, setActiveTab] = useState('dashboard')
  const [selectedScenario, setSelectedScenario] = useState(null)
  const [activeIncident, setActiveIncident] = useState(null)
  const [teamMembers, setTeamMembers] = useState(['Analyst-1', 'Responder-1'])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadDashboard()
    loadScenarios()
    loadIncidents()
  }, [])

  const loadDashboard = async () => {
    try {
      const res = await axios.get(`${API_URL}/soc/dashboard`)
      setDashboard(res.data)
    } catch (err) { console.error('Failed to load dashboard') }
  }

  const loadScenarios = async () => {
    try {
      const res = await axios.get(`${API_URL}/soc/scenarios`)
      setScenarios(res.data.scenarios || [])
    } catch (err) { console.error('Failed to load scenarios') }
  }

  const loadIncidents = async () => {
    try {
      const res = await axios.get(`${API_URL}/soc/incidents`)
      setIncidents(res.data.incidents || [])
    } catch (err) { console.error('Failed to load incidents') }
  }

  const startScenario = async (scenario) => {
    setLoading(true)
    try {
      const res = await axios.post(`${API_URL}/soc/scenario/start`, {
        scenario_id: scenario.id,
        team_members: teamMembers
      })
      if (res.data.success) {
        setActiveIncident(res.data)
        alert(`✅ Scenario started: ${scenario.name}`)
        loadIncidents()
      }
    } catch (err) {
      alert('Failed to start: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const addTimelineEvent = async (eventId, eventText) => {
    try {
      await axios.post(`${API_URL}/soc/timeline/add`, {
        incident_id: eventId,
        event: eventText
      })
      alert('✅ Event added to timeline')
    } catch (err) {
      alert('Failed: ' + err.message)
    }
  }

  const completeIncident = async (incidentId) => {
    const score = prompt('Enter score (0-100):', '80')
    const feedback = prompt('Enter feedback (comma-separated):', 'Good response, Improve documentation')
    
    try {
      await axios.post(`${API_URL}/soc/incident/complete`, {
        incident_id: incidentId,
        score: parseInt(score),
        feedback: feedback.split(',').map(f => f.trim())
      })
      alert('✅ Incident completed! Report generated.')
      setActiveIncident(null)
      loadDashboard()
      loadIncidents()
    } catch (err) {
      alert('Failed: ' + err.message)
    }
  }

  return (
    <div className="soc-panel">
      <div className="soc-sidebar">
        <h3>🎯 SOC Simulator</h3>
        
        <div className="soc-tabs">
          <button className={activeTab === 'dashboard' ? 'active' : ''} onClick={() => setActiveTab('dashboard')}>
            <Activity size={16} /> Dashboard
          </button>
          <button className={activeTab === 'scenarios' ? 'active' : ''} onClick={() => { setActiveTab('scenarios'); loadScenarios(); }}>
            <FileText size={16} /> Scenarios
          </button>
          <button className={activeTab === 'incidents' ? 'active' : ''} onClick={() => { setActiveTab('incidents'); loadIncidents(); }}>
            <AlertTriangle size={16} /> Incidents
          </button>
          <button className={activeTab === 'mitre' ? 'active' : ''} onClick={() => setActiveTab('mitre')}>
            <Shield size={16} /> MITRE ATT&CK
          </button>
          <button className={activeTab === 'certs' ? 'active' : ''} onClick={() => setActiveTab('certs')}>
            <Award size={16} /> Certifications
          </button>
        </div>

        <div className="soc-status-card">
          <Shield size={40} color="#00ff88" />
          <h4>SOC Status</h4>
          <p className="status-good">Operational</p>
        </div>
      </div>

      <div className="soc-main">
        {activeTab === 'dashboard' && dashboard && (
          <div className="soc-dashboard">
            <h4>🛡️ SOC Operations Dashboard</h4>
            
            <div className="soc-metrics-grid">
              <div className="soc-metric-card">
                <AlertTriangle size={32} color="#ffaa00" />
                <h3>{dashboard.active_incidents}</h3>
                <p>Active Incidents</p>
              </div>
              <div className="soc-metric-card">
                <CheckCircle size={32} color="#00ff88" />
                <h3>{dashboard.resolved_incidents}</h3>
                <p>Resolved</p>
              </div>
              <div className="soc-metric-card">
                <Clock size={32} color="#00f0ff" />
                <h3>{dashboard.mttr_minutes}m</h3>
                <p>MTTR</p>
              </div>
              <div className="soc-metric-card">
                <Users size={32} color="#bc13fe" />
                <h3>{dashboard.team_readiness}%</h3>
                <p>Team Readiness</p>
              </div>
            </div>

            <div className="soc-chart-placeholder">
              <h5>Incident Trend (30 Days)</h5>
              <div className="chart-bars">
                {[...Array(7)].map((_, i) => (
                  <div key={i} className="chart-bar" style={{height: `${Math.random() * 80 + 20}%`}}></div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'scenarios' && (
          <div className="soc-section">
            <h4>📋 Training Scenarios</h4>
            <div className="scenario-list">
              {scenarios.map((scenario) => (
                <div key={scenario.id} className="scenario-card">
                  <div className="scenario-header">
                    <h5>{scenario.name}</h5>
                    <span className={`difficulty-badge ${scenario.difficulty}`}>{scenario.difficulty}</span>
                  </div>
                  <p>{scenario.description}</p>
                  <div className="scenario-details">
                    <span>⏱️ {scenario.duration_minutes} min</span>
                    <span>👥 {scenario.roles_required.join(', ')}</span>
                    <span>🎯 {scenario.objectives.length} objectives</span>
                  </div>
                  <button 
                    onClick={() => startScenario(scenario)} 
                    disabled={loading}
                    className="soc-btn"
                  >
                    Start Scenario
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'incidents' && (
          <div className="soc-section">
            <h4>🚨 Active Incidents</h4>
            <div className="incidents-list">
              {incidents.filter(i => i.status === 'active').map((incident) => (
                <div key={incident.id} className="incident-card active">
                  <h5>{incident.scenario_name}</h5>
                  <p>Started: {incident.started_at?.split('T')[0]}</p>
                  <p>Team: {incident.team_members?.join(', ')}</p>
                  <p>Actions: {incident.actions_taken?.length || 0}</p>
                  <p>Timeline: {incident.timeline?.length || 0} events</p>
                  <div className="incident-actions">
                    <input 
                      type="text" 
                      placeholder="Add timeline event..."
                      onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                          addTimelineEvent(incident.id, e.target.value)
                          e.target.value = ''
                        }
                      }}
                      className="incident-input"
                    />
                    <button onClick={() => completeIncident(incident.id)} className="complete-btn">
                      Complete & Report
                    </button>
                  </div>
                </div>
              ))}
              {incidents.filter(i => i.status === 'active').length === 0 && (
                <p className="empty">No active incidents. Start a scenario!</p>
              )}
            </div>
          </div>
        )}

        {activeTab === 'mitre' && (
          <div className="soc-section">
            <h4>🎯 MITRE ATT&CK Framework</h4>
            <p>Map scenarios to real-world adversary techniques</p>
            <div className="mitre-grid">
              <div className="mitre-card">
                <h5>T1566.001 - Phishing</h5>
                <p>Tactic: Initial Access</p>
                <p>Technique: Spearphishing Attachment</p>
              </div>
              <div className="mitre-card">
                <h5>T1486 - Data Encrypted</h5>
                <p>Tactic: Impact</p>
                <p>Technique: Ransomware</p>
              </div>
              <div className="mitre-card">
                <h5>T1078 - Valid Accounts</h5>
                <p>Tactic: Persistence</p>
                <p>Technique: Insider Threat</p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'certs' && (
          <div className="soc-section">
            <h4>🏆 Team Certifications</h4>
            <div className="cert-list">
              <div className="cert-card">
                <Award size={32} color="#ffd700" />
                <h5>SOC Analyst Level 1</h5>
                <p>Complete 5 beginner scenarios</p>
                <div className="progress-bar">
                  <div className="progress-fill" style={{width: '40%'}}></div>
                </div>
                <span>2/5 Completed</span>
              </div>
              <div className="cert-card">
                <Award size={32} color="#c0c0c0" />
                <h5>SOC Responder Level 2</h5>
                <p>Complete 10 intermediate scenarios</p>
                <div className="progress-bar">
                  <div className="progress-fill" style={{width: '20%'}}></div>
                </div>
                <span>2/10 Completed</span>
              </div>
              <div className="cert-card">
                <Award size={32} color="#cd7f32" />
                <h5>SOC Manager Level 3</h5>
                <p>Complete 15 advanced scenarios</p>
                <div className="progress-bar">
                  <div className="progress-fill" style={{width: '10%'}}></div>
                </div>
                <span>1/15 Completed</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}