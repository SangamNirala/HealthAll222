#!/usr/bin/env python3

"""
Step-by-step test of the text normalization system
to debug and optimize for the specific examples
"""

from nlp_processor import IntelligentTextNormalizer
import re

def test_step_by_step():
    normalizer = IntelligentTextNormalizer()
    
    test_cases = [
        ("i having fever 2 days", "I have been having a fever for 2 days"),
        ("me chest hurt when breath", "My chest hurts when I breathe"),
        ("haedache really bad", "Headache really bad"),
        ("stomach ache n vomiting", "Stomach ache and vomiting"),
    ]
    
    for i, (original, expected) in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}: '{original}'")
        print(f"EXPECTED:    '{expected}'")
        print(f"{'='*60}")
        
        text = original
        
        # Step by step processing
        print(f"Original: '{text}'")
        
        # Step 1: Basic capitalization
        text, corrections = normalizer._fix_basic_capitalization(text)
        print(f"After capitalization: '{text}' | Corrections: {corrections}")
        
        # Step 2: Abbreviations
        text, corrections = normalizer._expand_abbreviations(text)
        print(f"After abbreviations: '{text}' | Corrections: {corrections}")
        
        # Step 3: Medical spelling
        text, corrections = normalizer._correct_medical_spelling(text)
        print(f"After spelling: '{text}' | Corrections: {corrections}")
        
        # Step 4: Pronoun corrections
        text, corrections = normalizer._fix_pronoun_patterns(text)
        print(f"After pronouns: '{text}' | Corrections: {corrections}")
        
        # Step 5: Grammar corrections
        text, corrections = normalizer._apply_grammar_corrections(text)
        print(f"After grammar: '{text}' | Corrections: {corrections}")
        
        # Final result
        print(f"\nFINAL RESULT: '{text}'")
        print(f"MATCHES EXPECTED: {text.lower() == expected.lower()}")


if __name__ == "__main__":
    test_step_by_step()