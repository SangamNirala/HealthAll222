#!/usr/bin/env python3
"""
🔬 WEEK 5 MEDICAL AI ENDPOINTS FOCUSED TESTING

Testing the specific Week 5 medical AI endpoints to verify critical issues have been fixed:
1. POST /api/medical-ai/integration-testing - ConversationFlowResult attribute issue
2. POST /api/medical-ai/clinical-validation - ValidationResult serialization issue  
3. POST /api/medical-ai/performance-benchmarking - Missing '_analyze_overall_performance' method
4. GET /api/medical-ai/week5-integration-performance - Ensure still working

Focus: Verify fixes for the original issues and capture specific error messages.
"""

import requests
import json
import time
from datetime import datetime
import traceback

# Backend URL from environment
BACKEND_URL = "https://symptom-tracker-3.preview.emergentagent.com/api"

def test_integration_testing_complete_pipeline():
    """Test POST /api/medical-ai/integration-testing with test_category='complete_pipeline'"""
    print("🧪 TESTING POST /api/medical-ai/integration-testing")
    print("   Focus: Verify ConversationFlowResult attribute issue is fixed")
    print("=" * 70)
    
    try:
        print("Testing with test_category='complete_pipeline'...")
        
        # Test payload as specified in review request
        payload = {
            "test_category": "complete_pipeline",
            "performance_targets": {
                "processing_time_ms": 30,
                "accuracy_threshold": 0.95
            },
            "validation_level": "comprehensive"
        }
        
        start_time = time.time()
        response = requests.post(
            f"{BACKEND_URL}/medical-ai/integration-testing",
            json=payload,
            timeout=30
        )
        processing_time = (time.time() - start_time) * 1000
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"⏱️  Processing Time: {processing_time:.1f}ms")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ SUCCESS: Integration testing endpoint working correctly")
                print(f"   Test Type: {data.get('test_type')}")
                print(f"   Total Tests: {data.get('total_tests')}")
                print(f"   Success Rate: {data.get('success_rate', 0):.1%}")
                print(f"   Algorithm Version: {data.get('algorithm_version')}")
                
                # Check for required fields
                required_fields = ["test_type", "total_tests", "passed_tests", "failed_tests", "success_rate"]
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    print(f"⚠️  Missing response fields: {missing_fields}")
                
                return True, "SUCCESS", data
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {str(e)}")
                response_text = response.text
                print(f"📄 Raw response: {response_text[:500]}...")
                return False, f"JSON decode error: {str(e)}", response_text[:500]
        else:
            error_text = response.text
            print(f"❌ HTTP {response.status_code} Error")
            print(f"📄 Error Details: {error_text}")
            
            # Check for specific ConversationFlowResult attribute errors
            if "ConversationFlowResult" in error_text and "attribute" in error_text:
                print(f"🚨 CRITICAL: ConversationFlowResult attribute issue still exists!")
                print(f"🔍 Error contains: ConversationFlowResult attribute problem")
            elif "recommended_interview_strategy" in error_text:
                print(f"🚨 CRITICAL: 'recommended_interview_strategy' attribute error detected!")
            
            return False, f"HTTP {response.status_code}", error_text
            
    except Exception as e:
        print(f"❌ Exception during integration testing: {str(e)}")
        traceback.print_exc()
        return False, f"Exception: {str(e)}", str(e)

