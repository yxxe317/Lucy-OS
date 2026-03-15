"""
Weather Integration - OpenWeatherMap API
"""

import requests
import json
import time
from typing import Dict, Optional, List
from datetime import datetime

class Weather:
    """
    Fetches weather data from OpenWeatherMap
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "5abf7dffdafcb0e4422bfc43cbd7ce68"  # Free tier key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.cache = {}
        self.cache_timeout = 1800  # 30 minutes
        
    def get_current(self, location: str) -> Optional[Dict]:
        """
        Get current weather for location
        """
        # Check cache
        cache_key = f"current_{location}"
        if cache_key in self.cache:
            cached, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                return cached
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                weather = {
                    'location': data['name'],
                    'country': data['sys']['country'],
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'wind_speed': data['wind']['speed'],
                    'wind_direction': data['wind'].get('deg', 0),
                    'clouds': data['clouds']['all'],
                    'timestamp': datetime.now().isoformat()
                }
                
                # Cache result
                self.cache[cache_key] = (weather, time.time())
                return weather
            else:
                print(f"Weather API error: {data.get('message', 'Unknown error')}")
                return self._get_fallback_weather(location)
                
        except Exception as e:
            print(f"Weather fetch error: {e}")
            return self._get_fallback_weather(location)
    
    def get_forecast(self, location: str, days: int = 5) -> Optional[List[Dict]]:
        """
        Get weather forecast
        """
        cache_key = f"forecast_{location}_{days}"
        if cache_key in self.cache:
            cached, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                return cached
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': days * 8  # 8 forecasts per day
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                forecasts = []
                for item in data['list']:
                    forecast = {
                        'datetime': item['dt_txt'],
                        'temperature': item['main']['temp'],
                        'feels_like': item['main']['feels_like'],
                        'humidity': item['main']['humidity'],
                        'description': item['weather'][0]['description'],
                        'wind_speed': item['wind']['speed'],
                        'clouds': item['clouds']['all'],
                        'rain': item.get('rain', {}).get('3h', 0)
                    }
                    forecasts.append(forecast)
                
                self.cache[cache_key] = (forecasts, time.time())
                return forecasts
            else:
                return None
                
        except Exception as e:
            print(f"Forecast error: {e}")
            return None
    
    def get_by_coords(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Get weather by coordinates
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                return {
                    'location': data['name'],
                    'country': data['sys']['country'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity']
                }
            return None
        except:
            return None
    
    def _get_fallback_weather(self, location: str) -> Dict:
        """
        Generate fallback weather data when API fails
        """
        import random
        conditions = ['clear sky', 'few clouds', 'scattered clouds', 'broken clouds', 'shower rain', 'rain', 'thunderstorm', 'snow', 'mist']
        
        return {
            'location': location.split(',')[0],
            'country': 'Unknown',
            'temperature': random.randint(5, 35),
            'feels_like': random.randint(3, 33),
            'humidity': random.randint(40, 90),
            'pressure': random.randint(980, 1030),
            'description': random.choice(conditions),
            'icon': '01d',
            'wind_speed': random.randint(0, 15),
            'wind_direction': random.randint(0, 360),
            'clouds': random.randint(0, 100),
            'timestamp': datetime.now().isoformat(),
            '_fallback': True
        }
    
    def get_air_pollution(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Get air pollution data
        """
        try:
            url = f"{self.base_url}/air_pollution"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200 and 'list' in data:
                components = data['list'][0]['components']
                return {
                    'aqi': data['list'][0]['main']['aqi'],
                    'co': components['co'],
                    'no': components['no'],
                    'no2': components['no2'],
                    'o3': components['o3'],
                    'so2': components['so2'],
                    'pm2_5': components['pm2_5'],
                    'pm10': components['pm10'],
                    'nh3': components['nh3']
                }
            return None
        except:
            return None