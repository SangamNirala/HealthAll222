#!/usr/bin/env python3
"""
PHASE 4 COMPREHENSIVE MEDICAL PATTERN RECOGNITION ENGINE TESTING
================================================================

Critical validation testing for Phase 4 Comprehensive Medical Pattern Recognition Engine
focusing on ultra-challenging scenarios and syndrome detection as specified in review request.

CRITICAL VALIDATION REQUIREMENTS:
1. Ultra-Challenging Scenario 1: Complex chest pain - MUST detect EMERGENCY urgency and acute coronary syndrome
2. Ultra-Challenging Scenario 2: Complex migraine - MUST detect URGENT urgency and migraine syndrome
3. Syndrome Detection: acute_coronary_syndrome, migraine_syndrome, stroke_syndrome, acute_abdomen
4. Performance: Processing times <40ms
5. API Integration: POST /api/medical-ai/initialize and POST /api/medical-ai/message
"""

import asyncio
import json
import time
import requests
import sys
import os
from datetime import datetime
from typing import Dict, Any, List

# Backend URL from environment
BACKEND_URL = "https://medreasoning.preview.emergentagent.com/api"

class Phase4CriticalTester:
    """
    🚨 PHASE 4 CRITICAL VALIDATION TESTER 🚨
    
    Tests the critical fixes for ultra-challenging scenarios and syndrome detection
    as specified in the review request.
    """
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.test_results = []
        self.critical_failures = []
        
        print("🚨 PHASE 4 CRITICAL VALIDATION TESTER INITIALIZED")
        print("=" * 80)
        
    async def run_critical_validation_tests(self):
        """Run all critical validation tests as specified in review request"""
        
        print("\n🎯 STARTING PHASE 4 CRITICAL VALIDATION TESTING")
        print("=" * 80)
        
        # Test 1: Ultra-Challenging Scenario 1 (MUST PASS)
        await self.test_ultra_challenging_scenario_1()
        
        # Test 2: Ultra-Challenging Scenario 2 (MUST PASS)
        await self.test_ultra_challenging_scenario_2()
        
        # Test 3: Syndrome Detection Validation
        await self.test_syndrome_detection_validation()
        
        # Test 4: Performance Requirements
        await self.test_performance_requirements()
        
        # Generate critical validation report
        self.generate_critical_validation_report()
        
    async def test_ultra_challenging_scenario_1(self):
        """
        🔥 ULTRA-CHALLENGING SCENARIO 1 (MUST PASS)
        
        Input: Complex chest pain scenario with radiation and associated symptoms
        Expected: EMERGENCY urgency (not routine)
        Expected: Acute coronary syndrome detection
        Expected: Processing <40ms
        """
        
        print("\n🔥 ULTRA-CHALLENGING SCENARIO 1 TESTING")
        print("-" * 50)
        
        scenario_1_input = "Sharp stabbing pain in my left upper chest that started suddenly this morning after lifting heavy boxes at work, getting progressively worse with deep breathing and movement, radiating down my left arm to my fingers with tingling, accompanied by mild nausea and cold sweats, comes in waves every 2-3 minutes lasting about 30 seconds each, completely disappears when I sit perfectly still and breathe shallow"
        
        print(f"Input: {scenario_1_input[:100]}...")
        print("Expected: EMERGENCY urgency, Acute coronary syndrome detection")
        
        # Test with Medical AI API
        scenario_1_results = await self.test_scenario_with_medical_ai(
            scenario_1_input, 
            "ultra-challenging-scenario-1",
            expected_urgency="emergency",
            expected_syndrome="acute_coronary_syndrome"
        )
        
        # Validate critical requirements
        critical_pass = (
            scenario_1_results.get("urgency_correct", False) and
            scenario_1_results.get("syndrome_detected", False) and
            scenario_1_results.get("performance_acceptable", False)
        )
        
        if not critical_pass:
            self.critical_failures.append("❌ CRITICAL FAILURE: Ultra-Challenging Scenario 1 failed")
            
        self.test_results.append({
            "test": "Ultra-Challenging Scenario 1",
            "status": "PASS" if critical_pass else "FAIL",
            "critical": True,
            "details": scenario_1_results
        })
        
        status = "✅ PASS" if critical_pass else "❌ FAIL"
        print(f"{status} - Urgency: {scenario_1_results.get('detected_urgency')}, Syndrome: {scenario_1_results.get('syndrome_detected')}")
        
    async def test_ultra_challenging_scenario_2(self):
        """
        🔥 ULTRA-CHALLENGING SCENARIO 2 (MUST PASS)
        
        Input: Complex migraine scenario with multiple triggers and symptoms
        Expected: URGENT urgency (not routine)
        Expected: Migraine syndrome detection
        """
        
        print("\n🔥 ULTRA-CHALLENGING SCENARIO 2 TESTING")
        print("-" * 50)
        
        scenario_2_input = "For the past month I've been getting these absolutely terrible headaches on the right side of my head, usually starting behind my right eye, throbbing and pulsating like my heart is beating in my head, typically triggered by fluorescent lights at work or when my kids are being loud, almost always accompanied by severe nausea and sensitivity to light and sound, sometimes progressing to vomiting, lasting anywhere from 4-12 hours, happening about 2-3 times per week usually in the late afternoon, completely debilitating - I have to lie in a dark quiet room and can't function at all"
        
        print(f"Input: {scenario_2_input[:100]}...")
        print("Expected: URGENT urgency, Migraine syndrome detection")
        
        # Test with Medical AI API
        scenario_2_results = await self.test_scenario_with_medical_ai(
            scenario_2_input,
            "ultra-challenging-scenario-2", 
            expected_urgency="urgent",
            expected_syndrome="migraine_syndrome"
        )
        
        # Validate critical requirements
        critical_pass = (
            scenario_2_results.get("urgency_correct", False) and
            scenario_2_results.get("syndrome_detected", False) and
            scenario_2_results.get("performance_acceptable", False)
        )
        
        if not critical_pass:
            self.critical_failures.append("❌ CRITICAL FAILURE: Ultra-Challenging Scenario 2 failed")
            
        self.test_results.append({
            "test": "Ultra-Challenging Scenario 2", 
            "status": "PASS" if critical_pass else "FAIL",
            "critical": True,
            "details": scenario_2_results
        })
        
        status = "✅ PASS" if critical_pass else "❌ FAIL"
        print(f"{status} - Urgency: {scenario_2_results.get('detected_urgency')}, Syndrome: {scenario_2_results.get('syndrome_detected')}")
        
    async def test_scenario_with_medical_ai(self, scenario_input: str, patient_id: str, expected_urgency: str, expected_syndrome: str) -> Dict[str, Any]:
        """Test scenario with Medical AI API endpoints"""
        
        results = {
            "api_success": False,
            "detected_urgency": "unknown",
            "urgency_correct": False,
            "syndrome_detected": False,
            "syndrome_mentioned": False,
            "performance_acceptable": False,
            "processing_time_ms": 0,
            "response_quality": False,
            "medical_reasoning": False,
            "error": None
        }
        
        try:
            # Initialize consultation
            start_time = time.time()
            
            init_response = requests.post(f"{self.backend_url}/medical-ai/initialize", 
                json={"patient_id": patient_id, "timestamp": datetime.now().isoformat()},
                timeout=30)
            
            if init_response.status_code == 200:
                init_data = init_response.json()
                consultation_id = init_data.get("consultation_id")
                
                # Send scenario message
                message_start_time = time.time()
                message_response = requests.post(f"{self.backend_url}/medical-ai/message",
                    json={
                        "consultation_id": consultation_id,
                        "message": scenario_input,
                        "timestamp": datetime.now().isoformat()
                    },
                    timeout=30)
                
                processing_time = (time.time() - message_start_time) * 1000  # Convert to milliseconds
                results["processing_time_ms"] = processing_time
                results["performance_acceptable"] = processing_time < 40
                
                if message_response.status_code == 200:
                    response_data = message_response.json()
                    results["api_success"] = True
                    
                    # Check urgency
                    detected_urgency = response_data.get("urgency", "routine")
                    results["detected_urgency"] = detected_urgency
                    results["urgency_correct"] = detected_urgency == expected_urgency
                    
                    # Check response quality
                    response_text = response_data.get("response", "")
                    results["response_quality"] = len(response_text) > 100
                    results["medical_reasoning"] = "context" in response_data or "medical_reasoning" in response_data
                    
                    # Check for syndrome mentions in response content
                    response_content = response_text.lower()
                    context_content = str(response_data.get("context", "")).lower()
                    differential_content = " ".join(response_data.get("differential_diagnoses", [])).lower()
                    all_content = f"{response_content} {context_content} {differential_content}"
                    
                    # Check for syndrome detection
                    if expected_syndrome == "acute_coronary_syndrome":
                        syndrome_keywords = ["acute coronary", "coronary syndrome", "heart attack", "myocardial infarction", "cardiac", "coronary artery"]
                        results["syndrome_mentioned"] = any(keyword in all_content for keyword in syndrome_keywords)
                    elif expected_syndrome == "migraine_syndrome":
                        syndrome_keywords = ["migraine", "migraine syndrome", "headache disorder", "cephalgia"]
                        results["syndrome_mentioned"] = any(keyword in all_content for keyword in syndrome_keywords)
                    
                    results["syndrome_detected"] = results["syndrome_mentioned"]
                    
                else:
                    results["error"] = f"Message API error: {message_response.status_code} - {message_response.text}"
            else:
                results["error"] = f"Init API error: {init_response.status_code} - {init_response.text}"
                
        except Exception as e:
            results["error"] = f"Exception: {str(e)}"
            
        return results
        
    async def test_syndrome_detection_validation(self):
        """
        🔬 SYNDROME DETECTION VALIDATION
        
        Test for detection of all 4 required syndromes:
        - acute_coronary_syndrome
        - migraine_syndrome  
        - stroke_syndrome
        - acute_abdomen
        """
        
        print("\n🔬 SYNDROME DETECTION VALIDATION")
        print("-" * 50)
        
        syndrome_test_cases = [
            {
                "name": "Acute Coronary Syndrome Detection",
                "input": "Crushing chest pain with shortness of breath, nausea, and sweating radiating to left arm",
                "expected_syndrome": "acute_coronary_syndrome",
                "expected_urgency": "emergency"
            },
            {
                "name": "Migraine Syndrome Detection",
                "input": "Severe throbbing headache with nausea, light sensitivity, and visual aura lasting 8 hours",
                "expected_syndrome": "migraine_syndrome",
                "expected_urgency": "urgent"
            },
            {
                "name": "Stroke Syndrome Detection", 
                "input": "Sudden weakness on left side with facial drooping and difficulty speaking",
                "expected_syndrome": "stroke_syndrome",
                "expected_urgency": "emergency"
            },
            {
                "name": "Acute Abdomen Detection",
                "input": "Severe right lower quadrant abdominal pain with fever, vomiting, and rebound tenderness",
                "expected_syndrome": "acute_abdomen",
                "expected_urgency": "emergency"
            }
        ]
        
        syndrome_detection_results = []
        
        for test_case in syndrome_test_cases:
            print(f"🔬 {test_case['name']}: {test_case['input'][:50]}...")
            
            # Test with Medical AI API
            results = await self.test_scenario_with_medical_ai(
                test_case["input"],
                f"syndrome-test-{test_case['name'].lower().replace(' ', '-')}",
                test_case["expected_urgency"],
                test_case["expected_syndrome"]
            )
            
            syndrome_success = results.get("syndrome_detected", False) and results.get("urgency_correct", False)
            syndrome_detection_results.append(syndrome_success)
            
            self.test_results.append({
                "test": test_case["name"],
                "status": "PASS" if syndrome_success else "FAIL",
                "details": results
            })
            
            status = "✅ PASS" if syndrome_success else "❌ FAIL"
            print(f"   {status} - Syndrome: {results.get('syndrome_detected')}, Urgency: {results.get('detected_urgency')}")
        
        # Overall syndrome detection success
        overall_syndrome_success = sum(syndrome_detection_results) >= 3  # At least 3/4 must pass
        
        if not overall_syndrome_success:
            self.critical_failures.append("❌ CRITICAL FAILURE: Syndrome detection validation failed")
            
        print(f"\n📊 SYNDROME DETECTION SUMMARY: {sum(syndrome_detection_results)}/4 syndromes detected correctly")
        
    async def test_performance_requirements(self):
        """
        ⚡ PERFORMANCE REQUIREMENTS VALIDATION
        
        Validate processing times are <40ms for multiple scenarios
        """
        
        print("\n⚡ PERFORMANCE REQUIREMENTS VALIDATION")
        print("-" * 50)
        
        performance_test_inputs = [
            "Chest pain with shortness of breath",
            "Severe headache with nausea and light sensitivity", 
            "Abdominal pain with fever and vomiting",
            "Sudden weakness and speech difficulty",
            "Sharp chest pain radiating to arm"
        ]
        
        performance_results = []
        
        for i, test_input in enumerate(performance_test_inputs, 1):
            print(f"⚡ Performance Test {i}: {test_input}")
            
            # Test performance with Medical AI API
            results = await self.test_scenario_with_medical_ai(
                test_input,
                f"performance-test-{i}",
                "routine",  # Don't care about urgency for performance test
                "none"      # Don't care about syndrome for performance test
            )
            
            processing_time = results.get("processing_time_ms", 999)
            performance_acceptable = processing_time < 40
            performance_results.append(performance_acceptable)
            
            status = "✅ PASS" if performance_acceptable else "❌ FAIL"
            print(f"   {status} - Processing Time: {processing_time:.1f}ms")
        
        # Calculate performance metrics
        avg_processing_time = sum(r.get("processing_time_ms", 999) for r in [
            await self.test_scenario_with_medical_ai(inp, f"perf-{i}", "routine", "none") 
            for i, inp in enumerate(performance_test_inputs)
        ]) / len(performance_test_inputs)
        
        performance_pass_rate = sum(performance_results) / len(performance_results)
        overall_performance_success = performance_pass_rate >= 0.8  # 80% must pass
        
        if not overall_performance_success:
            self.critical_failures.append("❌ CRITICAL FAILURE: Performance requirements not met")
            
        self.test_results.append({
            "test": "Performance Requirements",
            "status": "PASS" if overall_performance_success else "FAIL",
            "details": {
                "average_processing_time_ms": avg_processing_time,
                "performance_pass_rate": performance_pass_rate,
                "individual_results": performance_results
            }
        })
        
        print(f"\n📊 PERFORMANCE SUMMARY:")
        print(f"   Average Processing Time: {avg_processing_time:.1f}ms (Target: <40ms)")
        print(f"   Performance Pass Rate: {performance_pass_rate*100:.1f}% (Target: >80%)")
        
    def generate_critical_validation_report(self):
        """Generate critical validation report"""
        
        print("\n" + "=" * 80)
        print("🚨 PHASE 4 CRITICAL VALIDATION REPORT")
        print("=" * 80)
        
        # Calculate overall statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["status"] == "PASS")
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        # Critical tests
        critical_tests = [r for r in self.test_results if r.get("critical", False)]
        critical_passed = sum(1 for r in critical_tests if r["status"] == "PASS")
        critical_total = len(critical_tests)
        
        print(f"\n📊 OVERALL TEST RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {failed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Critical Tests: {critical_passed}/{critical_total} passed")
        
        # Detailed results
        print(f"\n🔍 DETAILED TEST RESULTS:")
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            critical_marker = " [CRITICAL]" if result.get("critical", False) else ""
            print(f"   {status_icon} {result['test']}{critical_marker}")
            
            # Show key details for failed tests
            if result["status"] == "FAIL" and "details" in result:
                details = result["details"]
                if isinstance(details, dict):
                    if "error" in details and details["error"]:
                        print(f"      Error: {details['error']}")
                    if "detected_urgency" in details:
                        print(f"      Detected Urgency: {details['detected_urgency']}")
                    if "syndrome_detected" in details:
                        print(f"      Syndrome Detected: {details['syndrome_detected']}")
                    if "processing_time_ms" in details:
                        print(f"      Processing Time: {details['processing_time_ms']:.1f}ms")
        
        # Critical failures
        if self.critical_failures:
            print(f"\n🚨 CRITICAL FAILURES:")
            for failure in self.critical_failures:
                print(f"   {failure}")
        
        # Final assessment
        print(f"\n🏆 FINAL ASSESSMENT:")
        if critical_passed == critical_total and success_rate >= 80:
            print("   ✅ PHASE 4 CRITICAL VALIDATION: SUCCESSFUL")
            print("   🎯 All critical ultra-challenging scenarios and syndrome detection working")
        elif critical_passed == critical_total:
            print("   ⚠️  PHASE 4 CRITICAL VALIDATION: MOSTLY SUCCESSFUL")
            print("   🔧 Critical scenarios pass but some minor issues detected")
        else:
            print("   ❌ PHASE 4 CRITICAL VALIDATION: FAILED")
            print("   🚨 Critical ultra-challenging scenarios or syndrome detection not working")
            print("   🔧 Major fixes required for Phase 4 implementation")
        
        print("\n" + "=" * 80)
        print("END OF PHASE 4 CRITICAL VALIDATION REPORT")
        print("=" * 80)

async def main():
    """Main testing function"""
    print("🚨 PHASE 4 CRITICAL VALIDATION TESTING")
    print("=" * 80)
    print("Testing critical fixes for ultra-challenging scenarios and syndrome detection...")
    print("=" * 80)
    
    # Initialize and run critical validation tests
    tester = Phase4CriticalTester()
    await tester.run_critical_validation_tests()

if __name__ == "__main__":
    asyncio.run(main())