import { useState } from 'react'
import { Shield, AlertTriangle, CheckCircle, Code, BookOpen, List, Lock } from 'lucide-react'
import './App.css'

export default function SecureDevPanel({ onSpeak }) {
  const [activeTab, setActiveTab] = useState('scanner')
  const [code, setCode] = useState('')
  const [scanResult, setScanResult] = useState(null)
  const [selectedRisk, setSelectedRisk] = useState(null)

  const scanCode = () => {
    // Simulated scan
    setScanResult({
      score: 85,
      findings: [
        { severity: 'high', title: 'SQL Injection Risk', line: 15, suggestion: 'Use parameterized queries' },
        { severity: 'medium', title: 'XSS Vulnerability', line: 42, suggestion: 'Sanitize user input' }
      ]
    })
  }

  const owaspTop10 = [
    { id: 'A01', title: 'Broken Access Control', severity: 'critical' },
    { id: 'A02', title: 'Cryptographic Failures', severity: 'high' },
    { id: 'A03', title: 'Injection', severity: 'critical' },
    { id: 'A04', title: 'Insecure Design', severity: 'high' },
    { id: 'A05', title: 'Security Misconfiguration', severity: 'medium' },
    { id: 'A06', title: 'Vulnerable Components', severity: 'high' },
    { id: 'A07', title: 'Authentication Failures', severity: 'critical' },
    { id: 'A08', title: 'Data Integrity Failures', severity: 'high' },
    { id: 'A09', title: 'Logging Failures', severity: 'medium' },
    { id: 'A10', title: 'Server-Side Request Forgery', severity: 'high' }
  ]

  return (
    <div className="secure-dev-panel-enhanced">
      {/* Enhanced Sidebar */}
      <div className="secure-dev-sidebar-enhanced">
        <h3><Lock size={24} /> Secure Dev Suite</h3>
        
        <div className="secure-dev-tabs-enhanced">
          <button className={activeTab === 'scanner' ? 'active' : ''} onClick={() => setActiveTab('scanner')}>
            <Code size={18} /> Code Scanner
          </button>
          <button className={activeTab === 'owasp' ? 'active' : ''} onClick={() => setActiveTab('owasp')}>
            <BookOpen size={18} /> OWASP Top 10
          </button>
          <button className={activeTab === 'checklists' ? 'active' : ''} onClick={() => setActiveTab('checklists')}>
            <List size={18} /> Checklists
          </button>
          <button className={activeTab === 'patterns' ? 'active' : ''} onClick={() => setActiveTab('patterns')}>
            <Shield size={18} /> Secure Patterns
          </button>
        </div>

        <div className="secure-dev-status-card-enhanced">
          <Shield size={48} color="#00ff88" />
          <h4>Security Status</h4>
          <p>Ready to Scan</p>
        </div>
      </div>

      {/* Enhanced Main Content */}
      <div className="secure-dev-main-enhanced">
        {activeTab === 'scanner' && (
          <div className="secure-dev-section-enhanced">
            <h4><Code size={24} /> Code Security Scanner</h4>
            
            <div className="code-editor-large">
              <textarea
                className="secure-dev-textarea-large"
                placeholder="# Paste your code here&#10;print(&quot;Hello World&quot;)"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                rows="15"
              />
              <button className="secure-dev-btn-large" onClick={scanCode}>
                <Shield size={20} /> Scan Code
              </button>
            </div>

            {scanResult && (
              <div className="scan-results-enhanced">
                <div className="score-display-large">
                  <h5>Security Score</h5>
                  <div className="score-bar-large">
                    <div className="score-fill-large" style={{ width: `${scanResult.score}%` }}></div>
                    <span>{scanResult.score}/100</span>
                  </div>
                </div>

                <div className="findings-list">
                  <h5>Security Findings</h5>
                  {scanResult.findings.map((finding, idx) => (
                    <div key={idx} className={`finding-item-large ${finding.severity}`}>
                      <AlertTriangle size={24} />
                      <div>
                        <strong>{finding.title}</strong>
                        <p>Line {finding.line}: {finding.suggestion}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'owasp' && (
          <div className="secure-dev-section-enhanced">
            <h4><BookOpen size={24} /> OWASP Top 10 Security Risks</h4>
            <div className="owasp-grid-enhanced">
              {owaspTop10.map((risk) => (
                <div key={risk.id} className={`owasp-card-enhanced ${risk.severity}`}>
                  <h5>{risk.id}: {risk.title}</h5>
                  <span className={`severity-badge ${risk.severity}`}>{risk.severity.toUpperCase()}</span>
                  <p>Click to view prevention strategies and best practices.</p>
                  <button className="owasp-btn" onClick={() => setSelectedRisk(risk)}>
                    View Details
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'checklists' && (
          <div className="secure-dev-section-enhanced">
            <h4><List size={24} /> Security Checklists</h4>
            <div className="checklist-container-enhanced">
              <div className="progress-bar-large">
                <div className="progress-fill-large" style={{ width: '65%' }}></div>
                <span>65% Complete</span>
              </div>
              <div className="checklist-items-enhanced">
                {['Input Validation', 'Authentication', 'Session Management', 'Error Handling', 'Logging'].map((item, idx) => (
                  <label key={idx} className="checklist-item-enhanced">
                    <input type="checkbox" defaultChecked={idx < 3} />
                    <span>{item}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'patterns' && (
          <div className="secure-dev-section-enhanced">
            <h4><Shield size={24} /> Secure Coding Patterns</h4>
            <div className="pattern-buttons-enhanced">
              <button className="pattern-btn-enhanced">Authentication</button>
              <button className="pattern-btn-enhanced">Authorization</button>
              <button className="pattern-btn-enhanced">Data Validation</button>
              <button className="pattern-btn-enhanced">Encryption</button>
            </div>
            <div className="pattern-details-enhanced">
              <h5>Secure Authentication Pattern</h5>
              <div className="recommendations-enhanced">
                <h6>Recommendations:</h6>
                <ul>
                  <li>Use multi-factor authentication (MFA)</li>
                  <li>Implement password complexity requirements</li>
                  <li>Use secure session tokens</li>
                  <li>Implement account lockout after failed attempts</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}