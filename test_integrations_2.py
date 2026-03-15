# test_integrations_2.py
from integrations.github import GitHub
from integrations.web_browser import WebBrowser
from integrations.api_gateway import APIGateway
from integrations.database import Database

print("="*60)
print("🧪 TESTING ADDITIONAL INTEGRATION MODULES")
print("="*60)

# ==================== TEST GITHUB ====================
print("\n🐙 1. TESTING GITHUB MODULE")
print("-" * 40)

github = GitHub()

print("\n📡 Fetching user 'torvalds'...")
user = github.get_user("torvalds")
if user:
    print(f"✅ User: {user.get('name', user['login'])}")
    print(f"   Repos: {user['public_repos']}")
    print(f"   Followers: {user['followers']}")
else:
    print("❌ Failed to get user")

print("\n📡 Fetching repo 'torvalds/linux'...")
repo = github.get_repo("torvalds", "linux")
if repo:
    print(f"✅ Repo: {repo['full_name']}")
    print(f"   Stars: {repo['stars']}")
    print(f"   Language: {repo['language']}")
else:
    print("❌ Failed to get repo")

print("\n📡 Searching for 'machine learning'...")
results = github.search_repositories("machine learning", limit=3)
if results:
    print(f"✅ Found {len(results)} results")
    for r in results:
        print(f"   • {r['name']} - {r['stars']} ⭐")
else:
    print("❌ Failed to search")

# ==================== TEST WEB BROWSER ====================
print("\n\n🌐 2. TESTING WEB BROWSER MODULE")
print("-" * 40)

browser = WebBrowser()

print("\n📡 Testing search...")
browser.search("artificial intelligence", engine="google")
browser.search("latest technology news", engine="duckduckgo")

print("\n📡 Testing Wikipedia...")
browser.wikipedia("Python programming")

print("\n📡 Testing YouTube...")
browser.youtube("machine learning tutorial")

print("\n📡 Testing Maps...")
browser.maps("Eiffel Tower, Paris")

print("\n📡 Getting history...")
history = browser.get_history(limit=5)
print(f"✅ Browser history: {len(history)} entries")

# ==================== TEST API GATEWAY ====================
print("\n\n🔌 3. TESTING API GATEWAY")
print("-" * 40)

gateway = APIGateway()

print(f"\n📡 Registered APIs: {gateway.list_apis()}")

print("\n📡 Testing JSONPlaceholder...")
posts = gateway.get('jsonplaceholder', 'posts/1')
if posts:
    print(f"✅ Post: {posts.get('title', 'N/A')}")
else:
    print("❌ Failed to get post")

print("\n📡 Testing RestCountries...")
countries = gateway.get('restcountries', 'name/usa')
if countries:
    print(f"✅ Got {len(countries) if isinstance(countries, list) else 1} countries")
else:
    print("❌ Failed to get countries")

print("\n📡 Testing Cat Facts...")
cats = gateway.get('catapi', 'fact')
if cats:
    print(f"✅ Cat fact: {cats.get('fact', 'N/A')}")
else:
    print("❌ Failed to get cat fact")

# ==================== TEST DATABASE ====================
print("\n\n💾 4. TESTING DATABASE MODULE")
print("-" * 40)

db = Database()

print("\n📡 Testing user preferences...")
db.save_preference("test_user", {"theme": "dark", "language": "en"})
prefs = db.get_preference("test_user")
print(f"✅ Preferences: {prefs}")

print("\n📡 Testing conversations...")
db.save_conversation("test_user", "user", "Hello Lucy!")
db.save_conversation("test_user", "lucy", "Hi there! How can I help?")
convos = db.get_conversations("test_user", limit=5)
print(f"✅ Saved {len(convos)} conversations")

print("\n📡 Testing tasks...")
task_id = db.add_task("test_user", "Learn Python", priority=1)
db.add_task("test_user", "Build Lucy", "Create AI assistant", priority=2)
tasks = db.get_tasks("test_user")
print(f"✅ Added {len(tasks)} tasks")

if tasks:
    db.complete_task(tasks[0]['id'])
    completed = db.get_tasks("test_user", status="completed")
    print(f"✅ Completed {len(completed)} tasks")

print("\n📡 Testing notes...")
note_id = db.save_note("test_user", "Ideas", "Make Lucy smarter", tags=["ai", "ideas"])
notes = db.get_notes("test_user")
print(f"✅ Saved {len(notes)} notes")

print("\n📡 Testing settings...")
db.set_setting("test_key", "test_value")
value = db.get_setting("test_key")
print(f"✅ Setting: {value}")

print("\n" + "="*60)
print("✅ ADDITIONAL INTEGRATION TESTS COMPLETE")
print("="*60)