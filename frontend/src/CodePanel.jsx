import { useState, useEffect } from 'react'
import axios from 'axios'
import { Play, FileText, Save, Folder, Calculator, Code, Copy } from 'lucide-react'
import './App.css'

const API_URL = "http://127.0.0.1:8000";

export default function CodePanel({ onSpeak }) {
  const [code, setCode] = useState('# Write your Python code here\nprint("Hello from Lucy!")')
  const [output, setOutput] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('editor')
  const [files, setFiles] = useState([])
  const [templates, setTemplates] = useState([])
  const [calcExpression, setCalcExpression] = useState('')
  const [calcResult, setCalcResult] = useState('')

  useEffect(() => {
    loadFiles()
    loadTemplates()
  }, [])

  const loadFiles = async () => {
    try {
      const res = await axios.get(`${API_URL}/code/files`)
      if (res.data.success) setFiles(res.data.files || [])
    } catch (err) { console.error('Failed to load files') }
  }

  const loadTemplates = async () => {
    try {
      const res = await axios.get(`${API_URL}/code/templates`)
      setTemplates(res.data.templates || [])
    } catch (err) { console.error('Failed to load templates') }
  }

  const executeCode = async () => {
    setLoading(true)
    setError('')
    setOutput('')
    try {
      const res = await axios.post(`${API_URL}/code/execute`, { code, language: 'python' })
      if (res.data.success) {
        setOutput(res.data.output || res.data.result || 'Executed successfully!')
        if (onSpeak && res.data.output) {
          onSpeak(`Code executed. ${res.data.output?.substring(0, 100)}`)
        }
      } else {
        setError(res.data.error || 'Execution failed')
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message)
    } finally {
      setLoading(false)
    }
  }

  const loadTemplate = (templateCode) => {
    setCode(templateCode)
  }

  const saveFile = async () => {
    const filename = prompt('Enter filename:', 'script.py')
    if (!filename) return
    try {
      await axios.post(`${API_URL}/code/file/write`, { path: filename, content: code })
      alert('✅ File saved!')
      loadFiles()
    } catch (err) {
      alert('❌ Failed to save: ' + err.message)
    }
  }

  const calculate = async () => {
    if (!calcExpression.trim()) return
    try {
      const res = await axios.post(`${API_URL}/code/calculate`, { expression: calcExpression })
      if (res.data.success) {
        setCalcResult(`= ${res.data.result}`)
        if (onSpeak) onSpeak(`The answer is ${res.data.result}`)
      } else {
        setCalcResult('Error')
      }
    } catch (err) {
      setCalcResult('Error')
    }
  }

  const copyCode = () => {
    navigator.clipboard.writeText(code)
    alert('✅ Code copied!')
  }

  return (
    <div className="code-panel">
      <div className="code-sidebar">
        <h3>⚡ Code Executor</h3>
        
        <div className="code-tabs">
          <button className={activeTab === 'editor' ? 'active' : ''} onClick={() => setActiveTab('editor')}>
            <Code size={16} /> Editor
          </button>
          <button className={activeTab === 'files' ? 'active' : ''} onClick={() => setActiveTab('files')}>
            <Folder size={16} /> Files
          </button>
          <button className={activeTab === 'calc' ? 'active' : ''} onClick={() => setActiveTab('calc')}>
            <Calculator size={16} /> Calculator
          </button>
          <button className={activeTab === 'templates' ? 'active' : ''} onClick={() => setActiveTab('templates')}>
            <FileText size={16} /> Templates
          </button>
        </div>

        {activeTab === 'editor' && (
          <div className="editor-controls">
            <button onClick={executeCode} disabled={loading} className="run-btn">
              <Play size={16} /> {loading ? 'Running...' : 'Run Code'}
            </button>
            <button onClick={saveFile} className="save-btn">
              <Save size={16} /> Save
            </button>
            <button onClick={copyCode} className="copy-btn">
              <Copy size={16} /> Copy
            </button>
          </div>
        )}

        {activeTab === 'files' && (
          <div className="files-list">
            {files.map((f, i) => (
              <div key={i} className="file-item">
                <FileText size={14} />
                <span>{f.name}</span>
                <span className="file-size">{(f.size / 1024).toFixed(1)} KB</span>
              </div>
            ))}
            {files.length === 0 && <p className="empty">No files yet</p>}
          </div>
        )}

        {activeTab === 'calc' && (
          <div className="calculator">
            <input
              value={calcExpression}
              onChange={(e) => setCalcExpression(e.target.value)}
              placeholder="2 + 2 * 5"
              className="calc-input"
              onKeyPress={(e) => e.key === 'Enter' && calculate()}
            />
            <button onClick={calculate}>=</button>
            <div className="calc-result">{calcResult}</div>
          </div>
        )}

        {activeTab === 'templates' && (
          <div className="templates-list">
            {templates.map((t, i) => (
              <button key={i} onClick={() => loadTemplate(t.code)} className="template-item">
                <FileText size={14} /> {t.name}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="code-main">
        {activeTab === 'editor' && (
          <>
            <div className="code-editor-container">
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                className="code-editor"
                spellCheck="false"
                placeholder="# Write Python code here..."
              />
            </div>
            <div className="code-output">
              <h4>📊 Output:</h4>
              {error && <div className="output-error">{error}</div>}
              {output && <pre className="output-success">{output}</pre>}
              {!output && !error && <p className="output-empty">Run code to see output...</p>}
            </div>
          </>
        )}

        {activeTab === 'files' && (
          <div className="files-main">
            <h4>📁 Workspace Files</h4>
            <p>Files are saved in the backend/workspace folder</p>
          </div>
        )}

        {activeTab === 'calc' && (
          <div className="calc-main">
            <h4>🔢 Calculator</h4>
            <p>Supports: +, -, *, /, parentheses, decimals</p>
            <p className="hint">Example: (10 + 5) * 2 - 3</p>
          </div>
        )}

        {activeTab === 'templates' && (
          <div className="templates-main">
            <h4>📝 Code Templates</h4>
            <p>Click a template to load it into the editor</p>
          </div>
        )}
      </div>
    </div>
  )
}