def test_clinical_validation():
    """Test POST /api/medical-ai/clinical-validation"""
    print("\n🔬 TESTING POST /api/medical-ai/clinical-validation")
    print("   Focus: Verify ValidationResult serialization works properly")
    print("=" * 70)
    
    try:
        print("Testing clinical validation endpoint...")
        
        # Test payload for clinical validation
        payload = {
            "specialty": "emergency_medicine",
            "validation_criteria": {
                "clinical_accuracy_weight": 0.4,
                "urgency_assessment_weight": 0.35,
                "clinical_context_weight": 0.25
            },
            "safety_assessment": True
        }
        
        start_time = time.time()
        response = requests.post(
            f"{BACKEND_URL}/medical-ai/clinical-validation",
            json=payload,
            timeout=30
        )
        processing_time = (time.time() - start_time) * 1000
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"⏱️  Processing Time: {processing_time:.1f}ms")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ SUCCESS: Clinical validation endpoint working correctly")
                print(f"   Validation Type: {data.get('validation_type')}")
                print(f"   Specialty: {data.get('specialty')}")
                print(f"   Clinical Accuracy: {data.get('clinical_accuracy_rate', 0):.1%}")
                print(f"   Safety Score: {data.get('safety_score', 0):.1%}")
                print(f"   Algorithm Version: {data.get('algorithm_version')}")
                
                # Check for required fields
                required_fields = ["validation_type", "specialty", "total_scenarios", "clinical_accuracy_rate", "safety_score"]
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    print(f"⚠️  Missing response fields: {missing_fields}")
                
                return True, "SUCCESS", data
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {str(e)}")
                response_text = response.text
                print(f"📄 Raw response: {response_text[:500]}...")
                return False, f"JSON decode error: {str(e)}", response_text[:500]
        else:
            error_text = response.text
            print(f"❌ HTTP {response.status_code} Error")
            print(f"📄 Error Details: {error_text}")
            
            # Check for specific ValidationResult serialization errors
            if "ValidationResult" in error_text and ("serialization" in error_text or "Pydantic" in error_text):
                print(f"🚨 CRITICAL: ValidationResult serialization issue still exists!")
                print(f"🔍 Error contains: ValidationResult serialization problem")
            elif "dictionaries" in error_text and "validation" in error_text:
                print(f"🚨 CRITICAL: Pydantic validation error about dictionaries detected!")
            
            return False, f"HTTP {response.status_code}", error_text
            
    except Exception as e:
        print(f"❌ Exception during clinical validation: {str(e)}")
        traceback.print_exc()
        return False, f"Exception: {str(e)}", str(e)

def test_performance_benchmarking():
    """Test POST /api/medical-ai/performance-benchmarking"""
    print("\n⚡ TESTING POST /api/medical-ai/performance-benchmarking")
    print("   Focus: Verify missing '_analyze_overall_performance' method is implemented")
    print("=" * 70)
    
    try:
        print("Testing performance benchmarking endpoint...")
        
        start_time = time.time()
        response = requests.post(
            f"{BACKEND_URL}/medical-ai/performance-benchmarking",
            json={},  # Empty payload as endpoint doesn't require specific parameters
            timeout=30
        )
        processing_time = (time.time() - start_time) * 1000
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"⏱️  Processing Time: {processing_time:.1f}ms")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ SUCCESS: Performance benchmarking endpoint working correctly")
                print(f"   Benchmarking Type: {data.get('benchmarking_type')}")
                
                # Check system health assessment
                system_health = data.get("system_health_assessment", {})
                health_score = system_health.get("overall_health_score", 0)
                performance_grade = system_health.get("performance_grade", "N/A")
                
                print(f"   Health Score: {health_score:.1%}")
                print(f"   Performance Grade: {performance_grade}")
                
                # Check performance targets
                targets = data.get("performance_targets_summary", {})
                all_targets_met = targets.get("all_targets_met", False)
                print(f"   All Targets Met: {all_targets_met}")
                print(f"   Algorithm Version: {data.get('algorithm_version')}")
                
                # Check for required fields
                required_fields = ["benchmarking_type", "benchmark_results", "overall_performance_metrics", "system_health_assessment"]
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    print(f"⚠️  Missing response fields: {missing_fields}")
                
                return True, "SUCCESS", data
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {str(e)}")
                response_text = response.text
                print(f"📄 Raw response: {response_text[:500]}...")
                return False, f"JSON decode error: {str(e)}", response_text[:500]
        else:
            error_text = response.text
            print(f"❌ HTTP {response.status_code} Error")
            print(f"📄 Error Details: {error_text}")
            
            # Check for specific _analyze_overall_performance method errors
            if "_analyze_overall_performance" in error_text:
                print(f"🚨 CRITICAL: '_analyze_overall_performance' method still missing!")
                print(f"🔍 Error contains: _analyze_overall_performance method issue")
            elif "AttributeError" in error_text and "method" in error_text:
                print(f"🚨 CRITICAL: Method missing error detected!")
            
            return False, f"HTTP {response.status_code}", error_text
            
    except Exception as e:
        print(f"❌ Exception during performance benchmarking: {str(e)}")
        traceback.print_exc()
        return False, f"Exception: {str(e)}", str(e)

