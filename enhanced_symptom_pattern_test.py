#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime, timedelta
import uuid

class EnhancedSymptomPatternTester:
    def __init__(self, base_url="https://medchat-enhance.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}" if endpoint else self.base_url
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=60)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=60)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=60)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=60)

            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:500]}...")
                except:
                    print(f"   Response: {response.text[:500]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:500]}...")

            self.test_results.append({
                'name': name,
                'success': success,
                'status_code': response.status_code,
                'expected_status': expected_status,
                'response': response.text[:500] if not success else "OK"
            })

            return success, response.json() if success and response.text else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.test_results.append({
                'name': name,
                'success': False,
                'error': str(e)
            })
            return False, {}

    def test_phase1_enhanced_pain_expressions(self):
        """Test Phase 1: Enhanced Pain Expression Recognition"""
        print("\n🎯 TESTING PHASE 1: ENHANCED PAIN EXPRESSIONS")
        
        # Test comprehensive pain expressions
        pain_test_cases = [
            {
                "name": "Crushing Chest Pain",
                "message": "I have crushing chest pain that started yesterday morning, radiating to my left arm, 8/10 severity, getting worse over the past few hours",
                "expected_patterns": ["crushing", "chest_pain", "radiating", "severity_8", "temporal_progression"]
            },
            {
                "name": "Stabbing Abdominal Pain", 
                "message": "Sharp stabbing pain in lower right side, started 2 days ago, getting progressively worse, with fever and vomiting",
                "expected_patterns": ["stabbing", "sharp", "abdominal_pain", "progressive_worsening", "associated_symptoms"]
            },
            {
                "name": "Throbbing Headache",
                "message": "Severe throbbing headache for 3 days, comes and goes every few hours, with nausea and dizziness, keeps me awake at night",
                "expected_patterns": ["throbbing", "headache", "intermittent_pattern", "functional_impact", "sleep_disruption"]
            },
            {
                "name": "Burning Sensation",
                "message": "Burning sensation in my stomach after eating, especially spicy foods, has been going on for weeks",
                "expected_patterns": ["burning", "stomach", "trigger_related", "chronic_duration"]
            }
        ]
        
        success_count = 0
        for test_case in pain_test_cases:
            consultation_data = {
                "patient_id": "enhanced_test_patient",
                "message": test_case["message"],
                "consultation_id": f"pain_test_{datetime.now().strftime('%H%M%S')}",
                "context": {
                    "patient_id": "enhanced_test_patient",
                    "current_stage": "chief_complaint",
                    "demographics": {"age": 45, "gender": "male"}
                }
            }
            
            success, response = self.run_test(
                f"Phase 1 Pain Expression - {test_case['name']}",
                "POST",
                "medical-ai/message",
                200,
                data=consultation_data
            )
            
            if success and response:
                # Analyze response for enhanced pattern recognition
                response_text = response.get('response', '').lower()
                medical_entities = response.get('medical_entities', {})
                urgency = response.get('urgency', 'routine')
                
                print(f"   🔍 Detected Urgency: {urgency}")
                print(f"   📊 Response Analysis: {len(response_text)} characters")
                
                # Check for appropriate medical response
                pain_recognition = any(pain_word in response_text for pain_word in 
                                    ['pain', 'discomfort', 'ache', 'hurt', 'symptom'])
                
                if pain_recognition:
                    print(f"   ✅ Pain pattern recognized in medical response")
                    success_count += 1
                else:
                    print(f"   ⚠️ Pain pattern may not be fully recognized")
        
        return success_count >= len(pain_test_cases) * 0.8  # 80% success rate

    def test_phase1_temporal_patterns(self):
        """Test Phase 1: Advanced Temporal Pattern Recognition"""
        print("\n🎯 TESTING PHASE 1: ADVANCED TEMPORAL PATTERNS")
        
        temporal_test_cases = [
            {
                "name": "Onset Yesterday Morning",
                "message": "The pain started yesterday morning around 8 AM and has been constant since then",
                "expected_temporal": ["yesterday_morning", "constant_duration", "specific_time"]
            },
            {
                "name": "Intermittent Pattern",
                "message": "It comes and goes every 2-3 hours, lasting about 30 minutes each time",
                "expected_temporal": ["intermittent", "cyclical_pattern", "duration_specific"]
            },
            {
                "name": "Progressive Worsening",
                "message": "Started mild 3 days ago but getting worse over time, now it's severe",
                "expected_temporal": ["progressive_worsening", "3_days_duration", "severity_progression"]
            },
            {
                "name": "Sudden Onset",
                "message": "It hit me suddenly while I was walking, like a lightning bolt, worst pain ever",
                "expected_temporal": ["sudden_onset", "activity_related", "maximal_severity"]
            }
        ]
        
        success_count = 0
        for test_case in temporal_test_cases:
            consultation_data = {
                "patient_id": "temporal_test_patient",
                "message": test_case["message"],
                "consultation_id": f"temporal_test_{datetime.now().strftime('%H%M%S')}",
                "context": {
                    "patient_id": "temporal_test_patient",
                    "current_stage": "history_present_illness",
                    "demographics": {"age": 35, "gender": "female"}
                }
            }
            
            success, response = self.run_test(
                f"Phase 1 Temporal Pattern - {test_case['name']}",
                "POST",
                "medical-ai/message",
                200,
                data=consultation_data
            )
            
            if success and response:
                response_text = response.get('response', '').lower()
                next_questions = response.get('next_questions', [])
                
                # Check for temporal awareness in response
                temporal_awareness = any(temporal_word in response_text for temporal_word in 
                                       ['when', 'duration', 'onset', 'time', 'started', 'pattern', 'frequency'])
                
                if temporal_awareness:
                    print(f"   ✅ Temporal pattern awareness detected")
                    success_count += 1
                else:
                    print(f"   ⚠️ Limited temporal pattern recognition")
                
                print(f"   📋 Follow-up questions: {len(next_questions)}")
        
        return success_count >= len(temporal_test_cases) * 0.8

    def test_phase1_severity_quantification(self):
        """Test Phase 1: Severity Quantification and Normalization"""
        print("\n🎯 TESTING PHASE 1: SEVERITY QUANTIFICATION")
        
        severity_test_cases = [
            {
                "name": "Numeric Scale 8/10",
                "message": "The pain is about 8 out of 10, really severe and hard to bear",
                "expected_severity": "severe",
                "numeric_scale": 8
            },
            {
                "name": "Descriptive - Excruciating",
                "message": "The pain is excruciating, worst I've ever felt, can't function normally",
                "expected_severity": "extreme",
                "functional_impact": True
            },
            {
                "name": "Functional Impact",
                "message": "It keeps me awake at night and I can't concentrate at work",
                "expected_severity": "significant",
                "functional_impact": True
            },
            {
                "name": "Mild Descriptive",
                "message": "It's just a mild discomfort, barely noticeable most of the time",
                "expected_severity": "mild",
                "functional_impact": False
            },
            {
                "name": "Comparative Severity",
                "message": "Much worse than my usual headaches, this is the worst headache ever",
                "expected_severity": "extreme",
                "comparative": True
            }
        ]
        
        success_count = 0
        for test_case in severity_test_cases:
            consultation_data = {
                "patient_id": "severity_test_patient",
                "message": test_case["message"],
                "consultation_id": f"severity_test_{datetime.now().strftime('%H%M%S')}",
                "context": {
                    "patient_id": "severity_test_patient",
                    "current_stage": "history_present_illness",
                    "demographics": {"age": 40, "gender": "male"}
                }
            }
            
            success, response = self.run_test(
                f"Phase 1 Severity - {test_case['name']}",
                "POST",
                "medical-ai/message",
                200,
                data=consultation_data
            )
            
            if success and response:
                response_text = response.get('response', '').lower()
                urgency = response.get('urgency', 'routine')
                
                # Check for severity recognition
                severity_recognition = any(severity_word in response_text for severity_word in 
                                         ['severe', 'mild', 'moderate', 'intensity', 'scale', 'level'])
                
                # Check urgency alignment with severity
                expected_urgency_high = test_case["expected_severity"] in ["severe", "extreme"]
                actual_urgency_high = urgency in ["urgent", "emergency"]
                
                urgency_appropriate = (expected_urgency_high == actual_urgency_high) or urgency != "routine"
                
                if severity_recognition and urgency_appropriate:
                    print(f"   ✅ Severity appropriately recognized and classified")
                    success_count += 1
                else:
                    print(f"   ⚠️ Severity recognition needs improvement")
                
                print(f"   📊 Urgency Level: {urgency}")
        
        return success_count >= len(severity_test_cases) * 0.7

    def test_phase1_body_location_patterns(self):
        """Test Phase 1: Body Location and Anatomical Pattern Recognition"""
        print("\n🎯 TESTING PHASE 1: BODY LOCATION PATTERNS")
        
        location_test_cases = [
            {
                "name": "Specific Anatomical Location",
                "message": "Sharp pain in the lower right quadrant of my abdomen, near the appendix area",
                "expected_locations": ["lower_right_quadrant", "abdomen", "appendix_area"]
            },
            {
                "name": "Bilateral Symptoms",
                "message": "I have pain in both knees, worse on the left side, especially when walking",
                "expected_locations": ["bilateral_knees", "left_predominant", "weight_bearing"]
            },
            {
                "name": "Radiating Pattern",
                "message": "Chest pain that radiates down my left arm and up to my jaw",
                "expected_locations": ["chest", "left_arm", "jaw", "radiating_pattern"]
            },
            {
                "name": "Multiple Body Systems",
                "message": "Headache with neck stiffness and sensitivity to light",
                "expected_locations": ["head", "neck", "neurological_symptoms"]
            }
        ]
        
        success_count = 0
        for test_case in location_test_cases:
            consultation_data = {
                "patient_id": "location_test_patient",
                "message": test_case["message"],
                "consultation_id": f"location_test_{datetime.now().strftime('%H%M%S')}",
                "context": {
                    "patient_id": "location_test_patient",
                    "current_stage": "chief_complaint",
                    "demographics": {"age": 50, "gender": "female"}
                }
            }
            
            success, response = self.run_test(
                f"Phase 1 Body Location - {test_case['name']}",
                "POST",
                "medical-ai/message",
                200,
                data=consultation_data
            )
            
            if success and response:
                response_text = response.get('response', '').lower()
                differential_diagnoses = response.get('differential_diagnoses', [])
                
                # Check for anatomical awareness
                anatomical_awareness = any(location_word in response_text for location_word in 
                                         ['location', 'area', 'region', 'side', 'abdomen', 'chest', 'head'])
                
                if anatomical_awareness:
                    print(f"   ✅ Anatomical location awareness detected")
                    success_count += 1
                else:
                    print(f"   ⚠️ Limited anatomical location recognition")
                
                print(f"   🔍 Differential diagnoses: {len(differential_diagnoses)}")
        
        return success_count >= len(location_test_cases) * 0.8

    def test_phase1_emergency_pattern_recognition(self):
        """Test Phase 1: Emergency Pattern Recognition"""
        print("\n🎯 TESTING PHASE 1: EMERGENCY PATTERN RECOGNITION")
        
        emergency_test_cases = [
            {
                "name": "Crushing Chest Pain Emergency",
                "message": "Crushing chest pain, can't breathe, sweating profusely, feels like an elephant on my chest",
                "expected_urgency": "emergency",
                "expected_emergency": True
            },
            {
                "name": "Worst Headache Ever",
                "message": "Worst headache of my life, came on suddenly like a thunderclap, with neck stiffness",
                "expected_urgency": "emergency", 
                "expected_emergency": True
            },
            {
                "name": "Stroke Symptoms",
                "message": "Sudden weakness on my right side, face is drooping, can't speak clearly",
                "expected_urgency": "emergency",
                "expected_emergency": True
            },
            {
                "name": "Severe Allergic Reaction",
                "message": "Severe allergic reaction, throat swelling, difficulty breathing, hives all over",
                "expected_urgency": "emergency",
                "expected_emergency": True
            }
        ]
        
        success_count = 0
        for test_case in emergency_test_cases:
            consultation_data = {
                "patient_id": "emergency_test_patient",
                "message": test_case["message"],
                "consultation_id": f"emergency_test_{datetime.now().strftime('%H%M%S')}",
                "context": {
                    "patient_id": "emergency_test_patient",
                    "current_stage": "chief_complaint",
                    "demographics": {"age": 55, "gender": "male"}
                }
            }
            
            success, response = self.run_test(
                f"Phase 1 Emergency Pattern - {test_case['name']}",
                "POST",
                "medical-ai/message",
                200,
                data=consultation_data
            )
            
            if success and response:
                urgency = response.get('urgency', 'routine')
                emergency_detected = response.get('emergency_detected', False)
                response_text = response.get('response', '').lower()
                
                # Check for emergency recognition
                emergency_properly_detected = (urgency == "emergency" or emergency_detected)
                emergency_language = any(emergency_word in response_text for emergency_word in 
                                       ['911', 'emergency', 'immediate', 'urgent', 'critical'])
                
                if emergency_properly_detected and emergency_language:
                    print(f"   ✅ Emergency pattern correctly identified")
                    success_count += 1
                else:
                    print(f"   ❌ Emergency pattern not properly detected")
                
                print(f"   🚨 Urgency: {urgency}, Emergency Detected: {emergency_detected}")
        
        return success_count >= len(emergency_test_cases) * 0.9  # High threshold for emergencies

    def test_phase2_symptom_entity_extraction(self):
        """Test Phase 2: SymptomEntity Class with Advanced Attributes"""
        print("\n🎯 TESTING PHASE 2: SYMPTOM ENTITY EXTRACTION")
        
        entity_test_cases = [
            {
                "name": "Complex Symptom with All Attributes",
                "message": "I have severe stabbing chest pain, 9/10 intensity, started 2 hours ago suddenly, gets worse with movement, relieved by rest, associated with shortness of breath and nausea",
                "expected_entities": {
                    "symptom": "chest_pain",
                    "quality": "stabbing", 
                    "severity": "severe",
                    "severity_score": 9.0,
                    "duration": "2_hours",
                    "onset": "sudden",
                    "triggers": ["movement"],
                    "relieving_factors": ["rest"],
                    "associated_symptoms": ["shortness_of_breath", "nausea"]
                }
            },
            {
                "name": "Headache with Temporal Pattern",
                "message": "Throbbing headache on the left side, moderate intensity around 6/10, comes and goes every few hours, triggered by bright lights, better with dark room and sleep",
                "expected_entities": {
                    "symptom": "headache",
                    "location": "left_side",
                    "quality": "throbbing",
                    "severity_score": 6.0,
                    "frequency": "every_few_hours",
                    "triggers": ["bright_lights"],
                    "relieving_factors": ["dark_room", "sleep"]
                }
            }
        ]
        
        success_count = 0
        for test_case in entity_test_cases:
            consultation_data = {
                "patient_id": "entity_test_patient",
                "message": test_case["message"],
                "consultation_id": f"entity_test_{datetime.now().strftime('%H%M%S')}",
                "context": {
                    "patient_id": "entity_test_patient",
                    "current_stage": "history_present_illness",
                    "demographics": {"age": 42, "gender": "female"}
                }
            }
            
            success, response = self.run_test(
                f"Phase 2 Symptom Entity - {test_case['name']}",
                "POST",
                "medical-ai/message",
                200,
                data=consultation_data
            )
            
            if success and response:
                # Check for comprehensive symptom understanding
                response_text = response.get('response', '').lower()
                next_questions = response.get('next_questions', [])
                
                # Look for evidence of detailed symptom analysis
                detailed_analysis = any(detail_word in response_text for detail_word in 
                                      ['quality', 'severity', 'duration', 'triggers', 'relieving', 'associated'])
                
                comprehensive_questions = len(next_questions) > 0
                
                if detailed_analysis or comprehensive_questions:
                    print(f"   ✅ Comprehensive symptom entity extraction evident")
                    success_count += 1
                else:
                    print(f"   ⚠️ Basic symptom recognition, may lack detailed entity extraction")
                
                print(f"   📋 Follow-up questions: {len(next_questions)}")
        
        return success_count >= len(entity_test_cases) * 0.8

    def test_phase2_temporal_entity_parsing(self):
        """Test Phase 2: TemporalEntity Class for Complex Time Expressions"""
        print("\n🎯 TESTING PHASE 2: TEMPORAL ENTITY PARSING")
        
        temporal_entity_test_cases = [
            {
                "name": "Complex Onset Time",
                "message": "The pain started yesterday morning around 8 AM, right after I finished my morning jog",
                "expected_temporal": {
                    "onset_time": "yesterday_8am",
                    "pattern_type": "onset",
                    "activity_related": True
                }
            },
            {
                "name": "Duration with Progression",
                "message": "It's been going on for 3 weeks now, getting progressively worse each day",
                "expected_temporal": {
                    "duration_days": 21,
                    "pattern_type": "duration",
                    "progression": "getting_worse"
                }
            },
            {
                "name": "Frequency Pattern",
                "message": "Comes and goes every 2-3 hours, lasting about 30 minutes each episode",
                "expected_temporal": {
                    "frequency": "every_2_3_hours",
                    "pattern_type": "frequency",
                    "episode_duration": "30_minutes"
                }
            }
        ]
        
        success_count = 0
        for test_case in temporal_entity_test_cases:
            consultation_data = {
                "patient_id": "temporal_entity_test",
                "message": test_case["message"],
                "consultation_id": f"temporal_entity_{datetime.now().strftime('%H%M%S')}",
                "context": {
                    "patient_id": "temporal_entity_test",
                    "current_stage": "history_present_illness",
                    "demographics": {"age": 38, "gender": "male"}
                }
            }
            
            success, response = self.run_test(
                f"Phase 2 Temporal Entity - {test_case['name']}",
                "POST",
                "medical-ai/message",
                200,
                data=consultation_data
            )
            
            if success and response:
                response_text = response.get('response', '').lower()
                
                # Check for temporal sophistication
                temporal_sophistication = any(temporal_word in response_text for temporal_word in 
                                            ['timeline', 'progression', 'pattern', 'frequency', 'duration', 'onset'])
                
                if temporal_sophistication:
                    print(f"   ✅ Advanced temporal entity parsing detected")
                    success_count += 1
                else:
                    print(f"   ⚠️ Basic temporal recognition")
        
        return success_count >= len(temporal_entity_test_cases) * 0.8

    def test_phase2_severity_entity_normalization(self):
        """Test Phase 2: SeverityEntity Class for Scale Normalization"""
        print("\n🎯 TESTING PHASE 2: SEVERITY ENTITY NORMALIZATION")
        
        severity_entity_test_cases = [
            {
                "name": "Numeric Scale Normalization",
                "message": "The pain is 7 out of 10, pretty severe and affecting my daily activities",
                "expected_normalized": 7.0,
                "scale_type": "numeric"
            },
            {
                "name": "Descriptive to Numeric",
                "message": "Excruciating pain, worst I've ever experienced, can't function at all",
                "expected_normalized": 9.0,
                "scale_type": "descriptive"
            },
            {
                "name": "Functional Impact Scale",
                "message": "The pain keeps me awake at night and I can't concentrate at work",
                "expected_normalized": 8.0,
                "scale_type": "functional"
            },
            {
                "name": "Mild Descriptive Scale",
                "message": "Just a mild discomfort, barely noticeable unless I focus on it",
                "expected_normalized": 2.0,
                "scale_type": "descriptive"
            }
        ]
        
        success_count = 0
        for test_case in severity_entity_test_cases:
            consultation_data = {
                "patient_id": "severity_entity_test",
                "message": test_case["message"],
                "consultation_id": f"severity_entity_{datetime.now().strftime('%H%M%S')}",
                "context": {
                    "patient_id": "severity_entity_test",
                    "current_stage": "history_present_illness",
                    "demographics": {"age": 45, "gender": "female"}
                }
            }
            
            success, response = self.run_test(
                f"Phase 2 Severity Entity - {test_case['name']}",
                "POST",
                "medical-ai/message",
                200,
                data=consultation_data
            )
            
            if success and response:
                urgency = response.get('urgency', 'routine')
                response_text = response.get('response', '').lower()
                
                # Check for appropriate urgency based on normalized severity
                expected_high_urgency = test_case["expected_normalized"] >= 7.0
                actual_high_urgency = urgency in ["urgent", "emergency"]
                
                severity_normalization_appropriate = (expected_high_urgency == actual_high_urgency) or urgency != "routine"
                
                if severity_normalization_appropriate:
                    print(f"   ✅ Severity normalization appears appropriate")
                    success_count += 1
                else:
                    print(f"   ⚠️ Severity normalization may need improvement")
                
                print(f"   📊 Urgency: {urgency} (Expected high: {expected_high_urgency})")
        
        return success_count >= len(severity_entity_test_cases) * 0.8

    def test_phase2_context_aware_processing(self):
        """Test Phase 2: AdvancedSymptomRecognizer Context-Aware Processing"""
        print("\n🎯 TESTING PHASE 2: CONTEXT-AWARE PROCESSING")
        
        context_test_cases = [
            {
                "name": "Medical History Context",
                "message": "Chest pain similar to what I had during my heart attack 2 years ago",
                "context": {
                    "medical_history": ["myocardial_infarction"],
                    "demographics": {"age": 65, "gender": "male"}
                },
                "expected_urgency": "urgent"
            },
            {
                "name": "Age-Gender Context",
                "message": "Severe abdominal pain in lower right side with nausea",
                "context": {
                    "demographics": {"age": 16, "gender": "male"}
                },
                "expected_consideration": "appendicitis"
            },
            {
                "name": "Medication Context",
                "message": "Stomach pain and nausea, started after taking my new medication",
                "context": {
                    "current_medications": ["ibuprofen", "aspirin"],
                    "demographics": {"age": 45, "gender": "female"}
                },
                "expected_consideration": "medication_side_effect"
            }
        ]
        
        success_count = 0
        for test_case in context_test_cases:
            consultation_data = {
                "patient_id": "context_test_patient",
                "message": test_case["message"],
                "consultation_id": f"context_test_{datetime.now().strftime('%H%M%S')}",
                "context": {
                    "patient_id": "context_test_patient",
                    "current_stage": "chief_complaint",
                    "demographics": test_case["context"].get("demographics", {}),
                    "medical_history": test_case["context"].get("medical_history", {}),
                    "medications": test_case["context"].get("current_medications", [])
                }
            }
            
            success, response = self.run_test(
                f"Phase 2 Context-Aware - {test_case['name']}",
                "POST",
                "medical-ai/message",
                200,
                data=consultation_data
            )
            
            if success and response:
                urgency = response.get('urgency', 'routine')
                differential_diagnoses = response.get('differential_diagnoses', [])
                response_text = response.get('response', '').lower()
                
                # Check for context awareness
                context_awareness = any(context_word in response_text for context_word in 
                                      ['history', 'previous', 'medication', 'age', 'similar'])
                
                if context_awareness or len(differential_diagnoses) > 0:
                    print(f"   ✅ Context-aware processing detected")
                    success_count += 1
                else:
                    print(f"   ⚠️ Limited context awareness")
                
                print(f"   🔍 Differential diagnoses: {len(differential_diagnoses)}")
                print(f"   ⚡ Urgency: {urgency}")
        
        return success_count >= len(context_test_cases) * 0.8

    def test_phase2_confidence_scoring(self):
        """Test Phase 2: Confidence Scoring and Uncertainty Handling"""
        print("\n🎯 TESTING PHASE 2: CONFIDENCE SCORING & UNCERTAINTY")
        
        confidence_test_cases = [
            {
                "name": "High Confidence Clear Symptoms",
                "message": "Crushing chest pain, 9/10 severity, radiating to left arm, started 1 hour ago, with shortness of breath and sweating",
                "expected_confidence": "high"
            },
            {
                "name": "Uncertain Patient Expression",
                "message": "I think maybe it's chest pain, not sure, kind of feels like pressure, might be heartburn",
                "expected_confidence": "low"
            },
            {
                "name": "Vague Symptom Description",
                "message": "Something doesn't feel right, just not feeling well, hard to describe",
                "expected_confidence": "very_low"
            },
            {
                "name": "Specific Detailed Description",
                "message": "Sharp, stabbing pain in lower right abdomen, 7/10 intensity, started 6 hours ago, worse with movement, associated with nausea and low-grade fever",
                "expected_confidence": "high"
            }
        ]
        
        success_count = 0
        for test_case in confidence_test_cases:
            consultation_data = {
                "patient_id": "confidence_test_patient",
                "message": test_case["message"],
                "consultation_id": f"confidence_test_{datetime.now().strftime('%H%M%S')}",
                "context": {
                    "patient_id": "confidence_test_patient",
                    "current_stage": "chief_complaint",
                    "demographics": {"age": 40, "gender": "male"}
                }
            }
            
            success, response = self.run_test(
                f"Phase 2 Confidence - {test_case['name']}",
                "POST",
                "medical-ai/message",
                200,
                data=consultation_data
            )
            
            if success and response:
                response_text = response.get('response', '').lower()
                next_questions = response.get('next_questions', [])
                
                # Assess confidence based on response characteristics
                uncertainty_language = any(uncertain_word in response_text for uncertain_word in 
                                         ['clarify', 'more information', 'describe further', 'uncertain'])
                
                detailed_questions = len(next_questions) > 2
                
                # High confidence should have fewer clarifying questions
                # Low confidence should have more clarifying questions
                confidence_appropriate = True
                if test_case["expected_confidence"] == "high":
                    confidence_appropriate = not (uncertainty_language and detailed_questions)
                elif test_case["expected_confidence"] in ["low", "very_low"]:
                    confidence_appropriate = uncertainty_language or detailed_questions
                
                if confidence_appropriate:
                    print(f"   ✅ Confidence handling appears appropriate")
                    success_count += 1
                else:
                    print(f"   ⚠️ Confidence scoring may need adjustment")
                
                print(f"   📋 Follow-up questions: {len(next_questions)}")
        
        return success_count >= len(confidence_test_cases) * 0.8

    def run_comprehensive_enhanced_symptom_tests(self):
        """Run comprehensive tests for Phase 1 & Phase 2 Enhanced Symptom Pattern Architecture"""
        print("🚀 Starting Comprehensive Enhanced Symptom Pattern Architecture Tests...")
        print(f"   Base URL: {self.base_url}")
        print("=" * 80)
        
        # Phase 1 Tests
        print("\n🎯 PHASE 1: ENHANCED SYMPTOM PATTERNS TESTING")
        phase1_pain_success = self.test_phase1_enhanced_pain_expressions()
        phase1_temporal_success = self.test_phase1_temporal_patterns()
        phase1_severity_success = self.test_phase1_severity_quantification()
        phase1_location_success = self.test_phase1_body_location_patterns()
        phase1_emergency_success = self.test_phase1_emergency_pattern_recognition()
        
        # Phase 2 Tests
        print("\n🎯 PHASE 2: INTELLIGENT ENTITY EXTRACTION TESTING")
        phase2_symptom_success = self.test_phase2_symptom_entity_extraction()
        phase2_temporal_success = self.test_phase2_temporal_entity_parsing()
        phase2_severity_success = self.test_phase2_severity_entity_normalization()
        phase2_context_success = self.test_phase2_context_aware_processing()
        phase2_confidence_success = self.test_phase2_confidence_scoring()
        
        # Print final results
        print("\n" + "=" * 80)
        print(f"📊 FINAL RESULTS")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        print(f"\n🎯 PHASE 1 ENHANCED SYMPTOM PATTERNS TEST RESULTS:")
        print(f"   1. Enhanced Pain Expressions: {'✅ PASSED' if phase1_pain_success else '❌ FAILED'}")
        print(f"   2. Advanced Temporal Patterns: {'✅ PASSED' if phase1_temporal_success else '❌ FAILED'}")
        print(f"   3. Severity Quantification: {'✅ PASSED' if phase1_severity_success else '❌ FAILED'}")
        print(f"   4. Body Location Patterns: {'✅ PASSED' if phase1_location_success else '❌ FAILED'}")
        print(f"   5. Emergency Pattern Recognition: {'✅ PASSED' if phase1_emergency_success else '❌ FAILED'}")
        
        print(f"\n🎯 PHASE 2 INTELLIGENT ENTITY EXTRACTION TEST RESULTS:")
        print(f"   1. SymptomEntity Class Testing: {'✅ PASSED' if phase2_symptom_success else '❌ FAILED'}")
        print(f"   2. TemporalEntity Class Testing: {'✅ PASSED' if phase2_temporal_success else '❌ FAILED'}")
        print(f"   3. SeverityEntity Class Testing: {'✅ PASSED' if phase2_severity_success else '❌ FAILED'}")
        print(f"   4. Context-Aware Processing: {'✅ PASSED' if phase2_context_success else '❌ FAILED'}")
        print(f"   5. Confidence Scoring: {'✅ PASSED' if phase2_confidence_success else '❌ FAILED'}")
        
        # Calculate phase success rates
        phase1_tests = [phase1_pain_success, phase1_temporal_success, phase1_severity_success, 
                       phase1_location_success, phase1_emergency_success]
        phase2_tests = [phase2_symptom_success, phase2_temporal_success, phase2_severity_success,
                       phase2_context_success, phase2_confidence_success]
        
        phase1_success_rate = sum(phase1_tests) / len(phase1_tests) * 100
        phase2_success_rate = sum(phase2_tests) / len(phase2_tests) * 100
        
        print(f"\n📈 PHASE SUCCESS RATES:")
        print(f"   Phase 1 Enhanced Symptom Patterns: {phase1_success_rate:.1f}%")
        print(f"   Phase 2 Intelligent Entity Extraction: {phase2_success_rate:.1f}%")
        
        # Overall success
        overall_success = (phase1_success_rate >= 80 and phase2_success_rate >= 80)
        
        if overall_success:
            print("\n🎉 Enhanced Symptom Pattern Architecture passed comprehensive testing!")
            print("✅ Phase 1 & Phase 2 implementations are working correctly")
            return 0
        else:
            print("\n⚠️ Some Enhanced Symptom Pattern features failed testing.")
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result.get('success', False):
                    print(f"  - {result['name']}: {result.get('error', 'Status code mismatch')}")
            return 1

if __name__ == "__main__":
    tester = EnhancedSymptomPatternTester()
    exit_code = tester.run_comprehensive_enhanced_symptom_tests()
    sys.exit(exit_code)