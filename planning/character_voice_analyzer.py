#!/usr/bin/env python3
"""
Character Voice Analyzer for Link Loader
Analyzes character dialogue for consistency and patterns

Author: Chen (Script/Narrative)
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from collections import Counter, defaultdict
import string

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))
from renpy_game_player import RenpyGame

@dataclass
class CharacterProfile:
    """Profile of a character's speaking patterns"""
    name: str
    total_lines: int
    word_count: int
    vocabulary: Set[str]
    word_frequency: Counter
    common_phrases: List[Tuple[str, int]]
    sentence_patterns: Dict[str, int]
    punctuation_usage: Dict[str, float]
    average_sentence_length: float
    contractions_usage: float
    questions_ratio: float
    exclamations_ratio: float
    
@dataclass
class Inconsistency:
    """Represents a potential inconsistency in character voice"""
    character: str
    line: str
    file: str
    line_number: int
    issue_type: str
    description: str
    severity: str  # low, medium, high

class CharacterVoiceAnalyzer:
    """Analyzes character dialogue for consistency"""
    
    def __init__(self, game_path: str):
        self.game = RenpyGame(game_path)
        self.character_profiles: Dict[str, CharacterProfile] = {}
        self.character_lines: Dict[str, List[Tuple[str, str, int]]] = defaultdict(list)
        self._extract_dialogue()
        self._build_profiles()
        
    def _extract_dialogue(self):
        """Extract all dialogue for each character"""
        for label, content in self.game.labels.items():
            for i, (indent, line, filename) in enumerate(content):
                line = line.strip()
                
                # Skip non-dialogue lines
                if not line or line.startswith('#') or line.startswith('$'):
                    continue
                
                # Check for character dialogue
                for char_id, char in self.game.characters.items():
                    if line.startswith(f'{char_id} "') and line.endswith('"'):
                        dialogue = line[len(char_id)+2:-1]
                        self.character_lines[char_id].append((dialogue, filename, i))
                        break
    
    def _build_profiles(self):
        """Build speaking profiles for each character"""
        for char_id, lines in self.character_lines.items():
            if not lines:
                continue
                
            char_name = self.game.characters[char_id].name if char_id in self.game.characters else char_id
            
            # Initialize counters
            all_words = []
            sentence_patterns = defaultdict(int)
            punctuation_counts = defaultdict(int)
            total_sentences = 0
            questions = 0
            exclamations = 0
            contractions = 0
            
            for dialogue, _, _ in lines:
                # Clean and tokenize
                words = self._tokenize(dialogue)
                all_words.extend(words)
                
                # Analyze sentence patterns
                sentences = self._split_sentences(dialogue)
                total_sentences += len(sentences)
                
                for sentence in sentences:
                    pattern = self._get_sentence_pattern(sentence)
                    sentence_patterns[pattern] += 1
                    
                    # Count punctuation
                    if sentence.endswith('?'):
                        questions += 1
                    elif sentence.endswith('!'):
                        exclamations += 1
                    
                # Count contractions
                contractions += len(re.findall(r"\w+'\w+", dialogue))
                
                # Count punctuation
                for char in dialogue:
                    if char in string.punctuation:
                        punctuation_counts[char] += 1
            
            # Calculate statistics
            word_freq = Counter(all_words)
            vocabulary = set(all_words)
            
            # Find common phrases (2-3 word combinations)
            phrases = self._extract_phrases(lines)
            common_phrases = phrases.most_common(10)
            
            # Calculate ratios
            total_words = len(all_words)
            avg_sentence_length = total_words / total_sentences if total_sentences > 0 else 0
            questions_ratio = questions / total_sentences if total_sentences > 0 else 0
            exclamations_ratio = exclamations / total_sentences if total_sentences > 0 else 0
            contractions_ratio = contractions / total_words if total_words > 0 else 0
            
            # Punctuation usage
            punctuation_usage = {}
            for punct, count in punctuation_counts.items():
                punctuation_usage[punct] = count / total_words if total_words > 0 else 0
            
            # Create profile
            self.character_profiles[char_id] = CharacterProfile(
                name=char_name,
                total_lines=len(lines),
                word_count=total_words,
                vocabulary=vocabulary,
                word_frequency=word_freq,
                common_phrases=common_phrases,
                sentence_patterns=dict(sentence_patterns),
                punctuation_usage=punctuation_usage,
                average_sentence_length=avg_sentence_length,
                contractions_usage=contractions_ratio,
                questions_ratio=questions_ratio,
                exclamations_ratio=exclamations_ratio
            )
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        # Remove punctuation and convert to lowercase
        text_clean = text.lower()
        for punct in string.punctuation:
            text_clean = text_clean.replace(punct, ' ')
        
        return text_clean.split()
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _get_sentence_pattern(self, sentence: str) -> str:
        """Get the grammatical pattern of a sentence"""
        # Simplified pattern detection
        sentence = sentence.strip()
        
        if sentence.startswith(('who', 'what', 'where', 'when', 'why', 'how')):
            return 'interrogative'
        elif sentence.endswith('?'):
            return 'question'
        elif sentence.endswith('!'):
            return 'exclamation'
        elif sentence.startswith(('i ', "i'", 'we ')):
            return 'first_person'
        elif sentence.startswith(('you ', "you'")):
            return 'second_person'
        else:
            return 'statement'
    
    def _extract_phrases(self, lines: List[Tuple[str, str, int]]) -> Counter:
        """Extract common phrases (2-3 word combinations)"""
        phrases = Counter()
        
        for dialogue, _, _ in lines:
            words = self._tokenize(dialogue)
            
            # 2-word phrases
            for i in range(len(words) - 1):
                phrase = f"{words[i]} {words[i+1]}"
                phrases[phrase] += 1
            
            # 3-word phrases
            for i in range(len(words) - 2):
                phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
                phrases[phrase] += 1
        
        return phrases
    
    def detect_inconsistencies(self) -> List[Inconsistency]:
        """Find dialogue that doesn't match character voice"""
        inconsistencies = []
        
        # Define character voice expectations
        character_expectations = {
            'pc': {  # Slim
                'expected_contractions': 0.7,  # High contraction usage
                'expected_formality': 'low',
                'vocabulary_style': 'western',
                'avoid_words': ['therefore', 'furthermore', 'indeed']
            },
            'clipi': {
                'expected_contractions': 0.3,  # Lower contraction usage
                'expected_formality': 'medium',
                'vocabulary_style': 'technical',
                'expected_patterns': ['processing', 'systems', 'operational']
            },
            't': {  # Terminal
                'expected_contractions': 0.0,  # No contractions
                'expected_formality': 'high',
                'vocabulary_style': 'formal',
                'expected_patterns': ['error', 'status', 'warning']
            }
        }
        
        for char_id, lines in self.character_lines.items():
            if char_id not in self.character_profiles:
                continue
                
            profile = self.character_profiles[char_id]
            expectations = character_expectations.get(char_id, {})
            
            for dialogue, filename, line_num in lines:
                # Check contraction usage
                if 'expected_contractions' in expectations:
                    expected = expectations['expected_contractions']
                    actual_contractions = len(re.findall(r"\w+'\w+", dialogue))
                    words_in_line = len(self._tokenize(dialogue))
                    actual_ratio = actual_contractions / words_in_line if words_in_line > 0 else 0
                    
                    if abs(actual_ratio - expected) > 0.3:
                        if actual_ratio < expected:
                            inconsistencies.append(Inconsistency(
                                character=profile.name,
                                line=dialogue,
                                file=filename,
                                line_number=line_num,
                                issue_type='contractions',
                                description='Too formal - missing expected contractions',
                                severity='medium'
                            ))
                        else:
                            inconsistencies.append(Inconsistency(
                                character=profile.name,
                                line=dialogue,
                                file=filename,
                                line_number=line_num,
                                issue_type='contractions',
                                description='Too informal - unexpected contractions',
                                severity='medium'
                            ))
                
                # Check for out-of-character words
                if 'avoid_words' in expectations:
                    words = set(self._tokenize(dialogue))
                    for avoid_word in expectations['avoid_words']:
                        if avoid_word in words:
                            inconsistencies.append(Inconsistency(
                                character=profile.name,
                                line=dialogue,
                                file=filename,
                                line_number=line_num,
                                issue_type='vocabulary',
                                description=f'Uses uncharacteristic word: "{avoid_word}"',
                                severity='high'
                            ))
                
                # Check for missing expected patterns
                if 'expected_patterns' in expectations:
                    words = set(self._tokenize(dialogue))
                    has_expected = any(pattern in dialogue.lower() for pattern in expectations['expected_patterns'])
                    
                    # Only flag if the line is substantial
                    if len(words) > 10 and not has_expected and char_id == 't':
                        inconsistencies.append(Inconsistency(
                            character=profile.name,
                            line=dialogue,
                            file=filename,
                            line_number=line_num,
                            issue_type='pattern',
                            description='Missing expected technical terminology',
                            severity='low'
                        ))
        
        return inconsistencies
    
    def compare_characters(self) -> Dict[str, Dict[str, float]]:
        """Compare speech patterns between characters"""
        comparison = {}
        
        char_ids = list(self.character_profiles.keys())
        
        for i, char_id1 in enumerate(char_ids):
            comparison[char_id1] = {}
            profile1 = self.character_profiles[char_id1]
            
            for j, char_id2 in enumerate(char_ids):
                if i == j:
                    comparison[char_id1][char_id2] = 1.0
                    continue
                
                profile2 = self.character_profiles[char_id2]
                
                # Calculate similarity based on various factors
                vocab_overlap = len(profile1.vocabulary & profile2.vocabulary) / len(profile1.vocabulary | profile2.vocabulary)
                
                # Compare ratios
                question_diff = abs(profile1.questions_ratio - profile2.questions_ratio)
                exclamation_diff = abs(profile1.exclamations_ratio - profile2.exclamations_ratio)
                contraction_diff = abs(profile1.contractions_usage - profile2.contractions_usage)
                
                # Calculate overall similarity (0-1)
                similarity = (vocab_overlap + (1 - question_diff) + (1 - exclamation_diff) + (1 - contraction_diff)) / 4
                
                comparison[char_id1][char_id2] = similarity
        
        return comparison
    
    def generate_report(self) -> str:
        """Generate a comprehensive voice analysis report"""
        lines = ["Character Voice Analysis Report", "=" * 40, ""]
        
        # Character profiles
        lines.append("## Character Profiles")
        for char_id, profile in self.character_profiles.items():
            lines.append(f"\n### {profile.name}")
            lines.append(f"Total lines: {profile.total_lines}")
            lines.append(f"Vocabulary size: {len(profile.vocabulary)}")
            lines.append(f"Average sentence length: {profile.average_sentence_length:.1f} words")
            lines.append(f"Contractions usage: {profile.contractions_usage:.1%}")
            lines.append(f"Questions: {profile.questions_ratio:.1%}")
            lines.append(f"Exclamations: {profile.exclamations_ratio:.1%}")
            
            lines.append("\nCommon phrases:")
            for phrase, count in profile.common_phrases[:5]:
                lines.append(f"  - '{phrase}' ({count} times)")
            
            lines.append("\nTop words:")
            for word, count in profile.word_frequency.most_common(10):
                lines.append(f"  - '{word}' ({count})")
        
        lines.append("")
        
        # Inconsistencies
        inconsistencies = self.detect_inconsistencies()
        lines.append("## Voice Inconsistencies")
        
        if inconsistencies:
            # Group by character
            by_character = defaultdict(list)
            for inc in inconsistencies:
                by_character[inc.character].append(inc)
            
            for character, char_issues in by_character.items():
                lines.append(f"\n### {character}")
                for issue in char_issues[:5]:  # Limit to top 5
                    lines.append(f"- [{issue.severity}] {issue.description}")
                    lines.append(f"  Line: '{issue.line[:50]}...'")
                    lines.append(f"  File: {issue.file}:{issue.line_number}")
                    lines.append("")
        else:
            lines.append("No major inconsistencies detected ✓")
        
        lines.append("")
        
        # Character comparison
        comparison = self.compare_characters()
        lines.append("## Character Voice Similarity Matrix")
        
        char_names = [self.character_profiles[cid].name for cid in comparison.keys()]
        
        # Create matrix
        lines.append("```")
        header = "Character".ljust(12) + " | " + " | ".join(name.ljust(10) for name in char_names)
        lines.append(header)
        lines.append("-" * len(header))
        
        for char_id, similarities in comparison.items():
            char_name = self.character_profiles[char_id].name
            row = char_name.ljust(12) + " | "
            for other_id in comparison.keys():
                sim = similarities[other_id]
                row += f"{sim:.2f}".ljust(10) + " | "
            lines.append(row.rstrip(" | "))
        
        lines.append("```")
        
        return "\n".join(lines)

