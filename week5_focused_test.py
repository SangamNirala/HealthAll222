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
BACKEND_URL = "https://medbot-query.preview.emergentagent.com/api"

def test_week5_integration_testing():
    """Test Week 5 Integration Testing with correct request format"""
    print("🧪 TESTING WEEK 5 INTEGRATION TESTING FRAMEWORK")
    print("=" * 60)
    
    # Test 1: Complete Pipeline Integration with correct format
    try:
        print("Testing Complete Pipeline Integration...")
        
        payload = {
            "test_category": "complete_pipeline",
            "test_parameters": {
                "test_scenario": "acute_chest_pain",
                "integration_type": "end_to_end_pipeline",
                "components_to_test": ["week1", "week2", "week3", "week4"],
                "performance_targets": {
                    "total_processing_time_ms": 30,
                    "accuracy_threshold": 0.95
                },
                "validation_level": "comprehensive"
            }
        }
        
        response = requests.post(
            f"{BACKEND_URL}/medical-ai/integration-testing",
            json=payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS - Test Type: {data.get('test_type')}")
            print(f"   Total Tests: {data.get('total_tests')}")
            print(f"   Success Rate: {data.get('success_rate', 0):.1%}")
            print(f"   Algorithm Version: {data.get('algorithm_version')}")
        else:
            print(f"❌ FAILED - {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEPTION - {str(e)}")
    
    print()

def test_week5_clinical_validation():
    """Test Week 5 Clinical Validation with correct request format"""
    print("🔬 TESTING WEEK 5 CLINICAL VALIDATION SCENARIOS")
    print("=" * 60)
    
    # Test 1: Emergency Medicine Validation
    try:
        print("Testing Emergency Medicine Clinical Validation...")
        
        payload = {
            "specialty": "emergency_medicine",
            "scenario_count": 5,
            "include_performance_metrics": True
        }
        
        response = requests.post(
            f"{BACKEND_URL}/medical-ai/clinical-validation",
            json=payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS - Validation Type: {data.get('validation_type')}")
            print(f"   Specialty: {data.get('specialty')}")
            print(f"   Total Scenarios: {data.get('total_scenarios')}")
            print(f"   Clinical Accuracy: {data.get('clinical_accuracy_rate', 0):.1%}")
            print(f"   Safety Score: {data.get('safety_score', 0):.1%}")
        else:
            print(f"❌ FAILED - {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEPTION - {str(e)}")
    
    print()

def test_week5_performance_benchmarking():
    """Test Week 5 Performance Benchmarking"""
    print("⚡ TESTING WEEK 5 PERFORMANCE BENCHMARKING")
    print("=" * 60)
    
    try:
        print("Testing Performance Benchmarking...")
        
        response = requests.post(
            f"{BACKEND_URL}/medical-ai/performance-benchmarking",
            json={},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS - Benchmarking Type: {data.get('benchmarking_type')}")
            
            # Check overall performance metrics
            overall_metrics = data.get('overall_performance_metrics', {})
            total_pipeline = overall_metrics.get('total_pipeline_performance', {})
            avg_time = total_pipeline.get('average_processing_time_ms', 0)
            
            print(f"   Average Processing Time: {avg_time:.1f}ms")
            print(f"   Target Compliance: {total_pipeline.get('target_compliance', False)}")
            
            # Check system health
            system_health = data.get('system_health_assessment', {})
            print(f"   Health Score: {system_health.get('overall_health_score', 0):.1%}")
            print(f"   Performance Grade: {system_health.get('performance_grade', 'N/A')}")
            
        else:
            print(f"❌ FAILED - {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEPTION - {str(e)}")
    
    print()

def test_week5_integration_performance():
    """Test Week 5 Integration Performance Metrics"""
    print("📊 TESTING WEEK 5 INTEGRATION PERFORMANCE METRICS")
    print("=" * 60)
    
    try:
        print("Testing Week 5 Integration Performance...")
        
        response = requests.get(
            f"{BACKEND_URL}/medical-ai/week5-integration-performance",
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS - Status: {data.get('status')}")
            
            # Check Week 5 capabilities
            capabilities = data.get('week5_capabilities', {})
            print(f"   Integration Testing Active: {capabilities.get('integration_testing_active', False)}")
            print(f"   Clinical Validation Active: {capabilities.get('clinical_validation_active', False)}")
            print(f"   Performance Benchmarking Active: {capabilities.get('performance_benchmarking_active', False)}")
            
            # Check validation targets
            targets = data.get('validation_targets', {})
            print(f"   Clinical Accuracy Target: {targets.get('clinical_accuracy_target', 0):.1%}")
            print(f"   Processing Time Target: {targets.get('processing_time_target_ms', 0)}ms")
            
            # Check system readiness
            readiness = data.get('system_readiness_assessment', {})
            print(f"   Production Deployment Ready: {readiness.get('production_deployment_ready', False)}")
            
        else:
            print(f"❌ FAILED - {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEPTION - {str(e)}")
    
    print()

def test_clinical_validation_scenarios():
    """Test specific clinical validation scenarios"""
    print("🏥 TESTING SPECIFIC CLINICAL VALIDATION SCENARIOS")
    print("=" * 60)
    
    scenarios = [
        {"specialty": "cardiology", "scenario_count": 3},
        {"specialty": "neurology", "scenario_count": 3},
        {"specialty": None, "scenario_count": 10}  # All specialties
    ]
    
    for scenario in scenarios:
        try:
            specialty_name = scenario["specialty"] or "All Specialties"
            print(f"Testing {specialty_name} Clinical Validation...")
            
            response = requests.post(
                f"{BACKEND_URL}/medical-ai/clinical-validation",
                json=scenario,
                timeout=30
            )
            
            print(f"  Status Code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ SUCCESS - Total Scenarios: {data.get('total_scenarios')}")
                print(f"     Clinical Accuracy: {data.get('clinical_accuracy_rate', 0):.1%}")
                print(f"     Safety Score: {data.get('safety_score', 0):.1%}")
                
                # Check production readiness
                prod_readiness = data.get('production_readiness', {})
                deployment_rec = prod_readiness.get('deployment_recommendation', 'unknown')
                print(f"     Deployment Recommendation: {deployment_rec}")
                
            else:
                print(f"  ❌ FAILED - {response.text[:200]}...")
                
        except Exception as e:
            print(f"  ❌ EXCEPTION - {str(e)}")
        
        print()

def main():
    """Run all Week 5 focused tests"""
    print("🚀 WEEK 5 FOCUSED TESTING - INTEGRATION TESTING & CLINICAL VALIDATION FRAMEWORK")
    print("=" * 100)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test started at: {datetime.now().isoformat()}")
    print("=" * 100)
    print()
    
    # Run focused tests
    test_week5_integration_testing()
    test_week5_clinical_validation()
    test_week5_performance_benchmarking()
    test_week5_integration_performance()
    test_clinical_validation_scenarios()
    
    print("=" * 100)
    print("🏁 WEEK 5 FOCUSED TESTING COMPLETE")
    print("=" * 100)

if __name__ == "__main__":
    main()