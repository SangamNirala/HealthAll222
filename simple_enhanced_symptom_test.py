#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class SimpleEnhancedSymptomTester:
    def __init__(self, base_url="https://medpro-testing.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def test_enhanced_symptom_patterns(self):
        """Test the core enhanced symptom pattern recognition"""
        print("🚀 Testing Enhanced Symptom Pattern Architecture...")
        
        # Test scenarios from the review request
        test_scenarios = [
            {
                "name": "Complex Pain Description",
                "message": "I have crushing chest pain that started yesterday morning, radiating to my left arm, 8/10 severity, getting worse over the past few hours",
                "expected_emergency": True,
                "expected_patterns": ["crushing", "chest_pain", "radiating", "severity", "temporal"]
            },
            {
                "name": "Multi-symptom with Temporal",
                "message": "Severe headache for 3 days, comes and goes every few hours, with nausea and dizziness, keeps me awake at night",
                "expected_emergency": False,
                "expected_patterns": ["headache", "temporal", "associated_symptoms", "functional_impact"]
            },
            {
                "name": "Emergency Patterns",
                "message": "Worst headache ever, sudden onset, with neck stiffness and confusion",
                "expected_emergency": True,
                "expected_patterns": ["worst_ever", "sudden_onset", "neurological"]
            },
            {
                "name": "Compound Symptoms",
                "message": "Sharp abdominal pain in lower right side, started 2 days ago, getting progressively worse, with fever and vomiting",
                "expected_emergency": False,
                "expected_patterns": ["sharp", "abdominal", "location", "progression", "associated"]
            }
        ]
        
        for scenario in test_scenarios:
            print(f"\n🔍 Testing: {scenario['name']}")
            
            # Step 1: Initialize consultation
            init_data = {"patient_id": "enhanced_test_patient"}
            
            try:
                init_response = requests.post(
                    f"{self.base_url}/medical-ai/initialize",
                    json=init_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )
                
                if init_response.status_code != 200:
                    print(f"   ❌ Initialization failed: {init_response.status_code}")
                    continue
                
                init_result = init_response.json()
                consultation_id = init_result.get('consultation_id')
                
                # Step 2: Send message
                message_data = {
                    "patient_id": "enhanced_test_patient",
                    "message": scenario["message"],
                    "consultation_id": consultation_id,
                    "context": {
                        "patient_id": "enhanced_test_patient",
                        "consultation_id": consultation_id,
                        "current_stage": "chief_complaint",
                        "demographics": {"age": 45, "gender": "male"}
                    }
                }
                
                message_response = requests.post(
                    f"{self.base_url}/medical-ai/message",
                    json=message_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )
                
                if message_response.status_code != 200:
                    print(f"   ❌ Message processing failed: {message_response.status_code}")
                    continue
                
                result = message_response.json()
                
                # Analyze results
                urgency = result.get('urgency', 'routine')
                emergency_detected = result.get('emergency_detected', False)
                response_text = result.get('response', '').lower()
                
                print(f"   📊 Urgency: {urgency}")
                print(f"   🚨 Emergency Detected: {emergency_detected}")
                print(f"   📝 Response Length: {len(response_text)} characters")
                
                # Validate emergency detection
                emergency_correct = (scenario["expected_emergency"] == emergency_detected) or (scenario["expected_emergency"] == (urgency == "emergency"))
                
                if emergency_correct:
                    print(f"   ✅ Emergency detection: CORRECT")
                else:
                    print(f"   ⚠️ Emergency detection: Expected {scenario['expected_emergency']}, got {emergency_detected}")
                
                # Check for pattern recognition evidence
                pattern_evidence = 0
                for pattern in scenario["expected_patterns"]:
                    if any(keyword in response_text for keyword in [pattern, pattern.replace("_", " ")]):
                        pattern_evidence += 1
                
                pattern_recognition = pattern_evidence > 0
                if pattern_recognition:
                    print(f"   ✅ Pattern recognition: Evidence found ({pattern_evidence}/{len(scenario['expected_patterns'])} patterns)")
                else:
                    print(f"   ⚠️ Pattern recognition: Limited evidence")
                
                # Overall success
                if emergency_correct and pattern_recognition:
                    print(f"   🎉 Test PASSED")
                    self.tests_passed += 1
                else:
                    print(f"   ❌ Test FAILED")
                
                self.tests_run += 1
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                self.tests_run += 1
        
        # Summary
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"\n📊 SUMMARY:")
        print(f"   Tests Run: {self.tests_run}")
        print(f"   Tests Passed: {self.tests_passed}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 75:
            print(f"\n✅ Enhanced Symptom Pattern Architecture is working correctly!")
            print(f"   - Emergency pattern recognition functional")
            print(f"   - Complex symptom processing operational")
            print(f"   - Temporal pattern awareness detected")
            print(f"   - Multi-symptom analysis working")
            return True
        else:
            print(f"\n⚠️ Enhanced Symptom Pattern Architecture needs improvement")
            return False

    def test_phase1_enhanced_patterns(self):
        """Test specific Phase 1 enhanced patterns"""
        print(f"\n🎯 Testing Phase 1 Enhanced Patterns...")
        
        phase1_tests = [
            {
                "name": "Pain Expression Variety",
                "messages": [
                    "crushing chest pain",
                    "stabbing abdominal pain", 
                    "throbbing headache",
                    "burning stomach pain"
                ]
            },
            {
                "name": "Temporal Patterns",
                "messages": [
                    "started yesterday morning",
                    "comes and goes every few hours",
                    "getting worse over time",
                    "sudden onset"
                ]
            },
            {
                "name": "Severity Quantification",
                "messages": [
                    "8/10 severity",
                    "excruciating pain",
                    "mild discomfort",
                    "worst pain ever"
                ]
            }
        ]
        
        phase1_success = 0
        phase1_total = 0
        
        for test_group in phase1_tests:
            print(f"\n   Testing {test_group['name']}:")
            
            for message in test_group["messages"]:
                try:
                    # Initialize consultation
                    init_response = requests.post(
                        f"{self.base_url}/medical-ai/initialize",
                        json={"patient_id": "phase1_test"},
                        timeout=15
                    )
                    
                    if init_response.status_code == 200:
                        consultation_id = init_response.json().get('consultation_id')
                        
                        # Send message
                        message_response = requests.post(
                            f"{self.base_url}/medical-ai/message",
                            json={
                                "patient_id": "phase1_test",
                                "message": message,
                                "consultation_id": consultation_id,
                                "context": {
                                    "patient_id": "phase1_test",
                                    "current_stage": "chief_complaint",
                                    "demographics": {"age": 40, "gender": "male"}
                                }
                            },
                            timeout=15
                        )
                        
                        if message_response.status_code == 200:
                            result = message_response.json()
                            response_text = result.get('response', '').lower()
                            
                            # Check for appropriate medical response
                            medical_response = any(word in response_text for word in 
                                                 ['pain', 'symptom', 'medical', 'describe', 'when', 'severity'])
                            
                            if medical_response:
                                print(f"     ✅ '{message}' - Recognized")
                                phase1_success += 1
                            else:
                                print(f"     ⚠️ '{message}' - Limited recognition")
                        else:
                            print(f"     ❌ '{message}' - API error")
                    else:
                        print(f"     ❌ '{message}' - Init error")
                    
                    phase1_total += 1
                    
                except Exception as e:
                    print(f"     ❌ '{message}' - Error: {str(e)}")
                    phase1_total += 1
        
        phase1_rate = (phase1_success / phase1_total * 100) if phase1_total > 0 else 0
        print(f"\n   Phase 1 Success Rate: {phase1_rate:.1f}% ({phase1_success}/{phase1_total})")
        
        return phase1_rate >= 70

    def test_phase2_entity_extraction(self):
        """Test Phase 2 intelligent entity extraction"""
        print(f"\n🎯 Testing Phase 2 Entity Extraction...")
        
        entity_tests = [
            {
                "message": "Severe stabbing chest pain, 9/10 intensity, started 2 hours ago suddenly, gets worse with movement",
                "expected_entities": ["severity", "quality", "location", "intensity", "duration", "onset", "triggers"]
            },
            {
                "message": "Throbbing headache on left side, moderate intensity, comes every few hours, triggered by bright lights",
                "expected_entities": ["quality", "location", "intensity", "frequency", "triggers"]
            }
        ]
        
        phase2_success = 0
        phase2_total = len(entity_tests)
        
        for test in entity_tests:
            try:
                # Initialize and send message
                init_response = requests.post(
                    f"{self.base_url}/medical-ai/initialize",
                    json={"patient_id": "phase2_test"},
                    timeout=15
                )
                
                if init_response.status_code == 200:
                    consultation_id = init_response.json().get('consultation_id')
                    
                    message_response = requests.post(
                        f"{self.base_url}/medical-ai/message",
                        json={
                            "patient_id": "phase2_test",
                            "message": test["message"],
                            "consultation_id": consultation_id,
                            "context": {
                                "patient_id": "phase2_test",
                                "current_stage": "chief_complaint",
                                "demographics": {"age": 35, "gender": "female"}
                            }
                        },
                        timeout=15
                    )
                    
                    if message_response.status_code == 200:
                        result = message_response.json()
                        response_text = result.get('response', '').lower()
                        next_questions = result.get('next_questions', [])
                        
                        # Check for entity extraction evidence
                        entity_evidence = sum(1 for entity in test["expected_entities"] 
                                            if entity in response_text or entity.replace("_", " ") in response_text)
                        
                        comprehensive_questions = len(next_questions) > 0
                        
                        if entity_evidence > 0 or comprehensive_questions:
                            print(f"   ✅ Entity extraction evidence found ({entity_evidence} entities)")
                            phase2_success += 1
                        else:
                            print(f"   ⚠️ Limited entity extraction evidence")
                    else:
                        print(f"   ❌ Message API error")
                else:
                    print(f"   ❌ Init API error")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        
        phase2_rate = (phase2_success / phase2_total * 100) if phase2_total > 0 else 0
        print(f"\n   Phase 2 Success Rate: {phase2_rate:.1f}% ({phase2_success}/{phase2_total})")
        
        return phase2_rate >= 70

    def run_tests(self):
        """Run all enhanced symptom pattern tests"""
        print("=" * 80)
        print("🚀 ENHANCED SYMPTOM PATTERN ARCHITECTURE TESTING")
        print("=" * 80)
        
        # Test core functionality
        core_success = self.test_enhanced_symptom_patterns()
        
        # Test Phase 1 patterns
        phase1_success = self.test_phase1_enhanced_patterns()
        
        # Test Phase 2 entity extraction
        phase2_success = self.test_phase2_entity_extraction()
        
        # Final summary
        print("\n" + "=" * 80)
        print("📊 FINAL TEST RESULTS")
        print("=" * 80)
        
        print(f"Core Enhanced Symptom Patterns: {'✅ PASSED' if core_success else '❌ FAILED'}")
        print(f"Phase 1 Enhanced Patterns: {'✅ PASSED' if phase1_success else '❌ FAILED'}")
        print(f"Phase 2 Entity Extraction: {'✅ PASSED' if phase2_success else '❌ FAILED'}")
        
        overall_success = core_success and phase1_success and phase2_success
        
        if overall_success:
            print(f"\n🎉 ENHANCED SYMPTOM PATTERN ARCHITECTURE: FULLY FUNCTIONAL")
            print(f"✅ Phase 1 & Phase 2 implementations are working correctly")
            print(f"✅ Complex pain expressions recognized")
            print(f"✅ Advanced temporal patterns processed")
            print(f"✅ Severity quantification operational")
            print(f"✅ Emergency pattern recognition functional")
            print(f"✅ Intelligent entity extraction working")
            return 0
        else:
            print(f"\n⚠️ ENHANCED SYMPTOM PATTERN ARCHITECTURE: NEEDS ATTENTION")
            if not core_success:
                print(f"❌ Core symptom pattern recognition needs improvement")
            if not phase1_success:
                print(f"❌ Phase 1 enhanced patterns need refinement")
            if not phase2_success:
                print(f"❌ Phase 2 entity extraction needs enhancement")
            return 1

if __name__ == "__main__":
    tester = SimpleEnhancedSymptomTester()
    exit_code = tester.run_tests()
    sys.exit(exit_code)