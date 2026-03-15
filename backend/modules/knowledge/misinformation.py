"""
Misinformation Detection - Fake news and bias detection
"""

import re
from typing import Dict, List, Optional, Set, Tuple

class MisinformationDetector:
    """
    Detects potential misinformation and bias in text
    """
    
    def __init__(self):
        self.clickbait_patterns = [
            r'you won\'t believe',
            r'shocked?',
            r'what happens next',
            r'jaw-dropping',
            r'mind-blowing',
            r'this will blow your mind',
            r'the reason why',
            r'doctors hate this',
            r'single trick',
            r'secret they don\'t want you to know',
            r'viral',
            r'unbelievable',
            r'^OMG',
            r'^WOW',
            r'^BREAKING:',
            r'^URGENT:'
        ]
        
        self.emotional_manipulation = [
            r'shocking',
            r'outrageous',
            r'disgusting',
            r'unbelievable',
            r'terrifying',
            r'incredible',
            r'miraculous',
            r'heartbreaking',
            r'heartwarming',
            r'pray for',
            r'thoughts and prayers'
        ]
        
        self.pseudoscience_indicators = [
            r'detox',
            r'cleanse',
            r'natural cure',
            r'secret remedy',
            r'big pharma',
            r'government cover-up',
            r'they don\'t want you to know',
            r'hidden truth',
            r'awakening',
            r'vibrational',
            r'quantum healing',
            r'energy field',
            r'crystal therapy'
        ]
        
        self.conspiracy_indicators = [
            r'illuminati',
            r'new world order',
            r'deep state',
            r'chemtrails',
            r'flat earth',
            r'moon landing hoax',
            r'fake news',
            r'alternative facts',
            r'controlled opposition',
            r'cabal',
            r'globalist',
            r'elite pedophile ring'
        ]
        
        self.reliable_domains = {
            'reuters.com', 'apnews.com', 'bbc.com', 'bbc.co.uk',
            'nytimes.com', 'wsj.com', 'economist.com', 'nature.com',
            'science.org', 'who.int', 'cdc.gov', 'nasa.gov',
            'nih.gov', 'harvard.edu', 'ox.ac.uk', 'cam.ac.uk'
        }
        
        self.unreliable_domains = {
            'infowars.com', 'breitbart.com', 'naturalnews.com',
            'beforeitsnews.com', 'collective-evolution.com',
            'yournewswire.com', 'prisonplanet.com', 'wakingtimes.com'
        }
    
    def analyze(self, text: str, url: str = None) -> Dict:
        """
        Analyze text for potential misinformation
        """
        results = {
            'risk_score': 0.0,
            'warnings': [],
            'indicators': {},
            'source_reliability': 0.5,
            'url': url,
            'is_likely_misinformation': False
        }
        
        text_lower = text.lower()
        
        # Check for clickbait
        clickbait_count = self._check_patterns(text_lower, self.clickbait_patterns)
        if clickbait_count > 0:
            results['indicators']['clickbait'] = clickbait_count
            results['warnings'].append(f"Contains clickbait phrases ({clickbait_count})")
            results['risk_score'] += clickbait_count * 0.1
        
        # Check for emotional manipulation
        emotion_count = self._check_patterns(text_lower, self.emotional_manipulation)
        if emotion_count > 0:
            results['indicators']['emotional_manipulation'] = emotion_count
            results['warnings'].append("Uses emotional manipulation language")
            results['risk_score'] += emotion_count * 0.1
        
        # Check for pseudoscience
        pseudo_count = self._check_patterns(text_lower, self.pseudoscience_indicators)
        if pseudo_count > 0:
            results['indicators']['pseudoscience'] = pseudo_count
            results['warnings'].append("Contains pseudoscientific claims")
            results['risk_score'] += pseudo_count * 0.15
        
        # Check for conspiracy theories
        conspiracy_count = self._check_patterns(text_lower, self.conspiracy_indicators)
        if conspiracy_count > 0:
            results['indicators']['conspiracy'] = conspiracy_count
            results['warnings'].append("Contains conspiracy theory indicators")
            results['risk_score'] += conspiracy_count * 0.2
        
        # Check source reliability
        if url:
            results['source_reliability'] = self._check_source(url)
            if results['source_reliability'] < 0.3:
                results['warnings'].append("Source is known to be unreliable")
                results['risk_score'] += 0.3
            elif results['source_reliability'] > 0.8:
                results['risk_score'] -= 0.2
        
        # Check for missing evidence
        if 'evidence' not in text_lower and 'study' not in text_lower and 'research' not in text_lower:
            results['warnings'].append("No evidence or sources cited")
            results['risk_score'] += 0.1
        
        # Check for extreme language
        extreme_words = ['always', 'never', 'everyone', 'no one', 'all', 'none', 'completely', 'totally']
        extreme_count = sum(1 for word in extreme_words if word in text_lower)
        if extreme_count > 3:
            results['indicators']['extreme_language'] = extreme_count
            results['risk_score'] += 0.1
        
        # Normalize risk score
        results['risk_score'] = min(1.0, results['risk_score'])
        results['is_likely_misinformation'] = results['risk_score'] > 0.5
        
        return results
    
    def _check_patterns(self, text: str, patterns: List[str]) -> int:
        """Count occurrences of patterns in text"""
        count = 0
        for pattern in patterns:
            if re.search(pattern, text):
                count += 1
        return count
    
    def _check_source(self, url: str) -> float:
        """Rate source reliability (0-1)"""
        url_lower = url.lower()
        
        for domain in self.reliable_domains:
            if domain in url_lower:
                return 0.9
        
        for domain in self.unreliable_domains:
            if domain in url_lower:
                return 0.1
        
        return 0.5  # Unknown source
    
    def check_headline(self, headline: str) -> Dict:
        """
        Check if headline is clickbait
        """
        result = {
            'headline': headline,
            'is_clickbait': False,
            'clickbait_score': 0.0,
            'reasons': []
        }
        
        headline_lower = headline.lower()
        
        for pattern in self.clickbait_patterns:
            if re.search(pattern, headline_lower):
                result['is_clickbait'] = True
                result['clickbait_score'] += 0.2
                result['reasons'].append(f"Contains: {pattern}")
        
        # Check for all caps
        if headline.isupper() and len(headline) > 10:
            result['is_clickbait'] = True
            result['clickbait_score'] += 0.1
            result['reasons'].append("All caps headline")
        
        # Check for excessive punctuation
        if '!!!' in headline or '???' in headline:
            result['is_clickbait'] = True
            result['clickbait_score'] += 0.1
            result['reasons'].append("Excessive punctuation")
        
        result['clickbait_score'] = min(1.0, result['clickbait_score'])
        
        return result
    
    def check_balance(self, article: str) -> Dict:
        """
        Check if article presents balanced view
        """
        result = {
            'balance_score': 0.5,
            'one_sided': False,
            'viewpoints': {'pro': 0, 'con': 0, 'neutral': 0}
        }
        
        article_lower = article.lower()
        
        # Look for viewpoint indicators
        pro_indicators = ['supports', 'advantages', 'benefits', 'positive', 'good', 'great', 'excellent']
        con_indicators = ['opposes', 'disadvantages', 'risks', 'negative', 'bad', 'terrible', 'dangerous']
        
        for word in pro_indicators:
            result['viewpoints']['pro'] += article_lower.count(word)
        
        for word in con_indicators:
            result['viewpoints']['con'] += article_lower.count(word)
        
        total = result['viewpoints']['pro'] + result['viewpoints']['con']
        if total > 0:
            balance = min(result['viewpoints']['pro'], result['viewpoints']['con']) / max(1, total/2)
            result['balance_score'] = balance
            result['one_sided'] = balance < 0.3
        
        return result
    
    def get_report(self, text: str, url: str = None) -> str:
        """
        Generate human-readable misinformation report
        """
        analysis = self.analyze(text, url)
        
        report = "🔍 MISINFORMATION DETECTION REPORT\n"
        report += "=" * 50 + "\n\n"
        
        # Risk level
        if analysis['risk_score'] < 0.3:
            report += "✅ LOW RISK - Content appears reliable\n"
        elif analysis['risk_score'] < 0.6:
            report += "⚠️ MEDIUM RISK - Exercise caution\n"
        else:
            report += "🚨 HIGH RISK - Potential misinformation\n"
        
        report += f"Risk Score: {analysis['risk_score']*100:.1f}%\n\n"
        
        # Source reliability
        report += f"📡 Source Reliability: {analysis['source_reliability']*100:.1f}%\n\n"
        
        # Warnings
        if analysis['warnings']:
            report += "⚠️ WARNINGS:\n"
            for warning in analysis['warnings']:
                report += f"  • {warning}\n"
            report += "\n"
        
        # Indicators
        if analysis['indicators']:
            report += "📊 DETECTED INDICATORS:\n"
            for indicator, count in analysis['indicators'].items():
                report += f"  • {indicator.replace('_', ' ').title()}: {count}\n"
        
        return report