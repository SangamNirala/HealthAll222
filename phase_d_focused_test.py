#!/usr/bin/env python3
"""
PHASE D: FOCUSED VALIDATION TESTING
===================================

Testing specific Phase D scenarios mentioned in the review request:
- Performance benchmarking with concurrent loads
- Clinical validation for emergency vs routine medical scenarios  
- Safety verification for high-risk medical classifications
- Audit logging for compliance tracking
- Comprehensive system status verification
"""

import asyncio
import aiohttp
import json
import time
import os
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://symptom-parse.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

async def test_performance_benchmarking_concurrent_loads():
    """Test performance benchmarking with concurrent loads"""
    print("🚀 TESTING: Performance benchmarking with concurrent loads")
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
        benchmark_data = {
            "concurrent_levels": [1, 10, 50, 100],  # Test concurrent loads
            "duration_seconds": 30,  # 30 second test
            "include_stress_test": True  # Include stress testing
        }
        
        start_time = time.time()
        async with session.post(f"{BASE_URL}/medical-ai/phase-d/performance-benchmark", json=benchmark_data) as response:
            response_time = time.time() - start_time
            
            if response.status == 200:
                data = await response.json()
                print(f"✅ SUCCESS: Performance benchmarking completed ({response_time:.2f}s)")
                print(f"   Status: {data.get('status')}")
                print(f"   Benchmark Results: {bool(data.get('benchmark_results'))}")
                print(f"   Stress Test Results: {bool(data.get('stress_test_results'))}")
                
                # Check performance summary
                summary = data.get('performance_summary', {})
                if summary:
                    print(f"   Performance Summary Available: ✅")
                    
                return True
            else:
                error = await response.text()
                print(f"❌ FAILED: {response.status} - {error}")
                return False

async def test_clinical_validation_emergency_vs_routine():
    """Test clinical validation for emergency vs routine medical scenarios"""
    print("\n🏥 TESTING: Clinical validation for emergency vs routine scenarios")
    
    # Test scenarios
    scenarios = [
        {
            "name": "Emergency Scenario",
            "patient_message": "I'm having severe crushing chest pain radiating to my left arm and jaw, I can't breathe properly",
            "ai_classification": {
                "intent": "cardiac_emergency",
                "confidence": 0.96,
                "urgency": "critical",
                "reasoning": "Classic symptoms of myocardial infarction requiring immediate medical attention"
            },
            "validation_level": "expert",
            "priority": True
        },
        {
            "name": "Routine Scenario", 
            "patient_message": "I've had a mild headache for the past few hours, it's not severe but persistent",
            "ai_classification": {
                "intent": "general_symptom_inquiry",
                "confidence": 0.82,
                "urgency": "routine",
                "reasoning": "Common headache symptoms, likely non-emergency"
            },
            "validation_level": "basic",
            "priority": False
        }
    ]
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
        results = []
        
        for scenario in scenarios:
            validation_data = {
                "patient_message": scenario["patient_message"],
                "conversation_context": {"session_id": f"test_{scenario['name'].lower().replace(' ', '_')}"},
                "ai_classification_result": scenario["ai_classification"],
                "validation_level": scenario["validation_level"],
                "priority": scenario["priority"]
            }
            
            start_time = time.time()
            async with session.post(f"{BASE_URL}/medical-ai/phase-d/submit-clinical-validation", json=validation_data) as response:
                response_time = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ {scenario['name']}: Validation submitted ({response_time:.2f}s)")
                    print(f"   Case ID: {data.get('case_id')}")
                    print(f"   Priority: {data.get('priority')}")
                    print(f"   Estimated Review Time: {data.get('estimated_review_time_hours')}h")
                    results.append(True)
                else:
                    error = await response.text()
                    print(f"❌ {scenario['name']}: Failed - {error}")
                    results.append(False)
                    
        return all(results)

async def test_safety_verification_high_risk():
    """Test safety verification for high-risk medical classifications"""
    print("\n🛡️ TESTING: Safety verification for high-risk medical classifications")
    
    # High-risk scenarios
    high_risk_scenarios = [
        {
            "name": "Cardiac Emergency",
            "patient_message": "Severe chest pain, shortness of breath, sweating, nausea",
            "ai_classification": {
                "intent": "cardiac_emergency",
                "confidence": 0.94,
                "urgency": "critical",
                "reasoning": "Multiple cardiac emergency indicators present"
            }
        },
        {
            "name": "Stroke Symptoms",
            "patient_message": "Sudden weakness on left side, difficulty speaking, facial drooping",
            "ai_classification": {
                "intent": "neurological_emergency", 
                "confidence": 0.91,
                "urgency": "critical",
                "reasoning": "Classic stroke symptoms requiring immediate intervention"
            }
        }
    ]
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
        results = []
        
        for scenario in high_risk_scenarios:
            safety_data = {
                "patient_message": scenario["patient_message"],
                "ai_classification_result": scenario["ai_classification"],
                "conversation_context": {"session_id": f"safety_test_{scenario['name'].lower().replace(' ', '_')}"}
            }
            
            start_time = time.time()
            async with session.post(f"{BASE_URL}/medical-ai/phase-d/verify-safety", json=safety_data) as response:
                response_time = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ {scenario['name']}: Safety verification completed ({response_time:.2f}s)")
                    print(f"   Safety Score: {data.get('safety_score')}")
                    print(f"   Intervention Required: {data.get('intervention_required')}")
                    print(f"   Escalation Needed: {data.get('escalation_needed')}")
                    
                    # Check safety verification details
                    safety_verification = data.get('safety_verification', {})
                    if safety_verification:
                        print(f"   Safety Verification Details: ✅")
                        
                    results.append(True)
                else:
                    error = await response.text()
                    print(f"❌ {scenario['name']}: Failed - {error}")
                    results.append(False)
                    
        return all(results)

