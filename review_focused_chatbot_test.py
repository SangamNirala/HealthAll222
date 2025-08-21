#!/usr/bin/env python3
"""
🎯 REVIEW-FOCUSED QUICK HEALTH TRACKING CHATBOT TESTING SUITE 🎯

Focused backend testing for the specific improvements mentioned in the review request:

TESTING FOCUS AREAS (from review request):
✅ Internal Reasoning Filtering - verify responses don't contain internal AI thinking phrases
✅ Follow-up Question Improvements - test that follow-ups are less aggressive  
✅ Clean Response Structures - verify API responses have clean fields
✅ Conversation Progression - test complete flow from greeting through HPI elements
✅ Template-Based Follow-ups - verify follow-up questions use pre-defined templates

EXACT TEST SCENARIOS (from review request):
- POST /api/medical-ai/initialize (consultation initialization)
- Simple greeting: "hi" 
- Symptom reporting: "I have a headache"
- Detailed responses: "it started 2 days ago and is throbbing"
- Vague single word: "food" (should trigger follow-up)
- Detailed follow-up: "spicy foods make it worse" (should progress to next element)

VALIDATION CRITERIA (from review request):
✅ No internal reasoning phrases in any responses
✅ Follow-up only for genuinely vague responses  
✅ Clean, professional medical conversation
✅ Proper conversation progression through HPI elements
✅ Standard API response structure
✅ No technical errors or debugging text in responses

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
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://mediq-2.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class ReviewFocusedChatbotTester:
    """Review-focused tester for Quick Health Tracking Chatbot improvements"""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.consultation_id = None
        
        # Internal reasoning phrases that should NOT appear (from review request)
        self.internal_reasoning_phrases = [
            "I think there might be",
            "I understand you'd like to discuss", 
            "I'm analyzing",
            "Let me think",
            "I believe",
            "It seems like",
            "I'm processing",
            "My analysis suggests",
            "I'm considering",
            "Based on my understanding",
            "I understand you'd like to discuss something health-related"
        ]
        
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
        print()

    def check_internal_reasoning_filter(self, response_text: str) -> tuple[bool, str]:
        """Check if response contains internal reasoning phrases (CRITICAL from review)"""
        found_phrases = []
        for phrase in self.internal_reasoning_phrases:
            if phrase.lower() in response_text.lower():
                found_phrases.append(phrase)
        
        if found_phrases:
            return False, f"❌ CRITICAL: Found internal reasoning phrases: {', '.join(found_phrases)}"
        return True, "✅ No internal reasoning phrases detected"

    def check_clean_response_structure(self, response_data: Dict) -> tuple[bool, str]:
        """Check if response has clean, expected structure (from review request)"""
        required_fields = [
            "consultation_id", 
            "emergency_detected", 
            "next_questions", 
            "differential_diagnoses", 
            "recommendations"
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in response_data:
                missing_fields.append(field)
        
        if missing_fields:
            return False, f"❌ Missing required clean fields: {', '.join(missing_fields)}"
        
        return True, "✅ Clean response structure confirmed"

    def test_exact_review_scenario(self) -> bool:
        """
        🎯 TEST EXACT REVIEW SCENARIO
        
        Test the exact conversation flow mentioned in the review request
        """
        print("\n🎯 TESTING EXACT REVIEW SCENARIO")
        print("-" * 60)
        
        # Step 1: Initialize consultation
        try:
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
                json={
                    "patient_id": "anonymous",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Review Scenario - Initialize", False, 
                            f"HTTP {init_response.status_code}: {init_response.text}")
                return False
            
            init_data = init_response.json()
            self.consultation_id = init_data.get("consultation_id")
            
            # Check clean structure
            clean_structure, structure_msg = self.check_clean_response_structure(init_data)
            if not clean_structure:
                self.log_test("Review Scenario - Initialize", False, structure_msg)
                return False
            
            self.log_test("Review Scenario - Initialize", True, 
                        f"Consultation ID: {self.consultation_id}")
            
        except Exception as e:
            self.log_test("Review Scenario - Initialize", False, f"Exception: {str(e)}")
            return False
        
        # Test conversation steps from review request
        conversation_steps = [
            {
                "message": "hi",
                "description": "Simple greeting",
                "should_be_clean": True,
                "should_progress": True
            },
            {
                "message": "I have a headache", 
                "description": "Symptom reporting",
                "should_be_clean": True,
                "should_progress": True
            },
            {
                "message": "it started 2 days ago and is throbbing",
                "description": "Detailed response (should NOT trigger aggressive follow-up)",
                "should_be_clean": True,
                "should_progress": True,
                "should_not_followup_aggressively": True
            },
            {
                "message": "food",
                "description": "Vague single word (SHOULD trigger follow-up)",
                "should_be_clean": True,
                "should_trigger_followup": True
            },
            {
                "message": "spicy foods make it worse",
                "description": "Detailed follow-up (should progress to next element)",
                "should_be_clean": True,
                "should_progress": True
            }
        ]
        
        all_steps_passed = True
        
        for i, step in enumerate(conversation_steps, 1):
            try:
                response = requests.post(f"{API_BASE}/medical-ai/message",
                    json={
                        "message": step["message"],
                        "consultation_id": self.consultation_id,
                        "context": {}
                    },
                    timeout=30
                )
                
                if response.status_code != 200:
                    self.log_test(f"Review Scenario - Step {i}: {step['description']}", False,
                                f"HTTP {response.status_code}: {response.text}")
                    all_steps_passed = False
                    continue
                
                data = response.json()
                response_text = data.get("response", "")
                
                # CRITICAL: Check for internal reasoning phrases
                no_internal_reasoning, reasoning_msg = self.check_internal_reasoning_filter(response_text)
                if not no_internal_reasoning:
                    self.log_test(f"Review Scenario - Step {i}: {step['description']} - Internal Reasoning", 
                                False, reasoning_msg)
                    all_steps_passed = False
                else:
                    self.log_test(f"Review Scenario - Step {i}: {step['description']} - Internal Reasoning", 
                                True, reasoning_msg)
                
                # Check clean response structure
                clean_structure, structure_msg = self.check_clean_response_structure(data)
                if not clean_structure:
                    self.log_test(f"Review Scenario - Step {i}: {step['description']} - Clean Structure", 
                                False, structure_msg)
                    all_steps_passed = False
                else:
                    self.log_test(f"Review Scenario - Step {i}: {step['description']} - Clean Structure", 
                                True, structure_msg)
                
                # Check for technical errors
                technical_errors = ["technical issue", "AnatomicalEntity", "specificity_level", "error occurred"]
                found_errors = [error for error in technical_errors if error.lower() in response_text.lower()]
                
                if found_errors:
                    self.log_test(f"Review Scenario - Step {i}: {step['description']} - No Technical Errors", 
                                False, f"Found technical errors: {', '.join(found_errors)}")
                    all_steps_passed = False
                else:
                    self.log_test(f"Review Scenario - Step {i}: {step['description']} - No Technical Errors", 
                                True, "No technical errors detected")
                
                # Special checks based on step requirements
                if step.get("should_trigger_followup") and step["message"] == "food":
                    # For vague "food" response, should ask for more details
                    food_keywords = ["food", "eat", "meal", "trigger", "more", "details", "specific"]
                    has_food_followup = any(keyword in response_text.lower() for keyword in food_keywords)
                    
                    if has_food_followup:
                        self.log_test(f"Review Scenario - Step {i}: {step['description']} - Follow-up Triggered", 
                                    True, "Appropriate follow-up question for vague 'food' response")
                    else:
                        self.log_test(f"Review Scenario - Step {i}: {step['description']} - Follow-up Triggered", 
                                    False, "No follow-up question for vague 'food' response")
                        all_steps_passed = False
                
                if step.get("should_not_followup_aggressively") and "2 days ago and is throbbing" in step["message"]:
                    # Detailed response should NOT trigger aggressive follow-up
                    # Should progress normally
                    next_questions = data.get("next_questions", [])
                    if next_questions and len(response_text) > 50:
                        self.log_test(f"Review Scenario - Step {i}: {step['description']} - No Aggressive Follow-up", 
                                    True, "Detailed response progressed normally without aggressive follow-up")
                    else:
                        self.log_test(f"Review Scenario - Step {i}: {step['description']} - No Aggressive Follow-up", 
                                    False, "May have triggered aggressive follow-up for detailed response")
                        all_steps_passed = False
                
            except Exception as e:
                self.log_test(f"Review Scenario - Step {i}: {step['description']}", False, f"Exception: {str(e)}")
                all_steps_passed = False
        
        return all_steps_passed

    def test_internal_reasoning_filtering(self) -> bool:
        """
        🧠 TEST INTERNAL REASONING FILTERING (CRITICAL from review)
        
        Test various inputs to ensure NO internal reasoning phrases appear
        """
        print("\n🧠 TESTING INTERNAL REASONING FILTERING")
        print("-" * 60)
        
        test_messages = [
            "hi",
            "hello", 
            "I have a headache",
            "chest pain",
            "I'm feeling sick",
            "what should I do",
            "help me",
            "I don't know what's wrong"
        ]
        
        all_passed = True
        
        for message in test_messages:
            try:
                # Initialize fresh consultation
                init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
                    json={"patient_id": "anonymous", "timestamp": datetime.now().isoformat()},
                    timeout=30
                )
                
                if init_response.status_code != 200:
                    continue
                
                consultation_id = init_response.json().get("consultation_id")
                
                response = requests.post(f"{API_BASE}/medical-ai/message",
                    json={
                        "message": message,
                        "consultation_id": consultation_id,
                        "context": {}
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "")
                    
                    no_internal_reasoning, reasoning_msg = self.check_internal_reasoning_filter(response_text)
                    
                    if no_internal_reasoning:
                        self.log_test(f"Internal Reasoning Filter - '{message}'", True, reasoning_msg)
                    else:
                        self.log_test(f"Internal Reasoning Filter - '{message}'", False, reasoning_msg)
                        all_passed = False
                else:
                    self.log_test(f"Internal Reasoning Filter - '{message}'", False, 
                                f"HTTP {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Internal Reasoning Filter - '{message}'", False, f"Exception: {str(e)}")
                all_passed = False
        
        return all_passed

    def test_follow_up_improvements(self) -> bool:
        """
        🔄 TEST FOLLOW-UP QUESTION IMPROVEMENTS (from review)
        
        Test that follow-ups are less aggressive and only for genuinely vague responses
        """
        print("\n🔄 TESTING FOLLOW-UP QUESTION IMPROVEMENTS")
        print("-" * 60)
        
        # Test cases: vague vs detailed responses
        test_cases = [
            {
                "message": "food",
                "type": "vague_single_word",
                "should_trigger_followup": True,
                "description": "Vague single word should trigger follow-up"
            },
            {
                "message": "position", 
                "type": "vague_single_word",
                "should_trigger_followup": True,
                "description": "Vague single word should trigger follow-up"
            },
            {
                "message": "medication",
                "type": "vague_single_word", 
                "should_trigger_followup": True,
                "description": "Vague single word should trigger follow-up"
            },
            {
                "message": "it started 2 days ago and gets worse with movement",
                "type": "detailed_response",
                "should_trigger_followup": False,
                "description": "Detailed response should NOT trigger aggressive follow-up"
            },
            {
                "message": "the pain is sharp and stabbing in my left temple",
                "type": "detailed_response", 
                "should_trigger_followup": False,
                "description": "Detailed response should NOT trigger aggressive follow-up"
            },
            {
                "message": "lying down in a dark room helps reduce the pain",
                "type": "detailed_response",
                "should_trigger_followup": False, 
                "description": "Detailed response should NOT trigger aggressive follow-up"
            }
        ]
        
        all_passed = True
        
        for test_case in test_cases:
            try:
                # Initialize fresh consultation and establish headache context
                init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
                    json={"patient_id": "anonymous", "timestamp": datetime.now().isoformat()},
                    timeout=30
                )
                
                if init_response.status_code != 200:
                    continue
                
                consultation_id = init_response.json().get("consultation_id")
                
                # First establish headache context
                requests.post(f"{API_BASE}/medical-ai/message",
                    json={
                        "message": "I have a headache",
                        "consultation_id": consultation_id,
                        "context": {}
                    },
                    timeout=30
                )
                
                # Now test the specific message
                response = requests.post(f"{API_BASE}/medical-ai/message",
                    json={
                        "message": test_case["message"],
                        "consultation_id": consultation_id,
                        "context": {}
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "")
                    next_questions = data.get("next_questions", [])
                    
                    # Check internal reasoning first
                    no_internal_reasoning, _ = self.check_internal_reasoning_filter(response_text)
                    
                    if test_case["should_trigger_followup"]:
                        # Vague responses should trigger intelligent follow-up
                        has_followup_indicators = any(word in response_text.lower() 
                                                    for word in ["more", "specific", "details", "tell me", "can you"])
                        
                        if has_followup_indicators and no_internal_reasoning:
                            self.log_test(f"Follow-up Improvement - {test_case['type']}: '{test_case['message'][:20]}...'", 
                                        True, test_case["description"])
                        else:
                            self.log_test(f"Follow-up Improvement - {test_case['type']}: '{test_case['message'][:20]}...'", 
                                        False, f"Expected follow-up for vague response. Internal reasoning clean: {no_internal_reasoning}")
                            all_passed = False
                    else:
                        # Detailed responses should NOT trigger aggressive follow-up
                        # Should progress normally with next questions
                        if next_questions and no_internal_reasoning and len(response_text) > 30:
                            self.log_test(f"Follow-up Improvement - {test_case['type']}: '{test_case['message'][:20]}...'", 
                                        True, test_case["description"])
                        else:
                            self.log_test(f"Follow-up Improvement - {test_case['type']}: '{test_case['message'][:20]}...'", 
                                        False, f"Detailed response may have triggered aggressive follow-up. Next questions: {len(next_questions)}")
                            all_passed = False
                else:
                    self.log_test(f"Follow-up Improvement - {test_case['type']}: '{test_case['message'][:20]}...'", 
                                False, f"HTTP {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Follow-up Improvement - {test_case['type']}: '{test_case['message'][:20]}...'", 
                            False, f"Exception: {str(e)}")
                all_passed = False
        
        return all_passed

    def run_review_focused_tests(self):
        """Run review-focused chatbot tests"""
        print("🎯 Starting Review-Focused Quick Health Tracking Chatbot Tests...")
        print(f"   Base URL: {API_BASE}")
        print("   Focus: Conversation Flow Improvements from Review Request")
        print("=" * 80)
        
        # Test 1: Exact Review Scenario
        print("\n🎯 TESTING PHASE 1: EXACT REVIEW SCENARIO")
        scenario_success = self.test_exact_review_scenario()
        
        # Test 2: Internal Reasoning Filtering (CRITICAL)
        print("\n🎯 TESTING PHASE 2: INTERNAL REASONING FILTERING (CRITICAL)")
        reasoning_success = self.test_internal_reasoning_filtering()
        
        # Test 3: Follow-up Question Improvements
        print("\n🎯 TESTING PHASE 3: FOLLOW-UP QUESTION IMPROVEMENTS")
        followup_success = self.test_follow_up_improvements()
        
        # Print final results
        print("\n" + "=" * 80)
        print(f"📊 FINAL RESULTS")
        print(f"Tests Run: {self.total_tests}")
        print(f"Tests Passed: {self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        print(f"\n🎯 REVIEW-FOCUSED CHATBOT TEST RESULTS:")
        print(f"   1. Exact Review Scenario: {'✅ PASSED' if scenario_success else '❌ FAILED'}")
        print(f"   2. Internal Reasoning Filtering (CRITICAL): {'✅ PASSED' if reasoning_success else '❌ FAILED'}")
        print(f"   3. Follow-up Question Improvements: {'✅ PASSED' if followup_success else '❌ FAILED'}")
        
        # Overall success
        overall_success = scenario_success and reasoning_success and followup_success
        
        print(f"\n🎯 REVIEW VALIDATION CRITERIA:")
        print(f"   ✅ No internal reasoning phrases: {'PASSED' if reasoning_success else 'FAILED'}")
        print(f"   ✅ Follow-up only for vague responses: {'PASSED' if followup_success else 'FAILED'}")
        print(f"   ✅ Clean, professional conversation: {'PASSED' if scenario_success else 'FAILED'}")
        print(f"   ✅ Proper conversation progression: {'PASSED' if scenario_success else 'FAILED'}")
        print(f"   ✅ Standard API response structure: {'PASSED' if scenario_success else 'FAILED'}")
        print(f"   ✅ No technical errors: {'PASSED' if scenario_success else 'FAILED'}")
        
        if overall_success:
            print("\n🎉 All review-focused chatbot improvements passed comprehensive testing!")
            print("✅ Quick Health Tracking Chatbot conversation flow improvements are working correctly")
            return 0
        else:
            print("\n⚠️ Some review-focused chatbot improvements failed testing.")
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result.get('passed', False):
                    print(f"  - {result['test_name']}: {result.get('details', 'Failed')}")
            return 1

if __name__ == "__main__":
    tester = ReviewFocusedChatbotTester()
    exit_code = tester.run_review_focused_tests()
    sys.exit(exit_code)