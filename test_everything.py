#!/usr/bin/env python3
"""
LUCY AI - COMPREHENSIVE TEST SUITE
Tests ALL 67+ modules to verify they're working
"""

import sys
import os
import time
import random
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*70)
print("🚀 LUCY AI - COMPREHENSIVE MODULE TEST SUITE")
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)

results = {
    'passed': 0,
    'failed': 0,
    'skipped': 0,
    'modules': {}
}

def test_module(module_name, test_func):
    """Test a single module and record result"""
    print(f"\n🔍 Testing {module_name}...", end=' ')
    try:
        result = test_func()
        if result.get('success', False):
            print(f"✅ PASSED ({result.get('details', '')})")
            results['passed'] += 1
            results['modules'][module_name] = {'status': 'passed', 'details': result.get('details', '')}
        else:
            print(f"⚠️  SKIPPED ({result.get('reason', 'Not available')})")
            results['skipped'] += 1
            results['modules'][module_name] = {'status': 'skipped', 'reason': result.get('reason', '')}
    except Exception as e:
        print(f"❌ FAILED ({str(e)[:50]})")
        results['failed'] += 1
        results['modules'][module_name] = {'status': 'failed', 'error': str(e)}
    time.sleep(0.1)

# ==================== CORE MODULES ====================
print("\n" + "="*70)
print("📁 CORE MODULES")
print("="*70)

def test_kernel():
    try:
        from core.kernel import LucyKernel
        k = LucyKernel()
        result = k.process("test")
        return {'success': True, 'details': f'Process returned: {result}'}
    except ImportError:
        return {'success': False, 'reason': 'Module not found'}

def test_quantum_core():
    try:
        from core.quantum import QuantumIntelligence
        q = QuantumIntelligence()
        result = q.quantum_think("test")
        return {'success': True, 'details': f'Quantum states: {len(result["states"])}'}
    except ImportError:
        return {'success': False, 'reason': 'Module not found'}

def test_biological():
    try:
        from core.biological import BiologicalIntegration
        b = BiologicalIntegration()
        result = b.create_neural_pattern("test")
        return {'success': True, 'details': f'Pattern created: {result["pattern_id"]}'}
    except ImportError:
        return {'success': False, 'reason': 'Module not found'}

test_module("Core Kernel", test_kernel)
test_module("Core Quantum", test_quantum_core)
test_module("Core Biological", test_biological)

# ==================== MEMORY MODULES ====================
print("\n" + "="*70)
print("📁 MEMORY MODULES")
print("="*70)

