"""
🚀 PHASE 7.1: AI-POWERED COMPREHENSIVE MEDICAL NLP TESTING SUITE
Revolutionary Gemini-Integrated Testing Engine for Medical Language Processing

IMPLEMENTATION SCOPE:
- Gemini-powered grammatical error pattern generator
- AI-enhanced incomplete sentence processor
- AI-powered colloquial language understanding  
- Emotional intelligence testing with AI validation

Algorithm Version: 7.1_ai_powered_medical_nlp_testing
"""

import asyncio
import json
import os
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

import google.generativeai as genai
from motor.motor_asyncio import AsyncIOMotorClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"

class LanguagePatternType(str, Enum):
    GRAMMATICAL_ERROR = "grammatical_error"
    INCOMPLETE_SENTENCE = "incomplete_sentence"
    COLLOQUIAL_LANGUAGE = "colloquial_language"
    EMOTIONAL_EXPRESSION = "emotional_expression"

@dataclass
class AIGeneratedTestCase:
    """Individual AI-generated test case with comprehensive metadata"""
    id: str
    pattern_type: LanguagePatternType
    input_text: str
    expected_entities: List[Dict[str, Any]]
    expected_intent: str
    expected_urgency: str
    difficulty_level: TestDifficulty
    confidence_score: float
    ai_reasoning: str
    success_criteria: Dict[str, Any]
    cultural_context: Optional[str] = None
    emotional_state: Optional[str] = None
    grammatical_errors: Optional[List[str]] = None
    medical_accuracy: float = 0.0
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()

@dataclass
class AIValidationResult:
    """AI-powered validation result with reasoning"""
    test_case_id: str
    accuracy_score: float
    semantic_equivalence: float
    medical_appropriateness: float
    confidence_assessment: float
    ai_reasoning: str
    improvement_suggestions: List[str]
    validation_confidence: float
    performance_metrics: Dict[str, Any]

