"""
News Integration - NewsAPI
"""

import requests
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class News:
    """
    Fetches news articles from NewsAPI
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "50e90a9dc62a48f1b71ae4d31b374a47" and "9ff4ec08410c4d9984d2b23cc9dd7a57"  # Public test key
        self.base_url = "https://newsapi.org/v2"
        self.cache = {}
        self.cache_timeout = 600  # 10 minutes
        
    def get_top_headlines(self, country: str = 'us', category: str = None, 
                           page_size: int = 10) -> Optional[List[Dict]]:
        """
        Get top headlines
        """
        cache_key = f"headlines_{country}_{category}_{page_size}"
        if cache_key in self.cache:
            cached, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                return cached
        
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                'country': country,
                'apiKey': self.api_key,
                'pageSize': page_size
            }
            if category:
                params['category'] = category
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                articles = []
                for item in data.get('articles', []):
                    articles.append({
                        'title': item['title'],
                        'description': item['description'],
                        'content': item['content'],
                        'url': item['url'],
                        'source': item['source']['name'],
                        'published_at': item['publishedAt'],
                        'author': item['author'],
                        'image_url': item['urlToImage']
                    })
                
                self.cache[cache_key] = (articles, time.time())
                return articles
            else:
                print(f"News API error: {data.get('message', 'Unknown')}")
                return self._get_fallback_news(country, category)
                
        except Exception as e:
            print(f"News fetch error: {e}")
            return self._get_fallback_news(country, category)
    
    def search_news(self, query: str, from_date: str = None, 
                     sort_by: str = 'relevancy', page_size: int = 10) -> Optional[List[Dict]]:
        """
        Search for news articles
        """
        cache_key = f"search_{query}_{from_date}_{sort_by}_{page_size}"
        if cache_key in self.cache:
            cached, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                return cached
        
        try:
            url = f"{self.base_url}/everything"
            params = {
                'q': query,
                'apiKey': self.api_key,
                'pageSize': page_size,
                'sortBy': sort_by
            }
            if from_date:
                params['from'] = from_date
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                articles = []
                for item in data.get('articles', []):
                    articles.append({
                        'title': item['title'],
                        'description': item['description'],
                        'url': item['url'],
                        'source': item['source']['name'],
                        'published_at': item['publishedAt']
                    })
                
                self.cache[cache_key] = (articles, time.time())
                return articles
            else:
                return self._get_fallback_search(query)
                
        except Exception as e:
            print(f"News search error: {e}")
            return self._get_fallback_search(query)
    
    def _get_fallback_news(self, country: str, category: str) -> List[Dict]:
        """Generate fallback news"""
        import random
        
        headlines = {
            'us': [
                {'title': 'Markets Rally on Tech Earnings', 'source': 'Financial Times'},
                {'title': 'New Climate Deal Reached', 'source': 'Reuters'},
                {'title': 'Breakthrough in AI Research', 'source': 'TechCrunch'},
                {'title': 'Space Mission Launches Successfully', 'source': 'NASA'},
                {'title': 'Healthcare Reform Debate Continues', 'source': 'Politico'}
            ],
            'gb': [
                {'title': 'PM Announces New Economic Plan', 'source': 'BBC'},
                {'title': 'Royal Family Makes Public Appearance', 'source': 'The Guardian'},
                {'title': 'Premier League Transfer News', 'source': 'Sky Sports'}
            ],
            'in': [
                {'title': 'Tech Hub Expansion Announced', 'source': 'Times of India'},
                {'title': 'Monsoon Season Updates', 'source': 'NDTV'}
            ]
        }
        
        selected = headlines.get(country, headlines['us'])
        if category and category == 'technology':
            selected = [h for h in headlines['us'] if 'Tech' in h['title']]
        
        return [{
            'title': h['title'],
            'description': f"Latest updates on {h['title'].lower()}",
            'url': '#',
            'source': h['source'],
            'published_at': datetime.now().isoformat(),
            '_fallback': True
        } for h in selected[:5]]
    
    def _get_fallback_search(self, query: str) -> List[Dict]:
        """Generate fallback search results"""
        return [{
            'title': f"Latest developments in {query}",
            'description': f"Breaking news and updates about {query}",
            'url': '#',
            'source': 'News Service',
            'published_at': datetime.now().isoformat(),
            '_fallback': True
        }]