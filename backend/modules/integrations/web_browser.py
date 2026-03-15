"""
Web Browser Automation - Selenium-based browsing
"""

import time
import webbrowser
from typing import Dict, List, Optional
from urllib.parse import quote

class WebBrowser:
    """
    Web browser control and automation
    """
    
    def __init__(self, use_selenium: bool = False):
        self.use_selenium = use_selenium
        self.history = []
        self.bookmarks = []
        self.current_url = None
        
    def open(self, url: str, new_tab: bool = True) -> bool:
        """
        Open a URL in browser
        """
        try:
            if not url.startswith('http'):
                url = 'https://' + url
            
            if new_tab:
                webbrowser.open_new_tab(url)
            else:
                webbrowser.open_new(url)
            
            self.history.append({
                'url': url,
                'timestamp': time.time()
            })
            self.current_url = url
            print(f"✅ Opened {url}")
            return True
        except Exception as e:
            print(f"Browser error: {e}")
            return False
    
    def search(self, query: str, engine: str = 'google') -> str:
        """
        Perform web search
        """
        search_urls = {
            'google': f"https://www.google.com/search?q={quote(query)}",
            'bing': f"https://www.bing.com/search?q={quote(query)}",
            'duckduckgo': f"https://duckduckgo.com/?q={quote(query)}",
            'yahoo': f"https://search.yahoo.com/search?p={quote(query)}"
        }
        
        url = search_urls.get(engine, search_urls['google'])
        self.open(url)
        return f"Searching {engine} for: {query}"
    
    def wikipedia(self, query: str) -> str:
        """
        Open Wikipedia article
        """
        url = f"https://en.wikipedia.org/wiki/{quote(query.replace(' ', '_'))}"
        self.open(url)
        return f"Opening Wikipedia: {query}"
    
    def youtube(self, query: str) -> str:
        """
        Search YouTube
        """
        url = f"https://www.youtube.com/results?search_query={quote(query)}"
        self.open(url)
        return f"Searching YouTube: {query}"
    
    def maps(self, location: str) -> str:
        """
        Open Google Maps
        """
        url = f"https://www.google.com/maps/search/{quote(location)}"
        self.open(url)
        return f"Opening Maps: {location}"
    
    def translate(self, text: str, target_lang: str = 'es') -> str:
        """
        Open Google Translate
        """
        url = f"https://translate.google.com/?sl=auto&tl={target_lang}&text={quote(text)}"
        self.open(url)
        return f"Translating to {target_lang}"
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """
        Get browsing history
        """
        return sorted(self.history[-limit:], key=lambda x: x['timestamp'], reverse=True)
    
    def add_bookmark(self, url: str, title: str = None) -> bool:
        """
        Add a bookmark
        """
        self.bookmarks.append({
            'url': url,
            'title': title or url,
            'timestamp': time.time()
        })
        return True
    
    def get_bookmarks(self) -> List[Dict]:
        """
        Get all bookmarks
        """
        return self.bookmarks
    
    def clear_history(self):
        """Clear browsing history"""
        self.history = []
    
    def open_news(self, topic: str = None) -> str:
        """
        Open news site
        """
        if topic:
            url = f"https://news.google.com/search?q={quote(topic)}"
        else:
            url = "https://news.google.com"
        self.open(url)
        return "Opening Google News"
    
    def open_weather(self, location: str) -> str:
        """
        Open weather forecast
        """
        url = f"https://weather.com/weather/today/l/{quote(location)}"
        self.open(url)
        return f"Opening weather for {location}"
    
    def open_social(self, platform: str) -> str:
        """
        Open social media platform
        """
        platforms = {
            'twitter': 'https://twitter.com',
            'facebook': 'https://facebook.com',
            'instagram': 'https://instagram.com',
            'linkedin': 'https://linkedin.com',
            'reddit': 'https://reddit.com',
            'github': 'https://github.com'
        }
        
        url = platforms.get(platform.lower(), platforms['twitter'])
        self.open(url)
        return f"Opening {platform}"