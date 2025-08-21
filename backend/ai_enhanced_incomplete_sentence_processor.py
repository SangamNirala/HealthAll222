"""
🧠 PHASE 7.1: AI-ENHANCED INCOMPLETE SENTENCE PROCESSOR
Revolutionary Gemini-Integrated Incomplete Medical Sentence Analysis and Completion System

CAPABILITIES:
- Understand and complete medical fragments using Gemini AI
- Generate completion suggestions with medical context
- Analyze incomplete medical statements with clinical reasoning
- Provide empathetic clarification strategies

Algorithm Version: 7.1_ai_incomplete_sentence_processing
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

class IncompletenessType(str, Enum):
    SUDDEN_CUTOFF = "sudden_cutoff"
    MISSING_CONTEXT = "missing_context"
    FRAGMENTED_THOUGHTS = "fragmented_thoughts"
    INTERRUPTED_SPEECH = "interrupted_speech"
    TRAILING_OFF = "trailing_off"
    EMOTIONAL_INTERRUPTION = "emotional_interruption"
    PAIN_INTERRUPTION = "pain_interruption"
    COGNITIVE_LIMITATION = "cognitive_limitation"

class CompletionUrgency(str, Enum):
    CRITICAL = "critical"         # Emergency information missing
    HIGH = "high"                 # Important medical details needed  
    MEDIUM = "medium"             # Clarification would be helpful
    LOW = "low"                   # Minor details missing

@dataclass
class IncompleteFragmentAnalysis:
    """Comprehensive analysis of incomplete medical fragment"""
    fragment_text: str
    incompleteness_type: IncompletenessType
    missing_elements: List[str]
    medical_entities_implied: List[Dict[str, Any]]
    urgency_level: CompletionUrgency
    completion_confidence: float
    clinical_context: Dict[str, Any]
    emotional_indicators: List[str]
    patient_state_assessment: Dict[str, Any]

@dataclass
class AICompletionSuggestion:
    """AI-generated completion suggestion with clinical reasoning"""
    suggested_completion: str
    completion_confidence: float
    medical_reasoning: str
    clarifying_questions: List[str]
    empathetic_prompts: List[str]
    risk_assessment: Dict[str, Any]
    clinical_priority: int  # 1-10 scale
    follow_up_strategy: str

class AIIncompleteSentenceProcessor:
    """
    🧠 Leverages Gemini for understanding and completing medical fragments with clinical intelligence
    """
    
    def __init__(self, testing_engine: GeminiPoweredTestingEngine = None):
        """Initialize AI incomplete sentence processor"""
        self.testing_engine = testing_engine or GeminiPoweredTestingEngine()
        self.processing_stats = {
            'total_fragments_processed': 0,
            'completion_suggestions_generated': 0,
            'average_processing_time': 0.0,
            'confidence_scores': []
        }
        
        logger.info("🧠 AI Incomplete Sentence Processor initialized")
    
    async def analyze_medical_fragments_with_ai(self, fragment_text: str) -> IncompleteFragmentAnalysis:
        """
        Use Gemini to understand medical context from fragments
        
        AI ANALYSIS PROMPT:
        "You are a medical AI expert analyzing incomplete medical statements.
        
        Fragment: '{fragment_text}'
        
        Analyze this medical fragment and provide:
        1. Most likely complete medical meaning
        2. Possible medical entities/symptoms implied
        3. Missing information that should be clarified
        4. Urgency level based on fragment context
        5. Confidence in interpretation
        6. Alternative interpretations if ambiguous
        
        Use medical knowledge and linguistic context for analysis."
        """
        
        fragment_analysis_prompt = f"""
        You are a medical AI expert specializing in understanding incomplete patient communications.
        
        PATIENT FRAGMENT: "{fragment_text}"
        
        Provide comprehensive medical fragment analysis:
        
        1. INCOMPLETENESS ASSESSMENT:
           - Type of incompleteness (sudden_cutoff, missing_context, fragmented_thoughts, interrupted_speech, trailing_off, emotional_interruption, pain_interruption, cognitive_limitation)
           - Specific missing elements (subject, verb, object, medical details, temporal information, severity, location)
           - Percentage of medical meaning recoverable (0-100%)
        
        2. MEDICAL CONTENT INFERENCE:
           - Primary symptoms or conditions implied
           - Anatomical references suggested
           - Severity indicators present
           - Temporal clues available
           - Medical entities extractable with confidence scores
        
        3. CLINICAL CONTEXT ANALYSIS:
           - Likely medical scenario
           - Patient emotional state indicators
           - Urgency level assessment (critical, high, medium, low)
           - Emergency indicators present
           - Pain or distress level implied
        
        4. COMPLETION STRATEGY:
           - Most probable complete medical meaning
           - Alternative interpretations
           - Critical information gaps
           - Risk assessment if left unclear
           - Clinical priority for clarification (1-10 scale)
        
        5. PATIENT STATE ASSESSMENT:
           - Emotional state indicators (anxiety, pain, confusion, fear)
           - Cognitive capacity implications
           - Communication barriers detected
           - Empathy requirements
        
        Format response as structured JSON for medical analysis processing.
        """
        
        try:
            start_time = time.time()
            ai_response = await self.testing_engine._call_gemini_with_fallback(fragment_analysis_prompt)
            processing_time = time.time() - start_time
            
            # Parse AI response into structured analysis
            analysis = self._parse_fragment_analysis(ai_response, fragment_text)
            
            # Update processing statistics
            self._update_processing_stats(analysis, processing_time)
            
            logger.info(f"✅ Fragment analysis completed in {processing_time:.3f}s")
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Fragment analysis failed: {e}")
            return self._generate_fallback_fragment_analysis(fragment_text)
    
    async def generate_completion_suggestions_with_ai(self, incomplete_input: str, context: Dict[str, Any] = None) -> List[AICompletionSuggestion]:
        """
        Use AI to suggest how to complete incomplete medical statements
        """
        
        context_info = context or {}
        patient_context = context_info.get('patient_history', 'No prior context available')
        conversation_context = context_info.get('conversation_history', 'No conversation history')
        
        completion_prompt = f"""
        You are a medical AI assistant helping complete and clarify incomplete patient statements.
        
        PATIENT STATEMENT: "{incomplete_input}"
        
        CONTEXT INFORMATION:
        - Patient History: {patient_context}
        - Conversation History: {conversation_context}
        
        Generate 3-5 completion suggestions with empathetic clarification strategies:
        
        FOR EACH COMPLETION SUGGESTION PROVIDE:
        1. COMPLETION ANALYSIS:
           - Most likely intended complete statement
           - Confidence in interpretation (0.0-1.0)
           - Medical reasoning for this completion
           - Alternative interpretations considered
        
        2. CLARIFICATION STRATEGY:
           - Empathetic questions to confirm understanding
           - Gentle prompts to gather missing information
           - Medical terminology explanations if needed
           - Emotional support language
        
        3. CLINICAL ASSESSMENT:
           - Risk level if left incomplete (low, medium, high, critical)
           - Medical priority for clarification (1-10)
           - Potential diagnostic implications
           - Safety considerations
        
        4. COMMUNICATION APPROACH:
           - Tone recommendations (reassuring, professional, urgent)
           - Phrasing suggestions for different patient types
           - Cultural sensitivity considerations
           - Follow-up conversation strategy
        
        EXAMPLE OUTPUT FORMAT:
        {{
            "completion_suggestions": [
                {{
                    "suggested_completion": "[complete medical statement]",
                    "completion_confidence": 0.85,
                    "medical_reasoning": "[clinical rationale]",
                    "clarifying_questions": [
                        "[empathetic question 1]",
                        "[empathetic question 2]"
                    ],
                    "empathetic_prompts": [
                        "[supportive prompt 1]",
                        "[supportive prompt 2]"
                    ],
                    "risk_assessment": {{
                        "risk_level": "[low/medium/high/critical]",
                        "safety_implications": "[safety concerns]",
                        "time_sensitivity": "[immediate/urgent/routine]"
                    }},
                    "clinical_priority": 7,
                    "follow_up_strategy": "[conversation continuation approach]"
                }}
            ]
        }}
        
        Ensure suggestions are medically appropriate, empathetic, and culturally sensitive.
        """
        
        try:
            ai_response = await self.testing_engine._call_gemini_with_fallback(completion_prompt)
            suggestions = self._parse_completion_suggestions(ai_response, incomplete_input)
            
            self.processing_stats['completion_suggestions_generated'] += len(suggestions)
            
            logger.info(f"✅ Generated {len(suggestions)} completion suggestions")
            return suggestions
            
        except Exception as e:
            logger.error(f"❌ Completion suggestion generation failed: {e}")
            return self._generate_fallback_completions(incomplete_input)
    
    async def assess_fragment_urgency_with_ai(self, fragment: str, medical_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Use AI to assess the urgency and medical significance of incomplete fragments
        """
        
        urgency_prompt = f"""
        You are a medical triage expert assessing the urgency of incomplete patient communications.
        
        PATIENT FRAGMENT: "{fragment}"
        MEDICAL CONTEXT: {json.dumps(medical_context or {}, indent=2)}
        
        Assess medical urgency and communication priorities:
        
        1. URGENCY CLASSIFICATION:
           - Emergency level (1-10 scale)
           - Time sensitivity (immediate, urgent, routine, non-urgent)
           - Triage category (emergency, urgent, semi-urgent, routine)
           
        2. MEDICAL RISK ASSESSMENT:
           - Potential conditions suggested by fragment
           - Worst-case scenario implications
           - Critical information gaps
           - Patient safety considerations
        
        3. COMPLETION PRIORITY:
           - How critical is completing this statement?
           - What medical information is at risk?
           - Clinical decision-making impact
           - Patient care implications
        
        4. INTERVENTION RECOMMENDATIONS:
           - Immediate actions needed
           - Information gathering priorities
           - Communication approach
           - Escalation thresholds
        
        Return structured assessment with clear recommendations.
        """
        
        try:
            ai_response = await self.testing_engine._call_gemini_with_fallback(urgency_prompt)
            urgency_assessment = self._parse_urgency_assessment(ai_response)
            
            logger.info("✅ Fragment urgency assessment completed")
            return urgency_assessment
            
        except Exception as e:
            logger.error(f"❌ Urgency assessment failed: {e}")
            return self._generate_fallback_urgency_assessment(fragment)
    
    async def generate_incomplete_sentence_test_cases(self, medical_scenarios: List[str], cases_per_scenario: int = 20) -> List[AIGeneratedTestCase]:
        """
        Generate comprehensive test cases for incomplete sentence processing
        """
        all_test_cases = []
        
        for scenario in medical_scenarios:
            scenario_prompt = f"""
            Generate {cases_per_scenario} realistic incomplete medical statements for testing NLP systems.
            
            MEDICAL SCENARIO: {scenario}
            
            Create diverse incomplete sentence patterns that real patients might produce:
            
            INCOMPLETENESS TYPES TO INCLUDE:
            1. Sudden cutoffs due to pain: "My chest is..." "I can't..."
            2. Emotional interruptions: "I'm scared that..." "What if..."
            3. Fragmentary descriptions: "Pain. Bad. Chest area."
            4. Missing context: "It hurts when..." "Started after..."
            5. Trailing off: "The doctor said something about..."
            6. Cognitive limitations: "Thing in my... you know..."
            7. Interrupted by symptoms: "I was feeling fine until—ow!"
            8. Stream of consciousness: "Pain and nausea and..."
            
            FOR EACH TEST CASE PROVIDE:
            - Incomplete patient statement
            - Most likely complete meaning
            - Medical entities that should be extracted
            - Urgency level assessment
            - Expected AI processing challenges
            - Success criteria for completion systems
            - Emotional state context
            - Clinical significance rating
            
            Ensure test cases represent diverse patient demographics and medical conditions.
            Return as JSON array for automated testing.
            """
            
            try:
                ai_response = await self.testing_engine._call_gemini_with_fallback(scenario_prompt)
                scenario_cases = self._parse_test_cases(ai_response, scenario)
                all_test_cases.extend(scenario_cases)
                
                logger.info(f"✅ Generated {len(scenario_cases)} test cases for {scenario}")
                
                # Brief delay to manage API rate limits
                await asyncio.sleep(0.3)
                
            except Exception as e:
                logger.error(f"❌ Test case generation failed for {scenario}: {e}")
                fallback_cases = self._generate_fallback_test_cases(scenario, 3)
                all_test_cases.extend(fallback_cases)
        
        logger.info(f"🎯 Total incomplete sentence test cases generated: {len(all_test_cases)}")
        return all_test_cases
    
    def _parse_fragment_analysis(self, ai_response: str, fragment_text: str) -> IncompleteFragmentAnalysis:
        """Parse AI fragment analysis response"""
        try:
            import re
            json_pattern = r'\{.*\}'
            json_match = re.search(json_pattern, ai_response, re.DOTALL)
            
            if json_match:
                analysis_data = json.loads(json_match.group())
            else:
                return self._generate_fallback_fragment_analysis(fragment_text)
            
            return IncompleteFragmentAnalysis(
                fragment_text=fragment_text,
                incompleteness_type=IncompletenessType(analysis_data.get('incompleteness_type', 'missing_context')),
                missing_elements=analysis_data.get('missing_elements', ['context']),
                medical_entities_implied=analysis_data.get('medical_entities', []),
                urgency_level=CompletionUrgency(analysis_data.get('urgency_level', 'medium')),
                completion_confidence=analysis_data.get('completion_confidence', 0.5),
                clinical_context=analysis_data.get('clinical_context', {}),
                emotional_indicators=analysis_data.get('emotional_indicators', []),
                patient_state_assessment=analysis_data.get('patient_state_assessment', {})
            )
            
        except Exception as e:
            logger.error(f"❌ Fragment analysis parsing failed: {e}")
            return self._generate_fallback_fragment_analysis(fragment_text)
    
    def _parse_completion_suggestions(self, ai_response: str, incomplete_input: str) -> List[AICompletionSuggestion]:
        """Parse AI completion suggestions"""
        try:
            import re
            json_pattern = r'\{.*\}'
            json_match = re.search(json_pattern, ai_response, re.DOTALL)
            
            if json_match:
                suggestions_data = json.loads(json_match.group())
                suggestions_list = suggestions_data.get('completion_suggestions', [])
            else:
                return self._generate_fallback_completions(incomplete_input)
            
            completions = []
            for suggestion in suggestions_list:
                completion = AICompletionSuggestion(
                    suggested_completion=suggestion.get('suggested_completion', 'Unable to complete'),
                    completion_confidence=suggestion.get('completion_confidence', 0.5),
                    medical_reasoning=suggestion.get('medical_reasoning', 'No reasoning provided'),
                    clarifying_questions=suggestion.get('clarifying_questions', []),
                    empathetic_prompts=suggestion.get('empathetic_prompts', []),
                    risk_assessment=suggestion.get('risk_assessment', {}),
                    clinical_priority=suggestion.get('clinical_priority', 5),
                    follow_up_strategy=suggestion.get('follow_up_strategy', 'Standard follow-up')
                )
                completions.append(completion)
            
            return completions
            
        except Exception as e:
            logger.error(f"❌ Completion suggestions parsing failed: {e}")
            return self._generate_fallback_completions(incomplete_input)
    
    def _parse_urgency_assessment(self, ai_response: str) -> Dict[str, Any]:
        """Parse AI urgency assessment"""
        try:
            import re
            json_pattern = r'\{.*\}'
            json_match = re.search(json_pattern, ai_response, re.DOTALL)
            
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._generate_fallback_urgency_assessment("")
                
        except Exception as e:
            logger.error(f"❌ Urgency assessment parsing failed: {e}")
            return self._generate_fallback_urgency_assessment("")
    
    def _parse_test_cases(self, ai_response: str, scenario: str) -> List[AIGeneratedTestCase]:
        """Parse AI-generated test cases"""
        try:
            import re
            json_pattern = r'\[.*\]'
            json_match = re.search(json_pattern, ai_response, re.DOTALL)
            
            if json_match:
                cases_data = json.loads(json_match.group())
            else:
                return self._generate_fallback_test_cases(scenario, 2)
            
            test_cases = []
            for case_data in cases_data:
                test_case = AIGeneratedTestCase(
                    id=f"incomplete_{scenario}_{len(test_cases)+1}",
                    pattern_type=LanguagePatternType.INCOMPLETE_SENTENCE,
                    input_text=case_data.get('incomplete_statement', ''),
                    expected_entities=case_data.get('medical_entities', []),
                    expected_intent=case_data.get('expected_intent', 'symptom_inquiry'),
                    expected_urgency=case_data.get('urgency_level', 'medium'),
                    difficulty_level=TestDifficulty(case_data.get('difficulty', 'medium')),
                    confidence_score=case_data.get('confidence', 0.5),
                    ai_reasoning=case_data.get('clinical_significance', 'Medical fragment analysis'),
                    success_criteria=case_data.get('success_criteria', {}),
                    emotional_state=case_data.get('emotional_context', 'neutral')
                )
                test_cases.append(test_case)
            
            return test_cases
            
        except Exception as e:
            logger.error(f"❌ Test case parsing failed: {e}")
            return self._generate_fallback_test_cases(scenario, 2)
    
    def _generate_fallback_fragment_analysis(self, fragment_text: str) -> IncompleteFragmentAnalysis:
        """Generate fallback fragment analysis"""
        return IncompleteFragmentAnalysis(
            fragment_text=fragment_text,
            incompleteness_type=IncompletenessType.MISSING_CONTEXT,
            missing_elements=['context', 'specificity'],
            medical_entities_implied=[{'entity': 'symptom', 'confidence': 0.5}],
            urgency_level=CompletionUrgency.MEDIUM,
            completion_confidence=0.4,
            clinical_context={'scenario': 'general_consultation'},
            emotional_indicators=['uncertain'],
            patient_state_assessment={'confidence': 'low', 'clarity': 'poor'}
        )
    
    def _generate_fallback_completions(self, incomplete_input: str) -> List[AICompletionSuggestion]:
        """Generate fallback completion suggestions"""
        return [
            AICompletionSuggestion(
                suggested_completion=f"Could you please complete your thought about '{incomplete_input[:20]}...'?",
                completion_confidence=0.6,
                medical_reasoning="Requesting clarification for incomplete medical statement",
                clarifying_questions=["Can you tell me more about what you were saying?"],
                empathetic_prompts=["I want to make sure I understand your concern completely."],
                risk_assessment={'risk_level': 'low', 'safety_implications': 'minimal'},
                clinical_priority=5,
                follow_up_strategy="Gentle clarification request"
            )
        ]
    
    def _generate_fallback_urgency_assessment(self, fragment: str) -> Dict[str, Any]:
        """Generate fallback urgency assessment"""
        return {
            'urgency_classification': {'emergency_level': 5, 'time_sensitivity': 'routine', 'triage_category': 'routine'},
            'medical_risk_assessment': {'potential_conditions': ['unspecified'], 'safety_considerations': 'standard'},
            'completion_priority': {'critical_level': 5, 'information_gaps': ['specificity'], 'clinical_impact': 'moderate'},
            'intervention_recommendations': {'immediate_actions': ['clarification'], 'escalation_threshold': 'standard'},
            'fallback_used': True
        }
    
    def _generate_fallback_test_cases(self, scenario: str, num_cases: int) -> List[AIGeneratedTestCase]:
        """Generate fallback test cases"""
        fallback_cases = []
        
        incomplete_patterns = [
            "I feel...",
            "My chest is...",
            "The pain started when...",
            "Doctor, I'm worried about...",
            "Something's wrong with my..."
        ]
        
        for i in range(min(num_cases, len(incomplete_patterns))):
            test_case = AIGeneratedTestCase(
                id=f"fallback_incomplete_{scenario}_{i+1}",
                pattern_type=LanguagePatternType.INCOMPLETE_SENTENCE,
                input_text=incomplete_patterns[i],
                expected_entities=[{'entity': 'symptom', 'type': 'medical_condition'}],
                expected_intent='symptom_inquiry',
                expected_urgency='medium',
                difficulty_level=TestDifficulty.MEDIUM,
                confidence_score=0.5,
                ai_reasoning="Fallback incomplete sentence pattern",
                success_criteria={'completion_required': True, 'clarification_needed': True},
                emotional_state='concerned'
            )
            fallback_cases.append(test_case)
        
        return fallback_cases
    
    def _update_processing_stats(self, analysis: IncompleteFragmentAnalysis, processing_time: float):
        """Update processing statistics"""
        self.processing_stats['total_fragments_processed'] += 1
        self.processing_stats['confidence_scores'].append(analysis.completion_confidence)
        
        # Update average processing time
        total_processed = self.processing_stats['total_fragments_processed']
        current_avg = self.processing_stats['average_processing_time']
        new_avg = ((current_avg * (total_processed - 1)) + processing_time) / total_processed
        self.processing_stats['average_processing_time'] = new_avg
    
    async def get_processing_statistics(self) -> Dict[str, Any]:
        """Get comprehensive processing statistics"""
        stats = self.processing_stats.copy()
        
        if stats['confidence_scores']:
            stats['average_confidence'] = sum(stats['confidence_scores']) / len(stats['confidence_scores'])
            stats['confidence_range'] = {
                'min': min(stats['confidence_scores']),
                'max': max(stats['confidence_scores'])
            }
        else:
            stats['average_confidence'] = 0.0
            stats['confidence_range'] = {'min': 0.0, 'max': 0.0}
        
        return {
            'algorithm_version': '7.1_ai_incomplete_sentence_processing',
            'processing_statistics': stats,
            'timestamp': datetime.utcnow().isoformat()
        }

# Global instance
ai_incomplete_processor = None

def get_ai_incomplete_processor() -> AIIncompleteSentenceProcessor:
    """Get or create global AI incomplete sentence processor"""
    global ai_incomplete_processor
    
    if ai_incomplete_processor is None:
        ai_incomplete_processor = AIIncompleteSentenceProcessor()
    
    return ai_incomplete_processor

# Convenience functions
async def analyze_medical_fragment(fragment_text: str) -> IncompleteFragmentAnalysis:
    """Quick function to analyze medical fragment"""
    processor = get_ai_incomplete_processor()
    return await processor.analyze_medical_fragments_with_ai(fragment_text)

async def generate_completion_suggestions(incomplete_input: str, context: Dict[str, Any] = None) -> List[AICompletionSuggestion]:
    """Quick function to generate completion suggestions"""
    processor = get_ai_incomplete_processor()
    return await processor.generate_completion_suggestions_with_ai(incomplete_input, context)