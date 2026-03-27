import React, { useState, useEffect } from 'react';
import './Dashboard.css';

const Dashboard = () => {
  const [systemStatus, setSystemStatus] = useState({
    isRunning: false,
    uptime: 0,
    memory: 0,
    cpu: 0,
    temperature: 0
  });

  const [securityStatus, setSecurityStatus] = useState({
    modelTrained: false,
    anomalyThreshold: 80,
    verificationCount: 0,
    consecutiveAnomalies: 0
  });

  const [activeTab, setActiveTab] = useState('overview');
  const [backendUrl, setBackendUrl] = useState('http://192.168.1.2:8000');

  useEffect(() => {
    // Fetch system status from backend
    const fetchStatus = async () => {
      try {
        const response = await fetch(`${backendUrl}/status`);
        if (response.ok) {
          const data = await response.json();
          setSecurityStatus(data);
        }
      } catch (error) {
        console.error('Failed to fetch security status:', error);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);

    return () => clearInterval(interval);
  }, [backendUrl]);

  const getStatusColor = (status) => {
    if (status === 'none') return '#4CAF50';
    if (status === 'warning') return '#FF9800';
    return '#f44336';
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'none': return 'Normal';
      case 'warning': return 'Warning';
      case 'lockdown': return 'LOCKDOWN';
      default: return 'Unknown';
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>🤖 Lucy OS Dashboard</h1>
        <div className="header-info">
          <span className="status-indicator">
            <span className="indicator-dot"></span>
            System Running
          </span>
        </div>
      </div>

      <div className="dashboard-tabs">
        <button
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`tab ${activeTab === 'security' ? 'active' : ''}`}
          onClick={() => setActiveTab('security')}
        >
          Security
        </button>
        <button
          className={`tab ${activeTab === 'biometric' ? 'active' : ''}`}
          onClick={() => setActiveTab('biometric')}
        >
          Biometric
        </button>
        <button
          className={`tab ${activeTab === 'settings' ? 'active' : ''}`}
          onClick={() => setActiveTab('settings')}
        >
          Settings
        </button>
      </div>

      <div className="dashboard-content">
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="tab-content">
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon">🤖</div>
                <div className="stat-info">
                  <div className="stat-value">Active</div>
                  <div className="stat-label">System Status</div>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">🔐</div>
                <div className="stat-info">
                  <div className="stat-value">{securityStatus.modelTrained ? 'Enabled' : 'Disabled'}</div>
                  <div className="stat-label">Biometric Security</div>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">📊</div>
                <div className="stat-info">
                  <div className="stat-value">{securityStatus.verificationCount}</div>
                  <div className="stat-label">Verifications</div>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">⚠️</div>
                <div className="stat-info">
                  <div className="stat-value">{securityStatus.consecutiveAnomalies}</div>
                  <div className="stat-label">Anomalies</div>
                </div>
              </div>
            </div>

            <div className="system-info">
              <h3>System Information</h3>
              <div className="info-grid">
                <div className="info-item">
                  <span className="info-label">Backend URL</span>
                  <span className="info-value">{backendUrl}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Security Threshold</span>
                  <span className="info-value">{securityStatus.anomalyThreshold}%</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Security Tab */}
        {activeTab === 'security' && (
          <div className="tab-content">
            <div className="security-status">
              <h3>Security Status</h3>
              <div className="status-card">
                <div className="status-header">
                  <span className="status-title">Biometric Authentication</span>
                  <span
                    className="status-badge"
                    style={{ backgroundColor: getStatusColor(securityStatus.consecutiveAnomalies > 0 ? 'lockdown' : 'none') }}
                  >
                    {getStatusText(securityStatus.consecutiveAnomalies > 0 ? 'lockdown' : 'none')}
                  </span>
                </div>
                <div className="status-details">
                  <div className="detail-row">
                    <span className="detail-label">Model Status</span>
                    <span className="detail-value">{securityStatus.modelTrained ? 'Trained ✓' : 'Not Trained'}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Verification Count</span>
                    <span className="detail-value">{securityStatus.verificationCount}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Anomaly Threshold</span>
                    <span className="detail-value">{securityStatus.anomalyThreshold}%</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Consecutive Anomalies</span>
                    <span className="detail-value" style={{ color: securityStatus.consecutiveAnomalies > 0 ? '#f44336' : '#4CAF50' }}>
                      {securityStatus.consecutiveAnomalies}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div className="security-actions">
              <h3>Security Actions</h3>
              <div className="action-buttons">
                <button className="action-btn primary">
                  <span className="btn-icon">🔐</span>
                  Calibrate Biometric
                </button>
                <button className="action-btn danger">
                  <span className="btn-icon">🚨</span>
                  Trigger Lockdown
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Biometric Tab */}
        {activeTab === 'biometric' && (
          <div className="tab-content">
            <div className="biometric-section">
              <h3>Biometric Calibration</h3>
              <p>Calibrate your typing rhythm for biometric authentication.</p>
              <button className="calibrate-btn" onClick={() => window.location.href = '/biometric'}>
                Start Calibration
              </button>
            </div>

            <div className="biometric-info">
              <h3>How It Works</h3>
              <ul>
                <li>Complete 10 rounds of typing the golden paragraph</li>
                <li>Your unique typing rhythm is captured</li>
                <li>A One-Class SVM model is trained on your data</li>
                <li>Future typing is verified against your biometric signature</li>
                <li>Abnormal typing patterns trigger security alerts</li>
              </ul>
            </div>
          </div>
        )}

        {/* Settings Tab */}
        {activeTab === 'settings' && (
          <div className="tab-content">
            <div className="settings-section">
              <h3>Settings</h3>
              
              <div className="setting-item">
                <label className="setting-label">Backend URL</label>
                <input
                  type="text"
                  value={backendUrl}
                  onChange={(e) => setBackendUrl(e.target.value)}
                  className="setting-input"
                />
              </div>

              <div className="setting-item">
                <label className="setting-label">Anomaly Threshold (%)</label>
                <input
                  type="number"
                  value={securityStatus.anomalyThreshold}
                  onChange={(e) => {
                    setSecurityStatus(prev => ({
                      ...prev,
                      anomalyThreshold: parseInt(e.target.value) || 80
                    }));
                  }}
                  className="setting-input"
                />
              </div>

              <div className="setting-item">
                <label className="setting-label">Calibration Rounds</label>
                <input
                  type="number"
                  value={10}
                  readOnly
                  className="setting-input"
                />
              </div>
            </div>

            <div className="settings-actions">
              <button className="save-btn">Save Settings</button>
              <button className="reset-btn">Reset to Defaults</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;