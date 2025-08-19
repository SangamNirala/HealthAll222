"""
🎛️ PERSONALIZATION MANAGER - STEP 1 IMPLEMENTATION
==================================================

Advanced personalization orchestration system that coordinates adaptive learning
with real-time medical conversation personalization and optimization.

Core Features:
- Real-time personalization orchestration
- Dynamic intent weighting based on patient patterns
- Communication style adaptation
- Population-level learning insights with privacy protection
- Integration with existing medical_intent_classifier
- Performance optimization and monitoring

Integration Points:
- WorldClassMedicalIntentClassifier for intent weighting
- AdaptiveLearningEngine for pattern recognition
- PatientLearningProfileManager for profile management
"""

import os
import asyncio
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import numpy as np
from collections import defaultdict, deque

# Import adaptive learning components
from adaptive_learning_engine import (
    AdaptiveLearningEngine, 
    CommunicationStyle, 
    PatientCommunicationPattern,
    LearningConfidenceLevel
)
from patient_learning_profiles import PatientLearningProfileManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PersonalizationLevel(str, Enum):
    """Levels of personalization applied"""
    MINIMAL = "minimal"      # Basic adaptation
    MODERATE = "moderate"    # Standard personalization
    ADVANCED = "advanced"    # Full personalization
    EXPERT = "expert"        # Maximum personalization

class AdaptationType(str, Enum):
    """Types of adaptations applied"""
    COMMUNICATION_STYLE = "communication_style"
    INTENT_WEIGHTING = "intent_weighting"
    RESPONSE_FORMALITY = "response_formality"
    TECHNICAL_LEVEL = "technical_level"
    RESPONSE_LENGTH = "response_length"

@dataclass
class PersonalizationResult:
    """Result of personalization application"""
    patient_id: str
    personalization_level: PersonalizationLevel
    adaptations_applied: List[AdaptationType]
    intent_weights_modified: bool
    style_adaptations: Dict[str, Any]
    processing_time_ms: float
    confidence_score: float
    improvement_estimate: float

@dataclass
class PopulationInsight:
    """Anonymized population-level learning insight"""
    insight_type: str
    description: str
    confidence: float
    affected_population_percentage: float
    recommendation: str
    evidence_count: int
    anonymized_patterns: List[str]

