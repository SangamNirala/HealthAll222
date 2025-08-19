"""
🏥 PHASE D: PERFECTION & SCALE - CLINICAL VALIDATION & SAFETY FRAMEWORK

World-Class Clinical Validation System for Medical Intent Classification

This system implements:
- Medical professional review and validation workflows  
- Clinical accuracy assessment and safety verification
- Medical safety protocols and error prevention
- Healthcare compliance and audit capabilities
- Clinical decision support validation
- Medical professional feedback integration

Algorithm Version: Phase_D_Clinical_Excellence_v1.0
Target: 99.8%+ clinical accuracy with medical professional validation
"""

import asyncio
import time
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging
import json
import uuid
from collections import defaultdict, deque
import numpy as np
from pydantic import BaseModel, Field

# Configure logging
logger = logging.getLogger(__name__)

class ClinicalValidationLevel(str, Enum):
    """Clinical validation complexity levels"""
    BASIC = "basic"                    # Standard intent classification
    INTERMEDIATE = "intermediate"      # Multi-symptom scenarios
    ADVANCED = "advanced"             # Complex medical presentations
    EXPERT = "expert"                 # Rare or emergency conditions

class MedicalProfessionalRole(str, Enum):
    """Medical professional roles for validation"""
    EMERGENCY_PHYSICIAN = "emergency_physician"
    INTERNAL_MEDICINE = "internal_medicine"  
    FAMILY_MEDICINE = "family_medicine"
    CARDIOLOGIST = "cardiologist"
    NEUROLOGIST = "neurologist"
    GASTROENTEROLOGIST = "gastroenterologist"
    PULMONOLOGIST = "pulmonologist"
    ENDOCRINOLOGIST = "endocrinologist"
    NURSE_PRACTITIONER = "nurse_practitioner"
    PHYSICIAN_ASSISTANT = "physician_assistant"
    CLINICAL_INFORMATICIST = "clinical_informaticist"

class ValidationStatus(str, Enum):
    """Validation review status"""
    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REQUIRES_REVISION = "requires_revision"
    REJECTED = "rejected"
    ESCALATED = "escalated"

class SafetyLevel(str, Enum):
    """Medical safety classification"""
    SAFE = "safe"                     # No safety concerns
    MONITOR = "monitor"               # Minor safety considerations  
    CAUTION = "caution"              # Moderate safety concerns
    WARNING = "warning"              # Significant safety issues
    CRITICAL = "critical"            # Critical safety concerns

@dataclass
class ClinicalValidationCase:
    """Individual case for clinical validation"""
    case_id: str
    patient_message: str
    conversation_context: Optional[Dict[str, Any]]
    ai_classification_result: Dict[str, Any]
    validation_level: ClinicalValidationLevel
    assigned_reviewer: Optional[str] = None
    reviewer_role: Optional[MedicalProfessionalRole] = None
    validation_status: ValidationStatus = ValidationStatus.PENDING
    safety_assessment: Optional[SafetyLevel] = None
    clinical_notes: str = ""
    reviewer_feedback: Dict[str, Any] = None
    created_timestamp: datetime = None
    reviewed_timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_timestamp is None:
            self.created_timestamp = datetime.utcnow()
        if self.reviewer_feedback is None:
            self.reviewer_feedback = {}

@dataclass  
class ClinicalAccuracyMetrics:
    """Clinical accuracy assessment metrics"""
    total_cases_reviewed: int
    approved_cases: int
    rejected_cases: int
    revision_required: int
    overall_accuracy_percentage: float
    accuracy_by_intent: Dict[str, float]
    accuracy_by_complexity: Dict[str, float]
    safety_distribution: Dict[str, int]
    reviewer_consensus_rate: float
    average_review_time_hours: float

@dataclass
class MedicalSafetyAlert:
    """Medical safety alert for concerning classifications"""
    alert_id: str
    case_id: str
    alert_type: str
    severity: SafetyLevel
    description: str
    recommended_action: str
    escalation_required: bool
    created_timestamp: datetime
    resolved_timestamp: Optional[datetime] = None
    resolution_notes: str = ""

