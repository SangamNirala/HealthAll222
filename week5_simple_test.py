#!/usr/bin/env python3
"""
WEEK 5 SIMPLE TESTING - Basic functionality test to validate Week 5 endpoints

This test focuses on basic endpoint availability and response structure validation
without triggering the complex validation logic that has import issues.
"""

import requests
import json
import time
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://medtest-platform.preview.emergentagent.com/api"

def test_basic_endpoint_availability():
    """Test basic endpoint availability"""
    print("🔍 TESTING BASIC ENDPOINT AVAILABILITY")
    print("=" * 60)
    
    endpoints = [
        ("GET", "/medical-ai/week5-integration-performance", {}),
    ]
    
    for method, endpoint, payload in endpoints:
        try:
            print(f"Testing {method} {endpoint}...")
            
            if method == "GET":
                response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=10)
            else:
                response = requests.post(f"{BACKEND_URL}{endpoint}", json=payload, timeout=10)
            
            print(f"  Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ SUCCESS - Response keys: {list(data.keys())[:5]}...")
            elif response.status_code == 422:
                print(f"  ⚠️  VALIDATION ERROR - {response.text[:100]}...")
            elif response.status_code == 500:
                print(f"  ❌ SERVER ERROR - {response.text[:100]}...")
            else:
                print(f"  ❓ OTHER - {response.text[:100]}...")
                
        except Exception as e:
            print(f"  ❌ EXCEPTION - {str(e)}")
        
        print()

