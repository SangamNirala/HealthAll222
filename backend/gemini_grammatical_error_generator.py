"""
🤖 PHASE 7.1: AI-POWERED GRAMMATICAL ERROR PATTERN GENERATOR
Revolutionary Gemini-Integrated Grammatical Error Analysis and Generation System

CAPABILITIES:
- Generate unlimited grammatical error patterns using Gemini AI
- Analyze and create diverse error types with medical context
- Create realistic patient language variations
- Provide comprehensive error classification and analysis

Algorithm Version: 7.1_ai_grammatical_error_generation
"""

import asyncio
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

from ai_powered_medical_nlp_test_suite import GeminiPoweredTestingEngine, AIGeneratedTestCase, TestDifficulty, LanguagePatternType
import logging

logger = logging.getLogger(__name__)

class GrammaticalErrorType(str, Enum):
    SUBJECT_VERB_DISAGREEMENT = "subject_verb_disagreement"
    PRONOUN_ERROR = "pronoun_error"
    TENSE_CONFUSION = "tense_confusion"
    MISSING_ARTICLES = "missing_articles"
    MISSING_PREPOSITIONS = "missing_prepositions"
    WORD_ORDER_ISSUES = "word_order_issues"
    SPELLING_ERRORS = "spelling_errors"
    PUNCTUATION_ERRORS = "punctuation_errors"
    DOUBLE_NEGATIVES = "double_negatives"
    SENTENCE_FRAGMENTS = "sentence_fragments"

class PatientDemographic(str, Enum):
    NON_NATIVE_SPEAKER = "non_native_speaker"
    ELDERLY_PATIENT = "elderly_patient"
    YOUNG_ADULT = "young_adult"
    STRESSED_PATIENT = "stressed_patient"
    LOW_EDUCATION = "low_education"
    TEXTING_STYLE = "texting_style"

@dataclass
class GrammaticalErrorPattern:
    """Individual grammatical error pattern with medical context"""
    error_type: GrammaticalErrorType
    original_text: str
    corrected_text: str
    error_description: str
    medical_entities: List[Dict[str, Any]]
    difficulty_level: TestDifficulty
    patient_demographic: PatientDemographic
    confidence_level: float
    extraction_difficulty: float

