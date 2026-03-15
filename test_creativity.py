# test_creativity.py
import time  # Add this line at the top
from creativity.poetry import PoetryGenerator
from creativity.story import StoryGenerator
from creativity.music import MusicGenerator
from creativity.visual import VisualArtGenerator
from creativity.design import DesignGenerator
from autonomy.goal_planner import GoalPlanner
from autonomy.task_executor import TaskExecutor
from autonomy.scheduler import Scheduler
from autonomy.resource_manager import ResourceManager
from autonomy.learning import AutonomousLearning
from datetime import datetime, timedelta
from creativity.poetry import PoetryGenerator
from creativity.story import StoryGenerator
from creativity.music import MusicGenerator
from creativity.visual import VisualArtGenerator
from creativity.design import DesignGenerator

print("="*60)
print("🎨 TESTING CREATIVITY MODULES")
print("="*60)

# ==================== TEST POETRY ====================
print("\n📝 1. TESTING POETRY GENERATOR")
print("-" * 40)

poetry = PoetryGenerator()

# Test haiku
print("\n📡 Generating haiku...")
haiku = poetry.generate_poem(form='haiku', theme='nature')
print(f"✅ {haiku['title']} ({haiku['form']})")
for line in haiku['lines']:
    print(f"   {line}")

# Test sonnet
print("\n📡 Generating sonnet...")
sonnet = poetry.generate_poem(form='sonnet', theme='love')
print(f"✅ {sonnet['title']} ({sonnet['form']})")
print(f"   First line: {sonnet['lines'][0][:50]}...")

# Test limerick
print("\n📡 Generating limerick...")
limerick = poetry.generate_poem(form='limerick', theme='fun')
print(f"✅ {limerick['title']}")
for line in limerick['lines']:
    print(f"   {line}")

# Test analysis
print("\n📡 Analyzing poem...")
analysis = poetry.analyze_poem(haiku)
print(f"✅ Analysis: {analysis['line_count']} lines, {analysis['word_count']} words")

print(f"\n✅ Poetic forms available: {poetry.get_poetic_forms()}")

# ==================== TEST STORY ====================
print("\n\n📖 2. TESTING STORY GENERATOR")
print("-" * 40)

story_gen = StoryGenerator()

# Test story generation
print("\n📡 Generating fantasy story...")
story = story_gen.generate_story(genre='fantasy', length='medium')
print(f"✅ Title: {story['title']}")
print(f"   Genre: {story['genre']}")
print(f"   Logline: {story['logline']}")
print(f"   Protagonist: {story['protagonist']}")
print(f"   Antagonist: {story['antagonist']}")
print(f"   Setting: {story['setting']}")
print(f"   Theme: {story['theme']}")
print(f"   Plot twist: {story['plot_twist']}")

# Test character generation
print("\n📡 Generating character...")
character = story_gen.generate_character()
print(f"✅ Character: {character['name']}")
print(f"   Role: {character['role']}")
print(f"   Personality: {character['personality']}")
print(f"   Goal: {character['goal']}")
print(f"   Backstory: {character['backstory']}")

# Test dialogue
print("\n📡 Generating dialogue...")
dialogue = story_gen.generate_dialogue('Hero', 'Villain', 'a final confrontation')
print(f"✅ Dialogue ({len(dialogue)} lines):")
for line in dialogue[:3]:
    print(f"   {line}")

# ==================== TEST MUSIC ====================
print("\n\n🎵 3. TESTING MUSIC GENERATOR")
print("-" * 40)

music = MusicGenerator()

# Test melody
print("\n📡 Generating melody in C major...")
melody = music.generate_melody(key='C', scale='major', length=8)
print(f"✅ Generated {len(melody)} notes")
for note in melody[:4]:
    print(f"   {note['note']} ({note['duration']})")

# Test chord progression
print("\n📡 Generating chord progression...")
chords = music.generate_chord_progression(key='C', mode='major', length=4)
print(f"✅ Progression: {' - '.join([c['root'].split('3')[0] for c in chords])}")

# Test bassline
print("\n📡 Generating bassline...")
bassline = music.generate_bassline(chords, pattern='walking')
print(f"✅ Generated {len(bassline)} bass notes")

# Test drum pattern
print("\n📡 Generating drum pattern...")
drums = music.generate_drum_pattern(genre='rock', bars=2)
print(f"✅ Drums: {', '.join(drums.keys())}")

# Test song structure
print("\n📡 Generating song structure...")
structure = music.generate_song_structure(genre='pop')
print(f"✅ Structure: {structure}")

# Test tempo suggestion
tempo = music.suggest_tempo('jazz', mood='medium')
print(f"✅ Suggested tempo: {tempo} BPM")

# ==================== TEST VISUAL ART ====================
print("\n\n🎨 4. TESTING VISUAL ART GENERATOR")
print("-" * 40)

