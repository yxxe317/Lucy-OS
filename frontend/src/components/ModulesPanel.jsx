import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Heart, BookOpen, Languages, Wrench, Brain, 
  Sparkles, Target, Shield, Infinity, Moon,
  Cloud, Newspaper, TrendingUp, Github 
} from 'lucide-react';

const API_URL = "http://127.0.0.1:8000";

export default function ModulesPanel() {
  const [activeModule, setActiveModule] = useState('emotion');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const modules = [
    { id: 'emotion', name: 'Emotion', icon: Heart, color: '#ff6b6b' },
    { id: 'knowledge', name: 'Knowledge', icon: BookOpen, color: '#4ecdc4' },
    { id: 'language', name: 'Language', icon: Languages, color: '#45b7d1' },
    { id: 'integrations', name: 'Integrations', icon: Wrench, color: '#96ceb4' },
    { id: 'quantum', name: 'Quantum', icon: Brain, color: '#9b59b6' },
    { id: 'creativity', name: 'Creativity', icon: Sparkles, color: '#f1c40f' },
    { id: 'autonomy', name: 'Autonomy', icon: Target, color: '#e67e22' },
    { id: 'ethics', name: 'Ethics', icon: Shield, color: '#e74c3c' },
    { id: 'advanced', name: 'Advanced', icon: Infinity, color: '#1abc9c' },
  ];

  const fetchData = async () => {
    setLoading(true);
    try {
      let res;
      switch(activeModule) {
        case 'emotion':
          res = await axios.get(`${API_URL}/api/emotion/mood`);
          break;
        case 'creativity':
          res = await axios.get(`${API_URL}/api/creativity/poem?theme=nature`);
          break;
        case 'advanced':
          res = await axios.get(`${API_URL}/api/advanced/dream`);
          break;
        case 'integrations':
          res = await axios.get(`${API_URL}/api/integrations/weather/London`);
          break;
        default:
          res = { data: { message: 'Select a module' } };
      }
      setData(res.data);
    } catch (error) {
      console.error('Error fetching module data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [activeModule]);

  return (
    <div className="modules-container">
      <div className="modules-sidebar">
        {modules.map(module => (
          <button
            key={module.id}
            className={`module-btn ${activeModule === module.id ? 'active' : ''}`}
            onClick={() => setActiveModule(module.id)}
            style={{ borderColor: module.color }}
          >
            <module.icon size={20} color={module.color} />
            <span>{module.name}</span>
          </button>
        ))}
      </div>

      <div className="module-content">
        <h2>{modules.find(m => m.id === activeModule)?.name} Module</h2>
        
        {loading && <div className="loading">Loading...</div>}
        
        {data && (
          <pre className="module-data">
            {JSON.stringify(data, null, 2)}
          </pre>
        )}

        <div className="module-actions">
          <button onClick={fetchData} className="refresh-btn">
            Refresh Data
          </button>
        </div>
      </div>
    </div>
  );
}