def test_week5_integration_performance_detailed():
    """Test Week 5 Integration Performance endpoint in detail"""
    print("📊 TESTING WEEK 5 INTEGRATION PERFORMANCE (DETAILED)")
    print("=" * 60)
    
    try:
        response = requests.get(
            f"{BACKEND_URL}/medical-ai/week5-integration-performance",
            timeout=15
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS - Week 5 Integration Performance endpoint is working")
            
            # Check main sections
            main_sections = [
                "status", "integration_testing_metrics", "clinical_validation_metrics",
                "week5_capabilities", "validation_targets", "system_readiness_assessment"
            ]
            
            print("\n📋 Response Structure Analysis:")
            for section in main_sections:
                if section in data:
                    print(f"  ✅ {section}: Present")
                    if isinstance(data[section], dict):
                        print(f"     Keys: {list(data[section].keys())[:3]}...")
                else:
                    print(f"  ❌ {section}: Missing")
            
            # Check specific values
            print("\n🎯 Key Values:")
            print(f"  System Status: {data.get('status', 'unknown')}")
            
            capabilities = data.get('week5_capabilities', {})
            print(f"  Integration Testing Active: {capabilities.get('integration_testing_active', False)}")
            print(f"  Clinical Validation Active: {capabilities.get('clinical_validation_active', False)}")
            print(f"  Performance Benchmarking Active: {capabilities.get('performance_benchmarking_active', False)}")
            
            targets = data.get('validation_targets', {})
            print(f"  Clinical Accuracy Target: {targets.get('clinical_accuracy_target', 0):.1%}")
            print(f"  Processing Time Target: {targets.get('processing_time_target_ms', 0)}ms")
            
            readiness = data.get('system_readiness_assessment', {})
            print(f"  Production Deployment Ready: {readiness.get('production_deployment_ready', False)}")
            
            coverage = data.get('testing_coverage', {})
            print(f"  Total Test Scenarios: {coverage.get('total_test_scenarios', 0)}")
            
            qa = data.get('quality_assurance', {})
            print(f"  Clinical Accuracy Validated: {qa.get('clinical_accuracy_validated', False)}")
            print(f"  Safety Assessment Completed: {qa.get('safety_assessment_completed', False)}")
            
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ EXCEPTION - {str(e)}")
    
    print()

def test_integration_testing_with_minimal_payload():
    """Test integration testing with minimal payload to avoid validation errors"""
    print("🧪 TESTING INTEGRATION TESTING (MINIMAL PAYLOAD)")
    print("=" * 60)
    
    test_categories = [
        "complete_pipeline",
        "clinical_validation", 
        "performance_benchmarking",
        "comprehensive_suite"
    ]
    
    for category in test_categories:
        try:
            print(f"Testing category: {category}...")
            
            payload = {
                "test_category": category,
                "test_parameters": {}
            }
            
            response = requests.post(
                f"{BACKEND_URL}/medical-ai/integration-testing",
                json=payload,
                timeout=15
            )
            
            print(f"  Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ SUCCESS - Test Type: {data.get('test_type')}")
                print(f"     Total Tests: {data.get('total_tests', 0)}")
                print(f"     Success Rate: {data.get('success_rate', 0):.1%}")
                print(f"     Algorithm Version: {data.get('algorithm_version', 'unknown')}")
            elif response.status_code == 422:
                print(f"  ⚠️  VALIDATION ERROR - {response.text[:150]}...")
            elif response.status_code == 500:
                print(f"  ❌ SERVER ERROR - {response.text[:150]}...")
            else:
                print(f"  ❓ OTHER ERROR - {response.text[:150]}...")
                
        except Exception as e:
            print(f"  ❌ EXCEPTION - {str(e)}")
        
        print()

def test_clinical_validation_with_minimal_payload():
    """Test clinical validation with minimal payload"""
    print("🔬 TESTING CLINICAL VALIDATION (MINIMAL PAYLOAD)")
    print("=" * 60)
    
    test_cases = [
        {"specialty": "emergency_medicine", "scenario_count": 1},
        {"specialty": "cardiology", "scenario_count": 1},
        {"specialty": None, "scenario_count": 1}  # All specialties
    ]
    
    for test_case in test_cases:
        try:
            specialty_name = test_case["specialty"] or "All Specialties"
            print(f"Testing {specialty_name}...")
            
            response = requests.post(
                f"{BACKEND_URL}/medical-ai/clinical-validation",
                json=test_case,
                timeout=15
            )
            
            print(f"  Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ SUCCESS - Validation Type: {data.get('validation_type')}")
                print(f"     Total Scenarios: {data.get('total_scenarios', 0)}")
                print(f"     Clinical Accuracy: {data.get('clinical_accuracy_rate', 0):.1%}")
                print(f"     Safety Score: {data.get('safety_score', 0):.1%}")
            elif response.status_code == 422:
                print(f"  ⚠️  VALIDATION ERROR - {response.text[:150]}...")
            elif response.status_code == 500:
                print(f"  ❌ SERVER ERROR - {response.text[:150]}...")
            else:
                print(f"  ❓ OTHER ERROR - {response.text[:150]}...")
                
        except Exception as e:
            print(f"  ❌ EXCEPTION - {str(e)}")
        
        print()

def test_performance_benchmarking():
    """Test performance benchmarking endpoint"""
    print("⚡ TESTING PERFORMANCE BENCHMARKING")
    print("=" * 60)
    
    try:
        print("Testing performance benchmarking...")
        
        response = requests.post(
            f"{BACKEND_URL}/medical-ai/performance-benchmarking",
            json={},
            timeout=15
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS - Performance Benchmarking endpoint is working")
            
            print(f"  Benchmarking Type: {data.get('benchmarking_type', 'unknown')}")
            
            overall_metrics = data.get('overall_performance_metrics', {})
            if overall_metrics:
                total_pipeline = overall_metrics.get('total_pipeline_performance', {})
                print(f"  Average Processing Time: {total_pipeline.get('average_processing_time_ms', 0):.1f}ms")
                print(f"  Target Compliance: {total_pipeline.get('target_compliance', False)}")
            
            system_health = data.get('system_health_assessment', {})
            if system_health:
                print(f"  Health Score: {system_health.get('overall_health_score', 0):.1%}")
                print(f"  Performance Grade: {system_health.get('performance_grade', 'unknown')}")
                print(f"  Production Readiness: {system_health.get('production_readiness', 'unknown')}")
                
        elif response.status_code == 500:
            print(f"❌ SERVER ERROR - {response.text[:200]}...")
        else:
            print(f"❓ OTHER ERROR - {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ EXCEPTION - {str(e)}")
    
    print()

def main():
    """Run all simple Week 5 tests"""
    print("🚀 WEEK 5 SIMPLE TESTING - BASIC FUNCTIONALITY VALIDATION")
    print("=" * 100)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test started at: {datetime.now().isoformat()}")
    print("=" * 100)
    print()
    
    # Run simple tests
    test_basic_endpoint_availability()
    test_week5_integration_performance_detailed()
    test_integration_testing_with_minimal_payload()
    test_clinical_validation_with_minimal_payload()
    test_performance_benchmarking()
    
    print("=" * 100)
    print("🏁 WEEK 5 SIMPLE TESTING COMPLETE")
    print("=" * 100)

if __name__ == "__main__":
    main()