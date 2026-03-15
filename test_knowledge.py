# test_knowledge.py
from knowledge.knowledge_graph import KnowledgeGraph
from knowledge.wikipedia import Wikipedia
from knowledge.web_search import WebSearch
from knowledge.reasoning import ReasoningEngine
from knowledge.fact_check import FactChecker
from knowledge.scientific import ScientificReasoning
from knowledge.mathematical import MathematicalReasoning
from knowledge.misinformation import MisinformationDetector

print("="*50)
print("TESTING LUCY KNOWLEDGE MODULES")
print("="*50)

# Test Knowledge Graph
print("\n1. Testing Knowledge Graph...")
kg = KnowledgeGraph()
entity_id = kg.add_entity("Earth", "planet")
print(f"✓ Added entity: Earth")
print(f"  Stats: {kg.get_statistics()}")

# Test Wikipedia
print("\n2. Testing Wikipedia...")
wiki = Wikipedia()
results = wiki.search("Python programming", limit=2)
print(f"✓ Found {len(results)} Wikipedia results")

# Test Web Search
print("\n3. Testing Web Search...")
web = WebSearch()
results = web.search("artificial intelligence", max_results=2)
print(f"✓ Search results: {results.get('total', 0)}")

# Test Reasoning
print("\n4. Testing Reasoning Engine...")
reason = ReasoningEngine(kg)
reason.add_fact("Earth orbits Sun")
reason.add_fact("Sun is a star")
deductions = reason.deduce("Earth orbits star")
print(f"✓ Deductions: {len(deductions)}")

# Test Fact Check (FIXED: added closing quote)
print("\n5. Testing Fact Checker...")
checker = FactChecker(kg, wiki, web)
result = checker.check("Earth is a planet")
print(f"✓ Verdict: {result['verdict']}")

# Test Scientific
print("\n6. Testing Scientific Reasoning...")
science = ScientificReasoning()
force = science.calculate("newton_second", mass=10, acceleration=9.8)
print(f"✓ Force calculation: {force} N")

# Test Mathematical (FIXED: added closing quote)
print("\n7. Testing Mathematical Reasoning...")
math_engine = MathematicalReasoning()
result = math_engine.calculate("2 + 2 * 3")
print(f"✓ Calculation: 2 + 2 * 3 = {result}")
solutions = math_engine.solve_equation("2x + 3 = 7")
print(f"✓ Equation solved: x = {solutions[0]}")

# Test Misinformation
print("\n8. Testing Misinformation Detector...")
detector = MisinformationDetector()
headline = "You won't believe what happens next!!!"
analysis = detector.check_headline(headline)
print(f"✓ Clickbait score: {analysis['clickbait_score']}")

print("\n" + "="*50)
print("✓ KNOWLEDGE TESTS COMPLETE")
print("="*50)