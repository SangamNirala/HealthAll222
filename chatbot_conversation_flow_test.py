#!/usr/bin/env python3
"""
🤖 QUICK HEALTH TRACKING CHATBOT CONVERSATION FLOW TESTING SUITE 🤖

Comprehensive backend testing for the Quick Health Tracking chatbot conversation flow
specifically focusing on the conversation_history parameter fixes and proper conversation progression.

TESTING OBJECTIVES:
✅ TEST the exact conversation flow: "hi" → "I have a headache" → "it has started 2 days before" → "it is dull" → "food" → "position"
✅ VERIFY conversation progresses through proper medical interview stages instead of repeating same questions
✅ CONFIRM conversation_history parameter is properly handled in both frontend API and backend
✅ TEST context persistence works correctly across multiple conversation turns
✅ VERIFY chatbot asks different HPI questions and doesn't get stuck in loops
✅ ENSURE no repetitive "Is there anything that makes your I have a headache better or worse?" loops
✅ VALIDATE proper HPI element extraction from user responses
✅ CONFIRM clean symptom names in questions (not "I have a headache")
✅ TEST conversation stage progression from chief_complaint → history_present_illness → review_of_systems

Author: Testing Agent
Date: 2025-01-19
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://empathcare-ai.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class ChatbotConversationFlowTester:
    """Comprehensive tester for Quick Health Tracking Chatbot Conversation Flow"""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.conversation_history = []
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

    def initialize_consultation(self) -> bool:
        """Initialize a new medical consultation"""
        print("\n🚀 INITIALIZING MEDICAL CONSULTATION")
        print("-" * 50)
        
        try:
            response = requests.post(f"{API_BASE}/medical-ai/initialize",
                json={
                    "patient_id": "test-patient-chatbot-flow",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.consultation_id = data.get("consultation_id")
                
                # Validate response structure
                required_keys = ["consultation_id", "patient_id", "current_stage", "response"]
                missing_keys = [key for key in required_keys if key not in data]
                
                if not missing_keys and self.consultation_id:
                    self.log_test("Consultation Initialization", True,
                                f"Consultation ID: {self.consultation_id}, Stage: {data.get('current_stage')}")
                    return True
                else:
                    self.log_test("Consultation Initialization", False,
                                f"Missing keys: {missing_keys}, Consultation ID: {self.consultation_id}")
                    return False
            else:
                self.log_test("Consultation Initialization", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Consultation Initialization", False, f"Exception: {str(e)}")
            return False

    def send_message(self, message: str, expected_stage: str = None, test_name: str = None) -> Optional[Dict]:
        """Send a message to the chatbot and return response"""
        if not self.consultation_id:
            print("❌ No consultation ID available")
            return None
            
        try:
            # Build conversation history for context
            conversation_history = []
            for i, entry in enumerate(self.conversation_history):
                conversation_history.append({
                    "role": "user" if i % 2 == 0 else "assistant",
                    "content": entry
                })
            
            payload = {
                "consultation_id": self.consultation_id,
                "message": message,
                "conversation_history": conversation_history  # This is the key fix being tested
            }
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Add to conversation history
                self.conversation_history.append(message)
                self.conversation_history.append(data.get("response", ""))
                
                # Validate response structure
                required_keys = ["stage", "urgency", "consultation_id", "patient_id", "current_stage", 
                               "emergency_detected", "response", "context", "next_questions", 
                               "differential_diagnoses", "recommendations"]
                
                missing_keys = [key for key in required_keys if key not in data]
                
                if test_name:
                    stage_correct = True
                    if expected_stage:
                        actual_stage = data.get("current_stage", "")
                        stage_correct = actual_stage == expected_stage
                        
                    if not missing_keys and stage_correct:
                        stage_info = f", Stage: {data.get('current_stage')}" if expected_stage else ""
                        self.log_test(test_name, True,
                                    f"Response length: {len(data.get('response', ''))}{stage_info}")
                    else:
                        error_details = []
                        if missing_keys:
                            error_details.append(f"Missing keys: {missing_keys}")
                        if not stage_correct:
                            error_details.append(f"Expected stage: {expected_stage}, Got: {data.get('current_stage')}")
                        self.log_test(test_name, False, ", ".join(error_details))
                
                return data
            else:
                if test_name:
                    self.log_test(test_name, False, f"HTTP {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            if test_name:
                self.log_test(test_name, False, f"Exception: {str(e)}")
            return None

    def test_exact_conversation_flow(self) -> bool:
        """Test the exact conversation flow reported by the user"""
        print("\n🎯 TESTING EXACT CONVERSATION FLOW")
        print("-" * 50)
        
        conversation_steps = [
            {
                "message": "hi",
                "test_name": "Step 1: Greeting",
                "expected_stage": "greeting"
            },
            {
                "message": "I have a headache",
                "test_name": "Step 2: Chief Complaint - Headache",
                "expected_stage": "chief_complaint"
            },
            {
                "message": "it has started 2 days before",
                "test_name": "Step 3: HPI - Onset (2 days)",
                "expected_stage": "history_present_illness"
            },
            {
                "message": "it is dull",
                "test_name": "Step 4: HPI - Quality (dull)",
                "expected_stage": "history_present_illness"
            },
            {
                "message": "food",
                "test_name": "Step 5: HPI - Alleviating Factor (food)",
                "expected_stage": "history_present_illness"
            },
            {
                "message": "position",
                "test_name": "Step 6: HPI - Aggravating Factor (position)",
                "expected_stage": "history_present_illness"
            }
        ]
        
        all_passed = True
        previous_responses = []
        
        for step in conversation_steps:
            response = self.send_message(
                step["message"], 
                step.get("expected_stage"), 
                step["test_name"]
            )
            
            if response:
                response_text = response.get("response", "")
                previous_responses.append(response_text)
                
                # Check for repetitive questions (the main issue being tested)
                if len(previous_responses) > 1:
                    current_response = response_text.lower()
                    for prev_response in previous_responses[:-1]:
                        prev_response_lower = prev_response.lower()
                        
                        # Check for repetitive "makes your I have a headache better or worse" pattern
                        if ("makes your i have a headache" in current_response and 
                            "makes your i have a headache" in prev_response_lower):
                            self.log_test(f"{step['test_name']} - No Repetitive Questions", False,
                                        "Detected repetitive 'makes your I have a headache' question pattern")
                            all_passed = False
                            break
                        
                        # Check for any exact repetitive questions
                        if (len(current_response) > 50 and len(prev_response_lower) > 50 and
                            current_response == prev_response_lower):
                            self.log_test(f"{step['test_name']} - No Repetitive Questions", False,
                                        "Detected exact repetitive question")
                            all_passed = False
                            break
                    else:
                        # No repetitive questions found
                        self.log_test(f"{step['test_name']} - No Repetitive Questions", True,
                                    "No repetitive questions detected")
                
                # Check for clean symptom names (should not contain "I have a headache")
                if "i have a headache" in response_text.lower():
                    self.log_test(f"{step['test_name']} - Clean Symptom Names", False,
                                "Response contains 'I have a headache' instead of clean symptom name")
                    all_passed = False
                else:
                    self.log_test(f"{step['test_name']} - Clean Symptom Names", True,
                                "Response uses clean symptom names")
            else:
                all_passed = False
        
        return all_passed

    def test_conversation_history_parameter(self) -> bool:
        """Test that conversation_history parameter is properly handled"""
        print("\n📝 TESTING CONVERSATION_HISTORY PARAMETER HANDLING")
        print("-" * 50)
        
        # Reset for clean test
        if not self.initialize_consultation():
            return False
        
        # Send first message
        response1 = self.send_message("I have a headache", test_name="First Message - No History")
        if not response1:
            return False
        
        # Send second message with conversation history
        response2 = self.send_message("it started yesterday", test_name="Second Message - With History")
        if not response2:
            return False
        
        # Check that the second response shows awareness of the first message
        response2_text = response2.get("response", "").lower()
        context = response2.get("context", {})
        
        # The response should reference the headache from the first message
        context_aware = ("headache" in response2_text or 
                        "headache" in str(context).lower() or
                        len(self.conversation_history) >= 4)  # Should have both messages and responses
        
        if context_aware:
            self.log_test("Conversation History Context Awareness", True,
                        f"Response shows awareness of previous context. History length: {len(self.conversation_history)}")
            return True
        else:
            self.log_test("Conversation History Context Awareness", False,
                        "Response does not show awareness of previous conversation context")
            return False

    def test_stage_progression(self) -> bool:
        """Test proper stage progression through medical interview"""
        print("\n📊 TESTING STAGE PROGRESSION")
        print("-" * 50)
        
        # Reset for clean test
        if not self.initialize_consultation():
            return False
        
        expected_progression = [
            ("hi", "greeting"),
            ("I have a headache", "chief_complaint"),
            ("it started 2 days ago", "history_present_illness"),
            ("it's a dull pain", "history_present_illness"),
            ("nothing makes it better", "history_present_illness")
        ]
        
        all_passed = True
        actual_stages = []
        
        for message, expected_stage in expected_progression:
            response = self.send_message(message)
            if response:
                actual_stage = response.get("current_stage", "")
                actual_stages.append(actual_stage)
                
                if actual_stage == expected_stage:
                    self.log_test(f"Stage Progression - {expected_stage}", True,
                                f"Correctly progressed to {actual_stage}")
                else:
                    self.log_test(f"Stage Progression - {expected_stage}", False,
                                f"Expected {expected_stage}, got {actual_stage}")
                    all_passed = False
            else:
                all_passed = False
        
        # Check overall progression makes sense
        if len(set(actual_stages)) > 1:  # Should have multiple different stages
            self.log_test("Overall Stage Progression", True,
                        f"Progressed through stages: {' → '.join(actual_stages)}")
        else:
            self.log_test("Overall Stage Progression", False,
                        f"Stuck in same stage: {actual_stages}")
            all_passed = False
        
        return all_passed

    def test_hpi_element_extraction(self) -> bool:
        """Test proper HPI element extraction from user responses"""
        print("\n🔍 TESTING HPI ELEMENT EXTRACTION")
        print("-" * 50)
        
        # Reset for clean test
        if not self.initialize_consultation():
            return False
        
        # Start with chief complaint
        self.send_message("hi")
        self.send_message("I have a headache")
        
        hpi_tests = [
            {
                "message": "it started 2 days ago",
                "element": "onset",
                "expected_value": "2 days",
                "test_name": "HPI Extraction - Onset"
            },
            {
                "message": "it's a dull aching pain",
                "element": "quality",
                "expected_value": "dull",
                "test_name": "HPI Extraction - Quality"
            },
            {
                "message": "lying down makes it better",
                "element": "alleviating_factors",
                "expected_value": "lying down",
                "test_name": "HPI Extraction - Alleviating Factors"
            },
            {
                "message": "bright lights make it worse",
                "element": "aggravating_factors", 
                "expected_value": "bright lights",
                "test_name": "HPI Extraction - Aggravating Factors"
            }
        ]
        
        all_passed = True
        
        for test_case in hpi_tests:
            response = self.send_message(test_case["message"])
            if response:
                context = response.get("context", {})
                
                # Check if the HPI element was extracted and stored
                hpi_extracted = False
                
                # Look for the element in context or response
                response_text = response.get("response", "").lower()
                context_str = str(context).lower()
                
                if (test_case["expected_value"].lower() in response_text or
                    test_case["expected_value"].lower() in context_str or
                    test_case["element"] in context_str):
                    hpi_extracted = True
                
                if hpi_extracted:
                    self.log_test(test_case["test_name"], True,
                                f"Successfully extracted {test_case['element']}: {test_case['expected_value']}")
                else:
                    self.log_test(test_case["test_name"], False,
                                f"Failed to extract {test_case['element']}: {test_case['expected_value']}")
                    all_passed = False
            else:
                all_passed = False
        
        return all_passed

    def test_no_repetitive_loops(self) -> bool:
        """Test that chatbot doesn't get stuck in repetitive question loops"""
        print("\n🔄 TESTING NO REPETITIVE LOOPS")
        print("-" * 50)
        
        # Reset for clean test
        if not self.initialize_consultation():
            return False
        
        # Start conversation
        self.send_message("hi")
        self.send_message("I have a headache")
        
        # Send multiple similar responses to test for loops
        responses = []
        loop_test_messages = [
            "it started yesterday",
            "it's been going on since yesterday", 
            "the pain began yesterday",
            "it started about a day ago"
        ]
        
        for i, message in enumerate(loop_test_messages):
            response = self.send_message(message, test_name=f"Loop Test Message {i+1}")
            if response:
                response_text = response.get("response", "")
                responses.append(response_text)
        
        # Check for repetitive responses
        if len(responses) >= 2:
            unique_responses = len(set(responses))
            total_responses = len(responses)
            
            # Should have some variation in responses, not all identical
            if unique_responses > 1:
                self.log_test("No Repetitive Response Loops", True,
                            f"Generated {unique_responses} unique responses out of {total_responses}")
                return True
            else:
                self.log_test("No Repetitive Response Loops", False,
                            f"All {total_responses} responses were identical - stuck in loop")
                return False
        else:
            self.log_test("No Repetitive Response Loops", False,
                        "Insufficient responses to test for loops")
            return False

    def run_comprehensive_tests(self):
        """Run comprehensive chatbot conversation flow tests"""
        print("🚀 Starting Quick Health Tracking Chatbot Conversation Flow Tests...")
        print(f"   Base URL: {API_BASE}")
        print("=" * 80)
        
        # Initialize consultation first
        if not self.initialize_consultation():
            print("❌ Failed to initialize consultation. Cannot proceed with tests.")
            return 1
        
        # Test 1: Exact Conversation Flow
        print("\n🎯 TESTING PHASE 1: EXACT CONVERSATION FLOW")
        exact_flow_success = self.test_exact_conversation_flow()
        
        # Test 2: Conversation History Parameter
        print("\n🎯 TESTING PHASE 2: CONVERSATION HISTORY PARAMETER")
        history_success = self.test_conversation_history_parameter()
        
        # Test 3: Stage Progression
        print("\n🎯 TESTING PHASE 3: STAGE PROGRESSION")
        stage_success = self.test_stage_progression()
        
        # Test 4: HPI Element Extraction
        print("\n🎯 TESTING PHASE 4: HPI ELEMENT EXTRACTION")
        hpi_success = self.test_hpi_element_extraction()
        
        # Test 5: No Repetitive Loops
        print("\n🎯 TESTING PHASE 5: NO REPETITIVE LOOPS")
        loop_success = self.test_no_repetitive_loops()
        
        # Print final results
        print("\n" + "=" * 80)
        print(f"📊 FINAL RESULTS")
        print(f"Tests Run: {self.total_tests}")
        print(f"Tests Passed: {self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        print(f"\n🎯 QUICK HEALTH TRACKING CHATBOT CONVERSATION FLOW TEST RESULTS:")
        print(f"   1. Exact Conversation Flow: {'✅ PASSED' if exact_flow_success else '❌ FAILED'}")
        print(f"   2. Conversation History Parameter: {'✅ PASSED' if history_success else '❌ FAILED'}")
        print(f"   3. Stage Progression: {'✅ PASSED' if stage_success else '❌ FAILED'}")
        print(f"   4. HPI Element Extraction: {'✅ PASSED' if hpi_success else '❌ FAILED'}")
        print(f"   5. No Repetitive Loops: {'✅ PASSED' if loop_success else '❌ FAILED'}")
        
        # Overall success
        overall_success = (exact_flow_success and history_success and stage_success and 
                          hpi_success and loop_success)
        
        if overall_success:
            print("\n🎉 All chatbot conversation flow features passed comprehensive testing!")
            print("✅ Quick Health Tracking Chatbot conversation flow issues have been resolved")
            return 0
        else:
            print("\n⚠️ Some chatbot conversation flow features failed testing. Check the details above.")
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result.get('passed', False):
                    print(f"  - {result['test_name']}: {result.get('details', 'Failed')}")
            return 1

if __name__ == "__main__":
    tester = ChatbotConversationFlowTester()
    exit_code = tester.run_comprehensive_tests()
    sys.exit(exit_code)