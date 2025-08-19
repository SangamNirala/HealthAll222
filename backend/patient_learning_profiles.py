"""
👤 PATIENT LEARNING PROFILES SYSTEM - STEP 1 IMPLEMENTATION
=========================================================

Advanced patient profile management system that tracks individual learning patterns,
communication styles, and personalization data with privacy-first design.

Core Features:
- Individual patient communication pattern tracking
- Vocabulary preference analysis and storage
- Intent classification accuracy history
- Temporal learning progression analytics
- Personalized confidence calibration data
- Privacy-compliant data management

Database Collections:
- patient_learning_profiles: Individual patient patterns
- conversation_learning_data: Conversation outcomes and feedback
- population_learning_patterns: Anonymized population insights
"""

import os
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from motor.motor_asyncio import AsyncIOMotorClient
import numpy as np
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProfileUpdateType(str, Enum):
    """Types of profile updates"""
    COMMUNICATION_STYLE = "communication_style"
    VOCABULARY_PREFERENCE = "vocabulary_preference"
    INTENT_ACCURACY = "intent_accuracy"
    INTERACTION_OUTCOME = "interaction_outcome"
    CONFIDENCE_CALIBRATION = "confidence_calibration"

@dataclass
class LearningMetrics:
    """Comprehensive learning metrics for patient profiles"""
    total_interactions: int = 0
    successful_interactions: int = 0
    failed_classifications: int = 0
    average_confidence: float = 0.0
    confidence_improvement: float = 0.0
    accuracy_trend: str = "stable"  # improving, declining, stable
    last_interaction_date: Optional[datetime] = None
    learning_velocity: float = 0.0  # How quickly the patient's profile improves

@dataclass
class IntentAccuracyHistory:
    """Track intent classification accuracy over time"""
    intent_type: str
    timestamp: datetime
    predicted_confidence: float
    actual_outcome: str  # success, failure, uncertain
    user_feedback: Optional[str] = None
    conversation_id: str = ""

@dataclass
class PersonalizationWeights:
    """Dynamic personalization weights for intent classification"""
    emergency_detection_weight: float = 1.0
    symptom_assessment_weight: float = 1.0
    medication_inquiry_weight: float = 1.0
    general_health_weight: float = 1.0
    mental_health_weight: float = 1.0
    specialist_referral_weight: float = 1.0
    last_updated: datetime = None
    confidence_in_weights: float = 0.5

