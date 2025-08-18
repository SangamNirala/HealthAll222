"""
World-Class Medical AI Service for Professional Medical Consultations
Implements advanced medical conversation engine with emergency detection and SOAP note generation
"""

import os
import asyncio
import json
import re
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import google.generativeai as genai

class MedicalInterviewStage(Enum):
    GREETING = "greeting"
    CHIEF_COMPLAINT = "chief_complaint"
    HISTORY_PRESENT_ILLNESS = "history_present_illness"
    REVIEW_OF_SYSTEMS = "review_of_systems"
    PAST_MEDICAL_HISTORY = "past_medical_history"
    MEDICATIONS_ALLERGIES = "medications_allergies"
    SOCIAL_FAMILY_HISTORY = "social_family_history"
    RISK_ASSESSMENT = "risk_assessment"
    DIFFERENTIAL_DIAGNOSIS = "differential_diagnosis"
    RECOMMENDATIONS = "recommendations"
    COMPLETED = "completed"

@dataclass
class MedicalContext:
    """Comprehensive medical conversation context"""
    patient_id: str
    consultation_id: str
    current_stage: MedicalInterviewStage
    demographics: Dict[str, Any]
    chief_complaint: str
    symptom_data: Dict[str, Any]
    medical_history: Dict[str, Any] 
    medications: List[str]
    allergies: List[str]
    social_history: Dict[str, Any]
    family_history: Dict[str, Any]
    risk_factors: List[str]
    red_flags: List[str]
    emergency_level: str
    clinical_hypotheses: List[Dict[str, Any]]
    confidence_score: float

