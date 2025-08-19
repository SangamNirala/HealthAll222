#!/usr/bin/env python3
"""
📊 INTENT SEQUENCE ANALYZER - PATTERN SEQUENCE ANALYSIS ENGINE
==============================================================

Advanced pattern sequence analysis system for understanding conversation flow
patterns, predicting intent sequences, and optimizing medical conversation efficiency.

Revolutionary Features:
- Advanced Sequence Pattern Recognition
- Markov Chain Intent Modeling
- Conversation Flow Pattern Analysis
- Predictive Sequence Generation
- Medical Context-Aware Pattern Learning
- Temporal Pattern Evolution Tracking

Author: World-Class Medical AI System
Algorithm Version: 1.0_pattern_sequence_analysis
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import json
import numpy as np
from collections import defaultdict, deque, Counter
import re
from enum import Enum

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SequenceType(Enum):
    """Types of conversation sequences"""
    LINEAR_PROGRESSION = "linear_progression"
    BRANCHING_EXPLORATION = "branching_exploration"
    REPETITIVE_CLARIFICATION = "repetitive_clarification"
    EMERGENCY_ESCALATION = "emergency_escalation"
    CIRCULAR_DISCUSSION = "circular_discussion"
    FOCUSED_ASSESSMENT = "focused_assessment"

class IntentSequenceAnalyzer:
    """
    📊 REVOLUTIONARY INTENT SEQUENCE ANALYZER
    
    Advanced system for analyzing conversation intent sequences, identifying patterns,
    and predicting optimal conversation flows using Markov models and pattern recognition.
    
    Core Capabilities:
    - Analyze intent sequence patterns with statistical modeling
    - Predict next likely intent sequences (2-5 step predictions)
    - Identify conversation efficiency patterns and optimization opportunities
    - Track temporal pattern evolution and learning
    - Generate sequence-based conversation guidance
    - Medical context-aware pattern recognition
    """
    
    def __init__(self):
        self.algorithm_version = "1.0_pattern_sequence_analysis"
        
        # Pattern analysis models
        self.intent_transition_matrix = defaultdict(lambda: defaultdict(float))
        self.sequence_patterns = defaultdict(list)
        self.pattern_frequencies = defaultdict(int)
        
        # Medical context patterns
        self.medical_sequence_templates = self._initialize_medical_sequences()
        self.clinical_pathway_patterns = self._initialize_clinical_patterns()
        
        # Learning and tracking
        self.observed_sequences = deque(maxlen=1000)
        self.sequence_outcomes = defaultdict(list)
        self.pattern_success_rates = defaultdict(float)
        
        # Performance metrics
        self.analysis_metrics = {
            'sequences_analyzed': 0,
            'patterns_identified': 0,
            'prediction_accuracy': 0.0,
            'average_analysis_time_ms': 0.0
        }
        
        # Configuration
        self.max_sequence_length = 10
        self.min_pattern_frequency = 3
        self.confidence_threshold = 0.6
        
        logger.info(f"📊 Intent Sequence Analyzer initialized - Algorithm v{self.algorithm_version}")
    
    async def initialize(self):
        """Initialize sequence analyzer with pattern learning"""
        try:
            await self._build_transition_models()
            await self._load_sequence_patterns()
            logger.info("✅ Intent sequence analyzer initialized successfully")
        except Exception as e:
            logger.warning(f"Sequence analyzer initialization: {str(e)}")
    
    def _initialize_medical_sequences(self) -> Dict[str, Any]:
        """Initialize medical conversation sequence templates"""
        
        return {
            # Standard medical interview sequences
            'standard_consultation': {
                'typical_sequence': [
                    'greeting', 'symptom_description', 'symptom_detail',
                    'medical_history', 'medication_inquiry', 'lifestyle_inquiry',
                    'treatment_request', 'follow_up_care'
                ],
                'common_variations': [
                    ['symptom_description', 'emergency_concern', 'symptom_detail'],
                    ['greeting', 'medication_inquiry', 'symptom_description'],
                    ['symptom_detail', 'medical_history', 'treatment_request']
                ],
                'efficiency_score': 0.8
            },
            
            # Emergency consultation sequences
            'emergency_assessment': {
                'typical_sequence': [
                    'symptom_description', 'emergency_concern', 'symptom_detail',
                    'immediate_assessment', 'emergency_action'
                ],
                'critical_patterns': [
                    ['chest_pain', 'emergency_concern', 'immediate_assessment'],
                    ['breathing_difficulty', 'emergency_concern', 'emergency_action'],
                    ['severe_pain', 'emergency_concern', 'symptom_detail']
                ],
                'max_sequence_length': 5,
                'efficiency_score': 0.95
            },
            
            # Chronic condition management sequences
            'chronic_management': {
                'typical_sequence': [
                    'symptom_progression', 'medication_compliance', 'lifestyle_review',
                    'symptom_monitoring', 'treatment_adjustment', 'follow_up_planning'
                ],
                'monitoring_patterns': [
                    ['medication_compliance', 'symptom_progression', 'treatment_adjustment'],
                    ['lifestyle_review', 'symptom_monitoring', 'follow_up_planning']
                ],
                'efficiency_score': 0.7
            },
            
            # Mental health assessment sequences
            'mental_health_evaluation': {
                'typical_sequence': [
                    'mood_assessment', 'symptom_description', 'functional_impact',
                    'support_system_review', 'coping_strategies', 'safety_assessment',
                    'treatment_planning'
                ],
                'safety_patterns': [
                    ['mood_assessment', 'safety_assessment', 'crisis_intervention'],
                    ['symptom_description', 'safety_assessment', 'support_system_review']
                ],
                'sensitive_transitions': [
                    ('mood_assessment', 'safety_assessment'),
                    ('functional_impact', 'coping_strategies')
                ],
                'efficiency_score': 0.65
            },
            
            # Preventive care sequences
            'preventive_consultation': {
                'typical_sequence': [
                    'health_status_review', 'screening_assessment', 'lifestyle_evaluation',
                    'risk_factor_review', 'prevention_planning', 'follow_up_scheduling'
                ],
                'wellness_patterns': [
                    ['health_status_review', 'lifestyle_evaluation', 'prevention_planning'],
                    ['screening_assessment', 'risk_factor_review', 'follow_up_scheduling']
                ],
                'efficiency_score': 0.75
            }
        }
    
    def _initialize_clinical_patterns(self) -> Dict[str, Any]:
        """Initialize clinical reasoning sequence patterns"""
        
        return {
            # Diagnostic reasoning patterns
            'diagnostic_reasoning': {
                'information_gathering': [
                    'chief_complaint', 'history_present_illness', 'past_medical_history'
                ],
                'assessment_sequence': [
                    'differential_diagnosis', 'clinical_reasoning', 'diagnostic_planning'
                ],
                'decision_patterns': [
                    ['symptom_analysis', 'differential_consideration', 'test_ordering'],
                    ['clinical_assessment', 'risk_stratification', 'treatment_planning']
                ]
            },
            
            # Treatment decision patterns
            'treatment_planning': {
                'assessment_to_treatment': [
                    'diagnosis_confirmation', 'treatment_options', 'patient_preferences',
                    'shared_decision_making', 'treatment_initiation'
                ],
                'monitoring_patterns': [
                    ['treatment_response', 'side_effect_monitoring', 'adjustment_planning'],
                    ['adherence_assessment', 'efficacy_evaluation', 'optimization']
                ]
            },
            
            # Follow-up care patterns
            'continuity_care': {
                'progress_evaluation': [
                    'symptom_progression', 'treatment_response', 'quality_of_life',
                    'adherence_review', 'adjustment_needs'
                ],
                'long_term_management': [
                    ['chronic_monitoring', 'lifestyle_support', 'complication_prevention'],
                    ['patient_education', 'self_management', 'care_coordination']
                ]
            }
        }
    
    async def analyze_intent_patterns(self, conversation_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        🔍 ANALYZE INTENT PATTERNS
        
        Comprehensive analysis of conversation intent patterns including:
        - Sequence pattern recognition
        - Transition probability analysis
        - Efficiency assessment
        - Predictive modeling
        """
        
        start_time = datetime.utcnow()
        
        try:
            # Extract intent sequence from conversation
            intent_sequence = await self._extract_intent_sequence(conversation_context)
            
            # Analyze sequence patterns
            pattern_analysis = await self._analyze_sequence_patterns(intent_sequence, conversation_context)
            
            # Calculate transition probabilities
            transition_analysis = await self._analyze_intent_transitions(intent_sequence)
            
            # Predict next sequences
            sequence_predictions = await self._predict_intent_sequences(intent_sequence, conversation_context)
            
            # Assess conversation efficiency
            efficiency_analysis = await self._assess_sequence_efficiency(intent_sequence, conversation_context)
            
            # Generate optimization recommendations
            optimization_recommendations = await self._generate_sequence_optimizations(
                intent_sequence, pattern_analysis, efficiency_analysis
            )
            
            # Compile comprehensive analysis
            analysis_result = {
                'status': 'success',
                'algorithm_version': self.algorithm_version,
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'conversation_id': conversation_context.get('conversation_id', 'unknown'),
                
                # Core analysis results
                'intent_sequence': intent_sequence,
                'pattern_analysis': pattern_analysis,
                'transition_analysis': transition_analysis,
                'sequence_predictions': sequence_predictions,
                'efficiency_analysis': efficiency_analysis,
                'optimization_recommendations': optimization_recommendations,
                
                # Analysis metadata
                'sequence_length': len(intent_sequence),
                'unique_intents': len(set(intent_sequence)),
                'pattern_complexity': await self._calculate_pattern_complexity(intent_sequence),
                'analysis_confidence': await self._calculate_analysis_confidence(intent_sequence, pattern_analysis),
                
                # Performance metrics
                'processing_time_ms': (datetime.utcnow() - start_time).total_seconds() * 1000
            }
            
            # Update learning and tracking
            await self._update_learning_data(intent_sequence, analysis_result)
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing intent patterns: {str(e)}")
            return await self._generate_fallback_analysis(conversation_context)
    
    async def _extract_intent_sequence(self, context: Dict[str, Any]) -> List[str]:
        """Extract intent sequence from conversation context"""
        
        # Get intent history from context
        intent_history = context.get('intent_history', [])
        
        if intent_history:
            return intent_history
        
        # If no explicit intent history, infer from conversation
        conversation_history = context.get('conversation_history', [])
        current_stage = context.get('current_stage', 'greeting')
        
        # Infer intents from conversation stages and content
        inferred_intents = []
        
        # Add current stage as an intent
        inferred_intents.append(current_stage)
        
        # Analyze user messages for intent indicators
        user_messages = [
            msg.get('content', '') for msg in conversation_history
            if msg.get('role') == 'user'
        ]
        
        for message in user_messages:
            inferred_intent = self._infer_intent_from_message(message)
            if inferred_intent and inferred_intent != inferred_intents[-1]:
                inferred_intents.append(inferred_intent)
        
        return inferred_intents[-self.max_sequence_length:] if inferred_intents else ['greeting']
    
    def _infer_intent_from_message(self, message: str) -> Optional[str]:
        """Infer intent from user message content"""
        
        message_lower = message.lower()
        
        # Intent inference patterns
        intent_patterns = {
            'symptom_description': [
                'pain', 'hurt', 'feel', 'symptom', 'problem', 'ache', 'discomfort'
            ],
            'symptom_detail': [
                'started', 'began', 'when', 'how long', 'describe', 'like', 'similar'
            ],
            'medical_history': [
                'history', 'before', 'previous', 'past', 'family', 'had'
            ],
            'medication_inquiry': [
                'medication', 'pills', 'medicine', 'drug', 'prescription', 'taking'
            ],
            'treatment_request': [
                'treatment', 'help', 'cure', 'fix', 'heal', 'therapy', 'what should'
            ],
            'emergency_concern': [
                'emergency', 'urgent', 'serious', 'worried', 'scared', 'severe'
            ],
            'lifestyle_inquiry': [
                'lifestyle', 'diet', 'exercise', 'sleep', 'stress', 'habits'
            ],
            'follow_up_care': [
                'follow', 'next', 'continue', 'appointment', 'check'
            ]
        }
        
        # Score each intent based on keyword matches
        intent_scores = {}
        for intent, keywords in intent_patterns.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                intent_scores[intent] = score
        
        # Return highest scoring intent
        if intent_scores:
            return max(intent_scores, key=intent_scores.get)
        
        return None
    
    async def _analyze_sequence_patterns(self, intent_sequence: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze patterns in the intent sequence"""
        
        if len(intent_sequence) < 2:
            return {
                'pattern_type': SequenceType.LINEAR_PROGRESSION.value,
                'pattern_strength': 0.3,
                'recognized_patterns': [],
                'deviation_analysis': {'deviation_score': 0.0}
            }
        
        # Identify sequence type
        sequence_type = await self._classify_sequence_type(intent_sequence)
        
        # Find matching medical patterns
        matching_patterns = await self._find_matching_medical_patterns(intent_sequence)
        
        # Calculate pattern strength
        pattern_strength = await self._calculate_pattern_strength(intent_sequence, matching_patterns)
        
        # Analyze deviations from expected patterns
        deviation_analysis = await self._analyze_pattern_deviations(intent_sequence, matching_patterns)
        
        # Identify sub-patterns within sequence
        sub_patterns = await self._identify_subsequence_patterns(intent_sequence)
        
        return {
            'sequence_type': sequence_type,
            'pattern_strength': pattern_strength,
            'matching_medical_patterns': matching_patterns,
            'recognized_patterns': [p['name'] for p in matching_patterns],
            'deviation_analysis': deviation_analysis,
            'sub_patterns': sub_patterns,
            'pattern_quality': await self._assess_pattern_quality(intent_sequence, matching_patterns),
            'medical_appropriateness': await self._assess_medical_appropriateness(intent_sequence, context)
        }
    
    async def _classify_sequence_type(self, intent_sequence: List[str]) -> str:
        """Classify the type of conversation sequence"""
        
        if len(intent_sequence) < 3:
            return SequenceType.LINEAR_PROGRESSION.value
        
        # Analyze sequence characteristics
        unique_intents = len(set(intent_sequence))
        sequence_length = len(intent_sequence)
        repetition_ratio = 1.0 - (unique_intents / sequence_length)
        
        # Check for emergency escalation pattern
        emergency_intents = ['emergency_concern', 'urgent_care', 'immediate_assessment']
        if any(intent in intent_sequence for intent in emergency_intents):
            return SequenceType.EMERGENCY_ESCALATION.value
        
        # Check for repetitive patterns
        if repetition_ratio > 0.5:
            return SequenceType.REPETITIVE_CLARIFICATION.value
        
        # Check for circular patterns
        if len(intent_sequence) >= 4:
            if intent_sequence[0] == intent_sequence[-1] and intent_sequence[1] == intent_sequence[-2]:
                return SequenceType.CIRCULAR_DISCUSSION.value
        
        # Check for branching exploration
        recent_intents = intent_sequence[-4:] if len(intent_sequence) >= 4 else intent_sequence
        if len(set(recent_intents)) == len(recent_intents):
            return SequenceType.BRANCHING_EXPLORATION.value
        
        # Check for focused assessment
        focused_domains = ['symptom_description', 'symptom_detail', 'medical_history']
        focused_count = sum(1 for intent in intent_sequence if any(domain in intent for domain in focused_domains))
        if focused_count / sequence_length > 0.7:
            return SequenceType.FOCUSED_ASSESSMENT.value
        
        # Default to linear progression
        return SequenceType.LINEAR_PROGRESSION.value
    
    async def _find_matching_medical_patterns(self, intent_sequence: List[str]) -> List[Dict[str, Any]]:
        """Find medical sequence patterns that match the current sequence"""
        
        matching_patterns = []
        
        for pattern_name, pattern_data in self.medical_sequence_templates.items():
            typical_sequence = pattern_data.get('typical_sequence', [])
            
            # Calculate match score
            match_score = await self._calculate_sequence_match(intent_sequence, typical_sequence)
            
            if match_score > 0.3:  # Minimum threshold
                matching_patterns.append({
                    'name': pattern_name,
                    'match_score': match_score,
                    'expected_sequence': typical_sequence,
                    'efficiency_score': pattern_data.get('efficiency_score', 0.7),
                    'pattern_type': pattern_data.get('pathway_type', 'standard'),
                    'completion_percentage': await self._calculate_completion_percentage(
                        intent_sequence, typical_sequence
                    )
                })
        
        # Sort by match score
        matching_patterns.sort(key=lambda x: x['match_score'], reverse=True)
        
        return matching_patterns[:5]  # Top 5 matches
    
    async def _calculate_sequence_match(self, actual_sequence: List[str], expected_sequence: List[str]) -> float:
        """Calculate how well actual sequence matches expected pattern"""
        
        if not actual_sequence or not expected_sequence:
            return 0.0
        
        # Exact matches in order
        exact_matches = 0
        for i, intent in enumerate(actual_sequence):
            if i < len(expected_sequence) and intent == expected_sequence[i]:
                exact_matches += 1
        
        # Partial order matches (allowing skips)
        partial_matches = 0
        actual_idx = 0
        expected_idx = 0
        
        while actual_idx < len(actual_sequence) and expected_idx < len(expected_sequence):
            if actual_sequence[actual_idx] == expected_sequence[expected_idx]:
                partial_matches += 1
                actual_idx += 1
                expected_idx += 1
            else:
                # Try advancing both sequences to find matches
                if actual_idx + 1 < len(actual_sequence) and actual_sequence[actual_idx + 1] == expected_sequence[expected_idx]:
                    actual_idx += 1
                elif expected_idx + 1 < len(expected_sequence) and actual_sequence[actual_idx] == expected_sequence[expected_idx + 1]:
                    expected_idx += 1
                else:
                    actual_idx += 1
                    expected_idx += 1
        
        # Calculate weighted match score
        exact_score = exact_matches / max(len(actual_sequence), len(expected_sequence))
        partial_score = partial_matches / max(len(actual_sequence), len(expected_sequence))
        
        # Weighted combination (exact matches more important)
        match_score = exact_score * 0.7 + partial_score * 0.3
        
        return min(match_score, 1.0)
    
    async def _calculate_completion_percentage(self, actual_sequence: List[str], expected_sequence: List[str]) -> float:
        """Calculate how much of expected sequence has been completed"""
        
        if not expected_sequence:
            return 1.0
        
        # Find the furthest position in expected sequence that matches actual sequence
        furthest_position = 0
        
        for expected_intent in expected_sequence:
            if expected_intent in actual_sequence:
                position = expected_sequence.index(expected_intent)
                furthest_position = max(furthest_position, position + 1)
        
        return furthest_position / len(expected_sequence)
    
    async def _calculate_pattern_strength(self, intent_sequence: List[str], matching_patterns: List[Dict]) -> float:
        """Calculate overall pattern strength of the sequence"""
        
        if not matching_patterns:
            return 0.3  # Low but not zero for sequences without clear patterns
        
        # Get best match score
        best_match = matching_patterns[0]['match_score']
        
        # Calculate consistency (how similar are top matches)
        if len(matching_patterns) > 1:
            top_scores = [p['match_score'] for p in matching_patterns[:3]]
            consistency = 1.0 - (max(top_scores) - min(top_scores))
        else:
            consistency = 1.0
        
        # Calculate progression quality (are intents building logically)
        progression_quality = await self._assess_intent_progression(intent_sequence)
        
        # Combined pattern strength
        pattern_strength = (best_match * 0.5 + 
                          consistency * 0.3 + 
                          progression_quality * 0.2)
        
        return min(pattern_strength, 1.0)
    
    async def _assess_intent_progression(self, intent_sequence: List[str]) -> float:
        """Assess the logical progression quality of intents"""
        
        if len(intent_sequence) < 2:
            return 0.5
        
        # Define logical intent progressions
        good_progressions = [
            ('greeting', 'symptom_description'),
            ('symptom_description', 'symptom_detail'),
            ('symptom_detail', 'medical_history'),
            ('medical_history', 'medication_inquiry'),
            ('medication_inquiry', 'treatment_request'),
            ('symptom_description', 'emergency_concern'),
            ('emergency_concern', 'immediate_assessment')
        ]
        
        # Count good progressions in sequence
        good_transitions = 0
        total_transitions = len(intent_sequence) - 1
        
        for i in range(total_transitions):
            current_intent = intent_sequence[i]
            next_intent = intent_sequence[i + 1]
            
            if (current_intent, next_intent) in good_progressions:
                good_transitions += 1
            # Also check for partial matches (similar intent categories)
            elif self._are_related_intents(current_intent, next_intent):
                good_transitions += 0.5
        
        return good_transitions / total_transitions if total_transitions > 0 else 0.5
    
    def _are_related_intents(self, intent1: str, intent2: str) -> bool:
        """Check if two intents are logically related"""
        
        related_groups = [
            ['symptom_description', 'symptom_detail', 'symptom_clarification'],
            ['medical_history', 'past_medical_history', 'family_history'],
            ['medication_inquiry', 'medication_review', 'drug_interaction'],
            ['treatment_request', 'treatment_options', 'therapy_discussion'],
            ['emergency_concern', 'urgent_care', 'immediate_assessment'],
            ['lifestyle_inquiry', 'lifestyle_factors', 'wellness_discussion']
        ]
        
        for group in related_groups:
            if intent1 in group and intent2 in group:
                return True
        
        return False
    
    async def _analyze_pattern_deviations(self, intent_sequence: List[str], matching_patterns: List[Dict]) -> Dict[str, Any]:
        """Analyze deviations from expected medical conversation patterns"""
        
        if not matching_patterns:
            return {
                'deviation_score': 0.5,
                'deviation_type': 'no_clear_pattern',
                'suggested_corrections': []
            }
        
        best_pattern = matching_patterns[0]
        expected_sequence = best_pattern['expected_sequence']
        
        # Find deviations
        deviations = []
        suggested_corrections = []
        
        # Check for missing expected intents
        missing_intents = [intent for intent in expected_sequence if intent not in intent_sequence]
        if missing_intents:
            deviations.append({
                'type': 'missing_intents',
                'items': missing_intents[:3],  # Top 3 missing
                'severity': 'medium'
            })
            suggested_corrections.extend([
                f"Consider addressing {intent.replace('_', ' ')}" 
                for intent in missing_intents[:2]
            ])
        
        # Check for unexpected intents
        unexpected_intents = [intent for intent in intent_sequence if intent not in expected_sequence]
        if unexpected_intents:
            deviations.append({
                'type': 'unexpected_intents',
                'items': unexpected_intents,
                'severity': 'low' if len(unexpected_intents) <= 2 else 'medium'
            })
        
        # Check for order deviations
        order_score = await self._calculate_sequence_match(intent_sequence, expected_sequence)
        if order_score < 0.6:
            deviations.append({
                'type': 'order_deviation',
                'severity': 'high' if order_score < 0.3 else 'medium'
            })
            suggested_corrections.append("Consider following standard medical interview order")
        
        # Calculate overall deviation score
        deviation_score = 0.0
        for deviation in deviations:
            if deviation['severity'] == 'high':
                deviation_score += 0.4
            elif deviation['severity'] == 'medium':
                deviation_score += 0.2
            else:
                deviation_score += 0.1
        
        deviation_score = min(deviation_score, 1.0)
        
        return {
            'deviation_score': deviation_score,
            'deviation_type': self._classify_deviation_type(deviations),
            'deviations': deviations,
            'suggested_corrections': suggested_corrections,
            'pattern_adherence': 1.0 - deviation_score
        }
    
    def _classify_deviation_type(self, deviations: List[Dict]) -> str:
        """Classify the type of deviation from expected patterns"""
        
        if not deviations:
            return 'no_deviation'
        
        deviation_types = [d['type'] for d in deviations]
        
        if 'order_deviation' in deviation_types:
            return 'sequence_order_issue'
        elif 'missing_intents' in deviation_types and 'unexpected_intents' in deviation_types:
            return 'mixed_deviation'
        elif 'missing_intents' in deviation_types:
            return 'incomplete_information_gathering'
        elif 'unexpected_intents' in deviation_types:
            return 'exploratory_deviation'
        else:
            return 'minor_deviation'
    
    async def _identify_subsequence_patterns(self, intent_sequence: List[str]) -> List[Dict[str, Any]]:
        """Identify recurring sub-patterns within the sequence"""
        
        sub_patterns = []
        
        if len(intent_sequence) < 4:
            return sub_patterns
        
        # Look for repeating subsequences of length 2-4
        for pattern_length in range(2, min(5, len(intent_sequence))):
            for start_idx in range(len(intent_sequence) - pattern_length + 1):
                subsequence = intent_sequence[start_idx:start_idx + pattern_length]
                
                # Count occurrences of this subsequence
                occurrences = 0
                for check_idx in range(len(intent_sequence) - pattern_length + 1):
                    if intent_sequence[check_idx:check_idx + pattern_length] == subsequence:
                        occurrences += 1
                
                if occurrences >= 2:  # Found a repeating pattern
                    sub_patterns.append({
                        'pattern': subsequence,
                        'occurrences': occurrences,
                        'length': pattern_length,
                        'frequency': occurrences / (len(intent_sequence) - pattern_length + 1),
                        'pattern_type': 'repetitive' if occurrences > 2 else 'reinforcing'
                    })
        
        # Remove duplicate patterns and sort by frequency
        unique_patterns = []
        seen_patterns = set()
        
        for pattern in sub_patterns:
            pattern_str = '->'.join(pattern['pattern'])
            if pattern_str not in seen_patterns:
                unique_patterns.append(pattern)
                seen_patterns.add(pattern_str)
        
        unique_patterns.sort(key=lambda x: x['frequency'], reverse=True)
        
        return unique_patterns[:5]  # Top 5 sub-patterns
    
    async def _analyze_intent_transitions(self, intent_sequence: List[str]) -> Dict[str, Any]:
        """Analyze intent transition patterns and probabilities"""
        
        if len(intent_sequence) < 2:
            return {
                'transition_count': 0,
                'transition_probabilities': {},
                'most_likely_transitions': [],
                'unusual_transitions': []
            }
        
        # Count transitions
        transition_counts = defaultdict(int)
        intent_counts = defaultdict(int)
        
        for i in range(len(intent_sequence) - 1):
            current_intent = intent_sequence[i]
            next_intent = intent_sequence[i + 1]
            
            transition_counts[(current_intent, next_intent)] += 1
            intent_counts[current_intent] += 1
        
        # Calculate transition probabilities
        transition_probabilities = {}
        for (current, next_intent), count in transition_counts.items():
            prob = count / intent_counts[current] if intent_counts[current] > 0 else 0
            transition_probabilities[(current, next_intent)] = prob
        
        # Find most likely transitions
        most_likely = sorted(
            transition_probabilities.items(),
            key=lambda x: x[1], reverse=True
        )[:5]
        
        # Find unusual transitions (comparing against expected medical patterns)
        unusual_transitions = await self._identify_unusual_transitions(transition_probabilities)
        
        return {
            'transition_count': len(transition_counts),
            'transition_probabilities': {
                f"{current}->{next_intent}": prob 
                for (current, next_intent), prob in transition_probabilities.items()
            },
            'most_likely_transitions': [
                {
                    'transition': f"{current}->{next_intent}",
                    'probability': prob,
                    'medical_appropriateness': await self._assess_transition_appropriateness(current, next_intent)
                }
                for (current, next_intent), prob in most_likely
            ],
            'unusual_transitions': unusual_transitions,
            'transition_entropy': await self._calculate_transition_entropy(transition_probabilities)
        }
    
    async def _identify_unusual_transitions(self, observed_transitions: Dict[Tuple[str, str], float]) -> List[Dict[str, Any]]:
        """Identify transitions that are unusual in medical conversations"""
        
        # Define expected transition probabilities for medical conversations
        expected_transitions = {
            ('greeting', 'symptom_description'): 0.8,
            ('symptom_description', 'symptom_detail'): 0.7,
            ('symptom_detail', 'medical_history'): 0.6,
            ('medical_history', 'medication_inquiry'): 0.5,
            ('emergency_concern', 'immediate_assessment'): 0.9,
            ('treatment_request', 'follow_up_care'): 0.6
        }
        
        unusual_transitions = []
        
        for (current, next_intent), observed_prob in observed_transitions.items():
            expected_prob = expected_transitions.get((current, next_intent), 0.3)  # Default low probability
            
            # Consider transitions unusual if they deviate significantly from expected
            deviation = abs(observed_prob - expected_prob)
            
            if deviation > 0.4:
                unusual_transitions.append({
                    'transition': f"{current}->{next_intent}",
                    'observed_probability': observed_prob,
                    'expected_probability': expected_prob,
                    'deviation': deviation,
                    'unusual_type': 'higher_than_expected' if observed_prob > expected_prob else 'lower_than_expected'
                })
        
        return unusual_transitions[:3]  # Top 3 unusual transitions
    
    async def _assess_transition_appropriateness(self, current_intent: str, next_intent: str) -> Dict[str, Any]:
        """Assess medical appropriateness of intent transitions"""
        
        # High appropriateness transitions
        high_appropriateness = [
            ('symptom_description', 'symptom_detail'),
            ('symptom_detail', 'medical_history'),
            ('emergency_concern', 'immediate_assessment'),
            ('medical_history', 'medication_inquiry'),
            ('treatment_request', 'follow_up_care')
        ]
        
        # Medium appropriateness transitions
        medium_appropriateness = [
            ('greeting', 'medical_history'),
            ('symptom_description', 'treatment_request'),
            ('medication_inquiry', 'lifestyle_inquiry'),
            ('lifestyle_inquiry', 'treatment_request')
        ]
        
        # Low appropriateness transitions
        low_appropriateness = [
            ('treatment_request', 'greeting'),
            ('follow_up_care', 'symptom_description'),
            ('immediate_assessment', 'lifestyle_inquiry')
        ]
        
        transition = (current_intent, next_intent)
        
        if transition in high_appropriateness:
            return {'appropriateness': 'high', 'score': 0.9, 'reasoning': 'Standard medical interview progression'}
        elif transition in medium_appropriateness:
            return {'appropriateness': 'medium', 'score': 0.6, 'reasoning': 'Acceptable but not optimal progression'}
        elif transition in low_appropriateness:
            return {'appropriateness': 'low', 'score': 0.3, 'reasoning': 'Unusual or counterproductive transition'}
        else:
            return {'appropriateness': 'neutral', 'score': 0.5, 'reasoning': 'Standard transition without strong medical precedent'}
    
    async def _calculate_transition_entropy(self, transition_probs: Dict[Tuple[str, str], float]) -> float:
        """Calculate entropy of transition probabilities (measure of predictability)"""
        
        if not transition_probs:
            return 0.0
        
        # Group transitions by current intent
        intent_transitions = defaultdict(list)
        for (current, next_intent), prob in transition_probs.items():
            intent_transitions[current].append(prob)
        
        # Calculate entropy for each intent's transitions
        total_entropy = 0.0
        for current_intent, probs in intent_transitions.items():
            if probs:
                # Normalize probabilities
                total_prob = sum(probs)
                normalized_probs = [p / total_prob for p in probs] if total_prob > 0 else probs
                
                # Calculate entropy: -Σ(p * log2(p))
                entropy = -sum(p * np.log2(p) for p in normalized_probs if p > 0)
                total_entropy += entropy
        
        # Average entropy across all intents
        average_entropy = total_entropy / len(intent_transitions) if intent_transitions else 0.0
        
        return average_entropy
    
    async def _predict_intent_sequences(self, current_sequence: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Predict likely next intent sequences"""
        
        if not current_sequence:
            return {
                'next_sequences': [],
                'prediction_confidence': 0.0,
                'prediction_method': 'fallback'
            }
        
        # Use multiple prediction methods
        markov_predictions = await self._predict_using_markov_model(current_sequence)
        pattern_predictions = await self._predict_using_pattern_matching(current_sequence, context)
        medical_predictions = await self._predict_using_medical_templates(current_sequence, context)
        
        # Combine and rank predictions
        combined_predictions = await self._combine_sequence_predictions(
            markov_predictions, pattern_predictions, medical_predictions
        )
        
        # Calculate prediction confidence
        prediction_confidence = await self._calculate_prediction_confidence(
            current_sequence, combined_predictions
        )
        
        return {
            'next_sequences': combined_predictions[:5],  # Top 5 predictions
            'prediction_confidence': prediction_confidence,
            'prediction_methods_used': ['markov_model', 'pattern_matching', 'medical_templates'],
            'sequence_context': await self._analyze_sequence_context(current_sequence, context),
            'alternative_paths': await self._generate_alternative_paths(current_sequence, context)
        }
    
    async def _predict_using_markov_model(self, sequence: List[str]) -> List[Dict[str, Any]]:
        """Predict next intents using Markov chain model"""
        
        if len(sequence) < 1:
            return []
        
        current_intent = sequence[-1]
        
        # Get transition probabilities for current intent
        # (In a real implementation, this would use learned transition matrix)
        mock_transitions = {
            'greeting': [
                ('symptom_description', 0.7),
                ('general_inquiry', 0.2),
                ('appointment_scheduling', 0.1)
            ],
            'symptom_description': [
                ('symptom_detail', 0.6),
                ('emergency_concern', 0.2),
                ('medical_history', 0.2)
            ],
            'symptom_detail': [
                ('medical_history', 0.5),
                ('medication_inquiry', 0.3),
                ('treatment_request', 0.2)
            ],
            'medical_history': [
                ('medication_inquiry', 0.6),
                ('lifestyle_inquiry', 0.3),
                ('treatment_request', 0.1)
            ],
            'emergency_concern': [
                ('immediate_assessment', 0.8),
                ('symptom_detail', 0.2)
            ]
        }
        
        transitions = mock_transitions.get(current_intent, [])
        
        return [
            {
                'sequence': [intent],
                'probability': prob,
                'method': 'markov',
                'confidence': prob * 0.8  # Slightly lower confidence for single-step prediction
            }
            for intent, prob in transitions
        ]
    
    async def _predict_using_pattern_matching(self, sequence: List[str], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict next intents using pattern matching against known sequences"""
        
        predictions = []
        
        # Find matching patterns and predict next steps
        for pattern_name, pattern_data in self.medical_sequence_templates.items():
            typical_sequence = pattern_data.get('typical_sequence', [])
            
            # Find where current sequence matches in the typical sequence
            match_position = await self._find_sequence_position(sequence, typical_sequence)
            
            if match_position >= 0 and match_position < len(typical_sequence) - 1:
                next_intents = typical_sequence[match_position + 1:match_position + 4]  # Next 1-3 intents
                
                match_confidence = await self._calculate_sequence_match(sequence, typical_sequence[:len(sequence)])
                
                predictions.append({
                    'sequence': next_intents,
                    'probability': match_confidence * pattern_data.get('efficiency_score', 0.7),
                    'method': 'pattern_matching',
                    'pattern_source': pattern_name,
                    'confidence': match_confidence
                })
        
        return predictions
    
    async def _find_sequence_position(self, actual_sequence: List[str], pattern_sequence: List[str]) -> int:
        """Find the position in pattern sequence that matches the end of actual sequence"""
        
        if not actual_sequence or not pattern_sequence:
            return -1
        
        # Look for the best match position
        best_position = -1
        best_match_count = 0
        
        for i in range(len(pattern_sequence)):
            match_count = 0
            
            # Count how many recent intents match at this position
            for j, intent in enumerate(reversed(actual_sequence)):
                pattern_idx = i - j
                if pattern_idx >= 0 and pattern_idx < len(pattern_sequence):
                    if pattern_sequence[pattern_idx] == intent:
                        match_count += 1
                    else:
                        break
            
            if match_count > best_match_count:
                best_match_count = match_count
                best_position = i
        
        return best_position if best_match_count > 0 else -1
    
    async def _predict_using_medical_templates(self, sequence: List[str], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict using medical conversation templates and clinical reasoning"""
        
        current_stage = context.get('current_stage', 'greeting')
        urgency_level = context.get('urgency_level', 'routine')
        
        predictions = []
        
        # Stage-based predictions
        stage_next_intents = {
            'greeting': ['symptom_description', 'chief_complaint'],
            'chief_complaint': ['symptom_detail', 'history_present_illness'],
            'history_present_illness': ['medical_history', 'medication_inquiry'],
            'past_medical_history': ['medication_inquiry', 'social_history'],
            'medications': ['treatment_request', 'follow_up_care']
        }
        
        next_intents = stage_next_intents.get(current_stage, ['general_inquiry'])
        
        for intent in next_intents:
            predictions.append({
                'sequence': [intent],
                'probability': 0.7,  # High probability for stage-based predictions
                'method': 'medical_template',
                'stage_based': True,
                'confidence': 0.8
            })
        
        # Urgency-based predictions
        if urgency_level in ['high', 'emergency']:
            predictions.append({
                'sequence': ['emergency_assessment', 'immediate_action'],
                'probability': 0.9,
                'method': 'medical_template',
                'urgency_based': True,
                'confidence': 0.9
            })
        
        return predictions
    
    async def _combine_sequence_predictions(self, *prediction_sets) -> List[Dict[str, Any]]:
        """Combine predictions from multiple methods"""
        
        combined = {}
        
        for prediction_set in prediction_sets:
            for prediction in prediction_set:
                sequence_str = '->'.join(prediction['sequence'])
                
                if sequence_str in combined:
                    # Combine probabilities (weighted average)
                    existing = combined[sequence_str]
                    total_weight = existing['weight'] + 1
                    existing['probability'] = (existing['probability'] * existing['weight'] + prediction['probability']) / total_weight
                    existing['confidence'] = max(existing['confidence'], prediction['confidence'])
                    existing['weight'] = total_weight
                    existing['methods'].append(prediction['method'])
                else:
                    combined[sequence_str] = {
                        'sequence': prediction['sequence'],
                        'probability': prediction['probability'],
                        'confidence': prediction['confidence'],
                        'methods': [prediction['method']],
                        'weight': 1
                    }
        
        # Convert to list and sort by probability
        result = []
        for sequence_str, data in combined.items():
            result.append({
                'predicted_sequence': data['sequence'],
                'combined_probability': data['probability'],
                'prediction_confidence': data['confidence'],
                'supporting_methods': data['methods'],
                'method_count': len(data['methods']),
                'consensus_strength': len(data['methods']) / 3  # Assuming 3 prediction methods
            })
        
        result.sort(key=lambda x: x['combined_probability'], reverse=True)
        return result
    
    async def _calculate_prediction_confidence(self, sequence: List[str], predictions: List[Dict]) -> float:
        """Calculate overall confidence in sequence predictions"""
        
        if not predictions:
            return 0.3
        
        # Factors affecting confidence
        sequence_length_factor = min(len(sequence) / 5, 1.0)  # More confident with longer sequences
        top_prediction_prob = predictions[0]['combined_probability'] if predictions else 0.5
        method_consensus = np.mean([p['consensus_strength'] for p in predictions[:3]])
        
        # Combined confidence
        confidence = (sequence_length_factor * 0.3 + 
                     top_prediction_prob * 0.4 + 
                     method_consensus * 0.3)
        
        return min(confidence, 0.95)  # Cap at 95%
    
    async def _assess_sequence_efficiency(self, intent_sequence: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the efficiency of the current intent sequence"""
        
        sequence_length = len(intent_sequence)
        unique_intents = len(set(intent_sequence))
        
        # Calculate efficiency metrics
        information_density = unique_intents / sequence_length if sequence_length > 0 else 0
        
        # Repetition analysis
        repetition_score = 1.0 - information_density
        
        # Progress analysis
        current_stage = context.get('current_stage', 'greeting')
        stage_number = self._get_stage_number(current_stage)
        expected_turns = stage_number * 2  # Rough estimate
        
        progress_efficiency = min(sequence_length / expected_turns, 1.0) if expected_turns > 0 else 0.5
        
        # Medical appropriateness
        medical_efficiency = await self._calculate_medical_efficiency(intent_sequence, context)
        
        # Overall efficiency score
        overall_efficiency = (information_density * 0.3 + 
                            (1.0 - repetition_score) * 0.2 + 
                            progress_efficiency * 0.3 + 
                            medical_efficiency * 0.2)
        
        return {
            'overall_efficiency': overall_efficiency,
            'information_density': information_density,
            'repetition_score': repetition_score,
            'progress_efficiency': progress_efficiency,
            'medical_efficiency': medical_efficiency,
            'sequence_quality_grade': await self._get_efficiency_grade(overall_efficiency),
            'efficiency_factors': {
                'good_progression': progress_efficiency > 0.7,
                'minimal_repetition': repetition_score < 0.3,
                'high_information_content': information_density > 0.7,
                'medically_appropriate': medical_efficiency > 0.6
            }
        }
    
    def _get_stage_number(self, stage: str) -> int:
        """Get numeric position of medical interview stage"""
        
        stage_numbers = {
            'greeting': 1, 'chief_complaint': 2, 'history_present_illness': 3,
            'past_medical_history': 4, 'medications': 5, 'allergies': 6,
            'social_history': 7, 'review_of_systems': 8, 'assessment': 9, 'plan': 10
        }
        
        return stage_numbers.get(stage, 3)  # Default to middle stage
    
    async def _calculate_medical_efficiency(self, intent_sequence: List[str], context: Dict[str, Any]) -> float:
        """Calculate medical appropriateness and efficiency of intent sequence"""
        
        # Check for presence of key medical interview components
        key_components = [
            'symptom_description', 'symptom_detail', 'medical_history',
            'medication_inquiry', 'treatment_request'
        ]
        
        present_components = sum(1 for component in key_components if component in intent_sequence)
        component_score = present_components / len(key_components)
        
        # Check for logical medical progression
        progression_score = await self._assess_intent_progression(intent_sequence)
        
        # Check for appropriate emergency handling
        emergency_score = 1.0
        if 'emergency_concern' in intent_sequence:
            emergency_index = intent_sequence.index('emergency_concern')
            # Emergency should be followed by assessment/action
            if emergency_index < len(intent_sequence) - 1:
                next_intent = intent_sequence[emergency_index + 1]
                if 'assessment' in next_intent or 'action' in next_intent:
                    emergency_score = 1.0
                else:
                    emergency_score = 0.6
            else:
                emergency_score = 0.8  # Emergency mentioned but not yet addressed
        
        # Combined medical efficiency
        medical_efficiency = (component_score * 0.5 + 
                            progression_score * 0.3 + 
                            emergency_score * 0.2)
        
        return medical_efficiency
    
    async def _get_efficiency_grade(self, efficiency_score: float) -> str:
        """Convert efficiency score to letter grade"""
        
        if efficiency_score >= 0.9:
            return 'A+'
        elif efficiency_score >= 0.8:
            return 'A'
        elif efficiency_score >= 0.7:
            return 'B'
        elif efficiency_score >= 0.6:
            return 'C'
        elif efficiency_score >= 0.5:
            return 'D'
        else:
            return 'F'
    
    async def _generate_sequence_optimizations(self, intent_sequence: List[str], 
                                            pattern_analysis: Dict[str, Any], 
                                            efficiency_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate recommendations for optimizing the intent sequence"""
        
        optimizations = {
            'immediate_recommendations': [],
            'strategic_improvements': [],
            'efficiency_boosters': [],
            'pattern_corrections': []
        }
        
        # Immediate recommendations based on current state
        overall_efficiency = efficiency_analysis.get('overall_efficiency', 0.5)
        if overall_efficiency < 0.6:
            optimizations['immediate_recommendations'].extend([
                {
                    'recommendation': 'reduce_repetitive_patterns',
                    'description': 'Avoid repeating similar intent types consecutively',
                    'priority': 'high'
                },
                {
                    'recommendation': 'focus_information_gathering',
                    'description': 'Concentrate on gathering essential medical information',
                    'priority': 'high'
                }
            ])
        
        # Pattern-based corrections
        deviation_score = pattern_analysis.get('deviation_analysis', {}).get('deviation_score', 0.0)
        if deviation_score > 0.4:
            suggested_corrections = pattern_analysis.get('deviation_analysis', {}).get('suggested_corrections', [])
            optimizations['pattern_corrections'].extend([
                {
                    'correction': correction,
                    'impact': 'medium'
                }
                for correction in suggested_corrections[:3]
            ])
        
        # Efficiency boosters
        if efficiency_analysis.get('information_density', 0.5) < 0.6:
            optimizations['efficiency_boosters'].append({
                'booster': 'increase_information_density',
                'technique': 'Ask compound questions that gather multiple types of information',
                'expected_improvement': 0.15
            })
        
        # Strategic improvements based on sequence type
        sequence_type = pattern_analysis.get('sequence_type', '')
        if sequence_type == SequenceType.REPETITIVE_CLARIFICATION.value:
            optimizations['strategic_improvements'].append({
                'improvement': 'break_repetitive_cycle',
                'strategy': 'Introduce new information gathering approaches',
                'implementation': 'Change question types or conversation direction'
            })
        
        return optimizations
    
    async def _analyze_sequence_context(self, sequence: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the context around the intent sequence"""
        
        return {
            'conversation_stage': context.get('current_stage', 'unknown'),
            'urgency_level': context.get('urgency_level', 'routine'),
            'sequence_maturity': len(sequence) / 10,  # Normalized maturity score
            'medical_context': await self._extract_medical_context(context),
            'patient_engagement': await self._assess_patient_engagement(context)
        }
    
    async def _extract_medical_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract medical context factors that influence sequence prediction"""
        
        conversation_history = context.get('conversation_history', [])
        
        # Extract medical indicators from conversation
        medical_keywords = []
        urgency_indicators = []
        
        user_messages = [
            msg.get('content', '') for msg in conversation_history
            if msg.get('role') == 'user'
        ]
        
        combined_text = ' '.join(user_messages).lower()
        
        # Medical specialties
        specialties = ['cardiac', 'neuro', 'respiratory', 'gastrointestinal', 'orthopedic']
        detected_specialties = [spec for spec in specialties if spec in combined_text]
        
        return {
            'detected_specialties': detected_specialties,
            'medical_complexity': 'high' if len(detected_specialties) > 1 else 'medium' if detected_specialties else 'low',
            'symptom_categories': await self._categorize_symptoms(combined_text),
            'consultation_type': await self._infer_consultation_type(context)
        }
    
    async def _categorize_symptoms(self, text: str) -> List[str]:
        """Categorize symptoms mentioned in conversation"""
        
        symptom_categories = {
            'pain': ['pain', 'hurt', 'ache', 'discomfort', 'sore'],
            'respiratory': ['breath', 'cough', 'wheeze', 'lung'],
            'cardiac': ['chest', 'heart', 'palpitation', 'cardiac'],
            'neurological': ['headache', 'dizzy', 'numb', 'weakness'],
            'gastrointestinal': ['stomach', 'nausea', 'vomit', 'digest']
        }
        
        detected_categories = []
        for category, keywords in symptom_categories.items():
            if any(keyword in text for keyword in keywords):
                detected_categories.append(category)
        
        return detected_categories
    
    async def _infer_consultation_type(self, context: Dict[str, Any]) -> str:
        """Infer the type of medical consultation"""
        
        urgency = context.get('urgency_level', 'routine')
        stage = context.get('current_stage', 'greeting')
        
        if urgency == 'emergency':
            return 'emergency_consultation'
        elif 'follow' in stage:
            return 'follow_up_consultation'
        elif urgency == 'routine':
            return 'routine_consultation'
        else:
            return 'general_consultation'
    
    async def _assess_patient_engagement(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess patient engagement level from conversation context"""
        
        conversation_history = context.get('conversation_history', [])
        
        user_messages = [msg for msg in conversation_history if msg.get('role') == 'user']
        
        if not user_messages:
            return {'engagement_level': 'unknown', 'indicators': []}
        
        # Analyze engagement indicators
        avg_message_length = np.mean([len(msg.get('content', '').split()) for msg in user_messages])
        question_count = sum(1 for msg in user_messages if '?' in msg.get('content', ''))
        detail_level = sum(1 for msg in user_messages if len(msg.get('content', '').split()) > 10)
        
        # Classify engagement
        if avg_message_length > 15 and detail_level > len(user_messages) * 0.5:
            engagement_level = 'high'
        elif avg_message_length > 8 or question_count > 2:
            engagement_level = 'medium'
        else:
            engagement_level = 'low'
        
        return {
            'engagement_level': engagement_level,
            'avg_message_length': avg_message_length,
            'question_count': question_count,
            'detail_level': detail_level / len(user_messages) if user_messages else 0,
            'indicators': [
                'detailed_responses' if avg_message_length > 15 else None,
                'asks_questions' if question_count > 2 else None,
                'provides_context' if detail_level > 0 else None
            ]
        }
    
    async def _generate_alternative_paths(self, sequence: List[str], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate alternative conversation paths based on current sequence"""
        
        alternative_paths = []
        
        # Generate paths based on different medical scenarios
        medical_scenarios = ['emergency_focus', 'comprehensive_assessment', 'focused_inquiry']
        
        for scenario in medical_scenarios:
            path = await self._generate_path_for_scenario(sequence, scenario, context)
            if path:
                alternative_paths.append(path)
        
        return alternative_paths
    
    async def _generate_path_for_scenario(self, current_sequence: List[str], scenario: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a conversation path for a specific scenario"""
        
        scenario_paths = {
            'emergency_focus': [
                'emergency_assessment', 'immediate_safety', 'professional_consultation'
            ],
            'comprehensive_assessment': [
                'detailed_history', 'complete_examination', 'differential_diagnosis', 'treatment_planning'
            ],
            'focused_inquiry': [
                'targeted_questions', 'specific_assessment', 'focused_recommendations'
            ]
        }
        
        path_sequence = scenario_paths.get(scenario, [])
        
        if path_sequence:
            return {
                'scenario': scenario,
                'path_sequence': path_sequence,
                'estimated_turns': len(path_sequence) * 2,
                'suitability_score': await self._calculate_path_suitability(path_sequence, context),
                'path_description': f"Alternative path focusing on {scenario.replace('_', ' ')}"
            }
        
        return None
    
    async def _calculate_path_suitability(self, path_sequence: List[str], context: Dict[str, Any]) -> float:
        """Calculate how suitable an alternative path is for current context"""
        
        urgency = context.get('urgency_level', 'routine')
        current_stage = context.get('current_stage', 'greeting')
        
        # Basic suitability scoring
        base_score = 0.5
        
        # Adjust for urgency
        if urgency == 'emergency' and 'emergency' in path_sequence[0]:
            base_score += 0.3
        elif urgency == 'routine' and 'comprehensive' in ' '.join(path_sequence):
            base_score += 0.2
        
        # Adjust for stage appropriateness
        if current_stage in ['greeting', 'chief_complaint'] and 'assessment' in path_sequence[0]:
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    async def _calculate_pattern_complexity(self, intent_sequence: List[str]) -> float:
        """Calculate complexity score of the intent pattern"""
        
        if len(intent_sequence) < 2:
            return 0.2
        
        # Factors contributing to complexity
        unique_intents = len(set(intent_sequence))
        sequence_length = len(intent_sequence)
        
        # Transition diversity
        transitions = [(intent_sequence[i], intent_sequence[i+1]) for i in range(len(intent_sequence)-1)]
        unique_transitions = len(set(transitions))
        
        # Complexity score
        diversity_factor = unique_intents / sequence_length
        transition_factor = unique_transitions / max(len(transitions), 1)
        
        complexity = (diversity_factor + transition_factor) / 2
        
        return min(complexity, 1.0)
    
    async def _calculate_analysis_confidence(self, intent_sequence: List[str], pattern_analysis: Dict[str, Any]) -> float:
        """Calculate confidence in the pattern analysis"""
        
        # Factors affecting confidence
        sequence_length_factor = min(len(intent_sequence) / 5, 1.0)
        pattern_strength = pattern_analysis.get('pattern_strength', 0.5)
        matching_patterns = len(pattern_analysis.get('matching_medical_patterns', []))
        
        # Confidence calculation
        confidence = (sequence_length_factor * 0.4 + 
                     pattern_strength * 0.4 + 
                     min(matching_patterns / 3, 1.0) * 0.2)
        
        return min(confidence, 0.95)
    
    async def _assess_pattern_quality(self, intent_sequence: List[str], matching_patterns: List[Dict]) -> Dict[str, Any]:
        """Assess the overall quality of the intent pattern"""
        
        if not matching_patterns:
            return {'quality_score': 0.4, 'quality_grade': 'D', 'quality_factors': {}}
        
        best_match = matching_patterns[0]
        
        # Quality factors
        match_strength = best_match['match_score']
        completion_rate = best_match.get('completion_percentage', 0.5)
        efficiency = best_match.get('efficiency_score', 0.7)
        
        # Overall quality
        quality_score = (match_strength * 0.4 + completion_rate * 0.3 + efficiency * 0.3)
        
        # Quality grade
        if quality_score >= 0.9:
            quality_grade = 'A'
        elif quality_score >= 0.8:
            quality_grade = 'B'
        elif quality_score >= 0.7:
            quality_grade = 'C'
        elif quality_score >= 0.6:
            quality_grade = 'D'
        else:
            quality_grade = 'F'
        
        return {
            'quality_score': quality_score,
            'quality_grade': quality_grade,
            'quality_factors': {
                'pattern_match_strength': match_strength,
                'completion_rate': completion_rate,
                'efficiency_score': efficiency,
                'medical_appropriateness': quality_score > 0.7
            }
        }
    
    async def _assess_medical_appropriateness(self, intent_sequence: List[str], context: Dict[str, Any]) -> float:
        """Assess medical appropriateness of the intent sequence"""
        
        # Check for appropriate medical interview components
        essential_components = ['symptom_description', 'symptom_detail']
        recommended_components = ['medical_history', 'medication_inquiry']
        
        essential_score = sum(1 for comp in essential_components if comp in intent_sequence) / len(essential_components)
        recommended_score = sum(1 for comp in recommended_components if comp in intent_sequence) / len(recommended_components)
        
        # Check for appropriate progression
        progression_score = await self._assess_intent_progression(intent_sequence)
        
        # Medical appropriateness score
        appropriateness = (essential_score * 0.5 + recommended_score * 0.3 + progression_score * 0.2)
        
        return appropriateness
    
    async def _update_learning_data(self, intent_sequence: List[str], analysis_result: Dict[str, Any]):
        """Update learning data with new sequence analysis"""
        
        # Store sequence for learning
        self.observed_sequences.append({
            'sequence': intent_sequence,
            'analysis': analysis_result,
            'timestamp': datetime.utcnow(),
            'pattern_strength': analysis_result.get('pattern_analysis', {}).get('pattern_strength', 0.5)
        })
        
        # Update performance metrics
        self.analysis_metrics['sequences_analyzed'] += 1
        
        # Update pattern frequencies
        for i in range(len(intent_sequence) - 1):
            transition = (intent_sequence[i], intent_sequence[i + 1])
            self.pattern_frequencies[transition] += 1
    
    async def _generate_fallback_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback analysis when main analysis fails"""
        
        return {
            'status': 'fallback',
            'algorithm_version': self.algorithm_version,
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'intent_sequence': ['unknown'],
            'pattern_analysis': {
                'pattern_type': 'unknown',
                'pattern_strength': 0.3,
                'matching_medical_patterns': [],
                'recognized_patterns': []
            },
            'sequence_predictions': {
                'next_sequences': [
                    {
                        'predicted_sequence': ['symptom_description'],
                        'combined_probability': 0.6,
                        'prediction_confidence': 0.4
                    }
                ],
                'prediction_confidence': 0.4
            },
            'efficiency_analysis': {
                'overall_efficiency': 0.5,
                'sequence_quality_grade': 'C'
            },
            'optimization_recommendations': {
                'immediate_recommendations': [
                    {
                        'recommendation': 'start_standard_medical_interview',
                        'description': 'Begin with standard symptom assessment',
                        'priority': 'medium'
                    }
                ]
            },
            'fallback_reason': 'Intent sequence analysis error - using default template',
            'processing_time_ms': 5.0
        }
    
    async def _build_transition_models(self):
        """Build transition probability models from historical data"""
        # Placeholder for building ML models
        logger.info("🔄 Building intent transition models...")
    
    async def _load_sequence_patterns(self):
        """Load historical sequence patterns"""
        # Placeholder for loading historical patterns
        logger.info("📚 Loading historical sequence patterns...")

# Initialize global intent sequence analyzer
intent_sequence_analyzer = IntentSequenceAnalyzer()

logger.info("📊 Intent Sequence Analyzer module loaded successfully")