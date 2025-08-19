"""
📈 PATTERN EVOLUTION TRACKER - STEP 2 IMPLEMENTATION
=================================================

Temporal pattern evolution tracking system for medical AI adaptive learning.
Tracks how medical language changes over time, analyzes trends, and provides
population-level learning insights with privacy protection.

Advanced Capabilities:
- Temporal Pattern Evolution: Track medical language changes over time
- Trend Analysis: Advanced statistical analysis of pattern evolution
- Population-level Learning: Aggregate anonymized insights across patients
- Medical Language Evolution: Track vocabulary and terminology changes
- Privacy-compliant Cross-patient Learning: K-anonymity protection

Algorithm Version: 2.0_temporal_pattern_evolution
"""

import os
import asyncio
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
from collections import defaultdict, deque, Counter
import google.generativeai as genai
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from scipy import stats
from scipy.stats import linregress, pearsonr
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EvolutionTrend(str, Enum):
    """Types of pattern evolution trends"""
    EMERGING = "emerging"        # New patterns gaining popularity
    GROWING = "growing"          # Established patterns increasing usage
    STABLE = "stable"           # Consistent usage over time
    DECLINING = "declining"     # Decreasing usage
    OBSOLETE = "obsolete"       # No longer used
    CYCLICAL = "cyclical"       # Seasonal or cyclical patterns
    VOLATILE = "volatile"       # Highly variable usage

class PatternLifecycleStage(str, Enum):
    """Stages in pattern lifecycle"""
    DISCOVERY = "discovery"      # Just discovered
    VALIDATION = "validation"    # Being validated
    ADOPTION = "adoption"        # Being adopted by users
    MATURITY = "maturity"       # Widespread usage
    DECLINE = "decline"         # Usage declining
    RETIREMENT = "retirement"   # No longer recommended

@dataclass
class EvolutionMetrics:
    """Metrics for tracking pattern evolution"""
    pattern_id: str
    usage_trend: EvolutionTrend
    lifecycle_stage: PatternLifecycleStage
    usage_velocity: float           # Rate of change in usage
    adoption_rate: float           # Speed of adoption
    retention_rate: float          # How well pattern is retained
    geographic_spread: int         # Number of regions using pattern
    demographic_diversity: float  # Diversity of users
    medical_validation_score: float # Clinical validation
    confidence_evolution: List[Tuple[datetime, float]]  # Confidence over time

@dataclass
class TemporalPatternInsight:
    """Insights from temporal pattern analysis"""
    insight_type: str
    pattern_ids: List[str]
    time_window: str
    trend_description: str
    statistical_significance: float
    medical_impact: float
    recommendation: str
    supporting_data: Dict[str, Any]
    confidence_level: float

@dataclass  
class PopulationLearningInsight:
    """Population-level learning insights with privacy protection"""
    insight_id: str
    insight_category: str
    description: str
    affected_pattern_count: int
    anonymized_patient_count: int
    statistical_confidence: float
    medical_significance: float
    actionable_recommendation: str
    privacy_protection_level: str
    discovery_date: datetime

