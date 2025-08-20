"""
🏥 STEP 3.2: CLINICAL-GRADE STRUCTURED OUTPUT MODELS
Advanced Multi-Symptom Parsing System - Medical Documentation Ready Data Structures

This module provides comprehensive, clinical-grade data structures for structured medical output
that meets medical documentation standards and clinical decision support requirements.

Algorithm Version: 3.2_multi_symptom_clinical_excellence
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union, Tuple
from enum import Enum
from datetime import datetime, timedelta
import uuid


class SeverityLevel(str, Enum):
    """Standardized clinical severity levels"""
    NONE = "none"
    MILD = "mild" 
    MODERATE = "moderate"
    SEVERE = "severe"
    EXTREME = "extreme"
    CRITICAL = "critical"


class UrgencyLevel(str, Enum):
    """Medical urgency classification"""
    ROUTINE = "routine"
    URGENT = "urgent" 
    EMERGENCY = "emergency"
    CRITICAL = "critical"


class TemporalPattern(str, Enum):
    """Symptom temporal patterns"""
    ACUTE = "acute"                    # <24 hours
    SUBACUTE = "subacute"             # 24 hours - 6 weeks  
    CHRONIC = "chronic"               # >6 weeks
    INTERMITTENT = "intermittent"     # Comes and goes
    PERSISTENT = "persistent"         # Constant
    PROGRESSIVE = "progressive"       # Getting worse
    CYCLICAL = "cyclical"            # Regular pattern
    UNKNOWN = "unknown"


class SymptomCategory(str, Enum):
    """Primary symptom categories"""
    PAIN = "pain"
    NEUROLOGICAL = "neurological"
    CARDIOVASCULAR = "cardiovascular"
    RESPIRATORY = "respiratory"
    GASTROINTESTINAL = "gastrointestinal"
    MUSCULOSKELETAL = "musculoskeletal"
    DERMATOLOGICAL = "dermatological"
    PSYCHIATRIC = "psychiatric"
    ENDOCRINE = "endocrine"
    UROLOGICAL = "urological"
    GYNECOLOGICAL = "gynecological"
    HEMATOLOGICAL = "hematological"
    IMMUNOLOGICAL = "immunological"
    CONSTITUTIONAL = "constitutional"
    OTHER = "other"


class ConfidenceLevel(str, Enum):
    """Confidence levels for medical analysis"""
    VERY_LOW = "very_low"      # 0.0-0.3
    LOW = "low"                # 0.3-0.5
    MODERATE = "moderate"      # 0.5-0.7
    HIGH = "high"              # 0.7-0.9
    VERY_HIGH = "very_high"    # 0.9-1.0


@dataclass
class StructuredSymptom:
    """Individual symptom with comprehensive clinical data"""
    
    # Core identification
    symptom_name: str
    medical_terminology: str
    original_text: str
    
    # Classification
    anatomical_location: str
    symptom_category: SymptomCategory
    confidence_score: float = 0.0
    
    # Clinical characteristics  
    severity_level: SeverityLevel = SeverityLevel.NONE
    duration: Optional[str] = None
    frequency: Optional[str] = None
    onset_type: Optional[str] = None  # sudden, gradual, insidious
    
    # Qualitative descriptors
    quality_descriptors: List[str] = field(default_factory=list)
    modifying_factors: List[str] = field(default_factory=list)
    aggravating_factors: List[str] = field(default_factory=list)
    alleviating_factors: List[str] = field(default_factory=list)
    
    # Context and associations
    associated_symptoms: List[str] = field(default_factory=list)
    trigger_factors: List[str] = field(default_factory=list)
    environmental_context: List[str] = field(default_factory=list)
    
    # Clinical significance
    clinical_significance: str = "routine"
    medical_significance_score: float = 0.0
    red_flag_indicators: List[str] = field(default_factory=list)
    
    # Metadata
    extraction_method: str = "multi_symptom_parser_v3.2"
    processing_timestamp: datetime = field(default_factory=datetime.now)
    unique_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class TemporalAnalysis:
    """Comprehensive temporal analysis of symptoms"""
    
    # Duration analysis
    overall_duration: Optional[str] = None
    onset_description: Optional[str] = None
    temporal_pattern: TemporalPattern = TemporalPattern.UNKNOWN
    
    # Progression analysis
    symptom_progression: str = "stable"  # improving, worsening, stable, fluctuating
    progression_rate: str = "unknown"    # rapid, gradual, slow
    progression_timeline: Optional[Dict[str, Any]] = None
    
    # Temporal relationships
    symptom_sequence: List[Dict[str, Any]] = field(default_factory=list)
    temporal_clusters: List[Dict[str, Any]] = field(default_factory=list)
    circadian_patterns: List[str] = field(default_factory=list)
    
    # Clinical temporal insights
    acute_vs_chronic_classification: str = "unknown"
    temporal_red_flags: List[str] = field(default_factory=list)
    urgency_temporal_indicators: List[str] = field(default_factory=list)


@dataclass
class OnsetAnalysis:
    """Detailed symptom onset analysis"""
    
    onset_timing: Optional[str] = None
    onset_type: str = "unknown"  # sudden, gradual, insidious
    onset_triggers: List[str] = field(default_factory=list)
    onset_circumstances: List[str] = field(default_factory=list)
    onset_severity: SeverityLevel = SeverityLevel.NONE
    
    # Clinical onset significance
    onset_clinical_significance: str = "routine"
    sudden_onset_red_flags: List[str] = field(default_factory=list)
    onset_pattern_insights: List[str] = field(default_factory=list)


@dataclass
class ProgressionAnalysis:
    """Symptom progression over time analysis"""
    
    progression_direction: str = "stable"  # improving, worsening, stable, cyclical
    progression_speed: str = "unknown"     # rapid, moderate, gradual, slow
    progression_pattern: str = "linear"    # linear, exponential, cyclical, erratic
    
    # Progression details
    severity_changes: List[Dict[str, Any]] = field(default_factory=list)
    functional_impact_changes: List[str] = field(default_factory=list)
    progression_triggers: List[str] = field(default_factory=list)
    
    # Clinical significance
    progression_red_flags: List[str] = field(default_factory=list)
    urgent_progression_indicators: List[str] = field(default_factory=list)
    expected_vs_actual_progression: str = "unknown"


@dataclass
class SeverityAssessment:
    """Comprehensive severity assessment across multiple dimensions"""
    
    # Overall severity
    overall_severity: SeverityLevel = SeverityLevel.NONE
    overall_severity_score: float = 0.0  # 0-10 scale
    severity_confidence: float = 0.0
    
    # Individual symptom severities
    individual_severities: Dict[str, SeverityLevel] = field(default_factory=dict)
    individual_severity_scores: Dict[str, float] = field(default_factory=dict)
    
    # Functional impact assessment
    functional_impact: str = "minimal"  # minimal, mild, moderate, severe, complete
    activities_affected: List[str] = field(default_factory=list)
    quality_of_life_impact: str = "minimal"
    
    # Clinical severity indicators
    severity_red_flags: List[str] = field(default_factory=list)
    severity_clinical_reasoning: List[str] = field(default_factory=list)
    comparative_severity: str = "typical"  # mild_for_condition, typical, severe_for_condition


@dataclass
class FunctionalImpactAssessment:
    """Assessment of functional impact on patient's life"""
    
    # Work/productivity impact
    work_impact: str = "none"  # none, minimal, moderate, severe, unable
    productivity_loss: Optional[float] = None  # 0-100%
    
    # Daily activities impact
    adl_impact: str = "none"  # Activities of Daily Living
    mobility_impact: str = "none"
    sleep_impact: str = "none" 
    cognitive_impact: str = "none"
    
    # Social/emotional impact
    social_impact: str = "none"
    emotional_impact: str = "none"
    relationships_affected: bool = False
    
    # Clinical functional assessment
    functional_status_score: float = 0.0  # 0-100
    disability_indicators: List[str] = field(default_factory=list)
    accommodation_needs: List[str] = field(default_factory=list)


