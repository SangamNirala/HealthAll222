#!/usr/bin/env python3
"""
STEP 2.2 CONTEXT-AWARE MEDICAL REASONING ENGINE COMPREHENSIVE TESTING
====================================================================

Comprehensive testing of Step 2.2 Context-Aware Medical Reasoning Engine fixes
addressing the critical issues identified in previous testing:

1. CONSULTATION FLOW PROBLEM: Medical AI responding with generic messages
2. MISSING API RESPONSE FIELDS: Missing contextual reasoning features
3. INCONSISTENT ACTIVATION: Contextual reasoning engine not consistently activated
4. ULTRA-CHALLENGING SCENARIOS FAILING: Only 1/3 scenarios properly processed

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
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://symptom-context.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class Step22ContextualReasoningTester:
    """Comprehensive tester for Step 2.2 Context-Aware Medical Reasoning Engine fixes"""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
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

    def test_ultra_challenging_scenario_1_positional_orthostatic(self) -> bool:
        """Test Scenario 1: Positional/Orthostatic - Morning dizziness when standing"""
        try:
            # Initialize consultation
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                json={
                    "patient_id": "test-scenario-1-orthostatic",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Ultra-Challenging Scenario 1 (Positional/Orthostatic)", False, 
                            f"Failed to initialize: {init_response.status_code}")
                return False
                
            consultation_id = init_response.json().get("consultation_id")
            
            # Ultra-challenging contextual scenario 1
            scenario_1 = "Every morning when I get out of bed I feel dizzy and nauseous, sometimes I even feel like I'm going to faint, but it goes away after I sit back down for a few minutes"
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": scenario_1,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "").lower()
                
                # Check for Step 2.2 API response fields
                step_22_fields = {
                    "causal_relationships": data.get("causal_relationships"),
                    "clinical_hypotheses": data.get("clinical_hypotheses"),
                    "contextual_factors": data.get("contextual_factors"),
                    "medical_reasoning_narrative": data.get("medical_reasoning_narrative"),
                    "context_based_recommendations": data.get("context_based_recommendations"),
                    "trigger_avoidance_strategies": data.get("trigger_avoidance_strategies"),
                    "specialist_referral_context": data.get("specialist_referral_context"),
                    "contextual_significance": data.get("contextual_significance"),
                    "reasoning_confidence": data.get("reasoning_confidence")
                }
                
                # Count present fields
                present_fields = [field for field, value in step_22_fields.items() if value is not None]
                
                # Check for contextual analysis in response
                contextual_indicators = [
                    "orthostatic", "positional", "standing", "sitting", "position",
                    "blood pressure", "hypotension", "circulation", "gradual"
                ]
                
                found_indicators = [indicator for indicator in contextual_indicators 
                                  if indicator in response_text]
                
                # Check urgency level - should be urgent/emergency for orthostatic symptoms
                urgency = data.get("urgency", "routine")
                
                # Evaluate success criteria
                has_contextual_analysis = len(found_indicators) >= 2
                has_appropriate_urgency = urgency in ["urgent", "emergency"]
                has_step_22_fields = len(present_fields) >= 3
                
                success = has_contextual_analysis and has_appropriate_urgency and has_step_22_fields
                
                if success:
                    self.log_test("Ultra-Challenging Scenario 1 (Positional/Orthostatic)", True,
                                f"Contextual analysis detected: {found_indicators}, urgency: {urgency}, Step 2.2 fields: {present_fields}")
                    return True
                else:
                    self.log_test("Ultra-Challenging Scenario 1 (Positional/Orthostatic)", False,
                                f"Insufficient analysis. Contextual: {found_indicators}, urgency: {urgency}, fields: {present_fields}", data)
                    return False
            else:
                self.log_test("Ultra-Challenging Scenario 1 (Positional/Orthostatic)", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Ultra-Challenging Scenario 1 (Positional/Orthostatic)", False, f"Exception: {str(e)}")
            return False

    def test_ultra_challenging_scenario_2_exertional_cardiac(self) -> bool:
        """Test Scenario 2: Exertional/Cardiac - Chest pain with exertion"""
        try:
            # Initialize consultation
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                json={
                    "patient_id": "test-scenario-2-cardiac",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Ultra-Challenging Scenario 2 (Exertional/Cardiac)", False, 
                            f"Failed to initialize: {init_response.status_code}")
                return False
                
            consultation_id = init_response.json().get("consultation_id")
            
            # Ultra-challenging contextual scenario 2
            scenario_2 = "I get this crushing chest pain whenever I walk uphill or climb more than one flight of stairs, feels like an elephant sitting on my chest, but it completely goes away within 2-3 minutes of resting"
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": scenario_2,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "").lower()
                
                # Check for Step 2.2 API response fields
                step_22_fields = {
                    "causal_relationships": data.get("causal_relationships"),
                    "clinical_hypotheses": data.get("clinical_hypotheses"),
                    "contextual_factors": data.get("contextual_factors"),
                    "medical_reasoning_narrative": data.get("medical_reasoning_narrative"),
                    "context_based_recommendations": data.get("context_based_recommendations"),
                    "trigger_avoidance_strategies": data.get("trigger_avoidance_strategies"),
                    "specialist_referral_context": data.get("specialist_referral_context"),
                    "contextual_significance": data.get("contextual_significance"),
                    "reasoning_confidence": data.get("reasoning_confidence")
                }
                
                # Count present fields
                present_fields = [field for field, value in step_22_fields.items() if value is not None]
                
                # Check for exertional cardiac context
                cardiac_indicators = [
                    "exertional", "angina", "cardiac", "coronary", "heart",
                    "exercise", "stairs", "walking", "activity", "rest"
                ]
                
                found_indicators = [indicator for indicator in cardiac_indicators 
                                  if indicator in response_text]
                
                # Check urgency level - should be emergency for exertional chest pain
                urgency = data.get("urgency", "routine")
                
                # Evaluate success criteria
                has_cardiac_analysis = len(found_indicators) >= 3
                has_emergency_urgency = urgency == "emergency"
                has_step_22_fields = len(present_fields) >= 4
                
                success = has_cardiac_analysis and has_emergency_urgency and has_step_22_fields
                
                if success:
                    self.log_test("Ultra-Challenging Scenario 2 (Exertional/Cardiac)", True,
                                f"Cardiac analysis detected: {found_indicators}, urgency: {urgency}, Step 2.2 fields: {present_fields}")
                    return True
                else:
                    self.log_test("Ultra-Challenging Scenario 2 (Exertional/Cardiac)", False,
                                f"Insufficient analysis. Cardiac: {found_indicators}, urgency: {urgency}, fields: {present_fields}", data)
                    return False
            else:
                self.log_test("Ultra-Challenging Scenario 2 (Exertional/Cardiac)", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Ultra-Challenging Scenario 2 (Exertional/Cardiac)", False, f"Exception: {str(e)}")
            return False

    def test_ultra_challenging_scenario_3_multi_context_dietary_stress(self) -> bool:
        """Test Scenario 3: Multi-Context Dietary/Stress - Complex trigger interaction"""
        try:
            # Initialize consultation
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                json={
                    "patient_id": "test-scenario-3-multi-context",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Ultra-Challenging Scenario 3 (Multi-Context Dietary/Stress)", False, 
                            f"Failed to initialize: {init_response.status_code}")
                return False
                
            consultation_id = init_response.json().get("consultation_id")
            
            # Ultra-challenging contextual scenario 3
            scenario_3 = "I've noticed that I get really bad stomach cramps and loose stools about 30-60 minutes after eating ice cream or drinking milk, but only when I'm stressed out at work"
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": scenario_3,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "").lower()
                
                # Check for Step 2.2 API response fields
                step_22_fields = {
                    "causal_relationships": data.get("causal_relationships"),
                    "clinical_hypotheses": data.get("clinical_hypotheses"),
                    "contextual_factors": data.get("contextual_factors"),
                    "medical_reasoning_narrative": data.get("medical_reasoning_narrative"),
                    "context_based_recommendations": data.get("context_based_recommendations"),
                    "trigger_avoidance_strategies": data.get("trigger_avoidance_strategies"),
                    "specialist_referral_context": data.get("specialist_referral_context"),
                    "contextual_significance": data.get("contextual_significance"),
                    "reasoning_confidence": data.get("reasoning_confidence")
                }
                
                # Count present fields
                present_fields = [field for field, value in step_22_fields.items() if value is not None]
                
                # Check for multi-context analysis
                multi_context_indicators = [
                    "lactose", "dairy", "intolerance", "milk", "ice cream",
                    "stress", "work", "trigger", "combination", "context"
                ]
                
                found_indicators = [indicator for indicator in multi_context_indicators 
                                  if indicator in response_text]
                
                # Check for causal relationship detection
                causal_indicators = ["after eating", "when stressed", "trigger", "cause", "relationship"]
                found_causal = [indicator for indicator in causal_indicators if indicator in response_text]
                
                # Evaluate success criteria
                has_multi_context_analysis = len(found_indicators) >= 3
                has_causal_relationships = len(found_causal) >= 2
                has_step_22_fields = len(present_fields) >= 3
                
                success = has_multi_context_analysis and has_causal_relationships and has_step_22_fields
                
                if success:
                    self.log_test("Ultra-Challenging Scenario 3 (Multi-Context Dietary/Stress)", True,
                                f"Multi-context analysis: {found_indicators}, causal: {found_causal}, Step 2.2 fields: {present_fields}")
                    return True
                else:
                    self.log_test("Ultra-Challenging Scenario 3 (Multi-Context Dietary/Stress)", False,
                                f"Insufficient analysis. Multi-context: {found_indicators}, causal: {found_causal}, fields: {present_fields}", data)
                    return False
            else:
                self.log_test("Ultra-Challenging Scenario 3 (Multi-Context Dietary/Stress)", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Ultra-Challenging Scenario 3 (Multi-Context Dietary/Stress)", False, f"Exception: {str(e)}")
            return False

    def test_step_22_api_response_fields(self) -> bool:
        """Test that all Step 2.2 API response fields are present"""
        try:
            # Initialize consultation
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                json={
                    "patient_id": "test-step-22-fields",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Step 2.2 API Response Fields", False, 
                            f"Failed to initialize: {init_response.status_code}")
                return False
                
            consultation_id = init_response.json().get("consultation_id")
            
            # Test with a complex contextual scenario
            complex_scenario = "I get severe headaches that start behind my right eye, throbbing like my heartbeat, usually triggered by bright fluorescent lights at work, especially when I'm stressed about deadlines, and they last for hours until I can rest in a dark room"
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": complex_scenario,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for all required Step 2.2 API response fields
                required_fields = [
                    "causal_relationships",
                    "clinical_hypotheses", 
                    "contextual_factors",
                    "medical_reasoning_narrative",
                    "context_based_recommendations",
                    "trigger_avoidance_strategies",
                    "specialist_referral_context",
                    "contextual_significance",
                    "reasoning_confidence"
                ]
                
                present_fields = []
                missing_fields = []
                
                for field in required_fields:
                    if field in data and data[field] is not None:
                        present_fields.append(field)
                    else:
                        missing_fields.append(field)
                
                # Success criteria: at least 7 out of 9 fields present
                success = len(present_fields) >= 7
                
                if success:
                    self.log_test("Step 2.2 API Response Fields", True,
                                f"Present fields ({len(present_fields)}/9): {present_fields}")
                    return True
                else:
                    self.log_test("Step 2.2 API Response Fields", False,
                                f"Missing fields ({len(missing_fields)}/9): {missing_fields}. Present: {present_fields}", data)
                    return False
            else:
                self.log_test("Step 2.2 API Response Fields", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Step 2.2 API Response Fields", False, f"Exception: {str(e)}")
            return False

    def test_consultation_flow_problem(self) -> bool:
        """Test that Medical AI doesn't respond with generic 'please describe symptoms' messages"""
        try:
            # Initialize consultation
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                json={
                    "patient_id": "test-consultation-flow",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Consultation Flow Problem", False, 
                            f"Failed to initialize: {init_response.status_code}")
                return False
                
            consultation_id = init_response.json().get("consultation_id")
            
            # Test with specific symptom descriptions
            test_scenarios = [
                "I have crushing chest pain that radiates to my left arm",
                "I get dizzy every morning when I stand up from bed",
                "I have severe stomach cramps after eating dairy products"
            ]
            
            generic_responses = 0
            contextual_responses = 0
            
            for scenario in test_scenarios:
                response = requests.post(f"{API_BASE}/medical-ai/message",
                    json={
                        "consultation_id": consultation_id,
                        "message": scenario,
                        "timestamp": datetime.now().isoformat()
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "").lower()
                    
                    # Check for generic responses
                    generic_phrases = [
                        "please describe your symptoms",
                        "can you tell me more about your symptoms",
                        "describe your symptoms",
                        "what symptoms are you experiencing"
                    ]
                    
                    is_generic = any(phrase in response_text for phrase in generic_phrases)
                    
                    # Check for contextual responses
                    contextual_phrases = [
                        "chest pain", "crushing", "radiating", "arm",
                        "dizzy", "standing", "orthostatic", "position",
                        "stomach", "dairy", "lactose", "intolerance"
                    ]
                    
                    has_contextual = any(phrase in response_text for phrase in contextual_phrases)
                    
                    if is_generic:
                        generic_responses += 1
                    if has_contextual:
                        contextual_responses += 1
                
            # Success criteria: No generic responses and at least 2 contextual responses
            success = generic_responses == 0 and contextual_responses >= 2
            
            if success:
                self.log_test("Consultation Flow Problem", True,
                            f"No generic responses detected. Contextual responses: {contextual_responses}/3")
                return True
            else:
                self.log_test("Consultation Flow Problem", False,
                            f"Generic responses: {generic_responses}, Contextual responses: {contextual_responses}")
                return False
                
        except Exception as e:
            self.log_test("Consultation Flow Problem", False, f"Exception: {str(e)}")
            return False

    def test_contextual_reasoning_consistency(self) -> bool:
        """Test that contextual reasoning engine is consistently activated"""
        try:
            # Test multiple scenarios to check consistency
            test_scenarios = [
                {
                    "message": "I get headaches when I'm under stress at work",
                    "expected_context": ["stress", "work", "trigger"]
                },
                {
                    "message": "My back pain gets worse when I sit for long periods",
                    "expected_context": ["sitting", "position", "duration"]
                },
                {
                    "message": "I feel nauseous after eating spicy food",
                    "expected_context": ["eating", "food", "trigger", "after"]
                },
                {
                    "message": "I have trouble sleeping when it's noisy outside",
                    "expected_context": ["noise", "environment", "sleep", "trigger"]
                }
            ]
            
            consistent_activations = 0
            total_scenarios = len(test_scenarios)
            
            for i, scenario in enumerate(test_scenarios):
                # Initialize new consultation for each test
                init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                    json={
                        "patient_id": f"test-consistency-{i}",
                        "timestamp": datetime.now().isoformat()
                    },
                    timeout=30
                )
                
                if init_response.status_code != 200:
                    continue
                    
                consultation_id = init_response.json().get("consultation_id")
                
                response = requests.post(f"{API_BASE}/medical-ai/message",
                    json={
                        "consultation_id": consultation_id,
                        "message": scenario["message"],
                        "timestamp": datetime.now().isoformat()
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "").lower()
                    
                    # Check if expected contextual elements are present
                    found_context = [ctx for ctx in scenario["expected_context"] 
                                   if ctx in response_text]
                    
                    # Check for Step 2.2 fields
                    has_contextual_fields = any(field in data for field in 
                                              ["contextual_factors", "causal_relationships", "trigger_avoidance_strategies"])
                    
                    if len(found_context) >= 1 or has_contextual_fields:
                        consistent_activations += 1
            
            # Success criteria: At least 75% consistency
            consistency_rate = consistent_activations / total_scenarios
            success = consistency_rate >= 0.75
            
            if success:
                self.log_test("Contextual Reasoning Consistency", True,
                            f"Consistency rate: {consistency_rate*100:.1f}% ({consistent_activations}/{total_scenarios})")
                return True
            else:
                self.log_test("Contextual Reasoning Consistency", False,
                            f"Low consistency rate: {consistency_rate*100:.1f}% ({consistent_activations}/{total_scenarios})")
                return False
                
        except Exception as e:
            self.log_test("Contextual Reasoning Consistency", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all Step 2.2 Context-Aware Medical Reasoning Engine tests"""
        print("🧠 STEP 2.2 CONTEXT-AWARE MEDICAL REASONING ENGINE COMPREHENSIVE TESTING")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Testing started at: {datetime.now().isoformat()}")
        print()
        
        # Run all tests
        test_methods = [
            self.test_ultra_challenging_scenario_1_positional_orthostatic,
            self.test_ultra_challenging_scenario_2_exertional_cardiac,
            self.test_ultra_challenging_scenario_3_multi_context_dietary_stress,
            self.test_step_22_api_response_fields,
            self.test_consultation_flow_problem,
            self.test_contextual_reasoning_consistency
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.log_test(test_method.__name__, False, f"Test execution failed: {str(e)}")
        
        # Print summary
        print("\n" + "=" * 80)
        print("🧠 STEP 2.2 CONTEXT-AWARE MEDICAL REASONING ENGINE TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.failed_tests} ❌")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        print()
        
        # Print detailed results
        print("DETAILED TEST RESULTS:")
        print("-" * 40)
        for result in self.test_results:
            print(f"{result['status']}: {result['test_name']}")
            if result['details']:
                print(f"   {result['details']}")
        
        print(f"\nTesting completed at: {datetime.now().isoformat()}")
        
        return self.passed_tests, self.failed_tests, self.total_tests

def main():
    """Main test execution"""
    tester = Step22ContextualReasoningTester()
    passed, failed, total = tester.run_all_tests()
    
    # Exit with appropriate code
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Step 2.2 Context-Aware Medical Reasoning Engine is working correctly.")
        sys.exit(0)
    else:
        print(f"\n⚠️  {failed} TESTS FAILED. Step 2.2 Context-Aware Medical Reasoning Engine needs attention.")
        sys.exit(1)

if __name__ == "__main__":
    main()