class PersonalizationManager:
    """
    🎛️ ADVANCED PERSONALIZATION ORCHESTRATION SYSTEM
    
    Orchestrates all aspects of medical conversation personalization using
    adaptive learning insights and patient communication patterns.
    
    Key Capabilities:
    - Real-time personalization application
    - Dynamic intent classification weighting
    - Communication style adaptation
    - Population-level insights with privacy protection
    - Integration with existing medical AI components
    - Performance monitoring and optimization
    """
    
    def __init__(self, db_client=None, learning_engine: AdaptiveLearningEngine = None, 
                 profile_manager: PatientLearningProfileManager = None):
        self.db = db_client
        self.learning_engine = learning_engine or AdaptiveLearningEngine(db_client)
        self.profile_manager = profile_manager or PatientLearningProfileManager(db_client)
        
        # Personalization configuration
        self.config = {
            'max_personalization_time_ms': 10,  # Target <15ms total
            'min_confidence_for_adaptation': 0.6,
            'population_learning_sample_size': 100,
            'adaptation_strength_factor': 0.8,
            'style_confidence_threshold': 0.7,
            'weight_adjustment_max': 0.3,  # Max 30% weight adjustment
            'anonymization_k_factor': 5  # Minimum group size for insights
        }
        
        # Performance tracking
        self.performance_metrics = {
            'total_personalizations': 0,
            'successful_adaptations': 0,
            'failed_adaptations': 0,
            'avg_processing_time_ms': 0,
            'style_adaptation_rate': 0.0,
            'intent_weight_modifications': 0
        }
        
        # Population learning cache
        self.population_insights_cache = {}
        self.cache_last_updated = datetime.min
        
        logger.info("🎛️ Personalization Manager initialized successfully")

    async def apply_personalization(self, patient_id: str, message: str, context: Dict[str, Any], 
                                  base_response: Dict[str, Any]) -> PersonalizationResult:
        """
        🎯 CORE PERSONALIZATION FUNCTION - Apply real-time personalization
        
        Applies comprehensive personalization to medical conversation based on
        patient learning profile and communication patterns.
        """
        start_time = time.time()
        
        try:
            # Get patient learning profile
            patient_profile = await self.profile_manager.get_profile(patient_id)
            
            if not patient_profile:
                # New patient - minimal personalization
                return PersonalizationResult(
                    patient_id=patient_id,
                    personalization_level=PersonalizationLevel.MINIMAL,
                    adaptations_applied=[],
                    intent_weights_modified=False,
                    style_adaptations={},
                    processing_time_ms=(time.time() - start_time) * 1000,
                    confidence_score=0.5,
                    improvement_estimate=0.0
                )
            
            # Determine personalization level
            personalization_level = self._determine_personalization_level(patient_profile)
            
            # Apply adaptations based on level
            adaptations = []
            style_adaptations = {}
            intent_weights_modified = False
            
            if personalization_level != PersonalizationLevel.MINIMAL:
                # Apply communication style adaptation
                style_adaptation = await self._apply_communication_style_adaptation(
                    patient_profile, base_response
                )
                if style_adaptation:
                    adaptations.append(AdaptationType.COMMUNICATION_STYLE)
                    style_adaptations.update(style_adaptation)
                
                # Apply intent weighting modifications
                intent_weights = await self._apply_intent_weighting(patient_profile, context)
                if intent_weights:
                    adaptations.append(AdaptationType.INTENT_WEIGHTING)
                    intent_weights_modified = True
                    style_adaptations['intent_weights'] = intent_weights
                
                # Apply response formality adaptation
                formality_adaptation = await self._apply_formality_adaptation(
                    patient_profile, base_response
                )
                if formality_adaptation:
                    adaptations.append(AdaptationType.RESPONSE_FORMALITY)
                    style_adaptations.update(formality_adaptation)
                
                # Apply technical level adaptation
                if personalization_level in [PersonalizationLevel.ADVANCED, PersonalizationLevel.EXPERT]:
                    technical_adaptation = await self._apply_technical_level_adaptation(
                        patient_profile, base_response
                    )
                    if technical_adaptation:
                        adaptations.append(AdaptationType.TECHNICAL_LEVEL)
                        style_adaptations.update(technical_adaptation)
            
            # Calculate improvement estimate
            improvement_estimate = self._calculate_improvement_estimate(
                patient_profile, len(adaptations)
            )
            
            # Update performance metrics
            self._update_performance_metrics(adaptations, start_time)
            
            # Log personalization for learning
            await self._log_personalization_outcome(
                patient_id, adaptations, style_adaptations, time.time() - start_time
            )
            
            return PersonalizationResult(
                patient_id=patient_id,
                personalization_level=personalization_level,
                adaptations_applied=adaptations,
                intent_weights_modified=intent_weights_modified,
                style_adaptations=style_adaptations,
                processing_time_ms=(time.time() - start_time) * 1000,
                confidence_score=patient_profile.get('confidence_score', 0.0),
                improvement_estimate=improvement_estimate
            )
            
        except Exception as e:
            logger.error(f"Personalization failed for {patient_id}: {str(e)}")
            self.performance_metrics['failed_adaptations'] += 1
            
            return PersonalizationResult(
                patient_id=patient_id,
                personalization_level=PersonalizationLevel.MINIMAL,
                adaptations_applied=[],
                intent_weights_modified=False,
                style_adaptations={'error': str(e)},
                processing_time_ms=(time.time() - start_time) * 1000,
                confidence_score=0.0,
                improvement_estimate=0.0
            )

    def _determine_personalization_level(self, patient_profile: Dict[str, Any]) -> PersonalizationLevel:
        """Determine appropriate personalization level based on profile maturity"""
        interaction_count = patient_profile.get('interaction_count', 0)
        confidence_score = patient_profile.get('confidence_score', 0.0)
        learning_quality = patient_profile.get('learning_metrics', {}).get('learning_quality_score', 0.0)
        
        # Calculate overall readiness score
        readiness_score = (
            min(1.0, interaction_count / 10.0) * 0.4 +  # Interaction depth
            confidence_score * 0.4 +                    # Confidence level
            learning_quality * 0.2                      # Learning quality
        )
        
        if readiness_score >= 0.85:
            return PersonalizationLevel.EXPERT
        elif readiness_score >= 0.7:
            return PersonalizationLevel.ADVANCED
        elif readiness_score >= 0.5:
            return PersonalizationLevel.MODERATE
        else:
            return PersonalizationLevel.MINIMAL

    async def _apply_communication_style_adaptation(self, patient_profile: Dict[str, Any], 
                                                   base_response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Apply communication style adaptation to response"""
        try:
            communication_style = patient_profile.get('communication_style', 'unknown')
            confidence_score = patient_profile.get('confidence_score', 0.0)
            
            if confidence_score < self.config['min_confidence_for_adaptation']:
                return None
            
            adaptations = {}
            
            if communication_style == 'formal_technical':
                adaptations['tone'] = 'formal_professional'
                adaptations['technical_level'] = 'high'
                adaptations['greeting_style'] = 'formal'
                
            elif communication_style == 'casual_simple':
                adaptations['tone'] = 'friendly_approachable'
                adaptations['technical_level'] = 'low'
                adaptations['greeting_style'] = 'casual'
                adaptations['language_simplification'] = True
                
            elif communication_style == 'formal_simple':
                adaptations['tone'] = 'professional_accessible'
                adaptations['technical_level'] = 'medium'
                adaptations['greeting_style'] = 'polite'
                
            elif communication_style == 'casual_technical':
                adaptations['tone'] = 'friendly_knowledgeable'
                adaptations['technical_level'] = 'high'
                adaptations['greeting_style'] = 'approachable'
            
            return adaptations if adaptations else None
            
        except Exception as e:
            logger.error(f"Communication style adaptation failed: {str(e)}")
            return None

    async def _apply_intent_weighting(self, patient_profile: Dict[str, Any], 
                                    context: Dict[str, Any]) -> Optional[Dict[str, float]]:
        """Apply personalized intent classification weighting"""
        try:
            personalization_weights = patient_profile.get('personalization_weights', {})
            weights_confidence = personalization_weights.get('confidence_in_weights', 0.0)
            
            if weights_confidence < self.config['min_confidence_for_adaptation']:
                return None
            
            # Extract current weights with bounds checking
            max_adjustment = self.config['weight_adjustment_max']
            
            weights = {
                'emergency_detection': max(0.7, min(1.3, personalization_weights.get('emergency_detection_weight', 1.0))),
                'symptom_assessment': max(0.7, min(1.3, personalization_weights.get('symptom_assessment_weight', 1.0))),
                'medication_inquiry': max(0.7, min(1.3, personalization_weights.get('medication_inquiry_weight', 1.0))),
                'general_health': max(0.7, min(1.3, personalization_weights.get('general_health_weight', 1.0))),
                'mental_health': max(0.7, min(1.3, personalization_weights.get('mental_health_weight', 1.0))),
                'specialist_referral': max(0.7, min(1.3, personalization_weights.get('specialist_referral_weight', 1.0)))
            }
            
            return weights
            
        except Exception as e:
            logger.error(f"Intent weighting failed: {str(e)}")
            return None

    async def _apply_formality_adaptation(self, patient_profile: Dict[str, Any], 
                                        base_response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Apply response formality adaptation"""
        try:
            formality_preference = patient_profile.get('formality_preference', 0.5)
            confidence_score = patient_profile.get('confidence_score', 0.0)
            
            if confidence_score < self.config['style_confidence_threshold']:
                return None
            
            adaptations = {}
            
            if formality_preference > 0.7:
                # High formality preference
                adaptations['address_style'] = 'formal'
                adaptations['question_phrasing'] = 'polite_detailed'
                adaptations['recommendation_style'] = 'professional'
                
            elif formality_preference < 0.3:
                # Low formality preference (casual)
                adaptations['address_style'] = 'friendly'
                adaptations['question_phrasing'] = 'conversational'
                adaptations['recommendation_style'] = 'supportive'
            
            return adaptations if adaptations else None
            
        except Exception as e:
            logger.error(f"Formality adaptation failed: {str(e)}")
            return None

    async def _apply_technical_level_adaptation(self, patient_profile: Dict[str, Any], 
                                              base_response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Apply technical complexity adaptation"""
        try:
            technical_preference = patient_profile.get('technical_preference', 0.5)
            vocabulary_complexity = patient_profile.get('vocabulary_complexity', 0.5)
            
            adaptations = {}
            
            # Combine technical preference and vocabulary complexity
            technical_level = (technical_preference + vocabulary_complexity) / 2
            
            if technical_level > 0.7:
                # High technical level
                adaptations['medical_terminology'] = 'advanced'
                adaptations['explanation_depth'] = 'detailed'
                adaptations['clinical_reasoning_visibility'] = 'high'
                
            elif technical_level < 0.3:
                # Low technical level
                adaptations['medical_terminology'] = 'simplified'
                adaptations['explanation_depth'] = 'basic'
                adaptations['clinical_reasoning_visibility'] = 'minimal'
                adaptations['analogies_and_examples'] = True
                
            else:
                # Medium technical level
                adaptations['medical_terminology'] = 'moderate'
                adaptations['explanation_depth'] = 'balanced'
                adaptations['clinical_reasoning_visibility'] = 'medium'
            
            return adaptations if adaptations else None
            
        except Exception as e:
            logger.error(f"Technical level adaptation failed: {str(e)}")
            return None

    def _calculate_improvement_estimate(self, patient_profile: Dict[str, Any], 
                                      adaptation_count: int) -> float:
        """Calculate estimated improvement from personalization"""
        try:
            base_confidence = patient_profile.get('confidence_score', 0.0)
            interaction_count = patient_profile.get('interaction_count', 0)
            
            # Base improvement from personalization
            personalization_boost = adaptation_count * 0.05  # 5% per adaptation
            
            # Maturity factor (more mature profiles benefit more)
            maturity_factor = min(1.0, interaction_count / 15.0)
            
            # Confidence factor (higher confidence = more reliable improvements)
            confidence_factor = base_confidence
            
            estimated_improvement = personalization_boost * maturity_factor * confidence_factor
            
            return min(0.3, estimated_improvement)  # Cap at 30% improvement
            
        except Exception as e:
            logger.error(f"Improvement estimation failed: {str(e)}")
            return 0.0

    async def _log_personalization_outcome(self, patient_id: str, adaptations: List[AdaptationType], 
                                         style_adaptations: Dict[str, Any], processing_time: float):
        """Log personalization outcome for learning"""
        try:
            if self.db is None:
                return
            
            log_entry = {
                'patient_id': patient_id,
                'timestamp': datetime.utcnow(),
                'adaptations_applied': [adaptation.value for adaptation in adaptations],
                'adaptation_count': len(adaptations),
                'style_adaptations': style_adaptations,
                'processing_time_ms': processing_time * 1000,
                'successful_personalization': len(adaptations) > 0
            }
            
            await self.db.conversation_learning_data.update_one(
                {
                    'patient_id': patient_id,
                    'timestamp': {'$gte': datetime.utcnow() - timedelta(seconds=10)}
                },
                {'$set': {'personalization_outcome': log_entry}},
                upsert=False
            )
            
        except Exception as e:
            logger.error(f"Failed to log personalization outcome: {str(e)}")

    def _update_performance_metrics(self, adaptations: List[AdaptationType], start_time: float):
        """Update personalization performance metrics"""
        try:
            self.performance_metrics['total_personalizations'] += 1
            processing_time = (time.time() - start_time) * 1000
            
            if adaptations:
                self.performance_metrics['successful_adaptations'] += 1
                
                # Check for style adaptations
                style_adaptations = [a for a in adaptations if a in [
                    AdaptationType.COMMUNICATION_STYLE, 
                    AdaptationType.RESPONSE_FORMALITY,
                    AdaptationType.TECHNICAL_LEVEL
                ]]
                
                if style_adaptations:
                    total_personalizations = self.performance_metrics['total_personalizations']
                    successful_style = self.performance_metrics.get('style_adaptations', 0) + 1
                    self.performance_metrics['style_adaptations'] = successful_style
                    self.performance_metrics['style_adaptation_rate'] = successful_style / total_personalizations
                
                # Track intent weight modifications
                if AdaptationType.INTENT_WEIGHTING in adaptations:
                    self.performance_metrics['intent_weight_modifications'] += 1
            
            # Update average processing time
            current_avg = self.performance_metrics['avg_processing_time_ms']
            total_events = self.performance_metrics['total_personalizations']
            
            if total_events == 1:
                self.performance_metrics['avg_processing_time_ms'] = processing_time
            else:
                self.performance_metrics['avg_processing_time_ms'] = (
                    (current_avg * (total_events - 1) + processing_time) / total_events
                )
            
        except Exception as e:
            logger.error(f"Failed to update performance metrics: {str(e)}")

    async def generate_population_insights(self, refresh_cache: bool = False) -> List[PopulationInsight]:
        """
        🌍 Generate population-level learning insights with privacy protection
        """
        try:
            # Check cache first
            cache_age = (datetime.utcnow() - self.cache_last_updated).seconds
            if not refresh_cache and cache_age < 3600 and self.population_insights_cache:  # 1 hour cache
                return self.population_insights_cache.get('insights', [])
            
            if self.db is None:
                return []
            
            insights = []
            
            # Get anonymized population data
            pipeline = [
                {'$group': {
                    '_id': '$communication_style',
                    'count': {'$sum': 1},
                    'avg_confidence': {'$avg': '$confidence_score'},
                    'avg_interactions': {'$avg': '$interaction_count'},
                    'avg_success_rate': {'$avg': {'$divide': ['$successful_interactions', '$interaction_count']}}
                }},
                {'$match': {'count': {'$gte': self.config['anonymization_k_factor']}}}  # K-anonymity
            ]
            
            communication_patterns = await self.db.patient_learning_profiles.aggregate(pipeline).to_list(length=20)
            total_profiles = await self.db.patient_learning_profiles.count_documents({})
            
            # Generate insights from communication patterns
            for pattern in communication_patterns:
                style = pattern['_id']
                count = pattern['count']
                percentage = (count / total_profiles) * 100
                
                if percentage > 15:  # Only report significant patterns
                    insights.append(PopulationInsight(
                        insight_type="communication_pattern_prevalence",
                        description=f"{style} communication style represents {percentage:.1f}% of population",
                        confidence=min(0.9, count / 50.0),  # Higher confidence with more data
                        affected_population_percentage=percentage,
                        recommendation=f"Optimize personalization for {style} style interactions",
                        evidence_count=count,
                        anonymized_patterns=[f"style_{style}", f"population_{count}"]
                    ))
            
            # Analyze technical preference trends
            tech_pipeline = [
                {'$bucket': {
                    'groupBy': '$technical_preference',
                    'boundaries': [0, 0.3, 0.7, 1.0],
                    'default': 'other',
                    'output': {
                        'count': {'$sum': 1},
                        'avg_success': {'$avg': {'$divide': ['$successful_interactions', '$interaction_count']}}
                    }
                }}
            ]
            
            tech_preferences = await self.db.patient_learning_profiles.aggregate(tech_pipeline).to_list(length=5)
            
            for bucket in tech_preferences:
                if bucket['count'] >= self.config['anonymization_k_factor']:
                    bucket_id = bucket['_id']
                    count = bucket['count']
                    percentage = (count / total_profiles) * 100
                    
                    if bucket_id == 0:  # Low technical preference
                        tech_level = "simple language"
                    elif bucket_id == 0.3:  # Medium technical preference
                        tech_level = "moderate technical detail"
                    else:  # High technical preference
                        tech_level = "advanced medical terminology"
                    
                    insights.append(PopulationInsight(
                        insight_type="technical_preference_trend",
                        description=f"{percentage:.1f}% of patients prefer {tech_level}",
                        confidence=min(0.9, count / 30.0),
                        affected_population_percentage=percentage,
                        recommendation=f"Ensure personalization algorithms account for {tech_level} preferences",
                        evidence_count=count,
                        anonymized_patterns=[f"tech_level_{bucket_id}", f"success_rate_{bucket['avg_success']:.2f}"]
                    ))
            
            # Cache results
            self.population_insights_cache = {
                'insights': insights,
                'generated_at': datetime.utcnow(),
                'total_population': total_profiles
            }
            self.cache_last_updated = datetime.utcnow()
            
            # Store anonymized insights in population_learning_patterns collection
            await self._store_population_insights(insights)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate population insights: {str(e)}")
            return []

    async def _store_population_insights(self, insights: List[PopulationInsight]):
        """Store anonymized population insights in database"""
        try:
            if not self.db or not insights:
                return
            
            # Prepare insights for storage
            insight_documents = []
            for insight in insights:
                doc = {
                    'insight_id': hashlib.sha256(f"{insight.insight_type}_{insight.description}".encode()).hexdigest()[:16],
                    'insight_type': insight.insight_type,
                    'description': insight.description,
                    'confidence': insight.confidence,
                    'affected_population_percentage': insight.affected_population_percentage,
                    'recommendation': insight.recommendation,
                    'evidence_count': insight.evidence_count,
                    'anonymized_patterns': insight.anonymized_patterns,
                    'generated_at': datetime.utcnow(),
                    'expiry_date': datetime.utcnow() + timedelta(days=30)
                }
                insight_documents.append(doc)
            
            # Store with upsert to avoid duplicates
            for doc in insight_documents:
                await self.db.population_learning_patterns.update_one(
                    {'insight_id': doc['insight_id']},
                    {'$set': doc},
                    upsert=True
                )
            
        except Exception as e:
            logger.error(f"Failed to store population insights: {str(e)}")

    async def get_feedback_integration_report(self) -> Dict[str, Any]:
        """
        📊 Generate comprehensive feedback integration report
        """
        try:
            if not self.db:
                return {'error': 'Database not available'}
            
            # Get recent personalization performance
            recent_conversations = await self.db.conversation_learning_data.find({
                'timestamp': {'$gte': datetime.utcnow() - timedelta(days=7)},
                'personalization_outcome': {'$exists': True}
            }).to_list(length=1000)
            
            # Calculate feedback integration metrics
            total_personalizations = len(recent_conversations)
            successful_personalizations = sum(1 for conv in recent_conversations 
                                           if conv.get('personalization_outcome', {}).get('successful_personalization', False))
            
            # Calculate average processing times
            processing_times = [conv.get('personalization_outcome', {}).get('processing_time_ms', 0) 
                              for conv in recent_conversations]
            avg_processing_time = np.mean(processing_times) if processing_times else 0
            
            # Get adaptation type distribution
            adaptation_counts = defaultdict(int)
            for conv in recent_conversations:
                adaptations = conv.get('personalization_outcome', {}).get('adaptations_applied', [])
                for adaptation in adaptations:
                    adaptation_counts[adaptation] += 1
            
            return {
                'report_period': '7_days',
                'personalization_metrics': {
                    'total_personalizations': total_personalizations,
                    'successful_personalizations': successful_personalizations,
                    'success_rate': successful_personalizations / max(1, total_personalizations),
                    'average_processing_time_ms': avg_processing_time
                },
                'adaptation_distribution': dict(adaptation_counts),
                'performance_targets': {
                    'processing_time_target_ms': self.config['max_personalization_time_ms'],
                    'processing_time_achieved': avg_processing_time <= self.config['max_personalization_time_ms'],
                    'success_rate_target': 0.8,
                    'success_rate_achieved': (successful_personalizations / max(1, total_personalizations)) >= 0.8
                },
                'system_performance': self.performance_metrics,
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate feedback integration report: {str(e)}")
            return {'error': str(e)}

    def get_real_time_personalization_status(self) -> Dict[str, Any]:
        """Get real-time personalization system status"""
        return {
            'system_status': 'active',
            'performance_metrics': self.performance_metrics,
            'cache_status': {
                'population_insights_cached': len(self.population_insights_cache) > 0,
                'cache_age_minutes': (datetime.utcnow() - self.cache_last_updated).seconds / 60
            },
            'configuration': {
                'max_personalization_time_ms': self.config['max_personalization_time_ms'],
                'min_confidence_threshold': self.config['min_confidence_for_adaptation'],
                'weight_adjustment_limit': self.config['weight_adjustment_max']
            },
            'health_check': {
                'learning_engine_available': self.learning_engine is not None,
                'profile_manager_available': self.profile_manager is not None,
                'database_available': self.db is not None
            }
        }