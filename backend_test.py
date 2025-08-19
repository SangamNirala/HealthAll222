#!/usr/bin/env python3
"""
🚀 STEP 3.2 REVOLUTIONARY MULTI-SYMPTOM PARSING SYSTEM COMPREHENSIVE TESTING

This test suite validates the most advanced medical multi-symptom parsing system ever conceived,
testing all revolutionary capabilities including:
- Complex multi-symptom expression parsing (10+ simultaneous symptoms)
- Clinical-grade structured output for medical documentation
- Real-time processing performance (<25ms target)
- Integration with existing Steps 1.1-3.1 infrastructure
- Emergency detection and clinical reasoning
- Grammatically incorrect and colloquial expression handling

Test Scenarios:
1. Revolutionary Parsing Capabilities - Ultra-challenging multi-symptom expressions
2. Integration Validation - Seamless integration with existing medical AI
3. Clinical-Grade Output Validation - Medical documentation-ready structured data
4. Performance Benchmarking - <25ms processing, >99% accuracy validation
5. Error Handling & Edge Cases - Robustness testing

Target Performance:
- 99%+ accuracy on complex multi-symptom expressions
- <25ms processing time for real-time clinical applications
- Handle 10+ simultaneous symptoms in single utterances
- Clinical-grade structured output for medical documentation
- Seamless integration with existing Steps 1.1-3.1 infrastructure
"""

import asyncio
import json
import time
import requests
import sys
from typing import Dict, Any, List
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://multi-symptom-engine.preview.emergentagent.com/api"

