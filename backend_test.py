#!/usr/bin/env python3
"""
🧠 ENHANCED MEDICAL INTENT CLASSIFIER TESTING SUITE 🧠

Comprehensive backend testing for the enhanced medical intent classifier with fixes 
and expanded subspecialty categories as requested in the review.

TESTING OBJECTIVES:
✅ TEST 3 Fixed Categories that were previously failing
✅ TEST New Subspecialty Categories (20 new ones across different domains)  
✅ VALIDATE Algorithm Version 3.2_comprehensive_subspecialty_expansion
✅ VERIFY Performance under 50ms target
✅ TEST Emergency/Urgent Classification with appropriate urgency levels
✅ ENSURE no pattern conflicts or incorrect classifications

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
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://context-flow-check.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class MedicalIntentClassifierTester:
    """Comprehensive tester for Enhanced Medical Intent Classifier"""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.performance_times = []
        
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

    def test_fixed_categories(self) -> bool:
        """
        🔧 TEST 3 FIXED CATEGORIES
        
        Test the 3 categories that were previously failing:
        1. cardiac_symptom_evaluation (was detected as unclear_intent)
        2. neurological_symptom_assessment (was misclassified as neurological_emergency_detection)  
        3. metabolic_disorder_evaluation (was detected as unclear_intent)
        """
        print("\n🔧 TESTING 3 FIXED CATEGORIES")
        print("-" * 50)
        
        fixed_category_tests = [
            {
                "name": "cardiac_symptom_evaluation - heart symptoms",
                "message": "I've been having heart symptoms lately, my heart feels weird",
                "expected_intent": "cardiac_symptom_evaluation",
                "expected_confidence": 0.8
            },
            {
                "name": "cardiac_symptom_evaluation - cardiac problems", 
                "message": "I'm concerned about cardiac problems, having some heart issues",
                "expected_intent": "cardiac_symptom_evaluation",
                "expected_confidence": 0.8
            },
            {
                "name": "cardiac_symptom_evaluation - my heart feels",
                "message": "My heart feels like it's racing and I'm worried about it",
                "expected_intent": "cardiac_symptom_evaluation", 
                "expected_confidence": 0.8
            },
            {
                "name": "neurological_symptom_assessment - neurological symptoms",
                "message": "I've been experiencing neurological symptoms, some nerve problems",
                "expected_intent": "neurological_symptom_assessment",
                "expected_confidence": 0.8
            },
            {
                "name": "neurological_symptom_assessment - nerve problems",
                "message": "Having nerve problems and some movement disorders recently",
                "expected_intent": "neurological_symptom_assessment",
                "expected_confidence": 0.8
            },
            {
                "name": "neurological_symptom_assessment - movement disorders",
                "message": "I'm having movement disorders and coordination problems",
                "expected_intent": "neurological_symptom_assessment",
                "expected_confidence": 0.8
            },
            {
                "name": "metabolic_disorder_evaluation - metabolic problems",
                "message": "I think I have metabolic problems, my metabolism seems off",
                "expected_intent": "metabolic_disorder_evaluation",
                "expected_confidence": 0.8
            },
            {
                "name": "metabolic_disorder_evaluation - hormone imbalance",
                "message": "I suspect a hormone imbalance, having hormonal issues",
                "expected_intent": "metabolic_disorder_evaluation",
                "expected_confidence": 0.8
            },
            {
                "name": "metabolic_disorder_evaluation - endocrine issues",
                "message": "Having endocrine issues and glandular problems lately",
                "expected_intent": "metabolic_disorder_evaluation",
                "expected_confidence": 0.8
            }
        ]
        
        all_passed = True
        
        for test_case in fixed_category_tests:
            try:
                start_time = time.time()
                
                response = requests.post(f"{API_BASE}/medical-ai/intent-classification",
                    json={
                        "message": test_case["message"],
                        "context": {}
                    },
                    timeout=30
                )
                
                processing_time = (time.time() - start_time) * 1000
                self.performance_times.append(processing_time)
                
                if response.status_code == 200:
                    data = response.json()
                    primary_intent = data.get("primary_intent", "")
                    confidence_score = data.get("confidence_score", 0.0)
                    
                    # Check if the intent matches expected
                    intent_correct = primary_intent == test_case["expected_intent"]
                    confidence_adequate = confidence_score >= test_case["expected_confidence"]
                    
                    if intent_correct and confidence_adequate:
                        self.log_test(test_case["name"], True,
                                    f"Intent: {primary_intent}, Confidence: {confidence_score:.3f}, Time: {processing_time:.1f}ms")
                    else:
                        self.log_test(test_case["name"], False,
                                    f"Expected: {test_case['expected_intent']}, Got: {primary_intent}, Confidence: {confidence_score:.3f}")
                        all_passed = False
                else:
                    self.log_test(test_case["name"], False,
                                f"HTTP {response.status_code}: {response.text}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(test_case["name"], False, f"Exception: {str(e)}")
                all_passed = False
        
        return all_passed

    def test_new_subspecialty_categories(self) -> bool:
        """
        🆕 TEST NEW SUBSPECIALTY CATEGORIES
        
        Test a representative sample of the 20 new subspecialty categories across different domains
        """
        print("\n🆕 TESTING NEW SUBSPECIALTY CATEGORIES")
        print("-" * 50)
        
        subspecialty_tests = [
            # Orthopedics
            {
                "name": "orthopedic_injury_assessment - bone fracture",
                "message": "I think I have a bone fracture in my arm, it's really painful",
                "expected_intent": "orthopedic_injury_assessment",
                "expected_confidence": 0.8
            },
            {
                "name": "sports_medicine_evaluation - joint injury", 
                "message": "I have a joint injury from playing sports, knee is swollen",
                "expected_intent": "sports_medicine_evaluation",
                "expected_confidence": 0.8
            },
            {
                "name": "sports_medicine_evaluation - sports injury",
                "message": "Got a sports injury during the game, need evaluation",
                "expected_intent": "sports_medicine_evaluation", 
                "expected_confidence": 0.8
            },
            
            # Dermatology
            {
                "name": "dermatological_assessment - skin rash",
                "message": "I have a skin rash that's been spreading, very itchy",
                "expected_intent": "dermatological_assessment",
                "expected_confidence": 0.8
            },
            {
                "name": "dermatological_assessment - suspicious mole",
                "message": "I have a suspicious mole that's changing color and shape",
                "expected_intent": "dermatological_assessment",
                "expected_confidence": 0.8
            },
            {
                "name": "dermatological_assessment - acne problems",
                "message": "Having severe acne problems, lots of breakouts recently",
                "expected_intent": "dermatological_assessment",
                "expected_confidence": 0.8
            },
            
            # Allergy/Immunology
            {
                "name": "allergic_reaction_assessment - allergic reaction",
                "message": "I'm having an allergic reaction, hives and swelling",
                "expected_intent": "allergic_reaction_assessment",
                "expected_confidence": 0.8
            },
            {
                "name": "immunodeficiency_evaluation - frequent infections",
                "message": "I keep getting frequent infections, immune system seems weak",
                "expected_intent": "immunodeficiency_evaluation",
                "expected_confidence": 0.8
            },
            
            # Mental Health
            {
                "name": "psychiatric_assessment - depression symptoms",
                "message": "I've been having depression symptoms, feeling hopeless",
                "expected_intent": "psychiatric_assessment",
                "expected_confidence": 0.8
            },
            {
                "name": "psychiatric_assessment - anxiety problems",
                "message": "Having severe anxiety problems, panic attacks daily",
                "expected_intent": "psychiatric_assessment",
                "expected_confidence": 0.8
            },
            {
                "name": "substance_abuse_evaluation - substance abuse",
                "message": "I think I have a substance abuse problem, need help",
                "expected_intent": "substance_abuse_evaluation",
                "expected_confidence": 0.8
            },
            
            # Pediatrics
            {
                "name": "pediatric_assessment - child fever",
                "message": "My child has a high fever and seems very sick",
                "expected_intent": "pediatric_assessment",
                "expected_confidence": 0.8
            },
            {
                "name": "pediatric_assessment - developmental delay",
                "message": "Concerned about developmental delay in my toddler",
                "expected_intent": "pediatric_assessment",
                "expected_confidence": 0.8
            },
            
            # Women's Health
            {
                "name": "obstetric_assessment - pregnancy bleeding",
                "message": "I'm pregnant and having some bleeding, very worried",
                "expected_intent": "obstetric_assessment",
                "expected_confidence": 0.8
            },
            {
                "name": "gynecological_assessment - menstrual problems",
                "message": "Having menstrual problems, periods are very irregular",
                "expected_intent": "gynecological_assessment",
                "expected_confidence": 0.8
            },
            
            # Oncology
            {
                "name": "cancer_screening_assessment - cancer screening",
                "message": "I need cancer screening, family history of cancer",
                "expected_intent": "cancer_screening_assessment",
                "expected_confidence": 0.8
            },
            {
                "name": "chemotherapy_monitoring - chemotherapy side effects",
                "message": "Having bad chemotherapy side effects, nausea and fatigue",
                "expected_intent": "chemotherapy_monitoring",
                "expected_confidence": 0.8
            },
            
            # Pain Management
            {
                "name": "chronic_pain_assessment - chronic pain",
                "message": "I have chronic pain that's been going on for months",
                "expected_intent": "chronic_pain_assessment",
                "expected_confidence": 0.8
            },
            {
                "name": "opioid_management - opioid withdrawal",
                "message": "Going through opioid withdrawal, need medical help",
                "expected_intent": "opioid_management",
                "expected_confidence": 0.8
            }
        ]
        
        all_passed = True
        
        for test_case in subspecialty_tests:
            try:
                start_time = time.time()
                
                response = requests.post(f"{API_BASE}/medical-ai/intent-classification",
                    json={
                        "message": test_case["message"],
                        "context": {}
                    },
                    timeout=30
                )
                
                processing_time = (time.time() - start_time) * 1000
                self.performance_times.append(processing_time)
                
                if response.status_code == 200:
                    data = response.json()
                    primary_intent = data.get("primary_intent", "")
                    confidence_score = data.get("confidence_score", 0.0)
                    
                    # Check if the intent matches expected
                    intent_correct = primary_intent == test_case["expected_intent"]
                    confidence_adequate = confidence_score >= test_case["expected_confidence"]
                    
                    if intent_correct and confidence_adequate:
                        self.log_test(test_case["name"], True,
                                    f"Intent: {primary_intent}, Confidence: {confidence_score:.3f}, Time: {processing_time:.1f}ms")
                    else:
                        self.log_test(test_case["name"], False,
                                    f"Expected: {test_case['expected_intent']}, Got: {primary_intent}, Confidence: {confidence_score:.3f}")
                        all_passed = False
                else:
                    self.log_test(test_case["name"], False,
                                f"HTTP {response.status_code}: {response.text}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(test_case["name"], False, f"Exception: {str(e)}")
                all_passed = False
        
        return all_passed

    def test_algorithm_version_validation(self) -> bool:
        """
        📋 TEST ALGORITHM VERSION VALIDATION
        
        Verify the system is running Algorithm Version 3.2_comprehensive_subspecialty_expansion
        """
        print("\n📋 TESTING ALGORITHM VERSION VALIDATION")
        print("-" * 50)
        
        try:
            # Test with a simple message to get algorithm version info
            response = requests.post(f"{API_BASE}/medical-ai/intent-classification",
                json={
                    "message": "I have a headache",
                    "context": {}
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                algorithm_version = data.get("algorithm_version", "")
                
                expected_version = "3.2_comprehensive_subspecialty_expansion"
                version_correct = algorithm_version == expected_version
                
                if version_correct:
                    self.log_test("Algorithm Version Validation", True,
                                f"Algorithm Version: {algorithm_version}")
                    return True
                else:
                    self.log_test("Algorithm Version Validation", False,
                                f"Expected: {expected_version}, Got: {algorithm_version}")
                    return False
            else:
                self.log_test("Algorithm Version Validation", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Algorithm Version Validation", False, f"Exception: {str(e)}")
            return False

    def test_performance_requirements(self) -> bool:
        """
        ⚡ TEST PERFORMANCE REQUIREMENTS
        
        Ensure processing times remain under 50ms target with expanded taxonomy
        """
        print("\n⚡ TESTING PERFORMANCE REQUIREMENTS")
        print("-" * 50)
        
        if not self.performance_times:
            self.log_test("Performance Requirements", False, "No performance data collected")
            return False
        
        avg_time = sum(self.performance_times) / len(self.performance_times)
        max_time = max(self.performance_times)
        min_time = min(self.performance_times)
        
        # Target is under 50ms
        target_time = 50.0
        
        performance_met = avg_time <= target_time and max_time <= (target_time * 2)  # Allow some tolerance for max
        
        if performance_met:
            self.log_test("Performance Requirements", True,
                        f"Avg: {avg_time:.1f}ms, Max: {max_time:.1f}ms, Min: {min_time:.1f}ms (Target: <{target_time}ms)")
            return True
        else:
            self.log_test("Performance Requirements", False,
                        f"Performance too slow. Avg: {avg_time:.1f}ms, Max: {max_time:.1f}ms (Target: <{target_time}ms)")
            return False

    def test_emergency_urgent_classification(self) -> bool:
        """
        🚨 TEST EMERGENCY/URGENT CLASSIFICATION
        
        Test that new emergency and urgent categories are properly classified with appropriate urgency levels
        """
        print("\n🚨 TESTING EMERGENCY/URGENT CLASSIFICATION")
        print("-" * 50)
        
        emergency_tests = [
            {
                "name": "Emergency - Crushing chest pain",
                "message": "I have crushing chest pain radiating to my arm, can't breathe",
                "expected_urgency": "emergency",
                "min_confidence": 0.8
            },
            {
                "name": "Emergency - Stroke symptoms",
                "message": "Sudden weakness on one side, facial drooping, slurred speech",
                "expected_urgency": "emergency", 
                "min_confidence": 0.8
            },
            {
                "name": "Emergency - Severe allergic reaction",
                "message": "Having severe allergic reaction, throat swelling, can't breathe",
                "expected_urgency": "emergency",
                "min_confidence": 0.8
            },
            {
                "name": "Urgent - Severe abdominal pain",
                "message": "Severe abdominal pain with vomiting, getting worse",
                "expected_urgency": "urgent",
                "min_confidence": 0.7
            },
            {
                "name": "Urgent - High fever in child",
                "message": "My child has very high fever and is lethargic",
                "expected_urgency": "urgent",
                "min_confidence": 0.7
            },
            {
                "name": "Urgent - Pregnancy bleeding",
                "message": "I'm pregnant and having heavy bleeding with cramping",
                "expected_urgency": "urgent",
                "min_confidence": 0.7
            }
        ]
        
        all_passed = True
        
        for test_case in emergency_tests:
            try:
                start_time = time.time()
                
                response = requests.post(f"{API_BASE}/medical-ai/intent-classification",
                    json={
                        "message": test_case["message"],
                        "context": {}
                    },
                    timeout=30
                )
                
                processing_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    data = response.json()
                    urgency_level = data.get("urgency_level", "")
                    confidence_score = data.get("confidence_score", 0.0)
                    
                    urgency_correct = urgency_level == test_case["expected_urgency"]
                    confidence_adequate = confidence_score >= test_case["min_confidence"]
                    
                    if urgency_correct and confidence_adequate:
                        self.log_test(test_case["name"], True,
                                    f"Urgency: {urgency_level}, Confidence: {confidence_score:.3f}, Time: {processing_time:.1f}ms")
                    else:
                        self.log_test(test_case["name"], False,
                                    f"Expected urgency: {test_case['expected_urgency']}, Got: {urgency_level}, Confidence: {confidence_score:.3f}")
                        all_passed = False
                else:
                    self.log_test(test_case["name"], False,
                                f"HTTP {response.status_code}: {response.text}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(test_case["name"], False, f"Exception: {str(e)}")
                all_passed = False
        
        return all_passed

    def test_pattern_conflicts(self) -> bool:
        """
        🔍 TEST PATTERN CONFLICTS
        
        Ensure the enhanced patterns don't create conflicts or incorrect classifications
        """
        print("\n🔍 TESTING PATTERN CONFLICTS")
        print("-" * 50)
        
        conflict_tests = [
            {
                "name": "Neurological vs Emergency - Mild headache",
                "message": "I have a mild headache that started this morning",
                "should_not_be": "neurological_emergency_detection",
                "expected_urgency_not": "emergency"
            },
            {
                "name": "Cardiac vs Emergency - Heart palpitations",
                "message": "I sometimes get heart palpitations when I'm stressed",
                "should_not_be": "emergency_concern",
                "expected_urgency_not": "emergency"
            },
            {
                "name": "GI vs Emergency - Mild stomach ache",
                "message": "I have a mild stomach ache after eating",
                "should_not_be": "emergency_concern",
                "expected_urgency_not": "emergency"
            },
            {
                "name": "Metabolic vs Cardiac - Weight gain",
                "message": "I've been gaining weight unexpectedly lately",
                "should_not_be": "cardiac_symptom_evaluation",
                "expected_urgency_not": "emergency"
            },
            {
                "name": "Routine vs Urgent - General wellness",
                "message": "I want to discuss my general wellness and health goals",
                "should_not_be": "emergency_concern",
                "expected_urgency_not": "urgent"
            }
        ]
        
        all_passed = True
        
        for test_case in conflict_tests:
            try:
                response = requests.post(f"{API_BASE}/medical-ai/intent-classification",
                    json={
                        "message": test_case["message"],
                        "context": {}
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    primary_intent = data.get("primary_intent", "")
                    urgency_level = data.get("urgency_level", "")
                    
                    # Check that it's NOT classified as the conflicting intent
                    intent_not_conflicted = primary_intent != test_case["should_not_be"]
                    urgency_not_conflicted = urgency_level != test_case["expected_urgency_not"]
                    
                    if intent_not_conflicted and urgency_not_conflicted:
                        self.log_test(test_case["name"], True,
                                    f"Intent: {primary_intent}, Urgency: {urgency_level} (avoided conflict)")
                    else:
                        self.log_test(test_case["name"], False,
                                    f"Conflict detected! Intent: {primary_intent}, Urgency: {urgency_level}")
                        all_passed = False
                else:
                    self.log_test(test_case["name"], False,
                                f"HTTP {response.status_code}: {response.text}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(test_case["name"], False, f"Exception: {str(e)}")
                all_passed = False
        
        return all_passed

    def run_comprehensive_tests(self):
        """Run comprehensive medical intent classifier tests"""
        print("🚀 Starting Enhanced Medical Intent Classifier Tests...")
        print(f"   Base URL: {API_BASE}")
        print("=" * 80)
        
        # Test 1: Fixed Categories
        print("\n🎯 TESTING PHASE 1: FIXED CATEGORIES")
        fixed_success = self.test_fixed_categories()
        
        # Test 2: New Subspecialty Categories
        print("\n🎯 TESTING PHASE 2: NEW SUBSPECIALTY CATEGORIES")
        subspecialty_success = self.test_new_subspecialty_categories()
        
        # Test 3: Algorithm Version Validation
        print("\n🎯 TESTING PHASE 3: ALGORITHM VERSION VALIDATION")
        version_success = self.test_algorithm_version_validation()
        
        # Test 4: Performance Requirements
        print("\n🎯 TESTING PHASE 4: PERFORMANCE REQUIREMENTS")
        performance_success = self.test_performance_requirements()
        
        # Test 5: Emergency/Urgent Classification
        print("\n🎯 TESTING PHASE 5: EMERGENCY/URGENT CLASSIFICATION")
        emergency_success = self.test_emergency_urgent_classification()
        
        # Test 6: Pattern Conflicts
        print("\n🎯 TESTING PHASE 6: PATTERN CONFLICTS")
        conflict_success = self.test_pattern_conflicts()
        
        # Print final results
        print("\n" + "=" * 80)
        print(f"📊 FINAL RESULTS")
        print(f"Tests Run: {self.total_tests}")
        print(f"Tests Passed: {self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        if self.performance_times:
            avg_time = sum(self.performance_times) / len(self.performance_times)
            print(f"Average Processing Time: {avg_time:.1f}ms")
        
        print(f"\n🎯 ENHANCED MEDICAL INTENT CLASSIFIER TEST RESULTS:")
        print(f"   1. Fixed Categories: {'✅ PASSED' if fixed_success else '❌ FAILED'}")
        print(f"   2. New Subspecialty Categories: {'✅ PASSED' if subspecialty_success else '❌ FAILED'}")
        print(f"   3. Algorithm Version Validation: {'✅ PASSED' if version_success else '❌ FAILED'}")
        print(f"   4. Performance Requirements: {'✅ PASSED' if performance_success else '❌ FAILED'}")
        print(f"   5. Emergency/Urgent Classification: {'✅ PASSED' if emergency_success else '❌ FAILED'}")
        print(f"   6. Pattern Conflicts: {'✅ PASSED' if conflict_success else '❌ FAILED'}")
        
        # Overall success
        overall_success = (fixed_success and subspecialty_success and version_success and 
                          performance_success and emergency_success and conflict_success)
        
        if overall_success:
            print("\n🎉 All enhanced medical intent classifier features passed comprehensive testing!")
            print("✅ Enhanced Medical Intent Classifier with subspecialty expansion is production-ready")
            return 0
        else:
            print("\n⚠️ Some enhanced medical intent classifier features failed testing. Check the details above.")
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result.get('passed', False):
                    print(f"  - {result['test_name']}: {result.get('details', 'Failed')}")
            return 1

if __name__ == "__main__":
    tester = MedicalIntentClassifierTester()
    exit_code = tester.run_comprehensive_tests()
    sys.exit(exit_code)