"""
Music Generation - Create melodies, chord progressions, and compositions
"""

import random
import math
from typing import List, Dict, Optional, Tuple

class MusicGenerator:
    """
    Generates musical ideas and compositions
    """
    
    def __init__(self):
        self.notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.note_frequencies = {
            'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13, 'E': 329.63,
            'F': 349.23, 'F#': 369.99, 'G': 392.00, 'G#': 415.30, 'A': 440.00,
            'A#': 466.16, 'B': 493.88
        }
        
        self.scales = {
            'major': [0, 2, 4, 5, 7, 9, 11],
            'natural_minor': [0, 2, 3, 5, 7, 8, 10],
            'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
            'melodic_minor': [0, 2, 3, 5, 7, 9, 11],
            'pentatonic_major': [0, 2, 4, 7, 9],
            'pentatonic_minor': [0, 3, 5, 7, 10],
            'blues': [0, 3, 5, 6, 7, 10],
            'dorian': [0, 2, 3, 5, 7, 9, 10],
            'mixolydian': [0, 2, 4, 5, 7, 9, 10],
            'lydian': [0, 2, 4, 6, 7, 9, 11],
            'phrygian': [0, 1, 3, 5, 7, 8, 10],
            'locrian': [0, 1, 3, 5, 6, 8, 10]
        }
        
        self.chord_types = {
            'major': [0, 4, 7],
            'minor': [0, 3, 7],
            'diminished': [0, 3, 6],
            'augmented': [0, 4, 8],
            'major7': [0, 4, 7, 11],
            'minor7': [0, 3, 7, 10],
            'dominant7': [0, 4, 7, 10],
            'half_diminished': [0, 3, 6, 10],
            'diminished7': [0, 3, 6, 9]
        }
        
        self.chord_progressions = {
            'major': [
                ['I', 'IV', 'V'],
                ['I', 'V', 'vi', 'IV'],
                ['ii', 'V', 'I'],
                ['I', 'vi', 'IV', 'V'],
                ['I', 'IV', 'ii', 'V'],
                ['I', 'III', 'IV', 'V'],
                ['vi', 'IV', 'I', 'V']
            ],
            'minor': [
                ['i', 'iv', 'v'],
                ['i', 'VI', 'III', 'VII'],
                ['i', 'VII', 'VI', 'v'],
                ['i', 'iv', 'VII', 'III'],
                ['i', 'v', 'VI', 'VII'],
                ['i', 'iv', 'i', 'V']
            ]
        }
        
        self.genres = {
            'classical': {'tempo': (60, 120), 'instruments': ['piano', 'strings', 'woodwinds']},
            'jazz': {'tempo': (100, 160), 'instruments': ['saxophone', 'trumpet', 'piano', 'bass', 'drums']},
            'rock': {'tempo': (110, 150), 'instruments': ['electric guitar', 'bass', 'drums', 'vocals']},
            'pop': {'tempo': (100, 130), 'instruments': ['synth', 'drums', 'bass', 'vocals']},
            'electronic': {'tempo': (120, 140), 'instruments': ['synth', 'drum machine', 'sampler']},
            'ambient': {'tempo': (60, 90), 'instruments': ['pads', 'synth', 'field recordings']},
            'blues': {'tempo': (70, 110), 'instruments': ['guitar', 'harmonica', 'piano', 'bass']},
            'metal': {'tempo': (140, 200), 'instruments': ['distorted guitar', 'bass', 'drums']},
            'reggae': {'tempo': (80, 110), 'instruments': ['guitar', 'bass', 'drums', 'organ']},
            'funk': {'tempo': (90, 120), 'instruments': ['guitar', 'bass', 'drums', 'horns']}
        }
        
        self.time_signatures = [(4,4), (3,4), (2,4), (6,8), (12,8), (5,4), (7,4)]
        
    def generate_melody(self, key: str = 'C', scale: str = 'major', 
                         length: int = 8, rhythm: str = 'medium',
                         octave: int = 4) -> List[Dict]:
        """
        Generate a melody
        """
        scale_notes = self._get_scale_notes(key, scale, octave)
        melody = []
        
        # Define rhythm patterns
        rhythm_patterns = {
            'slow': ['whole', 'half', 'half', 'quarter'],
            'medium': ['quarter', 'quarter', 'eighth', 'eighth'],
            'fast': ['eighth', 'eighth', 'sixteenth', 'quarter']
        }
        
        durations = rhythm_patterns.get(rhythm, rhythm_patterns['medium'])
        
        for i in range(length):
            note = random.choice(scale_notes)
            duration = random.choice(durations)
            velocity = random.randint(60, 100)
            
            # Add some variation
            if random.random() > 0.7:
                note = self._add_interval(note, random.choice([2, 4, 7, 12]))
            
            melody.append({
                'position': i,
                'note': note,
                'duration': duration,
                'velocity': velocity,
                'frequency': self._note_to_frequency(note)
            })
        
        return melody
    
    def _get_scale_notes(self, key: str, scale: str, octave: int = 4) -> List[str]:
        """Get notes in a scale"""
        root_idx = self.notes.index(key)
        scale_intervals = self.scales.get(scale, self.scales['major'])
        
        scale_notes = []
        for interval in scale_intervals:
            idx = (root_idx + interval) % 12
            note = self.notes[idx]
            scale_notes.append(f"{note}{octave}")
            
        return scale_notes
    
    def _note_to_frequency(self, note: str) -> float:
        """Convert note name to frequency"""
        import re
        match = re.match(r'([A-G]#?)(\d+)', note)
        if match:
            note_name, octave = match.groups()
            base_freq = self.note_frequencies.get(note_name, 440.0)
            return base_freq * (2 ** (int(octave) - 4))
        return 440.0
    
    def _add_interval(self, note: str, semitones: int) -> str:
        """Add interval to a note"""
        import re
        match = re.match(r'([A-G]#?)(\d+)', note)
        if not match:
            return note
        
        note_name, octave = match.groups()
        idx = self.notes.index(note_name)
        new_idx = (idx + semitones) % 12
        new_octave = int(octave) + ((idx + semitones) // 12)
        
        return f"{self.notes[new_idx]}{new_octave}"
    
    def generate_chord_progression(self, key: str = 'C', mode: str = 'major',
                                     length: int = 4, complexity: str = 'simple') -> List[Dict]:
        """
        Generate a chord progression
        """
        progression = []
        
        # Choose progression template
        templates = self.chord_progressions[mode]
        if complexity == 'simple':
            template = random.choice(templates[:3])
        elif complexity == 'medium':
            template = random.choice(templates[3:6])
        else:
            template = random.choice(templates)
        
        # Extend to desired length
        while len(progression) < length:
            progression.extend(template)
        progression = progression[:length]
        
        # Convert Roman numerals to actual chords
        chords = []
        for roman in progression:
            chord = self._roman_to_chord(roman, key, mode)
            chords.append(chord)
        
        return chords
    
    def _roman_to_chord(self, roman: str, key: str, mode: str) -> Dict:
        """Convert Roman numeral to chord"""
        scale_notes = self._get_scale_notes(key, mode, 3)
        
        roman_map = {
            'I': (0, 'major'), 'i': (0, 'minor'),
            'II': (1, 'major'), 'ii': (1, 'minor'),
            'III': (2, 'major'), 'iii': (2, 'minor'),
            'IV': (3, 'major'), 'iv': (3, 'minor'),
            'V': (4, 'major'), 'v': (4, 'minor'),
            'VI': (5, 'major'), 'vi': (5, 'minor'),
            'VII': (6, 'diminished'), 'vii': (6, 'diminished')
        }
        
        if roman not in roman_map:
            return {'root': scale_notes[0], 'type': 'major', 'notes': [scale_notes[0]]}
        
        degree, chord_type = roman_map[roman]
        root = scale_notes[degree]
        
        # Build chord notes
        chord_notes = [root]
        intervals = self.chord_types.get(chord_type, [0, 4, 7])
        
        for interval in intervals[1:]:
            chord_notes.append(self._add_interval(root, interval))
        
        return {
            'roman': roman,
            'root': root,
            'type': chord_type,
            'notes': chord_notes,
            'frequencies': [self._note_to_frequency(n) for n in chord_notes]
        }
    
    def generate_rhythm(self, bars: int = 4, beats_per_bar: int = 4,
                         complexity: float = 0.3) -> List[int]:
        """
        Generate a rhythm pattern
        """
        rhythm = []
        for _ in range(bars * beats_per_bar):
            # 1 = hit, 0 = rest
            if random.random() > complexity:
                rhythm.append(1)
            else:
                rhythm.append(0)
        
        # Add some accent patterns
        for i in range(len(rhythm)):
            if i % beats_per_bar == 0:  # First beat of bar
                if random.random() > 0.1:
                    rhythm[i] = 2  # Accent
            
        return rhythm
    
    def generate_bassline(self, chord_progression: List[Dict], 
                           pattern: str = 'walking') -> List[Dict]:
        """
        Generate a bassline from chord progression
        """
        bassline = []
        
        for chord in chord_progression:
            root_note = chord['notes'][0]
            
            if pattern == 'walking':
                # Walking bass line
                for i in range(4):  # 4 beats per chord
                    if i == 0:
                        note = root_note
                    elif i == 2:
                        # Fifth on third beat
                        note = self._add_interval(root_note, 7)
                    else:
                        # Chromatic approach or scale note
                        options = [
                            self._add_interval(root_note, random.choice([-2, -1, 1, 2])),
                            root_note
                        ]
                        note = random.choice(options)
                    
                    bassline.append({
                        'position': len(bassline),
                        'note': note,
                        'duration': 'quarter',
                        'velocity': 80
                    })
            
            elif pattern == 'simple':
                # Simple root on first beat
                bassline.append({
                    'position': len(bassline),
                    'note': root_note,
                    'duration': 'whole',
                    'velocity': 85
                })
            
            elif pattern == 'syncopated':
                # Syncopated pattern
                for i in range(8):  # 8 eighth notes
                    if random.random() > 0.5:
                        bassline.append({
                            'position': len(bassline),
                            'note': root_note,
                            'duration': 'eighth',
                            'velocity': random.randint(60, 90)
                        })
        
        return bassline
    
    def generate_drum_pattern(self, genre: str = 'rock', bars: int = 4) -> Dict:
        """
        Generate a drum pattern
        """
        patterns = {
            'rock': {
                'kick': [1, 0, 0, 0, 1, 0, 0, 0],
                'snare': [0, 0, 1, 0, 0, 0, 1, 0],
                'hihat': [1, 1, 1, 1, 1, 1, 1, 1],
                'crash': [1, 0, 0, 0, 0, 0, 0, 0]
            },
            'electronic': {
                'kick': [1, 0, 1, 0, 1, 0, 1, 0],
                'snare': [0, 0, 1, 0, 0, 0, 1, 0],
                'hihat': [1, 1, 1, 1, 1, 1, 1, 1],
                'clap': [0, 1, 0, 1, 0, 1, 0, 1]
            },
            'jazz': {
                'kick': [1, 0, 0, 1, 0, 0, 1, 0],
                'snare': [0, 0, 1, 0, 0, 0, 1, 0],
                'hihat': [1, 0, 1, 0, 1, 0, 1, 0],
                'ride': [1, 1, 1, 1, 1, 1, 1, 1]
            },
            'funk': {
                'kick': [1, 0, 0, 1, 0, 1, 0, 1],
                'snare': [0, 0, 1, 0, 0, 0, 1, 0],
                'hihat': [1, 0, 1, 0, 1, 0, 1, 0],
                'cowbell': [0, 0, 1, 0, 0, 1, 0, 0]
            },
            'hiphop': {
                'kick': [1, 0, 0, 0, 1, 0, 0, 0],
                'snare': [0, 0, 1, 0, 0, 0, 1, 0],
                'hihat': [1, 1, 1, 1, 1, 1, 1, 1],
                'open_hat': [0, 0, 0, 1, 0, 0, 0, 1]
            }
        }
        
        base_pattern = patterns.get(genre, patterns['rock'])
        
        # Repeat for requested number of bars
        full_pattern = {}
        for instrument, pattern in base_pattern.items():
            full_pattern[instrument] = pattern * bars
        
        return full_pattern
    
    def generate_song_structure(self, genre: str = 'pop') -> Dict:
        """
        Generate a song structure
        """
        structures = {
            'pop': {'intro': 4, 'verse': 8, 'chorus': 8, 'verse': 8, 'chorus': 8, 'bridge': 4, 'chorus': 8, 'outro': 4},
            'rock': {'intro': 4, 'verse': 8, 'chorus': 8, 'verse': 8, 'chorus': 8, 'solo': 8, 'chorus': 8, 'outro': 4},
            'jazz': {'intro': 8, 'head': 16, 'solo1': 16, 'solo2': 16, 'head': 16, 'outro': 8},
            'electronic': {'intro': 8, 'build': 8, 'drop': 16, 'break': 8, 'build': 8, 'drop': 16, 'outro': 8},
            'classical': {'exposition': 16, 'development': 16, 'recapitulation': 16, 'coda': 8}
        }
        
        return structures.get(genre, structures['pop'])
    
    def suggest_tempo(self, genre: str, mood: str = 'medium') -> int:
        """Suggest a tempo for a genre and mood"""
        tempo_range = self.genres.get(genre, self.genres['pop'])['tempo']
        
        mood_factors = {
            'slow': 0.7,
            'medium': 1.0,
            'fast': 1.3,
            'very_fast': 1.6
        }
        
        factor = mood_factors.get(mood, 1.0)
        base_tempo = random.randint(tempo_range[0], tempo_range[1])
        
        return int(base_tempo * factor)
    
    def suggest_instruments(self, genre: str) -> List[str]:
        """Suggest instruments for a genre"""
        return self.genres.get(genre, self.genres['pop'])['instruments']
    
    def generate_harmony(self, chord_progression: List[Dict]) -> List[Dict]:
        """
        Generate harmony parts from chord progression
        """
        harmony = []
        
        for chord in chord_progression:
            # Create harmony notes from chord tones
            for i in range(3):  # 3 harmony voices
                note = chord['notes'][i % len(chord['notes'])]
                harmony.append({
                    'note': self._add_interval(note, 12),  # Up an octave
                    'duration': chord.get('duration', 'quarter'),
                    'velocity': random.randint(50, 70)
                })
        
        return harmony
    
    def midi_export(self, melody: List[Dict], filename: str):
        """
        Export melody as MIDI (simplified)
        """
        midi_data = {
            'format': 1,
            'tracks': 1,
            'ticks_per_quarter': 480,
            'notes': melody
        }
        
        # Save as JSON for now (actual MIDI export would need mido library)
        import json
        with open(f"{filename}.json", 'w') as f:
            json.dump(midi_data, f, indent=2)
        print(f"✅ MIDI data saved to {filename}.json")