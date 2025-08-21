"""
😰 PHASE 7.1: AI-ENHANCED EMOTIONAL INTELLIGENCE VALIDATOR
Revolutionary Gemini-Integrated Emotional Context Testing and Validation System

CAPABILITIES:
- Generate emotionally complex medical scenarios using Gemini AI
- Validate empathetic responses with AI reasoning
- Create comprehensive emotional intelligence test cases
- Assess medical AI empathy and communication quality

Algorithm Version: 7.1_ai_emotional_intelligence_validation
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

from ai_powered_medical_nlp_test_suite import GeminiPoweredTestingEngine, AIGeneratedTestCase, TestDifficulty, LanguagePatternType, AIValidationResult
import logging

logger = logging.getLogger(__name__)

class EmotionalState(str, Enum):
    HIGH_ANXIETY = "high_anxiety"
    PANIC = "panic"
    DEPRESSION = "depression" 
    ANGER_FRUSTRATION = "anger_frustration"
    FEAR_TERROR = "fear_terror"
    EMBARRASSMENT_SHAME = "embarrassment_shame"
    HOPELESSNESS_DESPAIR = "hopelessness_despair"
    RELIEF_GRATITUDE = "relief_gratitude"
    CONFUSION_UNCERTAINTY = "confusion_uncertainty"
    GRIEF_LOSS = "grief_loss"

class EmpathyLevel(str, Enum):
    MINIMAL = "minimal"           # 1-2: Basic acknowledgment
    LOW = "low"                   # 3-4: Some emotional recognition
    MODERATE = "moderate"         # 5-6: Good emotional understanding
    HIGH = "high"                 # 7-8: Strong empathetic response
    EXCEPTIONAL = "exceptional"   # 9-10: Profound emotional connection

class CommunicationStyle(str, Enum):
    PROFESSIONAL_CLINICAL = "professional_clinical"
    WARM_SUPPORTIVE = "warm_supportive"
    REASSURING_CALM = "reassuring_calm"
    URGENT_DIRECTIVE = "urgent_directive"
    GENTLE_PATIENT = "gentle_patient"
    VALIDATING_AFFIRMING = "validating_affirming"

@dataclass
class EmotionalMedicalScenario:
    """Emotionally complex medical scenario with validation criteria"""
    scenario_id: str
    patient_emotional_state: EmotionalState
    medical_content: str
    emotional_markers: List[str]
    empathy_requirements: Dict[str, Any]
    communication_challenges: List[str]
    optimal_response_style: CommunicationStyle
    empathy_validation_criteria: Dict[str, Any]
    risk_factors: List[str]
    cultural_considerations: Optional[str] = None

@dataclass
class EmpathyValidationResult:
    """Comprehensive empathy validation with AI reasoning"""
    scenario_id: str
    ai_response_text: str
    empathy_score: float  # 0-10
    emotional_appropriateness: float  # 0-10
    medical_accuracy: float  # 0-10
    communication_effectiveness: float  # 0-10
    cultural_sensitivity: float  # 0-10
    overall_quality_score: float  # 0-10
    empathy_level: EmpathyLevel
    strengths_identified: List[str]
    improvement_areas: List[str]
    ai_reasoning: str
    validation_confidence: float

class AIEmotionalIntelligenceValidator:
    """
    😰 Uses Gemini for sophisticated emotional context understanding and empathy validation
    """
    
    def __init__(self, testing_engine: GeminiPoweredTestingEngine = None):
        """Initialize AI emotional intelligence validator"""
        self.testing_engine = testing_engine or GeminiPoweredTestingEngine()
        self.validation_stats = {
            'total_scenarios_generated': 0,
            'empathy_validations_performed': 0,
            'average_empathy_score': 0.0,
            'emotional_state_coverage': {},
            'average_validation_time': 0.0
        }
        
        logger.info("😰 AI Emotional Intelligence Validator initialized")
    
    async def generate_emotional_medical_scenarios_with_ai(self, base_symptoms: List[str], scenarios_per_symptom: int = 20) -> List[EmotionalMedicalScenario]:
        """
        Create emotionally complex medical scenarios using AI
        
        AI EMOTION PROMPT:
        "You are a psychology expert creating emotionally complex medical scenarios.
        
        Base symptoms: {base_symptoms}
        
        Create 20 different emotional presentations of these symptoms including:
        1. High anxiety/panic presentations  
        2. Depression-influenced descriptions
        3. Anger and frustration expressions
        4. Fear-based communications
        5. Embarrassment and shame contexts
        6. Hopelessness and despair presentations
        
        For each scenario:
        - Provide the emotional + medical text
        - Identify emotional state markers
        - Suggest appropriate empathetic responses
        - Rate urgency considering emotional context
        - Recommend communication strategies
        
        Ensure medical accuracy while capturing authentic emotional expressions."
        """
        
        all_scenarios = []
        
        for symptom in base_symptoms:
            symptom_scenarios_prompt = f"""
            You are a medical psychology expert creating realistic emotional medical scenarios for AI training.
            
            BASE SYMPTOM: {symptom}
            SCENARIOS TO GENERATE: {scenarios_per_symptom}
            
            Create {scenarios_per_symptom} diverse emotional presentations of {symptom} symptoms:
            
            EMOTIONAL STATES TO INCLUDE:
            1. HIGH ANXIETY/PANIC: "I'm freaking out about this {symptom}..."
            2. DEPRESSION: "I don't even care anymore about this {symptom}..."
            3. ANGER/FRUSTRATION: "I'm so pissed that this {symptom} won't go away..."
            4. FEAR/TERROR: "I'm terrified this {symptom} means something terrible..."
            5. EMBARRASSMENT/SHAME: "I'm so embarrassed to talk about this {symptom}..."
            6. HOPELESSNESS/DESPAIR: "Nothing helps this {symptom}, I give up..."
            7. RELIEF/GRATITUDE: "Thank god someone understands this {symptom}..."
            8. CONFUSION/UNCERTAINTY: "I don't understand what this {symptom} means..."
            9. GRIEF/LOSS: "Ever since I lost [person], this {symptom} started..."
            10. OVERWHELM: "Everything is too much with this {symptom}..."
            
            SCENARIO COMPLEXITY FACTORS:
            - Life stressors affecting symptoms
            - Family dynamics and medical history
            - Work/financial stress impacts
            - Relationship challenges
            - Previous traumatic medical experiences
            - Cultural/religious beliefs about health
            - Age-related fears and concerns
            - Social stigma and isolation
            
            FOR EACH SCENARIO PROVIDE:
            {{
                "scenario_id": "[unique_id]",
                "patient_emotional_state": "[primary emotional state]",
                "medical_content": "[patient's emotional medical statement]",
                "emotional_markers": ["[list of emotional indicators]"],
                "empathy_requirements": {{
                    "primary_needs": ["[emotional needs]"],
                    "validation_required": ["[what needs validation]"],
                    "support_type": "[type of support needed]",
                    "communication_approach": "[recommended approach]"
                }},
                "communication_challenges": ["[specific challenges]"],
                "optimal_response_style": "[best communication style]",
                "empathy_validation_criteria": {{
                    "acknowledgment_of_emotion": "[criteria]",
                    "medical_reassurance": "[criteria]", 
                    "next_steps_guidance": "[criteria]",
                    "emotional_support": "[criteria]"
                }},
                "risk_factors": ["[psychological/medical risks]"],
                "cultural_considerations": "[cultural factors if applicable]",
                "expected_empathy_level": "[minimal/low/moderate/high/exceptional]",
                "scenario_difficulty": "[easy/medium/hard/expert]"
            }}
            
            Ensure scenarios are:
            - Medically realistic and accurate
            - Emotionally authentic and complex
            - Culturally diverse and inclusive
            - Varying in difficulty and complexity
            - Representative of real patient experiences
            
            Return as JSON array for AI training and validation.
            """
            
            try:
                start_time = time.time()
                ai_response = await self.testing_engine._call_gemini_with_fallback(symptom_scenarios_prompt)
                generation_time = time.time() - start_time
                
                # Parse scenarios from AI response
                symptom_scenarios = self._parse_emotional_scenarios(ai_response, symptom)
                all_scenarios.extend(symptom_scenarios)
                
                # Update statistics
                self._update_scenario_stats(symptom_scenarios, generation_time)
                
                logger.info(f"✅ Generated {len(symptom_scenarios)} emotional scenarios for {symptom}")
                
                # Brief delay for API rate management
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"❌ Emotional scenario generation failed for {symptom}: {e}")
                fallback_scenarios = self._generate_fallback_emotional_scenarios(symptom, 3)
                all_scenarios.extend(fallback_scenarios)
        
        logger.info(f"🎯 Total emotional scenarios generated: {len(all_scenarios)}")
        return all_scenarios
    
    async def validate_empathetic_responses_with_ai(self, patient_input: str, ai_response: str, emotional_context: Dict[str, Any] = None) -> EmpathyValidationResult:
        """
        Use Gemini to evaluate empathetic response quality
        """
        
        context_info = emotional_context or {}
        
        empathy_validation_prompt = f"""
        You are an expert in medical empathy and therapeutic communication evaluating AI responses to emotionally distressed patients.
        
        PATIENT INPUT (with emotional context): "{patient_input}"
        AI RESPONSE TO EVALUATE: "{ai_response}"
        
        EMOTIONAL CONTEXT:
        - Patient Emotional State: {context_info.get('emotional_state', 'unknown')}
        - Emotional Intensity: {context_info.get('intensity_level', 'moderate')}
        - Cultural Background: {context_info.get('cultural_background', 'not specified')}
        - Previous Medical Trauma: {context_info.get('medical_trauma_history', 'unknown')}
        
        Provide comprehensive empathy validation analysis:
        
        1. EMPATHY ASSESSMENT (0-10 scales):
           - Empathy Level: How well does the response acknowledge and validate patient emotions?
           - Emotional Appropriateness: Is the emotional tone suitable for the patient's state?
           - Medical Accuracy: Does the response maintain medical accuracy while being empathetic?
           - Communication Effectiveness: How clear and helpful is the communication?
           - Cultural Sensitivity: How well does it respect cultural considerations?
        
        2. DETAILED EMPATHY ANALYSIS:
           - Emotional acknowledgment quality
           - Validation of patient experience
           - Reassurance and support provided
           - Professional boundary maintenance
           - Crisis intervention appropriateness
           - Trust-building elements
        
        3. COMMUNICATION QUALITY:
           - Language appropriateness for emotional state
           - Tone matching patient needs
           - Clarity and understandability
           - Action steps provided
           - Follow-up considerations
        
        4. STRENGTHS IDENTIFICATION:
           - What the AI response did well
           - Effective empathetic elements
           - Good medical communication aspects
           - Cultural sensitivity strengths
        
        5. IMPROVEMENT AREAS:
           - Specific empathy gaps
           - Communication enhancement opportunities
           - Cultural sensitivity improvements
           - Medical accuracy refinements
        
        6. OVERALL QUALITY ASSESSMENT:
           - Overall empathy level (minimal/low/moderate/high/exceptional)
           - Total quality score (0-10)
           - Validation confidence (0-10)
           - Risk assessment for patient care
        
        7. RECOMMENDATIONS:
           - Specific improvement suggestions
           - Alternative response approaches
           - Training focus areas
           - Communication strategy adjustments
        
        EVALUATION CRITERIA:
        - Exceptional (9-10): Profound emotional understanding, perfect tone, comprehensive support
        - High (7-8): Strong empathy, appropriate response, good emotional support
        - Moderate (5-6): Basic empathy recognition, adequate response
        - Low (3-4): Minimal emotional awareness, clinical but lacking warmth
        - Minimal (1-2): No emotional recognition, purely transactional
        
        Return detailed structured evaluation as JSON for AI improvement.
        """
        
        try:
            start_time = time.time()
            ai_validation_response = await self.testing_engine._call_gemini_with_fallback(empathy_validation_prompt)
            validation_time = time.time() - start_time
            
            # Parse validation result
            validation_result = self._parse_empathy_validation(ai_validation_response, patient_input, ai_response)
            
            # Update validation statistics
            self._update_validation_stats(validation_result, validation_time)
            
            logger.info(f"✅ Empathy validation completed in {validation_time:.3f}s")
            return validation_result
            
        except Exception as e:
            logger.error(f"❌ Empathy validation failed: {e}")
            return self._generate_fallback_validation(patient_input, ai_response)
    
    async def assess_emotional_complexity_with_ai(self, emotional_text: str) -> Dict[str, Any]:
        """
        Assess the emotional complexity and validation requirements of patient text
        """
        
        complexity_assessment_prompt = f"""
        You are a clinical psychology expert assessing emotional complexity in patient communications.
        
        PATIENT TEXT: "{emotional_text}"
        
        Provide comprehensive emotional complexity assessment:
        
        1. EMOTIONAL STATE ANALYSIS:
           - Primary emotions identified (list with confidence scores)
           - Emotional intensity level (1-10)
           - Emotional volatility indicators
           - Underlying psychological patterns
           - Crisis risk indicators
        
        2. COMMUNICATION CHALLENGES:
           - Complexity level for AI processing (1-10)
           - Empathy requirements (specific needs)
           - Cultural sensitivity requirements
           - Professional boundary considerations
           - Therapeutic response needs
        
        3. VALIDATION REQUIREMENTS:
           - What emotions need acknowledgment
           - What experiences need validation
           - What fears need addressing
           - What support is needed
           - What reassurances are appropriate
        
        4. RISK ASSESSMENT:
           - Suicide/self-harm risk indicators
           - Mental health crisis signs
           - Medical emergency emotional markers
           - Family/social support needs
           - Professional referral requirements
        
        5. RESPONSE STRATEGY RECOMMENDATIONS:
           - Optimal communication approach
           - Empathy level requirements
           - Language and tone recommendations
           - Cultural considerations
           - Follow-up communication needs
        
        Return structured assessment for AI empathy training and response optimization.
        """
        
        try:
            ai_response = await self.testing_engine._call_gemini_with_fallback(complexity_assessment_prompt)
            complexity_analysis = self._parse_emotional_complexity(ai_response)
            
            logger.info("✅ Emotional complexity assessment completed")
            return complexity_analysis
            
        except Exception as e:
            logger.error(f"❌ Emotional complexity assessment failed: {e}")
            return self._generate_fallback_complexity_assessment(emotional_text)
    
    async def generate_empathy_test_cases_with_ai(self, emotional_scenarios: List[str], cases_per_scenario: int = 10) -> List[AIGeneratedTestCase]:
        """
        Generate comprehensive empathy test cases for different emotional scenarios
        """
        all_test_cases = []
        
        for scenario in emotional_scenarios:
            scenario_prompt = f"""
            Generate {cases_per_scenario} empathy testing cases for medical AI systems.
            
            EMOTIONAL SCENARIO: {scenario}
            
            Create diverse test cases that evaluate AI empathy and emotional intelligence:
            
            TEST CASE CATEGORIES:
            1. Crisis Communication (suicide risk, self-harm, panic attacks)
            2. Chronic Illness Emotional Support (depression, hopelessness, anger)
            3. Medical Trauma Processing (past bad experiences, PTSD triggers)
            4. Family/Relationship Impact (guilt, burden, isolation)
            5. Cultural/Religious Emotional Conflicts (beliefs vs. medical advice)
            6. Financial/Social Stress (anxiety about costs, job loss fears)
            7. Body Image/Identity Issues (shame, embarrassment, self-worth)
            8. End-of-Life Emotional Processing (grief, fear, acceptance)
            
            FOR EACH TEST CASE PROVIDE:
            - Patient's emotionally complex statement
            - Emotional state and intensity markers
            - Cultural/demographic context
            - Expected empathetic response elements
            - Validation criteria for AI responses
            - Common empathy mistakes to avoid
            - Success metrics for emotional intelligence
            - Risk factors and safety considerations
            
            ENSURE TEST CASES ARE:
            - Emotionally authentic and realistic
            - Medically accurate and appropriate
            - Culturally diverse and inclusive
            - Varying in emotional complexity
            - Representative of real patient experiences
            - Suitable for AI training and evaluation
            
            Return as JSON array with comprehensive testing data.
            """
            
            try:
                ai_response = await self.testing_engine._call_gemini_with_fallback(scenario_prompt)
                scenario_test_cases = self._parse_empathy_test_cases(ai_response, scenario)
                all_test_cases.extend(scenario_test_cases)
                
                logger.info(f"✅ Generated {len(scenario_test_cases)} empathy test cases for {scenario}")
                
                # Brief delay for API management
                await asyncio.sleep(0.4)
                
            except Exception as e:
                logger.error(f"❌ Empathy test case generation failed for {scenario}: {e}")
                fallback_cases = self._generate_fallback_empathy_test_cases(scenario, 2)
                all_test_cases.extend(fallback_cases)
        
        logger.info(f"🎯 Total empathy test cases generated: {len(all_test_cases)}")
        return all_test_cases
    
    def _parse_emotional_scenarios(self, ai_response: str, symptom: str) -> List[EmotionalMedicalScenario]:
        """Parse AI-generated emotional scenarios"""
        try:
            import re
            json_pattern = r'\[.*\]'
            json_match = re.search(json_pattern, ai_response, re.DOTALL)
            
            if json_match:
                scenarios_data = json.loads(json_match.group())
            else:
                return self._generate_fallback_emotional_scenarios(symptom, 2)
            
            scenarios = []
            for scenario_data in scenarios_data:
                try:
                    scenario = EmotionalMedicalScenario(
                        scenario_id=scenario_data.get('scenario_id', f'{symptom}_emotional_{len(scenarios)}'),
                        patient_emotional_state=EmotionalState(scenario_data.get('patient_emotional_state', 'confusion_uncertainty')),
                        medical_content=scenario_data.get('medical_content', ''),
                        emotional_markers=scenario_data.get('emotional_markers', []),
                        empathy_requirements=scenario_data.get('empathy_requirements', {}),
                        communication_challenges=scenario_data.get('communication_challenges', []),
                        optimal_response_style=CommunicationStyle(scenario_data.get('optimal_response_style', 'warm_supportive')),
                        empathy_validation_criteria=scenario_data.get('empathy_validation_criteria', {}),
                        risk_factors=scenario_data.get('risk_factors', []),
                        cultural_considerations=scenario_data.get('cultural_considerations')
                    )
                    scenarios.append(scenario)
                except Exception as e:
                    logger.warning(f"⚠️ Skipping invalid emotional scenario: {e}")
                    continue
            
            return scenarios
            
        except Exception as e:
            logger.error(f"❌ Emotional scenarios parsing failed: {e}")
            return self._generate_fallback_emotional_scenarios(symptom, 2)
    
    def _parse_empathy_validation(self, ai_response: str, patient_input: str, ai_response_text: str) -> EmpathyValidationResult:
        """Parse AI empathy validation response"""
        try:
            import re
            json_pattern = r'\{.*\}'
            json_match = re.search(json_pattern, ai_response, re.DOTALL)
            
            if json_match:
                validation_data = json.loads(json_match.group())
            else:
                return self._generate_fallback_validation(patient_input, ai_response_text)
            
            # Extract scores and determine empathy level
            empathy_score = validation_data.get('empathy_level', 5.0)
            empathy_level = self._determine_empathy_level(empathy_score)
            
            return EmpathyValidationResult(
                scenario_id="validation_" + str(int(time.time())),
                ai_response_text=ai_response_text,
                empathy_score=empathy_score,
                emotional_appropriateness=validation_data.get('emotional_appropriateness', 5.0),
                medical_accuracy=validation_data.get('medical_accuracy', 5.0),
                communication_effectiveness=validation_data.get('communication_effectiveness', 5.0),
                cultural_sensitivity=validation_data.get('cultural_sensitivity', 5.0),
                overall_quality_score=validation_data.get('overall_quality_score', 5.0),
                empathy_level=empathy_level,
                strengths_identified=validation_data.get('strengths_identified', []),
                improvement_areas=validation_data.get('improvement_areas', []),
                ai_reasoning=validation_data.get('ai_reasoning', 'Validation analysis completed'),
                validation_confidence=validation_data.get('validation_confidence', 0.5)
            )
            
        except Exception as e:
            logger.error(f"❌ Empathy validation parsing failed: {e}")
            return self._generate_fallback_validation(patient_input, ai_response_text)
    
    def _parse_emotional_complexity(self, ai_response: str) -> Dict[str, Any]:
        """Parse AI emotional complexity assessment"""
        try:
            import re
            json_pattern = r'\{.*\}'
            json_match = re.search(json_pattern, ai_response, re.DOTALL)
            
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._generate_fallback_complexity_assessment("")
                
        except Exception as e:
            logger.error(f"❌ Emotional complexity parsing failed: {e}")
            return self._generate_fallback_complexity_assessment("")
    
    def _parse_empathy_test_cases(self, ai_response: str, scenario: str) -> List[AIGeneratedTestCase]:
        """Parse AI-generated empathy test cases"""
        try:
            import re
            json_pattern = r'\[.*\]'
            json_match = re.search(json_pattern, ai_response, re.DOTALL)
            
            if json_match:
                cases_data = json.loads(json_match.group())
            else:
                return self._generate_fallback_empathy_test_cases(scenario, 2)
            
            test_cases = []
            for case_data in cases_data:
                test_case = AIGeneratedTestCase(
                    id=f"empathy_{scenario}_{len(test_cases)+1}",
                    pattern_type=LanguagePatternType.EMOTIONAL_EXPRESSION,
                    input_text=case_data.get('patient_statement', ''),
                    expected_entities=case_data.get('medical_entities', []),
                    expected_intent=case_data.get('expected_intent', 'emotional_support'),
                    expected_urgency=case_data.get('urgency_level', 'medium'),
                    difficulty_level=TestDifficulty(case_data.get('difficulty', 'medium')),
                    confidence_score=case_data.get('confidence', 0.5),
                    ai_reasoning=case_data.get('empathy_requirements', 'Emotional intelligence test case'),
                    success_criteria=case_data.get('validation_criteria', {}),
                    emotional_state=case_data.get('emotional_state', 'mixed')
                )
                test_cases.append(test_case)
            
            return test_cases
            
        except Exception as e:
            logger.error(f"❌ Empathy test case parsing failed: {e}")
            return self._generate_fallback_empathy_test_cases(scenario, 2)
    
    def _determine_empathy_level(self, score: float) -> EmpathyLevel:
        """Determine empathy level from numeric score"""
        if score >= 9.0:
            return EmpathyLevel.EXCEPTIONAL
        elif score >= 7.0:
            return EmpathyLevel.HIGH
        elif score >= 5.0:
            return EmpathyLevel.MODERATE
        elif score >= 3.0:
            return EmpathyLevel.LOW
        else:
            return EmpathyLevel.MINIMAL
    
    def _generate_fallback_emotional_scenarios(self, symptom: str, num_scenarios: int) -> List[EmotionalMedicalScenario]:
        """Generate fallback emotional scenarios"""
        scenarios = []
        
        fallback_emotions = [
            (EmotionalState.HIGH_ANXIETY, f"I'm really worried about this {symptom}"),
            (EmotionalState.FEAR_TERROR, f"I'm scared this {symptom} means something serious"),
            (EmotionalState.ANGER_FRUSTRATION, f"This {symptom} is driving me crazy")
        ]
        
        for i in range(min(num_scenarios, len(fallback_emotions))):
            emotional_state, content = fallback_emotions[i]
            scenario = EmotionalMedicalScenario(
                scenario_id=f"fallback_{symptom}_emotional_{i+1}",
                patient_emotional_state=emotional_state,
                medical_content=content,
                emotional_markers=['worried', 'concerned'],
                empathy_requirements={'primary_needs': ['validation', 'reassurance']},
                communication_challenges=['emotional_distress'],
                optimal_response_style=CommunicationStyle.WARM_SUPPORTIVE,
                empathy_validation_criteria={'acknowledgment_required': True},
                risk_factors=['anxiety']
            )
            scenarios.append(scenario)
        
        return scenarios
    
    def _generate_fallback_validation(self, patient_input: str, ai_response: str) -> EmpathyValidationResult:
        """Generate fallback empathy validation"""
        return EmpathyValidationResult(
            scenario_id="fallback_validation",
            ai_response_text=ai_response,
            empathy_score=5.0,
            emotional_appropriateness=5.0,
            medical_accuracy=6.0,
            communication_effectiveness=5.0,
            cultural_sensitivity=5.0,
            overall_quality_score=5.2,
            empathy_level=EmpathyLevel.MODERATE,
            strengths_identified=['basic_response_provided'],
            improvement_areas=['empathy_enhancement_needed'],
            ai_reasoning="Fallback validation due to parsing error",
            validation_confidence=0.3
        )
    
    def _generate_fallback_complexity_assessment(self, text: str) -> Dict[str, Any]:
        """Generate fallback emotional complexity assessment"""
        return {
            'emotional_state_analysis': {'primary_emotions': ['concern'], 'intensity_level': 5},
            'communication_challenges': {'complexity_level': 5, 'empathy_requirements': 'moderate'},
            'validation_requirements': {'acknowledgment_needed': ['emotion'], 'support_type': 'general'},
            'risk_assessment': {'crisis_indicators': [], 'referral_needs': 'routine'},
            'response_strategy': {'approach': 'supportive', 'empathy_level': 'moderate'},
            'fallback_used': True
        }
    
    def _generate_fallback_empathy_test_cases(self, scenario: str, num_cases: int) -> List[AIGeneratedTestCase]:
        """Generate fallback empathy test cases"""
        fallback_cases = []
        
        emotional_statements = [
            "I'm really scared about what's happening to me",
            "I don't know what to do anymore with this pain",
            "Nobody understands how hard this is for me"
        ]
        
        for i in range(min(num_cases, len(emotional_statements))):
            test_case = AIGeneratedTestCase(
                id=f"fallback_empathy_{scenario}_{i+1}",
                pattern_type=LanguagePatternType.EMOTIONAL_EXPRESSION,
                input_text=emotional_statements[i],
                expected_entities=[{'entity': 'emotional_distress', 'type': 'psychological_state'}],
                expected_intent='emotional_support',
                expected_urgency='medium',
                difficulty_level=TestDifficulty.MEDIUM,
                confidence_score=0.5,
                ai_reasoning="Fallback emotional intelligence test case",
                success_criteria={'empathy_required': True, 'validation_needed': True},
                emotional_state='distressed'
            )
            fallback_cases.append(test_case)
        
        return fallback_cases
    
    def _update_scenario_stats(self, scenarios: List[EmotionalMedicalScenario], generation_time: float):
        """Update scenario generation statistics"""
        self.validation_stats['total_scenarios_generated'] += len(scenarios)
        
        # Track emotional state coverage
        for scenario in scenarios:
            emotional_state = scenario.patient_emotional_state.value
            self.validation_stats['emotional_state_coverage'][emotional_state] = \
                self.validation_stats['emotional_state_coverage'].get(emotional_state, 0) + 1
    
    def _update_validation_stats(self, validation_result: EmpathyValidationResult, validation_time: float):
        """Update validation statistics"""
        self.validation_stats['empathy_validations_performed'] += 1
        
        # Update average empathy score
        current_avg = self.validation_stats['average_empathy_score']
        total_validations = self.validation_stats['empathy_validations_performed']
        new_avg = ((current_avg * (total_validations - 1)) + validation_result.empathy_score) / total_validations
        self.validation_stats['average_empathy_score'] = new_avg
        
        # Update average validation time
        current_time_avg = self.validation_stats['average_validation_time']
        new_time_avg = ((current_time_avg * (total_validations - 1)) + validation_time) / total_validations
        self.validation_stats['average_validation_time'] = new_time_avg
    
    async def get_emotional_intelligence_statistics(self) -> Dict[str, Any]:
        """Get comprehensive emotional intelligence statistics"""
        return {
            'algorithm_version': '7.1_ai_emotional_intelligence_validation',
            'validation_statistics': self.validation_stats.copy(),
            'timestamp': datetime.utcnow().isoformat()
        }

# Global instance
ai_emotional_validator = None

def get_ai_emotional_validator() -> AIEmotionalIntelligenceValidator:
    """Get or create global AI emotional intelligence validator"""
    global ai_emotional_validator
    
    if ai_emotional_validator is None:
        ai_emotional_validator = AIEmotionalIntelligenceValidator()
    
    return ai_emotional_validator

# Convenience functions
async def generate_emotional_scenarios(symptoms: List[str], scenarios_per_symptom: int = 10) -> List[EmotionalMedicalScenario]:
    """Quick function to generate emotional medical scenarios"""
    validator = get_ai_emotional_validator()
    return await validator.generate_emotional_medical_scenarios_with_ai(symptoms, scenarios_per_symptom)

async def validate_empathetic_response(patient_input: str, ai_response: str, context: Dict[str, Any] = None) -> EmpathyValidationResult:
    """Quick function to validate empathetic response quality"""
    validator = get_ai_emotional_validator()
    return await validator.validate_empathetic_responses_with_ai(patient_input, ai_response, context)