def test_week5_integration_performance():
    """Test GET /api/medical-ai/week5-integration-performance"""
    print("\n📊 TESTING GET /api/medical-ai/week5-integration-performance")
    print("   Focus: Ensure this endpoint still works properly")
    print("=" * 70)
    
    try:
        print("Testing week5 integration performance endpoint...")
        
        start_time = time.time()
        response = requests.get(
            f"{BACKEND_URL}/medical-ai/week5-integration-performance",
            timeout=30
        )
        processing_time = (time.time() - start_time) * 1000
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"⏱️  Processing Time: {processing_time:.1f}ms")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ SUCCESS: Week5 integration performance endpoint working correctly")
                print(f"   Status: {data.get('status')}")
                
                # Check capabilities
                capabilities = data.get("week5_capabilities", {})
                integration_active = capabilities.get("integration_testing_active", False)
                validation_active = capabilities.get("clinical_validation_active", False)
                benchmarking_active = capabilities.get("performance_benchmarking_active", False)
                
                print(f"   Integration Testing Active: {integration_active}")
                print(f"   Clinical Validation Active: {validation_active}")
                print(f"   Performance Benchmarking Active: {benchmarking_active}")
                
                # Check system readiness
                readiness = data.get("system_readiness_assessment", {})
                deployment_ready = readiness.get("production_deployment_ready", False)
                print(f"   Production Deployment Ready: {deployment_ready}")
                
                # Check for required fields
                required_fields = ["status", "integration_testing_metrics", "clinical_validation_metrics", "week5_capabilities"]
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    print(f"⚠️  Missing response fields: {missing_fields}")
                
                return True, "SUCCESS", data
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {str(e)}")
                response_text = response.text
                print(f"📄 Raw response: {response_text[:500]}...")
                return False, f"JSON decode error: {str(e)}", response_text[:500]
        else:
            error_text = response.text
            print(f"❌ HTTP {response.status_code} Error")
            print(f"📄 Error Details: {error_text}")
            
            return False, f"HTTP {response.status_code}", error_text
            
    except Exception as e:
        print(f"❌ Exception during week5 integration performance: {str(e)}")
        traceback.print_exc()
        return False, f"Exception: {str(e)}", str(e)

