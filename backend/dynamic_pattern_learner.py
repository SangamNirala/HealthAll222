"""
🔬 DYNAMIC PATTERN LEARNER - STEP 2 IMPLEMENTATION
===============================================

Real-time pattern discovery engine for medical AI adaptive learning system.
Automatically discovers new symptom description patterns, medical language trends,
and evolving communication patterns from live patient conversations.

Advanced Capabilities:
- Real-time Pattern Discovery: Auto-discovery of new symptom description patterns
- Live Conversation Analysis: Continuous learning from ongoing interactions  
- Confidence Calibration: Feedback loops for accuracy improvement
- Medical Language Evolution: Tracking changes in medical vocabulary usage
- Population-level Learning: Aggregate anonymized insights across patients

Algorithm Version: 2.0_dynamic_pattern_discovery
"""

import os
import asyncio
import json
import time
import hashlib
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
from collections import defaultdict, deque, Counter
import google.generativeai as genai
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from scipy.stats import entropy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
import nltk
from nltk.corpus import stopwords

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class PatternType(str, Enum):
    """Types of patterns discovered"""
    SYMPTOM_DESCRIPTION = "symptom_description"
    TEMPORAL_EXPRESSION = "temporal_expression"
    SEVERITY_INDICATOR = "severity_indicator"
    MEDICAL_TERMINOLOGY = "medical_terminology"
    COMMUNICATION_STYLE = "communication_style"
    EMERGENCY_PATTERN = "emergency_pattern"
    ANATOMICAL_REFERENCE = "anatomical_reference"
    CONTEXTUAL_MODIFIER = "contextual_modifier"

class DiscoveryConfidence(str, Enum):
    """Confidence levels for discovered patterns"""
    VERY_HIGH = "very_high"    # 95%+ - Well-established pattern
    HIGH = "high"              # 85-95% - Strong evidence
    MODERATE = "moderate"      # 70-85% - Moderate evidence  
    LOW = "low"               # 50-70% - Weak evidence
    EXPERIMENTAL = "experimental" # <50% - Needs validation

@dataclass
class DiscoveredPattern:
    """Represents a newly discovered medical conversation pattern"""
    pattern_id: str
    pattern_type: PatternType
    pattern_text: str
    regex_pattern: str
    confidence: DiscoveryConfidence
    discovery_date: datetime
    usage_frequency: int
    example_contexts: List[str]
    medical_significance: float  # 0-1 scale
    validation_score: float
    patient_anonymized_ids: List[str]  # For tracking usage
    effectiveness_metrics: Dict[str, float]
    
@dataclass
class PatternEvolutionEvent:
    """Tracks how patterns change over time"""
    pattern_id: str
    event_type: str  # discovered, modified, deprecated, validated
    timestamp: datetime
    change_description: str
    confidence_before: float
    confidence_after: float
    evidence_data: Dict[str, Any]
    
@dataclass
class RealTimeInsight:
    """Real-time insights from pattern analysis"""
    insight_type: str
    description: str
    confidence: float
    supporting_evidence: List[str]
    actionable_recommendation: str
    impact_prediction: float
    