visual = VisualArtGenerator()

# Test art concept
print("\n📡 Generating art concept...")
art = visual.generate_art_concept()
print(f"✅ Title: {art['title']}")
print(f"   Movement: {art['movement']}")
print(f"   Medium: {art['medium']}")
print(f"   Description: {art['description'][:100]}...")

# Test color palette
print("\n📡 Generating color palette...")
palette = visual.generate_palette(mood='ocean')
print(f"✅ Palette: {palette}")

# Test composition sketch
print("\n📡 Generating composition sketch...")
sketch = visual.generate_composition_sketch()
print(f"✅ Composition: {sketch['composition_type']}")
print(f"   Elements: {len(sketch['elements'])} shapes")

# Test art critique
print("\n📡 Generating art critique...")
critique = visual.generate_art_critique(art)
print(f"✅ Critique: {critique}")

# Test artist suggestions
print("\n📡 Suggesting artists...")
artists = visual.suggest_artists(movement='impressionism')
print(f"✅ Impressionist artists: {', '.join(artists[:3])}")

# ==================== TEST DESIGN ====================
print("\n\n🎯 5. TESTING DESIGN GENERATOR")
print("-" * 40)

design = DesignGenerator()

# Test brand identity
print("\n📡 Generating brand identity...")
brand = design.generate_brand_identity()
print(f"✅ Company: {brand['company_name']}")
print(f"   Tagline: {brand['tagline']}")
print(f"   Archetype: {brand['archetype']}")
print(f"   Logo type: {brand['logo_type']}")
print(f"   Colors: {brand['primary_color']}, {brand['secondary_color']}")
print(f"   Typography: {brand['typography']['heading_font']}")

# Test UI layout
print("\n📡 Generating UI layout...")
ui = design.generate_ui_layout(page_type='website')
print(f"✅ Layout patterns: {', '.join(ui['patterns'][:3])}...")
print(f"   Grid system: {ui['grid_system']}")
print(f"   Interactive elements: {', '.join(ui['interactive_elements'])}")

# Test poster concept
print("\n📡 Generating poster concept...")
poster = design.generate_poster_concept()
print(f"✅ Poster: {poster['title']}")
print(f"   Style: {poster['style']}")
print(f"   Message: {poster['message']}")

# Test mood board
print("\n📡 Generating mood board...")
mood = design.generate_mood_board(theme='futuristic')
print(f"✅ Mood board: {mood['theme']}")
print(f"   Mood: {mood['mood']}")
print(f"   Keywords: {', '.join(mood['keywords'])}")

print("\n" + "="*60)
print("✅ ALL CREATIVITY MODULES TESTS COMPLETE")
print("="*60)
# Add to the end of test_creativity.py
from autonomy.goal_planner import GoalPlanner
from autonomy.task_executor import TaskExecutor
from autonomy.scheduler import Scheduler
from autonomy.resource_manager import ResourceManager
from autonomy.learning import AutonomousLearning

print("\n\n🤖 6. TESTING AUTONOMY MODULES")
print("-" * 40)

# Test Goal Planner
print("\n📡 Testing Goal Planner...")
gp = GoalPlanner()
goal = gp.create_goal("Learn Python programming", priority=2)
subgoals = gp.decompose_goal(goal['id'])
print(f"✅ Created goal: {goal['description']}")
print(f"   Subgoals: {len(subgoals)}")

# Test Task Executor
print("\n📡 Testing Task Executor...")
te = TaskExecutor()
task_id = te.add_task("Test Task", priority=1)
te.start_worker()
time.sleep(2)
te.stop_worker()
status = te.get_task_status(task_id)
print(f"✅ Task status: {status['status']}")

# Test Scheduler
print("\n📡 Testing Scheduler...")
sched = Scheduler()
from datetime import datetime, timedelta
event_time = datetime.now() + timedelta(minutes=1)
event_id = sched.add_event("Test Event", event_time)
upcoming = sched.get_upcoming_events()
print(f"✅ Created event: {len(upcoming)} upcoming")

# Test Resource Manager
print("\n📡 Testing Resource Manager...")
rm = ResourceManager()
rm.allocate('time', 30, 'task1')
rm.allocate('energy', 20, 'task1')
resources = rm.get_all_resources()
print(f"✅ Time used: {resources['time']['used']} mins")
print(f"   Energy used: {resources['energy']['used']}%")

# Test Autonomous Learning
print("\n📡 Testing Autonomous Learning...")
al = AutonomousLearning()
al.add_experience('action1', {'context': 'test'}, {'result': 'success'}, 0.8)
prediction = al.predict_outcome('action1', {'context': 'test'})
al.learn_skill('coding', [{'data': 'x'}] * 10)
perf = al.evaluate_performance()
print(f"✅ Prediction confidence: {prediction['confidence']:.2f}")
print(f"   Success rate: {perf['success_rate']:.2f}")