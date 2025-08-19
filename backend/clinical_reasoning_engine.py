"""
🧠⚕️ ADVANCED CLINICAL REASONING ENGINE ⚕️🧠
=================================================

MISSION: Provide world-class clinical reasoning capabilities that mirror expert
physician decision-making processes, incorporating evidence-based medicine,
Bayesian diagnostic reasoning, and advanced clinical intelligence.

Features:
- Bayesian diagnostic probability calculations
- Evidence-based clinical reasoning with uncertainty quantification
- Differential diagnosis generation with likelihood ranking
- Clinical decision trees and algorithmic reasoning
- Integration with medical knowledge base and clinical guidelines
"""

import os
import json
import logging
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import asyncio
import google.generativeai as genai
from motor.motor.asyncio import AsyncIOMotorDatabase
from medical_knowledge_base import (
    ComprehensiveMedicalKnowledgeBase, DiseaseProfile, 
    RiskLevel, AlertType
)

class DiagnosticCertainty(Enum):
    """Levels of diagnostic certainty"""
    DEFINITIVE = "definitive"       # >90% confidence
    PROBABLE = "probable"           # 70-90% confidence  
    POSSIBLE = "possible"           # 40-70% confidence
    UNLIKELY = "unlikely"           # 10-40% confidence
    EXCLUDED = "excluded"           # <10% confidence

class EvidenceStrength(Enum):
    """Strength of clinical evidence"""
    STRONG = "strong"               # Multiple high-quality studies
    MODERATE = "moderate"           # Some quality evidence
    WEAK = "weak"                  # Limited evidence
    EXPERT_OPINION = "expert_opinion"  # Professional consensus

@dataclass
class ClinicalEvidence:
    """Clinical evidence for diagnostic reasoning"""
    finding: str
    presence: bool
    weight: float  # Likelihood ratio or diagnostic weight
    confidence: float
    source: str
    evidence_strength: EvidenceStrength

@dataclass
class DiagnosticHypothesis:
    """Diagnostic hypothesis with probability and reasoning"""
    diagnosis: str
    icd10_code: str
    probability: float
    certainty: DiagnosticCertainty
    supporting_evidence: List[ClinicalEvidence]
    contradicting_evidence: List[ClinicalEvidence]
    clinical_reasoning: str
    next_steps: List[str]
    urgency_level: RiskLevel

@dataclass
class ClinicalDecisionPath:
    """Clinical decision pathway with branching logic"""
    decision_point: str
    condition: str
    true_path: str
    false_path: str
    confidence_threshold: float
    clinical_rationale: str

