import { useState } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = "http://127.0.0.1:8000";

export default function WebPanel({ onSpeak }) {
  const [url, setUrl] = useState('')
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)
  const [tab, setTab] = useState('fetch')
  const [loading, setLoading] = useState(false)

  const fetchUrl = async () => {
    if (!url) return
    setLoading(true)
    try {
      const res = await axios.post(`${API_URL}/web/fetch`, { url })
      setResult(res.data)
      if (res.data.success && onSpeak) {
        const speakRes = await axios.post(`${API_URL}/voice/speak`, { text: `I've fetched ${res.data.title}` })
        if (speakRes.data.status === 'ready') {
          onSpeak(speakRes.data.file)
        }
      }
    } catch (error) { 
      setResult({ error: error.message }) 
    } finally { 
      setLoading(false) 
    }
  }

  const searchWeb = async () => {
    if (!query) return
    setLoading(true)
    try {
      const res = await axios.post(`${API_URL}/web/search`, { query })
      setResult(res.data)
      if (res.data.summary && onSpeak) {
        const speakRes = await axios.post(`${API_URL}/voice/speak`, { text: res.data.summary })
        if (speakRes.data.status === 'ready') {
          onSpeak(speakRes.data.file)
        }
      }
    } catch (error) { 
      setResult({ error: error.message }) 
    } finally { 
      setLoading(false) 
    }
  }

  return (
    <div className="web-panel">
      <div className="web-sidebar">
        <h3>🌐 Web</h3>
        <div style={{display: 'flex', gap: '10px', marginBottom: '20px'}}>
          <button onClick={() => setTab('fetch')} style={{flex: 1}}>Fetch</button>
          <button onClick={() => setTab('search')} style={{flex: 1}}>Search</button>
        </div>
        {tab === 'fetch' ? (
          <div>
            <input value={url} onChange={e => setUrl(e.target.value)} placeholder="https://example.com" style={{width: '100%', marginBottom: '10px', padding: '10px'}} />
            <button onClick={fetchUrl} disabled={loading} style={{width: '100%', padding: '10px'}}>{loading ? '...' : 'Fetch'}</button>
          </div>
        ) : (
          <div>
            <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search..." style={{width: '100%', marginBottom: '10px', padding: '10px'}} />
            <button onClick={searchWeb} disabled={loading} style={{width: '100%', padding: '10px'}}>{loading ? '...' : 'Search'}</button>
          </div>
        )}
      </div>
      <div className="web-main" style={{flex: 1, padding: '20px'}}>
        {loading && <p>Loading...</p>}
        {result && !loading && (
          <div>
            {result.error && <p style={{color: 'red'}}>Error: {result.error}</p>}
            {result.summary && <div><h4>Summary</h4><p>{result.summary}</p>{result.spoke && <p style={{color: '#00ff88'}}>🔊 Spoke!</p>}</div>}
            {result.content && <div><h4>{result.title}</h4><p>{result.content}</p>{result.spoke && <p style={{color: '#00ff88'}}>🔊 Spoke!</p>}</div>}
          </div>
        )}
        {!result && !loading && <p>Enter URL or search query</p>}
      </div>
    </div>
  )
}