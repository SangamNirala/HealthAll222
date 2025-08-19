#!/usr/bin/env python3
"""
PHASE 4 COMPREHENSIVE MEDICAL PATTERN RECOGNITION ENGINE API TESTING
===================================================================

Comprehensive testing suite for the Phase 4 Comprehensive Medical Pattern Recognition Engine
via the Medical AI API endpoints. Tests the most advanced medical AI system ever created.

Testing Focus:
- Ultra-challenging scenario testing (100% success required)
- Medical AI API integration testing
- Performance requirements validation
- Syndrome detection validation
- Emergency detection testing
"""

import asyncio
import json
import time
import requests
import sys
from datetime import datetime
from typing import Dict, Any, List

# Backend URL from environment
BACKEND_URL = "https://symptom-tracker-3.preview.emergentagent.com/api"

class Phase4MedicalAPITester:
    """
    🚀 PHASE 4 COMPREHENSIVE MEDICAL PATTERN RECOGNITION ENGINE API TESTER 🚀
    
    Advanced testing suite for validating the revolutionary Phase 4 medical AI system
    via API endpoints with ultra-challenging scenarios and performance requirements.
    """
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.test_results = []
        self.performance_metrics = []
        
        print("🚀 PHASE 4 COMPREHENSIVE MEDICAL PATTERN RECOGNITION ENGINE API TESTER INITIALIZED")
        print("=" * 80)
        
    async def run_comprehensive_tests(self):
        """Run all comprehensive Phase 4 API tests"""
        
        print("\n🎯 STARTING PHASE 4 COMPREHENSIVE API TESTING SUITE")
        print("=" * 80)
        
        # Test 1: Ultra-Challenging Scenario Testing (MUST achieve 100% success)
        await self.test_ultra_challenging_scenarios()
        
        # Test 2: Performance Requirements Validation
        await self.test_performance_requirements()
        
        # Test 3: Medical AI Service Integration
        await self.test_medical_ai_integration()
        
        # Test 4: Syndrome Detection Engine via API
        await self.test_syndrome_detection_via_api()
        
        # Test 5: Emergency Detection Testing
        await self.test_emergency_detection()
        
        # Generate comprehensive test report
        self.generate_comprehensive_report()
        
    async def test_ultra_challenging_scenarios(self):
        """
        🔥 ULTRA-CHALLENGING SCENARIO TESTING (Must achieve 100% success)
        
        Tests the two ultra-challenging scenarios provided in the review request
        with detailed validation of expected results via Medical AI API.
        """
        
        print("\n🔥 ULTRA-CHALLENGING SCENARIO TESTING")
        print("-" * 50)
        
        # SCENARIO 1: Comprehensive Pattern Mastery
        scenario_1_input = """Sharp stabbing pain in my left upper chest that started suddenly this morning after lifting heavy boxes at work, getting progressively worse with deep breathing and movement, radiating down my left arm to my fingers with tingling, accompanied by mild nausea and cold sweats, comes in waves every 2-3 minutes lasting about 30 seconds each, completely disappears when I sit perfectly still and breathe shallow"""
        
        print("🎯 SCENARIO 1: Comprehensive Pattern Mastery")
        print(f"Input: {scenario_1_input[:100]}...")
        
        # Test via Medical AI API
        scenario_1_results = await self.test_scenario_via_api("scenario-1", scenario_1_input, {
            "expected_urgency": "emergency",
            "expected_emergency": True,
            "expected_patterns": ["chest pain", "radiation", "work-related", "positional"],
            "min_response_length": 200,
            "should_mention": ["emergency", "cardiac", "chest", "arm"]
        })
        
        self.test_results.append({
            "test": "Ultra-Challenging Scenario 1",
            "status": "PASS" if scenario_1_results["success"] else "FAIL",
            "details": scenario_1_results
        })
        
        # SCENARIO 2: Complex Multi-System Analysis
        scenario_2_input = """For the past month I've been getting these absolutely terrible headaches on the right side of my head, usually starting behind my right eye, throbbing and pulsating like my heart is beating in my head, typically triggered by fluorescent lights at work or when my kids are being loud, almost always accompanied by severe nausea and sensitivity to light and sound, sometimes progressing to vomiting, lasting anywhere from 4-12 hours, happening about 2-3 times per week usually in the late afternoon, completely debilitating - I have to lie in a dark quiet room and can't function at all"""
        
        print("🎯 SCENARIO 2: Complex Multi-System Analysis")
        print(f"Input: {scenario_2_input[:100]}...")
        
        # Test via Medical AI API
        scenario_2_results = await self.test_scenario_via_api("scenario-2", scenario_2_input, {
            "expected_urgency": "urgent",
            "expected_emergency": False,
            "expected_patterns": ["headache", "triggers", "temporal", "functional impact"],
            "min_response_length": 200,
            "should_mention": ["migraine", "headache", "light", "triggers"]
        })
        
        self.test_results.append({
            "test": "Ultra-Challenging Scenario 2", 
            "status": "PASS" if scenario_2_results["success"] else "FAIL",
            "details": scenario_2_results
        })
        
    async def test_scenario_via_api(self, scenario_id: str, input_text: str, validation_criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Test a scenario via Medical AI API with comprehensive validation"""
        
        results = {
            "success": True,
            "findings": [],
            "missing_elements": [],
            "api_metrics": {},
            "response_analysis": {}
        }
        
        try:
            # Initialize consultation
            start_time = time.time()
            init_response = requests.post(f"{self.backend_url}/medical-ai/initialize", 
                json={"patient_id": f"test-{scenario_id}", "timestamp": datetime.now().isoformat()},
                timeout=30)
            
            if init_response.status_code == 200:
                init_data = init_response.json()
                consultation_id = init_data.get("consultation_id")
                
                # Send scenario message
                message_start = time.time()
                message_response = requests.post(f"{self.backend_url}/medical-ai/message",
                    json={
                        "consultation_id": consultation_id,
                        "message": input_text,
                        "timestamp": datetime.now().isoformat()
                    },
                    timeout=30)
                
                processing_time = (time.time() - message_start) * 1000  # Convert to milliseconds
                total_time = (time.time() - start_time) * 1000
                
                if message_response.status_code == 200:
                    response_data = message_response.json()
                    
                    # Record API metrics
                    results["api_metrics"] = {
                        "processing_time_ms": processing_time,
                        "total_time_ms": total_time,
                        "meets_40ms_target": processing_time < 40,
                        "status_code": message_response.status_code
                    }
                    
                    # Validate response structure
                    required_fields = ["response", "urgency", "consultation_id", "current_stage"]
                    for field in required_fields:
                        if field in response_data:
                            results["findings"].append(f"✅ Required field '{field}' present")
                        else:
                            results["missing_elements"].append(f"❌ Required field '{field}' missing")
                            results["success"] = False
                    
                    # Validate urgency level
                    actual_urgency = response_data.get("urgency", "routine")
                    expected_urgency = validation_criteria.get("expected_urgency", "routine")
                    if actual_urgency == expected_urgency:
                        results["findings"].append(f"✅ Urgency level correct: {actual_urgency}")
                    else:
                        results["missing_elements"].append(f"❌ Urgency mismatch: got {actual_urgency}, expected {expected_urgency}")
                        results["success"] = False
                    
                    # Validate emergency detection
                    actual_emergency = response_data.get("emergency_detected", False)
                    expected_emergency = validation_criteria.get("expected_emergency", False)
                    if actual_emergency == expected_emergency:
                        results["findings"].append(f"✅ Emergency detection correct: {actual_emergency}")
                    else:
                        results["missing_elements"].append(f"❌ Emergency detection mismatch: got {actual_emergency}, expected {expected_emergency}")
                        results["success"] = False
                    
                    # Validate response quality
                    response_text = response_data.get("response", "")
                    min_length = validation_criteria.get("min_response_length", 100)
                    if len(response_text) >= min_length:
                        results["findings"].append(f"✅ Response quality adequate: {len(response_text)} chars")
                    else:
                        results["missing_elements"].append(f"❌ Response too short: {len(response_text)} chars (min {min_length})")
                        results["success"] = False
                    
                    # Check for expected mentions
                    should_mention = validation_criteria.get("should_mention", [])
                    response_lower = response_text.lower()
                    for term in should_mention:
                        if term.lower() in response_lower:
                            results["findings"].append(f"✅ Expected term '{term}' found in response")
                        else:
                            results["missing_elements"].append(f"❌ Expected term '{term}' not found in response")
                            results["success"] = False
                    
                    # Analyze response structure
                    results["response_analysis"] = {
                        "response_length": len(response_text),
                        "has_recommendations": len(response_data.get("recommendations", [])) > 0,
                        "has_differential": len(response_data.get("differential_diagnoses", [])) > 0,
                        "has_context": "context" in response_data,
                        "urgency_level": actual_urgency,
                        "emergency_detected": actual_emergency
                    }
                    
                else:
                    results["success"] = False
                    results["missing_elements"].append(f"❌ Message API failed: {message_response.status_code}")
                    
            else:
                results["success"] = False
                results["missing_elements"].append(f"❌ Init API failed: {init_response.status_code}")
                
        except Exception as e:
            results["success"] = False
            results["missing_elements"].append(f"❌ API test exception: {str(e)}")
        
        return results
    
    async def test_performance_requirements(self):
        """
        🚀 PERFORMANCE REQUIREMENTS VALIDATION
        
        Tests:
        - Processing Speed: <40ms per analysis (via API response times)
        - Response Quality: Comprehensive medical responses
        - API Reliability: Consistent successful responses
        """
        
        print("\n🚀 PERFORMANCE REQUIREMENTS VALIDATION")
        print("-" * 50)
        
        # Test multiple inputs for performance consistency
        test_inputs = [
            "Severe crushing chest pain with shortness of breath and nausea",
            "Throbbing headache with light sensitivity and nausea for 6 hours",
            "Sharp abdominal pain in right lower quadrant with fever and vomiting",
            "Sudden weakness on left side with facial drooping and speech difficulty",
            "Burning chest pain after meals with acid taste in mouth"
        ]
        
        performance_results = []
        
        for i, test_input in enumerate(test_inputs, 1):
            print(f"🔬 Performance Test {i}: {test_input[:50]}...")
            
            try:
                # Initialize consultation
                init_response = requests.post(f"{self.backend_url}/medical-ai/initialize", 
                    json={"patient_id": f"perf-test-{i}", "timestamp": datetime.now().isoformat()},
                    timeout=30)
                
                if init_response.status_code == 200:
                    init_data = init_response.json()
                    consultation_id = init_data.get("consultation_id")
                    
                    # Measure processing time
                    start_time = time.time()
                    message_response = requests.post(f"{self.backend_url}/medical-ai/message",
                        json={
                            "consultation_id": consultation_id,
                            "message": test_input,
                            "timestamp": datetime.now().isoformat()
                        },
                        timeout=30)
                    
                    processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                    
                    if message_response.status_code == 200:
                        response_data = message_response.json()
                        
                        # Analyze performance metrics
                        performance_metrics = {
                            "test_number": i,
                            "input_length": len(test_input),
                            "processing_time_ms": processing_time,
                            "meets_40ms_target": processing_time < 40,
                            "response_length": len(response_data.get("response", "")),
                            "has_urgency": "urgency" in response_data,
                            "has_recommendations": len(response_data.get("recommendations", [])) > 0,
                            "api_success": True
                        }
                        
                        performance_results.append(performance_metrics)
                        
                        # Print immediate results
                        status = "✅ PASS" if performance_metrics["meets_40ms_target"] and performance_metrics["api_success"] else "❌ FAIL"
                        print(f"   {status} - Time: {processing_time:.1f}ms, Response: {performance_metrics['response_length']} chars")
                    else:
                        print(f"   ❌ FAIL - Message API error: {message_response.status_code}")
                else:
                    print(f"   ❌ FAIL - Init API error: {init_response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ FAIL - Exception: {str(e)}")
        
        # Calculate aggregate performance metrics
        if performance_results:
            avg_processing_time = sum(r["processing_time_ms"] for r in performance_results) / len(performance_results)
            avg_response_length = sum(r["response_length"] for r in performance_results) / len(performance_results)
            performance_pass_rate = sum(1 for r in performance_results if r["meets_40ms_target"] and r["api_success"]) / len(performance_results)
            
            aggregate_results = {
                "average_processing_time_ms": avg_processing_time,
                "meets_avg_40ms_target": avg_processing_time < 40,
                "average_response_length": avg_response_length,
                "performance_pass_rate": performance_pass_rate,
                "meets_consistency_target": performance_pass_rate >= 0.8,  # 80% success rate
                "individual_results": performance_results
            }
            
            self.test_results.append({
                "test": "Performance Requirements Validation",
                "status": "PASS" if aggregate_results["meets_avg_40ms_target"] and aggregate_results["meets_consistency_target"] else "FAIL",
                "details": aggregate_results
            })
            
            print(f"\n📊 PERFORMANCE SUMMARY:")
            print(f"   Average Processing Time: {avg_processing_time:.1f}ms (Target: <40ms)")
            print(f"   Average Response Length: {avg_response_length:.0f} characters")
            print(f"   Performance Pass Rate: {performance_pass_rate*100:.1f}% (Target: >80%)")
        else:
            self.test_results.append({
                "test": "Performance Requirements Validation",
                "status": "FAIL",
                "details": {"error": "No successful performance tests"}
            })
    
    async def test_medical_ai_integration(self):
        """
        🏥 MEDICAL AI SERVICE INTEGRATION TESTING
        
        Tests Phase 4 integration with Medical AI endpoints:
        - POST /api/medical-ai/initialize
        - POST /api/medical-ai/message (with Phase 4 entity extraction)
        - Verify enhanced response structures
        - Test medical reasoning and recommendations
        """
        
        print("\n🏥 MEDICAL AI SERVICE INTEGRATION TESTING")
        print("-" * 50)
        
        integration_tests = [
            {
                "name": "Basic Medical Consultation",
                "input": "I have a headache and feel nauseous",
                "expected_fields": ["response", "urgency", "recommendations"],
                "min_response_length": 50
            },
            {
                "name": "Complex Symptom Analysis",
                "input": "Severe chest pain radiating to left arm with shortness of breath and sweating",
                "expected_fields": ["response", "urgency", "emergency_detected", "recommendations"],
                "expected_urgency": "emergency",
                "min_response_length": 100
            },
            {
                "name": "Multi-symptom Integration",
                "input": "Right lower abdominal pain with fever, nausea, and vomiting for 6 hours",
                "expected_fields": ["response", "urgency", "differential_diagnoses"],
                "expected_urgency": "urgent",
                "min_response_length": 100
            }
        ]
        
        for test_case in integration_tests:
            print(f"🔬 {test_case['name']}: {test_case['input'][:50]}...")
            
            try:
                # Initialize consultation
                init_response = requests.post(f"{self.backend_url}/medical-ai/initialize", 
                    json={"patient_id": f"integration-{test_case['name'].lower().replace(' ', '-')}", 
                          "timestamp": datetime.now().isoformat()},
                    timeout=30)
                
                if init_response.status_code == 200:
                    init_data = init_response.json()
                    consultation_id = init_data.get("consultation_id")
                    
                    # Send test message
                    message_response = requests.post(f"{self.backend_url}/medical-ai/message",
                        json={
                            "consultation_id": consultation_id,
                            "message": test_case["input"],
                            "timestamp": datetime.now().isoformat()
                        },
                        timeout=30)
                    
                    if message_response.status_code == 200:
                        response_data = message_response.json()
                        
                        # Validate integration results
                        integration_results = {
                            "api_success": True,
                            "has_required_fields": True,
                            "response_quality": True,
                            "urgency_correct": True,
                            "field_analysis": {}
                        }
                        
                        # Check required fields
                        for field in test_case["expected_fields"]:
                            if field in response_data:
                                integration_results["field_analysis"][field] = "✅ Present"
                            else:
                                integration_results["field_analysis"][field] = "❌ Missing"
                                integration_results["has_required_fields"] = False
                        
                        # Check response quality
                        response_length = len(response_data.get("response", ""))
                        min_length = test_case.get("min_response_length", 50)
                        if response_length < min_length:
                            integration_results["response_quality"] = False
                        
                        # Check urgency if specified
                        if "expected_urgency" in test_case:
                            actual_urgency = response_data.get("urgency", "routine")
                            if actual_urgency != test_case["expected_urgency"]:
                                integration_results["urgency_correct"] = False
                        
                        integration_results["response_length"] = response_length
                        integration_results["actual_urgency"] = response_data.get("urgency", "routine")
                        
                        success = all([
                            integration_results["api_success"],
                            integration_results["has_required_fields"],
                            integration_results["response_quality"],
                            integration_results["urgency_correct"]
                        ])
                        
                        self.test_results.append({
                            "test": f"Medical AI Integration - {test_case['name']}",
                            "status": "PASS" if success else "FAIL",
                            "details": integration_results
                        })
                        
                        status = "✅ PASS" if success else "❌ FAIL"
                        print(f"   {status} - Urgency: {response_data.get('urgency')}, Length: {response_length} chars")
                        
                    else:
                        print(f"   ❌ FAIL - Message API error: {message_response.status_code}")
                        self.test_results.append({
                            "test": f"Medical AI Integration - {test_case['name']}",
                            "status": "FAIL",
                            "details": {"error": f"Message API error: {message_response.status_code}"}
                        })
                else:
                    print(f"   ❌ FAIL - Init API error: {init_response.status_code}")
                    self.test_results.append({
                        "test": f"Medical AI Integration - {test_case['name']}",
                        "status": "FAIL", 
                        "details": {"error": f"Init API error: {init_response.status_code}"}
                    })
                    
            except Exception as e:
                print(f"   ❌ FAIL - Exception: {str(e)}")
                self.test_results.append({
                    "test": f"Medical AI Integration - {test_case['name']}",
                    "status": "FAIL",
                    "details": {"error": str(e)}
                })
    
    async def test_syndrome_detection_via_api(self):
        """
        🔬 SYNDROME DETECTION ENGINE TESTING VIA API
        
        Tests advanced syndrome recognition through API responses:
        - Acute coronary syndrome detection
        - Migraine syndrome identification  
        - Acute abdomen pattern recognition
        - Stroke syndrome analysis
        """
        
        print("\n🔬 SYNDROME DETECTION ENGINE TESTING VIA API")
        print("-" * 50)
        
        syndrome_test_cases = [
            {
                "name": "Acute Coronary Syndrome",
                "input": "Crushing substernal chest pain radiating to left arm with shortness of breath, nausea, and sweating",
                "expected_urgency": "emergency",
                "expected_mentions": ["cardiac", "heart", "emergency", "911"],
                "syndrome_indicators": ["chest pain", "radiation", "associated symptoms"]
            },
            {
                "name": "Migraine Syndrome",
                "input": "Severe unilateral throbbing headache with nausea, photophobia, phonophobia, and visual aura lasting 6 hours",
                "expected_urgency": "urgent",
                "expected_mentions": ["migraine", "headache", "light sensitivity"],
                "syndrome_indicators": ["unilateral", "throbbing", "nausea", "photophobia"]
            },
            {
                "name": "Acute Abdomen",
                "input": "Severe constant right lower quadrant abdominal pain with fever, vomiting, and rebound tenderness",
                "expected_urgency": "emergency",
                "expected_mentions": ["appendicitis", "emergency", "surgical"],
                "syndrome_indicators": ["right lower quadrant", "fever", "rebound tenderness"]
            },
            {
                "name": "Stroke Syndrome",
                "input": "Sudden onset left-sided weakness with facial drooping and speech difficulty",
                "expected_urgency": "emergency",
                "expected_mentions": ["stroke", "emergency", "911", "immediate"],
                "syndrome_indicators": ["sudden onset", "weakness", "facial drooping", "speech"]
            }
        ]
        
        for test_case in syndrome_test_cases:
            print(f"🔬 {test_case['name']}: {test_case['input'][:60]}...")
            
            try:
                # Initialize consultation
                init_response = requests.post(f"{self.backend_url}/medical-ai/initialize", 
                    json={"patient_id": f"syndrome-{test_case['name'].lower().replace(' ', '-')}", 
                          "timestamp": datetime.now().isoformat()},
                    timeout=30)
                
                if init_response.status_code == 200:
                    init_data = init_response.json()
                    consultation_id = init_data.get("consultation_id")
                    
                    # Send test message
                    message_response = requests.post(f"{self.backend_url}/medical-ai/message",
                        json={
                            "consultation_id": consultation_id,
                            "message": test_case["input"],
                            "timestamp": datetime.now().isoformat()
                        },
                        timeout=30)
                    
                    if message_response.status_code == 200:
                        response_data = message_response.json()
                        
                        # Analyze syndrome detection
                        syndrome_results = {
                            "urgency_correct": response_data.get("urgency") == test_case["expected_urgency"],
                            "mentions_found": 0,
                            "indicators_found": 0,
                            "response_analysis": {},
                            "success": True
                        }
                        
                        response_text = response_data.get("response", "").lower()
                        
                        # Check for expected mentions
                        for mention in test_case["expected_mentions"]:
                            if mention.lower() in response_text:
                                syndrome_results["mentions_found"] += 1
                        
                        # Check for syndrome indicators
                        for indicator in test_case["syndrome_indicators"]:
                            if indicator.lower() in response_text:
                                syndrome_results["indicators_found"] += 1
                        
                        # Calculate success metrics
                        mention_rate = syndrome_results["mentions_found"] / len(test_case["expected_mentions"])
                        indicator_rate = syndrome_results["indicators_found"] / len(test_case["syndrome_indicators"])
                        
                        syndrome_results["mention_rate"] = mention_rate
                        syndrome_results["indicator_rate"] = indicator_rate
                        syndrome_results["detected_urgency"] = response_data.get("urgency", "routine")
                        syndrome_results["emergency_detected"] = response_data.get("emergency_detected", False)
                        
                        # Overall success criteria
                        syndrome_results["success"] = (
                            syndrome_results["urgency_correct"] and
                            mention_rate >= 0.5 and  # At least 50% of expected mentions
                            indicator_rate >= 0.5    # At least 50% of syndrome indicators
                        )
                        
                        self.test_results.append({
                            "test": f"Syndrome Detection - {test_case['name']}",
                            "status": "PASS" if syndrome_results["success"] else "FAIL",
                            "details": syndrome_results
                        })
                        
                        status = "✅ PASS" if syndrome_results["success"] else "❌ FAIL"
                        print(f"   {status} - Urgency: {syndrome_results['detected_urgency']}, Mentions: {syndrome_results['mentions_found']}/{len(test_case['expected_mentions'])}")
                        
                    else:
                        print(f"   ❌ FAIL - Message API error: {message_response.status_code}")
                        self.test_results.append({
                            "test": f"Syndrome Detection - {test_case['name']}",
                            "status": "FAIL",
                            "details": {"error": f"Message API error: {message_response.status_code}"}
                        })
                else:
                    print(f"   ❌ FAIL - Init API error: {init_response.status_code}")
                    self.test_results.append({
                        "test": f"Syndrome Detection - {test_case['name']}",
                        "status": "FAIL",
                        "details": {"error": f"Init API error: {init_response.status_code}"}
                    })
                    
            except Exception as e:
                print(f"   ❌ FAIL - Exception: {str(e)}")
                self.test_results.append({
                    "test": f"Syndrome Detection - {test_case['name']}",
                    "status": "FAIL",
                    "details": {"error": str(e)}
                })
    
    async def test_emergency_detection(self):
        """
        🚨 EMERGENCY DETECTION TESTING
        
        Tests emergency detection capabilities with various critical scenarios
        """
        
        print("\n🚨 EMERGENCY DETECTION TESTING")
        print("-" * 50)
        
        emergency_test_cases = [
            {
                "name": "Cardiac Emergency",
                "input": "Severe crushing chest pain with shortness of breath and cold sweats",
                "expected_emergency": True,
                "expected_urgency": "emergency"
            },
            {
                "name": "Stroke Emergency",
                "input": "Sudden weakness on right side with facial drooping and slurred speech",
                "expected_emergency": True,
                "expected_urgency": "emergency"
            },
            {
                "name": "Severe Allergic Reaction",
                "input": "Throat swelling and difficulty breathing after eating peanuts",
                "expected_emergency": True,
                "expected_urgency": "emergency"
            },
            {
                "name": "Non-Emergency Symptom",
                "input": "Mild headache for the past hour",
                "expected_emergency": False,
                "expected_urgency": "routine"
            }
        ]
        
        for test_case in emergency_test_cases:
            print(f"🚨 {test_case['name']}: {test_case['input'][:50]}...")
            
            try:
                # Initialize consultation
                init_response = requests.post(f"{self.backend_url}/medical-ai/initialize", 
                    json={"patient_id": f"emergency-{test_case['name'].lower().replace(' ', '-')}", 
                          "timestamp": datetime.now().isoformat()},
                    timeout=30)
                
                if init_response.status_code == 200:
                    init_data = init_response.json()
                    consultation_id = init_data.get("consultation_id")
                    
                    # Send test message
                    message_response = requests.post(f"{self.backend_url}/medical-ai/message",
                        json={
                            "consultation_id": consultation_id,
                            "message": test_case["input"],
                            "timestamp": datetime.now().isoformat()
                        },
                        timeout=30)
                    
                    if message_response.status_code == 200:
                        response_data = message_response.json()
                        
                        # Validate emergency detection
                        emergency_results = {
                            "emergency_correct": response_data.get("emergency_detected", False) == test_case["expected_emergency"],
                            "urgency_correct": response_data.get("urgency") == test_case["expected_urgency"],
                            "detected_emergency": response_data.get("emergency_detected", False),
                            "detected_urgency": response_data.get("urgency", "routine"),
                            "has_911_recommendation": False,
                            "response_appropriate": True
                        }
                        
                        # Check for 911 recommendation in emergency cases
                        response_text = response_data.get("response", "").lower()
                        if test_case["expected_emergency"]:
                            emergency_results["has_911_recommendation"] = "911" in response_text or "emergency" in response_text
                        
                        emergency_results["success"] = (
                            emergency_results["emergency_correct"] and
                            emergency_results["urgency_correct"] and
                            (not test_case["expected_emergency"] or emergency_results["has_911_recommendation"])
                        )
                        
                        self.test_results.append({
                            "test": f"Emergency Detection - {test_case['name']}",
                            "status": "PASS" if emergency_results["success"] else "FAIL",
                            "details": emergency_results
                        })
                        
                        status = "✅ PASS" if emergency_results["success"] else "❌ FAIL"
                        print(f"   {status} - Emergency: {emergency_results['detected_emergency']}, Urgency: {emergency_results['detected_urgency']}")
                        
                    else:
                        print(f"   ❌ FAIL - Message API error: {message_response.status_code}")
                        self.test_results.append({
                            "test": f"Emergency Detection - {test_case['name']}",
                            "status": "FAIL",
                            "details": {"error": f"Message API error: {message_response.status_code}"}
                        })
                else:
                    print(f"   ❌ FAIL - Init API error: {init_response.status_code}")
                    self.test_results.append({
                        "test": f"Emergency Detection - {test_case['name']}",
                        "status": "FAIL",
                        "details": {"error": f"Init API error: {init_response.status_code}"}
                    })
                    
            except Exception as e:
                print(f"   ❌ FAIL - Exception: {str(e)}")
                self.test_results.append({
                    "test": f"Emergency Detection - {test_case['name']}",
                    "status": "FAIL",
                    "details": {"error": str(e)}
                })
    
    def generate_comprehensive_report(self):
        """Generate comprehensive test report with all results and metrics"""
        
        print("\n" + "=" * 80)
        print("🏆 PHASE 4 COMPREHENSIVE MEDICAL PATTERN RECOGNITION ENGINE API TEST REPORT")
        print("=" * 80)
        
        # Calculate overall statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["status"] == "PASS")
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\n📊 OVERALL TEST RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {failed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        # Categorize results
        categories = {
            "Ultra-Challenging Scenarios": [],
            "Performance Requirements": [],
            "Medical AI Integration": [],
            "Syndrome Detection": [],
            "Emergency Detection": []
        }
        
        for result in self.test_results:
            test_name = result["test"]
            if "Ultra-Challenging Scenario" in test_name:
                categories["Ultra-Challenging Scenarios"].append(result)
            elif "Performance Requirements" in test_name:
                categories["Performance Requirements"].append(result)
            elif "Medical AI Integration" in test_name:
                categories["Medical AI Integration"].append(result)
            elif "Syndrome Detection" in test_name:
                categories["Syndrome Detection"].append(result)
            elif "Emergency Detection" in test_name:
                categories["Emergency Detection"].append(result)
        
        # Print detailed results by category
        for category, results in categories.items():
            if results:
                print(f"\n🔍 {category.upper()}:")
                category_passed = sum(1 for r in results if r["status"] == "PASS")
                category_total = len(results)
                category_rate = (category_passed / category_total) * 100 if category_total > 0 else 0
                print(f"   Success Rate: {category_rate:.1f}% ({category_passed}/{category_total})")
                
                for result in results:
                    status_icon = "✅" if result["status"] == "PASS" else "❌"
                    print(f"   {status_icon} {result['test']}")
                    
                    # Print key details for failed tests
                    if result["status"] == "FAIL" and "details" in result:
                        details = result["details"]
                        if isinstance(details, dict):
                            if "missing_elements" in details and details["missing_elements"]:
                                print(f"      Issues: {', '.join(details['missing_elements'][:2])}")
                            if "error" in details:
                                print(f"      Error: {details['error']}")
        
        # Performance summary
        performance_tests = [r for r in self.test_results if "Performance" in r["test"]]
        if performance_tests:
            print(f"\n⚡ PERFORMANCE SUMMARY:")
            for result in performance_tests:
                if "details" in result and isinstance(result["details"], dict):
                    details = result["details"]
                    if "average_processing_time_ms" in details:
                        print(f"   Average Processing Time: {details['average_processing_time_ms']:.1f}ms (Target: <40ms)")
                    if "performance_pass_rate" in details:
                        print(f"   Performance Pass Rate: {details['performance_pass_rate']*100:.1f}% (Target: >80%)")
        
        # Critical findings
        critical_failures = []
        ultra_challenging_failed = any(r["status"] == "FAIL" for r in categories["Ultra-Challenging Scenarios"])
        performance_failed = any(r["status"] == "FAIL" for r in categories["Performance Requirements"])
        
        if ultra_challenging_failed:
            critical_failures.append("❌ CRITICAL: Ultra-challenging scenarios failed (100% success required)")
        if performance_failed:
            critical_failures.append("❌ CRITICAL: Performance requirements not met")
        
        if critical_failures:
            print(f"\n🚨 CRITICAL FAILURES:")
            for failure in critical_failures:
                print(f"   {failure}")
        
        # Final assessment
        print(f"\n🏆 FINAL ASSESSMENT:")
        if success_rate >= 90 and not critical_failures:
            print("   ✅ PHASE 4 COMPREHENSIVE MEDICAL PATTERN RECOGNITION ENGINE: PRODUCTION READY")
            print("   🎯 All critical requirements met with excellent performance")
        elif success_rate >= 75:
            print("   ⚠️  PHASE 4 SYSTEM: MOSTLY FUNCTIONAL with minor issues")
            print("   🔧 Some improvements needed before full production deployment")
        else:
            print("   ❌ PHASE 4 SYSTEM: SIGNIFICANT ISSUES DETECTED")
            print("   🚨 Major improvements required before production deployment")
        
        print("\n" + "=" * 80)
        print("END OF PHASE 4 COMPREHENSIVE API TESTING REPORT")
        print("=" * 80)

async def main():
    """Main testing function"""
    print("🚀 PHASE 4 COMPREHENSIVE MEDICAL PATTERN RECOGNITION ENGINE API TESTING")
    print("=" * 80)
    print("Testing the most advanced medical AI system ever created via API endpoints...")
    print("Algorithm Version: 4.0_revolutionary_comprehensive")
    print("=" * 80)
    
    # Initialize and run comprehensive tests
    tester = Phase4MedicalAPITester()
    await tester.run_comprehensive_tests()

if __name__ == "__main__":
    asyncio.run(main())