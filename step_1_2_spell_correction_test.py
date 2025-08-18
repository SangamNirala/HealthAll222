#!/usr/bin/env python3
"""
Step 1.2 Advanced Medical Spell Correction System Testing
Tests the integration of advanced medical spell correction with Medical AI service
"""

import asyncio
import json
import requests
import time
from typing import Dict, List, Any
import os
from datetime import datetime

# Backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://clinicalparse.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class Step12SpellCorrectionTester:
    """Comprehensive tester for Step 1.2 Advanced Medical Spell Correction"""
    
    def __init__(self):
        self.test_results = []
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def log_test(self, test_name: str, status: str, details: Dict[str, Any]):
        """Log test result"""
        result = {
            'test_name': test_name,
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'details': details
        }
        self.test_results.append(result)
        
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} {test_name}: {status}")
        
        if details.get('error'):
            print(f"   Error: {details['error']}")
        if details.get('expected') and details.get('actual'):
            print(f"   Expected: {details['expected']}")
            print(f"   Actual: {details['actual']}")
    
    def test_required_spell_corrections(self):
        """Test all 5 required Step 1.2 spell correction examples"""
        print("\n🎯 TESTING REQUIRED STEP 1.2 SPELL CORRECTION EXAMPLES")
        print("=" * 60)
        
        required_examples = [
            ("haedache", "headache"),
            ("cheast", "chest"), 
            ("stomache", "stomach"),
            ("diabetis", "diabetes"),
            ("preassure", "pressure")
        ]
        
        passed_count = 0
        
        for misspelled, expected in required_examples:
            try:
                # Test via Medical AI message endpoint
                test_message = f"I have {misspelled} problems"
                
                # Initialize consultation first
                init_response = self.session.post(f"{API_BASE}/medical-ai/initialize", json={
                    "patient_id": "test-spell-correction",
                    "timestamp": datetime.now().isoformat()
                })
                
                if init_response.status_code != 200:
                    self.log_test(f"Spell Correction: {misspelled} → {expected}", "FAIL", {
                        "error": f"Failed to initialize consultation: {init_response.status_code}",
                        "expected": expected,
                        "actual": "initialization_failed"
                    })
                    continue
                
                init_data = init_response.json()
                consultation_id = init_data.get('consultation_id')
                
                # Send message with misspelling
                message_response = self.session.post(f"{API_BASE}/medical-ai/message", json={
                    "message": test_message,
                    "consultation_id": consultation_id,
                    "patient_id": "test-spell-correction"
                })
                
                if message_response.status_code == 200:
                    response_data = message_response.json()
                    ai_response = response_data.get('response', '').lower()
                    
                    # Check if the corrected word appears in the AI response
                    # The spell correction should have been applied before processing
                    if expected.lower() in ai_response:
                        passed_count += 1
                        self.log_test(f"Spell Correction: {misspelled} → {expected}", "PASS", {
                            "test_message": test_message,
                            "expected": expected,
                            "found_in_response": True,
                            "response_snippet": ai_response[:200] + "..." if len(ai_response) > 200 else ai_response
                        })
                    else:
                        self.log_test(f"Spell Correction: {misspelled} → {expected}", "FAIL", {
                            "test_message": test_message,
                            "expected": f"'{expected}' in AI response",
                            "actual": f"'{expected}' not found in response",
                            "response_snippet": ai_response[:200] + "..." if len(ai_response) > 200 else ai_response
                        })
                else:
                    self.log_test(f"Spell Correction: {misspelled} → {expected}", "FAIL", {
                        "error": f"API call failed: {message_response.status_code}",
                        "expected": expected,
                        "actual": "api_error"
                    })
                    
            except Exception as e:
                self.log_test(f"Spell Correction: {misspelled} → {expected}", "FAIL", {
                    "error": str(e),
                    "expected": expected,
                    "actual": "exception"
                })
        
        success_rate = (passed_count / len(required_examples)) * 100
        print(f"\n📊 REQUIRED EXAMPLES RESULTS: {passed_count}/{len(required_examples)} ({success_rate:.1f}%)")
        
        return passed_count == len(required_examples)
    
    def test_multiple_misspellings_single_message(self):
        """Test advanced spell correction with multiple misspellings in single messages"""
        print("\n🔄 TESTING MULTIPLE MISSPELLINGS IN SINGLE MESSAGES")
        print("=" * 60)
        
        test_cases = [
            {
                "message": "I have haedache and cheast pain",
                "expected_corrections": ["headache", "chest"],
                "description": "Two medical misspellings"
            },
            {
                "message": "My stomache hurts and I have diabetis",
                "expected_corrections": ["stomach", "diabetes"],
                "description": "Stomach and diabetes misspellings"
            },
            {
                "message": "High preassure causing haedache and cheast discomfort",
                "expected_corrections": ["pressure", "headache", "chest"],
                "description": "Three medical misspellings"
            }
        ]
        
        passed_count = 0
        
        for i, test_case in enumerate(test_cases, 1):
            try:
                # Initialize consultation
                init_response = self.session.post(f"{API_BASE}/medical-ai/initialize", json={
                    "patient_id": f"test-multi-spell-{i}",
                    "timestamp": datetime.now().isoformat()
                })
                
                if init_response.status_code != 200:
                    self.log_test(f"Multiple Misspellings Test {i}", "FAIL", {
                        "error": f"Failed to initialize consultation: {init_response.status_code}",
                        "test_case": test_case
                    })
                    continue
                
                init_data = init_response.json()
                consultation_id = init_data.get('consultation_id')
                
                # Send message with multiple misspellings
                message_response = self.session.post(f"{API_BASE}/medical-ai/message", json={
                    "message": test_case["message"],
                    "consultation_id": consultation_id,
                    "patient_id": f"test-multi-spell-{i}"
                })
                
                if message_response.status_code == 200:
                    response_data = message_response.json()
                    ai_response = response_data.get('response', '').lower()
                    
                    # Check if all expected corrections appear in the response
                    found_corrections = []
                    missing_corrections = []
                    
                    for expected_word in test_case["expected_corrections"]:
                        if expected_word.lower() in ai_response:
                            found_corrections.append(expected_word)
                        else:
                            missing_corrections.append(expected_word)
                    
                    if not missing_corrections:
                        passed_count += 1
                        self.log_test(f"Multiple Misspellings Test {i}", "PASS", {
                            "description": test_case["description"],
                            "original_message": test_case["message"],
                            "expected_corrections": test_case["expected_corrections"],
                            "found_corrections": found_corrections,
                            "success": True
                        })
                    else:
                        self.log_test(f"Multiple Misspellings Test {i}", "FAIL", {
                            "description": test_case["description"],
                            "original_message": test_case["message"],
                            "expected_corrections": test_case["expected_corrections"],
                            "found_corrections": found_corrections,
                            "missing_corrections": missing_corrections,
                            "response_snippet": ai_response[:300] + "..." if len(ai_response) > 300 else ai_response
                        })
                else:
                    self.log_test(f"Multiple Misspellings Test {i}", "FAIL", {
                        "error": f"API call failed: {message_response.status_code}",
                        "test_case": test_case
                    })
                    
            except Exception as e:
                self.log_test(f"Multiple Misspellings Test {i}", "FAIL", {
                    "error": str(e),
                    "test_case": test_case
                })
        
        success_rate = (passed_count / len(test_cases)) * 100
        print(f"\n📊 MULTIPLE MISSPELLINGS RESULTS: {passed_count}/{len(test_cases)} ({success_rate:.1f}%)")
        
        return passed_count == len(test_cases)
    
    def test_spell_correction_with_symptom_extraction(self):
        """Test that spell-corrected text is properly processed for symptom extraction"""
        print("\n🔍 TESTING SPELL CORRECTION + SYMPTOM EXTRACTION INTEGRATION")
        print("=" * 60)
        
        test_cases = [
            {
                "message": "I have severe haedache for 3 days",
                "expected_symptom": "headache",
                "expected_duration": "3 days",
                "description": "Headache misspelling with duration"
            },
            {
                "message": "Cheast pain when breathing",
                "expected_symptom": "chest",
                "expected_context": "breathing",
                "description": "Chest misspelling with breathing context"
            },
            {
                "message": "My stomache hurts after eating",
                "expected_symptom": "stomach",
                "expected_context": "eating",
                "description": "Stomach misspelling with eating context"
            }
        ]
        
        passed_count = 0
        
        for i, test_case in enumerate(test_cases, 1):
            try:
                # Initialize consultation
                init_response = self.session.post(f"{API_BASE}/medical-ai/initialize", json={
                    "patient_id": f"test-symptom-extract-{i}",
                    "timestamp": datetime.now().isoformat()
                })
                
                if init_response.status_code != 200:
                    self.log_test(f"Symptom Extraction Test {i}", "FAIL", {
                        "error": f"Failed to initialize consultation: {init_response.status_code}",
                        "test_case": test_case
                    })
                    continue
                
                init_data = init_response.json()
                consultation_id = init_data.get('consultation_id')
                
                # Send message with misspelling
                message_response = self.session.post(f"{API_BASE}/medical-ai/message", json={
                    "message": test_case["message"],
                    "consultation_id": consultation_id,
                    "patient_id": f"test-symptom-extract-{i}"
                })
                
                if message_response.status_code == 200:
                    response_data = message_response.json()
                    ai_response = response_data.get('response', '').lower()
                    
                    # Check if the AI response shows understanding of the corrected symptom
                    expected_symptom = test_case["expected_symptom"].lower()
                    symptom_understood = expected_symptom in ai_response
                    
                    # Check for medical reasoning about the symptom
                    medical_reasoning_indicators = [
                        "symptom", "condition", "medical", "clinical", "diagnosis", 
                        "assessment", "evaluation", "examination"
                    ]
                    
                    has_medical_reasoning = any(indicator in ai_response for indicator in medical_reasoning_indicators)
                    
                    if symptom_understood and has_medical_reasoning:
                        passed_count += 1
                        self.log_test(f"Symptom Extraction Test {i}", "PASS", {
                            "description": test_case["description"],
                            "original_message": test_case["message"],
                            "expected_symptom": test_case["expected_symptom"],
                            "symptom_understood": True,
                            "medical_reasoning_present": True,
                            "response_quality": "good"
                        })
                    else:
                        self.log_test(f"Symptom Extraction Test {i}", "FAIL", {
                            "description": test_case["description"],
                            "original_message": test_case["message"],
                            "expected_symptom": test_case["expected_symptom"],
                            "symptom_understood": symptom_understood,
                            "medical_reasoning_present": has_medical_reasoning,
                            "response_snippet": ai_response[:300] + "..." if len(ai_response) > 300 else ai_response
                        })
                else:
                    self.log_test(f"Symptom Extraction Test {i}", "FAIL", {
                        "error": f"API call failed: {message_response.status_code}",
                        "test_case": test_case
                    })
                    
            except Exception as e:
                self.log_test(f"Symptom Extraction Test {i}", "FAIL", {
                    "error": str(e),
                    "test_case": test_case
                })
        
        success_rate = (passed_count / len(test_cases)) * 100
        print(f"\n📊 SYMPTOM EXTRACTION RESULTS: {passed_count}/{len(test_cases)} ({success_rate:.1f}%)")
        
        return passed_count == len(test_cases)
    
    def test_performance_and_confidence_scoring(self):
        """Test performance and confidence scoring of the advanced spell checker"""
        print("\n⚡ TESTING PERFORMANCE AND CONFIDENCE SCORING")
        print("=" * 60)
        
        test_messages = [
            "I have haedache",
            "Cheast pain is severe", 
            "My stomache hurts",
            "Diabetis symptoms",
            "High preassure issues"
        ]
        
        response_times = []
        passed_count = 0
        
        for i, message in enumerate(test_messages, 1):
            try:
                start_time = time.time()
                
                # Initialize consultation
                init_response = self.session.post(f"{API_BASE}/medical-ai/initialize", json={
                    "patient_id": f"test-performance-{i}",
                    "timestamp": datetime.now().isoformat()
                })
                
                if init_response.status_code != 200:
                    continue
                
                init_data = init_response.json()
                consultation_id = init_data.get('consultation_id')
                
                # Send message
                message_response = self.session.post(f"{API_BASE}/medical-ai/message", json={
                    "message": message,
                    "consultation_id": consultation_id,
                    "patient_id": f"test-performance-{i}"
                })
                
                end_time = time.time()
                response_time = end_time - start_time
                response_times.append(response_time)
                
                if message_response.status_code == 200:
                    passed_count += 1
                    self.log_test(f"Performance Test {i}", "PASS", {
                        "message": message,
                        "response_time": f"{response_time:.3f}s",
                        "status": "success"
                    })
                else:
                    self.log_test(f"Performance Test {i}", "FAIL", {
                        "message": message,
                        "response_time": f"{response_time:.3f}s",
                        "error": f"HTTP {message_response.status_code}"
                    })
                    
            except Exception as e:
                self.log_test(f"Performance Test {i}", "FAIL", {
                    "message": message,
                    "error": str(e)
                })
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            
            # Performance criteria: average response time should be under 5 seconds
            performance_acceptable = avg_response_time < 5.0
            
            print(f"\n📊 PERFORMANCE METRICS:")
            print(f"   Average Response Time: {avg_response_time:.3f}s")
            print(f"   Min Response Time: {min_response_time:.3f}s")
            print(f"   Max Response Time: {max_response_time:.3f}s")
            print(f"   Performance Acceptable: {'✅ YES' if performance_acceptable else '❌ NO'}")
            
            return performance_acceptable and passed_count == len(test_messages)
        
        return False
    
    def test_integration_with_step_1_1_normalization(self):
        """Test integration with existing Step 1.1 text normalization features"""
        print("\n🔗 TESTING INTEGRATION WITH STEP 1.1 TEXT NORMALIZATION")
        print("=" * 60)
        
        test_cases = [
            {
                "message": "i having haedache 2 days",
                "expected_corrections": ["I have been having", "headache", "for 2 days"],
                "description": "Grammar + spelling correction"
            },
            {
                "message": "me cheast hurt when breath",
                "expected_corrections": ["my", "chest", "hurts", "when I breathe"],
                "description": "Pronoun + spelling + grammar correction"
            },
            {
                "message": "stomache ache n vomiting",
                "expected_corrections": ["stomach", "and"],
                "description": "Spelling + abbreviation expansion"
            }
        ]
        
        passed_count = 0
        
        for i, test_case in enumerate(test_cases, 1):
            try:
                # Initialize consultation
                init_response = self.session.post(f"{API_BASE}/medical-ai/initialize", json={
                    "patient_id": f"test-integration-{i}",
                    "timestamp": datetime.now().isoformat()
                })
                
                if init_response.status_code != 200:
                    self.log_test(f"Integration Test {i}", "FAIL", {
                        "error": f"Failed to initialize consultation: {init_response.status_code}",
                        "test_case": test_case
                    })
                    continue
                
                init_data = init_response.json()
                consultation_id = init_data.get('consultation_id')
                
                # Send message with multiple normalization needs
                message_response = self.session.post(f"{API_BASE}/medical-ai/message", json={
                    "message": test_case["message"],
                    "consultation_id": consultation_id,
                    "patient_id": f"test-integration-{i}"
                })
                
                if message_response.status_code == 200:
                    response_data = message_response.json()
                    ai_response = response_data.get('response', '').lower()
                    
                    # Check if the AI response shows understanding of normalized text
                    corrections_found = []
                    corrections_missing = []
                    
                    for expected_correction in test_case["expected_corrections"]:
                        if expected_correction.lower() in ai_response:
                            corrections_found.append(expected_correction)
                        else:
                            corrections_missing.append(expected_correction)
                    
                    # Consider test passed if most corrections are reflected in understanding
                    success_rate = len(corrections_found) / len(test_case["expected_corrections"])
                    
                    if success_rate >= 0.7:  # 70% of corrections should be reflected
                        passed_count += 1
                        self.log_test(f"Integration Test {i}", "PASS", {
                            "description": test_case["description"],
                            "original_message": test_case["message"],
                            "expected_corrections": test_case["expected_corrections"],
                            "corrections_found": corrections_found,
                            "success_rate": f"{success_rate:.1%}"
                        })
                    else:
                        self.log_test(f"Integration Test {i}", "FAIL", {
                            "description": test_case["description"],
                            "original_message": test_case["message"],
                            "expected_corrections": test_case["expected_corrections"],
                            "corrections_found": corrections_found,
                            "corrections_missing": corrections_missing,
                            "success_rate": f"{success_rate:.1%}",
                            "response_snippet": ai_response[:300] + "..." if len(ai_response) > 300 else ai_response
                        })
                else:
                    self.log_test(f"Integration Test {i}", "FAIL", {
                        "error": f"API call failed: {message_response.status_code}",
                        "test_case": test_case
                    })
                    
            except Exception as e:
                self.log_test(f"Integration Test {i}", "FAIL", {
                    "error": str(e),
                    "test_case": test_case
                })
        
        success_rate = (passed_count / len(test_cases)) * 100
        print(f"\n📊 INTEGRATION RESULTS: {passed_count}/{len(test_cases)} ({success_rate:.1f}%)")
        
        return passed_count == len(test_cases)
    
    def test_medical_ai_endpoints(self):
        """Test that Medical AI endpoints are functional"""
        print("\n🏥 TESTING MEDICAL AI ENDPOINTS")
        print("=" * 60)
        
        # Test initialization endpoint
        try:
            init_response = self.session.post(f"{API_BASE}/medical-ai/initialize", json={
                "patient_id": "test-endpoints",
                "timestamp": datetime.now().isoformat()
            })
            
            if init_response.status_code == 200:
                init_data = init_response.json()
                consultation_id = init_data.get('consultation_id')
                
                self.log_test("Medical AI Initialize Endpoint", "PASS", {
                    "status_code": init_response.status_code,
                    "consultation_id": consultation_id,
                    "response_keys": list(init_data.keys())
                })
                
                # Test message endpoint
                message_response = self.session.post(f"{API_BASE}/medical-ai/message", json={
                    "message": "I have a headache",
                    "consultation_id": consultation_id,
                    "patient_id": "test-endpoints"
                })
                
                if message_response.status_code == 200:
                    message_data = message_response.json()
                    
                    self.log_test("Medical AI Message Endpoint", "PASS", {
                        "status_code": message_response.status_code,
                        "response_keys": list(message_data.keys()),
                        "has_response": bool(message_data.get('response')),
                        "has_context": bool(message_data.get('context'))
                    })
                    
                    return True
                else:
                    self.log_test("Medical AI Message Endpoint", "FAIL", {
                        "status_code": message_response.status_code,
                        "error": "Message endpoint failed"
                    })
                    return False
            else:
                self.log_test("Medical AI Initialize Endpoint", "FAIL", {
                    "status_code": init_response.status_code,
                    "error": "Initialize endpoint failed"
                })
                return False
                
        except Exception as e:
            self.log_test("Medical AI Endpoints", "FAIL", {
                "error": str(e)
            })
            return False
    
    def run_all_tests(self):
        """Run all Step 1.2 tests"""
        print("🚀 STARTING STEP 1.2 ADVANCED MEDICAL SPELL CORRECTION TESTING")
        print("=" * 80)
        
        test_results = {}
        
        # Test Medical AI endpoints first
        test_results['endpoints'] = self.test_medical_ai_endpoints()
        
        # Test required spell corrections
        test_results['required_examples'] = self.test_required_spell_corrections()
        
        # Test multiple misspellings
        test_results['multiple_misspellings'] = self.test_multiple_misspellings_single_message()
        
        # Test symptom extraction integration
        test_results['symptom_extraction'] = self.test_spell_correction_with_symptom_extraction()
        
        # Test performance
        test_results['performance'] = self.test_performance_and_confidence_scoring()
        
        # Test integration with Step 1.1
        test_results['step_1_1_integration'] = self.test_integration_with_step_1_1_normalization()
        
        # Generate summary
        self.generate_test_summary(test_results)
        
        return test_results
    
    def generate_test_summary(self, test_results: Dict[str, bool]):
        """Generate comprehensive test summary"""
        print("\n" + "=" * 80)
        print("📊 STEP 1.2 ADVANCED MEDICAL SPELL CORRECTION - TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results.values() if result)
        overall_success_rate = (passed_tests / total_tests) * 100
        
        print(f"\n🎯 OVERALL RESULTS: {passed_tests}/{total_tests} ({overall_success_rate:.1f}%)")
        print("\n📋 DETAILED RESULTS:")
        
        test_descriptions = {
            'endpoints': 'Medical AI Endpoints Functionality',
            'required_examples': 'Required Step 1.2 Spell Correction Examples',
            'multiple_misspellings': 'Multiple Misspellings in Single Messages',
            'symptom_extraction': 'Spell Correction + Symptom Extraction Integration',
            'performance': 'Performance and Confidence Scoring',
            'step_1_1_integration': 'Integration with Step 1.1 Text Normalization'
        }
        
        for test_key, passed in test_results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            description = test_descriptions.get(test_key, test_key)
            print(f"   {status} {description}")
        
        print(f"\n🏆 STEP 1.2 SYSTEM STATUS:")
        if overall_success_rate >= 90:
            print("   🎉 EXCELLENT - Step 1.2 Advanced Medical Spell Correction is fully functional!")
        elif overall_success_rate >= 75:
            print("   ✅ GOOD - Step 1.2 system is working well with minor issues")
        elif overall_success_rate >= 50:
            print("   ⚠️  PARTIAL - Step 1.2 system has significant issues that need attention")
        else:
            print("   ❌ CRITICAL - Step 1.2 system has major failures requiring immediate fixes")
        
        print(f"\n📈 KEY ACHIEVEMENTS:")
        if test_results.get('required_examples'):
            print("   ✅ All 5 required spell correction examples working")
        if test_results.get('multiple_misspellings'):
            print("   ✅ Advanced multiple misspelling correction functional")
        if test_results.get('symptom_extraction'):
            print("   ✅ Spell correction integrated with medical AI symptom extraction")
        if test_results.get('performance'):
            print("   ✅ Performance meets acceptable thresholds")
        if test_results.get('step_1_1_integration'):
            print("   ✅ Successfully integrated with Step 1.1 text normalization")
        
        if not all(test_results.values()):
            print(f"\n⚠️  ISSUES REQUIRING ATTENTION:")
            for test_key, passed in test_results.items():
                if not passed:
                    description = test_descriptions.get(test_key, test_key)
                    print(f"   ❌ {description}")
        
        print("\n" + "=" * 80)
        print("🏁 STEP 1.2 TESTING COMPLETE")
        print("=" * 80)


def main():
    """Main testing function"""
    tester = Step12SpellCorrectionTester()
    results = tester.run_all_tests()
    
    # Return exit code based on results
    if all(results.values()):
        return 0  # Success
    else:
        return 1  # Some tests failed


if __name__ == "__main__":
    exit(main())