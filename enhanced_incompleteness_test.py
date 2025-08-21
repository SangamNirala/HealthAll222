#!/usr/bin/env python3
"""
🧠 ENHANCED INCOMPLETENESS DETECTION SYSTEM COMPREHENSIVE TESTING
Testing the Revolutionary Enhanced Incompleteness Detection System for Medical AI

This test validates all components of the Enhanced Incompleteness Detection System
as requested in the review request.
"""

import requests
import json
import time
from typing import Dict, Any, List

# Backend URL from frontend environment
BACKEND_URL = "https://healthchat-genius.preview.emergentagent.com/api"

class EnhancedIncompletenessDetectionTester:
    """Comprehensive tester for Enhanced Incompleteness Detection System"""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        result = f"{status} - {test_name}"
        if details:
            result += f": {details}"
        
        self.test_results.append(result)
        print(result)
    
    def test_incompleteness_detection_endpoint(self, scenario_name: str, request_data: Dict[str, Any], expected_features: List[str]) -> bool:
        """Test incompleteness detection endpoint with specific scenario"""
        try:
            start_time = time.time()
            
            response = requests.post(
                f"{BACKEND_URL}/medical-ai/incompleteness-detection/analyze",
                json=request_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            processing_time = (time.time() - start_time) * 1000  # Convert to ms
            
            if response.status_code != 200:
                self.log_test(f"Incompleteness Detection - {scenario_name}", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            data = response.json()
            
            # Validate response structure
            required_fields = [
                "success", "patient_communication_profile", "incompleteness_score",
                "priority_gaps", "adaptive_strategy", "immediate_follow_ups",
                "processing_time_ms", "analysis_confidence", "algorithm_version"
            ]
            
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                self.log_test(f"Incompleteness Detection - {scenario_name}", False,
                            f"Missing fields: {missing_fields}")
                return False
            
            # Validate processing time requirement (<50ms)
            if processing_time > 50:
                self.log_test(f"Incompleteness Detection - {scenario_name} Performance", False,
                            f"Processing time {processing_time:.1f}ms exceeds 50ms requirement")
                return False
            
            # Validate analysis confidence (>0.6)
            if data.get("analysis_confidence", 0) < 0.6:
                self.log_test(f"Incompleteness Detection - {scenario_name} Confidence", False,
                            f"Analysis confidence {data.get('analysis_confidence')} below 0.6 requirement")
                return False
            
            # Validate incompleteness types detection
            detected_gaps = data.get("priority_gaps", [])
            gap_types = [gap.get("gap_type", "") for gap in detected_gaps]
            
            # Check for expected incompleteness types
            expected_types = ["linguistic", "medical_reasoning", "psychological", "cultural", "temporal"]
            detected_expected = any(gap_type in expected_types for gap_type in gap_types)
            
            if not detected_expected and len(detected_gaps) == 0:
                self.log_test(f"Incompleteness Detection - {scenario_name} Gap Detection", False,
                            "No incompleteness gaps detected when expected")
                return False
            
            # Validate patient communication profile
            profile = data.get("patient_communication_profile", {})
            profile_fields = ["communication_style", "anxiety_level", "detail_preference", "empathy_needs"]
            missing_profile_fields = [field for field in profile_fields if field not in profile]
            
            if missing_profile_fields:
                self.log_test(f"Incompleteness Detection - {scenario_name} Profile", False,
                            f"Missing profile fields: {missing_profile_fields}")
                return False
            
            # Validate adaptive strategy
            strategy = data.get("adaptive_strategy", {})
            strategy_fields = ["approach_type", "question_style", "empathy_level"]
            missing_strategy_fields = [field for field in strategy_fields if field not in strategy]
            
            if missing_strategy_fields:
                self.log_test(f"Incompleteness Detection - {scenario_name} Strategy", False,
                            f"Missing strategy fields: {missing_strategy_fields}")
                return False
            
            # Validate immediate follow-ups
            follow_ups = data.get("immediate_follow_ups", [])
            if len(follow_ups) == 0:
                self.log_test(f"Incompleteness Detection - {scenario_name} Follow-ups", False,
                            "No immediate follow-up questions generated")
                return False
            
            self.log_test(f"Incompleteness Detection - {scenario_name}", True,
                        f"Processing: {processing_time:.1f}ms, Confidence: {data.get('analysis_confidence'):.2f}, Gaps: {len(detected_gaps)}, Follow-ups: {len(follow_ups)}")
            return True
            
        except requests.exceptions.RequestException as e:
            self.log_test(f"Incompleteness Detection - {scenario_name}", False, f"Request error: {str(e)}")
            return False
        except Exception as e:
            self.log_test(f"Incompleteness Detection - {scenario_name}", False, f"Error: {str(e)}")
            return False
    
    def test_system_performance_endpoint(self) -> bool:
        """Test system performance endpoint"""
        try:
            response = requests.get(
                f"{BACKEND_URL}/medical-ai/incompleteness-detection/system-performance",
                timeout=10
            )
            
            if response.status_code != 200:
                self.log_test("System Performance API", False, f"HTTP {response.status_code}")
                return False
            
            data = response.json()
            
            # Validate response structure
            required_fields = ["system_capabilities", "performance_metrics", "algorithm_version", "integration_status"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                self.log_test("System Performance API", False, f"Missing fields: {missing_fields}")
                return False
            
            self.log_test("System Performance API", True, 
                        f"Algorithm: {data.get('algorithm_version')}, Status: {data.get('integration_status')}")
            return True
            
        except Exception as e:
            self.log_test("System Performance API", False, f"Error: {str(e)}")
            return False
    
    def test_medical_ai_integration(self) -> bool:
        """Test integration with main medical AI conversation flow"""
        try:
            # Test medical AI initialization
            init_response = requests.post(
                f"{BACKEND_URL}/medical-ai/initialize",
                json={"user_id": "test-patient-incompleteness", "session_type": "consultation"},
                timeout=10
            )
            
            if init_response.status_code != 200:
                self.log_test("Medical AI Integration - Initialize", False, f"HTTP {init_response.status_code}")
                return False
            
            session_data = init_response.json()
            session_id = session_data.get("session_id")
            
            if not session_id:
                self.log_test("Medical AI Integration - Initialize", False, "No session_id returned")
                return False
            
            # Test medical AI message with vague patient input
            message_response = requests.post(
                f"{BACKEND_URL}/medical-ai/message",
                json={
                    "session_id": session_id,
                    "message": "I hurt",
                    "user_id": "test-patient-incompleteness"
                },
                timeout=15
            )
            
            if message_response.status_code != 200:
                self.log_test("Medical AI Integration - Message", False, f"HTTP {message_response.status_code}")
                return False
            
            message_data = message_response.json()
            
            # Check if incompleteness analysis is included in response context
            context = message_data.get("context", {})
            has_incompleteness_analysis = "incompleteness_analysis" in context
            
            if not has_incompleteness_analysis:
                self.log_test("Medical AI Integration - Incompleteness Context", False, 
                            "No incompleteness_analysis in response context")
                return False
            
            self.log_test("Medical AI Integration", True, 
                        f"Session: {session_id}, Incompleteness analysis integrated")
            return True
            
        except Exception as e:
            self.log_test("Medical AI Integration", False, f"Error: {str(e)}")
            return False
    
    def run_comprehensive_tests(self):
        """Run all comprehensive tests for Enhanced Incompleteness Detection System"""
        print("🧠 ENHANCED INCOMPLETENESS DETECTION SYSTEM COMPREHENSIVE TESTING")
        print("=" * 80)
        
        # Test Scenario 1: Reserved Patient with Linguistic Incompleteness
        scenario_1 = {
            "patient_message": "I hurt",
            "conversation_context": {"messages": [], "topic": "medical_consultation"},
            "medical_context": {"chief_complaint": "", "current_symptoms": {}},
            "analysis_depth": "comprehensive"
        }
        self.test_incompleteness_detection_endpoint("Reserved Patient - Linguistic", scenario_1, 
                                                  ["linguistic", "vague_description"])
        
        # Test Scenario 2: Anxious Patient with Medical Reasoning Incompleteness
        scenario_2 = {
            "patient_message": "I'm so worried about this chest pain, what if it's my heart?",
            "conversation_context": {"messages": [{"role": "patient", "content": "chest pain"}]},
            "medical_context": {"chief_complaint": "chest pain", "current_symptoms": {"chest_pain": True}},
            "analysis_depth": "comprehensive"
        }
        self.test_incompleteness_detection_endpoint("Anxious Patient - Medical Reasoning", scenario_2,
                                                  ["medical_reasoning", "OLDCARTS"])
        
        # Test Scenario 3: Detailed Patient with Complete Information
        scenario_3 = {
            "patient_message": "I've been having a sharp, stabbing chest pain that started suddenly 2 hours ago on the left side, worse when I breathe deeply, with no radiation to arms, no shortness of breath, rate it 7/10, nothing makes it better, aspirin didn't help",
            "conversation_context": {"messages": []},
            "medical_context": {"chief_complaint": "chest pain"},
            "analysis_depth": "comprehensive"
        }
        self.test_incompleteness_detection_endpoint("Detailed Patient - Complete Info", scenario_3,
                                                  ["minimal_incompleteness"])
        
        # Test Scenario 4: Psychological Incompleteness Detection
        scenario_4 = {
            "patient_message": "Everything is fine, just some stomach issues, nothing serious",
            "conversation_context": {"messages": [{"role": "patient", "content": "I'm embarrassed"}, {"role": "doctor", "content": "What's bothering you?"}]},
            "medical_context": {"chief_complaint": "stomach issues"},
            "analysis_depth": "comprehensive"
        }
        self.test_incompleteness_detection_endpoint("Psychological Barriers", scenario_4,
                                                  ["psychological", "embarrassment"])
        
        # Test Scenario 5: Multi-dimensional Incompleteness
        scenario_5 = {
            "patient_message": "Been feeling off lately, maybe it's stress",
            "conversation_context": {"messages": []},
            "medical_context": {"chief_complaint": "feeling off"},
            "analysis_depth": "comprehensive"
        }
        self.test_incompleteness_detection_endpoint("Multi-dimensional Incompleteness", scenario_5,
                                                  ["temporal", "linguistic", "medical_reasoning"])
        
        # Test System Performance Endpoint
        self.test_system_performance_endpoint()
        
        # Test Medical AI Integration
        self.test_medical_ai_integration()
        
        # Performance Validation Tests
        self.test_performance_requirements()
        
        # Print Summary
        print("\n" + "=" * 80)
        print("🎯 ENHANCED INCOMPLETENESS DETECTION SYSTEM TEST SUMMARY")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT: Enhanced Incompleteness Detection System is production-ready!")
        elif success_rate >= 75:
            print("✅ GOOD: System is functional with minor issues")
        elif success_rate >= 50:
            print("⚠️ MODERATE: System needs improvements")
        else:
            print("❌ CRITICAL: System requires major fixes")
        
        print("\nDetailed Results:")
        for result in self.test_results:
            print(f"  {result}")
        
        return success_rate >= 75
    
    def test_performance_requirements(self):
        """Test specific performance requirements"""
        print("\n📊 PERFORMANCE VALIDATION TESTS")
        print("-" * 50)
        
        # Test processing time with multiple scenarios
        test_scenarios = [
            {"patient_message": "I have a headache", "analysis_depth": "basic"},
            {"patient_message": "My chest hurts when I breathe", "analysis_depth": "standard"},
            {"patient_message": "I've been experiencing intermittent abdominal pain for the past week", "analysis_depth": "comprehensive"}
        ]
        
        processing_times = []
        
        for i, scenario in enumerate(test_scenarios):
            try:
                start_time = time.time()
                response = requests.post(
                    f"{BACKEND_URL}/medical-ai/incompleteness-detection/analyze",
                    json=scenario,
                    timeout=10
                )
                processing_time = (time.time() - start_time) * 1000
                processing_times.append(processing_time)
                
                if response.status_code == 200:
                    data = response.json()
                    confidence = data.get("analysis_confidence", 0)
                    
                    # Validate performance requirements
                    time_ok = processing_time < 50
                    confidence_ok = confidence > 0.6
                    
                    self.log_test(f"Performance Test {i+1}", time_ok and confidence_ok,
                                f"Time: {processing_time:.1f}ms, Confidence: {confidence:.2f}")
                else:
                    self.log_test(f"Performance Test {i+1}", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Performance Test {i+1}", False, f"Error: {str(e)}")
        
        # Calculate average processing time
        if processing_times:
            avg_time = sum(processing_times) / len(processing_times)
            self.log_test("Average Processing Time", avg_time < 50, f"{avg_time:.1f}ms")

if __name__ == "__main__":
    tester = EnhancedIncompletenessDetectionTester()
    success = tester.run_comprehensive_tests()
    
    if success:
        print("\n🎉 ENHANCED INCOMPLETENESS DETECTION SYSTEM: COMPREHENSIVE TESTING SUCCESSFUL")
    else:
        print("\n❌ ENHANCED INCOMPLETENESS DETECTION SYSTEM: TESTING FAILED - REQUIRES ATTENTION")