"""
API Gateway - REST API endpoint manager
"""

import requests
import json
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin

class APIGateway:
    """
    Manage and call external APIs
    """
    
    def __init__(self):
        self.apis = {}
        self.responses = {}
        
        # Register common APIs
        self._register_common_apis()
    
    def _register_common_apis(self):
        """Register common public APIs"""
        self.register_api('jsonplaceholder', 'https://jsonplaceholder.typicode.com')
        self.register_api('restcountries', 'https://restcountries.com/v3.1')
        self.register_api('dogapi', 'https://dog.ceo/api')
        self.register_api('catapi', 'https://catfact.ninja')
        self.register_api('jokeapi', 'https://v2.jokeapi.dev/joke')
        self.register_api('numbersapi', 'http://numbersapi.com')
    
    def register_api(self, name: str, base_url: str, headers: Dict = None):
        """
        Register a new API
        """
        self.apis[name] = {
            'base_url': base_url.rstrip('/'),
            'headers': headers or {}
        }
        print(f"✅ Registered API: {name}")
    
    def get(self, api_name: str, endpoint: str, params: Dict = None) -> Optional[Any]:
        """
        Make GET request to API
        """
        if api_name not in self.apis:
            return {'error': f'API {api_name} not registered'}
        
        api = self.apis[api_name]
        url = urljoin(api['base_url'] + '/', endpoint.lstrip('/'))
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=api['headers'],
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.responses[f"{api_name}:{endpoint}"] = data
                return data
            else:
                return self._get_fallback(api_name, endpoint)
                
        except Exception as e:
            print(f"API error ({api_name}): {e}")
            return self._get_fallback(api_name, endpoint)
    
    def post(self, api_name: str, endpoint: str, data: Dict = None) -> Optional[Any]:
        """
        Make POST request to API
        """
        if api_name not in self.apis:
            return {'error': f'API {api_name} not registered'}
        
        api = self.apis[api_name]
        url = urljoin(api['base_url'] + '/', endpoint.lstrip('/'))
        
        try:
            response = requests.post(
                url,
                json=data,
                headers=api['headers'],
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"API POST error: {e}")
            return None
    
    def _get_fallback(self, api_name: str, endpoint: str) -> Any:
        """Get fallback data for API"""
        fallbacks = {
            'jsonplaceholder': {
                'posts': [
                    {'id': 1, 'title': 'Sample Post', 'body': 'This is a fallback post'},
                    {'id': 2, 'title': 'Another Post', 'body': 'More fallback content'}
                ],
                'users': [
                    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
                    {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
                ]
            },
            'restcountries': {
                'all': [
                    {'name': {'common': 'United States'}, 'capital': ['Washington DC']},
                    {'name': {'common': 'United Kingdom'}, 'capital': ['London']}
                ]
            },
            'dogapi': {
                'breeds/list/all': {'message': {'retriever': [], 'hound': []}}
            },
            'catapi': {
                'facts': [{'fact': 'Cats sleep 16 hours a day', 'length': 28}]
            }
        }
        
        # Try to find matching fallback
        for key, value in fallbacks.get(api_name, {}).items():
            if key in endpoint:
                return value
        
        # Generic fallback
        return {'message': 'API unavailable', 'fallback': True}
    
    def list_apis(self) -> List[str]:
        """List all registered APIs"""
        return list(self.apis.keys())
    
    def get_last_response(self, api_name: str = None, endpoint: str = None) -> Any:
        """Get last response from API"""
        if api_name and endpoint:
            return self.responses.get(f"{api_name}:{endpoint}")
        return self.responses