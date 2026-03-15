"""
Stock Market Integration - Yahoo Finance
"""

import requests
import time
from typing import Dict, List, Optional
from datetime import datetime

class Stocks:
    """
    Fetches stock market data
    """
    
    def __init__(self):
        self.base_url = "https://query1.finance.yahoo.com/v8/finance/chart"
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes
        
        # Common stock symbols
        self.popular_stocks = {
            'AAPL': 'Apple Inc.',
            'GOOGL': 'Alphabet Inc.',
            'MSFT': 'Microsoft Corporation',
            'AMZN': 'Amazon.com Inc.',
            'TSLA': 'Tesla Inc.',
            'META': 'Meta Platforms Inc.',
            'NFLX': 'Netflix Inc.',
            'NVDA': 'NVIDIA Corporation',
            'JPM': 'JPMorgan Chase & Co.',
            'V': 'Visa Inc.',
            'JNJ': 'Johnson & Johnson',
            'WMT': 'Walmart Inc.',
            'PG': 'Procter & Gamble Co.',
            'UNH': 'UnitedHealth Group Inc.',
            'HD': 'Home Depot Inc.',
            'DIS': 'The Walt Disney Co.',
            'MA': 'Mastercard Inc.',
            'BAC': 'Bank of America Corp.',
            'PFE': 'Pfizer Inc.',
            'KO': 'Coca-Cola Co.'
        }
    
    def get_quote(self, symbol: str) -> Optional[Dict]:
        """
        Get current stock quote
        """
        symbol = symbol.upper()
        cache_key = f"quote_{symbol}"
        
        if cache_key in self.cache:
            cached, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                return cached
        
        try:
            url = f"{self.base_url}/{symbol}"
            params = {
                'range': '1d',
                'interval': '1m'
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200 and 'chart' in data:
                result = data['chart']['result'][0]
                meta = result['meta']
                
                quote = {
                    'symbol': symbol,
                    'name': self.popular_stocks.get(symbol, symbol),
                    'price': meta.get('regularMarketPrice', 0),
                    'previous_close': meta.get('previousClose', 0),
                    'change': meta.get('regularMarketPrice', 0) - meta.get('previousClose', 0),
                    'change_percent': ((meta.get('regularMarketPrice', 0) - meta.get('previousClose', 0)) / meta.get('previousClose', 1)) * 100,
                    'day_high': meta.get('dayHigh', 0),
                    'day_low': meta.get('dayLow', 0),
                    'volume': meta.get('regularMarketVolume', 0),
                    'market_cap': meta.get('marketCap', 0),
                    'timestamp': datetime.now().isoformat()
                }
                
                self.cache[cache_key] = (quote, time.time())
                return quote
            else:
                return self._get_fallback_quote(symbol)
                
        except Exception as e:
            print(f"Stock quote error: {e}")
            return self._get_fallback_quote(symbol)
    
    def get_historical(self, symbol: str, range: str = '1mo') -> Optional[List[Dict]]:
        """
        Get historical stock data
        """
        symbol = symbol.upper()
        cache_key = f"hist_{symbol}_{range}"
        
        if cache_key in self.cache:
            cached, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout * 2:
                return cached
        
        try:
            url = f"{self.base_url}/{symbol}"
            params = {
                'range': range,
                'interval': '1d'
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200 and 'chart' in data:
                result = data['chart']['result'][0]
                timestamps = result.get('timestamp', [])
                quotes = result.get('indicators', {}).get('quote', [{}])[0]
                
                historical = []
                for i, ts in enumerate(timestamps):
                    historical.append({
                        'date': datetime.fromtimestamp(ts).isoformat(),
                        'open': quotes.get('open', [])[i] if i < len(quotes.get('open', [])) else 0,
                        'high': quotes.get('high', [])[i] if i < len(quotes.get('high', [])) else 0,
                        'low': quotes.get('low', [])[i] if i < len(quotes.get('low', [])) else 0,
                        'close': quotes.get('close', [])[i] if i < len(quotes.get('close', [])) else 0,
                        'volume': quotes.get('volume', [])[i] if i < len(quotes.get('volume', [])) else 0
                    })
                
                self.cache[cache_key] = (historical, time.time())
                return historical
            else:
                return None
                
        except Exception as e:
            print(f"Historical data error: {e}")
            return None
    
    def get_popular(self) -> List[Dict]:
        """
        Get popular stocks
        """
        quotes = []
        for symbol, name in list(self.popular_stocks.items())[:10]:
            quote = self.get_quote(symbol)
            if quote:
                quotes.append(quote)
        return quotes
    
    def search(self, query: str) -> List[Dict]:
        """
        Search for stocks
        """
        query = query.upper()
        results = []
        
        for symbol, name in self.popular_stocks.items():
            if query in symbol or query in name.upper():
                results.append({
                    'symbol': symbol,
                    'name': name
                })
        
        return results[:10]
    
    def _get_fallback_quote(self, symbol: str) -> Dict:
        """Generate fallback stock quote"""
        import random
        
        price = random.uniform(50, 500)
        prev_close = price * random.uniform(0.95, 1.05)
        
        return {
            'symbol': symbol,
            'name': self.popular_stocks.get(symbol, 'Unknown Company'),
            'price': round(price, 2),
            'previous_close': round(prev_close, 2),
            'change': round(price - prev_close, 2),
            'change_percent': round(((price - prev_close) / prev_close) * 100, 2),
            'day_high': round(price * 1.02, 2),
            'day_low': round(price * 0.98, 2),
            'volume': random.randint(1000000, 10000000),
            'market_cap': round(price * random.uniform(1e9, 1e12), 0),
            'timestamp': datetime.now().isoformat(),
            '_fallback': True
        }