@dataclass
class UrgencyAssessment:
    """Comprehensive urgency assessment"""
    
    urgency_level: UrgencyLevel = UrgencyLevel.ROUTINE
    urgency_score: float = 0.0  # 0-10 scale
    urgency_confidence: float = 0.0
    
    # Emergency indicators
    emergency_red_flags: List[str] = field(default_factory=list)
    critical_combinations: List[str] = field(default_factory=list)
    time_sensitive_factors: List[str] = field(default_factory=list)
    
    # Clinical urgency reasoning
    urgency_clinical_reasoning: List[str] = field(default_factory=list)
    recommended_timeframe: Optional[str] = None  # "immediate", "within_1_hour", "within_24_hours", etc.
    escalation_triggers: List[str] = field(default_factory=list)


@dataclass
class SymptomRelationship:
    """Relationship between two symptoms"""
    
    primary_symptom: str
    related_symptom: str
    relationship_type: str  # causal, associated, sequential, concurrent, antagonistic
    relationship_strength: float = 0.0  # 0-1.0
    confidence: float = 0.0
    
    # Clinical relationship details
    clinical_explanation: str = ""
    medical_syndrome: Optional[str] = None
    temporal_relationship: Optional[str] = None
    
    # Metadata
    evidence_level: str = "expert_opinion"  # research_proven, clinical_consensus, expert_opinion
    relationship_significance: str = "routine"