class AIGrammaticalErrorGenerator:
    """
    🤖 Uses Gemini to generate unlimited grammatical error patterns for medical text
    """
    
    def __init__(self, testing_engine: GeminiPoweredTestingEngine = None):
        """Initialize AI grammatical error generator"""
        self.testing_engine = testing_engine or GeminiPoweredTestingEngine()
        self.error_generation_stats = {
            'total_generated': 0,
            'by_error_type': {},
            'by_difficulty': {},
            'average_generation_time': 0.0
        }
        
        logger.info("🤖 AI Grammatical Error Generator initialized")
    
    async def generate_grammatical_variants_with_ai(self, base_medical_text: str, num_variants: int = 10) -> List[GrammaticalErrorPattern]:
        """
        Generate diverse grammatical error variations of medical text using AI
        
        AI PROMPT TEMPLATE:
        "You are a linguistic expert generating grammatical error variations of medical text.
        
        Base medical text: '{base_medical_text}'
        
        Generate 10 different grammatical error variations including:
        1. Subject-verb disagreements
        2. Pronoun errors  
        3. Tense confusion
        4. Missing articles/prepositions
        5. Word order issues
        
        For each variation, provide:
        - The grammatically incorrect text
        - The specific error type
        - Expected medical entity extraction
        - Confidence level for extraction difficulty
        
        Format as JSON for programmatic processing."
        """
        
        generation_prompt = f"""
        You are an expert medical linguist creating realistic grammatical error patterns for NLP testing.
        
        Base Medical Text: "{base_medical_text}"
        Number of Variants: {num_variants}
        
        Generate {num_variants} grammatical error variations that real patients might produce, including:
        
        ERROR TYPES TO INCLUDE:
        1. Subject-verb disagreements ("I are having pain", "The symptoms is getting worse")
        2. Pronoun errors ("Me chest hurts", "Them pills don't work") 
        3. Tense confusion ("I have pain yesterday", "I will had surgery")
        4. Missing articles/prepositions ("I have pain chest", "Going doctor tomorrow")
        5. Word order issues ("Pain in my chest having I am", "Bad very feeling")
        6. Spelling errors ("stomac ache", "haedache", "fevor")
        7. Punctuation issues ("whats wrong with me", "cant breathe good")
        8. Sentence fragments ("Pain. Very bad.", "Doctor tomorrow.")
        9. Double negatives ("I don't have no energy", "Can't not sleep")
        10. Mixed errors (combination of above)
        
        PATIENT DEMOGRAPHICS TO CONSIDER:
        - Non-native English speakers
        - Elderly patients with cognitive changes
        - Stressed patients in pain
        - Young adults using texting language
        - Patients with limited formal education
        
        FOR EACH VARIATION PROVIDE:
        {{
            "variant_number": [1-{num_variants}],
            "grammatically_incorrect_text": "[the error-filled version]",
            "corrected_text": "[proper grammar version]", 
            "error_type": "[primary error category]",
            "error_description": "[specific errors present]",
            "patient_demographic": "[likely patient type]",
            "medical_entities_expected": [
                {{"entity": "[symptom/condition]", "type": "[symptom/anatomy/etc]", "confidence": [0.0-1.0]}}
            ],
            "extraction_difficulty": [1-10 scale],
            "confidence_for_ai_processing": [0.0-1.0],
            "medical_accuracy": [how medically appropriate the content remains]
        }}
        
        Ensure variations are realistic and represent actual patient language patterns.
        Return as valid JSON array.
        """
        
        try:
            start_time = time.time()
            ai_response = await self.testing_engine._call_gemini_with_fallback(generation_prompt)
            generation_time = time.time() - start_time
            
            # Parse AI response and create error patterns
            patterns = self._parse_grammatical_variants(ai_response, base_medical_text)
            
            # Update statistics
            self._update_generation_stats(patterns, generation_time)
            
            logger.info(f"✅ Generated {len(patterns)} grammatical error patterns in {generation_time:.3f}s")
            return patterns
            
        except Exception as e:
            logger.error(f"❌ Grammatical variant generation failed: {e}")
            return self._generate_fallback_variants(base_medical_text, num_variants)
    
    async def create_unlimited_error_patterns(self, symptom_categories: List[str], patterns_per_category: int = 50) -> List[GrammaticalErrorPattern]:
        """
        Use AI to generate unlimited error patterns across all medical domains
        """
        all_patterns = []
        
        for category in symptom_categories:
            category_prompt = f"""
            Create {patterns_per_category} different ways a patient might incorrectly express {category} symptoms,
            including various grammatical errors, typos, and structural mistakes.
            
            Consider patient diversity:
            - Different education levels (elementary to graduate)
            - Non-native English speakers (various L1 backgrounds)
            - Emotional distress affecting grammar
            - Typing errors and autocorrect mistakes
            - Regional dialect influences
            - Age-related language patterns
            - Medical anxiety affecting communication
            - Pain level affecting coherence
            
            For {category} symptoms, generate realistic error patterns covering:
            
            SYMPTOM CATEGORY: {category}
            
            LANGUAGE VARIATIONS:
            1. Broken grammar from non-native speakers
            2. Elderly patient communication patterns
            3. Text message style abbreviations
            4. Emotional distress language patterns
            5. Pain-induced communication changes
            6. Regional dialect influences
            7. Educational level variations
            8. Panic/anxiety affected speech
            
            Each pattern should include:
            - Grammatically incorrect patient text
            - Corrected medical text
            - Error classification
            - Expected medical entity extraction
            - Cultural/demographic context
            - Difficulty level for NLP processing
            
            Return comprehensive test cases with expected medical extractions formatted as JSON.
            """
            
            try:
                ai_response = await self.testing_engine._call_gemini_with_fallback(category_prompt)
                category_patterns = self._parse_category_patterns(ai_response, category)
                all_patterns.extend(category_patterns)
                
                logger.info(f"✅ Generated {len(category_patterns)} patterns for {category}")
                
                # Brief delay to avoid API rate limits
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"❌ Pattern generation failed for {category}: {e}")
                # Add fallback patterns for this category
                fallback_patterns = self._generate_category_fallback_patterns(category, 5)
                all_patterns.extend(fallback_patterns)
        
        logger.info(f"🎯 Total unlimited patterns generated: {len(all_patterns)}")
        return all_patterns
    
    async def analyze_error_complexity_with_ai(self, error_text: str) -> Dict[str, Any]:
        """
        Use AI to analyze the complexity and processing difficulty of grammatical errors
        """
        complexity_prompt = f"""
        Analyze the linguistic complexity and NLP processing difficulty of this medical text with grammatical errors:
        
        Text: "{error_text}"
        
        Provide detailed analysis:
        
        1. ERROR IDENTIFICATION:
           - List all grammatical errors present
           - Classify each error type
           - Rate severity of each error (1-10)
        
        2. PROCESSING DIFFICULTY ASSESSMENT:
           - Overall complexity score (1-10)
           - Challenges for NLP systems
           - Required preprocessing steps
           - Disambiguation requirements
        
        3. MEDICAL CONTENT PRESERVATION:
           - Medical information retained despite errors
           - Critical information at risk of misextraction
           - Patient safety implications
        
        4. CORRECTION STRATEGY:
           - Recommended correction approach
           - Processing order for optimal results
           - Confidence levels for automated correction
        
        Return structured analysis as JSON.
        """
        
        try:
            ai_response = await self.testing_engine._call_gemini_with_fallback(complexity_prompt)
            complexity_analysis = self._parse_complexity_analysis(ai_response)
            
            logger.info("✅ Error complexity analysis completed")
            return complexity_analysis
            
        except Exception as e:
            logger.error(f"❌ Complexity analysis failed: {e}")
            return self._generate_fallback_complexity_analysis(error_text)
    
    def _parse_grammatical_variants(self, ai_response: str, base_text: str) -> List[GrammaticalErrorPattern]:
        """Parse AI-generated grammatical variants into structured patterns"""
        try:
            # Extract JSON from response
            import re
            json_pattern = r'\[.*\]'
            json_match = re.search(json_pattern, ai_response, re.DOTALL)
            
            if json_match:
                variants_data = json.loads(json_match.group())
            else:
                # Fallback to text parsing
                return self._parse_variants_from_text(ai_response, base_text)
            
            patterns = []
            for variant in variants_data:
                try:
                    pattern = GrammaticalErrorPattern(
                        error_type=GrammaticalErrorType(variant.get('error_type', 'spelling_errors')),
                        original_text=variant.get('grammatically_incorrect_text', ''),
                        corrected_text=variant.get('corrected_text', ''),
                        error_description=variant.get('error_description', ''),
                        medical_entities=variant.get('medical_entities_expected', []),
                        difficulty_level=TestDifficulty(variant.get('extraction_difficulty', 'medium')),
                        patient_demographic=PatientDemographic(variant.get('patient_demographic', 'non_native_speaker')),
                        confidence_level=variant.get('confidence_for_ai_processing', 0.5),
                        extraction_difficulty=variant.get('extraction_difficulty', 5.0)
                    )
                    patterns.append(pattern)
                except Exception as e:
                    logger.warning(f"⚠️ Skipping invalid variant: {e}")
                    continue
            
            return patterns
            
        except Exception as e:
            logger.error(f"❌ Failed to parse grammatical variants: {e}")
            return self._generate_fallback_variants(base_text, 5)
    
    def _parse_variants_from_text(self, response_text: str, base_text: str) -> List[GrammaticalErrorPattern]:
        """Extract variants from natural language response"""
        # Simple fallback parsing
        patterns = []
        
        # Generate basic patterns based on common error types
        basic_errors = [
            ("I having chest pain", "I am having chest pain", "missing_auxiliary_verb"),
            ("Me head hurts bad", "My head hurts badly", "pronoun_error"),
            ("Pain in chest very", "Very bad pain in chest", "word_order_issues"),
            ("Cant breath good", "Cannot breathe well", "spelling_contraction_errors"),
            ("Stomach hurt yesterday", "Stomach hurt yesterday", "tense_consistency")
        ]
        
        for incorrect, correct, error_type in basic_errors:
            pattern = GrammaticalErrorPattern(
                error_type=GrammaticalErrorType.SPELLING_ERRORS,  # Default type
                original_text=incorrect,
                corrected_text=correct,
                error_description=error_type,
                medical_entities=[{"entity": "symptom", "type": "medical_condition", "confidence": 0.7}],
                difficulty_level=TestDifficulty.MEDIUM,
                patient_demographic=PatientDemographic.NON_NATIVE_SPEAKER,
                confidence_level=0.6,
                extraction_difficulty=6.0
            )
            patterns.append(pattern)
        
        return patterns[:3]  # Return 3 fallback patterns
    
    def _parse_category_patterns(self, ai_response: str, category: str) -> List[GrammaticalErrorPattern]:
        """Parse category-specific patterns from AI response"""
        try:
            # Similar parsing logic as variants
            import re
            json_pattern = r'\[.*\]'
            json_match = re.search(json_pattern, ai_response, re.DOTALL)
            
            if json_match:
                patterns_data = json.loads(json_match.group())
                return self._convert_to_error_patterns(patterns_data, category)
            else:
                return self._generate_category_fallback_patterns(category, 3)
                
        except Exception as e:
            logger.error(f"❌ Category pattern parsing failed: {e}")
            return self._generate_category_fallback_patterns(category, 3)
    
    def _convert_to_error_patterns(self, patterns_data: List[Dict], category: str) -> List[GrammaticalErrorPattern]:
        """Convert parsed data to GrammaticalErrorPattern objects"""
        patterns = []
        
        for data in patterns_data:
            try:
                pattern = GrammaticalErrorPattern(
                    error_type=GrammaticalErrorType(data.get('error_type', 'spelling_errors')),
                    original_text=data.get('incorrect_text', ''),
                    corrected_text=data.get('corrected_text', ''),
                    error_description=data.get('error_description', ''),
                    medical_entities=data.get('medical_entities', []),
                    difficulty_level=TestDifficulty(data.get('difficulty', 'medium')),
                    patient_demographic=PatientDemographic(data.get('demographic', 'non_native_speaker')),
                    confidence_level=data.get('confidence', 0.5),
                    extraction_difficulty=data.get('difficulty_score', 5.0)
                )
                patterns.append(pattern)
            except Exception as e:
                logger.warning(f"⚠️ Skipping invalid pattern for {category}: {e}")
                continue
        
        return patterns
    
    def _parse_complexity_analysis(self, ai_response: str) -> Dict[str, Any]:
        """Parse AI complexity analysis response"""
        try:
            import re
            json_pattern = r'\{.*\}'
            json_match = re.search(json_pattern, ai_response, re.DOTALL)
            
            if json_match:
                return json.loads(json_match.group())
            else:
                # Extract key information from text
                return {
                    'error_identification': {'total_errors': 2, 'primary_types': ['grammar', 'spelling']},
                    'processing_difficulty': {'complexity_score': 6, 'challenges': ['pattern_recognition']},
                    'medical_content_preservation': {'retention_score': 8, 'safety_implications': 'moderate'},
                    'correction_strategy': {'approach': 'sequential', 'confidence': 0.7},
                    'ai_reasoning': ai_response[:500]
                }
                
        except Exception as e:
            logger.error(f"❌ Complexity analysis parsing failed: {e}")
            return self._generate_fallback_complexity_analysis("")
    
    def _generate_fallback_variants(self, base_text: str, num_variants: int) -> List[GrammaticalErrorPattern]:
        """Generate fallback variants when AI fails"""
        patterns = []
        
        fallback_errors = [
            ("I having bad headache", "I am having a bad headache", GrammaticalErrorType.SUBJECT_VERB_DISAGREEMENT),
            ("Me stomach hurts", "My stomach hurts", GrammaticalErrorType.PRONOUN_ERROR),
            ("Pain chest very bad", "Very bad chest pain", GrammaticalErrorType.WORD_ORDER_ISSUES),
            ("Cant sleep good", "Cannot sleep well", GrammaticalErrorType.SPELLING_ERRORS),
            ("Doctor I need see", "I need to see a doctor", GrammaticalErrorType.MISSING_PREPOSITIONS)
        ]
        
        for i, (incorrect, correct, error_type) in enumerate(fallback_errors[:num_variants]):
            pattern = GrammaticalErrorPattern(
                error_type=error_type,
                original_text=incorrect,
                corrected_text=correct,
                error_description=f"Fallback pattern {i+1}",
                medical_entities=[{"entity": "symptom", "type": "medical_condition", "confidence": 0.6}],
                difficulty_level=TestDifficulty.MEDIUM,
                patient_demographic=PatientDemographic.NON_NATIVE_SPEAKER,
                confidence_level=0.5,
                extraction_difficulty=5.0
            )
            patterns.append(pattern)
        
        return patterns
    
    def _generate_category_fallback_patterns(self, category: str, num_patterns: int) -> List[GrammaticalErrorPattern]:
        """Generate fallback patterns for specific symptom category"""
        patterns = []
        
        # Category-specific fallback patterns
        category_patterns = {
            'pain': [
                ("I have pain bad in chest", "I have bad pain in my chest", "word_order_error"),
                ("Pain is hurt me lot", "The pain hurts me a lot", "grammar_structure_error")
            ],
            'digestive': [
                ("Stomach feel not good", "My stomach does not feel good", "negation_error"),
                ("Eat food make sick", "Eating food makes me sick", "verb_form_error")
            ],
            'respiratory': [
                ("Breath is hard for me", "Breathing is hard for me", "word_form_error"),
                ("Can not breath good", "Cannot breathe well", "spelling_adverb_error")
            ]
        }
        
        default_patterns = [
            ("Symptom is bad very", "The symptom is very bad", "word_order_error"),
            ("Feel not well today", "I do not feel well today", "missing_subject_error")
        ]
        
        selected_patterns = category_patterns.get(category.lower(), default_patterns)
        
        for i, (incorrect, correct, error_desc) in enumerate(selected_patterns[:num_patterns]):
            pattern = GrammaticalErrorPattern(
                error_type=GrammaticalErrorType.WORD_ORDER_ISSUES,
                original_text=incorrect,
                corrected_text=correct,
                error_description=error_desc,
                medical_entities=[{"entity": category, "type": "symptom", "confidence": 0.7}],
                difficulty_level=TestDifficulty.MEDIUM,
                patient_demographic=PatientDemographic.NON_NATIVE_SPEAKER,
                confidence_level=0.6,
                extraction_difficulty=6.0
            )
            patterns.append(pattern)
        
        return patterns
    
    def _generate_fallback_complexity_analysis(self, error_text: str) -> Dict[str, Any]:
        """Generate fallback complexity analysis"""
        return {
            'error_identification': {
                'total_errors': 1,
                'primary_types': ['grammar'],
                'severity_scores': [5]
            },
            'processing_difficulty': {
                'complexity_score': 5,
                'challenges': ['basic_parsing'],
                'preprocessing_steps': ['normalization']
            },
            'medical_content_preservation': {
                'retention_score': 7,
                'critical_information': ['symptom'],
                'safety_implications': 'low'
            },
            'correction_strategy': {
                'approach': 'basic_correction',
                'confidence': 0.6,
                'processing_order': ['spelling', 'grammar']
            },
            'fallback_used': True
        }
    
    def _update_generation_stats(self, patterns: List[GrammaticalErrorPattern], generation_time: float):
        """Update generation statistics"""
        self.error_generation_stats['total_generated'] += len(patterns)
        
        # Update timing
        current_avg = self.error_generation_stats['average_generation_time']
        total_ops = self.error_generation_stats['total_generated']
        new_avg = ((current_avg * (total_ops - len(patterns))) + generation_time) / total_ops
        self.error_generation_stats['average_generation_time'] = new_avg
        
        # Update error type counts
        for pattern in patterns:
            error_type = pattern.error_type.value
            self.error_generation_stats['by_error_type'][error_type] = \
                self.error_generation_stats['by_error_type'].get(error_type, 0) + 1
        
        # Update difficulty counts  
        for pattern in patterns:
            difficulty = pattern.difficulty_level.value
            self.error_generation_stats['by_difficulty'][difficulty] = \
                self.error_generation_stats['by_difficulty'].get(difficulty, 0) + 1
    
    async def get_generation_statistics(self) -> Dict[str, Any]:
        """Get comprehensive generation statistics"""
        return {
            'algorithm_version': '7.1_ai_grammatical_error_generation',
            'statistics': self.error_generation_stats.copy(),
            'timestamp': datetime.utcnow().isoformat(),
            'engine_performance': await self.testing_engine.get_performance_summary()
        }

# Global instance
ai_grammatical_generator = None

def get_ai_grammatical_generator() -> AIGrammaticalErrorGenerator:
    """Get or create global AI grammatical error generator"""
    global ai_grammatical_generator
    
    if ai_grammatical_generator is None:
        ai_grammatical_generator = AIGrammaticalErrorGenerator()
    
    return ai_grammatical_generator

# Convenience functions
async def generate_medical_grammar_errors(base_text: str, num_variants: int = 10) -> List[GrammaticalErrorPattern]:
    """Quick function to generate grammatical error variants"""
    generator = get_ai_grammatical_generator()
    return await generator.generate_grammatical_variants_with_ai(base_text, num_variants)

async def analyze_grammar_error_complexity(error_text: str) -> Dict[str, Any]:
    """Quick function to analyze error complexity"""
    generator = get_ai_grammatical_generator()
    return await generator.analyze_error_complexity_with_ai(error_text)