class DynamicPatternLearner:
    """
    🧠 DYNAMIC PATTERN DISCOVERY ENGINE
    
    Advanced ML-powered system that discovers new medical conversation patterns
    in real-time, tracks their evolution, and continuously improves the system's
    understanding of medical language and communication patterns.
    
    Key Features:
    - Real-time pattern discovery from live conversations
    - ML-powered pattern validation and confidence scoring
    - Medical significance assessment for discovered patterns
    - Population-level learning with privacy protection
    - Continuous feedback loops for pattern refinement
    """
    
    def __init__(self, db_client: AsyncIOMotorClient = None):
        self.db = db_client
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        # Initialize Gemini AI for pattern analysis
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Pattern discovery configuration
        self.config = {
            'min_pattern_frequency': 3,  # Minimum occurrences to consider a pattern
            'confidence_threshold': 0.6,  # Minimum confidence for pattern acceptance
            'max_pattern_cache_size': 500,
            'discovery_window_hours': 24,  # Time window for pattern discovery
            'min_validation_samples': 5,
            'anonymization_k_factor': 5,  # Privacy protection
            'pattern_similarity_threshold': 0.8,
            'real_time_processing_limit_ms': 15  # Performance target
        }
        
        # Real-time pattern cache
        self.discovered_patterns_cache = {}
        self.pattern_candidates_queue = deque(maxlen=1000)
        self.validation_queue = deque(maxlen=200)
        
        # Pattern discovery algorithms
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 3),
            stop_words='english',
            min_df=2
        )
        
        self.clustering_model = DBSCAN(eps=0.3, min_samples=3)
        
        # Performance metrics
        self.performance_metrics = {
            'patterns_discovered_today': 0,
            'patterns_validated_today': 0,
            'pattern_accuracy_rate': 0.0,
            'avg_discovery_time_ms': 0.0,
            'false_positive_rate': 0.0,
            'pattern_adoption_rate': 0.0
        }
        
        # Stop words for medical pattern analysis
        self.medical_stop_words = set(stopwords.words('english')).union({
            'patient', 'doctor', 'feel', 'feeling', 'have', 'had', 'get', 'got',
            'really', 'very', 'quite', 'little', 'bit', 'much', 'more', 'less'
        })
        
        logger.info("🔬 Dynamic Pattern Learner initialized with real-time discovery capabilities")

    async def discover_patterns_from_conversation(self, conversation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        🎯 REAL-TIME PATTERN DISCOVERY FROM LIVE CONVERSATIONS
        
        Analyzes ongoing conversations to discover new medical language patterns,
        symptom descriptions, and communication trends in real-time.
        """
        start_time = time.time()
        
        try:
            conversation_id = conversation_data.get('conversation_id')
            patient_id = conversation_data.get('patient_id')
            messages = conversation_data.get('messages', [])
            
            if not messages:
                return {'status': 'no_messages', 'patterns_discovered': 0}
            
            # Extract potential patterns from conversation
            pattern_candidates = await self._extract_pattern_candidates(messages)
            
            # Real-time pattern validation using AI
            validated_patterns = await self._validate_patterns_real_time(pattern_candidates, conversation_data)
            
            # Medical significance assessment
            significant_patterns = await self._assess_medical_significance(validated_patterns)
            
            # Update pattern database with discoveries
            discovery_results = await self._record_pattern_discoveries(significant_patterns, patient_id)
            
            # Generate real-time insights
            insights = await self._generate_real_time_insights(significant_patterns)
            
            processing_time = (time.time() - start_time) * 1000
            
            # Update performance metrics
            self._update_discovery_metrics(len(significant_patterns), processing_time)
            
            return {
                'status': 'success',
                'conversation_id': conversation_id,
                'patterns_discovered': len(significant_patterns),
                'new_patterns': [asdict(pattern) for pattern in significant_patterns],
                'real_time_insights': [asdict(insight) for insight in insights],
                'processing_time_ms': processing_time,
                'algorithm_version': '2.0_dynamic_pattern_discovery'
            }
            
        except Exception as e:
            logger.error(f"Pattern discovery failed: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'processing_time_ms': (time.time() - start_time) * 1000
            }

    async def _extract_pattern_candidates(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        🔍 Extract potential patterns from conversation messages
        """
        candidates = []
        
        for message in messages:
            if message.get('role') != 'user':
                continue
                
            text = message.get('content', '').lower()
            timestamp = message.get('timestamp', datetime.utcnow())
            
            # Extract different types of patterns
            
            # 1. Symptom description patterns
            symptom_patterns = await self._extract_symptom_patterns(text)
            for pattern in symptom_patterns:
                candidates.append({
                    'type': PatternType.SYMPTOM_DESCRIPTION,
                    'text': pattern['text'],
                    'context': text,
                    'timestamp': timestamp,
                    'confidence_score': pattern['confidence'],
                    'metadata': pattern.get('metadata', {})
                })
            
            # 2. Temporal expression patterns
            temporal_patterns = self._extract_temporal_patterns(text)
            for pattern in temporal_patterns:
                candidates.append({
                    'type': PatternType.TEMPORAL_EXPRESSION,
                    'text': pattern,
                    'context': text,
                    'timestamp': timestamp,
                    'confidence_score': 0.8,
                    'metadata': {}
                })
            
            # 3. Severity indicators
            severity_patterns = self._extract_severity_patterns(text)
            for pattern in severity_patterns:
                candidates.append({
                    'type': PatternType.SEVERITY_INDICATOR,
                    'text': pattern,
                    'context': text,
                    'timestamp': timestamp,
                    'confidence_score': 0.7,
                    'metadata': {}
                })
                
            # 4. Medical terminology usage
            medical_terms = self._extract_medical_terminology(text)
            for term in medical_terms:
                candidates.append({
                    'type': PatternType.MEDICAL_TERMINOLOGY,
                    'text': term,
                    'context': text,
                    'timestamp': timestamp,
                    'confidence_score': 0.9,
                    'metadata': {}
                })
        
        return candidates

    async def _extract_symptom_patterns(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract symptom description patterns using AI analysis
        """
        if not self.gemini_model:
            return []
        
        try:
            prompt = f"""
            Analyze this medical conversation text and identify unique symptom description patterns:
            
            Text: "{text}"
            
            Extract patterns that could be:
            1. Novel ways of describing symptoms
            2. Unusual symptom combinations  
            3. Creative metaphors for medical conditions
            4. Regional or cultural variations in symptom descriptions
            
            Return JSON array with:
            {{
                "patterns": [
                    {{
                        "text": "extracted pattern",
                        "confidence": 0.8,
                        "pattern_type": "novel_description|symptom_combination|metaphor|cultural_variation",
                        "medical_relevance": 0.9,
                        "metadata": {{"key": "value"}}
                    }}
                ]
            }}
            
            Focus on genuinely new patterns that aren't already common medical terminology.
            Return valid JSON only.
            """
            
            response = await asyncio.to_thread(self.gemini_model.generate_content, prompt)
            response_text = response.text.strip()
            
            # Clean response
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
            
            result = json.loads(response_text)
            return result.get('patterns', [])
            
        except Exception as e:
            logger.error(f"AI symptom pattern extraction failed: {str(e)}")
            return []

    def _extract_temporal_patterns(self, text: str) -> List[str]:
        """
        Extract temporal expression patterns using regex
        """
        patterns = []
        
        # Common temporal patterns in medical conversations
        temporal_regexes = [
            r'for the (past|last) \d+ (days?|weeks?|months?|years?)',
            r'(started|began|happening) \d+ (days?|weeks?|months?) ago',
            r'(every|each) (few|couple) (hours?|days?|weeks?)',
            r'(getting|becoming) (better|worse) (over|in) the (past|last) \w+',
            r'(comes and goes|on and off) (every|for) \w+',
            r'(sudden|gradual) onset (of|with) \w+',
            r'(first noticed|first time) (this|it) (yesterday|today|last week)'
        ]
        
        for regex in temporal_regexes:
            matches = re.findall(regex, text, re.IGNORECASE)
            for match in matches:
                pattern_text = ' '.join(match) if isinstance(match, tuple) else match
                patterns.append(pattern_text)
        
        return list(set(patterns))  # Remove duplicates

    def _extract_severity_patterns(self, text: str) -> List[str]:
        """
        Extract severity indicator patterns
        """
        patterns = []
        
        severity_regexes = [
            r'(unbearable|excruciating|severe|intense|horrible) \w+',
            r'(worst|most) \w+ (ever|I\'ve ever had)',
            r'(can\'t|cannot) (sleep|work|function|move) (because|due to)',
            r'(scale of|rate it) \d+(/10| out of 10)',
            r'(mild|moderate|severe|extreme) \w+ (that|which)',
            r'(barely|hardly) (noticeable|feel it)',
            r'(throbbing|pounding|stabbing|burning|aching) \w+'
        ]
        
        for regex in severity_regexes:
            matches = re.findall(regex, text, re.IGNORECASE)
            for match in matches:
                pattern_text = ' '.join(match) if isinstance(match, tuple) else match
                patterns.append(pattern_text)
        
        return list(set(patterns))

    def _extract_medical_terminology(self, text: str) -> List[str]:
        """
        Extract medical terminology usage patterns
        """
        # Common medical terms that might indicate patient education level
        medical_terms = [
            'hypertension', 'diabetes', 'cardiovascular', 'respiratory',
            'gastrointestinal', 'neurological', 'inflammation', 'chronic',
            'acute', 'symptoms', 'diagnosis', 'prognosis', 'prescription',
            'medication', 'dosage', 'side effects', 'allergic reaction'
        ]
        
        found_terms = []
        text_lower = text.lower()
        
        for term in medical_terms:
            if term in text_lower:
                found_terms.append(term)
        
        return found_terms

    async def _validate_patterns_real_time(self, candidates: List[Dict[str, Any]], conversation_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        🎯 Real-time pattern validation using AI and statistical analysis
        """
        validated_patterns = []
        
        for candidate in candidates:
            if len(validated_patterns) >= 5:  # Limit for real-time processing
                break
                
            validation_score = await self._calculate_pattern_validation_score(candidate, conversation_context)
            
            if validation_score >= self.config['confidence_threshold']:
                candidate['validation_score'] = validation_score
                candidate['validated'] = True
                validated_patterns.append(candidate)
            
        return validated_patterns

    async def _calculate_pattern_validation_score(self, candidate: Dict[str, Any], context: Dict[str, Any]) -> float:
        """
        Calculate validation score for a pattern candidate
        """
        base_confidence = candidate.get('confidence_score', 0.5)
        
        # Check if pattern already exists
        if await self._pattern_exists(candidate['text']):
            return 0.2  # Lower score for existing patterns
        
        # Calculate medical relevance
        medical_relevance = await self._assess_medical_relevance(candidate['text'])
        
        # Check usage frequency in database
        usage_frequency = await self._get_pattern_usage_frequency(candidate['text'])
        frequency_score = min(usage_frequency / 10.0, 1.0)  # Normalize to 0-1
        
        # Combine scores
        validation_score = (
            base_confidence * 0.4 +
            medical_relevance * 0.4 +
            frequency_score * 0.2
        )
        
        return min(validation_score, 1.0)

    async def _assess_medical_significance(self, patterns: List[Dict[str, Any]]) -> List[DiscoveredPattern]:
        """
        🏥 Assess medical significance of discovered patterns
        """
        significant_patterns = []
        
        for pattern_data in patterns:
            if not self.gemini_model:
                continue
                
            try:
                # AI-powered medical significance assessment
                significance_score = await self._ai_assess_medical_significance(pattern_data)
                
                if significance_score >= 0.6:  # Threshold for medical significance
                    discovered_pattern = DiscoveredPattern(
                        pattern_id=hashlib.md5(pattern_data['text'].encode()).hexdigest()[:12],
                        pattern_type=PatternType(pattern_data['type']),
                        pattern_text=pattern_data['text'],
                        regex_pattern=self._generate_regex_pattern(pattern_data['text']),
                        confidence=self._map_to_discovery_confidence(pattern_data['validation_score']),
                        discovery_date=datetime.utcnow(),
                        usage_frequency=1,
                        example_contexts=[pattern_data['context']],
                        medical_significance=significance_score,
                        validation_score=pattern_data['validation_score'],
                        patient_anonymized_ids=[self._anonymize_patient_id(pattern_data.get('patient_id', 'anonymous'))],
                        effectiveness_metrics={'initial_discovery': 1.0}
                    )
                    
                    significant_patterns.append(discovered_pattern)
                    
            except Exception as e:
                logger.error(f"Medical significance assessment failed: {str(e)}")
                continue
        
        return significant_patterns

    async def _ai_assess_medical_significance(self, pattern_data: Dict[str, Any]) -> float:
        """
        AI-powered assessment of medical significance
        """
        if not self.gemini_model:
            return 0.5
            
        try:
            prompt = f"""
            Assess the medical significance of this discovered pattern:
            
            Pattern: "{pattern_data['text']}"
            Type: {pattern_data['type']}
            Context: "{pattern_data['context']}"
            
            Rate the medical significance from 0.0 to 1.0 based on:
            1. Clinical relevance (0.4 weight)
            2. Diagnostic value (0.3 weight)
            3. Patient safety impact (0.2 weight)
            4. Educational value (0.1 weight)
            
            Consider:
            - Does this help identify symptoms?
            - Could it aid in diagnosis?
            - Does it reveal important patient communication patterns?
            - Is it medically accurate and useful?
            
            Return only a single float value between 0.0 and 1.0.
            """
            
            response = await asyncio.to_thread(self.gemini_model.generate_content, prompt)
            score_text = response.text.strip()
            
            # Extract float value
            try:
                score = float(score_text)
                return max(0.0, min(1.0, score))
            except ValueError:
                return 0.5
                
        except Exception as e:
            logger.error(f"AI medical significance assessment failed: {str(e)}")
            return 0.5

    async def _record_pattern_discoveries(self, patterns: List[DiscoveredPattern], patient_id: str) -> Dict[str, Any]:
        """
        📊 Record discovered patterns in database with privacy protection
        """
        if self.db is None:
            return {'status': 'no_database'}
        
        try:
            recorded_patterns = []
            
            for pattern in patterns:
                # Check if pattern already exists
                existing_pattern = await self.db.discovered_patterns.find_one({
                    'pattern_id': pattern.pattern_id
                })
                
                if existing_pattern:
                    # Update usage frequency and contexts
                    await self.db.discovered_patterns.update_one(
                        {'pattern_id': pattern.pattern_id},
                        {
                            '$inc': {'usage_frequency': 1},
                            '$addToSet': {
                                'example_contexts': {'$each': pattern.example_contexts},
                                'patient_anonymized_ids': self._anonymize_patient_id(patient_id)
                            },
                            '$set': {'last_seen': datetime.utcnow()}
                        }
                    )
                    recorded_patterns.append('updated')
                else:
                    # Insert new pattern
                    pattern_doc = asdict(pattern)
                    pattern_doc['last_seen'] = datetime.utcnow()
                    pattern_doc['validation_status'] = 'discovered'
                    
                    await self.db.discovered_patterns.insert_one(pattern_doc)
                    recorded_patterns.append('new')
                
                # Record pattern discovery event
                discovery_event = {
                    'pattern_id': pattern.pattern_id,
                    'event_type': 'discovered',
                    'timestamp': datetime.utcnow(),
                    'patient_id_anonymous': self._anonymize_patient_id(patient_id),
                    'confidence': float(pattern.validation_score),
                    'medical_significance': float(pattern.medical_significance)
                }
                
                await self.db.pattern_evolution_events.insert_one(discovery_event)
            
            return {
                'status': 'success',
                'patterns_recorded': len(recorded_patterns),
                'new_patterns': recorded_patterns.count('new'),
                'updated_patterns': recorded_patterns.count('updated')
            }
            
        except Exception as e:
            logger.error(f"Failed to record pattern discoveries: {str(e)}")
            return {'status': 'error', 'error': str(e)}

    async def _generate_real_time_insights(self, patterns: List[DiscoveredPattern]) -> List[RealTimeInsight]:
        """
        💡 Generate actionable insights from discovered patterns
        """
        insights = []
        
        if not patterns:
            return insights
        
        # Group patterns by type
        pattern_groups = defaultdict(list)
        for pattern in patterns:
            pattern_groups[pattern.pattern_type].append(pattern)
        
        # Generate insights for each group
        for pattern_type, group_patterns in pattern_groups.items():
            if len(group_patterns) >= 2:  # Need multiple patterns for trend analysis
                insight = RealTimeInsight(
                    insight_type=f"{pattern_type.value}_trend",
                    description=f"Detected emerging trend in {pattern_type.value.replace('_', ' ')} patterns",
                    confidence=np.mean([p.validation_score for p in group_patterns]),
                    supporting_evidence=[p.pattern_text for p in group_patterns[:3]],
                    actionable_recommendation=f"Consider updating {pattern_type.value} recognition models",
                    impact_prediction=0.7
                )
                insights.append(insight)
        
        # High medical significance insight
        high_significance_patterns = [p for p in patterns if p.medical_significance >= 0.8]
        if high_significance_patterns:
            insight = RealTimeInsight(
                insight_type="high_medical_significance",
                description="Discovered patterns with high medical significance",
                confidence=0.9,
                supporting_evidence=[p.pattern_text for p in high_significance_patterns[:2]],
                actionable_recommendation="Prioritize validation and integration of these patterns",
                impact_prediction=0.85
            )
            insights.append(insight)
        
        return insights

    async def _pattern_exists(self, pattern_text: str) -> bool:
        """
        Check if pattern already exists in database
        """
        if self.db is None:
            return False
        
        try:
            existing = await self.db.discovered_patterns.find_one({
                'pattern_text': pattern_text
            })
            return existing is not None
        except:
            return False

    async def _assess_medical_relevance(self, pattern_text: str) -> float:
        """
        Assess medical relevance of a pattern
        """
        # Simple medical relevance scoring based on keywords
        medical_keywords = [
            'pain', 'symptom', 'feel', 'hurt', 'ache', 'condition',
            'treatment', 'medication', 'doctor', 'hospital', 'clinic',
            'diagnosis', 'chronic', 'acute', 'severe', 'mild'
        ]
        
        text_lower = pattern_text.lower()
        keyword_count = sum(1 for keyword in medical_keywords if keyword in text_lower)
        
        return min(keyword_count / len(medical_keywords), 1.0)

    async def _get_pattern_usage_frequency(self, pattern_text: str) -> int:
        """
        Get usage frequency for a pattern from database
        """
        if not self.db:
            return 0
        
        try:
            pattern = await self.db.discovered_patterns.find_one({
                'pattern_text': pattern_text
            })
            return pattern.get('usage_frequency', 0) if pattern else 0
        except:
            return 0

    def _generate_regex_pattern(self, pattern_text: str) -> str:
        """
        Generate a regex pattern from discovered text
        """
        # Simple regex generation - can be enhanced with more sophisticated NLP
        escaped = re.escape(pattern_text)
        # Allow for minor variations
        flexible = escaped.replace(r'\ ', r'\s+').replace(r'\-', r'[-\s]?')
        return f"\\b{flexible}\\b"

    def _map_to_discovery_confidence(self, validation_score: float) -> DiscoveryConfidence:
        """
        Map validation score to discovery confidence enum
        """
        if validation_score >= 0.95:
            return DiscoveryConfidence.VERY_HIGH
        elif validation_score >= 0.85:
            return DiscoveryConfidence.HIGH
        elif validation_score >= 0.70:
            return DiscoveryConfidence.MODERATE
        elif validation_score >= 0.50:
            return DiscoveryConfidence.LOW
        else:
            return DiscoveryConfidence.EXPERIMENTAL

    def _anonymize_patient_id(self, patient_id: str) -> str:
        """
        Anonymize patient ID for privacy protection
        """
        if not patient_id:
            return 'anonymous'
        
        salt = self.config.get('anonymization_salt', 'pattern_discovery_2025')
        return hashlib.sha256(f"{patient_id}_{salt}".encode()).hexdigest()[:10]

    def _update_discovery_metrics(self, patterns_discovered: int, processing_time: float):
        """
        Update performance metrics for pattern discovery
        """
        self.performance_metrics['patterns_discovered_today'] += patterns_discovered
        
        # Update average processing time
        current_avg = self.performance_metrics['avg_discovery_time_ms']
        if current_avg == 0:
            self.performance_metrics['avg_discovery_time_ms'] = processing_time
        else:
            self.performance_metrics['avg_discovery_time_ms'] = (current_avg + processing_time) / 2

    async def get_pattern_discovery_analytics(self) -> Dict[str, Any]:
        """
        📊 Get comprehensive pattern discovery analytics
        """
        if not self.db:
            return {'error': 'Database not available'}
        
        try:
            # Get total patterns discovered
            total_patterns = await self.db.discovered_patterns.count_documents({})
            
            # Get patterns by type
            type_distribution = await self.db.discovered_patterns.aggregate([
                {'$group': {'_id': '$pattern_type', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]).to_list(length=10)
            
            # Get high confidence patterns
            high_confidence_patterns = await self.db.discovered_patterns.count_documents({
                'confidence': {'$in': ['very_high', 'high']}
            })
            
            # Get recent discoveries (last 24 hours)
            recent_discoveries = await self.db.discovered_patterns.count_documents({
                'discovery_date': {'$gte': datetime.utcnow() - timedelta(hours=24)}
            })
            
            # Get most frequent patterns
            frequent_patterns = await self.db.discovered_patterns.find(
                {},
                {'pattern_text': 1, 'usage_frequency': 1, 'medical_significance': 1}
            ).sort('usage_frequency', -1).limit(5).to_list(length=5)
            
            return {
                'total_patterns_discovered': total_patterns,
                'high_confidence_patterns': high_confidence_patterns,
                'recent_discoveries_24h': recent_discoveries,
                'pattern_type_distribution': type_distribution,
                'most_frequent_patterns': frequent_patterns,
                'performance_metrics': self.performance_metrics,
                'algorithm_version': '2.0_dynamic_pattern_discovery'
            }
            
        except Exception as e:
            logger.error(f"Failed to get pattern discovery analytics: {str(e)}")
            return {'error': str(e)}

    async def calibrate_pattern_confidence(self, feedback_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        🎯 Calibrate pattern confidence based on user feedback
        """
        calibration_results = {
            'patterns_updated': 0,
            'confidence_improvements': 0,
            'patterns_deprecated': 0
        }
        
        if not self.db:
            return calibration_results
        
        try:
            for feedback in feedback_data:
                pattern_id = feedback.get('pattern_id')
                user_feedback = feedback.get('feedback')  # 'helpful', 'not_helpful', 'incorrect'
                evidence_quality = feedback.get('evidence_quality', 0.5)
                
                if not pattern_id:
                    continue
                
                # Get current pattern
                pattern = await self.db.discovered_patterns.find_one({
                    'pattern_id': pattern_id
                })
                
                if not pattern:
                    continue
                
                # Calculate confidence adjustment
                confidence_adjustment = 0.0
                if user_feedback == 'helpful':
                    confidence_adjustment = 0.1 * evidence_quality
                elif user_feedback == 'not_helpful':
                    confidence_adjustment = -0.05
                elif user_feedback == 'incorrect':
                    confidence_adjustment = -0.2
                
                # Update pattern confidence
                current_validation = pattern.get('validation_score', 0.5)
                new_validation = max(0.0, min(1.0, current_validation + confidence_adjustment))
                
                update_result = await self.db.discovered_patterns.update_one(
                    {'pattern_id': pattern_id},
                    {
                        '$set': {
                            'validation_score': new_validation,
                            'confidence': self._map_to_discovery_confidence(new_validation).value,
                            'last_calibrated': datetime.utcnow()
                        },
                        '$inc': {'feedback_count': 1}
                    }
                )
                
                if update_result.modified_count > 0:
                    calibration_results['patterns_updated'] += 1
                    
                    if confidence_adjustment > 0:
                        calibration_results['confidence_improvements'] += 1
                    elif new_validation < 0.3:  # Mark for deprecation
                        await self.db.discovered_patterns.update_one(
                            {'pattern_id': pattern_id},
                            {'$set': {'status': 'deprecated'}}
                        )
                        calibration_results['patterns_deprecated'] += 1
                
                # Record calibration event
                calibration_event = {
                    'pattern_id': pattern_id,
                    'event_type': 'confidence_calibrated',
                    'timestamp': datetime.utcnow(),
                    'feedback_type': user_feedback,
                    'confidence_before': current_validation,
                    'confidence_after': new_validation,
                    'evidence_quality': evidence_quality
                }
                
                await self.db.pattern_evolution_events.insert_one(calibration_event)
            
            return calibration_results
            
        except Exception as e:
            logger.error(f"Pattern confidence calibration failed: {str(e)}")
            return {'error': str(e)}