@dataclass
class ClinicalCluster:
    """Clinically meaningful symptom cluster"""
    
    cluster_name: str
    cluster_type: str  # syndrome, constellation, complex, pattern
    symptoms_in_cluster: List[str]
    cluster_confidence: float = 0.0
    
    # Clinical significance
    medical_syndrome: Optional[str] = None
    differential_diagnosis_clues: List[str] = field(default_factory=list)
    clinical_reasoning: str = ""
    urgency_implications: UrgencyLevel = UrgencyLevel.ROUTINE
    
    # Pattern details
    required_symptoms: List[str] = field(default_factory=list)
    supporting_symptoms: List[str] = field(default_factory=list)
    exclusion_criteria: List[str] = field(default_factory=list)


@dataclass
class MedicalSyndrome:
    """Identified medical syndrome or complex"""
    
    syndrome_name: str
    syndrome_category: str  # acute, chronic, genetic, infectious, autoimmune, etc.
    confidence_score: float = 0.0
    
    # Supporting evidence
    supporting_symptoms: List[str] = field(default_factory=list)
    supporting_findings: List[str] = field(default_factory=list)
    diagnostic_criteria_met: int = 0
    diagnostic_criteria_total: int = 0
    
    # Clinical implications
    urgency_level: UrgencyLevel = UrgencyLevel.ROUTINE
    specialist_referral: Optional[str] = None
    differential_diagnoses: List[str] = field(default_factory=list)
    
    # Treatment implications
    treatment_urgency: str = "routine"
    monitoring_requirements: List[str] = field(default_factory=list)
    prognostic_implications: List[str] = field(default_factory=list)


@dataclass
class SymptomRelationshipMap:
    """Comprehensive mapping of symptom relationships"""
    
    # Individual relationships
    symptom_pairs: List[SymptomRelationship] = field(default_factory=list)
    relationship_matrix: Dict[str, Dict[str, float]] = field(default_factory=dict)
    
    # Cluster analysis
    identified_clusters: List[ClinicalCluster] = field(default_factory=list)
    cluster_hierarchy: Dict[str, List[str]] = field(default_factory=dict)
    
    # Network analysis
    central_symptoms: List[str] = field(default_factory=list)  # Most connected
    isolated_symptoms: List[str] = field(default_factory=list)
    relationship_patterns: List[str] = field(default_factory=list)
    
    # Clinical insights
    medical_syndromes: List[MedicalSyndrome] = field(default_factory=list)
    clinical_coherence_score: float = 0.0
    relationship_clinical_reasoning: List[str] = field(default_factory=list)


