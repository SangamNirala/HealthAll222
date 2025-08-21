"""
🎯 INTELLIGENT CONVERSATION ORCHESTRATOR WITH AI-POWERED FLOW MANAGEMENT
=======================================================================

AI-powered conversation flow management system using Gemini for adaptive interactions.
Determines optimal questioning sequences and manages conversation progression with
clinical intelligence and patient engagement optimization.

Algorithm Version: 6.2_intelligent_conversation_orchestration
"""

import os
import asyncio
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import google.generativeai as genai

from gemini_progressive_questioning_engine import (
    AISymptomAnalysis,
    AIGeneratedQuestion,
    AIProgressiveQuestionResult
)

# Configure logger
logger = logging.getLogger(__name__)


@dataclass
class AIQuestionRecommendation:
    """
    🎯 AI-POWERED QUESTION RECOMMENDATION WITH CONVERSATION INTELLIGENCE
    
    Sophisticated recommendation for next optimal question based on conversation analysis
    """
    recommended_question: str
    reasoning: str
    conversation_efficiency_score: float
    patient_engagement_level: str  # high, medium, low
    information_completeness: float  # 0-1 scale
    should_continue_questioning: bool
    should_escalate_to_assessment: bool
    estimated_questions_remaining: int
    conversation_quality_indicators: List[str]


@dataclass
class ConversationProgressAnalysis:
    """
    📊 COMPREHENSIVE CONVERSATION PROGRESS ANALYSIS
    
    AI-powered analysis of conversation effectiveness and progress
    """
    information_gathered: Dict[str, Any]
    information_gaps: List[str]
    conversation_turns: int
    efficiency_score: float  # 0-1 scale
    patient_cooperation_level: str
    medical_completeness: float
    time_to_completion_estimate: float
    conversation_quality_score: float


