"""
Advanced NLP Processor for Medical Text Normalization
Implements intelligent text preprocessing to handle poor grammar, typos, and informal language in medical queries
Enhanced with world-class medical spell correction (Step 1.2)
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Import the advanced medical spell checker
from medical_spell_checker import AdvancedMedicalSpellChecker, SpellCorrectionResult


@dataclass
class NormalizationResult:
    """Result of text normalization process"""
    original_text: str
    normalized_text: str
    corrections_applied: List[str]
    confidence_score: float
    medical_entities_preserved: List[str]
    spell_corrections: List[SpellCorrectionResult] = None  # Step 1.2 enhancement


class IntelligentTextNormalizer:
    """
    World-class text normalization system specifically designed for medical conversations
    Handles grammar errors, spelling mistakes, informal language, and medical context preservation
    """
    
    def __init__(self):
        self.grammar_patterns = self._load_grammar_patterns()
        self.medical_spell_corrections = self._load_medical_spell_corrections()
        self.informal_to_formal_medical = self._load_informal_to_formal_medical()
        self.abbreviation_expansions = self._load_abbreviation_expansions()
        self.pronoun_corrections = self._load_pronoun_corrections()
        self.verb_tense_patterns = self._load_verb_tense_patterns()
        
        # Initialize advanced medical spell checker (Step 1.2)
        self.advanced_spell_checker = AdvancedMedicalSpellChecker()
        
    def normalize_medical_text(self, text: str) -> NormalizationResult:
        """
        Main normalization function that applies all text processing steps
        
        Args:
            text (str): Raw input text from patient
            
        Returns:
            NormalizationResult: Comprehensive normalization result
        """
        original_text = text
        normalized = text
        corrections = []
        medical_entities = []
        
        # Step 1: Preserve medical entities before processing
        medical_entities = self._extract_and_preserve_medical_entities(normalized)
        
        # Step 2: Fix basic capitalization first
        normalized, caps_corrections = self._fix_basic_capitalization(normalized)
        corrections.extend(caps_corrections)
        
        # Step 3: Expand abbreviations early (before grammar corrections)
        normalized, abbrev_corrections = self._expand_abbreviations(normalized)
        corrections.extend(abbrev_corrections)
        
        # Step 4: Correct medical spelling errors
        normalized, spell_corrections = self._correct_medical_spelling(normalized)
        corrections.extend(spell_corrections)
        
        # Step 5: Fix pronoun patterns (me -> my, i -> I) 
        normalized, pronoun_corrections = self._fix_pronoun_patterns(normalized)
        corrections.extend(pronoun_corrections)
        
        # Step 6: Apply grammar corrections (includes complex patterns)
        normalized, grammar_corrections = self._apply_grammar_corrections(normalized)
        corrections.extend(grammar_corrections)
        
        # Step 7: Convert informal to formal medical language (Step 1.3 Enhancement)
        normalized, informal_corrections = self._convert_informal_to_formal(normalized)
        corrections.extend(informal_corrections)
        
        # Step 8: Fix verb tenses for medical context
        normalized, tense_corrections = self._fix_verb_tenses(normalized)
        corrections.extend(tense_corrections)
        
        # Step 9: Final cleanup and ensure proper sentence capitalization
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        # Ensure first letter is capitalized
        if normalized and normalized[0].islower():
            normalized = normalized[0].upper() + normalized[1:]
        
        # Calculate confidence score based on corrections applied
        confidence_score = self._calculate_confidence_score(original_text, normalized, corrections)
        
        # Collect spell correction details for analysis
        spell_correction_details = []
        words = re.findall(r'\b[a-zA-Z]+\b', original_text)
        for word in words:
            if len(word) > 2:
                spell_result = self.advanced_spell_checker.correct_medical_spelling(word)
                if spell_result.corrected_word.lower() != spell_result.original_word.lower():
                    spell_correction_details.append(spell_result)
        
        return NormalizationResult(
            original_text=original_text,
            normalized_text=normalized,
            corrections_applied=corrections,
            confidence_score=confidence_score,
            medical_entities_preserved=medical_entities,
            spell_corrections=spell_correction_details
        )
    
    def _load_grammar_patterns(self) -> List[Dict[str, str]]:
        """Load grammar correction patterns for medical text"""
        return [
            # Specific fever pattern (most specific first)
            {"pattern": r"\bI\s+having\s+fever\s+(\d+)\s+days?\b", "replacement": r"I have been having a fever for \1 days", "desc": "I having fever X days -> I have been having a fever for X days"},
            
            # General "having" patterns  
            {"pattern": r"\bI\s+having\s+", "replacement": "I have been having ", "desc": "I having -> I have been having"},
            {"pattern": r"\bi\s+having\s+", "replacement": "I have been having ", "desc": "i having -> I have been having"},
            {"pattern": r"\bi\s+have\s+", "replacement": "I have ", "desc": "capitalize I"},
            {"pattern": r"\bi\s+am\s+having\s+", "replacement": "I have been having ", "desc": "i am having -> I have been having"},
            {"pattern": r"\bi\s+got\s+", "replacement": "I have ", "desc": "i got -> I have"},
            {"pattern": r"\bme\s+(.+?)\s+hurt", "replacement": r"my \1 hurts", "desc": "me X hurt -> my X hurts"},
            {"pattern": r"\bme\s+(.+?)\s+pain", "replacement": r"my \1 has pain", "desc": "me X pain -> my X has pain"},
            
            # When/while corrections for breathing and symptoms
            {"pattern": r"\bwhen\s+breath\b", "replacement": "when I breathe", "desc": "when breath -> when I breathe"},
            {"pattern": r"\bwhen\s+breathe\b", "replacement": "when I breathe", "desc": "when breathe -> when I breathe"},
            {"pattern": r"\bwhen\s+eat\b", "replacement": "when I eat", "desc": "when eat -> when I eat"},
            {"pattern": r"\bwhen\s+walk\b", "replacement": "when I walk", "desc": "when walk -> when I walk"},
            
            # Common medical grammar patterns
            {"pattern": r"\bhurt\s+when\b", "replacement": "hurts when", "desc": "hurt when -> hurts when"},
            {"pattern": r"\bpain\s+when\b", "replacement": "painful when", "desc": "pain when -> painful when"},
        ]
    
    def _load_medical_spell_corrections(self) -> Dict[str, str]:
        """Load medical spelling corrections dictionary"""
        return {
            # Common medical term misspellings
            "haedache": "headache",
            "headach": "headache", 
            "headake": "headache",
            "cheast": "chest",
            "stomache": "stomach",
            "stomack": "stomach",
            "tummy": "stomach",
            "diabetis": "diabetes",
            "diabeties": "diabetes",
            "preassure": "pressure",
            "pressur": "pressure",
            "temperatur": "temperature",
            "temprature": "temperature",
            "nausea": "nausea",  # Often misspelled as "nauseus"
            "nauseus": "nausea",
            "nausia": "nausea",
            "dizzy": "dizzy",
            "dizy": "dizzy",
            "throwin up": "throwing up",
            "trowing up": "throwing up",
        }
    
    def _load_informal_to_formal_medical(self) -> Dict[str, str]:
        """Load comprehensive informal to formal medical language mappings - Step 1.3 Enhancement"""
        return {
            # DIGESTIVE SYSTEM - Colloquial to medical standard
            "tummy hurt": "abdominal pain",
            "tummy hurts": "abdominal pain", 
            "tummy pain": "abdominal pain",
            "tummy ache": "abdominal pain",
            "belly pain": "abdominal pain",
            "belly hurt": "abdominal pain",
            "belly hurts": "abdominal pain",
            "belly ache": "abdominal pain",
            "stomach hurt": "abdominal pain",
            "stomach hurts": "abdominal pain",
            "gut pain": "abdominal pain",
            "gut hurt": "abdominal pain",
            
            # BOWEL MOVEMENTS
            "can't poop": "experiencing constipation",
            "cant poop": "experiencing constipation",
            "cannot poop": "experiencing constipation",
            "trouble pooping": "difficulty with bowel movements",
            "hard to poop": "difficulty with bowel movements",
            "blocked up": "experiencing constipation",
            "backed up": "experiencing constipation",
            "the runs": "experiencing diarrhea",
            "loose stools": "loose bowel movements",
            "runny poop": "loose bowel movements",
            
            # NAUSEA & VOMITING
            "throwing up": "vomiting",
            "puking": "vomiting",
            "barfing": "vomiting",
            "upchucking": "vomiting",
            "feeling sick": "experiencing nausea",
            "queasy": "nauseous",
            "gonna be sick": "feeling nauseous",
            "gonna throw up": "feeling nauseous",
            
            # GENERAL FEELING UNWELL
            "feeling crappy": "feeling unwell",
            "feel crappy": "feel unwell",
            "feeling awful": "feeling unwell",
            "feel awful": "feel unwell",
            "feeling lousy": "feeling unwell",
            "feel lousy": "feel unwell",
            "feeling rough": "feeling unwell",
            "feel rough": "feel unwell",
            "feeling terrible": "feeling very unwell",
            "feel terrible": "feel very unwell",
            "feeling like crap": "feeling unwell",
            "feel like crap": "feel unwell",
            "under the weather": "feeling unwell",
            "not feeling good": "feeling unwell",
            "don't feel good": "not feeling well",
            "dont feel good": "not feeling well",
            "feeling off": "feeling unwell",
            "feel off": "feel unwell",
            
            # DIZZINESS & BALANCE
            "dizzy spells": "episodes of dizziness",
            "head spinning": "experiencing dizziness",
            "lightheaded": "experiencing lightheadedness",
            "woozy": "dizzy",
            "feeling faint": "experiencing lightheadedness",
            "about to pass out": "feeling faint",
            "gonna faint": "feeling faint",
            "room spinning": "experiencing vertigo",
            
            # PAIN DESCRIPTORS
            "really bad": "severe",
            "super bad": "severe", 
            "awful pain": "severe pain",
            "terrible pain": "severe pain",
            "killing me": "severe pain",
            "excruciating": "extremely severe",
            "unbearable": "extremely severe",
            "sharp pain": "acute pain",
            "stabbing pain": "sharp stabbing pain",
            "throbbing": "pulsating pain",
            "pounding": "throbbing pain",
            
            # BREATHING ISSUES
            "can't breathe": "difficulty breathing",
            "cant breathe": "difficulty breathing",
            "cannot breathe": "difficulty breathing",
            "short of breath": "experiencing shortness of breath",
            "out of breath": "experiencing breathlessness",
            "winded": "short of breath",
            "gasping": "having difficulty breathing",
            "wheezing": "experiencing wheezing",
            
            # SLEEP ISSUES
            "can't sleep": "experiencing insomnia",
            "cant sleep": "experiencing insomnia",
            "cannot sleep": "experiencing insomnia",
            "trouble sleeping": "difficulty sleeping",
            "tossing and turning": "restless sleep",
            "wide awake": "experiencing insomnia",
            
            # FATIGUE & ENERGY
            "wiped out": "extremely fatigued",
            "exhausted": "severely fatigued",
            "drained": "feeling fatigued",
            "beat": "feeling tired",
            "pooped": "feeling tired",
            "worn out": "feeling fatigued",
            "dead tired": "extremely fatigued",
            "no energy": "experiencing fatigue",
            
            # HEADACHES
            "head hurts": "experiencing headache",
            "head is pounding": "experiencing severe headache",
            "splitting headache": "severe headache",
            "migraine": "severe headache",
            "head is killing me": "severe headache",
            
            # FEVER & TEMPERATURE
            "burning up": "experiencing fever",
            "running a fever": "having a fever",
            "feverish": "feeling feverish",
            "hot and cold": "experiencing chills and fever",
            "the chills": "experiencing chills",
            "shivering": "experiencing chills",
            
            # CHEST & HEART
            "chest tight": "chest tightness",
            "chest heavy": "chest pressure",
            "heart racing": "experiencing rapid heartbeat",
            "heart pounding": "experiencing palpitations",
            "fluttering heart": "experiencing palpitations",
            
            # THROAT ISSUES  
            "sore throat": "throat pain",
            "scratchy throat": "throat irritation",
            "throat hurts": "throat pain",
            "can't swallow": "difficulty swallowing",
            "cant swallow": "difficulty swallowing",
            
            # SKIN CONDITIONS
            "itchy": "experiencing itching",
            "scratchy": "experiencing itching",
            "breaking out": "developing a rash",
            "bumps": "skin lesions",
            "spots": "skin lesions",
            
            # MUSCLE & JOINT
            "achy": "experiencing aches",
            "stiff": "experiencing stiffness",
            "creaky joints": "joint stiffness",
            "sore muscles": "muscle pain",
            "muscle cramps": "muscle spasms",
            
            # MENTAL HEALTH
            "stressed out": "experiencing stress",
            "anxious": "feeling anxious",
            "worried sick": "extremely anxious",
            "freaking out": "experiencing anxiety",
            "bummed out": "feeling depressed",
            "down in the dumps": "feeling depressed",
            
            # URGENCY EXPRESSIONS
            "really urgent": "urgent medical concern",
            "emergency": "urgent medical situation",
            "need help now": "urgent medical attention needed",
            "something's wrong": "experiencing concerning symptoms",
        }
    
    def _load_abbreviation_expansions(self) -> Dict[str, str]:
        """Load abbreviation expansion mappings"""
        return {
            # Common abbreviations in medical context
            " n ": " and ",
            " & ": " and ",
            " w/ ": " with ",
            " w/o ": " without ",
            " b4 ": " before ",
            " ur ": " your ",
            " u ": " you ",
            " r ": " are ",
            " cant ": " cannot ",
            " wont ": " will not ",
            " dont ": " do not ",
            " doesnt ": " does not ",
            " isnt ": " is not ",
            " wasnt ": " was not ",
        }
    
    def _load_pronoun_corrections(self) -> List[Dict[str, str]]:
        """Load pronoun correction patterns"""
        return [
            {"pattern": r"\bme\s+", "replacement": "my ", "desc": "me -> my (when possessive)"},
            {"pattern": r"^i\s+", "replacement": "I ", "desc": "sentence start i -> I"},
            {"pattern": r"\s+i\s+", "replacement": " I ", "desc": "middle sentence i -> I"},
        ]
    
    def _load_verb_tense_patterns(self) -> List[Dict[str, str]]:
        """Load verb tense correction patterns for medical context"""
        return [
            # Only apply these if the grammar patterns didn't already handle it
            {"pattern": r"\bhurt\s+(\d+)\s+days?", "replacement": r"has been hurting for \1 days", "desc": "hurt X days -> has been hurting for X days"},
            {"pattern": r"\bpain\s+(\d+)\s+days?", "replacement": r"pain for \1 days", "desc": "pain X days -> pain for X days"},
            # Skip fever pattern as it's handled by grammar patterns
        ]
    
    def _extract_and_preserve_medical_entities(self, text: str) -> List[str]:
        """Extract and preserve important medical entities during processing"""
        medical_entities = []
        
        # Extract numbers with medical units
        number_patterns = [
            r'\d+/\d+',  # Blood pressure, pain scale
            r'\d+\s*mg',  # Medications
            r'\d+\s*degrees?',  # Temperature
            r'\d+\s*bpm',  # Heart rate
        ]
        
        for pattern in number_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            medical_entities.extend(matches)
        
        return medical_entities
    
    def _fix_basic_capitalization(self, text: str) -> Tuple[str, List[str]]:
        """Fix basic capitalization issues"""
        corrections = []
        original = text
        
        # Capitalize first letter of sentence
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
            corrections.append("Capitalized sentence start")
        
        # Capitalize 'I' when standalone
        text = re.sub(r'\bi\b', 'I', text)
        if 'i' in original and 'I' in text:
            corrections.append("Capitalized pronoun 'I'")
        
        return text, corrections
    
    def _correct_medical_spelling(self, text: str) -> Tuple[str, List[str]]:
        """Advanced medical spelling correction using Step 1.2 enhancement"""
        corrections = []
        
        # Step 1: Apply basic dictionary corrections first (for compatibility)
        for misspelled, correct in self.medical_spell_corrections.items():
            if misspelled.lower() in text.lower():
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(misspelled) + r'\b'
                if re.search(pattern, text, re.IGNORECASE):
                    text = re.sub(pattern, correct, text, flags=re.IGNORECASE)
                    corrections.append(f"Basic spelling correction: '{misspelled}' -> '{correct}'")
        
        # Step 2: Apply advanced spell checking to all words (Step 1.2 enhancement)
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        
        for word in words:
            if len(word) > 2:  # Only check words longer than 2 characters
                spell_result = self.advanced_spell_checker.correct_medical_spelling(word)
                
                # Apply correction if confidence is high enough and word actually changed
                if (spell_result.confidence_score >= 0.7 and 
                    spell_result.corrected_word.lower() != spell_result.original_word.lower()):
                    
                    # Replace the word in text (case-preserving)
                    pattern = r'\b' + re.escape(word) + r'\b'
                    text = re.sub(pattern, spell_result.corrected_word, text, flags=re.IGNORECASE)
                    
                    corrections.append(
                        f"Advanced spelling correction: '{spell_result.original_word}' -> "
                        f"'{spell_result.corrected_word}' (confidence: {spell_result.confidence_score:.2f}, "
                        f"method: {spell_result.correction_method})"
                    )
        
        return text, corrections
    
    def _fix_pronoun_patterns(self, text: str) -> Tuple[str, List[str]]:
        """Fix pronoun usage patterns"""
        corrections = []
        
        for pattern_info in self.pronoun_corrections:
            pattern = pattern_info["pattern"]
            replacement = pattern_info["replacement"]
            desc = pattern_info["desc"]
            
            if re.search(pattern, text, re.IGNORECASE):
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
                corrections.append(f"Fixed pronoun: {desc}")
        
        return text, corrections
    
    def _apply_grammar_corrections(self, text: str) -> Tuple[str, List[str]]:
        """Apply comprehensive grammar corrections"""
        corrections = []
        
        for pattern_info in self.grammar_patterns:
            pattern = pattern_info["pattern"]
            replacement = pattern_info["replacement"]
            desc = pattern_info["desc"]
            
            if re.search(pattern, text, re.IGNORECASE):
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
                corrections.append(f"Grammar correction: {desc}")
        
        return text, corrections
    
    def _expand_abbreviations(self, text: str) -> Tuple[str, List[str]]:
        """Expand common abbreviations"""
        corrections = []
        
        for abbrev, expansion in self.abbreviation_expansions.items():
            if abbrev in text:
                text = text.replace(abbrev, expansion)
                corrections.append(f"Expanded abbreviation: '{abbrev.strip()}' -> '{expansion.strip()}'")
        
        return text, corrections
    
    def _convert_informal_to_formal(self, text: str) -> Tuple[str, List[str]]:
        """Convert informal language to formal medical language"""
        corrections = []
        
        for informal, formal in self.informal_to_formal_medical.items():
            if informal.lower() in text.lower():
                # Use word boundaries for better matching
                pattern = r'\b' + re.escape(informal) + r'\b'
                if re.search(pattern, text, re.IGNORECASE):
                    text = re.sub(pattern, formal, text, flags=re.IGNORECASE)
                    corrections.append(f"Formalized language: '{informal}' -> '{formal}'")
        
        return text, corrections
    
    def _fix_verb_tenses(self, text: str) -> Tuple[str, List[str]]:
        """Fix verb tenses for medical context"""
        corrections = []
        
        for pattern_info in self.verb_tense_patterns:
            pattern = pattern_info["pattern"]
            replacement = pattern_info["replacement"]
            desc = pattern_info["desc"]
            
            if re.search(pattern, text, re.IGNORECASE):
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
                corrections.append(f"Fixed verb tense: {desc}")
        
        return text, corrections
    
    def _final_cleanup(self, text: str) -> Tuple[str, List[str]]:
        """Final cleanup and sentence structure fixes"""
        corrections = []
        original = text
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common punctuation issues
        text = re.sub(r'\s+\.', '.', text)  # Remove space before period
        text = re.sub(r'\s+,', ',', text)   # Remove space before comma
        
        # Ensure proper sentence ending
        if text and not text.endswith(('.', '!', '?')):
            text = text + '.'
            corrections.append("Added sentence ending punctuation")
        
        if text != original:
            corrections.append("Applied final formatting cleanup")
        
        return text, corrections
    
    def _calculate_confidence_score(self, original: str, normalized: str, corrections: List[str]) -> float:
        """Calculate confidence score based on normalization quality"""
        
        # Base confidence
        confidence = 0.8
        
        # Adjust based on number of corrections
        num_corrections = len(corrections)
        if num_corrections == 0:
            confidence = 1.0  # Perfect input
        elif num_corrections <= 2:
            confidence = 0.95  # Minor corrections
        elif num_corrections <= 4:
            confidence = 0.85  # Moderate corrections
        elif num_corrections <= 6:
            confidence = 0.75  # Significant corrections
        else:
            confidence = 0.65  # Major corrections needed
        
        # Adjust for length and complexity
        word_count = len(original.split())
        if word_count < 3:
            confidence -= 0.05  # Very short text is harder to normalize accurately
        
        # Boost confidence for successful medical term preservation
        medical_terms = ["pain", "hurt", "fever", "headache", "chest", "stomach", "breathing", "vomiting"]
        preserved_terms = sum(1 for term in medical_terms if term in normalized.lower())
        confidence += min(preserved_terms * 0.02, 0.1)
        
        return min(max(confidence, 0.5), 1.0)  # Clamp between 0.5 and 1.0


# Convenience function for easy integration
def normalize_medical_text(text: str) -> NormalizationResult:
    """
    Convenience function to normalize medical text
    
    Args:
        text (str): Raw medical text to normalize
        
    Returns:
        NormalizationResult: Normalized text with metadata
    """
    normalizer = IntelligentTextNormalizer()
    return normalizer.normalize_medical_text(text)


# Test function to validate the examples from the requirements
def test_normalization_examples():
    """Test the specific examples mentioned in the requirements"""
    
    normalizer = IntelligentTextNormalizer()
    
    test_cases = [
        ("i having fever 2 days", "I have been having a fever for 2 days"),
        ("me chest hurt when breath", "My chest hurts when I breathe"),
        ("haedache really bad", "Headache really bad"),
        ("stomach ache n vomiting", "Stomach ache and vomiting"),
    ]
    
    print("Testing Text Normalization Examples:")
    print("=" * 50)
    
    for original, expected in test_cases:
        result = normalizer.normalize_medical_text(original)
        print(f"Original: '{original}'")
        print(f"Expected: '{expected}'")
        print(f"Actual:   '{result.normalized_text}'")
        print(f"Match:    {result.normalized_text.lower() == expected.lower()}")
        print(f"Corrections: {result.corrections_applied}")
        print(f"Confidence: {result.confidence_score:.2f}")
        print("-" * 40)


if __name__ == "__main__":
    # Run tests when script is executed directly
    test_normalization_examples()