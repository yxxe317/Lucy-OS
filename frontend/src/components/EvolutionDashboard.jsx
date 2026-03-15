// frontend/src/components/EvolutionDashboard.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Brain, Target, History, Award, TrendingUp } from 'lucide-react';
import './EvolutionDashboard.css';

const API_URL = "http://127.0.0.1:8000";

function EvolutionDashboard() {
  const [goals, setGoals] = useState([]);
  const [history, setHistory] = useState([]);
  const [benchmark, setBenchmark] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [goalsRes, historyRes] = await Promise.all([
        axios.get(`${API_URL}/evolution/goals`),
        axios.get(`${API_URL}/evolution/history`)
      ]);
      setGoals(goalsRes.data.goals || []);
      setHistory(historyRes.data.history || []);
    } catch (error) {
      console.error("Failed to load evolution data:", error);
    }
    setLoading(false);
  };

  const runBenchmark = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/evolution/benchmark`);
      setBenchmark(res.data);
    } catch (error) {
      console.error("Benchmark failed:", error);
    }
    setLoading(false);
  };

  const addGoal = async () => {
    const goal = prompt("Enter your long-term goal:");
    if (!goal) return;
    
    const priority = prompt("Priority (1-10, default 5):", "5");
    
    try {
      await axios.post(`${API_URL}/evolution/goal`, {
        goal,
        priority: parseInt(priority) || 5
      });
      loadData();
    } catch (error) {
      console.error("Failed to add goal:", error);
    }
  };

  return (
    <div className="evolution-dashboard">
      <div className="dashboard-header">
        <h2><Brain size={24} /> Lucy's Evolution Dashboard</h2>
        <button onClick={runBenchmark} disabled={loading}>
          Run Intelligence Benchmark
        </button>
      </div>

      {benchmark && (
        <div className="benchmark-card">
          <h3><TrendingUp size={20} /> Latest Benchmark</h3>
          <div className="score">{Math.round(benchmark.average_score * 100)}%</div>
          <p>{benchmark.improvement_since_last}</p>
          <div className="test-results">
            {benchmark.results?.map((r, i) => (
              <div key={i} className={`test-result ${r.passed ? 'passed' : 'failed'}`}>
                <span>{r.category}</span>
                <span>{Math.round(r.score * 100)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="goals-section">
        <div className="section-header">
          <h3><Target size={20} /> Long-Term Goals</h3>
          <button onClick={addGoal} className="add-goal-btn">+ Add Goal</button>
        </div>
        
        {goals.length === 0 ? (
          <p className="empty">No active goals</p>
        ) : (
          goals.map(goal => (
            <div key={goal.id} className="goal-card">
              <div className="goal-header">
                <span className="goal-priority">P{goal.priority}</span>
                <span className="goal-text">{goal.goal}</span>
              </div>
              <div className="goal-progress">
                <div className="progress-bar">
                  <div 
                    className="progress-fill" 
                    style={{width: `${goal.progress * 100}%`}}
                  />
                </div>
                <span className="progress-text">{Math.round(goal.progress * 100)}%</span>
              </div>
              <div className="goal-dates">
                <span>Created: {new Date(goal.created).toLocaleDateString()}</span>
                <span>Target: {new Date(goal.target).toLocaleDateString()}</span>
              </div>
            </div>
          ))
        )}
      </div>

      <div className="history-section">
        <h3><History size={20} /> Evolution History</h3>
        {history.length === 0 ? (
          <p className="empty">No evolution events yet</p>
        ) : (
          history.map(event => (
            <div key={event.node_id} className="history-event">
              <div className="event-icon">
                {event.type === 'benchmark' && <Award size={16} />}
                {event.type === 'prompt_evolution' && <Brain size={16} />}
                {event.type === 'skill_synthesis' && <TrendingUp size={16} />}
              </div>
              <div className="event-details">
                <div className="event-description">{event.description}</div>
                <div className="event-meta">
                  <span>{new Date(event.timestamp).toLocaleString()}</span>
                  <span className="event-impact">Impact: +{Math.round(event.impact * 100)}%</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default EvolutionDashboard;