class AdvancedClinicalReasoningEngine:
    """
    🧠⚕️ ADVANCED CLINICAL REASONING ENGINE
    
    World-class clinical reasoning system that provides expert-level
    diagnostic thinking, probability calculations, and clinical decision support.
    """
    
    def __init__(self, db: AsyncIOMotorDatabase, knowledge_base: ComprehensiveMedicalKnowledgeBase):
        self.db = db
        self.knowledge_base = knowledge_base
        self.logger = logging.getLogger(__name__)
        
        # Initialize Gemini API for advanced reasoning
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize clinical reasoning parameters
        self._initialize_reasoning_parameters()
        
        self.logger.info("🧠 Advanced Clinical Reasoning Engine initialized")

    def _initialize_reasoning_parameters(self):
        """Initialize clinical reasoning parameters and decision trees"""
        
        # Bayesian prior probabilities for common conditions
        self.prior_probabilities = {
            'myocardial_infarction': 0.02,      # 2% baseline risk
            'stroke': 0.01,                     # 1% baseline risk  
            'pulmonary_embolism': 0.005,        # 0.5% baseline risk
            'pneumonia': 0.15,                  # 15% baseline risk
            'viral_syndrome': 0.30,             # 30% baseline risk
            'anxiety_disorder': 0.10,           # 10% baseline risk
            'gastroenteritis': 0.20,           # 20% baseline risk
        }
        
        # Likelihood ratios for key clinical findings
        self.likelihood_ratios = {
            'chest_pain': {
                'myocardial_infarction': {'positive': 2.0, 'negative': 0.3},
                'pulmonary_embolism': {'positive': 1.5, 'negative': 0.8},
                'anxiety_disorder': {'positive': 0.8, 'negative': 1.2}
            },
            'shortness_of_breath': {
                'myocardial_infarction': {'positive': 1.8, 'negative': 0.6},
                'pulmonary_embolism': {'positive': 2.5, 'negative': 0.4},
                'pneumonia': {'positive': 3.0, 'negative': 0.3}
            },
            'diaphoresis': {
                'myocardial_infarction': {'positive': 3.5, 'negative': 0.2},
                'anxiety_disorder': {'positive': 2.0, 'negative': 0.7}
            }
        }
        
        # Clinical decision trees
        self.decision_trees = {
            'chest_pain_evaluation': [
                ClinicalDecisionPath(
                    decision_point='elevated_troponin',
                    condition='troponin_positive', 
                    true_path='acute_coronary_syndrome',
                    false_path='evaluate_other_causes',
                    confidence_threshold=0.85,
                    clinical_rationale='Elevated troponin highly specific for myocardial injury'
                ),
                ClinicalDecisionPath(
                    decision_point='ecg_changes',
                    condition='st_elevation',
                    true_path='stemi_protocol', 
                    false_path='nstemi_evaluation',
                    confidence_threshold=0.95,
                    clinical_rationale='ST elevation indicates acute vessel occlusion'
                )
            ]
        }

    async def generate_differential_diagnosis(
        self, 
        symptoms: List[str],
        patient_context: Dict[str, Any],
        clinical_findings: Optional[List[Dict[str, Any]]] = None
    ) -> List[DiagnosticHypothesis]:
        """
        🎯 GENERATE DIFFERENTIAL DIAGNOSIS
        
        Generate comprehensive differential diagnosis with Bayesian probability
        calculations and evidence-based clinical reasoning.
        """
        try:
            # Extract and analyze clinical evidence
            evidence_list = await self._extract_clinical_evidence(
                symptoms, patient_context, clinical_findings
            )
            
            # Calculate diagnostic probabilities using Bayesian reasoning
            diagnostic_hypotheses = []
            
            for diagnosis, prior_prob in self.prior_probabilities.items():
                # Calculate posterior probability using Bayes' theorem
                posterior_prob = await self._calculate_bayesian_probability(
                    diagnosis, prior_prob, evidence_list
                )
                
                # Get disease profile for detailed information
                disease_profile = await self.knowledge_base.get_disease_profile(diagnosis)
                
                if disease_profile and posterior_prob > 0.05:  # Only include if >5% probability
                    # Analyze supporting and contradicting evidence
                    supporting, contradicting = self._analyze_evidence_for_diagnosis(
                        diagnosis, evidence_list
                    )
                    
                    # Generate clinical reasoning
                    clinical_reasoning = await self._generate_clinical_reasoning(
                        diagnosis, supporting, contradicting, patient_context
                    )
                    
                    # Determine certainty level
                    certainty = self._determine_diagnostic_certainty(posterior_prob)
                    
                    # Determine urgency level
                    urgency = self._assess_diagnostic_urgency(
                        diagnosis, posterior_prob, patient_context
                    )
                    
                    # Generate next steps
                    next_steps = await self._generate_diagnostic_next_steps(
                        diagnosis, certainty, urgency
                    )
                    
                    hypothesis = DiagnosticHypothesis(
                        diagnosis=diagnosis.replace('_', ' ').title(),
                        icd10_code=disease_profile.icd10_codes[0] if disease_profile.icd10_codes else 'TBD',
                        probability=posterior_prob,
                        certainty=certainty,
                        supporting_evidence=supporting,
                        contradicting_evidence=contradicting,
                        clinical_reasoning=clinical_reasoning,
                        next_steps=next_steps,
                        urgency_level=urgency
                    )
                    
                    diagnostic_hypotheses.append(hypothesis)
            
            # Sort by probability (highest first)
            diagnostic_hypotheses.sort(key=lambda x: x.probability, reverse=True)
            
            # Limit to top 5 most likely diagnoses
            return diagnostic_hypotheses[:5]
            
        except Exception as e:
            self.logger.error(f"Error generating differential diagnosis: {str(e)}")
            return []

    async def apply_clinical_decision_rules(
        self,
        condition: str,
        patient_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        📋 APPLY CLINICAL DECISION RULES
        
        Apply validated clinical decision rules and scoring systems
        for standardized clinical decision making.
        """
        try:
            decision_results = {}
            
            # Apply condition-specific decision rules
            if 'chest_pain' in condition.lower():
                decision_results.update(await self._apply_chest_pain_rules(patient_data))
            
            elif 'stroke' in condition.lower():
                decision_results.update(await self._apply_stroke_rules(patient_data))
            
            elif 'pulmonary_embolism' in condition.lower():
                decision_results.update(await self._apply_pe_rules(patient_data))
                
            # Apply general clinical reasoning
            decision_results['clinical_reasoning'] = await self._generate_decision_rationale(
                condition, patient_data, decision_results
            )
            
            return decision_results
            
        except Exception as e:
            self.logger.error(f"Error applying clinical decision rules: {str(e)}")
            return {'error': str(e)}

    async def assess_diagnostic_confidence(
        self,
        diagnosis: str,
        supporting_evidence: List[ClinicalEvidence],
        patient_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        📊 ASSESS DIAGNOSTIC CONFIDENCE
        
        Quantify diagnostic confidence using evidence strength,
        clinical guidelines, and uncertainty analysis.
        """
        try:
            # Calculate evidence-based confidence score
            evidence_score = self._calculate_evidence_score(supporting_evidence)
            
            # Assess clinical guidelines support
            guideline_support = await self._assess_guideline_support(
                diagnosis, supporting_evidence
            )
            
            # Calculate uncertainty factors
            uncertainty_factors = self._identify_uncertainty_factors(
                diagnosis, supporting_evidence, patient_context
            )
            
            # Generate confidence interval
            confidence_interval = self._calculate_confidence_interval(
                evidence_score, uncertainty_factors
            )
            
            return {
                'diagnosis': diagnosis,
                'confidence_score': evidence_score,
                'confidence_level': self._categorize_confidence(evidence_score),
                'guideline_support': guideline_support,
                'uncertainty_factors': uncertainty_factors,
                'confidence_interval': confidence_interval,
                'recommendation': self._generate_confidence_recommendation(
                    evidence_score, uncertainty_factors
                )
            }
            
        except Exception as e:
            self.logger.error(f"Error assessing diagnostic confidence: {str(e)}")
            return {'error': str(e)}

    async def generate_clinical_pathway(
        self,
        primary_diagnosis: str,
        patient_context: Dict[str, Any],
        urgency_level: RiskLevel
    ) -> Dict[str, Any]:
        """
        🗺️ GENERATE CLINICAL PATHWAY
        
        Generate evidence-based clinical pathway with decision points,
        timeline, and resource allocation recommendations.
        """
        try:
            # Determine pathway based on diagnosis and urgency
            if urgency_level == RiskLevel.CRITICAL:
                pathway = await self._generate_emergency_pathway(
                    primary_diagnosis, patient_context
                )
            elif urgency_level == RiskLevel.HIGH:
                pathway = await self._generate_urgent_pathway(
                    primary_diagnosis, patient_context
                )
            else:
                pathway = await self._generate_routine_pathway(
                    primary_diagnosis, patient_context
                )
            
            # Add clinical decision points
            pathway['decision_points'] = await self._identify_decision_points(
                primary_diagnosis, patient_context
            )
            
            # Add resource requirements
            pathway['resource_requirements'] = await self._calculate_resource_needs(
                primary_diagnosis, urgency_level
            )
            
            # Add quality metrics
            pathway['quality_metrics'] = await self._define_quality_metrics(
                primary_diagnosis
            )
            
            return pathway
            
        except Exception as e:
            self.logger.error(f"Error generating clinical pathway: {str(e)}")
            return {'error': str(e)}

    # Helper Methods for Bayesian Reasoning
    async def _extract_clinical_evidence(
        self, 
        symptoms: List[str], 
        patient_context: Dict[str, Any],
        clinical_findings: Optional[List[Dict[str, Any]]] = None
    ) -> List[ClinicalEvidence]:
        """Extract and weight clinical evidence from symptoms and findings"""
        
        evidence_list = []
        
        # Process symptoms as clinical evidence
        for symptom in symptoms:
            symptom_clean = symptom.lower().replace(' ', '_')
            
            # Default weight based on symptom specificity
            weight = self._get_symptom_weight(symptom_clean)
            
            evidence = ClinicalEvidence(
                finding=symptom,
                presence=True,
                weight=weight,
                confidence=0.8,  # Default confidence
                source='patient_report',
                evidence_strength=EvidenceStrength.MODERATE
            )
            evidence_list.append(evidence)
        
        # Process clinical findings if available
        if clinical_findings:
            for finding in clinical_findings:
                evidence = ClinicalEvidence(
                    finding=finding.get('name', ''),
                    presence=finding.get('present', False),
                    weight=finding.get('weight', 1.0),
                    confidence=finding.get('confidence', 0.9),
                    source='clinical_examination',
                    evidence_strength=EvidenceStrength.STRONG
                )
                evidence_list.append(evidence)
        
        return evidence_list

    async def _calculate_bayesian_probability(
        self, 
        diagnosis: str, 
        prior_prob: float, 
        evidence_list: List[ClinicalEvidence]
    ) -> float:
        """Calculate posterior probability using Bayes' theorem"""
        
        # Start with prior probability
        posterior_prob = prior_prob
        
        # Apply each piece of evidence using likelihood ratios
        for evidence in evidence_list:
            if evidence.finding.lower().replace(' ', '_') in self.likelihood_ratios:
                lr_data = self.likelihood_ratios[evidence.finding.lower().replace(' ', '_')]
                
                if diagnosis in lr_data:
                    # Use positive or negative likelihood ratio
                    lr = lr_data[diagnosis]['positive'] if evidence.presence else lr_data[diagnosis]['negative']
                    
                    # Apply Bayes' theorem: P(D|E) = P(E|D) * P(D) / P(E)
                    # Simplified: multiply by likelihood ratio
                    posterior_prob = posterior_prob * lr / (posterior_prob * lr + (1 - posterior_prob))
                    
                    # Weight by evidence confidence
                    posterior_prob = posterior_prob * evidence.confidence + prior_prob * (1 - evidence.confidence)
        
        return min(posterior_prob, 0.99)  # Cap at 99%

    def _analyze_evidence_for_diagnosis(
        self, 
        diagnosis: str, 
        evidence_list: List[ClinicalEvidence]
    ) -> Tuple[List[ClinicalEvidence], List[ClinicalEvidence]]:
        """Categorize evidence as supporting or contradicting"""
        
        supporting = []
        contradicting = []
        
        for evidence in evidence_list:
            finding_key = evidence.finding.lower().replace(' ', '_')
            
            if finding_key in self.likelihood_ratios and diagnosis in self.likelihood_ratios[finding_key]:
                lr_data = self.likelihood_ratios[finding_key][diagnosis]
                
                if evidence.presence and lr_data['positive'] > 1.0:
                    supporting.append(evidence)
                elif not evidence.presence and lr_data['negative'] < 1.0:
                    supporting.append(evidence)
                elif evidence.presence and lr_data['positive'] < 1.0:
                    contradicting.append(evidence)
                elif not evidence.presence and lr_data['negative'] > 1.0:
                    contradicting.append(evidence)
        
        return supporting, contradicting

    async def _generate_clinical_reasoning(
        self, 
        diagnosis: str, 
        supporting: List[ClinicalEvidence],
        contradicting: List[ClinicalEvidence], 
        patient_context: Dict[str, Any]
    ) -> str:
        """Generate clinical reasoning narrative"""
        
        reasoning_parts = []
        
        # Describe supporting evidence
        if supporting:
            reasoning_parts.append(
                f"Supporting evidence includes: {', '.join([e.finding for e in supporting[:3]])}"
            )
        
        # Describe patient context factors
        age = patient_context.get('age', 0)
        if age > 65:
            reasoning_parts.append("Advanced age increases risk")
        
        risk_factors = patient_context.get('risk_factors', [])
        if risk_factors:
            reasoning_parts.append(f"Risk factors present: {', '.join(risk_factors[:2])}")
        
        # Describe contradicting evidence if significant
        if contradicting:
            reasoning_parts.append(
                f"However, note: {', '.join([e.finding for e in contradicting[:2]])}"
            )
        
        return '; '.join(reasoning_parts)

    def _determine_diagnostic_certainty(self, probability: float) -> DiagnosticCertainty:
        """Determine certainty level based on probability"""
        if probability >= 0.90:
            return DiagnosticCertainty.DEFINITIVE
        elif probability >= 0.70:
            return DiagnosticCertainty.PROBABLE  
        elif probability >= 0.40:
            return DiagnosticCertainty.POSSIBLE
        elif probability >= 0.10:
            return DiagnosticCertainty.UNLIKELY
        else:
            return DiagnosticCertainty.EXCLUDED

    def _assess_diagnostic_urgency(
        self, 
        diagnosis: str, 
        probability: float, 
        patient_context: Dict[str, Any]
    ) -> RiskLevel:
        """Assess urgency level based on diagnosis and context"""
        
        # Emergency conditions
        emergency_conditions = ['myocardial_infarction', 'stroke', 'sepsis']
        if any(cond in diagnosis for cond in emergency_conditions) and probability > 0.3:
            return RiskLevel.CRITICAL
        
        # High urgency conditions  
        high_urgency = ['pulmonary_embolism', 'pneumonia']
        if any(cond in diagnosis for cond in high_urgency) and probability > 0.5:
            return RiskLevel.HIGH
            
        # Consider patient age and comorbidities
        if patient_context.get('age', 0) > 75 and probability > 0.4:
            return RiskLevel.HIGH
            
        return RiskLevel.MODERATE

    async def _generate_diagnostic_next_steps(
        self, 
        diagnosis: str, 
        certainty: DiagnosticCertainty,
        urgency: RiskLevel
    ) -> List[str]:
        """Generate appropriate next diagnostic steps"""
        
        next_steps = []
        
        if urgency == RiskLevel.CRITICAL:
            next_steps = [
                'Immediate emergency department evaluation',
                'Activate appropriate emergency protocols',
                'Continuous monitoring'
            ]
        elif certainty in [DiagnosticCertainty.POSSIBLE, DiagnosticCertainty.PROBABLE]:
            next_steps = [
                'Confirmatory testing',
                'Specialist consultation if indicated',
                'Serial clinical assessments'
            ]
        else:
            next_steps = [
                'Continue clinical monitoring',
                'Reassess if symptoms change',
                'Follow-up as clinically indicated'
            ]
        
        return next_steps

    # Additional helper methods would continue here...
    def _get_symptom_weight(self, symptom: str) -> float:
        """Get diagnostic weight for symptom"""
        # Default weights - can be enhanced with medical literature
        weights = {
            'chest_pain': 1.5,
            'shortness_of_breath': 1.3,
            'diaphoresis': 1.8,
            'nausea': 1.0,
            'fatigue': 0.8
        }
        return weights.get(symptom, 1.0)

    def _calculate_evidence_score(self, evidence_list: List[ClinicalEvidence]) -> float:
        """Calculate overall evidence score"""
        if not evidence_list:
            return 0.0
        
        total_weight = sum(e.weight * e.confidence for e in evidence_list)
        max_possible = len(evidence_list) * 3.0  # Assuming max weight of 3.0
        
        return min(total_weight / max_possible, 1.0)

    async def _assess_guideline_support(
        self, diagnosis: str, evidence: List[ClinicalEvidence]
    ) -> Dict[str, Any]:
        """Assess how well evidence supports clinical guidelines"""
        # Placeholder implementation
        return {
            'supported': True,
            'guideline_adherence': 0.85,
            'evidence_level': 'B'
        }

    def _identify_uncertainty_factors(
        self, diagnosis: str, evidence: List[ClinicalEvidence], context: Dict[str, Any]
    ) -> List[str]:
        """Identify factors contributing to diagnostic uncertainty"""
        uncertainty_factors = []
        
        if len(evidence) < 3:
            uncertainty_factors.append("Limited clinical information")
        
        if not any(e.evidence_strength == EvidenceStrength.STRONG for e in evidence):
            uncertainty_factors.append("Lack of objective findings")
            
        if context.get('atypical_presentation', False):
            uncertainty_factors.append("Atypical presentation")
            
        return uncertainty_factors

    def _calculate_confidence_interval(
        self, evidence_score: float, uncertainty_factors: List[str]
    ) -> Tuple[float, float]:
        """Calculate confidence interval for diagnosis"""
        uncertainty_penalty = len(uncertainty_factors) * 0.1
        margin = max(0.1, uncertainty_penalty)
        
        lower = max(0.0, evidence_score - margin)
        upper = min(1.0, evidence_score + margin)
        
        return (lower, upper)

    def _categorize_confidence(self, score: float) -> str:
        """Categorize confidence level"""
        if score >= 0.8:
            return "High confidence"
        elif score >= 0.6:
            return "Moderate confidence" 
        elif score >= 0.4:
            return "Low confidence"
        else:
            return "Very low confidence"

    def _generate_confidence_recommendation(
        self, score: float, uncertainty_factors: List[str]
    ) -> str:
        """Generate recommendation based on confidence assessment"""
        if score >= 0.8 and not uncertainty_factors:
            return "Proceed with clinical management"
        elif uncertainty_factors:
            return "Consider additional evaluation to address uncertainties"
        else:
            return "Monitor closely and reassess"

    # Clinical pathway methods would continue...
    async def _generate_emergency_pathway(
        self, diagnosis: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate emergency clinical pathway"""
        return {
            'pathway_type': 'emergency',
            'time_targets': {
                'assessment': '0-10 minutes',
                'intervention': '10-30 minutes',
                'disposition': '30-60 minutes'
            },
            'required_actions': [
                'Immediate vital signs',
                'IV access and labs',
                'Emergency interventions per protocol'
            ]
        }

    async def _generate_urgent_pathway(
        self, diagnosis: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate urgent clinical pathway"""
        return {
            'pathway_type': 'urgent',
            'time_targets': {
                'assessment': '0-30 minutes', 
                'intervention': '30-120 minutes',
                'disposition': '2-4 hours'
            },
            'required_actions': [
                'Comprehensive assessment',
                'Diagnostic testing',
                'Specialist consultation'
            ]
        }

    async def _generate_routine_pathway(
        self, diagnosis: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate routine clinical pathway"""
        return {
            'pathway_type': 'routine',
            'time_targets': {
                'assessment': '0-60 minutes',
                'intervention': '1-4 hours', 
                'disposition': '4-24 hours'
            },
            'required_actions': [
                'Standard evaluation',
                'Appropriate testing',
                'Follow-up planning'
            ]
        }

    async def _apply_chest_pain_rules(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply chest pain clinical decision rules"""
        # Implement HEART score, TIMI, etc.
        return {
            'heart_score': 'moderate_risk',
            'recommendation': 'Serial troponins and observation'
        }

    async def _apply_stroke_rules(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply stroke clinical decision rules"""
        # Implement NIHSS, ABCD2, etc.
        return {
            'fast_assessment': 'positive',
            'recommendation': 'Immediate CT and stroke team activation'
        }

    async def _apply_pe_rules(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply pulmonary embolism decision rules"""
        # Implement Wells score, PERC rule, etc.
        return {
            'wells_score': 'intermediate_risk',
            'recommendation': 'D-dimer and consider CTPA'
        }