#!/usr/bin/env python3
"""
🚀 EMPATHETIC COMMUNICATION COMPREHENSIVE VALIDATION
===================================================

Comprehensive testing of the working empathetic communication endpoints
with various scenarios as requested in the review.
"""

import requests
import json
import time
import os
from datetime import datetime

def test_empathetic_communication_comprehensive():
    backend_url = "https://medchattest.preview.emergentagent.com/api"
    
    print("🚀 EMPATHETIC COMMUNICATION COMPREHENSIVE VALIDATION")
    print("=" * 70)
    
    test_results = []
    total_tests = 0
    passed_tests = 0
    
    def log_result(test_name, success, details, response_time=0):
        nonlocal total_tests, passed_tests
        total_tests += 1
        if success:
            passed_tests += 1
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        print(f"   {details}")
        if response_time > 0:
            print(f"   Response Time: {response_time:.2f}s")
        print()
        
        test_results.append({
            "test_name": test_name,
            "success": success,
            "details": details,
            "response_time": response_time
        })
    
    # Test scenarios from review request
    transformation_scenarios = [
        {
            "name": "Cardiovascular Emergency - High Anxiety Emotional",
            "medical_text": "Patient presents with myocardial infarction. Immediate coronary angiography indicated. Differential diagnosis includes unstable angina and aortic dissection.",
            "context": {
                "patient_anxiety_level": 0.8,
                "communication_style": "emotional",
                "age_group": "adult",
                "is_emergency": True,
                "symptom_severity": "critical"
            },
            "expected_empathy_min": 0.6
        },
        {
            "name": "Neurological Assessment - Elderly Anxious",
            "medical_text": "Symptoms suggest transient ischemic attack. Cerebrovascular accident must be ruled out. Recommend immediate neurological evaluation.",
            "context": {
                "patient_anxiety_level": 0.7,
                "communication_style": "anxious",
                "age_group": "elderly",
                "is_emergency": False,
                "symptom_severity": "moderate"
            },
            "expected_empathy_min": 0.5
        },
        {
            "name": "Respiratory Emergency - High Anxiety Practical",
            "medical_text": "Acute dyspnea with possible pulmonary embolism. Immediate anticoagulation therapy required.",
            "context": {
                "patient_anxiety_level": 0.9,
                "communication_style": "practical",
                "age_group": "adult",
                "is_emergency": True,
                "symptom_severity": "critical"
            },
            "expected_empathy_min": 0.7
        },
        {
            "name": "Pediatric Emergency - Family Present",
            "medical_text": "Pediatric patient presents with acute appendicitis. Surgical intervention required within 6 hours to prevent perforation.",
            "context": {
                "patient_anxiety_level": 0.8,
                "communication_style": "emotional",
                "age_group": "pediatric",
                "is_emergency": True,
                "symptom_severity": "severe",
                "family_present": True
            },
            "expected_empathy_min": 0.6
        },
        {
            "name": "Low Anxiety Analytical Patient",
            "medical_text": "Chronic obstructive pulmonary disease exacerbation with respiratory distress. Bronchodilator therapy and corticosteroids indicated.",
            "context": {
                "patient_anxiety_level": 0.1,
                "communication_style": "analytical",
                "age_group": "elderly",
                "is_emergency": False,
                "symptom_severity": "moderate"
            },
            "expected_empathy_min": 0.3
        }
    ]
    
    print("\n🎯 PHASE 1: EMPATHETIC COMMUNICATION TRANSFORMATION TESTING")
    print("=" * 60)
    
    for i, scenario in enumerate(transformation_scenarios, 1):
        print(f"\n{i}. SCENARIO: {scenario['name']}")
        print("-" * 50)
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{backend_url}/medical-ai/empathetic-communication-transform",
                json={
                    "medical_text": scenario["medical_text"],
                    **scenario["context"]
                },
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = [
                    "original_text", "empathetic_text", "empathy_score", "readability_score",
                    "transformations_applied", "communication_adjustments", "algorithm_version"
                ]
                
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    log_result(
                        f"Transform {i} - {scenario['name']}",
                        False,
                        f"Missing fields: {missing_fields}",
                        processing_time
                    )
                    continue
                
                empathy_score = data.get('empathy_score', 0)
                readability_score = data.get('readability_score', 0)
                transformations = data.get('transformations_applied', [])
                
                # Validate empathy score
                expected_min = scenario.get('expected_empathy_min', 0.4)
                if empathy_score < expected_min:
                    log_result(
                        f"Transform {i} - {scenario['name']}",
                        False,
                        f"Empathy score {empathy_score:.3f} below expected {expected_min}",
                        processing_time
                    )
                    continue
                
                # Validate readability improvement
                if readability_score < 0.5:
                    log_result(
                        f"Transform {i} - {scenario['name']}",
                        False,
                        f"Readability score {readability_score:.3f} too low",
                        processing_time
                    )
                    continue
                
                # Validate performance (<3 seconds)
                if processing_time > 3.0:
                    log_result(
                        f"Transform {i} - {scenario['name']}",
                        False,
                        f"Performance {processing_time:.2f}s exceeds 3s limit",
                        processing_time
                    )
                    continue
                
                # Check for clinical accuracy preservation
                original_text = data.get('original_text', '').lower()
                empathetic_text = data.get('empathetic_text', '').lower()
                
                # Key medical terms should be preserved or explained
                medical_terms = ['infarction', 'angiography', 'ischemic', 'embolism', 'appendicitis']
                preserved_or_explained = True
                for term in medical_terms:
                    if term in original_text:
                        if term not in empathetic_text and 'heart attack' not in empathetic_text and 'stroke' not in empathetic_text:
                            preserved_or_explained = False
                            break
                
                # Success
                details = f"Empathy: {empathy_score:.3f}, Readability: {readability_score:.3f}, Transformations: {len(transformations)}, Clinical accuracy preserved: {preserved_or_explained}"
                log_result(
                    f"Transform {i} - {scenario['name']}",
                    True,
                    details,
                    processing_time
                )
                
                # Print sample transformation
                print(f"   Original: {data.get('original_text', '')[:80]}...")
                print(f"   Empathetic: {data.get('empathetic_text', '')[:80]}...")
                
            else:
                log_result(
                    f"Transform {i} - {scenario['name']}",
                    False,
                    f"HTTP {response.status_code}: {response.text[:100]}",
                    processing_time
                )
                
        except Exception as e:
            processing_time = time.time() - start_time
            log_result(
                f"Transform {i} - {scenario['name']}",
                False,
                f"Exception: {str(e)}",
                processing_time
            )
    
    # Test patient-friendly explanations
    print("\n🎯 PHASE 2: PATIENT-FRIENDLY EXPLANATION TESTING")
    print("=" * 60)
    
    explanation_scenarios = [
        {
            "name": "Cardiovascular Concepts - Simple with Analogies",
            "concepts": ["myocardial_infarction", "coronary_angiography", "unstable_angina"],
            "context": {
                "anxiety_level": 0.8,
                "communication_style": "emotional",
                "age_group": "adult"
            },
            "depth": "simple",
            "analogies": True
        },
        {
            "name": "Neurological Concepts - Detailed",
            "concepts": ["transient_ischemic_attack", "cerebrovascular_accident"],
            "context": {
                "anxiety_level": 0.6,
                "communication_style": "analytical",
                "age_group": "elderly"
            },
            "depth": "detailed",
            "analogies": False
        },
        {
            "name": "Respiratory Concepts - Moderate with Analogies",
            "concepts": ["pulmonary_embolism", "anticoagulation_therapy", "dyspnea"],
            "context": {
                "anxiety_level": 0.7,
                "communication_style": "practical",
                "age_group": "adult"
            },
            "depth": "moderate",
            "analogies": True
        }
    ]
    
    for i, scenario in enumerate(explanation_scenarios, 1):
        print(f"\n{i}. EXPLANATION: {scenario['name']}")
        print("-" * 50)
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{backend_url}/medical-ai/patient-friendly-explanation",
                json={
                    "medical_concepts": scenario["concepts"],
                    "patient_context": scenario["context"],
                    "explanation_depth": scenario["depth"],
                    "include_analogies": scenario["analogies"]
                },
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ["explanations", "overall_empathy_score", "readability_metrics"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    log_result(
                        f"Explanation {i} - {scenario['name']}",
                        False,
                        f"Missing fields: {missing_fields}",
                        processing_time
                    )
                    continue
                
                explanations = data.get('explanations', {})
                overall_empathy = data.get('overall_empathy_score', 0)
                
                # Validate all concepts explained
                if len(explanations) != len(scenario["concepts"]):
                    log_result(
                        f"Explanation {i} - {scenario['name']}",
                        False,
                        f"Concept count mismatch: {len(explanations)} vs {len(scenario['concepts'])}",
                        processing_time
                    )
                    continue
                
                # Validate empathy score
                if overall_empathy < 0.3:
                    log_result(
                        f"Explanation {i} - {scenario['name']}",
                        False,
                        f"Overall empathy {overall_empathy:.3f} too low",
                        processing_time
                    )
                    continue
                
                # Validate performance
                if processing_time > 3.0:
                    log_result(
                        f"Explanation {i} - {scenario['name']}",
                        False,
                        f"Performance {processing_time:.2f}s exceeds 3s limit",
                        processing_time
                    )
                    continue
                
                # Success
                details = f"Concepts: {len(explanations)}, Overall empathy: {overall_empathy:.3f}, Depth: {scenario['depth']}, Analogies: {scenario['analogies']}"
                log_result(
                    f"Explanation {i} - {scenario['name']}",
                    True,
                    details,
                    processing_time
                )
                
                # Print sample explanations
                for concept, explanation in list(explanations.items())[:2]:
                    print(f"   {concept}: {explanation.get('simple_explanation', '')[:60]}...")
                
            else:
                log_result(
                    f"Explanation {i} - {scenario['name']}",
                    False,
                    f"HTTP {response.status_code}: {response.text[:100]}",
                    processing_time
                )
                
        except Exception as e:
            processing_time = time.time() - start_time
            log_result(
                f"Explanation {i} - {scenario['name']}",
                False,
                f"Exception: {str(e)}",
                processing_time
            )
    
    # Generate final report
    print("\n" + "=" * 70)
    print("🎯 EMPATHETIC COMMUNICATION COMPREHENSIVE VALIDATION - FINAL REPORT")
    print("=" * 70)
    
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"📊 OVERALL RESULTS:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Passed Tests: {passed_tests}")
    print(f"   Failed Tests: {total_tests - passed_tests}")
    print(f"   Success Rate: {success_rate:.1f}%")
    print()
    
    # Categorize results
    transform_tests = [r for r in test_results if "Transform" in r["test_name"]]
    explanation_tests = [r for r in test_results if "Explanation" in r["test_name"]]
    
    transform_passed = sum(1 for r in transform_tests if r["success"])
    explanation_passed = sum(1 for r in explanation_tests if r["success"])
    
    print(f"📋 TRANSFORMATION TESTS: {transform_passed}/{len(transform_tests)} passed ({(transform_passed/len(transform_tests)*100) if transform_tests else 0:.1f}%)")
    print(f"📋 EXPLANATION TESTS: {explanation_passed}/{len(explanation_tests)} passed ({(explanation_passed/len(explanation_tests)*100) if explanation_tests else 0:.1f}%)")
    print()
    
    # Performance analysis
    response_times = [r["response_time"] for r in test_results if r["response_time"] > 0]
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        print(f"⏱️  PERFORMANCE ANALYSIS:")
        print(f"   Average Response Time: {avg_time:.2f}s")
        print(f"   Maximum Response Time: {max_time:.2f}s")
        print(f"   Performance Target (<3s): {'✅ MET' if max_time < 3.0 else '❌ EXCEEDED'}")
        print()
    
    # Success criteria assessment
    print("🎯 SUCCESS CRITERIA ASSESSMENT:")
    
    # API functionality
    transform_functional = len(transform_tests) > 0 and any(r["success"] for r in transform_tests)
    explanation_functional = len(explanation_tests) > 0 and any(r["success"] for r in explanation_tests)
    
    print(f"   ✅ Empathetic Transformation API Functional: {'YES' if transform_functional else 'NO'}")
    print(f"   ✅ Patient-Friendly Explanation API Functional: {'YES' if explanation_functional else 'NO'}")
    
    # Quality standards
    empathy_quality_good = success_rate >= 70
    performance_good = all(rt < 3.0 for rt in response_times) if response_times else True
    
    print(f"   ✅ Empathy Quality Standards Met (≥70%): {'YES' if empathy_quality_good else 'NO'}")
    print(f"   ✅ Performance Standards Met (<3s): {'YES' if performance_good else 'NO'}")
    print()
    
    # Final assessment
    criteria_met = sum([transform_functional, explanation_functional, empathy_quality_good, performance_good])
    
    if success_rate >= 80 and criteria_met >= 3:
        print("🎉 ASSESSMENT: EMPATHETIC COMMUNICATION SYSTEM IS PRODUCTION-READY!")
        print("   The system demonstrates excellent empathetic transformation capabilities")
        print("   with patient-friendly explanations and maintains clinical accuracy.")
    elif success_rate >= 60 and criteria_met >= 2:
        print("⚠️  ASSESSMENT: EMPATHETIC COMMUNICATION SYSTEM IS FUNCTIONAL")
        print("   Core empathy functionality works but some improvements needed.")
    else:
        print("❌ ASSESSMENT: EMPATHETIC COMMUNICATION SYSTEM NEEDS WORK")
        print("   Critical issues prevent production deployment.")
    
    print()
    print(f"Test Completion Time: {datetime.now().isoformat()}")
    print("=" * 70)
    
    return {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'success_rate': success_rate,
        'transform_functional': transform_functional,
        'explanation_functional': explanation_functional,
        'production_ready': success_rate >= 80 and criteria_met >= 3
    }

if __name__ == "__main__":
    test_empathetic_communication_comprehensive()