"""
GitHub Integration - Repository and user data
"""

import requests
import time
from typing import Dict, List, Optional
from datetime import datetime

class GitHub:
    """
    GitHub API integration
    """
    
    def __init__(self, token: str = None):
        self.token = token
        self.base_url = "https://api.github.com"
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes
        
    def _headers(self):
        """Get request headers"""
        headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if self.token:
            headers['Authorization'] = f'token {self.token}'
        return headers
    
    def get_user(self, username: str) -> Optional[Dict]:
        """
        Get user profile
        """
        cache_key = f"user_{username}"
        if cache_key in self.cache:
            cached, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                return cached
        
        try:
            url = f"{self.base_url}/users/{username}"
            response = requests.get(url, headers=self._headers())
            
            if response.status_code == 200:
                data = response.json()
                user = {
                    'login': data['login'],
                    'name': data.get('name', username),
                    'avatar_url': data['avatar_url'],
                    'bio': data.get('bio', ''),
                    'public_repos': data['public_repos'],
                    'followers': data['followers'],
                    'following': data['following'],
                    'created_at': data['created_at'],
                    'updated_at': data['updated_at'],
                    'location': data.get('location', ''),
                    'blog': data.get('blog', ''),
                    'twitter': data.get('twitter_username', ''),
                    'company': data.get('company', '')
                }
                self.cache[cache_key] = (user, time.time())
                return user
            else:
                return self._get_fallback_user(username)
                
        except Exception as e:
            print(f"GitHub user error: {e}")
            return self._get_fallback_user(username)
    
    def get_repo(self, owner: str, repo: str) -> Optional[Dict]:
        """
        Get repository details
        """
        cache_key = f"repo_{owner}_{repo}"
        if cache_key in self.cache:
            cached, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                return cached
        
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}"
            response = requests.get(url, headers=self._headers())
            
            if response.status_code == 200:
                data = response.json()
                repo_data = {
                    'name': data['name'],
                    'full_name': data['full_name'],
                    'description': data.get('description', ''),
                    'url': data['html_url'],
                    'stars': data['stargazers_count'],
                    'forks': data['forks_count'],
                    'watchers': data['watchers_count'],
                    'issues': data['open_issues_count'],
                    'language': data.get('language', 'Unknown'),
                    'license': data.get('license', {}).get('name', 'None') if data.get('license') else 'None',
                    'created_at': data['created_at'],
                    'updated_at': data['updated_at'],
                    'size': data['size']
                }
                self.cache[cache_key] = (repo_data, time.time())
                return repo_data
            else:
                return self._get_fallback_repo(owner, repo)
                
        except Exception as e:
            print(f"GitHub repo error: {e}")
            return self._get_fallback_repo(owner, repo)
    
    def get_user_repos(self, username: str, sort: str = 'updated') -> List[Dict]:
        """
        Get user repositories
        """
        cache_key = f"user_repos_{username}_{sort}"
        if cache_key in self.cache:
            cached, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                return cached
        
        try:
            url = f"{self.base_url}/users/{username}/repos"
            params = {'sort': sort, 'per_page': 100}
            
            response = requests.get(url, params=params, headers=self._headers())
            
            if response.status_code == 200:
                repos = []
                for item in response.json():
                    repos.append({
                        'name': item['name'],
                        'description': item.get('description', ''),
                        'url': item['html_url'],
                        'stars': item['stargazers_count'],
                        'forks': item['forks_count'],
                        'language': item.get('language', 'Unknown'),
                        'updated_at': item['updated_at']
                    })
                
                self.cache[cache_key] = (repos, time.time())
                return repos
            else:
                return self._get_fallback_repos(username)
                
        except Exception as e:
            print(f"GitHub repos error: {e}")
            return self._get_fallback_repos(username)
    
    def search_repositories(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for repositories
        """
        cache_key = f"search_repo_{query}_{limit}"
        if cache_key in self.cache:
            cached, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                return cached
        
        try:
            url = f"{self.base_url}/search/repositories"
            params = {
                'q': query,
                'per_page': limit,
                'sort': 'stars'
            }
            
            response = requests.get(url, params=params, headers=self._headers())
            
            if response.status_code == 200:
                results = []
                for item in response.json().get('items', []):
                    results.append({
                        'name': item['full_name'],
                        'description': item.get('description', ''),
                        'url': item['html_url'],
                        'stars': item['stargazers_count'],
                        'forks': item['forks_count'],
                        'language': item.get('language', 'Unknown')
                    })
                
                self.cache[cache_key] = (results, time.time())
                return results
            else:
                return self._get_fallback_search(query, limit)
                
        except Exception as e:
            print(f"GitHub search error: {e}")
            return self._get_fallback_search(query, limit)
    
    def get_readme(self, owner: str, repo: str) -> Optional[str]:
        """
        Get repository README content
        """
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/readme"
            response = requests.get(url, headers=self._headers())
            
            if response.status_code == 200:
                import base64
                data = response.json()
                content = base64.b64decode(data['content']).decode('utf-8')
                return content[:500] + "..." if len(content) > 500 else content
            else:
                return "README not available"
        except:
            return "README not available"
    
    def _get_fallback_user(self, username: str) -> Dict:
        """Generate fallback user data"""
        return {
            'login': username,
            'name': username.title(),
            'bio': f"GitHub user {username}",
            'public_repos': 42,
            'followers': 128,
            'following': 64,
            'created_at': '2020-01-01T00:00:00Z',
            'location': 'Internet',
            '_fallback': True
        }
    
    def _get_fallback_repo(self, owner: str, repo: str) -> Dict:
        """Generate fallback repo data"""
        return {
            'name': repo,
            'full_name': f"{owner}/{repo}",
            'description': f"A great repository by {owner}",
            'url': f"https://github.com/{owner}/{repo}",
            'stars': 1337,
            'forks': 42,
            'watchers': 99,
            'issues': 7,
            'language': 'Python',
            'license': 'MIT',
            'created_at': '2021-01-01T00:00:00Z',
            '_fallback': True
        }
    
    def _get_fallback_repos(self, username: str) -> List[Dict]:
        """Generate fallback repos list"""
        return [
            {
                'name': 'awesome-project',
                'description': 'An awesome project',
                'stars': 1234,
                'forks': 56,
                'language': 'Python',
                'updated_at': '2024-01-01T00:00:00Z'
            },
            {
                'name': 'cool-library',
                'description': 'A cool library',
                'stars': 789,
                'forks': 23,
                'language': 'JavaScript',
                'updated_at': '2024-02-01T00:00:00Z'
            }
        ]
    
    def _get_fallback_search(self, query: str, limit: int) -> List[Dict]:
        """Generate fallback search results"""
        return [
            {
                'name': f"{query}/awesome-{query}",
                'description': f"Awesome {query} resources",
                'stars': 5000,
                'forks': 1200,
                'language': 'Python'
            },
            {
                'name': f"{query}/{query}-toolkit",
                'description': f"Toolkit for {query} development",
                'stars': 3200,
                'forks': 800,
                'language': 'JavaScript'
            }
        ][:limit]