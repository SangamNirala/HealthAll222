#!/usr/bin/env python3
"""
🚀 PHASE 5: ENHANCED MEDICAL RESPONSE GENERATION SYSTEM TESTING
===============================================================

Comprehensive testing of Phase 5 Enhanced Medical Response Generation system
as requested in the review. Focus on:

1. Enhanced Medical Response Template API: POST /api/medical-ai/enhanced-response-template
2. Symptom Category Analysis API: POST /api/medical-ai/symptom-category-analysis
3. Template Structure Validation for chest_pain template
4. Robustness Testing with various symptom descriptions

TESTING REQUIREMENTS FROM REVIEW:
- Test with "chest pain" (should return cardiovascular category with appropriate questions)
- Test with "severe headache" (should return neurological category)
- Test with "shortness of breath" (should return respiratory category)
- Test with "abdominal pain" (should return gastrointestinal category)
- Verify chest_pain template includes specific questions and red flags
- Test robustness with various medical conditions dynamically

TARGET: Validate Step 5.1 from Phase 5: Enhanced Medical Response Generation
"""

import requests
import json
import time
import os
from typing import Dict, Any, List
from datetime import datetime

class Phase5EnhancedResponseTester:
    def __init__(self):
        # Get backend URL from environment
        self.backend_url = os.getenv('REACT_APP_BACKEND_URL', 'https://medchat-enhance-1.preview.emergentagent.com')
        if not self.backend_url.endswith('/api'):
            self.backend_url = f"{self.backend_url}/api"
        
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
        print(f"🚀 PHASE 5: ENHANCED MEDICAL RESPONSE GENERATION SYSTEM TESTING")
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
            "response_time_ms": round(response_time * 1000, 2),
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        print(f"   Details: {details}")
        if response_time > 0:
            print(f"   Response Time: {result['response_time_ms']}ms")
        print()

    def test_enhanced_response_template_api(self, symptom_description: str, expected_category: str = None, test_name: str = None) -> Dict[str, Any]:
        """Test the Enhanced Medical Response Template API"""
        
        if not test_name:
            test_name = f"Enhanced Response Template - {symptom_description}"
        
        print(f"🧪 Testing Enhanced Response Template API")
        print(f"Input: '{symptom_description}'")
        print(f"Expected Category: {expected_category or 'Any'}")
        
        # Prepare request payload
        payload = {
            "symptom_description": symptom_description,
            "patient_context": {
                "demographics": {"age": 45, "gender": "male"},
                "medical_history": []
            }
        }
        
        # Measure processing time
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.backend_url}/medical-ai/enhanced-response-template",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = [
                    "symptom_name", "category", "questions", "red_flags", 
                    "follow_up_protocol", "urgency_indicators", "differential_considerations",
                    "assessment_timeline", "patient_education", "when_to_seek_care",
                    "clinical_reasoning", "confidence_score", "algorithm_version"
                ]
                
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    self.log_test_result(
                        test_name,
                        False,
                        f"Missing required fields: {missing_fields}",
                        processing_time,
                        data
                    )
                    return data
                
                # Validate category if expected
                actual_category = data.get('category', '').lower()
                if expected_category and expected_category.lower() not in actual_category:
                    self.log_test_result(
                        test_name,
                        False,
                        f"Category mismatch: expected '{expected_category}', got '{actual_category}'",
                        processing_time,
                        data
                    )
                    return data
                
                # Validate content quality
                questions = data.get('questions', [])
                red_flags = data.get('red_flags', [])
                confidence = data.get('confidence_score', 0)
                
                if len(questions) < 3:
                    self.log_test_result(
                        test_name,
                        False,
                        f"Insufficient questions: {len(questions)} (expected at least 3)",
                        processing_time,
                        data
                    )
                    return data
                
                if len(red_flags) < 2:
                    self.log_test_result(
                        test_name,
                        False,
                        f"Insufficient red flags: {len(red_flags)} (expected at least 2)",
                        processing_time,
                        data
                    )
                    return data
                
                if confidence < 0.5:
                    self.log_test_result(
                        test_name,
                        False,
                        f"Low confidence score: {confidence} (expected >= 0.5)",
                        processing_time,
                        data
                    )
                    return data
                
                # Success
                details = f"Category: {actual_category}, Questions: {len(questions)}, Red Flags: {len(red_flags)}, Confidence: {confidence:.3f}"
                self.log_test_result(test_name, True, details, processing_time, data)
                return data
                
            else:
                self.log_test_result(
                    test_name,
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    processing_time
                )
                return {}
                
        except Exception as e:
            end_time = time.time()
            processing_time = end_time - start_time
            
            self.log_test_result(
                test_name,
                False,
                f"Exception: {str(e)}",
                processing_time
            )
            return {}

    def test_symptom_category_analysis_api(self, symptom_description: str, expected_category: str = None) -> Dict[str, Any]:
        """Test the Symptom Category Analysis API"""
        
        test_name = f"Symptom Category Analysis - {symptom_description}"
        
        print(f"🧪 Testing Symptom Category Analysis API")
        print(f"Input: '{symptom_description}'")
        print(f"Expected Category: {expected_category or 'Any'}")
        
        # Prepare request payload
        payload = {
            "symptom_description": symptom_description
        }
        
        # Measure processing time
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.backend_url}/medical-ai/symptom-category-analysis",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = [
                    "identified_symptom", "category", "confidence", 
                    "related_symptoms", "category_description"
                ]
                
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    self.log_test_result(
                        test_name,
                        False,
                        f"Missing required fields: {missing_fields}",
                        processing_time,
                        data
                    )
                    return data
                
                # Validate category if expected
                actual_category = data.get('category', '').lower()
                if expected_category and expected_category.lower() not in actual_category:
                    self.log_test_result(
                        test_name,
                        False,
                        f"Category mismatch: expected '{expected_category}', got '{actual_category}'",
                        processing_time,
                        data
                    )
                    return data
                
                # Validate content quality
                identified_symptom = data.get('identified_symptom', '')
                confidence = data.get('confidence', 0)
                related_symptoms = data.get('related_symptoms', [])
                
                if not identified_symptom:
                    self.log_test_result(
                        test_name,
                        False,
                        "No symptom identified",
                        processing_time,
                        data
                    )
                    return data
                
                if confidence < 0.3:
                    self.log_test_result(
                        test_name,
                        False,
                        f"Very low confidence: {confidence} (expected >= 0.3)",
                        processing_time,
                        data
                    )
                    return data
                
                # Success
                details = f"Identified: {identified_symptom}, Category: {actual_category}, Confidence: {confidence:.3f}, Related: {len(related_symptoms)}"
                self.log_test_result(test_name, True, details, processing_time, data)
                return data
                
            else:
                self.log_test_result(
                    test_name,
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    processing_time
                )
                return {}
                
        except Exception as e:
            end_time = time.time()
            processing_time = end_time - start_time
            
            self.log_test_result(
                test_name,
                False,
                f"Exception: {str(e)}",
                processing_time
            )
            return {}

    def validate_chest_pain_template_structure(self, template_data: Dict[str, Any]) -> bool:
        """Validate that chest_pain template includes specific requirements from review"""
        
        print(f"🔍 Validating Chest Pain Template Structure")
        
        questions = template_data.get('questions', [])
        red_flags = template_data.get('red_flags', [])
        follow_up_protocol = template_data.get('follow_up_protocol', '')
        
        # Check for specific questions mentioned in review
        expected_question_keywords = [
            ['describe', 'chest', 'discomfort'],  # "Can you describe the chest discomfort?"
            ['sharp', 'dull', 'pressure'],        # "Is it sharp, dull, or pressure-like?"
            ['radiation', 'arm', 'jaw', 'neck', 'back']  # Questions about radiation
        ]
        
        questions_text = ' '.join(questions).lower()
        questions_found = 0
        
        for keywords in expected_question_keywords:
            if any(keyword in questions_text for keyword in keywords):
                questions_found += 1
        
        # Check for specific red flags mentioned in review
        expected_red_flag_keywords = [
            'crushing', 'radiating', 'shortness of breath'
        ]
        
        red_flags_text = ' '.join(red_flags).lower()
        red_flags_found = sum(1 for keyword in expected_red_flag_keywords if keyword in red_flags_text)
        
        # Check follow-up protocol
        protocol_correct = 'chest_pain_assessment' in follow_up_protocol.lower()
        
        validation_details = f"Questions found: {questions_found}/3, Red flags found: {red_flags_found}/3, Protocol correct: {protocol_correct}"
        
        # Consider validation successful if at least 2/3 criteria are met
        validation_success = (questions_found >= 2) and (red_flags_found >= 2) and protocol_correct
        
        self.log_test_result(
            "Chest Pain Template Structure Validation",
            validation_success,
            validation_details,
            0,
            template_data
        )
        
        return validation_success

    def test_review_request_scenarios(self):
        """Test the specific scenarios mentioned in the review request"""
        
        print(f"\n🎯 TESTING REVIEW REQUEST SCENARIOS")
        print("=" * 60)
        
        # Test scenarios from review request
        test_scenarios = [
            {
                "symptom": "chest pain",
                "expected_category": "cardiovascular",
                "description": "Should return cardiovascular category with appropriate questions"
            },
            {
                "symptom": "severe headache",
                "expected_category": "neurological",
                "description": "Should return neurological category"
            },
            {
                "symptom": "shortness of breath",
                "expected_category": "respiratory",
                "description": "Should return respiratory category"
            },
            {
                "symptom": "abdominal pain",
                "expected_category": "gastrointestinal",
                "description": "Should return gastrointestinal category"
            }
        ]
        
        chest_pain_template = None
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n{i}. SCENARIO: {scenario['description']}")
            print("-" * 50)
            
            # Test Enhanced Response Template API
            template_result = self.test_enhanced_response_template_api(
                scenario["symptom"],
                scenario["expected_category"],
                f"Review Scenario {i} - Enhanced Template"
            )
            
            # Store chest pain template for detailed validation
            if scenario["symptom"] == "chest pain" and template_result:
                chest_pain_template = template_result
            
            # Test Symptom Category Analysis API
            self.test_symptom_category_analysis_api(
                scenario["symptom"],
                scenario["expected_category"]
            )
        
        # Validate chest pain template structure if available
        if chest_pain_template:
            print(f"\n5. CHEST PAIN TEMPLATE STRUCTURE VALIDATION")
            print("-" * 50)
            self.validate_chest_pain_template_structure(chest_pain_template)

    def test_robustness_with_various_conditions(self):
        """Test robustness with various medical conditions dynamically"""
        
        print(f"\n🛡️ TESTING ROBUSTNESS WITH VARIOUS MEDICAL CONDITIONS")
        print("=" * 60)
        
        # Various medical conditions to test robustness
        robustness_test_cases = [
            "migraine with visual aura",
            "acute myocardial infarction symptoms",
            "asthma exacerbation",
            "appendicitis pain",
            "stroke symptoms with weakness",
            "pneumonia with fever",
            "kidney stones with flank pain",
            "anxiety attack with palpitations",
            "diabetic ketoacidosis symptoms",
            "allergic reaction with swelling",
            "back pain with sciatica",
            "urinary tract infection symptoms"
        ]
        
        for i, condition in enumerate(robustness_test_cases, 1):
            print(f"\n{i}. ROBUSTNESS TEST: {condition}")
            print("-" * 40)
            
            # Test both APIs for robustness
            self.test_enhanced_response_template_api(
                condition,
                None,  # No expected category for robustness testing
                f"Robustness Test {i} - Enhanced Template"
            )
            
            self.test_symptom_category_analysis_api(condition)

    def test_edge_cases_and_error_handling(self):
        """Test edge cases and error handling"""
        
        print(f"\n🔧 TESTING EDGE CASES AND ERROR HANDLING")
        print("=" * 60)
        
        edge_cases = [
            {
                "symptom": "",
                "test_name": "Empty Input",
                "should_fail": True
            },
            {
                "symptom": "xyz abc nonsense medical term",
                "test_name": "Non-medical Input",
                "should_fail": False  # Should handle gracefully
            },
            {
                "symptom": "chest pain " * 100,  # Very long input
                "test_name": "Very Long Input",
                "should_fail": False
            },
            {
                "symptom": "chest pain!!! @#$% with shortness of breath???",
                "test_name": "Special Characters",
                "should_fail": False
            }
        ]
        
        for i, case in enumerate(edge_cases, 1):
            print(f"\n{i}. EDGE CASE: {case['test_name']}")
            print("-" * 40)
            
            # Test Enhanced Response Template API
            try:
                start_time = time.time()
                response = requests.post(
                    f"{self.backend_url}/medical-ai/enhanced-response-template",
                    json={
                        "symptom_description": case["symptom"],
                        "patient_context": {}
                    },
                    headers={'Content-Type': 'application/json'},
                    timeout=15
                )
                processing_time = time.time() - start_time
                
                if case["should_fail"]:
                    if response.status_code != 200:
                        self.log_test_result(
                            f"Edge Case {i} - Enhanced Template",
                            True,
                            f"Correctly failed with HTTP {response.status_code}",
                            processing_time
                        )
                    else:
                        data = response.json()
                        if not data or data.get('confidence_score', 1) < 0.1:
                            self.log_test_result(
                                f"Edge Case {i} - Enhanced Template",
                                True,
                                "Correctly handled with low confidence",
                                processing_time
                            )
                        else:
                            self.log_test_result(
                                f"Edge Case {i} - Enhanced Template",
                                False,
                                "Expected failure but request succeeded",
                                processing_time
                            )
                else:
                    if response.status_code == 200:
                        self.log_test_result(
                            f"Edge Case {i} - Enhanced Template",
                            True,
                            "Handled gracefully",
                            processing_time
                        )
                    else:
                        self.log_test_result(
                            f"Edge Case {i} - Enhanced Template",
                            False,
                            f"Unexpected failure: HTTP {response.status_code}",
                            processing_time
                        )
                        
            except Exception as e:
                if case["should_fail"]:
                    self.log_test_result(
                        f"Edge Case {i} - Enhanced Template",
                        True,
                        f"Correctly failed with exception: {str(e)}",
                        0
                    )
                else:
                    self.log_test_result(
                        f"Edge Case {i} - Enhanced Template",
                        False,
                        f"Unexpected exception: {str(e)}",
                        0
                    )

    def run_comprehensive_tests(self):
        """Run all comprehensive tests for Phase 5 Enhanced Medical Response Generation"""
        
        print(f"🚀 PHASE 5: ENHANCED MEDICAL RESPONSE GENERATION COMPREHENSIVE TESTING")
        print("=" * 80)
        print(f"Testing Step 5.1 from Phase 5: Enhanced Medical Response Generation")
        print(f"Backend URL: {self.backend_url}")
        print(f"Test Start Time: {datetime.now().isoformat()}")
        print("=" * 80)
        print()
        
        # Run all test scenarios
        self.test_review_request_scenarios()
        self.test_robustness_with_various_conditions()
        self.test_edge_cases_and_error_handling()
        
        # Generate final report
        self.generate_final_report()

    def generate_final_report(self):
        """Generate comprehensive final test report"""
        
        print("=" * 80)
        print("🎯 PHASE 5: ENHANCED MEDICAL RESPONSE GENERATION - FINAL TEST REPORT")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed Tests: {self.passed_tests}")
        print(f"   Failed Tests: {self.total_tests - self.passed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        # Categorize results by test type
        categories = {
            "Review Request Scenarios": [],
            "Robustness Tests": [],
            "Edge Cases": [],
            "Template Structure Validation": []
        }
        
        for result in self.test_results:
            test_name = result["test_name"]
            if "Review Scenario" in test_name:
                categories["Review Request Scenarios"].append(result)
            elif "Robustness Test" in test_name:
                categories["Robustness Tests"].append(result)
            elif "Edge Case" in test_name:
                categories["Edge Cases"].append(result)
            elif "Template Structure" in test_name:
                categories["Template Structure Validation"].append(result)
            else:
                # Default to Review Request Scenarios for symptom category analysis
                categories["Review Request Scenarios"].append(result)
        
        # Report by category
        for category_name, results in categories.items():
            if results:
                passed = sum(1 for r in results if r["success"])
                total = len(results)
                rate = (passed / total) * 100 if total > 0 else 0
                
                print(f"📋 {category_name.upper()}: {passed}/{total} passed ({rate:.1f}%)")
                for result in results:
                    status = "✅" if result["success"] else "❌"
                    print(f"   {status} {result['test_name']}")
                print()
        
        # Critical success criteria assessment
        print("🎯 CRITICAL SUCCESS CRITERIA ASSESSMENT:")
        
        # Check if Enhanced Response Template API is functional
        template_api_tests = [r for r in self.test_results if "Enhanced Template" in r["test_name"] and "Edge Case" not in r["test_name"]]
        template_api_functional = len(template_api_tests) > 0 and any(r["success"] for r in template_api_tests)
        print(f"   ✅ Enhanced Response Template API Functional: {'YES' if template_api_functional else 'NO'}")
        
        # Check if Symptom Category Analysis API is functional
        category_api_tests = [r for r in self.test_results if "Symptom Category Analysis" in r["test_name"]]
        category_api_functional = len(category_api_tests) > 0 and any(r["success"] for r in category_api_tests)
        print(f"   ✅ Symptom Category Analysis API Functional: {'YES' if category_api_functional else 'NO'}")
        
        # Check if review request scenarios passed
        review_tests = [r for r in categories["Review Request Scenarios"] if r["success"]]
        review_scenarios_passed = len(review_tests) >= 6  # At least 6 out of 8 review scenarios (4 template + 4 category)
        print(f"   ✅ Review Request Scenarios Passed: {'YES' if review_scenarios_passed else 'NO'}")
        
        # Check if chest pain template structure is validated
        template_structure_tests = [r for r in categories["Template Structure Validation"] if r["success"]]
        template_structure_validated = len(template_structure_tests) > 0
        print(f"   ✅ Chest Pain Template Structure Validated: {'YES' if template_structure_validated else 'NO'}")
        
        # Check if robustness testing passed
        robustness_tests = [r for r in categories["Robustness Tests"] if r["success"]]
        robustness_passed = len(robustness_tests) >= 8  # At least 8 out of 12 robustness tests
        print(f"   ✅ Robustness Testing Passed: {'YES' if robustness_passed else 'NO'}")
        
        # Check if error handling works
        edge_case_tests = [r for r in categories["Edge Cases"] if r["success"]]
        error_handling_works = len(edge_case_tests) >= 3  # At least 3 out of 4 edge cases
        print(f"   ✅ Error Handling Works: {'YES' if error_handling_works else 'NO'}")
        
        print()
        
        # Performance analysis
        response_times = [r["response_time_ms"] for r in self.test_results if r["response_time_ms"] > 0]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            print(f"⏱️  PERFORMANCE ANALYSIS:")
            print(f"   Average Response Time: {avg_response_time:.2f}ms")
            print(f"   Maximum Response Time: {max_response_time:.2f}ms")
            print(f"   Performance Target (<5000ms): {'✅ MET' if max_response_time < 5000 else '❌ EXCEEDED'}")
            print()
        
        # Final assessment
        critical_criteria_met = sum([
            template_api_functional,
            category_api_functional,
            review_scenarios_passed,
            template_structure_validated,
            robustness_passed,
            error_handling_works
        ])
        
        if success_rate >= 80 and critical_criteria_met >= 5:
            print("🎉 ASSESSMENT: PHASE 5 ENHANCED MEDICAL RESPONSE GENERATION SYSTEM IS PRODUCTION-READY!")
            print("   The system demonstrates excellent symptom-specific response template generation")
            print("   with comprehensive medical categorization and clinical reasoning capabilities.")
        elif success_rate >= 60 and critical_criteria_met >= 4:
            print("⚠️  ASSESSMENT: PHASE 5 SYSTEM IS FUNCTIONAL BUT NEEDS IMPROVEMENTS")
            print("   Core functionality is working but some components need attention.")
        else:
            print("❌ ASSESSMENT: PHASE 5 SYSTEM NEEDS SIGNIFICANT WORK")
            print("   Multiple critical issues detected that prevent production deployment.")
        
        print()
        print(f"Test Completion Time: {datetime.now().isoformat()}")
        print("=" * 80)
        
        return {
            'total_tests': self.total_tests,
            'passed_tests': self.passed_tests,
            'success_rate': success_rate,
            'critical_criteria_met': critical_criteria_met,
            'template_api_functional': template_api_functional,
            'category_api_functional': category_api_functional,
            'production_ready': success_rate >= 80 and critical_criteria_met >= 5
        }

def main():
    """Main test execution function"""
    tester = Phase5EnhancedResponseTester()
    results = tester.run_comprehensive_tests()
    
    print(f"\n🎉 PHASE 5 ENHANCED MEDICAL RESPONSE GENERATION TESTING COMPLETE!")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    main()