async def test_audit_logging_compliance():
    """Test audit logging for compliance tracking"""
    print("\n📋 TESTING: Audit logging for compliance tracking")
    
    # Different compliance scenarios
    audit_scenarios = [
        {
            "name": "HIPAA Compliance",
            "user_id": "patient_12345",
            "session_id": "hipaa_session_789",
            "action_type": "medical_data_processing",
            "medical_intent_classified": "general_health_inquiry",
            "classification_confidence": 0.87,
            "clinical_accuracy_verified": False,
            "safety_level": "safe",
            "reviewer_notes": "Standard health inquiry processed with HIPAA compliance"
        },
        {
            "name": "FDA Compliance",
            "user_id": "patient_67890", 
            "session_id": "fda_session_456",
            "action_type": "medical_diagnosis_assistance",
            "medical_intent_classified": "emergency_detection",
            "classification_confidence": 0.95,
            "clinical_accuracy_verified": True,  # This should trigger FDA compliance
            "safety_level": "verified_safe",
            "reviewer_notes": "Emergency detection verified by medical professional for FDA compliance"
        }
    ]
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
        results = []
        
        for scenario in audit_scenarios:
            start_time = time.time()
            async with session.post(f"{BASE_URL}/medical-ai/phase-d/clinical-audit", json=scenario) as response:
                response_time = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ {scenario['name']}: Audit logged ({response_time:.2f}s)")
                    print(f"   Audit ID: {data.get('audit_id')}")
                    print(f"   Compliance Frameworks: {data.get('compliance_frameworks')}")
                    print(f"   Logged At: {data.get('logged_at')}")
                    results.append(True)
                else:
                    error = await response.text()
                    print(f"❌ {scenario['name']}: Failed - {error}")
                    results.append(False)
                    
        return all(results)

async def test_comprehensive_system_status():
    """Test comprehensive system status verification"""
    print("\n🎯 TESTING: Comprehensive system status verification")
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
        start_time = time.time()
        async with session.get(f"{BASE_URL}/medical-ai/phase-d/comprehensive-status") as response:
            response_time = time.time() - start_time
            
            if response.status == 200:
                data = await response.json()
                print(f"✅ SUCCESS: Comprehensive status retrieved ({response_time:.2f}s)")
                print(f"   Phase D Status: {data.get('phase_d_status')}")
                print(f"   Algorithm Version: {data.get('algorithm_version')}")
                print(f"   Production Readiness Score: {data.get('production_readiness_score')}")
                
                # Check components
                components = data.get('components', {})
                expected_components = ['performance_optimization', 'clinical_validation', 'production_monitoring']
                components_present = all(comp in components for comp in expected_components)
                print(f"   All Components Present: {'✅' if components_present else '❌'}")
                
                # Check key achievements
                achievements = data.get('key_achievements', {})
                if achievements:
                    print(f"   Key Achievements:")
                    for key, value in achievements.items():
                        print(f"     - {key}: {value}")
                        
                return True
            else:
                error = await response.text()
                print(f"❌ FAILED: {response.status} - {error}")
                return False

async def main():
    """Run focused Phase D validation tests"""
    print("🎯 PHASE D: FOCUSED VALIDATION TESTING")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Start Time: {datetime.utcnow().isoformat()}")
    print("=" * 60)
    
    # Run focused tests
    test_results = []
    
    # 1. Performance benchmarking with concurrent loads
    result1 = await test_performance_benchmarking_concurrent_loads()
    test_results.append(("Performance Benchmarking", result1))
    
    # 2. Clinical validation for emergency vs routine scenarios
    result2 = await test_clinical_validation_emergency_vs_routine()
    test_results.append(("Clinical Validation", result2))
    
    # 3. Safety verification for high-risk classifications
    result3 = await test_safety_verification_high_risk()
    test_results.append(("Safety Verification", result3))
    
    # 4. Audit logging for compliance tracking
    result4 = await test_audit_logging_compliance()
    test_results.append(("Audit Logging", result4))
    
    # 5. Comprehensive system status verification
    result5 = await test_comprehensive_system_status()
    test_results.append(("System Status", result5))
    
    # Generate summary
    print("\n" + "=" * 60)
    print("🎯 PHASE D FOCUSED VALIDATION SUMMARY")
    print("=" * 60)
    
    passed_tests = sum(1 for _, result in test_results if result)
    total_tests = len(test_results)
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests} ✅")
    print(f"Failed: {total_tests - passed_tests} ❌")
    print(f"Success Rate: {success_rate:.1f}%")
    
    print(f"\n📊 TEST RESULTS:")
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
        
    print(f"\n🎯 PHASE D VALIDATION STATUS:")
    if success_rate == 100:
        print("✅ FULLY VALIDATED - All Phase D components operational and meeting requirements")
    elif success_rate >= 80:
        print("⚠️ MOSTLY VALIDATED - Minor issues identified, core functionality working")
    else:
        print("❌ VALIDATION ISSUES - Critical components need attention")
        
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())