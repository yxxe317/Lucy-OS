"""
Text Summarizer - Summarize long texts
"""

import re
from collections import Counter
from typing import List, Dict, Optional

class TextSummarizer:
    """
    Summarizes long texts using extraction methods
    """
    
    def __init__(self):
        self.stop_words = {
            'a', 'an', 'the', 'and', 'or', 'but', 'if', 'then', 'else',
            'when', 'at', 'from', 'by', 'on', 'off', 'for', 'in', 'out',
            'over', 'under', 'again', 'further', 'then', 'once', 'here',
            'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both',
            'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
            'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
            's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
        }
    
    def summarize(self, text: str, ratio: float = 0.3, max_sentences: int = None) -> str:
        """
        Summarize text by extracting important sentences
        """
        sentences = self._split_sentences(text)
        
        if len(sentences) <= 3:
            return text
        
        # Calculate sentence scores
        scores = self._score_sentences(sentences)
        
        # Select top sentences
        num_sentences = max(1, int(len(sentences) * ratio))
        if max_sentences:
            num_sentences = min(num_sentences, max_sentences)
        
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:num_sentences]
        top_indices.sort()  # Keep original order
        
        summary = ' '.join([sentences[i] for i in top_indices])
        return summary
    
    def summarize_by_percentage(self, text: str, percentage: float) -> str:
        """
        Summarize by percentage (0.1 = 10% of original)
        """
        return self.summarize(text, ratio=percentage/100)
    
    def summarize_by_sentences(self, text: str, num_sentences: int) -> str:
        """
        Summarize to specific number of sentences
        """
        return self.summarize(text, max_sentences=num_sentences)
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def _score_sentences(self, sentences: List[str]) -> List[float]:
        """Score each sentence by importance"""
        # Calculate word frequencies
        word_freq = self._get_word_frequencies(' '.join(sentences))
        
        scores = []
        for sentence in sentences:
            score = self._score_sentence(sentence, word_freq)
            scores.append(score)
        
        return scores
    
    def _get_word_frequencies(self, text: str) -> Dict[str, float]:
        """Get normalized word frequencies"""
        words = re.findall(r'\w+', text.lower())
        words = [w for w in words if w not in self.stop_words and len(w) > 2]
        
        freq = Counter(words)
        max_freq = max(freq.values()) if freq else 1
        
        # Normalize
        return {word: count/max_freq for word, count in freq.items()}
    
    def _score_sentence(self, sentence: str, word_freq: Dict[str, float]) -> float:
        """Score a single sentence"""
        words = re.findall(r'\w+', sentence.lower())
        words = [w for w in words if w not in self.stop_words]
        
        if not words:
            return 0
        
        # Sum of word frequencies
        score = sum(word_freq.get(word, 0) for word in words)
        
        # Bonus for sentences with proper structure
        if sentence[0].isupper():  # Starts with capital
            score *= 1.1
        
        # Position bonus (earlier sentences often more important)
        # This will be applied separately
        
        return score
    
    def extract_keywords(self, text: str, num_keywords: int = 5) -> List[str]:
        """
        Extract key phrases from text
        """
        words = re.findall(r'\w+', text.lower())
        words = [w for w in words if w not in self.stop_words and len(w) > 2]
        
        freq = Counter(words)
        return [word for word, _ in freq.most_common(num_keywords)]
    
    def get_title(self, text: str) -> str:
        """
        Generate a title from text
        """
        keywords = self.extract_keywords(text, 3)
        return ' '.join(keywords).title()