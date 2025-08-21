"""
🤖 STEP 6.2: REVOLUTIONARY AI-POWERED PROGRESSIVE QUESTIONING ENGINE WITH GEMINI LLM INTEGRATION
=========================================================================================================

World-class AI-powered progressive questioning system that uses Gemini LLM to intelligently analyze 
ANY vague medical symptom and dynamically generate contextually appropriate follow-up questions in real-time.

This system transcends predefined examples by leveraging advanced AI to understand, analyze, and respond 
to unlimited variations of vague medical expressions with human-like medical reasoning.

🧠 REVOLUTIONARY ENHANCEMENT: Uses Gemini LLM to analyze any vague symptom expression and generate 
medically appropriate progressive questions dynamically, making the system infinitely scalable and 
intelligent without being limited to predefined patterns.

Algorithm Version: 6.2_ai_powered_progressive_questioning
"""

import os
import asyncio
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import google.generativeai as genai

# Import existing Task 6.1 components for integration
from intelligent_clarification_system import (
    IntelligentClarificationEngine,
    ClarificationAnalysisResult,
    UnclearInputType,
    analyze_and_clarify_unclear_input
)

# Configure logger
logger = logging.getLogger(__name__)


class AIProgressiveQuestioningType(Enum):
    """Types of AI-powered progressive questioning approaches"""
    SYMPTOM_SPECIFICATION = "symptom_specification"  # "sick" → specific symptoms
    LOCATION_INQUIRY = "location_inquiry"           # "pain" → location and character
    PHYSICAL_VS_EMOTIONAL = "physical_vs_emotional"  # "bad" → differentiate concerns
    TEMPORAL_EXPLORATION = "temporal_exploration"    # time-based questioning
    SEVERITY_ASSESSMENT = "severity_assessment"      # intensity evaluation
    FUNCTIONAL_IMPACT = "functional_impact"         # daily life impact
    ASSOCIATED_SYMPTOMS = "associated_symptoms"      # related symptoms
    TRIGGER_IDENTIFICATION = "trigger_identification" # causative factors


@dataclass
class AISymptomAnalysis:
    """
    🧠 AI-POWERED SYMPTOM ANALYSIS RESULT WITH GEMINI INTELLIGENCE
    
    Comprehensive analysis of vague symptoms using Gemini LLM with unlimited adaptability
    """
    original_input: str
    vagueness_type: str
    missing_information: List[str]
    clinical_priority: str  # emergency, urgent, routine
    medical_domains: List[str]  # cardiovascular, neurological, etc.
    urgency_indicators: List[str]
    patient_communication_style: str
    confidence_score: float
    ai_reasoning: str
    processing_time_ms: float
    gemini_model_used: str


@dataclass
class AIGeneratedQuestion:
    """
    💎 AI-GENERATED PROGRESSIVE QUESTION WITH MEDICAL INTELLIGENCE
    
    Dynamically generated question using Gemini LLM with clinical reasoning
    """
    question_text: str
    medical_reasoning: str
    expected_information_type: str
    clinical_priority: int  # 1-5, 1 is highest
    empathy_level: str  # high, medium, low
    follow_up_strategy: str
    confidence_score: float
    question_category: str
    estimated_information_gain: float  # 0-1 scale


@dataclass
class AIProgressiveQuestionResult:
    """
    🎯 COMPREHENSIVE AI PROGRESSIVE QUESTIONING RESULT
    
    Complete analysis and question generation result with AI-powered insights
    """
    symptom_analysis: AISymptomAnalysis
    generated_questions: List[AIGeneratedQuestion]
    conversation_strategy: str
    recommended_next_action: str
    should_escalate: bool
    escalation_reason: Optional[str]
    conversation_efficiency_score: float
    total_processing_time_ms: float


