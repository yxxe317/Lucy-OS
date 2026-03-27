import React, { useState, useEffect, useRef } from 'react';
import './ReasoningTree.css';

const ReasoningTree = ({ thoughts = [], autoScroll = true }) => {
  const scrollRef = useRef(null);
  const [thoughtCount, setThoughtCount] = useState(0);
  const [stats, setStats] = useState({ by_type: {} });

  // Auto-scroll to bottom when new thoughts arrive
  useEffect(() => {
    if (autoScroll && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
    setThoughtCount(thoughts.length);
  }, [thoughts, autoScroll]);

  // Update stats from thoughts
  useEffect(() => {
    if (thoughts.length > 0) {
      const by_type = {};
      thoughts.forEach(thought => {
        const type = thought.type || 'unknown';
        by_type[type] = (by_type[type] || 0) + 1;
      });
      setStats({ by_type });
    }
  }, [thoughts]);

  // Get icon for thought type
  const getThoughtIcon = (type) => {
    const icons = {
      'Hardware Logic': '💾',
      'Memory Recall': '🧠',
      'Security Check': '🔒',
      'Social Intelligence': '💬',
      'Reasoning Process': '🤔',
      'Action Execution': '⚡'
    };
    return icons[type] || '🔮';
  };

  // Get color for thought type
  const getThoughtColor = (type) => {
    const colors = {
      'Hardware Logic': '#4CAF50',
      'Memory Recall': '#2196F3',
      'Security Check': '#FF9800',
      'Social Intelligence': '#E91E63',
      'Reasoning Process': '#9C27B0',
      'Action Execution': '#FF5722'
    };
    return colors[type] || '#607D8B';
  };

  // Format timestamp
  const formatTimestamp = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
      hour12: false, 
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit'
    });
  };

  // Get thought type from content (fallback)
  const getThoughtTypeFromContent = (content) => {
    const contentLower = content.toLowerCase();
    if (contentLower.includes('hardware') || contentLower.includes('gpu') || contentLower.includes('cpu')) {
      return 'Hardware Logic';
    }
    if (contentLower.includes('memory') || contentLower.includes('recall') || contentLower.includes('learned')) {
      return 'Memory Recall';
    }
    if (contentLower.includes('security') || contentLower.includes('verify') || contentLower.includes('protect')) {
      return 'Security Check';
    }
    if (contentLower.includes('social') || contentLower.includes('emotion') || contentLower.includes('feel')) {
      return 'Social Intelligence';
    }
    return 'Reasoning Process';
  };

  // Process thoughts for display
  const displayThoughts = thoughts.map(thought => ({
    ...thought,
    displayType: thought.type || getThoughtTypeFromContent(thought.content || ''),
    displayIcon: getThoughtIcon(thought.displayType),
    displayColor: getThoughtColor(thought.displayType)
  }));

  return (
    <div className="reasoning-tree-container">
      {/* Stats Header */}
      <div className="reasoning-stats">
        <div className="stat-item">
          <span className="stat-value">{thoughtCount}</span>
          <span className="stat-label">Thoughts</span>
        </div>
        {Object.entries(stats.by_type).map(([type, count]) => (
          <div key={type} className="stat-item">
            <span className="stat-label">{type}:</span>
            <span className="stat-value">{count}</span>
          </div>
        ))}
      </div>

      {/* Timeline Container */}
      <div className="reasoning-timeline" ref={scrollRef}>
        {displayThoughts.length === 0 ? (
          <div className="no-thoughts">
            <p>Waiting for Lucy to think...</p>
          </div>
        ) : (
          displayThoughts.map((thought, index) => (
            <div 
              key={thought.id || index}
              className={`thought-card ${thought.type || ''}`}
              style={{ borderLeftColor: thought.displayColor }}
            >
              {/* Timeline connector */}
              {index > 0 && (
                <div className="timeline-line"></div>
              )}

              {/* Thought header */}
              <div className="thought-header">
                <span className="thought-icon">{thought.displayIcon}</span>
                <div className="thought-meta">
                  <span className="thought-type">{thought.displayType}</span>
                  <span className="thought-time">{formatTimestamp(thought.timestamp)}</span>
                </div>
              </div>

              {/* Thought content */}
              <div className="thought-content">
                <p>{thought.content || 'No thought content'}</p>
              </div>

              {/* Memory flashback indicator */}
              {thought.memory_flashback && thought.memory_flashback.found && (
                <div className="memory-flashback">
                  <span className="flashback-icon">📚</span>
                  <span className="flashback-label">Memory Flashback</span>
                  <p className="flashback-content">
                    "{thought.memory_flashback.content?.substring(0, 100)}..."
                  </p>
                  <span className="similarity-score">
                    Similarity: {(thought.memory_flashback.similarity * 100).toFixed(1)}%
                  </span>
                </div>
              )}

              {/* Processing time */}
              {thought.processing_time && (
                <div className="processing-time">
                  ⚡ {thought.processing_time.toFixed(2)}ms
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Loading indicator */}
      {thoughts.length > 0 && (
        <div className="thinking-indicator">
          <span className="thinking-dot"></span>
          <span className="thinking-dot"></span>
          <span className="thinking-dot"></span>
        </div>
      )}
    </div>
  );
};

export default ReasoningTree;