"""
🚀 STEP 6.2: COMPREHENSIVE AI-POWERED PROGRESSIVE QUESTIONING SERVICE
===================================================================

Main service orchestrator for the revolutionary AI-powered progressive questioning system.
Integrates all AI components and provides seamless integration with existing Task 6.1 system.

This service coordinates:
1. AI-powered symptom analysis using Gemini LLM
2. Dynamic question generation with medical reasoning  
3. Intelligent conversation orchestration
4. Integration with existing medical AI infrastructure

Algorithm Version: 6.2_comprehensive_ai_progressive_questioning_service
"""

import asyncio
import time
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

# Import AI-powered components
from gemini_progressive_questioning_engine import (
    LLMSymptomAnalyzer,
    AIQuestionGenerator, 
    AISymptomAnalysis,
    AIGeneratedQuestion,
    AIProgressiveQuestionResult,
    llm_symptom_analyzer,
    ai_question_generator
)

from intelligent_conversation_orchestrator import (
    IntelligentConversationOrchestrator,
    AIQuestionRecommendation,
    ConversationProgressAnalysis,
    intelligent_conversation_orchestrator
)

# Import existing Task 6.1 components for integration
from intelligent_clarification_system import (
    IntelligentClarificationEngine,
    ClarificationAnalysisResult,
    UnclearInputType,
    analyze_and_clarify_unclear_input,
    generate_clarification_response
)

# Configure logger
logger = logging.getLogger(__name__)


@dataclass
class EnhancedClarificationWithAI:
    """
    🔗 ENHANCED CLARIFICATION SYSTEM WITH AI-POWERED PROGRESSIVE QUESTIONING
    
    Seamless integration of Task 6.1 clarification system with new AI-powered
    progressive questioning capabilities for unlimited scalability.
    """
    pass


