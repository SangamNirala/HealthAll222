#!/usr/bin/env python3
"""
🎯 STEP 4.2 INTELLIGENT FOLLOW-UP SYSTEM FOCUSED TESTING

This test suite validates the enhanced Step 4.2 incompleteness detection system
with better debug logging and improved detection logic as requested in the review.

TESTING SCOPE (5 Priority Scenarios):
1. INCOMPLETE PAIN DESCRIPTIONS - "chest pain" should detect missing pain_quality and pain_severity
2. EMOTIONAL RESPONSES - "scared" should detect emotional_without_medical_details  
3. TEMPORAL VAGUENESS - "recently" should detect vague_temporal_information
4. VERIFY WORKING CASES - "I'm not feeling well" should still trigger vague_symptom_description
5. VERIFY WORKING CASES - "chest" should still trigger incomplete_anatomical_description

TARGET: 100% SUCCESS RATE - All 5 specific test cases should pass with proper incompleteness detection
"""

import asyncio
import json
import time
import requests
import sys
from typing import Dict, Any, List
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://healthprobe.preview.emergentagent.com/api"

class Step42FollowUpTester:
    """Focused tester for Step 4.2 Intelligent Follow-up System"""
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_test_result(self, test_name: str, success: bool, details: str, response_time: float = 0):
        """Log individual test results"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "response_time_ms": response_time,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        print(f"   Details: {details}")
        if response_time > 0:
            print(f"   Response Time: {response_time:.2f}ms")
        print()

    async def initialize_consultation(self) -> str:
        """Initialize a consultation and return consultation_id"""
        try:
            request_data = {
                "patient_id": "anonymous",
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.backend_url}/medical-ai/initialize",
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                consultation_id = result.get("consultation_id", "")
                if consultation_id:
                    print(f"✅ Consultation initialized: {consultation_id}")
                    return consultation_id
                else:
                    print("❌ No consultation_id returned")
                    return ""
            else:
                print(f"❌ Initialization failed: HTTP {response.status_code}")
                return ""
                
        except Exception as e:
            print(f"❌ Initialization exception: {str(e)}")
            return ""

    async def send_message(self, consultation_id: str, message: str, context: Dict = None) -> Dict[str, Any]:
        """Send a message and return the response"""
        try:
            request_data = {
                "message": message,
                "consultation_id": consultation_id,
                "patient_id": "anonymous"
            }
            
            if context:
                request_data["context"] = context
            
            start_time = time.time()
            response = requests.post(
                f"{self.backend_url}/medical-ai/message",
                json=request_data,
                timeout=30
            )
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                result["_response_time"] = response_time
                return result
            else:
                return {
                    "error": f"HTTP {response.status_code}: {response.text[:200]}",
                    "_response_time": response_time
                }
                
        except Exception as e:
            return {
                "error": f"Exception: {str(e)}",
                "_response_time": 0
            }

    async def test_incomplete_pain_descriptions(self):
        """
        PRIORITY 1: INCOMPLETE PAIN DESCRIPTIONS
        Test: "chest pain" should detect missing pain_quality and pain_severity
        """
        print("🎯 TESTING PRIORITY 1: INCOMPLETE PAIN DESCRIPTIONS")
        print("=" * 80)
        
        # Initialize consultation
        consultation_id = await self.initialize_consultation()
        if not consultation_id:
            self.log_test_result("Pain Description - Initialization", False, "Failed to initialize consultation")
            return
        
        # Send greeting first
        greeting_response = await self.send_message(consultation_id, "hi")
        if "error" in greeting_response:
            self.log_test_result("Pain Description - Greeting", False, f"Greeting failed: {greeting_response['error']}")
            return
        
        # Test incomplete pain description
        pain_response = await self.send_message(consultation_id, "chest pain")
        response_time = pain_response.get("_response_time", 0)
        
        if "error" in pain_response:
            self.log_test_result(
                "Incomplete Pain Description - chest pain",
                False,
                f"Request failed: {pain_response['error']}",
                response_time
            )
            return
        
        # Check for incompleteness detection
        response_text = pain_response.get("response", "").lower()
        next_questions = pain_response.get("next_questions", [])
        
        # Look for pain quality/severity follow-up questions
        pain_quality_detected = any(
            keyword in response_text for keyword in [
                "crushing", "pressure", "sharp", "burning", "stabbing", 
                "quality", "describe", "type of pain", "kind of pain"
            ]
        )
        
        pain_severity_detected = any(
            keyword in response_text for keyword in [
                "severity", "scale", "1 to 10", "how bad", "intense", "severe"
            ]
        )
        
        cardiovascular_context = any(
            keyword in response_text for keyword in [
                "heart", "cardiac", "cardiovascular", "chest pain"
            ]
        )
        
        # Check if this is domain-specific cardiovascular follow-up
        domain_specific_followup = pain_quality_detected and cardiovascular_context
        
        success = domain_specific_followup or (pain_quality_detected and pain_severity_detected)
        
        details = f"Pain quality follow-up: {pain_quality_detected}, Pain severity follow-up: {pain_severity_detected}, Cardiovascular context: {cardiovascular_context}, Domain-specific: {domain_specific_followup}"
        
        self.log_test_result(
            "Incomplete Pain Description - chest pain",
            success,
            details,
            response_time
        )

    async def test_emotional_responses(self):
        """
        PRIORITY 2: EMOTIONAL RESPONSES
        Test: "scared" should detect emotional_without_medical_details
        """
        print("🎯 TESTING PRIORITY 2: EMOTIONAL RESPONSES")
        print("=" * 80)
        
        # Initialize consultation
        consultation_id = await self.initialize_consultation()
        if not consultation_id:
            self.log_test_result("Emotional Response - Initialization", False, "Failed to initialize consultation")
            return
        
        # Send greeting first
        greeting_response = await self.send_message(consultation_id, "hi")
        if "error" in greeting_response:
            self.log_test_result("Emotional Response - Greeting", False, f"Greeting failed: {greeting_response['error']}")
            return
        
        # Test emotional response
        emotional_response = await self.send_message(consultation_id, "scared")
        response_time = emotional_response.get("_response_time", 0)
        
        if "error" in emotional_response:
            self.log_test_result(
                "Emotional Response - scared",
                False,
                f"Request failed: {emotional_response['error']}",
                response_time
            )
            return
        
        # Check for empathetic emotional follow-up
        response_text = emotional_response.get("response", "").lower()
        
        # Look for empathetic response asking for underlying symptoms
        empathetic_language = any(
            keyword in response_text for keyword in [
                "understand", "sorry", "help", "support", "concern", "worried"
            ]
        )
        
        medical_details_request = any(
            keyword in response_text for keyword in [
                "symptoms", "feeling", "experiencing", "what's", "tell me", 
                "describe", "happening", "physical", "body"
            ]
        )
        
        emotional_acknowledgment = any(
            keyword in response_text for keyword in [
                "scared", "fear", "anxiety", "worried", "frightened"
            ]
        )
        
        # Check if this is an empathetic response asking for underlying symptoms
        empathetic_followup = empathetic_language and medical_details_request
        
        success = empathetic_followup or (emotional_acknowledgment and medical_details_request)
        
        details = f"Empathetic language: {empathetic_language}, Medical details request: {medical_details_request}, Emotional acknowledgment: {emotional_acknowledgment}, Empathetic follow-up: {empathetic_followup}"
        
        self.log_test_result(
            "Emotional Response - scared",
            success,
            details,
            response_time
        )

    async def test_temporal_vagueness(self):
        """
        PRIORITY 3: TEMPORAL VAGUENESS
        Test: "recently" should detect vague_temporal_information
        """
        print("🎯 TESTING PRIORITY 3: TEMPORAL VAGUENESS")
        print("=" * 80)
        
        # Initialize consultation
        consultation_id = await self.initialize_consultation()
        if not consultation_id:
            self.log_test_result("Temporal Vagueness - Initialization", False, "Failed to initialize consultation")
            return
        
        # Send greeting first
        greeting_response = await self.send_message(consultation_id, "hi")
        if "error" in greeting_response:
            self.log_test_result("Temporal Vagueness - Greeting", False, f"Greeting failed: {greeting_response['error']}")
            return
        
        # Test temporal vagueness
        temporal_response = await self.send_message(consultation_id, "recently")
        response_time = temporal_response.get("_response_time", 0)
        
        if "error" in temporal_response:
            self.log_test_result(
                "Temporal Vagueness - recently",
                False,
                f"Request failed: {temporal_response['error']}",
                response_time
            )
            return
        
        # Check for temporal clarification follow-up
        response_text = temporal_response.get("response", "").lower()
        
        # Look for specific timeframe clarification
        timeframe_clarification = any(
            keyword in response_text for keyword in [
                "when", "how long", "specific", "exactly", "timeframe", 
                "hours", "days", "weeks", "months", "time"
            ]
        )
        
        temporal_specificity_request = any(
            keyword in response_text for keyword in [
                "specific", "exactly", "precise", "clarify", "more details"
            ]
        )
        
        temporal_options = any(
            keyword in response_text for keyword in [
                "hours", "days", "weeks", "yesterday", "today", "this week"
            ]
        )
        
        # Check if this asks for specific timeframe
        temporal_followup = timeframe_clarification and (temporal_specificity_request or temporal_options)
        
        success = temporal_followup or timeframe_clarification
        
        details = f"Timeframe clarification: {timeframe_clarification}, Specificity request: {temporal_specificity_request}, Temporal options: {temporal_options}, Temporal follow-up: {temporal_followup}"
        
        self.log_test_result(
            "Temporal Vagueness - recently",
            success,
            details,
            response_time
        )

    async def test_working_case_vague_symptom(self):
        """
        PRIORITY 4: VERIFY WORKING CASES
        Test: "I'm not feeling well" should still trigger vague_symptom_description follow-up
        """
        print("🎯 TESTING PRIORITY 4: VERIFY WORKING CASE - VAGUE SYMPTOM")
        print("=" * 80)
        
        # Initialize consultation
        consultation_id = await self.initialize_consultation()
        if not consultation_id:
            self.log_test_result("Working Case Vague - Initialization", False, "Failed to initialize consultation")
            return
        
        # Send greeting first
        greeting_response = await self.send_message(consultation_id, "hi")
        if "error" in greeting_response:
            self.log_test_result("Working Case Vague - Greeting", False, f"Greeting failed: {greeting_response['error']}")
            return
        
        # Test vague symptom description
        vague_response = await self.send_message(consultation_id, "I'm not feeling well")
        response_time = vague_response.get("_response_time", 0)
        
        if "error" in vague_response:
            self.log_test_result(
                "Working Case - I'm not feeling well",
                False,
                f"Request failed: {vague_response['error']}",
                response_time
            )
            return
        
        # Check for vague symptom follow-up
        response_text = vague_response.get("response", "").lower()
        
        # Look for specific symptom clarification
        symptom_clarification = any(
            keyword in response_text for keyword in [
                "specific", "symptoms", "describe", "tell me more", "what exactly",
                "details", "experiencing", "feeling", "bothering"
            ]
        )
        
        medical_inquiry = any(
            keyword in response_text for keyword in [
                "pain", "nausea", "headache", "fever", "tired", "dizzy", "symptoms"
            ]
        )
        
        follow_up_questions = any(
            keyword in response_text for keyword in [
                "?", "can you", "could you", "would you", "please tell", "help me understand"
            ]
        )
        
        # Check if this is appropriate vague symptom follow-up
        vague_symptom_followup = symptom_clarification and follow_up_questions
        
        success = vague_symptom_followup or (symptom_clarification and medical_inquiry)
        
        details = f"Symptom clarification: {symptom_clarification}, Medical inquiry: {medical_inquiry}, Follow-up questions: {follow_up_questions}, Vague symptom follow-up: {vague_symptom_followup}"
        
        self.log_test_result(
            "Working Case - I'm not feeling well",
            success,
            details,
            response_time
        )

    async def test_working_case_anatomical(self):
        """
        PRIORITY 5: VERIFY WORKING CASES
        Test: "chest" should still trigger incomplete_anatomical_description follow-up
        """
        print("🎯 TESTING PRIORITY 5: VERIFY WORKING CASE - ANATOMICAL")
        print("=" * 80)
        
        # Initialize consultation
        consultation_id = await self.initialize_consultation()
        if not consultation_id:
            self.log_test_result("Working Case Anatomical - Initialization", False, "Failed to initialize consultation")
            return
        
        # Send greeting first
        greeting_response = await self.send_message(consultation_id, "hi")
        if "error" in greeting_response:
            self.log_test_result("Working Case Anatomical - Greeting", False, f"Greeting failed: {greeting_response['error']}")
            return
        
        # Test incomplete anatomical description
        anatomical_response = await self.send_message(consultation_id, "chest")
        response_time = anatomical_response.get("_response_time", 0)
        
        if "error" in anatomical_response:
            self.log_test_result(
                "Working Case - chest",
                False,
                f"Request failed: {anatomical_response['error']}",
                response_time
            )
            return
        
        # Check for anatomical follow-up
        response_text = anatomical_response.get("response", "").lower()
        
        # Look for anatomical clarification
        anatomical_clarification = any(
            keyword in response_text for keyword in [
                "chest", "what about", "tell me more", "describe", "experiencing",
                "feeling", "symptoms", "problem", "issue"
            ]
        )
        
        symptom_inquiry = any(
            keyword in response_text for keyword in [
                "pain", "discomfort", "pressure", "tightness", "burning", 
                "ache", "symptoms", "feeling"
            ]
        )
        
        follow_up_questions = any(
            keyword in response_text for keyword in [
                "?", "can you", "could you", "would you", "please", "help me"
            ]
        )
        
        # Check if this is appropriate anatomical follow-up
        anatomical_followup = anatomical_clarification and follow_up_questions
        
        success = anatomical_followup or (anatomical_clarification and symptom_inquiry)
        
        details = f"Anatomical clarification: {anatomical_clarification}, Symptom inquiry: {symptom_inquiry}, Follow-up questions: {follow_up_questions}, Anatomical follow-up: {anatomical_followup}"
        
        self.log_test_result(
            "Working Case - chest",
            success,
            details,
            response_time
        )

    async def run_focused_tests(self):
        """Run all focused tests for Step 4.2 Intelligent Follow-up System"""
        print("🎯 STEP 4.2 INTELLIGENT FOLLOW-UP SYSTEM FOCUSED TESTING")
        print("=" * 100)
        print(f"Backend URL: {self.backend_url}")
        print(f"Test Start Time: {datetime.now().isoformat()}")
        print("=" * 100)
        print()
        
        # Run all priority test scenarios
        await self.test_incomplete_pain_descriptions()
        await self.test_emotional_responses()
        await self.test_temporal_vagueness()
        await self.test_working_case_vague_symptom()
        await self.test_working_case_anatomical()
        
        # Generate final report
        self.generate_final_report()

    def generate_final_report(self):
        """Generate focused final test report"""
        print("=" * 100)
        print("🎯 STEP 4.2 INTELLIGENT FOLLOW-UP SYSTEM - FOCUSED TEST REPORT")
        print("=" * 100)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed Tests: {self.passed_tests}")
        print(f"   Failed Tests: {self.total_tests - self.passed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        # Priority scenario results
        print("🎯 PRIORITY SCENARIO RESULTS:")
        priority_scenarios = [
            "Incomplete Pain Description - chest pain",
            "Emotional Response - scared", 
            "Temporal Vagueness - recently",
            "Working Case - I'm not feeling well",
            "Working Case - chest"
        ]
        
        for scenario in priority_scenarios:
            result = next((r for r in self.test_results if r["test_name"] == scenario), None)
            if result:
                status = "✅ PASS" if result["success"] else "❌ FAIL"
                print(f"   {status} {scenario}")
                if not result["success"]:
                    print(f"      Issue: {result['details']}")
        print()
        
        # Enhanced detection analysis
        print("🔍 ENHANCED DETECTION ANALYSIS:")
        
        # Check pain detection enhancement
        pain_test = next((r for r in self.test_results if "chest pain" in r["test_name"]), None)
        if pain_test:
            pain_working = pain_test["success"]
            print(f"   ✅ Pain Quality/Severity Detection: {'WORKING' if pain_working else 'NEEDS WORK'}")
        
        # Check emotional response enhancement
        emotional_test = next((r for r in self.test_results if "scared" in r["test_name"]), None)
        if emotional_test:
            emotional_working = emotional_test["success"]
            print(f"   ✅ Emotional Response Detection: {'WORKING' if emotional_working else 'NEEDS WORK'}")
        
        # Check temporal enhancement
        temporal_test = next((r for r in self.test_results if "recently" in r["test_name"]), None)
        if temporal_test:
            temporal_working = temporal_test["success"]
            print(f"   ✅ Temporal Vagueness Detection: {'WORKING' if temporal_working else 'NEEDS WORK'}")
        
        # Check working cases preservation
        working_cases = [r for r in self.test_results if "Working Case" in r["test_name"]]
        working_preserved = all(r["success"] for r in working_cases)
        print(f"   ✅ Previously Working Cases: {'PRESERVED' if working_preserved else 'BROKEN'}")
        print()
        
        # Debug logging assessment
        print("🐛 DEBUG LOGGING ASSESSMENT:")
        print("   Note: Debug logging validation requires backend log access")
        print("   Expected: Comprehensive debug logs for incompleteness detection")
        print("   Expected: Reordered detection priority with emotional responses checked earlier")
        print("   Expected: Enhanced pain detection with quality/severity descriptors")
        print()
        
        # Final assessment
        print("🎯 STEP 4.2 ENHANCEMENT ASSESSMENT:")
        if success_rate == 100:
            print("🎉 EXCELLENT: All 5 priority scenarios pass - Step 4.2 enhancements are working perfectly!")
            print("   ✅ Incomplete pain descriptions detected correctly")
            print("   ✅ Emotional responses trigger empathetic follow-up")
            print("   ✅ Temporal vagueness prompts specific timeframe requests")
            print("   ✅ Previously working cases still function correctly")
        elif success_rate >= 80:
            print("⚠️  GOOD: Most scenarios pass - Step 4.2 enhancements are mostly working")
            print("   Some fine-tuning may be needed for optimal performance")
        elif success_rate >= 60:
            print("⚠️  PARTIAL: Some scenarios pass - Step 4.2 enhancements need work")
            print("   Core functionality present but detection logic needs improvement")
        else:
            print("❌ NEEDS WORK: Multiple scenarios fail - Step 4.2 enhancements not working")
            print("   Significant issues with incompleteness detection system")
        
        print()
        print(f"Test Completion Time: {datetime.now().isoformat()}")
        print("=" * 100)

async def main():
    """Main test execution function"""
    tester = Step42FollowUpTester()
    await tester.run_focused_tests()

if __name__ == "__main__":
    asyncio.run(main())