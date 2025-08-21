#!/usr/bin/env python3
"""
🔮 WEEK 4 COMPREHENSIVE TESTING - PREDICTIVE INTENT MODELING & SUBSPECIALTY CLINICAL REASONING ENGINE

Test the revolutionary ML-powered Week 4 components with comprehensive validation:
- POST /api/medical-ai/predictive-intent-modeling
- POST /api/medical-ai/conversation-intelligence  
- GET /api/medical-ai/predictive-modeling-performance
- POST /api/medical-ai/subspecialty-reasoning

Validation targets:
- >90% accuracy in intent prediction
- <25ms processing times for predictive modeling
- Subspecialty-level clinical intelligence
- Emergency scenario detection and clinical appropriateness
"""

import asyncio
import aiohttp
import json
import time
import sys
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import statistics

# Backend URL from environment
BACKEND_URL = "https://empathcare-ai.preview.emergentagent.com/api"

@dataclass
class TestResult:
    test_name: str
    success: bool
    response_time_ms: float
    details: Dict[str, Any]
    error_message: Optional[str] = None

class Week4ComprehensiveTester:
    def __init__(self):
        self.results = []
        self.session = None
        
    async def setup_session(self):
        """Setup HTTP session"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'Content-Type': 'application/json'}
        )
    
    async def cleanup_session(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
    
    async def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request with timing"""
        start_time = time.time()
        
        try:
            url = f"{BACKEND_URL}{endpoint}"
            
            if method.upper() == "GET":
                async with self.session.get(url) as response:
                    response_data = await response.json()
                    status_code = response.status
            else:
                async with self.session.post(url, json=data) as response:
                    response_data = await response.json()
                    status_code = response.status
            
            response_time = (time.time() - start_time) * 1000
            
            return {
                "success": status_code == 200,
                "status_code": status_code,
                "data": response_data,
                "response_time_ms": response_time
            }
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "status_code": 500,
                "data": {"error": str(e)},
                "response_time_ms": response_time
            }
    
    async def test_predictive_intent_modeling(self):
        """Test POST /api/medical-ai/predictive-intent-modeling"""
        print("🔮 Testing Predictive Intent Modeling...")
        
        # Test scenario from review request
        test_data = {
            "conversation_history": [
                {"message": "I have chest pain", "timestamp": "2025-01-17T10:00:00Z", "speaker": "patient"},
                {"message": "It started 2 hours ago", "timestamp": "2025-01-17T10:01:00Z", "speaker": "patient"},
                {"message": "It's crushing pressure", "timestamp": "2025-01-17T10:02:00Z", "speaker": "patient"}
            ],
            "current_context": {
                "patient_age": 55,
                "gender": "male",
                "medical_history": ["hypertension"],
                "current_medications": ["lisinopril"]
            },
            "patient_data": {
                "age": 55,
                "gender": "male",
                "risk_factors": ["hypertension", "smoking_history"]
            }
        }
        
        result = await self.make_request("POST", "/medical-ai/predictive-intent-modeling", test_data)
        
        success = result["success"]
        details = {}
        
        if success:
            data = result["data"]
            details = {
                "predicted_intents_count": len(data.get("predicted_intents", [])),
                "processing_time_ms": data.get("processing_time_ms", 0),
                "algorithm_version": data.get("algorithm_version", "unknown"),
                "confidence_levels": [],
                "clinical_contexts": [],
                "time_likelihoods": []
            }
            
            # Validate predicted intents (should be 3-5)
            predicted_intents = data.get("predicted_intents", [])
            if len(predicted_intents) >= 3 and len(predicted_intents) <= 5:
                details["intent_count_valid"] = True
            else:
                details["intent_count_valid"] = False
                success = False
            
            # Validate confidence scores and levels
            for intent in predicted_intents:
                confidence_score = intent.get("confidence_score", 0)
                confidence_level = intent.get("confidence_level", "")
                clinical_context = intent.get("clinical_context", "")
                time_likelihood = intent.get("time_likelihood", "")
                
                details["confidence_levels"].append(confidence_level)
                details["clinical_contexts"].append(clinical_context)
                details["time_likelihoods"].append(time_likelihood)
                
                # Validate confidence level categorization
                if confidence_score > 0.9 and confidence_level != "very_high":
                    success = False
                elif 0.7 <= confidence_score <= 0.9 and confidence_level != "high":
                    success = False
                elif 0.5 <= confidence_score < 0.7 and confidence_level != "moderate":
                    success = False
                elif 0.3 <= confidence_score < 0.5 and confidence_level != "low":
                    success = False
                elif confidence_score < 0.3 and confidence_level != "very_low":
                    success = False
            
            # Validate processing time (<25ms target)
            processing_time = data.get("processing_time_ms", 999)
            details["processing_time_target_met"] = processing_time < 25
            
            # Check for emergency concern prediction (chest pain scenario)
            emergency_detected = any("emergency" in intent.get("clinical_context", "").lower() or 
                                   "urgent" in intent.get("clinical_context", "").lower() or
                                   "immediate" in intent.get("time_likelihood", "").lower()
                                   for intent in predicted_intents)
            details["emergency_concern_detected"] = emergency_detected
            
        self.results.append(TestResult(
            test_name="Predictive Intent Modeling",
            success=success,
            response_time_ms=result["response_time_ms"],
            details=details,
            error_message=result["data"].get("error") if not success else None
        ))
        
        return success
    
    async def test_conversation_intelligence(self):
        """Test POST /api/medical-ai/conversation-intelligence"""
        print("🧠 Testing Conversation Intelligence...")
        
        # Test multiple scenarios
        scenarios = [
            {
                "name": "Emergency Scenario",
                "data": {
                    "conversation_history": [
                        {"message": "I'm having severe chest pain", "timestamp": "2025-01-17T10:00:00Z", "speaker": "patient"},
                        {"message": "It feels like an elephant sitting on my chest", "timestamp": "2025-01-17T10:01:00Z", "speaker": "patient"},
                        {"message": "I'm also short of breath", "timestamp": "2025-01-17T10:02:00Z", "speaker": "patient"}
                    ],
                    "current_context": {
                        "patient_age": 67,
                        "gender": "male",
                        "medical_history": ["diabetes", "hypertension"]
                    },
                    "patient_data": {
                        "age": 67,
                        "gender": "male",
                        "risk_factors": ["diabetes", "hypertension", "family_history_cad"]
                    }
                }
            },
            {
                "name": "Routine Scenario", 
                "data": {
                    "conversation_history": [
                        {"message": "I have a mild headache", "timestamp": "2025-01-17T10:00:00Z", "speaker": "patient"},
                        {"message": "It started this morning", "timestamp": "2025-01-17T10:01:00Z", "speaker": "patient"},
                        {"message": "It's not too bad, just annoying", "timestamp": "2025-01-17T10:02:00Z", "speaker": "patient"}
                    ],
                    "current_context": {
                        "patient_age": 28,
                        "gender": "female"
                    },
                    "patient_data": {
                        "age": 28,
                        "gender": "female"
                    }
                }
            },
            {
                "name": "Complex Scenario",
                "data": {
                    "conversation_history": [
                        {"message": "I've been having stomach pain", "timestamp": "2025-01-17T10:00:00Z", "speaker": "patient"},
                        {"message": "Also feeling nauseous and dizzy", "timestamp": "2025-01-17T10:01:00Z", "speaker": "patient"},
                        {"message": "The pain is getting worse", "timestamp": "2025-01-17T10:02:00Z", "speaker": "patient"},
                        {"message": "I haven't eaten much today", "timestamp": "2025-01-17T10:03:00Z", "speaker": "patient"}
                    ],
                    "current_context": {
                        "patient_age": 45,
                        "gender": "female",
                        "medical_history": ["GERD"]
                    },
                    "patient_data": {
                        "age": 45,
                        "gender": "female",
                        "medical_history": ["GERD"]
                    }
                }
            }
        ]
        
        all_success = True
        scenario_results = []
        
        for scenario in scenarios:
            result = await self.make_request("POST", "/medical-ai/conversation-intelligence", scenario["data"])
            
            scenario_success = result["success"]
            scenario_details = {"scenario_name": scenario["name"]}
            
            if scenario_success:
                data = result["data"]
                scenario_details.update({
                    "predicted_intents_count": len(data.get("predicted_intents", [])),
                    "has_progression_analysis": "progression_analysis" in data,
                    "has_proactive_responses": "proactive_responses" in data,
                    "has_risk_assessment": "conversation_risk_assessment" in data,
                    "has_engagement_optimization": "engagement_optimization" in data,
                    "has_clinical_decision_support": "clinical_decision_support" in data,
                    "processing_time_ms": data.get("processing_time_ms", 0),
                    "algorithm_version": data.get("algorithm_version", "unknown")
                })
                
                # Validate processing time (<30ms target)
                processing_time = data.get("processing_time_ms", 999)
                scenario_details["processing_time_target_met"] = processing_time < 30
                
                # Validate comprehensive analysis components
                required_components = [
                    "predicted_intents", "progression_analysis", "proactive_responses",
                    "conversation_risk_assessment", "engagement_optimization", "clinical_decision_support"
                ]
                
                missing_components = [comp for comp in required_components if comp not in data]
                scenario_details["missing_components"] = missing_components
                
                if missing_components:
                    scenario_success = False
                
            else:
                scenario_details["error"] = result["data"].get("error", "Unknown error")
            
            scenario_results.append(scenario_details)
            
            if not scenario_success:
                all_success = False
        
        self.results.append(TestResult(
            test_name="Conversation Intelligence",
            success=all_success,
            response_time_ms=sum(r.get("processing_time_ms", 0) for r in scenario_results) / len(scenario_results),
            details={"scenarios": scenario_results},
            error_message=None if all_success else "One or more scenarios failed"
        ))
        
        return all_success
    
    async def test_predictive_modeling_performance(self):
        """Test GET /api/medical-ai/predictive-modeling-performance"""
        print("📊 Testing Predictive Modeling Performance...")
        
        result = await self.make_request("GET", "/medical-ai/predictive-modeling-performance")
        
        success = result["success"]
        details = {}
        
        if success:
            data = result["data"]
            details = {
                "status": data.get("status", "unknown"),
                "has_predictive_metrics": "predictive_modeling_metrics" in data,
                "has_subspecialty_metrics": "subspecialty_reasoning_metrics" in data,
                "has_week4_capabilities": "week4_capabilities" in data,
                "has_advanced_features": "advanced_features" in data,
                "algorithm_versions": data.get("algorithm_versions", {})
            }
            
            # Validate >90% accuracy target
            predictive_metrics = data.get("predictive_modeling_metrics", {})
            model_accuracy = predictive_metrics.get("model_accuracy", 0)
            details["model_accuracy"] = model_accuracy
            details["accuracy_target_met"] = model_accuracy >= 0.90
            
            # Validate operational status
            details["operational_status"] = data.get("status") == "operational"
            
            # Check Week 4 capabilities
            week4_caps = data.get("week4_capabilities", {})
            details["week4_capabilities"] = {
                "predictive_intent_accuracy_target": week4_caps.get("predictive_intent_accuracy_target"),
                "processing_time_target_ms": week4_caps.get("processing_time_target_ms"),
                "supported_subspecialties": week4_caps.get("supported_subspecialties", []),
                "ml_models_active": week4_caps.get("ml_models_active", False),
                "clinical_reasoning_active": week4_caps.get("clinical_reasoning_active", False)
            }
            
            # Validate advanced features
            advanced_features = data.get("advanced_features", {})
            required_features = [
                "conversation_intelligence", "proactive_response_generation",
                "clinical_risk_assessment", "engagement_optimization", "clinical_decision_support"
            ]
            
            missing_features = [feat for feat in required_features if not advanced_features.get(feat, False)]
            details["missing_advanced_features"] = missing_features
            
            if missing_features:
                success = False
        
        self.results.append(TestResult(
            test_name="Predictive Modeling Performance",
            success=success,
            response_time_ms=result["response_time_ms"],
            details=details,
            error_message=result["data"].get("error") if not success else None
        ))
        
        return success
    
    async def test_subspecialty_reasoning(self):
        """Test POST /api/medical-ai/subspecialty-reasoning"""
        print("🏥 Testing Subspecialty Clinical Reasoning...")
        
        # Test cardiology scenario as specified in review
        cardiology_test = {
            "subspecialty": "cardiology",
            "intents": [
                {
                    "intent_name": "cardiac_chest_pain_assessment",
                    "confidence": 0.95,
                    "clinical_context": "acute chest pain with cardiac risk factors"
                }
            ],
            "context": {
                "patient_data": {
                    "age": 58,
                    "gender": "male",
                    "symptoms": ["chest pain", "shortness of breath"],
                    "risk_factors": ["hypertension", "diabetes", "smoking_history"],
                    "vital_signs": {
                        "blood_pressure": "160/95",
                        "heart_rate": 95,
                        "respiratory_rate": 22
                    }
                },
                "clinical_scenario": "acute_chest_pain_evaluation"
            }
        }
        
        # Test other subspecialties if implemented
        subspecialty_tests = [
            {
                "name": "Cardiology",
                "data": cardiology_test
            },
            {
                "name": "Neurology",
                "data": {
                    "subspecialty": "neurology",
                    "intents": [
                        {
                            "intent_name": "neurological_symptom_assessment",
                            "confidence": 0.88,
                            "clinical_context": "acute neurological symptoms"
                        }
                    ],
                    "context": {
                        "patient_data": {
                            "age": 72,
                            "gender": "female",
                            "symptoms": ["weakness", "speech_difficulty"],
                            "onset": "sudden"
                        },
                        "clinical_scenario": "stroke_evaluation"
                    }
                }
            },
            {
                "name": "Emergency Medicine",
                "data": {
                    "subspecialty": "emergency_medicine",
                    "intents": [
                        {
                            "intent_name": "emergency_triage_assessment",
                            "confidence": 0.92,
                            "clinical_context": "emergency department triage"
                        }
                    ],
                    "context": {
                        "patient_data": {
                            "age": 45,
                            "gender": "male",
                            "chief_complaint": "severe_abdominal_pain",
                            "triage_level": "urgent"
                        },
                        "clinical_scenario": "emergency_triage"
                    }
                }
            }
        ]
        
        all_success = True
        subspecialty_results = []
        
        for test in subspecialty_tests:
            result = await self.make_request("POST", "/medical-ai/subspecialty-reasoning", test["data"])
            
            test_success = result["success"]
            test_details = {"subspecialty": test["name"]}
            
            if test_success:
                data = result["data"]
                test_details.update({
                    "subspecialty": data.get("subspecialty", "unknown"),
                    "has_reasoning_result": "reasoning_result" in data,
                    "processing_time_ms": data.get("processing_time_ms", 0),
                    "algorithm_version": data.get("algorithm_version", "unknown")
                })
                
                # Validate processing time (<25ms target)
                processing_time = data.get("processing_time_ms", 999)
                test_details["processing_time_target_met"] = processing_time < 25
                
                # Validate reasoning result structure
                reasoning_result = data.get("reasoning_result", {})
                if reasoning_result:
                    test_details["reasoning_components"] = list(reasoning_result.keys())
                    
                    # Check for cardiology-specific components
                    if test["name"] == "Cardiology":
                        cardiology_components = [
                            "cardiac_risk_stratification", "clinical_decision_rules",
                            "specialist_referral_criteria", "emergency_protocols"
                        ]
                        
                        found_components = [comp for comp in cardiology_components 
                                         if any(comp in str(reasoning_result).lower() for comp in cardiology_components)]
                        test_details["cardiology_specific_components"] = found_components
                        
                        # Check for Modified HEART Score, ECG indications, biomarker recommendations
                        reasoning_text = str(reasoning_result).lower()
                        test_details["has_heart_score"] = "heart" in reasoning_text or "risk stratification" in reasoning_text
                        test_details["has_ecg_indication"] = "ecg" in reasoning_text or "electrocardiogram" in reasoning_text
                        test_details["has_biomarker_rec"] = "troponin" in reasoning_text or "biomarker" in reasoning_text
                        test_details["has_imaging_protocol"] = "echo" in reasoning_text or "imaging" in reasoning_text
                        test_details["has_emergency_protocol"] = "acs" in reasoning_text or "emergency" in reasoning_text
                
            else:
                test_details["error"] = result["data"].get("error", "Unknown error")
            
            subspecialty_results.append(test_details)
            
            if not test_success:
                all_success = False
        
        self.results.append(TestResult(
            test_name="Subspecialty Clinical Reasoning",
            success=all_success,
            response_time_ms=statistics.mean([r.get("processing_time_ms", 0) for r in subspecialty_results if r.get("processing_time_ms", 0) > 0]),
            details={"subspecialty_tests": subspecialty_results},
            error_message=None if all_success else "One or more subspecialty tests failed"
        ))
        
        return all_success
    
    async def test_clinical_validation_scenarios(self):
        """Test clinical validation scenarios"""
        print("🩺 Testing Clinical Validation Scenarios...")
        
        # Emergency scenarios
        emergency_scenarios = [
            {
                "name": "Chest Pain Emergency",
                "conversation": [
                    {"message": "I have crushing chest pain", "timestamp": "2025-01-17T10:00:00Z", "speaker": "patient"},
                    {"message": "It started 30 minutes ago", "timestamp": "2025-01-17T10:01:00Z", "speaker": "patient"},
                    {"message": "I feel like I'm dying", "timestamp": "2025-01-17T10:02:00Z", "speaker": "patient"}
                ],
                "expected_urgency": "emergency"
            },
            {
                "name": "Stroke Symptoms",
                "conversation": [
                    {"message": "I can't speak properly", "timestamp": "2025-01-17T10:00:00Z", "speaker": "patient"},
                    {"message": "My face feels numb", "timestamp": "2025-01-17T10:01:00Z", "speaker": "patient"},
                    {"message": "I can't move my right arm", "timestamp": "2025-01-17T10:02:00Z", "speaker": "patient"}
                ],
                "expected_urgency": "emergency"
            }
        ]
        
        # Routine scenarios
        routine_scenarios = [
            {
                "name": "Mild Headache",
                "conversation": [
                    {"message": "I have a mild headache", "timestamp": "2025-01-17T10:00:00Z", "speaker": "patient"},
                    {"message": "It started this morning", "timestamp": "2025-01-17T10:01:00Z", "speaker": "patient"},
                    {"message": "It's not too bad", "timestamp": "2025-01-17T10:02:00Z", "speaker": "patient"}
                ],
                "expected_urgency": "routine"
            },
            {
                "name": "General Wellness",
                "conversation": [
                    {"message": "I want to improve my health", "timestamp": "2025-01-17T10:00:00Z", "speaker": "patient"},
                    {"message": "I exercise regularly", "timestamp": "2025-01-17T10:01:00Z", "speaker": "patient"},
                    {"message": "Any suggestions?", "timestamp": "2025-01-17T10:02:00Z", "speaker": "patient"}
                ],
                "expected_urgency": "routine"
            }
        ]
        
        all_scenarios = emergency_scenarios + routine_scenarios
        validation_results = []
        all_success = True
        
        for scenario in all_scenarios:
            # Test with predictive intent modeling
            test_data = {
                "conversation_history": scenario["conversation"],
                "current_context": {"patient_age": 45, "gender": "male"},
                "patient_data": {"age": 45, "gender": "male"}
            }
            
            result = await self.make_request("POST", "/medical-ai/predictive-intent-modeling", test_data)
            
            scenario_success = result["success"]
            scenario_details = {
                "scenario_name": scenario["name"],
                "expected_urgency": scenario["expected_urgency"]
            }
            
            if scenario_success:
                data = result["data"]
                predicted_intents = data.get("predicted_intents", [])
                
                # Check if urgency matches expectation
                urgency_detected = "routine"
                for intent in predicted_intents:
                    clinical_context = intent.get("clinical_context", "").lower()
                    time_likelihood = intent.get("time_likelihood", "").lower()
                    
                    if any(word in clinical_context or word in time_likelihood 
                           for word in ["emergency", "urgent", "immediate", "critical"]):
                        urgency_detected = "emergency"
                        break
                
                scenario_details["detected_urgency"] = urgency_detected
                scenario_details["urgency_match"] = urgency_detected == scenario["expected_urgency"]
                scenario_details["processing_time_ms"] = data.get("processing_time_ms", 0)
                
                if not scenario_details["urgency_match"]:
                    scenario_success = False
            
            else:
                scenario_details["error"] = result["data"].get("error", "Unknown error")
            
            validation_results.append(scenario_details)
            
            if not scenario_success:
                all_success = False
        
        # Calculate clinical appropriateness rate
        successful_scenarios = [r for r in validation_results if r.get("urgency_match", False)]
        clinical_appropriateness_rate = len(successful_scenarios) / len(validation_results) if validation_results else 0
        
        self.results.append(TestResult(
            test_name="Clinical Validation Scenarios",
            success=all_success and clinical_appropriateness_rate >= 0.95,  # >95% target
            response_time_ms=statistics.mean([r.get("processing_time_ms", 0) for r in validation_results if r.get("processing_time_ms", 0) > 0]),
            details={
                "scenarios": validation_results,
                "clinical_appropriateness_rate": clinical_appropriateness_rate,
                "total_scenarios": len(validation_results),
                "successful_scenarios": len(successful_scenarios)
            },
            error_message=None if all_success else f"Clinical appropriateness rate: {clinical_appropriateness_rate:.1%}"
        ))
        
        return all_success and clinical_appropriateness_rate >= 0.95
    
    async def run_comprehensive_tests(self):
        """Run all Week 4 comprehensive tests"""
        print("🚀 Starting Week 4 Comprehensive Testing...")
        print("=" * 80)
        
        await self.setup_session()
        
        try:
            # Run all tests
            tests = [
                self.test_predictive_intent_modeling(),
                self.test_conversation_intelligence(),
                self.test_predictive_modeling_performance(),
                self.test_subspecialty_reasoning(),
                self.test_clinical_validation_scenarios()
            ]
            
            results = await asyncio.gather(*tests, return_exceptions=True)
            
            # Print results
            print("\n" + "=" * 80)
            print("📊 WEEK 4 COMPREHENSIVE TEST RESULTS")
            print("=" * 80)
            
            total_tests = len(self.results)
            passed_tests = sum(1 for r in self.results if r.success)
            success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
            
            print(f"Overall Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests} tests passed)")
            print()
            
            for result in self.results:
                status = "✅ PASS" if result.success else "❌ FAIL"
                print(f"{status} {result.test_name}")
                print(f"   Response Time: {result.response_time_ms:.1f}ms")
                
                if result.error_message:
                    print(f"   Error: {result.error_message}")
                
                # Print key details
                if result.test_name == "Predictive Intent Modeling":
                    details = result.details
                    print(f"   Predicted Intents: {details.get('predicted_intents_count', 0)}")
                    print(f"   Processing Time Target Met: {details.get('processing_time_target_met', False)}")
                    print(f"   Emergency Detection: {details.get('emergency_concern_detected', False)}")
                    print(f"   Algorithm Version: {details.get('algorithm_version', 'unknown')}")
                
                elif result.test_name == "Conversation Intelligence":
                    scenarios = result.details.get("scenarios", [])
                    print(f"   Scenarios Tested: {len(scenarios)}")
                    for scenario in scenarios:
                        print(f"     - {scenario['scenario_name']}: {'✅' if scenario.get('processing_time_target_met', False) else '❌'}")
                
                elif result.test_name == "Predictive Modeling Performance":
                    details = result.details
                    print(f"   Model Accuracy: {details.get('model_accuracy', 0):.1%}")
                    print(f"   Accuracy Target Met: {details.get('accuracy_target_met', False)}")
                    print(f"   Operational Status: {details.get('operational_status', False)}")
                
                elif result.test_name == "Subspecialty Clinical Reasoning":
                    subspecialty_tests = result.details.get("subspecialty_tests", [])
                    print(f"   Subspecialties Tested: {len(subspecialty_tests)}")
                    for test in subspecialty_tests:
                        print(f"     - {test['subspecialty']}: {'✅' if test.get('processing_time_target_met', False) else '❌'}")
                
                elif result.test_name == "Clinical Validation Scenarios":
                    details = result.details
                    print(f"   Clinical Appropriateness Rate: {details.get('clinical_appropriateness_rate', 0):.1%}")
                    print(f"   Scenarios: {details.get('successful_scenarios', 0)}/{details.get('total_scenarios', 0)}")
                
                print()
            
            # Performance summary
            print("🎯 PERFORMANCE SUMMARY")
            print("-" * 40)
            
            processing_times = [r.response_time_ms for r in self.results if r.response_time_ms > 0]
            if processing_times:
                avg_time = statistics.mean(processing_times)
                max_time = max(processing_times)
                min_time = min(processing_times)
                
                print(f"Average Response Time: {avg_time:.1f}ms")
                print(f"Max Response Time: {max_time:.1f}ms")
                print(f"Min Response Time: {min_time:.1f}ms")
                print(f"<25ms Target Met: {'✅' if avg_time < 25 else '❌'}")
            
            print()
            
            # Final assessment
            print("🏆 FINAL ASSESSMENT")
            print("-" * 40)
            
            if success_rate >= 90:
                print("✅ WEEK 4 COMPONENTS ARE PRODUCTION-READY")
                print("   All critical functionality validated successfully")
            elif success_rate >= 75:
                print("⚠️  WEEK 4 COMPONENTS MOSTLY FUNCTIONAL")
                print("   Minor issues identified, but core functionality working")
            else:
                print("❌ WEEK 4 COMPONENTS NEED ATTENTION")
                print("   Significant issues found requiring fixes")
            
            return success_rate >= 75
            
        finally:
            await self.cleanup_session()

async def main():
    """Main test execution"""
    tester = Week4ComprehensiveTester()
    success = await tester.run_comprehensive_tests()
    
    if success:
        print("\n🎉 Week 4 comprehensive testing completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Week 4 comprehensive testing failed!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())