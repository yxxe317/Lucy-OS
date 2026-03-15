"""
Wikipedia Integration - Fetch and query Wikipedia content
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any

class Wikipedia:
    """
    Wikipedia API wrapper for knowledge retrieval
    """
    
    def __init__(self, language: str = "en"):
        self.language = language
        self.base_url = f"https://{language}.wikipedia.org/api/rest_v1"
        self.search_url = f"https://{language}.wikipedia.org/w/api.php"
        self.cache = {}
        self.rate_limit = 0.5  # 500ms between requests
        self.last_request = 0
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for articles
        """
        self._rate_limit()
        
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'format': 'json',
            'srlimit': limit
        }
        
        try:
            response = requests.get(self.search_url, params=params)
            data = response.json()
            
            results = []
            for item in data.get('query', {}).get('search', []):
                results.append({
                    'title': item['title'],
                    'page_id': item['pageid'],
                    'snippet': item['snippet'],
                    'word_count': item['wordcount'],
                    'timestamp': item['timestamp']
                })
            
            return results
        except Exception as e:
            print(f"Wikipedia search error: {e}")
            return []
    
    def get_summary(self, title: str, sentences: int = 5) -> Optional[str]:
        """
        Get article summary
        """
        # Check cache
        cache_key = f"summary_{title}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        self._rate_limit()
        
        params = {
            'action': 'query',
            'titles': title,
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
            'exsentences': sentences,
            'format': 'json'
        }
        
        try:
            response = requests.get(self.search_url, params=params)
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            for page_id, page in pages.items():
                if 'extract' in page:
                    summary = page['extract']
                    self.cache[cache_key] = summary
                    return summary
            
            return None
        except Exception as e:
            print(f"Wikipedia summary error: {e}")
            return None
    
    def get_full_article(self, title: str) -> Optional[Dict]:
        """
        Get full article content
        """
        self._rate_limit()
        
        params = {
            'action': 'parse',
            'page': title,
            'format': 'json',
            'prop': 'text|links|categories|sections'
        }
        
        try:
            response = requests.get(self.search_url, params=params)
            data = response.json()
            
            parse = data.get('parse', {})
            return {
                'title': parse.get('title'),
                'page_id': parse.get('pageid'),
                'text': parse.get('text', {}).get('*', ''),
                'links': [link['*'] for link in parse.get('links', [])],
                'categories': [cat['*'] for cat in parse.get('categories', [])],
                'sections': parse.get('sections', [])
            }
        except Exception as e:
            print(f"Wikipedia article error: {e}")
            return None
    
    def get_random_articles(self, count: int = 5) -> List[str]:
        """
        Get random article titles
        """
        self._rate_limit()
        
        params = {
            'action': 'query',
            'list': 'random',
            'rnnamespace': 0,
            'rnlimit': count,
            'format': 'json'
        }
        
        try:
            response = requests.get(self.search_url, params=params)
            data = response.json()
            
            return [item['title'] for item in data.get('query', {}).get('random', [])]
        except Exception as e:
            print(f"Wikipedia random error: {e}")
            return []
    
    def get_wikidata(self, title: str) -> Optional[Dict]:
        """
        Get Wikidata entity for article
        """
        self._rate_limit()
        
        # First get page info to get Wikidata ID
        params = {
            'action': 'query',
            'titles': title,
            'prop': 'pageprops',
            'ppprop': 'wikibase_item',
            'format': 'json'
        }
        
        try:
            response = requests.get(self.search_url, params=params)
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            for page in pages.values():
                wikidata_id = page.get('pageprops', {}).get('wikibase_item')
                if wikidata_id:
                    return self._fetch_wikidata(wikidata_id)
            
            return None
        except Exception as e:
            print(f"Wikidata error: {e}")
            return None
    
    def _fetch_wikidata(self, entity_id: str) -> Optional[Dict]:
        """
        Fetch Wikidata entity
        """
        url = f"https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            entity = data.get('entities', {}).get(entity_id, {})
            claims = entity.get('claims', {})
            
            # Extract basic info
            result = {
                'id': entity_id,
                'labels': {},
                'descriptions': {},
                'claims': {}
            }
            
            # Get labels
            for lang, label in entity.get('labels', {}).items():
                result['labels'][lang] = label['value']
            
            # Get descriptions
            for lang, desc in entity.get('descriptions', {}).items():
                result['descriptions'][lang] = desc['value']
            
            # Get claims (simplified)
            for prop, values in claims.items():
                result['claims'][prop] = []
                for claim in values:
                    if 'mainsnak' in claim and 'datavalue' in claim['mainsnak']:
                        result['claims'][prop].append(claim['mainsnak']['datavalue']['value'])
            
            return result
        except Exception as e:
            print(f"Wikidata fetch error: {e}")
            return None
    
    def _rate_limit(self):
        """Ensure we don't exceed rate limits"""
        elapsed = time.time() - self.last_request
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request = time.time()
    
    def clear_cache(self):
        """Clear cached results"""
        self.cache.clear()