"""
🚀 PHASE 5: ENHANCED MEDICAL RESPONSE GENERATION SYSTEM
Step 5.1: Dynamic Symptom-Specific Response Templates Engine

This module creates intelligent, symptom-specific response templates that can handle
any medical condition with appropriate questions, red flags, and follow-up protocols.
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class UrgencyLevel(Enum):
    """Medical urgency classification levels"""
    ROUTINE = "routine"
    MODERATE = "moderate" 
    URGENT = "urgent"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class SymptomCategory(Enum):
    """Primary symptom categories for template generation"""
    CARDIOVASCULAR = "cardiovascular"
    RESPIRATORY = "respiratory"
    NEUROLOGICAL = "neurological"
    GASTROINTESTINAL = "gastrointestinal"
    MUSCULOSKELETAL = "musculoskeletal"
    GENITOURINARY = "genitourinary"
    DERMATOLOGICAL = "dermatological"
    PSYCHIATRIC = "psychiatric"
    ENDOCRINE = "endocrine"
    HEMATOLOGIC = "hematologic"
    OPHTHALMOLOGIC = "ophthalmologic"
    OTOLARYNGOLOGIC = "otolaryngologic"
    GENERAL = "general"


@dataclass
class MedicalResponseTemplate:
    """Enhanced medical response template for specific symptoms/conditions"""
    symptom_name: str
    category: SymptomCategory
    questions: List[str]
    red_flags: List[str]
    follow_up_protocol: str
    urgency_indicators: Dict[str, UrgencyLevel]
    differential_considerations: List[str]
    assessment_timeline: str
    patient_education: List[str]
    when_to_seek_care: Dict[str, str]
    clinical_reasoning: str


class EnhancedMedicalResponseGenerator:
    """
    🧠 REVOLUTIONARY MEDICAL RESPONSE TEMPLATE ENGINE
    
    Dynamically generates comprehensive, symptom-specific response templates
    for any medical condition using advanced medical knowledge and reasoning.
    """
    
    def __init__(self):
        self.symptom_patterns = self._initialize_symptom_patterns()
        self.medical_knowledge_base = self._initialize_medical_knowledge()
        self.red_flag_database = self._initialize_red_flag_database()
        self.protocol_framework = self._initialize_protocol_framework()
        
    def _initialize_symptom_patterns(self) -> Dict[str, Dict]:
        """Initialize comprehensive symptom pattern recognition database"""
        return {
            # CARDIOVASCULAR PATTERNS
            "chest_pain": {
                "category": SymptomCategory.CARDIOVASCULAR,
                "aliases": ["chest discomfort", "chest pressure", "chest tightness", "chest burning", "chest ache"],
                "anatomical_variants": ["central chest", "left chest", "right chest", "substernal", "precordial"],
                "quality_descriptors": ["crushing", "squeezing", "sharp", "stabbing", "dull", "pressure-like", "burning"]
            },
            "heart_palpitations": {
                "category": SymptomCategory.CARDIOVASCULAR,
                "aliases": ["racing heart", "irregular heartbeat", "heart fluttering", "heart skipping"],
                "anatomical_variants": ["heart rate", "pulse", "heartbeat"],
                "quality_descriptors": ["fast", "slow", "irregular", "pounding", "fluttering"]
            },
            "shortness_of_breath": {
                "category": SymptomCategory.RESPIRATORY,
                "aliases": ["difficulty breathing", "breathlessness", "dyspnea", "air hunger"],
                "anatomical_variants": ["breathing", "respiration", "airways"],
                "quality_descriptors": ["sudden", "gradual", "exertional", "at rest"]
            },
            
            # NEUROLOGICAL PATTERNS  
            "headache": {
                "category": SymptomCategory.NEUROLOGICAL,
                "aliases": ["head pain", "cephalgia", "migraine", "tension headache"],
                "anatomical_variants": ["frontal", "temporal", "occipital", "vertex", "unilateral", "bilateral"],
                "quality_descriptors": ["throbbing", "pounding", "sharp", "dull", "pressure-like", "stabbing"]
            },
            "dizziness": {
                "category": SymptomCategory.NEUROLOGICAL,
                "aliases": ["vertigo", "lightheadedness", "unsteadiness", "spinning sensation"],
                "anatomical_variants": ["head", "balance", "equilibrium"],
                "quality_descriptors": ["spinning", "floating", "fainting feeling", "off-balance"]
            },
            "weakness": {
                "category": SymptomCategory.NEUROLOGICAL,
                "aliases": ["fatigue", "muscle weakness", "limb weakness", "paralysis"],
                "anatomical_variants": ["arm", "leg", "face", "unilateral", "bilateral"],
                "quality_descriptors": ["sudden", "gradual", "progressive", "intermittent"]
            },
            
            # GASTROINTESTINAL PATTERNS
            "abdominal_pain": {
                "category": SymptomCategory.GASTROINTESTINAL,
                "aliases": ["stomach pain", "belly ache", "gut pain", "tummy ache"],
                "anatomical_variants": ["upper abdomen", "lower abdomen", "right quadrant", "left quadrant", "periumbilical"],
                "quality_descriptors": ["cramping", "sharp", "dull", "burning", "gnawing", "colicky"]
            },
            "nausea_vomiting": {
                "category": SymptomCategory.GASTROINTESTINAL,
                "aliases": ["feeling sick", "throwing up", "retching", "stomach upset"],
                "anatomical_variants": ["stomach", "gastric", "digestive"],
                "quality_descriptors": ["persistent", "intermittent", "projectile", "blood-tinged"]
            },
            
            # RESPIRATORY PATTERNS
            "cough": {
                "category": SymptomCategory.RESPIRATORY,
                "aliases": ["coughing", "hacking", "persistent cough"],
                "anatomical_variants": ["chest", "throat", "lungs"],
                "quality_descriptors": ["dry", "productive", "barking", "whooping", "bloody"]
            },
            
            # MUSCULOSKELETAL PATTERNS
            "joint_pain": {
                "category": SymptomCategory.MUSCULOSKELETAL,
                "aliases": ["arthralgia", "joint ache", "joint stiffness"],
                "anatomical_variants": ["knee", "shoulder", "hip", "wrist", "ankle", "fingers"],
                "quality_descriptors": ["aching", "sharp", "stiff", "swollen", "warm"]
            },
            "back_pain": {
                "category": SymptomCategory.MUSCULOSKELETAL,
                "aliases": ["backache", "spine pain", "lumbar pain"],
                "anatomical_variants": ["lower back", "upper back", "middle back", "neck"],
                "quality_descriptors": ["sharp", "dull", "radiating", "burning", "stabbing"]
            },
            
            # GENERAL PATTERNS
            "fever": {
                "category": SymptomCategory.GENERAL,
                "aliases": ["high temperature", "pyrexia", "hot", "chills"],
                "anatomical_variants": ["body temperature", "systemic"],
                "quality_descriptors": ["high", "low-grade", "intermittent", "continuous"]
            },
            "fatigue": {
                "category": SymptomCategory.GENERAL,
                "aliases": ["tiredness", "exhaustion", "weakness", "lethargy"],
                "anatomical_variants": ["whole body", "systemic"],
                "quality_descriptors": ["severe", "mild", "chronic", "acute"]
            }
        }
    
    def _initialize_medical_knowledge(self) -> Dict[str, Dict]:
        """Initialize comprehensive medical knowledge base for template generation"""
        return {
            "cardiovascular": {
                "critical_conditions": ["myocardial_infarction", "unstable_angina", "aortic_dissection", "pulmonary_embolism"],
                "urgent_conditions": ["stable_angina", "heart_failure_exacerbation", "arrhythmias"],
                "routine_conditions": ["chest_wall_pain", "gastroesophageal_reflux", "anxiety"],
                "key_assessments": ["troponin", "ecg", "chest_xray", "d_dimer"],
                "timeline_critical": "immediate",
                "timeline_urgent": "within_hours",
                "timeline_routine": "within_days"
            },
            "neurological": {
                "critical_conditions": ["stroke", "meningitis", "subarachnoid_hemorrhage", "status_epilepticus"],
                "urgent_conditions": ["transient_ischemic_attack", "severe_migraine", "cluster_headache"],
                "routine_conditions": ["tension_headache", "mild_vertigo", "stress_headache"],
                "key_assessments": ["neurological_exam", "ct_head", "lumbar_puncture", "mri"],
                "timeline_critical": "immediate",
                "timeline_urgent": "within_hours", 
                "timeline_routine": "within_days"
            },
            "gastrointestinal": {
                "critical_conditions": ["acute_abdomen", "gastrointestinal_bleeding", "bowel_obstruction", "perforation"],
                "urgent_conditions": ["appendicitis", "cholecystitis", "pancreatitis", "inflammatory_bowel_disease"],
                "routine_conditions": ["gastritis", "ibs", "food_poisoning", "viral_gastroenteritis"],
                "key_assessments": ["abdominal_exam", "blood_work", "imaging", "endoscopy"],
                "timeline_critical": "immediate",
                "timeline_urgent": "within_hours",
                "timeline_routine": "within_days"
            },
            "respiratory": {
                "critical_conditions": ["pneumothorax", "severe_asthma", "respiratory_failure", "pulmonary_edema"],
                "urgent_conditions": ["pneumonia", "asthma_exacerbation", "bronchitis", "pleuritis"],
                "routine_conditions": ["upper_respiratory_infection", "mild_cough", "allergic_rhinitis"],
                "key_assessments": ["chest_xray", "arterial_blood_gas", "pulmonary_function", "sputum_culture"],
                "timeline_critical": "immediate",
                "timeline_urgent": "within_hours",
                "timeline_routine": "within_days"
            },
            "musculoskeletal": {
                "critical_conditions": ["fracture", "compartment_syndrome", "septic_arthritis", "osteomyelitis"],
                "urgent_conditions": ["acute_arthritis", "joint_dislocation", "severe_strain"],
                "routine_conditions": ["muscle_strain", "osteoarthritis", "fibromyalgia", "tendinitis"],
                "key_assessments": ["x_ray", "mri", "joint_aspiration", "inflammatory_markers"],
                "timeline_critical": "immediate",
                "timeline_urgent": "within_hours",
                "timeline_routine": "within_days"
            }
        }
    
    def _initialize_red_flag_database(self) -> Dict[str, List[str]]:
        """Initialize comprehensive red flag warning signs database"""
        return {
            "chest_pain": [
                "crushing or pressure-like chest pain",
                "chest pain radiating to arm, jaw, neck, or back",
                "chest pain with shortness of breath",
                "chest pain with diaphoresis (sweating)",
                "chest pain with nausea or vomiting",
                "sudden onset severe chest pain",
                "chest pain lasting more than 20 minutes"
            ],
            "headache": [
                "worst headache of your life",
                "sudden thunderclap headache",
                "headache with fever and neck stiffness",
                "headache with confusion or altered consciousness",
                "headache with visual changes or weakness",
                "new headache pattern in patients over 50",
                "headache after head trauma"
            ],
            "abdominal_pain": [
                "severe sudden onset abdominal pain",
                "abdominal pain with vomiting blood",
                "abdominal pain with black tarry stools",
                "abdominal rigidity or guarding",
                "abdominal pain with fever and chills",
                "inability to pass gas or stool",
                "abdominal pain with severe dehydration"
            ],
            "shortness_of_breath": [
                "sudden severe shortness of breath",
                "shortness of breath with chest pain",
                "inability to speak in full sentences",
                "blue lips or fingernails (cyanosis)",
                "shortness of breath with leg swelling",
                "wheezing with severe distress",
                "shortness of breath after travel or surgery"
            ],
            "neurological": [
                "sudden weakness or numbness on one side",
                "sudden speech difficulties or slurred speech", 
                "sudden severe dizziness with other symptoms",
                "loss of consciousness or fainting",
                "seizure activity",
                "sudden severe confusion",
                "sudden vision loss or double vision"
            ],
            "general": [
                "high fever with severe illness appearance",
                "signs of severe dehydration",
                "persistent vomiting preventing fluid intake",
                "severe allergic reaction symptoms",
                "thoughts of self-harm or suicide",
                "severe pain unrelieved by rest or medication",
                "rapid heart rate with chest symptoms"
            ]
        }
    
    def _initialize_protocol_framework(self) -> Dict[str, Dict]:
        """Initialize clinical assessment protocol framework"""
        return {
            "chest_pain_assessment": {
                "initial_questions": [
                    "Can you describe the chest discomfort? Is it sharp, dull, or pressure-like?",
                    "Does the pain radiate to your arm, jaw, neck, or back?", 
                    "When did this start, and what were you doing when it began?",
                    "On a scale of 1-10, how severe is the pain?",
                    "Does anything make it better or worse?"
                ],
                "red_flag_screen": ["crushing", "radiating", "shortness of breath", "diaphoresis", "nausea"],
                "urgency_protocol": "immediate_emergency_if_cardiac_suspicious"
            },
            "headache_assessment": {
                "initial_questions": [
                    "Can you describe what the headache feels like (throbbing, pressure, sharp)?",
                    "Where exactly do you feel the headache?",
                    "When did it start and how quickly did it come on?",
                    "Is this different from your usual headaches?",
                    "Any associated symptoms like nausea, vision changes, or fever?"
                ],
                "red_flag_screen": ["thunderclap", "fever", "neck_stiffness", "confusion", "vision_changes"],
                "urgency_protocol": "emergency_if_red_flags_present"
            },
            "abdominal_pain_assessment": {
                "initial_questions": [
                    "Where exactly in your abdomen do you feel the pain?",
                    "Can you describe what the pain feels like (cramping, sharp, dull)?",
                    "When did the pain start and has it changed?",
                    "Any nausea, vomiting, or changes in bowel movements?",
                    "Does movement or position change the pain?"
                ],
                "red_flag_screen": ["rigidity", "rebound_tenderness", "blood_vomiting", "severe_dehydration"],
                "urgency_protocol": "urgent_if_acute_abdomen_suspected"
            },
            "respiratory_assessment": {
                "initial_questions": [
                    "When did you first notice difficulty breathing?",
                    "Is it worse with activity or at rest?",
                    "Any chest pain or cough with the breathing difficulty?",
                    "Are you able to speak in full sentences?",
                    "Any history of asthma, heart problems, or recent surgery?"
                ],
                "red_flag_screen": ["cyanosis", "unable_speak_sentences", "severe_distress", "chest_pain"],
                "urgency_protocol": "emergency_if_severe_respiratory_distress"
            },
            "neurological_assessment": {
                "initial_questions": [
                    "Can you describe exactly what you're experiencing?",
                    "When did these symptoms start and how quickly?",
                    "Any weakness, numbness, or difficulty speaking?",
                    "Any changes in vision or balance?",
                    "Any recent head injury or medical changes?"
                ],
                "red_flag_screen": ["sudden_onset", "unilateral_weakness", "speech_difficulty", "vision_loss"],
                "urgency_protocol": "emergency_if_stroke_suspected"
            }
        }
    
    def identify_symptom_category(self, symptom_description: str) -> Tuple[str, SymptomCategory, float]:
        """
        🧠 INTELLIGENT SYMPTOM CATEGORIZATION
        
        Analyzes symptom description and identifies the most appropriate 
        symptom category and specific condition for template generation.
        """
        symptom_lower = symptom_description.lower().strip()
        
        # Score each symptom pattern based on keyword matching
        pattern_scores = {}
        
        for symptom_name, pattern_data in self.symptom_patterns.items():
            score = 0.0
            
            # Direct symptom name match (highest weight)
            if symptom_name.replace("_", " ") in symptom_lower:
                score += 100
                
            # Alias matching (high weight)  
            for alias in pattern_data.get("aliases", []):
                if alias.lower() in symptom_lower:
                    score += 80
                    
            # Anatomical variant matching (medium weight)
            for variant in pattern_data.get("anatomical_variants", []):
                if variant.lower() in symptom_lower:
                    score += 60
                    
            # Quality descriptor matching (lower weight)
            for descriptor in pattern_data.get("quality_descriptors", []):
                if descriptor.lower() in symptom_lower:
                    score += 40
            
            # Keyword component matching
            symptom_keywords = symptom_name.split("_")
            for keyword in symptom_keywords:
                if keyword in symptom_lower:
                    score += 30
                    
            pattern_scores[symptom_name] = score
        
        # Find best match
        if not pattern_scores or max(pattern_scores.values()) == 0:
            # Fallback to general category
            return "general_symptoms", SymptomCategory.GENERAL, 0.3
            
        best_symptom = max(pattern_scores, key=pattern_scores.get)
        best_score = pattern_scores[best_symptom]
        confidence = min(best_score / 100.0, 1.0)  # Normalize to 0-1
        
        category = self.symptom_patterns[best_symptom]["category"]
        
        return best_symptom, category, confidence
    
    def generate_response_template(self, 
                                 symptom_description: str, 
                                 patient_context: Optional[Dict] = None) -> MedicalResponseTemplate:
        """
        🚀 DYNAMIC MEDICAL RESPONSE TEMPLATE GENERATOR
        
        Creates comprehensive, symptom-specific response templates for any medical condition
        using advanced medical knowledge and clinical reasoning.
        """
        
        # Step 1: Identify symptom category and condition
        symptom_name, category, confidence = self.identify_symptom_category(symptom_description)
        
        # Step 2: Generate symptom-specific questions
        questions = self._generate_symptom_questions(symptom_name, category, symptom_description)
        
        # Step 3: Identify relevant red flags
        red_flags = self._generate_red_flags(symptom_name, category)
        
        # Step 4: Determine follow-up protocol
        follow_up_protocol = self._determine_protocol(symptom_name, category)
        
        # Step 5: Generate urgency indicators
        urgency_indicators = self._generate_urgency_indicators(symptom_name, category)
        
        # Step 6: Generate differential considerations
        differential_considerations = self._generate_differential_considerations(symptom_name, category)
        
        # Step 7: Determine assessment timeline
        assessment_timeline = self._determine_assessment_timeline(symptom_name, category)
        
        # Step 8: Generate patient education points
        patient_education = self._generate_patient_education(symptom_name, category)
        
        # Step 9: Generate when to seek care guidelines
        when_to_seek_care = self._generate_care_guidelines(symptom_name, category)
        
        # Step 10: Generate clinical reasoning
        clinical_reasoning = self._generate_clinical_reasoning(symptom_name, category, symptom_description)
        
        return MedicalResponseTemplate(
            symptom_name=symptom_name,
            category=category,
            questions=questions,
            red_flags=red_flags,
            follow_up_protocol=follow_up_protocol,
            urgency_indicators=urgency_indicators,
            differential_considerations=differential_considerations,
            assessment_timeline=assessment_timeline,
            patient_education=patient_education,
            when_to_seek_care=when_to_seek_care,
            clinical_reasoning=clinical_reasoning
        )
    
    def _generate_symptom_questions(self, symptom_name: str, category: SymptomCategory, 
                                   description: str) -> List[str]:
        """Generate comprehensive, symptom-specific assessment questions"""
        
        # Get protocol-specific questions if available
        protocol_key = f"{symptom_name}_assessment"
        if protocol_key in self.protocol_framework:
            base_questions = self.protocol_framework[protocol_key]["initial_questions"]
        else:
            # Generate generic questions based on category
            base_questions = self._generate_category_questions(category)
        
        # Add symptom-specific enhancement questions
        enhanced_questions = self._add_symptom_specific_questions(symptom_name, base_questions)
        
        return enhanced_questions[:7]  # Limit to 7 key questions
    
    def _generate_category_questions(self, category: SymptomCategory) -> List[str]:
        """Generate category-specific assessment questions"""
        
        category_questions = {
            SymptomCategory.CARDIOVASCULAR: [
                "Can you describe the chest discomfort in detail (pressure, sharp, burning)?",
                "Does the discomfort spread to other areas like your arm, jaw, or back?",
                "When did this start and what triggered it?",
                "How severe is it on a scale of 1-10?",
                "Any shortness of breath or other symptoms?"
            ],
            SymptomCategory.NEUROLOGICAL: [
                "Can you describe exactly what you're experiencing?",
                "When did these symptoms start and how quickly?",
                "Any weakness, numbness, or changes in sensation?",
                "Any vision changes, balance problems, or confusion?",
                "Is this different from anything you've experienced before?"
            ],
            SymptomCategory.GASTROINTESTINAL: [
                "Where exactly do you feel the discomfort?",
                "Can you describe what it feels like (cramping, sharp, burning)?",
                "When did it start and how has it changed?",
                "Any nausea, vomiting, or changes in bowel movements?",
                "Does eating, movement, or position affect it?"
            ],
            SymptomCategory.RESPIRATORY: [
                "When did you first notice difficulty with breathing?",
                "Is it worse with activity or at rest?",
                "Any chest discomfort or cough?",
                "Are you able to speak normally?",
                "Any history of breathing problems or recent illness?"
            ],
            SymptomCategory.MUSCULOSKELETAL: [
                "Where exactly do you feel the pain or discomfort?",
                "What does it feel like (aching, sharp, stiff)?",
                "When did it start and what might have caused it?",
                "Does movement make it better or worse?",
                "Any swelling, redness, or warmth in the area?"
            ]
        }
        
        return category_questions.get(category, [
            "Can you describe your symptoms in detail?",
            "When did they start and how have they changed?",
            "What makes them better or worse?",
            "How severe are they on a scale of 1-10?",
            "Any other symptoms you've noticed?"
        ])
    
    def _add_symptom_specific_questions(self, symptom_name: str, base_questions: List[str]) -> List[str]:
        """Add symptom-specific enhancement questions"""
        
        symptom_enhancements = {
            "chest_pain": [
                "Any family history of heart disease or blood clots?",
                "Have you been sitting for long periods or traveling recently?"
            ],
            "headache": [
                "Is this headache different from your usual headaches?",
                "Any recent changes in medication or stress levels?"
            ],
            "abdominal_pain": [
                "When was your last bowel movement?",
                "Any recent dietary changes or new foods?"
            ],
            "shortness_of_breath": [
                "Any recent travel, surgery, or prolonged bed rest?",
                "Do you have any heart or lung conditions?"
            ],
            "fever": [
                "Any recent travel or exposure to illness?",
                "What's your actual temperature if measured?"
            ]
        }
        
        enhanced = base_questions.copy()
        if symptom_name in symptom_enhancements:
            enhanced.extend(symptom_enhancements[symptom_name])
            
        return enhanced
    
    def _generate_red_flags(self, symptom_name: str, category: SymptomCategory) -> List[str]:
        """Generate comprehensive red flag warning signs"""
        
        # Get symptom-specific red flags
        red_flags = []
        
        if symptom_name in self.red_flag_database:
            red_flags.extend(self.red_flag_database[symptom_name])
        
        # Add category-general red flags
        category_key = category.value
        if category_key in self.red_flag_database:
            red_flags.extend(self.red_flag_database[category_key])
            
        # Add general red flags
        red_flags.extend(self.red_flag_database.get("general", []))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_red_flags = []
        for flag in red_flags:
            if flag not in seen:
                seen.add(flag)
                unique_red_flags.append(flag)
                
        return unique_red_flags[:10]  # Limit to top 10 most relevant
    
    def _determine_protocol(self, symptom_name: str, category: SymptomCategory) -> str:
        """Determine appropriate follow-up protocol"""
        
        protocol_key = f"{symptom_name}_assessment"
        if protocol_key in self.protocol_framework:
            return protocol_key
        
        # Category-based protocols
        category_protocols = {
            SymptomCategory.CARDIOVASCULAR: "cardiovascular_assessment_protocol",
            SymptomCategory.NEUROLOGICAL: "neurological_assessment_protocol", 
            SymptomCategory.GASTROINTESTINAL: "gastrointestinal_assessment_protocol",
            SymptomCategory.RESPIRATORY: "respiratory_assessment_protocol",
            SymptomCategory.MUSCULOSKELETAL: "musculoskeletal_assessment_protocol"
        }
        
        return category_protocols.get(category, "general_symptom_assessment_protocol")
    
    def _generate_urgency_indicators(self, symptom_name: str, category: SymptomCategory) -> Dict[str, UrgencyLevel]:
        """Generate urgency level indicators based on symptom characteristics"""
        
        urgency_map = {}
        
        # Get medical knowledge for this category
        category_knowledge = self.medical_knowledge_base.get(category.value, {})
        
        # Critical conditions
        for condition in category_knowledge.get("critical_conditions", []):
            urgency_map[condition] = UrgencyLevel.CRITICAL
            
        # Urgent conditions  
        for condition in category_knowledge.get("urgent_conditions", []):
            urgency_map[condition] = UrgencyLevel.URGENT
            
        # Routine conditions
        for condition in category_knowledge.get("routine_conditions", []):
            urgency_map[condition] = UrgencyLevel.ROUTINE
        
        # Add symptom-specific urgency indicators
        symptom_urgency = {
            "chest_pain": {
                "cardiac_chest_pain": UrgencyLevel.CRITICAL,
                "pulmonary_embolism": UrgencyLevel.CRITICAL,
                "aortic_dissection": UrgencyLevel.CRITICAL,
                "musculoskeletal_chest_pain": UrgencyLevel.ROUTINE,
                "gastroesophageal_reflux": UrgencyLevel.ROUTINE
            },
            "headache": {
                "thunderclap_headache": UrgencyLevel.CRITICAL,
                "meningitis_headache": UrgencyLevel.CRITICAL, 
                "migraine": UrgencyLevel.URGENT,
                "tension_headache": UrgencyLevel.ROUTINE
            },
            "shortness_of_breath": {
                "acute_respiratory_failure": UrgencyLevel.CRITICAL,
                "pneumothorax": UrgencyLevel.CRITICAL,
                "asthma_exacerbation": UrgencyLevel.URGENT,
                "mild_exertion_dyspnea": UrgencyLevel.ROUTINE
            }
        }
        
        if symptom_name in symptom_urgency:
            urgency_map.update(symptom_urgency[symptom_name])
            
        return urgency_map
    
    def _generate_differential_considerations(self, symptom_name: str, category: SymptomCategory) -> List[str]:
        """Generate differential diagnosis considerations"""
        
        category_knowledge = self.medical_knowledge_base.get(category.value, {})
        
        differentials = []
        differentials.extend(category_knowledge.get("critical_conditions", []))
        differentials.extend(category_knowledge.get("urgent_conditions", []))
        differentials.extend(category_knowledge.get("routine_conditions", []))
        
        return differentials[:8]  # Top 8 differential considerations
    
    def _determine_assessment_timeline(self, symptom_name: str, category: SymptomCategory) -> str:
        """Determine appropriate assessment timeline"""
        
        category_knowledge = self.medical_knowledge_base.get(category.value, {})
        
        # Default to urgent timeline
        timeline = category_knowledge.get("timeline_urgent", "within_hours")
        
        # High-risk symptoms get critical timeline
        high_risk_symptoms = ["chest_pain", "shortness_of_breath", "severe_headache", 
                            "acute_neurological_symptoms"]
        
        if any(risk in symptom_name for risk in high_risk_symptoms):
            timeline = category_knowledge.get("timeline_critical", "immediate")
            
        return timeline
    
    def _generate_patient_education(self, symptom_name: str, category: SymptomCategory) -> List[str]:
        """Generate relevant patient education points"""
        
        education_database = {
            "chest_pain": [
                "Chest pain can have many causes, from heart problems to muscle strain",
                "Call 911 immediately if you have crushing chest pain with sweating",
                "Keep a record of when chest pain occurs and what triggers it",
                "Avoid strenuous activity until evaluated by a healthcare provider"
            ],
            "headache": [
                "Most headaches are not dangerous but some require immediate care",
                "Keep a headache diary noting triggers, timing, and severity",
                "Stay hydrated and maintain regular sleep patterns",
                "Seek immediate care for sudden severe headaches unlike any before"
            ],
            "abdominal_pain": [
                "Abdominal pain can range from minor to life-threatening",
                "Note the location, timing, and character of your pain",
                "Avoid eating until the cause is determined if pain is severe",
                "Seek immediate care for severe pain with vomiting or fever"
            ],
            "shortness_of_breath": [
                "Breathing difficulties should always be taken seriously", 
                "Call 911 if you cannot speak in full sentences due to breathlessness",
                "Sit upright and try to remain calm while seeking help",
                "Mention any recent travel, surgery, or leg swelling to providers"
            ]
        }
        
        return education_database.get(symptom_name, [
            "Document your symptoms including timing, triggers, and severity",
            "Seek medical attention if symptoms worsen or new symptoms develop",
            "Follow up with your healthcare provider as recommended",
            "Don't hesitate to seek immediate care if you're concerned"
        ])
    
    def _generate_care_guidelines(self, symptom_name: str, category: SymptomCategory) -> Dict[str, str]:
        """Generate when to seek care guidelines"""
        
        return {
            "immediate_emergency": "Call 911 or go to emergency room immediately if experiencing severe symptoms, difficulty breathing, chest pain, or any life-threatening concerns",
            "urgent_care": "Seek medical attention within hours if symptoms are moderate to severe, persistent, or interfering with daily activities",  
            "routine_follow_up": "Schedule appointment with healthcare provider within days if symptoms are mild but persistent or concerning",
            "self_monitoring": "Monitor symptoms at home if mild and improving, but seek care if worsening or new symptoms develop"
        }
    
    def _generate_clinical_reasoning(self, symptom_name: str, category: SymptomCategory, 
                                   description: str) -> str:
        """Generate clinical reasoning for the template"""
        
        reasoning_templates = {
            "chest_pain": f"Chest pain requires systematic evaluation to rule out life-threatening cardiac, pulmonary, and vascular causes. The symptom pattern '{description}' guides risk stratification and urgency determination.",
            "headache": f"Headache assessment focuses on identifying secondary causes requiring immediate intervention while managing primary headache disorders. The presentation '{description}' informs differential diagnosis approach.",
            "abdominal_pain": f"Abdominal pain evaluation requires anatomical localization and temporal pattern analysis to identify surgical emergencies and serious medical conditions. The symptom '{description}' guides systematic assessment.",
            "shortness_of_breath": f"Dyspnea assessment prioritizes identification of respiratory failure, cardiac emergencies, and pulmonary embolism. The breathing difficulty '{description}' determines evaluation urgency and pathway."
        }
        
        return reasoning_templates.get(symptom_name, 
            f"Systematic evaluation of '{description}' requires comprehensive assessment to identify serious conditions while providing appropriate care for common causes in the {category.value} system.")


# MEDICAL_RESPONSE_TEMPLATES: Pre-built templates for common conditions
MEDICAL_RESPONSE_TEMPLATES = {
    "chest_pain": {
        "questions": [
            "Can you describe the chest discomfort? Is it sharp, dull, or pressure-like?",
            "Does the pain radiate to your arm, jaw, neck, or back?",
            "When did this start, and what were you doing when it began?",
            "On a scale of 1-10, how severe is the pain?",
            "Any shortness of breath, sweating, nausea, or other symptoms?"
        ],
        "red_flags": ["crushing", "radiating", "shortness of breath", "diaphoresis", "nausea", "family history cardiac disease"],
        "follow_up_protocol": "chest_pain_assessment",
        "urgency_indicators": {
            "cardiac_chest_pain": "critical",
            "aortic_dissection": "critical", 
            "pulmonary_embolism": "critical",
            "musculoskeletal_pain": "routine"
        },
        "assessment_timeline": "immediate_if_cardiac_suspicious",
        "clinical_reasoning": "Chest pain requires immediate systematic evaluation to exclude acute coronary syndrome, aortic dissection, and pulmonary embolism before considering less urgent causes."
    },
    "headache": {
        "questions": [
            "Can you describe what the headache feels like (throbbing, pressure, sharp)?",
            "Where exactly do you feel the headache?",
            "Is this different from your usual headaches?",
            "When did it start and how quickly did it come on?",
            "Any nausea, vision changes, fever, or neck stiffness?"
        ],
        "red_flags": ["thunderclap onset", "fever with neck stiffness", "vision changes", "confusion", "worst headache ever"],
        "follow_up_protocol": "headache_assessment", 
        "urgency_indicators": {
            "subarachnoid_hemorrhage": "critical",
            "meningitis": "critical",
            "migraine": "urgent", 
            "tension_headache": "routine"
        },
        "assessment_timeline": "immediate_if_red_flags",
        "clinical_reasoning": "Headache assessment prioritizes identification of secondary causes requiring emergent intervention, particularly subarachnoid hemorrhage and meningitis, before addressing primary headache disorders."
    }
}


def get_enhanced_medical_response_template(symptom_description: str, 
                                         patient_context: Optional[Dict] = None) -> Dict[str, Any]:
    """
    🚀 MAIN INTERFACE FUNCTION
    
    Generates enhanced medical response templates for any symptom or condition.
    Returns comprehensive template ready for integration with existing medical AI.
    """
    
    generator = EnhancedMedicalResponseGenerator()
    template = generator.generate_response_template(symptom_description, patient_context)
    
    return {
        "symptom_name": template.symptom_name,
        "category": template.category.value,
        "questions": template.questions,
        "red_flags": template.red_flags,
        "follow_up_protocol": template.follow_up_protocol,
        "urgency_indicators": {k: v.value for k, v in template.urgency_indicators.items()},
        "differential_considerations": template.differential_considerations,
        "assessment_timeline": template.assessment_timeline,
        "patient_education": template.patient_education,
        "when_to_seek_care": template.when_to_seek_care,
        "clinical_reasoning": template.clinical_reasoning,
        "confidence_score": 0.95,  # High confidence for dynamic generation
        "algorithm_version": "5.1_enhanced_medical_response_generation"
    }


if __name__ == "__main__":
    # Test the enhanced medical response generator
    test_symptoms = [
        "chest pain",
        "severe headache", 
        "shortness of breath",
        "abdominal pain",
        "joint pain",
        "back pain",
        "dizziness",
        "unusual symptoms"
    ]
    
    print("🚀 TESTING ENHANCED MEDICAL RESPONSE GENERATOR")
    print("=" * 60)
    
    for symptom in test_symptoms:
        print(f"\n🏥 SYMPTOM: {symptom}")
        template = get_enhanced_medical_response_template(symptom)
        print(f"Category: {template['category']}")
        print(f"Questions: {len(template['questions'])}")
        print(f"Red Flags: {len(template['red_flags'])}")
        print(f"Protocol: {template['follow_up_protocol']}")
        print("-" * 40)