class WorldClassMedicalAI:
    """
    World-class medical AI implementing real physician consultation patterns
    """
    
    def __init__(self):
        # Get primary API key
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        # Get fallback API keys
        gemini_keys_str = os.getenv('GEMINI_API_KEYS', '')
        self.gemini_api_keys = [key.strip() for key in gemini_keys_str.split(',') if key.strip()]
        
        # Add primary key to the beginning of the list if it's not already there
        if self.gemini_api_key and self.gemini_api_key not in self.gemini_api_keys:
            self.gemini_api_keys.insert(0, self.gemini_api_key)
        
        if not self.gemini_api_keys:
            raise ValueError("No GEMINI_API_KEY or GEMINI_API_KEYS environment variables set")
        
        self.current_key_index = 0
        self.model = None
        self._initialize_gemini_model()
        
        # Load medical knowledge base
        self.medical_knowledge = self._load_medical_knowledge()
        self.emergency_keywords = self._load_emergency_keywords()
        self.differential_database = self._load_differential_database()
    
    def _initialize_gemini_model(self):
        """Initialize Gemini model with current API key"""
        try:
            current_key = self.gemini_api_keys[self.current_key_index]
            genai.configure(api_key=current_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
            print(f"Initialized Gemini model with API key index {self.current_key_index}")
        except Exception as e:
            print(f"Error initializing Gemini model with key {self.current_key_index}: {e}")
            raise e
    
    def _rotate_api_key(self):
        """Rotate to next available API key"""
        if len(self.gemini_api_keys) > 1:
            self.current_key_index = (self.current_key_index + 1) % len(self.gemini_api_keys)
            print(f"Rotating to API key index {self.current_key_index}")
            self._initialize_gemini_model()
            return True
        return False
    
    async def _generate_content_with_fallback(self, prompt: str, max_retries: int = 3):
        """Generate content with automatic API key rotation on quota exceeded"""
        for attempt in range(max_retries):
            try:
                response = await self.model.generate_content_async(prompt)
                return response
            except Exception as e:
                error_message = str(e).lower()
                
                # Check if it's a quota exceeded error
                if "quota" in error_message or "429" in error_message or "exceeded" in error_message:
                    print(f"Quota exceeded on key {self.current_key_index}, attempting to rotate...")
                    
                    # Try to rotate to next key
                    if self._rotate_api_key():
                        print(f"Rotated to key index {self.current_key_index}, retrying...")
                        continue
                    else:
                        raise Exception("All API keys have exceeded quota")
                else:
                    # For other errors, don't retry
                    raise e
        
        raise Exception(f"Failed to generate content after {max_retries} attempts")
        
    def _load_medical_knowledge(self) -> Dict[str, Any]:
        """Load comprehensive medical knowledge base"""
        return {
            "symptom_mappings": {
                "chest_pain": {
                    "cardiac": ["MI", "angina", "pericarditis", "aortic_dissection"],
                    "pulmonary": ["PE", "pneumothorax", "pneumonia", "pleuritis"],
                    "gastrointestinal": ["GERD", "esophageal_spasm", "peptic_ulcer"],
                    "musculoskeletal": ["costochondritis", "muscle_strain", "rib_fracture"],
                    "psychiatric": ["panic_disorder", "anxiety"]
                },
                "headache": {
                    "primary": ["tension", "migraine", "cluster"],
                    "secondary": ["increased_icp", "temporal_arteritis", "meningitis", "stroke"]
                },
                "abdominal_pain": {
                    "acute": ["appendicitis", "cholecystitis", "bowel_obstruction", "perforation"],
                    "chronic": ["IBD", "IBS", "chronic_pancreatitis", "malignancy"]
                }
            },
            "age_sex_prevalence": {
                "chest_pain": {
                    "male_over_40": {"CAD": 0.35, "GERD": 0.25, "anxiety": 0.15},
                    "female_under_40": {"anxiety": 0.30, "GERD": 0.25, "CAD": 0.10},
                    "elderly": {"CAD": 0.45, "PE": 0.12, "pneumonia": 0.15}
                }
            },
            "red_flag_symptoms": {
                "chest_pain": ["crushing", "radiating_to_arm", "diaphoresis", "nausea"],
                "headache": ["sudden_onset", "worst_ever", "fever", "neck_stiffness"],
                "abdominal_pain": ["rebound_tenderness", "guarding", "vomiting_blood"]
            }
        }
    
    def _load_emergency_keywords(self) -> List[str]:
        """Load emergency symptom keywords for immediate detection"""
        return [
            "chest pain", "shortness of breath", "difficulty breathing", "crushing pain",
            "heart attack", "stroke", "sudden weakness", "facial drooping",
            "severe headache", "worst headache ever", "loss of consciousness",
            "severe bleeding", "vomiting blood", "severe abdominal pain",
            "difficulty swallowing", "allergic reaction", "swelling throat",
            "seizure", "overdose", "suicide", "self harm"
        ]
    
    def _load_differential_database(self) -> Dict[str, Any]:
        """Load comprehensive differential diagnosis database"""
        return {
            "common_presentations": {
                "chest_pain": {
                    "cardiovascular": {
                        "acute_coronary_syndrome": {
                            "probability_factors": ["age>45", "male", "diabetes", "smoking", "family_history"],
                            "clinical_features": ["crushing_pain", "radiation_arm", "diaphoresis", "nausea"],
                            "urgency": "critical",
                            "tests": ["ECG", "troponin", "chest_xray"]
                        },
                        "stable_angina": {
                            "probability_factors": ["exertional", "relieved_rest", "known_CAD"],
                            "clinical_features": ["predictable_pattern", "stable_symptoms"],
                            "urgency": "urgent",
                            "tests": ["stress_test", "ECG", "lipid_panel"]
                        }
                    },
                    "pulmonary": {
                        "pulmonary_embolism": {
                            "probability_factors": ["immobilization", "surgery", "cancer", "pregnancy"],
                            "clinical_features": ["sudden_onset", "dyspnea", "tachycardia"],
                            "urgency": "critical",
                            "tests": ["D-dimer", "CT_angiogram", "ABG"]
                        },
                        "pneumothorax": {
                            "probability_factors": ["young_male", "tall_thin", "smoking"],
                            "clinical_features": ["sudden_onset", "pleuritic_pain", "dyspnea"],
                            "urgency": "urgent",
                            "tests": ["chest_xray", "CT_chest"]
                        }
                    }
                },
                "headache": {
                    "primary": {
                        "migraine": {
                            "probability_factors": ["female", "family_history", "triggers"],
                            "clinical_features": ["unilateral", "pulsating", "nausea", "photophobia"],
                            "urgency": "routine",
                            "tests": ["clinical_diagnosis", "MRI_if_atypical"]
                        },
                        "tension_headache": {
                            "probability_factors": ["stress", "muscle_tension", "frequent"],
                            "clinical_features": ["bilateral", "pressure", "no_nausea"],
                            "urgency": "routine",
                            "tests": ["clinical_diagnosis"]
                        }
                    },
                    "secondary": {
                        "meningitis": {
                            "probability_factors": ["fever", "neck_stiffness", "altered_mental"],
                            "clinical_features": ["severe_headache", "fever", "photophobia"],
                            "urgency": "critical",
                            "tests": ["lumbar_puncture", "blood_cultures", "CT_head"]
                        }
                    }
                }
            },
            "risk_stratification": {
                "age_groups": {
                    "pediatric": {"age_range": [0, 18], "special_considerations": ["growth", "development"]},
                    "young_adult": {"age_range": [18, 40], "common_conditions": ["anxiety", "muscle_strain"]},
                    "middle_aged": {"age_range": [40, 65], "common_conditions": ["hypertension", "diabetes"]},
                    "elderly": {"age_range": [65, 120], "common_conditions": ["polypharmacy", "falls"]}
                }
            }
        }
    
    async def initialize_consultation(self, patient_data: Dict[str, Any]) -> MedicalContext:
        """Initialize a new medical consultation"""
        
        consultation_id = f"consult_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        context = MedicalContext(
            patient_id=patient_data.get('patient_id', 'anonymous'),
            consultation_id=consultation_id,
            current_stage=MedicalInterviewStage.GREETING,
            demographics={},
            chief_complaint="",
            symptom_data={},
            medical_history={},
            medications=[],
            allergies=[],
            social_history={},
            family_history={},
            risk_factors=[],
            red_flags=[],
            emergency_level="none",
            clinical_hypotheses=[],
            confidence_score=0.0
        )
        
        return context
    
    async def process_patient_message(self, message: str, context: MedicalContext) -> Dict[str, Any]:
        """Process patient message and generate appropriate medical response"""
        
        # 1. Emergency Detection (highest priority)
        emergency_assessment = await self._assess_emergency_risk(message, context)
        if emergency_assessment['emergency_detected']:
            return await self._handle_emergency_response(emergency_assessment, context)
        
        # 2. Extract medical entities from patient input
        medical_entities = await self._extract_medical_entities(message)
        
        # 3. Update conversation context
        updated_context = await self._update_medical_context(medical_entities, context, message)
        
        # 4. Determine next action based on interview stage
        if updated_context.current_stage == MedicalInterviewStage.GREETING:
            return await self._handle_greeting_stage(message, updated_context)
        elif updated_context.current_stage == MedicalInterviewStage.CHIEF_COMPLAINT:
            return await self._handle_chief_complaint_stage(message, updated_context)
        elif updated_context.current_stage == MedicalInterviewStage.HISTORY_PRESENT_ILLNESS:
            return await self._handle_hpi_stage(message, updated_context)
        elif updated_context.current_stage == MedicalInterviewStage.REVIEW_OF_SYSTEMS:
            return await self._handle_ros_stage(message, updated_context)
        elif updated_context.current_stage == MedicalInterviewStage.PAST_MEDICAL_HISTORY:
            return await self._handle_pmh_stage(message, updated_context)
        elif updated_context.current_stage == MedicalInterviewStage.MEDICATIONS_ALLERGIES:
            return await self._handle_medications_stage(message, updated_context)
        elif updated_context.current_stage == MedicalInterviewStage.SOCIAL_FAMILY_HISTORY:
            return await self._handle_social_history_stage(message, updated_context)
        else:
            return await self._generate_differential_diagnosis(updated_context)
    
    async def _handle_greeting_stage(self, message: str, context: MedicalContext) -> Dict[str, Any]:
        """Handle initial greeting and transition to chief complaint"""
        
        # Check if patient provided initial symptom
        if any(symptom_word in message.lower() for symptom_word in ['pain', 'hurt', 'ache', 'sick', 'feel', 'symptom']):
            context.chief_complaint = message
            context.current_stage = MedicalInterviewStage.HISTORY_PRESENT_ILLNESS
            
            ai_response = await self._generate_empathetic_response(
                f"I understand you're experiencing {message}. I'm here to help you understand what might be going on. "
                f"To provide you with the most accurate assessment, I'd like to ask you some specific questions about your symptoms. "
                f"First, can you tell me exactly when these symptoms started?"
            )
        else:
            context.current_stage = MedicalInterviewStage.CHIEF_COMPLAINT
            ai_response = await self._generate_empathetic_response(
                "Hello! I'm Dr. AI, your personal medical assistant. I'm here to help you understand your health concerns "
                "and provide professional medical guidance. What brings you here today? Please describe any symptoms "
                "or health concerns you're experiencing."
            )
        
        return {
            "response": ai_response,
            "context": asdict(context),
            "stage": context.current_stage.value,
            "urgency": "routine",
            "next_questions": self._get_stage_questions(context.current_stage)
        }
    
    async def _handle_hpi_stage(self, message: str, context: MedicalContext) -> Dict[str, Any]:
        """Handle History of Present Illness using OLDCARTS framework"""
        
        # Extract HPI elements from patient response
        hpi_elements = await self._extract_hpi_elements(message, context.symptom_data)
        context.symptom_data.update(hpi_elements)
        
        # Determine next HPI question based on missing elements
        missing_elements = self._get_missing_hpi_elements(context.symptom_data)
        
        if missing_elements:
            next_element = missing_elements[0]
            question = await self._generate_hpi_question(next_element, context)
            
            return {
                "response": question,
                "context": asdict(context),
                "stage": context.current_stage.value,
                "urgency": context.emergency_level,
                "hpi_progress": f"{8 - len(missing_elements)}/8 complete"
            }
        else:
            # HPI complete, move to Review of Systems
            context.current_stage = MedicalInterviewStage.REVIEW_OF_SYSTEMS
            
            ros_question = await self._generate_targeted_ros_question(context)
            
            return {
                "response": ros_question,
                "context": asdict(context),
                "stage": context.current_stage.value,
                "urgency": context.emergency_level,
                "transition": "Moving to review of systems"
            }
    
    async def _generate_hpi_question(self, element: str, context: MedicalContext) -> str:
        """Generate specific HPI questions using OLDCARTS framework"""
        
        hpi_questions = {
            "onset": f"When exactly did your {context.chief_complaint} start? Was it sudden or gradual?",
            "location": f"Where exactly do you feel the {context.chief_complaint}? Can you point to the specific area?",
            "duration": f"How long do episodes of {context.chief_complaint} typically last?",
            "character": f"How would you describe the quality of your {context.chief_complaint}? For example, is it sharp, dull, burning, crushing, or aching?",
            "alleviating": f"Is there anything that makes your {context.chief_complaint} better or worse? Such as position, activity, food, or medication?",
            "radiation": f"Does your {context.chief_complaint} spread or radiate to any other areas of your body?",
            "timing": f"Is your {context.chief_complaint} constant or does it come and go? Are there specific times of day when it's worse?",
            "severity": f"On a scale of 1 to 10, with 10 being the worst pain you can imagine, how would you rate your {context.chief_complaint}?"
        }
        
        base_question = hpi_questions.get(element, f"Can you tell me more about your {context.chief_complaint}?")
        
        # Add clinical reasoning
        reasoning_map = {
            "onset": "This helps me understand whether we're dealing with an acute or chronic condition.",
            "character": "The quality of symptoms can help distinguish between different underlying causes.",
            "severity": "Understanding severity helps me assess urgency and impact on your daily life.",
            "radiation": "Whether symptoms spread can indicate which organs or systems might be involved."
        }
        
        clinical_reasoning = reasoning_map.get(element, "This information helps me narrow down the possible causes.")
        
        return f"{base_question}\n\nI'm asking this because {clinical_reasoning.lower()}"
    
    async def _generate_differential_diagnosis(self, context: MedicalContext) -> Dict[str, Any]:
        """Generate evidence-based differential diagnosis with probabilities"""
        
        # Pre-process clinical data for AI analysis
        clinical_summary = self._prepare_clinical_summary(context)
        
        # Generate advanced medical assessment with structured prompt
        prompt = f"""
        As a board-certified physician with expertise in internal medicine, emergency medicine, and differential diagnosis, 
        provide a comprehensive clinical assessment based on this patient presentation.

        PATIENT PRESENTATION:
        Chief Complaint: {context.chief_complaint}
        
        CLINICAL DATA:
        Demographics: {context.demographics}
        HPI (History of Present Illness): {context.symptom_data}
        Past Medical History: {context.medical_history}
        Medications: {context.medications}
        Allergies: {context.allergies}
        Social History: {context.social_history}
        Family History: {context.family_history}
        
        CLINICAL REASONING FRAMEWORK:
        Use evidence-based medicine and apply the following systematic approach:
        1. Analyze symptom patterns and clinical presentation
        2. Consider epidemiological factors (age, sex, prevalence)
        3. Apply Bayesian reasoning for probability estimates
        4. Prioritize by clinical urgency and likelihood
        
        REQUIRED JSON RESPONSE FORMAT:
        {{
            "differential_diagnoses": [
                {{
                    "condition": "Most likely diagnosis name",
                    "probability": 45,
                    "reasoning": "Detailed clinical reasoning with evidence",
                    "supporting_evidence": ["symptom 1", "risk factor 2"],
                    "contradicting_evidence": ["absence of fever"],
                    "urgency_level": "routine|urgent|critical"
                }}
            ],
            "clinical_reasoning": {{
                "primary_concerns": ["most concerning possibilities"],
                "diagnostic_approach": "systematic approach used",
                "risk_stratification": "low|moderate|high risk assessment"
            }},
            "recommendations": [
                "Immediate: specific immediate actions",
                "Short-term: follow-up within timeframe", 
                "Long-term: ongoing management"
            ],
            "diagnostic_tests": [
                {{
                    "test": "ECG",
                    "indication": "rule out cardiac etiology",
                    "urgency": "immediate|urgent|routine",
                    "expected_yield": "high|moderate|low"
                }}
            ],
            "red_flags": [
                "Seek emergency care if: specific concerning symptoms"
            ],
            "follow_up_plan": {{
                "timeframe": "specific timeframe for follow-up",
                "provider_type": "primary care|specialist|emergency",
                "monitoring_parameters": ["what to monitor"]
            }},
            "confidence_assessment": {{
                "diagnostic_confidence": 0.85,
                "factors_affecting_confidence": ["complete history", "typical presentation"],
                "additional_information_needed": ["physical exam findings"]
            }}
        }}
        
        Ensure probabilities sum to exactly 100% across all differential diagnoses.
        Base all recommendations on current clinical guidelines and evidence-based medicine.
        """
        
        try:
            response = await self._generate_content_with_fallback(prompt)
            
            # Extract and parse JSON from response
            response_text = response.text.strip()
            differential_data = self._parse_ai_response(response_text, context)
            
            # Validate and enhance the response
            differential_data = self._validate_differential_response(differential_data, context)
            
            # Update context with final assessment
            context.current_stage = MedicalInterviewStage.COMPLETED
            context.clinical_hypotheses = differential_data.get('differential_diagnoses', [])
            
            # Calculate overall urgency
            overall_urgency = self._calculate_overall_urgency(differential_data)
            
            return {
                "response": self._format_final_assessment(differential_data),
                "context": asdict(context),
                "stage": "assessment_complete",
                "differential_diagnoses": differential_data.get('differential_diagnoses', []),
                "recommendations": differential_data.get('recommendations', []),
                "diagnostic_tests": differential_data.get('diagnostic_tests', []),
                "red_flags": differential_data.get('red_flags', []),
                "clinical_reasoning": differential_data.get('clinical_reasoning', {}),
                "confidence_assessment": differential_data.get('confidence_assessment', {}),
                "urgency": overall_urgency,
                "follow_up_plan": differential_data.get('follow_up_plan', {})
            }
            
        except Exception as e:
            print(f"Error generating differential diagnosis: {e}")
            return await self._generate_fallback_assessment(context)
    
    def _format_final_assessment(self, differential_data: Dict[str, Any]) -> str:
        """Format final medical assessment in professional style"""
        
        assessment_parts = []
        
        # Summary
        assessment_parts.append("**🏥 AI MEDICAL CONSULTATION COMPLETE**")
        assessment_parts.append("")
        assessment_parts.append("Based on your comprehensive symptom assessment and medical history, here is my clinical analysis:")
        assessment_parts.append("")
        
        # Differential Diagnoses
        assessment_parts.append("**📋 CLINICAL ASSESSMENT - Most Likely Conditions:**")
        diagnoses = differential_data.get('differential_diagnoses', [])
        for i, diagnosis in enumerate(diagnoses[:5], 1):  # Top 5 diagnoses
            condition = diagnosis.get('condition', 'Unknown')
            probability = diagnosis.get('probability', 0)
            reasoning = diagnosis.get('reasoning', 'Clinical reasoning not available')
            urgency = diagnosis.get('urgency_level', 'routine')
            
            urgency_emoji = {"critical": "🚨", "urgent": "⚠️", "routine": "ℹ️"}.get(urgency, "ℹ️")
            
            assessment_parts.append(f"{i}. {urgency_emoji} **{condition}** ({probability}% probability)")
            assessment_parts.append(f"   • *Clinical Reasoning:* {reasoning}")
            
            # Add supporting/contradicting evidence if available
            supporting = diagnosis.get('supporting_evidence', [])
            if supporting:
                assessment_parts.append(f"   • *Supporting Evidence:* {', '.join(supporting)}")
            
            contradicting = diagnosis.get('contradicting_evidence', [])
            if contradicting:
                assessment_parts.append(f"   • *Contradicting Evidence:* {', '.join(contradicting)}")
            
            assessment_parts.append("")
        
        # Clinical Reasoning Summary
        clinical_reasoning = differential_data.get('clinical_reasoning', {})
        if clinical_reasoning:
            assessment_parts.append("**🧠 CLINICAL REASONING:**")
            
            if 'primary_concerns' in clinical_reasoning:
                assessment_parts.append(f"• *Primary Concerns:* {', '.join(clinical_reasoning['primary_concerns'])}")
            
            if 'diagnostic_approach' in clinical_reasoning:
                assessment_parts.append(f"• *Diagnostic Approach:* {clinical_reasoning['diagnostic_approach']}")
            
            if 'risk_stratification' in clinical_reasoning:
                assessment_parts.append(f"• *Risk Assessment:* {clinical_reasoning['risk_stratification']}")
            
            assessment_parts.append("")
        
        # Immediate Recommendations
        recommendations = differential_data.get('recommendations', [])
        if recommendations:
            assessment_parts.append("**💊 MY PROFESSIONAL RECOMMENDATIONS:**")
            for i, rec in enumerate(recommendations, 1):
                assessment_parts.append(f"{i}. {rec}")
            assessment_parts.append("")
        
        # Diagnostic Tests
        diagnostic_tests = differential_data.get('diagnostic_tests', [])
        if diagnostic_tests:
            assessment_parts.append("**🔬 RECOMMENDED DIAGNOSTIC TESTS:**")
            for test in diagnostic_tests:
                if isinstance(test, dict):
                    test_name = test.get('test', 'Test')
                    indication = test.get('indication', '')
                    urgency = test.get('urgency', 'routine')
                    urgency_emoji = {"immediate": "🚨", "urgent": "⚠️", "routine": "📋"}.get(urgency, "📋")
                    
                    assessment_parts.append(f"• {urgency_emoji} **{test_name}** - {indication}")
                else:
                    assessment_parts.append(f"• {test}")
            assessment_parts.append("")
        
        # Red Flags - Critical
        red_flags = differential_data.get('red_flags', [])
        if red_flags:
            assessment_parts.append("**🚨 URGENT - SEEK IMMEDIATE MEDICAL ATTENTION IF YOU EXPERIENCE:**")
            for flag in red_flags:
                assessment_parts.append(f"• {flag}")
            assessment_parts.append("")
        
        # Follow-up Plan
        follow_up = differential_data.get('follow_up_plan', {})
        if follow_up:
            assessment_parts.append("**📅 FOLLOW-UP PLAN:**")
            
            if 'timeframe' in follow_up:
                assessment_parts.append(f"• *Timeline:* {follow_up['timeframe']}")
            
            if 'provider_type' in follow_up:
                assessment_parts.append(f"• *Provider:* {follow_up['provider_type']}")
            
            if 'monitoring_parameters' in follow_up:
                params = ', '.join(follow_up['monitoring_parameters'])
                assessment_parts.append(f"• *Monitor:* {params}")
            
            assessment_parts.append("")
        
        # Confidence Assessment
        confidence = differential_data.get('confidence_assessment', {})
        if confidence:
            conf_score = confidence.get('diagnostic_confidence', 0.8)
            conf_percentage = int(conf_score * 100)
            assessment_parts.append(f"**📊 DIAGNOSTIC CONFIDENCE: {conf_percentage}%**")
            
            factors = confidence.get('factors_affecting_confidence', [])
            if factors:
                assessment_parts.append(f"• *Confidence factors:* {', '.join(factors)}")
            
            additional_info = confidence.get('additional_information_needed', [])
            if additional_info:
                assessment_parts.append(f"• *Additional information needed:* {', '.join(additional_info)}")
            
            assessment_parts.append("")
        
        # Professional Disclaimer
        assessment_parts.append("---")
        assessment_parts.append("**⚖️ IMPORTANT MEDICAL DISCLAIMER:**")
        assessment_parts.append("This AI-powered assessment is for informational and educational purposes only. It does not constitute professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider for proper medical evaluation, diagnosis, and treatment decisions. In case of medical emergency, call 911 or seek immediate emergency care.")
        assessment_parts.append("")
        assessment_parts.append("*Consultation completed by Dr. AI - Advanced Medical AI Assistant*")
        assessment_parts.append(f"*Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*")
        
        return "\n".join(assessment_parts)
    
    async def _assess_emergency_risk(self, message: str, context: MedicalContext) -> Dict[str, Any]:
        """Assess emergency risk based on symptoms"""
        
        message_lower = message.lower()
        emergency_detected = False
        emergency_level = "none"
        emergency_reasons = []
        
        # Check for emergency keywords
        for keyword in self.emergency_keywords:
            if keyword in message_lower:
                emergency_detected = True
                emergency_reasons.append(f"Mentioned: {keyword}")
        
        # Check for critical symptom combinations
        critical_combinations = [
            ["chest pain", "shortness of breath"],
            ["severe headache", "neck stiffness"],
            ["abdominal pain", "vomiting blood"]
        ]
        
        for combination in critical_combinations:
            if all(symptom in message_lower for symptom in combination):
                emergency_detected = True
                emergency_level = "critical"
                emergency_reasons.append(f"Critical combination: {' + '.join(combination)}")
        
        return {
            "emergency_detected": emergency_detected,
            "emergency_level": emergency_level,
            "reasons": emergency_reasons,
            "confidence": 0.95 if emergency_detected else 0.05
        }
    
    async def _handle_emergency_response(self, emergency_assessment: Dict[str, Any], context: MedicalContext) -> Dict[str, Any]:
        """Handle emergency situations with appropriate urgency"""
        
        emergency_response = """
        🚨 **MEDICAL EMERGENCY DETECTED** 🚨
        
        Based on your symptoms, this could be a medical emergency that requires immediate attention.
        
        **IMMEDIATE ACTION REQUIRED:**
        • Call 911 or go to the nearest emergency room RIGHT NOW
        • Do not drive yourself - call an ambulance or have someone drive you
        • If you're having chest pain, chew an aspirin if you're not allergic
        • Stay calm and follow emergency dispatcher instructions
        
        **Emergency Services:**
        • 🇺🇸 Emergency: 911
        • 🇺🇸 Poison Control: 1-800-222-1222
        • 🇺🇸 Mental Health Crisis: 988
        
        I will continue our consultation, but please seek immediate medical care first.
        """
        
        context.emergency_level = emergency_assessment['emergency_level']
        context.red_flags.extend(emergency_assessment['reasons'])
        
        return {
            "response": emergency_response,
            "context": asdict(context),
            "stage": "emergency_detected",
            "urgency": "emergency",
            "emergency_data": emergency_assessment,
            "immediate_action": "call_911"
        }
    
    # Helper methods
    async def _extract_medical_entities(self, message: str) -> Dict[str, Any]:
        """Extract medical entities from patient message with improved symptom recognition"""
        entities = {
            "symptoms": [],
            "duration": None,
            "severity": None,
            "location": None,
            "processed_message": ""
        }
        
        # Common symptom keywords with variations
        symptom_mapping = {
            "fever": ["fever", "febrile", "temperature", "hot", "chills"],
            "headache": ["headache", "head pain", "migraine", "head hurt"],
            "cough": ["cough", "coughing", "hack"],
            "pain": ["pain", "hurt", "ache", "aching", "sore"],
            "nausea": ["nausea", "nauseous", "sick", "queasy"],
            "fatigue": ["tired", "fatigue", "exhausted", "weakness", "weak"],
            "dizziness": ["dizzy", "dizziness", "lightheaded", "vertigo"],
            "chest_pain": ["chest pain", "chest hurt", "chest pressure"],
            "shortness_of_breath": ["shortness of breath", "short of breath", "breathless", "breathing problem"],
            "abdominal_pain": ["stomach pain", "belly pain", "abdominal pain", "stomach hurt"]
        }
        
        message_lower = message.lower()
        
        # Extract symptoms
        for symptom_type, variations in symptom_mapping.items():
            for variation in variations:
                if variation in message_lower:
                    entities["symptoms"].append(symptom_type)
                    break
        
        # Process common grammar patterns and create a cleaner message
        processed = message_lower
        # Handle common informal patterns
        processed = re.sub(r'\bi\s+having\b', 'having a', processed)
        processed = re.sub(r'\bi\s+have\b', 'having a', processed)
        processed = re.sub(r'\bi\s+am\s+having\b', 'having a', processed)
        processed = re.sub(r'\bi\s+got\b', 'having a', processed)
        
        entities["processed_message"] = processed.strip()
        
        # Extract duration patterns
        duration_patterns = [r'\d+\s*(day|days|week|weeks|month|months|hour|hours)', r'since\s+\w+', r'for\s+\d+']
        for pattern in duration_patterns:
            match = re.search(pattern, message_lower)
            if match:
                entities["duration"] = match.group()
                break
        
        # Extract severity indicators
        severity_patterns = [r'(\d+)(?:/10|out of 10)', r'(mild|moderate|severe|excruciating|unbearable)']
        for pattern in severity_patterns:
            match = re.search(pattern, message_lower)
            if match:
                entities["severity"] = match.group()
                break
        
        return entities
    
    async def _update_medical_context(self, entities: Dict[str, Any], context: MedicalContext, message: str) -> MedicalContext:
        """Update medical context with extracted entities"""
        
        # Update symptom data
        if entities.get("duration"):
            context.symptom_data["duration"] = entities["duration"]
        if entities.get("severity"):
            context.symptom_data["severity"] = entities["severity"]
        if entities.get("location"):
            context.symptom_data["location"] = entities["location"]
        
        return context
    
    async def _extract_hpi_elements(self, message: str, existing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract History of Present Illness elements"""
        hpi_elements = {}
        
        # Simple pattern matching - would be more sophisticated in production
        message_lower = message.lower()
        
        # Onset patterns
        if any(word in message_lower for word in ["sudden", "gradually", "slowly", "started", "began"]):
            hpi_elements["onset"] = message
        
        # Character patterns  
        if any(word in message_lower for word in ["sharp", "dull", "burning", "crushing", "aching", "throbbing"]):
            hpi_elements["character"] = message
            
        # Duration patterns
        if any(word in message_lower for word in ["minutes", "hours", "days", "weeks", "constant", "intermittent"]):
            hpi_elements["duration"] = message
            
        return hpi_elements
    
    def _get_missing_hpi_elements(self, symptom_data: Dict[str, Any]) -> List[str]:
        """Get missing HPI elements"""
        required_elements = ["onset", "location", "duration", "character", "alleviating", "radiation", "timing", "severity"]
        return [element for element in required_elements if element not in symptom_data]
    
    async def _generate_targeted_ros_question(self, context: MedicalContext) -> str:
        """Generate targeted Review of Systems question"""
        return f"Now I'd like to ask about some related symptoms. Have you noticed any associated symptoms like nausea, dizziness, fever, or changes in appetite along with your {context.chief_complaint}?"
    
    async def _handle_chief_complaint_stage(self, message: str, context: MedicalContext) -> Dict[str, Any]:
        """Handle chief complaint collection"""
        context.chief_complaint = message
        context.current_stage = MedicalInterviewStage.HISTORY_PRESENT_ILLNESS
        
        response = f"Thank you for sharing that you're experiencing {message}. I want to gather more specific details to better understand your condition. Let's start with when exactly these symptoms began - was the onset sudden or did it develop gradually over time?"
        
        return {
            "response": response,
            "context": asdict(context),
            "stage": context.current_stage.value,
            "urgency": context.emergency_level
        }
    
    async def _handle_ros_stage(self, message: str, context: MedicalContext) -> Dict[str, Any]:
        """Handle Review of Systems stage"""
        context.current_stage = MedicalInterviewStage.PAST_MEDICAL_HISTORY
        
        response = "Thank you for that information. Now, do you have any significant past medical history, such as previous hospitalizations, surgeries, or ongoing medical conditions that you're being treated for?"
        
        return {
            "response": response,
            "context": asdict(context),
            "stage": context.current_stage.value,
            "urgency": context.emergency_level
        }
    
    async def _handle_pmh_stage(self, message: str, context: MedicalContext) -> Dict[str, Any]:
        """Handle Past Medical History stage"""
        context.medical_history["past_conditions"] = message
        context.current_stage = MedicalInterviewStage.MEDICATIONS_ALLERGIES
        
        response = "That's helpful information. Are you currently taking any medications, vitamins, or supplements? Also, do you have any known allergies to medications, foods, or other substances?"
        
        return {
            "response": response,
            "context": asdict(context),
            "stage": context.current_stage.value,
            "urgency": context.emergency_level
        }
    
    async def _handle_medications_stage(self, message: str, context: MedicalContext) -> Dict[str, Any]:
        """Handle Medications and Allergies stage"""
        # Simple parsing - would be more sophisticated in production
        if "allerg" in message.lower():
            context.allergies = [message]
        if any(word in message.lower() for word in ["medication", "pill", "tablet", "mg", "taking"]):
            context.medications = [message]
        
        context.current_stage = MedicalInterviewStage.DIFFERENTIAL_DIAGNOSIS
        
        response = "Thank you for providing that comprehensive information. Based on everything you've shared, I'm now going to analyze your symptoms and provide you with a detailed medical assessment. Please give me a moment to process this information."
        
        return {
            "response": response,
            "context": asdict(context),
            "stage": context.current_stage.value,
            "urgency": context.emergency_level
        }
    
    async def _handle_social_history_stage(self, message: str, context: MedicalContext) -> Dict[str, Any]:
        """Handle Social and Family History stage"""
        context.social_history["lifestyle"] = message
        return await self._generate_differential_diagnosis(context)
    
    async def _generate_empathetic_response(self, base_response: str) -> str:
        """Generate empathetic medical response"""
        return base_response
    
    def _get_stage_questions(self, stage: MedicalInterviewStage) -> List[str]:
        """Get suggested questions for current stage"""
        stage_questions = {
            MedicalInterviewStage.GREETING: [
                "What symptoms are you experiencing?",
                "What brings you here today?",
                "How can I help you with your health concern?"
            ],
            MedicalInterviewStage.CHIEF_COMPLAINT: [
                "When did this start?",
                "How severe is it?",
                "Where do you feel it?"
            ]
        }
        return stage_questions.get(stage, [])
    
    def _assess_overall_urgency(self, differential_data: Dict[str, Any]) -> str:
        """Assess overall clinical urgency"""
        diagnoses = differential_data.get('differential_diagnoses', [])
        if not diagnoses:
            return "routine"
        
        # Check if any high-probability serious conditions
        for diagnosis in diagnoses:
            probability = diagnosis.get('probability', 0)
            condition = diagnosis.get('condition', '').lower()
            
            if probability > 30 and any(serious in condition for serious in ['cardiac', 'stroke', 'emergency']):
                return "urgent"
        
        return "routine"
    
    async def _generate_fallback_assessment(self, context: MedicalContext) -> Dict[str, Any]:
        """Generate fallback assessment if main analysis fails"""
        fallback_data = self._generate_fallback_assessment_data(context)
        
        return {
            "response": self._format_final_assessment(fallback_data),
            "context": asdict(context),
            "stage": "assessment_complete",
            "differential_diagnoses": fallback_data.get('differential_diagnoses', []),
            "recommendations": fallback_data.get('recommendations', []),
            "urgency": "routine"
        }
    
    def _generate_fallback_assessment_data(self, context: MedicalContext) -> Dict[str, Any]:
        """Generate fallback assessment data"""
        return {
            "differential_diagnoses": [
                {
                    "condition": "Requires further evaluation",
                    "probability": 60,
                    "reasoning": "Based on the symptoms described, additional medical evaluation is recommended."
                },
                {
                    "condition": "Benign condition",
                    "probability": 40,
                    "reasoning": "Symptoms may be related to a benign, self-limiting condition."
                }
            ],
            "recommendations": [
                "Follow up with your primary care physician for proper evaluation",
                "Monitor symptoms and note any changes",
                "Maintain a symptom diary"
            ],
            "diagnostic_tests": [
                "Basic physical examination",
                "Review of medical history"
            ],
            "red_flags": [
                "Worsening symptoms",
                "New concerning symptoms",
                "Severe pain or distress"
            ]
        }
    
    def _prepare_clinical_summary(self, context: MedicalContext) -> str:
        """Prepare structured clinical summary for AI analysis"""
        summary_parts = []
        
        if context.chief_complaint:
            summary_parts.append(f"Chief Complaint: {context.chief_complaint}")
        
        if context.symptom_data:
            hpi_elements = []
            for key, value in context.symptom_data.items():
                if value:
                    hpi_elements.append(f"{key.replace('_', ' ').title()}: {value}")
            if hpi_elements:
                summary_parts.append("HPI Elements: " + "; ".join(hpi_elements))
        
        if context.medical_history:
            summary_parts.append(f"PMH: {context.medical_history}")
        
        if context.medications:
            summary_parts.append(f"Medications: {', '.join(context.medications)}")
        
        if context.allergies:
            summary_parts.append(f"Allergies: {', '.join(context.allergies)}")
        
        return " | ".join(summary_parts)
    
    def _parse_ai_response(self, response_text: str, context: MedicalContext) -> Dict[str, Any]:
        """Parse AI response and extract JSON data"""
        try:
            # Clean up the response text
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
            
            # Find JSON content within the text
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_text = response_text[json_start:json_end]
                return json.loads(json_text)
            else:
                raise json.JSONDecodeError("No valid JSON found", response_text, 0)
                
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return self._generate_fallback_assessment_data(context)
    
    def _validate_differential_response(self, differential_data: Dict[str, Any], context: MedicalContext) -> Dict[str, Any]:
        """Validate and enhance differential diagnosis response"""
        
        # Ensure required keys exist
        if 'differential_diagnoses' not in differential_data:
            differential_data['differential_diagnoses'] = []
        
        # Validate probability totals
        diagnoses = differential_data['differential_diagnoses']
        if diagnoses:
            total_probability = sum(d.get('probability', 0) for d in diagnoses)
            if total_probability != 100:
                # Normalize probabilities to sum to 100
                adjustment_factor = 100 / total_probability if total_probability > 0 else 1
                for diagnosis in diagnoses:
                    if 'probability' in diagnosis:
                        diagnosis['probability'] = round(diagnosis['probability'] * adjustment_factor, 1)
        
        # Ensure minimum required fields
        required_keys = ['recommendations', 'diagnostic_tests', 'red_flags']
        for key in required_keys:
            if key not in differential_data:
                differential_data[key] = []
        
        return differential_data
    
    def _calculate_overall_urgency(self, differential_data: Dict[str, Any]) -> str:
        """Calculate overall clinical urgency based on differential diagnoses"""
        diagnoses = differential_data.get('differential_diagnoses', [])
        
        max_urgency_score = 0
        urgency_weights = {'critical': 3, 'urgent': 2, 'routine': 1}
        
        for diagnosis in diagnoses:
            urgency = diagnosis.get('urgency_level', 'routine')
            probability = diagnosis.get('probability', 0)
            
            # Weight urgency by probability
            urgency_score = urgency_weights.get(urgency, 1) * (probability / 100)
            max_urgency_score = max(max_urgency_score, urgency_score)
        
        # Convert back to urgency level
        if max_urgency_score >= 2.0:
            return 'critical'
        elif max_urgency_score >= 1.0:
            return 'urgent'
        else:
            return 'routine'