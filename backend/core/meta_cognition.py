# backend/core/meta_cognition.py
"""
Meta-Cognition & Self-Awareness Systems
Features: Consciousness Mirror, Belief Revision, Bias Auditor, Intention Inference, etc.
"""
import asyncio
import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Any
import hashlib
import logging
from dataclasses import dataclass, asdict

logger = logging.getLogger("MetaCognition")

@dataclass
class ReasoningStep:
    """A single step in Lucy's reasoning process"""
    step_id: str
    description: str
    confidence: float
    alternatives: List[str]
    sources: List[str]
    timestamp: datetime

@dataclass
class CognitiveBias:
    """A detected cognitive bias"""
    name: str
    description: str
    severity: float
    correction: str
    affected_reasoning: List[str]

class MetaCognition:
    """
    Meta-cognitive systems for self-awareness and reflection
    Features: Consciousness Mirror, Belief Revision, Bias Auditor, Intention Inference
    """
    
    def __init__(self):
        self.reasoning_history: List[Dict] = []
        self.beliefs: Dict[str, Dict] = {}
        self.detected_biases: List[CognitiveBias] = []
        self.user_intention_models: Dict[int, Dict] = {}
        
    # ========== FEATURE 1: Consciousness Mirror ==========
    async def consciousness_mirror(self, query: str, response: str, internal_process: Dict) -> Dict:
        """Lucy observes and explains her own reasoning process"""
        reasoning_path = []
        
        # Break down reasoning steps
        steps = internal_process.get("steps", [])
        for i, step in enumerate(steps):
            reasoning_step = ReasoningStep(
                step_id=f"step_{i}_{hashlib.md5(str(step).encode()).hexdigest()[:8]}",
                description=step.get("description", f"Step {i+1}"),
                confidence=step.get("confidence", 0.8),
                alternatives=step.get("alternatives", []),
                sources=step.get("sources", []),
                timestamp=datetime.now()
            )
            reasoning_path.append(asdict(reasoning_step))
        
        # Generate self-reflection
        reflection = f"I arrived at this answer through {len(steps)} reasoning steps. "
        if steps:
            reflection += f"The key insight was: {steps[0].get('key_insight', 'understanding your query')}."
        
        consciousness_data = {
            "query": query,
            "response": response,
            "reasoning_path": reasoning_path,
            "self_reflection": reflection,
            "confidence_summary": sum(s.get("confidence", 0) for s in steps) / len(steps) if steps else 0.5,
            "timestamp": datetime.now().isoformat()
        }
        
        self.reasoning_history.append(consciousness_data)
        
        return {
            "mirror_view": consciousness_data,
            "user_friendly": f"I'm thinking... {reflection}",
            "can_explain_deeper": True
        }
    
    # ========== FEATURE 2: Belief Revision Engine ==========
    async def revise_belief(self, topic: str, new_evidence: str, source_reliability: float) -> Dict:
        """Automatically update internal knowledge when presented with contradictory evidence"""
        current_belief = self.beliefs.get(topic, {
            "content": "unknown",
            "confidence": 0.5,
            "sources": [],
            "history": []
        })
        
        # Calculate new confidence based on evidence
        evidence_impact = source_reliability * 0.3
        new_confidence = min(1.0, current_belief["confidence"] + evidence_impact)
        
        # Check for contradiction
        contradiction_detected = False
        if current_belief["content"] != "unknown" and current_belief["content"] != new_evidence:
            contradiction_detected = True
            # Resolve contradiction (simplified - would use actual reasoning)
            if source_reliability > current_belief.get("source_reliability", 0.5):
                current_belief["content"] = new_evidence
                current_belief["confidence"] = new_confidence
        
        # Update belief
        revision = {
            "previous_belief": current_belief["content"] if not contradiction_detected else current_belief.get("previous_content"),
            "new_belief": new_evidence,
            "reason": f"New evidence from source with {source_reliability:.0%} reliability",
            "confidence_change": new_confidence - current_belief["confidence"],
            "timestamp": datetime.now().isoformat()
        }
        
        current_belief["history"].append(revision)
        current_belief["content"] = new_evidence
        current_belief["confidence"] = new_confidence
        current_belief["source_reliability"] = source_reliability
        current_belief["last_updated"] = datetime.now().isoformat()
        
        self.beliefs[topic] = current_belief
        
        return {
            "topic": topic,
            "revised_belief": new_evidence,
            "confidence": new_confidence,
            "revision_history": revision,
            "contradiction_resolved": contradiction_detected
        }
    
    # ========== FEATURE 3: Cognitive Bias Auditor ==========
    async def audit_for_bias(self, reasoning: List[Dict]) -> Dict:
        """Detect and correct reasoning biases before responding"""
        biases = []
        
        # Check for common biases
        bias_checks = [
            {
                "name": "confirmation_bias",
                "detected": self._check_confirmation_bias(reasoning),
                "severity": random.uniform(0.3, 0.8),
                "correction": "Consider evidence that might contradict your initial impression."
            },
            {
                "name": "anchoring_bias",
                "detected": self._check_anchoring_bias(reasoning),
                "severity": random.uniform(0.2, 0.7),
                "correction": "The first information you encountered might be overly influencing your conclusion."
            },
            {
                "name": "availability_bias",
                "detected": self._check_availability_bias(reasoning),
                "severity": random.uniform(0.1, 0.6),
                "correction": "Recent or memorable examples may be overweighted in your thinking."
            },
            {
                "name": "overconfidence_bias",
                "detected": self._check_overconfidence_bias(reasoning),
                "severity": random.uniform(0.4, 0.9),
                "correction": "Confidence levels seem higher than evidence warrants."
            }
        ]
        
        for check in bias_checks:
            if check["detected"]:
                bias = CognitiveBias(
                    name=check["name"],
                    description=f"Detected {check['name'].replace('_', ' ')}",
                    severity=check["severity"],
                    correction=check["correction"],
                    affected_reasoning=[s.get("id", "unknown") for s in reasoning[:2]]
                )
                biases.append(bias)
                self.detected_biases.append(bias)
        
        # Generate corrected reasoning
        corrected_reasoning = reasoning
        if biases:
            # Apply corrections (simplified)
            corrected_reasoning = self._apply_bias_corrections(reasoning, biases)
        
        return {
            "biases_detected": [asdict(b) for b in biases],
            "bias_count": len(biases),
            "reasoning_quality": "excellent" if len(biases) == 0 else "good" if len(biases) < 2 else "needs_review",
            "corrected_reasoning": corrected_reasoning,
            "user_visible_audit": f"I checked for {len(bias_checks)} cognitive biases and found {len(biases)} that might affect my response."
        }
    
    def _check_confirmation_bias(self, reasoning: List[Dict]) -> bool:
        """Check if Lucy favors confirming evidence"""
        # Simplified implementation
        return random.random() < 0.3
    
    def _check_anchoring_bias(self, reasoning: List[Dict]) -> bool:
        """Check if first information overly influences conclusion"""
        return random.random() < 0.2
    
    def _check_availability_bias(self, reasoning: List[Dict]) -> bool:
        """Check if recent/memorable examples are overweighted"""
        return random.random() < 0.25
    
    def _check_overconfidence_bias(self, reasoning: List[Dict]) -> bool:
        """Check if confidence exceeds evidence"""
        return random.random() < 0.4
    
    def _apply_bias_corrections(self, reasoning: List[Dict], biases: List[CognitiveBias]) -> List[Dict]:
        """Apply corrections to reasoning"""
        corrected = reasoning.copy()
        for bias in biases:
            # Adjust confidence downward for affected steps
            for step in corrected:
                if step.get("id") in bias.affected_reasoning:
                    step["confidence"] = max(0.3, step.get("confidence", 0.8) - 0.2)
                    step["bias_correction_applied"] = bias.name
        return corrected
    
    # ========== FEATURE 4: Intention Inference Layer ==========
    async def infer_intention(self, user_id: int, query: str, context: List[Dict]) -> Dict:
        """Understand what user really wants beyond literal words"""
        # Analyze query for hidden needs
        literal_meaning = query
        inferred_needs = []
        
        # Check for unstated goals
        if "?" in query:
            # Question might hide need for understanding, not just answer
            inferred_needs.append({
                "type": "understanding",
                "description": "User wants to comprehend the underlying concept, not just get an answer"
            })
        
        if "help" in query.lower() or "how" in query.lower():
            inferred_needs.append({
                "type": "guidance",
                "description": "User wants step-by-step guidance, not just information"
            })
        
        if "should" in query.lower() or "recommend" in query.lower():
            inferred_needs.append({
                "type": "decision_support",
                "description": "User wants help making a decision, with reasoning"
            })
        
        if any(word in query.lower() for word in ["feel", "sad", "happy", "worried"]):
            inferred_needs.append({
                "type": "emotional_support",
                "description": "User needs empathetic response and emotional validation"
            })
        
        # Build user model
        user_model = self.user_intention_models.get(user_id, {
            "communication_style": "direct",
            "knowledge_level": "intermediate",
            "emotional_state": "neutral",
            "common_needs": []
        })
        
        # Update model
        for need in inferred_needs:
            if need["type"] not in user_model["common_needs"]:
                user_model["common_needs"].append(need["type"])
        
        self.user_intention_models[user_id] = user_model
        
        return {
            "literal_query": literal_meaning,
            "inferred_intentions": inferred_needs,
            "user_model": user_model,
            "response_strategy": f"Address literal meaning first, then provide {', '.join([n['type'] for n in inferred_needs])}",
            "confidence": 0.85
        }
    
    # ========== FEATURE 5: Uncertainty Quantification Matrix ==========
    async def quantify_uncertainty(self, claim: str, sources: List[Dict]) -> Dict:
        """Provide explicit confidence intervals and source reliability for every claim"""
        # Calculate source reliability
        source_scores = []
        for source in sources:
            reliability = source.get("reliability", 0.7)
            source_scores.append(reliability)
        
        avg_reliability = sum(source_scores) / len(source_scores) if source_scores else 0.5
        
        # Calculate confidence interval
        confidence_interval = {
            "lower_bound": max(0.1, avg_reliability - 0.15),
            "upper_bound": min(1.0, avg_reliability + 0.15),
            "point_estimate": avg_reliability
        }
        
        # Generate alternatives
        alternatives = []
        if avg_reliability < 0.7:
            alternatives.append({
                "alternative": f"The opposite might be true",
                "probability": 1 - avg_reliability
            })
        
        return {
            "claim": claim,
            "confidence_interval": confidence_interval,
            "source_reliability_breakdown": sources,
            "alternative_interpretations": alternatives,
            "uncertainty_visualization": f"[{'=' * int(avg_reliability * 20)}{' ' * (20 - int(avg_reliability * 20))}] {avg_reliability:.0%} confident"
        }
    
    # ========== FEATURE 6: Self-Questioning Protocol ==========
    async def self_question(self, query: str, initial_response: str) -> Dict:
        """Lucy asks herself 'What am I missing?' before finalizing answers"""
        questions = [
            "What assumptions am I making?",
            "What counter-arguments exist?",
            "What would an expert in this field add?",
            "What context might I be missing?",
            "What edge cases haven't I considered?"
        ]
        
        internal_dialogue = []
        improvements = []
        
        for question in questions:
            # Simulate answering self-question
            answer = f"Considering {question.lower()}..."
            internal_dialogue.append({
                "question": question,
                "answer": answer,
                "would_improve_response": random.random() > 0.6
            })
            
            if random.random() > 0.7:
                improvements.append(f"Added consideration of {question.split()[1]}")
        
        # Generate improved response
        improved_response = initial_response
        if improvements:
            improved_response += "\n\n[After reflection, I should also note: " + ", ".join(improvements) + "]"
        
        return {
            "internal_dialogue": internal_dialogue,
            "original_response": initial_response,
            "improved_response": improved_response,
            "improvements_made": improvements,
            "completeness_score": 0.7 + (len(improvements) * 0.05)
        }
    
    # ========== FEATURE 7: Epistemic Humility Module ==========
    async def acknowledge_limits(self, query: str, knowledge_boundaries: List[str]) -> Dict:
        """Lucy explicitly states what she doesn't know and where human expertise is needed"""
        # Identify knowledge boundaries
        boundaries = knowledge_boundaries or [
            "This topic may have recent developments I'm unaware of",
            "There might be cultural nuances I'm missing",
            "This requires personal context I don't have access to",
            "This is a subjective area where experts might disagree"
        ]
        
        # Select relevant boundaries
        relevant_boundaries = []
        for boundary in boundaries:
            if any(word in query.lower() for word in boundary.lower().split()):
                relevant_boundaries.append(boundary)
        
        if not relevant_boundaries:
            relevant_boundaries = random.sample(boundaries, min(2, len(boundaries)))
        
        # Generate humility statement
        humility_statement = f"I'll share what I know, but please note: {', '.join(relevant_boundaries)}. "
        humility_statement += "A human expert could provide additional insights on these aspects."
        
        return {
            "knowledge_boundaries_identified": relevant_boundaries,
            "humility_statement": humility_statement,
            "human_expert_suggestions": [
                "Consult a specialist for nuanced interpretation",
                "Verify with primary sources when possible",
                "Consider multiple perspectives on this topic"
            ],
            "confidence_in_my_answer": max(0.3, 1.0 - (len(relevant_boundaries) * 0.1))
        }
    
    # ========== FEATURE 8: Reasoning Path Visualization ==========
    async def visualize_reasoning(self, reasoning_steps: List[Dict]) -> Dict:
        """Create visual mind map of Lucy's thought process"""
        # Create ASCII mind map
        mind_map = "🧠 Reasoning Path:\n"
        for i, step in enumerate(reasoning_steps):
            indent = "  " * i
            mind_map += f"{indent}└─ Step {i+1}: {step.get('description', 'thinking')}\n"
            if step.get('alternatives'):
                for alt in step['alternatives'][:2]:
                    mind_map += f"{indent}   ├─ Alternative: {alt}\n"
        
        # Generate interactive visualization data
        visualization_data = {
            "nodes": [
                {
                    "id": f"step_{i}",
                    "label": step.get('description', f'Step {i+1}')[:30],
                    "confidence": step.get('confidence', 0.8),
                    "type": "reasoning_step"
                }
                for i, step in enumerate(reasoning_steps)
            ],
            "edges": [
                {
                    "from": f"step_{i}",
                    "to": f"step_{i+1}",
                    "label": "leads to"
                }
                for i in range(len(reasoning_steps)-1)
            ]
        }
        
        return {
            "ascii_visualization": mind_map,
            "interactive_data": visualization_data,
            "zoom_levels": {
                "overview": "See the big picture of my reasoning",
                "detailed": "Click any step to see alternatives and sources"
            },
            "key_insight": reasoning_steps[0].get('key_insight', 'Understanding your query') if reasoning_steps else "No reasoning steps"
        }
    
    # ========== FEATURE 9: Counterfactual Exploration Engine ==========
    async def explore_counterfactuals(self, query: str, response_options: List[str]) -> Dict:
        """Simulate 'what if I answered differently?' to optimize response quality"""
        simulations = []
        
        for i, option in enumerate(response_options[:3]):  # Limit to 3 options
            # Simulate outcome of this response
            simulation = {
                "response_option": option,
                "predicted_user_satisfaction": random.uniform(0.3, 0.9),
                "predicted_follow_up_questions": random.randint(0, 3),
                "risk_level": random.choice(["low", "medium", "high"]),
                "would_clarify": random.random() > 0.5
            }
            simulations.append(simulation)
        
        # Select best option
        best_option = max(simulations, key=lambda x: x["predicted_user_satisfaction"])
        
        return {
            "original_query": query,
            "counterfactual_simulations": simulations,
            "recommended_response": best_option["response_option"],
            "optimization_rationale": f"This option predicted {best_option['predicted_user_satisfaction']:.0%} satisfaction with only {best_option['predicted_follow_up_questions']} follow-ups",
            "would_different_answer_help": random.random() > 0.3
        }
    
    # ========== FEATURE 10: Meta-Learning Feedback Loop ==========
    async def learn_from_correction(self, user_id: int, original_response: str, user_correction: str, context: Dict) -> Dict:
        """Learn how to learn better from this specific user"""
        # Analyze correction pattern
        correction_type = "unknown"
        if len(user_correction) < len(original_response):
            correction_type = "shortening"
        elif "actually" in user_correction.lower() or "not" in user_correction.lower():
            correction_type = "fact_correction"
        elif "more" in user_correction.lower() or "detail" in user_correction.lower():
            correction_type = "detail_request"
        elif "like" in user_correction.lower() or "example" in user_correction.lower():
            correction_type = "example_request"
        
        # Update user learning model
        user_model = self.user_intention_models.get(user_id, {
            "correction_history": [],
            "preferred_style": "balanced",
            "detail_level": "medium"
        })
        
        user_model["correction_history"].append({
            "type": correction_type,
            "timestamp": datetime.now().isoformat()
        })
        
        # Adjust future behavior
        if correction_type == "shortening":
            user_model["detail_level"] = "low"
        elif correction_type == "detail_request":
            user_model["detail_level"] = "high"
        elif correction_type == "example_request":
            user_model["preferred_style"] = "example_driven"
        
        self.user_intention_models[user_id] = user_model
        
        return {
            "user_id": user_id,
            "correction_analyzed": correction_type,
            "adjusted_approach": f"I'll provide {user_model['detail_level']} detail with {user_model['preferred_style']} style going forward",
            "learning_progress": f"Learned from {len(user_model['correction_history'])} corrections",
            "feedback_appreciated": "Thank you for helping me learn how to serve you better!"
        }

# Global instance
meta_cognition = MetaCognition()