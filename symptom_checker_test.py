#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime, timedelta
import uuid

class SymptomCheckerAPITester:
    def __init__(self, base_url="https://symptom-analyzer-5.preview.emergentagent.com/api"):
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
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)

            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:300]}...")
                except:
                    print(f"   Response: {response.text[:300]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:300]}...")

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

    def test_symptom_assessment(self):
        """Test POST /api/symptom-checker/assess - Main symptom assessment endpoint"""
        print("\n🔍 Testing Symptom Assessment Endpoint...")
        
        # Test 1: Comprehensive symptom assessment with multiple symptoms
        assessment_data = {
            "user_id": f"guest_user_{datetime.now().strftime('%H%M%S')}",
            "symptoms": [
                {
                    "name": "headache",
                    "severity": 6,
                    "frequency": 3,
                    "duration_days": 2,
                    "life_impact": 4,
                    "description": "Throbbing pain on the right side of head",
                    "triggers": ["stress", "lack_of_sleep"]
                },
                {
                    "name": "fatigue",
                    "severity": 7,
                    "frequency": 4,
                    "duration_days": 3,
                    "life_impact": 5,
                    "description": "Constant tiredness affecting work performance",
                    "triggers": ["poor_sleep", "work_stress"]
                }
            ],
            "additional_info": {
                "age": 32,
                "gender": "female",
                "medical_history": ["migraines"],
                "current_medications": ["ibuprofen"],
                "lifestyle_factors": ["high_stress_job", "irregular_sleep"]
            }
        }
        
        success1, response1 = self.run_test(
            "Symptom Assessment - Multiple Symptoms",
            "POST",
            "symptom-checker/assess",
            200,
            data=assessment_data
        )
        
        # Validate assessment response structure
        if success1 and response1:
            expected_keys = ['assessment_id', 'symptom_profile', 'instant_relief', 'action_plan', 
                           'medical_advisory', 'ai_recommendations', 'estimated_relief_time', 'confidence_score']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Assessment response contains all required keys: {expected_keys}")
                
                assessment_id = response1.get('assessment_id', '')
                symptom_profile = response1.get('symptom_profile', {})
                instant_relief = response1.get('instant_relief', [])
                action_plan = response1.get('action_plan', {})
                medical_advisory = response1.get('medical_advisory', {})
                confidence_score = response1.get('confidence_score', 0)
                
                print(f"   🆔 Assessment ID: {assessment_id}")
                print(f"   📊 Symptom profile severity: {symptom_profile.get('severity_score', 0)}")
                print(f"   💊 Instant relief options: {len(instant_relief)}")
                print(f"   📋 Action plan provided: {'Yes' if action_plan else 'No'}")
                print(f"   🏥 Medical advisory level: {medical_advisory.get('alert_level', 'unknown')}")
                print(f"   🎯 Confidence score: {confidence_score}")
                
                # Store assessment_id for progress testing
                self.test_assessment_id = assessment_id
                self.test_user_id = assessment_data["user_id"]
                
            else:
                print(f"   ❌ Assessment response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Single severe symptom assessment
        severe_symptom_data = {
            "user_id": f"guest_user_severe_{datetime.now().strftime('%H%M%S')}",
            "symptoms": [
                {
                    "name": "chest_pain",
                    "severity": 9,
                    "frequency": 5,
                    "duration_days": 0,
                    "life_impact": 5,
                    "description": "Sharp chest pain with difficulty breathing",
                    "triggers": ["physical_exertion"]
                }
            ],
            "additional_info": {
                "age": 45,
                "gender": "male",
                "medical_history": ["hypertension"],
                "current_medications": ["lisinopril"]
            }
        }
        
        success2, response2 = self.run_test(
            "Symptom Assessment - Severe Chest Pain",
            "POST",
            "symptom-checker/assess",
            200,
            data=severe_symptom_data
        )
        
        # Validate severe symptom handling
        if success2 and response2:
            medical_advisory = response2.get('medical_advisory', {})
            alert_level = medical_advisory.get('alert_level', '')
            print(f"   🚨 Severe symptom alert level: {alert_level}")
            
            # Should trigger high alert for chest pain
            severe_handling_valid = alert_level in ['red', 'emergency']
            print(f"   🏥 Severe symptom handling: {'✅' if severe_handling_valid else '❌'}")
        
        # Test 3: Mild symptoms assessment
        mild_symptom_data = {
            "user_id": f"guest_user_mild_{datetime.now().strftime('%H%M%S')}",
            "symptoms": [
                {
                    "name": "runny_nose",
                    "severity": 3,
                    "frequency": 2,
                    "duration_days": 1,
                    "life_impact": 2,
                    "description": "Mild cold symptoms",
                    "triggers": ["weather_change"]
                }
            ],
            "additional_info": {
                "age": 28,
                "gender": "female"
            }
        }
        
        success3, response3 = self.run_test(
            "Symptom Assessment - Mild Cold Symptoms",
            "POST",
            "symptom-checker/assess",
            200,
            data=mild_symptom_data
        )
        
        return success1 and success2 and success3

    def test_progress_update(self):
        """Test POST /api/symptom-checker/progress-update - Progress tracking endpoint"""
        print("\n📈 Testing Progress Update Endpoint...")
        
        # Use assessment_id from previous test if available
        plan_id = getattr(self, 'test_assessment_id', f"plan_{datetime.now().strftime('%H%M%S')}")
        user_id = getattr(self, 'test_user_id', f"test_user_{datetime.now().strftime('%H%M%S')}")
        
        # Test 1: Day 1 progress update
        progress_data_day1 = {
            "plan_id": plan_id,
            "user_id": user_id,
            "day": 1,
            "time_of_day": "morning",
            "symptom_ratings": {
                "headache": 5,
                "fatigue": 6
            },
            "interventions_used": ["rest", "hydration", "ibuprofen"],
            "intervention_effectiveness": {
                "rest": 7,
                "hydration": 6,
                "ibuprofen": 8
            },
            "side_effects": [],
            "triggers_identified": ["stress", "dehydration"],
            "notes": "Feeling slightly better after rest and medication",
            "overall_improvement": 6,
            "quality_of_life_impact": 7,
            "sleep_quality": 6,
            "energy_level": 5
        }
        
        success1, response1 = self.run_test(
            "Progress Update - Day 1 Morning",
            "POST",
            "symptom-checker/progress-update",
            200,
            data=progress_data_day1
        )
        
        # Validate progress response
        if success1 and response1:
            expected_keys = ['success', 'progress_logged', 'current_analytics', 
                           'adjustment_needed', 'next_milestone', 'recommendations']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Progress response contains all required keys: {expected_keys}")
                
                progress_logged = response1.get('progress_logged', False)
                current_analytics = response1.get('current_analytics', {})
                adjustment_needed = response1.get('adjustment_needed', False)
                recommendations = response1.get('recommendations', [])
                
                print(f"   📝 Progress logged: {progress_logged}")
                print(f"   📊 Analytics available: {'Yes' if current_analytics else 'No'}")
                print(f"   🔧 Adjustment needed: {adjustment_needed}")
                print(f"   💡 Recommendations provided: {len(recommendations)}")
                
            else:
                print(f"   ❌ Progress response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Day 2 progress update with improvement
        progress_data_day2 = {
            "plan_id": plan_id,
            "user_id": user_id,
            "day": 2,
            "time_of_day": "evening",
            "symptom_ratings": {
                "headache": 3,
                "fatigue": 4
            },
            "interventions_used": ["rest", "hydration", "meditation"],
            "intervention_effectiveness": {
                "rest": 8,
                "hydration": 7,
                "meditation": 9
            },
            "side_effects": [],
            "triggers_identified": ["work_stress"],
            "notes": "Significant improvement, meditation really helped",
            "overall_improvement": 8,
            "quality_of_life_impact": 8,
            "sleep_quality": 8,
            "energy_level": 7
        }
        
        success2, response2 = self.run_test(
            "Progress Update - Day 2 Evening (Improved)",
            "POST",
            "symptom-checker/progress-update",
            200,
            data=progress_data_day2
        )
        
        # Test 3: Day 3 progress update with worsening
        progress_data_day3 = {
            "plan_id": plan_id,
            "user_id": user_id,
            "day": 3,
            "time_of_day": "midday",
            "symptom_ratings": {
                "headache": 7,
                "fatigue": 8
            },
            "interventions_used": ["rest", "ibuprofen"],
            "intervention_effectiveness": {
                "rest": 4,
                "ibuprofen": 5
            },
            "side_effects": ["stomach_upset"],
            "triggers_identified": ["poor_sleep", "work_deadline"],
            "notes": "Symptoms worsened, medication less effective",
            "overall_improvement": 3,
            "quality_of_life_impact": 4,
            "sleep_quality": 3,
            "energy_level": 3
        }
        
        success3, response3 = self.run_test(
            "Progress Update - Day 3 Midday (Worsened)",
            "POST",
            "symptom-checker/progress-update",
            200,
            data=progress_data_day3
        )
        
        # Validate worsening detection
        if success3 and response3:
            adjustment_needed = response3.get('adjustment_needed', False)
            print(f"   🔧 Adjustment needed for worsening: {adjustment_needed}")
        
        return success1 and success2 and success3

    def test_emergency_check(self):
        """Test POST /api/symptom-checker/emergency-check - Emergency symptom checking"""
        print("\n🚨 Testing Emergency Check Endpoint...")
        
        # Test 1: Emergency symptoms (chest pain + difficulty breathing)
        emergency_symptoms = {
            "symptoms": [
                {
                    "name": "chest_pain",
                    "severity": 9,
                    "frequency": 5,
                    "duration_days": 0,
                    "life_impact": 5,
                    "description": "Severe chest pain with crushing sensation"
                },
                {
                    "name": "difficulty_breathing",
                    "severity": 8,
                    "frequency": 5,
                    "duration_days": 0,
                    "life_impact": 5,
                    "description": "Shortness of breath, can't catch breath"
                }
            ]
        }
        
        success1, response1 = self.run_test(
            "Emergency Check - Chest Pain + Breathing Difficulty",
            "POST",
            "symptom-checker/emergency-check",
            200,
            data=emergency_symptoms
        )
        
        # Validate emergency response
        if success1 and response1:
            expected_keys = ['alert_level', 'urgency_message', 'immediate_actions', 
                           'emergency_contacts', 'disclaimer', 'assessment_time']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Emergency response contains all required keys: {expected_keys}")
                
                alert_level = response1.get('alert_level', '')
                urgency_message = response1.get('urgency_message', '')
                immediate_actions = response1.get('immediate_actions', [])
                emergency_contacts = response1.get('emergency_contacts', [])
                
                print(f"   🚨 Alert level: {alert_level}")
                print(f"   📢 Urgency message: {urgency_message[:50]}...")
                print(f"   🏃 Immediate actions: {len(immediate_actions)}")
                print(f"   📞 Emergency contacts: {len(emergency_contacts)}")
                
                # Should be EMERGENCY level for these symptoms
                emergency_valid = alert_level.upper() == 'EMERGENCY'
                print(f"   🏥 Emergency detection: {'✅' if emergency_valid else '❌'}")
                
            else:
                print(f"   ❌ Emergency response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: High severity symptoms (multiple severe symptoms)
        high_severity_symptoms = {
            "symptoms": [
                {
                    "name": "severe_headache",
                    "severity": 8,
                    "frequency": 4,
                    "duration_days": 1,
                    "life_impact": 4
                },
                {
                    "name": "nausea",
                    "severity": 8,
                    "frequency": 4,
                    "duration_days": 1,
                    "life_impact": 4
                }
            ]
        }
        
        success2, response2 = self.run_test(
            "Emergency Check - Multiple High Severity",
            "POST",
            "symptom-checker/emergency-check",
            200,
            data=high_severity_symptoms
        )
        
        if success2 and response2:
            alert_level = response2.get('alert_level', '')
            print(f"   🔴 High severity alert level: {alert_level}")
            
            # Should be RED level for multiple high severity
            red_alert_valid = alert_level.upper() == 'RED'
            print(f"   🔴 Red alert detection: {'✅' if red_alert_valid else '❌'}")
        
        # Test 3: Moderate symptoms (should be yellow alert)
        moderate_symptoms = {
            "symptoms": [
                {
                    "name": "headache",
                    "severity": 5,
                    "frequency": 3,
                    "duration_days": 2,
                    "life_impact": 3
                },
                {
                    "name": "fatigue",
                    "severity": 4,
                    "frequency": 2,
                    "duration_days": 3,
                    "life_impact": 2
                }
            ]
        }
        
        success3, response3 = self.run_test(
            "Emergency Check - Moderate Symptoms",
            "POST",
            "symptom-checker/emergency-check",
            200,
            data=moderate_symptoms
        )
        
        if success3 and response3:
            alert_level = response3.get('alert_level', '')
            print(f"   🟡 Moderate symptoms alert level: {alert_level}")
            
            # Should be YELLOW level for moderate symptoms
            yellow_alert_valid = alert_level.upper() == 'YELLOW'
            print(f"   🟡 Yellow alert detection: {'✅' if yellow_alert_valid else '❌'}")
        
        # Test 4: Empty symptoms (edge case)
        empty_symptoms = {
            "symptoms": []
        }
        
        success4, response4 = self.run_test(
            "Emergency Check - No Symptoms",
            "POST",
            "symptom-checker/emergency-check",
            200,
            data=empty_symptoms
        )
        
        return success1 and success2 and success3 and success4

    def run_symptom_checker_tests(self):
        """Run all symptom checker API tests"""
        print("🚀 Starting Symptom Checker API Tests...")
        print(f"   Base URL: {self.base_url}")
        print("=" * 60)
        
        # Test the three main endpoints requested
        assess_success = self.test_symptom_assessment()
        progress_success = self.test_progress_update()
        emergency_success = self.test_emergency_check()
        
        # Print summary
        print(f"\n📊 Test Summary:")
        print(f"   Tests run: {self.tests_run}")
        print(f"   Tests passed: {self.tests_passed}")
        print(f"   Success rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        print(f"\n📋 Symptom Checker Test Results:")
        print(f"   ✅ Symptom Assessment: {'PASS' if assess_success else 'FAIL'}")
        print(f"   ✅ Progress Update: {'PASS' if progress_success else 'FAIL'}")
        print(f"   ✅ Emergency Check: {'PASS' if emergency_success else 'FAIL'}")
        
        overall_success = assess_success and progress_success and emergency_success
        
        print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
        
        return overall_success

if __name__ == "__main__":
    tester = SymptomCheckerAPITester()
    success = tester.run_symptom_checker_tests()
    sys.exit(0 if success else 1)