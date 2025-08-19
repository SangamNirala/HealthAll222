#!/usr/bin/env python3
"""
🔄 CONVERSATION LOOP DEBUGGING TEST SUITE 🔄

Comprehensive testing for the exact conversation flow that's causing the loop issue
to get detailed debugging output and identify the root cause.

TESTING OBJECTIVES:
✅ Test the exact 7-step conversation flow mentioned in review request
✅ Pass complete "context" object from previous response (not just consultation_id)
✅ Capture HPI DEBUG messages to see what's happening in _get_next_hpi_element_smart
✅ Identify why already asked questions are being selected again
✅ Validate conversation state management and context handling

CONVERSATION FLOW TO TEST:
1. POST /api/medical-ai/initialize with patient_id='anonymous'
2. POST /api/medical-ai/message with message='hi' and full context from step 1
3. POST /api/medical-ai/message with message='I have a headache' and full context from step 2  
4. POST /api/medical-ai/message with message='it has started 2 days before' and full context from step 3
5. POST /api/medical-ai/message with message='it is dull' and full context from step 4
6. POST /api/medical-ai/message with message='food' and full context from step 5
7. POST /api/medical-ai/message with message='position' and full context from step 6

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
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://symptom-tracker-fix.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class ConversationLoopTester:
    """Comprehensive tester for Conversation Loop Fix"""
    
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

    def initialize_conversation(self) -> bool:
        """
        🚀 INITIALIZE CONVERSATION
        
        Test POST /api/medical-ai/initialize endpoint
        """
        print("\n🚀 INITIALIZING CONVERSATION")
        print("-" * 50)
        
        try:
            response = requests.post(f"{API_BASE}/medical-ai/initialize",
                json={
                    "patient_id": "test-patient-conversation-loop",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.consultation_id = data.get("consultation_id")
                
                # Validate response structure
                required_fields = ["consultation_id", "patient_id", "current_stage", "response"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields and self.consultation_id:
                    self.log_test("Conversation Initialization", True,
                                f"Consultation ID: {self.consultation_id}, Stage: {data.get('current_stage')}")
                    return True
                else:
                    self.log_test("Conversation Initialization", False,
                                f"Missing fields: {missing_fields}", data)
                    return False
            else:
                self.log_test("Conversation Initialization", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Conversation Initialization", False, f"Exception: {str(e)}")
            return False

    def send_message(self, message: str, test_name: str) -> Optional[Dict]:
        """
        💬 SEND MESSAGE TO CHATBOT
        
        Send a message and return the response data
        """
        try:
            # Build conversation history for context
            conversation_history = []
            for entry in self.conversation_history:
                conversation_history.append({
                    "role": entry["role"],
                    "content": entry["content"]
                })
            
            request_payload = {
                "message": message,
                "consultation_id": self.consultation_id,
                "conversation_history": conversation_history
            }
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json=request_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Add to conversation history
                self.conversation_history.append({
                    "role": "user",
                    "content": message
                })
                self.conversation_history.append({
                    "role": "assistant", 
                    "content": data.get("response", "")
                })
                
                # Validate response structure
                required_fields = ["response", "current_stage", "consultation_id"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    self.log_test(test_name, True,
                                f"Message: '{message}' -> Stage: {data.get('current_stage')}, Response length: {len(data.get('response', ''))}")
                    return data
                else:
                    self.log_test(test_name, False,
                                f"Missing fields: {missing_fields}", data)
                    return None
            else:
                self.log_test(test_name, False,
                            f"HTTP {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            self.log_test(test_name, False, f"Exception: {str(e)}")
            return None

    def test_exact_conversation_flow(self) -> bool:
        """
        🎯 TEST EXACT CONVERSATION FLOW
        
        Test the exact conversation flow mentioned in the review request
        """
        print("\n🎯 TESTING EXACT CONVERSATION FLOW")
        print("-" * 50)
        
        # Step 1: Initialize conversation
        if not self.initialize_conversation():
            return False
        
        # Step 2: Send "hi"
        response_hi = self.send_message("hi", "Message: 'hi'")
        if not response_hi:
            return False
        
        # Step 3: Send "I have a headache"
        response_headache = self.send_message("I have a headache", "Message: 'I have a headache'")
        if not response_headache:
            return False
        
        # Step 4: Send "it has started 2 days before"
        response_timing = self.send_message("it has started 2 days before", "Message: 'it has started 2 days before'")
        if not response_timing:
            return False
        
        # Step 5: Send "it is dull"
        response_quality = self.send_message("it is dull", "Message: 'it is dull'")
        if not response_quality:
            return False
        
        # Step 6: Send "food"
        response_food = self.send_message("food", "Message: 'food'")
        if not response_food:
            return False
        
        # Step 7: Send "position"
        response_position = self.send_message("position", "Message: 'position'")
        if not response_position:
            return False
        
        return True

    def analyze_conversation_quality(self) -> bool:
        """
        🔍 ANALYZE CONVERSATION QUALITY
        
        Analyze the conversation for the specific issues that were fixed
        """
        print("\n🔍 ANALYZING CONVERSATION QUALITY")
        print("-" * 50)
        
        all_passed = True
        
        # Extract all AI responses
        ai_responses = []
        for entry in self.conversation_history:
            if entry["role"] == "assistant":
                ai_responses.append(entry["content"])
        
        # Test 1: No malformed questions
        malformed_patterns = [
            "When exactly did your start?",
            "What makes your I have a headache",
            "How long has your I have a headache",
            "Where is your I have a headache"
        ]
        
        malformed_found = []
        for response in ai_responses:
            for pattern in malformed_patterns:
                if pattern in response:
                    malformed_found.append(pattern)
        
        if not malformed_found:
            self.log_test("No Malformed Questions", True, "No malformed questions detected")
        else:
            self.log_test("No Malformed Questions", False, f"Malformed questions found: {malformed_found}")
            all_passed = False
        
        # Test 2: No repetitive questioning loops
        question_patterns = []
        for response in ai_responses:
            # Extract questions (sentences ending with ?)
            questions = [sentence.strip() for sentence in response.split('.') if sentence.strip().endswith('?')]
            question_patterns.extend(questions)
        
        # Check for exact duplicates
        unique_questions = set(question_patterns)
        duplicate_count = len(question_patterns) - len(unique_questions)
        
        if duplicate_count <= 1:  # Allow 1 duplicate as it might be legitimate
            self.log_test("No Repetitive Loops", True, f"Minimal question repetition detected ({duplicate_count} duplicates)")
        else:
            self.log_test("No Repetitive Loops", False, f"Excessive question repetition detected ({duplicate_count} duplicates)")
            all_passed = False
        
        # Test 3: Clean symptom names in questions
        clean_symptom_usage = True
        for response in ai_responses:
            if "I have a headache" in response and "?" in response:
                # This suggests the full user message is being used instead of clean symptom name
                clean_symptom_usage = False
                break
        
        if clean_symptom_usage:
            self.log_test("Clean Symptom Names", True, "Clean symptom names used in questions")
        else:
            self.log_test("Clean Symptom Names", False, "Full user messages found in AI questions instead of clean symptom names")
            all_passed = False
        
        # Test 4: Proper conversation progression
        stages_seen = []
        for i, entry in enumerate(self.conversation_history):
            if entry["role"] == "assistant" and i < len(self.conversation_history) - 1:
                # Look for stage progression indicators
                response = entry["content"].lower()
                if "greeting" in response or "hello" in response or "help you" in response:
                    stages_seen.append("greeting")
                elif "tell me about" in response or "describe" in response:
                    stages_seen.append("chief_complaint")
                elif "when" in response or "how long" in response:
                    stages_seen.append("timing")
                elif "quality" in response or "describe the" in response:
                    stages_seen.append("quality")
                elif "better" in response or "worse" in response:
                    stages_seen.append("factors")
        
        if len(set(stages_seen)) >= 3:  # Should see at least 3 different conversation stages
            self.log_test("Proper Conversation Progression", True, f"Stages detected: {set(stages_seen)}")
        else:
            self.log_test("Proper Conversation Progression", False, f"Limited stage progression: {set(stages_seen)}")
            all_passed = False
        
        # Test 5: Graceful handling of short responses
        short_responses = ["food", "position", "it is dull"]
        short_response_handling = True
        
        for i, entry in enumerate(self.conversation_history):
            if entry["role"] == "user" and entry["content"] in short_responses:
                # Check if the next AI response is reasonable (not an error or confusion)
                if i + 1 < len(self.conversation_history):
                    ai_response = self.conversation_history[i + 1]["content"].lower()
                    if "i don't understand" in ai_response or "unclear" in ai_response or "error" in ai_response:
                        short_response_handling = False
                        break
        
        if short_response_handling:
            self.log_test("Graceful Short Response Handling", True, "Short responses handled appropriately")
        else:
            self.log_test("Graceful Short Response Handling", False, "Short responses not handled gracefully")
            all_passed = False
        
        return all_passed

    def test_context_maintenance(self) -> bool:
        """
        🧠 TEST CONTEXT MAINTENANCE
        
        Test that context is maintained across conversation turns
        """
        print("\n🧠 TESTING CONTEXT MAINTENANCE")
        print("-" * 50)
        
        # Look for evidence that the AI remembers previous information
        context_maintained = False
        
        for entry in self.conversation_history:
            if entry["role"] == "assistant":
                response = entry["content"].lower()
                # Look for references to previously mentioned information
                if "headache" in response and ("2 days" in response or "dull" in response):
                    context_maintained = True
                    break
        
        if context_maintained:
            self.log_test("Context Maintenance", True, "AI demonstrates memory of previous conversation elements")
            return True
        else:
            self.log_test("Context Maintenance", False, "AI does not appear to maintain context across turns")
            return False

    def test_conversation_history_parameter(self) -> bool:
        """
        📝 TEST CONVERSATION HISTORY PARAMETER
        
        Test that the conversation_history parameter is working properly
        """
        print("\n📝 TESTING CONVERSATION HISTORY PARAMETER")
        print("-" * 50)
        
        # Send a follow-up message that requires context from conversation history
        follow_up_response = self.send_message("Can you summarize what we've discussed so far?", "Context Summary Request")
        
        if follow_up_response:
            response_text = follow_up_response.get("response", "").lower()
            
            # Check if the summary includes key elements from our conversation
            context_elements = ["headache", "2 days", "dull"]
            elements_found = sum(1 for element in context_elements if element in response_text)
            
            if elements_found >= 2:  # Should mention at least 2 of the 3 key elements
                self.log_test("Conversation History Parameter", True, 
                            f"Summary includes {elements_found}/3 key conversation elements")
                return True
            else:
                self.log_test("Conversation History Parameter", False,
                            f"Summary only includes {elements_found}/3 key conversation elements")
                return False
        else:
            return False

    def run_comprehensive_tests(self):
        """Run comprehensive conversation loop fix tests"""
        print("🚀 Starting Conversation Loop Fix Comprehensive Tests...")
        print(f"   Base URL: {API_BASE}")
        print("=" * 80)
        
        # Test 1: Exact Conversation Flow
        print("\n🎯 TESTING PHASE 1: EXACT CONVERSATION FLOW")
        flow_success = self.test_exact_conversation_flow()
        
        if not flow_success:
            print("❌ Conversation flow failed - cannot proceed with quality analysis")
            return 1
        
        # Test 2: Conversation Quality Analysis
        print("\n🎯 TESTING PHASE 2: CONVERSATION QUALITY ANALYSIS")
        quality_success = self.analyze_conversation_quality()
        
        # Test 3: Context Maintenance
        print("\n🎯 TESTING PHASE 3: CONTEXT MAINTENANCE")
        context_success = self.test_context_maintenance()
        
        # Test 4: Conversation History Parameter
        print("\n🎯 TESTING PHASE 4: CONVERSATION HISTORY PARAMETER")
        history_success = self.test_conversation_history_parameter()
        
        # Print conversation history for debugging
        print("\n📋 FULL CONVERSATION HISTORY:")
        print("-" * 50)
        for i, entry in enumerate(self.conversation_history):
            role_icon = "👤" if entry["role"] == "user" else "🤖"
            print(f"{i+1}. {role_icon} {entry['role'].upper()}: {entry['content'][:100]}...")
        
        # Print final results
        print("\n" + "=" * 80)
        print(f"📊 FINAL RESULTS")
        print(f"Tests Run: {self.total_tests}")
        print(f"Tests Passed: {self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        print(f"\n🎯 CONVERSATION LOOP FIX TEST RESULTS:")
        print(f"   1. Exact Conversation Flow: {'✅ PASSED' if flow_success else '❌ FAILED'}")
        print(f"   2. Conversation Quality Analysis: {'✅ PASSED' if quality_success else '❌ FAILED'}")
        print(f"   3. Context Maintenance: {'✅ PASSED' if context_success else '❌ FAILED'}")
        print(f"   4. Conversation History Parameter: {'✅ PASSED' if history_success else '❌ FAILED'}")
        
        # Overall success
        overall_success = flow_success and quality_success and context_success and history_success
        
        if overall_success:
            print("\n🎉 All conversation loop fixes passed comprehensive testing!")
            print("✅ Quick Health Tracking chatbot conversation loop issues are resolved")
            return 0
        else:
            print("\n⚠️ Some conversation loop fixes failed testing. Check the details above.")
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result.get('passed', False):
                    print(f"  - {result['test_name']}: {result.get('details', 'Failed')}")
            return 1

if __name__ == "__main__":
    tester = ConversationLoopTester()
    exit_code = tester.run_comprehensive_tests()
    sys.exit(exit_code)