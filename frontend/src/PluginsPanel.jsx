import { useState, useEffect } from 'react'
import axios from 'axios'
import { Puzzle, Power, Settings } from 'lucide-react'
import './App.css'

const API_URL = "http://127.0.0.1:8000";

export default function PluginsPanel() {
  const [plugins, setPlugins] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadPlugins()
  }, [])

  const loadPlugins = async () => {
    try {
      const res = await axios.get(`${API_URL}/plugins/list`)
      setPlugins(res.data.plugins || [])
    } catch (error) {
      console.error("Failed to load plugins")
    }
  }

  const togglePlugin = async (pluginId, currentStatus) => {
    setLoading(true)
    try {
      const endpoint = currentStatus ? '/plugins/disable' : '/plugins/enable'
      await axios.post(`${API_URL}${endpoint}`, { plugin_id: pluginId })
      loadPlugins()
    } catch (error) {
      alert("Failed to toggle plugin")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="plugins-panel">
      <div className="plugins-sidebar">
        <h3>🔌 Plugin Manager</h3>
        <p className="plugins-info">Enable or disable Lucy's capabilities</p>
      </div>

      <div className="plugins-main">
        <div className="plugins-grid">
          {plugins.map((plugin) => (
            <div key={plugin.id} className={`plugin-card ${plugin.enabled ? 'enabled' : 'disabled'}`}>
              <div className="plugin-header">
                <Puzzle size={24} color={plugin.enabled ? '#00ff88' : '#555'} />
                <h4>{plugin.name}</h4>
              </div>
              <p className="plugin-description">{plugin.description}</p>
              <div className="plugin-status">
                <span className={`status-badge ${plugin.enabled ? 'on' : 'off'}`}>
                  {plugin.enabled ? 'ON' : 'OFF'}
                </span>
              </div>
              <button 
                className={`toggle-btn ${plugin.enabled ? 'disable' : 'enable'}`}
                onClick={() => togglePlugin(plugin.id, plugin.enabled)}
                disabled={loading}
              >
                <Power size={16} /> {plugin.enabled ? 'Disable' : 'Enable'}
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}