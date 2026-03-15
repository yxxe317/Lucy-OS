import { useState, useEffect } from 'react'
import axios from 'axios'
import { Search, Database, Trash2, Eye } from 'lucide-react'
import './App.css'

const API_URL = "http://127.0.0.1:8000";

export default function MemoryPanel() {
  const [stats, setStats] = useState(null)
  const [memories, setMemories] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadStats()
    loadMemories()
  }, [])

  const loadStats = async () => {
    try {
      const res = await axios.get(`${API_URL}/memory/stats`)
      setStats(res.data)
    } catch (error) {
      console.error("Failed to load stats")
    }
  }

  const loadMemories = async () => {
    try {
      const res = await axios.get(`${API_URL}/memory/all?limit=50`)
      setMemories(res.data.memories || [])
    } catch (error) {
      console.error("Failed to load memories")
    }
  }

  const searchMemories = async () => {
    if (!searchQuery.trim()) return
    
    setLoading(true)
    try {
      const res = await axios.get(`${API_URL}/memory/search?q=${encodeURIComponent(searchQuery)}&limit=10`)
      setSearchResults(res.data.memories || [])
    } catch (error) {
      console.error("Search failed")
    } finally {
      setLoading(false)
    }
  }

  const deleteMemory = async (id) => {
    if (!confirm('Delete this memory?')) return
    
    try {
      await axios.delete(`${API_URL}/memory/${id}`)
      loadMemories()
      loadStats()
    } catch (error) {
      alert("Failed to delete")
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') searchMemories()
  }

  return (
    <div className="memory-panel">
      <div className="memory-sidebar">
        <h3>💾 Memory Stats</h3>
        
        <div className="stat-card">
          <Database size={24} color="#00f0ff" />
          <div>
            <div className="stat-value">{stats?.total_memories || 0}</div>
            <div className="stat-label">Total Memories</div>
          </div>
        </div>

        <div className="search-box">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Search memories..."
            className="search-input"
          />
          <button onClick={searchMemories} disabled={loading}>
            <Search size={16} />
          </button>
        </div>
      </div>

      <div className="memory-main">
        {searchResults.length > 0 ? (
          <>
            <h3>🔍 Search Results ({searchResults.length})</h3>
            <div className="memories-list">
              {searchResults.map((mem, idx) => (
                <div key={idx} className="memory-item">
                  <div className="memory-content">{mem.content}</div>
                  <div className="memory-meta">
                    <span>{mem.metadata?.timestamp?.split('T')[0]}</span>
                    <span className="distance">Relevance: {(1 - mem.distance).toFixed(2)}</span>
                  </div>
                </div>
              ))}
            </div>
          </>
        ) : memories.length > 0 ? (
          <>
            <h3>📚 Recent Memories ({memories.length})</h3>
            <div className="memories-list">
              {memories.map((mem, idx) => (
                <div key={idx} className="memory-item">
                  <div className="memory-content">{mem.content}</div>
                  <div className="memory-meta">
                    <span>{mem.metadata?.timestamp?.split('T')[0]}</span>
                    <button 
                      className="delete-btn"
                      onClick={() => deleteMemory(mem.metadata?.id)}
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </>
        ) : (
          <div className="no-memories">
            <Database size={64} color="#555" />
            <p>No memories yet</p>
            <p style={{fontSize: '0.8rem', color: '#444'}}>Start chatting to build memory!</p>
          </div>
        )}
      </div>
    </div>
  )
}