def main():
    """Main test execution function"""
    print("🔬 WEEK 5 MEDICAL AI ENDPOINTS FOCUSED TESTING")
    print("=" * 70)
    print("Testing specific endpoints to verify critical issue fixes:")
    print("1. POST /api/medical-ai/integration-testing")
    print("2. POST /api/medical-ai/clinical-validation") 
    print("3. POST /api/medical-ai/performance-benchmarking")
    print("4. GET /api/medical-ai/week5-integration-performance")
    print("=" * 70)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test started at: {datetime.utcnow().isoformat()}")
    print("=" * 70)
    
    # Store test results
    test_results = {}
    
    # Test 1: Integration Testing
    success, status, details = test_integration_testing_complete_pipeline()
    test_results["integration_testing"] = {"success": success, "status": status, "details": details}
    
    # Test 2: Clinical Validation
    success, status, details = test_clinical_validation()
    test_results["clinical_validation"] = {"success": success, "status": status, "details": details}
    
    # Test 3: Performance Benchmarking
    success, status, details = test_performance_benchmarking()
    test_results["performance_benchmarking"] = {"success": success, "status": status, "details": details}
    
    # Test 4: Week5 Integration Performance
    success, status, details = test_week5_integration_performance()
    test_results["week5_integration_performance"] = {"success": success, "status": status, "details": details}
    
    # Generate final report
    print("\n" + "=" * 70)
    print("📋 WEEK 5 FOCUSED TEST REPORT - CRITICAL ISSUE VERIFICATION")
    print("=" * 70)
    
    successful_tests = sum(1 for result in test_results.values() if result["success"])
    total_tests = len(test_results)
    success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n🎯 ENDPOINT TEST RESULTS:")
    
    for endpoint, result in test_results.items():
        endpoint_name = endpoint.replace("_", " ").title()
        status_emoji = "✅" if result["success"] else "❌"
        print(f"   {status_emoji} {endpoint_name}: {result['status']}")
    
    print(f"\n📊 OVERALL RESULTS:")
    print(f"   Total Endpoints Tested: {total_tests}")
    print(f"   Successful Endpoints: {successful_tests}")
    print(f"   Success Rate: {success_rate:.1f}%")
    
    print(f"\n🔍 CRITICAL ISSUE STATUS:")
    
    # Check specific issues mentioned in review request
    integration_result = test_results.get("integration_testing", {})
    if integration_result.get("success"):
        print(f"   ✅ ConversationFlowResult attribute issue: FIXED")
    else:
        error_details = str(integration_result.get("details", ""))
        if "ConversationFlowResult" in error_details or "recommended_interview_strategy" in error_details:
            print(f"   ❌ ConversationFlowResult attribute issue: STILL EXISTS")
        else:
            print(f"   ⚠️  ConversationFlowResult attribute issue: UNKNOWN (different error)")
    
    validation_result = test_results.get("clinical_validation", {})
    if validation_result.get("success"):
        print(f"   ✅ ValidationResult serialization issue: FIXED")
    else:
        error_details = str(validation_result.get("details", ""))
        if "ValidationResult" in error_details or "Pydantic" in error_details:
            print(f"   ❌ ValidationResult serialization issue: STILL EXISTS")
        else:
            print(f"   ⚠️  ValidationResult serialization issue: UNKNOWN (different error)")
    
    benchmarking_result = test_results.get("performance_benchmarking", {})
    if benchmarking_result.get("success"):
        print(f"   ✅ Missing '_analyze_overall_performance' method: FIXED")
    else:
        error_details = str(benchmarking_result.get("details", ""))
        if "_analyze_overall_performance" in error_details:
            print(f"   ❌ Missing '_analyze_overall_performance' method: STILL EXISTS")
        else:
            print(f"   ⚠️  Missing '_analyze_overall_performance' method: UNKNOWN (different error)")
    
    performance_result = test_results.get("week5_integration_performance", {})
    if performance_result.get("success"):
        print(f"   ✅ Week5 performance endpoint: WORKING PROPERLY")
    else:
        print(f"   ❌ Week5 performance endpoint: HAS ISSUES")
    
    # Final assessment
    if success_rate == 100:
        overall_status = "ALL ISSUES FIXED"
        status_emoji = "🎉"
    elif success_rate >= 75:
        overall_status = "MOSTLY SUCCESSFUL"
        status_emoji = "⚠️"
    else:
        overall_status = "NEEDS ATTENTION"
        status_emoji = "❌"
    
    print(f"\n🚀 FINAL ASSESSMENT:")
    print(f"   {status_emoji} Overall Status: {overall_status}")
    print(f"   Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print(f"   🎉 All critical issues have been resolved!")
    elif success_rate >= 75:
        print(f"   👍 Most issues resolved, some endpoints need attention")
    else:
        print(f"   🔧 Multiple critical issues still need to be addressed")
    
    print("\n" + "=" * 70)
    print("🏁 WEEK 5 FOCUSED TESTING COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()