class IntelligentConversationOrchestrator:
    """
    🧠 AI-POWERED CONVERSATION FLOW MANAGEMENT USING GEMINI FOR ADAPTIVE INTERACTIONS
    
    Advanced conversation orchestration that uses AI to determine the most appropriate 
    next question based on conversation context, medical priorities, and patient engagement.
    """
    
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        gemini_keys_str = os.getenv('GEMINI_API_KEYS', '')
        self.gemini_api_keys = [key.strip() for key in gemini_keys_str.split(',') if key.strip()]
        
        if self.gemini_api_key and self.gemini_api_key not in self.gemini_api_keys:
            self.gemini_api_keys.insert(0, self.gemini_api_key)
        
        if not self.gemini_api_keys:
            raise ValueError("No GEMINI_API_KEY configured for Intelligent Conversation Orchestrator")
            
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
                logger.info(f"Initialized Gemini model for conversation orchestration")
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
    
    async def determine_next_ai_question(self, current_conversation: List[Dict], patient_response: str, medical_objectives: List[str]) -> AIQuestionRecommendation:
        """
        🎯 USE AI TO DETERMINE THE MOST APPROPRIATE NEXT QUESTION BASED ON CONVERSATION FLOW
        
        Analyzes conversation context and determines optimal next questioning approach
        with clinical intelligence and patient engagement optimization.
        """
        
        conversation_analysis_prompt = self._create_conversation_analysis_prompt(
            current_conversation, patient_response, medical_objectives
        )
        
        try:
            response = await self._query_gemini_with_retry(conversation_analysis_prompt)
            recommendation = self._parse_ai_conversation_analysis(response)
            return recommendation
            
        except Exception as e:
            logger.error(f"AI conversation analysis failed: {str(e)}")
            return self._create_fallback_recommendation(current_conversation, patient_response)
    
    def _create_conversation_analysis_prompt(self, current_conversation: List[Dict], patient_response: str, medical_objectives: List[str]) -> str:
        """Create comprehensive prompt for conversation analysis"""
        
        conversation_summary = self._summarize_conversation(current_conversation)
        
        prompt = f"""
You are managing a medical conversation where we're gathering specific information from initially vague symptoms.

Conversation So Far: {conversation_summary}
Latest Patient Response: "{patient_response}"
Medical Information Still Needed: {json.dumps(medical_objectives, indent=2)}

Analyze the conversation and determine the optimal next approach:

Provide your analysis in this JSON format:
{{
    "information_gained": {{
        "new_information": ["list of new medical information from latest response"],
        "confirmed_information": ["list of information confirmed or clarified"],
        "information_quality": "excellent|good|moderate|poor"
    }},
    "information_gaps": ["list of critical information still missing"],
    "patient_engagement": {{
        "cooperation_level": "excellent|good|moderate|poor|resistant",
        "communication_style": "detailed|moderate|minimal|evasive",
        "emotional_state": "calm|anxious|frustrated|cooperative|overwhelmed"
    }},
    "conversation_assessment": {{
        "efficiency_score": 0.0-1.0,
        "turns_used": 0,
        "estimated_completion": "1-2|3-4|5+|ready_for_assessment",
        "quality_indicators": ["list of conversation quality factors"]
    }},
    "next_question_recommendation": {{
        "recommended_question": "specific next question to ask",
        "reasoning": "detailed medical reasoning for this question",
        "question_type": "location|severity|timeline|quality|associated_symptoms|triggers|clarification",
        "priority_level": 1-5,
        "expected_information_gain": 0.0-1.0
    }},
    "conversation_decision": {{
        "should_continue_questioning": true|false,
        "should_escalate_to_assessment": true|false,
        "reasoning": "why continue questioning or move to assessment"
    }},
    "patient_adaptation": {{
        "communication_adjustments": ["how to adapt communication style"],
        "empathy_level": "high|medium|low",
        "question_complexity": "simple|moderate|detailed"
    }}
}}

Key Analysis Requirements:
1. What new medical information was gained from the latest response?
2. What critical information is still missing for proper medical assessment?
3. How is the patient responding to questioning (engaged, overwhelmed, cooperative)?
4. Should we continue progressive questioning or move to medical assessment?
5. What should be the next most important question to ask?
6. How should we adapt our communication style based on patient responses?

Consider these factors:
- Medical completeness and safety
- Patient engagement and cooperation
- Conversation efficiency
- Clinical priorities and urgency
- Communication style adaptation

Provide specific, actionable recommendations with clear medical reasoning.
"""
        
        return prompt
    
    def _summarize_conversation(self, conversation: List[Dict]) -> str:
        """Create a summary of the conversation for analysis"""
        
        if not conversation:
            return "No previous conversation"
        
        summary_parts = []
        for i, turn in enumerate(conversation[-5:], 1):  # Last 5 turns
            role = turn.get('role', 'unknown')
            content = turn.get('content', '')[:100]  # Limit length
            summary_parts.append(f"Turn {i} ({role}): {content}")
        
        return " | ".join(summary_parts)
    
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
    
    def _parse_ai_conversation_analysis(self, gemini_response: str) -> AIQuestionRecommendation:
        """Parse AI response into conversation recommendation"""
        
        try:
            # Extract JSON from response
            json_start = gemini_response.find('{')
            json_end = gemini_response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = gemini_response[json_start:json_end]
                analysis_data = json.loads(json_str)
                
                next_question = analysis_data.get('next_question_recommendation', {})
                conversation_assessment = analysis_data.get('conversation_assessment', {})
                conversation_decision = analysis_data.get('conversation_decision', {})
                patient_engagement = analysis_data.get('patient_engagement', {})
                
                return AIQuestionRecommendation(
                    recommended_question=next_question.get('recommended_question', 'Can you tell me more about your symptoms?'),
                    reasoning=next_question.get('reasoning', 'Continue gathering medical information'),
                    conversation_efficiency_score=float(conversation_assessment.get('efficiency_score', 0.7)),
                    patient_engagement_level=patient_engagement.get('cooperation_level', 'moderate'),
                    information_completeness=float(next_question.get('expected_information_gain', 0.7)),
                    should_continue_questioning=conversation_decision.get('should_continue_questioning', True),
                    should_escalate_to_assessment=conversation_decision.get('should_escalate_to_assessment', False),
                    estimated_questions_remaining=self._estimate_questions_remaining(conversation_assessment.get('estimated_completion', '3-4')),
                    conversation_quality_indicators=conversation_assessment.get('quality_indicators', ['gathering_information'])
                )
                
            else:
                return self._create_simple_fallback_recommendation()
                
        except Exception as e:
            logger.error(f"Failed to parse AI conversation analysis: {str(e)}")
            return self._create_simple_fallback_recommendation()
    
    def _estimate_questions_remaining(self, completion_estimate: str) -> int:
        """Estimate number of questions remaining based on AI assessment"""
        
        if completion_estimate == "ready_for_assessment":
            return 0
        elif completion_estimate == "1-2":
            return 2
        elif completion_estimate == "3-4":
            return 3
        else:  # "5+"
            return 5
    
    def _create_fallback_recommendation(self, conversation: List[Dict], patient_response: str) -> AIQuestionRecommendation:
        """Create fallback recommendation based on simple heuristics"""
        
        # Simple fallback logic
        if not conversation:
            question = "Can you help me understand what specific symptoms you're experiencing?"
        elif len(conversation) < 3:
            question = "Can you tell me more about where you're experiencing these symptoms and what they feel like?"
        else:
            question = "How long have you been experiencing these symptoms, and is there anything that makes them better or worse?"
        
        return AIQuestionRecommendation(
            recommended_question=question,
            reasoning="Fallback recommendation for continued information gathering",
            conversation_efficiency_score=0.6,
            patient_engagement_level="moderate",
            information_completeness=0.5,
            should_continue_questioning=True,
            should_escalate_to_assessment=False,
            estimated_questions_remaining=3,
            conversation_quality_indicators=["fallback_mode"]
        )
    
    def _create_simple_fallback_recommendation(self) -> AIQuestionRecommendation:
        """Create simple fallback when all parsing fails"""
        
        return AIQuestionRecommendation(
            recommended_question="Can you describe your symptoms in more detail?",
            reasoning="Simple fallback for continued assessment",
            conversation_efficiency_score=0.5,
            patient_engagement_level="unknown",
            information_completeness=0.4,
            should_continue_questioning=True,
            should_escalate_to_assessment=False,
            estimated_questions_remaining=4,
            conversation_quality_indicators=["simple_fallback"]
        )
    
    async def analyze_conversation_progress(self, conversation_history: List[Dict], initial_symptom: str) -> ConversationProgressAnalysis:
        """
        📊 ANALYZE CONVERSATION PROGRESS AND EFFECTIVENESS
        
        Comprehensive analysis of how well the conversation is progressing toward
        gathering complete medical information.
        """
        
        progress_prompt = f"""
Analyze the progress of this medical conversation that started with vague symptom: "{initial_symptom}"

Conversation History: {json.dumps(conversation_history[-10:], indent=2)}

Provide comprehensive progress analysis in JSON format:
{{
    "information_gathered": {{
        "symptoms": ["list of specific symptoms identified"],
        "locations": ["anatomical locations identified"],
        "qualities": ["symptom qualities/descriptions"],
        "timeline": ["temporal information gathered"],
        "triggers": ["identified triggers or aggravating factors"],
        "severity": ["severity information obtained"]
    }},
    "information_gaps": ["critical information still missing"],
    "conversation_metrics": {{
        "turns": {len(conversation_history)},
        "efficiency_score": 0.0-1.0,
        "patient_cooperation": "excellent|good|moderate|poor",
        "information_quality": "excellent|good|moderate|poor",
        "medical_completeness": 0.0-1.0
    }},
    "progress_assessment": {{
        "time_to_completion_estimate": "minutes",
        "questions_remaining_estimate": 0-10,
        "conversation_quality_score": 0.0-1.0,
        "readiness_for_medical_assessment": "ready|nearly_ready|more_info_needed"
    }},
    "recommendations": {{
        "continue_current_approach": true|false,
        "adjust_communication_style": "suggestions for improvement",
        "focus_areas": ["what to prioritize in remaining questions"]
    }}
}}
"""
        
        try:
            response = await self._query_gemini_with_retry(progress_prompt)
            return self._parse_progress_analysis(response, conversation_history)
            
        except Exception as e:
            logger.error(f"Progress analysis failed: {str(e)}")
            return self._create_fallback_progress_analysis(conversation_history)
    
    def _parse_progress_analysis(self, gemini_response: str, conversation_history: List[Dict]) -> ConversationProgressAnalysis:
        """Parse progress analysis response"""
        
        try:
            json_start = gemini_response.find('{')
            json_end = gemini_response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = gemini_response[json_start:json_end]
                analysis_data = json.loads(json_str)
                
                info_gathered = analysis_data.get('information_gathered', {})
                metrics = analysis_data.get('conversation_metrics', {})
                progress = analysis_data.get('progress_assessment', {})
                
                return ConversationProgressAnalysis(
                    information_gathered=info_gathered,
                    information_gaps=analysis_data.get('information_gaps', ['more_details_needed']),
                    conversation_turns=len(conversation_history),
                    efficiency_score=float(metrics.get('efficiency_score', 0.6)),
                    patient_cooperation_level=metrics.get('patient_cooperation', 'moderate'),
                    medical_completeness=float(metrics.get('medical_completeness', 0.5)),
                    time_to_completion_estimate=float(progress.get('time_to_completion_estimate', '5')),
                    conversation_quality_score=float(progress.get('conversation_quality_score', 0.6))
                )
                
        except Exception as e:
            logger.error(f"Failed to parse progress analysis: {str(e)}")
            
        return self._create_fallback_progress_analysis(conversation_history)
    
    def _create_fallback_progress_analysis(self, conversation_history: List[Dict]) -> ConversationProgressAnalysis:
        """Create fallback progress analysis"""
        
        return ConversationProgressAnalysis(
            information_gathered={"basic_info": ["symptom_mentioned"]},
            information_gaps=["location", "severity", "timeline", "quality"],
            conversation_turns=len(conversation_history),
            efficiency_score=0.5,
            patient_cooperation_level="moderate",
            medical_completeness=0.3,
            time_to_completion_estimate=5.0,
            conversation_quality_score=0.5
        )


# Global instance for easy access (with graceful error handling)
try:
    intelligent_conversation_orchestrator = IntelligentConversationOrchestrator()
    print("✅ Intelligent Conversation Orchestrator initialized successfully")
except ValueError as e:
    print(f"⚠️ Intelligent Conversation Orchestrator not available: {e}")
    intelligent_conversation_orchestrator = None
except Exception as e:
    print(f"⚠️ Intelligent Conversation Orchestrator initialization failed: {e}")
    intelligent_conversation_orchestrator = None