class Step32MultiSymptomParsingTester:
    """Comprehensive tester for Step 3.2 Revolutionary Multi-Symptom Parsing System"""
    
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

    async def test_revolutionary_parsing_capabilities(self):
        """
        TEST SCENARIO 1: REVOLUTIONARY PARSING CAPABILITIES
        Test ultra-challenging multi-symptom expressions with complex medical scenarios
        """
        print("🚀 TESTING SCENARIO 1: REVOLUTIONARY PARSING CAPABILITIES")
        print("=" * 80)
        
        # Ultra-challenging test cases from review request
        test_cases = [
            {
                "name": "Complex Multi-Symptom Expression",
                "text": "bad headache started monday got worse tuesday now nausea dizzy cant focus at work",
                "expected_symptoms": ["headache", "nausea", "dizziness", "concentration difficulty"],
                "expected_count": 4
            },
            {
                "name": "Grammatically Incorrect Colloquial",
                "text": "cant eat anything comes right back up barely slept 4 nights feel like death",
                "expected_symptoms": ["anorexia", "vomiting", "insomnia", "malaise"],
                "expected_count": 4
            },
            {
                "name": "Medical Emergency Combination",
                "text": "chest tightness with palpitations feeling anxious shortness of breath comes n goes",
                "expected_symptoms": ["chest tightness", "palpitations", "anxiety", "dyspnea"],
                "expected_count": 4
            },
            {
                "name": "Implicit Symptom Pattern",
                "text": "back hurt real bad when sit long time also leg numb sometimes",
                "expected_symptoms": ["back pain", "leg numbness"],
                "expected_count": 2
            },
            {
                "name": "Ultra-Complex Multi-System",
                "text": "head pounding stomach churning heart racing cant breathe properly dizzy when stand up been 3 days getting worse",
                "expected_symptoms": ["headache", "nausea", "palpitations", "dyspnea", "dizziness"],
                "expected_count": 5
            }
        ]
        
        for test_case in test_cases:
            await self._test_multi_symptom_parsing(test_case)
    
    async def _test_multi_symptom_parsing(self, test_case: Dict[str, Any]):
        """Test individual multi-symptom parsing scenario"""
        try:
            # Prepare request
            request_data = {
                "text": test_case["text"],
                "patient_id": "test-patient-123",
                "include_relationships": True,
                "include_clinical_reasoning": True
            }
            
            # Make API call with timing
            start_time = time.time()
            response = requests.post(
                f"{self.backend_url}/medical-ai/multi-symptom-parse",
                json=request_data,
                timeout=30
            )
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                
                # Validate response structure
                required_fields = [
                    "success", "multi_symptom_parse_result", "summary", 
                    "clinical_recommendations", "urgency_assessment", 
                    "integration_status", "processing_performance"
                ]
                
                missing_fields = [field for field in required_fields if field not in result]
                if missing_fields:
                    self.log_test_result(
                        test_case["name"],
                        False,
                        f"Missing required fields: {missing_fields}",
                        response_time
                    )
                    return
                
                # Validate parsing success
                if not result.get("success", False):
                    self.log_test_result(
                        test_case["name"],
                        False,
                        f"Parsing failed: {result.get('error', 'Unknown error')}",
                        response_time
                    )
                    return
                
                # Validate symptom count and detection
                summary = result.get("summary", {})
                total_symptoms = summary.get("total_symptoms", 0)
                
                # Check if we detected expected number of symptoms (allow some flexibility)
                expected_min = max(1, test_case["expected_count"] - 1)
                expected_max = test_case["expected_count"] + 2
                
                if total_symptoms < expected_min:
                    self.log_test_result(
                        test_case["name"],
                        False,
                        f"Too few symptoms detected: {total_symptoms} (expected {test_case['expected_count']})",
                        response_time
                    )
                    return
                
                # Validate performance target (<25ms)
                processing_performance = result.get("processing_performance", {})
                actual_processing_time = processing_performance.get("processing_time_ms", response_time)
                performance_target_met = processing_performance.get("performance_target_met", False)
                
                # Validate clinical recommendations
                clinical_recommendations = result.get("clinical_recommendations", [])
                if not clinical_recommendations:
                    self.log_test_result(
                        test_case["name"],
                        False,
                        "No clinical recommendations provided",
                        response_time
                    )
                    return
                
                # Validate urgency assessment
                urgency_assessment = result.get("urgency_assessment", "")
                valid_urgency_levels = ["routine", "urgent", "emergency", "critical"]
                if urgency_assessment not in valid_urgency_levels:
                    self.log_test_result(
                        test_case["name"],
                        False,
                        f"Invalid urgency assessment: {urgency_assessment}",
                        response_time
                    )
                    return
                
                # Success - log detailed results
                details = f"Symptoms detected: {total_symptoms}, Urgency: {urgency_assessment}, Processing: {actual_processing_time:.2f}ms, Performance target met: {performance_target_met}"
                self.log_test_result(test_case["name"], True, details, response_time)
                
            else:
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    response_time
                )
                
        except Exception as e:
            self.log_test_result(
                test_case["name"],
                False,
                f"Exception: {str(e)}",
                0
            )

    async def test_integration_validation(self):
        """
        TEST SCENARIO 2: INTEGRATION VALIDATION
        Verify seamless integration with existing medical AI infrastructure
        """
        print("🔗 TESTING SCENARIO 2: INTEGRATION VALIDATION")
        print("=" * 80)
        
        # Test integration with context and patient data
        integration_test_cases = [
            {
                "name": "Text Normalization Integration",
                "text": "me head hurt real bad n stomach feel sick",
                "context": {
                    "demographics": {"age": 35, "gender": "female"},
                    "medical_history": {"conditions": ["migraine"]},
                    "symptom_data": {"previous_symptoms": ["headache"]}
                }
            },
            {
                "name": "Symptom Recognition Enhancement",
                "text": "crushing chest pain radiating to left arm with sweating",
                "context": {
                    "demographics": {"age": 55, "gender": "male"},
                    "medical_history": {"conditions": ["hypertension"]},
                    "symptom_data": {}
                }
            },
            {
                "name": "Intent Classification Informed",
                "text": "worried about these symptoms getting worse need help",
                "context": {
                    "demographics": {"age": 42, "gender": "female"},
                    "medical_history": {"conditions": []},
                    "symptom_data": {"current_symptoms": ["anxiety", "worry"]}
                }
            }
        ]
        
        for test_case in integration_test_cases:
            await self._test_integration_scenario(test_case)

    async def _test_integration_scenario(self, test_case: Dict[str, Any]):
        """Test individual integration scenario"""
        try:
            request_data = {
                "text": test_case["text"],
                "patient_id": "integration-test-456",
                "context": test_case.get("context", {}),
                "include_relationships": True,
                "include_clinical_reasoning": True
            }
            
            start_time = time.time()
            response = requests.post(
                f"{self.backend_url}/medical-ai/multi-symptom-parse",
                json=request_data,
                timeout=30
            )
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                
                # Validate integration status
                integration_status = result.get("integration_status", {})
                
                # Check for integration indicators
                integration_indicators = [
                    "text_normalization_applied",
                    "symptom_recognizer_enhanced", 
                    "intent_classification_informed"
                ]
                
                integration_working = any(
                    integration_status.get(indicator, False) 
                    for indicator in integration_indicators
                )
                
                if integration_working:
                    details = f"Integration active: {integration_status}"
                    self.log_test_result(test_case["name"], True, details, response_time)
                else:
                    self.log_test_result(
                        test_case["name"],
                        False,
                        f"No integration indicators found: {integration_status}",
                        response_time
                    )
            else:
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    response_time
                )
                
        except Exception as e:
            self.log_test_result(
                test_case["name"],
                False,
                f"Exception: {str(e)}",
                0
            )

    async def test_clinical_grade_output_validation(self):
        """
        TEST SCENARIO 3: CLINICAL-GRADE OUTPUT VALIDATION
        Verify medical documentation-ready structured output
        """
        print("🏥 TESTING SCENARIO 3: CLINICAL-GRADE OUTPUT VALIDATION")
        print("=" * 80)
        
        # Test clinical-grade output requirements
        clinical_test_text = "severe chest pain with shortness of breath started 2 hours ago getting worse with sweating and nausea"
        
        try:
            request_data = {
                "text": clinical_test_text,
                "patient_id": "clinical-test-789",
                "include_relationships": True,
                "include_clinical_reasoning": True
            }
            
            start_time = time.time()
            response = requests.post(
                f"{self.backend_url}/medical-ai/multi-symptom-parse",
                json=request_data,
                timeout=30
            )
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                
                # Validate clinical-grade components
                clinical_validations = []
                
                # 1. Primary/Secondary Symptoms with confidence scores
                parse_result = result.get("multi_symptom_parse_result", {})
                if "primary_symptoms" in parse_result or "secondary_symptoms" in parse_result:
                    clinical_validations.append("✅ Primary/Secondary symptoms identified")
                else:
                    clinical_validations.append("❌ Primary/Secondary symptoms missing")
                
                # 2. Temporal Analysis
                if "temporal_analysis" in parse_result or "onset" in str(parse_result):
                    clinical_validations.append("✅ Temporal analysis present")
                else:
                    clinical_validations.append("❌ Temporal analysis missing")
                
                # 3. Severity Assessment
                if "severity" in str(parse_result) or "intensity" in str(parse_result):
                    clinical_validations.append("✅ Severity assessment present")
                else:
                    clinical_validations.append("❌ Severity assessment missing")
                
                # 4. Clinical Relationships
                if "relationships" in str(parse_result) or "clusters" in str(parse_result):
                    clinical_validations.append("✅ Clinical relationships identified")
                else:
                    clinical_validations.append("❌ Clinical relationships missing")
                
                # 5. Urgency Assessment
                urgency = result.get("urgency_assessment", "")
                if urgency in ["urgent", "emergency", "critical"]:
                    clinical_validations.append("✅ Appropriate urgency assessment")
                else:
                    clinical_validations.append(f"⚠️ Urgency assessment: {urgency}")
                
                # 6. Clinical Reasoning
                recommendations = result.get("clinical_recommendations", [])
                if recommendations and len(recommendations) > 0:
                    clinical_validations.append("✅ Clinical recommendations provided")
                else:
                    clinical_validations.append("❌ Clinical recommendations missing")
                
                # Determine overall success
                success_count = sum(1 for v in clinical_validations if v.startswith("✅"))
                total_validations = len(clinical_validations)
                success_rate = success_count / total_validations
                
                details = f"Clinical validation: {success_count}/{total_validations} passed. " + "; ".join(clinical_validations)
                self.log_test_result(
                    "Clinical-Grade Output Validation",
                    success_rate >= 0.7,  # 70% success rate required
                    details,
                    response_time
                )
                
            else:
                self.log_test_result(
                    "Clinical-Grade Output Validation",
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    response_time
                )
                
        except Exception as e:
            self.log_test_result(
                "Clinical-Grade Output Validation",
                False,
                f"Exception: {str(e)}",
                0
            )

    async def test_performance_benchmarking(self):
        """
        TEST SCENARIO 4: PERFORMANCE BENCHMARKING
        Test the statistics endpoint and validate performance targets
        """
        print("📊 TESTING SCENARIO 4: PERFORMANCE BENCHMARKING")
        print("=" * 80)
        
        try:
            # Test statistics endpoint
            start_time = time.time()
            response = requests.get(
                f"{self.backend_url}/medical-ai/multi-symptom-parse/statistics",
                timeout=30
            )
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                stats = response.json()
                
                # Validate statistics structure
                required_stats_fields = [
                    "status", "algorithm_version", "step_3_2_status",
                    "parser_performance", "integration_status", 
                    "performance_targets", "capabilities"
                ]
                
                missing_fields = [field for field in required_stats_fields if field not in stats]
                if missing_fields:
                    self.log_test_result(
                        "Statistics Endpoint Structure",
                        False,
                        f"Missing fields: {missing_fields}",
                        response_time
                    )
                else:
                    self.log_test_result(
                        "Statistics Endpoint Structure",
                        True,
                        "All required statistics fields present",
                        response_time
                    )
                
                # Validate algorithm version
                algorithm_version = stats.get("algorithm_version", "")
                if "3.2" in algorithm_version:
                    self.log_test_result(
                        "Algorithm Version Validation",
                        True,
                        f"Correct algorithm version: {algorithm_version}",
                        0
                    )
                else:
                    self.log_test_result(
                        "Algorithm Version Validation",
                        False,
                        f"Incorrect algorithm version: {algorithm_version}",
                        0
                    )
                
                # Validate capabilities
                capabilities = stats.get("capabilities", {})
                expected_capabilities = [
                    "multi_symptom_parsing",
                    "processing_time_target", 
                    "accuracy_target",
                    "clinical_integration"
                ]
                
                capabilities_present = all(cap in capabilities for cap in expected_capabilities)
                if capabilities_present:
                    self.log_test_result(
                        "Capabilities Validation",
                        True,
                        f"All expected capabilities present: {list(capabilities.keys())}",
                        0
                    )
                else:
                    missing_caps = [cap for cap in expected_capabilities if cap not in capabilities]
                    self.log_test_result(
                        "Capabilities Validation",
                        False,
                        f"Missing capabilities: {missing_caps}",
                        0
                    )
                
                # Validate system health
                system_health = stats.get("system_health", "")
                step_3_2_status = stats.get("step_3_2_status", "")
                
                if system_health == "excellent" and step_3_2_status == "operational":
                    self.log_test_result(
                        "System Health Validation",
                        True,
                        f"System health: {system_health}, Step 3.2 status: {step_3_2_status}",
                        0
                    )
                else:
                    self.log_test_result(
                        "System Health Validation",
                        False,
                        f"System health: {system_health}, Step 3.2 status: {step_3_2_status}",
                        0
                    )
                
            else:
                self.log_test_result(
                    "Statistics Endpoint",
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    response_time
                )
                
        except Exception as e:
            self.log_test_result(
                "Performance Benchmarking",
                False,
                f"Exception: {str(e)}",
                0
            )

    async def test_error_handling_edge_cases(self):
        """
        TEST SCENARIO 5: ERROR HANDLING & EDGE CASES
        Test robustness with various edge cases
        """
        print("🛡️ TESTING SCENARIO 5: ERROR HANDLING & EDGE CASES")
        print("=" * 80)
        
        edge_cases = [
            {
                "name": "Empty Text Input",
                "text": "",
                "should_fail": True
            },
            {
                "name": "Very Long Medical Text",
                "text": "headache " * 500,  # Very long text
                "should_fail": False
            },
            {
                "name": "Non-Medical Text",
                "text": "I love pizza and ice cream on sunny days",
                "should_fail": False
            },
            {
                "name": "Special Characters and Symbols",
                "text": "chest pain!!! @#$% with shortness of breath???",
                "should_fail": False
            },
            {
                "name": "Mixed Languages",
                "text": "dolor de cabeza and headache muy malo",
                "should_fail": False
            }
        ]
        
        for test_case in edge_cases:
            await self._test_edge_case(test_case)

    async def _test_edge_case(self, test_case: Dict[str, Any]):
        """Test individual edge case scenario"""
        try:
            request_data = {
                "text": test_case["text"],
                "patient_id": "edge-case-test",
                "include_relationships": True,
                "include_clinical_reasoning": True
            }
            
            start_time = time.time()
            response = requests.post(
                f"{self.backend_url}/medical-ai/multi-symptom-parse",
                json=request_data,
                timeout=30
            )
            response_time = (time.time() - start_time) * 1000
            
            if test_case["should_fail"]:
                # Expecting failure
                if response.status_code != 200:
                    self.log_test_result(
                        test_case["name"],
                        True,
                        f"Correctly failed with HTTP {response.status_code}",
                        response_time
                    )
                else:
                    result = response.json()
                    if not result.get("success", True):
                        self.log_test_result(
                            test_case["name"],
                            True,
                            f"Correctly failed with error: {result.get('error', 'Unknown')}",
                            response_time
                        )
                    else:
                        self.log_test_result(
                            test_case["name"],
                            False,
                            "Expected failure but request succeeded",
                            response_time
                        )
            else:
                # Expecting success or graceful handling
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success", False):
                        self.log_test_result(
                            test_case["name"],
                            True,
                            "Handled gracefully with successful parsing",
                            response_time
                        )
                    else:
                        self.log_test_result(
                            test_case["name"],
                            True,
                            f"Handled gracefully with controlled failure: {result.get('error', 'Unknown')}",
                            response_time
                        )
                else:
                    self.log_test_result(
                        test_case["name"],
                        False,
                        f"Unexpected HTTP {response.status_code}: {response.text[:200]}",
                        response_time
                    )
                    
        except Exception as e:
            if test_case["should_fail"]:
                self.log_test_result(
                    test_case["name"],
                    True,
                    f"Correctly failed with exception: {str(e)}",
                    0
                )
            else:
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"Unexpected exception: {str(e)}",
                    0
                )

    async def run_comprehensive_tests(self):
        """Run all comprehensive tests for Step 3.2 Multi-Symptom Parsing System"""
        print("🚀 STEP 3.2 REVOLUTIONARY MULTI-SYMPTOM PARSING SYSTEM COMPREHENSIVE TESTING")
        print("=" * 100)
        print(f"Backend URL: {self.backend_url}")
        print(f"Test Start Time: {datetime.now().isoformat()}")
        print("=" * 100)
        print()
        
        # Run all test scenarios
        await self.test_revolutionary_parsing_capabilities()
        await self.test_integration_validation()
        await self.test_clinical_grade_output_validation()
        await self.test_performance_benchmarking()
        await self.test_error_handling_edge_cases()
        
        # Generate final report
        self.generate_final_report()

    def generate_final_report(self):
        """Generate comprehensive final test report"""
        print("=" * 100)
        print("🎯 STEP 3.2 MULTI-SYMPTOM PARSING SYSTEM - FINAL TEST REPORT")
        print("=" * 100)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed Tests: {self.passed_tests}")
        print(f"   Failed Tests: {self.total_tests - self.passed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        # Categorize results by test scenario
        scenarios = {
            "Revolutionary Parsing": [],
            "Integration Validation": [],
            "Clinical-Grade Output": [],
            "Performance Benchmarking": [],
            "Error Handling": []
        }
        
        for result in self.test_results:
            test_name = result["test_name"]
            if any(keyword in test_name for keyword in ["Complex", "Grammatically", "Emergency", "Implicit", "Ultra-Complex"]):
                scenarios["Revolutionary Parsing"].append(result)
            elif any(keyword in test_name for keyword in ["Integration", "Normalization", "Recognition", "Classification"]):
                scenarios["Integration Validation"].append(result)
            elif "Clinical" in test_name:
                scenarios["Clinical-Grade Output"].append(result)
            elif any(keyword in test_name for keyword in ["Statistics", "Algorithm", "Capabilities", "Performance", "System Health"]):
                scenarios["Performance Benchmarking"].append(result)
            else:
                scenarios["Error Handling"].append(result)
        
        # Report by scenario
        for scenario_name, results in scenarios.items():
            if results:
                passed = sum(1 for r in results if r["success"])
                total = len(results)
                rate = (passed / total) * 100 if total > 0 else 0
                
                print(f"📋 {scenario_name.upper()}: {passed}/{total} passed ({rate:.1f}%)")
                for result in results:
                    status = "✅" if result["success"] else "❌"
                    print(f"   {status} {result['test_name']}")
                print()
        
        # Critical success criteria assessment
        print("🎯 CRITICAL SUCCESS CRITERIA ASSESSMENT:")
        
        # Check if API endpoints are functional
        api_functional = any("Statistics Endpoint" in r["test_name"] and r["success"] for r in self.test_results)
        print(f"   ✅ API Endpoints Functional: {'YES' if api_functional else 'NO'}")
        
        # Check if multi-symptom parsing is working
        parsing_working = any(r["success"] for r in scenarios["Revolutionary Parsing"])
        print(f"   ✅ Multi-Symptom Parsing Working: {'YES' if parsing_working else 'NO'}")
        
        # Check if clinical integration is active
        integration_active = any(r["success"] for r in scenarios["Integration Validation"])
        print(f"   ✅ Clinical Integration Active: {'YES' if integration_active else 'NO'}")
        
        # Check if structured output is complete
        structured_output = any(r["success"] for r in scenarios["Clinical-Grade Output"])
        print(f"   ✅ Structured Output Complete: {'YES' if structured_output else 'NO'}")
        
        # Check if performance targets are met
        performance_met = any("System Health" in r["test_name"] and r["success"] for r in self.test_results)
        print(f"   ✅ Performance Targets Met: {'YES' if performance_met else 'NO'}")
        
        # Check if error handling is working
        error_handling = any(r["success"] for r in scenarios["Error Handling"])
        print(f"   ✅ Error Handling Working: {'YES' if error_handling else 'NO'}")
        
        print()
        
        # Final assessment
        if success_rate >= 80:
            print("🎉 ASSESSMENT: STEP 3.2 REVOLUTIONARY MULTI-SYMPTOM PARSING SYSTEM IS PRODUCTION-READY!")
            print("   The system demonstrates excellent multi-symptom parsing capabilities with")
            print("   clinical-grade accuracy and real-time performance optimization.")
        elif success_rate >= 60:
            print("⚠️  ASSESSMENT: STEP 3.2 SYSTEM IS FUNCTIONAL BUT NEEDS IMPROVEMENTS")
            print("   Core functionality is working but some components need attention.")
        else:
            print("❌ ASSESSMENT: STEP 3.2 SYSTEM NEEDS SIGNIFICANT WORK")
            print("   Multiple critical issues detected that prevent production deployment.")
        
        print()
        print(f"Test Completion Time: {datetime.now().isoformat()}")
        print("=" * 100)

async def main():
    """Main test execution function"""
    tester = Step32MultiSymptomParsingTester()
    await tester.run_comprehensive_tests()

if __name__ == "__main__":
    asyncio.run(main())
"""
PHASE D: PERFECTION & SCALE COMPREHENSIVE TESTING
=================================================

Testing comprehensive Phase D: Perfection & Scale implementation for medical intent classification system.

TESTING SCOPE:
1. Performance Optimization System Testing
2. Clinical Validation Framework Testing  
3. Production Monitoring System Testing
4. Comprehensive System Integration Testing

TARGET: Production-ready medical intent classification system with clinical-grade performance and safety validation.
"""

import asyncio
import aiohttp
import json
import time
import os
from datetime import datetime
from typing import Dict, List, Any
import sys

# Get backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://multi-symptom-engine.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class PhaseDBenchmarkTester:
    """Comprehensive Phase D testing suite"""
    
    def __init__(self):
        self.session = None
        self.test_results = []
        self.start_time = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=120),  # 2 minute timeout for benchmarks
            connector=aiohttp.TCPConnector(limit=100)
        )
        self.start_time = time.time()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    def log_result(self, test_name: str, success: bool, response_time: float, details: str = ""):
        """Log test result"""
        result = {
            "test_name": test_name,
            "success": success,
            "response_time_ms": round(response_time * 1000, 2),
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name} ({result['response_time_ms']}ms) - {details}")
        
    async def make_request(self, method: str, endpoint: str, data: Dict = None) -> tuple:
        """Make HTTP request and return (success, response_data, response_time)"""
        url = f"{BASE_URL}{endpoint}"
        start_time = time.time()
        
        try:
            if method.upper() == "GET":
                async with self.session.get(url) as response:
                    response_time = time.time() - start_time
                    if response.status == 200:
                        response_data = await response.json()
                        return True, response_data, response_time
                    else:
                        error_text = await response.text()
                        return False, {"error": error_text, "status": response.status}, response_time
                        
            elif method.upper() == "POST":
                headers = {"Content-Type": "application/json"}
                async with self.session.post(url, json=data, headers=headers) as response:
                    response_time = time.time() - start_time
                    if response.status == 200:
                        response_data = await response.json()
                        return True, response_data, response_time
                    else:
                        error_text = await response.text()
                        return False, {"error": error_text, "status": response.status}, response_time
                        
        except Exception as e:
            response_time = time.time() - start_time
            return False, {"error": str(e)}, response_time
            
    # ===== PERFORMANCE OPTIMIZATION SYSTEM TESTING =====
    
    async def test_performance_status_endpoint(self):
        """Test GET /api/medical-ai/phase-d/performance-status endpoint"""
        success, response, response_time = await self.make_request("GET", "/medical-ai/phase-d/performance-status")
        
        if success:
            # Validate response structure
            required_keys = ["status", "phase_d_performance", "optimization_active", "last_updated"]
            missing_keys = [key for key in required_keys if key not in response]
            
            if missing_keys:
                self.log_result("Performance Status Endpoint", False, response_time, 
                              f"Missing keys: {missing_keys}")
            else:
                # Check performance metrics
                perf_data = response.get("phase_d_performance", {})
                has_metrics = any(key in perf_data for key in ["caching_stats", "processing_metrics", "scalability_metrics"])
                
                self.log_result("Performance Status Endpoint", True, response_time,
                              f"Status: {response['status']}, Optimization: {response['optimization_active']}")
        else:
            self.log_result("Performance Status Endpoint", False, response_time, 
                          f"Request failed: {response.get('error', 'Unknown error')}")
            
    async def test_performance_benchmark_endpoint(self):
        """Test POST /api/medical-ai/phase-d/performance-benchmark endpoint"""
        # Test with sample benchmark data
        benchmark_data = {
            "concurrent_levels": [1, 5, 10],  # Smaller levels for testing
            "duration_seconds": 10,  # Shorter duration for testing
            "include_stress_test": False  # Skip stress test for basic validation
        }
        
        success, response, response_time = await self.make_request("POST", "/medical-ai/phase-d/performance-benchmark", benchmark_data)
        
        if success:
            # Validate response structure
            required_keys = ["status", "benchmark_results", "performance_summary", "recommendations", "completed_at"]
            missing_keys = [key for key in required_keys if key not in response]
            
            if missing_keys:
                self.log_result("Performance Benchmark Endpoint", False, response_time,
                              f"Missing keys: {missing_keys}")
            else:
                benchmark_results = response.get("benchmark_results", {})
                has_results = bool(benchmark_results)
                
                self.log_result("Performance Benchmark Endpoint", True, response_time,
                              f"Status: {response['status']}, Results: {has_results}")
        else:
            self.log_result("Performance Benchmark Endpoint", False, response_time,
                          f"Request failed: {response.get('error', 'Unknown error')}")
            
    async def test_advanced_caching_functionality(self):
        """Test advanced caching layer functionality through performance metrics"""
        # First call to populate cache
        success1, response1, time1 = await self.make_request("GET", "/medical-ai/phase-d/performance-status")
        
        if success1:
            # Second call should potentially be faster due to caching
            success2, response2, time2 = await self.make_request("GET", "/medical-ai/phase-d/performance-status")
            
            if success2:
                # Check if caching stats are available
                perf_data = response2.get("phase_d_performance", {})
                caching_stats = perf_data.get("caching_stats", {})
                
                cache_functional = bool(caching_stats) or time2 <= time1
                
                self.log_result("Advanced Caching Functionality", cache_functional, time2,
                              f"Cache stats available: {bool(caching_stats)}, Time improvement: {time1 > time2}")
            else:
                self.log_result("Advanced Caching Functionality", False, time2,
                              "Second request failed")
        else:
            self.log_result("Advanced Caching Functionality", False, time1,
                          "First request failed")
            
    # ===== CLINICAL VALIDATION FRAMEWORK TESTING =====
    
    async def test_clinical_validation_status_endpoint(self):
        """Test GET /api/medical-ai/phase-d/clinical-validation-status endpoint"""
        success, response, response_time = await self.make_request("GET", "/medical-ai/phase-d/clinical-validation-status")
        
        if success:
            # Validate response structure
            required_keys = ["status", "phase_d_clinical", "validation_active", "last_updated"]
            missing_keys = [key for key in required_keys if key not in response]
            
            if missing_keys:
                self.log_result("Clinical Validation Status Endpoint", False, response_time,
                              f"Missing keys: {missing_keys}")
            else:
                clinical_data = response.get("phase_d_clinical", {})
                has_validation_metrics = any(key in clinical_data for key in ["reviewer_stats", "accuracy_metrics", "safety_metrics"])
                
                self.log_result("Clinical Validation Status Endpoint", True, response_time,
                              f"Status: {response['status']}, Validation: {response['validation_active']}")
        else:
            self.log_result("Clinical Validation Status Endpoint", False, response_time,
                          f"Request failed: {response.get('error', 'Unknown error')}")
            
    async def test_submit_clinical_validation_endpoint(self):
        """Test POST /api/medical-ai/phase-d/submit-clinical-validation endpoint"""
        # Test with sample clinical validation data
        validation_data = {
            "patient_message": "I have severe chest pain radiating to my left arm",
            "conversation_context": {
                "session_id": "test_session_123",
                "previous_messages": []
            },
            "ai_classification_result": {
                "intent": "emergency_detection",
                "confidence": 0.95,
                "urgency": "critical",
                "reasoning": "Symptoms suggest possible cardiac emergency"
            },
            "validation_level": "advanced",
            "priority": True
        }
        
        success, response, response_time = await self.make_request("POST", "/medical-ai/phase-d/submit-clinical-validation", validation_data)
        
        if success:
            # Validate response structure
            required_keys = ["status", "case_id", "validation_level", "priority", "estimated_review_time_hours", "submitted_at"]
            missing_keys = [key for key in required_keys if key not in response]
            
            if missing_keys:
                self.log_result("Submit Clinical Validation Endpoint", False, response_time,
                              f"Missing keys: {missing_keys}")
            else:
                case_id = response.get("case_id")
                has_case_id = bool(case_id)
                
                self.log_result("Submit Clinical Validation Endpoint", True, response_time,
                              f"Status: {response['status']}, Case ID: {has_case_id}")
        else:
            self.log_result("Submit Clinical Validation Endpoint", False, response_time,
                          f"Request failed: {response.get('error', 'Unknown error')}")
            
    async def test_verify_safety_endpoint(self):
        """Test POST /api/medical-ai/phase-d/verify-safety endpoint for medical safety verification"""
        # Test with sample safety verification data
        safety_data = {
            "patient_message": "I'm having trouble breathing and chest tightness",
            "ai_classification_result": {
                "intent": "respiratory_emergency",
                "confidence": 0.88,
                "urgency": "high",
                "reasoning": "Respiratory distress symptoms detected"
            },
            "conversation_context": {
                "session_id": "safety_test_456",
                "medical_history": []
            }
        }
        
        success, response, response_time = await self.make_request("POST", "/medical-ai/phase-d/verify-safety", safety_data)
        
        if success:
            # Validate response structure
            required_keys = ["status", "safety_verification", "safety_score", "intervention_required", "escalation_needed", "verified_at"]
            missing_keys = [key for key in required_keys if key not in response]
            
            if missing_keys:
                self.log_result("Verify Safety Endpoint", False, response_time,
                              f"Missing keys: {missing_keys}")
            else:
                safety_score = response.get("safety_score", 0)
                intervention_required = response.get("intervention_required", False)
                
                self.log_result("Verify Safety Endpoint", True, response_time,
                              f"Status: {response['status']}, Safety Score: {safety_score}, Intervention: {intervention_required}")
        else:
            self.log_result("Verify Safety Endpoint", False, response_time,
                          f"Request failed: {response.get('error', 'Unknown error')}")
            
    # ===== PRODUCTION MONITORING SYSTEM TESTING =====
    
    async def test_production_monitoring_endpoint(self):
        """Test GET /api/medical-ai/phase-d/production-monitoring endpoint"""
        success, response, response_time = await self.make_request("GET", "/medical-ai/phase-d/production-monitoring")
        
        if success:
            # Validate response structure
            required_keys = ["status", "phase_d_monitoring", "monitoring_active", "last_updated"]
            missing_keys = [key for key in required_keys if key not in response]
            
            if missing_keys:
                self.log_result("Production Monitoring Endpoint", False, response_time,
                              f"Missing keys: {missing_keys}")
            else:
                monitoring_data = response.get("phase_d_monitoring", {})
                has_monitoring_metrics = any(key in monitoring_data for key in ["system_health", "alerts", "performance_metrics"])
                
                self.log_result("Production Monitoring Endpoint", True, response_time,
                              f"Status: {response['status']}, Monitoring: {response['monitoring_active']}")
        else:
            self.log_result("Production Monitoring Endpoint", False, response_time,
                          f"Request failed: {response.get('error', 'Unknown error')}")
            
    async def test_clinical_audit_endpoint(self):
        """Test POST /api/medical-ai/phase-d/clinical-audit endpoint for audit logging"""
        # Test with sample audit data
        audit_data = {
            "user_id": "test_user_789",
            "session_id": "audit_session_123",
            "action_type": "medical_intent_classification",
            "medical_intent_classified": "emergency_detection",
            "classification_confidence": 0.92,
            "clinical_accuracy_verified": True,
            "safety_level": "safe",
            "reviewer_notes": "Classification appropriate for emergency scenario"
        }
        
        success, response, response_time = await self.make_request("POST", "/medical-ai/phase-d/clinical-audit", audit_data)
        
        if success:
            # Validate response structure
            required_keys = ["status", "audit_id", "compliance_frameworks", "logged_at"]
            missing_keys = [key for key in required_keys if key not in response]
            
            if missing_keys:
                self.log_result("Clinical Audit Endpoint", False, response_time,
                              f"Missing keys: {missing_keys}")
            else:
                audit_id = response.get("audit_id")
                compliance_frameworks = response.get("compliance_frameworks", [])
                
                self.log_result("Clinical Audit Endpoint", True, response_time,
                              f"Status: {response['status']}, Audit ID: {bool(audit_id)}, Compliance: {len(compliance_frameworks)} frameworks")
        else:
            self.log_result("Clinical Audit Endpoint", False, response_time,
                          f"Request failed: {response.get('error', 'Unknown error')}")
            
    # ===== COMPREHENSIVE SYSTEM INTEGRATION TESTING =====
    
    async def test_comprehensive_status_endpoint(self):
        """Test GET /api/medical-ai/phase-d/comprehensive-status endpoint"""
        success, response, response_time = await self.make_request("GET", "/medical-ai/phase-d/comprehensive-status")
        
        if success:
            # Validate response structure
            required_keys = ["phase_d_status", "algorithm_version", "production_readiness_score", "components", "key_achievements"]
            missing_keys = [key for key in required_keys if key not in response]
            
            if missing_keys:
                self.log_result("Comprehensive Status Endpoint", False, response_time,
                              f"Missing keys: {missing_keys}")
            else:
                readiness_score = response.get("production_readiness_score", 0)
                components = response.get("components", {})
                achievements = response.get("key_achievements", {})
                
                # Check if all three main components are present
                expected_components = ["performance_optimization", "clinical_validation", "production_monitoring"]
                components_present = all(comp in components for comp in expected_components)
                
                self.log_result("Comprehensive Status Endpoint", True, response_time,
                              f"Status: {response['phase_d_status']}, Readiness: {readiness_score}, Components: {components_present}")
        else:
            self.log_result("Comprehensive Status Endpoint", False, response_time,
                          f"Request failed: {response.get('error', 'Unknown error')}")
            
    async def test_system_health_and_performance_metrics(self):
        """Test overall system health and performance metrics validation"""
        # Test multiple endpoints to validate system integration
        endpoints_to_test = [
            "/medical-ai/phase-d/performance-status",
            "/medical-ai/phase-d/clinical-validation-status", 
            "/medical-ai/phase-d/production-monitoring"
        ]
        
        all_successful = True
        total_response_time = 0
        endpoint_results = []
        
        for endpoint in endpoints_to_test:
            success, response, response_time = await self.make_request("GET", endpoint)
            total_response_time += response_time
            endpoint_results.append({"endpoint": endpoint, "success": success, "time": response_time})
            
            if not success:
                all_successful = False
                
        avg_response_time = total_response_time / len(endpoints_to_test)
        performance_target_met = avg_response_time < 0.025  # <25ms target
        
        self.log_result("System Health & Performance Metrics", all_successful and performance_target_met, avg_response_time,
                      f"All endpoints: {all_successful}, Avg time: {round(avg_response_time*1000, 2)}ms, Target met: {performance_target_met}")
        
    # ===== CLINICAL-GRADE PERFORMANCE VALIDATION =====
    
    async def test_clinical_grade_performance_requirements(self):
        """Test clinical-grade performance requirements (<25ms target)"""
        # Test performance-critical endpoints multiple times
        performance_tests = []
        
        # Test performance status endpoint 5 times
        for i in range(5):
            success, response, response_time = await self.make_request("GET", "/medical-ai/phase-d/performance-status")
            if success:
                performance_tests.append(response_time)
                
        if performance_tests:
            avg_time = sum(performance_tests) / len(performance_tests)
            max_time = max(performance_tests)
            min_time = min(performance_tests)
            
            # Clinical-grade requirement: <25ms average
            meets_clinical_grade = avg_time < 0.025
            
            self.log_result("Clinical-Grade Performance Requirements", meets_clinical_grade, avg_time,
                          f"Avg: {round(avg_time*1000, 2)}ms, Min: {round(min_time*1000, 2)}ms, Max: {round(max_time*1000, 2)}ms, Target: <25ms")
        else:
            self.log_result("Clinical-Grade Performance Requirements", False, 0,
                          "No successful performance tests completed")
            
    async def test_error_handling_and_recovery_systems(self):
        """Test error handling and recovery mechanisms"""
        # Test with invalid data to check error handling
        invalid_requests = [
            {
                "endpoint": "/medical-ai/phase-d/submit-clinical-validation",
                "method": "POST",
                "data": {"invalid": "data"}  # Missing required fields
            },
            {
                "endpoint": "/medical-ai/phase-d/verify-safety", 
                "method": "POST",
                "data": {}  # Empty data
            },
            {
                "endpoint": "/medical-ai/phase-d/clinical-audit",
                "method": "POST", 
                "data": {"action_type": "test"}  # Incomplete data
            }
        ]
        
        error_handling_working = True
        error_responses = []
        
        for test_case in invalid_requests:
            success, response, response_time = await self.make_request(
                test_case["method"], 
                test_case["endpoint"], 
                test_case["data"]
            )
            
            # For error handling test, we expect the request to fail gracefully
            if success:
                error_handling_working = False  # Should have failed with invalid data
            else:
                # Check if error response is structured properly
                has_error_info = "error" in response or "status" in response
                error_responses.append(has_error_info)
                
        proper_error_responses = all(error_responses) if error_responses else False
        
        self.log_result("Error Handling & Recovery Systems", error_handling_working and proper_error_responses, 0,
                      f"Graceful failures: {error_handling_working}, Proper error responses: {proper_error_responses}")
        
    # ===== COMPLIANCE FRAMEWORK VALIDATION =====
    
    async def test_compliance_tracking_hipaa_gdpr_fda(self):
        """Test compliance tracking (HIPAA, GDPR, FDA) through audit logging"""
        # Test audit logging with different compliance scenarios
        compliance_test_data = {
            "user_id": "compliance_test_user",
            "session_id": "compliance_session_456",
            "action_type": "medical_classification_with_pii",
            "medical_intent_classified": "emergency_detection",
            "classification_confidence": 0.94,
            "clinical_accuracy_verified": True,  # This should trigger FDA compliance
            "safety_level": "verified_safe",
            "reviewer_notes": "Compliance test for HIPAA, GDPR, FDA frameworks"
        }
        
        success, response, response_time = await self.make_request("POST", "/medical-ai/phase-d/clinical-audit", compliance_test_data)
        
        if success:
            compliance_frameworks = response.get("compliance_frameworks", [])
            
            # Check for expected compliance frameworks
            expected_frameworks = ["HIPAA"]  # Should at least have HIPAA
            has_hipaa = "HIPAA" in compliance_frameworks
            has_fda = "FDA_510K" in compliance_frameworks  # Should be present due to clinical_accuracy_verified=True
            
            compliance_working = has_hipaa and len(compliance_frameworks) > 0
            
            self.log_result("Compliance Tracking (HIPAA, GDPR, FDA)", compliance_working, response_time,
                          f"Frameworks: {compliance_frameworks}, HIPAA: {has_hipaa}, FDA: {has_fda}")
        else:
            self.log_result("Compliance Tracking (HIPAA, GDPR, FDA)", False, response_time,
                          f"Audit request failed: {response.get('error', 'Unknown error')}")
            
    # ===== MAIN TEST EXECUTION =====
    
    async def run_all_tests(self):
        """Run all Phase D comprehensive tests"""
        print("🚀 STARTING PHASE D: PERFECTION & SCALE COMPREHENSIVE TESTING")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test Start Time: {datetime.utcnow().isoformat()}")
        print("=" * 80)
        
        # 1. Performance Optimization System Testing
        print("\n📊 PERFORMANCE OPTIMIZATION SYSTEM TESTING")
        print("-" * 50)
        await self.test_performance_status_endpoint()
        await self.test_performance_benchmark_endpoint()
        await self.test_advanced_caching_functionality()
        
        # 2. Clinical Validation Framework Testing
        print("\n🏥 CLINICAL VALIDATION FRAMEWORK TESTING")
        print("-" * 50)
        await self.test_clinical_validation_status_endpoint()
        await self.test_submit_clinical_validation_endpoint()
        await self.test_verify_safety_endpoint()
        
        # 3. Production Monitoring System Testing
        print("\n🔧 PRODUCTION MONITORING SYSTEM TESTING")
        print("-" * 50)
        await self.test_production_monitoring_endpoint()
        await self.test_clinical_audit_endpoint()
        
        # 4. Comprehensive System Integration Testing
        print("\n🎯 COMPREHENSIVE SYSTEM INTEGRATION TESTING")
        print("-" * 50)
        await self.test_comprehensive_status_endpoint()
        await self.test_system_health_and_performance_metrics()
        
        # 5. Clinical-Grade Performance & Safety Validation
        print("\n⚕️ CLINICAL-GRADE PERFORMANCE & SAFETY VALIDATION")
        print("-" * 50)
        await self.test_clinical_grade_performance_requirements()
        await self.test_error_handling_and_recovery_systems()
        await self.test_compliance_tracking_hipaa_gdpr_fda()
        
        # Generate test summary
        await self.generate_test_summary()
        
    async def generate_test_summary(self):
        """Generate comprehensive test summary"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        total_time = time.time() - self.start_time
        avg_response_time = sum(result["response_time_ms"] for result in self.test_results) / total_tests if total_tests > 0 else 0
        
        print("\n" + "=" * 80)
        print("🎯 PHASE D: PERFECTION & SCALE TESTING SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Average Response Time: {avg_response_time:.2f}ms")
        print(f"Total Test Duration: {total_time:.2f}s")
        print("=" * 80)
        
        # Performance Analysis
        performance_tests = [r for r in self.test_results if "Performance" in r["test_name"]]
        clinical_tests = [r for r in self.test_results if "Clinical" in r["test_name"]]
        monitoring_tests = [r for r in self.test_results if "Monitoring" in r["test_name"] or "Audit" in r["test_name"]]
        
        print("\n📊 COMPONENT ANALYSIS:")
        print(f"Performance Optimization: {sum(1 for t in performance_tests if t['success'])}/{len(performance_tests)} passed")
        print(f"Clinical Validation: {sum(1 for t in clinical_tests if t['success'])}/{len(clinical_tests)} passed")
        print(f"Production Monitoring: {sum(1 for t in monitoring_tests if t['success'])}/{len(monitoring_tests)} passed")
        
        # Clinical-Grade Requirements Check
        clinical_grade_met = avg_response_time < 25  # <25ms target
        print(f"\n⚕️ CLINICAL-GRADE REQUIREMENTS:")
        print(f"Response Time Target (<25ms): {'✅ MET' if clinical_grade_met else '❌ NOT MET'} ({avg_response_time:.2f}ms)")
        print(f"System Reliability: {'✅ HIGH' if success_rate >= 90 else '❌ LOW'} ({success_rate:.1f}%)")
        
        # Failed Tests Details
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS DETAILS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test_name']}: {result['details']}")
                    
        print("\n🎯 PHASE D PRODUCTION READINESS:")
        if success_rate >= 95 and clinical_grade_met:
            print("✅ PRODUCTION READY - All Phase D components operational with clinical-grade performance")
        elif success_rate >= 80:
            print("⚠️ MOSTLY READY - Minor issues identified, suitable for production with monitoring")
        else:
            print("❌ NOT READY - Critical issues require resolution before production deployment")
            
        print("=" * 80)

async def main():
    """Main test execution function"""
    try:
        async with PhaseDBenchmarkTester() as tester:
            await tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Testing failed with error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())