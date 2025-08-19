#!/usr/bin/env python3
"""
🚀 STEP 3.1 PHASE A COMPREHENSIVE BACKEND TESTING
Foundation Excellence Medical Intent Classification System Testing

This comprehensive test suite validates all aspects of the newly implemented
Step 3.1 Phase A Medical Intent Classification System including:

1. Medical Intent Classification API Testing
2. Multi-Message Intent Analysis Testing  
3. Intent Performance Metrics Testing
4. Integration Testing with existing Medical AI
5. Confidence Scoring Validation
6. Performance Requirements Validation

Test Coverage:
- 20+ intent categories recognition
- Confidence scoring between 0-1
- Performance targets <100ms (target <50ms)
- Clinical reasoning integration
- Emergency detection enhancement
- Algorithm version 3.1_foundation_excellence
"""

import asyncio
import json
import time
import requests
import sys
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add the backend directory to Python path
sys.path.append('/app/backend')

# Test configuration
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://medai-debug-1.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class MedicalIntentClassificationTester:
    """
    🧪 COMPREHENSIVE MEDICAL INTENT CLASSIFICATION TESTING SUITE
    
    Tests all aspects of the Step 3.1 Phase A Foundation Excellence system
    with realistic medical scenarios and performance validation.
    """
    
    def __init__(self):
        self.test_results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": [],
            "performance_metrics": {},
            "critical_issues": [],
            "summary": ""
        }
        
        # Test scenarios for comprehensive validation
        self.test_scenarios = self._load_comprehensive_test_scenarios()
        
    def _load_comprehensive_test_scenarios(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load comprehensive test scenarios covering all intent categories"""
        
        return {
            # 1. MEDICAL INTENT CLASSIFICATION API TESTING
            "symptom_reporting_scenarios": [
                {
                    "message": "I have severe chest pain that started this morning",
                    "expected_intent": "symptom_reporting",
                    "expected_urgency": ["high", "urgent", "critical"],
                    "expected_confidence_min": 0.8,
                    "scenario_name": "Acute Chest Pain Reporting"
                },
                {
                    "message": "My headache has been getting worse over the past few days",
                    "expected_intent": "symptom_reporting", 
                    "expected_urgency": ["medium", "high"],
                    "expected_confidence_min": 0.7,
                    "scenario_name": "Progressive Headache"
                },
                {
                    "message": "I'm experiencing shortness of breath and feeling dizzy",
                    "expected_intent": "symptom_reporting",
                    "expected_urgency": ["high", "urgent", "critical"],
                    "expected_confidence_min": 0.8,
                    "scenario_name": "Respiratory Distress"
                }
            ],
            
            "emergency_scenarios": [
                {
                    "message": "I can't breathe, need help now",
                    "expected_intent": "emergency_concern",
                    "expected_urgency": ["critical", "emergency"],
                    "expected_confidence_min": 0.9,
                    "scenario_name": "Breathing Emergency"
                },
                {
                    "message": "Something's really wrong, call 911",
                    "expected_intent": "emergency_concern",
                    "expected_urgency": ["critical", "emergency"],
                    "expected_confidence_min": 0.9,
                    "scenario_name": "Emergency Call Request"
                },
                {
                    "message": "I think I'm having a heart attack",
                    "expected_intent": "emergency_concern",
                    "expected_urgency": ["critical", "emergency"],
                    "expected_confidence_min": 0.85,
                    "scenario_name": "Suspected Heart Attack"
                }
            ],
            
            "anxiety_emotional_scenarios": [
                {
                    "message": "I'm worried this might be serious",
                    "expected_intent": "anxiety_concern",
                    "expected_urgency": ["low", "medium"],
                    "expected_confidence_min": 0.7,
                    "scenario_name": "Health Anxiety"
                },
                {
                    "message": "I'm scared it could be cancer",
                    "expected_intent": "anxiety_concern",
                    "expected_urgency": ["medium", "high"],
                    "expected_confidence_min": 0.8,
                    "scenario_name": "Cancer Fear"
                },
                {
                    "message": "This is making me really anxious and stressed",
                    "expected_intent": "emotional_distress",
                    "expected_urgency": ["medium"],
                    "expected_confidence_min": 0.7,
                    "scenario_name": "Emotional Distress"
                }
            ],
            
            "medication_inquiries": [
                {
                    "message": "What are the side effects of my medication?",
                    "expected_intent": "medication_inquiry",
                    "expected_urgency": ["low", "medium"],
                    "expected_confidence_min": 0.8,
                    "scenario_name": "Side Effects Inquiry"
                },
                {
                    "message": "I'm having an allergic reaction to this drug",
                    "expected_intent": "allergy_reporting",
                    "expected_urgency": ["high", "urgent", "critical"],
                    "expected_confidence_min": 0.9,
                    "scenario_name": "Drug Allergy"
                },
                {
                    "message": "How often should I take this medication?",
                    "expected_intent": "medication_inquiry",
                    "expected_urgency": ["low", "medium"],
                    "expected_confidence_min": 0.8,
                    "scenario_name": "Dosage Question"
                }
            ],
            
            "treatment_guidance_requests": [
                {
                    "message": "Should I go to the ER?",
                    "expected_intent": "medical_guidance",
                    "expected_urgency": ["medium", "high"],
                    "expected_confidence_min": 0.8,
                    "scenario_name": "ER Decision"
                },
                {
                    "message": "What should I do about this pain?",
                    "expected_intent": "medical_guidance",
                    "expected_urgency": ["medium"],
                    "expected_confidence_min": 0.7,
                    "scenario_name": "Pain Management Guidance"
                },
                {
                    "message": "I need a second opinion on my diagnosis",
                    "expected_intent": "second_opinion",
                    "expected_urgency": ["medium"],
                    "expected_confidence_min": 0.8,
                    "scenario_name": "Second Opinion Request"
                }
            ],
            
            # 2. MULTI-MESSAGE CONVERSATION SEQUENCES
            "conversation_sequences": [
                {
                    "messages": [
                        "I have chest pain",
                        "It started about an hour ago",
                        "It's getting worse and I'm sweating",
                        "Should I call 911?"
                    ],
                    "expected_progression": ["symptom_reporting", "duration_inquiry", "progression_tracking", "medical_guidance"],
                    "scenario_name": "Escalating Chest Pain Conversation"
                },
                {
                    "messages": [
                        "I'm worried about my headaches",
                        "They've been happening for weeks",
                        "Sometimes they're really severe",
                        "What could be causing this?"
                    ],
                    "expected_progression": ["anxiety_concern", "duration_inquiry", "severity_assessment", "medical_guidance"],
                    "scenario_name": "Chronic Headache Inquiry"
                }
            ]
        }
    
    async def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run all comprehensive tests for Step 3.1 Phase A system"""
        
        print("🚀 STARTING STEP 3.1 PHASE A COMPREHENSIVE TESTING")
        print("=" * 80)
        
        # Test 1: Medical Intent Classification API Testing
        await self._test_medical_intent_classification_api()
        
        # Test 2: Multi-Message Intent Analysis Testing
        await self._test_multi_message_intent_analysis()
        
        # Test 3: Intent Performance Metrics Testing
        await self._test_intent_performance_metrics()
        
        # Test 4: Integration Testing with existing Medical AI
        await self._test_medical_ai_integration()
        
        # Test 5: Confidence Scoring Validation
        await self._test_confidence_scoring_validation()
        
        # Test 6: Performance Requirements Validation
        await self._test_performance_requirements()
        
        # Generate final summary
        self._generate_test_summary()
        
        return self.test_results
    
    async def _test_medical_intent_classification_api(self):
        """Test 1: Medical Intent Classification API Testing"""
        
        print("\n📋 TEST 1: MEDICAL INTENT CLASSIFICATION API TESTING")
        print("-" * 60)
        
        test_categories = [
            ("Symptom Reporting", self.test_scenarios["symptom_reporting_scenarios"]),
            ("Emergency Scenarios", self.test_scenarios["emergency_scenarios"]),
            ("Anxiety/Emotional", self.test_scenarios["anxiety_emotional_scenarios"]),
            ("Medication Inquiries", self.test_scenarios["medication_inquiries"]),
            ("Treatment Guidance", self.test_scenarios["treatment_guidance_requests"])
        ]
        
        for category_name, scenarios in test_categories:
            print(f"\n🔍 Testing {category_name}:")
            
            for scenario in scenarios:
                await self._test_single_intent_classification(scenario, category_name)
    
    async def _test_single_intent_classification(self, scenario: Dict[str, Any], category: str):
        """Test a single intent classification scenario"""
        
        test_name = f"{category} - {scenario['scenario_name']}"
        self.test_results["total_tests"] += 1
        
        try:
            # Prepare request
            request_data = {
                "message": scenario["message"],
                "conversation_context": None,
                "include_detailed_analysis": True
            }
            
            # Record start time for performance measurement
            start_time = time.time()
            
            # Make API call
            response = requests.post(
                f"{API_BASE}/medical-ai/intent-classification",
                json=request_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            # Record end time
            end_time = time.time()
            processing_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                result = response.json()
                
                # Validate response structure
                required_fields = [
                    "primary_intent", "confidence_score", "confidence_level",
                    "urgency_level", "clinical_significance", "clinical_reasoning",
                    "processing_time_ms", "algorithm_version"
                ]
                
                missing_fields = [field for field in required_fields if field not in result]
                if missing_fields:
                    raise Exception(f"Missing required fields: {missing_fields}")
                
                # Validate intent classification
                intent_match = result["primary_intent"] == scenario["expected_intent"]
                
                # Validate urgency level
                urgency_match = result["urgency_level"] in scenario["expected_urgency"]
                
                # Validate confidence score
                confidence_valid = result["confidence_score"] >= scenario["expected_confidence_min"]
                
                # Validate confidence score range
                confidence_range_valid = 0.0 <= result["confidence_score"] <= 1.0
                
                # Validate algorithm version
                algorithm_version_valid = result["algorithm_version"] == "3.1_foundation_excellence"
                
                # Check for clinical reasoning
                clinical_reasoning_present = len(result["clinical_reasoning"]) > 0
                
                # Overall test success
                test_passed = (intent_match and urgency_match and confidence_valid and 
                             confidence_range_valid and algorithm_version_valid and 
                             clinical_reasoning_present)
                
                if test_passed:
                    self.test_results["passed_tests"] += 1
                    print(f"  ✅ {test_name}")
                    print(f"     Intent: {result['primary_intent']} (confidence: {result['confidence_score']:.3f})")
                    print(f"     Urgency: {result['urgency_level']}, Processing: {processing_time:.1f}ms")
                else:
                    self.test_results["failed_tests"] += 1
                    print(f"  ❌ {test_name}")
                    print(f"     Expected intent: {scenario['expected_intent']}, Got: {result['primary_intent']}")
                    print(f"     Expected urgency: {scenario['expected_urgency']}, Got: {result['urgency_level']}")
                    print(f"     Confidence: {result['confidence_score']:.3f} (min: {scenario['expected_confidence_min']})")
                
                # Store detailed results
                self.test_results["test_details"].append({
                    "test_name": test_name,
                    "passed": test_passed,
                    "message": scenario["message"],
                    "expected_intent": scenario["expected_intent"],
                    "actual_intent": result["primary_intent"],
                    "confidence_score": result["confidence_score"],
                    "urgency_level": result["urgency_level"],
                    "processing_time_ms": processing_time,
                    "clinical_reasoning": result["clinical_reasoning"]
                })
                
            else:
                self.test_results["failed_tests"] += 1
                error_msg = f"API call failed with status {response.status_code}: {response.text}"
                print(f"  ❌ {test_name} - {error_msg}")
                self.test_results["critical_issues"].append(f"{test_name}: {error_msg}")
                
        except Exception as e:
            self.test_results["failed_tests"] += 1
            error_msg = f"Test failed: {str(e)}"
            print(f"  ❌ {test_name} - {error_msg}")
            self.test_results["critical_issues"].append(f"{test_name}: {error_msg}")
    
    async def _test_multi_message_intent_analysis(self):
        """Test 2: Multi-Message Intent Analysis Testing"""
        
        print("\n📋 TEST 2: MULTI-MESSAGE INTENT ANALYSIS TESTING")
        print("-" * 60)
        
        for scenario in self.test_scenarios["conversation_sequences"]:
            test_name = f"Multi-Message - {scenario['scenario_name']}"
            self.test_results["total_tests"] += 1
            
            try:
                # Prepare request
                request_data = {
                    "messages": scenario["messages"],
                    "conversation_id": f"test_conv_{int(time.time())}",
                    "analyze_progression": True
                }
                
                # Make API call
                response = requests.post(
                    f"{API_BASE}/medical-ai/multi-message-intent",
                    json=request_data,
                    headers={"Content-Type": "application/json"},
                    timeout=15
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Validate response structure
                    required_fields = [
                        "conversation_summary", "message_analyses", 
                        "intent_progression", "conversation_insights"
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in result]
                    if missing_fields:
                        raise Exception(f"Missing required fields: {missing_fields}")
                    
                    # Validate number of message analyses
                    analyses_count_valid = len(result["message_analyses"]) == len(scenario["messages"])
                    
                    # Validate intent progression tracking
                    progression_valid = len(result["intent_progression"]) == len(scenario["messages"]) - 1
                    
                    # Validate conversation insights generation
                    insights_present = len(result["conversation_insights"]) > 0
                    
                    # Validate conversation summary
                    summary_present = len(result["conversation_summary"]) > 0
                    
                    test_passed = (analyses_count_valid and progression_valid and 
                                 insights_present and summary_present)
                    
                    if test_passed:
                        self.test_results["passed_tests"] += 1
                        print(f"  ✅ {test_name}")
                        print(f"     Messages analyzed: {len(result['message_analyses'])}")
                        print(f"     Progression steps: {len(result['intent_progression'])}")
                        print(f"     Insights generated: {len(result['conversation_insights'])}")
                    else:
                        self.test_results["failed_tests"] += 1
                        print(f"  ❌ {test_name}")
                        print(f"     Analyses count: {len(result['message_analyses'])} (expected: {len(scenario['messages'])})")
                        
                else:
                    self.test_results["failed_tests"] += 1
                    error_msg = f"API call failed with status {response.status_code}"
                    print(f"  ❌ {test_name} - {error_msg}")
                    self.test_results["critical_issues"].append(f"{test_name}: {error_msg}")
                    
            except Exception as e:
                self.test_results["failed_tests"] += 1
                error_msg = f"Test failed: {str(e)}"
                print(f"  ❌ {test_name} - {error_msg}")
                self.test_results["critical_issues"].append(f"{test_name}: {error_msg}")
    
    async def _test_intent_performance_metrics(self):
        """Test 3: Intent Performance Metrics Testing"""
        
        print("\n📋 TEST 3: INTENT PERFORMANCE METRICS TESTING")
        print("-" * 60)
        
        test_name = "Intent Performance Metrics API"
        self.test_results["total_tests"] += 1
        
        try:
            # Make API call
            response = requests.get(
                f"{API_BASE}/medical-ai/intent-performance",
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Validate response structure
                required_fields = [
                    "status", "performance_metrics", "system_capabilities",
                    "intent_categories", "last_updated"
                ]
                
                missing_fields = [field for field in required_fields if field not in result]
                if missing_fields:
                    raise Exception(f"Missing required fields: {missing_fields}")
                
                # Validate system status
                status_valid = result["status"] == "operational"
                
                # Validate algorithm version reporting
                algorithm_version_valid = (
                    "algorithm_version" in result["performance_metrics"] and
                    result["performance_metrics"]["algorithm_version"] == "3.1_foundation_excellence"
                )
                
                # Validate intent categories (should be 20+)
                intent_categories_valid = len(result["intent_categories"]) >= 20
                
                # Validate performance metrics structure
                perf_metrics = result["performance_metrics"]
                metrics_valid = all(key in perf_metrics for key in [
                    "total_classifications", "average_processing_time_ms", 
                    "confidence_distribution", "algorithm_version"
                ])
                
                test_passed = (status_valid and algorithm_version_valid and 
                             intent_categories_valid and metrics_valid)
                
                if test_passed:
                    self.test_results["passed_tests"] += 1
                    print(f"  ✅ {test_name}")
                    print(f"     Status: {result['status']}")
                    print(f"     Algorithm version: {perf_metrics['algorithm_version']}")
                    print(f"     Intent categories: {len(result['intent_categories'])}")
                    print(f"     Avg processing time: {perf_metrics.get('average_processing_time_ms', 'N/A')}ms")
                    
                    # Store performance metrics for later analysis
                    self.test_results["performance_metrics"] = perf_metrics
                else:
                    self.test_results["failed_tests"] += 1
                    print(f"  ❌ {test_name}")
                    print(f"     Status: {result.get('status', 'unknown')}")
                    print(f"     Intent categories: {len(result.get('intent_categories', []))}")
                    
            else:
                self.test_results["failed_tests"] += 1
                error_msg = f"API call failed with status {response.status_code}"
                print(f"  ❌ {test_name} - {error_msg}")
                self.test_results["critical_issues"].append(f"{test_name}: {error_msg}")
                
        except Exception as e:
            self.test_results["failed_tests"] += 1
            error_msg = f"Test failed: {str(e)}"
            print(f"  ❌ {test_name} - {error_msg}")
            self.test_results["critical_issues"].append(f"{test_name}: {error_msg}")
    
    async def _test_medical_ai_integration(self):
        """Test 4: Integration Testing with existing Medical AI"""
        
        print("\n📋 TEST 4: MEDICAL AI INTEGRATION TESTING")
        print("-" * 60)
        
        # Test existing medical AI endpoints still work
        integration_tests = [
            {
                "name": "Medical AI Initialization",
                "endpoint": "/medical-ai/initialize",
                "method": "POST",
                "data": {
                    "patient_id": "test_patient_intent_integration",
                    "timestamp": datetime.utcnow().isoformat()
                }
            },
            {
                "name": "Medical AI Message Processing",
                "endpoint": "/medical-ai/message", 
                "method": "POST",
                "data": {
                    "consultation_id": "test_consultation_intent",
                    "message": "I have chest pain with shortness of breath",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        ]
        
        for test_config in integration_tests:
            test_name = f"Integration - {test_config['name']}"
            self.test_results["total_tests"] += 1
            
            try:
                if test_config["method"] == "POST":
                    response = requests.post(
                        f"{API_BASE}{test_config['endpoint']}",
                        json=test_config["data"],
                        headers={"Content-Type": "application/json"},
                        timeout=10
                    )
                else:
                    response = requests.get(
                        f"{API_BASE}{test_config['endpoint']}",
                        timeout=10
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Basic validation that response has expected structure
                    response_valid = isinstance(result, dict) and len(result) > 0
                    
                    if response_valid:
                        self.test_results["passed_tests"] += 1
                        print(f"  ✅ {test_name}")
                        
                        # Check if response includes intent analysis (for message processing)
                        if "message" in test_config["data"]:
                            has_intent_info = any(key in result for key in [
                                "intent_analysis", "medical_reasoning", "urgency"
                            ])
                            if has_intent_info:
                                print(f"     Intent integration detected in response")
                    else:
                        self.test_results["failed_tests"] += 1
                        print(f"  ❌ {test_name} - Invalid response structure")
                        
                else:
                    self.test_results["failed_tests"] += 1
                    error_msg = f"API call failed with status {response.status_code}"
                    print(f"  ❌ {test_name} - {error_msg}")
                    
            except Exception as e:
                self.test_results["failed_tests"] += 1
                error_msg = f"Test failed: {str(e)}"
                print(f"  ❌ {test_name} - {error_msg}")
    
    async def _test_confidence_scoring_validation(self):
        """Test 5: Confidence Scoring Validation"""
        
        print("\n📋 TEST 5: CONFIDENCE SCORING VALIDATION")
        print("-" * 60)
        
        # Test scenarios with different expected confidence levels
        confidence_test_scenarios = [
            {
                "message": "I have severe chest pain and can't breathe",
                "expected_confidence_min": 0.8,
                "expected_confidence_level": ["high", "very_high"],
                "scenario_name": "High Confidence Emergency"
            },
            {
                "message": "I think maybe something might be wrong",
                "expected_confidence_max": 0.6,
                "expected_confidence_level": ["low", "medium"],
                "scenario_name": "Low Confidence Uncertain"
            },
            {
                "message": "What are the side effects of aspirin?",
                "expected_confidence_min": 0.7,
                "expected_confidence_level": ["medium", "high"],
                "scenario_name": "Medium Confidence Clear Question"
            }
        ]
        
        for scenario in confidence_test_scenarios:
            test_name = f"Confidence Validation - {scenario['scenario_name']}"
            self.test_results["total_tests"] += 1
            
            try:
                request_data = {
                    "message": scenario["message"],
                    "include_detailed_analysis": True
                }
                
                response = requests.post(
                    f"{API_BASE}/medical-ai/intent-classification",
                    json=request_data,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Validate confidence score range
                    confidence_score = result["confidence_score"]
                    confidence_range_valid = 0.0 <= confidence_score <= 1.0
                    
                    # Validate confidence level matches score
                    confidence_level = result["confidence_level"]
                    confidence_level_valid = confidence_level in scenario["expected_confidence_level"]
                    
                    # Validate confidence factors present
                    confidence_factors_present = (
                        "confidence_factors" in result and 
                        len(result["confidence_factors"]) > 0
                    )
                    
                    # Validate confidence interval
                    confidence_interval_valid = (
                        "confidence_interval" in result and
                        len(result["confidence_interval"]) == 2 and
                        result["confidence_interval"][0] <= confidence_score <= result["confidence_interval"][1]
                    )
                    
                    # Validate uncertainty indicators
                    uncertainty_indicators_present = "uncertainty_indicators" in result
                    
                    # Check specific confidence expectations
                    confidence_expectation_met = True
                    if "expected_confidence_min" in scenario:
                        confidence_expectation_met = confidence_score >= scenario["expected_confidence_min"]
                    elif "expected_confidence_max" in scenario:
                        confidence_expectation_met = confidence_score <= scenario["expected_confidence_max"]
                    
                    test_passed = (confidence_range_valid and confidence_level_valid and 
                                 confidence_factors_present and confidence_interval_valid and
                                 uncertainty_indicators_present and confidence_expectation_met)
                    
                    if test_passed:
                        self.test_results["passed_tests"] += 1
                        print(f"  ✅ {test_name}")
                        print(f"     Confidence: {confidence_score:.3f} ({confidence_level})")
                        print(f"     Interval: {result['confidence_interval']}")
                        print(f"     Uncertainty indicators: {len(result['uncertainty_indicators'])}")
                    else:
                        self.test_results["failed_tests"] += 1
                        print(f"  ❌ {test_name}")
                        print(f"     Confidence: {confidence_score:.3f} (expected level: {scenario['expected_confidence_level']})")
                        
                else:
                    self.test_results["failed_tests"] += 1
                    error_msg = f"API call failed with status {response.status_code}"
                    print(f"  ❌ {test_name} - {error_msg}")
                    
            except Exception as e:
                self.test_results["failed_tests"] += 1
                error_msg = f"Test failed: {str(e)}"
                print(f"  ❌ {test_name} - {error_msg}")
    
    async def _test_performance_requirements(self):
        """Test 6: Performance Requirements Validation"""
        
        print("\n📋 TEST 6: PERFORMANCE REQUIREMENTS VALIDATION")
        print("-" * 60)
        
        # Test performance with multiple requests
        performance_test_messages = [
            "I have chest pain",
            "My head hurts really bad",
            "I'm worried about my symptoms",
            "Should I see a doctor?",
            "I need help with my medication"
        ]
        
        processing_times = []
        
        for i, message in enumerate(performance_test_messages):
            test_name = f"Performance Test {i+1}"
            self.test_results["total_tests"] += 1
            
            try:
                request_data = {
                    "message": message,
                    "include_detailed_analysis": True
                }
                
                # Measure processing time
                start_time = time.time()
                
                response = requests.post(
                    f"{API_BASE}/medical-ai/intent-classification",
                    json=request_data,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                end_time = time.time()
                total_time = (end_time - start_time) * 1000  # Convert to milliseconds
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Get reported processing time
                    reported_time = result.get("processing_time_ms", total_time)
                    processing_times.append(reported_time)
                    
                    # Validate performance targets
                    target_met_50ms = reported_time < 50  # Target performance
                    target_met_100ms = reported_time < 100  # Acceptable performance
                    
                    if target_met_50ms:
                        self.test_results["passed_tests"] += 1
                        print(f"  ✅ {test_name} - {reported_time:.1f}ms (Target <50ms)")
                    elif target_met_100ms:
                        self.test_results["passed_tests"] += 1
                        print(f"  ✅ {test_name} - {reported_time:.1f}ms (Acceptable <100ms)")
                    else:
                        self.test_results["failed_tests"] += 1
                        print(f"  ❌ {test_name} - {reported_time:.1f}ms (Exceeds 100ms limit)")
                        self.test_results["critical_issues"].append(
                            f"Performance issue: {reported_time:.1f}ms exceeds 100ms target"
                        )
                        
                else:
                    self.test_results["failed_tests"] += 1
                    print(f"  ❌ {test_name} - API call failed")
                    
            except Exception as e:
                self.test_results["failed_tests"] += 1
                print(f"  ❌ {test_name} - {str(e)}")
        
        # Calculate performance statistics
        if processing_times:
            avg_time = sum(processing_times) / len(processing_times)
            max_time = max(processing_times)
            min_time = min(processing_times)
            
            print(f"\n📊 PERFORMANCE SUMMARY:")
            print(f"   Average processing time: {avg_time:.1f}ms")
            print(f"   Min processing time: {min_time:.1f}ms")
            print(f"   Max processing time: {max_time:.1f}ms")
            print(f"   Target <50ms: {'✅ MET' if avg_time < 50 else '❌ NOT MET'}")
            print(f"   Acceptable <100ms: {'✅ MET' if avg_time < 100 else '❌ NOT MET'}")
            
            self.test_results["performance_metrics"]["measured_avg_processing_time"] = avg_time
            self.test_results["performance_metrics"]["measured_max_processing_time"] = max_time
            self.test_results["performance_metrics"]["measured_min_processing_time"] = min_time
    
    def _generate_test_summary(self):
        """Generate comprehensive test summary"""
        
        total_tests = self.test_results["total_tests"]
        passed_tests = self.test_results["passed_tests"]
        failed_tests = self.test_results["failed_tests"]
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "=" * 80)
        print("🏆 STEP 3.1 PHASE A COMPREHENSIVE TESTING SUMMARY")
        print("=" * 80)
        
        print(f"\n📊 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {failed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        # Performance summary
        if "measured_avg_processing_time" in self.test_results["performance_metrics"]:
            avg_time = self.test_results["performance_metrics"]["measured_avg_processing_time"]
            print(f"\n⚡ PERFORMANCE RESULTS:")
            print(f"   Average Processing Time: {avg_time:.1f}ms")
            print(f"   Target <50ms: {'✅ MET' if avg_time < 50 else '❌ NOT MET'}")
            print(f"   Acceptable <100ms: {'✅ MET' if avg_time < 100 else '❌ NOT MET'}")
        
        # Critical issues
        if self.test_results["critical_issues"]:
            print(f"\n🚨 CRITICAL ISSUES ({len(self.test_results['critical_issues'])}):")
            for issue in self.test_results["critical_issues"]:
                print(f"   • {issue}")
        
        # Test categories summary
        category_results = {}
        for test_detail in self.test_results["test_details"]:
            category = test_detail["test_name"].split(" - ")[0]
            if category not in category_results:
                category_results[category] = {"passed": 0, "total": 0}
            category_results[category]["total"] += 1
            if test_detail["passed"]:
                category_results[category]["passed"] += 1
        
        if category_results:
            print(f"\n📋 CATEGORY BREAKDOWN:")
            for category, results in category_results.items():
                success_rate = (results["passed"] / results["total"] * 100) if results["total"] > 0 else 0
                status = "✅" if success_rate >= 80 else "⚠️" if success_rate >= 60 else "❌"
                print(f"   {status} {category}: {results['passed']}/{results['total']} ({success_rate:.1f}%)")
        
        # Generate summary message
        if success_rate >= 90:
            status_emoji = "🎉"
            status_message = "EXCELLENT - Step 3.1 Phase A system is fully functional"
        elif success_rate >= 80:
            status_emoji = "✅"
            status_message = "GOOD - Step 3.1 Phase A system is mostly functional with minor issues"
        elif success_rate >= 60:
            status_emoji = "⚠️"
            status_message = "MODERATE - Step 3.1 Phase A system has significant issues requiring attention"
        else:
            status_emoji = "❌"
            status_message = "CRITICAL - Step 3.1 Phase A system has major functionality problems"
        
        print(f"\n{status_emoji} FINAL ASSESSMENT: {status_message}")
        
        self.test_results["summary"] = f"{status_emoji} {status_message} (Success Rate: {success_rate:.1f}%)"

async def main():
    """Main test execution function"""
    
    print("🚀 STEP 3.1 PHASE A: FOUNDATION EXCELLENCE MEDICAL INTENT CLASSIFICATION TESTING")
    print("🎯 Testing comprehensive medical intent classification system with clinical-grade precision")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"📡 API Base: {API_BASE}")
    
    # Initialize tester
    tester = MedicalIntentClassificationTester()
    
    # Run comprehensive tests
    results = await tester.run_comprehensive_tests()
    
    # Return results for potential further processing
    return results

if __name__ == "__main__":
    # Run the comprehensive test suite
    asyncio.run(main())