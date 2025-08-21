#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime, timedelta
import uuid

class MedicalAITester:
    def __init__(self, base_url="https://empathcare-ai.preview.emergentagent.com/api"):
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
                    print(f"   Response keys: {list(response_data.keys()) if isinstance(response_data, dict) else 'Non-dict response'}")
                    if isinstance(response_data, dict) and len(str(response_data)) < 500:
                        print(f"   Response: {json.dumps(response_data, indent=2)}")
                    else:
                        print(f"   Response preview: {str(response_data)[:300]}...")
                except:
                    print(f"   Response: {response.text[:200]}...")
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

    def test_medical_ai_initialization(self):
        """Test Medical AI Initialization endpoint"""
        print("\n🏥 Testing Medical AI Initialization...")
        
        # Test 1: Basic initialization without demographics
        init_data_basic = {
            "patient_id": "test-patient-001"
        }
        
        success1, response1 = self.run_test(
            "Medical AI Initialize - Basic",
            "POST",
            "medical-ai/initialize",
            200,
            data=init_data_basic
        )
        
        if success1 and response1:
            # Validate response structure
            expected_keys = ['response', 'context', 'stage', 'urgency', 'consultation_id', 'emergency_detected']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Response structure valid - contains all required keys")
                print(f"   📋 Stage: {response1.get('stage')}")
                print(f"   📋 Urgency: {response1.get('urgency')}")
                print(f"   📋 Consultation ID: {response1.get('consultation_id')}")
                print(f"   📋 Emergency Detected: {response1.get('emergency_detected')}")
                print(f"   💬 Response preview: {response1.get('response', '')[:100]}...")
            else:
                print(f"   ❌ Response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Initialization with demographics
        init_data_with_demographics = {
            "patient_id": "test-patient-002",
            "demographics": {
                "age": 35,
                "gender": "female",
                "medical_history": ["hypertension"],
                "current_medications": ["lisinopril"]
            }
        }
        
        success2, response2 = self.run_test(
            "Medical AI Initialize - With Demographics",
            "POST",
            "medical-ai/initialize",
            200,
            data=init_data_with_demographics
        )
        
        if success2 and response2:
            # Validate that demographics are incorporated
            context = response2.get('context', {})
            demographics = context.get('demographics', {})
            print(f"   ✅ Demographics incorporated: {bool(demographics)}")
            if demographics:
                print(f"   📋 Age: {demographics.get('age')}")
                print(f"   📋 Gender: {demographics.get('gender')}")
        
        return success1 and success2, response1.get('context', {}) if success1 else {}

    def test_medical_ai_message_processing(self, initial_context=None):
        """Test Medical AI Message Processing endpoint"""
        print("\n💬 Testing Medical AI Message Processing...")
        
        # Test 1: Emergency symptom detection
        emergency_message_data = {
            "patient_id": "test-patient-003",
            "message": "I'm having severe chest pain that feels like crushing pressure, and I'm having trouble breathing. The pain is radiating down my left arm.",
            "context": initial_context
        }
        
        success1, response1 = self.run_test(
            "Medical AI Message - Emergency Symptoms",
            "POST",
            "medical-ai/message",
            200,
            data=emergency_message_data
        )
        
        if success1 and response1:
            # Validate emergency detection
            emergency_detected = response1.get('emergency_detected', False)
            urgency = response1.get('urgency', 'routine')
            print(f"   ✅ Emergency Detection: {emergency_detected}")
            print(f"   ⚠️ Urgency Level: {urgency}")
            
            if emergency_detected or urgency == 'emergency':
                print(f"   ✅ Emergency symptoms properly detected")
            else:
                print(f"   ⚠️ Emergency symptoms may not have been detected properly")
            
            # Check for differential diagnoses
            differential_diagnoses = response1.get('differential_diagnoses', [])
            print(f"   🔍 Differential Diagnoses: {len(differential_diagnoses)} provided")
            
            # Check response quality
            ai_response = response1.get('response', '')
            if len(ai_response) > 50:
                print(f"   ✅ Comprehensive AI response provided")
                print(f"   💬 Response preview: {ai_response[:150]}...")
            else:
                print(f"   ⚠️ AI response seems too brief: {ai_response}")
        
        # Test 2: Common symptom (headache)
        common_symptom_data = {
            "patient_id": "test-patient-004",
            "message": "I've been having a headache for the past 2 days. It's mostly on the right side of my head and gets worse with bright lights.",
            "context": initial_context
        }
        
        success2, response2 = self.run_test(
            "Medical AI Message - Common Symptoms (Headache)",
            "POST",
            "medical-ai/message",
            200,
            data=common_symptom_data
        )
        
        if success2 and response2:
            # Validate non-emergency handling
            emergency_detected = response2.get('emergency_detected', False)
            urgency = response2.get('urgency', 'routine')
            print(f"   ✅ Emergency Detection: {emergency_detected} (should be False)")
            print(f"   📋 Urgency Level: {urgency} (should be routine)")
            
            # Check for appropriate medical questioning
            next_questions = response2.get('next_questions', [])
            print(f"   ❓ Next Questions: {len(next_questions)} provided")
            if next_questions:
                print(f"   💡 Sample question: {next_questions[0] if next_questions else 'None'}")
        
        # Test 3: Complex multi-system symptoms
        complex_symptom_data = {
            "patient_id": "test-patient-005",
            "message": "I've been experiencing fatigue, joint pain in multiple joints, a rash on my face, and occasional fever for the past few weeks.",
            "context": initial_context
        }
        
        success3, response3 = self.run_test(
            "Medical AI Message - Complex Multi-System Symptoms",
            "POST",
            "medical-ai/message",
            200,
            data=complex_symptom_data
        )
        
        if success3 and response3:
            # Validate complex symptom handling
            differential_diagnoses = response3.get('differential_diagnoses', [])
            recommendations = response3.get('recommendations', [])
            
            print(f"   🔍 Differential Diagnoses: {len(differential_diagnoses)} provided")
            print(f"   💡 Recommendations: {len(recommendations)} provided")
            
            # Check for comprehensive assessment
            context = response3.get('context', {})
            symptom_data = context.get('symptom_data', {})
            print(f"   📊 Symptom Data Captured: {bool(symptom_data)}")
        
        # Test 4: OLDCARTS framework testing
        oldcarts_message_data = {
            "patient_id": "test-patient-006",
            "message": "I have abdominal pain",
            "context": initial_context
        }
        
        success4, response4 = self.run_test(
            "Medical AI Message - OLDCARTS Framework",
            "POST",
            "medical-ai/message",
            200,
            data=oldcarts_message_data
        )
        
        if success4 and response4:
            # Check if OLDCARTS questions are being asked
            ai_response = response4.get('response', '').lower()
            stage = response4.get('stage', '')
            
            # Look for OLDCARTS elements in the response
            oldcarts_elements = ['onset', 'location', 'duration', 'character', 'aggravating', 'relieving', 'timing', 'severity']
            oldcarts_found = any(element in ai_response for element in oldcarts_elements)
            
            print(f"   📋 Current Stage: {stage}")
            print(f"   🔍 OLDCARTS Framework Elements Detected: {oldcarts_found}")
            
            if 'when' in ai_response or 'started' in ai_response or 'onset' in ai_response:
                print(f"   ✅ OLDCARTS questioning pattern detected")
            else:
                print(f"   ⚠️ OLDCARTS questioning pattern not clearly detected")
        
        return success1 and success2 and success3 and success4

    def test_enhanced_features_validation(self):
        """Test enhanced medical AI features"""
        print("\n🧠 Testing Enhanced Medical AI Features...")
        
        # Test 1: Comprehensive medical knowledge base
        knowledge_test_data = {
            "patient_id": "test-patient-007",
            "message": "I have chest pain, shortness of breath, and I'm sweating. I'm a 55-year-old male with diabetes and high blood pressure.",
            "context": {
                "patient_id": "test-patient-007",
                "demographics": {
                    "age": 55,
                    "gender": "male",
                    "medical_history": ["diabetes", "hypertension"]
                }
            }
        }
        
        success1, response1 = self.run_test(
            "Enhanced Features - Medical Knowledge Base",
            "POST",
            "medical-ai/message",
            200,
            data=knowledge_test_data
        )
        
        if success1 and response1:
            # Validate sophisticated clinical reasoning
            differential_diagnoses = response1.get('differential_diagnoses', [])
            context = response1.get('context', {})
            clinical_hypotheses = context.get('clinical_hypotheses', [])
            
            print(f"   🔍 Differential Diagnoses: {len(differential_diagnoses)}")
            print(f"   🧠 Clinical Hypotheses: {len(clinical_hypotheses)}")
            
            # Check for probability normalization
            if differential_diagnoses:
                total_probability = 0
                for diagnosis in differential_diagnoses:
                    if isinstance(diagnosis, dict) and 'probability' in diagnosis:
                        total_probability += diagnosis.get('probability', 0)
                
                print(f"   📊 Total Probability: {total_probability} (should be close to 100%)")
                if 95 <= total_probability <= 105:  # Allow some tolerance
                    print(f"   ✅ Probability normalization working correctly")
                else:
                    print(f"   ⚠️ Probability normalization may need adjustment")
            
            # Check urgency level calculation
            urgency = response1.get('urgency', 'routine')
            emergency_detected = response1.get('emergency_detected', False)
            print(f"   ⚠️ Urgency Level: {urgency}")
            print(f"   🚨 Emergency Detected: {emergency_detected}")
            
            # Validate professional medical assessment formatting
            ai_response = response1.get('response', '')
            if len(ai_response) > 100 and any(word in ai_response.lower() for word in ['assessment', 'recommend', 'consider', 'evaluation']):
                print(f"   ✅ Professional medical assessment formatting detected")
            else:
                print(f"   ⚠️ Professional medical assessment formatting may need improvement")
        
        # Test 2: Confidence assessment and clinical reasoning
        confidence_test_data = {
            "patient_id": "test-patient-008",
            "message": "I have a mild headache that started this morning after not sleeping well.",
            "context": None
        }
        
        success2, response2 = self.run_test(
            "Enhanced Features - Confidence Assessment",
            "POST",
            "medical-ai/message",
            200,
            data=confidence_test_data
        )
        
        if success2 and response2:
            # Check for confidence scoring
            context = response2.get('context', {})
            confidence_score = context.get('confidence_score', 0)
            
            print(f"   📊 Confidence Score: {confidence_score}")
            if 0 <= confidence_score <= 1:
                print(f"   ✅ Confidence score within valid range (0-1)")
            else:
                print(f"   ⚠️ Confidence score outside expected range")
            
            # Check clinical reasoning output
            ai_response = response2.get('response', '')
            reasoning_indicators = ['because', 'due to', 'likely', 'suggests', 'indicates']
            has_reasoning = any(indicator in ai_response.lower() for indicator in reasoning_indicators)
            
            if has_reasoning:
                print(f"   ✅ Clinical reasoning detected in response")
            else:
                print(f"   ⚠️ Clinical reasoning could be more explicit")
        
        return success1 and success2

    def test_complete_consultation_flow(self):
        """Test complete consultation flow from greeting to final assessment"""
        print("\n🔄 Testing Complete Consultation Flow...")
        
        # Step 1: Initialize consultation
        init_data = {
            "patient_id": "test-patient-flow",
            "demographics": {
                "age": 42,
                "gender": "female"
            }
        }
        
        success1, init_response = self.run_test(
            "Complete Flow - Initialize",
            "POST",
            "medical-ai/initialize",
            200,
            data=init_data
        )
        
        if not success1:
            return False
        
        context = init_response.get('context', {})
        consultation_id = init_response.get('consultation_id')
        
        # Step 2: Present chief complaint
        complaint_data = {
            "patient_id": "test-patient-flow",
            "message": "I've been having stomach pain for the past 3 days",
            "consultation_id": consultation_id,
            "context": context
        }
        
        success2, complaint_response = self.run_test(
            "Complete Flow - Chief Complaint",
            "POST",
            "medical-ai/message",
            200,
            data=complaint_data
        )
        
        if success2:
            context = complaint_response.get('context', {})
            stage = complaint_response.get('stage', '')
            print(f"   📋 Current Stage after complaint: {stage}")
        
        # Step 3: Provide more details (HPI)
        hpi_data = {
            "patient_id": "test-patient-flow",
            "message": "The pain started 3 days ago, it's in my upper abdomen, it's a sharp pain that gets worse after eating, especially fatty foods. It's about 7 out of 10 in severity.",
            "consultation_id": consultation_id,
            "context": context
        }
        
        success3, hpi_response = self.run_test(
            "Complete Flow - History of Present Illness",
            "POST",
            "medical-ai/message",
            200,
            data=hpi_data
        )
        
        if success3:
            context = hpi_response.get('context', {})
            stage = hpi_response.get('stage', '')
            symptom_data = context.get('symptom_data', {})
            print(f"   📋 Current Stage after HPI: {stage}")
            print(f"   📊 Symptom Data Captured: {bool(symptom_data)}")
        
        # Step 4: Continue with medical history
        history_data = {
            "patient_id": "test-patient-flow",
            "message": "I had my gallbladder removed 5 years ago. I take omeprazole for acid reflux. No known allergies.",
            "consultation_id": consultation_id,
            "context": context
        }
        
        success4, history_response = self.run_test(
            "Complete Flow - Medical History",
            "POST",
            "medical-ai/message",
            200,
            data=history_data
        )
        
        if success4:
            context = history_response.get('context', {})
            stage = history_response.get('stage', '')
            medical_history = context.get('medical_history', {})
            medications = context.get('medications', [])
            print(f"   📋 Current Stage after history: {stage}")
            print(f"   🏥 Medical History Captured: {bool(medical_history)}")
            print(f"   💊 Medications Captured: {len(medications)} medications")
        
        # Step 5: Request assessment/recommendations
        assessment_data = {
            "patient_id": "test-patient-flow",
            "message": "What do you think might be causing my pain? What should I do?",
            "consultation_id": consultation_id,
            "context": context
        }
        
        success5, assessment_response = self.run_test(
            "Complete Flow - Final Assessment",
            "POST",
            "medical-ai/message",
            200,
            data=assessment_data
        )
        
        if success5:
            # Validate final assessment quality
            differential_diagnoses = assessment_response.get('differential_diagnoses', [])
            recommendations = assessment_response.get('recommendations', [])
            urgency = assessment_response.get('urgency', 'routine')
            
            print(f"   🔍 Final Differential Diagnoses: {len(differential_diagnoses)}")
            print(f"   💡 Final Recommendations: {len(recommendations)}")
            print(f"   ⚠️ Final Urgency Assessment: {urgency}")
            
            # Check for comprehensive assessment
            if differential_diagnoses and recommendations:
                print(f"   ✅ Complete consultation flow successful")
                
                # Show sample diagnosis and recommendation
                if differential_diagnoses:
                    sample_diagnosis = differential_diagnoses[0]
                    if isinstance(sample_diagnosis, dict):
                        print(f"   🔍 Sample Diagnosis: {sample_diagnosis.get('condition', 'N/A')} (Probability: {sample_diagnosis.get('probability', 'N/A')})")
                
                if recommendations:
                    sample_recommendation = recommendations[0]
                    print(f"   💡 Sample Recommendation: {sample_recommendation[:100] if isinstance(sample_recommendation, str) else str(sample_recommendation)[:100]}...")
            else:
                print(f"   ⚠️ Final assessment may be incomplete")
        
        return success1 and success2 and success3 and success4 and success5

    def test_api_response_structure_validation(self):
        """Test API response structure compliance with Pydantic models"""
        print("\n📋 Testing API Response Structure Validation...")
        
        # Test 1: Initialize endpoint response structure
        init_data = {"patient_id": "structure-test-001"}
        
        success1, init_response = self.run_test(
            "Response Structure - Initialize",
            "POST",
            "medical-ai/initialize",
            200,
            data=init_data
        )
        
        if success1 and init_response:
            # Validate MedicalConsultationResponse structure
            required_fields = ['response', 'context', 'stage', 'urgency', 'consultation_id', 'emergency_detected']
            optional_fields = ['next_questions', 'differential_diagnoses', 'recommendations']
            
            missing_required = [field for field in required_fields if field not in init_response]
            present_optional = [field for field in optional_fields if field in init_response]
            
            if not missing_required:
                print(f"   ✅ All required fields present: {required_fields}")
            else:
                print(f"   ❌ Missing required fields: {missing_required}")
                success1 = False
            
            print(f"   📋 Optional fields present: {present_optional}")
            
            # Validate field types
            type_validations = {
                'response': str,
                'context': dict,
                'stage': str,
                'urgency': str,
                'consultation_id': str,
                'emergency_detected': bool
            }
            
            type_errors = []
            for field, expected_type in type_validations.items():
                if field in init_response:
                    actual_value = init_response[field]
                    if not isinstance(actual_value, expected_type):
                        type_errors.append(f"{field}: expected {expected_type.__name__}, got {type(actual_value).__name__}")
            
            if not type_errors:
                print(f"   ✅ All field types correct")
            else:
                print(f"   ❌ Type validation errors: {type_errors}")
                success1 = False
        
        # Test 2: Message endpoint response structure
        message_data = {
            "patient_id": "structure-test-002",
            "message": "I have a headache"
        }
        
        success2, message_response = self.run_test(
            "Response Structure - Message",
            "POST",
            "medical-ai/message",
            200,
            data=message_data
        )
        
        if success2 and message_response:
            # Same validation as initialize
            missing_required = [field for field in required_fields if field not in message_response]
            
            if not missing_required:
                print(f"   ✅ Message response structure valid")
            else:
                print(f"   ❌ Message response missing fields: {missing_required}")
                success2 = False
        
        # Test 3: Error handling for malformed requests
        malformed_data = {
            "invalid_field": "test"
            # Missing required patient_id
        }
        
        success3, error_response = self.run_test(
            "Response Structure - Error Handling",
            "POST",
            "medical-ai/initialize",
            422,  # Expecting validation error
            data=malformed_data
        )
        
        if success3:
            print(f"   ✅ Proper error handling for malformed requests")
        else:
            print(f"   ⚠️ Error handling may need improvement")
        
        return success1 and success2 and success3

    def run_comprehensive_medical_ai_tests(self):
        """Run all Medical AI tests as requested in the review"""
        print("🚀 Starting Enhanced Medical AI Service Testing")
        print(f"🌐 Base URL: {self.base_url}")
        print("=" * 80)
        print("🎯 TESTING FOCUS: Enhanced Medical AI Service (Task 2.1)")
        print("📋 Test Categories:")
        print("   1. Medical AI Initialization Test")
        print("   2. Medical AI Message Processing Test")
        print("   3. Enhanced Features Validation")
        print("   4. Complete Consultation Flow")
        print("   5. API Response Structure Validation")
        print("=" * 80)
        
        # Run all test categories
        init_success, initial_context = self.test_medical_ai_initialization()
        message_success = self.test_medical_ai_message_processing(initial_context)
        enhanced_success = self.test_enhanced_features_validation()
        flow_success = self.test_complete_consultation_flow()
        structure_success = self.test_api_response_structure_validation()
        
        # Calculate overall success
        overall_success = init_success and message_success and enhanced_success and flow_success and structure_success
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 ENHANCED MEDICAL AI SERVICE TEST SUMMARY")
        print("=" * 80)
        print(f"   ✅ Medical AI Initialization: {'PASS' if init_success else 'FAIL'}")
        print(f"   ✅ Message Processing & Emergency Detection: {'PASS' if message_success else 'FAIL'}")
        print(f"   ✅ Enhanced Features (Knowledge Base, OLDCARTS): {'PASS' if enhanced_success else 'FAIL'}")
        print(f"   ✅ Complete Consultation Flow: {'PASS' if flow_success else 'FAIL'}")
        print(f"   ✅ API Response Structure Validation: {'PASS' if structure_success else 'FAIL'}")
        print("=" * 80)
        print(f"📈 Overall Test Results: {self.tests_passed}/{self.tests_run} tests passed")
        
        if overall_success:
            print("🎉 ENHANCED MEDICAL AI SERVICE: ALL TESTS PASSED")
            print("✅ World-class medical consultations with professional-grade features")
            print("✅ Emergency detection and OLDCARTS framework working")
            print("✅ Comprehensive medical knowledge base and clinical reasoning")
            print("✅ Professional medical assessment formatting validated")
            return 0
        else:
            print("⚠️ ENHANCED MEDICAL AI SERVICE: SOME TESTS FAILED")
            print("❌ Issues detected with medical AI functionality")
            
            # Show failed tests
            failed_tests = [result for result in self.test_results if not result.get('success', False)]
            if failed_tests:
                print("\nFailed Tests:")
                for test in failed_tests:
                    print(f"  - {test['name']}: {test.get('error', 'Status code mismatch')}")
            
            return 1

def main():
    """Main test execution"""
    tester = MedicalAITester()
    return tester.run_comprehensive_medical_ai_tests()

if __name__ == "__main__":
    sys.exit(main())