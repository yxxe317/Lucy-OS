import React, { useState, useEffect } from 'react';
import './CognitiveDashboard.css';

const CognitiveDashboard = () => {
  const [config, setConfig] = useState(null);
  const [vramStatus, setVRAMStatus] = useState(null);
  const [hardwareHealth, setHardwareHealth] = useState(null);
  const [taskHistory, setTaskHistory] = useState([]);
  const [layersStatus, setLayersStatus] = useState({});
  const [voiceEngine, setVoiceEngine] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      // Fetch master config
      const configRes = await fetch('http://localhost:8000/settings/master');
      const configData = await configRes.json();
      setConfig(configData);

      // Fetch VRAM status
      const vramRes = await fetch('http://localhost:8000/settings/vram');
      const vramData = await vramRes.json();
      setVRAMStatus(vramData);

      // Fetch hardware health
      const healthRes = await fetch('http://localhost:8000/settings/hardware/health');
      const healthData = await healthRes.json();
      setHardwareHealth(healthData);

      // Fetch task history
      const historyRes = await fetch('http://localhost:8000/settings/tasks/history?limit=10');
      const historyData = await historyRes.json();
      setTaskHistory(historyData.tasks);

      // Fetch layers status
      const layersRes = await fetch('http://localhost:8000/settings/layers/status');
      const layersData = await layersRes.json();
      setLayersStatus(layersData);

      // Fetch voice engine status
      const voiceRes = await fetch('http://localhost:8000/settings/voice/engine');
      const voiceData = await voiceRes.json();
      setVoiceEngine(voiceData);

      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  };

  const refreshData = () => {
    fetchData();
  };

  const getHealthColor = (value, max) => {
    const percentage = (value / max) * 100;
    if (percentage < 70) return '#4caf50';
    if (percentage < 85) return '#ff9800';
    return '#f44336';
  };

  const getPriorityColor = (priority) => {
    if (priority >= 4) return '#ff5252';
    if (priority >= 3) return '#ffab40';
    if (priority >= 2) return '#ffd740';
    return '#4caf50';
  };

  if (loading) {
    return (
      <div className="cognitive-dashboard loading">
        <div className="loading-spinner"></div>
        <p>Loading Cognitive Dashboard...</p>
      </div>
    );
  }

  return (
    <div className="cognitive-dashboard">
      <div className="dashboard-header">
        <h1>Cognitive Dashboard</h1>
        <div className="dashboard-actions">
          <button onClick={refreshData} className="refresh-btn">
            🔄 Refresh
          </button>
        </div>
      </div>

      {/* Sovereign Status Banner */}
      {config && config.version && (
        <div className="sovereign-banner">
          <span className="sovereign-badge">👑 SOVEREIGN STATUS ACTIVE</span>
          <span className="version-badge">v{config.version}</span>
          <span className="autonomy-badge">Autonomy Level: {config.autonomy_level}/10</span>
        </div>
      )}

      {/* Main Grid */}
      <div className="dashboard-grid">
        {/* Master Configuration Card */}
        <div className="dashboard-card config-card">
          <div className="card-header">
            <h3>🎛️ Master Configuration</h3>
          </div>
          <div className="card-content">
            <div className="config-row">
              <span className="config-label">Autonomy Level:</span>
              <span className="config-value">{config.autonomy_level}/10</span>
            </div>
            <div className="config-row">
              <span className="config-label">VRAM Limit:</span>
              <span className="config-value">{config.max_vram_gb} GB</span>
            </div>
            <div className="config-row">
              <span className="config-label">Temp Threshold:</span>
              <span className="config-value">{config.max_temp_c}°C</span>
            </div>
            <div className="config-row">
              <span className="config-label">Fan Control:</span>
              <span className={`config-value ${config.fan_speed_auto ? 'active' : 'inactive'}`}>
                {config.fan_speed_auto ? 'Auto' : 'Manual'}
              </span>
            </div>
            <div className="config-row">
              <span className="config-label">Auction Enabled:</span>
              <span className={`config-value ${config.auction_enabled ? 'active' : 'inactive'}`}>
                {config.auction_enabled ? 'Yes' : 'No'}
              </span>
            </div>
          </div>
        </div>

        {/* VRAM Status Card */}
        <div className="dashboard-card vram-card">
          <div className="card-header">
            <h3>💾 VRAM Allocation</h3>
          </div>
          <div className="card-content">
            {vramStatus ? (
              <>
                <div className="vram-bar-container">
                  <div className="vram-bar">
                    <div 
                      className="vram-bar-fill" 
                      style={{ width: `${(vramStatus.allocated_gb / 6) * 100}%` }}
                    ></div>
                  </div>
                  <div className="vram-stats">
                    <span>Used: {vramStatus.allocated_gb.toFixed(1)} GB</span>
                    <span>Available: {vramStatus.available_gb.toFixed(1)} GB</span>
                  </div>
                </div>
                <div className="vram-message">{vramStatus.message}</div>
              </>
            ) : (
              <p className="no-data">No VRAM data available</p>
            )}
          </div>
        </div>

        {/* Hardware Health Card */}
        <div className="dashboard-card hardware-card">
          <div className="card-header">
            <h3>🖥️ Hardware Health</h3>
          </div>
          <div className="card-content">
            {hardwareHealth ? (
              <>
                <div className="health-metric">
                  <span className="health-label">GPU Temperature</span>
                  <span 
                    className="health-value" 
                    style={{ color: getHealthColor(hardwareHealth.gpu_temp, 100) }}
                  >
                    {hardwareHealth.gpu_temp.toFixed(1)}°C
                  </span>
                </div>
                <div className="health-metric">
                  <span className="health-label">Fan Speed</span>
                  <span className="health-value">{hardwareHealth.fan_speed}%</span>
                </div>
                <div className="health-metric">
                  <span className="health-label">Disk Temperature</span>
                  <span 
                    className="health-value" 
                    style={{ color: getHealthColor(hardwareHealth.disk_temp, 100) }}
                  >
                    {hardwareHealth.disk_temp.toFixed(1)}°C
                  </span>
                </div>
                <div className="health-metric">
                  <span className="health-label">Voltage</span>
                  <span className="health-value">{hardwareHealth.voltage}V</span>
                </div>
              </>
            ) : (
              <p className="no-data">No hardware data available</p>
            )}
          </div>
        </div>

        {/* Layers Status Card */}
        <div className="dashboard-card layers-card">
          <div className="card-header">
            <h3>📊 Routine Layers</h3>
          </div>
          <div className="card-content">
            {Object.entries(layersStatus).map(([layer, status]) => (
              <div key={layer} className="layer-row">
                <span className="layer-name">{layer.toUpperCase()}</span>
                <span className={`layer-status ${status.enabled ? 'enabled' : 'disabled'}`}>
                  {status.enabled ? '✓ Active' : '✗ Inactive'}
                </span>
                <span className="layer-count">{status.routines} routines</span>
              </div>
            ))}
          </div>
        </div>

        {/* Voice Engine Card */}
        <div className="dashboard-card voice-card">
          <div className="card-header">
            <h3>🎤 Voice Engine</h3>
          </div>
          <div className="card-content">
            {voiceEngine ? (
              <>
                <div className="voice-status">
                  <span className="engine-name">E2-TTS</span>
                  <span className={`engine-status ${voiceEngine.status === 'ready' ? 'ready' : 'error'}`}>
                    {voiceEngine.status}
                  </span>
                </div>
                <div className="voice-emotions">
                  <p className="emotion-label">Emotion Range:</p>
                  <div className="emotion-tags">
                    {voiceEngine.emotion_range.map((emotion, idx) => (
                      <span key={idx} className="emotion-tag">{emotion}</span>
                    ))}
                  </div>
                </div>
                <div className="voice-features">
                  <span className="feature">🌬️ Breath: {voiceEngine.breath_enabled ? 'On' : 'Off'}</span>
                  <span className="feature">⏸️ Pause: {voiceEngine.pause_enabled ? 'On' : 'Off'}</span>
                </div>
              </>
            ) : (
              <p className="no-data">No voice data available</p>
            )}
          </div>
        </div>

        {/* Task History Card */}
        <div className="dashboard-card history-card">
          <div className="card-header">
            <h3>📋 Recent Tasks</h3>
          </div>
          <div className="card-content">
            {taskHistory.length > 0 ? (
              <div className="task-list">
                {taskHistory.map((task, idx) => (
                  <div key={idx} className="task-item">
                    <div className="task-priority" style={{ backgroundColor: getPriorityColor(task.priority) }}>
                      {task.priority}
                    </div>
                    <div className="task-info">
                      <span className="task-name">{task.behavior_name}</span>
                      <span className="task-message">{task.message}</span>
                    </div>
                    <div className="task-meta">
                      <span className="task-type">{task.action_type}</span>
                      <span className="task-status">{task.status}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-data">No tasks recorded</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CognitiveDashboard;