class LLMSymptomAnalyzer:
    """
    🔬 AI-POWERED SYMPTOM ANALYSIS USING GEMINI FOR UNLIMITED SCALABILITY
    
    Uses Gemini LLM to analyze ANY vague symptom expression with medical context
    and clinical reasoning. No limitations to predefined patterns.
    """
    
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        gemini_keys_str = os.getenv('GEMINI_API_KEYS', '')
        self.gemini_api_keys = [key.strip() for key in gemini_keys_str.split(',') if key.strip()]
        
        if self.gemini_api_key and self.gemini_api_key not in self.gemini_api_keys:
            self.gemini_api_keys.insert(0, self.gemini_api_key)
        
        if not self.gemini_api_keys:
            raise ValueError("No GEMINI_API_KEY configured for AI Progressive Questioning")
            
        self.current_key_index = 0
        self.model = None
        self._initialize_gemini_model()
    
    def _initialize_gemini_model(self):
        """Initialize Gemini model with current API key"""
        try:
            if self.current_key_index < len(self.gemini_api_keys):
                api_key = self.gemini_api_keys[self.current_key_index]
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info(f"Initialized Gemini model with API key index {self.current_key_index}")
            else:
                raise ValueError("All Gemini API keys exhausted")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {str(e)}")
            self._rotate_api_key()
    
    def _rotate_api_key(self):
        """Rotate to next API key"""
        self.current_key_index = (self.current_key_index + 1) % len(self.gemini_api_keys)
        if self.current_key_index == 0:
            logger.warning("Cycled through all Gemini API keys")
        self._initialize_gemini_model()
    
    async def analyze_vague_symptom_with_ai(self, patient_input: str, medical_context: Dict[str, Any] = None) -> AISymptomAnalysis:
        """
        🧠 USE GEMINI LLM TO ANALYZE ANY VAGUE SYMPTOM EXPRESSION
        
        Revolutionary AI analysis that handles unlimited variations of vague medical expressions
        with human-like medical reasoning and clinical intelligence.
        """
        start_time = time.time()
        
        # Construct comprehensive AI analysis prompt
        analysis_prompt = self._create_symptom_analysis_prompt(patient_input, medical_context)
        
        try:
            response = await self._query_gemini_with_retry(analysis_prompt)
            analysis_result = self._parse_ai_symptom_analysis(response, patient_input)
            
            processing_time = (time.time() - start_time) * 1000
            analysis_result.processing_time_ms = processing_time
            analysis_result.gemini_model_used = "gemini-1.5-flash"
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"AI symptom analysis failed: {str(e)}")
            # Fallback to basic analysis
            return self._create_fallback_analysis(patient_input, time.time() - start_time)
    
    def _create_symptom_analysis_prompt(self, patient_input: str, medical_context: Dict[str, Any] = None) -> str:
        """Create comprehensive AI prompt for symptom analysis"""
        
        context_info = ""
        if medical_context:
            context_info = f"\nMedical Context: {json.dumps(medical_context, indent=2)}"
        
        prompt = f"""
You are a world-class medical AI assistant analyzing a patient's vague symptom expression with clinical expertise.

Patient Input: "{patient_input}"{context_info}

Please analyze this vague symptom expression and provide a comprehensive medical assessment in JSON format:

{{
    "vagueness_type": "emotional_vague|physical_vague|functional_vague|temporal_vague|location_vague|quality_vague",
    "missing_information": ["list of critical medical information gaps"],
    "clinical_priority": "emergency|urgent|routine",
    "medical_domains": ["list of potentially relevant medical specialties"],
    "urgency_indicators": ["list of any red flags or concerning elements"],
    "patient_communication_style": "minimal|emotional|technical|uncertain|direct",
    "confidence_score": 0.0-1.0,
    "ai_reasoning": "detailed clinical reasoning for this analysis",
    "recommended_questioning_approach": "symptom_specification|location_inquiry|severity_assessment|temporal_exploration",
    "potential_diagnoses_to_consider": ["list of differential diagnoses to explore"],
    "information_gathering_priority": ["ordered list of most important information to gather"]
}}

Key Requirements:
1. Analyze the TYPE of vagueness (emotional, physical, functional, etc.)
2. Identify MISSING critical medical information (location, severity, onset, quality, etc.)
3. Assess clinical priority level (emergency, urgent, routine)
4. Determine relevant medical domains (cardiac, respiratory, GI, neurological, etc.)
5. Detect urgency indicators or red flags
6. Assess patient communication style for appropriate response adaptation
7. Provide confidence in analysis with medical reasoning

Examples of analysis quality expected:
- "sick" → emotional_vague, missing: [specific_symptoms, location, severity], domains: [general_medicine], approach: symptom_specification
- "pain" → location_vague, missing: [location, quality, severity], domains: [varies_by_location], approach: location_inquiry  
- "bad" → emotional_vague, missing: [symptom_type, physical_vs_emotional], domains: [psychiatry, general_medicine], approach: physical_vs_emotional

Provide thorough medical reasoning with evidence-based clinical thinking.
"""
        
        return prompt
    
    async def _query_gemini_with_retry(self, prompt: str, max_retries: int = 3) -> str:
        """Query Gemini with retry logic and API key rotation"""
        
        for attempt in range(max_retries):
            try:
                if not self.model:
                    self._initialize_gemini_model()
                
                response = await asyncio.to_thread(self.model.generate_content, prompt)
                
                if response.text:
                    return response.text.strip()
                else:
                    raise Exception("Empty response from Gemini")
                    
            except Exception as e:
                logger.warning(f"Gemini query attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    self._rotate_api_key()
                    await asyncio.sleep(1)
                else:
                    raise e
    
    def _parse_ai_symptom_analysis(self, gemini_response: str, patient_input: str) -> AISymptomAnalysis:
        """Parse Gemini response into structured analysis"""
        
        try:
            # Try to extract JSON from response
            json_start = gemini_response.find('{')
            json_end = gemini_response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = gemini_response[json_start:json_end]
                analysis_data = json.loads(json_str)
            else:
                # Fallback parsing if no clear JSON structure
                analysis_data = self._extract_analysis_from_text(gemini_response)
            
            return AISymptomAnalysis(
                original_input=patient_input,
                vagueness_type=analysis_data.get('vagueness_type', 'emotional_vague'),
                missing_information=analysis_data.get('missing_information', ['specific_symptoms']),
                clinical_priority=analysis_data.get('clinical_priority', 'routine'),
                medical_domains=analysis_data.get('medical_domains', ['general_medicine']),
                urgency_indicators=analysis_data.get('urgency_indicators', []),
                patient_communication_style=analysis_data.get('patient_communication_style', 'uncertain'),
                confidence_score=float(analysis_data.get('confidence_score', 0.7)),
                ai_reasoning=analysis_data.get('ai_reasoning', 'AI analysis completed'),
                processing_time_ms=0.0,  # Set by caller
                gemini_model_used=""  # Set by caller
            )
            
        except Exception as e:
            logger.error(f"Failed to parse AI analysis: {str(e)}")
            return self._create_fallback_analysis(patient_input, 0)
    
    def _extract_analysis_from_text(self, response_text: str) -> Dict[str, Any]:
        """Extract analysis from unstructured text response"""
        
        # Basic fallback extraction
        return {
            "vagueness_type": "emotional_vague",
            "missing_information": ["specific_symptoms", "location", "severity"],
            "clinical_priority": "routine",
            "medical_domains": ["general_medicine"],
            "urgency_indicators": [],
            "patient_communication_style": "uncertain",
            "confidence_score": 0.6,
            "ai_reasoning": f"Analyzed patient input with fallback parsing: {response_text[:200]}..."
        }
    
    def _create_fallback_analysis(self, patient_input: str, processing_time: float) -> AISymptomAnalysis:
        """Create fallback analysis if AI fails"""
        
        return AISymptomAnalysis(
            original_input=patient_input,
            vagueness_type="emotional_vague",
            missing_information=["specific_symptoms", "location", "severity"],
            clinical_priority="routine",
            medical_domains=["general_medicine"],
            urgency_indicators=[],
            patient_communication_style="uncertain",
            confidence_score=0.5,
            ai_reasoning="Fallback analysis due to AI processing error",
            processing_time_ms=processing_time * 1000,
            gemini_model_used="fallback"
        )


class AIQuestionGenerator:
    """
    💎 GENERATE PROGRESSIVE QUESTIONS USING GEMINI AI FOR UNLIMITED ADAPTABILITY
    
    Uses Gemini to generate contextually perfect progressive questions with clinical reasoning
    """
    
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        gemini_keys_str = os.getenv('GEMINI_API_KEYS', '')
        self.gemini_api_keys = [key.strip() for key in gemini_keys_str.split(',') if key.strip()]
        
        if self.gemini_api_key and self.gemini_api_key not in self.gemini_api_keys:
            self.gemini_api_keys.insert(0, self.gemini_api_key)
        
        self.current_key_index = 0
        self.model = None
        self._initialize_gemini_model()
    
    def _initialize_gemini_model(self):
        """Initialize Gemini model with current API key"""
        try:
            if self.current_key_index < len(self.gemini_api_keys):
                api_key = self.gemini_api_keys[self.current_key_index]
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
            else:
                raise ValueError("All Gemini API keys exhausted")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {str(e)}")
            self._rotate_api_key()
    
    def _rotate_api_key(self):
        """Rotate to next API key"""
        self.current_key_index = (self.current_key_index + 1) % len(self.gemini_api_keys)
        self._initialize_gemini_model()
    
    async def generate_progressive_questions_with_ai(self, symptom_analysis: AISymptomAnalysis, conversation_state: Dict[str, Any] = None, patient_profile: Dict[str, Any] = None) -> List[AIGeneratedQuestion]:
        """
        🧠 USE GEMINI TO GENERATE CONTEXTUALLY PERFECT PROGRESSIVE QUESTIONS
        
        Generates medically appropriate progressive questions that transform vague symptoms
        into specific, clinically actionable information.
        """
        
        question_prompt = self._create_question_generation_prompt(symptom_analysis, conversation_state, patient_profile)
        
        try:
            response = await self._query_gemini_with_retry(question_prompt)
            questions = self._parse_ai_generated_questions(response)
            return questions
            
        except Exception as e:
            logger.error(f"AI question generation failed: {str(e)}")
            return self._create_fallback_questions(symptom_analysis)
    
    def _create_question_generation_prompt(self, symptom_analysis: AISymptomAnalysis, conversation_state: Dict[str, Any] = None, patient_profile: Dict[str, Any] = None) -> str:
        """Create comprehensive prompt for AI question generation"""
        
        conversation_info = ""
        if conversation_state:
            conversation_info = f"\nConversation History: {json.dumps(conversation_state, indent=2)}"
        
        profile_info = ""
        if patient_profile:
            profile_info = f"\nPatient Profile: {json.dumps(patient_profile, indent=2)}"
        
        prompt = f"""
You are an expert medical interviewer generating progressive questions for a vague symptom using advanced clinical reasoning.

Symptom Analysis: {asdict(symptom_analysis)}{conversation_info}{profile_info}

Generate 3-5 progressive questions that will transform this vague symptom into specific, clinically actionable information. 

Questions should be:
1. Medically appropriate and evidence-based
2. Empathetic and patient-centered  
3. Progressively more specific (general → detailed)
4. Adapted to patient's communication style
5. Prioritized by clinical importance

For each question, provide this JSON structure:
{{
    "questions": [
        {{
            "question_text": "Clear, empathetic question text",
            "medical_reasoning": "Why this question is medically important",
            "expected_information_type": "location|severity|timeline|quality|associated_symptoms|triggers",
            "clinical_priority": 1-5,
            "empathy_level": "high|medium|low", 
            "follow_up_strategy": "How to use the answer",
            "confidence_score": 0.0-1.0,
            "question_category": "symptom_specification|location_inquiry|severity_assessment|etc",
            "estimated_information_gain": 0.0-1.0
        }}
    ]
}}

MANDATORY EXAMPLES TO FOLLOW:
- "sick" → "Can you describe how you're feeling sick? Nausea, fatigue, fever, or something else?"
- "pain" → "Where is the pain located? Can you describe what it feels like?"  
- "bad" → "What specifically is bothering you? Physical symptoms or emotional concerns?"

Generate similar quality questions for the current symptom with:
- High empathy for emotional communication styles
- Clear specificity for minimal communicators
- Medical precision for technical inquiries
- Appropriate urgency for emergency indicators

Focus on efficient information gathering with clinical reasoning.
"""
        
        return prompt
    
    async def _query_gemini_with_retry(self, prompt: str, max_retries: int = 3) -> str:
        """Query Gemini with retry logic"""
        for attempt in range(max_retries):
            try:
                if not self.model:
                    self._initialize_gemini_model()
                
                response = await asyncio.to_thread(self.model.generate_content, prompt)
                
                if response.text:
                    return response.text.strip()
                else:
                    raise Exception("Empty response from Gemini")
                    
            except Exception as e:
                logger.warning(f"Gemini query attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    self._rotate_api_key()
                    await asyncio.sleep(1)
                else:
                    raise e
    
    def _parse_ai_generated_questions(self, gemini_response: str) -> List[AIGeneratedQuestion]:
        """Parse AI response into structured questions"""
        
        try:
            # Extract JSON from response
            json_start = gemini_response.find('{')
            json_end = gemini_response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = gemini_response[json_start:json_end]
                questions_data = json.loads(json_str)
                
                questions = []
                for q_data in questions_data.get('questions', []):
                    question = AIGeneratedQuestion(
                        question_text=q_data.get('question_text', 'Can you tell me more about your symptoms?'),
                        medical_reasoning=q_data.get('medical_reasoning', 'Gather more specific information'),
                        expected_information_type=q_data.get('expected_information_type', 'symptoms'),
                        clinical_priority=int(q_data.get('clinical_priority', 3)),
                        empathy_level=q_data.get('empathy_level', 'medium'),
                        follow_up_strategy=q_data.get('follow_up_strategy', 'Continue assessment'),
                        confidence_score=float(q_data.get('confidence_score', 0.7)),
                        question_category=q_data.get('question_category', 'symptom_specification'),
                        estimated_information_gain=float(q_data.get('estimated_information_gain', 0.7))
                    )
                    questions.append(question)
                
                return questions[:3]  # Return top 3 questions
            else:
                return self._extract_questions_from_text(gemini_response)
                
        except Exception as e:
            logger.error(f"Failed to parse AI questions: {str(e)}")
            return self._create_fallback_questions_simple()
    
    def _extract_questions_from_text(self, response_text: str) -> List[AIGeneratedQuestion]:
        """Extract questions from unstructured text"""
        
        # Try to find question-like sentences
        lines = response_text.split('\n')
        questions = []
        
        for line in lines:
            line = line.strip()
            if line and ('?' in line or 'what' in line.lower() or 'how' in line.lower() or 'where' in line.lower()):
                question = AIGeneratedQuestion(
                    question_text=line,
                    medical_reasoning="Extracted from AI response",
                    expected_information_type="symptoms",
                    clinical_priority=3,
                    empathy_level="medium",
                    follow_up_strategy="Continue assessment",
                    confidence_score=0.6,
                    question_category="symptom_specification",
                    estimated_information_gain=0.6
                )
                questions.append(question)
                
                if len(questions) >= 3:
                    break
        
        return questions if questions else self._create_fallback_questions_simple()
    
    def _create_fallback_questions_simple(self) -> List[AIGeneratedQuestion]:
        """Create simple fallback questions"""
        
        return [
            AIGeneratedQuestion(
                question_text="Can you help me understand what specific symptoms you're experiencing?",
                medical_reasoning="Gather basic symptom information",
                expected_information_type="symptoms",
                clinical_priority=1,
                empathy_level="high",
                follow_up_strategy="Assess specific symptoms",
                confidence_score=0.8,
                question_category="symptom_specification",
                estimated_information_gain=0.8
            )
        ]
    
    def _create_fallback_questions(self, symptom_analysis: AISymptomAnalysis) -> List[AIGeneratedQuestion]:
        """Create contextual fallback questions based on analysis"""
        
        # Create context-aware fallback questions
        if "sick" in symptom_analysis.original_input.lower():
            return [
                AIGeneratedQuestion(
                    question_text="Can you describe how you're feeling sick? Nausea, fatigue, fever, or something else?",
                    medical_reasoning="Specify type of sickness symptoms",
                    expected_information_type="symptoms",
                    clinical_priority=1,
                    empathy_level="high",
                    follow_up_strategy="Assess specific illness symptoms",
                    confidence_score=0.9,
                    question_category="symptom_specification",
                    estimated_information_gain=0.9
                )
            ]
        elif "pain" in symptom_analysis.original_input.lower():
            return [
                AIGeneratedQuestion(
                    question_text="Where is the pain located? Can you describe what it feels like?",
                    medical_reasoning="Determine pain location and quality",
                    expected_information_type="location",
                    clinical_priority=1,
                    empathy_level="medium",
                    follow_up_strategy="Assess pain characteristics",
                    confidence_score=0.9,
                    question_category="location_inquiry",
                    estimated_information_gain=0.9
                )
            ]
        elif "bad" in symptom_analysis.original_input.lower():
            return [
                AIGeneratedQuestion(
                    question_text="What specifically is bothering you? Physical symptoms or emotional concerns?",
                    medical_reasoning="Differentiate physical vs emotional issues",
                    expected_information_type="symptoms",
                    clinical_priority=1,
                    empathy_level="high",
                    follow_up_strategy="Clarify concern type",
                    confidence_score=0.9,
                    question_category="physical_vs_emotional",
                    estimated_information_gain=0.8
                )
            ]
        else:
            return self._create_fallback_questions_simple()


# Global instances for easy access
llm_symptom_analyzer = LLMSymptomAnalyzer()
ai_question_generator = AIQuestionGenerator()