@dataclass
class ConfidenceAnalysis:
    """Comprehensive confidence analysis"""
    
    # Overall confidence
    overall_confidence: float = 0.0
    confidence_level: ConfidenceLevel = ConfidenceLevel.MODERATE
    
    # Component confidence scores
    symptom_detection_confidence: float = 0.0
    relationship_confidence: float = 0.0
    severity_confidence: float = 0.0
    temporal_confidence: float = 0.0
    clinical_reasoning_confidence: float = 0.0
    
    # Confidence factors
    confidence_boosters: List[str] = field(default_factory=list)
    confidence_detractors: List[str] = field(default_factory=list)
    confidence_limitations: List[str] = field(default_factory=list)
    
    # Reliability indicators
    reliability_score: float = 0.0
    reliability_factors: List[str] = field(default_factory=list)
    validation_indicators: List[str] = field(default_factory=list)


@dataclass
class UncertaintyAssessment:
    """Assessment of uncertainty in analysis"""
    
    # Uncertainty levels
    overall_uncertainty: float = 0.0  # 0-1.0
    uncertainty_sources: List[str] = field(default_factory=list)
    ambiguity_factors: List[str] = field(default_factory=list)
    
    # Specific uncertainty areas
    symptom_identification_uncertainty: float = 0.0
    relationship_uncertainty: float = 0.0
    severity_uncertainty: float = 0.0
    temporal_uncertainty: float = 0.0
    
    # Clinical uncertainty
    diagnostic_uncertainty: List[str] = field(default_factory=list)
    clinical_decision_uncertainty: List[str] = field(default_factory=list)
    uncertainty_clinical_impact: str = "minimal"


@dataclass
class ClinicalReasoning:
    """Clinical reasoning and medical logic"""
    
    # Primary clinical reasoning
    clinical_logic: List[str] = field(default_factory=list)
    medical_reasoning_chain: List[Dict[str, str]] = field(default_factory=list)
    evidence_synthesis: List[str] = field(default_factory=list)
    
    # Differential reasoning
    differential_considerations: List[str] = field(default_factory=list)
    rule_out_reasoning: List[str] = field(default_factory=list)
    diagnostic_hypotheses: List[str] = field(default_factory=list)
    
    # Clinical decision support
    recommended_actions: List[str] = field(default_factory=list)
    clinical_guidelines_applied: List[str] = field(default_factory=list)
    evidence_based_reasoning: List[str] = field(default_factory=list)
    
    # Reasoning quality
    reasoning_confidence: float = 0.0
    reasoning_completeness: float = 0.0
    clinical_appropriateness: float = 0.0


@dataclass
class ParsingMetadata:
    """Metadata about the parsing process"""
    
    # Processing details
    processing_timestamp: datetime = field(default_factory=datetime.now)
    processing_duration_ms: float = 0.0
    algorithm_version: str = "3.2_multi_symptom_clinical_excellence"
    
    # Input characteristics
    input_text: str = ""
    input_length: int = 0
    input_complexity_score: float = 0.0
    
    # Processing statistics
    symptoms_detected: int = 0
    relationships_identified: int = 0
    patterns_matched: int = 0
    confidence_calculations: int = 0
    
    # Quality metrics
    parsing_quality_score: float = 0.0
    clinical_coherence_achieved: float = 0.0
    processing_efficiency_score: float = 0.0


@dataclass
class PerformanceMetrics:
    """Performance metrics for the parsing process"""
    
    # Speed metrics
    total_processing_time_ms: float = 0.0
    symptom_extraction_time_ms: float = 0.0
    relationship_analysis_time_ms: float = 0.0
    confidence_calculation_time_ms: float = 0.0
    
    # Accuracy metrics
    estimated_accuracy: float = 0.0
    confidence_accuracy_correlation: float = 0.0
    clinical_appropriateness_score: float = 0.0
    
    # Efficiency metrics
    patterns_per_ms: float = 0.0
    symptoms_per_ms: float = 0.0
    memory_efficiency_score: float = 0.0
    
    # Quality metrics
    output_completeness: float = 0.0
    clinical_utility_score: float = 0.0
    integration_compatibility: float = 0.0


