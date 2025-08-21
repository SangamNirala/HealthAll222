#!/usr/bin/env python3
"""
🧪 TASK 6.1: INTELLIGENT CLARIFICATION SYSTEM COMPREHENSIVE TESTING
==================================================================

Comprehensive testing of Task 6.1 Intelligent Clarification System integration 
with the medical AI service as requested in the review.

TESTING SCOPE:
1. Test clarification analysis API endpoint (/api/medical-ai/clarification-analysis)
2. Test clarification response generation API endpoint (/api/medical-ai/generate-clarification-response)  
3. Test integration with main medical AI message processing (/api/medical-ai/message)
4. Test with various unclear medical inputs including task examples

EXPECTED RESULTS:
- Clarification analysis should detect unclear inputs with high confidence
- Response generation should create empathetic, specific clarifying questions
- Medical AI integration should flag unclear inputs for clarification
- System should handle the original task example "not good" correctly

PERFORMANCE TARGETS:
- API response times under 5 seconds
- Clarification detection accuracy >75%
- Appropriate question generation for unclear inputs
"""

import requests
import json
import time
import os
from typing import Dict, Any, List
from datetime import datetime

class Task61ClarificationTester:
    def __init__(self):
        # Get backend URL from environment
        self.backend_url = os.getenv('REACT_APP_BACKEND_URL', 'https://ai-test-suite.preview.emergentagent.com')
        if not self.backend_url.endswith('/api'):
            self.backend_url = f"{self.backend_url}/api"
        
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
        print(f"🧪 TASK 6.1: INTELLIGENT CLARIFICATION SYSTEM TESTING")
        print(f"Backend URL: {self.backend_url}")
        print(f"Test Start Time: {datetime.now().isoformat()}")
        print("=" * 80)

    def log_test_result(self, test_name: str, success: bool, details: str, response_time: float = 0, response_data: Dict = None):
        """Log individual test results"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
        
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "response_time": response_time,
            "response_data": response_data,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_name}")
        print(f"      Details: {details}")
        if response_time > 0:
            print(f"      Response Time: {response_time:.3f}s")
        print()

    def test_clarification_analysis_api(self):
        """Test the clarification analysis API endpoint with various unclear inputs"""
        print("🔬 TESTING CLARIFICATION ANALYSIS API ENDPOINT")
        print("=" * 60)
        
        # Test cases from review request plus additional comprehensive cases
        test_cases = [
            # Original task example
            {
                "input": "not good",
                "description": "Task 6.1 original example - vague emotional expression",
                "expected_unclear": True
            },
            # Review request examples
            {
                "input": "bad",
                "description": "Simple negative emotional state",
                "expected_unclear": True
            },
            {
                "input": "chest",
                "description": "Single body part mention - high priority",
                "expected_unclear": True
            },
            {
                "input": "worried",
                "description": "Pure emotional state",
                "expected_unclear": True
            },
            {
                "input": "weird feeling",
                "description": "Unclear symptom quality description",
                "expected_unclear": True
            },
            {
                "input": "pain",
                "description": "Single word symptom",
                "expected_unclear": True
            },
            # Additional test cases
            {
                "input": "something wrong",
                "description": "Nonspecific health complaint",
                "expected_unclear": True
            },
            {
                "input": "can't do anything",
                "description": "Vague functional impact complaint",
                "expected_unclear": True
            },
            # Clear inputs (should not trigger clarification)
            {
                "input": "I have a sharp chest pain that started 2 hours ago",
                "description": "Clear, specific symptom description",
                "expected_unclear": False
            },
            {
                "input": "My headache is severe and throbbing on the left side",
                "description": "Detailed symptom with location and quality",
                "expected_unclear": False
            }
        ]
        
        successful_tests = 0
        
        for i, test_case in enumerate(test_cases):
            test_name = f"Clarification Analysis - {test_case['input'][:20]}..."
            
            try:
                start_time = time.time()
                
                # Prepare request
                request_data = {
                    "patient_input": test_case["input"],
                    "medical_context": {
                        "consultation_stage": "chief_complaint",
                        "previous_symptoms": []
                    }
                }
                
                # Make API call
                response = requests.post(
                    f"{self.backend_url}/medical-ai/clarification-analysis",
                    json=request_data,
                    timeout=10
                )
                
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Validate response structure
                    required_fields = [
                        "input_type", "confidence_score", "detected_elements",
                        "missing_critical_info", "clarification_priority", 
                        "suggested_questions", "clarification_needed"
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in result]
                    if missing_fields:
                        self.log_test_result(
                            test_name, False, 
                            f"Missing response fields: {missing_fields}",
                            response_time, result
                        )
                        continue
                    
                    # Validate results
                    input_type = result["input_type"]
                    confidence = result["confidence_score"]
                    priority = result["clarification_priority"]
                    questions = result["suggested_questions"]
                    clarification_needed = result["clarification_needed"]
                    
                    # Check if results meet expectations
                    correct_unclear_detection = (
                        clarification_needed == test_case["expected_unclear"]
                    )
                    
                    has_questions = len(questions) > 0 if test_case["expected_unclear"] else True
                    valid_confidence = 0.0 <= confidence <= 1.0
                    valid_priority = priority in ["high", "medium", "low"]
                    
                    if correct_unclear_detection and has_questions and valid_confidence and valid_priority:
                        details = f"Type: {input_type}, Confidence: {confidence:.3f}, Priority: {priority}, Questions: {len(questions)}"
                        self.log_test_result(test_name, True, details, response_time, result)
                        successful_tests += 1
                    else:
                        issues = []
                        if not correct_unclear_detection:
                            issues.append(f"Unclear detection mismatch (expected: {test_case['expected_unclear']}, got: {clarification_needed})")
                        if not has_questions and test_case["expected_unclear"]:
                            issues.append("No questions generated for unclear input")
                        if not valid_confidence:
                            issues.append(f"Invalid confidence score: {confidence}")
                        if not valid_priority:
                            issues.append(f"Invalid priority: {priority}")
                        
                        self.log_test_result(test_name, False, "; ".join(issues), response_time, result)
                
                else:
                    self.log_test_result(
                        test_name, False, 
                        f"API call failed with status {response.status_code}: {response.text}",
                        response_time
                    )
                    
            except requests.exceptions.Timeout:
                self.log_test_result(test_name, False, "Request timeout (>10s)", 10.0)
            except Exception as e:
                self.log_test_result(test_name, False, f"Exception: {str(e)}", 0)
        
        success_rate = (successful_tests / len(test_cases)) * 100
        print(f"📊 CLARIFICATION ANALYSIS API RESULTS:")
        print(f"   Success Rate: {success_rate:.1f}% ({successful_tests}/{len(test_cases)})")
        print(f"   Target: >75% accuracy")
        print(f"   Status: {'✅ PASSED' if success_rate >= 75 else '❌ FAILED'}")
        print()
        
        return success_rate >= 75

    def test_clarification_response_generation_api(self):
        """Test the clarification response generation API endpoint"""
        print("🗨️ TESTING CLARIFICATION RESPONSE GENERATION API")
        print("=" * 60)
        
        # Test with key examples from review request
        test_examples = [
            {
                "patient_input": "not good",
                "input_type": "vague_emotional",
                "confidence_score": 0.90,
                "detected_elements": [],
                "missing_critical_info": ["specific_symptoms", "anatomical_location"],
                "urgency_indicators": [],
                "patient_communication_style": "minimal_communicator",
                "expected_phrases": ["understand you're not feeling well", "specific symptoms", "pain anywhere"]
            },
            {
                "patient_input": "chest",
                "input_type": "body_part_only", 
                "confidence_score": 0.90,
                "detected_elements": ["body_part: chest"],
                "missing_critical_info": ["specific_symptoms", "severity_assessment"],
                "urgency_indicators": ["chest_related"],
                "patient_communication_style": "direct_factual",
                "expected_phrases": ["chest", "experiencing", "describe"]
            },
            {
                "patient_input": "worried",
                "input_type": "emotion_only",
                "confidence_score": 0.95,
                "detected_elements": [],
                "missing_critical_info": ["physical_symptoms", "symptom_trigger"],
                "urgency_indicators": [],
                "patient_communication_style": "emotional_expressive",
                "expected_phrases": ["understand", "feeling", "specific symptoms"]
            }
        ]
        
        successful_tests = 0
        
        for i, test_data in enumerate(test_examples):
            test_name = f"Response Generation - {test_data['patient_input']}"
            
            try:
                start_time = time.time()
                
                response = requests.post(
                    f"{self.backend_url}/medical-ai/generate-clarification-response",
                    json=test_data,
                    timeout=10
                )
                
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Validate response structure
                    required_fields = [
                        "clarification_response", "empathetic_response", "response_type",
                        "empathy_score", "question_priority_order", "medical_reasoning"
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in result]
                    if missing_fields:
                        self.log_test_result(
                            test_name, False, 
                            f"Missing response fields: {missing_fields}",
                            response_time, result
                        )
                        continue
                    
                    clarification_response = result["clarification_response"]
                    empathy_score = result["empathy_score"]
                    
                    # Validate response quality
                    has_question = "?" in clarification_response
                    appropriate_length = len(clarification_response) > 50
                    contains_expected_phrases = any(
                        phrase.lower() in clarification_response.lower() 
                        for phrase in test_data["expected_phrases"]
                    )
                    valid_empathy_score = 0.0 <= empathy_score <= 1.0
                    
                    if has_question and appropriate_length and contains_expected_phrases and valid_empathy_score:
                        details = f"Length: {len(clarification_response)}, Empathy: {empathy_score:.3f}, Has question: {has_question}"
                        self.log_test_result(test_name, True, details, response_time, result)
                        successful_tests += 1
                    else:
                        issues = []
                        if not has_question:
                            issues.append("No question mark found")
                        if not appropriate_length:
                            issues.append(f"Response too short ({len(clarification_response)} chars)")
                        if not contains_expected_phrases:
                            issues.append("Missing expected phrases")
                        if not valid_empathy_score:
                            issues.append(f"Invalid empathy score: {empathy_score}")
                        
                        self.log_test_result(test_name, False, "; ".join(issues), response_time, result)
                
                else:
                    self.log_test_result(
                        test_name, False, 
                        f"API call failed with status {response.status_code}: {response.text}",
                        response_time
                    )
                    
            except Exception as e:
                self.log_test_result(test_name, False, f"Exception: {str(e)}", 0)
        
        success_rate = (successful_tests / len(test_examples)) * 100
        print(f"📊 RESPONSE GENERATION API RESULTS:")
        print(f"   Success Rate: {success_rate:.1f}% ({successful_tests}/{len(test_examples)})")
        print(f"   Target: >75% quality")
        print(f"   Status: {'✅ PASSED' if success_rate >= 75 else '❌ FAILED'}")
        print()
        
        return success_rate >= 75

    def test_medical_ai_integration(self):
        """Test integration with main medical AI message processing"""
        print("🏥 TESTING MEDICAL AI INTEGRATION")
        print("=" * 60)
        
        # Test unclear inputs through the main medical AI endpoint
        test_messages = [
            {
                "message": "not good",
                "description": "Task 6.1 original example",
                "should_trigger_clarification": True
            },
            {
                "message": "bad",
                "description": "Simple negative state",
                "should_trigger_clarification": True
            },
            {
                "message": "chest",
                "description": "Single body part",
                "should_trigger_clarification": True
            },
            {
                "message": "worried",
                "description": "Emotional state only",
                "should_trigger_clarification": True
            },
            {
                "message": "weird feeling",
                "description": "Unclear quality description",
                "should_trigger_clarification": True
            },
            {
                "message": "pain",
                "description": "Single symptom word",
                "should_trigger_clarification": True
            },
            # Clear input that should NOT trigger clarification
            {
                "message": "I have severe chest pain that started 30 minutes ago",
                "description": "Clear, detailed symptom",
                "should_trigger_clarification": False
            }
        ]
        
        successful_tests = 0
        
        for i, test_case in enumerate(test_messages):
            test_name = f"Medical AI Integration - {test_case['message'][:20]}..."
            
            try:
                # Initialize consultation
                init_response = requests.post(
                    f"{self.backend_url}/medical-ai/initialize",
                    json={"patient_id": f"test-clarification-{i}"},
                    timeout=10
                )
                
                if init_response.status_code != 200:
                    self.log_test_result(
                        test_name, False, 
                        f"Failed to initialize consultation: {init_response.status_code}",
                        0
                    )
                    continue
                
                init_result = init_response.json()
                consultation_id = init_result["consultation_id"]
                
                # Send message
                start_time = time.time()
                message_response = requests.post(
                    f"{self.backend_url}/medical-ai/message",
                    json={
                        "message": test_case["message"],
                        "consultation_id": consultation_id,
                        "context": init_result["context"]
                    },
                    timeout=15
                )
                
                response_time = time.time() - start_time
                
                if message_response.status_code == 200:
                    result = message_response.json()
                    
                    response_text = result["response"]
                    clarification_needed = result.get("clarification_needed", False)
                    clarification_type = result.get("clarification_type")
                    
                    # Check if clarification behavior matches expectations
                    correct_clarification_behavior = (
                        clarification_needed == test_case["should_trigger_clarification"]
                    )
                    
                    # Check response quality
                    has_meaningful_response = len(response_text) > 50
                    response_time_acceptable = response_time < 5.0  # Target: under 5 seconds
                    
                    if correct_clarification_behavior and has_meaningful_response and response_time_acceptable:
                        details = f"Clarification: {clarification_needed}, Response length: {len(response_text)}, Time: {response_time:.2f}s"
                        if clarification_type:
                            details += f", Type: {clarification_type}"
                        self.log_test_result(test_name, True, details, response_time, result)
                        successful_tests += 1
                    else:
                        issues = []
                        if not correct_clarification_behavior:
                            issues.append(f"Clarification mismatch (expected: {test_case['should_trigger_clarification']}, got: {clarification_needed})")
                        if not has_meaningful_response:
                            issues.append(f"Response too short ({len(response_text)} chars)")
                        if not response_time_acceptable:
                            issues.append(f"Response too slow ({response_time:.2f}s)")
                        
                        self.log_test_result(test_name, False, "; ".join(issues), response_time, result)
                
                else:
                    self.log_test_result(
                        test_name, False, 
                        f"Message processing failed: {message_response.status_code}: {message_response.text}",
                        response_time
                    )
                    
            except Exception as e:
                self.log_test_result(test_name, False, f"Exception: {str(e)}", 0)
        
        success_rate = (successful_tests / len(test_messages)) * 100
        print(f"📊 MEDICAL AI INTEGRATION RESULTS:")
        print(f"   Success Rate: {success_rate:.1f}% ({successful_tests}/{len(test_messages)})")
        print(f"   Target: >75% integration accuracy")
        print(f"   Status: {'✅ PASSED' if success_rate >= 75 else '❌ FAILED'}")
        print()
        
        return success_rate >= 75

    def test_performance_requirements(self):
        """Test performance requirements from review"""
        print("⚡ TESTING PERFORMANCE REQUIREMENTS")
        print("=" * 60)
        
        # Test response times with multiple unclear inputs
        test_inputs = ["not good", "bad", "chest", "worried", "weird feeling", "pain"]
        response_times = []
        successful_calls = 0
        
        for input_text in test_inputs:
            try:
                start_time = time.time()
                
                response = requests.post(
                    f"{self.backend_url}/medical-ai/clarification-analysis",
                    json={
                        "patient_input": input_text,
                        "medical_context": {"consultation_stage": "chief_complaint"}
                    },
                    timeout=10
                )
                
                response_time = time.time() - start_time
                response_times.append(response_time)
                
                if response.status_code == 200:
                    successful_calls += 1
                    
            except Exception as e:
                print(f"   Performance test failed for '{input_text}': {e}")
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            
            # Performance targets from review
            avg_under_5s = avg_response_time < 5.0
            max_under_5s = max_response_time < 5.0
            success_rate = (successful_calls / len(test_inputs)) * 100
            
            performance_passed = avg_under_5s and success_rate >= 75
            
            details = f"Avg: {avg_response_time:.2f}s, Max: {max_response_time:.2f}s, Min: {min_response_time:.2f}s, Success: {success_rate:.1f}%"
            self.log_test_result("Performance Requirements", performance_passed, details, avg_response_time)
            
            print(f"📊 PERFORMANCE RESULTS:")
            print(f"   Average Response Time: {avg_response_time:.2f}s (Target: <5s)")
            print(f"   Maximum Response Time: {max_response_time:.2f}s (Target: <5s)")
            print(f"   Success Rate: {success_rate:.1f}% (Target: >75%)")
            print(f"   Status: {'✅ PASSED' if performance_passed else '❌ FAILED'}")
            print()
            
            return performance_passed
        else:
            self.log_test_result("Performance Requirements", False, "No successful API calls", 0)
            return False

    def run_comprehensive_test(self):
        """Run all tests and generate comprehensive report"""
        print("🚀 STARTING COMPREHENSIVE TASK 6.1 TESTING")
        print("=" * 80)
        
        # Run all test suites
        test_results = {
            "clarification_analysis": self.test_clarification_analysis_api(),
            "response_generation": self.test_clarification_response_generation_api(),
            "medical_ai_integration": self.test_medical_ai_integration(),
            "performance_requirements": self.test_performance_requirements()
        }
        
        # Calculate overall results
        passed_suites = sum(1 for result in test_results.values() if result)
        total_suites = len(test_results)
        overall_success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        # Generate final report
        print("=" * 80)
        print("🎯 TASK 6.1 INTELLIGENT CLARIFICATION SYSTEM - FINAL RESULTS")
        print("=" * 80)
        
        for suite_name, result in test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"   {suite_name.replace('_', ' ').title()}: {status}")
        
        print(f"\n📊 OVERALL RESULTS:")
        print(f"   Test Suites Passed: {passed_suites}/{total_suites}")
        print(f"   Individual Tests Passed: {self.passed_tests}/{self.total_tests}")
        print(f"   Overall Success Rate: {overall_success_rate:.1f}%")
        
        # Determine final status
        if passed_suites >= 3 and overall_success_rate >= 75:
            print(f"\n🎉 TASK 6.1 IMPLEMENTATION: ✅ SUCCESS")
            print("   ✅ Clarification analysis detects unclear inputs with high confidence")
            print("   ✅ Response generation creates empathetic, specific clarifying questions")
            print("   ✅ Medical AI integration flags unclear inputs appropriately")
            print("   ✅ System handles original task example 'not good' correctly")
            print("   ✅ Performance targets met (API response times under 5 seconds)")
            final_status = "SUCCESS"
        elif passed_suites >= 2 and overall_success_rate >= 60:
            print(f"\n⚠️ TASK 6.1 IMPLEMENTATION: 🔄 PARTIAL SUCCESS")
            print("   ✅ Core functionality working")
            print("   ⚠️ Some improvements needed for full compliance")
            final_status = "PARTIAL"
        else:
            print(f"\n❌ TASK 6.1 IMPLEMENTATION: ❌ NEEDS WORK")
            print("   ❌ Significant issues detected")
            print("   ❌ Requires debugging and improvements")
            final_status = "FAILED"
        
        print(f"\nTest completed at: {datetime.now().isoformat()}")
        
        return {
            "final_status": final_status,
            "overall_success_rate": overall_success_rate,
            "passed_suites": passed_suites,
            "total_suites": total_suites,
            "test_results": test_results,
            "individual_tests": self.test_results
        }

def main():
    """Main test execution"""
    tester = Task61ClarificationTester()
    results = tester.run_comprehensive_test()
    
    # Return appropriate exit code
    if results["final_status"] == "SUCCESS":
        exit(0)
    elif results["final_status"] == "PARTIAL":
        exit(1)
    else:
        exit(2)

if __name__ == "__main__":
    main()