class ClinicalValidationWorkflow:
    """
    👨‍⚕️ CLINICAL VALIDATION WORKFLOW MANAGER
    
    Manages the complete workflow for medical professional review and validation
    of AI intent classification results with clinical accuracy tracking.
    """
    
    def __init__(self):
        """Initialize clinical validation workflow"""
        self.validation_cases = {}  # case_id -> ClinicalValidationCase
        self.pending_reviews = deque()  # Queue of cases awaiting review
        self.completed_reviews = {}  # case_id -> completed review
        self.safety_alerts = {}  # alert_id -> MedicalSafetyAlert
        
        # Reviewer assignments and workloads
        self.active_reviewers = {}  # reviewer_id -> reviewer_info
        self.reviewer_workloads = defaultdict(int)  # reviewer_id -> case_count
        
        # Validation statistics
        self.validation_stats = {
            "total_cases_submitted": 0,
            "total_cases_completed": 0,
            "current_pending_reviews": 0,
            "average_review_time_hours": 0.0,
            "reviewer_consensus_rate": 0.0
        }
        
        logger.info("ClinicalValidationWorkflow initialized")
    
    async def submit_case_for_validation(
        self,
        patient_message: str,
        conversation_context: Optional[Dict[str, Any]],
        ai_classification_result: Dict[str, Any],
        validation_level: ClinicalValidationLevel = ClinicalValidationLevel.BASIC,
        priority: bool = False
    ) -> str:
        """Submit a case for medical professional validation"""
        
        case_id = str(uuid.uuid4())
        
        validation_case = ClinicalValidationCase(
            case_id=case_id,
            patient_message=patient_message,
            conversation_context=conversation_context,
            ai_classification_result=ai_classification_result,
            validation_level=validation_level
        )
        
        # Store case
        self.validation_cases[case_id] = validation_case
        
        # Assign reviewer based on case complexity and urgency
        assigned_reviewer = await self._assign_reviewer(validation_case, priority)
        if assigned_reviewer:
            validation_case.assigned_reviewer = assigned_reviewer["reviewer_id"]
            validation_case.reviewer_role = assigned_reviewer["role"]
            validation_case.validation_status = ValidationStatus.IN_REVIEW
            self.reviewer_workloads[assigned_reviewer["reviewer_id"]] += 1
        else:
            # Add to pending queue if no reviewer available
            if priority:
                self.pending_reviews.appendleft(case_id)  # Priority cases to front
            else:
                self.pending_reviews.append(case_id)
        
        # Check for immediate safety concerns
        await self._assess_immediate_safety(validation_case)
        
        # Update statistics
        self.validation_stats["total_cases_submitted"] += 1
        self.validation_stats["current_pending_reviews"] = len(self.pending_reviews)
        
        logger.info(f"Case {case_id} submitted for {validation_level.value} validation")
        return case_id
    
    async def _assign_reviewer(
        self, 
        case: ClinicalValidationCase,
        priority: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Intelligently assign reviewer based on case characteristics"""
        
        # Determine required expertise based on AI classification
        ai_result = case.ai_classification_result
        primary_intent = ai_result.get("primary_intent", "")
        urgency_level = ai_result.get("urgency_level", "")
        
        # Map intent to required medical expertise
        required_expertise = self._map_intent_to_expertise(primary_intent, urgency_level)
        
        # Find available reviewer with appropriate expertise
        available_reviewers = []
        for reviewer_id, reviewer_info in self.active_reviewers.items():
            if (reviewer_info["role"] in required_expertise and
                reviewer_info["status"] == "available" and
                self.reviewer_workloads[reviewer_id] < reviewer_info["max_concurrent_cases"]):
                
                # Calculate reviewer suitability score
                suitability_score = self._calculate_reviewer_suitability(
                    reviewer_info, case, priority
                )
                available_reviewers.append((reviewer_id, reviewer_info, suitability_score))
        
        if not available_reviewers:
            return None
        
        # Select best reviewer based on suitability score
        available_reviewers.sort(key=lambda x: x[2], reverse=True)
        best_reviewer_id, best_reviewer_info, _ = available_reviewers[0]
        
        return {
            "reviewer_id": best_reviewer_id,
            "role": best_reviewer_info["role"],
            "expertise": best_reviewer_info["expertise"]
        }
    
    def _map_intent_to_expertise(
        self, 
        primary_intent: str, 
        urgency_level: str
    ) -> List[MedicalProfessionalRole]:
        """Map medical intent to required reviewer expertise"""
        
        # Emergency cases can be reviewed by emergency physicians or appropriate specialists
        if urgency_level in ["critical", "emergency"]:
            base_expertise = [MedicalProfessionalRole.EMERGENCY_PHYSICIAN]
        else:
            base_expertise = [
                MedicalProfessionalRole.INTERNAL_MEDICINE,
                MedicalProfessionalRole.FAMILY_MEDICINE,
                MedicalProfessionalRole.NURSE_PRACTITIONER,
                MedicalProfessionalRole.PHYSICIAN_ASSISTANT
            ]
        
        # Add specialist expertise based on intent
        if "cardiac" in primary_intent or "chest_pain" in primary_intent:
            base_expertise.extend([
                MedicalProfessionalRole.CARDIOLOGIST,
                MedicalProfessionalRole.EMERGENCY_PHYSICIAN
            ])
        elif "neurological" in primary_intent or "headache" in primary_intent:
            base_expertise.extend([
                MedicalProfessionalRole.NEUROLOGIST,
                MedicalProfessionalRole.EMERGENCY_PHYSICIAN
            ])
        elif "gi_symptom" in primary_intent or "digestive" in primary_intent:
            base_expertise.append(MedicalProfessionalRole.GASTROENTEROLOGIST)
        elif "respiratory" in primary_intent or "breathing" in primary_intent:
            base_expertise.append(MedicalProfessionalRole.PULMONOLOGIST)
        elif "endocrine" in primary_intent or "metabolic" in primary_intent:
            base_expertise.append(MedicalProfessionalRole.ENDOCRINOLOGIST)
        
        return list(set(base_expertise))  # Remove duplicates
    
    def _calculate_reviewer_suitability(
        self,
        reviewer_info: Dict[str, Any],
        case: ClinicalValidationCase,
        priority: bool
    ) -> float:
        """Calculate reviewer suitability score"""
        score = 0.0
        
        # Base score from reviewer experience
        score += reviewer_info.get("experience_years", 0) * 0.1
        
        # Specialty matching bonus
        required_expertise = self._map_intent_to_expertise(
            case.ai_classification_result.get("primary_intent", ""),
            case.ai_classification_result.get("urgency_level", "")
        )
        if reviewer_info["role"] in required_expertise:
            score += 5.0
        
        # Workload penalty (prefer less busy reviewers)
        current_workload = self.reviewer_workloads[reviewer_info["reviewer_id"]]
        max_workload = reviewer_info.get("max_concurrent_cases", 10)
        workload_penalty = (current_workload / max_workload) * 2.0
        score -= workload_penalty
        
        # Priority case bonus for senior reviewers
        if priority and reviewer_info.get("seniority_level", "junior") in ["senior", "attending"]:
            score += 3.0
        
        # Performance history bonus
        performance_rating = reviewer_info.get("performance_rating", 3.0)
        score += (performance_rating - 3.0) * 2.0  # Ratings on 1-5 scale
        
        return max(0.0, score)
    
    async def _assess_immediate_safety(self, case: ClinicalValidationCase):
        """Assess immediate medical safety concerns"""
        ai_result = case.ai_classification_result
        
        # Check for critical safety indicators
        safety_concerns = []
        
        urgency_level = ai_result.get("urgency_level", "")
        primary_intent = ai_result.get("primary_intent", "")
        confidence_score = ai_result.get("confidence_score", 0.0)
        
        # Critical urgency with low confidence = safety concern
        if urgency_level in ["critical", "emergency"] and confidence_score < 0.7:
            safety_concerns.append({
                "type": "low_confidence_emergency",
                "severity": SafetyLevel.WARNING,
                "description": "Emergency classification with low confidence score"
            })
        
        # Potential false negatives for serious conditions
        if "chest_pain" in case.patient_message.lower() and primary_intent not in ["cardiac_chest_pain_assessment", "emergency_concern"]:
            safety_concerns.append({
                "type": "potential_cardiac_miss",
                "severity": SafetyLevel.CAUTION,
                "description": "Chest pain reported but not classified as cardiac emergency"
            })
        
        # Create safety alerts if needed
        for concern in safety_concerns:
            alert_id = str(uuid.uuid4())
            safety_alert = MedicalSafetyAlert(
                alert_id=alert_id,
                case_id=case.case_id,
                alert_type=concern["type"],
                severity=concern["severity"],
                description=concern["description"],
                recommended_action="Immediate medical professional review required",
                escalation_required=concern["severity"] in [SafetyLevel.WARNING, SafetyLevel.CRITICAL],
                created_timestamp=datetime.utcnow()
            )
            
            self.safety_alerts[alert_id] = safety_alert
            
            # Update case safety assessment
            case.safety_assessment = concern["severity"]
            
            logger.warning(f"Safety alert created: {alert_id} for case {case.case_id}")
    
    async def submit_reviewer_feedback(
        self,
        case_id: str,
        reviewer_id: str,
        validation_decision: ValidationStatus,
        clinical_accuracy_rating: float,
        safety_assessment: SafetyLevel,
        clinical_notes: str,
        suggested_corrections: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Submit medical professional review feedback"""
        
        if case_id not in self.validation_cases:
            logger.error(f"Case {case_id} not found for review")
            return False
        
        case = self.validation_cases[case_id]
        
        # Verify reviewer assignment
        if case.assigned_reviewer != reviewer_id:
            logger.error(f"Reviewer {reviewer_id} not assigned to case {case_id}")
            return False
        
        # Update case with review feedback
        case.validation_status = validation_decision
        case.safety_assessment = safety_assessment
        case.clinical_notes = clinical_notes
        case.reviewed_timestamp = datetime.utcnow()
        
        # Store detailed feedback
        case.reviewer_feedback = {
            "reviewer_id": reviewer_id,
            "clinical_accuracy_rating": clinical_accuracy_rating,
            "safety_assessment": safety_assessment.value,
            "validation_decision": validation_decision.value,
            "clinical_notes": clinical_notes,
            "suggested_corrections": suggested_corrections or {},
            "review_duration_minutes": (
                case.reviewed_timestamp - case.created_timestamp
            ).total_seconds() / 60
        }
        
        # Move to completed reviews
        self.completed_reviews[case_id] = case
        
        # Update reviewer workload
        self.reviewer_workloads[reviewer_id] -= 1
        
        # Check if case requires escalation
        if (validation_decision == ValidationStatus.REJECTED or
            safety_assessment in [SafetyLevel.WARNING, SafetyLevel.CRITICAL]):
            await self._escalate_case(case)
        
        # Update statistics
        self.validation_stats["total_cases_completed"] += 1
        
        # Update average review time
        total_review_time = sum(
            review.reviewer_feedback.get("review_duration_minutes", 0)
            for review in self.completed_reviews.values()
        )
        self.validation_stats["average_review_time_hours"] = (
            total_review_time / len(self.completed_reviews) / 60
        ) if self.completed_reviews else 0
        
        logger.info(f"Review completed for case {case_id}: {validation_decision.value}")
        return True
    
    async def _escalate_case(self, case: ClinicalValidationCase):
        """Escalate case for additional review"""
        # Create escalation alert
        alert_id = str(uuid.uuid4())
        escalation_alert = MedicalSafetyAlert(
            alert_id=alert_id,
            case_id=case.case_id,
            alert_type="case_escalation",
            severity=case.safety_assessment,
            description=f"Case escalated due to {case.validation_status.value} with {case.safety_assessment.value} safety rating",
            recommended_action="Senior medical professional review required",
            escalation_required=True,
            created_timestamp=datetime.utcnow()
        )
        
        self.safety_alerts[alert_id] = escalation_alert
        case.validation_status = ValidationStatus.ESCALATED
        
        logger.warning(f"Case {case.case_id} escalated for additional review")
    
    def register_medical_professional(
        self,
        reviewer_id: str,
        role: MedicalProfessionalRole,
        name: str,
        credentials: str,
        experience_years: int,
        expertise_areas: List[str],
        max_concurrent_cases: int = 10
    ) -> bool:
        """Register medical professional as reviewer"""
        
        reviewer_info = {
            "reviewer_id": reviewer_id,
            "role": role,
            "name": name,
            "credentials": credentials,
            "experience_years": experience_years,
            "expertise_areas": expertise_areas,
            "max_concurrent_cases": max_concurrent_cases,
            "status": "available",
            "performance_rating": 3.0,  # Default rating
            "seniority_level": self._determine_seniority(experience_years),
            "registered_timestamp": datetime.utcnow(),
            "cases_reviewed": 0,
            "average_accuracy_rating": 0.0
        }
        
        self.active_reviewers[reviewer_id] = reviewer_info
        self.reviewer_workloads[reviewer_id] = 0
        
        logger.info(f"Medical professional registered: {name} ({role.value})")
        return True
    
    def _determine_seniority(self, experience_years: int) -> str:
        """Determine seniority level based on experience"""
        if experience_years >= 15:
            return "attending"
        elif experience_years >= 8:
            return "senior"
        elif experience_years >= 3:
            return "mid_level"
        else:
            return "junior"
    
    def get_validation_metrics(self) -> ClinicalAccuracyMetrics:
        """Get comprehensive clinical validation metrics"""
        
        completed_cases = list(self.completed_reviews.values())
        total_cases = len(completed_cases)
        
        if total_cases == 0:
            return ClinicalAccuracyMetrics(
                total_cases_reviewed=0,
                approved_cases=0,
                rejected_cases=0,
                revision_required=0,
                overall_accuracy_percentage=0.0,
                accuracy_by_intent={},
                accuracy_by_complexity={},
                safety_distribution={},
                reviewer_consensus_rate=0.0,
                average_review_time_hours=0.0
            )
        
        # Calculate basic metrics
        approved_cases = len([c for c in completed_cases if c.validation_status == ValidationStatus.APPROVED])
        rejected_cases = len([c for c in completed_cases if c.validation_status == ValidationStatus.REJECTED])
        revision_required = len([c for c in completed_cases if c.validation_status == ValidationStatus.REQUIRES_REVISION])
        
        overall_accuracy = (approved_cases / total_cases) * 100
        
        # Calculate accuracy by intent type
        accuracy_by_intent = {}
        intent_counts = defaultdict(lambda: {"total": 0, "approved": 0})
        
        for case in completed_cases:
            intent = case.ai_classification_result.get("primary_intent", "unknown")
            intent_counts[intent]["total"] += 1
            if case.validation_status == ValidationStatus.APPROVED:
                intent_counts[intent]["approved"] += 1
        
        for intent, counts in intent_counts.items():
            accuracy_by_intent[intent] = (counts["approved"] / counts["total"]) * 100
        
        # Calculate accuracy by complexity
        accuracy_by_complexity = {}
        complexity_counts = defaultdict(lambda: {"total": 0, "approved": 0})
        
        for case in completed_cases:
            complexity = case.validation_level.value
            complexity_counts[complexity]["total"] += 1
            if case.validation_status == ValidationStatus.APPROVED:
                complexity_counts[complexity]["approved"] += 1
        
        for complexity, counts in complexity_counts.items():
            accuracy_by_complexity[complexity] = (counts["approved"] / counts["total"]) * 100
        
        # Safety distribution
        safety_distribution = defaultdict(int)
        for case in completed_cases:
            if case.safety_assessment:
                safety_distribution[case.safety_assessment.value] += 1
        
        # Calculate average review time
        review_times = [
            case.reviewer_feedback.get("review_duration_minutes", 0)
            for case in completed_cases
            if case.reviewer_feedback
        ]
        average_review_time = (sum(review_times) / len(review_times) / 60) if review_times else 0
        
        return ClinicalAccuracyMetrics(
            total_cases_reviewed=total_cases,
            approved_cases=approved_cases,
            rejected_cases=rejected_cases,
            revision_required=revision_required,
            overall_accuracy_percentage=overall_accuracy,
            accuracy_by_intent=dict(accuracy_by_intent),
            accuracy_by_complexity=dict(accuracy_by_complexity),
            safety_distribution=dict(safety_distribution),
            reviewer_consensus_rate=95.0,  # Placeholder - would calculate from multi-reviewer cases
            average_review_time_hours=average_review_time
        )
    
    def get_safety_alerts(self, severity_filter: Optional[SafetyLevel] = None) -> List[MedicalSafetyAlert]:
        """Get current safety alerts"""
        alerts = list(self.safety_alerts.values())
        
        if severity_filter:
            alerts = [alert for alert in alerts if alert.severity == severity_filter]
        
        # Sort by creation time (newest first)
        alerts.sort(key=lambda x: x.created_timestamp, reverse=True)
        
        return alerts
    
    def get_reviewer_statistics(self) -> Dict[str, Any]:
        """Get comprehensive reviewer performance statistics"""
        reviewer_stats = {}
        
        for reviewer_id, reviewer_info in self.active_reviewers.items():
            # Get cases reviewed by this reviewer
            reviewer_cases = [
                case for case in self.completed_reviews.values()
                if case.assigned_reviewer == reviewer_id
            ]
            
            cases_count = len(reviewer_cases)
            
            if cases_count > 0:
                # Calculate reviewer-specific metrics
                approved_count = len([c for c in reviewer_cases if c.validation_status == ValidationStatus.APPROVED])
                accuracy_rate = (approved_count / cases_count) * 100
                
                avg_review_time = np.mean([
                    c.reviewer_feedback.get("review_duration_minutes", 0)
                    for c in reviewer_cases if c.reviewer_feedback
                ])
                
                reviewer_stats[reviewer_id] = {
                    "name": reviewer_info["name"],
                    "role": reviewer_info["role"].value,
                    "cases_reviewed": cases_count,
                    "accuracy_rate": round(accuracy_rate, 1),
                    "average_review_time_minutes": round(avg_review_time, 1),
                    "current_workload": self.reviewer_workloads[reviewer_id],
                    "experience_years": reviewer_info["experience_years"],
                    "performance_rating": reviewer_info["performance_rating"]
                }
        
        return reviewer_stats

class MedicalSafetyVerificationSystem:
    """
    🛡️ MEDICAL SAFETY VERIFICATION SYSTEM
    
    Comprehensive medical safety verification and error prevention system
    with real-time safety monitoring and intervention protocols.
    """
    
    def __init__(self):
        """Initialize medical safety verification system"""
        self.safety_rules = self._initialize_safety_rules()
        self.safety_violations = []
        self.intervention_protocols = self._initialize_intervention_protocols()
        
        # Safety monitoring statistics
        self.safety_stats = {
            "total_classifications_monitored": 0,
            "safety_violations_detected": 0,
            "interventions_triggered": 0,
            "false_positive_rate": 0.0,
            "safety_score": 1.0
        }
        
        logger.info("MedicalSafetyVerificationSystem initialized")
    
    def _initialize_safety_rules(self) -> Dict[str, Any]:
        """Initialize comprehensive medical safety rules"""
        return {
            "emergency_detection_rules": {
                "chest_pain_keywords": ["chest pain", "crushing", "pressure", "squeezing"],
                "stroke_keywords": ["weakness", "facial drooping", "speech difficulty", "sudden"],
                "breathing_keywords": ["can't breathe", "shortness of breath", "difficulty breathing"],
                "consciousness_keywords": ["unconscious", "loss of consciousness", "fainting"],
                "severe_pain_keywords": ["worst pain ever", "unbearable", "excruciating"]
            },
            "safety_thresholds": {
                "emergency_confidence_minimum": 0.8,
                "low_confidence_emergency_threshold": 0.5,
                "false_negative_risk_threshold": 0.3
            },
            "contraindication_rules": {
                "medication_interactions": [],
                "allergy_contraindications": [],
                "condition_contraindications": []
            }
        }
    
    def _initialize_intervention_protocols(self) -> Dict[str, Any]:
        """Initialize medical intervention protocols"""
        return {
            "immediate_escalation": {
                "conditions": ["potential_cardiac_event", "stroke_symptoms", "respiratory_emergency"],
                "actions": ["flag_for_emergency_review", "notify_medical_team", "patient_safety_alert"]
            },
            "enhanced_review": {
                "conditions": ["low_confidence_serious", "conflicting_symptoms", "rare_condition"],
                "actions": ["assign_specialist_reviewer", "request_additional_information"]
            },
            "patient_education": {
                "conditions": ["common_misconception", "anxiety_driven", "health_literacy_concern"],
                "actions": ["provide_educational_resources", "recommend_primary_care_followup"]
            }
        }
    
    async def verify_classification_safety(
        self,
        patient_message: str,
        ai_classification_result: Dict[str, Any],
        conversation_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Comprehensive safety verification of AI classification"""
        
        verification_result = {
            "safety_status": SafetyLevel.SAFE,
            "safety_score": 1.0,
            "violations_detected": [],
            "recommendations": [],
            "intervention_required": False,
            "escalation_needed": False,
            "verification_notes": ""
        }
        
        # Update monitoring statistics
        self.safety_stats["total_classifications_monitored"] += 1
        
        # Rule 1: Emergency Detection Safety Check
        emergency_safety = await self._verify_emergency_detection(
            patient_message, ai_classification_result
        )
        if emergency_safety["violations"]:
            verification_result["violations_detected"].extend(emergency_safety["violations"])
            verification_result["safety_status"] = max(verification_result["safety_status"], emergency_safety["severity"])
        
        # Rule 2: Confidence-Based Safety Check
        confidence_safety = await self._verify_confidence_appropriateness(
            ai_classification_result
        )
        if confidence_safety["violations"]:
            verification_result["violations_detected"].extend(confidence_safety["violations"])
            verification_result["safety_status"] = max(verification_result["safety_status"], confidence_safety["severity"])
        
        # Rule 3: Clinical Logic Consistency Check
        logic_safety = await self._verify_clinical_logic_consistency(
            patient_message, ai_classification_result
        )
        if logic_safety["violations"]:
            verification_result["violations_detected"].extend(logic_safety["violations"])
            verification_result["safety_status"] = max(verification_result["safety_status"], logic_safety["severity"])
        
        # Rule 4: Contraindication and Drug Interaction Check
        contraindication_safety = await self._verify_contraindications(
            patient_message, ai_classification_result, conversation_context
        )
        if contraindication_safety["violations"]:
            verification_result["violations_detected"].extend(contraindication_safety["violations"])
            verification_result["safety_status"] = max(verification_result["safety_status"], contraindication_safety["severity"])
        
        # Calculate overall safety score
        if verification_result["violations_detected"]:
            severity_weights = {
                SafetyLevel.MONITOR: 0.95,
                SafetyLevel.CAUTION: 0.85,
                SafetyLevel.WARNING: 0.65,
                SafetyLevel.CRITICAL: 0.35
            }
            verification_result["safety_score"] = severity_weights.get(verification_result["safety_status"], 1.0)
        
        # Determine if intervention is required
        if verification_result["safety_status"] in [SafetyLevel.WARNING, SafetyLevel.CRITICAL]:
            verification_result["intervention_required"] = True
            verification_result["escalation_needed"] = True
            self.safety_stats["interventions_triggered"] += 1
        
        # Generate recommendations
        verification_result["recommendations"] = self._generate_safety_recommendations(
            verification_result["violations_detected"]
        )
        
        # Update safety statistics
        if verification_result["violations_detected"]:
            self.safety_stats["safety_violations_detected"] += 1
        
        # Calculate running safety score
        violation_rate = self.safety_stats["safety_violations_detected"] / self.safety_stats["total_classifications_monitored"]
        self.safety_stats["safety_score"] = 1.0 - (violation_rate * 0.5)  # 50% penalty for violations
        
        logger.info(f"Safety verification completed: {verification_result['safety_status'].value}")
        return verification_result
    
    async def _verify_emergency_detection(
        self,
        patient_message: str,
        ai_classification_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Verify appropriate emergency detection"""
        violations = []
        severity = SafetyLevel.SAFE
        
        message_lower = patient_message.lower()
        primary_intent = ai_classification_result.get("primary_intent", "")
        urgency_level = ai_classification_result.get("urgency_level", "")
        confidence_score = ai_classification_result.get("confidence_score", 0.0)
        
        # Check for potential missed emergencies
        emergency_keywords = self.safety_rules["emergency_detection_rules"]
        
        # Chest pain not classified as emergency
        if any(keyword in message_lower for keyword in emergency_keywords["chest_pain_keywords"]):
            if urgency_level not in ["critical", "emergency"] and "cardiac" not in primary_intent:
                violations.append({
                    "type": "potential_cardiac_emergency_missed",
                    "description": "Chest pain reported but not classified with appropriate urgency",
                    "recommendation": "Emergency cardiac evaluation required"
                })
                severity = SafetyLevel.WARNING
        
        # Stroke symptoms not flagged
        stroke_indicators = sum(1 for keyword in emergency_keywords["stroke_keywords"] if keyword in message_lower)
        if stroke_indicators >= 2 and urgency_level != "emergency":
            violations.append({
                "type": "potential_stroke_missed",
                "description": "Multiple stroke indicators present without emergency classification",
                "recommendation": "Immediate neurological emergency evaluation"
            })
            severity = SafetyLevel.CRITICAL
        
        # Breathing emergency not properly flagged
        if any(keyword in message_lower for keyword in emergency_keywords["breathing_keywords"]):
            if urgency_level not in ["critical", "emergency"]:
                violations.append({
                    "type": "respiratory_emergency_missed",
                    "description": "Severe breathing difficulty not classified as emergency",
                    "recommendation": "Immediate respiratory emergency evaluation"
                })
                severity = SafetyLevel.WARNING
        
        return {
            "violations": violations,
            "severity": severity
        }
    
    async def _verify_confidence_appropriateness(
        self,
        ai_classification_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Verify confidence levels are appropriate for classification"""
        violations = []
        severity = SafetyLevel.SAFE
        
        confidence_score = ai_classification_result.get("confidence_score", 0.0)
        urgency_level = ai_classification_result.get("urgency_level", "")
        primary_intent = ai_classification_result.get("primary_intent", "")
        
        # Emergency classifications should have high confidence
        if urgency_level in ["critical", "emergency"]:
            min_confidence = self.safety_rules["safety_thresholds"]["emergency_confidence_minimum"]
            if confidence_score < min_confidence:
                violations.append({
                    "type": "low_confidence_emergency",
                    "description": f"Emergency classification with low confidence ({confidence_score:.2f})",
                    "recommendation": "Manual review required for low-confidence emergency classification"
                })
                severity = SafetyLevel.CAUTION
        
        # Very low confidence on any classification
        if confidence_score < 0.3:
            violations.append({
                "type": "very_low_confidence",
                "description": f"Extremely low confidence score ({confidence_score:.2f})",
                "recommendation": "Classification requires human review due to low confidence"
            })
            severity = SafetyLevel.MONITOR
        
        return {
            "violations": violations,
            "severity": severity
        }
    
    async def _verify_clinical_logic_consistency(
        self,
        patient_message: str,
        ai_classification_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Verify clinical logic consistency"""
        violations = []
        severity = SafetyLevel.SAFE
        
        # This would include more sophisticated clinical logic checks
        # For now, implementing basic consistency checks
        
        primary_intent = ai_classification_result.get("primary_intent", "")
        urgency_level = ai_classification_result.get("urgency_level", "")
        
        # Consistency between intent and urgency
        emergency_intents = ["emergency_concern", "crisis_intervention", "neurological_emergency_detection"]
        if primary_intent in emergency_intents and urgency_level not in ["critical", "emergency"]:
            violations.append({
                "type": "intent_urgency_mismatch",
                "description": "Emergency intent with non-emergency urgency level",
                "recommendation": "Review urgency classification for emergency intent"
            })
            severity = SafetyLevel.CAUTION
        
        return {
            "violations": violations,
            "severity": severity
        }
    
    async def _verify_contraindications(
        self,
        patient_message: str,
        ai_classification_result: Dict[str, Any],
        conversation_context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Verify contraindications and drug interactions"""
        violations = []
        severity = SafetyLevel.SAFE
        
        # This would include comprehensive contraindication checking
        # Placeholder for more sophisticated drug interaction and contraindication logic
        
        return {
            "violations": violations,
            "severity": severity
        }
    
    def _generate_safety_recommendations(self, violations: List[Dict[str, Any]]) -> List[str]:
        """Generate safety recommendations based on violations"""
        recommendations = []
        
        for violation in violations:
            if violation.get("recommendation"):
                recommendations.append(violation["recommendation"])
        
        # Add general safety recommendations
        if violations:
            recommendations.extend([
                "Consider manual review by medical professional",
                "Document safety concerns in clinical notes",
                "Monitor patient closely for condition changes"
            ])
        
        return list(set(recommendations))  # Remove duplicates
    
    def get_safety_statistics(self) -> Dict[str, Any]:
        """Get comprehensive safety verification statistics"""
        return {
            "total_classifications_monitored": self.safety_stats["total_classifications_monitored"],
            "safety_violations_detected": self.safety_stats["safety_violations_detected"],
            "interventions_triggered": self.safety_stats["interventions_triggered"],
            "safety_violation_rate": (
                self.safety_stats["safety_violations_detected"] / 
                max(1, self.safety_stats["total_classifications_monitored"])
            ) * 100,
            "intervention_rate": (
                self.safety_stats["interventions_triggered"] /
                max(1, self.safety_stats["total_classifications_monitored"])
            ) * 100,
            "overall_safety_score": self.safety_stats["safety_score"],
            "safety_rules_active": len(self.safety_rules),
            "intervention_protocols_active": len(self.intervention_protocols)
        }

# Global instances
clinical_validation_workflow = ClinicalValidationWorkflow()
medical_safety_verification = MedicalSafetyVerificationSystem()

async def initialize_clinical_validation():
    """Initialize clinical validation and safety systems"""
    try:
        # Register sample medical professionals for testing
        await _register_sample_reviewers()
        
        logger.info("Clinical Validation & Safety Framework initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize clinical validation: {e}")
        return False

async def _register_sample_reviewers():
    """Register sample medical professional reviewers for testing"""
    sample_reviewers = [
        {
            "reviewer_id": "md_emergency_001",
            "role": MedicalProfessionalRole.EMERGENCY_PHYSICIAN,
            "name": "Dr. Sarah Johnson",
            "credentials": "MD, Board Certified Emergency Medicine",
            "experience_years": 12,
            "expertise_areas": ["emergency_medicine", "trauma", "cardiac_emergencies"]
        },
        {
            "reviewer_id": "md_internal_001", 
            "role": MedicalProfessionalRole.INTERNAL_MEDICINE,
            "name": "Dr. Michael Chen",
            "credentials": "MD, Board Certified Internal Medicine",
            "experience_years": 8,
            "expertise_areas": ["internal_medicine", "chronic_disease", "preventive_care"]
        },
        {
            "reviewer_id": "np_family_001",
            "role": MedicalProfessionalRole.NURSE_PRACTITIONER,
            "name": "Jennifer Williams, NP",
            "credentials": "MSN, FNP-BC",
            "experience_years": 6,
            "expertise_areas": ["family_medicine", "primary_care", "patient_education"]
        }
    ]
    
    for reviewer in sample_reviewers:
        clinical_validation_workflow.register_medical_professional(**reviewer)

async def get_clinical_validation_status() -> Dict[str, Any]:
    """Get comprehensive clinical validation system status"""
    validation_metrics = clinical_validation_workflow.get_validation_metrics()
    safety_stats = medical_safety_verification.get_safety_statistics()
    reviewer_stats = clinical_validation_workflow.get_reviewer_statistics()
    
    return {
        "phase_d_clinical_status": "operational",
        "algorithm_version": "Phase_D_Clinical_Excellence_v1.0",
        "validation_metrics": asdict(validation_metrics),
        "safety_verification": safety_stats,
        "reviewer_performance": reviewer_stats,
        "active_reviewers": len(clinical_validation_workflow.active_reviewers),
        "pending_reviews": len(clinical_validation_workflow.pending_reviews),
        "safety_alerts": len(clinical_validation_workflow.get_safety_alerts()),
        "system_targets": {
            "target_clinical_accuracy": 99.8,
            "target_safety_score": 0.95,
            "target_review_time_hours": 24
        },
        "last_updated": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    # Quick test of clinical validation system
    async def test_clinical_validation():
        # Initialize system
        await initialize_clinical_validation()
        
        # Submit test case for validation
        case_id = await clinical_validation_workflow.submit_case_for_validation(
            patient_message="I have severe chest pain that started an hour ago",
            conversation_context=None,
            ai_classification_result={
                "primary_intent": "cardiac_chest_pain_assessment",
                "confidence_score": 0.92,
                "urgency_level": "emergency"
            },
            validation_level=ClinicalValidationLevel.ADVANCED
        )
        print(f"Test case submitted: {case_id}")
        
        # Test safety verification
        safety_result = await medical_safety_verification.verify_classification_safety(
            patient_message="I have chest pain",
            ai_classification_result={
                "primary_intent": "symptom_reporting",
                "confidence_score": 0.45,
                "urgency_level": "routine"
            }
        )
        print(f"Safety verification: {safety_result['safety_status']}")
        
        # Get system status
        status = await get_clinical_validation_status()
        print(f"System Status: {status['phase_d_clinical_status']}")
    
    # Run test
    asyncio.run(test_clinical_validation())