@dataclass
class IntegrationMetadata:
    """Metadata for integration with existing systems"""
    
    # Integration with Steps 1.1-3.1
    text_normalization_applied: bool = False
    symptom_recognizer_enhanced: bool = False
    intent_classification_informed: bool = False
    
    # Integration results
    normalization_confidence: float = 0.0
    symptom_recognition_enhancement: float = 0.0
    intent_classification_improvement: float = 0.0
    
    # System compatibility
    medical_ai_version: str = ""
    compatibility_score: float = 0.0
    integration_quality: str = "excellent"
    
    # Enhancement metadata
    enhancement_applied: List[str] = field(default_factory=list)
    enhancement_confidence: Dict[str, float] = field(default_factory=dict)
    enhancement_impact: Dict[str, str] = field(default_factory=dict)


@dataclass
class MultiSymptomParseResult:
    """
    🏥 CLINICAL-GRADE MULTI-SYMPTOM PARSE RESULT
    
    Revolutionary Step 3.2 Implementation - The ultimate structured output that meets 
    medical documentation standards and clinical decision support requirements.
    
    This comprehensive result provides specialist-level medical intelligence and 
    clinical-grade structured data for advanced medical AI applications.
    """
    
    # === PRIMARY SYMPTOM ANALYSIS ===
    primary_symptoms: List[StructuredSymptom] = field(default_factory=list)
    secondary_symptoms: List[StructuredSymptom] = field(default_factory=list) 
    associated_symptoms: List[StructuredSymptom] = field(default_factory=list)
    
    # === TEMPORAL ANALYSIS ===
    temporal_data: TemporalAnalysis = field(default_factory=TemporalAnalysis)
    onset_analysis: OnsetAnalysis = field(default_factory=OnsetAnalysis)
    progression_patterns: ProgressionAnalysis = field(default_factory=ProgressionAnalysis)
    
    # === SEVERITY ASSESSMENT ===
    severity_assessment: SeverityAssessment = field(default_factory=SeverityAssessment)
    functional_impact: FunctionalImpactAssessment = field(default_factory=FunctionalImpactAssessment)
    urgency_indicators: UrgencyAssessment = field(default_factory=UrgencyAssessment)
    
    # === CLINICAL RELATIONSHIPS ===
    symptom_relationships: SymptomRelationshipMap = field(default_factory=SymptomRelationshipMap)
    clinical_clusters: List[ClinicalCluster] = field(default_factory=list)
    potential_syndromes: List[MedicalSyndrome] = field(default_factory=list)
    
    # === ADVANCED ANALYTICS ===
    confidence_metrics: ConfidenceAnalysis = field(default_factory=ConfidenceAnalysis)
    uncertainty_indicators: UncertaintyAssessment = field(default_factory=UncertaintyAssessment)
    clinical_reasoning: ClinicalReasoning = field(default_factory=ClinicalReasoning)
    
    # === INTEGRATION DATA ===
    parsing_metadata: ParsingMetadata = field(default_factory=ParsingMetadata)
    processing_performance: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    integration_hooks: IntegrationMetadata = field(default_factory=IntegrationMetadata)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "primary_symptoms": [asdict(s) for s in self.primary_symptoms],
            "secondary_symptoms": [asdict(s) for s in self.secondary_symptoms],
            "associated_symptoms": [asdict(s) for s in self.associated_symptoms],
            "temporal_data": asdict(self.temporal_data),
            "onset_analysis": asdict(self.onset_analysis),
            "progression_patterns": asdict(self.progression_patterns),
            "severity_assessment": asdict(self.severity_assessment),
            "functional_impact": asdict(self.functional_impact),
            "urgency_indicators": asdict(self.urgency_indicators),
            "symptom_relationships": asdict(self.symptom_relationships),
            "clinical_clusters": [asdict(c) for c in self.clinical_clusters],
            "potential_syndromes": [asdict(s) for s in self.potential_syndromes],
            "confidence_metrics": asdict(self.confidence_metrics),
            "uncertainty_indicators": asdict(self.uncertainty_indicators),
            "clinical_reasoning": asdict(self.clinical_reasoning),
            "parsing_metadata": asdict(self.parsing_metadata),
            "processing_performance": asdict(self.processing_performance),
            "integration_hooks": asdict(self.integration_hooks)
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get concise summary for quick analysis"""
        return {
            "total_symptoms": len(self.primary_symptoms) + len(self.secondary_symptoms),
            "primary_symptoms_count": len(self.primary_symptoms),
            "overall_severity": self.severity_assessment.overall_severity.value,
            "urgency_level": self.urgency_indicators.urgency_level.value,
            "confidence_score": self.confidence_metrics.overall_confidence,
            "syndromes_detected": len(self.potential_syndromes),
            "clinical_clusters": len(self.clinical_clusters),
            "processing_time_ms": self.processing_performance.total_processing_time_ms,
            "clinical_coherence": self.parsing_metadata.clinical_coherence_achieved
        }


# ============================================================================
# UTILITY FUNCTIONS FOR CLINICAL DATA STRUCTURES
# ============================================================================

def create_structured_symptom(
    symptom_name: str,
    medical_term: str,
    location: str,
    category: SymptomCategory,
    confidence: float = 0.0,
    severity: SeverityLevel = SeverityLevel.NONE,
    original_text: str = None,
    **kwargs
) -> StructuredSymptom:
    """Factory function to create structured symptom with defaults"""
    
    # Remove original_text from kwargs to avoid duplicate parameter
    filtered_kwargs = {k: v for k, v in kwargs.items() if k != 'original_text'}
    
    return StructuredSymptom(
        symptom_name=symptom_name,
        medical_terminology=medical_term,
        original_text=original_text or symptom_name,
        anatomical_location=location,
        symptom_category=category,
        confidence_score=confidence,
        severity_level=severity,
        **filtered_kwargs
    )


def calculate_overall_confidence(components: List[float], weights: List[float] = None) -> float:
    """Calculate weighted overall confidence from component scores"""
    if not components:
        return 0.0
    
    if weights is None:
        weights = [1.0] * len(components)
    
    if len(weights) != len(components):
        weights = weights[:len(components)] + [1.0] * (len(components) - len(weights))
    
    weighted_sum = sum(c * w for c, w in zip(components, weights))
    weight_sum = sum(weights)
    
    return min(1.0, max(0.0, weighted_sum / weight_sum if weight_sum > 0 else 0.0))


def classify_confidence_level(score: float) -> ConfidenceLevel:
    """Classify numerical confidence score into categorical level"""
    if score < 0.3:
        return ConfidenceLevel.VERY_LOW
    elif score < 0.5:
        return ConfidenceLevel.LOW
    elif score < 0.7:
        return ConfidenceLevel.MODERATE
    elif score < 0.9:
        return ConfidenceLevel.HIGH
    else:
        return ConfidenceLevel.VERY_HIGH


def create_empty_parse_result() -> MultiSymptomParseResult:
    """Create empty parse result with initialized defaults"""
    return MultiSymptomParseResult()


# Export all key classes and functions
__all__ = [
    # Enums
    'SeverityLevel', 'UrgencyLevel', 'TemporalPattern', 'SymptomCategory', 'ConfidenceLevel',
    
    # Core Data Classes
    'StructuredSymptom', 'TemporalAnalysis', 'OnsetAnalysis', 'ProgressionAnalysis',
    'SeverityAssessment', 'FunctionalImpactAssessment', 'UrgencyAssessment',
    'SymptomRelationship', 'ClinicalCluster', 'MedicalSyndrome', 'SymptomRelationshipMap',
    'ConfidenceAnalysis', 'UncertaintyAssessment', 'ClinicalReasoning',
    'ParsingMetadata', 'PerformanceMetrics', 'IntegrationMetadata',
    
    # Main Result Class
    'MultiSymptomParseResult',
    
    # Utility Functions
    'create_structured_symptom', 'calculate_overall_confidence', 'classify_confidence_level',
    'create_empty_parse_result'
]