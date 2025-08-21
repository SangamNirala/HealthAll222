"""
🗣️ PHASE 7.1: AI-POWERED COLLOQUIAL LANGUAGE PROCESSOR
Revolutionary Gemini-Integrated Colloquial and Cultural Medical Language Understanding System

CAPABILITIES:
- Expand colloquial patterns with unlimited AI variations
- Understand cultural and demographic-specific medical expressions
- Generate culturally sensitive test cases
- Analyze informal medical language patterns

Algorithm Version: 7.1_ai_colloquial_language_processing
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

from ai_powered_medical_nlp_test_suite import GeminiPoweredTestingEngine, AIGeneratedTestCase, TestDifficulty, LanguagePatternType
import logging

logger = logging.getLogger(__name__)

class ColloquialCategory(str, Enum):
    CHILDLIKE_EXPRESSIONS = "childlike_expressions"
    ELDER_GENERATION_TERMS = "elder_generation_terms"
    REGIONAL_VARIATIONS = "regional_variations"
    INTERNET_SLANG = "internet_slang"
    EUPHEMISTIC_DESCRIPTIONS = "euphemistic_descriptions"
    GENERATIONAL_LANGUAGE = "generational_language"
    CULTURAL_EXPRESSIONS = "cultural_expressions"
    INFORMAL_MEDICAL_TERMS = "informal_medical_terms"

class CulturalContext(str, Enum):
    AFRICAN_AMERICAN = "african_american"
    HISPANIC_LATINO = "hispanic_latino"
    ASIAN_AMERICAN = "asian_american"
    RURAL_SOUTHERN = "rural_southern"
    URBAN_NORTHEAST = "urban_northeast"
    MIDWEST_TRADITIONAL = "midwest_traditional"
    WEST_COAST_CASUAL = "west_coast_casual"
    IMMIGRANT_COMMUNITIES = "immigrant_communities"
    LGBTQ_COMMUNITY = "lgbtq_community"
    ELDERLY_COMMUNITY = "elderly_community"

@dataclass
class ColloquialPattern:
    """Individual colloquial language pattern with medical mapping"""
    informal_expression: str
    formal_medical_equivalent: str
    colloquial_category: ColloquialCategory
    cultural_context: CulturalContext
    usage_demographics: Dict[str, Any]
    medical_entities: List[Dict[str, Any]]
    confidence_mapping: float
    cultural_sensitivity: str  # high, medium, low
    generational_preference: str
    regional_distribution: List[str]

@dataclass
class CulturalMedicalAnalysis:
    """Comprehensive cultural medical language analysis"""
    cultural_context: str
    common_expressions: List[str]
    taboo_topics: List[str]
    preferred_communication_styles: List[str]
    generational_differences: Dict[str, Any]
    sensitivity_guidelines: List[str]
    medical_terminology_preferences: Dict[str, str]

class AIColloquialLanguageProcessor:
    """
    🗣️ Uses Gemini for unlimited colloquial language pattern recognition and cultural understanding
    """
    
    def __init__(self, testing_engine: GeminiPoweredTestingEngine = None):
        """Initialize AI colloquial language processor"""
        self.testing_engine = testing_engine or GeminiPoweredTestingEngine()
        self.pattern_stats = {
            'total_patterns_generated': 0,
            'cultural_contexts_analyzed': 0,
            'average_generation_time': 0.0,
            'cultural_sensitivity_scores': []
        }
        
        logger.info("🗣️ AI Colloquial Language Processor initialized")
    
    async def expand_colloquial_patterns_with_ai(self, formal_medical_terms: List[str]) -> List[ColloquialPattern]:
        """
        Generate unlimited colloquial variations using AI
        
        AI EXPANSION PROMPT:
        "You are a linguistic anthropologist studying how people informally describe medical symptoms.
        
        Formal medical terms: {formal_medical_terms}
        
        Generate 25+ different informal, colloquial, slang, and regional ways people might describe these symptoms, including:
        - Child-like expressions
        - Elder generation terms  
        - Regional/cultural variations
        - Internet slang adaptations
        - Euphemistic descriptions
        - Generational language differences
        
        For each informal expression, provide the formal medical equivalent and usage context."
        """
        
        expansion_prompt = f"""
        You are a medical anthropologist and linguist expert analyzing how diverse populations express medical symptoms informally.
        
        FORMAL MEDICAL TERMS TO EXPAND: {formal_medical_terms}
        
        Generate comprehensive colloquial variations across cultural and demographic lines:
        
        COLLOQUIAL CATEGORIES TO COVER:
        1. CHILDLIKE EXPRESSIONS:
           - "Tummy hurts", "Owie", "Booboo", "Owchie"
           - Simple descriptive language
           - Comfort-seeking expressions
        
        2. ELDER GENERATION TERMS:
           - "Rheumatism", "The vapors", "Feeling poorly"
           - Traditional folk medicine terms
           - Historical medical expressions
        
        3. REGIONAL/CULTURAL VARIATIONS:
           - Southern US: "Feeling right poorly", "Peaked"
           - Urban slang: "Feeling busted", "All messed up"
           - Rural expressions: "Under the weather", "Feeling off"
        
        4. INTERNET/TEXTING SLANG:
           - "Feeling sus", "Body is glitching", "System error"
           - Abbreviated forms: "rlly sick", "cant even"
           - Emoji-influenced descriptions
        
        5. EUPHEMISTIC DESCRIPTIONS:
           - "Lady problems", "Bathroom issues"
           - Indirect references to sensitive topics
           - Polite circumlocutions
        
        6. GENERATIONAL LANGUAGE:
           - Gen Z: "My body is not vibing", "Feeling lowkey sick"
           - Millennial: "Everything is broken", "Having a moment"
           - Baby Boomer: "Not feeling up to par", "Under the weather"
        
        7. CULTURAL EXPRESSIONS:
           - Hispanic/Latino: "Mal de ojo", "Susto", "Empacho"
           - African American: "Feeling all out of sorts"
           - Asian: References to hot/cold balance, qi
        
        8. INFORMAL MEDICAL TERMS:
           - "Bug", "Crud", "Funk", "Nasty cold"
           - Body part nicknames
           - Symptom descriptives
        
        FOR EACH COLLOQUIAL EXPRESSION PROVIDE:
        {{
            "informal_expression": "[colloquial term]",
            "formal_medical_equivalent": "[medical terminology]",
            "colloquial_category": "[category from above]",
            "cultural_context": "[specific demographic/region]",
            "usage_demographics": {{
                "age_groups": ["[primary age groups]"],
                "regions": ["[geographic regions]"],
                "cultural_backgrounds": ["[cultural groups]"],
                "socioeconomic_factors": ["[relevant factors]"]
            }},
            "medical_entities_implied": [
                {{"entity": "[symptom/condition]", "type": "[classification]", "confidence": [0.0-1.0]}}
            ],
            "confidence_mapping": [0.0-1.0],
            "cultural_sensitivity": "[high/medium/low]",
            "generational_preference": "[primary generation]",
            "regional_distribution": ["[regions where common]"],
            "usage_notes": "[context and appropriate usage]"
        }}
        
        Generate 25+ diverse expressions covering all categories and cultural contexts.
        Ensure cultural authenticity and respectful representation.
        Return as JSON array for automated processing.
        """
        
        try:
            start_time = time.time()
            ai_response = await self.testing_engine._call_gemini_with_fallback(expansion_prompt)
            generation_time = time.time() - start_time
            
            # Parse AI response into colloquial patterns
            patterns = self._parse_colloquial_patterns(ai_response, formal_medical_terms)
            
            # Update statistics
            self._update_pattern_stats(patterns, generation_time)
            
            logger.info(f"✅ Generated {len(patterns)} colloquial patterns in {generation_time:.3f}s")
            return patterns
            
        except Exception as e:
            logger.error(f"❌ Colloquial pattern expansion failed: {e}")
            return self._generate_fallback_colloquial_patterns(formal_medical_terms)
    
    async def understand_cultural_medical_expressions_with_ai(self, cultural_context: str) -> CulturalMedicalAnalysis:
        """
        Use AI to understand cultural and demographic-specific medical language
        """
        
        cultural_analysis_prompt = f"""
        You are a medical anthropologist specializing in cross-cultural healthcare communication.
        
        CULTURAL CONTEXT: {cultural_context}
        
        Provide comprehensive analysis of medical language patterns for this cultural group:
        
        1. COMMON INFORMAL MEDICAL EXPRESSIONS:
           - Traditional folk medicine terms
           - Culturally specific symptom descriptions
           - Religious/spiritual health concepts
           - Family/community health language
           - Generation-specific expressions
        
        2. CULTURAL TABOOS AND SENSITIVE TOPICS:
           - Medical topics that are avoided or discussed indirectly
           - Gender-specific communication patterns
           - Mental health stigma considerations
           - Body part/function discussion norms
           - Privacy and family involvement expectations
        
        3. PREFERRED COMMUNICATION STYLES:
           - Direct vs. indirect communication preferences
           - Authority figure interaction patterns
           - Family involvement in medical discussions
           - Nonverbal communication importance
           - Respect and hierarchy considerations
        
        4. GENERATIONAL DIFFERENCES:
           - First generation vs. acculturated language patterns
           - Traditional medicine integration
           - Technology comfort levels
           - Language mixing patterns
           - Medical authority attitudes
        
        5. REGIONAL VARIATIONS:
           - Geographic distribution of expressions
           - Urban vs. rural differences
           - Socioeconomic language variations
           - Educational level impacts
        
        6. MEDICAL TERMINOLOGY PREFERENCES:
           - Preferred terms for common conditions
           - Euphemisms and indirect references
           - Traditional vs. Western medical concepts
           - Pain and symptom description patterns
           - Emotional expression of health concerns
        
        7. CULTURAL SENSITIVITY GUIDELINES:
           - Respectful communication approaches
           - Avoiding cultural insensitivity
           - Building trust and rapport
           - Understanding cultural context
           - Appropriate terminology usage
        
        Provide culturally authentic and respectful analysis based on established research and cultural knowledge.
        Return as structured JSON for medical AI training.
        """
        
        try:
            ai_response = await self.testing_engine._call_gemini_with_fallback(cultural_analysis_prompt)
            cultural_analysis = self._parse_cultural_analysis(ai_response, cultural_context)
            
            self.pattern_stats['cultural_contexts_analyzed'] += 1
            
            logger.info(f"✅ Cultural analysis completed for {cultural_context}")
            return cultural_analysis
            
        except Exception as e:
            logger.error(f"❌ Cultural analysis failed: {e}")
            return self._generate_fallback_cultural_analysis(cultural_context)
    
    async def generate_cultural_test_cases_with_ai(self, cultural_contexts: List[str], cases_per_context: int = 15) -> List[AIGeneratedTestCase]:
        """
        Generate culturally diverse test cases for colloquial language understanding
        """
        all_test_cases = []
        
        for context in cultural_contexts:
            context_prompt = f"""
            Generate {cases_per_context} authentic medical language test cases for {context} cultural context.
            
            CULTURAL CONTEXT: {context}
            
            Create realistic scenarios where patients from this cultural background express health concerns:
            
            TEST CASE TYPES TO INCLUDE:
            1. Traditional/Folk Medicine References
            2. Cultural Euphemisms for Sensitive Topics
            3. Generation-Specific Language Patterns
            4. Regional Dialect Expressions
            5. Family/Community Health Communication
            6. Religious/Spiritual Health Concepts
            7. Code-Switching Between Languages
            8. Culturally Influenced Symptom Descriptions
            
            FOR EACH TEST CASE PROVIDE:
            - Authentic patient expression in cultural context
            - Formal medical equivalent
            - Cultural background explanation
            - Expected medical entity extraction
            - Cultural sensitivity considerations
            - Communication approach recommendations
            - Potential misunderstanding risks
            - Success criteria for AI processing
            
            ENSURE:
            - Cultural authenticity and respect
            - Realistic patient scenarios
            - Diverse age groups and situations
            - Both common and challenging expressions
            - Educational value for AI systems
            
            Return as JSON array with comprehensive test case data.
            """
            
            try:
                ai_response = await self.testing_engine._call_gemini_with_fallback(context_prompt)
                context_cases = self._parse_cultural_test_cases(ai_response, context)
                all_test_cases.extend(context_cases)
                
                logger.info(f"✅ Generated {len(context_cases)} test cases for {context}")
                
                # Brief delay for API rate management
                await asyncio.sleep(0.4)
                
            except Exception as e:
                logger.error(f"❌ Cultural test case generation failed for {context}: {e}")
                fallback_cases = self._generate_fallback_cultural_test_cases(context, 3)
                all_test_cases.extend(fallback_cases)
        
        logger.info(f"🎯 Total cultural test cases generated: {len(all_test_cases)}")
        return all_test_cases
    
    async def analyze_colloquial_complexity_with_ai(self, colloquial_text: str) -> Dict[str, Any]:
        """
        Analyze the complexity and cultural context of colloquial medical expressions
        """
        
        complexity_prompt = f"""
        Analyze the linguistic and cultural complexity of this colloquial medical expression:
        
        EXPRESSION: "{colloquial_text}"
        
        Provide comprehensive complexity analysis:
        
        1. LINGUISTIC COMPLEXITY:
           - Informal language level (1-10)
           - Cultural specificity (1-10)
           - Generation binding (how tied to specific age group)
           - Regional limitation (geographic restriction level)
           - Ambiguity level (potential for misunderstanding)
        
        2. CULTURAL CONTEXT REQUIREMENTS:
           - Cultural knowledge needed for understanding
           - Historical/generational context importance
           - Religious/spiritual context relevance
           - Socioeconomic context factors
           - Educational level considerations
        
        3. AI PROCESSING CHALLENGES:
           - Pattern recognition difficulty
           - Context dependency level
           - Disambiguation requirements
           - Cultural sensitivity needs
           - Translation complexity to medical terms
        
        4. MEDICAL ACCURACY PRESERVATION:
           - Medical information clarity
           - Risk of misinterpretation
           - Critical details potentially lost
           - Emergency recognition challenges
           - Clinical decision-making impact
        
        5. COMMUNICATION RECOMMENDATIONS:
           - Clarification strategies
           - Cultural bridge-building approaches
           - Respectful interaction methods
           - Trust-building considerations
           - Follow-up communication needs
        
        Return detailed analysis for AI system training and cultural competency.
        """
        
        try:
            ai_response = await self.testing_engine._call_gemini_with_fallback(complexity_prompt)
            complexity_analysis = self._parse_complexity_analysis(ai_response)
            
            logger.info("✅ Colloquial complexity analysis completed")
            return complexity_analysis
            
        except Exception as e:
            logger.error(f"❌ Complexity analysis failed: {e}")
            return self._generate_fallback_complexity_analysis(colloquial_text)
    
    def _parse_colloquial_patterns(self, ai_response: str, formal_terms: List[str]) -> List[ColloquialPattern]:
        """Parse AI-generated colloquial patterns"""
        try:
            import re
            json_pattern = r'\[.*\]'
            json_match = re.search(json_pattern, ai_response, re.DOTALL)
            
            if json_match:
                patterns_data = json.loads(json_match.group())
            else:
                return self._generate_fallback_colloquial_patterns(formal_terms)
            
            patterns = []
            for pattern_data in patterns_data:
                try:
                    pattern = ColloquialPattern(
                        informal_expression=pattern_data.get('informal_expression', ''),
                        formal_medical_equivalent=pattern_data.get('formal_medical_equivalent', ''),
                        colloquial_category=ColloquialCategory(pattern_data.get('colloquial_category', 'informal_medical_terms')),
                        cultural_context=CulturalContext(pattern_data.get('cultural_context', 'urban_northeast')),
                        usage_demographics=pattern_data.get('usage_demographics', {}),
                        medical_entities=pattern_data.get('medical_entities_implied', []),
                        confidence_mapping=pattern_data.get('confidence_mapping', 0.5),
                        cultural_sensitivity=pattern_data.get('cultural_sensitivity', 'medium'),
                        generational_preference=pattern_data.get('generational_preference', 'mixed'),
                        regional_distribution=pattern_data.get('regional_distribution', ['general'])
                    )
                    patterns.append(pattern)
                except Exception as e:
                    logger.warning(f"⚠️ Skipping invalid pattern: {e}")
                    continue
            
            return patterns
            
        except Exception as e:
            logger.error(f"❌ Colloquial pattern parsing failed: {e}")
            return self._generate_fallback_colloquial_patterns(formal_terms)
    
    def _parse_cultural_analysis(self, ai_response: str, cultural_context: str) -> CulturalMedicalAnalysis:
        """Parse AI cultural analysis response"""
        try:
            import re
            json_pattern = r'\{.*\}'
            json_match = re.search(json_pattern, ai_response, re.DOTALL)
            
            if json_match:
                analysis_data = json.loads(json_match.group())
            else:
                return self._generate_fallback_cultural_analysis(cultural_context)
            
            return CulturalMedicalAnalysis(
                cultural_context=cultural_context,
                common_expressions=analysis_data.get('common_expressions', []),
                taboo_topics=analysis_data.get('taboo_topics', []),
                preferred_communication_styles=analysis_data.get('communication_styles', []),
                generational_differences=analysis_data.get('generational_differences', {}),
                sensitivity_guidelines=analysis_data.get('sensitivity_guidelines', []),
                medical_terminology_preferences=analysis_data.get('terminology_preferences', {})
            )
            
        except Exception as e:
            logger.error(f"❌ Cultural analysis parsing failed: {e}")
            return self._generate_fallback_cultural_analysis(cultural_context)
    
    def _parse_cultural_test_cases(self, ai_response: str, context: str) -> List[AIGeneratedTestCase]:
        """Parse AI-generated cultural test cases"""
        try:
            import re
            json_pattern = r'\[.*\]'
            json_match = re.search(json_pattern, ai_response, re.DOTALL)
            
            if json_match:
                cases_data = json.loads(json_match.group())
            else:
                return self._generate_fallback_cultural_test_cases(context, 2)
            
            test_cases = []
            for case_data in cases_data:
                test_case = AIGeneratedTestCase(
                    id=f"cultural_{context}_{len(test_cases)+1}",
                    pattern_type=LanguagePatternType.COLLOQUIAL_LANGUAGE,
                    input_text=case_data.get('patient_expression', ''),
                    expected_entities=case_data.get('medical_entities', []),
                    expected_intent=case_data.get('expected_intent', 'symptom_inquiry'),
                    expected_urgency=case_data.get('urgency_level', 'medium'),
                    difficulty_level=TestDifficulty(case_data.get('difficulty', 'medium')),
                    confidence_score=case_data.get('confidence', 0.5),
                    ai_reasoning=case_data.get('cultural_explanation', 'Cultural language pattern'),
                    success_criteria=case_data.get('success_criteria', {}),
                    cultural_context=context
                )
                test_cases.append(test_case)
            
            return test_cases
            
        except Exception as e:
            logger.error(f"❌ Cultural test case parsing failed: {e}")
            return self._generate_fallback_cultural_test_cases(context, 2)
    
    def _parse_complexity_analysis(self, ai_response: str) -> Dict[str, Any]:
        """Parse AI complexity analysis response"""
        try:
            import re
            json_pattern = r'\{.*\}'
            json_match = re.search(json_pattern, ai_response, re.DOTALL)
            
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._generate_fallback_complexity_analysis("")
                
        except Exception as e:
            logger.error(f"❌ Complexity analysis parsing failed: {e}")
            return self._generate_fallback_complexity_analysis("")
    
    def _generate_fallback_colloquial_patterns(self, formal_terms: List[str]) -> List[ColloquialPattern]:
        """Generate fallback colloquial patterns"""
        patterns = []
        
        # Basic colloquial mappings
        basic_mappings = [
            ("tummy ache", "abdominal pain", ColloquialCategory.CHILDLIKE_EXPRESSIONS),
            ("feeling poorly", "general malaise", ColloquialCategory.ELDER_GENERATION_TERMS),
            ("banged up", "injured/bruised", ColloquialCategory.INFORMAL_MEDICAL_TERMS),
            ("under the weather", "feeling unwell", ColloquialCategory.EUPHEMISTIC_DESCRIPTIONS),
            ("busted", "injured/broken", ColloquialCategory.INTERNET_SLANG)
        ]
        
        for informal, formal, category in basic_mappings:
            pattern = ColloquialPattern(
                informal_expression=informal,
                formal_medical_equivalent=formal,
                colloquial_category=category,
                cultural_context=CulturalContext.URBAN_NORTHEAST,
                usage_demographics={'age_groups': ['mixed'], 'regions': ['general']},
                medical_entities=[{'entity': 'symptom', 'confidence': 0.6}],
                confidence_mapping=0.6,
                cultural_sensitivity='low',
                generational_preference='mixed',
                regional_distribution=['general']
            )
            patterns.append(pattern)
        
        return patterns
    
    def _generate_fallback_cultural_analysis(self, cultural_context: str) -> CulturalMedicalAnalysis:
        """Generate fallback cultural analysis"""
        return CulturalMedicalAnalysis(
            cultural_context=cultural_context,
            common_expressions=['feeling unwell', 'not feeling good'],
            taboo_topics=['private health matters'],
            preferred_communication_styles=['respectful', 'professional'],
            generational_differences={'older': 'formal', 'younger': 'casual'},
            sensitivity_guidelines=['be respectful', 'avoid assumptions'],
            medical_terminology_preferences={'pain': 'discomfort', 'sick': 'unwell'}
        )
    
    def _generate_fallback_cultural_test_cases(self, context: str, num_cases: int) -> List[AIGeneratedTestCase]:
        """Generate fallback cultural test cases"""
        fallback_cases = []
        
        basic_expressions = [
            "I'm not feeling too good",
            "Something ain't right with me",
            "Been under the weather lately"
        ]
        
        for i in range(min(num_cases, len(basic_expressions))):
            test_case = AIGeneratedTestCase(
                id=f"fallback_cultural_{context}_{i+1}",
                pattern_type=LanguagePatternType.COLLOQUIAL_LANGUAGE,
                input_text=basic_expressions[i],
                expected_entities=[{'entity': 'general_malaise', 'type': 'symptom'}],
                expected_intent='symptom_inquiry',
                expected_urgency='medium',
                difficulty_level=TestDifficulty.MEDIUM,
                confidence_score=0.5,
                ai_reasoning="Fallback colloquial expression",
                success_criteria={'cultural_sensitivity': True, 'accurate_extraction': True},
                cultural_context=context
            )
            fallback_cases.append(test_case)
        
        return fallback_cases
    
    def _generate_fallback_complexity_analysis(self, text: str) -> Dict[str, Any]:
        """Generate fallback complexity analysis"""
        return {
            'linguistic_complexity': {'informal_level': 5, 'cultural_specificity': 3, 'ambiguity_level': 4},
            'cultural_context_requirements': {'cultural_knowledge_needed': 'basic'},
            'ai_processing_challenges': {'difficulty_level': 5, 'context_dependency': 'medium'},
            'medical_accuracy_preservation': {'clarity_score': 6, 'misinterpretation_risk': 'low'},
            'communication_recommendations': ['seek clarification', 'use respectful tone'],
            'fallback_used': True
        }
    
    def _update_pattern_stats(self, patterns: List[ColloquialPattern], generation_time: float):
        """Update pattern generation statistics"""
        self.pattern_stats['total_patterns_generated'] += len(patterns)
        
        # Update timing
        current_avg = self.pattern_stats['average_generation_time']
        total_patterns = self.pattern_stats['total_patterns_generated']
        new_avg = ((current_avg * (total_patterns - len(patterns))) + generation_time) / total_patterns
        self.pattern_stats['average_generation_time'] = new_avg
        
        # Update cultural sensitivity scores
        for pattern in patterns:
            sensitivity_score = {'high': 3, 'medium': 2, 'low': 1}.get(pattern.cultural_sensitivity, 2)
            self.pattern_stats['cultural_sensitivity_scores'].append(sensitivity_score)
    
    async def get_colloquial_statistics(self) -> Dict[str, Any]:
        """Get comprehensive colloquial processing statistics"""
        stats = self.pattern_stats.copy()
        
        if stats['cultural_sensitivity_scores']:
            stats['average_sensitivity_score'] = sum(stats['cultural_sensitivity_scores']) / len(stats['cultural_sensitivity_scores'])
        else:
            stats['average_sensitivity_score'] = 0.0
        
        return {
            'algorithm_version': '7.1_ai_colloquial_language_processing',
            'processing_statistics': stats,
            'timestamp': datetime.utcnow().isoformat()
        }

# Global instance
ai_colloquial_processor = None

def get_ai_colloquial_processor() -> AIColloquialLanguageProcessor:
    """Get or create global AI colloquial language processor"""
    global ai_colloquial_processor
    
    if ai_colloquial_processor is None:
        ai_colloquial_processor = AIColloquialLanguageProcessor()
    
    return ai_colloquial_processor

# Convenience functions
async def expand_colloquial_patterns(formal_terms: List[str]) -> List[ColloquialPattern]:
    """Quick function to expand colloquial patterns"""
    processor = get_ai_colloquial_processor()
    return await processor.expand_colloquial_patterns_with_ai(formal_terms)

async def analyze_cultural_medical_language(cultural_context: str) -> CulturalMedicalAnalysis:
    """Quick function to analyze cultural medical language"""
    processor = get_ai_colloquial_processor()
    return await processor.understand_cultural_medical_expressions_with_ai(cultural_context)