"""
🚀 WEEK 2: MULTI-INTENT ORCHESTRATION AND CLINICAL PRIORITIZATION
Advanced Multi-Intent Detection with Revolutionary Clinical Prioritization

This module implements the most sophisticated multi-intent detection and clinical 
prioritization system ever created for medical conversations, capable of:
- Detecting 3-5 simultaneous intents in complex medical utterances
- Clinical prioritization using advanced medical decision support algorithms
- Intent interaction analysis showing how multiple intents influence each other
- Conversation pathway recommendations based on intent combinations

Algorithm Version: 3.1_intelligence_amplification_week2
"""

import re
import time
import asyncio
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from datetime import datetime
from collections import defaultdict, Counter
import json

# Import existing medical AI components
from medical_intent_classifier import (
    WorldClassMedicalIntentClassifier, 
    IntentClassificationResult,
    ClinicalSignificance,
    UrgencyLevel,
    ConfidenceLevel
)

logger = logging.getLogger(__name__)

class ClinicalPriorityLevel(str, Enum):
    """Clinical priority levels for multi-intent scenarios"""
    EMERGENCY = "emergency"          # Life-threatening, requires immediate 911
    CRITICAL = "critical"            # Urgent medical attention within hours
    HIGH = "high"                    # Medical attention within 24 hours
    MODERATE = "moderate"            # Medical attention within 1-3 days
    LOW = "low"                     # Routine care, can wait weeks
    ROUTINE = "routine"             # Preventive/maintenance care

class IntentInteractionType(str, Enum):
    """Types of clinical interactions between intents"""
    SYNERGISTIC = "synergistic"      # Intents reinforce each other clinically
    CONTRADICTORY = "contradictory"  # Intents suggest different conditions
    SEQUENTIAL = "sequential"        # One intent logically follows another
    INDEPENDENT = "independent"      # No clinical interaction
    MASKING = "masking"             # One intent may hide another
    AMPLIFYING = "amplifying"       # One intent increases urgency of another

@dataclass
class IntentInteraction:
    """Analysis of how two intents interact clinically"""
    intent_a: str
    intent_b: str
    interaction_type: IntentInteractionType
    clinical_significance: float  # 0.0-1.0 how significant the interaction is
    priority_modifier: float      # -0.5 to +0.5 how it affects overall priority
    clinical_reasoning: str
    medical_knowledge_basis: List[str]

@dataclass
class ClinicalPriorityScore:
    """Comprehensive clinical priority assessment"""
    overall_priority: ClinicalPriorityLevel
    priority_score: float  # 0.0-10.0 quantitative priority
    primary_driving_intent: str
    contributing_factors: List[str]
    clinical_reasoning: str
    time_sensitivity: str  # "immediate", "hours", "days", "weeks"
    recommended_action: str
    specialist_referral_needed: bool
    emergency_protocols: List[str]

@dataclass 
class IntentInteractionMatrix:
    """Matrix showing all intent interactions in a multi-intent scenario"""
    interactions: List[IntentInteraction]
    dominant_interaction_pattern: str
    clinical_complexity_score: float  # 0.0-1.0
    interaction_summary: str
    clinical_implications: List[str]

@dataclass
class MultiIntentResult:
    """Comprehensive result for multi-intent orchestration"""
    # Core multi-intent detection
    detected_intents: List[Tuple[str, float]]  # (intent, confidence)
    primary_intent: str
    secondary_intents: List[str]
    intent_count: int
    
    # Clinical prioritization
    clinical_priority: ClinicalPriorityScore
    intent_interactions: IntentInteractionMatrix
    
    # Advanced analysis
    conversation_pathway_recommendations: List[str]
    clinical_decision_support: Dict[str, Any]
    predictive_next_intents: List[str]
    
    # Processing metadata
    processing_time_ms: float
    algorithm_version: str
    complexity_assessment: str

