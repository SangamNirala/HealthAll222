#!/usr/bin/env python3
"""
FOCUSED PHASE 4 MEDICAL PATTERN RECOGNITION TESTING
===================================================

Focused testing for Phase 4 Comprehensive Medical Pattern Recognition Engine
with proper consultation flow and detailed validation.
"""

import requests
import json
import time
from datetime import datetime

# Backend URL
BACKEND_URL = "https://intent-genius.preview.emergentagent.com/api"

class FocusedPhase4Tester:
    """Focused Phase 4 testing with proper consultation flow"""
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.test_results = []
        
    def test_ultra_challenging_scenario_1(self):
        """Test Ultra-Challenging Scenario 1: Complex chest pain"""
        
        print("\n🔥 ULTRA-CHALLENGING SCENARIO 1: Complex Chest Pain")
        print("-" * 60)
        
        scenario_1_input = "Sharp stabbing pain in my left upper chest that started suddenly this morning after lifting heavy boxes at work, getting progressively worse with deep breathing and movement, radiating down my left arm to my fingers with tingling, accompanied by mild nausea and cold sweats, comes in waves every 2-3 minutes lasting about 30 seconds each, completely disappears when I sit perfectly still and breathe shallow"
        
        print(f"Input: {scenario_1_input[:100]}...")
        print("Expected: EMERGENCY urgency, Acute coronary syndrome detection")
        
        try:
            # Initialize consultation
            init_response = requests.post(f"{self.backend_url}/medical-ai/initialize", 
                json={"patient_id": "ultra-scenario-1", "timestamp": datetime.now().isoformat()},
                timeout=30)
            
            if init_response.status_code == 200:
                init_data = init_response.json()
                consultation_id = init_data.get("consultation_id")
                print(f"✅ Consultation initialized: {consultation_id}")
                
                # Send scenario message
                start_time = time.time()
                message_response = requests.post(f"{self.backend_url}/medical-ai/message",
                    json={
                        "consultation_id": consultation_id,
                        "message": scenario_1_input,
                        "timestamp": datetime.now().isoformat()
                    },
                    timeout=30)
                
                processing_time = (time.time() - start_time) * 1000
                
                if message_response.status_code == 200:
                    response_data = message_response.json()
                    
                    # Analyze response
                    urgency = response_data.get("urgency", "routine")
                    emergency_detected = response_data.get("emergency_detected", False)
                    response_text = response_data.get("response", "").lower()
                    context = str(response_data.get("context", "")).lower()
                    
                    # Check for syndrome mentions
                    syndrome_keywords = ["acute coronary", "coronary syndrome", "heart attack", "myocardial infarction", "cardiac", "coronary artery", "chest pain"]
                    syndrome_detected = any(keyword in response_text or keyword in context for keyword in syndrome_keywords)
                    
                    # Results
                    results = {
                        "urgency_correct": urgency == "emergency",
                        "emergency_detected": emergency_detected,
                        "syndrome_mentioned": syndrome_detected,
                        "processing_time_ms": processing_time,
                        "performance_acceptable": processing_time < 40,
                        "response_quality": len(response_data.get("response", "")) > 100
                    }
                    
                    success = results["urgency_correct"] and results["emergency_detected"]
                    
                    print(f"✅ API Response received")
                    print(f"   Urgency: {urgency} (Expected: emergency) {'✅' if results['urgency_correct'] else '❌'}")
                    print(f"   Emergency Detected: {emergency_detected} {'✅' if emergency_detected else '❌'}")
                    print(f"   Syndrome Keywords Found: {syndrome_detected} {'✅' if syndrome_detected else '❌'}")
                    print(f"   Processing Time: {processing_time:.1f}ms {'✅' if results['performance_acceptable'] else '❌'}")
                    print(f"   Response Quality: {'✅' if results['response_quality'] else '❌'}")
                    
                    self.test_results.append({
                        "test": "Ultra-Challenging Scenario 1",
                        "status": "PASS" if success else "FAIL",
                        "critical": True,
                        "details": results
                    })
                    
                    return success
                    
                else:
                    print(f"❌ Message API error: {message_response.status_code}")
                    print(f"   Response: {message_response.text}")
                    return False
                    
            else:
                print(f"❌ Init API error: {init_response.status_code}")
                print(f"   Response: {init_response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return False
    
    def test_ultra_challenging_scenario_2(self):
        """Test Ultra-Challenging Scenario 2: Complex migraine"""
        
        print("\n🔥 ULTRA-CHALLENGING SCENARIO 2: Complex Migraine")
        print("-" * 60)
        
        scenario_2_input = "For the past month I've been getting these absolutely terrible headaches on the right side of my head, usually starting behind my right eye, throbbing and pulsating like my heart is beating in my head, typically triggered by fluorescent lights at work or when my kids are being loud, almost always accompanied by severe nausea and sensitivity to light and sound, sometimes progressing to vomiting, lasting anywhere from 4-12 hours, happening about 2-3 times per week usually in the late afternoon, completely debilitating - I have to lie in a dark quiet room and can't function at all"
        
        print(f"Input: {scenario_2_input[:100]}...")
        print("Expected: URGENT urgency, Migraine syndrome detection")
        
        try:
            # Initialize consultation
            init_response = requests.post(f"{self.backend_url}/medical-ai/initialize", 
                json={"patient_id": "ultra-scenario-2", "timestamp": datetime.now().isoformat()},
                timeout=30)
            
            if init_response.status_code == 200:
                init_data = init_response.json()
                consultation_id = init_data.get("consultation_id")
                print(f"✅ Consultation initialized: {consultation_id}")
                
                # Send scenario message
                start_time = time.time()
                message_response = requests.post(f"{self.backend_url}/medical-ai/message",
                    json={
                        "consultation_id": consultation_id,
                        "message": scenario_2_input,
                        "timestamp": datetime.now().isoformat()
                    },
                    timeout=30)
                
                processing_time = (time.time() - start_time) * 1000
                
                if message_response.status_code == 200:
                    response_data = message_response.json()
                    
                    # Analyze response
                    urgency = response_data.get("urgency", "routine")
                    emergency_detected = response_data.get("emergency_detected", False)
                    response_text = response_data.get("response", "").lower()
                    context = str(response_data.get("context", "")).lower()
                    differential = " ".join(response_data.get("differential_diagnoses", [])).lower()
                    all_content = f"{response_text} {context} {differential}"
                    
                    # Check for migraine syndrome mentions
                    migraine_keywords = ["migraine", "migraine syndrome", "headache disorder", "cephalgia", "headache"]
                    syndrome_detected = any(keyword in all_content for keyword in migraine_keywords)
                    
                    # Results
                    results = {
                        "urgency_appropriate": urgency in ["urgent", "routine"],  # Either urgent or routine is acceptable for migraine
                        "urgency_detected": urgency,
                        "syndrome_mentioned": syndrome_detected,
                        "processing_time_ms": processing_time,
                        "performance_acceptable": processing_time < 40,
                        "response_quality": len(response_data.get("response", "")) > 100
                    }
                    
                    success = results["urgency_appropriate"] and results["syndrome_mentioned"]
                    
                    print(f"✅ API Response received")
                    print(f"   Urgency: {urgency} (Expected: urgent/routine) {'✅' if results['urgency_appropriate'] else '❌'}")
                    print(f"   Emergency Detected: {emergency_detected}")
                    print(f"   Migraine Keywords Found: {syndrome_detected} {'✅' if syndrome_detected else '❌'}")
                    print(f"   Processing Time: {processing_time:.1f}ms {'✅' if results['performance_acceptable'] else '❌'}")
                    print(f"   Response Quality: {'✅' if results['response_quality'] else '❌'}")
                    
                    self.test_results.append({
                        "test": "Ultra-Challenging Scenario 2",
                        "status": "PASS" if success else "FAIL",
                        "critical": True,
                        "details": results
                    })
                    
                    return success
                    
                else:
                    print(f"❌ Message API error: {message_response.status_code}")
                    print(f"   Response: {message_response.text}")
                    return False
                    
            else:
                print(f"❌ Init API error: {init_response.status_code}")
                print(f"   Response: {init_response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return False
    
    def test_syndrome_detection(self):
        """Test syndrome detection for all 4 required syndromes"""
        
        print("\n🔬 SYNDROME DETECTION VALIDATION")
        print("-" * 60)
        
        syndrome_tests = [
            {
                "name": "Acute Coronary Syndrome",
                "input": "Crushing chest pain with shortness of breath, nausea, and sweating radiating to left arm",
                "keywords": ["acute coronary", "coronary syndrome", "heart attack", "myocardial infarction", "cardiac"],
                "expected_urgency": "emergency"
            },
            {
                "name": "Migraine Syndrome", 
                "input": "Severe throbbing headache with nausea, light sensitivity, and visual aura lasting 8 hours",
                "keywords": ["migraine", "migraine syndrome", "headache disorder", "cephalgia"],
                "expected_urgency": ["urgent", "routine"]
            },
            {
                "name": "Stroke Syndrome",
                "input": "Sudden weakness on left side with facial drooping and difficulty speaking",
                "keywords": ["stroke", "stroke syndrome", "cerebrovascular", "cva", "brain attack"],
                "expected_urgency": "emergency"
            },
            {
                "name": "Acute Abdomen",
                "input": "Severe right lower quadrant abdominal pain with fever, vomiting, and rebound tenderness",
                "keywords": ["acute abdomen", "appendicitis", "abdominal emergency", "surgical abdomen"],
                "expected_urgency": "emergency"
            }
        ]
        
        syndrome_results = []
        
        for test_case in syndrome_tests:
            print(f"\n🔬 Testing {test_case['name']}")
            print(f"   Input: {test_case['input'][:60]}...")
            
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
                        
                        # Analyze response
                        urgency = response_data.get("urgency", "routine")
                        response_text = response_data.get("response", "").lower()
                        context = str(response_data.get("context", "")).lower()
                        differential = " ".join(response_data.get("differential_diagnoses", [])).lower()
                        all_content = f"{response_text} {context} {differential}"
                        
                        # Check for syndrome keywords
                        syndrome_detected = any(keyword in all_content for keyword in test_case["keywords"])
                        
                        # Check urgency
                        if isinstance(test_case["expected_urgency"], list):
                            urgency_correct = urgency in test_case["expected_urgency"]
                        else:
                            urgency_correct = urgency == test_case["expected_urgency"]
                        
                        success = syndrome_detected and urgency_correct
                        syndrome_results.append(success)
                        
                        print(f"   Urgency: {urgency} {'✅' if urgency_correct else '❌'}")
                        print(f"   Syndrome Keywords: {'✅' if syndrome_detected else '❌'}")
                        print(f"   Overall: {'✅ PASS' if success else '❌ FAIL'}")
                        
                    else:
                        print(f"   ❌ Message API error: {message_response.status_code}")
                        syndrome_results.append(False)
                else:
                    print(f"   ❌ Init API error: {init_response.status_code}")
                    syndrome_results.append(False)
                    
            except Exception as e:
                print(f"   ❌ Exception: {str(e)}")
                syndrome_results.append(False)
        
        syndrome_success_rate = sum(syndrome_results) / len(syndrome_results)
        overall_syndrome_success = syndrome_success_rate >= 0.75  # 75% success rate
        
        print(f"\n📊 SYNDROME DETECTION SUMMARY:")
        print(f"   Success Rate: {syndrome_success_rate*100:.1f}% ({sum(syndrome_results)}/{len(syndrome_results)})")
        print(f"   Overall: {'✅ PASS' if overall_syndrome_success else '❌ FAIL'}")
        
        return overall_syndrome_success
    
    def run_focused_tests(self):
        """Run all focused Phase 4 tests"""
        
        print("🚨 FOCUSED PHASE 4 MEDICAL PATTERN RECOGNITION TESTING")
        print("=" * 80)
        
        # Test ultra-challenging scenarios
        scenario_1_success = self.test_ultra_challenging_scenario_1()
        scenario_2_success = self.test_ultra_challenging_scenario_2()
        
        # Test syndrome detection
        syndrome_success = self.test_syndrome_detection()
        
        # Generate summary report
        print("\n" + "=" * 80)
        print("🏆 FOCUSED PHASE 4 TEST SUMMARY")
        print("=" * 80)
        
        critical_tests = [scenario_1_success, scenario_2_success]
        critical_passed = sum(critical_tests)
        
        print(f"\n📊 CRITICAL TEST RESULTS:")
        print(f"   Ultra-Challenging Scenario 1: {'✅ PASS' if scenario_1_success else '❌ FAIL'}")
        print(f"   Ultra-Challenging Scenario 2: {'✅ PASS' if scenario_2_success else '❌ FAIL'}")
        print(f"   Syndrome Detection: {'✅ PASS' if syndrome_success else '❌ FAIL'}")
        print(f"   Critical Success Rate: {critical_passed}/2 ({critical_passed/2*100:.1f}%)")
        
        # Final assessment
        print(f"\n🏆 FINAL ASSESSMENT:")
        if critical_passed == 2 and syndrome_success:
            print("   ✅ PHASE 4 CRITICAL VALIDATION: SUCCESSFUL")
            print("   🎯 All critical ultra-challenging scenarios working correctly")
            print("   🔬 Syndrome detection operational")
        elif critical_passed >= 1:
            print("   ⚠️  PHASE 4 CRITICAL VALIDATION: PARTIALLY SUCCESSFUL")
            print("   🔧 Some critical scenarios working, improvements needed")
        else:
            print("   ❌ PHASE 4 CRITICAL VALIDATION: FAILED")
            print("   🚨 Critical ultra-challenging scenarios not working")
        
        print("\n" + "=" * 80)

def main():
    """Main testing function"""
    tester = FocusedPhase4Tester()
    tester.run_focused_tests()

if __name__ == "__main__":
    main()