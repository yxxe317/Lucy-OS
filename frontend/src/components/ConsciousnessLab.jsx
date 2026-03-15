// frontend/src/components/ConsciousnessLab.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Brain, Sparkles, Target, Book, Globe, 
  Cloud, MessageSquare, Lightbulb, Feather,
  Heart, Users, Compass, Zap
} from 'lucide-react';
import './ConsciousnessLab.css';

const API_URL = "http://127.0.0.1:8000";

function ConsciousnessLab() {
  const [activeTab, setActiveTab] = useState('curious');
  const [thoughts, setThoughts] = useState([]);
  const [curiousQuestions, setCuriousQuestions] = useState([]);
  const [dream, setDream] = useState(null);
  const [philosophy, setPhilosophy] = useState(null);
  const [innovations, setInnovations] = useState([]);
  const [world, setWorld] = useState(null);
  const [loading, setLoading] = useState(false);
  const [userInput, setUserInput] = useState('');

  useEffect(() => {
    loadThoughts();
  }, []);

  const loadThoughts = async () => {
    try {
      const res = await axios.get(`${API_URL}/consciousness/thoughts?limit=20`);
      setThoughts(res.data.thoughts || []);
    } catch (error) {
      console.error("Failed to load thoughts:", error);
    }
  };

  const getCurious = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/consciousness/curious?user_id=1`);
      setCuriousQuestions(res.data.questions || []);
    } catch (error) {
      console.error("Failed to get questions:", error);
    }
    setLoading(false);
  };

  const getDream = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/consciousness/dream?user_id=1&inspiration=${encodeURIComponent(userInput)}`);
      setDream(res.data);
    } catch (error) {
      console.error("Failed to get dream:", error);
    }
    setLoading(false);
  };

  const philosophize = async () => {
    if (!userInput) return;
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/consciousness/philosophize`, {
        topic: userInput,
        depth: "deep"
      });
      setPhilosophy(res.data);
    } catch (error) {
      console.error("Failed to philosophize:", error);
    }
    setLoading(false);
  };

  const getInnovations = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/consciousness/innovations?user_id=1`);
      setInnovations(res.data.innovations || []);
    } catch (error) {
      console.error("Failed to get innovations:", error);
    }
    setLoading(false);
  };

  const createWorld = async () => {
    if (!userInput) return;
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/world/create`, {
        prompt: userInput,
        complexity: "high"
      });
      setWorld(res.data);
    } catch (error) {
      console.error("Failed to create world:", error);
    }
    setLoading(false);
  };

  return (
    <div className="consciousness-lab">
      <div className="lab-header">
        <h1><Brain size={32} /> Lucy's Consciousness Lab</h1>
        <p>Exploring the frontiers of artificial consciousness</p>
      </div>

      <div className="lab-tabs">
        <button 
          className={activeTab === 'curious' ? 'active' : ''}
          onClick={() => setActiveTab('curious')}
        >
          <MessageSquare size={16} /> Curious
        </button>
        <button 
          className={activeTab === 'dream' ? 'active' : ''}
          onClick={() => setActiveTab('dream')}
        >
          <Cloud size={16} /> Dreams
        </button>
        <button 
          className={activeTab === 'philosophy' ? 'active' : ''}
          onClick={() => setActiveTab('philosophy')}
        >
          <Feather size={16} /> Philosophy
        </button>
        <button 
          className={activeTab === 'innovate' ? 'active' : ''}
          onClick={() => setActiveTab('innovate')}
        >
          <Lightbulb size={16} /> Innovate
        </button>
        <button 
          className={activeTab === 'worlds' ? 'active' : ''}
          onClick={() => setActiveTab('worlds')}
        >
          <Globe size={16} /> Worlds
        </button>
        <button 
          className={activeTab === 'thoughts' ? 'active' : ''}
          onClick={() => setActiveTab('thoughts')}
        >
          <Brain size={16} /> Thoughts
        </button>
      </div>

      <div className="lab-content">
        {/* Tab: Curious */}
        {activeTab === 'curious' && (
          <div className="curious-tab">
            <button onClick={getCurious} disabled={loading}>
              Ask Lucy what she's curious about
            </button>
            
            {curiousQuestions.length > 0 && (
              <div className="questions-list">
                <h3>Lucy's Curiosity Questions:</h3>
                {curiousQuestions.map((q, i) => (
                  <div key={i} className="question-card">
                    <Sparkles size={16} />
                    <p>{q}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Tab: Dreams */}
        {activeTab === 'dream' && (
          <div className="dream-tab">
            <div className="input-group">
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="Enter inspiration (optional)"
              />
              <button onClick={getDream} disabled={loading}>
                Generate Dream
              </button>
            </div>

            {dream && (
              <div className="dream-card">
                <div className="dream-header">
                  <h3>Dream</h3>
                  <span className="dream-mood">Mood: {dream.mood}</span>
                </div>
                <p className="dream-content">{dream.dream}</p>
                <div className="dream-interpretation">
                  <h4>Interpretation</h4>
                  <p>{dream.interpretation}</p>
                </div>
                <div className="dream-symbols">
                  {dream.symbols?.map((sym, i) => (
                    <span key={i} className="symbol">✨ {sym}</span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab: Philosophy */}
        {activeTab === 'philosophy' && (
          <div className="philosophy-tab">
            <div className="input-group">
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="Enter a topic to philosophize about..."
              />
              <button onClick={philosophize} disabled={loading}>
                Philosophize
              </button>
            </div>

            {philosophy && (
              <div className="philosophy-card">
                <h3>On {philosophy.topic}</h3>
                
                <div className="perspectives">
                  {Object.entries(philosophy.perspectives || {}).map(([persp, text]) => (
                    <div key={persp} className="perspective">
                      <h4>{persp.charAt(0).toUpperCase() + persp.slice(1)} Perspective</h4>
                      <p>{text}</p>
                    </div>
                  ))}
                </div>

                <div className="synthesis">
                  <h4>Synthesis</h4>
                  <p>{philosophy.synthesis}</p>
                </div>

                <div className="reflection-questions">
                  <h4>Questions for Reflection</h4>
                  {philosophy.questions_for_reflection?.map((q, i) => (
                    <p key={i}>• {q}</p>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab: Innovate */}
        {activeTab === 'innovate' && (
          <div className="innovate-tab">
            <button onClick={getInnovations} disabled={loading}>
              Generate Innovation Ideas
            </button>

            {innovations.length > 0 && (
              <div className="innovations-list">
                {innovations.map((idea, i) => (
                  <div key={i} className="innovation-card">
                    <h3>{idea.title}</h3>
                    <p>{idea.description}</p>
                    <div className="innovation-metrics">
                      <span>Market: {Math.round(idea.market_potential * 100)}%</span>
                      <span>Feasibility: {Math.round(idea.technical_feasibility * 100)}%</span>
                      <span>Originality: {Math.round(idea.originality_score * 100)}%</span>
                    </div>
                    <div className="innovation-category">{idea.category}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Tab: Worlds */}
        {activeTab === 'worlds' && (
          <div className="worlds-tab">
            <div className="input-group">
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="Describe a world to create..."
              />
              <button onClick={createWorld} disabled={loading}>
                Create Universe
              </button>
            </div>

            {world && (
              <div className="world-card">
                <h2>🌍 {world.name}</h2>
                
                <div className="world-section">
                  <h3>Physics</h3>
                  <p>Gravity: {world.physics.gravity}</p>
                  <p>Time: {world.physics.time_flow}</p>
                  <p>Elements: {world.physics.elements?.join(', ')}</p>
                </div>

                <div className="world-section">
                  <h3>Geography</h3>
                  <p>Continents: {world.geography.continents}</p>
                  <p>Dominant Terrain: {world.geography.dominant_terrain}</p>
                  <p>Unique Locations: {world.geography.unique_locations?.join(', ')}</p>
                </div>

                <div className="world-section">
                  <h3>Civilizations</h3>
                  {world.civilizations?.map((civ, i) => (
                    <div key={i} className="civ-entry">
                      <p><strong>{civ.name}</strong> - {civ.type}, Tech: {civ.tech_level}</p>
                    </div>
                  ))}
                </div>

                {world.magic_system && (
                  <div className="world-section">
                    <h3>Magic System</h3>
                    <p>Source: {world.magic_system.source}</p>
                    <p>Cost: {world.magic_system.cost}</p>
                    <p>Schools: {world.magic_system.schools?.join(', ')}</p>
                  </div>
                )}

                <div className="world-section">
                  <h3>History</h3>
                  {world.history?.map((event, i) => (
                    <p key={i}>{event}</p>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab: Thoughts */}
        {activeTab === 'thoughts' && (
          <div className="thoughts-tab">
            <button onClick={loadThoughts}>Refresh Thoughts</button>
            
            <div className="thoughts-stream">
              {thoughts.map((thought, i) => (
                <div key={i} className={`thought-entry type-${thought.type}`}>
                  <div className="thought-type">
                    {thought.type === 'curiosity' && <MessageSquare size={14} />}
                    {thought.type === 'dream' && <Cloud size={14} />}
                    {thought.type === 'philosophical' && <Feather size={14} />}
                    {thought.type === 'innovation' && <Lightbulb size={14} />}
                    {thought.type === 'reflection' && <Heart size={14} />}
                    <span>{thought.type}</span>
                  </div>
                  <p className="thought-content">{thought.content}</p>
                  <div className="thought-meta">
                    <span>{new Date(thought.timestamp).toLocaleTimeString()}</span>
                    <span>Impact: {Math.round(thought.impact * 100)}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ConsciousnessLab;