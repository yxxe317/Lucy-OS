"""
Fact Checker - Verify claims against knowledge sources
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class FactChecker:
    """
    Verifies factual claims using multiple sources
    """
    
    def __init__(self, knowledge_graph=None, wikipedia=None, web_search=None):
        self.kg = knowledge_graph
        self.wiki = wikipedia
        self.web = web_search
        self.verification_cache = {}
        self.confidence_threshold = 0.7
        
        # Known reliable sources
        self.reliable_sources = {
            'wikipedia.org': 0.9,
            'britannica.com': 0.95,
            'who.int': 0.9,
            'nasa.gov': 0.95,
            'nih.gov': 0.9,
            'cdc.gov': 0.9,
            'un.org': 0.85,
            'bbc.com': 0.7,
            'reuters.com': 0.8,
            'apnews.com': 0.8
        }
    
    def check(self, claim: str) -> Dict:
        """
        Check if a claim is factual
        """
        # Check cache
        if claim in self.verification_cache:
            return self.verification_cache[claim]
        
        results = {
            'claim': claim,
            'verdict': 'unknown',
            'confidence': 0.0,
            'sources': [],
            'contradictions': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Check knowledge graph
        if self.kg:
            kg_result = self._check_kg(claim)
            if kg_result:
                results['sources'].append(kg_result)
                results['confidence'] += kg_result['confidence'] * 0.5
        
        # Check Wikipedia
        if self.wiki:
            wiki_result = self._check_wiki(claim)
            if wiki_result:
                results['sources'].append(wiki_result)
                results['confidence'] += wiki_result['confidence'] * 0.3
        
        # Web search as fallback
        if self.web and results['confidence'] < self.confidence_threshold:
            web_result = self._check_web(claim)
            if web_result:
                results['sources'].append(web_result)
                results['confidence'] += web_result['confidence'] * 0.2
        
        # Normalize confidence
        results['confidence'] = min(1.0, results['confidence'])
        
        # Determine verdict
        if results['confidence'] >= self.confidence_threshold:
            results['verdict'] = 'likely_true'
        elif results['confidence'] <= 0.3:
            results['verdict'] = 'likely_false'
        else:
            results['verdict'] = 'uncertain'
        
        # Check for contradictions
        if len(results['sources']) > 1:
            self._check_contradictions(results)
        
        # Cache result
        self.verification_cache[claim] = results
        return results
    
    def _check_kg(self, claim: str) -> Optional[Dict]:
        """
        Check claim against knowledge graph
        """
        # Extract potential entities
        words = claim.split()
        for word in words:
            entities = self.kg.find_entity(word)
            if entities:
                return {
                    'source': 'knowledge_graph',
                    'confidence': 0.8,
                    'evidence': f"Found in knowledge graph: {entities[0]['name']}",
                    'url': None
                }
        return None
    
    def _check_wiki(self, claim: str) -> Optional[Dict]:
        """
        Check claim against Wikipedia
        """
        # Search Wikipedia
        results = self.wiki.search(claim, limit=3)
        
        for result in results:
            # Get summary to check if it contains the claim
            summary = self.wiki.get_summary(result['title'])
            if summary and claim.lower() in summary.lower():
                return {
                    'source': 'wikipedia',
                    'confidence': 0.85,
                    'evidence': summary[:200] + "...",
                    'url': f"https://en.wikipedia.org/wiki/{result['title'].replace(' ', '_')}"
                }
        
        return None
    
    def _check_web(self, claim: str) -> Optional[Dict]:
        """
        Check claim via web search
        """
        results = self.web.search(claim, max_results=5)
        
        for result in results.get('results', []):
            url = result.get('url', '')
            
            # Check source reliability
            source_reliability = 0.5
            for domain, reliability in self.reliable_sources.items():
                if domain in url:
                    source_reliability = reliability
                    break
            
            return {
                'source': result.get('source', 'web'),
                'confidence': source_reliability,
                'evidence': result.get('snippet', ''),
                'url': url
            }
        
        return None
    
    def _check_contradictions(self, results: Dict):
        """
        Check for contradictions between sources
        """
        sources = results['sources']
        for i, src1 in enumerate(sources):
            for src2 in sources[i+1:]:
                # Simple contradiction check based on confidence difference
                if abs(src1['confidence'] - src2['confidence']) > 0.5:
                    results['contradictions'].append({
                        'source1': src1['source'],
                        'source2': src2['source'],
                        'confidence_gap': abs(src1['confidence'] - src2['confidence'])
                    })
    
    def verify_batch(self, claims: List[str]) -> List[Dict]:
        """
        Verify multiple claims
        """
        return [self.check(claim) for claim in claims]
    
    def get_credibility_report(self, claim: str) -> str:
        """
        Get human-readable credibility report
        """
        result = self.check(claim)
        
        report = f"📋 FACT CHECK: \"{claim}\"\n"
        report += "=" * 50 + "\n\n"
        
        # Verdict with color indicator
        if result['verdict'] == 'likely_true':
            report += "✅ VERDICT: LIKELY TRUE\n"
        elif result['verdict'] == 'likely_false':
            report += "❌ VERDICT: LIKELY FALSE\n"
        else:
            report += "⚠️ VERDICT: UNCERTAIN\n"
        
        report += f"Confidence: {result['confidence']*100:.1f}%\n\n"
        
        # Sources
        if result['sources']:
            report += "📚 SOURCES:\n"
            for src in result['sources']:
                report += f"  • {src['source']} (confidence: {src['confidence']*100:.0f}%)\n"
                report += f"    Evidence: {src['evidence'][:100]}...\n"
        
        # Contradictions
        if result['contradictions']:
            report += "\n⚠️ CONTRADICTIONS DETECTED:\n"
            for cont in result['contradictions']:
                report += f"  • {cont['source1']} vs {cont['source2']}\n"
        
        return report