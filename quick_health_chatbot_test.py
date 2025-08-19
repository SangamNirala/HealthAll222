#!/usr/bin/env python3
"""
🩺 QUICK HEALTH TRACKING CHATBOT BACKEND TESTING SUITE 🩺

Comprehensive backend testing for the Quick Health Tracking chatbot functionality
specifically focusing on the recently fixed technical issue with symptom processing.

TESTING OBJECTIVES:
✅ TEST POST /api/medical-ai/initialize endpoint for consultation initialization
✅ TEST POST /api/medical-ai/message endpoint with "I have a headache" symptom
✅ TEST conversation flow: initialize -> send "hi" -> send "I have a headache"
✅ VERIFY no "I apologize, but I'm experiencing a technical issue" error message
✅ CONFIRM proper medical responses are generated for symptom processing
✅ TEST additional symptoms like "chest pain", "stomach ache" to ensure broad fix

Author: Testing Agent
Date: 2025-01-17
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, Any, List

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://medimpl-verify.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class QuickHealthChatbotTester:
    """Comprehensive tester for Quick Health Tracking Chatbot Backend"""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.consultation_id = None
        
    def log_test(self, test_name: str, passed: bool, details: str = "", response_data: Dict = None):
        """Log test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            self.failed_tests += 1
            status = "❌ FAIL"
            
        result = {
            "test_name": test_name,
            "status": status,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        
        self.test_results.append(result)
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        if not passed and response_data:
            print(f"   Response: {json.dumps(response_data, indent=2)[:500]}...")
        print()

    def test_consultation_initialization(self) -> bool:
        """
        🚀 TEST CONSULTATION INITIALIZATION
        
        Test POST /api/medical-ai/initialize endpoint to ensure consultation initialization works
        """
        print("\n🚀 TESTING CONSULTATION INITIALIZATION")
        print("-" * 50)
        
        try:
            response = requests.post(f"{API_BASE}/medical-ai/initialize",
                json={
                    "patient_id": "anonymous",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                required_fields = ["consultation_id", "patient_id", "current_stage", "response"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    self.consultation_id = data.get("consultation_id")
                    response_text = data.get("response", "")
                    
                    # Check that response is not an error message
                    error_indicators = [
                        "I apologize, but I'm experiencing a technical issue",
                        "technical error",
                        "system error",
                        "AnatomicalEntity",
                        "missing 1 required positional argument"
                    ]
                    
                    has_error = any(error in response_text for error in error_indicators)
                    
                    if not has_error and len(response_text) > 10:
                        self.log_test("Consultation Initialization", True,
                                    f"Consultation ID: {self.consultation_id}, Stage: {data.get('current_stage')}")
                        return True
                    else:
                        self.log_test("Consultation Initialization", False,
                                    f"Error detected in response: {response_text[:200]}...")
                        return False
                else:
                    self.log_test("Consultation Initialization", False,
                                f"Missing required fields: {missing_fields}")
                    return False
            else:
                self.log_test("Consultation Initialization", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Consultation Initialization", False, f"Exception: {str(e)}")
            return False

    def test_basic_greeting_message(self) -> bool:
        """
        👋 TEST BASIC GREETING MESSAGE
        
        Test sending "hi" message to verify basic conversation flow
        """
        print("\n👋 TESTING BASIC GREETING MESSAGE")
        print("-" * 50)
        
        if not self.consultation_id:
            self.log_test("Basic Greeting Message", False, "No consultation ID available")
            return False
        
        try:
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": self.consultation_id,
                    "message": "hi",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "")
                
                # Check that response is not an error message
                error_indicators = [
                    "I apologize, but I'm experiencing a technical issue",
                    "technical error",
                    "system error",
                    "AnatomicalEntity",
                    "missing 1 required positional argument"
                ]
                
                has_error = any(error in response_text for error in error_indicators)
                
                if not has_error and len(response_text) > 10:
                    self.log_test("Basic Greeting Message", True,
                                f"Response received: {response_text[:100]}...")
                    return True
                else:
                    self.log_test("Basic Greeting Message", False,
                                f"Error detected in response: {response_text[:200]}...")
                    return False
            else:
                self.log_test("Basic Greeting Message", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Basic Greeting Message", False, f"Exception: {str(e)}")
            return False

    def test_headache_symptom_processing(self) -> bool:
        """
        🤕 TEST HEADACHE SYMPTOM PROCESSING
        
        Test the specific symptom "I have a headache" that was previously causing the AnatomicalEntity error
        """
        print("\n🤕 TESTING HEADACHE SYMPTOM PROCESSING")
        print("-" * 50)
        
        if not self.consultation_id:
            self.log_test("Headache Symptom Processing", False, "No consultation ID available")
            return False
        
        try:
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": self.consultation_id,
                    "message": "I have a headache",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "")
                
                # Check that response is not an error message
                error_indicators = [
                    "I apologize, but I'm experiencing a technical issue",
                    "technical error",
                    "system error",
                    "AnatomicalEntity",
                    "missing 1 required positional argument",
                    "specificity_level"
                ]
                
                has_error = any(error in response_text for error in error_indicators)
                
                # Check for medical response indicators
                medical_indicators = [
                    "headache",
                    "pain",
                    "symptom",
                    "medical",
                    "doctor",
                    "treatment",
                    "medication",
                    "when did",
                    "how long",
                    "severity",
                    "location"
                ]
                
                has_medical_content = any(indicator in response_text.lower() for indicator in medical_indicators)
                
                if not has_error and has_medical_content and len(response_text) > 20:
                    self.log_test("Headache Symptom Processing", True,
                                f"Medical response generated: {response_text[:150]}...")
                    return True
                else:
                    self.log_test("Headache Symptom Processing", False,
                                f"Error or non-medical response: {response_text[:200]}...")
                    return False
            else:
                self.log_test("Headache Symptom Processing", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Headache Symptom Processing", False, f"Exception: {str(e)}")
            return False

    def test_additional_symptoms(self) -> bool:
        """
        🩺 TEST ADDITIONAL SYMPTOMS
        
        Test additional symptoms like "chest pain", "stomach ache" to ensure the fix works broadly
        """
        print("\n🩺 TESTING ADDITIONAL SYMPTOMS")
        print("-" * 50)
        
        symptoms_to_test = [
            "chest pain",
            "stomach ache",
            "back pain",
            "sore throat",
            "joint pain"
        ]
        
        all_passed = True
        
        for symptom in symptoms_to_test:
            # Create new consultation for each symptom test
            try:
                init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
                    json={
                        "patient_id": "anonymous",
                        "timestamp": datetime.now().isoformat()
                    },
                    timeout=30
                )
                
                if init_response.status_code != 200:
                    self.log_test(f"Additional Symptom - {symptom} (Init)", False,
                                f"Failed to initialize consultation")
                    all_passed = False
                    continue
                
                consultation_data = init_response.json()
                temp_consultation_id = consultation_data.get("consultation_id")
                
                if not temp_consultation_id:
                    self.log_test(f"Additional Symptom - {symptom} (Init)", False,
                                f"No consultation ID received")
                    all_passed = False
                    continue
                
                # Test the symptom
                response = requests.post(f"{API_BASE}/medical-ai/message",
                    json={
                        "consultation_id": temp_consultation_id,
                        "message": f"I have {symptom}",
                        "timestamp": datetime.now().isoformat()
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "")
                    
                    # Check that response is not an error message
                    error_indicators = [
                        "I apologize, but I'm experiencing a technical issue",
                        "technical error",
                        "system error",
                        "AnatomicalEntity",
                        "missing 1 required positional argument",
                        "specificity_level"
                    ]
                    
                    has_error = any(error in response_text for error in error_indicators)
                    
                    # Check for medical response indicators
                    medical_indicators = [
                        symptom.split()[0],  # First word of symptom
                        "pain",
                        "symptom",
                        "medical",
                        "when did",
                        "how long",
                        "severity"
                    ]
                    
                    has_medical_content = any(indicator in response_text.lower() for indicator in medical_indicators)
                    
                    if not has_error and has_medical_content and len(response_text) > 20:
                        self.log_test(f"Additional Symptom - {symptom}", True,
                                    f"Medical response generated: {response_text[:100]}...")
                    else:
                        self.log_test(f"Additional Symptom - {symptom}", False,
                                    f"Error or non-medical response: {response_text[:150]}...")
                        all_passed = False
                else:
                    self.log_test(f"Additional Symptom - {symptom}", False,
                                f"HTTP {response.status_code}: {response.text}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Additional Symptom - {symptom}", False, f"Exception: {str(e)}")
                all_passed = False
        
        return all_passed

    def test_conversation_flow_integration(self) -> bool:
        """
        🔄 TEST COMPLETE CONVERSATION FLOW
        
        Test the complete conversation flow: initialize -> "hi" -> "I have a headache"
        """
        print("\n🔄 TESTING COMPLETE CONVERSATION FLOW")
        print("-" * 50)
        
        try:
            # Step 1: Initialize new consultation
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
                json={
                    "patient_id": "anonymous",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Conversation Flow - Initialize", False,
                            f"HTTP {init_response.status_code}: {init_response.text}")
                return False
            
            init_data = init_response.json()
            flow_consultation_id = init_data.get("consultation_id")
            
            if not flow_consultation_id:
                self.log_test("Conversation Flow - Initialize", False, "No consultation ID received")
                return False
            
            # Step 2: Send greeting
            greeting_response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": flow_consultation_id,
                    "message": "hi",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if greeting_response.status_code != 200:
                self.log_test("Conversation Flow - Greeting", False,
                            f"HTTP {greeting_response.status_code}: {greeting_response.text}")
                return False
            
            greeting_data = greeting_response.json()
            greeting_text = greeting_data.get("response", "")
            
            # Check greeting response
            error_indicators = [
                "I apologize, but I'm experiencing a technical issue",
                "technical error",
                "system error",
                "AnatomicalEntity"
            ]
            
            if any(error in greeting_text for error in error_indicators):
                self.log_test("Conversation Flow - Greeting", False,
                            f"Error in greeting: {greeting_text[:150]}...")
                return False
            
            # Step 3: Send headache symptom
            symptom_response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": flow_consultation_id,
                    "message": "I have a headache",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if symptom_response.status_code != 200:
                self.log_test("Conversation Flow - Symptom", False,
                            f"HTTP {symptom_response.status_code}: {symptom_response.text}")
                return False
            
            symptom_data = symptom_response.json()
            symptom_text = symptom_data.get("response", "")
            
            # Check symptom response
            has_error = any(error in symptom_text for error in error_indicators)
            
            medical_indicators = [
                "headache",
                "pain",
                "symptom",
                "when did",
                "how long",
                "severity"
            ]
            
            has_medical_content = any(indicator in symptom_text.lower() for indicator in medical_indicators)
            
            if not has_error and has_medical_content and len(symptom_text) > 20:
                self.log_test("Conversation Flow Integration", True,
                            f"Complete flow successful. Final response: {symptom_text[:100]}...")
                return True
            else:
                self.log_test("Conversation Flow Integration", False,
                            f"Error in symptom processing: {symptom_text[:150]}...")
                return False
                
        except Exception as e:
            self.log_test("Conversation Flow Integration", False, f"Exception: {str(e)}")
            return False

    def test_error_message_absence(self) -> bool:
        """
        🚫 TEST ERROR MESSAGE ABSENCE
        
        Specifically verify that the error "I apologize, but I'm experiencing a technical issue" 
        no longer appears in responses
        """
        print("\n🚫 TESTING ERROR MESSAGE ABSENCE")
        print("-" * 50)
        
        test_messages = [
            "I have a headache",
            "My chest hurts",
            "I feel dizzy",
            "I have stomach pain",
            "My back is sore"
        ]
        
        all_passed = True
        
        for message in test_messages:
            try:
                # Initialize consultation
                init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
                    json={
                        "patient_id": "anonymous",
                        "timestamp": datetime.now().isoformat()
                    },
                    timeout=30
                )
                
                if init_response.status_code != 200:
                    continue
                
                init_data = init_response.json()
                temp_consultation_id = init_data.get("consultation_id")
                
                if not temp_consultation_id:
                    continue
                
                # Send message
                response = requests.post(f"{API_BASE}/medical-ai/message",
                    json={
                        "consultation_id": temp_consultation_id,
                        "message": message,
                        "timestamp": datetime.now().isoformat()
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "")
                    
                    # Check for the specific error message
                    error_message = "I apologize, but I'm experiencing a technical issue"
                    
                    if error_message in response_text:
                        self.log_test(f"Error Message Absence - {message}", False,
                                    f"Found error message: {response_text[:150]}...")
                        all_passed = False
                    else:
                        self.log_test(f"Error Message Absence - {message}", True,
                                    f"No error message found")
                        
            except Exception as e:
                self.log_test(f"Error Message Absence - {message}", False, f"Exception: {str(e)}")
                all_passed = False
        
        return all_passed

    def run_comprehensive_tests(self):
        """Run comprehensive Quick Health Tracking chatbot tests"""
        print("🚀 Starting Quick Health Tracking Chatbot Backend Tests...")
        print(f"   Base URL: {API_BASE}")
        print("=" * 80)
        
        # Test 1: Consultation Initialization
        print("\n🎯 TESTING PHASE 1: CONSULTATION INITIALIZATION")
        init_success = self.test_consultation_initialization()
        
        # Test 2: Basic Greeting Message
        print("\n🎯 TESTING PHASE 2: BASIC GREETING MESSAGE")
        greeting_success = self.test_basic_greeting_message()
        
        # Test 3: Headache Symptom Processing (The main fix)
        print("\n🎯 TESTING PHASE 3: HEADACHE SYMPTOM PROCESSING")
        headache_success = self.test_headache_symptom_processing()
        
        # Test 4: Additional Symptoms
        print("\n🎯 TESTING PHASE 4: ADDITIONAL SYMPTOMS")
        additional_success = self.test_additional_symptoms()
        
        # Test 5: Complete Conversation Flow
        print("\n🎯 TESTING PHASE 5: CONVERSATION FLOW INTEGRATION")
        flow_success = self.test_conversation_flow_integration()
        
        # Test 6: Error Message Absence
        print("\n🎯 TESTING PHASE 6: ERROR MESSAGE ABSENCE")
        error_absence_success = self.test_error_message_absence()
        
        # Print final results
        print("\n" + "=" * 80)
        print(f"📊 FINAL RESULTS")
        print(f"Tests Run: {self.total_tests}")
        print(f"Tests Passed: {self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        print(f"\n🎯 QUICK HEALTH TRACKING CHATBOT TEST RESULTS:")
        print(f"   1. Consultation Initialization: {'✅ PASSED' if init_success else '❌ FAILED'}")
        print(f"   2. Basic Greeting Message: {'✅ PASSED' if greeting_success else '❌ FAILED'}")
        print(f"   3. Headache Symptom Processing: {'✅ PASSED' if headache_success else '❌ FAILED'}")
        print(f"   4. Additional Symptoms: {'✅ PASSED' if additional_success else '❌ FAILED'}")
        print(f"   5. Conversation Flow Integration: {'✅ PASSED' if flow_success else '❌ FAILED'}")
        print(f"   6. Error Message Absence: {'✅ PASSED' if error_absence_success else '❌ FAILED'}")
        
        # Overall success
        overall_success = (init_success and greeting_success and headache_success and 
                          additional_success and flow_success and error_absence_success)
        
        if overall_success:
            print("\n🎉 All Quick Health Tracking chatbot features passed comprehensive testing!")
            print("✅ Quick Health Tracking chatbot technical issue has been successfully resolved")
            print("✅ Chatbot now processes symptoms correctly without technical errors")
            return 0
        else:
            print("\n⚠️ Some Quick Health Tracking chatbot features failed testing. Check the details above.")
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result.get('passed', False):
                    print(f"  - {result['test_name']}: {result.get('details', 'Failed')}")
            return 1

if __name__ == "__main__":
    tester = QuickHealthChatbotTester()
    exit_code = tester.run_comprehensive_tests()
    sys.exit(exit_code)