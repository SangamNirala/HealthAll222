#!/usr/bin/env python3
"""
🎯 PHASE 1 CRITICAL FIXES COMPREHENSIVE TESTING

This test suite validates the Phase 1 medical AI multi-symptom parsing system implementation
as requested in the review. Focus on testing core functionality that was supposed to be implemented.

TESTING FOCUS AREAS:
1. Multi-Symptom Pattern Extraction - Complex multi-symptom expressions
2. Symptom Relationship Mapping - Clinical correlation analysis  
3. Clinical Reasoning Engine - Medical logic generation
4. Emergency Combination Detection - Red flag identification
5. Temporal Relationship Extraction - Time-based analysis

PERFORMANCE REQUIREMENTS:
- Processing time should be <25ms (target from specification)
- Accuracy should be >75% based on detected symptoms matching input
- Emergency detection should have 100% sensitivity for critical combinations
- All API responses should have proper JSON structure without errors

CRITICAL SUCCESS CRITERIA:
- Multi-symptom detection working (not just single symptoms)
- Emergency combinations properly detected with urgency escalation  
- Clinical relationships identified between symptoms
- Temporal patterns extracted from time expressions
- Clinical reasoning provides medical explanations
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

class Phase1MultiSymptomTester:
    """Comprehensive tester for Phase 1 Multi-Symptom Parsing System"""
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.critical_failures = []
        
    def log_test_result(self, test_name: str, success: bool, details: str, response_time: float = 0, critical: bool = False):
        """Log individual test results"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
        elif critical:
            self.critical_failures.append(test_name)
            
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "response_time_ms": response_time,
            "critical": critical,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        critical_marker = " [CRITICAL]" if critical else ""
        print(f"{status}{critical_marker} - {test_name}")
        print(f"   Details: {details}")
        if response_time > 0:
            print(f"   Response Time: {response_time:.2f}ms")
        print()

    async def run_comprehensive_tests(self):
        """Run all Phase 1 comprehensive tests"""
        print("🎯 PHASE 1 CRITICAL FIXES COMPREHENSIVE TESTING")
        print("=" * 80)
        print(f"Testing endpoint: {self.backend_url}/medical-ai/multi-symptom-parse")
        print()
        
        # Test 1: Multi-Symptom Pattern Extraction
        await self.test_multi_symptom_pattern_extraction()
        
        # Test 2: Symptom Relationship Mapping
        await self.test_symptom_relationship_mapping()
        
        # Test 3: Clinical Reasoning Engine
        await self.test_clinical_reasoning_engine()
        
        # Test 4: Emergency Combination Detection
        await self.test_emergency_combination_detection()
        
        # Test 5: Temporal Relationship Extraction
        await self.test_temporal_relationship_extraction()
        
        # Test 6: Performance Requirements
        await self.test_performance_requirements()
        
        # Generate final report
        self.generate_final_report()

    async def test_multi_symptom_pattern_extraction(self):
        """
        TEST 1: MULTI-SYMPTOM PATTERN EXTRACTION
        Test complex multi-symptom expressions from review request
        """
        print("🔍 TEST 1: MULTI-SYMPTOM PATTERN EXTRACTION")
        print("-" * 60)
        
        test_cases = [
            {
                "name": "Complex Multi-Symptom Expression 1",
                "text": "head hurts stomach upset cant sleep 3 nights",
                "expected_symptoms": ["headache", "gastrointestinal_upset", "insomnia"],
                "min_symptoms": 3,
                "critical": True
            },
            {
                "name": "Complex Multi-Symptom Expression 2", 
                "text": "chest pain and shortness of breath",
                "expected_symptoms": ["chest_pain", "dyspnea"],
                "min_symptoms": 2,
                "expected_urgency": "emergency",
                "critical": True
            },
            {
                "name": "Complex Multi-Symptom Expression 3",
                "text": "back pain fatigue dizziness fever",
                "expected_symptoms": ["back_pain", "fatigue", "dizziness", "fever"],
                "min_symptoms": 4,
                "critical": True
            },
            {
                "name": "GI Cluster Detection",
                "text": "nausea vomiting diarrhea stomach ache",
                "expected_symptoms": ["nausea", "vomiting", "diarrhea", "abdominal_pain"],
                "min_symptoms": 4,
                "critical": True
            },
            {
                "name": "Informal Language Multi-Symptom",
                "text": "my head is killing me and i feel sick to my stomach cant keep anything down",
                "expected_symptoms": ["headache", "nausea", "vomiting"],
                "min_symptoms": 3,
                "critical": False
            }
        ]
        
        for test_case in test_cases:
            await self._test_multi_symptom_extraction(test_case)

    async def _test_multi_symptom_extraction(self, test_case: Dict[str, Any]):
        """Test individual multi-symptom extraction scenario"""
        try:
            request_data = {
                "text": test_case["text"],
                "patient_id": "test-patient-phase1",
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
            
            if response.status_code != 200:
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            result = response.json()
            
            # Validate response structure
            if not result.get("success", False):
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"Parsing failed: {result.get('error', 'Unknown error')}",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            # Check multi-symptom detection
            parse_result = result.get("multi_symptom_parse_result", {})
            primary_symptoms = parse_result.get("primary_symptoms", [])
            secondary_symptoms = parse_result.get("secondary_symptoms", [])
            total_symptoms = len(primary_symptoms) + len(secondary_symptoms)
            
            min_expected = test_case.get("min_symptoms", 1)
            
            if total_symptoms < min_expected:
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"Insufficient symptoms detected: {total_symptoms} (expected ≥{min_expected}). Primary: {len(primary_symptoms)}, Secondary: {len(secondary_symptoms)}",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            # Check urgency if specified
            if "expected_urgency" in test_case:
                urgency = result.get("urgency_assessment", "routine")
                if urgency != test_case["expected_urgency"]:
                    self.log_test_result(
                        test_case["name"],
                        False,
                        f"Wrong urgency level: {urgency} (expected {test_case['expected_urgency']})",
                        response_time,
                        test_case.get("critical", False)
                    )
                    return
            
            # Success
            symptom_names = [s.get("symptom_name", "") for s in primary_symptoms + secondary_symptoms]
            self.log_test_result(
                test_case["name"],
                True,
                f"Successfully detected {total_symptoms} symptoms: {symptom_names}",
                response_time,
                test_case.get("critical", False)
            )
            
        except Exception as e:
            self.log_test_result(
                test_case["name"],
                False,
                f"Exception: {str(e)}",
                0,
                test_case.get("critical", False)
            )

    async def test_symptom_relationship_mapping(self):
        """
        TEST 2: SYMPTOM RELATIONSHIP MAPPING
        Test clinical correlation analysis
        """
        print("🔗 TEST 2: SYMPTOM RELATIONSHIP MAPPING")
        print("-" * 60)
        
        test_cases = [
            {
                "name": "Cardiac Emergency Relationship",
                "text": "chest pain with shortness of breath and sweating",
                "expected_relationships": True,
                "expected_clusters": ["cardiac_emergency"],
                "critical": True
            },
            {
                "name": "Neurological Cluster",
                "text": "severe headache neck stiffness fever",
                "expected_relationships": True,
                "expected_clusters": ["neurological_emergency"],
                "critical": True
            },
            {
                "name": "Stroke Symptoms",
                "text": "weakness facial drooping speech problems",
                "expected_relationships": True,
                "expected_clusters": ["stroke_syndrome"],
                "critical": True
            },
            {
                "name": "GI Syndrome",
                "text": "abdominal pain nausea vomiting fever",
                "expected_relationships": True,
                "expected_clusters": ["gastrointestinal"],
                "critical": False
            }
        ]
        
        for test_case in test_cases:
            await self._test_symptom_relationships(test_case)

    async def _test_symptom_relationships(self, test_case: Dict[str, Any]):
        """Test symptom relationship mapping"""
        try:
            request_data = {
                "text": test_case["text"],
                "patient_id": "test-patient-relationships",
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
            
            if response.status_code != 200:
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            result = response.json()
            
            if not result.get("success", False):
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"Parsing failed: {result.get('error', 'Unknown error')}",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            # Check symptom relationships
            parse_result = result.get("multi_symptom_parse_result", {})
            symptom_relationships = parse_result.get("symptom_relationships", {})
            
            if not symptom_relationships:
                self.log_test_result(
                    test_case["name"],
                    False,
                    "No symptom relationships found in response",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            # Check relationship confidence
            relationship_confidence = symptom_relationships.get("relationship_confidence", 0.0)
            if relationship_confidence <= 0.0:
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"No relationship confidence: {relationship_confidence}",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            # Check identified clusters
            identified_clusters = symptom_relationships.get("identified_clusters", [])
            if not identified_clusters:
                self.log_test_result(
                    test_case["name"],
                    False,
                    "No identified clusters found",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            # Success
            cluster_names = [cluster.get("cluster_name", "") for cluster in identified_clusters]
            self.log_test_result(
                test_case["name"],
                True,
                f"Relationships detected with confidence {relationship_confidence:.2f}, clusters: {cluster_names}",
                response_time,
                test_case.get("critical", False)
            )
            
        except Exception as e:
            self.log_test_result(
                test_case["name"],
                False,
                f"Exception: {str(e)}",
                0,
                test_case.get("critical", False)
            )

    async def test_clinical_reasoning_engine(self):
        """
        TEST 3: CLINICAL REASONING ENGINE
        Test medical logic generation
        """
        print("🧠 TEST 3: CLINICAL REASONING ENGINE")
        print("-" * 60)
        
        test_cases = [
            {
                "name": "Emergency Clinical Reasoning",
                "text": "crushing chest pain radiating to left arm with nausea",
                "expected_reasoning": True,
                "expected_urgency": "emergency",
                "critical": True
            },
            {
                "name": "Complex Symptom Reasoning",
                "text": "headache with visual changes and neck stiffness",
                "expected_reasoning": True,
                "expected_urgency": "urgent",
                "critical": True
            },
            {
                "name": "Multi-System Reasoning",
                "text": "fatigue shortness of breath chest pain on exertion",
                "expected_reasoning": True,
                "critical": False
            }
        ]
        
        for test_case in test_cases:
            await self._test_clinical_reasoning(test_case)

    async def _test_clinical_reasoning(self, test_case: Dict[str, Any]):
        """Test clinical reasoning generation"""
        try:
            request_data = {
                "text": test_case["text"],
                "patient_id": "test-patient-reasoning",
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
            
            if response.status_code != 200:
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            result = response.json()
            
            if not result.get("success", False):
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"Parsing failed: {result.get('error', 'Unknown error')}",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            # Check clinical reasoning
            parse_result = result.get("multi_symptom_parse_result", {})
            clinical_reasoning = parse_result.get("clinical_reasoning", {})
            
            if not clinical_reasoning:
                self.log_test_result(
                    test_case["name"],
                    False,
                    "No clinical reasoning found in response",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            # Check clinical logic
            clinical_logic = clinical_reasoning.get("clinical_logic", [])
            if not clinical_logic:
                self.log_test_result(
                    test_case["name"],
                    False,
                    "No clinical logic found",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            # Check recommended actions
            recommended_actions = clinical_reasoning.get("recommended_actions", [])
            if not recommended_actions:
                self.log_test_result(
                    test_case["name"],
                    False,
                    "No recommended actions found",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            # Check urgency if specified
            if "expected_urgency" in test_case:
                urgency = result.get("urgency_assessment", "routine")
                if urgency != test_case["expected_urgency"]:
                    self.log_test_result(
                        test_case["name"],
                        False,
                        f"Wrong urgency level: {urgency} (expected {test_case['expected_urgency']})",
                        response_time,
                        test_case.get("critical", False)
                    )
                    return
            
            # Success
            reasoning_confidence = clinical_reasoning.get("reasoning_confidence", 0.0)
            self.log_test_result(
                test_case["name"],
                True,
                f"Clinical reasoning generated with {len(clinical_logic)} logic points, {len(recommended_actions)} actions, confidence: {reasoning_confidence:.2f}",
                response_time,
                test_case.get("critical", False)
            )
            
        except Exception as e:
            self.log_test_result(
                test_case["name"],
                False,
                f"Exception: {str(e)}",
                0,
                test_case.get("critical", False)
            )

    async def test_emergency_combination_detection(self):
        """
        TEST 4: EMERGENCY COMBINATION DETECTION
        Test red flag symptom combinations
        """
        print("🚨 TEST 4: EMERGENCY COMBINATION DETECTION")
        print("-" * 60)
        
        test_cases = [
            {
                "name": "Cardiac Emergency Combination",
                "text": "chest pain shortness of breath sweating",
                "expected_urgency": "emergency",
                "critical": True
            },
            {
                "name": "Neurological Emergency",
                "text": "severe headache neck stiffness fever",
                "expected_urgency": "emergency",
                "critical": True
            },
            {
                "name": "Stroke Emergency",
                "text": "weakness facial drooping speech problems",
                "expected_urgency": "emergency",
                "critical": True
            },
            {
                "name": "Respiratory Emergency",
                "text": "severe shortness of breath chest pain cannot breathe",
                "expected_urgency": "emergency",
                "critical": True
            },
            {
                "name": "Non-Emergency Control",
                "text": "mild headache and tired",
                "expected_urgency": "routine",
                "critical": False
            }
        ]
        
        for test_case in test_cases:
            await self._test_emergency_detection(test_case)

    async def _test_emergency_detection(self, test_case: Dict[str, Any]):
        """Test emergency combination detection"""
        try:
            request_data = {
                "text": test_case["text"],
                "patient_id": "test-patient-emergency",
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
            
            if response.status_code != 200:
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            result = response.json()
            
            if not result.get("success", False):
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"Parsing failed: {result.get('error', 'Unknown error')}",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            # Check urgency assessment
            urgency_assessment = result.get("urgency_assessment", "routine")
            expected_urgency = test_case.get("expected_urgency", "routine")
            
            if urgency_assessment != expected_urgency:
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"Wrong urgency level: {urgency_assessment} (expected {expected_urgency})",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            # Check urgency indicators
            parse_result = result.get("multi_symptom_parse_result", {})
            urgency_indicators = parse_result.get("urgency_indicators", {})
            
            if expected_urgency == "emergency":
                emergency_flags = urgency_indicators.get("emergency_flags", [])
                if not emergency_flags:
                    self.log_test_result(
                        test_case["name"],
                        False,
                        "Emergency expected but no emergency flags found",
                        response_time,
                        test_case.get("critical", False)
                    )
                    return
            
            # Success
            confidence_score = urgency_indicators.get("confidence_score", 0.0)
            emergency_flags = urgency_indicators.get("emergency_flags", [])
            self.log_test_result(
                test_case["name"],
                True,
                f"Correct urgency: {urgency_assessment}, confidence: {confidence_score:.2f}, flags: {len(emergency_flags)}",
                response_time,
                test_case.get("critical", False)
            )
            
        except Exception as e:
            self.log_test_result(
                test_case["name"],
                False,
                f"Exception: {str(e)}",
                0,
                test_case.get("critical", False)
            )

    async def test_temporal_relationship_extraction(self):
        """
        TEST 5: TEMPORAL RELATIONSHIP EXTRACTION
        Test time-based analysis
        """
        print("⏰ TEST 5: TEMPORAL RELATIONSHIP EXTRACTION")
        print("-" * 60)
        
        test_cases = [
            {
                "name": "Onset Timing",
                "text": "symptoms started 3 days ago",
                "expected_temporal": True,
                "temporal_type": "onset",
                "critical": True
            },
            {
                "name": "Progression Pattern",
                "text": "getting worse over time",
                "expected_temporal": True,
                "temporal_type": "progression",
                "critical": True
            },
            {
                "name": "Frequency Pattern",
                "text": "comes and goes every few hours",
                "expected_temporal": True,
                "temporal_type": "frequency",
                "critical": True
            },
            {
                "name": "Acute Onset",
                "text": "sudden onset this morning",
                "expected_temporal": True,
                "temporal_type": "acute_onset",
                "critical": True
            },
            {
                "name": "Complex Temporal",
                "text": "headache started yesterday morning getting worse throughout the day",
                "expected_temporal": True,
                "temporal_type": "complex",
                "critical": False
            }
        ]
        
        for test_case in test_cases:
            await self._test_temporal_extraction(test_case)

    async def _test_temporal_extraction(self, test_case: Dict[str, Any]):
        """Test temporal relationship extraction"""
        try:
            request_data = {
                "text": test_case["text"],
                "patient_id": "test-patient-temporal",
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
            
            if response.status_code != 200:
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            result = response.json()
            
            if not result.get("success", False):
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"Parsing failed: {result.get('error', 'Unknown error')}",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            # Check for temporal analysis in the response
            parse_result = result.get("multi_symptom_parse_result", {})
            
            # Look for temporal analysis in various places
            temporal_found = False
            temporal_details = []
            
            # Check if there's a temporal_analysis field
            if "temporal_analysis" in parse_result:
                temporal_analysis = parse_result["temporal_analysis"]
                if temporal_analysis:
                    temporal_found = True
                    temporal_details.append(f"temporal_analysis: {temporal_analysis}")
            
            # Check primary symptoms for temporal data
            primary_symptoms = parse_result.get("primary_symptoms", [])
            for symptom in primary_symptoms:
                if "temporal_data" in symptom or "temporal_relationships" in symptom:
                    temporal_found = True
                    temporal_details.append(f"symptom temporal data found")
                    break
            
            # Check clinical reasoning for temporal mentions
            clinical_reasoning = parse_result.get("clinical_reasoning", {})
            clinical_logic = clinical_reasoning.get("clinical_logic", [])
            for logic in clinical_logic:
                if any(temporal_word in str(logic).lower() for temporal_word in ["time", "onset", "duration", "progression", "temporal"]):
                    temporal_found = True
                    temporal_details.append(f"temporal reasoning found")
                    break
            
            if not temporal_found:
                self.log_test_result(
                    test_case["name"],
                    False,
                    "No temporal analysis found in response",
                    response_time,
                    test_case.get("critical", False)
                )
                return
            
            # Success
            self.log_test_result(
                test_case["name"],
                True,
                f"Temporal analysis detected: {'; '.join(temporal_details)}",
                response_time,
                test_case.get("critical", False)
            )
            
        except Exception as e:
            self.log_test_result(
                test_case["name"],
                False,
                f"Exception: {str(e)}",
                0,
                test_case.get("critical", False)
            )

    async def test_performance_requirements(self):
        """
        TEST 6: PERFORMANCE REQUIREMENTS
        Test processing time and accuracy requirements
        """
        print("⚡ TEST 6: PERFORMANCE REQUIREMENTS")
        print("-" * 60)
        
        # Test processing time with multiple scenarios
        test_cases = [
            {
                "name": "Performance Test 1",
                "text": "chest pain shortness of breath",
                "target_time_ms": 25.0
            },
            {
                "name": "Performance Test 2", 
                "text": "headache nausea dizziness fatigue",
                "target_time_ms": 25.0
            },
            {
                "name": "Performance Test 3",
                "text": "severe abdominal pain with vomiting and fever started yesterday",
                "target_time_ms": 25.0
            }
        ]
        
        total_times = []
        
        for test_case in test_cases:
            processing_time = await self._test_performance(test_case)
            if processing_time is not None:
                total_times.append(processing_time)
        
        # Calculate average performance
        if total_times:
            avg_time = sum(total_times) / len(total_times)
            target_met = avg_time < 25.0
            
            self.log_test_result(
                "Average Performance",
                target_met,
                f"Average processing time: {avg_time:.2f}ms (target: <25ms)",
                avg_time,
                True
            )

    async def _test_performance(self, test_case: Dict[str, Any]) -> float:
        """Test individual performance scenario"""
        try:
            request_data = {
                "text": test_case["text"],
                "patient_id": "test-patient-performance",
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
                
                # Check if processing performance is reported
                processing_performance = result.get("processing_performance", {})
                reported_time = processing_performance.get("processing_time_ms", response_time)
                
                target_met = reported_time < test_case["target_time_ms"]
                
                self.log_test_result(
                    test_case["name"],
                    target_met,
                    f"Processing time: {reported_time:.2f}ms (target: <{test_case['target_time_ms']}ms)",
                    reported_time,
                    False
                )
                
                return reported_time
            else:
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response_time,
                    False
                )
                return None
                
        except Exception as e:
            self.log_test_result(
                test_case["name"],
                False,
                f"Exception: {str(e)}",
                0,
                False
            )
            return None

    def generate_final_report(self):
        """Generate comprehensive final report"""
        print("\n" + "=" * 80)
        print("🎯 PHASE 1 CRITICAL FIXES COMPREHENSIVE TESTING REPORT")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed: {self.passed_tests}")
        print(f"   Failed: {self.total_tests - self.passed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        # Critical failures
        if self.critical_failures:
            print(f"❌ CRITICAL FAILURES ({len(self.critical_failures)}):")
            for failure in self.critical_failures:
                print(f"   - {failure}")
            print()
        
        # Test category breakdown
        categories = {
            "Multi-Symptom Pattern Extraction": [],
            "Symptom Relationship Mapping": [],
            "Clinical Reasoning Engine": [],
            "Emergency Combination Detection": [],
            "Temporal Relationship Extraction": [],
            "Performance Requirements": []
        }
        
        for result in self.test_results:
            test_name = result["test_name"]
            if "Multi-Symptom" in test_name or "Complex" in test_name or "GI Cluster" in test_name:
                categories["Multi-Symptom Pattern Extraction"].append(result)
            elif "Relationship" in test_name or "Cardiac Emergency" in test_name or "Neurological Cluster" in test_name:
                categories["Symptom Relationship Mapping"].append(result)
            elif "Reasoning" in test_name:
                categories["Clinical Reasoning Engine"].append(result)
            elif "Emergency" in test_name or "Stroke" in test_name:
                categories["Emergency Combination Detection"].append(result)
            elif "Temporal" in test_name or "Onset" in test_name or "Progression" in test_name:
                categories["Temporal Relationship Extraction"].append(result)
            elif "Performance" in test_name:
                categories["Performance Requirements"].append(result)
        
        print("📋 CATEGORY BREAKDOWN:")
        for category, results in categories.items():
            if results:
                passed = sum(1 for r in results if r["success"])
                total = len(results)
                rate = (passed / total * 100) if total > 0 else 0
                status = "✅" if rate >= 75 else "⚠️" if rate >= 50 else "❌"
                print(f"   {status} {category}: {passed}/{total} ({rate:.1f}%)")
        print()
        
        # Performance summary
        performance_results = [r for r in self.test_results if "Performance" in r["test_name"]]
        if performance_results:
            avg_time = sum(r["response_time_ms"] for r in performance_results) / len(performance_results)
            print(f"⚡ PERFORMANCE SUMMARY:")
            print(f"   Average Response Time: {avg_time:.2f}ms")
            print(f"   Target: <25ms")
            print(f"   Performance Target Met: {'✅ YES' if avg_time < 25 else '❌ NO'}")
            print()
        
        # Final assessment
        print("🎯 PHASE 1 ASSESSMENT:")
        if success_rate >= 75 and len(self.critical_failures) == 0:
            print("   ✅ PHASE 1 IMPLEMENTATION SUCCESSFUL")
            print("   Multi-symptom parsing system is working correctly")
        elif success_rate >= 50:
            print("   ⚠️ PHASE 1 PARTIALLY WORKING")
            print("   Some core functionality implemented but issues remain")
        else:
            print("   ❌ PHASE 1 IMPLEMENTATION FAILED")
            print("   Core multi-symptom parsing functionality not working")
        
        print("\n" + "=" * 80)

async def main():
    """Main test execution"""
    tester = Phase1MultiSymptomTester()
    await tester.run_comprehensive_tests()

if __name__ == "__main__":
    asyncio.run(main())