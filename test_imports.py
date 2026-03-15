# test_imports.py
print("📦 TESTING ALL MODULE IMPORTS")
print("="*60)

modules = [
    ('core', ['kernel', 'quantum', 'biological']),
    ('memory', ['long_term', 'working', 'episodic', 'semantic', 'procedural', 
                'emotional', 'memory_palace', 'consolidation', 'forgetting']),
    ('emotion', ['mood_engine', 'personality', 'empathy', 'humor']),
    ('knowledge', ['knowledge_graph', 'wikipedia', 'web_search', 'reasoning', 
                   'fact_check', 'scientific', 'mathematical', 'misinformation']),
    ('language', ['translator', 'tts', 'stt', 'creative', 'summarizer', 'negotiator', 'tutor']),
    ('integrations', ['weather', 'news', 'stocks', 'crypto', 'email_client', 
                      'calendar', 'smart_home', 'github', 'web_browser', 'api_gateway', 'database']),
    ('quantum', ['quantum_algorithm', 'entanglement', 'quantum_memory', 'quantum_decision', 'quantum_sim']),
    ('creativity', ['poetry', 'story', 'music', 'visual', 'design']),
    ('autonomy', ['goal_planner', 'task_executor', 'scheduler', 'resource_manager', 'learning']),
    ('ethics', ['ethical_framework', 'safety', 'bias_detection', 'privacy', 'audit']),
    ('advanced', ['brain_computer', 'consciousness', 'dream', 'time_perception', 'multiverse'])
]

success = 0
fail = 0

for folder, files in modules:
    print(f"\n📁 {folder.upper()}/")
    for file in files:
        try:
            exec(f"from {folder}.{file} import *")
            print(f"  ✅ {file}.py")
            success += 1
        except Exception as e:
            print(f"  ❌ {file}.py - {str(e)[:50]}")
            fail += 1

print("\n" + "="*60)
print(f"📊 SUMMARY: {success} modules loaded, {fail} failed")
print("="*60)