class PatternEvolutionTracker:
    """
    📊 TEMPORAL PATTERN EVOLUTION TRACKING SYSTEM
    
    Advanced analytics system that tracks how medical conversation patterns
    evolve over time, identifies trends, and provides population-level insights
    while maintaining strict privacy protection.
    
    Key Features:
    - Temporal evolution analysis with statistical significance
    - Population-level learning with K-anonymity protection
    - Medical language trend detection and prediction
    - Pattern lifecycle management and optimization
    - Privacy-compliant cross-patient insights
    """
    
    def __init__(self, db_client: AsyncIOMotorClient = None):
        self.db = db_client
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        # Initialize Gemini AI for trend analysis
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Evolution tracking configuration
        self.config = {
            'min_data_points_for_trend': 5,
            'trend_analysis_window_days': 30,
            'population_min_sample_size': 10,
            'k_anonymity_threshold': 5,  # Privacy protection
            'statistical_significance_threshold': 0.05,
            'medical_significance_threshold': 0.6,
            'trend_sensitivity': 0.1,  # Minimum change to consider significant
            'max_evolution_cache_size': 1000
        }
        
        # Analytics cache
        self.evolution_cache = {}
        self.trend_analysis_cache = {}
        self.population_insights_cache = {}
        self.cache_last_updated = None
        
        # Statistical models
        self.scaler = MinMaxScaler()
        
        # Performance tracking
        self.analytics_metrics = {
            'trends_analyzed': 0,
            'population_insights_generated': 0,
            'statistical_models_updated': 0,
            'privacy_violations_prevented': 0,
            'avg_analysis_time_ms': 0.0
        }
        
        logger.info("📈 Pattern Evolution Tracker initialized with temporal analysis capabilities")

    async def track_pattern_evolution(self, time_window_days: int = 30) -> Dict[str, Any]:
        """
        🕐 COMPREHENSIVE PATTERN EVOLUTION ANALYSIS
        
        Analyzes how patterns have evolved over the specified time window,
        identifying trends, lifecycle changes, and population-level insights.
        """
        start_time = time.time()
        
        try:
            # Get pattern evolution data
            evolution_data = await self._get_pattern_evolution_data(time_window_days)
            
            # Analyze temporal trends
            trend_analysis = await self._analyze_temporal_trends(evolution_data)
            
            # Track pattern lifecycles
            lifecycle_analysis = await self._analyze_pattern_lifecycles(evolution_data)
            
            # Generate population-level insights
            population_insights = await self._generate_population_insights(evolution_data)
            
            # Predict future trends
            trend_predictions = await self._predict_future_trends(evolution_data)
            
            # Generate medical language evolution insights
            language_evolution = await self._analyze_medical_language_evolution(evolution_data)
            
            processing_time = (time.time() - start_time) * 1000
            
            # Update performance metrics
            self._update_analytics_metrics(len(trend_analysis), processing_time)
            
            return {
                'status': 'success',
                'time_window_days': time_window_days,
                'patterns_analyzed': len(evolution_data),
                'temporal_trends': trend_analysis,
                'lifecycle_analysis': lifecycle_analysis,
                'population_insights': [asdict(insight) for insight in population_insights],
                'trend_predictions': trend_predictions,
                'medical_language_evolution': language_evolution,
                'processing_time_ms': processing_time,
                'algorithm_version': '2.0_temporal_pattern_evolution'
            }
            
        except Exception as e:
            logger.error(f"Pattern evolution tracking failed: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'processing_time_ms': (time.time() - start_time) * 1000
            }

    async def _get_pattern_evolution_data(self, time_window_days: int) -> Dict[str, Any]:
        """
        📊 Retrieve pattern evolution data from database
        """
        if self.db is None:
            return {}
        
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=time_window_days)
            
            # Get pattern discovery and usage events
            evolution_events = await self.db.pattern_evolution_events.find({
                'timestamp': {'$gte': start_date, '$lte': end_date}
            }).sort('timestamp', 1).to_list(length=None)
            
            # Get current pattern states
            current_patterns = await self.db.discovered_patterns.find({
                'discovery_date': {'$gte': start_date - timedelta(days=90)}  # Extended window for context
            }).to_list(length=None)
            
            # Organize data by pattern
            pattern_evolution = defaultdict(lambda: {
                'events': [],
                'usage_history': [],
                'confidence_history': [],
                'current_state': None
            })
            
            # Process events
            for event in evolution_events:
                pattern_id = event['pattern_id']
                pattern_evolution[pattern_id]['events'].append(event)
                
                if event['event_type'] in ['discovered', 'usage_updated']:
                    pattern_evolution[pattern_id]['usage_history'].append({
                        'timestamp': event['timestamp'],
                        'usage_count': event.get('usage_count', 1),
                        'confidence': event.get('confidence', 0.5)
                    })
            
            # Process current states
            for pattern in current_patterns:
                pattern_id = pattern['pattern_id']
                pattern_evolution[pattern_id]['current_state'] = pattern
            
            return dict(pattern_evolution)
            
        except Exception as e:
            logger.error(f"Failed to retrieve pattern evolution data: {str(e)}")
            return {}

    async def _analyze_temporal_trends(self, evolution_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        📈 Analyze temporal trends in pattern evolution
        """
        trend_analysis = {
            'emerging_patterns': [],
            'declining_patterns': [],
            'stable_patterns': [],
            'cyclical_patterns': [],
            'trend_statistics': {}
        }
        
        pattern_trends = []
        
        for pattern_id, data in evolution_data.items():
            usage_history = data.get('usage_history', [])
            
            if len(usage_history) < self.config['min_data_points_for_trend']:
                continue
            
            # Prepare time series data
            timestamps = [entry['timestamp'] for entry in usage_history]
            usage_counts = [entry['usage_count'] for entry in usage_history]
            
            # Convert timestamps to ordinal for regression
            time_ordinals = [(ts - timestamps[0]).total_seconds() / 86400 for ts in timestamps]
            
            if len(time_ordinals) >= 3:  # Minimum for trend analysis
                # Linear regression for trend detection
                slope, intercept, r_value, p_value, std_err = linregress(time_ordinals, usage_counts)
                
                # Classify trend
                trend = self._classify_trend(slope, r_value, p_value)
                
                pattern_analysis = {
                    'pattern_id': pattern_id,
                    'trend': trend.value,
                    'slope': float(slope),
                    'correlation': float(r_value),
                    'p_value': float(p_value),
                    'statistical_significance': p_value < self.config['statistical_significance_threshold'],
                    'usage_velocity': float(slope),
                    'pattern_text': data.get('current_state', {}).get('pattern_text', 'Unknown')
                }
                
                pattern_trends.append(pattern_analysis)
                
                # Categorize by trend
                if trend == EvolutionTrend.EMERGING or trend == EvolutionTrend.GROWING:
                    trend_analysis['emerging_patterns'].append(pattern_analysis)
                elif trend == EvolutionTrend.DECLINING:
                    trend_analysis['declining_patterns'].append(pattern_analysis)
                elif trend == EvolutionTrend.STABLE:
                    trend_analysis['stable_patterns'].append(pattern_analysis)
                elif trend == EvolutionTrend.CYCLICAL:
                    trend_analysis['cyclical_patterns'].append(pattern_analysis)
        
        # Overall trend statistics
        if pattern_trends:
            slopes = [t['slope'] for t in pattern_trends]
            correlations = [t['correlation'] for t in pattern_trends]
            
            trend_analysis['trend_statistics'] = {
                'total_patterns_analyzed': len(pattern_trends),
                'avg_trend_slope': float(np.mean(slopes)),
                'trend_slope_std': float(np.std(slopes)),
                'avg_correlation': float(np.mean(correlations)),
                'significant_trends': sum(1 for t in pattern_trends if t['statistical_significance'])
            }
        
        return trend_analysis

    def _classify_trend(self, slope: float, r_value: float, p_value: float) -> EvolutionTrend:
        """
        Classify trend based on statistical analysis
        """
        significance_threshold = self.config['statistical_significance_threshold']
        sensitivity = self.config['trend_sensitivity']
        
        # Check statistical significance
        if p_value > significance_threshold:
            return EvolutionTrend.STABLE
        
        # Check correlation strength
        abs_correlation = abs(r_value)
        
        if abs_correlation < 0.3:  # Weak correlation
            return EvolutionTrend.VOLATILE
        elif abs_correlation > 0.8 and abs(slope) > sensitivity:  # Strong correlation with significant slope
            if slope > 0:
                return EvolutionTrend.GROWING if slope < 2 * sensitivity else EvolutionTrend.EMERGING
            else:
                return EvolutionTrend.DECLINING
        else:
            return EvolutionTrend.STABLE

    async def _analyze_pattern_lifecycles(self, evolution_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        🔄 Analyze pattern lifecycles and stages
        """
        lifecycle_analysis = {
            'lifecycle_distribution': defaultdict(int),
            'pattern_lifecycles': [],
            'lifecycle_insights': []
        }
        
        for pattern_id, data in evolution_data.items():
            current_state = data.get('current_state')
            if not current_state:
                continue
            
            # Determine lifecycle stage
            discovery_date = current_state.get('discovery_date')
            usage_frequency = current_state.get('usage_frequency', 0)
            confidence = current_state.get('validation_score', 0.0)
            
            if discovery_date:
                days_since_discovery = (datetime.utcnow() - discovery_date).days
                
                lifecycle_stage = self._determine_lifecycle_stage(
                    days_since_discovery, usage_frequency, confidence
                )
                
                lifecycle_analysis['lifecycle_distribution'][lifecycle_stage.value] += 1
                lifecycle_analysis['pattern_lifecycles'].append({
                    'pattern_id': pattern_id,
                    'lifecycle_stage': lifecycle_stage.value,
                    'days_since_discovery': days_since_discovery,
                    'usage_frequency': usage_frequency,
                    'confidence': confidence,
                    'pattern_text': current_state.get('pattern_text', 'Unknown')
                })
        
        # Generate lifecycle insights
        total_patterns = len(lifecycle_analysis['pattern_lifecycles'])
        if total_patterns > 0:
            for stage, count in lifecycle_analysis['lifecycle_distribution'].items():
                percentage = (count / total_patterns) * 100
                lifecycle_analysis['lifecycle_insights'].append({
                    'stage': stage,
                    'count': count,
                    'percentage': round(percentage, 2),
                    'insight': self._generate_lifecycle_insight(stage, percentage)
                })
        
        return lifecycle_analysis

    def _determine_lifecycle_stage(self, days_since_discovery: int, usage_frequency: int, confidence: float) -> PatternLifecycleStage:
        """
        Determine pattern lifecycle stage based on metrics
        """
        if days_since_discovery <= 7 and usage_frequency < 5:
            return PatternLifecycleStage.DISCOVERY
        elif days_since_discovery <= 30 and confidence < 0.7:
            return PatternLifecycleStage.VALIDATION
        elif days_since_discovery <= 90 and usage_frequency < 20:
            return PatternLifecycleStage.ADOPTION
        elif usage_frequency >= 20 and confidence >= 0.8:
            return PatternLifecycleStage.MATURITY
        elif usage_frequency < 5 and days_since_discovery > 90:
            return PatternLifecycleStage.DECLINE
        else:
            return PatternLifecycleStage.RETIREMENT

    def _generate_lifecycle_insight(self, stage: str, percentage: float) -> str:
        """
        Generate insight description for lifecycle stage
        """
        insights = {
            'discovery': f"Discovery stage represents {percentage}% of patterns - indicating active pattern identification",
            'validation': f"Validation stage at {percentage}% shows healthy pattern verification process",
            'adoption': f"Adoption stage at {percentage}% indicates good pattern uptake",
            'maturity': f"Maturity stage at {percentage}% shows stable, validated patterns",
            'decline': f"Decline stage at {percentage}% suggests some patterns losing relevance",
            'retirement': f"Retirement stage at {percentage}% indicates outdated pattern cleanup"
        }
        return insights.get(stage, f"Stage {stage} represents {percentage}% of patterns")

    async def _generate_population_insights(self, evolution_data: Dict[str, Any]) -> List[PopulationLearningInsight]:
        """
        👥 Generate population-level learning insights with privacy protection
        """
        insights = []
        
        if self.db is None or len(evolution_data) < self.config['population_min_sample_size']:
            return insights
        
        try:
            # Privacy-protected pattern usage analysis
            usage_patterns = await self._analyze_population_usage_patterns(evolution_data)
            
            # Medical significance trends across population
            medical_trends = await self._analyze_population_medical_trends(evolution_data)
            
            # Communication style evolution
            communication_evolution = await self._analyze_population_communication_evolution(evolution_data)
            
            # Generate insights from analyses
            if usage_patterns:
                insights.append(PopulationLearningInsight(
                    insight_id=f"usage_pattern_{datetime.utcnow().strftime('%Y%m%d')}",
                    insight_category="usage_patterns",
                    description=usage_patterns['description'],
                    affected_pattern_count=usage_patterns['pattern_count'],
                    anonymized_patient_count=usage_patterns['patient_count'],
                    statistical_confidence=usage_patterns['confidence'],
                    medical_significance=usage_patterns['medical_significance'],
                    actionable_recommendation=usage_patterns['recommendation'],
                    privacy_protection_level="k_anonymity_5",
                    discovery_date=datetime.utcnow()
                ))
            
            if medical_trends:
                insights.append(PopulationLearningInsight(
                    insight_id=f"medical_trend_{datetime.utcnow().strftime('%Y%m%d')}",
                    insight_category="medical_trends",
                    description=medical_trends['description'],
                    affected_pattern_count=medical_trends['pattern_count'],
                    anonymized_patient_count=medical_trends['patient_count'],
                    statistical_confidence=medical_trends['confidence'],
                    medical_significance=medical_trends['medical_significance'],
                    actionable_recommendation=medical_trends['recommendation'],
                    privacy_protection_level="k_anonymity_5",
                    discovery_date=datetime.utcnow()
                ))
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate population insights: {str(e)}")
            return []

    async def _analyze_population_usage_patterns(self, evolution_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyze population-level usage patterns with privacy protection
        """
        try:
            # Aggregate usage data with privacy protection
            pattern_usage = {}
            anonymized_patient_ids = set()
            
            for pattern_id, data in evolution_data.items():
                current_state = data.get('current_state')
                if not current_state:
                    continue
                
                usage_freq = current_state.get('usage_frequency', 0)
                anon_patient_ids = current_state.get('patient_anonymized_ids', [])
                
                # Apply K-anonymity threshold
                if len(anon_patient_ids) >= self.config['k_anonymity_threshold']:
                    pattern_usage[pattern_id] = usage_freq
                    anonymized_patient_ids.update(anon_patient_ids)
            
            if len(pattern_usage) < 5:  # Minimum for meaningful analysis
                return None
            
            # Statistical analysis
            usage_values = list(pattern_usage.values())
            mean_usage = np.mean(usage_values)
            std_usage = np.std(usage_values)
            
            # Identify high-usage patterns (>1 std dev above mean)
            high_usage_threshold = mean_usage + std_usage
            high_usage_patterns = [pid for pid, usage in pattern_usage.items() if usage > high_usage_threshold]
            
            return {
                'description': f"Population analysis reveals {len(high_usage_patterns)} high-adoption patterns with mean usage {mean_usage:.1f}",
                'pattern_count': len(pattern_usage),
                'patient_count': len(anonymized_patient_ids),
                'confidence': 0.85,  # High confidence due to population size
                'medical_significance': 0.7,
                'recommendation': f"Focus on promoting {len(high_usage_patterns)} high-adoption patterns across user base"
            }
            
        except Exception as e:
            logger.error(f"Population usage analysis failed: {str(e)}")
            return None

    async def _analyze_population_medical_trends(self, evolution_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyze medical significance trends across population
        """
        try:
            medical_significance_scores = []
            pattern_types = Counter()
            
            for pattern_id, data in evolution_data.items():
                current_state = data.get('current_state')
                if not current_state:
                    continue
                
                # Apply privacy threshold
                anon_patient_ids = current_state.get('patient_anonymized_ids', [])
                if len(anon_patient_ids) < self.config['k_anonymity_threshold']:
                    continue
                
                med_sig = current_state.get('medical_significance', 0.0)
                pattern_type = current_state.get('pattern_type', 'unknown')
                
                medical_significance_scores.append(med_sig)
                pattern_types[pattern_type] += 1
            
            if len(medical_significance_scores) < 10:
                return None
            
            # Analyze trends
            avg_medical_significance = np.mean(medical_significance_scores)
            high_significance_count = sum(1 for score in medical_significance_scores if score >= 0.8)
            
            # Most common pattern type
            most_common_type = pattern_types.most_common(1)[0] if pattern_types else ('unknown', 0)
            
            return {
                'description': f"Medical analysis shows {high_significance_count} high-significance patterns, avg significance {avg_medical_significance:.2f}",
                'pattern_count': len(medical_significance_scores),
                'patient_count': len(set().union(*[data.get('current_state', {}).get('patient_anonymized_ids', []) for data in evolution_data.values()])),
                'confidence': 0.9,
                'medical_significance': avg_medical_significance,
                'recommendation': f"Prioritize {most_common_type[0]} patterns with {high_significance_count} high-significance variants identified"
            }
            
        except Exception as e:
            logger.error(f"Medical trends analysis failed: {str(e)}")
            return None

    async def _analyze_population_communication_evolution(self, evolution_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyze communication style evolution across population
        """
        # This would analyze how communication styles are changing
        # Implementation would involve privacy-protected analysis of communication patterns
        # For now, returning None to maintain focus on core functionality
        return None

    async def _predict_future_trends(self, evolution_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        🔮 Predict future pattern trends using statistical modeling
        """
        predictions = {
            'emerging_pattern_candidates': [],
            'declining_pattern_warnings': [],
            'growth_predictions': [],
            'confidence_level': 0.0
        }
        
        prediction_count = 0
        
        for pattern_id, data in evolution_data.items():
            usage_history = data.get('usage_history', [])
            
            if len(usage_history) >= 5:  # Minimum for prediction
                # Extract time series
                timestamps = [entry['timestamp'] for entry in usage_history]
                usage_counts = [entry['usage_count'] for entry in usage_history]
                
                # Simple linear extrapolation for prediction
                time_ordinals = [(ts - timestamps[0]).total_seconds() / 86400 for ts in timestamps]
                
                if len(time_ordinals) >= 3:
                    slope, intercept, r_value, p_value, std_err = linregress(time_ordinals, usage_counts)
                    
                    # Predict usage in 30 days
                    future_time = time_ordinals[-1] + 30
                    predicted_usage = slope * future_time + intercept
                    
                    current_usage = usage_counts[-1]
                    change_percentage = ((predicted_usage - current_usage) / max(current_usage, 1)) * 100
                    
                    pattern_info = {
                        'pattern_id': pattern_id,
                        'current_usage': current_usage,
                        'predicted_usage': max(0, predicted_usage),
                        'change_percentage': change_percentage,
                        'confidence': abs(r_value),
                        'pattern_text': data.get('current_state', {}).get('pattern_text', 'Unknown')
                    }
                    
                    if change_percentage > 50 and abs(r_value) > 0.6:  # Strong positive trend
                        predictions['emerging_pattern_candidates'].append(pattern_info)
                    elif change_percentage < -50 and abs(r_value) > 0.6:  # Strong negative trend
                        predictions['declining_pattern_warnings'].append(pattern_info)
                    elif abs(change_percentage) > 20:  # Moderate change
                        predictions['growth_predictions'].append(pattern_info)
                    
                    prediction_count += 1
        
        # Calculate overall confidence
        if prediction_count > 0:
            predictions['confidence_level'] = min(0.8, prediction_count / 20)  # Max 80% confidence
        
        return predictions

    async def _analyze_medical_language_evolution(self, evolution_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        🏥 Analyze how medical language usage is evolving
        """
        language_evolution = {
            'terminology_trends': {},
            'complexity_evolution': {},
            'new_expressions': [],
            'obsolete_expressions': []
        }
        
        # Analyze pattern types and their evolution
        pattern_type_usage = defaultdict(list)
        
        for pattern_id, data in evolution_data.items():
            current_state = data.get('current_state')
            if not current_state:
                continue
            
            pattern_type = current_state.get('pattern_type', 'unknown')
            usage_freq = current_state.get('usage_frequency', 0)
            discovery_date = current_state.get('discovery_date')
            
            if discovery_date:
                days_old = (datetime.utcnow() - discovery_date).days
                pattern_type_usage[pattern_type].append({
                    'usage': usage_freq,
                    'age_days': days_old,
                    'pattern_id': pattern_id
                })
        
        # Analyze trends by pattern type
        for pattern_type, patterns in pattern_type_usage.items():
            if len(patterns) >= 3:
                recent_patterns = [p for p in patterns if p['age_days'] <= 30]
                older_patterns = [p for p in patterns if p['age_days'] > 30]
                
                if recent_patterns and older_patterns:
                    recent_avg_usage = np.mean([p['usage'] for p in recent_patterns])
                    older_avg_usage = np.mean([p['usage'] for p in older_patterns])
                    
                    trend = "increasing" if recent_avg_usage > older_avg_usage else "decreasing"
                    change_magnitude = abs(recent_avg_usage - older_avg_usage)
                    
                    language_evolution['terminology_trends'][pattern_type] = {
                        'trend': trend,
                        'change_magnitude': float(change_magnitude),
                        'recent_usage': float(recent_avg_usage),
                        'older_usage': float(older_avg_usage)
                    }
        
        return language_evolution

    def _update_analytics_metrics(self, trends_analyzed: int, processing_time: float):
        """
        Update analytics performance metrics
        """
        self.analytics_metrics['trends_analyzed'] += trends_analyzed
        
        # Update average processing time
        current_avg = self.analytics_metrics['avg_analysis_time_ms']
        if current_avg == 0:
            self.analytics_metrics['avg_analysis_time_ms'] = processing_time
        else:
            self.analytics_metrics['avg_analysis_time_ms'] = (current_avg + processing_time) / 2

    async def get_evolution_analytics_dashboard(self) -> Dict[str, Any]:
        """
        📊 Get comprehensive evolution analytics for dashboard
        """
        if not self.db:
            return {'error': 'Database not available'}
        
        try:
            # Get recent evolution trends (last 7 days)
            recent_trends = await self.track_pattern_evolution(7)
            
            # Get monthly evolution trends
            monthly_trends = await self.track_pattern_evolution(30)
            
            # Get pattern lifecycle statistics
            lifecycle_stats = await self._get_lifecycle_statistics()
            
            # Get population learning summary
            population_summary = await self._get_population_learning_summary()
            
            return {
                'recent_trends': recent_trends,
                'monthly_trends': monthly_trends,
                'lifecycle_statistics': lifecycle_stats,
                'population_learning_summary': population_summary,
                'performance_metrics': self.analytics_metrics,
                'cache_status': {
                    'evolution_cache_size': len(self.evolution_cache),
                    'last_updated': self.cache_last_updated
                },
                'algorithm_version': '2.0_temporal_pattern_evolution'
            }
            
        except Exception as e:
            logger.error(f"Failed to get evolution analytics dashboard: {str(e)}")
            return {'error': str(e)}

    async def _get_lifecycle_statistics(self) -> Dict[str, Any]:
        """
        Get pattern lifecycle statistics
        """
        if not self.db:
            return {}
        
        try:
            # Get patterns by lifecycle stage
            lifecycle_pipeline = [
                {
                    '$group': {
                        '_id': '$lifecycle_stage',
                        'count': {'$sum': 1},
                        'avg_usage': {'$avg': '$usage_frequency'},
                        'avg_confidence': {'$avg': '$validation_score'}
                    }
                }
            ]
            
            # Note: This assumes lifecycle_stage is tracked in discovered_patterns
            # In practice, would need to calculate dynamically
            lifecycle_stats = await self.db.discovered_patterns.aggregate(lifecycle_pipeline).to_list(length=10)
            
            return {
                'lifecycle_distribution': lifecycle_stats,
                'total_patterns_tracked': sum(stage['count'] for stage in lifecycle_stats)
            }
            
        except Exception as e:
            logger.error(f"Failed to get lifecycle statistics: {str(e)}")
            return {}

    async def _get_population_learning_summary(self) -> Dict[str, Any]:
        """
        Get population learning insights summary
        """
        if not self.db:
            return {}
        
        try:
            # Get anonymized population insights
            recent_insights = await self.db.population_learning_insights.find({
                'discovery_date': {'$gte': datetime.utcnow() - timedelta(days=7)}
            }).sort('discovery_date', -1).limit(5).to_list(length=5)
            
            # Get total population metrics with privacy protection
            total_patterns = await self.db.discovered_patterns.count_documents({})
            
            # Count patterns with sufficient anonymized usage (K-anonymity)
            k_anonymous_patterns = await self.db.discovered_patterns.count_documents({
                'patient_anonymized_ids.4': {'$exists': True}  # At least 5 anonymized IDs
            })
            
            return {
                'recent_population_insights': len(recent_insights),
                'total_patterns_in_system': total_patterns,
                'privacy_compliant_patterns': k_anonymous_patterns,
                'privacy_protection_rate': (k_anonymous_patterns / max(total_patterns, 1)) * 100
            }
            
        except Exception as e:
            logger.error(f"Failed to get population learning summary: {str(e)}")
            return {}

    async def update_pattern_evolution_event(self, pattern_id: str, event_type: str, event_data: Dict[str, Any]) -> bool:
        """
        📝 Record a pattern evolution event
        """
        if not self.db:
            return False
        
        try:
            event_doc = {
                'pattern_id': pattern_id,
                'event_type': event_type,
                'timestamp': datetime.utcnow(),
                'event_data': event_data,
                'recorded_by': 'pattern_evolution_tracker'
            }
            
            await self.db.pattern_evolution_events.insert_one(event_doc)
            
            # Clear relevant caches
            if pattern_id in self.evolution_cache:
                del self.evolution_cache[pattern_id]
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to record pattern evolution event: {str(e)}")
            return False