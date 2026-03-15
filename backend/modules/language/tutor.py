"""
Language Tutor - Helps learn new languages
"""

import random
from typing import Dict, List, Optional, Tuple

class LanguageTutor:
    """
    Language learning assistant
    """
    
    def __init__(self):
        self.lessons = {}
        self.vocabulary = {}
        self.user_progress = {}
        
        self._init_spanish()
        self._init_french()
        self._init_german()
    
    def _init_spanish(self):
        """Initialize Spanish vocabulary"""
        self.vocabulary['es'] = {
            'greetings': [
                ('hola', 'hello'),
                ('buenos días', 'good morning'),
                ('buenas tardes', 'good afternoon'),
                ('buenas noches', 'good night'),
                ('adiós', 'goodbye'),
                ('hasta luego', 'see you later'),
                ('¿cómo estás?', 'how are you?')
            ],
            'basics': [
                ('sí', 'yes'),
                ('no', 'no'),
                ('por favor', 'please'),
                ('gracias', 'thank you'),
                ('de nada', 'you\'re welcome'),
                ('lo siento', 'sorry'),
                ('perdón', 'excuse me')
            ],
            'numbers': [
                ('uno', 'one'),
                ('dos', 'two'),
                ('tres', 'three'),
                ('cuatro', 'four'),
                ('cinco', 'five'),
                ('seis', 'six'),
                ('siete', 'seven'),
                ('ocho', 'eight'),
                ('nueve', 'nine'),
                ('diez', 'ten')
            ],
            'food': [
                ('comida', 'food'),
                ('agua', 'water'),
                ('pan', 'bread'),
                ('fruta', 'fruit'),
                ('verdura', 'vegetable'),
                ('carne', 'meat'),
                ('pescado', 'fish')
            ],
            'common_verbs': [
                ('ser', 'to be (permanent)'),
                ('estar', 'to be (temporary)'),
                ('tener', 'to have'),
                ('hacer', 'to do/make'),
                ('ir', 'to go'),
                ('venir', 'to come'),
                ('hablar', 'to speak')
            ]
        }
    
    def _init_french(self):
        """Initialize French vocabulary"""
        self.vocabulary['fr'] = {
            'greetings': [
                ('bonjour', 'hello'),
                ('bonsoir', 'good evening'),
                ('au revoir', 'goodbye'),
                ('à bientôt', 'see you soon'),
                ('comment ça va?', 'how are you?'),
                ('merci', 'thank you'),
                ('s\'il vous plaît', 'please')
            ],
            'basics': [
                ('oui', 'yes'),
                ('non', 'no'),
                ('pardon', 'sorry'),
                ('excusez-moi', 'excuse me'),
                ('de rien', 'you\'re welcome'),
                ('je ne comprends pas', 'I don\'t understand')
            ],
            'numbers': [
                ('un', 'one'),
                ('deux', 'two'),
                ('trois', 'three'),
                ('quatre', 'four'),
                ('cinq', 'five'),
                ('six', 'six'),
                ('sept', 'seven'),
                ('huit', 'eight'),
                ('neuf', 'nine'),
                ('dix', 'ten')
            ]
        }
    
    def _init_german(self):
        """Initialize German vocabulary"""
        self.vocabulary['de'] = {
            'greetings': [
                ('hallo', 'hello'),
                ('guten Morgen', 'good morning'),
                ('guten Abend', 'good evening'),
                ('auf Wiedersehen', 'goodbye'),
                ('tschüss', 'bye'),
                ('wie geht\'s?', 'how are you?'),
                ('danke', 'thank you'),
                ('bitte', 'please/you\'re welcome')
            ],
            'basics': [
                ('ja', 'yes'),
                ('nein', 'no'),
                ('Entschuldigung', 'excuse me'),
                ('es tut mir leid', 'I\'m sorry'),
                ('ich verstehe nicht', 'I don\'t understand')
            ]
        }
    
    def get_lesson(self, language: str, level: str = 'beginner') -> Dict:
        """
        Get a language lesson
        """
        if language not in self.vocabulary:
            return {'error': f'Language {language} not available'}
        
        lesson = {
            'language': language,
            'level': level,
            'categories': [],
            'words': [],
            'practice': []
        }
        
        # Get vocabulary for this language
        vocab = self.vocabulary[language]
        
        # Include all categories for beginner
        for category, words in vocab.items():
            lesson['categories'].append(category)
            for word_pair in words[:5]:  # First 5 words per category
                lesson['words'].append({
                    'foreign': word_pair[0],
                    'english': word_pair[1],
                    'category': category
                })
        
        # Generate practice sentences
        lesson['practice'] = self._generate_practice_sentences(language, level)
        
        return lesson
    
    def _generate_practice_sentences(self, language: str, level: str) -> List[Dict]:
        """Generate practice sentences"""
        sentences = []
        
        if language == 'es':
            if level == 'beginner':
                sentences = [
                    {'english': 'Hello, how are you?', 'answer': 'Hola, ¿cómo estás?'},
                    {'english': 'Good morning, thank you', 'answer': 'Buenos días, gracias'},
                    {'english': 'Yes, please', 'answer': 'Sí, por favor'}
                ]
            elif level == 'intermediate':
                sentences = [
                    {'english': 'I would like to eat bread', 'answer': 'Me gustaría comer pan'},
                    {'english': 'Where is the bathroom?', 'answer': '¿Dónde está el baño?'}
                ]
        
        elif language == 'fr':
            sentences = [
                {'english': 'Hello, how are you?', 'answer': 'Bonjour, comment ça va?'},
                {'english': 'Thank you very much', 'answer': 'Merci beaucoup'}
            ]
        
        elif language == 'de':
            sentences = [
                {'english': 'Hello, how are you?', 'answer': 'Hallo, wie geht\'s?'},
                {'english': 'Thank you very much', 'answer': 'Vielen Dank'}
            ]
        
        return sentences
    
    def quiz(self, language: str, category: str = None, num_questions: int = 5) -> List[Dict]:
        """
        Generate a quiz
        """
        if language not in self.vocabulary:
            return []
        
        vocab = self.vocabulary[language]
        questions = []
        
        # Collect words from specified category or all
        words = []
        if category and category in vocab:
            words = vocab[category]
        else:
            for cat_words in vocab.values():
                words.extend(cat_words)
        
        # Randomly select questions
        selected = random.sample(words, min(num_questions, len(words)))
        
        for foreign, english in selected:
            # 50% chance of foreign->english or english->foreign
            if random.random() > 0.5:
                questions.append({
                    'question': f"What does '{foreign}' mean?",
                    'answer': english,
                    'type': 'foreign_to_english'
                })
            else:
                questions.append({
                    'question': f"How do you say '{english}' in {language}?",
                    'answer': foreign,
                    'type': 'english_to_foreign'
                })
        
        return questions
    
    def track_progress(self, user_id: str, language: str, 
                        correct: int, total: int):
        """
        Track user progress
        """
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {}
        
        if language not in self.user_progress[user_id]:
            self.user_progress[user_id][language] = {
                'total_attempts': 0,
                'correct_attempts': 0,
                'lessons_completed': [],
                'current_level': 'beginner'
            }
        
        progress = self.user_progress[user_id][language]
        progress['total_attempts'] += total
        progress['correct_attempts'] += correct
        
        # Update level based on accuracy
        accuracy = progress['correct_attempts'] / max(1, progress['total_attempts'])
        if accuracy > 0.8 and progress['current_level'] == 'beginner':
            progress['current_level'] = 'intermediate'
        elif accuracy > 0.9 and progress['current_level'] == 'intermediate':
            progress['current_level'] = 'advanced'
    
    def get_progress(self, user_id: str, language: str) -> Dict:
        """Get user progress"""
        return self.user_progress.get(user_id, {}).get(language, {
            'total_attempts': 0,
            'correct_attempts': 0,
            'current_level': 'beginner'
        })
    
    def get_available_languages(self) -> List[str]:
        """Get list of available languages"""
        return list(self.vocabulary.keys())