class PatientLearningProfileManager:
    """
    🎯 ADVANCED PATIENT LEARNING PROFILE MANAGEMENT SYSTEM
    
    Manages individual patient learning profiles with comprehensive tracking
    of communication patterns, learning progression, and personalization data.
    
    Key Capabilities:
    - Real-time profile updates and retrieval
    - Learning progression analytics
    - Intent accuracy tracking and improvement
    - Communication style evolution monitoring
    - Privacy-compliant data management
    """
    
    def __init__(self, db_client: AsyncIOMotorClient = None):
        self.db = db_client
        
        # Profile management configuration
        self.config = {
            'max_history_entries': 100,
            'confidence_threshold': 0.7,
            'learning_window_days': 30,
            'min_interactions_for_trends': 5,
            'accuracy_improvement_threshold': 0.1,
            'profile_cache_ttl': 300  # 5 minutes
        }
        
        # In-memory cache for frequently accessed profiles
        self.profile_cache = {}
        self.cache_timestamps = {}
        
        logger.info("🎯 Patient Learning Profile Manager initialized")

    async def create_or_update_profile(self, patient_id: str, learning_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        📝 Create new profile or update existing patient learning profile
        """
        try:
            start_time = datetime.utcnow()
            
            # Get existing profile
            existing_profile = await self.get_profile(patient_id)
            
            if existing_profile:
                # Update existing profile
                updated_profile = await self._update_existing_profile(existing_profile, learning_data)
            else:
                # Create new profile
                updated_profile = await self._create_new_profile(patient_id, learning_data)
            
            # Calculate learning metrics
            updated_profile['learning_metrics'] = await self._calculate_learning_metrics(patient_id, updated_profile)
            
            # Update personalization weights
            updated_profile['personalization_weights'] = await self._update_personalization_weights(
                patient_id, updated_profile
            )
            
            # Save to database
            if self.db:
                await self.db.patient_learning_profiles.update_one(
                    {'patient_id': patient_id},
                    {'$set': updated_profile},
                    upsert=True
                )
            
            # Update cache
            self._update_profile_cache(patient_id, updated_profile)
            
            # Log conversation learning data
            await self._log_conversation_learning_data(patient_id, learning_data)
            
            processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            return {
                'status': 'success',
                'patient_id': patient_id,
                'profile_updated': True,
                'learning_metrics': updated_profile.get('learning_metrics', {}),
                'processing_time_ms': processing_time,
                'profile_confidence': updated_profile.get('confidence_score', 0.0)
            }
            
        except Exception as e:
            logger.error(f"Failed to create/update profile for {patient_id}: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'patient_id': patient_id
            }

    async def get_profile(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """
        📋 Get comprehensive patient learning profile
        """
        try:
            # Check cache first
            cached_profile = self._get_from_cache(patient_id)
            if cached_profile:
                return cached_profile
            
            # Get from database
            if self.db:
                profile = await self.db.patient_learning_profiles.find_one({'patient_id': patient_id})
                if profile:
                    profile.pop('_id', None)
                    self._update_profile_cache(patient_id, profile)
                    return profile
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get profile for {patient_id}: {str(e)}")
            return None

    async def _create_new_profile(self, patient_id: str, learning_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new patient learning profile"""
        return {
            'patient_id': patient_id,
            'created_at': datetime.utcnow(),
            'last_updated': datetime.utcnow(),
            
            # Communication patterns
            'communication_style': learning_data.get('communication_style', 'unknown'),
            'vocabulary_complexity': learning_data.get('vocabulary_complexity', 0.5),
            'technical_preference': learning_data.get('technical_preference', 0.5),
            'formality_preference': learning_data.get('formality_preference', 0.5),
            'response_length_preference': learning_data.get('response_length_preference', 'medium'),
            
            # Learning history
            'symptom_description_patterns': learning_data.get('symptom_patterns', [])[:10],
            'common_phrases': learning_data.get('common_phrases', [])[:20],
            'vocabulary_preferences': learning_data.get('vocabulary_preferences', []),
            
            # Interaction tracking
            'interaction_count': 1,
            'total_conversation_time': learning_data.get('conversation_time', 0),
            'successful_interactions': 1 if learning_data.get('success', False) else 0,
            'failed_interactions': 0 if learning_data.get('success', False) else 1,
            
            # Confidence and accuracy
            'confidence_score': learning_data.get('confidence_score', 0.6),
            'intent_accuracy_history': [],
            'confidence_calibration_data': {
                'initial_confidence': learning_data.get('confidence_score', 0.6),
                'calibrated_confidence': learning_data.get('confidence_score', 0.6),
                'calibration_factor': 1.0,
                'last_calibration': datetime.utcnow()
            },
            
            # Privacy and preferences
            'privacy_level': learning_data.get('privacy_level', 'standard'),
            'learning_consent': learning_data.get('learning_consent', True),
            
            # Temporal patterns
            'interaction_time_patterns': {
                'preferred_hours': [],
                'session_durations': [],
                'response_times': []
            }
        }

    async def _update_existing_profile(self, existing_profile: Dict[str, Any], learning_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing patient learning profile with new learning data"""
        
        # Update interaction counts
        existing_profile['interaction_count'] = existing_profile.get('interaction_count', 0) + 1
        existing_profile['last_updated'] = datetime.utcnow()
        
        # Update communication patterns with weighted average (favor recent interactions)
        decay_factor = 0.9  # Weight for existing data
        new_factor = 0.1    # Weight for new data
        
        if learning_data.get('vocabulary_complexity') is not None:
            existing_profile['vocabulary_complexity'] = (
                decay_factor * existing_profile.get('vocabulary_complexity', 0.5) +
                new_factor * learning_data['vocabulary_complexity']
            )
        
        if learning_data.get('technical_preference') is not None:
            existing_profile['technical_preference'] = (
                decay_factor * existing_profile.get('technical_preference', 0.5) +
                new_factor * learning_data['technical_preference']
            )
        
        if learning_data.get('formality_preference') is not None:
            existing_profile['formality_preference'] = (
                decay_factor * existing_profile.get('formality_preference', 0.5) +
                new_factor * learning_data['formality_preference']
            )
        
        # Update communication style if confidence is high enough
        if learning_data.get('confidence_score', 0) > 0.8:
            existing_profile['communication_style'] = learning_data.get('communication_style', 
                                                                     existing_profile.get('communication_style'))
        
        # Update symptom patterns (keep top 10 most frequent)
        existing_patterns = existing_profile.get('symptom_description_patterns', [])
        new_patterns = learning_data.get('symptom_patterns', [])
        
        # Combine and deduplicate patterns
        all_patterns = existing_patterns + new_patterns
        pattern_counts = defaultdict(int)
        for pattern in all_patterns:
            pattern_counts[pattern] += 1
        
        # Keep top 10 most frequent patterns
        top_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        existing_profile['symptom_description_patterns'] = [pattern for pattern, _ in top_patterns]
        
        # Update conversation time tracking
        conversation_time = learning_data.get('conversation_time', 0)
        existing_profile['total_conversation_time'] = (
            existing_profile.get('total_conversation_time', 0) + conversation_time
        )
        
        # Track interaction outcomes
        if learning_data.get('success', False):
            existing_profile['successful_interactions'] = existing_profile.get('successful_interactions', 0) + 1
        else:
            existing_profile['failed_interactions'] = existing_profile.get('failed_interactions', 0) + 1
        
        # Update confidence score with moving average
        existing_confidence = existing_profile.get('confidence_score', 0.6)
        new_confidence = learning_data.get('confidence_score', existing_confidence)
        existing_profile['confidence_score'] = (
            decay_factor * existing_confidence + new_factor * new_confidence
        )
        
        return existing_profile

    async def _calculate_learning_metrics(self, patient_id: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive learning metrics for the patient"""
        try:
            total_interactions = profile.get('interaction_count', 0)
            successful_interactions = profile.get('successful_interactions', 0)
            failed_interactions = profile.get('failed_interactions', 0)
            
            # Calculate success rate
            success_rate = (successful_interactions / total_interactions) if total_interactions > 0 else 0.0
            
            # Calculate accuracy trend
            accuracy_trend = await self._calculate_accuracy_trend(patient_id)
            
            # Calculate learning velocity (improvement over time)
            learning_velocity = await self._calculate_learning_velocity(patient_id)
            
            # Calculate confidence improvement
            confidence_improvement = await self._calculate_confidence_improvement(patient_id)
            
            return {
                'total_interactions': total_interactions,
                'successful_interactions': successful_interactions,
                'failed_classifications': failed_interactions,
                'success_rate': success_rate,
                'average_confidence': profile.get('confidence_score', 0.0),
                'confidence_improvement': confidence_improvement,
                'accuracy_trend': accuracy_trend,
                'last_interaction_date': profile.get('last_updated'),
                'learning_velocity': learning_velocity,
                'profile_maturity': min(1.0, total_interactions / 20.0),  # Mature after 20 interactions
                'learning_quality_score': self._calculate_learning_quality(profile)
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate learning metrics: {str(e)}")
            return {}

    async def _calculate_accuracy_trend(self, patient_id: str) -> str:
        """Calculate accuracy trend over recent interactions"""
        try:
            if self.db is None:
                return "stable"
            
            # Get recent conversation data
            recent_conversations = await self.db.conversation_learning_data.find({
                'patient_id': patient_id,
                'timestamp': {'$gte': datetime.utcnow() - timedelta(days=7)}
            }).sort('timestamp', -1).limit(10).to_list(length=10)
            
            if len(recent_conversations) < 3:
                return "stable"
            
            # Calculate trend in accuracy scores
            accuracies = [conv.get('intent_accuracy', 0.0) for conv in recent_conversations]
            
            # Simple linear trend calculation
            x = list(range(len(accuracies)))
            slope = np.polyfit(x, accuracies, 1)[0]
            
            if slope > 0.05:
                return "improving"
            elif slope < -0.05:
                return "declining"
            else:
                return "stable"
                
        except Exception as e:
            logger.error(f"Failed to calculate accuracy trend: {str(e)}")
            return "stable"

    async def _calculate_learning_velocity(self, patient_id: str) -> float:
        """Calculate how quickly the patient's profile is improving"""
        try:
            if self.db is None:
                return 0.0
            
            # Get conversation data from last 30 days
            conversations = await self.db.conversation_learning_data.find({
                'patient_id': patient_id,
                'timestamp': {'$gte': datetime.utcnow() - timedelta(days=30)}
            }).sort('timestamp', 1).to_list(length=50)
            
            if len(conversations) < 5:
                return 0.0
            
            # Calculate improvement rate in confidence scores
            confidences = [conv.get('intent_accuracy', 0.0) for conv in conversations]
            
            # Calculate velocity as improvement per interaction
            first_half = np.mean(confidences[:len(confidences)//2])
            second_half = np.mean(confidences[len(confidences)//2:])
            
            velocity = (second_half - first_half) / (len(confidences) / 2)
            return max(0.0, min(1.0, velocity))  # Normalize to 0-1 range
            
        except Exception as e:
            logger.error(f"Failed to calculate learning velocity: {str(e)}")
            return 0.0

    async def _calculate_confidence_improvement(self, patient_id: str) -> float:
        """Calculate improvement in confidence calibration"""
        try:
            profile = await self.get_profile(patient_id)
            if not profile:
                return 0.0
            
            calibration_data = profile.get('confidence_calibration_data', {})
            initial_confidence = calibration_data.get('initial_confidence', 0.6)
            current_confidence = profile.get('confidence_score', 0.6)
            
            improvement = current_confidence - initial_confidence
            return max(-1.0, min(1.0, improvement))  # Normalize to -1 to 1 range
            
        except Exception as e:
            logger.error(f"Failed to calculate confidence improvement: {str(e)}")
            return 0.0

    def _calculate_learning_quality(self, profile: Dict[str, Any]) -> float:
        """Calculate overall learning quality score"""
        try:
            # Factors that indicate good learning
            interaction_count = profile.get('interaction_count', 0)
            confidence_score = profile.get('confidence_score', 0.0)
            success_rate = profile.get('successful_interactions', 0) / max(1, interaction_count)
            pattern_richness = len(profile.get('symptom_description_patterns', []))
            
            # Weighted quality score
            quality_score = (
                min(1.0, interaction_count / 10.0) * 0.3 +  # Interaction depth
                confidence_score * 0.4 +                    # Confidence level
                success_rate * 0.2 +                        # Success rate
                min(1.0, pattern_richness / 5.0) * 0.1     # Pattern diversity
            )
            
            return quality_score
            
        except Exception as e:
            logger.error(f"Failed to calculate learning quality: {str(e)}")
            return 0.5

    async def _update_personalization_weights(self, patient_id: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Update personalized intent classification weights"""
        try:
            # Get existing weights or create defaults
            existing_weights = profile.get('personalization_weights', {})
            
            # Calculate new weights based on communication style and preferences
            communication_style = profile.get('communication_style', 'unknown')
            technical_preference = profile.get('technical_preference', 0.5)
            formality_preference = profile.get('formality_preference', 0.5)
            
            # Base weights
            weights = PersonalizationWeights()
            
            # Adjust weights based on communication style
            if communication_style == 'formal_technical':
                weights.symptom_assessment_weight = 1.2
                weights.medication_inquiry_weight = 1.15
                weights.specialist_referral_weight = 1.1
            elif communication_style == 'casual_simple':
                weights.general_health_weight = 1.2
                weights.mental_health_weight = 1.1
                weights.emergency_detection_weight = 1.05
            elif communication_style == 'formal_simple':
                weights.general_health_weight = 1.1
                weights.symptom_assessment_weight = 1.05
            elif communication_style == 'casual_technical':
                weights.medication_inquiry_weight = 1.1
                weights.specialist_referral_weight = 1.05
            
            # Fine-tune based on preferences
            if technical_preference > 0.7:
                weights.symptom_assessment_weight *= 1.1
                weights.medication_inquiry_weight *= 1.05
            elif technical_preference < 0.3:
                weights.general_health_weight *= 1.1
                weights.mental_health_weight *= 1.05
            
            # Calculate confidence in weights based on interaction count and success rate
            interaction_count = profile.get('interaction_count', 0)
            success_rate = profile.get('successful_interactions', 0) / max(1, interaction_count)
            
            weights.confidence_in_weights = min(0.95, (interaction_count / 15.0) * success_rate)
            weights.last_updated = datetime.utcnow()
            
            return asdict(weights)
            
        except Exception as e:
            logger.error(f"Failed to update personalization weights: {str(e)}")
            return asdict(PersonalizationWeights())

    async def _log_conversation_learning_data(self, patient_id: str, learning_data: Dict[str, Any]):
        """Log detailed conversation learning data for analysis"""
        try:
            if not self.db:
                return
            
            conversation_entry = {
                'patient_id': patient_id,
                'conversation_id': learning_data.get('conversation_id', f"conv_{int(datetime.utcnow().timestamp())}"),
                'timestamp': datetime.utcnow(),
                
                # Learning outcomes
                'intent_accuracy': learning_data.get('intent_accuracy', 0.0),
                'confidence_score': learning_data.get('confidence_score', 0.0),
                'style_match_score': learning_data.get('style_match_score', 0.0),
                'processing_time_ms': learning_data.get('processing_time_ms', 0),
                
                # Interaction details
                'message_length': learning_data.get('message_length', 0),
                'technical_terms_count': learning_data.get('technical_terms_count', 0),
                'formality_indicators': learning_data.get('formality_indicators', {}),
                
                # Outcomes and feedback
                'successful_classification': learning_data.get('success', False),
                'user_feedback': learning_data.get('user_feedback'),
                'improvement_opportunities': learning_data.get('improvement_opportunities', []),
                
                # Pattern discoveries
                'new_patterns_discovered': learning_data.get('new_patterns', []),
                'communication_adaptations': learning_data.get('adaptations', [])
            }
            
            await self.db.conversation_learning_data.insert_one(conversation_entry)
            
        except Exception as e:
            logger.error(f"Failed to log conversation learning data: {str(e)}")

    def _get_from_cache(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Get profile from cache if valid"""
        if patient_id not in self.profile_cache:
            return None
        
        cache_time = self.cache_timestamps.get(patient_id, datetime.min)
        if (datetime.utcnow() - cache_time).seconds > self.config['profile_cache_ttl']:
            # Cache expired
            self.profile_cache.pop(patient_id, None)
            self.cache_timestamps.pop(patient_id, None)
            return None
        
        return self.profile_cache[patient_id]

    def _update_profile_cache(self, patient_id: str, profile: Dict[str, Any]):
        """Update profile cache"""
        self.profile_cache[patient_id] = profile
        self.cache_timestamps[patient_id] = datetime.utcnow()
        
        # Keep cache size reasonable
        if len(self.profile_cache) > 100:
            # Remove oldest entry
            oldest_id = min(self.cache_timestamps.items(), key=lambda x: x[1])[0]
            self.profile_cache.pop(oldest_id, None)
            self.cache_timestamps.pop(oldest_id, None)

    async def get_patient_insights(self, patient_id: str) -> Dict[str, Any]:
        """
        🧠 Get comprehensive patient learning insights
        """
        try:
            profile = await self.get_profile(patient_id)
            if not profile:
                return {'error': 'Patient profile not found'}
            
            # Generate insights based on profile data
            insights = {
                'patient_id': patient_id,
                'profile_summary': {
                    'communication_style': profile.get('communication_style', 'unknown'),
                    'interaction_count': profile.get('interaction_count', 0),
                    'confidence_score': profile.get('confidence_score', 0.0),
                    'learning_quality': profile.get('learning_metrics', {}).get('learning_quality_score', 0.0)
                },
                
                'communication_insights': {
                    'preferred_style': profile.get('communication_style', 'unknown'),
                    'technical_preference': profile.get('technical_preference', 0.5),
                    'formality_level': profile.get('formality_preference', 0.5),
                    'response_preference': profile.get('response_length_preference', 'medium')
                },
                
                'learning_progress': {
                    'accuracy_trend': profile.get('learning_metrics', {}).get('accuracy_trend', 'stable'),
                    'learning_velocity': profile.get('learning_metrics', {}).get('learning_velocity', 0.0),
                    'confidence_improvement': profile.get('learning_metrics', {}).get('confidence_improvement', 0.0),
                    'profile_maturity': profile.get('learning_metrics', {}).get('profile_maturity', 0.0)
                },
                
                'personalization_status': {
                    'weights_confidence': profile.get('personalization_weights', {}).get('confidence_in_weights', 0.0),
                    'active_adaptations': len(profile.get('symptom_description_patterns', [])),
                    'last_updated': profile.get('last_updated', datetime.utcnow()).isoformat()
                }
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to get patient insights: {str(e)}")
            return {'error': str(e)}

    async def get_learning_analytics(self) -> Dict[str, Any]:
        """
        📊 Get system-wide learning analytics
        """
        try:
            if not self.db:
                return {'error': 'Database not available'}
            
            # Get aggregated statistics
            total_profiles = await self.db.patient_learning_profiles.count_documents({})
            
            # Get profiles with different confidence levels
            high_confidence_profiles = await self.db.patient_learning_profiles.count_documents({
                'confidence_score': {'$gte': 0.8}
            })
            
            # Get recent activity (last 7 days)
            recent_activity = await self.db.conversation_learning_data.count_documents({
                'timestamp': {'$gte': datetime.utcnow() - timedelta(days=7)}
            })
            
            # Calculate average metrics
            pipeline = [
                {'$group': {
                    '_id': None,
                    'avg_interactions': {'$avg': '$interaction_count'},
                    'avg_confidence': {'$avg': '$confidence_score'},
                    'avg_success_rate': {'$avg': {'$divide': ['$successful_interactions', '$interaction_count']}}
                }}
            ]
            
            avg_metrics = await self.db.patient_learning_profiles.aggregate(pipeline).to_list(length=1)
            avg_data = avg_metrics[0] if avg_metrics else {}
            
            return {
                'system_overview': {
                    'total_learning_profiles': total_profiles,
                    'high_confidence_profiles': high_confidence_profiles,
                    'confidence_rate': high_confidence_profiles / max(1, total_profiles),
                    'recent_activity_7d': recent_activity
                },
                
                'performance_metrics': {
                    'average_interactions_per_profile': avg_data.get('avg_interactions', 0.0),
                    'average_confidence_score': avg_data.get('avg_confidence', 0.0),
                    'average_success_rate': avg_data.get('avg_success_rate', 0.0)
                },
                
                'cache_performance': {
                    'cached_profiles': len(self.profile_cache),
                    'cache_utilization': len(self.profile_cache) / max(1, total_profiles)
                },
                
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get learning analytics: {str(e)}")
            return {'error': str(e)}