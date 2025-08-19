#!/usr/bin/env python3
"""
🩺 MEDICAL CHATBOT CONVERSATION FLOW TESTING SUITE 🩺

Comprehensive backend testing for the medical chatbot conversation flow fix
as requested in the review. Tests the specific conversation flow mentioned by the user:

CRITICAL TEST SCENARIOS:
1. Test the exact conversation flow mentioned by user:
   - Initialize conversation  
   - Send "hi" message
   - Send "I have a headache" message
   - Send "it has started 2 days before" 
   - Send "it is dull"
   - Send "food"
   - Send "position"

2. Verify that the conversation progresses properly and doesn't get stuck in loops
3. Check that "I have a headache" is properly recognized as a symptom
4. Ensure that HPI questions use clean symptom names instead of full user messages
5. Validate that conversation_history parameter is working and context is maintained

Author: Testing Agent
Date: 2025-01-19
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, Any, List

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://multi-symptom-engine.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class ConversationFlowTester:
    """Comprehensive tester for Medical Chatbot Conversation Flow"""
    
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
        """Initialize the medical conversation"""
        print("\n🏥 INITIALIZING MEDICAL CONVERSATION")
        print("-" * 50)
        
        try:
            response = requests.post(f"{API_BASE}/medical-ai/initialize",
                json={
                    "patient_id": "anonymous"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.consultation_id = data.get('consultation_id')
                
                # Check required fields
                required_fields = ['consultation_id', 'patient_id', 'current_stage', 'response']
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

    def send_message(self, message: str, expected_stage: str = None, should_progress: bool = True) -> Dict[str, Any]:
        """Send a message and validate response"""
        try:
            # Build conversation history for context
            conversation_history = []
            for msg in self.conversation_history:
                conversation_history.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("message", ""),
                    "timestamp": msg.get("timestamp", datetime.now().isoformat())
                })
            
            # Get the current stage from the last response or default to greeting
            current_stage = "greeting"
            if self.conversation_history:
                for entry in reversed(self.conversation_history):
                    if entry.get("role") == "assistant" and entry.get("stage"):
                        current_stage = entry.get("stage")
                        break
            
            request_data = {
                "patient_id": "anonymous",
                "message": message,
                "consultation_id": self.consultation_id,
                "conversation_history": conversation_history,
                "context": {
                    "patient_id": "anonymous",
                    "consultation_id": self.consultation_id,
                    "current_stage": current_stage,
                    "demographics": {}
                }
            }
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Store conversation history
                self.conversation_history.append({
                    "role": "user",
                    "message": message,
                    "timestamp": datetime.now().isoformat(),
                    "stage": data.get('current_stage', 'unknown')
                })
                
                self.conversation_history.append({
                    "role": "assistant",
                    "message": data.get('response', ''),
                    "timestamp": datetime.now().isoformat(),
                    "stage": data.get('current_stage', 'unknown')
                })
                
                return data
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
                
        except Exception as e:
            return {"error": f"Exception: {str(e)}"}

    def test_exact_conversation_flow(self) -> bool:
        """Test the exact conversation flow mentioned by the user"""
        print("\n🎯 TESTING EXACT CONVERSATION FLOW")
        print("-" * 50)
        
        all_passed = True
        
        # Step 1: Send "hi" message
        print("Step 1: Sending 'hi' message...")
        response1 = self.send_message("hi")
        
        if "error" not in response1:
            stage = response1.get('current_stage', '')
            response_text = response1.get('response', '')
            
            # Check if greeting is handled properly
            greeting_handled = len(response_text) > 0 and not response_text.startswith("I apologize")
            
            if greeting_handled:
                self.log_test("Step 1: Hi Message", True,
                            f"Stage: {stage}, Response length: {len(response_text)} chars")
            else:
                self.log_test("Step 1: Hi Message", False,
                            f"Greeting not handled properly. Response: {response_text[:100]}...")
                all_passed = False
        else:
            self.log_test("Step 1: Hi Message", False, response1["error"])
            all_passed = False
        
        # Step 2: Send "I have a headache" message
        print("Step 2: Sending 'I have a headache' message...")
        response2 = self.send_message("I have a headache")
        
        if "error" not in response2:
            stage = response2.get('current_stage', '')
            response_text = response2.get('response', '')
            urgency = response2.get('urgency', '')
            
            # Critical check: Should NOT return "unclear_intent"
            unclear_intent = "unclear_intent" in response_text.lower() or "unclear" in response_text.lower()
            
            # Check if symptom is properly recognized
            symptom_recognized = not unclear_intent and len(response_text) > 50
            
            # Check if response contains clean symptom name in questions (not full user message)
            contains_full_message = "I have a headache" in response_text
            contains_clean_symptom = "headache" in response_text.lower()
            
            if symptom_recognized and not contains_full_message:
                self.log_test("Step 2: I have a headache", True,
                            f"Symptom recognized, Stage: {stage}, Urgency: {urgency}, Clean symptom used: {contains_clean_symptom}")
            else:
                details = []
                if unclear_intent:
                    details.append("Returns unclear_intent")
                if contains_full_message:
                    details.append("Uses full user message instead of clean symptom")
                if not symptom_recognized:
                    details.append("Symptom not properly recognized")
                
                self.log_test("Step 2: I have a headache", False,
                            f"Issues: {', '.join(details)}. Response: {response_text[:200]}...")
                all_passed = False
        else:
            self.log_test("Step 2: I have a headache", False, response2["error"])
            all_passed = False
        
        # Step 3: Send "it has started 2 days before"
        print("Step 3: Sending 'it has started 2 days before' message...")
        response3 = self.send_message("it has started 2 days before")
        
        if "error" not in response3:
            stage = response3.get('current_stage', '')
            response_text = response3.get('response', '')
            
            # Check if temporal information is processed
            temporal_processed = len(response_text) > 30 and not response_text.startswith("I apologize")
            
            if temporal_processed:
                self.log_test("Step 3: Temporal Information", True,
                            f"Temporal info processed, Stage: {stage}")
            else:
                self.log_test("Step 3: Temporal Information", False,
                            f"Temporal info not processed properly. Response: {response_text[:100]}...")
                all_passed = False
        else:
            self.log_test("Step 3: Temporal Information", False, response3["error"])
            all_passed = False
        
        # Step 4: Send "it is dull"
        print("Step 4: Sending 'it is dull' message...")
        response4 = self.send_message("it is dull")
        
        if "error" not in response4:
            stage = response4.get('current_stage', '')
            response_text = response4.get('response', '')
            
            # Check if quality information is processed
            quality_processed = len(response_text) > 30 and not response_text.startswith("I apologize")
            
            if quality_processed:
                self.log_test("Step 4: Quality Information", True,
                            f"Quality info processed, Stage: {stage}")
            else:
                self.log_test("Step 4: Quality Information", False,
                            f"Quality info not processed properly. Response: {response_text[:100]}...")
                all_passed = False
        else:
            self.log_test("Step 4: Quality Information", False, response4["error"])
            all_passed = False
        
        # Step 5: Send "food"
        print("Step 5: Sending 'food' message...")
        response5 = self.send_message("food")
        
        if "error" not in response5:
            stage = response5.get('current_stage', '')
            response_text = response5.get('response', '')
            
            # Check if trigger information is processed
            trigger_processed = len(response_text) > 30 and not response_text.startswith("I apologize")
            
            if trigger_processed:
                self.log_test("Step 5: Trigger Information", True,
                            f"Trigger info processed, Stage: {stage}")
            else:
                self.log_test("Step 5: Trigger Information", False,
                            f"Trigger info not processed properly. Response: {response_text[:100]}...")
                all_passed = False
        else:
            self.log_test("Step 5: Trigger Information", False, response5["error"])
            all_passed = False
        
        # Step 6: Send "position"
        print("Step 6: Sending 'position' message...")
        response6 = self.send_message("position")
        
        if "error" not in response6:
            stage = response6.get('current_stage', '')
            response_text = response6.get('response', '')
            
            # Check if positional information is processed
            position_processed = len(response_text) > 30 and not response_text.startswith("I apologize")
            
            if position_processed:
                self.log_test("Step 6: Position Information", True,
                            f"Position info processed, Stage: {stage}")
            else:
                self.log_test("Step 6: Position Information", False,
                            f"Position info not processed properly. Response: {response_text[:100]}...")
                all_passed = False
        else:
            self.log_test("Step 6: Position Information", False, response6["error"])
            all_passed = False
        
        return all_passed

    def test_conversation_progression(self) -> bool:
        """Test that conversation progresses properly without loops"""
        print("\n🔄 TESTING CONVERSATION PROGRESSION")
        print("-" * 50)
        
        # Analyze conversation history for loops
        stages_seen = []
        questions_asked = []
        
        for entry in self.conversation_history:
            if entry.get("role") == "assistant":
                stage = entry.get("stage", "unknown")
                response = entry.get("message", "")
                
                stages_seen.append(stage)
                
                # Extract questions (lines ending with ?)
                questions = [line.strip() for line in response.split('\n') if line.strip().endswith('?')]
                questions_asked.extend(questions)
        
        # Check for stage progression
        unique_stages = list(set(stages_seen))
        stage_progression = len(unique_stages) > 1 or len(stages_seen) <= 3
        
        # Check for repeated questions (indicating loops)
        question_counts = {}
        for question in questions_asked:
            question_counts[question] = question_counts.get(question, 0) + 1
        
        repeated_questions = [q for q, count in question_counts.items() if count > 2]
        no_loops = len(repeated_questions) == 0
        
        if stage_progression and no_loops:
            self.log_test("Conversation Progression", True,
                        f"Stages: {unique_stages}, No repeated questions detected")
            return True
        else:
            issues = []
            if not stage_progression:
                issues.append("No stage progression")
            if not no_loops:
                issues.append(f"Repeated questions: {repeated_questions}")
            
            self.log_test("Conversation Progression", False,
                        f"Issues: {', '.join(issues)}")
            return False

    def test_symptom_recognition(self) -> bool:
        """Test that 'I have a headache' is properly recognized as a symptom"""
        print("\n🧠 TESTING SYMPTOM RECOGNITION")
        print("-" * 50)
        
        # Find the response to "I have a headache"
        headache_response = None
        for i, entry in enumerate(self.conversation_history):
            if entry.get("role") == "user" and entry.get("message") == "I have a headache":
                if i + 1 < len(self.conversation_history):
                    headache_response = self.conversation_history[i + 1]
                break
        
        if not headache_response:
            self.log_test("Symptom Recognition", False, "Could not find response to 'I have a headache'")
            return False
        
        response_text = headache_response.get("message", "")
        
        # Check that it doesn't return unclear_intent
        unclear_intent = "unclear_intent" in response_text.lower() or "unclear" in response_text.lower()
        
        # Check that it recognizes it as a medical symptom
        medical_response = any(keyword in response_text.lower() for keyword in 
                             ["pain", "symptom", "headache", "medical", "describe", "tell me more"])
        
        # Check that response is substantial (not just an error)
        substantial_response = len(response_text) > 50
        
        if not unclear_intent and medical_response and substantial_response:
            self.log_test("Symptom Recognition", True,
                        f"Headache properly recognized as symptom, response length: {len(response_text)}")
            return True
        else:
            issues = []
            if unclear_intent:
                issues.append("Returns unclear_intent")
            if not medical_response:
                issues.append("Not recognized as medical symptom")
            if not substantial_response:
                issues.append("Response too short")
            
            self.log_test("Symptom Recognition", False,
                        f"Issues: {', '.join(issues)}. Response: {response_text[:200]}...")
            return False

    def test_clean_symptom_names(self) -> bool:
        """Test that HPI questions use clean symptom names instead of full user messages"""
        print("\n🧹 TESTING CLEAN SYMPTOM NAMES IN QUESTIONS")
        print("-" * 50)
        
        # Analyze all assistant responses for question formatting
        problematic_responses = []
        clean_responses = []
        
        for entry in self.conversation_history:
            if entry.get("role") == "assistant":
                response = entry.get("message", "")
                
                # Check if response contains the full user message "I have a headache"
                if "I have a headache" in response:
                    problematic_responses.append(response)
                elif "headache" in response.lower():
                    clean_responses.append(response)
        
        # Test passes if we have clean symptom usage and no problematic usage
        has_clean_usage = len(clean_responses) > 0
        no_problematic_usage = len(problematic_responses) == 0
        
        if has_clean_usage and no_problematic_usage:
            self.log_test("Clean Symptom Names", True,
                        f"Clean symptom usage found in {len(clean_responses)} responses, no problematic usage")
            return True
        else:
            issues = []
            if not has_clean_usage:
                issues.append("No clean symptom usage found")
            if not no_problematic_usage:
                issues.append(f"Found {len(problematic_responses)} responses with full user message")
                for resp in problematic_responses[:2]:  # Show first 2 examples
                    issues.append(f"Example: {resp[:100]}...")
            
            self.log_test("Clean Symptom Names", False,
                        f"Issues: {', '.join(issues)}")
            return False

    def test_conversation_history_parameter(self) -> bool:
        """Test that conversation_history parameter is working and context is maintained"""
        print("\n📚 TESTING CONVERSATION HISTORY PARAMETER")
        print("-" * 50)
        
        # Check if context is maintained across messages
        context_maintained = True
        context_issues = []
        
        # Look for evidence of context maintenance in responses
        for i, entry in enumerate(self.conversation_history):
            if entry.get("role") == "assistant" and i > 2:  # After a few exchanges
                response = entry.get("message", "")
                
                # Check if response shows awareness of previous conversation
                # (references to headache, previous answers, etc.)
                shows_context = any(keyword in response.lower() for keyword in 
                                  ["headache", "mentioned", "told", "said", "described", "2 days", "dull"])
                
                if not shows_context and len(response) > 50:
                    context_issues.append(f"Response {i} may lack context awareness")
        
        # If we have few context issues relative to total responses, consider it working
        assistant_responses = len([e for e in self.conversation_history if e.get("role") == "assistant"])
        context_maintained = len(context_issues) < (assistant_responses * 0.5)  # Less than 50% have issues
        
        if context_maintained:
            self.log_test("Conversation History Parameter", True,
                        f"Context maintained across {assistant_responses} responses, {len(context_issues)} potential issues")
            return True
        else:
            self.log_test("Conversation History Parameter", False,
                        f"Context issues: {context_issues}")
            return False

    def run_comprehensive_tests(self):
        """Run comprehensive conversation flow tests"""
        print("🚀 Starting Medical Chatbot Conversation Flow Tests...")
        print(f"   Base URL: {API_BASE}")
        print("=" * 80)
        
        # Initialize conversation
        init_success = self.initialize_conversation()
        if not init_success:
            print("❌ Failed to initialize conversation. Aborting tests.")
            return 1
        
        # Test the exact conversation flow
        print("\n🎯 TESTING PHASE 1: EXACT CONVERSATION FLOW")
        flow_success = self.test_exact_conversation_flow()
        
        # Test conversation progression
        print("\n🎯 TESTING PHASE 2: CONVERSATION PROGRESSION")
        progression_success = self.test_conversation_progression()
        
        # Test symptom recognition
        print("\n🎯 TESTING PHASE 3: SYMPTOM RECOGNITION")
        recognition_success = self.test_symptom_recognition()
        
        # Test clean symptom names
        print("\n🎯 TESTING PHASE 4: CLEAN SYMPTOM NAMES")
        clean_names_success = self.test_clean_symptom_names()
        
        # Test conversation history parameter
        print("\n🎯 TESTING PHASE 5: CONVERSATION HISTORY PARAMETER")
        history_success = self.test_conversation_history_parameter()
        
        # Print conversation history for debugging
        print("\n📝 CONVERSATION HISTORY:")
        print("-" * 50)
        for i, entry in enumerate(self.conversation_history):
            role = entry.get("role", "unknown")
            message = entry.get("message", "")
            stage = entry.get("stage", "unknown")
            print(f"{i+1}. {role.upper()}: {message[:100]}{'...' if len(message) > 100 else ''}")
            print(f"   Stage: {stage}")
            print()
        
        # Print final results
        print("\n" + "=" * 80)
        print(f"📊 FINAL RESULTS")
        print(f"Tests Run: {self.total_tests}")
        print(f"Tests Passed: {self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        print(f"\n🎯 CONVERSATION FLOW TEST RESULTS:")
        print(f"   1. Exact Conversation Flow: {'✅ PASSED' if flow_success else '❌ FAILED'}")
        print(f"   2. Conversation Progression: {'✅ PASSED' if progression_success else '❌ FAILED'}")
        print(f"   3. Symptom Recognition: {'✅ PASSED' if recognition_success else '❌ FAILED'}")
        print(f"   4. Clean Symptom Names: {'✅ PASSED' if clean_names_success else '❌ FAILED'}")
        print(f"   5. Conversation History Parameter: {'✅ PASSED' if history_success else '❌ FAILED'}")
        
        # Overall success
        overall_success = (flow_success and progression_success and recognition_success and 
                          clean_names_success and history_success)
        
        if overall_success:
            print("\n🎉 All conversation flow tests passed!")
            print("✅ Medical chatbot conversation flow issue has been resolved")
            return 0
        else:
            print("\n⚠️ Some conversation flow tests failed. The conversation loop issue may still exist.")
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result.get('passed', False):
                    print(f"  - {result['test_name']}: {result.get('details', 'Failed')}")
            return 1

if __name__ == "__main__":
    tester = ConversationFlowTester()
    exit_code = tester.run_comprehensive_tests()
    sys.exit(exit_code)