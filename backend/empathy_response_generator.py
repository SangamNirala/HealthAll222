"""
💝🤖 EMPATHETIC RESPONSE GENERATOR 🤖💝
=========================================

MISSION: Generate emotionally intelligent, empathetic medical responses that match
patient emotional states while maintaining clinical professionalism and appropriate
therapeutic boundaries.

Features:
- Emotional state-matched response generation
- Professional empathy calibration (0.0 - 1.0 scale)
- Cultural sensitivity adaptation
- Medical professional boundary maintenance
- Real-time response optimization based on patient emotional needs
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import asyncio
import google.generativeai as genai
from motor.motor_asyncio import AsyncIOMotorDatabase

@dataclass
class EmpathyCalibration:
    """Empathy calibration settings for different emotional states"""
    emotional_state: str
    empathy_level: float  # 0.0 - 1.0
    response_tone: str
    validation_phrases: List[str]
    professional_boundaries: List[str]
    cultural_adaptations: List[str]

class EmpathyResponseGenerator:
    """
    💝🤖 EMPATHETIC RESPONSE GENERATOR
    
    Generates emotionally intelligent medical responses that provide appropriate
    empathy while maintaining professional medical standards and cultural sensitivity.
    """
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.logger = logging.getLogger(__name__)
        
        # Initialize Gemini API
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Empathy calibration settings for different emotional states
        self.empathy_calibrations = {
            'anxiety': EmpathyCalibration(
                emotional_state='anxiety',
                empathy_level=0.8,
                response_tone='reassuring_professional',
                validation_phrases=[
                    "I understand your concern", "It's natural to feel worried",
                    "Your feelings are completely valid", "Many patients share similar concerns"
                ],
                professional_boundaries=[
                    "While I can provide information and support, a medical examination is needed for diagnosis",
                    "I want to help ease your concerns while ensuring you get proper medical care"
                ],
                cultural_adaptations=['direct_communication', 'detailed_explanation', 'family_consideration']
            ),
            'fear': EmpathyCalibration(
                emotional_state='fear',
                empathy_level=0.85,
                response_tone='gentle_supportive',
                validation_phrases=[
                    "I can hear how frightened you are", "Fear about health is very understandable",
                    "Let's work through this together", "You're not alone in feeling this way"
                ],
                professional_boundaries=[
                    "I'm here to provide support and information to help reduce your fear",
                    "Professional medical evaluation will give us the clearest picture"
                ],
                cultural_adaptations=['empathetic_approach', 'step_by_step_explanation', 'comfort_focus']
            ),
            'frustration': EmpathyCalibration(
                emotional_state='frustration',
                empathy_level=0.7,
                response_tone='understanding_solution_focused',
                validation_phrases=[
                    "I can understand your frustration", "This situation must be really challenging",
                    "Your frustration is completely justified", "Let's see how we can help"
                ],
                professional_boundaries=[
                    "I want to help find solutions while working within medical protocols",
                    "Your concerns are important and deserve proper attention"
                ],
                cultural_adaptations=['problem_solving_focus', 'direct_acknowledgment', 'action_oriented']
            ),
            'depression': EmpathyCalibration(
                emotional_state='depression',
                empathy_level=0.9,
                response_tone='compassionate_hopeful',
                validation_phrases=[
                    "I hear how difficult things are for you", "These feelings are very real and valid",
                    "You've taken an important step by reaching out", "There is hope and help available"
                ],
                professional_boundaries=[
                    "Mental health support is crucial and I encourage professional counseling",
                    "While I can offer support, comprehensive mental health care requires specialized attention"
                ],
                cultural_adaptations=['gentle_approach', 'hope_instilling', 'resource_providing', 'stigma_sensitive']
            ),
            'panic': EmpathyCalibration(
                emotional_state='panic',
                empathy_level=0.95,
                response_tone='calm_immediate_support',
                validation_phrases=[
                    "I'm here with you right now", "Let's focus on getting you the help you need",
                    "You're going to be okay", "Help is available immediately"
                ],
                professional_boundaries=[
                    "This level of distress requires immediate professional attention",
                    "I'm providing support while ensuring you get urgent care"
                ],
                cultural_adaptations=['crisis_sensitive', 'immediate_action', 'calm_presence']
            ),
            'hope': EmpathyCalibration(
                emotional_state='hope',
                empathy_level=0.6,
                response_tone='encouraging_positive',
                validation_phrases=[
                    "I'm glad to hear your positive outlook", "Your hopefulness is wonderful to see",
                    "That's great progress", "Your attitude can be really helpful in healing"
                ],
                professional_boundaries=[
                    "Your positive attitude combined with proper medical care is a great combination",
                    "Let's continue supporting your progress with appropriate medical guidance"
                ],
                cultural_adaptations=['positive_reinforcement', 'progress_acknowledgment', 'forward_looking']
            ),
            'relief': EmpathyCalibration(
                emotional_state='relief',
                empathy_level=0.5,
                response_tone='warm_professional',
                validation_phrases=[
                    "I'm so glad you're feeling relieved", "That must be such a weight off your shoulders",
                    "It's wonderful to hear good news", "Your relief is very understandable"
                ],
                professional_boundaries=[
                    "This positive development is encouraging while we continue appropriate monitoring",
                    "It's great to share in your relief while maintaining proper medical oversight"
                ],
                cultural_adaptations=['celebration_appropriate', 'continued_care_focus', 'gratitude_expression']
            ),
            'calm': EmpathyCalibration(
                emotional_state='calm',
                empathy_level=0.4,
                response_tone='professional_informative',
                validation_phrases=[
                    "I appreciate your thoughtful approach", "Your calm demeanor is helpful",
                    "Thank you for the clear information", "Your composed approach is beneficial"
                ],
                professional_boundaries=[
                    "Professional medical guidance combined with your thoughtful approach is ideal",
                    "Maintaining this collaborative approach will serve your health well"
                ],
                cultural_adaptations=['respectful_professional', 'information_focused', 'collaborative']
            )
        }
        
        # Response optimization templates
        self.response_templates = {
            'medical_validation': {
                'high_anxiety': "I understand this is causing you significant worry, and that's completely natural when it comes to your health.",
                'moderate_anxiety': "It's normal to have some concern about your health symptoms.",
                'pain_acknowledgment': "I can hear that you're experiencing considerable discomfort, and pain can be really challenging to deal with.",
                'uncertainty_support': "Not knowing what's causing your symptoms can be really unsettling."
            },
            'professional_reassurance': {
                'information_gathering': "Let me help you by gathering some more information so we can better understand what's going on.",
                'next_steps': "Here's what I recommend as the next steps to address your concerns.",
                'medical_expertise': "Based on medical knowledge and your symptoms, here's what we should consider.",
                'collaborative_approach': "Let's work together to get you the care and answers you need."
            },
            'cultural_sensitivity': {
                'family_oriented': "I understand that health decisions often involve family considerations.",
                'direct_communication': "I'll provide you with clear, straightforward information.",
                'holistic_health': "We'll consider all aspects of your health and well-being.",
                'respectful_approach': "I want to ensure you feel heard and respected in this process."
            }
        }
        
        self.logger.info("💝 Empathy Response Generator initialized")

    async def generate_empathy_recommendations(
        self,
        sentiment_results: Dict[str, Any],
        communication_analysis: Dict[str, Any],
        medical_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        🎯 GENERATE EMPATHY RECOMMENDATIONS
        
        Analyzes emotional state and generates recommendations for empathetic response
        including empathy level, tone, and cultural considerations.
        """
        
        try:
            primary_emotion = sentiment_results.get('primary_emotion', 'calm')
            
            # Get base empathy calibration
            calibration = self.empathy_calibrations.get(
                primary_emotion, 
                self.empathy_calibrations['calm']
            )
            
            # Adjust empathy level based on intensity and context
            intensity = sentiment_results.get('intensity_level', 3)
            medical_anxiety = sentiment_results.get('medical_anxiety_score', 0.3)
            urgency_score = sentiment_results.get('urgency_score', 0.3)
            
            # Calculate adjusted empathy level
            empathy_adjustment = 0
            if intensity >= 4:
                empathy_adjustment += 0.1
            if medical_anxiety > 0.7:
                empathy_adjustment += 0.15
            if urgency_score > 0.8:
                empathy_adjustment += 0.2
            
            adjusted_empathy_level = min(calibration.empathy_level + empathy_adjustment, 1.0)
            
            # Determine cultural factors
            cultural_factors = await self._analyze_cultural_considerations(
                communication_analysis, medical_context
            )
            
            # Generate tone recommendation
            tone_recommendation = await self._determine_response_tone(
                primary_emotion, intensity, communication_analysis
            )
            
            return {
                'empathy_level': adjusted_empathy_level,
                'tone': tone_recommendation,
                'validation_phrases': calibration.validation_phrases,
                'professional_boundaries': calibration.professional_boundaries,
                'cultural_factors': cultural_factors,
                
                # Additional recommendations
                'priority_elements': self._get_priority_response_elements(
                    primary_emotion, intensity, medical_anxiety
                ),
                'avoid_elements': self._get_elements_to_avoid(primary_emotion),
                'response_structure_guidance': self._get_response_structure_guidance(
                    primary_emotion, communication_analysis.get('style', 'formal')
                )
            }
            
        except Exception as e:
            self.logger.error(f"Error generating empathy recommendations: {str(e)}")
            return self._default_empathy_recommendations()

    async def optimize_medical_response(
        self,
        original_response: str,
        emotional_analysis,  # EmotionalAnalysis object
        medical_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        🎯 OPTIMIZE MEDICAL RESPONSE WITH EMPATHY
        
        Takes a clinical response and optimizes it for emotional intelligence
        while maintaining medical accuracy and professionalism.
        """
        
        try:
            # Extract emotional context
            primary_emotion = emotional_analysis.primary_emotion.value
            empathy_level = emotional_analysis.recommended_empathy_level
            suggested_tone = emotional_analysis.suggested_response_tone
            intensity = emotional_analysis.emotional_intensity.value
            
            # Build optimization prompt
            optimization_prompt = self._build_empathy_optimization_prompt(
                original_response, primary_emotion, empathy_level, 
                suggested_tone, intensity, medical_context
            )
            
            # Generate optimized response using Gemini
            optimized_result = await self._generate_optimized_response(optimization_prompt)
            
            # Validate and refine the optimized response
            validated_response = await self._validate_empathetic_response(
                optimized_result, emotional_analysis, medical_context
            )
            
            # Calculate optimization metrics
            optimization_metrics = await self._calculate_optimization_metrics(
                original_response, validated_response, emotional_analysis
            )
            
            return {
                'response': validated_response['optimized_text'],
                'adjustments': validated_response['adjustments_made'],
                'validation_phrases': validated_response['validation_elements'],
                'boundary_maintenance': validated_response['professional_boundaries'],
                'cultural_considerations': validated_response['cultural_adaptations'],
                'emotional_validation': validated_response['validation_elements'],
                
                # Scoring and analytics
                'empathy_score': optimization_metrics['empathy_score'],
                'appropriateness_score': optimization_metrics['appropriateness_score'],
                'effectiveness_score': optimization_metrics['effectiveness_prediction'],
                
                # Optimization metadata
                'original_response_length': len(original_response),
                'optimized_response_length': len(validated_response['optimized_text']),
                'optimization_timestamp': datetime.now(),
                'primary_emotional_target': primary_emotion
            }
            
        except Exception as e:
            self.logger.error(f"Error optimizing medical response: {str(e)}")
            return self._fallback_optimization_result(original_response)

    def _build_empathy_optimization_prompt(
        self, 
        original_response: str,
        primary_emotion: str,
        empathy_level: float,
        suggested_tone: str,
        intensity: int,
        medical_context: Dict[str, Any]
    ) -> str:
        """Build comprehensive prompt for empathy optimization"""
        
        calibration = self.empathy_calibrations.get(primary_emotion, self.empathy_calibrations['calm'])
        
        return f"""
        As a medical communication expert specializing in empathetic patient care, optimize this medical response for emotional intelligence.

        ORIGINAL MEDICAL RESPONSE:
        "{original_response}"

        PATIENT EMOTIONAL STATE:
        - Primary Emotion: {primary_emotion}
        - Emotional Intensity: {intensity}/5
        - Recommended Empathy Level: {empathy_level:.2f}/1.0
        - Suggested Tone: {suggested_tone}

        OPTIMIZATION GUIDELINES:
        - Validation Phrases: {', '.join(calibration.validation_phrases[:2])}
        - Professional Boundaries: {', '.join(calibration.professional_boundaries)}
        - Response Tone: {calibration.response_tone}

        MEDICAL CONTEXT: {json.dumps(medical_context, default=str)}

        Generate an optimized response in JSON format:
        {{
            "optimized_response": "Enhanced response with appropriate empathy",
            "adjustments_made": ["list", "of", "specific", "adjustments"],
            "empathy_elements_added": ["validation", "phrases", "used"],
            "professional_boundary_maintenance": ["how", "boundaries", "maintained"],
            "cultural_adaptations": ["any", "cultural", "considerations"],
            "tone_adjustments": "description of tone modifications",
            "medical_accuracy_preservation": "how medical accuracy was maintained",
            "empathy_calibration_applied": "{empathy_level:.2f}"
        }}

        REQUIREMENTS:
        1. Maintain complete medical accuracy and safety
        2. Apply appropriate empathy level ({empathy_level:.2f})
        3. Include emotional validation for {primary_emotion}
        4. Keep professional boundaries intact
        5. Match tone to patient emotional needs
        6. Preserve all critical medical information
        7. Enhance patient emotional support without compromising clinical guidance
        """

    async def _generate_optimized_response(self, prompt: str) -> Dict[str, Any]:
        """Generate optimized response using Gemini"""
        
        try:
            response = await self.model.generate_content_async(prompt)
            result = json.loads(response.text.strip())
            return result
        except Exception as e:
            self.logger.error(f"Gemini optimization error: {str(e)}")
            return {
                "optimized_response": "I understand your concern. Let me help you with appropriate medical guidance.",
                "adjustments_made": ["basic_empathy_added"],
                "empathy_elements_added": ["understanding_acknowledgment"],
                "professional_boundary_maintenance": ["maintained_clinical_focus"],
                "cultural_adaptations": ["professional_approach"],
                "tone_adjustments": "basic empathetic enhancement"
            }

    async def _validate_empathetic_response(
        self,
        optimized_result: Dict[str, Any],
        emotional_analysis,
        medical_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate and refine the empathetically optimized response"""
        
        try:
            optimized_text = optimized_result.get('optimized_response', '')
            
            # Validation checks
            validation_issues = []
            
            # Check for appropriate empathy level
            empathy_indicators = len([phrase for phrase in ['understand', 'feel', 'concern', 'support', 'help'] 
                                   if phrase.lower() in optimized_text.lower()])
            
            target_empathy = emotional_analysis.recommended_empathy_level
            if target_empathy > 0.7 and empathy_indicators < 2:
                validation_issues.append('insufficient_empathy')
            elif target_empathy < 0.4 and empathy_indicators > 3:
                validation_issues.append('excessive_empathy')
            
            # Check for professional boundaries
            if not any(word in optimized_text.lower() for word in ['medical', 'professional', 'recommend', 'important']):
                validation_issues.append('weak_professional_boundaries')
            
            # Apply fixes if needed
            if validation_issues:
                optimized_text = await self._apply_validation_fixes(
                    optimized_text, validation_issues, emotional_analysis
                )
                optimized_result['adjustments_made'].extend([f"validation_fix_{issue}" for issue in validation_issues])
            
            return {
                'optimized_text': optimized_text,
                'adjustments_made': optimized_result.get('adjustments_made', []),
                'validation_elements': optimized_result.get('empathy_elements_added', []),
                'professional_boundaries': optimized_result.get('professional_boundary_maintenance', []),
                'cultural_adaptations': optimized_result.get('cultural_adaptations', []),
                'validation_issues_fixed': validation_issues
            }
            
        except Exception as e:
            self.logger.error(f"Response validation error: {str(e)}")
            return {
                'optimized_text': optimized_result.get('optimized_response', 'I understand your concern and want to help.'),
                'adjustments_made': ['basic_optimization'],
                'validation_elements': ['understanding'],
                'professional_boundaries': ['medical_focus'],
                'cultural_adaptations': [],
                'validation_issues_fixed': []
            }

    async def _calculate_optimization_metrics(
        self,
        original_response: str,
        optimized_response: Dict[str, Any],
        emotional_analysis
    ) -> Dict[str, float]:
        """Calculate metrics for optimization quality"""
        
        optimized_text = optimized_response['optimized_text']
        
        # Empathy score calculation
        empathy_words = ['understand', 'feel', 'concern', 'support', 'help', 'care', 'worry', 'comfort']
        empathy_count = sum(1 for word in empathy_words if word in optimized_text.lower())
        empathy_score = min(empathy_count * 0.15, 1.0)
        
        # Appropriateness score (medical professionalism maintained)
        professional_words = ['medical', 'recommend', 'professional', 'important', 'appropriate', 'care']
        professional_count = sum(1 for word in professional_words if word in optimized_text.lower())
        appropriateness_score = min(professional_count * 0.2 + 0.4, 1.0)
        
        # Effectiveness prediction (combination of factors)
        length_factor = min(len(optimized_text) / len(original_response), 2.0) * 0.2
        adjustment_factor = len(optimized_response.get('adjustments_made', [])) * 0.1
        effectiveness_score = min((empathy_score + appropriateness_score + length_factor + adjustment_factor) / 2.4, 1.0)
        
        return {
            'empathy_score': empathy_score,
            'appropriateness_score': appropriateness_score,
            'effectiveness_prediction': effectiveness_score
        }

    # Helper methods
    async def _analyze_cultural_considerations(
        self, communication_analysis: Dict[str, Any], medical_context: Dict[str, Any]
    ) -> List[str]:
        """Analyze cultural considerations for empathetic responses"""
        
        cultural_factors = []
        
        # Communication style considerations
        style = communication_analysis.get('style', 'formal')
        if style == 'formal':
            cultural_factors.extend(['respectful_professional', 'detailed_explanation'])
        elif style == 'casual':
            cultural_factors.extend(['approachable_tone', 'conversational'])
        
        # Add general cultural sensitivity
        cultural_factors.extend(['inclusive_language', 'non_judgmental'])
        
        return cultural_factors

    async def _determine_response_tone(
        self, emotion: str, intensity: int, communication_analysis: Dict[str, Any]
    ) -> str:
        """Determine optimal response tone"""
        
        base_tone = self.empathy_calibrations.get(emotion, self.empathy_calibrations['calm']).response_tone
        
        # Adjust based on intensity
        if intensity >= 4:
            if 'professional' in base_tone:
                base_tone = base_tone.replace('professional', 'supportive_professional')
        
        return base_tone

    def _get_priority_response_elements(self, emotion: str, intensity: int, medical_anxiety: float) -> List[str]:
        """Get priority elements to include in response"""
        
        elements = ['medical_information', 'next_steps']
        
        if emotion in ['anxiety', 'fear', 'panic']:
            elements.extend(['reassurance', 'validation'])
        if emotion == 'frustration':
            elements.extend(['acknowledgment', 'solution_focus'])
        if emotion in ['depression', 'desperation']:
            elements.extend(['hope_instilling', 'support_resources'])
        if medical_anxiety > 0.7:
            elements.append('anxiety_specific_reassurance')
        if intensity >= 4:
            elements.append('immediate_support')
            
        return elements

    def _get_elements_to_avoid(self, emotion: str) -> List[str]:
        """Get elements to avoid in response"""
        
        avoid_elements = []
        
        if emotion in ['anxiety', 'fear', 'panic']:
            avoid_elements.extend(['dismissive_language', 'worst_case_scenarios'])
        if emotion == 'frustration':
            avoid_elements.extend(['defensive_responses', 'minimizing_concerns'])
        if emotion in ['depression', 'desperation']:
            avoid_elements.extend(['false_optimism', 'rushed_solutions'])
            
        return avoid_elements

    def _get_response_structure_guidance(self, emotion: str, communication_style: str) -> Dict[str, str]:
        """Get guidance for structuring the response"""
        
        if emotion in ['panic', 'desperation']:
            return {
                'opening': 'immediate_validation_and_support',
                'middle': 'concrete_next_steps',
                'closing': 'continued_support_assurance'
            }
        elif emotion in ['anxiety', 'fear']:
            return {
                'opening': 'empathetic_acknowledgment',
                'middle': 'informative_reassurance',
                'closing': 'collaborative_next_steps'
            }
        else:
            return {
                'opening': 'professional_acknowledgment',
                'middle': 'informative_guidance',
                'closing': 'supportive_next_steps'
            }

    async def _apply_validation_fixes(
        self, optimized_text: str, validation_issues: List[str], emotional_analysis
    ) -> str:
        """Apply fixes for validation issues"""
        
        fixes = []
        
        if 'insufficient_empathy' in validation_issues:
            primary_emotion = emotional_analysis.primary_emotion.value
            validation_phrase = self.empathy_calibrations.get(primary_emotion, self.empathy_calibrations['calm']).validation_phrases[0]
            fixes.append(f"{validation_phrase}. ")
        
        if 'weak_professional_boundaries' in validation_issues:
            fixes.append("It's important that we approach this with appropriate medical guidance. ")
        
        # Apply fixes to beginning of response
        fixed_text = ''.join(fixes) + optimized_text
        
        return fixed_text

    def _default_empathy_recommendations(self) -> Dict[str, Any]:
        """Return default empathy recommendations"""
        return {
            'empathy_level': 0.6,
            'tone': 'professional_supportive',
            'validation_phrases': ['I understand your concern'],
            'professional_boundaries': ['Medical evaluation is important'],
            'cultural_factors': ['respectful_communication'],
            'priority_elements': ['medical_information', 'support'],
            'avoid_elements': ['dismissive_language'],
            'response_structure_guidance': {
                'opening': 'professional_acknowledgment',
                'middle': 'informative_guidance',
                'closing': 'supportive_next_steps'
            }
        }

    def _fallback_optimization_result(self, original_response: str) -> Dict[str, Any]:
        """Return fallback optimization result"""
        return {
            'response': f"I understand your concern. {original_response}",
            'adjustments': ['basic_empathy_addition'],
            'validation_phrases': ['understanding_acknowledgment'],
            'boundary_maintenance': ['professional_focus_maintained'],
            'cultural_considerations': [],
            'empathy_score': 0.6,
            'appropriateness_score': 0.8,
            'effectiveness_score': 0.7,
            'original_response_length': len(original_response),
            'optimized_response_length': len(original_response) + 25,
            'optimization_timestamp': datetime.now(),
            'primary_emotional_target': 'general'
        }