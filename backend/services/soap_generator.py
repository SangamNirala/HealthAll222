from datetime import datetime
from typing import Dict, Any, List
from dataclasses import asdict
import json

class ProfessionalSOAPGenerator:
    """Generate medical-grade SOAP notes matching physician documentation standards"""
    
    def __init__(self):
        self.medical_terminology = self._load_medical_terminology()
        self.icd_codes = self._load_icd_codes()
        
    def _load_medical_terminology(self) -> Dict[str, Any]:
        """Load medical terminology mappings"""
        return {
            "symptoms": {
                "chest pain": "chest discomfort",
                "headache": "cephalgia", 
                "stomach pain": "abdominal pain",
                "shortness of breath": "dyspnea",
                "dizziness": "vertigo",
                "joint pain": "arthralgia",
                "muscle pain": "myalgia"
            },
            "severity_terms": {
                "mild": "1-3/10",
                "moderate": "4-6/10", 
                "severe": "7-10/10"
            }
        }
    
    def _load_icd_codes(self) -> Dict[str, str]:
        """Load ICD-10 code mappings for common conditions"""
        return {
            "tension headache": "G44.209",
            "migraine": "G43.909",
            "chest pain": "R06.02",
            "abdominal pain": "R10.9",
            "shortness of breath": "R06.00",
            "hypertension": "I10",
            "diabetes": "E11.9",
            "anxiety": "F41.9",
            "depression": "F32.9",
            "gerd": "K21.9",
            "gastroesophageal reflux": "K21.9",
            "upper respiratory infection": "J06.9",
            "viral syndrome": "B34.9",
            "muscle strain": "M79.1",
            "acute bronchitis": "J20.9"
        }
        
    async def generate_comprehensive_soap(self, consultation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete SOAP note from consultation data"""
        
        soap_note = {
            "header": self._create_header(consultation_data),
            "subjective": await self._generate_subjective(consultation_data),
            "objective": self._generate_objective(consultation_data),
            "assessment": await self._generate_assessment(consultation_data),
            "plan": await self._generate_plan(consultation_data),
            "generated_at": datetime.now().isoformat(),
            "consultation_id": consultation_data.get('consultation_id'),
            "version": "1.0"
        }
        
        return soap_note
    
    def _create_header(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Create professional medical document header"""
        
        demographics = data.get('demographics', {})
        age = demographics.get('age', 'Unknown')
        sex = demographics.get('sex', 'Unknown')
        
        return {
            "patient_demographics": f"{age}-year-old {sex}",
            "date_of_service": datetime.now().strftime("%B %d, %Y"),
            "time_of_service": datetime.now().strftime("%I:%M %p"),
            "consultation_type": "AI-Assisted Medical Consultation",
            "provider": "Dr. AI (Advanced Medical AI Assistant)",
            "consultation_method": "Telemedicine - AI Chat Interface",
            "documentation_time": datetime.now().strftime("%B %d, %Y at %I:%M %p")
        }
    
    async def _generate_subjective(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive subjective section"""
        
        return {
            "chief_complaint": self._format_chief_complaint(data),
            "history_present_illness": self._generate_hpi_narrative(data),
            "review_of_systems": self._generate_ros_narrative(data),
            "past_medical_history": self._format_pmh(data),
            "medications": self._format_medications(data),
            "allergies": self._format_allergies(data),
            "social_history": self._format_social_history(data),
            "family_history": self._format_family_history(data)
        }
    
    def _format_chief_complaint(self, data: Dict[str, Any]) -> str:
        """Format the chief complaint professionally"""
        chief_complaint = data.get('chief_complaint', 'General health concerns')
        
        # Clean and format the chief complaint
        if chief_complaint:
            # Ensure proper formatting
            chief_complaint = chief_complaint.strip()
            if not chief_complaint.endswith('.'):
                chief_complaint += '.'
            return f'"{chief_complaint}"'
        
        return '"Patient reports general health concerns."'
    
    def _generate_hpi_narrative(self, data: Dict[str, Any]) -> str:
        """Generate professional HPI narrative using medical documentation standards"""
        
        symptom_data = data.get('symptom_data', {})
        chief_complaint = data.get('chief_complaint', 'symptoms')
        
        hpi_parts = []
        
        # Opening statement
        hpi_parts.append(f"Patient reports {chief_complaint}")
        
        # OLDCARTS elements
        if 'onset' in symptom_data:
            hpi_parts.append(f"with onset {symptom_data['onset']}")
        
        if 'duration' in symptom_data:
            hpi_parts.append(f"Duration: {symptom_data['duration']}")
        
        if 'character' in symptom_data:
            hpi_parts.append(f"Character described as {symptom_data['character']}")
        
        if 'location' in symptom_data:
            hpi_parts.append(f"Located in {symptom_data['location']}")
        
        if 'radiation' in symptom_data:
            hpi_parts.append(f"Radiation: {symptom_data['radiation']}")
        
        if 'severity' in symptom_data:
            hpi_parts.append(f"Severity rated {symptom_data['severity']}/10")
        
        if 'alleviating' in symptom_data:
            hpi_parts.append(f"Alleviating factors: {symptom_data['alleviating']}")
        
        if 'aggravating' in symptom_data:
            hpi_parts.append(f"Aggravating factors: {symptom_data['aggravating']}")
        
        if 'timing' in symptom_data:
            hpi_parts.append(f"Timing pattern: {symptom_data['timing']}")
        
        # Associated symptoms
        if 'associated_symptoms' in symptom_data:
            associated = symptom_data['associated_symptoms']
            if associated:
                hpi_parts.append(f"Associated symptoms include: {', '.join(associated)}")
        
        # Context and impact
        if 'impact_daily_activities' in symptom_data:
            hpi_parts.append(f"Impact on daily activities: {symptom_data['impact_daily_activities']}")
        
        if 'previous_episodes' in symptom_data:
            hpi_parts.append(f"Previous similar episodes: {symptom_data['previous_episodes']}")
        
        if 'treatments_tried' in symptom_data:
            hpi_parts.append(f"Treatments attempted: {symptom_data['treatments_tried']}")
        
        # If no specific HPI data, provide a general narrative
        if len(hpi_parts) == 1:  # Only has the opening statement
            hpi_parts.append("Patient provided limited additional details about symptom characteristics")
        
        return ". ".join(hpi_parts) + "."
    
    def _generate_ros_narrative(self, data: Dict[str, Any]) -> str:
        """Generate review of systems narrative"""
        ros_data = data.get('review_of_systems', {})
        
        if not ros_data:
            return "Review of systems not fully elicited during AI consultation. Patient advised to discuss comprehensive review with healthcare provider."
        
        ros_parts = []
        for system, findings in ros_data.items():
            if findings:
                ros_parts.append(f"{system.title()}: {findings}")
        
        if ros_parts:
            return ". ".join(ros_parts) + "."
        else:
            return "No additional systemic symptoms reported."
    
    def _format_pmh(self, data: Dict[str, Any]) -> str:
        """Format past medical history"""
        pmh = data.get('past_medical_history', {})
        
        if not pmh:
            return "Past medical history not obtained during AI consultation."
        
        pmh_items = []
        
        if 'conditions' in pmh and pmh['conditions']:
            conditions = ', '.join(pmh['conditions'])
            pmh_items.append(f"Medical conditions: {conditions}")
        
        if 'surgeries' in pmh and pmh['surgeries']:
            surgeries = ', '.join(pmh['surgeries'])
            pmh_items.append(f"Surgical history: {surgeries}")
        
        if 'hospitalizations' in pmh and pmh['hospitalizations']:
            hospitalizations = ', '.join(pmh['hospitalizations'])
            pmh_items.append(f"Hospitalizations: {hospitalizations}")
        
        if pmh_items:
            return ". ".join(pmh_items) + "."
        else:
            return "No significant past medical history reported."
    
    def _format_medications(self, data: Dict[str, Any]) -> str:
        """Format current medications"""
        medications = data.get('medications', [])
        
        if not medications:
            return "Current medications not fully reviewed during AI consultation."
        
        if isinstance(medications, list) and medications:
            med_list = ', '.join(medications)
            return f"Current medications: {med_list}."
        
        return "No current medications reported."
    
    def _format_allergies(self, data: Dict[str, Any]) -> str:
        """Format allergies"""
        allergies = data.get('allergies', [])
        
        if not allergies:
            return "Allergies not assessed during AI consultation."
        
        if isinstance(allergies, list) and allergies:
            allergy_list = ', '.join(allergies)
            return f"Known allergies: {allergy_list}."
        
        return "No known drug allergies reported."
    
    def _format_social_history(self, data: Dict[str, Any]) -> str:
        """Format social history"""
        social_history = data.get('social_history', {})
        
        if not social_history:
            return "Social history not obtained during AI consultation."
        
        social_items = []
        
        if 'smoking' in social_history:
            social_items.append(f"Tobacco use: {social_history['smoking']}")
        
        if 'alcohol' in social_history:
            social_items.append(f"Alcohol use: {social_history['alcohol']}")
        
        if 'occupation' in social_history:
            social_items.append(f"Occupation: {social_history['occupation']}")
        
        if social_items:
            return ". ".join(social_items) + "."
        else:
            return "Limited social history obtained."
    
    def _format_family_history(self, data: Dict[str, Any]) -> str:
        """Format family history"""
        family_history = data.get('family_history', {})
        
        if not family_history:
            return "Family history not assessed during AI consultation."
        
        if family_history:
            family_items = []
            for relation, conditions in family_history.items():
                if conditions:
                    family_items.append(f"{relation}: {conditions}")
            
            if family_items:
                return ". ".join(family_items) + "."
        
        return "Family history not significant or not reported."
    
    def _generate_objective(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate objective section (physical exam findings)"""
        
        return {
            "vital_signs": "Not obtained during telemedicine AI consultation",
            "physical_examination": "Limited physical examination via telemedicine consultation. Patient advised for in-person evaluation for complete physical assessment.",
            "diagnostic_results": "No diagnostic tests performed during AI consultation",
            "clinical_observations": self._generate_clinical_observations(data)
        }
    
    def _generate_clinical_observations(self, data: Dict[str, Any]) -> str:
        """Generate clinical observations from AI consultation"""
        observations = []
        
        # Communication and engagement
        observations.append("Patient engaged appropriately during AI consultation")
        
        # Symptom presentation
        if data.get('emergency_level') == 'emergency':
            observations.append("Patient presentation suggests potential emergency condition")
        elif data.get('emergency_level') == 'urgent':
            observations.append("Patient presentation requires timely medical evaluation")
        else:
            observations.append("Patient presentation appears stable for telemedicine evaluation")
        
        # Communication quality
        messages = data.get('messages', [])
        if messages:
            user_messages = [m for m in messages if m.get('type') == 'user']
            if len(user_messages) >= 5:
                observations.append("Patient provided detailed symptom history")
            else:
                observations.append("Limited symptom details provided during consultation")
        
        return ". ".join(observations) + "."
    
    async def _generate_assessment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive assessment section"""
        
        clinical_hypotheses = data.get('clinical_hypotheses', [])
        
        assessment = {
            "clinical_impression": self._generate_clinical_impression(data),
            "differential_diagnosis": self._format_differential_diagnoses(clinical_hypotheses),
            "risk_stratification": self._assess_clinical_risk(data),
            "clinical_reasoning": self._generate_clinical_reasoning(data)
        }
        
        return assessment
    
    def _generate_clinical_impression(self, data: Dict[str, Any]) -> str:
        """Generate primary clinical impression"""
        clinical_hypotheses = data.get('clinical_hypotheses', [])
        chief_complaint = data.get('chief_complaint', 'symptoms')
        
        if clinical_hypotheses:
            primary_diagnosis = clinical_hypotheses[0]
            condition = primary_diagnosis.get('condition', 'Unknown condition')
            probability = primary_diagnosis.get('probability', 0)
            
            if probability >= 70:
                certainty = "likely"
            elif probability >= 50:
                certainty = "probable"
            else:
                certainty = "possible"
            
            return f"Patient presents with {chief_complaint}, {certainty} {condition} based on symptom presentation and clinical analysis."
        else:
            return f"Patient presents with {chief_complaint}. Further evaluation needed for definitive diagnosis."
    
    def _format_differential_diagnoses(self, hypotheses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format differential diagnoses with clinical reasoning"""
        
        formatted_diagnoses = []
        
        for i, hypothesis in enumerate(hypotheses[:5], 1):  # Top 5 diagnoses
            formatted_diagnosis = {
                "rank": i,
                "condition": hypothesis.get('condition', 'Unknown condition'),
                "probability": f"{hypothesis.get('probability', 0)}%",
                "icd_code": self._lookup_icd_code(hypothesis.get('condition', '')),
                "clinical_reasoning": hypothesis.get('reasoning', 'Clinical reasoning not available'),
                "supporting_evidence": hypothesis.get('supporting_evidence', []),
                "contradicting_evidence": hypothesis.get('contradicting_evidence', [])
            }
            formatted_diagnoses.append(formatted_diagnosis)
        
        return formatted_diagnoses
    
    def _lookup_icd_code(self, condition: str) -> str:
        """Look up ICD-10 code for condition"""
        condition_lower = condition.lower()
        
        # Direct match
        if condition_lower in self.icd_codes:
            return self.icd_codes[condition_lower]
        
        # Partial match
        for icd_condition, code in self.icd_codes.items():
            if icd_condition in condition_lower or condition_lower in icd_condition:
                return code
        
        return "To be determined - consult ICD-10 manual"
    
    def _assess_clinical_risk(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Assess clinical risk stratification"""
        emergency_level = data.get('emergency_level', 'none')
        clinical_hypotheses = data.get('clinical_hypotheses', [])
        
        if emergency_level == 'emergency':
            risk_level = "High"
            risk_factors = "Emergency presentation requiring immediate medical attention"
        elif emergency_level == 'urgent':
            risk_level = "Moderate"
            risk_factors = "Urgent presentation requiring timely medical evaluation"
        elif clinical_hypotheses:
            highest_probability = max([h.get('probability', 0) for h in clinical_hypotheses])
            if highest_probability >= 70:
                risk_level = "Low-Moderate"
                risk_factors = "Well-defined clinical presentation with probable diagnosis"
            else:
                risk_level = "Low"
                risk_factors = "Stable presentation with multiple diagnostic considerations"
        else:
            risk_level = "Low"
            risk_factors = "Stable presentation requiring further evaluation"
        
        return {
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "immediate_concerns": self._identify_immediate_concerns(data),
            "monitoring_needs": "Symptom monitoring and follow-up as outlined in plan"
        }
    
    def _identify_immediate_concerns(self, data: Dict[str, Any]) -> str:
        """Identify immediate clinical concerns"""
        emergency_level = data.get('emergency_level', 'none')
        red_flags = data.get('red_flags', [])
        
        if emergency_level == 'emergency':
            return "Emergency presentation - immediate medical attention required"
        elif red_flags:
            return f"Red flag symptoms present: {', '.join(red_flags)}"
        else:
            return "No immediate life-threatening concerns identified"
    
    def _generate_clinical_reasoning(self, data: Dict[str, Any]) -> str:
        """Generate clinical reasoning narrative"""
        clinical_hypotheses = data.get('clinical_hypotheses', [])
        symptom_data = data.get('symptom_data', {})
        
        reasoning_parts = []
        
        if clinical_hypotheses:
            primary_hypothesis = clinical_hypotheses[0]
            reasoning_parts.append(f"Primary consideration of {primary_hypothesis.get('condition', 'unknown condition')} based on {primary_hypothesis.get('reasoning', 'clinical presentation')}")
        
        if symptom_data:
            reasoning_parts.append(f"Symptom pattern suggests {self._analyze_symptom_pattern(symptom_data)}")
        
        emergency_level = data.get('emergency_level', 'none')
        if emergency_level != 'none':
            reasoning_parts.append(f"Clinical presentation classified as {emergency_level} priority based on symptom severity and urgency indicators")
        
        if reasoning_parts:
            return ". ".join(reasoning_parts) + "."
        else:
            return "Clinical reasoning based on AI analysis of symptom presentation and medical knowledge base."
    
    def _analyze_symptom_pattern(self, symptom_data: Dict[str, Any]) -> str:
        """Analyze symptom patterns for clinical reasoning"""
        patterns = []
        
        if 'onset' in symptom_data:
            onset = symptom_data['onset'].lower()
            if 'sudden' in onset:
                patterns.append("acute presentation")
            elif 'gradual' in onset:
                patterns.append("chronic or subacute condition")
        
        if 'severity' in symptom_data:
            try:
                severity = int(symptom_data['severity'])
                if severity >= 7:
                    patterns.append("high symptom severity")
                elif severity >= 4:
                    patterns.append("moderate symptom burden")
            except:
                pass
        
        if patterns:
            return " and ".join(patterns)
        else:
            return "symptom pattern requiring clinical correlation"
    
    async def _generate_plan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive treatment plan"""
        
        plan = {
            "diagnostic_workup": self._recommend_diagnostic_tests(data),
            "therapeutic_interventions": self._generate_treatment_recommendations(data),
            "patient_education": self._generate_patient_education(data),
            "follow_up_plan": self._create_follow_up_plan(data),
            "return_precautions": self._generate_return_precautions(data),
            "monitoring_requirements": self._suggest_monitoring(data),
            "referrals": self._suggest_referrals(data)
        }
        
        return plan
    
    def _recommend_diagnostic_tests(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Recommend evidence-based diagnostic tests"""
        
        chief_complaint = data.get('chief_complaint', '').lower()
        clinical_hypotheses = data.get('clinical_hypotheses', [])
        
        test_recommendations = []
        
        # Basic tests based on chief complaint
        if 'chest pain' in chief_complaint:
            test_recommendations.extend([
                {
                    "test": "12-lead ECG",
                    "indication": "Rule out acute coronary syndrome",
                    "urgency": "immediate"
                },
                {
                    "test": "Chest X-ray",
                    "indication": "Evaluate for pneumothorax, pneumonia",
                    "urgency": "routine"
                },
                {
                    "test": "Cardiac enzymes (Troponin)",
                    "indication": "Assess for myocardial injury",
                    "urgency": "urgent"
                }
            ])
        
        elif 'headache' in chief_complaint:
            test_recommendations.extend([
                {
                    "test": "Neurological examination",
                    "indication": "Assess for focal deficits",
                    "urgency": "immediate"
                },
                {
                    "test": "Blood pressure measurement",
                    "indication": "Rule out hypertensive emergency",
                    "urgency": "immediate"
                }
            ])
        
        elif 'abdominal pain' in chief_complaint:
            test_recommendations.extend([
                {
                    "test": "Complete Blood Count (CBC)",
                    "indication": "Assess for infection, bleeding",
                    "urgency": "routine"
                },
                {
                    "test": "Comprehensive Metabolic Panel",
                    "indication": "Evaluate electrolytes, kidney function",
                    "urgency": "routine"
                },
                {
                    "test": "Abdominal CT scan",
                    "indication": "Evaluate for structural abnormalities",
                    "urgency": "urgent if severe pain"
                }
            ])
        
        # Add hypothesis-specific tests
        for hypothesis in clinical_hypotheses:
            condition = hypothesis.get('condition', '').lower()
            
            if 'diabetes' in condition:
                test_recommendations.append({
                    "test": "Hemoglobin A1c",
                    "indication": "Assess long-term glucose control",
                    "urgency": "routine"
                })
            
            elif 'thyroid' in condition:
                test_recommendations.append({
                    "test": "TSH, Free T4",
                    "indication": "Evaluate thyroid function",
                    "urgency": "routine"
                })
        
        # General screening if no specific tests recommended
        if not test_recommendations:
            test_recommendations.append({
                "test": "Complete metabolic panel and CBC",
                "indication": "General medical screening",
                "urgency": "routine"
            })
        
        return test_recommendations
    
    def _generate_treatment_recommendations(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate evidence-based treatment recommendations"""
        
        treatments = []
        clinical_hypotheses = data.get('clinical_hypotheses', [])
        
        for hypothesis in clinical_hypotheses:
            condition = hypothesis.get('condition', '').lower()
            probability = hypothesis.get('probability', 0)
            
            # Only recommend treatments for high-probability diagnoses
            if probability >= 30:
                
                if 'tension headache' in condition:
                    treatments.append({
                        "treatment": "Acetaminophen 650mg every 6 hours as needed",
                        "indication": f"First-line treatment for {hypothesis['condition']}",
                        "duration": "As needed for symptom relief",
                        "monitoring": "Monitor for overuse"
                    })
                
                elif 'migraine' in condition:
                    treatments.append({
                        "treatment": "Sumatriptan 50mg at onset, may repeat once after 2 hours",
                        "indication": f"Specific treatment for {hypothesis['condition']}",
                        "duration": "As needed for episodes",
                        "monitoring": "Limit to 9 doses per month"
                    })
                
                elif 'gerd' in condition or 'reflux' in condition:
                    treatments.append({
                        "treatment": "Omeprazole 20mg daily before breakfast",
                        "indication": f"Acid suppression for {hypothesis['condition']}",
                        "duration": "4-8 weeks initially",
                        "monitoring": "Reassess after 8 weeks"
                    })
        
        # General supportive care
        treatments.append({
            "treatment": "Adequate hydration (8-10 glasses water daily)",
            "indication": "General supportive care",
            "duration": "Ongoing",
            "monitoring": "Monitor urine color for hydration status"
        })
        
        # Symptomatic care if no specific treatments
        if len(treatments) == 1:  # Only has general care
            treatments.append({
                "treatment": "Symptomatic care as tolerated",
                "indication": "General symptom management pending further evaluation",
                "duration": "Until medical follow-up",
                "monitoring": "Monitor symptom progression"
            })
        
        return treatments
    
    def _generate_patient_education(self, data: Dict[str, Any]) -> List[str]:
        """Generate comprehensive patient education points"""
        
        education_points = []
        chief_complaint = data.get('chief_complaint', '').lower()
        
        # General education
        education_points.extend([
            "This AI consultation provides general medical information and should not replace professional medical advice",
            "Keep a symptom diary to track patterns and triggers",
            "Take medications as prescribed and report any side effects"
        ])
        
        # Condition-specific education
        if 'chest pain' in chief_complaint:
            education_points.extend([
                "Seek immediate medical attention for crushing chest pain, especially with arm pain or shortness of breath",
                "Avoid strenuous activity until cleared by a physician",
                "Consider cardiac risk factor modification (diet, exercise, smoking cessation)"
            ])
        
        elif 'headache' in chief_complaint:
            education_points.extend([
                "Maintain regular sleep schedule and manage stress",
                "Identify and avoid known headache triggers",
                "Seek immediate care for sudden, severe headache or headache with fever"
            ])
        
        elif 'abdominal' in chief_complaint:
            education_points.extend([
                "Monitor for signs of worsening pain or fever",
                "Maintain adequate hydration if tolerated",
                "Avoid solid foods if nausea or vomiting present"
            ])
        
        # General wellness education
        education_points.extend([
            "Follow up with your primary care physician for ongoing care",
            "Maintain a healthy lifestyle with regular exercise and balanced nutrition",
            "Stay up to date with preventive care and screenings"
        ])
        
        return education_points
    
    def _create_follow_up_plan(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Create appropriate follow-up plan"""
        
        clinical_hypotheses = data.get('clinical_hypotheses', [])
        emergency_level = data.get('emergency_level', 'none')
        highest_probability = max([h.get('probability', 0) for h in clinical_hypotheses]) if clinical_hypotheses else 0
        
        if emergency_level == 'emergency':
            urgency = "immediate emergency evaluation"
        elif emergency_level == 'urgent':
            urgency = "within 24 hours"
        elif highest_probability >= 70:
            urgency = "within 1-2 weeks"
        elif highest_probability >= 40:
            urgency = "within 2-4 weeks"
        else:
            urgency = "within 4-6 weeks or as needed"
        
        return {
            "primary_care_physician": f"Follow up {urgency} for ongoing management",
            "specialist_referral": "Consider specialist referral if symptoms persist or worsen",
            "diagnostic_follow_up": "Review test results when available",
            "symptom_monitoring": "Return if symptoms significantly worsen or new symptoms develop"
        }
    
    def _generate_return_precautions(self, data: Dict[str, Any]) -> List[str]:
        """Generate comprehensive return precautions (red flags)"""
        
        chief_complaint = data.get('chief_complaint', '').lower()
        return_precautions = []
        
        # General precautions
        return_precautions.extend([
            "Return immediately if symptoms become severe or life-threatening",
            "Seek emergency care if you develop difficulty breathing",
            "Return if you develop signs of infection (fever, chills)"
        ])
        
        # Condition-specific precautions
        if 'chest' in chief_complaint:
            return_precautions.extend([
                "Call 911 for crushing chest pain, especially with nausea, sweating, or arm pain",
                "Seek immediate care for severe shortness of breath",
                "Return for chest pain that is getting progressively worse"
            ])
        
        elif 'head' in chief_complaint:
            return_precautions.extend([
                "Seek immediate care for sudden, severe headache ('worst headache of your life')",
                "Return immediately for headache with fever and neck stiffness",
                "Seek emergency care for headache with vision changes or weakness"
            ])
        
        elif 'abdominal' in chief_complaint:
            return_precautions.extend([
                "Seek immediate care for severe abdominal pain with vomiting",
                "Return for signs of dehydration (dizziness, dry mouth, decreased urination)",
                "Call for abdominal pain with blood in vomit or stool"
            ])
        
        # General emergency precautions
        return_precautions.extend([
            "Call 911 for any life-threatening emergency",
            "Return for any symptom that causes significant concern or anxiety",
            "Seek immediate care if condition worsens despite treatment"
        ])
        
        return return_precautions

    def _suggest_monitoring(self, data: Dict[str, Any]) -> List[str]:
        """Suggest monitoring requirements"""
        clinical_hypotheses = data.get('clinical_hypotheses', [])
        chief_complaint = data.get('chief_complaint', '').lower()
        
        monitoring = []
        
        # General monitoring
        monitoring.extend([
            "Monitor symptom progression and severity",
            "Track any new or worsening symptoms",
            "Record symptom patterns and triggers"
        ])
        
        # Condition-specific monitoring
        if 'chest pain' in chief_complaint:
            monitoring.extend([
                "Monitor for chest pain recurrence or worsening",
                "Track activity tolerance",
                "Monitor for shortness of breath"
            ])
        elif 'headache' in chief_complaint:
            monitoring.extend([
                "Track headache frequency and severity",
                "Monitor for headache triggers",
                "Record pain relief effectiveness"
            ])
        
        # Treatment-specific monitoring
        for hypothesis in clinical_hypotheses:
            condition = hypothesis.get('condition', '').lower()
            if 'hypertension' in condition:
                monitoring.append("Monitor blood pressure regularly")
            elif 'diabetes' in condition:
                monitoring.append("Monitor blood glucose levels")
        
        return monitoring
    
    def _suggest_referrals(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Suggest appropriate referrals"""
        clinical_hypotheses = data.get('clinical_hypotheses', [])
        chief_complaint = data.get('chief_complaint', '').lower()
        emergency_level = data.get('emergency_level', 'none')
        
        referrals = []
        
        # Emergency referral
        if emergency_level == 'emergency':
            referrals.append({
                "specialty": "Emergency Medicine",
                "urgency": "Immediate",
                "indication": "Emergency presentation requiring immediate evaluation"
            })
        
        # Condition-specific referrals
        if 'chest pain' in chief_complaint:
            referrals.append({
                "specialty": "Cardiology", 
                "urgency": "Routine",
                "indication": "Chest pain evaluation and cardiac risk assessment"
            })
        
        elif 'headache' in chief_complaint and any('migraine' in h.get('condition', '').lower() for h in clinical_hypotheses):
            referrals.append({
                "specialty": "Neurology",
                "urgency": "Routine", 
                "indication": "Headache evaluation and migraine management"
            })
        
        # Primary care referral (always recommended)
        referrals.append({
            "specialty": "Primary Care Physician",
            "urgency": "Routine",
            "indication": "Comprehensive evaluation and ongoing medical management"
        })
        
        return referrals

    def generate_ai_consult_summary(self, data: Dict[str, Any]) -> str:
        """Generate AI Consult Summary matching Doctronic.ai format"""
        
        demographics = data.get('demographics', {})
        age = demographics.get('age', 'Unknown age')
        sex = demographics.get('sex', 'unknown sex')
        
        symptom_data = data.get('symptom_data', {})
        duration = symptom_data.get('duration', 'unknown duration')
        chief_complaint = data.get('chief_complaint', 'symptoms')
        
        clinical_hypotheses = data.get('clinical_hypotheses', [])
        primary_diagnosis = clinical_hypotheses[0] if clinical_hypotheses else {'condition': 'requires further evaluation'}
        
        secondary_conditions = clinical_hypotheses[1:3] if len(clinical_hypotheses) > 1 else []
        secondary_text = f" with {', '.join([h['condition'] for h in secondary_conditions])}" if secondary_conditions else ""
        
        recommended_actions = self._get_recommended_actions(data)
        tests_needed = self._get_tests_needed(data)
        
        summary = f"""AI Consult Summary
{datetime.now().strftime('%b %d, %Y, %I:%M %p')}

You are a {age}-year-old {sex} experiencing {duration} of {chief_complaint}, most likely due to {primary_diagnosis['condition']}{secondary_text} being key considerations.

The recommended plan is to {recommended_actions}, with further evaluation including {tests_needed} if your symptoms persist or worsen."""
        
        return summary
    
    def _get_recommended_actions(self, data: Dict[str, Any]) -> str:
        """Get primary recommended actions"""
        
        clinical_hypotheses = data.get('clinical_hypotheses', [])
        emergency_level = data.get('emergency_level', 'none')
        
        if emergency_level == 'critical' or emergency_level == 'emergency':
            return "seek immediate emergency medical care"
        elif emergency_level == 'high' or emergency_level == 'urgent':
            return "see a healthcare provider within 24 hours"
        elif clinical_hypotheses:
            primary_condition = clinical_hypotheses[0].get('condition', '').lower()
            
            if 'infection' in primary_condition:
                return "see your primary care physician for antibiotic evaluation"
            elif 'cardiac' in primary_condition or 'heart' in primary_condition:
                return "follow up with your primary care physician and consider cardiology referral"
            else:
                return "follow up with your primary care physician for further evaluation"
        else:
            return "monitor symptoms and follow up with your healthcare provider as needed"
    
    def _get_tests_needed(self, data: Dict[str, Any]) -> str:
        """Get primary tests needed"""
        
        chief_complaint = data.get('chief_complaint', '').lower()
        
        if 'chest' in chief_complaint:
            return "ECG, chest X-ray, and cardiac enzymes"
        elif 'head' in chief_complaint:
            return "neurological examination and blood pressure monitoring"
        elif 'abdominal' in chief_complaint:
            return "blood work and abdominal imaging"
        else:
            return "appropriate diagnostic testing based on your symptoms"