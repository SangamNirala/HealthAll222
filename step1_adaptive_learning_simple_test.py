#!/usr/bin/env python3
"""
🧠 STEP 1 ADAPTIVE LEARNING ENGINE - SIMPLIFIED BACKEND TESTING
==============================================================

Simplified synchronous testing of the Step 1 Adaptive Learning & Personalization Engine
for the Quick Health Tracking chatbot.

TESTING SCOPE - 4 NEW API ENDPOINTS:
1. POST /api/medical-ai/adaptive-learning/update-patient-profile
2. GET /api/medical-ai/adaptive-learning/patient-insights/{patient_id}
3. POST /api/medical-ai/adaptive-learning/feedback-integration
4. GET /api/medical-ai/adaptive-learning/learning-analytics
"""

import json
import time
import requests
import sys
import os
from datetime import datetime
import uuid

# Test configuration
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://symptom-analyzer-6.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class AdaptiveLearningTester:
    """Simplified tester for Step 1 Adaptive Learning & Personalization Engine"""
    
    def __init__(self):
        self.test_results = []
        self.performance_metrics = []
        
        # Generate test patient IDs for consistent testing
        self.test_patient_ids = [
            f"test_patient_{uuid.uuid4().hex[:8]}",
            f"test_patient_{uuid.uuid4().hex[:8]}",
            f"test_patient_{uuid.uuid4().hex[:8]}"
        ]
        
        print("🚀 STEP 1 ADAPTIVE LEARNING ENGINE TESTING INITIALIZED")
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test Patient IDs: {self.test_patient_ids}")
        print("=" * 80)

    def log_test_result(self, test_name: str, success: bool, details: str, performance_ms: float = 0):
        """Log test result with performance metrics"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            'test_name': test_name,
            'success': success,
            'details': details,
            'performance_ms': performance_ms,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.test_results.append(result)
        
        if performance_ms > 0:
            self.performance_metrics.append({
                'test': test_name,
                'processing_time_ms': performance_ms,
                'meets_target': performance_ms < 15.0
            })
        
        print(f"{status} {test_name}")
        print(f"   Details: {details}")
        if performance_ms > 0:
            target_status = "✅ MEETS TARGET" if performance_ms < 15.0 else "⚠️ EXCEEDS TARGET"
            print(f"   Performance: {performance_ms:.2f}ms {target_status}")
        print()

    def test_update_patient_profile_endpoint(self):
        """Test POST /api/medical-ai/adaptive-learning/update-patient-profile"""
        print("🧠 TESTING: Update Patient Profile Endpoint")
        print("-" * 50)
        
        test_scenarios = [
            {
                "name": "Formal Technical Communication Style",
                "patient_id": self.test_patient_ids[0],
                "interaction_data": {
                    "message": "I am experiencing severe chest pain with radiating discomfort to my left arm. Could you please provide a comprehensive assessment of my cardiovascular symptoms?",
                    "context": {"stage": "chief_complaint", "urgency": "emergency"},
                    "response_data": {"confidence": 0.92, "intent": "emergency_detection"},
                    "processing_time_ms": 12.5
                }
            },
            {
                "name": "Casual Simple Communication Style",
                "patient_id": self.test_patient_ids[1],
                "interaction_data": {
                    "message": "hey doc, my head hurts really bad and i feel sick",
                    "context": {"stage": "chief_complaint", "urgency": "routine"},
                    "response_data": {"confidence": 0.78, "intent": "symptom_assessment"},
                    "processing_time_ms": 8.3
                }
            },
            {
                "name": "Mixed Communication Style with Medical History",
                "patient_id": self.test_patient_ids[2],
                "interaction_data": {
                    "message": "I've been having these episodes of shortness of breath, especially when I exercise. My family has a history of heart problems.",
                    "context": {"stage": "history_present_illness", "urgency": "moderate"},
                    "response_data": {"confidence": 0.85, "intent": "cardiovascular_assessment"},
                    "processing_time_ms": 11.7
                }
            }
        ]
        
        for scenario in test_scenarios:
            try:
                start_time = time.time()
                
                response = requests.post(
                    f"{API_BASE}/medical-ai/adaptive-learning/update-patient-profile",
                    json={
                        "patient_id": scenario["patient_id"],
                        "interaction_data": scenario["interaction_data"]
                    },
                    timeout=30
                )
                
                processing_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate response structure
                    required_fields = [
                        "status", "patient_id", "learning_applied", "profile_updated",
                        "adaptation_profile", "personalization_weights", "processing_time_ms",
                        "performance_target_met", "algorithm_version"
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if not missing_fields:
                        # Validate adaptation profile structure
                        adaptation_profile = data.get("adaptation_profile", {})
                        profile_fields = ["communication_style", "personalization_level", "confidence_score", "interaction_count"]
                        profile_complete = all(field in adaptation_profile for field in profile_fields)
                        
                        # Check performance target
                        backend_processing_time = data.get("processing_time_ms", 0)
                        performance_target_met = data.get("performance_target_met", False)
                        
                        # Validate algorithm version
                        algorithm_version = data.get("algorithm_version")
                        correct_version = algorithm_version == "1.0_adaptive_learning_foundation"
                        
                        if profile_complete and correct_version:
                            self.log_test_result(
                                f"Update Patient Profile - {scenario['name']}",
                                True,
                                f"Profile updated successfully. Style: {adaptation_profile.get('communication_style')}, "
                                f"Level: {adaptation_profile.get('personalization_level')}, "
                                f"Confidence: {adaptation_profile.get('confidence_score'):.3f}, "
                                f"Backend Processing: {backend_processing_time:.2f}ms",
                                backend_processing_time
                            )
                        else:
                            self.log_test_result(
                                f"Update Patient Profile - {scenario['name']}",
                                False,
                                f"Response validation failed. Profile complete: {profile_complete}, "
                                f"Correct version: {correct_version}",
                                processing_time
                            )
                    else:
                        self.log_test_result(
                            f"Update Patient Profile - {scenario['name']}",
                            False,
                            f"Missing required fields: {missing_fields}",
                            processing_time
                        )
                else:
                    self.log_test_result(
                        f"Update Patient Profile - {scenario['name']}",
                        False,
                        f"HTTP {response.status_code}: {response.text[:200]}",
                        processing_time
                    )
                    
            except Exception as e:
                self.log_test_result(
                    f"Update Patient Profile - {scenario['name']}",
                    False,
                    f"Exception: {str(e)[:200]}"
                )

    def test_patient_insights_endpoint(self):
        """Test GET /api/medical-ai/adaptive-learning/patient-insights/{patient_id}"""
        print("👤 TESTING: Patient Insights Endpoint")
        print("-" * 50)
        
        for i, patient_id in enumerate(self.test_patient_ids):
            try:
                start_time = time.time()
                
                response = requests.get(
                    f"{API_BASE}/medical-ai/adaptive-learning/patient-insights/{patient_id}",
                    timeout=30
                )
                
                processing_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate response structure
                    required_fields = ["patient_id", "insights", "learning_metrics", "personalization_status"]
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if not missing_fields:
                        # Validate insights structure
                        insights = data.get("insights", {})
                        insights_fields = ["profile_summary", "communication_insights", "ai_generated_insights", "adaptive_capabilities"]
                        insights_complete = all(field in insights for field in insights_fields)
                        
                        # Validate learning metrics
                        learning_metrics = data.get("learning_metrics", {})
                        metrics_fields = ["learning_progress", "pattern_recognition_quality", "confidence_calibration", "interaction_efficiency"]
                        metrics_complete = all(field in learning_metrics for field in metrics_fields)
                        
                        # Validate personalization status
                        personalization_status = data.get("personalization_status", {})
                        status_fields = ["system_status", "performance_metrics", "configuration"]
                        status_complete = all(field in personalization_status for field in status_fields)
                        
                        if insights_complete and metrics_complete and status_complete:
                            # Extract key metrics for validation
                            ai_insights_count = len(insights.get("ai_generated_insights", []))
                            adaptive_capabilities = insights.get("adaptive_capabilities", {})
                            
                            self.log_test_result(
                                f"Patient Insights - Patient {i+1}",
                                True,
                                f"Comprehensive insights retrieved. AI insights: {ai_insights_count}, "
                                f"Style adaptation: {adaptive_capabilities.get('style_adaptation_active', False)}, "
                                f"Intent weighting: {adaptive_capabilities.get('intent_weighting_personalized', False)}, "
                                f"Learning feedback: {adaptive_capabilities.get('learning_feedback_integrated', False)}",
                                processing_time
                            )
                        else:
                            self.log_test_result(
                                f"Patient Insights - Patient {i+1}",
                                False,
                                f"Response structure validation failed. Insights: {insights_complete}, "
                                f"Metrics: {metrics_complete}, Status: {status_complete}",
                                processing_time
                            )
                    else:
                        self.log_test_result(
                            f"Patient Insights - Patient {i+1}",
                            False,
                            f"Missing required fields: {missing_fields}",
                            processing_time
                        )
                        
                elif response.status_code == 404:
                    # Expected for new patients - this is acceptable
                    self.log_test_result(
                        f"Patient Insights - Patient {i+1}",
                        True,
                        "Patient not found (expected for new patient) - proper 404 handling",
                        processing_time
                    )
                else:
                    self.log_test_result(
                        f"Patient Insights - Patient {i+1}",
                        False,
                        f"HTTP {response.status_code}: {response.text[:200]}",
                        processing_time
                    )
                    
            except Exception as e:
                self.log_test_result(
                    f"Patient Insights - Patient {i+1}",
                    False,
                    f"Exception: {str(e)[:200]}"
                )

    def test_feedback_integration_endpoint(self):
        """Test POST /api/medical-ai/adaptive-learning/feedback-integration"""
        print("🔄 TESTING: Feedback Integration Endpoint")
        print("-" * 50)
        
        feedback_scenarios = [
            {
                "name": "Successful Emergency Detection Feedback",
                "patient_id": self.test_patient_ids[0],
                "conversation_id": f"conv_{uuid.uuid4().hex[:8]}",
                "feedback_data": {
                    "user_satisfaction": 0.95,
                    "response_appropriateness": 0.92,
                    "style_match": 0.88,
                    "technical_level_appropriate": True
                },
                "outcome_data": {
                    "intent_classification_correct": True,
                    "emergency_detected_correctly": True,
                    "conversation_completed": True,
                    "user_followed_recommendations": True,
                    "processing_efficiency": 0.91
                }
            },
            {
                "name": "Style Mismatch Learning Feedback",
                "patient_id": self.test_patient_ids[1],
                "conversation_id": f"conv_{uuid.uuid4().hex[:8]}",
                "feedback_data": {
                    "user_satisfaction": 0.65,
                    "response_appropriateness": 0.70,
                    "style_match": 0.45,  # Low style match for learning
                    "technical_level_appropriate": False
                },
                "outcome_data": {
                    "intent_classification_correct": True,
                    "style_adaptation_needed": True,
                    "conversation_completed": True,
                    "user_requested_simpler_language": True,
                    "processing_efficiency": 0.78
                }
            }
        ]
        
        for scenario in feedback_scenarios:
            try:
                start_time = time.time()
                
                response = requests.post(
                    f"{API_BASE}/medical-ai/adaptive-learning/feedback-integration",
                    json={
                        "patient_id": scenario["patient_id"],
                        "conversation_id": scenario["conversation_id"],
                        "feedback_data": scenario["feedback_data"],
                        "outcome_data": scenario["outcome_data"]
                    },
                    timeout=30
                )
                
                processing_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate response structure
                    required_fields = [
                        "status", "patient_id", "conversation_id", "feedback_integrated",
                        "learning_improvements", "algorithm_updates", "performance_impact",
                        "population_learning"
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if not missing_fields:
                        # Validate learning improvements
                        learning_improvements = data.get("learning_improvements", {})
                        algorithm_updates = data.get("algorithm_updates", {})
                        performance_impact = data.get("performance_impact", {})
                        population_learning = data.get("population_learning", {})
                        
                        # Check key learning indicators
                        feedback_integrated = data.get("feedback_integrated", False)
                        privacy_protection = population_learning.get("privacy_protection_active", False)
                        backend_processing_time = performance_impact.get("processing_time_ms", 0)
                        
                        if feedback_integrated and privacy_protection:
                            self.log_test_result(
                                f"Feedback Integration - {scenario['name']}",
                                True,
                                f"Feedback integrated successfully. Learning enhanced: {learning_improvements.get('personalization_enhanced', False)}, "
                                f"Patterns improved: {algorithm_updates.get('pattern_recognition_improved', False)}, "
                                f"Privacy protected: {privacy_protection}, "
                                f"Backend Processing: {backend_processing_time:.2f}ms",
                                backend_processing_time
                            )
                        else:
                            self.log_test_result(
                                f"Feedback Integration - {scenario['name']}",
                                False,
                                f"Feedback integration validation failed. Integrated: {feedback_integrated}, "
                                f"Privacy: {privacy_protection}",
                                processing_time
                            )
                    else:
                        self.log_test_result(
                            f"Feedback Integration - {scenario['name']}",
                            False,
                            f"Missing required fields: {missing_fields}",
                            processing_time
                        )
                else:
                    self.log_test_result(
                        f"Feedback Integration - {scenario['name']}",
                        False,
                        f"HTTP {response.status_code}: {response.text[:200]}",
                        processing_time
                    )
                    
            except Exception as e:
                self.log_test_result(
                    f"Feedback Integration - {scenario['name']}",
                    False,
                    f"Exception: {str(e)[:200]}"
                )

    def test_learning_analytics_endpoint(self):
        """Test GET /api/medical-ai/adaptive-learning/learning-analytics"""
        print("📊 TESTING: Learning Analytics Endpoint")
        print("-" * 50)
        
        try:
            start_time = time.time()
            
            response = requests.get(
                f"{API_BASE}/medical-ai/adaptive-learning/learning-analytics",
                timeout=30
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ["system_overview", "performance_metrics", "population_insights", "generated_at"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    # Validate system overview
                    system_overview = data.get("system_overview", {})
                    overview_fields = ["total_learning_profiles", "active_learning_sessions", "high_confidence_profiles", "system_maturity"]
                    overview_complete = all(field in system_overview for field in overview_fields)
                    
                    # Validate performance metrics
                    performance_metrics = data.get("performance_metrics", {})
                    metrics_sections = ["adaptive_learning_engine", "personalization_system", "profile_management"]
                    metrics_complete = all(section in performance_metrics for section in metrics_sections)
                    
                    # Validate population insights
                    population_insights = data.get("population_insights", [])
                    insights_valid = isinstance(population_insights, list)
                    
                    # Check adaptive learning engine performance
                    engine_metrics = performance_metrics.get("adaptive_learning_engine", {})
                    avg_processing_time = engine_metrics.get("avg_processing_time_ms", 0)
                    performance_target_achieved = engine_metrics.get("performance_target_achieved", False)
                    
                    if overview_complete and metrics_complete and insights_valid:
                        self.log_test_result(
                            "Learning Analytics - System Overview",
                            True,
                            f"Comprehensive analytics retrieved. Profiles: {system_overview.get('total_learning_profiles', 0)}, "
                            f"Sessions: {system_overview.get('active_learning_sessions', 0)}, "
                            f"High confidence: {system_overview.get('high_confidence_profiles', 0)}, "
                            f"Maturity: {system_overview.get('system_maturity', 'unknown')}, "
                            f"Avg processing: {avg_processing_time:.2f}ms, "
                            f"Target achieved: {performance_target_achieved}",
                            processing_time
                        )
                        
                        # Test population insights privacy protection
                        privacy_protected = True
                        for insight in population_insights:
                            if 'patient_id' in str(insight) or 'personal' in str(insight).lower():
                                privacy_protected = False
                                break
                        
                        self.log_test_result(
                            "Learning Analytics - Privacy Protection",
                            privacy_protected,
                            f"Population insights privacy check. Insights count: {len(population_insights)}, "
                            f"Privacy protected: {privacy_protected}",
                            0
                        )
                        
                    else:
                        self.log_test_result(
                            "Learning Analytics - System Overview",
                            False,
                            f"Response structure validation failed. Overview: {overview_complete}, "
                            f"Metrics: {metrics_complete}, Insights: {insights_valid}",
                            processing_time
                        )
                else:
                    self.log_test_result(
                        "Learning Analytics - System Overview",
                        False,
                        f"Missing required fields: {missing_fields}",
                        processing_time
                    )
            else:
                self.log_test_result(
                    "Learning Analytics - System Overview",
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    processing_time
                )
                
        except Exception as e:
            self.log_test_result(
                "Learning Analytics - System Overview",
                False,
                f"Exception: {str(e)[:200]}"
            )

    def test_integration_with_existing_system(self):
        """Test integration with existing medical AI system"""
        print("🔗 TESTING: Integration with Existing Medical AI System")
        print("-" * 50)
        
        # Test that adaptive learning endpoints don't interfere with existing medical AI
        try:
            start_time = time.time()
            
            # Test existing medical AI initialization endpoint
            response = requests.post(
                f"{API_BASE}/medical-ai/initialize",
                json={"patient_id": "integration_test_patient"},
                timeout=30
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                # Check that existing functionality still works
                required_fields = ["consultation_id", "patient_id", "current_stage", "response"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    self.log_test_result(
                        "Integration - Existing Medical AI Compatibility",
                        True,
                        f"Existing medical AI initialization works correctly. "
                        f"Consultation ID: {data.get('consultation_id', 'N/A')[:16]}..., "
                        f"Stage: {data.get('current_stage', 'N/A')}",
                        processing_time
                    )
                else:
                    self.log_test_result(
                        "Integration - Existing Medical AI Compatibility",
                        False,
                        f"Existing medical AI missing fields: {missing_fields}",
                        processing_time
                    )
            else:
                self.log_test_result(
                    "Integration - Existing Medical AI Compatibility",
                    False,
                    f"Existing medical AI failed: HTTP {response.status_code}",
                    processing_time
                )
                
        except Exception as e:
            self.log_test_result(
                "Integration - Existing Medical AI Compatibility",
                False,
                f"Integration test exception: {str(e)[:200]}"
            )

    def run_comprehensive_tests(self):
        """Run all comprehensive tests for Step 1 Adaptive Learning Engine"""
        print("🚀 STARTING COMPREHENSIVE STEP 1 ADAPTIVE LEARNING ENGINE TESTING")
        print("=" * 80)
        
        # Run all test suites
        self.test_update_patient_profile_endpoint()
        self.test_patient_insights_endpoint()
        self.test_feedback_integration_endpoint()
        self.test_learning_analytics_endpoint()
        self.test_integration_with_existing_system()
        
        # Generate comprehensive test report
        self.generate_test_report()

    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("📊 COMPREHENSIVE TEST REPORT - STEP 1 ADAPTIVE LEARNING ENGINE")
        print("=" * 80)
        
        # Calculate overall statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"📈 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        # Performance analysis
        if self.performance_metrics:
            processing_times = [metric['processing_time_ms'] for metric in self.performance_metrics]
            avg_time = sum(processing_times) / len(processing_times)
            target_met_count = sum(1 for metric in self.performance_metrics if metric['meets_target'])
            target_met_percentage = (target_met_count / len(self.performance_metrics)) * 100
            
            print(f"⚡ PERFORMANCE ANALYSIS:")
            print(f"   Average Processing Time: {avg_time:.2f}ms")
            print(f"   <15ms Target Met: {target_met_percentage:.1f}% of tests")
            print(f"   Fastest Test: {min(processing_times):.2f}ms")
            print(f"   Slowest Test: {max(processing_times):.2f}ms")
            print()
        
        # Endpoint-specific results
        print(f"🔍 ENDPOINT-SPECIFIC RESULTS:")
        
        endpoint_groups = {
            "Update Patient Profile": [r for r in self.test_results if "Update Patient Profile" in r['test_name']],
            "Patient Insights": [r for r in self.test_results if "Patient Insights" in r['test_name']],
            "Feedback Integration": [r for r in self.test_results if "Feedback Integration" in r['test_name']],
            "Learning Analytics": [r for r in self.test_results if "Learning Analytics" in r['test_name']],
            "Integration": [r for r in self.test_results if "Integration" in r['test_name']]
        }
        
        for endpoint, results in endpoint_groups.items():
            if results:
                passed = sum(1 for r in results if r['success'])
                total = len(results)
                rate = (passed / total) * 100 if total > 0 else 0
                status = "✅ PASS" if rate >= 80 else "⚠️ PARTIAL" if rate >= 60 else "❌ FAIL"
                print(f"   {endpoint}: {passed}/{total} ({rate:.1f}%) {status}")
        
        print()
        
        # Critical issues
        critical_failures = [r for r in self.test_results if not r['success'] and any(keyword in r['test_name'] for keyword in ["Update Patient Profile", "Learning Analytics"])]
        
        if critical_failures:
            print(f"🚨 CRITICAL ISSUES:")
            for failure in critical_failures:
                print(f"   ❌ {failure['test_name']}: {failure['details'][:100]}...")
            print()
        
        # Success highlights
        key_successes = [r for r in self.test_results if r['success'] and any(keyword in r['test_name'] for keyword in ["Update Patient Profile", "Learning Analytics", "Integration"])]
        
        if key_successes:
            print(f"🎉 KEY SUCCESSES:")
            for success in key_successes[:5]:  # Show top 5
                print(f"   ✅ {success['test_name']}")
            print()
        
        # Final assessment
        if success_rate >= 90:
            assessment = "🎯 EXCELLENT - Step 1 Adaptive Learning Engine is production-ready"
        elif success_rate >= 80:
            assessment = "✅ GOOD - Step 1 Adaptive Learning Engine is functional with minor issues"
        elif success_rate >= 70:
            assessment = "⚠️ ACCEPTABLE - Step 1 Adaptive Learning Engine needs improvements"
        else:
            assessment = "❌ NEEDS WORK - Step 1 Adaptive Learning Engine has significant issues"
        
        print(f"🏆 FINAL ASSESSMENT: {assessment}")
        print(f"📊 Overall Success Rate: {success_rate:.1f}%")
        
        if self.performance_metrics:
            avg_performance = sum(metric['processing_time_ms'] for metric in self.performance_metrics) / len(self.performance_metrics)
            performance_status = "✅ MEETS TARGET" if avg_performance < 15.0 else "⚠️ EXCEEDS TARGET"
            print(f"⚡ Performance Status: {avg_performance:.2f}ms average {performance_status}")
        
        print("=" * 80)

def main():
    """Main test execution function"""
    tester = AdaptiveLearningTester()
    tester.run_comprehensive_tests()

if __name__ == "__main__":
    main()