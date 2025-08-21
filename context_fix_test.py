#!/usr/bin/env python3
"""
🔧 CONTEXT FIX COMPREHENSIVE TESTING SUITE 🔧

CRITICAL TESTING: Tests the EXACT issue identified in the review request.
The main issue was API context handling between requests - proper API calls 
must include the complete context object from previous responses, not just consultation_id.

EXACT CONVERSATION FLOW TO TEST:
initialize → 'hi' → 'I have a headache' → 'it has started 2 days before' → 'it is dull' → 'food' → 'position'

KEY REQUIREMENT: When making API calls, ensure you pass the full 'context' object 
from previous API responses, not just the consultation_id. The server requires 
the complete context to maintain conversation state.

Author: Testing Agent  
Date: 2025-01-17
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://nlptest-phase7.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class ContextFixTester:
    """Test the context passing fix for conversation loop"""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_test(self, test_name: str, passed: bool, details: str = ""):
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
            "timestamp": datetime.now().isoformat()
        }
        
        self.test_results.append(result)
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        print()

    def test_with_proper_context_passing(self) -> bool:
        """
        🎯 TEST WITH PROPER CONTEXT PASSING
        
        Test the exact conversation flow with proper context object passing
        """
        print("\n🎯 TESTING WITH PROPER CONTEXT PASSING")
        print("-" * 60)
        
        # Step 1: Initialize conversation
        print("Step 1: Initialize conversation...")
        try:
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
                json={
                    "patient_id": "anonymous",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Initialize Conversation", False, f"HTTP {init_response.status_code}")
                return False
                
            init_data = init_response.json()
            consultation_id = init_data.get("consultation_id")
            full_context = init_data.get("context", {})  # CRITICAL: Get full context
            
            print(f"   Consultation ID: {consultation_id}")
            print(f"   Context keys: {list(full_context.keys())}")
            
        except Exception as e:
            self.log_test("Initialize Conversation", False, f"Exception: {str(e)}")
            return False
        
        # Conversation steps with proper context passing
        conversation_steps = [
            ("hi", "Greeting"),
            ("I have a headache", "Symptom recognition"),
            ("it has started 2 days before", "HPI timing"),
            ("it is dull", "HPI quality"),
            ("food", "HPI aggravating factors"),
            ("position", "HPI positional factors")
        ]
        
        all_passed = True
        conversation_log = []
        
        for step_num, (message, description) in enumerate(conversation_steps, 1):
            print(f"\nStep {step_num + 1}: '{message}' ({description})")
            
            try:
                # CRITICAL: Pass the FULL context object, not just consultation_id
                request_payload = {
                    "message": message,
                    "context": full_context,  # Full context object from previous response
                    "consultation_id": consultation_id,
                    "conversation_history": []
                }
                
                print(f"   Sending context keys: {list(full_context.keys())}")
                
                response = requests.post(f"{API_BASE}/medical-ai/message",
                    json=request_payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # CRITICAL: Update context for next request
                    full_context = data.get("context", full_context)
                    
                    response_text = data.get("response", "")
                    current_stage = data.get("current_stage", "")
                    urgency = data.get("urgency", "")
                    
                    # Check for success indicators
                    no_generic_fallback = "I understand you'd like to discuss something health-related" not in response_text
                    has_meaningful_response = len(response_text) > 50
                    no_technical_error = "technical issue" not in response_text.lower()
                    
                    step_success = no_generic_fallback and has_meaningful_response and no_technical_error
                    
                    conversation_log.append({
                        "step": step_num + 1,
                        "message": message,
                        "response_preview": response_text[:100] + "..." if len(response_text) > 100 else response_text,
                        "stage": current_stage,
                        "urgency": urgency,
                        "success": step_success,
                        "generic_fallback": not no_generic_fallback
                    })
                    
                    if step_success:
                        print(f"   ✅ SUCCESS: Stage: {current_stage}, Response: {len(response_text)} chars")
                    else:
                        print(f"   ❌ FAILED: Generic fallback: {not no_generic_fallback}, Response length: {len(response_text)}")
                        all_passed = False
                        
                else:
                    print(f"   ❌ HTTP {response.status_code}: {response.text}")
                    all_passed = False
                    
            except Exception as e:
                print(f"   ❌ Exception: {str(e)}")
                all_passed = False
        
        # Print conversation summary
        print(f"\n📋 CONVERSATION SUMMARY:")
        for entry in conversation_log:
            status = "✅" if entry["success"] else "❌"
            fallback_note = " (GENERIC FALLBACK)" if entry["generic_fallback"] else ""
            print(f"   {status} Step {entry['step']}: '{entry['message']}' → {entry['response_preview']}{fallback_note}")
        
        # Overall assessment
        success_count = sum(1 for entry in conversation_log if entry["success"])
        total_steps = len(conversation_log)
        
        if all_passed:
            self.log_test("Proper Context Passing", True, 
                        f"All {total_steps} conversation steps successful with proper context passing")
        else:
            self.log_test("Proper Context Passing", False,
                        f"Only {success_count}/{total_steps} steps successful. Context passing issues detected.")
        
        return all_passed

    def test_without_proper_context(self) -> bool:
        """
        🚫 TEST WITHOUT PROPER CONTEXT (CONTROL TEST)
        
        Test the same flow but only passing consultation_id to demonstrate the issue
        """
        print("\n🚫 TESTING WITHOUT PROPER CONTEXT (CONTROL TEST)")
        print("-" * 60)
        
        # Initialize conversation
        try:
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
                json={
                    "patient_id": "anonymous",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Control Test - Initialize", False, f"HTTP {init_response.status_code}")
                return False
                
            init_data = init_response.json()
            consultation_id = init_data.get("consultation_id")
            
        except Exception as e:
            self.log_test("Control Test - Initialize", False, f"Exception: {str(e)}")
            return False
        
        # Test with only consultation_id (the wrong way)
        print("Testing 'I have a headache' with only consultation_id...")
        
        try:
            # WRONG WAY: Only pass consultation_id, not full context
            request_payload = {
                "message": "I have a headache",
                "consultation_id": consultation_id,  # Only consultation_id
                "conversation_history": []
                # Missing: "context": full_context
            }
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json=request_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "")
                
                # This should likely fail or give generic response
                has_generic_fallback = "I understand you'd like to discuss something health-related" in response_text
                
                if has_generic_fallback:
                    self.log_test("Control Test - Without Context", True,
                                "Confirmed: Without proper context, conversation fails with generic fallback")
                    return True
                else:
                    self.log_test("Control Test - Without Context", False,
                                "Unexpected: Conversation worked without proper context")
                    return False
            else:
                self.log_test("Control Test - Without Context", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Control Test - Without Context", False, f"Exception: {str(e)}")
            return False

    def test_context_object_structure(self) -> bool:
        """
        🔍 TEST CONTEXT OBJECT STRUCTURE
        
        Analyze the structure of the context object to understand what's required
        """
        print("\n🔍 TESTING CONTEXT OBJECT STRUCTURE")
        print("-" * 60)
        
        try:
            # Initialize and get context
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
                json={
                    "patient_id": "anonymous",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code == 200:
                init_data = init_response.json()
                context = init_data.get("context", {})
                
                print(f"Context object structure:")
                print(json.dumps(context, indent=2))
                
                # Check for required fields
                has_consultation_id = "consultation_id" in context
                has_patient_id = "patient_id" in context
                has_stage = "current_stage" in context
                has_medical_context = "medical_context" in context
                
                required_fields = has_consultation_id and has_patient_id and has_stage
                
                if required_fields:
                    self.log_test("Context Object Structure", True,
                                f"Context has required fields: consultation_id, patient_id, current_stage")
                else:
                    self.log_test("Context Object Structure", False,
                                f"Missing required fields - ID: {has_consultation_id}, Patient: {has_patient_id}, Stage: {has_stage}")
                
                return required_fields
            else:
                self.log_test("Context Object Structure", False, f"HTTP {init_response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Context Object Structure", False, f"Exception: {str(e)}")
            return False

    def run_comprehensive_tests(self):
        """Run comprehensive context fix tests"""
        print("🚀 Starting Context Fix Tests...")
        print(f"   Base URL: {API_BASE}")
        print("=" * 80)
        
        # Test 1: Context Object Structure
        print("\n🎯 TESTING PHASE 1: CONTEXT OBJECT STRUCTURE")
        structure_success = self.test_context_object_structure()
        
        # Test 2: Proper Context Passing
        print("\n🎯 TESTING PHASE 2: PROPER CONTEXT PASSING")
        proper_context_success = self.test_with_proper_context_passing()
        
        # Test 3: Control Test (Without Proper Context)
        print("\n🎯 TESTING PHASE 3: CONTROL TEST (WITHOUT PROPER CONTEXT)")
        control_success = self.test_without_proper_context()
        
        # Print final results
        print("\n" + "=" * 80)
        print(f"📊 FINAL RESULTS")
        print(f"Tests Run: {self.total_tests}")
        print(f"Tests Passed: {self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        print(f"\n🎯 CONTEXT FIX TEST RESULTS:")
        print(f"   1. Context Object Structure: {'✅ PASSED' if structure_success else '❌ FAILED'}")
        print(f"   2. Proper Context Passing: {'✅ PASSED' if proper_context_success else '❌ FAILED'}")
        print(f"   3. Control Test (Without Context): {'✅ PASSED' if control_success else '❌ FAILED'}")
        
        # Key findings
        if proper_context_success:
            print("\n🎉 CONTEXT FIX VALIDATION SUCCESSFUL!")
            print("✅ Proper context passing resolves the conversation loop issue")
            print("✅ The exact conversation flow works when full context is passed")
            return 0
        else:
            print("\n⚠️ CONTEXT FIX VALIDATION FAILED!")
            print("❌ Conversation still fails even with proper context passing")
            print("❌ Additional investigation needed beyond context handling")
            
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result.get('passed', False):
                    print(f"  - {result['test_name']}: {result.get('details', 'Failed')}")
            return 1

if __name__ == "__main__":
    tester = ContextFixTester()
    exit_code = tester.run_comprehensive_tests()
    sys.exit(exit_code)