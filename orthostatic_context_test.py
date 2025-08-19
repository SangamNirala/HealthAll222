#!/usr/bin/env python3
"""
CONTEXT-AWARE MEDICAL REASONING ENGINE - ORTHOSTATIC SYMPTOMS TESTING
====================================================================

Comprehensive testing of the Context-Aware Medical Reasoning Engine specifically 
for the orthostatic symptoms scenario as requested in the review.

SPECIFIC TEST SCENARIO:
"Every morning when I get out of bed I feel dizzy and nauseous, sometimes I even 
feel like I'm going to faint, but it goes away after I sit back down for a few 
minutes. This also happens when I stand up quickly from a chair or get up from 
squatting down."

EXPECTED RESULTS:
1. Urgency level should be "urgent" (not "routine" or "emergency")
2. Contextual reasoning fields should be populated with orthostatic-specific content
3. Response should include orthostatic pattern detection
4. Clinical hypotheses should mention orthostatic hypotension
5. Recommendations should include orthostatic-specific advice

INVESTIGATION FOCUS:
1. AdvancedSymptomRecognizer.extract_medical_entities method orthostatic pattern detection
2. ContextAwareMedicalReasoner contextual reasoning generation
3. Contextual reasoning integration into API response
4. Urgency assessment using contextual reasoning results

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
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://clinicaldecision.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class OrthostatiContextTester:
    """Comprehensive tester for orthostatic symptoms contextual reasoning"""
    
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

    def test_medical_ai_initialization(self) -> tuple:
        """Test Medical AI service initialization for orthostatic testing"""
        try:
            response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                json={
                    "patient_id": "orthostatic-test-patient",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                required_keys = ["consultation_id", "patient_id", "current_stage", "response"]
                
                if all(key in data for key in required_keys):
                    consultation_id = data.get('consultation_id')
                    self.log_test("Medical AI Initialization for Orthostatic Testing", True, 
                                f"Successfully initialized with consultation_id: {consultation_id}")
                    return True, consultation_id
                else:
                    self.log_test("Medical AI Initialization for Orthostatic Testing", False, 
                                f"Missing required keys. Got: {list(data.keys())}", data)
                    return False, None
            else:
                self.log_test("Medical AI Initialization for Orthostatic Testing", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False, None
                
        except Exception as e:
            self.log_test("Medical AI Initialization for Orthostatic Testing", False, f"Exception: {str(e)}")
            return False, None

    def test_orthostatic_symptoms_scenario(self, consultation_id: str) -> bool:
        """Test the specific orthostatic symptoms scenario from the review request"""
        try:
            # The exact orthostatic scenario from the review request
            orthostatic_message = "Every morning when I get out of bed I feel dizzy and nauseous, sometimes I even feel like I'm going to faint, but it goes away after I sit back down for a few minutes. This also happens when I stand up quickly from a chair or get up from squatting down."
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": orthostatic_message,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract key response elements
                urgency = data.get("urgency", "routine")
                response_text = data.get("response", "").lower()
                differential_diagnoses = data.get("differential_diagnoses", [])
                recommendations = data.get("recommendations", [])
                context = data.get("context", {})
                
                # Test Results Analysis
                test_results = {
                    "urgency_level": urgency,
                    "response_text": response_text,
                    "differential_diagnoses": differential_diagnoses,
                    "recommendations": recommendations,
                    "context": context
                }
                
                # EXPECTED RESULT 1: Urgency level should be "urgent"
                urgency_correct = urgency == "urgent"
                
                # EXPECTED RESULT 2: Contextual reasoning fields populated with orthostatic content
                orthostatic_keywords = [
                    "orthostatic", "positional", "standing", "sitting", "position", 
                    "postural", "blood pressure", "hypotension", "dizziness", "presyncope"
                ]
                
                found_orthostatic_keywords = [kw for kw in orthostatic_keywords if kw in response_text]
                contextual_reasoning_present = len(found_orthostatic_keywords) >= 3
                
                # EXPECTED RESULT 3: Orthostatic pattern detection
                pattern_indicators = [
                    "morning", "get out of bed", "stand up", "position change", 
                    "sitting down", "relief", "pattern", "trigger"
                ]
                
                found_pattern_indicators = [pi for pi in pattern_indicators if pi in response_text]
                pattern_detection = len(found_pattern_indicators) >= 3
                
                # EXPECTED RESULT 4: Clinical hypotheses mention orthostatic hypotension
                clinical_hypotheses_text = ""
                if isinstance(differential_diagnoses, list):
                    for diagnosis in differential_diagnoses:
                        if isinstance(diagnosis, dict):
                            condition = diagnosis.get('condition', '').lower()
                            clinical_hypotheses_text += condition + " "
                        elif isinstance(diagnosis, str):
                            clinical_hypotheses_text += diagnosis.lower() + " "
                
                # Also check response text for clinical hypotheses
                clinical_hypotheses_text += response_text
                
                orthostatic_hypothesis = any(term in clinical_hypotheses_text for term in 
                                           ["orthostatic hypotension", "postural hypotension", 
                                            "orthostatic", "positional hypotension"])
                
                # EXPECTED RESULT 5: Recommendations include orthostatic-specific advice
                recommendations_text = ""
                if isinstance(recommendations, list):
                    for rec in recommendations:
                        if isinstance(rec, dict):
                            recommendations_text += rec.get('recommendation', '').lower() + " "
                        elif isinstance(rec, str):
                            recommendations_text += rec.lower() + " "
                
                # Also check response text for recommendations
                recommendations_text += response_text
                
                orthostatic_recommendations = any(term in recommendations_text for term in 
                                                ["slowly", "gradual", "hydration", "rise slowly", 
                                                 "sit for", "position change", "avoid sudden"])
                
                # Calculate overall success
                success_criteria = [
                    urgency_correct,
                    contextual_reasoning_present,
                    pattern_detection,
                    orthostatic_hypothesis,
                    orthostatic_recommendations
                ]
                
                passed_criteria = sum(success_criteria)
                overall_success = passed_criteria >= 4  # Need at least 4/5 criteria
                
                # Detailed results
                details = f"""
