#!/usr/bin/env python3
"""
🎯 PHASE 1 CRITICAL FIXES COMPREHENSIVE BACKEND TESTING

This test suite validates the Phase 1 critical fixes implementation as requested
in the review, focusing on comprehensive testing of:

1. Multi-Symptom Pattern Extraction - Complex multi-symptom expressions
2. Emergency Combination Detection - Red flag identification  
3. Clinical Reasoning Engine - Medical logic generation
4. Temporal Relationship Extraction - Time-based analysis
5. Performance Testing - Validate targets (<25ms processing, >95% accuracy)

TESTING SCOPE:
- RevolutionaryMultiSymptomParser system validation
- AdvancedSymptomRelationshipEngine testing
- /api/medical-ai/multi-symptom-parse endpoint comprehensive testing
- Performance benchmarking and accuracy validation

TARGET: Validate Phase 1 core functionality is working correctly
"""

import asyncio
import json
import time
import requests
import sys
from typing import Dict, Any, List
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://empathcare-ai.preview.emergentagent.com/api"

class Phase1CriticalFixesTester:
    """Comprehensive tester for Phase 1 Critical Fixes Implementation"""
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.performance_metrics = []
        
    def log_test_result(self, test_name: str, success: bool, details: str, response_time: float = 0, additional_data: Dict = None):
        """Log individual test results"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "response_time_ms": response_time,
            "timestamp": datetime.now().isoformat(),
            "additional_data": additional_data or {}
        }
        self.test_results.append(result)
        
        # Track performance metrics
        if response_time > 0:
            self.performance_metrics.append({
                "test": test_name,
                "processing_time_ms": response_time,
                "target_met": response_time < 25.0
            })
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        print(f"   Details: {details}")
        if response_time > 0:
            print(f"   Response Time: {response_time:.2f}ms (Target: <25ms)")
        print()

    async def test_multi_symptom_pattern_extraction(self):
        """
        TEST AREA 1: MULTI-SYMPTOM PATTERN EXTRACTION
        Test complex multi-symptom expressions as specified in review request
        """
        print("🎯 TESTING AREA 1: MULTI-SYMPTOM PATTERN EXTRACTION")
        print("=" * 80)
        
        # Test cases from review request
        test_cases = [
            {
                "name": "Complex Multi-Symptom Expression 1",
                "text": "head hurts stomach upset cant sleep 3 nights",
                "expected_symptoms": ["headache", "stomach upset", "insomnia"],
                "expected_count": 3,
                "temporal_elements": ["3 nights"]
            },
            {
                "name": "Complex Multi-Symptom Expression 2", 
                "text": "severe chest pain with shortness of breath and sweating",
                "expected_symptoms": ["chest pain", "shortness of breath", "sweating"],
                "expected_count": 3,
                "severity_indicators": ["severe"],
                "emergency_potential": True
            },
            {
                "name": "Complex Multi-Symptom Expression 3",
                "text": "crushing chest pain radiating to left arm with nausea",
                "expected_symptoms": ["chest pain", "arm pain", "nausea"],
                "expected_count": 3,
                "quality_descriptors": ["crushing", "radiating"],
                "emergency_potential": True
            },
            {
                "name": "Complex Multi-Symptom Expression 4",
                "text": "joint pain, fatigue, rash, fever",
                "expected_symptoms": ["joint pain", "fatigue", "rash", "fever"],
                "expected_count": 4,
                "systemic_symptoms": True
            }
        ]
        
        for test_case in test_cases:
            await self._test_multi_symptom_parsing(test_case, "Multi-Symptom Pattern Extraction")

    async def test_emergency_combination_detection(self):
        """
        TEST AREA 2: EMERGENCY COMBINATION DETECTION
        Test red flag identification as specified in review request
        """
        print("🚨 TESTING AREA 2: EMERGENCY COMBINATION DETECTION")
        print("=" * 80)
        
        # Emergency test cases from review request
        emergency_cases = [
            {
                "name": "Emergency Combination 1",
                "text": "chest pain and shortness of breath",
                "expected_symptoms": ["chest pain", "shortness of breath"],
                "expected_urgency": ["urgent", "emergency", "critical"],
                "emergency_combination": True,
                "red_flags": ["cardiac emergency"]
            },
            {
                "name": "Emergency Combination 2",
                "text": "worst headache ever with neck stiffness",
                "expected_symptoms": ["headache", "neck stiffness"],
                "expected_urgency": ["urgent", "emergency", "critical"],
                "emergency_combination": True,
                "red_flags": ["neurological emergency", "meningitis"]
            },
            {
                "name": "Emergency Combination 3",
                "text": "sudden weakness and facial drooping",
                "expected_symptoms": ["weakness", "facial drooping"],
                "expected_urgency": ["urgent", "emergency", "critical"],
                "emergency_combination": True,
                "red_flags": ["stroke", "neurological emergency"]
            },
            {
                "name": "Emergency Combination 4",
                "text": "severe allergic reaction throat swelling",
                "expected_symptoms": ["allergic reaction", "throat swelling"],
                "expected_urgency": ["urgent", "emergency", "critical"],
                "emergency_combination": True,
                "red_flags": ["anaphylaxis", "airway emergency"]
            }
        ]
        
        for test_case in emergency_cases:
            await self._test_emergency_detection(test_case)

    async def test_clinical_reasoning_engine(self):
        """
        TEST AREA 3: CLINICAL REASONING ENGINE
        Test medical logic generation as specified in review request
        """
        print("🧠 TESTING AREA 3: CLINICAL REASONING ENGINE")
        print("=" * 80)
        
        # Clinical reasoning test cases
        reasoning_cases = [
            {
                "name": "Clinical Reasoning - Cardiac Symptoms",
                "text": "crushing chest pain radiating to left arm with nausea and sweating",
                "expected_reasoning_elements": [
                    "differential diagnosis", "clinical assessment", "medical evaluation",
                    "cardiac", "myocardial", "angina", "emergency"
                ],
                "syndrome_detection": ["acute coronary syndrome", "cardiac emergency"]
            },
            {
                "name": "Clinical Reasoning - Neurological Symptoms",
                "text": "sudden severe headache with neck stiffness and light sensitivity",
                "expected_reasoning_elements": [
                    "neurological assessment", "meningeal signs", "intracranial pressure",
                    "emergency evaluation", "lumbar puncture"
                ],
                "syndrome_detection": ["meningitis", "subarachnoid hemorrhage"]
            },
            {
                "name": "Clinical Reasoning - Multi-System Symptoms",
                "text": "joint pain, fatigue, rash, and fever for 2 weeks",
                "expected_reasoning_elements": [
                    "systemic illness", "autoimmune", "inflammatory", "rheumatological",
                    "infectious disease", "laboratory evaluation"
                ],
                "syndrome_detection": ["systemic lupus erythematosus", "rheumatoid arthritis"]
            }
        ]
        
        for test_case in reasoning_cases:
            await self._test_clinical_reasoning(test_case)

    async def test_temporal_relationship_extraction(self):
        """
        TEST AREA 4: TEMPORAL RELATIONSHIP EXTRACTION
        Test time-based analysis as specified in review request
        """
        print("⏰ TESTING AREA 4: TEMPORAL RELATIONSHIP EXTRACTION")
        print("=" * 80)
        
        # Temporal test cases from review request
        temporal_cases = [
            {
                "name": "Temporal Pattern 1",
                "text": "headache started yesterday morning",
                "temporal_elements": ["yesterday morning", "started"],
                "expected_timeline": "acute onset",
                "duration_category": "recent"
            },
            {
                "name": "Temporal Pattern 2",
                "text": "pain comes and goes every few hours",
                "temporal_elements": ["comes and goes", "every few hours"],
                "expected_timeline": "intermittent",
                "pattern_type": "cyclical"
            },
            {
                "name": "Temporal Pattern 3",
                "text": "symptoms getting worse over time",
                "temporal_elements": ["getting worse", "over time"],
                "expected_timeline": "progressive",
                "trend": "worsening"
            },
            {
                "name": "Temporal Pattern 4",
                "text": "sudden onset of severe chest pain",
                "temporal_elements": ["sudden onset"],
                "expected_timeline": "acute",
                "urgency_modifier": "emergency"
            }
        ]
        
        for test_case in temporal_cases:
            await self._test_temporal_extraction(test_case)

    async def test_performance_validation(self):
        """
        TEST AREA 5: PERFORMANCE TESTING
        Validate performance targets as specified in review request
        """
        print("⚡ TESTING AREA 5: PERFORMANCE VALIDATION")
        print("=" * 80)
        
        # Performance test cases
        performance_cases = [
            {
                "name": "Performance Test - Simple Expression",
                "text": "I have a headache",
                "target_time_ms": 25.0
            },
            {
                "name": "Performance Test - Complex Expression",
                "text": "severe crushing chest pain radiating to left arm with shortness of breath nausea and sweating started 30 minutes ago getting worse",
                "target_time_ms": 25.0
            },
            {
                "name": "Performance Test - Multi-System Expression",
                "text": "joint pain in hands and knees with morning stiffness fatigue rash on face fever chills night sweats weight loss for 3 weeks",
                "target_time_ms": 25.0
            }
        ]
        
        processing_times = []
        
        for test_case in performance_cases:
            processing_time = await self._test_performance(test_case)
            if processing_time is not None:
                processing_times.append(processing_time)
        
        # Calculate performance statistics
        if processing_times:
            avg_time = sum(processing_times) / len(processing_times)
            max_time = max(processing_times)
            min_time = min(processing_times)
            target_met_count = sum(1 for t in processing_times if t < 25.0)
            target_met_percentage = (target_met_count / len(processing_times)) * 100
            
            self.log_test_result(
                "Performance Summary",
                target_met_percentage >= 80,  # 80% of tests should meet target
                f"Avg: {avg_time:.2f}ms, Max: {max_time:.2f}ms, Min: {min_time:.2f}ms, Target Met: {target_met_percentage:.1f}%",
                avg_time,
                {
                    "average_time_ms": avg_time,
                    "max_time_ms": max_time,
                    "min_time_ms": min_time,
                    "target_met_percentage": target_met_percentage,
                    "total_tests": len(processing_times)
                }
            )

    async def _test_multi_symptom_parsing(self, test_case: Dict[str, Any], test_category: str):
        """Test individual multi-symptom parsing scenario"""
        try:
            # Prepare request
            request_data = {
                "text": test_case["text"],
                "patient_id": "phase1-test-patient",
                "include_relationships": True,
                "include_clinical_reasoning": True,
                "context": {
                    "demographics": {"age": 35, "gender": "adult"},
                    "test_category": test_category
                }
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
                if not self._validate_response_structure(result):
                    self.log_test_result(
                        test_case["name"],
                        False,
                        "Invalid response structure",
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
                
                # Validate symptom detection
                summary = result.get("summary", {})
                total_symptoms = summary.get("total_symptoms", 0)
                
                # Check symptom count (allow some flexibility)
                expected_min = max(1, test_case["expected_count"] - 1)
                
                if total_symptoms < expected_min:
                    self.log_test_result(
                        test_case["name"],
                        False,
                        f"Insufficient symptoms detected: {total_symptoms} (expected ≥{expected_min})",
                        response_time
                    )
                    return
                
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
                
                # Success
                self.log_test_result(
                    test_case["name"],
                    True,
                    f"Successfully parsed {total_symptoms} symptoms with clinical recommendations",
                    response_time,
                    {
                        "symptoms_detected": total_symptoms,
                        "recommendations_count": len(clinical_recommendations),
                        "urgency": result.get("urgency_assessment", "unknown")
                    }
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

    async def _test_emergency_detection(self, test_case: Dict[str, Any]):
        """Test emergency combination detection"""
        try:
            request_data = {
                "text": test_case["text"],
                "patient_id": "emergency-test-patient",
                "include_relationships": True,
                "include_clinical_reasoning": True,
                "emergency_detection": True
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
                
                if not result.get("success", False):
                    self.log_test_result(
                        test_case["name"],
                        False,
                        f"Emergency parsing failed: {result.get('error', 'Unknown error')}",
                        response_time
                    )
                    return
                
                # Check urgency assessment
                urgency_assessment = result.get("urgency_assessment", "routine").lower()
                expected_urgency = [u.lower() for u in test_case.get("expected_urgency", [])]
                
                urgency_detected = any(urgency in urgency_assessment for urgency in expected_urgency)
                
                if not urgency_detected:
                    self.log_test_result(
                        test_case["name"],
                        False,
                        f"Emergency not detected. Urgency: {urgency_assessment} (expected: {expected_urgency})",
                        response_time
                    )
                    return
                
                # Check for clinical recommendations mentioning emergency
                clinical_recommendations = result.get("clinical_recommendations", [])
                emergency_mentioned = any(
                    any(keyword in rec.lower() for keyword in ["emergency", "urgent", "911", "immediate", "critical"])
                    for rec in clinical_recommendations
                )
                
                self.log_test_result(
                    test_case["name"],
                    True,
                    f"Emergency detected: {urgency_assessment}, Emergency recommendations: {emergency_mentioned}",
                    response_time,
                    {
                        "urgency_level": urgency_assessment,
                        "emergency_recommendations": emergency_mentioned,
                        "recommendations_count": len(clinical_recommendations)
                    }
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

    async def _test_clinical_reasoning(self, test_case: Dict[str, Any]):
        """Test clinical reasoning engine"""
        try:
            request_data = {
                "text": test_case["text"],
                "patient_id": "reasoning-test-patient",
                "include_relationships": True,
                "include_clinical_reasoning": True,
                "detailed_analysis": True
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
                
                if not result.get("success", False):
                    self.log_test_result(
                        test_case["name"],
                        False,
                        f"Clinical reasoning failed: {result.get('error', 'Unknown error')}",
                        response_time
                    )
                    return
                
                # Check for clinical reasoning in recommendations
                clinical_recommendations = result.get("clinical_recommendations", [])
                reasoning_content = " ".join(clinical_recommendations).lower()
                
                # Check for expected reasoning elements
                expected_elements = test_case.get("expected_reasoning_elements", [])
                elements_found = sum(1 for element in expected_elements if element.lower() in reasoning_content)
                elements_percentage = (elements_found / len(expected_elements)) * 100 if expected_elements else 0
                
                # Check for syndrome detection in multi_symptom_parse_result
                parse_result = result.get("multi_symptom_parse_result", {})
                syndrome_detection = parse_result.get("syndrome_detection", {})
                
                reasoning_quality = elements_percentage >= 30  # At least 30% of expected elements
                
                self.log_test_result(
                    test_case["name"],
                    reasoning_quality,
                    f"Clinical reasoning elements found: {elements_found}/{len(expected_elements)} ({elements_percentage:.1f}%)",
                    response_time,
                    {
                        "reasoning_elements_found": elements_found,
                        "reasoning_elements_total": len(expected_elements),
                        "reasoning_percentage": elements_percentage,
                        "syndrome_detection": bool(syndrome_detection),
                        "recommendations_count": len(clinical_recommendations)
                    }
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

    async def _test_temporal_extraction(self, test_case: Dict[str, Any]):
        """Test temporal relationship extraction"""
        try:
            request_data = {
                "text": test_case["text"],
                "patient_id": "temporal-test-patient",
                "include_relationships": True,
                "include_clinical_reasoning": True,
                "temporal_analysis": True
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
                
                if not result.get("success", False):
                    self.log_test_result(
                        test_case["name"],
                        False,
                        f"Temporal extraction failed: {result.get('error', 'Unknown error')}",
                        response_time
                    )
                    return
                
                # Check for temporal elements in parse result
                parse_result = result.get("multi_symptom_parse_result", {})
                temporal_relationships = parse_result.get("temporal_relationships", {})
                
                # Check if temporal elements are detected
                expected_temporal = test_case.get("temporal_elements", [])
                temporal_detected = bool(temporal_relationships) or any(
                    element.lower() in result.get("summary", {}).get("description", "").lower()
                    for element in expected_temporal
                )
                
                # Check clinical recommendations for temporal awareness
                clinical_recommendations = result.get("clinical_recommendations", [])
                temporal_awareness = any(
                    any(keyword in rec.lower() for keyword in ["onset", "duration", "timeline", "acute", "chronic", "sudden", "gradual"])
                    for rec in clinical_recommendations
                )
                
                temporal_success = temporal_detected or temporal_awareness
                
                self.log_test_result(
                    test_case["name"],
                    temporal_success,
                    f"Temporal analysis: detected={temporal_detected}, awareness={temporal_awareness}",
                    response_time,
                    {
                        "temporal_relationships_detected": bool(temporal_relationships),
                        "temporal_awareness_in_recommendations": temporal_awareness,
                        "expected_temporal_elements": len(expected_temporal)
                    }
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

    async def _test_performance(self, test_case: Dict[str, Any]) -> float:
        """Test performance for a specific case"""
        try:
            request_data = {
                "text": test_case["text"],
                "patient_id": "performance-test-patient",
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
            
            target_met = response_time < test_case["target_time_ms"]
            
            if response.status_code == 200:
                result = response.json()
                success = result.get("success", False) and target_met
                
                self.log_test_result(
                    test_case["name"],
                    success,
                    f"Processing time: {response_time:.2f}ms (Target: <{test_case['target_time_ms']}ms)",
                    response_time
                )
                
                return response_time
            else:
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    response_time
                )
                return response_time
                
        except Exception as e:
            self.log_test_result(
                test_case["name"],
                False,
                f"Exception: {str(e)}",
                0
            )
            return None

    def _validate_response_structure(self, result: Dict[str, Any]) -> bool:
        """Validate the response has required structure"""
        required_fields = [
            "success", "summary", "clinical_recommendations", 
            "urgency_assessment", "integration_status", "processing_performance"
        ]
        
        return all(field in result for field in required_fields)

    async def run_comprehensive_tests(self):
        """Run all Phase 1 critical fixes tests"""
        print("🎯 PHASE 1 CRITICAL FIXES COMPREHENSIVE TESTING INITIATED")
        print("=" * 80)
        print(f"Backend URL: {self.backend_url}")
        print(f"Test Start Time: {datetime.now().isoformat()}")
        print()
        
        # Run all test areas
        await self.test_multi_symptom_pattern_extraction()
        await self.test_emergency_combination_detection()
        await self.test_clinical_reasoning_engine()
        await self.test_temporal_relationship_extraction()
        await self.test_performance_validation()
        
        # Generate final report
        self.generate_final_report()

    def generate_final_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 80)
        print("🎯 PHASE 1 CRITICAL FIXES TESTING FINAL REPORT")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed Tests: {self.passed_tests}")
        print(f"   Failed Tests: {self.total_tests - self.passed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        # Performance analysis
        if self.performance_metrics:
            avg_time = sum(m["processing_time_ms"] for m in self.performance_metrics) / len(self.performance_metrics)
            target_met_count = sum(1 for m in self.performance_metrics if m["target_met"])
            target_met_percentage = (target_met_count / len(self.performance_metrics)) * 100
            
            print(f"⚡ PERFORMANCE ANALYSIS:")
            print(f"   Average Processing Time: {avg_time:.2f}ms")
            print(f"   Target (<25ms) Met: {target_met_count}/{len(self.performance_metrics)} ({target_met_percentage:.1f}%)")
            print()
        
        # Test area breakdown
        test_areas = {}
        for result in self.test_results:
            area = result["test_name"].split(" - ")[0] if " - " in result["test_name"] else "Other"
            if area not in test_areas:
                test_areas[area] = {"total": 0, "passed": 0}
            test_areas[area]["total"] += 1
            if result["success"]:
                test_areas[area]["passed"] += 1
        
        print(f"📋 TEST AREA BREAKDOWN:")
        for area, stats in test_areas.items():
            area_success_rate = (stats["passed"] / stats["total"]) * 100 if stats["total"] > 0 else 0
            status = "✅" if area_success_rate >= 80 else "⚠️" if area_success_rate >= 60 else "❌"
            print(f"   {status} {area}: {stats['passed']}/{stats['total']} ({area_success_rate:.1f}%)")
        
        print()
        
        # Critical issues
        failed_tests = [r for r in self.test_results if not r["success"]]
        if failed_tests:
            print(f"❌ CRITICAL ISSUES IDENTIFIED:")
            for test in failed_tests[:5]:  # Show top 5 failures
                print(f"   • {test['test_name']}: {test['details']}")
            if len(failed_tests) > 5:
                print(f"   ... and {len(failed_tests) - 5} more issues")
        else:
            print(f"✅ NO CRITICAL ISSUES IDENTIFIED")
        
        print()
        print(f"Test Completion Time: {datetime.now().isoformat()}")
        print("=" * 80)

async def main():
    """Main test execution"""
    tester = Phase1CriticalFixesTester()
    await tester.run_comprehensive_tests()

if __name__ == "__main__":
    asyncio.run(main())