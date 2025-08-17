"""
Comprehensive Medical Knowledge Database for World-Class Medical AI
Contains symptoms, conditions, treatments, and medical relationships
"""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class SymptomSeverity(Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"

class UrgencyLevel(Enum):
    ROUTINE = "routine"
    URGENT = "urgent"
    EMERGENT = "emergent"
    CRITICAL = "critical"

@dataclass
class MedicalCondition:
    """Represents a medical condition with comprehensive details"""
    name: str
    icd_code: str
    category: str
    prevalence: Dict[str, float]  # Age/gender specific prevalence
    typical_symptoms: List[str]
    red_flags: List[str]
    diagnostic_criteria: List[str]
    treatment_options: List[str]
    prognosis: str
    urgency_level: UrgencyLevel

@dataclass
class SymptomProfile:
    """Represents a symptom with comprehensive medical details"""
    name: str
    medical_term: str
    category: str
    associated_conditions: List[str]
    red_flag_combinations: List[List[str]]
    assessment_questions: List[str]
    severity_indicators: Dict[str, List[str]]

class ComprehensiveMedicalKnowledgeDatabase:
    """
    World-class medical knowledge database with comprehensive symptom-disease mappings
    """
    
    def __init__(self):
        self.symptoms_database = self._initialize_symptoms_database()
        self.conditions_database = self._initialize_conditions_database()
        self.treatments_database = self._initialize_treatments_database()
        self.emergency_protocols = self._initialize_emergency_protocols()
        self.differential_diagnosis_rules = self._initialize_differential_rules()
        self.medication_database = self._initialize_medication_database()
    
    def _initialize_symptoms_database(self) -> Dict[str, SymptomProfile]:
        """Initialize comprehensive symptoms database"""
        
        symptoms = {
            "chest_pain": SymptomProfile(
                name="Chest Pain",
                medical_term="Thoracic Pain",
                category="cardiovascular",
                associated_conditions=[
                    "myocardial_infarction", "angina", "pericarditis", "aortic_dissection",
                    "pulmonary_embolism", "pneumothorax", "gerd", "costochondritis"
                ],
                red_flag_combinations=[
                    ["crushing_pain", "diaphoresis", "nausea"],
                    ["sudden_onset", "tearing_pain", "back_pain"],
                    ["shortness_of_breath", "leg_swelling", "recent_surgery"]
                ],
                assessment_questions=[
                    "When did the chest pain start?",
                    "Can you describe the quality of the pain (crushing, stabbing, burning)?",
                    "Does the pain radiate to your arm, jaw, or back?",
                    "What makes the pain better or worse?",
                    "Have you experienced shortness of breath or sweating?"
                ],
                severity_indicators={
                    "mild": ["intermittent", "relieved_by_rest", "no_radiation"],
                    "moderate": ["persistent", "mild_radiation", "some_shortness_of_breath"],
                    "severe": ["crushing", "severe_radiation", "diaphoresis", "nausea"],
                    "critical": ["sudden_onset", "tearing", "loss_of_consciousness"]
                }
            ),
            
            "headache": SymptomProfile(
                name="Headache",
                medical_term="Cephalgia",
                category="neurological",
                associated_conditions=[
                    "tension_headache", "migraine", "cluster_headache", "sinusitis",
                    "meningitis", "subarachnoid_hemorrhage", "brain_tumor", "temporal_arteritis"
                ],
                red_flag_combinations=[
                    ["sudden_onset", "worst_headache_ever"],
                    ["fever", "neck_stiffness", "photophobia"],
                    ["headache", "vision_changes", "weakness"]
                ],
                assessment_questions=[
                    "When did this headache start and how quickly?",
                    "Is this the worst headache you've ever had?",
                    "Do you have fever, neck stiffness, or sensitivity to light?",
                    "Are you experiencing any vision changes or weakness?",
                    "Have you had similar headaches before?"
                ],
                severity_indicators={
                    "mild": ["gradual_onset", "manageable_pain", "no_associated_symptoms"],
                    "moderate": ["persistent", "some_nausea", "light_sensitivity"],
                    "severe": ["severe_pain", "vomiting", "unable_to_function"],
                    "critical": ["sudden_onset", "worst_ever", "neurological_signs"]
                }
            ),
            
            "shortness_of_breath": SymptomProfile(
                name="Shortness of Breath",
                medical_term="Dyspnea",
                category="respiratory",
                associated_conditions=[
                    "asthma", "copd", "pneumonia", "pulmonary_embolism",
                    "heart_failure", "pneumothorax", "anaphylaxis"
                ],
                red_flag_combinations=[
                    ["sudden_onset", "chest_pain", "leg_swelling"],
                    ["wheezing", "throat_swelling", "rash"],
                    ["fever", "cough", "chest_pain"]
                ],
                assessment_questions=[
                    "When did you first notice difficulty breathing?",
                    "Is the shortness of breath worse with activity or at rest?",
                    "Do you have chest pain or wheezing?",
                    "Have you had any recent travel or surgery?",
                    "Are you experiencing any swelling in your legs?"
                ],
                severity_indicators={
                    "mild": ["with_exertion_only", "able_to_speak_sentences"],
                    "moderate": ["with_minimal_activity", "speaking_phrases"],
                    "severe": ["at_rest", "speaking_words_only", "use_accessory_muscles"],
                    "critical": ["unable_to_speak", "cyanosis", "altered_mental_status"]
                }
            ),
            
            "abdominal_pain": SymptomProfile(
                name="Abdominal Pain",
                medical_term="Abdominal Pain",
                category="gastrointestinal",
                associated_conditions=[
                    "appendicitis", "cholecystitis", "bowel_obstruction", "pancreatitis",
                    "peptic_ulcer", "kidney_stones", "ovarian_cyst", "gastroenteritis"
                ],
                red_flag_combinations=[
                    ["severe_pain", "vomiting", "fever"],
                    ["right_lower_quadrant", "guarding", "rebound_tenderness"],
                    ["epigastric_pain", "back_pain", "nausea"]
                ],
                assessment_questions=[
                    "Where exactly is the pain located?",
                    "When did the pain start and how has it changed?",
                    "What makes the pain better or worse?",
                    "Have you had nausea, vomiting, or changes in bowel movements?",
                    "Do you have fever or chills?"
                ],
                severity_indicators={
                    "mild": ["intermittent", "crampy", "no_associated_symptoms"],
                    "moderate": ["persistent", "some_nausea", "interferes_with_activity"],
                    "severe": ["constant", "sharp", "vomiting", "unable_to_eat"],
                    "critical": ["excruciating", "rigid_abdomen", "signs_of_shock"]
                }
            ),
            
            "fever": SymptomProfile(
                name="Fever",
                medical_term="Pyrexia",
                category="systemic",
                associated_conditions=[
                    "viral_infection", "bacterial_infection", "pneumonia", "urinary_tract_infection",
                    "meningitis", "sepsis", "malaria", "autoimmune_disease"
                ],
                red_flag_combinations=[
                    ["high_fever", "neck_stiffness", "rash"],
                    ["fever", "shortness_of_breath", "cough"],
                    ["fever", "severe_headache", "confusion"]
                ],
                assessment_questions=[
                    "What is your temperature and when did the fever start?",
                    "Do you have chills, sweats, or shaking?",
                    "Are you experiencing any other symptoms like headache or cough?",
                    "Have you traveled recently or been exposed to illness?",
                    "Do you have any chronic medical conditions?"
                ],
                severity_indicators={
                    "mild": ["100-101°F", "manageable_discomfort"],
                    "moderate": ["101-103°F", "chills", "body_aches"],
                    "severe": ["103-105°F", "severe_chills", "dehydration"],
                    "critical": [">105°F", "altered_mental_status", "organ_dysfunction"]
                }
            )
        }
        
        return symptoms
    
    def _initialize_conditions_database(self) -> Dict[str, MedicalCondition]:
        """Initialize comprehensive conditions database"""
        
        conditions = {
            "myocardial_infarction": MedicalCondition(
                name="Myocardial Infarction (Heart Attack)",
                icd_code="I21.9",
                category="cardiovascular",
                prevalence={
                    "male_over_45": 0.15,
                    "female_over_55": 0.12,
                    "male_under_45": 0.02,
                    "female_under_55": 0.01
                },
                typical_symptoms=[
                    "crushing_chest_pain", "left_arm_pain", "jaw_pain",
                    "shortness_of_breath", "diaphoresis", "nausea"
                ],
                red_flags=[
                    "crushing_substernal_pain", "radiation_to_left_arm",
                    "diaphoresis", "nausea_vomiting", "shortness_of_breath"
                ],
                diagnostic_criteria=[
                    "Chest pain >20 minutes", "ECG changes", "Elevated troponins",
                    "Risk factors present", "Associated symptoms"
                ],
                treatment_options=[
                    "Immediate 911 call", "Aspirin 325mg", "Nitroglycerin",
                    "Emergency cardiac catheterization", "Antiplatelet therapy"
                ],
                prognosis="Excellent with early intervention, poor if delayed",
                urgency_level=UrgencyLevel.CRITICAL
            ),
            
            "tension_headache": MedicalCondition(
                name="Tension Headache",
                icd_code="G44.209",
                category="neurological",
                prevalence={
                    "general_population": 0.38,
                    "female": 0.42,
                    "male": 0.34
                },
                typical_symptoms=[
                    "bilateral_headache", "band_like_pressure", "mild_to_moderate_pain",
                    "no_nausea", "no_photophobia"
                ],
                red_flags=[],
                diagnostic_criteria=[
                    "Bilateral location", "Pressing/tightening quality",
                    "Mild to moderate intensity", "No aggravation by routine activity"
                ],
                treatment_options=[
                    "Acetaminophen 650mg", "Ibuprofen 400mg", "Stress management",
                    "Regular sleep schedule", "Hydration"
                ],
                prognosis="Excellent, typically resolves within hours",
                urgency_level=UrgencyLevel.ROUTINE
            ),
            
            "pneumonia": MedicalCondition(
                name="Pneumonia",
                icd_code="J18.9",
                category="respiratory",
                prevalence={
                    "elderly": 0.05,
                    "adults": 0.02,
                    "immunocompromised": 0.08
                },
                typical_symptoms=[
                    "fever", "cough", "shortness_of_breath", "chest_pain",
                    "fatigue", "chills", "purulent_sputum"
                ],
                red_flags=[
                    "high_fever", "severe_shortness_of_breath",
                    "confusion", "low_blood_pressure"
                ],
                diagnostic_criteria=[
                    "Fever + respiratory symptoms", "Chest X-ray infiltrate",
                    "Elevated white blood cells", "Physical exam findings"
                ],
                treatment_options=[
                    "Antibiotic therapy", "Supportive care", "Oxygen if needed",
                    "Hospitalization if severe", "Follow-up chest X-ray"
                ],
                prognosis="Good with appropriate treatment",
                urgency_level=UrgencyLevel.URGENT
            ),
            
            "gastroenteritis": MedicalCondition(
                name="Gastroenteritis",
                icd_code="K59.1",
                category="gastrointestinal",
                prevalence={
                    "general_population": 0.15,
                    "children": 0.25,
                    "elderly": 0.12
                },
                typical_symptoms=[
                    "nausea", "vomiting", "diarrhea", "abdominal_cramping",
                    "low_grade_fever", "dehydration"
                ],
                red_flags=[
                    "severe_dehydration", "blood_in_stool", "high_fever",
                    "severe_abdominal_pain"
                ],
                diagnostic_criteria=[
                    "Acute onset nausea/vomiting", "Diarrhea", "Abdominal pain",
                    "Recent exposure or food intake"
                ],
                treatment_options=[
                    "Oral rehydration", "BRAT diet", "Antiemetics if needed",
                    "Avoid dairy temporarily", "Gradual diet advancement"
                ],
                prognosis="Excellent, usually resolves in 3-5 days",
                urgency_level=UrgencyLevel.ROUTINE
            )
        }
        
        return conditions
    
    def _initialize_treatments_database(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive treatments database"""
        
        return {
            "cardiovascular": {
                "acute_coronary_syndrome": {
                    "immediate": ["Call 911", "Aspirin 325mg", "Nitroglycerin"],
                    "hospital": ["Cardiac catheterization", "Antiplatelet therapy", "Beta-blockers"],
                    "long_term": ["Lifestyle modification", "Cardiac rehabilitation", "Risk factor modification"]
                },
                "hypertension": {
                    "lifestyle": ["Low sodium diet", "Regular exercise", "Weight management", "Stress reduction"],
                    "medications": ["ACE inhibitors", "Thiazide diuretics", "Calcium channel blockers"],
                    "monitoring": ["Home blood pressure monitoring", "Regular physician visits"]
                }
            },
            "respiratory": {
                "asthma": {
                    "acute": ["Bronchodilators", "Systemic corticosteroids", "Oxygen"],
                    "chronic": ["Inhaled corticosteroids", "Long-acting bronchodilators", "Leukotriene modifiers"],
                    "lifestyle": ["Trigger avoidance", "Action plan", "Peak flow monitoring"]
                },
                "pneumonia": {
                    "antibiotic_therapy": ["Amoxicillin", "Azithromycin", "Fluoroquinolones"],
                    "supportive": ["Rest", "Hydration", "Fever management"],
                    "severe": ["Hospitalization", "IV antibiotics", "Oxygen therapy"]
                }
            },
            "gastrointestinal": {
                "gerd": {
                    "lifestyle": ["Elevate head of bed", "Avoid trigger foods", "Weight loss"],
                    "medications": ["Proton pump inhibitors", "H2 receptor antagonists"],
                    "severe": ["Surgical intervention (Nissen fundoplication)"]
                },
                "gastroenteritis": {
                    "hydration": ["Oral rehydration solution", "Clear fluids", "Electrolyte replacement"],
                    "dietary": ["BRAT diet", "Avoid dairy", "Gradual advancement"],
                    "medications": ["Antiemetics", "Probiotics", "Avoid antibiotics unless bacterial"]
                }
            },
            "neurological": {
                "migraine": {
                    "acute": ["Sumatriptan", "NSAIDs", "Antiemetics"],
                    "prophylactic": ["Beta-blockers", "Anticonvulsants", "Antidepressants"],
                    "lifestyle": ["Trigger identification", "Regular sleep", "Stress management"]
                },
                "tension_headache": {
                    "immediate": ["Acetaminophen", "Ibuprofen", "Rest"],
                    "prevention": ["Stress management", "Regular exercise", "Adequate sleep"],
                    "chronic": ["Tricyclic antidepressants", "Muscle relaxants"]
                }
            }
        }
    
    def _initialize_emergency_protocols(self) -> Dict[str, Dict[str, Any]]:
        """Initialize emergency response protocols"""
        
        return {
            "chest_pain_protocol": {
                "immediate_actions": [
                    "Call 911 immediately",
                    "Chew aspirin 325mg if not allergic",
                    "Nitroglycerin if prescribed",
                    "Stay calm and sit upright",
                    "Do not drive yourself"
                ],
                "assessment_priorities": [
                    "Time of onset", "Character of pain", "Radiation pattern",
                    "Associated symptoms", "Risk factors"
                ],
                "red_flags": [
                    "Crushing substernal pain", "Radiation to arm/jaw",
                    "Diaphoresis", "Shortness of breath", "Nausea/vomiting"
                ]
            },
            "stroke_protocol": {
                "immediate_actions": [
                    "Call 911 immediately",
                    "Note time of symptom onset",
                    "Keep patient calm and comfortable",
                    "Do not give food or water",
                    "Monitor airway and breathing"
                ],
                "fast_assessment": [
                    "Face - facial drooping",
                    "Arms - arm weakness",
                    "Speech - speech difficulty",
                    "Time - note onset time"
                ],
                "red_flags": [
                    "Sudden weakness", "Facial drooping", "Speech changes",
                    "Severe headache", "Vision changes", "Confusion"
                ]
            },
            "anaphylaxis_protocol": {
                "immediate_actions": [
                    "Call 911 immediately",
                    "Epinephrine auto-injector if available",
                    "Remove or avoid trigger",
                    "Position patient lying flat",
                    "Prepare for CPR if needed"
                ],
                "assessment": [
                    "Onset after exposure", "Skin reactions",
                    "Respiratory symptoms", "Cardiovascular symptoms"
                ],
                "red_flags": [
                    "Throat swelling", "Difficulty breathing", "Rapid pulse",
                    "Dizziness", "Loss of consciousness"
                ]
            }
        }
    
    def _initialize_differential_rules(self) -> Dict[str, Any]:
        """Initialize differential diagnosis rules and probability matrices"""
        
        return {
            "chest_pain_ddx": {
                "age_gender_modifiers": {
                    "male_over_40": {"cad": 1.5, "gerd": 1.0, "anxiety": 0.8},
                    "female_under_40": {"anxiety": 1.3, "gerd": 1.1, "cad": 0.6},
                    "elderly": {"cad": 2.0, "pe": 1.4, "pneumonia": 1.3}
                },
                "symptom_weights": {
                    "crushing_pain": {"mi": 3.0, "angina": 2.5},
                    "burning_pain": {"gerd": 2.8, "peptic_ulcer": 2.0},
                    "sharp_pain": {"pneumothorax": 2.5, "costochondritis": 2.0},
                    "radiation_arm": {"mi": 3.5, "angina": 3.0},
                    "diaphoresis": {"mi": 3.0, "pe": 1.5}
                }
            },
            "headache_ddx": {
                "red_flag_rules": {
                    "sudden_onset": ["subarachnoid_hemorrhage", "meningitis"],
                    "fever_neck_stiffness": ["meningitis", "encephalitis"],
                    "neurological_deficits": ["stroke", "brain_tumor", "intracranial_hemorrhage"]
                },
                "chronic_patterns": {
                    "episodic_with_aura": ["migraine"],
                    "daily_bilateral": ["tension_headache", "medication_overuse"],
                    "unilateral_severe": ["cluster_headache", "temporal_arteritis"]
                }
            }
        }
    
    def _initialize_medication_database(self) -> Dict[str, Dict[str, Any]]:
        """Initialize medication database with interactions and contraindications"""
        
        return {
            "aspirin": {
                "indications": ["MI prevention", "Stroke prevention", "Pain relief"],
                "contraindications": ["Bleeding disorders", "Active peptic ulcer", "Severe liver disease"],
                "interactions": ["Warfarin", "Methotrexate", "ACE inhibitors"],
                "dosing": {
                    "cardioprotective": "81mg daily",
                    "acute_MI": "325mg chewed once",
                    "pain": "325-650mg every 4-6 hours"
                }
            },
            "acetaminophen": {
                "indications": ["Pain relief", "Fever reduction"],
                "contraindications": ["Severe liver disease", "Alcohol abuse"],
                "interactions": ["Warfarin", "Phenytoin"],
                "dosing": {
                    "adult": "650mg every 6 hours, max 3g daily",
                    "elderly": "500mg every 6 hours, max 2.5g daily"
                }
            },
            "ibuprofen": {
                "indications": ["Pain relief", "Anti-inflammatory", "Fever reduction"],
                "contraindications": ["Kidney disease", "Heart failure", "Active bleeding"],
                "interactions": ["ACE inhibitors", "Lithium", "Warfarin"],
                "dosing": {
                    "adult": "400-600mg every 6-8 hours, max 2.4g daily"
                }
            }
        }
    
    def get_symptom_profile(self, symptom_name: str) -> Optional[SymptomProfile]:
        """Get comprehensive symptom profile"""
        return self.symptoms_database.get(symptom_name.lower().replace(" ", "_"))
    
    def get_condition_details(self, condition_name: str) -> Optional[MedicalCondition]:
        """Get detailed condition information"""
        return self.conditions_database.get(condition_name.lower().replace(" ", "_"))
    
    def get_differential_probabilities(self, symptoms: List[str], demographics: Dict[str, Any]) -> Dict[str, float]:
        """Calculate differential diagnosis probabilities based on symptoms and demographics"""
        
        probabilities = {}
        
        # Simplified probability calculation - in real implementation would be more sophisticated
        for symptom in symptoms:
            symptom_profile = self.get_symptom_profile(symptom)
            if symptom_profile:
                for condition in symptom_profile.associated_conditions:
                    if condition not in probabilities:
                        probabilities[condition] = 0.1
                    probabilities[condition] += 0.2
        
        # Normalize probabilities to sum to 100%
        total = sum(probabilities.values())
        if total > 0:
            probabilities = {k: (v/total * 100) for k, v in probabilities.items()}
        
        # Sort by probability
        return dict(sorted(probabilities.items(), key=lambda x: x[1], reverse=True))
    
    def assess_emergency_risk(self, symptoms: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess emergency risk based on symptoms and context"""
        
        risk_level = "routine"
        risk_factors = []
        
        # Check for emergency symptom combinations
        emergency_combinations = [
            (["chest_pain", "shortness_of_breath"], "critical"),
            (["sudden_headache", "neck_stiffness"], "critical"),
            (["severe_abdominal_pain", "vomiting"], "urgent"),
            (["high_fever", "confusion"], "urgent")
        ]
        
        for combination, level in emergency_combinations:
            if all(symptom in symptoms for symptom in combination):
                risk_level = level
                risk_factors.append(f"Critical combination: {' + '.join(combination)}")
        
        return {
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "emergency_protocol": self.emergency_protocols.get(f"{symptoms[0]}_protocol") if symptoms else None
        }
    
    def get_treatment_recommendations(self, condition: str, severity: str) -> List[str]:
        """Get treatment recommendations for a condition"""
        
        condition_category = self._get_condition_category(condition)
        treatments = self.treatments_database.get(condition_category, {}).get(condition, {})
        
        recommendations = []
        
        if severity in ["mild", "routine"]:
            recommendations.extend(treatments.get("lifestyle", []))
            recommendations.extend(treatments.get("immediate", [])[:2])
        elif severity in ["moderate", "urgent"]:
            recommendations.extend(treatments.get("medications", []))
            recommendations.extend(treatments.get("immediate", []))
        elif severity in ["severe", "critical"]:
            recommendations.extend(treatments.get("severe", []))
            recommendations.extend(treatments.get("hospital", []))
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _get_condition_category(self, condition: str) -> str:
        """Determine the category of a medical condition"""
        
        cardiovascular_conditions = ["myocardial_infarction", "angina", "hypertension"]
        respiratory_conditions = ["pneumonia", "asthma", "copd"]
        gastrointestinal_conditions = ["gastroenteritis", "gerd", "appendicitis"]
        neurological_conditions = ["migraine", "tension_headache", "stroke"]
        
        if condition in cardiovascular_conditions:
            return "cardiovascular"
        elif condition in respiratory_conditions:
            return "respiratory"
        elif condition in gastrointestinal_conditions:
            return "gastrointestinal"
        elif condition in neurological_conditions:
            return "neurological"
        else:
            return "general"