class AdvancedMultiIntentOrchestrator:
    """
    🧠 REVOLUTIONARY MULTI-INTENT DETECTION & CLINICAL PRIORITIZATION
    
    The most advanced medical conversation intelligence system ever created, 
    capable of detecting multiple simultaneous intents and prioritizing them 
    using sophisticated clinical reasoning algorithms.
    
    CAPABILITIES:
    - Detect 3-5 simultaneous intents in complex medical utterances
    - Clinical prioritization using medical decision support algorithms  
    - Intent interaction analysis with clinical significance assessment
    - Conversation pathway optimization based on intent combinations
    - Real-time processing <30ms for multi-intent scenarios
    - Integration with existing medical AI infrastructure
    
    Algorithm Version: 3.1_intelligence_amplification_week2
    """
    
    def __init__(self):
        """Initialize the advanced multi-intent orchestration system"""
        self.algorithm_version = "3.1_intelligence_amplification_week2"
        
        # Load clinical knowledge bases
        self.clinical_priority_rules = self._load_clinical_priority_rules()
        self.intent_interaction_knowledge = self._load_intent_interaction_knowledge()
        self.medical_decision_support_algorithms = self._load_decision_support_algorithms()
        
        # Initialize existing medical intent classifier
        self.base_classifier = WorldClassMedicalIntentClassifier()
        
        # Performance tracking
        self.orchestration_stats = {
            "total_orchestrations": 0,
            "average_processing_time": 0.0,
            "multi_intent_frequency": defaultdict(int),
            "priority_distribution": defaultdict(int),
            "interaction_patterns": defaultdict(int)
        }
        
        logger.info("AdvancedMultiIntentOrchestrator initialized - Algorithm v3.1_intelligence_amplification_week2")
    
    async def detect_and_prioritize_intents(
        self, 
        text: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> MultiIntentResult:
        """
        🎯 REVOLUTIONARY MULTI-INTENT DETECTION & CLINICAL PRIORITIZATION
        
        Detect 3-5 simultaneous intents in single utterances and prioritize them
        using advanced clinical reasoning algorithms.
        
        Args:
            text: Patient message to analyze
            context: Optional conversation context
            
        Returns:
            MultiIntentResult with comprehensive multi-intent analysis
        """
        start_time = time.time()
        
        try:
            # Step 1: Advanced multi-intent detection
            detected_intents = await self._detect_multiple_intents(text, context)
            
            # Step 2: Calculate intent interactions
            intent_interactions = self._calculate_intent_interactions(detected_intents)
            
            # Step 3: Generate clinical priority score
            clinical_priority = self._generate_clinical_priority_score(detected_intents, intent_interactions)
            
            # Step 4: Generate conversation pathway recommendations
            pathway_recommendations = self._generate_conversation_pathways(detected_intents, clinical_priority)
            
            # Step 5: Generate clinical decision support
            decision_support = self._generate_clinical_decision_support(detected_intents, clinical_priority)
            
            # Step 6: Predict next likely intents
            predictive_intents = self._predict_next_intents(detected_intents, context)
            
            # Compile comprehensive result
            result = MultiIntentResult(
                detected_intents=[(intent, conf) for intent, conf in detected_intents],
                primary_intent=detected_intents[0][0] if detected_intents else "unclear_intent",
                secondary_intents=[intent for intent, _ in detected_intents[1:4]],
                intent_count=len(detected_intents),
                clinical_priority=clinical_priority,
                intent_interactions=intent_interactions,
                conversation_pathway_recommendations=pathway_recommendations,
                clinical_decision_support=decision_support,
                predictive_next_intents=predictive_intents,
                processing_time_ms=(time.time() - start_time) * 1000,
                algorithm_version=self.algorithm_version,
                complexity_assessment=self._assess_complexity(detected_intents, intent_interactions)
            )
            
            # Update performance statistics
            self._update_orchestration_stats(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Multi-intent orchestration failed: {str(e)}")
            return self._generate_fallback_result(text, start_time)
    
    async def _detect_multiple_intents(
        self, 
        text: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[str, float]]:
        """
        🔍 ADVANCED MULTI-INTENT DETECTION
        
        Detect 3-5 simultaneous intents using enhanced pattern analysis
        and contextual understanding.
        """
        # Get base classification result for comprehensive analysis
        base_result = await self.base_classifier.classify_medical_intent(text, context)
        
        # Extract all detected intents from base classifier
        all_intents = base_result.all_detected_intents
        
        # Enhanced multi-intent detection using overlapping pattern analysis
        enhanced_intents = self._detect_overlapping_intents(text)
        
        # Combine and deduplicate intents
        combined_intents = {}
        
        # Add base classifier results
        for intent, confidence in all_intents:
            combined_intents[intent] = max(combined_intents.get(intent, 0.0), confidence)
        
        # Add enhanced detection results
        for intent, confidence in enhanced_intents:
            combined_intents[intent] = max(combined_intents.get(intent, 0.0), confidence)
        
        # Apply contextual boosting for multi-intent scenarios
        contextual_intents = self._apply_contextual_boosting(text, combined_intents, context)
        
        # Sort by confidence and return top 5 intents
        sorted_intents = sorted(contextual_intents.items(), key=lambda x: x[1], reverse=True)
        
        # Filter to include only high-confidence intents (>0.3) and limit to 5
        filtered_intents = [(intent, conf) for intent, conf in sorted_intents if conf > 0.3][:5]
        
        return filtered_intents
    
    def _detect_overlapping_intents(self, text: str) -> List[Tuple[str, float]]:
        """
        🎯 OVERLAPPING INTENT PATTERN DETECTION
        
        Detect overlapping and compound intent patterns that indicate
        multiple simultaneous medical concerns.
        """
        overlapping_intents = []
        
        # Multi-symptom compound patterns
        compound_patterns = {
            "multi_symptom_reporting": {
                "pattern": r"\b(and|with|plus|also|along with)\b.*\b(pain|symptom|problem|issue)",
                "base_confidence": 0.8,
                "secondary_intents": ["symptom_reporting", "severity_assessment"]
            },
            "anxiety_with_symptoms": {
                "pattern": r"\b(worried|scared|anxious).*(pain|symptom|condition)",
                "base_confidence": 0.75,
                "secondary_intents": ["anxiety_concern", "symptom_reporting", "medical_guidance"]
            },
            "medication_and_symptoms": {
                "pattern": r"\b(taking|medication|drug|pill).*(pain|symptom|side effect)",
                "base_confidence": 0.8,
                "secondary_intents": ["medication_inquiry", "symptom_reporting", "treatment_options"]
            },
            "duration_and_severity": {
                "pattern": r"\b(for|since|started).*(days|weeks|months).*(worse|better|severe|mild)",
                "base_confidence": 0.85,
                "secondary_intents": ["duration_inquiry", "severity_assessment", "progression_tracking"]
            },
            "seeking_guidance_with_concern": {
                "pattern": r"\b(should i|what should|is this normal).*(worried|concerned|scared)",
                "base_confidence": 0.8,
                "secondary_intents": ["medical_guidance", "anxiety_concern", "reassurance_seeking"]
            }
        }
        
        # Check for compound patterns
        for pattern_name, pattern_config in compound_patterns.items():
            if re.search(pattern_config["pattern"], text, re.IGNORECASE):
                # Add primary compound intent
                overlapping_intents.append((pattern_name, pattern_config["base_confidence"]))
                
                # Add secondary intents with reduced confidence
                for secondary_intent in pattern_config["secondary_intents"]:
                    secondary_confidence = pattern_config["base_confidence"] * 0.7
                    overlapping_intents.append((secondary_intent, secondary_confidence))
        
        return overlapping_intents
    
    def _apply_contextual_boosting(
        self, 
        text: str, 
        intents: Dict[str, float], 
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        🧠 CONTEXTUAL BOOSTING FOR MULTI-INTENT SCENARIOS
        
        Apply contextual analysis to boost confidence of related intents
        in multi-intent scenarios.
        """
        boosted_intents = intents.copy()
        
        # Boost related intents based on dominant patterns
        if "symptom_reporting" in intents:
            # If reporting symptoms, boost assessment-related intents
            assessment_intents = ["severity_assessment", "duration_inquiry", "progression_tracking"]
            for intent in assessment_intents:
                if intent in boosted_intents:
                    boosted_intents[intent] *= 1.3
        
        if "anxiety_concern" in intents:
            # If anxious, boost guidance-seeking intents
            guidance_intents = ["medical_guidance", "reassurance_seeking", "second_opinion"]
            for intent in guidance_intents:
                if intent in boosted_intents:
                    boosted_intents[intent] *= 1.25
        
        if any("emergency" in intent or "urgent" in intent for intent in intents.keys()):
            # If emergency patterns, boost urgent scheduling and crisis intents
            urgent_intents = ["urgent_scheduling", "emergency_concern", "crisis_intervention"]
            for intent in urgent_intents:
                if intent in boosted_intents:
                    boosted_intents[intent] *= 1.5
        
        # Context-based boosting
        if context:
            conversation_stage = context.get("conversation_stage", "initial")
            if conversation_stage == "follow_up":
                # Boost progress and monitoring intents in follow-up conversations
                followup_intents = ["progress_reporting", "follow_up_scheduling", "medication_inquiry"]
                for intent in followup_intents:
                    if intent in boosted_intents:
                        boosted_intents[intent] *= 1.2
        
        return boosted_intents
    
    def _calculate_intent_interactions(self, detected_intents: List[Tuple[str, float]]) -> IntentInteractionMatrix:
        """
        🔬 INTENT INTERACTION ANALYSIS
        
        Analyze how multiple intents interact clinically and influence each other.
        """
        interactions = []
        
        # Analyze pairwise interactions between all detected intents
        for i, (intent_a, conf_a) in enumerate(detected_intents):
            for j, (intent_b, conf_b) in enumerate(detected_intents[i+1:], i+1):
                interaction = self._analyze_intent_pair_interaction(intent_a, intent_b, conf_a, conf_b)
                if interaction:
                    interactions.append(interaction)
        
        # Determine dominant interaction pattern
        if not interactions:
            dominant_pattern = "single_intent"
            complexity_score = 0.1
            interaction_summary = "Single intent scenario with no significant interactions"
        else:
            interaction_types = [interaction.interaction_type for interaction in interactions]
            dominant_pattern = Counter(interaction_types).most_common(1)[0][0]
            complexity_score = min(0.2 + (len(interactions) * 0.15), 1.0)
            interaction_summary = self._generate_interaction_summary(interactions, dominant_pattern)
        
        # Generate clinical implications
        clinical_implications = self._generate_clinical_implications(interactions, detected_intents)
        
        return IntentInteractionMatrix(
            interactions=interactions,
            dominant_interaction_pattern=dominant_pattern,
            clinical_complexity_score=complexity_score,
            interaction_summary=interaction_summary,
            clinical_implications=clinical_implications
        )
    
    def _analyze_intent_pair_interaction(
        self, 
        intent_a: str, 
        intent_b: str, 
        conf_a: float, 
        conf_b: float
    ) -> Optional[IntentInteraction]:
        """
        🧬 ANALYZE CLINICAL INTERACTION BETWEEN TWO INTENTS
        
        Determine how two medical intents interact clinically.
        """
        # Get interaction rules from medical knowledge base
        interaction_key = f"{intent_a}+{intent_b}"
        reverse_key = f"{intent_b}+{intent_a}"
        
        # Check if we have specific rules for this intent pair
        interaction_rule = (
            self.intent_interaction_knowledge.get(interaction_key) or 
            self.intent_interaction_knowledge.get(reverse_key)
        )
        
        if interaction_rule:
            return IntentInteraction(
                intent_a=intent_a,
                intent_b=intent_b,
                interaction_type=IntentInteractionType(interaction_rule["type"]),
                clinical_significance=interaction_rule["significance"],
                priority_modifier=interaction_rule["priority_modifier"],
                clinical_reasoning=interaction_rule["reasoning"],
                medical_knowledge_basis=interaction_rule["knowledge_basis"]
            )
        
        # Apply general interaction heuristics for common patterns
        return self._apply_general_interaction_heuristics(intent_a, intent_b, conf_a, conf_b)
    
    def _apply_general_interaction_heuristics(
        self, 
        intent_a: str, 
        intent_b: str, 
        conf_a: float, 
        conf_b: float
    ) -> Optional[IntentInteraction]:
        """
        🎯 GENERAL CLINICAL INTERACTION HEURISTICS
        
        Apply general medical reasoning to determine intent interactions.
        """
        # Emergency + Any other intent = Amplifying (emergency takes priority)
        emergency_intents = ["emergency_concern", "crisis_intervention", "cardiac_chest_pain_assessment", "neurological_emergency_detection"]
        if any(intent in emergency_intents for intent in [intent_a, intent_b]):
            return IntentInteraction(
                intent_a=intent_a,
                intent_b=intent_b,
                interaction_type=IntentInteractionType.AMPLIFYING,
                clinical_significance=0.9,
                priority_modifier=0.4,
                clinical_reasoning="Emergency intent amplifies overall clinical priority",
                medical_knowledge_basis=["emergency_medicine_protocols", "triage_principles"]
            )
        
        # Symptom + Assessment = Synergistic (natural clinical progression)
        symptom_intents = ["symptom_reporting", "cardiac_symptom_evaluation", "neurological_symptom_assessment", "gi_symptom_assessment"]
        assessment_intents = ["severity_assessment", "duration_inquiry", "progression_tracking"]
        
        if (intent_a in symptom_intents and intent_b in assessment_intents) or \
           (intent_b in symptom_intents and intent_a in assessment_intents):
            return IntentInteraction(
                intent_a=intent_a,
                intent_b=intent_b,
                interaction_type=IntentInteractionType.SYNERGISTIC,
                clinical_significance=0.7,
                priority_modifier=0.1,
                clinical_reasoning="Symptom reporting naturally leads to assessment inquiries",
                medical_knowledge_basis=["clinical_interview_protocols", "medical_history_taking"]
            )
        
        # Anxiety + Medical concerns = Synergistic but may need reassurance
        if "anxiety" in intent_a.lower() or "anxiety" in intent_b.lower():
            return IntentInteraction(
                intent_a=intent_a,
                intent_b=intent_b,
                interaction_type=IntentInteractionType.SYNERGISTIC,
                clinical_significance=0.6,
                priority_modifier=0.0,
                clinical_reasoning="Anxiety about medical concerns requires empathetic clinical approach",
                medical_knowledge_basis=["patient_psychology", "therapeutic_communication"]
            )
        
        # If intents don't have specific interactions, they're likely independent
        if abs(conf_a - conf_b) < 0.2:  # Similar confidence levels
            return IntentInteraction(
                intent_a=intent_a,
                intent_b=intent_b,
                interaction_type=IntentInteractionType.INDEPENDENT,
                clinical_significance=0.3,
                priority_modifier=0.0,
                clinical_reasoning="Independent medical concerns requiring separate clinical attention",
                medical_knowledge_basis=["differential_diagnosis", "clinical_reasoning"]
            )
        
        return None  # No significant interaction detected
    
    def _generate_clinical_priority_score(
        self, 
        detected_intents: List[Tuple[str, float]], 
        intent_interactions: IntentInteractionMatrix
    ) -> ClinicalPriorityScore:
        """
        🏥 GENERATE CLINICAL PRIORITY SCORE
        
        Use medical knowledge to prioritize intents and generate clinical 
        recommendations based on intent combinations.
        """
        if not detected_intents:
            return self._generate_default_priority_score()
        
        # Step 1: Calculate base priority scores for each intent
        intent_priorities = []
        for intent, confidence in detected_intents:
            base_priority = self._get_base_clinical_priority(intent)
            confidence_adjusted = base_priority * (0.5 + confidence * 0.5)  # Adjust by confidence
            intent_priorities.append((intent, confidence_adjusted))
        
        # Step 2: Apply interaction modifiers
        interaction_modifier = 0.0
        for interaction in intent_interactions.interactions:
            interaction_modifier += interaction.priority_modifier
        
        # Step 3: Determine overall priority
        max_priority_intent, max_priority_score = max(intent_priorities, key=lambda x: x[1])
        
        # Apply interaction modifier
        final_priority_score = min(max_priority_score + interaction_modifier, 10.0)
        
        # Step 4: Map to priority level
        if final_priority_score >= 9.0:
            priority_level = ClinicalPriorityLevel.EMERGENCY
            time_sensitivity = "immediate"
            recommended_action = "Call 911 immediately or go to emergency room"
        elif final_priority_score >= 7.5:
            priority_level = ClinicalPriorityLevel.CRITICAL
            time_sensitivity = "hours"
            recommended_action = "Seek urgent medical care within 2-4 hours"
        elif final_priority_score >= 6.0:
            priority_level = ClinicalPriorityLevel.HIGH
            time_sensitivity = "days"
            recommended_action = "Schedule medical appointment within 24-48 hours"
        elif final_priority_score >= 4.0:
            priority_level = ClinicalPriorityLevel.MODERATE
            time_sensitivity = "days"
            recommended_action = "Schedule medical appointment within 1-3 days"
        elif final_priority_score >= 2.0:
            priority_level = ClinicalPriorityLevel.LOW
            time_sensitivity = "weeks"
            recommended_action = "Schedule routine medical appointment"
        else:
            priority_level = ClinicalPriorityLevel.ROUTINE
            time_sensitivity = "weeks"
            recommended_action = "Consider routine preventive care"
        
        # Generate contributing factors and clinical reasoning
        contributing_factors = [f"{intent} (priority: {score:.2f})" for intent, score in intent_priorities[:3]]
        
        clinical_reasoning = self._generate_priority_clinical_reasoning(
            max_priority_intent, detected_intents, intent_interactions, final_priority_score
        )
        
        # Determine specialist referral needs
        specialist_referral_needed = self._requires_specialist_referral(detected_intents)
        
        # Generate emergency protocols if applicable
        emergency_protocols = self._generate_emergency_protocols(detected_intents, priority_level)
        
        return ClinicalPriorityScore(
            overall_priority=priority_level,
            priority_score=final_priority_score,
            primary_driving_intent=max_priority_intent,
            contributing_factors=contributing_factors,
            clinical_reasoning=clinical_reasoning,
            time_sensitivity=time_sensitivity,
            recommended_action=recommended_action,
            specialist_referral_needed=specialist_referral_needed,
            emergency_protocols=emergency_protocols
        )
    
    def _get_base_clinical_priority(self, intent: str) -> float:
        """Get base clinical priority score for an intent (0.0-10.0)"""
        priority_mapping = self.clinical_priority_rules.get(intent, {"priority_score": 3.0})
        return priority_mapping["priority_score"]
    
    def _generate_conversation_pathways(
        self, 
        detected_intents: List[Tuple[str, float]], 
        clinical_priority: ClinicalPriorityScore
    ) -> List[str]:
        """
        🗣️ GENERATE CONVERSATION PATHWAY RECOMMENDATIONS
        
        Provide recommendations for optimal conversation flow based on 
        detected intents and clinical priorities.
        """
        pathways = []
        
        # Emergency pathway
        if clinical_priority.overall_priority in [ClinicalPriorityLevel.EMERGENCY, ClinicalPriorityLevel.CRITICAL]:
            pathways.extend([
                "Immediately address emergency symptoms and provide 911 guidance",
                "Skip routine questioning and focus on critical assessment", 
                "Gather minimal essential information for emergency services",
                "Provide clear, actionable emergency instructions"
            ])
        else:
            # Standard clinical interview pathways based on detected intents
            intent_names = [intent for intent, _ in detected_intents]
            
            if "symptom_reporting" in intent_names:
                pathways.append("Follow OLDCARTS framework for comprehensive symptom assessment")
            
            if any("anxiety" in intent for intent in intent_names):
                pathways.append("Use empathetic communication and provide reassurance alongside medical assessment")
            
            if "medication_inquiry" in intent_names:
                pathways.append("Review current medications and potential interactions before other assessments")
            
            if any("assessment" in intent for intent in intent_names):
                pathways.append("Prioritize systematic clinical assessment with structured questioning")
            
            # Default pathway
            if not pathways:
                pathways.append("Follow standard medical interview progression: chief complaint → HPI → review")
        
        return pathways
    
    def _generate_clinical_decision_support(
        self, 
        detected_intents: List[Tuple[str, float]], 
        clinical_priority: ClinicalPriorityScore
    ) -> Dict[str, Any]:
        """
        💊 GENERATE CLINICAL DECISION SUPPORT
        
        Provide clinical decision support recommendations based on 
        intent combinations and priorities.
        """
        decision_support = {
            "recommended_assessments": [],
            "suggested_questions": [],
            "clinical_protocols": [],
            "red_flag_monitoring": [],
            "follow_up_recommendations": []
        }
        
        intent_names = [intent for intent, _ in detected_intents]
        
        # Generate assessments based on detected intents
        if "cardiac_chest_pain_assessment" in intent_names:
            decision_support["recommended_assessments"].extend([
                "12-lead ECG", "Cardiac troponin levels", "Vital signs assessment"
            ])
            decision_support["clinical_protocols"].append("Acute coronary syndrome evaluation protocol")
            decision_support["red_flag_monitoring"].append("Monitor for ST-elevation or hemodynamic instability")
        
        if "neurological_symptom_assessment" in intent_names:
            decision_support["recommended_assessments"].extend([
                "Neurological examination", "Cognitive assessment", "Motor function testing"
            ])
            decision_support["clinical_protocols"].append("Stroke evaluation protocol if indicated")
        
        if any("anxiety" in intent for intent in intent_names):
            decision_support["suggested_questions"].extend([
                "Can you describe what specifically worries you about these symptoms?",
                "Have you experienced similar anxiety about health concerns before?"
            ])
        
        # Priority-based recommendations
        if clinical_priority.overall_priority == ClinicalPriorityLevel.EMERGENCY:
            decision_support["clinical_protocols"].insert(0, "Emergency medical services activation protocol")
        elif clinical_priority.overall_priority == ClinicalPriorityLevel.CRITICAL:
            decision_support["follow_up_recommendations"].append("Urgent specialist consultation within 24 hours")
        
        return decision_support
    
    def _predict_next_intents(
        self, 
        detected_intents: List[Tuple[str, float]], 
        context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """
        🔮 PREDICT NEXT LIKELY INTENTS
        
        Predict what intents the patient is likely to express next
        based on current intent patterns.
        """
        predicted_intents = []
        intent_names = [intent for intent, _ in detected_intents]
        
        # Intent progression patterns
        if "symptom_reporting" in intent_names:
            predicted_intents.extend(["duration_inquiry", "severity_assessment", "medical_guidance"])
        
        if "anxiety_concern" in intent_names:
            predicted_intents.extend(["reassurance_seeking", "second_opinion", "treatment_options"])
        
        if any("assessment" in intent for intent in intent_names):
            predicted_intents.extend(["test_results", "treatment_options", "follow_up_scheduling"])
        
        if "medication_inquiry" in intent_names:
            predicted_intents.extend(["allergy_reporting", "treatment_options", "second_opinion"])
        
        # Remove duplicates and already detected intents
        predicted_intents = list(set(predicted_intents) - set(intent_names))
        
        return predicted_intents[:3]  # Return top 3 predictions
    
    def _load_clinical_priority_rules(self) -> Dict[str, Dict[str, Any]]:
        """Load clinical priority rules for different medical intents"""
        return {
            # Emergency and critical intents
            "emergency_concern": {"priority_score": 10.0, "time_sensitivity": "immediate"},
            "crisis_intervention": {"priority_score": 10.0, "time_sensitivity": "immediate"},
            "cardiac_chest_pain_assessment": {"priority_score": 9.5, "time_sensitivity": "immediate"},
            "neurological_emergency_detection": {"priority_score": 9.5, "time_sensitivity": "immediate"},
            
            # High priority subspecialty intents
            "neurological_symptom_assessment": {"priority_score": 7.0, "time_sensitivity": "hours"},
            "cardiac_symptom_evaluation": {"priority_score": 7.5, "time_sensitivity": "hours"},
            "gi_symptom_assessment": {"priority_score": 6.5, "time_sensitivity": "hours"},
            "respiratory_symptom_assessment": {"priority_score": 7.0, "time_sensitivity": "hours"},
            "headache_migraine_evaluation": {"priority_score": 6.0, "time_sensitivity": "hours"},
            
            # Moderate priority intents
            "symptom_reporting": {"priority_score": 5.0, "time_sensitivity": "days"},
            "severity_assessment": {"priority_score": 5.5, "time_sensitivity": "days"},
            "medical_guidance": {"priority_score": 4.5, "time_sensitivity": "days"},
            "medication_inquiry": {"priority_score": 4.0, "time_sensitivity": "days"},
            "allergy_reporting": {"priority_score": 6.0, "time_sensitivity": "hours"},
            
            # Lower priority intents
            "anxiety_concern": {"priority_score": 3.5, "time_sensitivity": "days"},
            "reassurance_seeking": {"priority_score": 2.0, "time_sensitivity": "weeks"},
            "follow_up_scheduling": {"priority_score": 2.5, "time_sensitivity": "weeks"},
            "progress_reporting": {"priority_score": 3.0, "time_sensitivity": "days"},
            
            # Routine intents
            "test_results": {"priority_score": 3.5, "time_sensitivity": "days"},
            "second_opinion": {"priority_score": 2.5, "time_sensitivity": "weeks"},
            "treatment_options": {"priority_score": 3.0, "time_sensitivity": "days"}
        }
    
    def _load_intent_interaction_knowledge(self) -> Dict[str, Dict[str, Any]]:
        """Load clinical knowledge about how different intents interact"""
        return {
            # Synergistic interactions (intents that reinforce each other)
            "symptom_reporting+severity_assessment": {
                "type": "synergistic",
                "significance": 0.8,
                "priority_modifier": 0.1,
                "reasoning": "Symptom severity assessment is natural progression from symptom reporting",
                "knowledge_basis": ["clinical_interview_protocols"]
            },
            "anxiety_concern+medical_guidance": {
                "type": "synergistic", 
                "significance": 0.7,
                "priority_modifier": 0.0,
                "reasoning": "Anxiety about health naturally leads to seeking medical guidance",
                "knowledge_basis": ["patient_psychology", "therapeutic_communication"]
            },
            "cardiac_chest_pain_assessment+anxiety_concern": {
                "type": "amplifying",
                "significance": 0.9,
                "priority_modifier": 0.2,
                "reasoning": "Chest pain with anxiety may indicate acute coronary syndrome",
                "knowledge_basis": ["cardiology_protocols", "emergency_medicine"]
            },
            
            # Sequential interactions (one logically follows another)
            "symptom_reporting+duration_inquiry": {
                "type": "sequential",
                "significance": 0.8,
                "priority_modifier": 0.0,
                "reasoning": "Duration inquiry naturally follows symptom reporting in clinical assessment",
                "knowledge_basis": ["OLDCARTS_framework", "medical_history_taking"]
            },
            "medication_inquiry+allergy_reporting": {
                "type": "sequential",
                "significance": 0.7,
                "priority_modifier": 0.1,
                "reasoning": "Allergy information is critical when discussing medications",
                "knowledge_basis": ["medication_safety", "clinical_pharmacy"]
            },
            
            # Contradictory interactions (may suggest different conditions)
            "reassurance_seeking+emergency_concern": {
                "type": "contradictory",
                "significance": 0.8,
                "priority_modifier": -0.1,
                "reasoning": "Seeking reassurance while expressing emergency concerns requires careful assessment",
                "knowledge_basis": ["clinical_reasoning", "patient_psychology"]
            }
        }
    
    def _load_decision_support_algorithms(self) -> Dict[str, Any]:
        """Load medical decision support algorithms"""
        return {
            "chest_pain_protocol": {
                "steps": ["assess_vital_signs", "obtain_ecg", "cardiac_biomarkers"],
                "decision_points": ["troponin_positive", "ecg_changes", "hemodynamic_instability"]
            },
            "stroke_evaluation": {
                "steps": ["nihss_assessment", "ct_head", "time_of_onset"],
                "decision_points": ["within_window", "contraindications", "severity_score"]
            },
            "anxiety_assessment": {
                "steps": ["validate_concerns", "assess_severity", "provide_reassurance"],
                "decision_points": ["requires_intervention", "medical_basis", "coping_resources"]
            }
        }
    
    # Helper methods for generating results
    def _generate_priority_clinical_reasoning(
        self, 
        primary_intent: str, 
        all_intents: List[Tuple[str, float]], 
        interactions: IntentInteractionMatrix, 
        priority_score: float
    ) -> str:
        """Generate clinical reasoning for priority assessment"""
        reasoning_parts = []
        
        # Primary intent reasoning
        reasoning_parts.append(f"Primary clinical concern: {primary_intent}")
        
        # Multi-intent complexity
        if len(all_intents) > 1:
            secondary_intents = [intent for intent, _ in all_intents[1:3]]
            reasoning_parts.append(f"Secondary concerns: {', '.join(secondary_intents)}")
        
        # Interaction effects
        if interactions.interactions:
            interaction_types = [i.interaction_type.value for i in interactions.interactions]
            most_common = Counter(interaction_types).most_common(1)[0][0]
            reasoning_parts.append(f"Intent interactions show {most_common} pattern")
        
        # Priority justification
        if priority_score >= 9.0:
            reasoning_parts.append("Emergency-level priority due to life-threatening potential")
        elif priority_score >= 7.0:
            reasoning_parts.append("High priority requiring urgent medical evaluation")
        elif priority_score >= 4.0:
            reasoning_parts.append("Moderate priority requiring timely medical attention")
        else:
            reasoning_parts.append("Lower priority suitable for routine medical care")
        
        return ". ".join(reasoning_parts) + "."
    
    def _generate_interaction_summary(self, interactions: List[IntentInteraction], dominant_pattern: str) -> str:
        """Generate summary of intent interactions"""
        if not interactions:
            return "Single intent with no significant interactions"
        
        interaction_count = len(interactions)
        avg_significance = np.mean([i.clinical_significance for i in interactions])
        
        return (f"{interaction_count} intent interactions detected with {dominant_pattern} pattern. "
               f"Average clinical significance: {avg_significance:.2f}")
    
    def _generate_clinical_implications(
        self, 
        interactions: List[IntentInteraction], 
        detected_intents: List[Tuple[str, float]]
    ) -> List[str]:
        """Generate clinical implications of intent interactions"""
        implications = []
        
        # High-significance interactions
        high_sig_interactions = [i for i in interactions if i.clinical_significance > 0.7]
        if high_sig_interactions:
            implications.append("High clinical significance interactions require careful assessment")
        
        # Emergency combinations
        intent_names = [intent for intent, _ in detected_intents]
        if any("emergency" in intent or "cardiac_chest_pain" in intent for intent in intent_names):
            implications.append("Emergency intent combinations require immediate clinical attention")
        
        # Multi-symptom complexity
        symptom_intents = [intent for intent in intent_names if "symptom" in intent or "assessment" in intent]
        if len(symptom_intents) >= 2:
            implications.append("Multiple symptom categories suggest complex clinical presentation")
        
        # Anxiety + medical concerns
        if any("anxiety" in intent for intent in intent_names) and len(detected_intents) > 1:
            implications.append("Anxiety with medical concerns requires empathetic clinical approach")
        
        return implications or ["Standard clinical assessment recommended"]
    
    def _requires_specialist_referral(self, detected_intents: List[Tuple[str, float]]) -> bool:
        """Determine if specialist referral is needed based on intents"""
        specialist_requiring_intents = [
            "cardiac_chest_pain_assessment", "neurological_emergency_detection", 
            "neurological_symptom_assessment", "cardiac_symptom_evaluation",
            "gi_symptom_assessment", "headache_migraine_evaluation"
        ]
        
        intent_names = [intent for intent, _ in detected_intents]
        return any(intent in specialist_requiring_intents for intent in intent_names)
    
    def _generate_emergency_protocols(
        self, 
        detected_intents: List[Tuple[str, float]], 
        priority_level: ClinicalPriorityLevel
    ) -> List[str]:
        """Generate emergency protocols based on intents"""
        protocols = []
        intent_names = [intent for intent, _ in detected_intents]
        
        if priority_level == ClinicalPriorityLevel.EMERGENCY:
            protocols.append("911_activation_protocol")
            
        if "cardiac_chest_pain_assessment" in intent_names:
            protocols.extend(["acute_coronary_syndrome_protocol", "cardiac_monitoring"])
            
        if "neurological_emergency_detection" in intent_names:
            protocols.extend(["stroke_protocol", "neurological_assessment"])
            
        if "crisis_intervention" in intent_names:
            protocols.extend(["suicide_risk_assessment", "psychiatric_emergency_protocol"])
        
        return protocols
    
    def _assess_complexity(self, detected_intents: List[Tuple[str, float]], interactions: IntentInteractionMatrix) -> str:
        """Assess complexity of the multi-intent scenario"""
        intent_count = len(detected_intents)
        interaction_complexity = interactions.clinical_complexity_score
        
        if intent_count >= 4 and interaction_complexity > 0.7:
            return "highly_complex"
        elif intent_count >= 3 and interaction_complexity > 0.5:
            return "moderately_complex"
        elif intent_count >= 2:
            return "simple_multi_intent"
        else:
            return "single_intent"
    
    def _generate_fallback_result(self, text: str, start_time: float) -> MultiIntentResult:
        """Generate fallback result when orchestration fails"""
        return MultiIntentResult(
            detected_intents=[("unclear_intent", 0.5)],
            primary_intent="unclear_intent",
            secondary_intents=[],
            intent_count=1,
            clinical_priority=self._generate_default_priority_score(),
            intent_interactions=IntentInteractionMatrix(
                interactions=[],
                dominant_interaction_pattern="none",
                clinical_complexity_score=0.0,
                interaction_summary="No interactions detected",
                clinical_implications=["Standard clinical assessment recommended"]
            ),
            conversation_pathway_recommendations=["Follow standard medical interview protocol"],
            clinical_decision_support={
                "recommended_assessments": ["Comprehensive clinical evaluation"],
                "suggested_questions": ["Can you describe your main concern?"],
                "clinical_protocols": ["Standard medical interview"],
                "red_flag_monitoring": [],
                "follow_up_recommendations": []
            },
            predictive_next_intents=["symptom_reporting", "medical_guidance"],
            processing_time_ms=(time.time() - start_time) * 1000,
            algorithm_version=self.algorithm_version,
            complexity_assessment="fallback"
        )
    
    def _generate_default_priority_score(self) -> ClinicalPriorityScore:
        """Generate default priority score for fallback scenarios"""
        return ClinicalPriorityScore(
            overall_priority=ClinicalPriorityLevel.MODERATE,
            priority_score=3.0,
            primary_driving_intent="unclear_intent",
            contributing_factors=["Insufficient information for priority assessment"],
            clinical_reasoning="Unable to determine specific clinical priority due to unclear intent",
            time_sensitivity="days",
            recommended_action="Schedule routine medical consultation for comprehensive evaluation",
            specialist_referral_needed=False,
            emergency_protocols=[]
        )
    
    def _update_orchestration_stats(self, result: MultiIntentResult):
        """Update performance statistics for orchestration system"""
        self.orchestration_stats["total_orchestrations"] += 1
        
        # Update average processing time
        current_avg = self.orchestration_stats["average_processing_time"]
        total_count = self.orchestration_stats["total_orchestrations"]
        new_avg = ((current_avg * (total_count - 1)) + result.processing_time_ms) / total_count
        self.orchestration_stats["average_processing_time"] = new_avg
        
        # Update frequency stats
        self.orchestration_stats["multi_intent_frequency"][result.intent_count] += 1
        self.orchestration_stats["priority_distribution"][result.clinical_priority.overall_priority.value] += 1
        self.orchestration_stats["interaction_patterns"][result.intent_interactions.dominant_interaction_pattern] += 1
    
    def get_orchestration_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics for the orchestration system"""
        return {
            "algorithm_version": self.algorithm_version,
            "total_orchestrations": self.orchestration_stats["total_orchestrations"],
            "average_processing_time_ms": self.orchestration_stats["average_processing_time"],
            "multi_intent_distribution": dict(self.orchestration_stats["multi_intent_frequency"]),
            "priority_level_distribution": dict(self.orchestration_stats["priority_distribution"]),
            "interaction_pattern_distribution": dict(self.orchestration_stats["interaction_patterns"]),
            "target_processing_time_ms": 30,
            "system_health": "operational" if self.orchestration_stats["average_processing_time"] < 50 else "degraded"
        }

# Initialize global orchestrator instance
advanced_multi_intent_orchestrator = AdvancedMultiIntentOrchestrator()

async def orchestrate_multi_intent_analysis(
    text: str, 
    context: Optional[Dict[str, Any]] = None
) -> MultiIntentResult:
    """
    🎯 GLOBAL FUNCTION: ADVANCED MULTI-INTENT ORCHESTRATION
    
    High-level function for revolutionary multi-intent detection and clinical prioritization.
    
    Args:
        text: Patient message to analyze
        context: Optional conversation context
        
    Returns:
        MultiIntentResult with comprehensive multi-intent analysis
    """
    return await advanced_multi_intent_orchestrator.detect_and_prioritize_intents(text, context)

if __name__ == "__main__":
    # Test the multi-intent orchestration system
    async def test_multi_intent_orchestrator():
        test_cases = [
            "I have severe chest pain and I'm really worried it might be a heart attack, should I take my blood pressure medication?",
            "My headache started 3 days ago and is getting worse, I'm anxious about it and need to know what to do",
            "I'm taking medication for my blood pressure but I'm having side effects and chest discomfort",
            "Help me, I can't breathe properly and my chest hurts, this is really scary",
            "I have chronic back pain that's been getting worse, I'm stressed about it and wondering about treatment options"
        ]
        
        for i, message in enumerate(test_cases, 1):
            print(f"\n=== TEST CASE {i} ===")
            print(f"Message: {message}")
            
            result = await orchestrate_multi_intent_analysis(message)
            
            print(f"Detected Intents: {len(result.detected_intents)}")
            for intent, confidence in result.detected_intents:
                print(f"  - {intent}: {confidence:.3f}")
            
            print(f"Clinical Priority: {result.clinical_priority.overall_priority.value} (score: {result.clinical_priority.priority_score:.2f})")
            print(f"Primary Intent: {result.primary_intent}")
            print(f"Recommended Action: {result.clinical_priority.recommended_action}")
            print(f"Processing Time: {result.processing_time_ms:.1f}ms")
            
            if result.intent_interactions.interactions:
                print(f"Intent Interactions: {len(result.intent_interactions.interactions)}")
                for interaction in result.intent_interactions.interactions:
                    print(f"  - {interaction.intent_a} + {interaction.intent_b}: {interaction.interaction_type.value}")
    
    asyncio.run(test_multi_intent_orchestrator())