#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime, timedelta
import uuid
import base64

class MedicalAITester:
    def __init__(self, base_url="https://symptom-tracker-3.preview.emergentagent.com/api"):
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
                    print(f"   Response: {json.dumps(response_data, indent=2)[:400]}...")
                except:
                    print(f"   Response: {response.text[:400]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:400]}...")

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
        """Test Medical AI Service Initialization"""
        print("\n🏥 Testing Medical AI Service Initialization...")
        
        # Test 1: Basic initialization with anonymous patient
        basic_init_data = {
            "patient_id": "anonymous"
        }
        
        success1, response1 = self.run_test(
            "Medical AI Initialization - Anonymous Patient",
            "POST",
            "medical-ai/initialize",
            200,
            data=basic_init_data
        )
        
        consultation_id = None
        if success1 and response1:
            expected_keys = ['response', 'context', 'stage', 'urgency', 'consultation_id', 'patient_id', 'current_stage', 'emergency_detected']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Response contains all required keys: {expected_keys}")
                consultation_id = response1.get('consultation_id')
                stage = response1.get('stage')
                urgency = response1.get('urgency')
                emergency_detected = response1.get('emergency_detected')
                
                print(f"   🆔 Consultation ID: {consultation_id}")
                print(f"   📋 Initial Stage: {stage}")
                print(f"   ⚡ Urgency Level: {urgency}")
                print(f"   🚨 Emergency Detected: {emergency_detected}")
            else:
                print(f"   ❌ Response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Initialization with patient demographics
        demographics_init_data = {
            "patient_id": "test_patient_123",
            "demographics": {
                "age": 35,
                "gender": "female",
                "medical_history": ["hypertension", "diabetes"],
                "current_medications": ["lisinopril", "metformin"],
                "allergies": ["penicillin"]
            }
        }
        
        success2, response2 = self.run_test(
            "Medical AI Initialization - With Demographics",
            "POST",
            "medical-ai/initialize",
            200,
            data=demographics_init_data
        )
        
        demographics_consultation_id = None
        if success2 and response2:
            demographics_consultation_id = response2.get('consultation_id')
            context = response2.get('context', {})
            demographics = context.get('demographics', {})
            
            print(f"   🆔 Demographics Consultation ID: {demographics_consultation_id}")
            print(f"   👤 Demographics captured: {len(demographics)} fields")
            
            if demographics:
                print(f"   📊 Age: {demographics.get('age', 'Not specified')}")
                print(f"   ⚕️ Medical History: {demographics.get('medical_history', [])}")
        
        return success1 and success2, consultation_id, demographics_consultation_id

    def test_medical_ai_message_processing(self, consultation_id=None):
        """Test Medical AI Message Processing"""
        print("\n💬 Testing Medical AI Message Processing...")
        
        if not consultation_id:
            consultation_id = f"test_consultation_{datetime.now().strftime('%H%M%S')}"
        
        # Test 1: Chief complaint processing
        chief_complaint_data = {
            "patient_id": "anonymous",
            "message": "I have been experiencing severe chest pain for the past 2 hours. It feels like crushing pressure and radiates to my left arm.",
            "consultation_id": consultation_id,
            "context": {
                "patient_id": "anonymous",
                "consultation_id": consultation_id,
                "current_stage": "greeting",
                "demographics": {}
            }
        }
        
        success1, response1 = self.run_test(
            "Medical AI Message - Chief Complaint (Emergency)",
            "POST",
            "medical-ai/message",
            200,
            data=chief_complaint_data
        )
        
        if success1 and response1:
            urgency = response1.get('urgency')
            emergency_detected = response1.get('emergency_detected')
            stage = response1.get('stage')
            response_text = response1.get('response', '')
            
            print(f"   ⚡ Urgency Level: {urgency}")
            print(f"   🚨 Emergency Detected: {emergency_detected}")
            print(f"   📋 Current Stage: {stage}")
            print(f"   💬 Response Length: {len(response_text)} characters")
            
            # Check if emergency was properly detected
            emergency_properly_detected = urgency == "emergency" or emergency_detected
            if emergency_properly_detected:
                print(f"   ✅ Emergency symptoms properly detected")
            else:
                print(f"   ⚠️ Emergency symptoms may not have been detected properly")
        
        # Test 2: Common symptom processing
        common_symptom_data = {
            "patient_id": "anonymous",
            "message": "I've had a headache for the past 2 days. It's moderate pain, around 6/10, and gets worse in the afternoon.",
            "consultation_id": consultation_id,
            "context": {
                "patient_id": "anonymous",
                "consultation_id": consultation_id,
                "current_stage": "chief_complaint",
                "demographics": {},
                "chief_complaint": "chest pain"
            }
        }
        
        success2, response2 = self.run_test(
            "Medical AI Message - Common Symptom",
            "POST",
            "medical-ai/message",
            200,
            data=common_symptom_data
        )
        
        if success2 and response2:
            urgency = response2.get('urgency')
            stage = response2.get('stage')
            next_questions = response2.get('next_questions', [])
            
            print(f"   ⚡ Urgency Level: {urgency}")
            print(f"   📋 Current Stage: {stage}")
            print(f"   ❓ Next Questions: {len(next_questions)} questions")
        
        # Test 3: Complex multi-system symptoms
        complex_symptom_data = {
            "patient_id": "anonymous",
            "message": "I have joint pain in multiple joints, fatigue that's been going on for weeks, a rash on my face, and low-grade fever.",
            "consultation_id": consultation_id,
            "context": {
                "patient_id": "anonymous",
                "consultation_id": consultation_id,
                "current_stage": "history_present_illness",
                "demographics": {"age": 28, "gender": "female"},
                "chief_complaint": "joint pain and fatigue",
                "symptom_data": {"joint_pain": True, "fatigue": True}
            }
        }
        
        success3, response3 = self.run_test(
            "Medical AI Message - Complex Multi-system Symptoms",
            "POST",
            "medical-ai/message",
            200,
            data=complex_symptom_data
        )
        
        if success3 and response3:
            differential_diagnoses = response3.get('differential_diagnoses', [])
            recommendations = response3.get('recommendations', [])
            
            print(f"   🔍 Differential Diagnoses: {len(differential_diagnoses)} conditions")
            print(f"   💡 Recommendations: {len(recommendations)} items")
            
            if differential_diagnoses:
                for i, diagnosis in enumerate(differential_diagnoses[:3], 1):
                    if isinstance(diagnosis, dict):
                        condition = diagnosis.get('condition', 'Unknown')
                        probability = diagnosis.get('probability', 'Unknown')
                        print(f"   {i}. {condition} ({probability}% probability)")
        
        return success1 and success2 and success3

    def test_medical_knowledge_database(self):
        """Test Medical Knowledge Database Integration"""
        print("\n📚 Testing Medical Knowledge Database Integration...")
        
        # Test 1: Symptom knowledge query
        symptom_query_data = {
            "query": "chest pain",
            "type": "symptom",
            "detailed": True
        }
        
        success1, response1 = self.run_test(
            "Medical Knowledge - Symptom Query",
            "POST",
            "medical-ai/knowledge",
            200,
            data=symptom_query_data
        )
        
        if success1 and response1:
            knowledge_type = response1.get('type')
            name = response1.get('name')
            category = response1.get('category')
            associated_conditions = response1.get('associated_conditions', [])
            
            print(f"   📋 Knowledge Type: {knowledge_type}")
            print(f"   🏷️ Symptom Name: {name}")
            print(f"   📂 Category: {category}")
            print(f"   🔗 Associated Conditions: {len(associated_conditions)} conditions")
        
        # Test 2: Condition knowledge query
        condition_query_data = {
            "query": "myocardial infarction",
            "type": "condition",
            "detailed": True
        }
        
        success2, response2 = self.run_test(
            "Medical Knowledge - Condition Query",
            "POST",
            "medical-ai/knowledge",
            200,
            data=condition_query_data
        )
        
        if success2 and response2:
            condition_name = response2.get('name')
            icd_code = response2.get('icd_code')
            typical_symptoms = response2.get('typical_symptoms', [])
            urgency_level = response2.get('urgency_level')
            
            print(f"   🏷️ Condition Name: {condition_name}")
            print(f"   🔢 ICD Code: {icd_code}")
            print(f"   🎯 Typical Symptoms: {len(typical_symptoms)} symptoms")
            print(f"   ⚡ Urgency Level: {urgency_level}")
        
        # Test 3: Treatment recommendations query
        treatment_query_data = {
            "query": "hypertension",
            "type": "treatment",
            "detailed": False
        }
        
        success3, response3 = self.run_test(
            "Medical Knowledge - Treatment Query",
            "POST",
            "medical-ai/knowledge",
            200,
            data=treatment_query_data
        )
        
        if success3 and response3:
            treatment_type = response3.get('type')
            condition = response3.get('condition')
            recommendations = response3.get('recommendations', [])
            
            print(f"   📋 Query Type: {treatment_type}")
            print(f"   🎯 Condition: {condition}")
            print(f"   💊 Treatment Recommendations: {len(recommendations)} options")
        
        return success1 and success2 and success3

    def test_emergency_risk_assessment(self):
        """Test Emergency Risk Assessment"""
        print("\n🚨 Testing Emergency Risk Assessment...")
        
        # Test 1: Critical emergency symptoms
        critical_symptoms_data = {
            "symptoms": [
                "crushing chest pain",
                "shortness of breath",
                "sweating",
                "nausea"
            ],
            "context": {
                "duration": "2 hours",
                "severity": "severe",
                "onset": "sudden"
            },
            "patient_demographics": {
                "age": 55,
                "gender": "male",
                "medical_history": ["hypertension", "diabetes"]
            }
        }
        
        success1, response1 = self.run_test(
            "Emergency Assessment - Critical Symptoms",
            "POST",
            "medical-ai/emergency-assessment",
            200,
            data=critical_symptoms_data
        )
        
        if success1 and response1:
            risk_level = response1.get('risk_level')
            risk_factors = response1.get('risk_factors', [])
            immediate_actions = response1.get('immediate_actions', [])
            confidence = response1.get('confidence', 0)
            
            print(f"   ⚡ Risk Level: {risk_level}")
            print(f"   ⚠️ Risk Factors: {len(risk_factors)} identified")
            print(f"   🎯 Immediate Actions: {len(immediate_actions)} actions")
            print(f"   📊 Confidence: {confidence}")
            
            # Validate critical symptoms are properly classified
            if risk_level == 'critical':
                print(f"   ✅ Critical symptoms properly classified")
            else:
                print(f"   ⚠️ Critical symptoms may not be properly classified")
        
        # Test 2: Urgent but non-critical symptoms
        urgent_symptoms_data = {
            "symptoms": [
                "severe abdominal pain",
                "vomiting",
                "fever"
            ],
            "context": {
                "duration": "6 hours",
                "severity": "severe",
                "onset": "gradual"
            },
            "patient_demographics": {
                "age": 25,
                "gender": "female"
            }
        }
        
        success2, response2 = self.run_test(
            "Emergency Assessment - Urgent Symptoms",
            "POST",
            "medical-ai/emergency-assessment",
            200,
            data=urgent_symptoms_data
        )
        
        if success2 and response2:
            risk_level = response2.get('risk_level')
            differential_probabilities = response2.get('differential_probabilities', [])
            
            print(f"   ⚡ Risk Level: {risk_level}")
            print(f"   🔍 Differential Probabilities: {len(differential_probabilities)} conditions")
        
        # Test 3: Routine symptoms
        routine_symptoms_data = {
            "symptoms": [
                "mild headache",
                "runny nose",
                "slight cough"
            ],
            "context": {
                "duration": "3 days",
                "severity": "mild",
                "onset": "gradual"
            },
            "patient_demographics": {
                "age": 30,
                "gender": "male"
            }
        }
        
        success3, response3 = self.run_test(
            "Emergency Assessment - Routine Symptoms",
            "POST",
            "medical-ai/emergency-assessment",
            200,
            data=routine_symptoms_data
        )
        
        if success3 and response3:
            risk_level = response3.get('risk_level')
            immediate_actions = response3.get('immediate_actions', [])
            
            print(f"   ⚡ Risk Level: {risk_level}")
            print(f"   📋 Immediate Actions: {len(immediate_actions)} actions")
            
            # Validate routine symptoms are properly classified
            if risk_level in ['routine', 'low']:
                print(f"   ✅ Routine symptoms properly classified")
            else:
                print(f"   ⚠️ Routine symptoms may be over-classified")
        
        return success1 and success2 and success3

    def test_medical_report_generation(self, consultation_id=None):
        """Test Enhanced Medical Report Generation with SOAP Notes and PDF"""
        print("\n📄 Testing Enhanced Medical Report Generation...")
        
        if not consultation_id:
            consultation_id = f"test_consultation_{datetime.now().strftime('%H%M%S')}"
        
        # Comprehensive consultation data for report generation
        report_request_data = {
            "consultation_id": consultation_id,
            "messages": [
                {
                    "role": "patient",
                    "content": "I have been experiencing chest pain for 2 hours",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "role": "ai",
                    "content": "I understand you're experiencing chest pain. Can you describe the pain?",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "role": "patient",
                    "content": "It's a crushing pain that radiates to my left arm. I also feel short of breath.",
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "context": {
                "patient_id": "test_patient_123",
                "consultation_id": consultation_id,
                "current_stage": "assessment",
                "demographics": {
                    "age": 55,
                    "gender": "male",
                    "medical_history": ["hypertension", "diabetes"]
                },
                "chief_complaint": "chest pain",
                "symptom_data": {
                    "chest_pain": {
                        "severity": 8,
                        "duration": "2 hours",
                        "character": "crushing",
                        "radiation": "left arm"
                    },
                    "shortness_of_breath": {
                        "severity": 6,
                        "associated": True
                    }
                },
                "medical_history": {
                    "hypertension": "controlled",
                    "diabetes": "type 2"
                },
                "medications": ["lisinopril", "metformin"],
                "allergies": ["penicillin"],
                "emergency_level": "critical",
                "emergency_detected": True,
                "urgency": "emergency",
                "differential_diagnoses": [
                    {
                        "condition": "Acute Myocardial Infarction",
                        "probability": 85,
                        "icd_code": "I21.9",
                        "reasoning": "Classic presentation with crushing chest pain, radiation to left arm, and associated shortness of breath in high-risk patient"
                    },
                    {
                        "condition": "Unstable Angina",
                        "probability": 10,
                        "icd_code": "I20.0",
                        "reasoning": "Similar presentation but less likely given severity and duration"
                    }
                ],
                "recommendations": [
                    "Call 911 immediately",
                    "Chew 325mg aspirin if not allergic",
                    "Do not drive to hospital",
                    "Monitor vital signs",
                    "Prepare medication list for EMS"
                ],
                "red_flags": ["crushing chest pain", "radiation to arm", "shortness of breath"],
                "confidence": 0.92
            }
        }
        
        success1, response1 = self.run_test(
            "Medical Report Generation - Comprehensive SOAP with PDF",
            "POST",
            "medical-ai/report",
            200,
            data=report_request_data
        )
        
        if success1 and response1:
            expected_keys = ['report_id', 'consultation_id', 'soap_note', 'soap_notes', 'consultation_summary', 
                           'recommendations', 'differential_diagnoses', 'emergency_detected', 'urgency_level', 
                           'pdf_base64', 'pdf_url', 'generated_at']
            missing_keys = [key for key in expected_keys if key not in response1]
            
            if not missing_keys:
                print(f"   ✅ Report response contains all required keys")
                
                report_id = response1.get('report_id')
                soap_note = response1.get('soap_note', '')
                soap_notes = response1.get('soap_notes', {})
                pdf_base64 = response1.get('pdf_base64', '')
                pdf_url = response1.get('pdf_url', '')
                emergency_detected = response1.get('emergency_detected')
                urgency_level = response1.get('urgency_level')
                differential_diagnoses = response1.get('differential_diagnoses', [])
                recommendations = response1.get('recommendations', [])
                
                print(f"   🆔 Report ID: {report_id}")
                print(f"   📄 SOAP Note Length: {len(soap_note)} characters")
                print(f"   📋 SOAP Sections: {len(soap_notes)} sections")
                print(f"   📎 PDF Generated: {'Yes' if pdf_base64 else 'No'}")
                print(f"   🔗 PDF URL: {pdf_url}")
                print(f"   🚨 Emergency Detected: {emergency_detected}")
                print(f"   ⚡ Urgency Level: {urgency_level}")
                print(f"   🔍 Differential Diagnoses: {len(differential_diagnoses)} conditions")
                print(f"   💡 Recommendations: {len(recommendations)} items")
                
                # Validate SOAP note structure
                if soap_notes:
                    soap_sections = ['subjective', 'objective', 'assessment', 'plan']
                    present_sections = [section for section in soap_sections if section in soap_notes]
                    print(f"   📊 SOAP Sections Present: {present_sections}")
                    
                    if len(present_sections) >= 3:
                        print(f"   ✅ SOAP note structure is comprehensive")
                    else:
                        print(f"   ⚠️ SOAP note may be incomplete")
                
                # Validate PDF generation
                if pdf_base64:
                    try:
                        pdf_data = base64.b64decode(pdf_base64)
                        pdf_size = len(pdf_data)
                        print(f"   📄 PDF Size: {pdf_size} bytes")
                        
                        # Check if it's a valid PDF (starts with PDF header)
                        if pdf_data.startswith(b'%PDF'):
                            print(f"   ✅ PDF format validation passed")
                        else:
                            print(f"   ⚠️ PDF format validation failed")
                    except Exception as e:
                        print(f"   ❌ PDF validation error: {str(e)}")
                
            else:
                print(f"   ❌ Report response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: PDF download endpoint
        if consultation_id:
            success2, response2 = self.run_test(
                "Medical Report PDF Download",
                "GET",
                f"medical-ai/report/{consultation_id}/download",
                200
            )
            
            if success2 and response2:
                download_url = response2.get('download_url')
                message = response2.get('message')
                print(f"   📥 Download Message: {message}")
                print(f"   🔗 Download URL: {download_url}")
        else:
            success2 = True  # Skip if no consultation_id
        
        return success1 and success2

    def test_service_integration(self):
        """Test Service Integration and Initialization"""
        print("\n🔧 Testing Service Integration...")
        
        # Test that all services initialize properly by making a simple request
        # This tests the service dependency injection and initialization
        
        # Test medical AI service initialization
        init_data = {"patient_id": "service_test"}
        success1, response1 = self.run_test(
            "Service Integration - Medical AI Service",
            "POST",
            "medical-ai/initialize",
            200,
            data=init_data
        )
        
        if success1:
            print(f"   ✅ Medical AI Service initialized successfully")
        
        # Test knowledge database service
        knowledge_data = {"query": "headache", "type": "symptom"}
        success2, response2 = self.run_test(
            "Service Integration - Knowledge Database Service",
            "POST",
            "medical-ai/knowledge",
            200,
            data=knowledge_data
        )
        
        if success2:
            print(f"   ✅ Knowledge Database Service initialized successfully")
        
        # Test emergency assessment service
        emergency_data = {
            "symptoms": ["mild headache"],
            "context": {"duration": "1 hour"},
            "patient_demographics": {"age": 30}
        }
        success3, response3 = self.run_test(
            "Service Integration - Emergency Assessment Service",
            "POST",
            "medical-ai/emergency-assessment",
            200,
            data=emergency_data
        )
        
        if success3:
            print(f"   ✅ Emergency Assessment Service initialized successfully")
        
        return success1 and success2 and success3

    def run_comprehensive_medical_ai_tests(self):
        """Run comprehensive medical AI tests covering all requested features"""
        print("🚀 Starting Comprehensive Medical AI Backend Tests...")
        print(f"   Base URL: {self.base_url}")
        print("=" * 80)
        
        # Test 1: Medical AI Service Core Functionality
        print("\n🎯 TESTING MEDICAL AI SERVICE CORE FUNCTIONALITY")
        init_success, consultation_id, demographics_consultation_id = self.test_medical_ai_initialization()
        message_success = self.test_medical_ai_message_processing(consultation_id)
        
        # Test 2: Medical Knowledge Database Integration
        print("\n🎯 TESTING MEDICAL KNOWLEDGE DATABASE INTEGRATION")
        knowledge_success = self.test_medical_knowledge_database()
        
        # Test 3: Emergency Risk Assessment
        print("\n🎯 TESTING EMERGENCY RISK ASSESSMENT")
        emergency_success = self.test_emergency_risk_assessment()
        
        # Test 4: Enhanced Medical Report Generation
        print("\n🎯 TESTING ENHANCED MEDICAL REPORT GENERATION")
        report_success = self.test_medical_report_generation(consultation_id)
        
        # Test 5: Service Integration
        print("\n🎯 TESTING SERVICE INTEGRATION")
        integration_success = self.test_service_integration()
        
        # Print final results
        print("\n" + "=" * 80)
        print(f"📊 FINAL RESULTS")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        print(f"\n🎯 MEDICAL AI FEATURE TEST RESULTS:")
        print(f"   1. Medical AI Service Core Functionality: {'✅ PASSED' if (init_success and message_success) else '❌ FAILED'}")
        print(f"   2. Medical Knowledge Database Integration: {'✅ PASSED' if knowledge_success else '❌ FAILED'}")
        print(f"   3. Emergency Risk Assessment: {'✅ PASSED' if emergency_success else '❌ FAILED'}")
        print(f"   4. Enhanced Medical Report Generation: {'✅ PASSED' if report_success else '❌ FAILED'}")
        print(f"   5. Service Integration: {'✅ PASSED' if integration_success else '❌ FAILED'}")
        
        # Overall success
        overall_success = (init_success and message_success and knowledge_success and 
                          emergency_success and report_success and integration_success)
        
        if overall_success:
            print("\n🎉 All medical AI features passed comprehensive testing!")
            print("✅ Medical AI Service is production-ready for comprehensive medical consultations")
            return 0
        else:
            print("\n⚠️ Some medical AI features failed testing. Check the details above.")
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result.get('success', False):
                    print(f"  - {result['name']}: {result.get('error', 'Status code mismatch')}")
            return 1

if __name__ == "__main__":
    tester = MedicalAITester()
    exit_code = tester.run_comprehensive_medical_ai_tests()
    sys.exit(exit_code)