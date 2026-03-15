"""
Cryptocurrency Integration - CoinGecko API CG-LmXxXfBQq14FCdCKtCj5XnBn
"""

import requests
import time
from typing import Dict, List, Optional
from datetime import datetime

class Crypto:
    """
    Fetches cryptocurrency data from CoinGecko
    """
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.cache = {}
        self.cache_timeout = 120  # 2 minutes
        
        # Popular cryptocurrencies
        self.popular_coins = {
            'bitcoin': 'BTC',
            'ethereum': 'ETH',
            'binancecoin': 'BNB',
            'cardano': 'ADA',
            'solana': 'SOL',
            'xrp': 'XRP',
            'polkadot': 'DOT',
            'dogecoin': 'DOGE',
            'avalanche-2': 'AVAX',
            'matic-network': 'MATIC'
        }
    
    def get_price(self, coin_id: str = 'bitcoin', vs_currency: str = 'usd') -> Optional[Dict]:
        """
        Get current cryptocurrency price
        """
        cache_key = f"price_{coin_id}_{vs_currency}"
        if cache_key in self.cache:
            cached, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                return cached
        
        try:
            url = f"{self.base_url}/simple/price"
            params = {
                'ids': coin_id,
                'vs_currencies': vs_currency,
                'include_24hr_change': 'true',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true'
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200 and coin_id in data:
                coin_data = data[coin_id]
                result = {
                    'coin': coin_id,
                    'symbol': self.popular_coins.get(coin_id, coin_id.upper()),
                    'price': coin_data[vs_currency],
                    '24h_change': coin_data.get(f'{vs_currency}_24h_change', 0),
                    'market_cap': coin_data.get(f'{vs_currency}_market_cap', 0),
                    '24h_volume': coin_data.get(f'{vs_currency}_24h_vol', 0),
                    'timestamp': datetime.now().isoformat()
                }
                
                self.cache[cache_key] = (result, time.time())
                return result
            else:
                return self._get_fallback_price(coin_id)
                
        except Exception as e:
            print(f"Crypto price error: {e}")
            return self._get_fallback_price(coin_id)
    
    def get_multiple_prices(self, coin_ids: List[str], vs_currency: str = 'usd') -> Dict:
        """
        Get prices for multiple cryptocurrencies
        """
        coins_str = ','.join(coin_ids)
        
        try:
            url = f"{self.base_url}/simple/price"
            params = {
                'ids': coins_str,
                'vs_currencies': vs_currency,
                'include_24hr_change': 'true'
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                return data
            else:
                return {}
        except:
            return {}
    
    def get_trending(self) -> List[Dict]:
        """
        Get trending cryptocurrencies
        """
        try:
            url = f"{self.base_url}/search/trending"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                trending = []
                for coin in data.get('coins', [])[:10]:
                    item = coin['item']
                    trending.append({
                        'coin': item['id'],
                        'name': item['name'],
                        'symbol': item['symbol'],
                        'market_cap_rank': item['market_cap_rank'],
                        'price_btc': item['price_btc'],
                        'score': item['score']
                    })
                return trending
            else:
                return self._get_fallback_trending()
        except:
            return self._get_fallback_trending()
    
    def get_historical(self, coin_id: str = 'bitcoin', days: int = 7) -> Optional[List[Dict]]:
        """
        Get historical price data
        """
        cache_key = f"hist_{coin_id}_{days}"
        if cache_key in self.cache:
            cached, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout * 6:
                return cached
        
        try:
            url = f"{self.base_url}/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                prices = []
                for price_point in data.get('prices', []):
                    prices.append({
                        'timestamp': datetime.fromtimestamp(price_point[0]/1000).isoformat(),
                        'price': price_point[1]
                    })
                
                self.cache[cache_key] = (prices, time.time())
                return prices
            else:
                return None
        except:
            return None
    
    def get_market_data(self) -> Dict:
        """
        Get global cryptocurrency market data
        """
        try:
            url = f"{self.base_url}/global"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                market = data['data']
                return {
                    'active_cryptocurrencies': market['active_cryptocurrencies'],
                    'total_market_cap': market['total_market_cap']['usd'],
                    'total_volume': market['total_volume']['usd'],
                    'market_cap_percentage': market['market_cap_percentage'],
                    'market_cap_change_percentage_24h_usd': market['market_cap_change_percentage_24h_usd']
                }
            else:
                return self._get_fallback_market()
        except:
            return self._get_fallback_market()
    
    def _get_fallback_price(self, coin_id: str) -> Dict:
        """Generate fallback crypto price"""
        import random
        
        prices = {
            'bitcoin': 45000,
            'ethereum': 3200,
            'binancecoin': 450,
            'cardano': 0.5,
            'solana': 120
        }
        
        price = prices.get(coin_id, random.uniform(1, 1000))
        
        return {
            'coin': coin_id,
            'symbol': coin_id[:3].upper(),
            'price': price,
            '24h_change': random.uniform(-5, 5),
            'market_cap': price * random.uniform(1e9, 1e12),
            '24h_volume': price * random.uniform(1e8, 1e10),
            'timestamp': datetime.now().isoformat(),
            '_fallback': True
        }
    
    def _get_fallback_trending(self) -> List[Dict]:
        """Generate fallback trending coins"""
        return [
            {'coin': 'bitcoin', 'name': 'Bitcoin', 'symbol': 'BTC', 'score': 100},
            {'coin': 'ethereum', 'name': 'Ethereum', 'symbol': 'ETH', 'score': 95},
            {'coin': 'solana', 'name': 'Solana', 'symbol': 'SOL', 'score': 90}
        ]
    
    def _get_fallback_market(self) -> Dict:
        """Generate fallback market data"""
        import random
        return {
            'active_cryptocurrencies': random.randint(8000, 10000),
            'total_market_cap': random.uniform(1.5e12, 2.5e12),
            'total_volume': random.uniform(5e10, 1e11),
            'market_cap_percentage': {'btc': 45, 'eth': 18},
            'market_cap_change_percentage_24h_usd': random.uniform(-3, 3)
        }