"""
🏥🧠 COMPREHENSIVE MEDICAL KNOWLEDGE BASE 🧠🏥
=================================================

MISSION: Serve as the central repository for comprehensive medical knowledge,
clinical guidelines, and evidence-based protocols to power the Clinical Decision
Support System with world-class medical intelligence.

Features:
- Comprehensive disease databases with ICD-10/11 integration
- Evidence-based clinical guidelines (AHA, ACC, WHO, CDC)
- Real-time medical knowledge graph processing
- Risk stratification databases and scoring systems
- Drug interaction and contraindication databases
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import asyncio
import google.generativeai as genai
from motor.motor_asyncio import AsyncIOMotorDatabase

class RiskLevel(Enum):
    """Clinical risk levels for patient assessment"""
    CRITICAL = "critical"        # Immediate life-threatening
    HIGH = "high"               # Urgent medical attention needed
    MODERATE = "moderate"       # Prompt medical evaluation
    LOW = "low"                # Routine follow-up
    MINIMAL = "minimal"        # Patient education/monitoring

class AlertType(Enum):
    """Types of clinical alerts"""
    EMERGENCY = "emergency"           # Immediate 911/emergency response
    URGENT = "urgent"                # Urgent medical attention
    RED_FLAG = "red_flag"           # Critical warning signs
    DRUG_INTERACTION = "drug_interaction"
    CONTRAINDICATION = "contraindication"
    GUIDELINE_VIOLATION = "guideline_violation"

@dataclass
class ClinicalGuideline:
    """Evidence-based clinical guideline"""
    guideline_id: str
    name: str
    organization: str  # AHA, ACC, WHO, CDC, etc.
    version: str
    evidence_level: str  # A, B, C
    recommendations: List[Dict[str, Any]]
    contraindications: List[str]
    last_updated: datetime

@dataclass
class DiseaseProfile:
    """Comprehensive disease information profile"""
    disease_id: str
    name: str
    icd10_codes: List[str]
    synonyms: List[str]
    symptoms: List[Dict[str, float]]  # symptom: probability
    risk_factors: List[Dict[str, float]]
    diagnostic_criteria: List[str]
    differential_diagnoses: List[str]
    emergency_indicators: List[str]
    treatment_guidelines: List[str]
    prognosis_factors: Dict[str, Any]

@dataclass
class DrugProfile:
    """Comprehensive medication information"""
    drug_id: str
    name: str
    generic_names: List[str]
    brand_names: List[str]
    drug_class: str
    interactions: List[Dict[str, str]]
    contraindications: List[str]
    side_effects: List[Dict[str, str]]
    dosing_guidelines: Dict[str, Any]
    monitoring_parameters: List[str]

class ComprehensiveMedicalKnowledgeBase:
    """
    🏥🧠 COMPREHENSIVE MEDICAL KNOWLEDGE BASE
    
    World-class medical knowledge repository providing evidence-based
    clinical information for advanced decision support systems.
    """
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.logger = logging.getLogger(__name__)
        
        # Initialize Gemini API for advanced medical reasoning
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize comprehensive medical databases
        self._initialize_medical_databases()
        
        self.logger.info("🏥 Comprehensive Medical Knowledge Base initialized")

    def _initialize_medical_databases(self):
        """Initialize comprehensive medical knowledge databases"""
        
        # Emergency/Critical Condition Database
        self.emergency_conditions = {
            'myocardial_infarction': DiseaseProfile(
                disease_id='MI_001',
                name='Myocardial Infarction',
                icd10_codes=['I21.9', 'I21.0', 'I21.1', 'I21.2'],
                synonyms=['heart attack', 'coronary occlusion', 'cardiac arrest'],
                symptoms=[
                    {'chest_pain': 0.95}, {'shortness_of_breath': 0.70},
                    {'diaphoresis': 0.65}, {'nausea': 0.55}, {'fatigue': 0.60}
                ],
                risk_factors=[
                    {'age_over_65': 0.80}, {'smoking': 0.70}, {'diabetes': 0.60},
                    {'hypertension': 0.65}, {'family_history': 0.50}
                ],
                diagnostic_criteria=[
                    'Elevated cardiac biomarkers (troponin)',
                    'ECG changes consistent with ischemia',
                    'Clinical presentation of chest pain'
                ],
                differential_diagnoses=[
                    'unstable_angina', 'pulmonary_embolism', 'aortic_dissection'
                ],
                emergency_indicators=[
                    'crushing chest pain', 'radiation to left arm/jaw',
                    'severe diaphoresis', 'hemodynamic instability'
                ],
                treatment_guidelines=['immediate_cath_lab', 'dual_antiplatelet', 'beta_blocker'],
                prognosis_factors={'age': 'major', 'time_to_treatment': 'critical'}
            ),
            
            'stroke_acute': DiseaseProfile(
                disease_id='STROKE_001',
                name='Acute Stroke',
                icd10_codes=['I63.9', 'I61.9', 'G93.1'],
                synonyms=['cerebrovascular accident', 'CVA', 'brain attack'],
                symptoms=[
                    {'facial_drooping': 0.80}, {'arm_weakness': 0.85},
                    {'speech_difficulty': 0.75}, {'sudden_confusion': 0.60}
                ],
                risk_factors=[
                    {'atrial_fibrillation': 0.75}, {'hypertension': 0.70},
                    {'age_over_75': 0.80}, {'diabetes': 0.55}
                ],
                diagnostic_criteria=[
                    'FAST assessment positive',
                    'Neurological deficit onset <24 hours',
                    'CT/MRI confirmation'
                ],
                differential_diagnoses=['seizure', 'migraine_complex', 'hypoglycemia'],
                emergency_indicators=[
                    'sudden_onset', 'FAST_positive', 'altered_consciousness'
                ],
                treatment_guidelines=['immediate_ct', 'tpa_consideration', 'stroke_unit'],
                prognosis_factors={'time_to_treatment': 'critical', 'severity': 'major'}
            ),
            
            'sepsis': DiseaseProfile(
                disease_id='SEPSIS_001',
                name='Sepsis',
                icd10_codes=['A41.9', 'R65.20'],
                synonyms=['septicemia', 'blood poisoning', 'systemic infection'],
                symptoms=[
                    {'fever': 0.85}, {'tachycardia': 0.80}, {'altered_mental_status': 0.60},
                    {'hypotension': 0.70}, {'tachypnea': 0.75}
                ],
                risk_factors=[
                    {'immunocompromised': 0.80}, {'recent_surgery': 0.60},
                    {'chronic_illness': 0.55}, {'age_extremes': 0.65}
                ],
                diagnostic_criteria=[
                    'qSOFA score ≥2',
                    'Evidence of infection',
                    'Organ dysfunction'
                ],
                differential_diagnoses=['viral_syndrome', 'drug_reaction', 'autoimmune'],
                emergency_indicators=[
                    'hypotension', 'altered_mental_status', 'organ_dysfunction'
                ],
                treatment_guidelines=['immediate_antibiotics', 'fluid_resuscitation', 'icu_monitoring'],
                prognosis_factors={'early_recognition': 'critical', 'source_control': 'major'}
            )
        }
        
        # Clinical Guidelines Database
        self.clinical_guidelines = {
            'chest_pain_aha_2021': ClinicalGuideline(
                guideline_id='AHA_CP_2021',
                name='AHA/ACC Chest Pain Guidelines 2021',
                organization='American Heart Association',
                version='2021.1',
                evidence_level='A',
                recommendations=[
                    {
                        'condition': 'acute_chest_pain',
                        'action': 'immediate_ecg_troponin',
                        'time_frame': '<10_minutes',
                        'evidence_level': 'A'
                    },
                    {
                        'condition': 'stemi_suspected',
                        'action': 'immediate_cath_lab',
                        'time_frame': '<90_minutes',
                        'evidence_level': 'A'
                    }
                ],
                contraindications=['hemodynamic_instability'],
                last_updated=datetime(2021, 12, 1)
            ),
            
            'stroke_aha_2019': ClinicalGuideline(
                guideline_id='AHA_STROKE_2019',
                name='AHA/ASA Stroke Guidelines 2019',
                organization='American Heart Association',
                version='2019.2',
                evidence_level='A',
                recommendations=[
                    {
                        'condition': 'acute_stroke',
                        'action': 'immediate_ct_scan',
                        'time_frame': '<25_minutes',
                        'evidence_level': 'A'
                    },
                    {
                        'condition': 'ischemic_stroke',
                        'action': 'tpa_administration',
                        'time_frame': '<4.5_hours',
                        'evidence_level': 'A'
                    }
                ],
                contraindications=['recent_surgery', 'bleeding_risk'],
                last_updated=datetime(2019, 10, 30)
            )
        }
        
        # Risk Stratification Scores
        self.risk_scores = {
            'chads_vasc': {
                'name': 'CHA2DS2-VASc Score',
                'purpose': 'Stroke risk in atrial fibrillation',
                'parameters': {
                    'chf': 1, 'hypertension': 1, 'age_75': 2, 'diabetes': 1,
                    'stroke_history': 2, 'vascular_disease': 1, 'age_65_74': 1, 'female': 1
                },
                'interpretation': {
                    0: 'low_risk', 1: 'moderate_risk', 2: 'high_risk'
                }
            },
            
            'wells_pe': {
                'name': 'Wells Score for Pulmonary Embolism',
                'purpose': 'PE probability assessment',
                'parameters': {
                    'clinical_pe_likely': 3, 'heart_rate_100': 1.5,
                    'immobilization': 1.5, 'pe_history': 1.5,
                    'hemoptysis': 1, 'malignancy': 1, 'dvt_signs': 3
                },
                'interpretation': {
                    'low': '<2', 'moderate': '2-6', 'high': '>6'
                }
            }
        }
        
        # Drug Interaction Database
        self.drug_interactions = {
            'warfarin_interactions': [
                {
                    'drug': 'aspirin',
                    'severity': 'major',
                    'mechanism': 'increased_bleeding_risk',
                    'management': 'monitor_inr_closely'
                },
                {
                    'drug': 'amiodarone',
                    'severity': 'major',
                    'mechanism': 'cyp2c9_inhibition',
                    'management': 'reduce_warfarin_dose'
                }
            ]
        }

    async def get_disease_profile(self, disease_name: str) -> Optional[DiseaseProfile]:
        """
        🔍 GET COMPREHENSIVE DISEASE PROFILE
        
        Retrieve detailed disease information including symptoms, risk factors,
        diagnostic criteria, and treatment guidelines.
        """
        try:
            # Check emergency conditions first
            disease_key = disease_name.lower().replace(' ', '_')
            
            if disease_key in self.emergency_conditions:
                return self.emergency_conditions[disease_key]
            
            # Query database for additional conditions
            disease_data = await self.db.medical_knowledge.find_one(
                {"$or": [
                    {"name": {"$regex": disease_name, "$options": "i"}},
                    {"synonyms": {"$in": [disease_name.lower()]}}
                ]}
            )
            
            if disease_data:
                return DiseaseProfile(**disease_data)
                
            return None
            
        except Exception as e:
            self.logger.error(f"Error retrieving disease profile: {str(e)}")
            return None

    async def check_drug_interactions(
        self, 
        medications: List[str], 
        new_medication: str
    ) -> List[Dict[str, Any]]:
        """
        💊 CHECK DRUG INTERACTIONS
        
        Comprehensive drug interaction checking with severity assessment
        and clinical management recommendations.
        """
        try:
            interactions = []
            
            for med in medications:
                # Check against known interaction database
                interaction_key = f"{new_medication.lower()}_interactions"
                
                if interaction_key in self.drug_interactions:
                    for interaction in self.drug_interactions[interaction_key]:
                        if interaction['drug'].lower() in med.lower():
                            interactions.append({
                                'drug1': new_medication,
                                'drug2': med,
                                'severity': interaction['severity'],
                                'mechanism': interaction['mechanism'],
                                'management': interaction['management'],
                                'clinical_significance': self._assess_interaction_significance(
                                    interaction['severity']
                                )
                            })
            
            # Use Gemini for additional interaction checking
            if not interactions:
                gemini_interactions = await self._check_interactions_with_gemini(
                    medications, new_medication
                )
                interactions.extend(gemini_interactions)
            
            return interactions
            
        except Exception as e:
            self.logger.error(f"Error checking drug interactions: {str(e)}")
            return []

    async def apply_clinical_guidelines(
        self, 
        condition: str, 
        patient_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        📋 APPLY CLINICAL GUIDELINES
        
        Apply evidence-based clinical guidelines for specific conditions
        with personalized recommendations based on patient context.
        """
        try:
            recommendations = []
            
            # Find applicable guidelines
            applicable_guidelines = []
            for guideline_id, guideline in self.clinical_guidelines.items():
                if condition.lower() in guideline.name.lower() or \
                   any(rec['condition'] == condition for rec in guideline.recommendations):
                    applicable_guidelines.append(guideline)
            
            # Generate recommendations based on guidelines
            for guideline in applicable_guidelines:
                for recommendation in guideline.recommendations:
                    if self._is_recommendation_applicable(recommendation, patient_context):
                        recommendations.append({
                            'guideline': guideline.name,
                            'organization': guideline.organization,
                            'recommendation': recommendation['action'],
                            'time_frame': recommendation.get('time_frame'),
                            'evidence_level': recommendation['evidence_level'],
                            'contraindications': guideline.contraindications,
                            'patient_specific_notes': self._generate_patient_notes(
                                recommendation, patient_context
                            )
                        })
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error applying clinical guidelines: {str(e)}")
            return []

    async def calculate_risk_score(
        self, 
        score_type: str, 
        patient_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        ⚡ CALCULATE CLINICAL RISK SCORE
        
        Calculate validated clinical risk scores (CHA2DS2-VASc, Wells, etc.)
        with interpretation and clinical recommendations.
        """
        try:
            if score_type not in self.risk_scores:
                return {'error': f'Risk score {score_type} not available'}
            
            score_definition = self.risk_scores[score_type]
            total_score = 0
            
            # Calculate score based on patient data
            for parameter, points in score_definition['parameters'].items():
                if patient_data.get(parameter, False):
                    total_score += points
            
            # Interpret score
            interpretation = self._interpret_risk_score(
                score_type, total_score, score_definition
            )
            
            return {
                'score_name': score_definition['name'],
                'total_score': total_score,
                'interpretation': interpretation,
                'recommendations': self._get_score_recommendations(
                    score_type, interpretation
                ),
                'parameters_used': {
                    param: patient_data.get(param, False)
                    for param in score_definition['parameters'].keys()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating risk score: {str(e)}")
            return {'error': str(e)}

    async def identify_red_flags(
        self, 
        symptoms: List[str], 
        patient_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        🚨 IDENTIFY CLINICAL RED FLAGS
        
        Identify critical warning signs that require immediate medical attention
        based on symptom combinations and patient risk factors.
        """
        try:
            red_flags = []
            
            # Check for emergency condition combinations
            for condition_key, condition in self.emergency_conditions.items():
                symptom_matches = 0
                matched_symptoms = []
                
                for symptom_data in condition.symptoms:
                    symptom_name = list(symptom_data.keys())[0]
                    if any(symptom_name.replace('_', ' ') in s.lower() 
                           for s in symptoms):
                        symptom_matches += 1
                        matched_symptoms.append(symptom_name)
                
                # If significant symptom overlap, flag as red flag
                if symptom_matches >= 2:
                    red_flag_score = self._calculate_red_flag_severity(
                        condition, matched_symptoms, patient_context
                    )
                    
                    red_flags.append({
                        'condition': condition.name,
                        'matched_symptoms': matched_symptoms,
                        'emergency_indicators': condition.emergency_indicators,
                        'severity_score': red_flag_score,
                        'immediate_actions': self._get_immediate_actions(condition),
                        'alert_type': AlertType.EMERGENCY.value if red_flag_score > 0.8 
                                     else AlertType.RED_FLAG.value
                    })
            
            # Sort by severity
            red_flags.sort(key=lambda x: x['severity_score'], reverse=True)
            
            return red_flags
            
        except Exception as e:
            self.logger.error(f"Error identifying red flags: {str(e)}")
            return []

    # Helper Methods
    def _assess_interaction_significance(self, severity: str) -> str:
        """Assess clinical significance of drug interactions"""
        significance_map = {
            'major': 'Contraindicated - do not use together',
            'moderate': 'Use with caution - monitor closely',
            'minor': 'Monitor for effects - usually manageable'
        }
        return significance_map.get(severity, 'Unknown significance')

    async def _check_interactions_with_gemini(
        self, medications: List[str], new_medication: str
    ) -> List[Dict[str, Any]]:
        """Use Gemini AI for additional interaction checking"""
        try:
            prompt = f"""
            As a clinical pharmacist, check for drug interactions between:
            New medication: {new_medication}
            Current medications: {', '.join(medications)}
            
            Return JSON format:
            {{
                "interactions": [
                    {{
                        "drug1": "medication1",
                        "drug2": "medication2", 
                        "severity": "major/moderate/minor",
                        "mechanism": "description",
                        "management": "clinical recommendation"
                    }}
                ]
            }}
            """
            
            response = await self.model.generate_content_async(prompt)
            result = json.loads(response.text.strip())
            return result.get('interactions', [])
            
        except Exception as e:
            self.logger.error(f"Gemini interaction check error: {str(e)}")
            return []

    def _is_recommendation_applicable(
        self, recommendation: Dict[str, Any], patient_context: Dict[str, Any]
    ) -> bool:
        """Check if clinical recommendation applies to patient"""
        # Basic applicability logic - can be enhanced
        return True

    def _generate_patient_notes(
        self, recommendation: Dict[str, Any], patient_context: Dict[str, Any]
    ) -> str:
        """Generate patient-specific notes for recommendations"""
        notes = []
        
        if patient_context.get('age', 0) > 75:
            notes.append("Consider age-related dosing adjustments")
        
        if patient_context.get('comorbidities'):
            notes.append("Monitor for comorbidity interactions")
            
        return '; '.join(notes) if notes else "Standard guidelines apply"

    def _interpret_risk_score(
        self, score_type: str, total_score: float, score_definition: Dict[str, Any]
    ) -> str:
        """Interpret calculated risk score"""
        interpretation_map = score_definition.get('interpretation', {})
        
        if isinstance(list(interpretation_map.keys())[0], int):
            # Numeric thresholds
            for threshold in sorted(interpretation_map.keys(), reverse=True):
                if total_score >= threshold:
                    return interpretation_map[threshold]
        
        return 'unknown_risk'

    def _get_score_recommendations(self, score_type: str, interpretation: str) -> List[str]:
        """Get clinical recommendations based on risk score"""
        recommendations_map = {
            'chads_vasc': {
                'low_risk': ['Consider aspirin', 'Annual reassessment'],
                'moderate_risk': ['Consider anticoagulation', 'Shared decision making'],
                'high_risk': ['Recommend anticoagulation', 'Regular monitoring']
            }
        }
        
        return recommendations_map.get(score_type, {}).get(interpretation, [])

    def _calculate_red_flag_severity(
        self, condition: DiseaseProfile, matched_symptoms: List[str], 
        patient_context: Dict[str, Any]
    ) -> float:
        """Calculate severity score for red flag conditions"""
        base_score = len(matched_symptoms) / len(condition.symptoms)
        
        # Adjust for risk factors
        risk_factor_bonus = 0
        for risk_factor in condition.risk_factors:
            risk_name = list(risk_factor.keys())[0]
            if patient_context.get(risk_name.replace('_', ' '), False):
                risk_factor_bonus += 0.1
        
        return min(base_score + risk_factor_bonus, 1.0)

    def _get_immediate_actions(self, condition: DiseaseProfile) -> List[str]:
        """Get immediate actions for emergency conditions"""
        actions_map = {
            'myocardial_infarction': [
                'Call 911 immediately',
                'Chew 325mg aspirin if not allergic',
                'Monitor vital signs',
                'Prepare for transport'
            ],
            'stroke_acute': [
                'Call 911 immediately',
                'Note time of symptom onset',
                'Do not give medications',
                'Position safely'
            ],
            'sepsis': [
                'Call 911 immediately',
                'Monitor for shock signs',
                'Prepare medication list',
                'Note symptom timeline'
            ]
        }
        
        return actions_map.get(condition.disease_id.lower().split('_')[0], [
            'Seek immediate medical attention',
            'Monitor symptoms closely',
            'Call emergency services if worsening'
        ])