ORTHOSTATIC SYMPTOMS SCENARIO ANALYSIS:
1. Urgency Level: {urgency} (Expected: urgent) - {'✅' if urgency_correct else '❌'}
2. Contextual Reasoning: Found {len(found_orthostatic_keywords)} orthostatic keywords {found_orthostatic_keywords} - {'✅' if contextual_reasoning_present else '❌'}
3. Pattern Detection: Found {len(found_pattern_indicators)} pattern indicators {found_pattern_indicators} - {'✅' if pattern_detection else '❌'}
4. Clinical Hypotheses: Orthostatic hypotension mentioned - {'✅' if orthostatic_hypothesis else '❌'}
5. Recommendations: Orthostatic-specific advice present - {'✅' if orthostatic_recommendations else '❌'}

Overall Success: {passed_criteria}/5 criteria met
                """
                
                self.log_test("Orthostatic Symptoms Scenario", overall_success, details, test_results)
                return overall_success
                
            else:
                self.log_test("Orthostatic Symptoms Scenario", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Orthostatic Symptoms Scenario", False, f"Exception: {str(e)}")
            return False

    def test_contextual_reasoning_integration(self, consultation_id: str) -> bool:
        """Test that contextual reasoning is properly integrated into the API response"""
        try:
            # Test with a simpler orthostatic scenario to verify integration
            test_message = "I get dizzy when I stand up from sitting"
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": test_message,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "").lower()
                
                # Check for contextual reasoning integration
                contextual_indicators = [
                    "positional", "standing", "orthostatic", "position", 
                    "blood pressure", "dizziness", "context", "trigger"
                ]
                
                found_indicators = [indicator for indicator in contextual_indicators 
                                  if indicator in response_text]
                
                integration_success = len(found_indicators) >= 2
                
                details = f"Found contextual reasoning indicators: {found_indicators}"
                
                self.log_test("Contextual Reasoning Integration", integration_success, details)
                return integration_success
                
            else:
                self.log_test("Contextual Reasoning Integration", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Contextual Reasoning Integration", False, f"Exception: {str(e)}")
            return False

    def test_urgency_assessment_with_contextual_reasoning(self, consultation_id: str) -> bool:
        """Test that urgency assessment properly uses contextual reasoning results"""
        try:
            # Test different orthostatic scenarios with expected urgency levels
            test_scenarios = [
                {
                    "message": "I feel dizzy when I stand up, but it goes away quickly",
                    "expected_urgency": "urgent",
                    "scenario_name": "Basic Orthostatic Symptoms"
                },
                {
                    "message": "Every morning I get dizzy and nearly faint when getting out of bed, happens daily for weeks",
                    "expected_urgency": "urgent", 
                    "scenario_name": "Chronic Orthostatic with Near-Syncope"
                },
                {
                    "message": "I have a mild headache that comes and goes",
                    "expected_urgency": "routine",
                    "scenario_name": "Non-Orthostatic Control"
                }
            ]
            
            results = []
            
            for scenario in test_scenarios:
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
                    actual_urgency = data.get("urgency", "routine")
                    
                    # For orthostatic scenarios, we expect "urgent"
                    # For non-orthostatic, we expect "routine"
                    urgency_correct = actual_urgency == scenario["expected_urgency"]
                    
                    results.append({
                        "scenario": scenario["scenario_name"],
                        "expected": scenario["expected_urgency"],
                        "actual": actual_urgency,
                        "correct": urgency_correct
                    })
                else:
                    results.append({
                        "scenario": scenario["scenario_name"],
                        "error": f"HTTP {response.status_code}"
                    })
            
            # Calculate success rate
            correct_assessments = sum(1 for r in results if r.get("correct", False))
            total_assessments = len(results)
            success_rate = correct_assessments / total_assessments if total_assessments > 0 else 0
            
            overall_success = success_rate >= 0.67  # At least 2/3 correct
            
            details = f"Urgency Assessment Results: {correct_assessments}/{total_assessments} correct\n"
            for result in results:
                if "error" not in result:
                    status = "✅" if result["correct"] else "❌"
                    details += f"  {status} {result['scenario']}: Expected {result['expected']}, Got {result['actual']}\n"
                else:
                    details += f"  ❌ {result['scenario']}: {result['error']}\n"
            
            self.log_test("Urgency Assessment with Contextual Reasoning", overall_success, details)
            return overall_success
            
        except Exception as e:
            self.log_test("Urgency Assessment with Contextual Reasoning", False, f"Exception: {str(e)}")
            return False

    def test_advanced_orthostatic_pattern_detection(self, consultation_id: str) -> bool:
        """Test advanced orthostatic pattern detection capabilities"""
        try:
            # Test various orthostatic pattern variations
            orthostatic_variations = [
                "I get lightheaded when I stand up from lying down",
                "Dizziness happens when I get up too fast from a chair", 
                "Feel faint when changing from sitting to standing position",
                "Dizzy spells occur when I rise from squatting or bending over"
            ]
            
            pattern_detection_results = []
            
            for variation in orthostatic_variations:
                response = requests.post(f"{API_BASE}/medical-ai/message",
                    json={
                        "consultation_id": consultation_id,
                        "message": variation,
                        "timestamp": datetime.now().isoformat()
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "").lower()
                    
                    # Check for orthostatic pattern recognition
                    orthostatic_patterns = [
                        "orthostatic", "positional", "postural", "standing", 
                        "position change", "blood pressure", "hypotension"
                    ]
                    
                    found_patterns = [pattern for pattern in orthostatic_patterns 
                                    if pattern in response_text]
                    
                    pattern_detected = len(found_patterns) >= 1
                    
                    pattern_detection_results.append({
                        "variation": variation[:50] + "...",
                        "patterns_found": found_patterns,
                        "detected": pattern_detected
                    })
                else:
                    pattern_detection_results.append({
                        "variation": variation[:50] + "...",
                        "error": f"HTTP {response.status_code}"
                    })
            
            # Calculate success rate
            successful_detections = sum(1 for r in pattern_detection_results if r.get("detected", False))
            total_variations = len(pattern_detection_results)
            detection_rate = successful_detections / total_variations if total_variations > 0 else 0
            
            overall_success = detection_rate >= 0.75  # At least 75% detection rate
            
            details = f"Pattern Detection Results: {successful_detections}/{total_variations} variations detected\n"
            for result in pattern_detection_results:
                if "error" not in result:
                    status = "✅" if result["detected"] else "❌"
                    details += f"  {status} {result['variation']}: {result['patterns_found']}\n"
                else:
                    details += f"  ❌ {result['variation']}: {result['error']}\n"
            
            self.log_test("Advanced Orthostatic Pattern Detection", overall_success, details)
            return overall_success
            
        except Exception as e:
            self.log_test("Advanced Orthostatic Pattern Detection", False, f"Exception: {str(e)}")
            return False

    def run_comprehensive_orthostatic_tests(self):
        """Run all orthostatic contextual reasoning tests"""
        print("🩺 CONTEXT-AWARE MEDICAL REASONING ENGINE - ORTHOSTATIC SYMPTOMS TESTING")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Testing started at: {datetime.now().isoformat()}")
        print()
        
        # Test 1: Initialize Medical AI
        print("🔧 INITIALIZING MEDICAL AI SERVICE...")
        init_success, consultation_id = self.test_medical_ai_initialization()
        
        if not init_success or not consultation_id:
            print("❌ Failed to initialize Medical AI service. Cannot proceed with testing.")
            return self.passed_tests, self.failed_tests, self.total_tests
        
        # Test 2: Main Orthostatic Symptoms Scenario
        print("\n🎯 TESTING MAIN ORTHOSTATIC SYMPTOMS SCENARIO...")
        main_scenario_success = self.test_orthostatic_symptoms_scenario(consultation_id)
        
        # Test 3: Contextual Reasoning Integration
        print("\n🧠 TESTING CONTEXTUAL REASONING INTEGRATION...")
        integration_success = self.test_contextual_reasoning_integration(consultation_id)
        
        # Test 4: Urgency Assessment with Contextual Reasoning
        print("\n⚡ TESTING URGENCY ASSESSMENT WITH CONTEXTUAL REASONING...")
        urgency_success = self.test_urgency_assessment_with_contextual_reasoning(consultation_id)
        
        # Test 5: Advanced Orthostatic Pattern Detection
        print("\n🔍 TESTING ADVANCED ORTHOSTATIC PATTERN DETECTION...")
        pattern_success = self.test_advanced_orthostatic_pattern_detection(consultation_id)
        
        # Print summary
        print("\n" + "=" * 80)
        print("🩺 ORTHOSTATIC SYMPTOMS CONTEXTUAL REASONING TEST SUMMARY")
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
    tester = OrthostatiContextTester()
    passed, failed, total = tester.run_comprehensive_orthostatic_tests()
    
    # Exit with appropriate code
    if failed == 0:
        print("\n🎉 ALL ORTHOSTATIC CONTEXTUAL REASONING TESTS PASSED!")
        print("✅ Context-Aware Medical Reasoning Engine is working correctly for orthostatic symptoms.")
        sys.exit(0)
    else:
        print(f"\n⚠️  {failed} TESTS FAILED. Context-Aware Medical Reasoning Engine needs attention.")
        print("❌ Orthostatic symptoms contextual reasoning requires debugging.")
        sys.exit(1)

if __name__ == "__main__":
    main()