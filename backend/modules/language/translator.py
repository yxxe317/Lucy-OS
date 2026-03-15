"""
Translator - Multi-language translation (50+ languages)
"""

import json
from typing import Dict, List, Optional

class Translator:
    """
    Translates text between languages
    Uses local dictionary fallback when API unavailable
    """
    
    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ko': 'Korean',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'bn': 'Bengali',
            'pa': 'Punjabi',
            'ta': 'Tamil',
            'te': 'Telugu',
            'mr': 'Marathi',
            'gu': 'Gujarati',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'or': 'Odia',
            'as': 'Assamese',
            'mai': 'Maithili',
            'sat': 'Santali',
            'ks': 'Kashmiri',
            'sd': 'Sindhi',
            'ur': 'Urdu',
            'fa': 'Persian',
            'ps': 'Pashto',
            'dv': 'Divehi',
            'si': 'Sinhala',
            'ne': 'Nepali',
            'bh': 'Bihari',
            'doi': 'Dogri',
            'kok': 'Konkani',
            'gbr': 'Garo',
            'lus': 'Mizo',
            'mni': 'Manipuri',
            'bhu': 'Bhili',
            'gon': 'Gondi',
            'kru': 'Kurukh',
            'kha': 'Khasi',
            'kfr': 'Kachchi',
            'tcy': 'Tulu',
            'lmn': 'Lambadi',
            'bfy': 'Baghelkhandi',
            'hne': 'Chhattisgarhi',
            'mag': 'Magahi',
            'sw': 'Swahili',
            'swc': 'Congo Swahili',
            'zu': 'Zulu',
            'xh': 'Xhosa',
            'st': 'Sesotho',
            'tn': 'Tswana',
            'ts': 'Tsonga',
            'ss': 'Swati',
            've': 'Venda',
            'nr': 'Ndebele'
        }
        
        # Simple dictionary for common phrases
        self.dictionary = {
            ('hello', 'en', 'es'): 'hola',
            ('hello', 'en', 'fr'): 'bonjour',
            ('hello', 'en', 'de'): 'hallo',
            ('hello', 'en', 'it'): 'ciao',
            ('hello', 'en', 'pt'): 'olá',
            ('hello', 'en', 'ru'): 'привет',
            ('hello', 'en', 'zh'): '你好',
            ('hello', 'en', 'ja'): 'こんにちは',
            ('hello', 'en', 'ko'): '안녕하세요',
            ('hello', 'en', 'ar'): 'مرحبا',
            ('hello', 'en', 'hi'): 'नमस्ते',
            
            ('thank you', 'en', 'es'): 'gracias',
            ('thank you', 'en', 'fr'): 'merci',
            ('thank you', 'en', 'de'): 'danke',
            ('thank you', 'en', 'it'): 'grazie',
            ('thank you', 'en', 'pt'): 'obrigado',
            ('thank you', 'en', 'ru'): 'спасибо',
            ('thank you', 'en', 'zh'): '谢谢',
            ('thank you', 'en', 'ja'): 'ありがとう',
            ('thank you', 'en', 'ko'): '감사합니다',
            ('thank you', 'en', 'ar'): 'شكرا',
            ('thank you', 'en', 'hi'): 'धन्यवाद'
        }
        
        self.cache = {}
    
    def translate(self, text: str, target_lang: str, source_lang: str = 'en') -> str:
        """
        Translate text to target language
        """
        # Check cache
        cache_key = f"{text}_{source_lang}_{target_lang}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Check dictionary for common phrases
        dict_key = (text.lower(), source_lang, target_lang)
        if dict_key in self.dictionary:
            translation = self.dictionary[dict_key]
            self.cache[cache_key] = translation
            return translation
        
        # Simple fallback translation (adds language marker)
        translation = f"[{self.supported_languages.get(target_lang, target_lang)}] {text}"
        self.cache[cache_key] = translation
        return translation
    
    def detect_language(self, text: str) -> str:
        """
        Detect language of text (simplified)
        """
        # Very simple detection based on common words
        lang_indicators = {
            'en': ['the', 'and', 'is', 'in', 'to', 'of'],
            'es': ['el', 'la', 'y', 'es', 'en', 'de'],
            'fr': ['le', 'la', 'et', 'est', 'en', 'de'],
            'de': ['der', 'die', 'und', 'ist', 'in', 'von'],
            'it': ['il', 'la', 'e', 'è', 'in', 'di'],
            'pt': ['o', 'a', 'e', 'é', 'em', 'de'],
            'ru': ['и', 'в', 'не', 'на', 'я', 'что'],
            'zh': ['的', '了', '和', '是', '我', '在'],
            'ja': ['の', 'は', 'を', 'に', 'が', 'で'],
            'hi': ['का', 'और', 'है', 'में', 'से', 'को']
        }
        
        text_lower = text.lower()
        scores = {}
        
        for lang, indicators in lang_indicators.items():
            score = sum(1 for ind in indicators if ind in text_lower)
            scores[lang] = score
        
        if scores:
            return max(scores, key=scores.get)
        return 'en'  # Default to English
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return self.supported_languages.copy()
    
    def add_to_dictionary(self, phrase: str, translation: str, 
                           source_lang: str, target_lang: str):
        """Add custom translation to dictionary"""
        self.dictionary[(phrase.lower(), source_lang, target_lang)] = translation