class AIProgressiveQuestioningService:
    """
    🎯 COMPREHENSIVE AI-POWERED PROGRESSIVE QUESTIONING SERVICE
    
    Main orchestration service that coordinates all AI components to deliver
    revolutionary progressive questioning capabilities with seamless integration.
    """
    
    def __init__(self):
        # Initialize AI-powered components with error handling
        self.llm_symptom_analyzer = llm_symptom_analyzer
        self.ai_question_generator = ai_question_generator
        self.conversation_orchestrator = intelligent_conversation_orchestrator
        
        # Check if AI components are available
        self.ai_components_available = (
            self.llm_symptom_analyzer is not None and 
            self.ai_question_generator is not None and
            self.conversation_orchestrator is not None
        )
        
        if not self.ai_components_available:
            logger.warning("AI Progressive Questioning components not fully available - will use fallback mode")
        
        # Initialize existing Task 6.1 components for integration
        self.intelligent_clarification_engine = None
        try:
            from intelligent_clarification_system import intelligent_clarification_engine
            self.intelligent_clarification_engine = intelligent_clarification_engine
        except:
            logger.warning("Could not load existing clarification engine")
        
        logger.info("AI Progressive Questioning Service initialized successfully")
    
    async def process_unclear_input_with_ai_progression(self, patient_input: str, medical_context: Dict[str, Any] = None, conversation_history: List[Dict] = None) -> AIProgressiveQuestionResult:
        """
        🚀 MAIN AI-POWERED PROGRESSIVE QUESTIONING WORKFLOW
        
        Integrated workflow:
        1. Use Task 6.1 system for initial unclear input detection
        2. If unclear input detected, use AI for progressive questioning
        3. Generate AI-powered questions using Gemini
        4. Track conversation progression with AI analysis
        5. Seamlessly transition to normal medical consultation when sufficient specificity achieved
        """
        
        start_time = time.time()
        
        try:
            # Check if AI components are available
            if not self.ai_components_available:
                logger.warning("AI components not available, returning fallback result")
                return self._create_fallback_result(patient_input, medical_context, start_time)
            
            # Step 1: Use existing Task 6.1 system for initial analysis
            clarification_result = None
            if self.intelligent_clarification_engine:
                try:
                    clarification_result = await self.intelligent_clarification_engine.analyze_unclear_input(
                        patient_input, medical_context
                    )
                    logger.info(f"Task 6.1 analysis completed: confidence={clarification_result.confidence_score}")
                except Exception as e:
                    logger.warning(f"Task 6.1 analysis failed, proceeding with AI-only: {str(e)}")
            
            # Step 2: AI-powered symptom analysis using Gemini
            ai_symptom_analysis = await self.llm_symptom_analyzer.analyze_vague_symptom_with_ai(
                patient_input, medical_context
            )
            
            # Step 3: Determine if AI progressive questioning should be used
            should_use_ai_questioning = self._should_use_ai_progressive_questioning(
                ai_symptom_analysis, clarification_result, conversation_history
            )
            
            if should_use_ai_questioning:
                # Step 4: Generate AI-powered progressive questions
                patient_profile = self._extract_patient_profile(medical_context, conversation_history)
                conversation_state = self._prepare_conversation_state(conversation_history)
                
                ai_questions = await self.ai_question_generator.generate_progressive_questions_with_ai(
                    ai_symptom_analysis, conversation_state, patient_profile
                )
                
                # Step 5: Determine conversation strategy
                conversation_strategy = await self._determine_conversation_strategy(
                    ai_symptom_analysis, ai_questions, conversation_history
                )
                
                # Step 6: Create comprehensive result
                total_processing_time = (time.time() - start_time) * 1000
                
                result = AIProgressiveQuestionResult(
                    symptom_analysis=ai_symptom_analysis,
                    generated_questions=ai_questions,
                    conversation_strategy=conversation_strategy,
                    recommended_next_action=self._determine_next_action(ai_symptom_analysis, ai_questions),
                    should_escalate=ai_symptom_analysis.clinical_priority == "emergency",
                    escalation_reason=f"Emergency priority detected: {ai_symptom_analysis.ai_reasoning}" if ai_symptom_analysis.clinical_priority == "emergency" else None,
                    conversation_efficiency_score=self._calculate_efficiency_score(ai_symptom_analysis, ai_questions),
                    total_processing_time_ms=total_processing_time
                )
                
                logger.info(f"AI progressive questioning completed: {len(ai_questions)} questions generated in {total_processing_time:.2f}ms")
                return result
            
            else:
                # Use traditional Task 6.1 approach for simpler cases
                return await self._handle_traditional_clarification(
                    patient_input, medical_context, clarification_result, start_time
                )
                
        except Exception as e:
            logger.error(f"AI progressive questioning failed: {str(e)}")
            return await self._handle_fallback_questioning(patient_input, medical_context, start_time)
    
    def _should_use_ai_progressive_questioning(self, ai_analysis: AISymptomAnalysis, clarification_result: ClarificationAnalysisResult = None, conversation_history: List[Dict] = None) -> bool:
        """
        🤔 DETERMINE WHETHER TO USE AI PROGRESSIVE QUESTIONING
        
        Decision logic based on:
        1. Complexity of vague input
        2. AI confidence scores
        3. Conversation history
        4. Clinical priority
        """
        
        # Always use AI for mandatory examples
        mandatory_examples = ["sick", "pain", "bad"]
        if any(example in ai_analysis.original_input.lower() for example in mandatory_examples):
            return True
        
        # Use AI for complex vague expressions
        if ai_analysis.confidence_score < 0.6:
            return True
        
        # Use AI for high priority cases
        if ai_analysis.clinical_priority in ["emergency", "urgent"]:
            return True
        
        # Use AI for complex medical domains
        if len(ai_analysis.medical_domains) > 1:
            return True
        
        # Use AI for multiple missing information types
        if len(ai_analysis.missing_information) > 2:
            return True
        
        # Use AI if Task 6.1 confidence is low
        if clarification_result and clarification_result.confidence_score < 0.7:
            return True
        
        # Use AI for ongoing conversations with multiple turns
        if conversation_history and len(conversation_history) > 2:
            return True
        
        # Default to AI for comprehensive analysis
        return True
    
    def _extract_patient_profile(self, medical_context: Dict[str, Any] = None, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """Extract patient communication profile for question adaptation"""
        
        profile = {
            "communication_style": "balanced",
            "emotional_state": "neutral",
            "medical_literacy": "general",
            "response_length": "moderate"
        }
        
        if conversation_history:
            # Analyze conversation patterns
            patient_responses = [turn.get('content', '') for turn in conversation_history if turn.get('role') == 'patient']
            
            if patient_responses:
                avg_length = sum(len(response.split()) for response in patient_responses) / len(patient_responses)
                
                if avg_length < 3:
                    profile["response_length"] = "minimal"
                    profile["communication_style"] = "brief"
                elif avg_length > 15:
                    profile["response_length"] = "detailed"
                    profile["communication_style"] = "expressive"
                
                # Check for emotional indicators
                emotional_words = ["scared", "worried", "anxious", "frustrated", "concerned"]
                if any(word in ' '.join(patient_responses).lower() for word in emotional_words):
                    profile["emotional_state"] = "distressed"
        
        if medical_context:
            # Extract additional context
            if medical_context.get('age'):
                age = medical_context['age']
                if age < 30:
                    profile["communication_style"] = "informal"
                elif age > 65:
                    profile["communication_style"] = "formal"
        
        return profile
    
    def _prepare_conversation_state(self, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """Prepare conversation state for AI analysis"""
        
        state = {
            "turn_count": 0,
            "information_gathered": [],
            "patient_responses": [],
            "question_types_used": [],
            "conversation_flow": "initial"
        }
        
        if conversation_history:
            state["turn_count"] = len(conversation_history)
            state["patient_responses"] = [turn.get('content', '') for turn in conversation_history if turn.get('role') == 'patient']
            
            if state["turn_count"] > 5:
                state["conversation_flow"] = "extended"
            elif state["turn_count"] > 2:
                state["conversation_flow"] = "developing"
        
        return state
    
    async def _determine_conversation_strategy(self, ai_analysis: AISymptomAnalysis, ai_questions: List[AIGeneratedQuestion], conversation_history: List[Dict] = None) -> str:
        """Determine optimal conversation strategy"""
        
        # Emergency cases require immediate escalation strategy
        if ai_analysis.clinical_priority == "emergency":
            return "immediate_escalation_with_safety_questions"
        
        # High confidence symptoms with clear questions
        if ai_analysis.confidence_score > 0.8 and ai_questions:
            return "direct_progressive_questioning"
        
        # Multiple medical domains require systematic exploration
        if len(ai_analysis.medical_domains) > 1:
            return "systematic_domain_exploration"
        
        # Complex vague expressions need gentle exploration
        if ai_analysis.vagueness_type in ["emotional_vague", "functional_vague"]:
            return "empathetic_exploration"
        
        # Default comprehensive strategy
        return "comprehensive_progressive_questioning"
    
    def _determine_next_action(self, ai_analysis: AISymptomAnalysis, ai_questions: List[AIGeneratedQuestion]) -> str:
        """Determine recommended next action"""
        
        if ai_analysis.clinical_priority == "emergency":
            return "escalate_to_emergency_assessment"
        
        if not ai_questions:
            return "fallback_to_general_medical_assessment"
        
        primary_question = ai_questions[0] if ai_questions else None
        if primary_question and primary_question.clinical_priority <= 2:
            return "ask_high_priority_progressive_question"
        
        return "continue_progressive_questioning"
    
    def _calculate_efficiency_score(self, ai_analysis: AISymptomAnalysis, ai_questions: List[AIGeneratedQuestion]) -> float:
        """Calculate conversation efficiency score"""
        
        base_score = ai_analysis.confidence_score
        
        # Boost for high-quality questions
        if ai_questions:
            avg_question_confidence = sum(q.confidence_score for q in ai_questions) / len(ai_questions)
            base_score = (base_score + avg_question_confidence) / 2
        
        # Boost for clear clinical priority
        if ai_analysis.clinical_priority in ["emergency", "urgent"]:
            base_score = min(1.0, base_score + 0.1)
        
        # Adjust for missing information complexity
        if len(ai_analysis.missing_information) > 3:
            base_score = max(0.3, base_score - 0.1)
        
        return base_score
    
    async def _handle_traditional_clarification(self, patient_input: str, medical_context: Dict[str, Any], start_time: float, clarification_result: ClarificationAnalysisResult = None) -> AIProgressiveQuestionResult:
        """Handle cases using traditional Task 6.1 approach with AI enhancement"""
        
        if not clarification_result and self.intelligent_clarification_engine:
            clarification_result = await self.intelligent_clarification_engine.analyze_unclear_input(
                patient_input, medical_context
            )
        
        # Convert Task 6.1 result to AI format for consistency
        ai_analysis = AISymptomAnalysis(
            original_input=patient_input,
            vagueness_type=clarification_result.input_type.value if clarification_result else "general_vague",
            missing_information=clarification_result.missing_critical_info if clarification_result else ["specific_symptoms"],
            clinical_priority=clarification_result.clarification_priority if clarification_result else "routine",
            medical_domains=["general_medicine"],
            urgency_indicators=clarification_result.urgency_indicators if clarification_result else [],
            patient_communication_style=clarification_result.patient_communication_style if clarification_result else "balanced",
            confidence_score=clarification_result.confidence_score if clarification_result else 0.6,
            ai_reasoning="Traditional Task 6.1 analysis with AI enhancement",
            processing_time_ms=0.0,
            gemini_model_used="task_6.1_integration"
        )
        
        # Create simple question from Task 6.1
        ai_questions = []
        if clarification_result and clarification_result.suggested_questions:
            for i, question_text in enumerate(clarification_result.suggested_questions[:3]):
                ai_questions.append(
                    AIGeneratedQuestion(
                        question_text=question_text,
                        medical_reasoning="Generated by Task 6.1 intelligent clarification system",
                        expected_information_type="symptoms",
                        clinical_priority=i + 1,
                        empathy_level="medium",
                        follow_up_strategy="Continue medical assessment",
                        confidence_score=clarification_result.confidence_score,
                        question_category="clarification",
                        estimated_information_gain=0.7
                    )
                )
        
        total_processing_time = (time.time() - start_time) * 1000
        
        return AIProgressiveQuestionResult(
            symptom_analysis=ai_analysis,
            generated_questions=ai_questions,
            conversation_strategy="traditional_clarification_enhanced",
            recommended_next_action="continue_traditional_assessment",
            should_escalate=False,
            escalation_reason=None,
            conversation_efficiency_score=ai_analysis.confidence_score,
            total_processing_time_ms=total_processing_time
        )
    
    async def _handle_fallback_questioning(self, patient_input: str, medical_context: Dict[str, Any], start_time: float) -> AIProgressiveQuestionResult:
        """Handle fallback when all AI processing fails"""
        
        # Create minimal analysis
        ai_analysis = AISymptomAnalysis(
            original_input=patient_input,
            vagueness_type="general_vague",
            missing_information=["specific_symptoms", "location", "severity"],
            clinical_priority="routine",
            medical_domains=["general_medicine"],
            urgency_indicators=[],
            patient_communication_style="unknown",
            confidence_score=0.5,
            ai_reasoning="Fallback analysis due to AI processing error",
            processing_time_ms=0.0,
            gemini_model_used="fallback"
        )
        
        # Create basic fallback questions
        ai_questions = [
            AIGeneratedQuestion(
                question_text="I want to make sure I understand your health concerns properly. Can you help me by describing any specific symptoms you're experiencing?",
                medical_reasoning="Basic symptom clarification",
                expected_information_type="symptoms",
                clinical_priority=1,
                empathy_level="high",
                follow_up_strategy="Continue assessment",
                confidence_score=0.8,
                question_category="fallback",
                estimated_information_gain=0.7
            )
        ]
        
        total_processing_time = (time.time() - start_time) * 1000
        
        return AIProgressiveQuestionResult(
            symptom_analysis=ai_analysis,
            generated_questions=ai_questions,
            conversation_strategy="fallback_questioning",
            recommended_next_action="continue_basic_assessment",
            should_escalate=False,
            escalation_reason=None,
            conversation_efficiency_score=0.5,
            total_processing_time_ms=total_processing_time
        )
    
    async def optimize_conversation_with_ai(self, conversation_history: List[Dict], patient_response: str, medical_objectives: List[str]) -> AIQuestionRecommendation:
        """
        🎯 AI-POWERED CONVERSATION FLOW OPTIMIZATION
        
        Uses Gemini to analyze conversation effectiveness and recommend optimal next steps
        for gathering specific medical information from vague initial symptoms.
        """
        
        try:
            recommendation = await self.conversation_orchestrator.determine_next_ai_question(
                conversation_history, patient_response, medical_objectives
            )
            return recommendation
            
        except Exception as e:
            logger.error(f"Conversation optimization failed: {str(e)}")
            return AIQuestionRecommendation(
                recommended_question="Can you tell me more about your symptoms?",
                reasoning="Fallback recommendation for continued assessment",
                conversation_efficiency_score=0.5,
                patient_engagement_level="unknown",
                information_completeness=0.4,
                should_continue_questioning=True,
                should_escalate_to_assessment=False,
                estimated_questions_remaining=3,
                conversation_quality_indicators=["fallback_mode"]
            )
    
    async def analyze_conversation_progress(self, conversation_history: List[Dict], initial_symptom: str) -> ConversationProgressAnalysis:
        """
        📊 COMPREHENSIVE CONVERSATION PROGRESS ANALYSIS
        
        Analyze conversation effectiveness and progress toward complete medical information
        """
        
        try:
            progress_analysis = await self.conversation_orchestrator.analyze_conversation_progress(
                conversation_history, initial_symptom
            )
            return progress_analysis
            
        except Exception as e:
            logger.error(f"Progress analysis failed: {str(e)}")
            return ConversationProgressAnalysis(
                information_gathered={"basic_info": ["symptom_mentioned"]},
                information_gaps=["location", "severity", "timeline"],
                conversation_turns=len(conversation_history),
                efficiency_score=0.5,
                patient_cooperation_level="unknown",
                medical_completeness=0.3,
                time_to_completion_estimate=5.0,
                conversation_quality_score=0.5
            )
    
    def _create_fallback_result(self, patient_input: str, medical_context: Dict[str, Any], start_time: float) -> AIProgressiveQuestionResult:
        """
        Create a fallback result when AI components are not available
        """
        from gemini_progressive_questioning_engine import AISymptomAnalysis, AIGeneratedQuestion, AIProgressiveQuestionResult
        
        # Create basic symptom analysis
        fallback_symptom_analysis = AISymptomAnalysis(
            vagueness_type="general_vague",
            missing_information=["location", "severity", "duration"],
            clinical_priority="medium",
            medical_domains=["general"],
            confidence_score=0.5,
            ai_reasoning="Fallback analysis - AI components not available",
            patient_communication_style="standard"
        )
        
        # Create basic question
        fallback_question = AIGeneratedQuestion(
            question_text="Can you tell me more specifically about what you're experiencing?",
            medical_reasoning="Basic clarification needed for proper assessment",
            clinical_priority="medium",
            empathy_level="moderate",
            question_category="clarification",
            confidence_score=0.6
        )
        
        total_processing_time = (time.time() - start_time) * 1000
        
        return AIProgressiveQuestionResult(
            symptom_analysis=fallback_symptom_analysis,
            generated_questions=[fallback_question],
            conversation_strategy="fallback_clarification",
            should_escalate=False,
            escalation_reason="",
            conversation_efficiency_score=0.5,
            total_processing_time_ms=total_processing_time
        )


# Global service instance
ai_progressive_questioning_service = AIProgressiveQuestioningService()


# Main API functions for easy integration
async def analyze_with_ai_progressive_questioning(patient_input: str, medical_context: Dict[str, Any] = None, conversation_history: List[Dict] = None) -> AIProgressiveQuestionResult:
    """
    🚀 MAIN API FUNCTION: AI-POWERED PROGRESSIVE QUESTIONING ANALYSIS
    
    Analyzes ANY vague medical expression and generates contextually appropriate
    progressive questions without being limited to predefined patterns.
    """
    return await ai_progressive_questioning_service.process_unclear_input_with_ai_progression(
        patient_input, medical_context, conversation_history
    )


async def generate_ai_powered_progressive_question(symptom_analysis: AISymptomAnalysis, conversation_state: Dict[str, Any] = None, patient_profile: Dict[str, Any] = None) -> List[AIGeneratedQuestion]:
    """
    🧠 GENERATE NEXT PROGRESSIVE QUESTION USING AI ANALYSIS
    
    Leverages Gemini LLM to determine the most appropriate next question based on
    conversation context, medical priorities, and patient communication style.
    """
    return await ai_progressive_questioning_service.ai_question_generator.generate_progressive_questions_with_ai(
        symptom_analysis, conversation_state, patient_profile
    )


async def optimize_conversation_with_ai(conversation_history: List[Dict], patient_response: str, medical_objectives: List[str]) -> AIQuestionRecommendation:
    """
    🎯 AI-POWERED CONVERSATION FLOW OPTIMIZATION
    
    Uses Gemini to analyze conversation effectiveness and recommend optimal next steps
    for gathering specific medical information from vague initial symptoms.
    """
    return await ai_progressive_questioning_service.optimize_conversation_with_ai(
        conversation_history, patient_response, medical_objectives
    )