"""
Web Search - DuckDuckGo and fallback search engines
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any
import urllib.parse

class WebSearch:
    """
    Web search using multiple backends
    """
    
    def __init__(self):
        self.cache = {}
        self.last_request = 0
        self.rate_limit = 1.0  # 1 second between requests
        
        # Search engines
        self.engines = {
            'duckduckgo': self._search_duckduckgo,
            'brave': self._search_brave,
            'fallback': self._search_fallback
        }
        
        self.current_engine = 'duckduckgo'
    
    def search(self, query: str, max_results: int = 10) -> Dict:
        """
        Perform web search
        """
        # Check cache
        cache_key = f"{query}_{max_results}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Try each engine until we get results
        results = None
        for engine_name in ['duckduckgo', 'brave', 'fallback']:
            try:
                results = self.engines[engine_name](query, max_results)
                if results and results.get('results'):
                    self.current_engine = engine_name
                    break
            except Exception as e:
                print(f"Search engine {engine_name} failed: {e}")
                continue
        
        if results:
            self.cache[cache_key] = results
            return results
        
        return {'results': [], 'total': 0, 'engine': 'none'}
    
    def _search_duckduckgo(self, query: str, max_results: int) -> Dict:
        """
        Search using DuckDuckGo API
        """
        self._rate_limit()
        
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1&skip_disambig=1"
        
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            
            results = []
            
            # Add abstract if available
            if data.get('Abstract'):
                results.append({
                    'title': data.get('Heading', 'Summary'),
                    'snippet': data['Abstract'],
                    'url': data.get('AbstractURL', ''),
                    'source': 'DuckDuckGo'
                })
            
            # Add related topics
            for topic in data.get('RelatedTopics', [])[:max_results-1]:
                if isinstance(topic, dict) and 'Text' in topic:
                    results.append({
                        'title': topic.get('FirstURL', '').split('/')[-1].replace('_', ' '),
                        'snippet': topic['Text'],
                        'url': topic.get('FirstURL', ''),
                        'source': 'DuckDuckGo'
                    })
            
            return {
                'results': results,
                'total': len(results),
                'engine': 'duckduckgo'
            }
        except Exception as e:
            print(f"DuckDuckGo error: {e}")
            return {'results': [], 'total': 0, 'engine': 'duckduckgo', 'error': str(e)}
    
    def _search_brave(self, query: str, max_results: int) -> Dict:
        """
        Search using Brave Search API (requires API key)
        """
        # This would need an API key - using fallback for now
        return self._search_fallback(query, max_results)
    
    def _search_fallback(self, query: str, max_results: int) -> Dict:
        """
        Fallback search using Wikipedia and other sources
        """
        results = []
        
        # Try Wikipedia
        from knowledge.wikipedia import Wikipedia
        wiki = Wikipedia()
        wiki_results = wiki.search(query, limit=max_results)
        
        for item in wiki_results:
            results.append({
                'title': item['title'],
                'snippet': item['snippet'].replace('<span class="searchmatch">', '').replace('</span>', ''),
                'url': f"https://en.wikipedia.org/wiki/{item['title'].replace(' ', '_')}",
                'source': 'Wikipedia'
            })
        
        return {
            'results': results[:max_results],
            'total': len(results),
            'engine': 'fallback'
        }
    
    def get_news(self, topic: str, max_results: int = 5) -> List[Dict]:
        """
        Get news articles on topic
        """
        # Simplified news search
        query = f"{topic} news"
        results = self.search(query, max_results)
        return results.get('results', [])
    
    def get_weather(self, location: str) -> Optional[Dict]:
        """
        Get weather for location (simplified)
        """
        # This would use a weather API
        return {
            'location': location,
            'temperature': '22°C',
            'conditions': 'Partly cloudy',
            'humidity': '65%',
            'wind': '10 km/h'
        }
    
    def _rate_limit(self):
        """Rate limiting for API calls"""
        elapsed = time.time() - self.last_request
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request = time.time()
    
    def clear_cache(self):
        """Clear search cache"""
        self.cache.clear()