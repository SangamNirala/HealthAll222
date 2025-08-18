#!/usr/bin/env python3
"""
🚀 WEEK 1 SUBSPECIALTY INTENT CLASSIFICATION BACKEND TESTING
===========================================================

Comprehensive testing suite for the newly implemented Week 1 subspecialty intent 
classification system with 30+ medical intent categories and subspecialty-level 
clinical reasoning.

Testing Focus Areas:
1. NEW SUBSPECIALTY CATEGORIES VALIDATION (12 new categories)
2. API ENDPOINT TESTING (intent-classification, multi-message-intent)
3. HIGH PRIORITY TEST SCENARIOS (Emergency scenarios)
4. VALIDATION REQUIREMENTS (Performance, confidence, clinical reasoning)
5. ADVANCED FEATURES TESTING (Clinical reasoning engines, decision support)

Algorithm Version: 3.1_intelligence_amplification
"""

import asyncio
import json
import time
import requests
import sys
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://medical-intents.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class Week1SubspecialtyIntentTester:
    """
    🎯 WEEK 1 SUBSPECIALTY INTENT CLASSIFICATION COMPREHENSIVE TESTER
    
    Advanced testing suite for validating the revolutionary Week 1 subspecialty 
    intent classification system with clinical-grade precision and subspecialty 
    reasoning engines.
    """
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.api_base = API_BASE
        self.test_results = []
        self.performance_metrics = []
        self.subspecialty_validations = []
        
        # Test statistics
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
        print("🎯 WEEK 1 SUBSPECIALTY INTENT CLASSIFICATION TESTER INITIALIZED")
        print("=" * 80)
        print(f"Backend URL: {self.backend_url}")
        print(f"API Base: {self.api_base}")
        
    def log_test(self, test_name: str, passed: bool, details: str, data: Any = None):
        """Log test result with comprehensive details"""
        status = "✅ PASS" if passed else "❌ FAIL"
        self.test_results.append({
            "test_name": test_name,
            "status": status,
            "passed": passed,
            "details": details,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
        
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
            
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        if not passed and data:
            print(f"   Data: {json.dumps(data, indent=2)[:200]}...")
    
    def test_api_endpoints_availability(self):
        """
        🔗 TEST API ENDPOINTS AVAILABILITY
        
        Verify that the required API endpoints are available and responding.
        """
        print("\n🔗 TESTING API ENDPOINTS AVAILABILITY")
        print("-" * 50)
        
        endpoints_to_test = [
            "/medical-ai/intent-classification",
            "/medical-ai/multi-message-intent"
        ]
        
        for endpoint in endpoints_to_test:
            try:
                # Test with a simple POST request
                response = requests.post(f"{self.api_base}{endpoint}",
                    json={"message": "test connectivity"},
                    timeout=10
                )
                
                # Accept any response that's not a connection error
                if response.status_code in [200, 400, 422]:  # 400/422 are expected for invalid data
                    self.log_test(f"API Endpoint {endpoint}", True, 
                                f"Endpoint available (HTTP {response.status_code})")
                else:
                    self.log_test(f"API Endpoint {endpoint}", False,
                                f"Unexpected status code: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                self.log_test(f"API Endpoint {endpoint}", False,
                            f"Connection error: {str(e)}")
    
    def test_new_subspecialty_categories(self):
        """
        🏥 TEST NEW SUBSPECIALTY CATEGORIES VALIDATION
        
        Test all 12 new subspecialty categories across 5 medical domains:
        - Cardiovascular (3 categories)
        - Neurological (3 categories) 
        - Gastrointestinal (2 categories)
        - Respiratory (2 categories)
        - Endocrine (2 categories)
        """
        print("\n🏥 TESTING NEW SUBSPECIALTY CATEGORIES")
        print("-" * 50)
        
        subspecialty_test_cases = [
            # CARDIOVASCULAR SUBSPECIALTY (3 categories)
            {
                "category": "cardiac_chest_pain_assessment",
                "subspecialty": "cardiology",
                "test_message": "I have crushing chest pain that feels like an elephant sitting on my chest, radiating down my left arm",
                "expected_urgency": "critical",
                "expected_confidence": 0.90,
                "clinical_significance": "critical"
            },
            {
                "category": "cardiac_symptom_evaluation", 
                "subspecialty": "cardiology",
                "test_message": "My heart has been racing and I get short of breath when I climb stairs",
                "expected_urgency": "high",
                "expected_confidence": 0.85,
                "clinical_significance": "high"
            },
            {
                "category": "cardiovascular_risk_assessment",
                "subspecialty": "cardiology", 
                "test_message": "I have a family history of heart disease and my cholesterol is high",
                "expected_urgency": "medium",
                "expected_confidence": 0.80,
                "clinical_significance": "medium"
            },
            
            # NEUROLOGICAL SUBSPECIALTY (3 categories)
            {
                "category": "neurological_symptom_assessment",
                "subspecialty": "neurology",
                "test_message": "I have sudden weakness in my right arm and my face feels numb",
                "expected_urgency": "high", 
                "expected_confidence": 0.90,
                "clinical_significance": "high"
            },
            {
                "category": "headache_migraine_evaluation",
                "subspecialty": "neurology",
                "test_message": "I have the worst headache of my life with neck stiffness and sensitivity to light",
                "expected_urgency": "critical",
                "expected_confidence": 0.95,
                "clinical_significance": "critical"
            },
            {
                "category": "neurological_emergency_detection",
                "subspecialty": "neurology",
                "test_message": "I think I'm having a stroke - my speech is slurred and my face is drooping",
                "expected_urgency": "critical",
                "expected_confidence": 0.95,
                "clinical_significance": "critical"
            },
            
            # GASTROINTESTINAL SUBSPECIALTY (2 categories)
            {
                "category": "gi_symptom_assessment",
                "subspecialty": "gastroenterology",
                "test_message": "I have severe abdominal pain and there's blood in my stool",
                "expected_urgency": "high",
                "expected_confidence": 0.90,
                "clinical_significance": "high"
            },
            {
                "category": "digestive_disorder_evaluation",
                "subspecialty": "gastroenterology",
                "test_message": "I have chronic diarrhea and cramping that's been going on for months",
                "expected_urgency": "medium",
                "expected_confidence": 0.80,
                "clinical_significance": "medium"
            },
            
            # RESPIRATORY SUBSPECIALTY (2 categories)
            {
                "category": "respiratory_symptom_assessment",
                "subspecialty": "pulmonology",
                "test_message": "I can't breathe properly and I'm wheezing badly",
                "expected_urgency": "high",
                "expected_confidence": 0.90,
                "clinical_significance": "high"
            },
            {
                "category": "breathing_difficulty_evaluation",
                "subspecialty": "pulmonology", 
                "test_message": "My asthma has been getting worse and I'm having trouble with daily activities",
                "expected_urgency": "high",
                "expected_confidence": 0.85,
                "clinical_significance": "high"
            },
            
            # ENDOCRINE SUBSPECIALTY (2 categories)
            {
                "category": "endocrine_symptom_assessment",
                "subspecialty": "endocrinology",
                "test_message": "My blood sugar has been out of control for weeks and I'm always thirsty",
                "expected_urgency": "high",
                "expected_confidence": 0.85,
                "clinical_significance": "medium"
            },
            {
                "category": "metabolic_disorder_evaluation",
                "subspecialty": "endocrinology",
                "test_message": "I have unexplained weight gain and fatigue despite getting enough sleep",
                "expected_urgency": "medium",
                "expected_confidence": 0.80,
                "clinical_significance": "medium"
            }
        ]
        
        subspecialty_results = []
        total_processing_time = 0.0
        
        for i, test_case in enumerate(subspecialty_test_cases, 1):
            print(f"\n🎯 Testing {test_case['category']} ({test_case['subspecialty']})")
            print(f"Message: {test_case['test_message'][:80]}...")
            
            try:
                start_time = time.time()
                
                response = requests.post(f"{self.api_base}/medical-ai/intent-classification",
                    json={
                        "message": test_case["test_message"],
                        "conversation_context": {
                            "patient_id": f"test-subspecialty-{i}",
                            "timestamp": datetime.now().isoformat()
                        }
                    },
                    timeout=30
                )
                
                processing_time = (time.time() - start_time) * 1000  # Convert to ms
                total_processing_time += processing_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate subspecialty classification
                    primary_intent = data.get("primary_intent", "")
                    confidence_score = data.get("confidence_score", 0.0)
                    urgency_level = data.get("urgency_level", "low")
                    clinical_reasoning = data.get("clinical_reasoning", "")
                    
                    # Check if the expected category is detected
                    category_detected = test_case["category"] in primary_intent or any(
                        test_case["category"] in intent[0] for intent in data.get("all_detected_intents", [])
                    )
                    
                    # Validate confidence score
                    confidence_met = confidence_score >= test_case["expected_confidence"]
                    
                    # Validate urgency level (allow for higher urgency than expected)
                    urgency_levels = ["low", "medium", "high", "urgent", "critical", "emergency"]
                    expected_urgency_index = urgency_levels.index(test_case["expected_urgency"])
                    actual_urgency_index = urgency_levels.index(urgency_level) if urgency_level in urgency_levels else 0
                    urgency_appropriate = actual_urgency_index >= expected_urgency_index
                    
                    # Check for subspecialty-specific clinical reasoning
                    subspecialty_reasoning = test_case["subspecialty"] in clinical_reasoning.lower()
                    
                    # Validate processing time (<50ms target)
                    performance_met = processing_time < 50.0
                    
                    test_result = {
                        "category": test_case["category"],
                        "subspecialty": test_case["subspecialty"],
                        "category_detected": category_detected,
                        "confidence_score": confidence_score,
                        "confidence_met": confidence_met,
                        "urgency_level": urgency_level,
                        "urgency_appropriate": urgency_appropriate,
                        "subspecialty_reasoning": subspecialty_reasoning,
                        "processing_time_ms": processing_time,
                        "performance_met": performance_met,
                        "success": (category_detected and confidence_met and 
                                  urgency_appropriate and performance_met)
                    }
                    
                    subspecialty_results.append(test_result)
                    
                    status = "✅ PASS" if test_result["success"] else "❌ FAIL"
                    print(f"   {status} - Intent: {primary_intent}, Confidence: {confidence_score:.3f}, "
                          f"Urgency: {urgency_level}, Time: {processing_time:.1f}ms")
                    
                    if not test_result["success"]:
                        issues = []
                        if not category_detected:
                            issues.append("category not detected")
                        if not confidence_met:
                            issues.append(f"confidence {confidence_score:.3f} < {test_case['expected_confidence']}")
                        if not urgency_appropriate:
                            issues.append(f"urgency {urgency_level} < {test_case['expected_urgency']}")
                        if not performance_met:
                            issues.append(f"time {processing_time:.1f}ms > 50ms")
                        print(f"   Issues: {', '.join(issues)}")
                    
                else:
                    print(f"   ❌ FAIL - HTTP {response.status_code}: {response.text[:100]}")
                    subspecialty_results.append({
                        "category": test_case["category"],
                        "success": False,
                        "error": f"HTTP {response.status_code}"
                    })
                    
            except Exception as e:
                print(f"   ❌ FAIL - Exception: {str(e)}")
                subspecialty_results.append({
                    "category": test_case["category"],
                    "success": False,
                    "error": str(e)
                })
        
        # Calculate overall subspecialty metrics
        successful_categories = sum(1 for r in subspecialty_results if r.get("success", False))
        avg_processing_time = total_processing_time / len(subspecialty_test_cases) if subspecialty_test_cases else 0
        avg_confidence = sum(r.get("confidence_score", 0) for r in subspecialty_results) / len(subspecialty_results) if subspecialty_results else 0
        
        subspecialty_summary = {
            "categories_passed": successful_categories,
            "total_categories": len(subspecialty_test_cases),
            "success_rate": (successful_categories / len(subspecialty_test_cases)) * 100,
            "average_processing_time_ms": avg_processing_time,
            "average_confidence_score": avg_confidence,
            "performance_target_met": avg_processing_time < 50.0,
            "individual_results": subspecialty_results
        }
        
        # Log overall subspecialty test result
        subspecialty_passed = successful_categories >= len(subspecialty_test_cases) * 0.8  # 80% pass rate
        
        self.log_test("New Subspecialty Categories Validation", subspecialty_passed,
                     f"Success Rate: {subspecialty_summary['success_rate']:.1f}%, "
                     f"Avg Time: {avg_processing_time:.1f}ms, "
                     f"Avg Confidence: {avg_confidence:.3f}",
                     subspecialty_summary)
        
        print(f"\n📊 SUBSPECIALTY CATEGORIES SUMMARY:")
        print(f"   Categories Passed: {successful_categories}/{len(subspecialty_test_cases)}")
        print(f"   Success Rate: {subspecialty_summary['success_rate']:.1f}%")
        print(f"   Average Processing Time: {avg_processing_time:.1f}ms (Target: <50ms)")
        print(f"   Average Confidence Score: {avg_confidence:.3f}")
        print(f"   Performance Target Met: {'✅' if subspecialty_summary['performance_target_met'] else '❌'}")
        
        return subspecialty_passed
    
    def test_high_priority_emergency_scenarios(self):
        """
        🚨 TEST HIGH PRIORITY EMERGENCY SCENARIOS
        
        Test the 5 high-priority emergency scenarios from the review request:
        1. Cardiology Emergency
        2. Neurology Emergency  
        3. GI Emergency
        4. Respiratory Emergency
        5. Endocrine Concern
        """
        print("\n🚨 TESTING HIGH PRIORITY EMERGENCY SCENARIOS")
        print("-" * 50)
        
        emergency_scenarios = [
            {
                "name": "Cardiology Emergency",
                "message": "I have crushing chest pain that radiates to my left arm and shortness of breath",
                "expected_intent": "cardiac_chest_pain_assessment",
                "expected_urgency": "critical",
                "expected_confidence": 0.90,
                "emergency_protocol": True
            },
            {
                "name": "Neurology Emergency", 
                "message": "I have sudden weakness in my right arm and slurred speech",
                "expected_intent": "neurological_emergency_detection",
                "expected_urgency": "critical",
                "expected_confidence": 0.90,
                "emergency_protocol": True
            },
            {
                "name": "GI Emergency",
                "message": "I have severe abdominal pain and blood in my stool",
                "expected_intent": "gi_symptom_assessment", 
                "expected_urgency": "high",
                "expected_confidence": 0.90,
                "emergency_protocol": True
            },
            {
                "name": "Respiratory Emergency",
                "message": "I can't breathe and I'm wheezing badly",
                "expected_intent": "respiratory_symptom_assessment",
                "expected_urgency": "high",
                "expected_confidence": 0.90,
                "emergency_protocol": True
            },
            {
                "name": "Endocrine Concern",
                "message": "My blood sugar has been out of control for weeks",
                "expected_intent": "endocrine_symptom_assessment",
                "expected_urgency": "high",
                "expected_confidence": 0.85,
                "emergency_protocol": False
            }
        ]
        
        emergency_results = []
        total_processing_time = 0.0
        
        for i, scenario in enumerate(emergency_scenarios, 1):
            print(f"\n🎯 Testing {scenario['name']}")
            print(f"Message: {scenario['message']}")
            
            try:
                start_time = time.time()
                
                response = requests.post(f"{self.api_base}/medical-ai/intent-classification",
                    json={
                        "message": scenario["message"],
                        "conversation_context": {
                            "patient_id": f"emergency-test-{i}",
                            "timestamp": datetime.now().isoformat()
                        }
                    },
                    timeout=30
                )
                
                processing_time = (time.time() - start_time) * 1000
                total_processing_time += processing_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    primary_intent = data.get("primary_intent", "")
                    confidence_score = data.get("confidence_score", 0.0)
                    urgency_level = data.get("urgency_level", "low")
                    clinical_reasoning = data.get("clinical_reasoning", "")
                    red_flag_indicators = data.get("red_flag_indicators", [])
                    
                    # Validate intent detection
                    intent_detected = (scenario["expected_intent"] in primary_intent or 
                                     any(scenario["expected_intent"] in intent[0] 
                                         for intent in data.get("all_detected_intents", [])))
                    
                    # Validate confidence
                    confidence_met = confidence_score >= scenario["expected_confidence"]
                    
                    # Validate urgency
                    urgency_levels = ["low", "medium", "high", "urgent", "critical", "emergency"]
                    expected_urgency_index = urgency_levels.index(scenario["expected_urgency"])
                    actual_urgency_index = urgency_levels.index(urgency_level) if urgency_level in urgency_levels else 0
                    urgency_appropriate = actual_urgency_index >= expected_urgency_index
                    
                    # Check emergency protocol activation
                    emergency_activated = (scenario["emergency_protocol"] and 
                                         (urgency_level in ["critical", "emergency"] or 
                                          len(red_flag_indicators) > 0))
                    
                    # Validate processing time
                    performance_met = processing_time < 50.0
                    
                    # Check for subspecialty-specific reasoning
                    subspecialty_reasoning = any(subspecialty in clinical_reasoning.lower() 
                                               for subspecialty in ["cardiology", "neurology", "gastroenterology", 
                                                                   "pulmonology", "endocrinology"])
                    
                    scenario_result = {
                        "scenario": scenario["name"],
                        "intent_detected": intent_detected,
                        "confidence_score": confidence_score,
                        "confidence_met": confidence_met,
                        "urgency_level": urgency_level,
                        "urgency_appropriate": urgency_appropriate,
                        "emergency_activated": emergency_activated or not scenario["emergency_protocol"],
                        "subspecialty_reasoning": subspecialty_reasoning,
                        "processing_time_ms": processing_time,
                        "performance_met": performance_met,
                        "success": (intent_detected and confidence_met and urgency_appropriate and 
                                  (emergency_activated or not scenario["emergency_protocol"]) and 
                                  performance_met)
                    }
                    
                    emergency_results.append(scenario_result)
                    
                    status = "✅ PASS" if scenario_result["success"] else "❌ FAIL"
                    print(f"   {status} - Intent: {primary_intent}, Confidence: {confidence_score:.3f}, "
                          f"Urgency: {urgency_level}, Time: {processing_time:.1f}ms")
                    
                    if scenario["emergency_protocol"] and urgency_level in ["critical", "emergency"]:
                        print(f"   🚨 Emergency Protocol Activated: {urgency_level}")
                    
                    if not scenario_result["success"]:
                        issues = []
                        if not intent_detected:
                            issues.append("intent not detected")
                        if not confidence_met:
                            issues.append(f"confidence {confidence_score:.3f} < {scenario['expected_confidence']}")
                        if not urgency_appropriate:
                            issues.append(f"urgency {urgency_level} < {scenario['expected_urgency']}")
                        if scenario["emergency_protocol"] and not emergency_activated:
                            issues.append("emergency protocol not activated")
                        if not performance_met:
                            issues.append(f"time {processing_time:.1f}ms > 50ms")
                        print(f"   Issues: {', '.join(issues)}")
                    
                else:
                    print(f"   ❌ FAIL - HTTP {response.status_code}: {response.text[:100]}")
                    emergency_results.append({
                        "scenario": scenario["name"],
                        "success": False,
                        "error": f"HTTP {response.status_code}"
                    })
                    
            except Exception as e:
                print(f"   ❌ FAIL - Exception: {str(e)}")
                emergency_results.append({
                    "scenario": scenario["name"],
                    "success": False,
                    "error": str(e)
                })
        
        # Calculate emergency scenario metrics
        successful_scenarios = sum(1 for r in emergency_results if r.get("success", False))
        avg_processing_time = total_processing_time / len(emergency_scenarios) if emergency_scenarios else 0
        avg_confidence = sum(r.get("confidence_score", 0) for r in emergency_results) / len(emergency_results) if emergency_results else 0
        
        emergency_summary = {
            "scenarios_passed": successful_scenarios,
            "total_scenarios": len(emergency_scenarios),
            "success_rate": (successful_scenarios / len(emergency_scenarios)) * 100,
            "average_processing_time_ms": avg_processing_time,
            "average_confidence_score": avg_confidence,
            "individual_results": emergency_results
        }
        
        # Log overall emergency scenarios test result
        emergency_passed = successful_scenarios >= len(emergency_scenarios) * 0.8  # 80% pass rate for comprehensive testing
        
        self.log_test("High Priority Emergency Scenarios", emergency_passed,
                     f"Success Rate: {emergency_summary['success_rate']:.1f}%, "
                     f"Avg Time: {avg_processing_time:.1f}ms, "
                     f"Avg Confidence: {avg_confidence:.3f}",
                     emergency_summary)
        
        print(f"\n📊 EMERGENCY SCENARIOS SUMMARY:")
        print(f"   Scenarios Passed: {successful_scenarios}/{len(emergency_scenarios)}")
        print(f"   Success Rate: {emergency_summary['success_rate']:.1f}%")
        print(f"   Average Processing Time: {avg_processing_time:.1f}ms (Target: <50ms)")
        print(f"   Average Confidence Score: {avg_confidence:.3f}")
        
        return emergency_passed
    
    def test_algorithm_version_validation(self):
        """
        🔧 TEST ALGORITHM VERSION VALIDATION
        
        Verify that the system is running Algorithm Version 3.1_intelligence_amplification
        """
        print("\n🔧 TESTING ALGORITHM VERSION VALIDATION")
        print("-" * 50)
        
        try:
            response = requests.post(f"{self.api_base}/medical-ai/intent-classification",
                json={
                    "message": "Test algorithm version",
                    "conversation_context": {
                        "patient_id": "version-test",
                        "timestamp": datetime.now().isoformat()
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                algorithm_version = data.get("algorithm_version", "")
                
                expected_version = "3.1_intelligence_amplification"
                version_correct = expected_version in algorithm_version
                
                self.log_test("Algorithm Version Validation", version_correct,
                            f"Expected: {expected_version}, Got: {algorithm_version}")
                
                print(f"   Algorithm Version: {algorithm_version}")
                print(f"   Expected: {expected_version}")
                print(f"   Status: {'✅ CORRECT' if version_correct else '❌ INCORRECT'}")
                
                return version_correct
            else:
                self.log_test("Algorithm Version Validation", False,
                            f"HTTP {response.status_code}: {response.text[:100]}")
                return False
                
        except Exception as e:
            self.log_test("Algorithm Version Validation", False, f"Exception: {str(e)}")
            return False
    
    def run_comprehensive_tests(self):
        """Run all comprehensive Week 1 subspecialty intent classification tests"""
        print("🎯 WEEK 1 SUBSPECIALTY INTENT CLASSIFICATION COMPREHENSIVE TESTING")
        print("=" * 80)
        print(f"Backend URL: {self.backend_url}")
        print(f"Testing started at: {datetime.now().isoformat()}")
        print()
        
        # Run all tests
        test_methods = [
            self.test_api_endpoints_availability,
            self.test_algorithm_version_validation,
            self.test_new_subspecialty_categories,
            self.test_high_priority_emergency_scenarios
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.log_test(test_method.__name__, False, f"Test execution failed: {str(e)}")
        
        # Print comprehensive summary
        print("\n" + "=" * 80)
        print("🎯 WEEK 1 SUBSPECIALTY INTENT CLASSIFICATION TEST SUMMARY")
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
    tester = Week1SubspecialtyIntentTester()
    passed, failed, total = tester.run_comprehensive_tests()
    
    # Exit with appropriate code
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Week 1 Subspecialty Intent Classification system is working correctly.")
        sys.exit(0)
    else:
        print(f"\n⚠️  {failed} TESTS FAILED. Week 1 Subspecialty Intent Classification system needs attention.")
        sys.exit(1)

if __name__ == "__main__":
    main()