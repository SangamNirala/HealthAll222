#!/usr/bin/env python3
"""
🎯 MULTI-SYMPTOM PARSING ENDPOINT FOCUSED TESTING

This test suite focuses specifically on testing the multi-symptom parsing endpoint 
`/api/medical-ai/multi-symptom-parse` to identify the root cause of the 
"first argument must be callable or None" error reported in the _assess_multi_symptom_urgency method.

TESTING SCOPE:
1. Test simple scenarios to reproduce the error
2. Test the statistics endpoint
3. Identify exactly where the error occurs
4. Check if the fix with default="routine" parameter is working
5. Examine logs for detailed error traces

TARGET: Identify and validate the fix for the max() function error
"""

import asyncio
import json
import time
import requests
import sys
from typing import Dict, Any, List
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://medchat-enhance-1.preview.emergentagent.com/api"

class MultiSymptomParseErrorTester:
    """Focused tester for multi-symptom parsing error diagnosis"""
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_test_result(self, test_name: str, success: bool, details: str, response_time: float = 0, response_data: Dict = None):
        """Log individual test results with detailed response data"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "response_time_ms": response_time,
            "response_data": response_data,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        print(f"   Details: {details}")
        if response_time > 0:
            print(f"   Response Time: {response_time:.2f}ms")
        if not success and response_data:
            print(f"   Error Response: {json.dumps(response_data, indent=2)}")
        print()

    async def test_simple_scenarios(self):
        """
        TEST SCENARIO 1: SIMPLE SCENARIOS FROM REVIEW REQUEST
        Test the exact scenarios mentioned in the review request to reproduce the error
        """
        print("🎯 TESTING SCENARIO 1: SIMPLE SCENARIOS FROM REVIEW REQUEST")
        print("=" * 80)
        
        # Test cases from review request
        test_cases = [
            {
                "name": "Simple Head Hurts",
                "text": "head hurts",
                "description": "Basic single symptom test"
            },
            {
                "name": "Multi-Symptom Expression",
                "text": "head hurts stomach upset cant sleep",
                "description": "Multiple symptoms in informal language"
            },
            {
                "name": "Emergency Scenario",
                "text": "chest pain and shortness of breath",
                "description": "Emergency combination that should trigger urgency assessment"
            }
        ]
        
        for test_case in test_cases:
            await self._test_multi_symptom_parsing_detailed(test_case)

    async def _test_multi_symptom_parsing_detailed(self, test_case: Dict[str, Any]):
        """Test individual multi-symptom parsing scenario with detailed error analysis"""
        try:
            # Prepare request
            request_data = {
                "text": test_case["text"],
                "patient_id": "error-test-123",
                "include_relationships": True,
                "include_clinical_reasoning": True
            }
            
            print(f"🔍 Testing: {test_case['name']}")
            print(f"   Input: '{test_case['text']}'")
            print(f"   Description: {test_case['description']}")
            
            # Make API call with timing
            start_time = time.time()
            response = requests.post(
                f"{self.backend_url}/medical-ai/multi-symptom-parse",
                json=request_data,
                timeout=30
            )
            response_time = (time.time() - start_time) * 1000
            
            print(f"   HTTP Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    
                    # Check if parsing was successful
                    if result.get("success", False):
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
                                response_time,
                                result
                            )
                            return
                        
                        # Extract key information
                        summary = result.get("summary", {})
                        urgency = result.get("urgency_assessment", "unknown")
                        total_symptoms = summary.get("total_symptoms", 0)
                        
                        # Success - log detailed results
                        details = f"SUCCESS: {total_symptoms} symptoms detected, urgency: {urgency}"
                        self.log_test_result(test_case["name"], True, details, response_time, result)
                        
                        # Print additional details for successful parsing
                        print(f"   ✅ Symptoms detected: {total_symptoms}")
                        print(f"   ✅ Urgency assessment: {urgency}")
                        print(f"   ✅ Clinical recommendations: {len(result.get('clinical_recommendations', []))}")
                        
                    else:
                        # Parsing failed - this might be our error
                        error_msg = result.get("error", "Unknown parsing error")
                        self.log_test_result(
                            test_case["name"],
                            False,
                            f"PARSING FAILED: {error_msg}",
                            response_time,
                            result
                        )
                        
                        # Check if this is the specific error we're looking for
                        if "first argument must be callable or None" in error_msg:
                            print(f"   🎯 FOUND TARGET ERROR: {error_msg}")
                        
                except json.JSONDecodeError as e:
                    self.log_test_result(
                        test_case["name"],
                        False,
                        f"JSON decode error: {str(e)}",
                        response_time,
                        {"raw_response": response.text[:500]}
                    )
                    
            else:
                # HTTP error
                try:
                    error_response = response.json()
                except:
                    error_response = {"raw_text": response.text[:500]}
                
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    response_time,
                    error_response
                )
                
                # Check if this is the specific error we're looking for
                if "first argument must be callable or None" in response.text:
                    print(f"   🎯 FOUND TARGET ERROR in HTTP response: {response.text[:300]}")
                
        except Exception as e:
            self.log_test_result(
                test_case["name"],
                False,
                f"Exception: {str(e)}",
                0,
                {"exception": str(e)}
            )
            
            # Check if this is the specific error we're looking for
            if "first argument must be callable or None" in str(e):
                print(f"   🎯 FOUND TARGET ERROR in exception: {str(e)}")

    async def test_statistics_endpoint(self):
        """
        TEST SCENARIO 2: STATISTICS ENDPOINT
        Test the statistics endpoint to see if it works correctly
        """
        print("📊 TESTING SCENARIO 2: STATISTICS ENDPOINT")
        print("=" * 80)
        
        try:
            # Test statistics endpoint
            start_time = time.time()
            response = requests.get(
                f"{self.backend_url}/medical-ai/multi-symptom-parser-statistics",
                timeout=30
            )
            response_time = (time.time() - start_time) * 1000
            
            print(f"   HTTP Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    stats = response.json()
                    
                    # Validate statistics structure
                    required_stats_fields = [
                        "status", "algorithm_version", "parser_performance"
                    ]
                    
                    missing_fields = [field for field in required_stats_fields if field not in stats]
                    if missing_fields:
                        self.log_test_result(
                            "Statistics Endpoint",
                            False,
                            f"Missing fields: {missing_fields}",
                            response_time,
                            stats
                        )
                    else:
                        # Success
                        algorithm_version = stats.get("algorithm_version", "unknown")
                        status = stats.get("status", "unknown")
                        
                        details = f"SUCCESS: Status={status}, Algorithm={algorithm_version}"
                        self.log_test_result("Statistics Endpoint", True, details, response_time, stats)
                        
                        print(f"   ✅ Status: {status}")
                        print(f"   ✅ Algorithm Version: {algorithm_version}")
                        print(f"   ✅ Response structure valid")
                        
                except json.JSONDecodeError as e:
                    self.log_test_result(
                        "Statistics Endpoint",
                        False,
                        f"JSON decode error: {str(e)}",
                        response_time,
                        {"raw_response": response.text[:500]}
                    )
                    
            else:
                # HTTP error
                try:
                    error_response = response.json()
                except:
                    error_response = {"raw_text": response.text[:500]}
                
                self.log_test_result(
                    "Statistics Endpoint",
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    response_time,
                    error_response
                )
                
        except Exception as e:
            self.log_test_result(
                "Statistics Endpoint",
                False,
                f"Exception: {str(e)}",
                0,
                {"exception": str(e)}
            )

    async def test_edge_cases_for_max_error(self):
        """
        TEST SCENARIO 3: EDGE CASES TO TRIGGER MAX ERROR
        Test specific scenarios that might trigger the max() function error
        """
        print("🔍 TESTING SCENARIO 3: EDGE CASES TO TRIGGER MAX ERROR")
        print("=" * 80)
        
        # Edge cases that might trigger the max() error in _assess_multi_symptom_urgency
        edge_cases = [
            {
                "name": "Empty Syndromes Test",
                "text": "mild headache",
                "description": "Simple symptom that might not generate syndromes"
            },
            {
                "name": "Complex Multi-System",
                "text": "severe chest pain with shortness of breath and sweating",
                "description": "Complex scenario that should generate multiple syndromes"
            },
            {
                "name": "Vague Symptoms",
                "text": "not feeling well tired",
                "description": "Vague symptoms that might not trigger syndrome detection"
            },
            {
                "name": "Emergency Combination",
                "text": "crushing chest pain radiating to left arm with nausea",
                "description": "Clear emergency that should trigger syndrome detection"
            }
        ]
        
        for test_case in edge_cases:
            await self._test_multi_symptom_parsing_detailed(test_case)

    async def test_data_structure_validation(self):
        """
        TEST SCENARIO 4: DATA STRUCTURE VALIDATION
        Test to understand the data structures in parse_result that might cause the error
        """
        print("🔬 TESTING SCENARIO 4: DATA STRUCTURE VALIDATION")
        print("=" * 80)
        
        # Test with a scenario that should work to understand the data structure
        test_case = {
            "name": "Data Structure Analysis",
            "text": "headache and nausea",
            "description": "Simple multi-symptom for structure analysis"
        }
        
        try:
            request_data = {
                "text": test_case["text"],
                "patient_id": "structure-test-456",
                "include_relationships": True,
                "include_clinical_reasoning": True
            }
            
            print(f"🔍 Analyzing data structures for: '{test_case['text']}'")
            
            start_time = time.time()
            response = requests.post(
                f"{self.backend_url}/medical-ai/multi-symptom-parse",
                json=request_data,
                timeout=30
            )
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("success", False):
                    # Analyze the structure
                    parse_result = result.get("multi_symptom_parse_result", {})
                    
                    print("   📋 Parse Result Structure Analysis:")
                    print(f"   - Keys in parse_result: {list(parse_result.keys())}")
                    
                    # Look for syndrome-related data
                    if "potential_syndromes" in parse_result:
                        syndromes = parse_result["potential_syndromes"]
                        print(f"   - Potential syndromes found: {len(syndromes) if isinstance(syndromes, list) else 'Not a list'}")
                        if isinstance(syndromes, list) and syndromes:
                            print(f"   - First syndrome structure: {list(syndromes[0].keys()) if syndromes[0] else 'Empty'}")
                    
                    # Look for urgency indicators
                    if "urgency_indicators" in parse_result:
                        urgency_indicators = parse_result["urgency_indicators"]
                        print(f"   - Urgency indicators: {urgency_indicators}")
                    
                    # Look for symptom relationships
                    if "symptom_relationships" in parse_result:
                        relationships = parse_result["symptom_relationships"]
                        print(f"   - Symptom relationships: {type(relationships)}")
                        if isinstance(relationships, dict):
                            print(f"   - Relationship keys: {list(relationships.keys())}")
                    
                    self.log_test_result(
                        test_case["name"],
                        True,
                        "Structure analysis completed successfully",
                        response_time,
                        result
                    )
                    
                else:
                    error_msg = result.get("error", "Unknown error")
                    self.log_test_result(
                        test_case["name"],
                        False,
                        f"Parsing failed: {error_msg}",
                        response_time,
                        result
                    )
                    
                    if "first argument must be callable or None" in error_msg:
                        print(f"   🎯 FOUND TARGET ERROR during structure analysis: {error_msg}")
                        
            else:
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    response_time,
                    {"raw_response": response.text[:500]}
                )
                
        except Exception as e:
            self.log_test_result(
                test_case["name"],
                False,
                f"Exception during structure analysis: {str(e)}",
                0,
                {"exception": str(e)}
            )

    async def run_comprehensive_tests(self):
        """Run all comprehensive tests for multi-symptom parsing error diagnosis"""
        print("🎯 MULTI-SYMPTOM PARSING ERROR DIAGNOSIS TESTING")
        print("=" * 100)
        print(f"Backend URL: {self.backend_url}")
        print(f"Test Start Time: {datetime.now().isoformat()}")
        print("Target Error: 'first argument must be callable or None' in _assess_multi_symptom_urgency")
        print("=" * 100)
        print()
        
        # Run all test scenarios
        await self.test_simple_scenarios()
        await self.test_statistics_endpoint()
        await self.test_edge_cases_for_max_error()
        await self.test_data_structure_validation()
        
        # Generate final report
        self.generate_final_report()

    def generate_final_report(self):
        """Generate comprehensive final test report"""
        print("=" * 100)
        print("🎯 MULTI-SYMPTOM PARSING ERROR DIAGNOSIS - FINAL TEST REPORT")
        print("=" * 100)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed Tests: {self.passed_tests}")
        print(f"   Failed Tests: {self.total_tests - self.passed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        # Analyze errors for the target error
        target_error_found = False
        target_error_tests = []
        
        for result in self.test_results:
            if not result["success"]:
                error_details = result["details"]
                response_data = result.get("response_data", {})
                
                # Check for the target error in various places
                if ("first argument must be callable or None" in error_details or
                    (response_data and "first argument must be callable or None" in str(response_data))):
                    target_error_found = True
                    target_error_tests.append(result)
        
        print("🎯 TARGET ERROR ANALYSIS:")
        if target_error_found:
            print(f"   ❌ TARGET ERROR FOUND: 'first argument must be callable or None'")
            print(f"   📍 Error occurred in {len(target_error_tests)} test(s):")
            for error_test in target_error_tests:
                print(f"      - {error_test['test_name']}: {error_test['details']}")
        else:
            print(f"   ✅ TARGET ERROR NOT FOUND: The max() function error may have been fixed")
        print()
        
        # Categorize results by test scenario
        scenarios = {
            "Simple Scenarios": [],
            "Statistics Endpoint": [],
            "Edge Cases": [],
            "Data Structure": []
        }
        
        for result in self.test_results:
            test_name = result["test_name"]
            if "Statistics" in test_name:
                scenarios["Statistics Endpoint"].append(result)
            elif any(keyword in test_name for keyword in ["Simple", "Multi-Symptom Expression", "Emergency Scenario"]):
                scenarios["Simple Scenarios"].append(result)
            elif any(keyword in test_name for keyword in ["Empty", "Complex", "Vague", "Emergency Combination"]):
                scenarios["Edge Cases"].append(result)
            elif "Data Structure" in test_name:
                scenarios["Data Structure"].append(result)
        
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
        
        # API Functionality Assessment
        print("🔧 API FUNCTIONALITY ASSESSMENT:")
        
        # Check if multi-symptom parsing endpoint is working
        parsing_working = any(r["success"] for r in self.test_results if "Statistics" not in r["test_name"])
        print(f"   Multi-Symptom Parsing Endpoint: {'✅ WORKING' if parsing_working else '❌ NOT WORKING'}")
        
        # Check if statistics endpoint is working
        stats_working = any(r["success"] for r in self.test_results if "Statistics" in r["test_name"])
        print(f"   Statistics Endpoint: {'✅ WORKING' if stats_working else '❌ NOT WORKING'}")
        
        print()
        
        # Root Cause Analysis
        print("🔍 ROOT CAUSE ANALYSIS:")
        if target_error_found:
            print("   🎯 ISSUE CONFIRMED: The 'first argument must be callable or None' error is still occurring")
            print("   📍 LOCATION: _assess_multi_symptom_urgency method around line 10205")
            print("   🔧 LIKELY CAUSE: max() function called with default parameter as string instead of callable")
            print("   💡 SUGGESTED FIX: Change default='routine' to default=lambda: 'routine' or use different approach")
        else:
            if parsing_working:
                print("   ✅ ISSUE RESOLVED: The max() function error appears to have been fixed")
                print("   🎉 MULTI-SYMPTOM PARSING: Working correctly with all test scenarios")
            else:
                print("   ❓ UNCLEAR STATUS: No target error found but parsing still failing")
                print("   🔍 INVESTIGATION NEEDED: Different error may be occurring")
        
        print()
        
        # Final assessment
        if success_rate >= 80:
            print("🎉 ASSESSMENT: MULTI-SYMPTOM PARSING SYSTEM IS WORKING WELL!")
            print("   The system successfully handles the test scenarios without the target error.")
        elif success_rate >= 50:
            print("⚠️  ASSESSMENT: MULTI-SYMPTOM PARSING HAS MIXED RESULTS")
            print("   Some functionality is working but issues remain.")
        else:
            print("❌ ASSESSMENT: MULTI-SYMPTOM PARSING NEEDS SIGNIFICANT WORK")
            print("   Multiple critical issues detected.")
        
        print()
        print(f"Test Completion Time: {datetime.now().isoformat()}")
        print("=" * 100)

async def main():
    """Main test execution function"""
    tester = MultiSymptomParseErrorTester()
    await tester.run_comprehensive_tests()

if __name__ == "__main__":
    asyncio.run(main())