class GeminiPoweredTestingEngine:
    """
    🤖 Core AI-driven testing engine using Gemini LLM for unlimited pattern understanding
    """
    
    def __init__(self, mongo_url: str = None):
        """Initialize Gemini-powered testing engine"""
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.gemini_api_keys = self._load_api_keys()
        self.current_key_index = 0
        
        if not self.gemini_api_keys:
            raise ValueError("No GEMINI_API_KEY or GEMINI_API_KEYS found")
        
        self._initialize_gemini_client()
        
        # MongoDB connection for test data storage
        if mongo_url:
            self.mongo_client = AsyncIOMotorClient(mongo_url)
            self.db = self.mongo_client[os.environ.get('DB_NAME', 'test_database')]
        else:
            self.mongo_client = None
            self.db = None
            
        # Performance tracking
        self.performance_metrics = {
            'tests_generated': 0,
            'tests_validated': 0,
            'average_generation_time': 0.0,
            'average_validation_time': 0.0,
            'accuracy_scores': []
        }
        
        logger.info("🚀 Gemini-Powered Medical NLP Testing Engine Initialized")
    
    def _load_api_keys(self) -> List[str]:
        """Load Gemini API keys from environment"""
        keys = []
        
        # Primary key
        if self.gemini_api_key:
            keys.append(self.gemini_api_key)
        
        # Additional keys
        keys_str = os.getenv('GEMINI_API_KEYS', '')
        additional_keys = [key.strip() for key in keys_str.split(',') if key.strip()]
        
        for key in additional_keys:
            if key not in keys:
                keys.append(key)
                
        return keys
    
    def _initialize_gemini_client(self):
        """Initialize Gemini client with current API key"""
        try:
            current_key = self.gemini_api_keys[self.current_key_index]
            genai.configure(api_key=current_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
            logger.info(f"✅ Gemini client initialized with key index {self.current_key_index}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini client: {e}")
            self._rotate_api_key()
    
    def _rotate_api_key(self):
        """Rotate to next API key if available"""
        if len(self.gemini_api_keys) > 1:
            self.current_key_index = (self.current_key_index + 1) % len(self.gemini_api_keys)
            self._initialize_gemini_client()
            logger.info(f"🔄 Rotated to API key index {self.current_key_index}")
    
    async def _call_gemini_with_fallback(self, prompt: str, max_retries: int = 3) -> str:
        """Call Gemini API with fallback and error handling"""
        for attempt in range(max_retries):
            try:
                response = await asyncio.to_thread(
                    self.model.generate_content, 
                    prompt,
                    generation_config={
                        'temperature': 0.7,
                        'max_output_tokens': 2048,
                    }
                )
                return response.text
                
            except Exception as e:
                logger.warning(f"⚠️ Gemini API call failed (attempt {attempt + 1}): {e}")
                
                if attempt < max_retries - 1:
                    self._rotate_api_key()
                    await asyncio.sleep(1)  # Brief delay before retry
                else:
                    raise Exception(f"All Gemini API attempts failed: {e}")
    
    async def analyze_language_patterns_with_ai(self, input_text: str) -> Dict[str, Any]:
        """
        🧠 Use Gemini to analyze ANY language pattern and generate appropriate tests
        """
        analysis_prompt = f"""
        You are a medical linguistics expert analyzing patient language patterns.
        
        Input Text: "{input_text}"
        
        Provide comprehensive analysis:
        
        1. LANGUAGE PATTERN ANALYSIS:
           - Grammar quality (1-10 scale)
           - Completeness level (1-10 scale) 
           - Formality level (1-10 scale)
           - Emotional intensity (1-10 scale)
           
        2. MEDICAL CONTENT EXTRACTION:
           - Primary symptoms mentioned
           - Urgency indicators
           - Anatomical references
           - Temporal information
           
        3. PATTERN CLASSIFICATION:
           - Pattern type (grammatical_error, incomplete_sentence, colloquial_language, emotional_expression)
           - Difficulty level for AI processing (easy, medium, hard, expert)
           - Cultural/demographic context indicators
           
        4. TESTING RECOMMENDATIONS:
           - What aspects need testing
           - Expected challenges for NLP systems
           - Validation criteria
        
        Format response as structured JSON for programmatic processing.
        """
        
        try:
            start_time = time.time()
            ai_response = await self._call_gemini_with_fallback(analysis_prompt)
            processing_time = time.time() - start_time
            
            # Parse AI response
            analysis_result = self._parse_ai_analysis(ai_response)
            analysis_result['processing_time'] = processing_time
            
            logger.info(f"✅ Language pattern analysis completed in {processing_time:.3f}s")
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Language pattern analysis failed: {e}")
            return self._generate_fallback_analysis(input_text)
    
    def _parse_ai_analysis(self, ai_response: str) -> Dict[str, Any]:
        """Parse and structure AI analysis response"""
        try:
            # Try to extract JSON from response
            import re
            json_pattern = r'\{.*\}'
            json_match = re.search(json_pattern, ai_response, re.DOTALL)
            
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback parsing if no JSON found
                return self._extract_analysis_from_text(ai_response)
                
        except Exception as e:
            logger.warning(f"⚠️ AI response parsing failed: {e}")
            return self._generate_default_analysis()
    
    def _extract_analysis_from_text(self, response_text: str) -> Dict[str, Any]:
        """Extract analysis from natural language response"""
        return {
            'language_patterns': {
                'grammar_quality': 5,
                'completeness_level': 5,
                'formality_level': 5,
                'emotional_intensity': 3
            },
            'medical_content': {
                'primary_symptoms': ['general_health_concern'],
                'urgency_indicators': [],
                'anatomical_references': [],
                'temporal_information': None
            },
            'pattern_classification': {
                'pattern_type': 'colloquial_language',
                'difficulty_level': 'medium',
                'cultural_context': 'general'
            },
            'testing_recommendations': {
                'focus_areas': ['symptom_extraction', 'intent_classification'],
                'expected_challenges': ['pattern_recognition'],
                'validation_criteria': ['accuracy', 'completeness']
            },
            'ai_reasoning': response_text[:500] + "..." if len(response_text) > 500 else response_text
        }
    
    def _generate_fallback_analysis(self, input_text: str) -> Dict[str, Any]:
        """Generate basic analysis when AI fails"""
        return {
            'language_patterns': {
                'grammar_quality': 6,
                'completeness_level': 7,
                'formality_level': 5,
                'emotional_intensity': 3
            },
            'medical_content': {
                'primary_symptoms': ['unspecified_symptom'],
                'urgency_indicators': [],
                'anatomical_references': [],
                'temporal_information': None
            },
            'pattern_classification': {
                'pattern_type': 'colloquial_language',
                'difficulty_level': 'medium',
                'cultural_context': 'general'
            },
            'testing_recommendations': {
                'focus_areas': ['basic_processing'],
                'expected_challenges': ['pattern_recognition'],
                'validation_criteria': ['functionality']
            },
            'ai_reasoning': 'Fallback analysis due to AI processing error',
            'processing_time': 0.1,
            'fallback_used': True
        }
    
    def _generate_default_analysis(self) -> Dict[str, Any]:
        """Generate default analysis structure"""
        return {
            'language_patterns': {
                'grammar_quality': 5,
                'completeness_level': 5,
                'formality_level': 5,
                'emotional_intensity': 2
            },
            'medical_content': {
                'primary_symptoms': [],
                'urgency_indicators': [],
                'anatomical_references': [],
                'temporal_information': None
            },
            'pattern_classification': {
                'pattern_type': 'colloquial_language',
                'difficulty_level': 'medium',
                'cultural_context': 'general'
            },
            'testing_recommendations': {
                'focus_areas': ['basic_functionality'],
                'expected_challenges': ['processing'],
                'validation_criteria': ['completion']
            },
            'ai_reasoning': 'Default analysis structure'
        }
    
    async def store_test_case(self, test_case: AIGeneratedTestCase) -> bool:
        """Store generated test case in MongoDB"""
        if not self.db:
            logger.warning("⚠️ No database connection - test case not stored")
            return False
            
        try:
            test_case_dict = asdict(test_case)
            await self.db.ai_test_cases.insert_one(test_case_dict)
            logger.info(f"✅ Test case {test_case.id} stored successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to store test case: {e}")
            return False
    
    async def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        summary = {
            'algorithm_version': '7.1_ai_powered_medical_nlp_testing',
            'performance_metrics': self.performance_metrics.copy(),
            'current_api_key_index': self.current_key_index,
            'total_api_keys': len(self.gemini_api_keys),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Calculate average accuracy if available
        if self.performance_metrics['accuracy_scores']:
            summary['average_accuracy'] = sum(self.performance_metrics['accuracy_scores']) / len(self.performance_metrics['accuracy_scores'])
        else:
            summary['average_accuracy'] = 0.0
            
        return summary

# Global instance for easy access
ai_testing_engine = None

def get_ai_testing_engine() -> GeminiPoweredTestingEngine:
    """Get or create global AI testing engine instance"""
    global ai_testing_engine
    
    if ai_testing_engine is None:
        mongo_url = os.environ.get('MONGO_URL')
        ai_testing_engine = GeminiPoweredTestingEngine(mongo_url)
    
    return ai_testing_engine

# Helper functions for easy integration
async def analyze_medical_text_with_ai(input_text: str) -> Dict[str, Any]:
    """Quick function to analyze medical text with AI"""
    engine = get_ai_testing_engine()
    return await engine.analyze_language_patterns_with_ai(input_text)

async def get_testing_performance_summary() -> Dict[str, Any]:
    """Quick function to get performance summary"""
    engine = get_ai_testing_engine()
    return await engine.get_performance_summary()