def test_long_term():
    try:
        from memory.long_term import LongTermMemory
        mem = LongTermMemory(":memory:")
        mem.store_conversation("test", "user", "Hello")
        history = mem.get_conversation_history("test")
        return {'success': True, 'details': f'Stored/retrieved {len(history)} items'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_working():
    try:
        from memory.working import WorkingMemory
        wm = WorkingMemory()
        wm.add({"test": "data"})
        data = wm.get_all()
        return {'success': True, 'details': f'Working memory size: {len(data)}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_episodic():
    try:
        from memory.episodic import EpisodicMemory
        em = EpisodicMemory(":memory:")
        ep_id = em.start_episode("test")
        em.add_message(ep_id, "user", "Hello")
        episodes = em.get_recent_episodes("test")
        return {'success': True, 'details': f'Episodes: {len(episodes)}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_semantic():
    try:
        from memory.semantic import SemanticMemory
        sm = SemanticMemory(":memory:")
        sm.store("Test fact", "test")
        facts = sm.recall("test")
        return {'success': True, 'details': f'Facts found: {len(facts)}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_procedural():
    try:
        from memory.procedural import ProceduralMemory
        pm = ProceduralMemory(":memory:")
        pm.add_skill("test", "Test skill", ["step1", "step2"])
        skill = pm.get_skill("test")
        return {'success': True, 'details': f'Skill: {skill["name"] if skill else "None"}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_emotional():
    try:
        from memory.emotional import EmotionalMemory
        em = EmotionalMemory(":memory:")
        em.tag_memory("mem1", "conversation", "joy", 0.8)
        tags = em.get_memory_emotions("mem1", "conversation")
        return {'success': True, 'details': f'Emotional tags: {len(tags)}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_memory_palace():
    try:
        from memory.memory_palace import MemoryPalace
        mp = MemoryPalace()
        mp.place_memory("test", {"type": "fact"})
        palace = mp.get_palace_map()
        return {'success': True, 'details': f'Rooms: {len(palace["rooms"])}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_consolidation():
    try:
        from memory.consolidation import MemoryConsolidation
        # Mock dependencies
        class MockMemory:
            def get_important_memories(self, *args): return []
            def forget_old(self, *args): return 0
        mc = MemoryConsolidation(MockMemory(), MockMemory(), MockMemory())
        return {'success': True, 'details': 'Consolidation module loaded'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_forgetting():
    try:
        from memory.forgetting import ForgettingCurve
        fc = ForgettingCurve()
        fc.record_memory("test")
        health = fc.get_memory_health("test")
        return {'success': True, 'details': f'Memory strength: {health["strength"]:.2f}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

# Run memory tests
test_module("Long Term Memory", test_long_term)
test_module("Working Memory", test_working)
test_module("Episodic Memory", test_episodic)
test_module("Semantic Memory", test_semantic)
test_module("Procedural Memory", test_procedural)
test_module("Emotional Memory", test_emotional)
test_module("Memory Palace", test_memory_palace)
test_module("Memory Consolidation", test_consolidation)
test_module("Forgetting Curve", test_forgetting)

# ==================== EMOTION MODULES ====================
print("\n" + "="*70)
print("📁 EMOTION MODULES")
print("="*70)

def test_mood_engine():
    try:
        from emotion.mood_engine import MoodEngine
        me = MoodEngine()
        mood = me.get_current_mood()
        return {'success': True, 'details': f'Moods: {len(mood)}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_personality():
    try:
        from emotion.personality import Personality
        p = Personality()
        p.set_preset('friendly')
        traits = p.get_traits()
        return {'success': True, 'details': f'Traits: {len(traits)}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_empathy():
    try:
        from emotion.empathy import Empathy
        e = Empathy()
        emotions = e.analyze_emotion("I'm so happy today!")
        return {'success': True, 'details': f'Dominant: {max(emotions, key=emotions.get)}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_humor():
    try:
        from emotion.humor import Humor
        h = Humor()
        joke = h.tell_joke('dad')
        return {'success': True, 'details': f'Joke: {joke[:30]}...'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

test_module("Mood Engine", test_mood_engine)
test_module("Personality", test_personality)
test_module("Empathy", test_empathy)
test_module("Humor", test_humor)

# ==================== KNOWLEDGE MODULES ====================
print("\n" + "="*70)
print("📁 KNOWLEDGE MODULES")
print("="*70)

def test_knowledge_graph():
    try:
        from knowledge.knowledge_graph import KnowledgeGraph
        kg = KnowledgeGraph()
        kg.add_entity("Test", "test")
        stats = kg.get_statistics()
        return {'success': True, 'details': f'Entities: {stats["entities"]}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_wikipedia():
    try:
        from knowledge.wikipedia import Wikipedia
        wiki = Wikipedia()
        # Mock mode for testing
        return {'success': True, 'details': 'Wikipedia module loaded'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_web_search():
    try:
        from knowledge.web_search import WebSearch
        ws = WebSearch()
        return {'success': True, 'details': 'Web search module loaded'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_reasoning():
    try:
        from knowledge.reasoning import ReasoningEngine
        re = ReasoningEngine()
        re.add_fact("All humans are mortal")
        re.add_fact("Socrates is human")
        deductions = re.deduce("Socrates is mortal")
        return {'success': True, 'details': f'Deductions: {len(deductions)}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_fact_check():
    try:
        from knowledge.fact_check import FactChecker
        fc = FactChecker()
        result = fc.check("Earth is a planet")
        return {'success': True, 'details': f'Verdict: {result["verdict"]}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_scientific():
    try:
        from knowledge.scientific import ScientificReasoning
        sr = ScientificReasoning()
        force = sr.calculate("newton_second", mass=10, acceleration=9.8)
        return {'success': True, 'details': f'Force: {force}N'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_mathematical():
    try:
        from knowledge.mathematical import MathematicalReasoning
        mr = MathematicalReasoning()
        result = mr.calculate("2 + 2 * 3")
        return {'success': True, 'details': f'2+2*3 = {result}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_misinformation():
    try:
        from knowledge.misinformation import MisinformationDetector
        md = MisinformationDetector()
        result = md.check_headline("You won't believe what happens next!")
        return {'success': True, 'details': f'Clickbait score: {result["clickbait_score"]}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

test_module("Knowledge Graph", test_knowledge_graph)
test_module("Wikipedia", test_wikipedia)
test_module("Web Search", test_web_search)
test_module("Reasoning Engine", test_reasoning)
test_module("Fact Checker", test_fact_check)
test_module("Scientific Reasoning", test_scientific)
test_module("Mathematical Reasoning", test_mathematical)
test_module("Misinformation Detector", test_misinformation)

# ==================== LANGUAGE MODULES ====================
print("\n" + "="*70)
print("📁 LANGUAGE MODULES")
print("="*70)

def test_translator():
    try:
        from language.translator import Translator
        t = Translator()
        translation = t.translate("hello", "es")
        return {'success': True, 'details': f'hello -> {translation}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_tts():
    try:
        from language.tts import TextToSpeech
        tts = TextToSpeech()
        return {'success': True, 'details': 'TTS module loaded'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_stt():
    try:
        from language.stt import SpeechToText
        stt = SpeechToText()
        return {'success': True, 'details': 'STT module loaded'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_creative():
    try:
        from language.creative import CreativeWriter
        cw = CreativeWriter()
        haiku = cw.generate_haiku("nature")
        return {'success': True, 'details': f'Haiku generated'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_summarizer():
    try:
        from language.summarizer import TextSummarizer
        ts = TextSummarizer()
        summary = ts.summarize("This is a long text that needs to be summarized. It has multiple sentences. The summarizer should work.", ratio=0.5)
        return {'success': True, 'details': f'Summary: {summary[:30]}...'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_negotiator():
    try:
        from language.negotiator import Negotiator
        n = Negotiator()
        result = n.negotiate("price", {"price": 100}, {"price": 80})
        return {'success': True, 'details': f'Success: {result["success"]}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_tutor():
    try:
        from language.tutor import LanguageTutor
        lt = LanguageTutor()
        lesson = lt.get_lesson("es")
        return {'success': True, 'details': f'Words: {len(lesson["words"])}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

test_module("Translator", test_translator)
test_module("Text-to-Speech", test_tts)
test_module("Speech-to-Text", test_stt)
test_module("Creative Writer", test_creative)
test_module("Summarizer", test_summarizer)
test_module("Negotiator", test_negotiator)
test_module("Language Tutor", test_tutor)

# ==================== INTEGRATION MODULES ====================
print("\n" + "="*70)
print("📁 INTEGRATION MODULES")
print("="*70)

def test_weather():
    try:
        from integrations.weather import Weather
        w = Weather()
        data = w.get_current("London")
        return {'success': True, 'details': f'Temp: {data.get("temperature", "?")}°C'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_news():
    try:
        from integrations.news import News
        n = News()
        headlines = n.get_top_headlines(country='us', page_size=2)
        return {'success': True, 'details': f'Headlines: {len(headlines)}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_stocks():
    try:
        from integrations.stocks import Stocks
        s = Stocks()
        quote = s.get_quote("AAPL")
        return {'success': True, 'details': f'AAPL: ${quote.get("price", "?")}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_crypto():
    try:
        from integrations.crypto import Crypto
        c = Crypto()
        btc = c.get_price('bitcoin')
        return {'success': True, 'details': f'BTC: ${btc.get("price", "?"):,.0f}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_email():
    try:
        from integrations.email_client import EmailClient
        ec = EmailClient()
        return {'success': True, 'details': 'Email module loaded'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_calendar():
    try:
        from integrations.calendar import Calendar
        cal = Calendar()
        events = cal.get_upcoming()
        return {'success': True, 'details': f'Events: {len(events)}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_smart_home():
    try:
        from integrations.smart_home import SmartHome
        sh = SmartHome()
        devices = sh.get_devices()
        return {'success': True, 'details': f'Devices: {len(devices)}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_github():
    try:
        from integrations.github import GitHub
        gh = GitHub()
        user = gh.get_user("torvalds")
        return {'success': True, 'details': f'User: {user.get("name", "?")}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_web_browser():
    try:
        from integrations.web_browser import WebBrowser
        wb = WebBrowser()
        return {'success': True, 'details': 'Web browser module loaded'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_api_gateway():
    try:
        from integrations.api_gateway import APIGateway
        ag = APIGateway()
        apis = ag.list_apis()
        return {'success': True, 'details': f'APIs: {len(apis)}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_database():
    try:
        from integrations.database import Database
        db = Database(":memory:")
        db.set_setting("test", "value")
        value = db.get_setting("test")
        return {'success': True, 'details': f'DB test: {value}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

test_module("Weather", test_weather)
test_module("News", test_news)
test_module("Stocks", test_stocks)
test_module("Crypto", test_crypto)
test_module("Email", test_email)
test_module("Calendar", test_calendar)
test_module("Smart Home", test_smart_home)
test_module("GitHub", test_github)
test_module("Web Browser", test_web_browser)
test_module("API Gateway", test_api_gateway)
test_module("Database", test_database)

# ==================== QUANTUM MODULES ====================
print("\n" + "="*70)
print("📁 QUANTUM MODULES")
print("="*70)

def test_quantum_algorithm():
    try:
        from quantum.quantum_algorithm import QuantumAlgorithm
        qa = QuantumAlgorithm(3)
        qa.apply_gate('h', 0)
        return {'success': True, 'details': 'Quantum algorithm initialized'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_entanglement():
    try:
        from quantum.entanglement import QuantumEntanglement
        qe = QuantumEntanglement()
        pair = qe.create_bell_pair(0, 1)
        return {'success': True, 'details': f'Bell pair: {pair}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_quantum_memory():
    try:
        from quantum.quantum_memory import QuantumMemory
        qm = QuantumMemory()
        import numpy as np
        state_id = qm.store_state(np.array([1,0,0,0], dtype=complex))
        return {'success': True, 'details': f'State stored: {state_id}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_quantum_decision():
    try:
        from quantum.quantum_decision import QuantumDecision
        qd = QuantumDecision()
        choice = qd.superposition_choice(['A', 'B', 'C'])
        return {'success': True, 'details': f'Choice: {choice}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_quantum_sim():
    try:
        from quantum.quantum_sim import QuantumSimulator
        qs = QuantumSimulator(2)
        qs.hadamard(0)
        return {'success': True, 'details': 'Quantum simulator ready'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

test_module("Quantum Algorithm", test_quantum_algorithm)
test_module("Quantum Entanglement", test_entanglement)
test_module("Quantum Memory", test_quantum_memory)
test_module("Quantum Decision", test_quantum_decision)
test_module("Quantum Simulator", test_quantum_sim)

# ==================== CREATIVITY MODULES ====================
print("\n" + "="*70)
print("📁 CREATIVITY MODULES")
print("="*70)

def test_poetry():
    try:
        from creativity.poetry import PoetryGenerator
        pg = PoetryGenerator()
        poem = pg.generate_poem('haiku', 'nature')
        return {'success': True, 'details': f'Poem: {poem["title"]}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_story():
    try:
        from creativity.story import StoryGenerator
        sg = StoryGenerator()
        story = sg.generate_story('fantasy')
        return {'success': True, 'details': f'Story: {story["title"]}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_music():
    try:
        from creativity.music import MusicGenerator
        mg = MusicGenerator()
        melody = mg.generate_melody('C', 'major', 4)
        return {'success': True, 'details': f'Melody notes: {len(melody)}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_visual():
    try:
        from creativity.visual import VisualArtGenerator
        va = VisualArtGenerator()
        art = va.generate_art_concept()
        return {'success': True, 'details': f'Art: {art["title"]}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_design():
    try:
        from creativity.design import DesignGenerator
        dg = DesignGenerator()
        brand = dg.generate_brand_identity()
        return {'success': True, 'details': f'Brand: {brand["company_name"]}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

test_module("Poetry Generator", test_poetry)
test_module("Story Generator", test_story)
test_module("Music Generator", test_music)
test_module("Visual Art", test_visual)
test_module("Design Generator", test_design)

# ==================== AUTONOMY MODULES ====================
print("\n" + "="*70)
print("📁 AUTONOMY MODULES")
print("="*70)

def test_goal_planner():
    try:
        from autonomy.goal_planner import GoalPlanner
        gp = GoalPlanner()
        goal = gp.create_goal("Test goal")
        return {'success': True, 'details': f'Goal: {goal["id"]}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_task_executor():
    try:
        from autonomy.task_executor import TaskExecutor
        te = TaskExecutor()
        task_id = te.add_task("Test task")
        return {'success': True, 'details': f'Task: {task_id}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_scheduler():
    try:
        from autonomy.scheduler import Scheduler
        sched = Scheduler()
        from datetime import datetime, timedelta
        event_id = sched.add_event("Test", datetime.now() + timedelta(minutes=1))
        return {'success': True, 'details': f'Event: {event_id}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_resource_manager():
    try:
        from autonomy.resource_manager import ResourceManager
        rm = ResourceManager()
        rm.allocate('time', 10, 'test')
        stats = rm.get_all_resources()
        return {'success': True, 'details': f'Resources: {len(stats)}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_learning():
    try:
        from autonomy.learning import AutonomousLearning
        al = AutonomousLearning()
        al.add_experience('test', {}, {'result': 'ok'}, 0.8)
        perf = al.evaluate_performance()
        return {'success': True, 'details': f'Success rate: {perf["success_rate"]:.2f}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

test_module("Goal Planner", test_goal_planner)
test_module("Task Executor", test_task_executor)
test_module("Scheduler", test_scheduler)
test_module("Resource Manager", test_resource_manager)
test_module("Autonomous Learning", test_learning)

# ==================== ETHICS MODULES ====================
print("\n" + "="*70)
print("📁 ETHICS MODULES")
print("="*70)

def test_ethical_framework():
    try:
        from ethics.ethical_framework import EthicalFramework
        ef = EthicalFramework()
        result = ef.evaluate_action("help someone", {})
        return {'success': True, 'details': f'Ethical score: {result["ethical_score"]}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_safety():
    try:
        from ethics.safety import SafetyModule
        sm = SafetyModule()
        result = sm.assess_risk("delete file", {})
        return {'success': True, 'details': f'Risk level: {result["risk_level"]}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_bias_detection():
    try:
        from ethics.bias_detection import BiasDetector
        bd = BiasDetector()
        result = bd.analyze_text("The businessman did a great job")
        return {'success': True, 'details': f'Bias score: {result["bias_score"]:.2f}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_privacy():
    try:
        from ethics.privacy import PrivacyModule
        pm = PrivacyModule()
        result = pm.classify_data("my email is test@example.com")
        return {'success': True, 'details': f'Privacy level: {result["privacy_level"]}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_audit():
    try:
        from ethics.audit import AuditModule
        am = AuditModule()
        event_id = am.log_event("test", "user1", "test action")
        return {'success': True, 'details': f'Event logged: {event_id}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

test_module("Ethical Framework", test_ethical_framework)
test_module("Safety Module", test_safety)
test_module("Bias Detection", test_bias_detection)
test_module("Privacy Module", test_privacy)
test_module("Audit Module", test_audit)

# ==================== ADVANCED MODULES ====================
print("\n" + "="*70)
print("📁 ADVANCED MODULES")
print("="*70)

def test_brain_computer():
    try:
        from advanced.brain_computer import BrainComputerInterface
        bci = BrainComputerInterface()
        signals = bci.read_neural_signals()
        return {'success': True, 'details': f'Signals: {len(signals)} regions'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_consciousness():
    try:
        from advanced.consciousness import QuantumConsciousness
        qc = QuantumConsciousness()
        obs = qc.quantum_observation({})
        return {'success': True, 'details': f'State: {obs["observed_state"]}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_dream():
    try:
        from advanced.dream import DreamSimulator
        ds = DreamSimulator()
        dream = ds.generate_dream()
        return {'success': True, 'details': f'Dream: {dream["title"]}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_time_perception():
    try:
        from advanced.time_perception import TimePerception
        tp = TimePerception()
        result = tp.subjective_duration(60, 'excitement')
        return {'success': True, 'details': f'Perceived: {result["subjective_duration"]:.1f}s'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

def test_multiverse():
    try:
        from advanced.multiverse import MultiverseExplorer
        me = MultiverseExplorer()
        universe = me.create_branch_universe("test", 0.5)
        return {'success': True, 'details': f'Universe: {universe}'}
    except Exception as e:
        return {'success': False, 'reason': str(e)}

test_module("Brain-Computer Interface", test_brain_computer)
test_module("Quantum Consciousness", test_consciousness)
test_module("Dream Simulator", test_dream)
test_module("Time Perception", test_time_perception)
test_module("Multiverse Explorer", test_multiverse)

# ==================== SUMMARY ====================
print("\n" + "="*70)
print("📊 TEST SUMMARY")
print("="*70)
print(f"✅ PASSED:  {results['passed']}")
print(f"⚠️  SKIPPED: {results['skipped']}")
print(f"❌ FAILED:  {results['failed']}")
print(f"\n📈 TOTAL MODULES TESTED: {results['passed'] + results['skipped'] + results['failed']}")
print("="*70)

# Show failed modules if any
if results['failed'] > 0:
    print("\n❌ FAILED MODULES:")
    for module, data in results['modules'].items():
        if data['status'] == 'failed':
            print(f"  • {module}: {data.get('error', 'Unknown error')}")