def main():
    """Run the character voice analyzer"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze character voice in Link Loader")
    parser.add_argument("--game", default="../current/renpy-8.3.7-sdk/link_loader_1_2/game",
                        help="Path to game directory")
    parser.add_argument("--export", help="Export analysis to JSON file")
    parser.add_argument("--character", help="Analyze specific character")
    
    args = parser.parse_args()
    
    # Create analyzer
    print("Analyzing character voices...")
    analyzer = CharacterVoiceAnalyzer(args.game)
    
    # Generate report
    report = analyzer.generate_report()
    print("\n" + report)
    
    # Export if requested
    if args.export:
        data = {
            'profiles': {},
            'inconsistencies': [],
            'comparison': analyzer.compare_characters()
        }
        
        # Export profiles
        for char_id, profile in analyzer.character_profiles.items():
            data['profiles'][char_id] = {
                'name': profile.name,
                'total_lines': profile.total_lines,
                'vocabulary_size': len(profile.vocabulary),
                'average_sentence_length': profile.average_sentence_length,
                'contractions_usage': profile.contractions_usage,
                'questions_ratio': profile.questions_ratio,
                'exclamations_ratio': profile.exclamations_ratio,
                'common_phrases': profile.common_phrases
            }
        
        # Export inconsistencies
        for inc in analyzer.detect_inconsistencies():
            data['inconsistencies'].append({
                'character': inc.character,
                'line': inc.line,
                'file': inc.file,
                'line_number': inc.line_number,
                'issue_type': inc.issue_type,
                'description': inc.description,
                'severity': inc.severity
            })
        
        with open(args.export, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nAnalysis exported to {args.export}")

if __name__ == "__main__":
    main()