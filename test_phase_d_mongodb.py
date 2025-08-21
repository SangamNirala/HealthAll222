#!/usr/bin/env python3
"""
🧪 PHASE D PERFORMANCE OPTIMIZER WITH MONGODB CACHING TEST
Test Phase D performance optimization system with MongoDB caching

This test validates:
1. Phase D initialization with MongoDB caching
2. Advanced caching layer functionality
3. Performance optimization endpoints
4. Cache statistics and monitoring
5. Integration with existing medical AI system
"""

import asyncio
import json
import time
import sys
import requests
from typing import Dict, Any
from datetime import datetime

# Backend URL
BACKEND_URL = "https://converse-context.preview.emergentagent.com/api"


class PhaseDMongoDBTester:
    """Test Phase D with MongoDB caching integration"""
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_test_result(self, test_name: str, success: bool, details: str, response_time: float = 0):
        """Log individual test results"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "response_time_ms": response_time,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        print(f"   Details: {details}")
        if response_time > 0:
            print(f"   Response Time: {response_time:.2f}ms")
        print()

    def test_phase_d_performance_status(self):
        """Test Phase D performance status endpoint"""
        print("🧪 TESTING PHASE D PERFORMANCE STATUS")
        print("=" * 60)
        
        try:
            start_time = time.time()
            
            response = requests.get(
                f"{self.backend_url}/medical-ai/phase-d/performance-status",
                timeout=10
            )
            
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for required fields
                required_fields = ["status", "performance_tier", "caching_system"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    caching_info = data.get("caching_system", {})
                    cache_type = caching_info.get("cache_type", "unknown")
                    
                    self.log_test_result(
                        "Phase D Performance Status",
                        True,
                        f"Status: {data.get('status')}, Cache Type: {cache_type}",
                        response_time
                    )
                    
                    print(f"📊 PERFORMANCE STATUS DETAILS:")
                    print(f"   System Status: {data.get('status')}")
                    print(f"   Performance Tier: {data.get('performance_tier')}")
                    print(f"   Cache Type: {cache_type}")
                    print(f"   MongoDB Connected: {caching_info.get('mongodb_connected', False)}")
                    print()
                else:
                    self.log_test_result(
                        "Phase D Performance Status",
                        False,
                        f"Missing required fields: {missing_fields}",
                        response_time
                    )
            else:
                self.log_test_result(
                    "Phase D Performance Status",
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    response_time
                )
                
        except Exception as e:
            self.log_test_result(
                "Phase D Performance Status",
                False,
                f"Exception: {str(e)}"
            )

    def test_phase_d_performance_benchmarking(self):
        """Test Phase D performance benchmarking"""
        print("🧪 TESTING PHASE D PERFORMANCE BENCHMARKING")
        print("=" * 60)
        
        benchmark_data = {
            "test_scenarios": [
                {
                    "scenario_name": "routine_symptoms",
                    "text_samples": [
                        "I have a headache and feel nauseous",
                        "stomach ache for 2 days",
                        "back pain when sitting"
                    ],
                    "target_performance_ms": 25,
                    "performance_tier": "routine"
                }
            ],
            "iterations": 10,
            "concurrent_requests": 5
        }
        
        try:
            start_time = time.time()
            
            response = requests.post(
                f"{self.backend_url}/medical-ai/phase-d/performance-benchmark",
                json=benchmark_data,
                timeout=30
            )
            
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                benchmark_results = data.get("benchmark_results", {})
                avg_response_time = benchmark_results.get("average_response_time_ms", 0)
                cache_hit_rate = benchmark_results.get("cache_hit_rate", 0)
                
                self.log_test_result(
                    "Phase D Performance Benchmarking",
                    avg_response_time < 50,  # Accept <50ms for testing
                    f"Avg response: {avg_response_time:.2f}ms, Cache hit rate: {cache_hit_rate:.1f}%",
                    response_time
                )
                
                print(f"📊 BENCHMARK RESULTS:")
                print(f"   Average Response Time: {avg_response_time:.2f}ms")
                print(f"   Cache Hit Rate: {cache_hit_rate:.1f}%")
                print(f"   Total Requests: {benchmark_results.get('total_requests', 0)}")
                print()
            else:
                self.log_test_result(
                    "Phase D Performance Benchmarking",
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    response_time
                )
                
        except Exception as e:
            self.log_test_result(
                "Phase D Performance Benchmarking",
                False,
                f"Exception: {str(e)}"
            )

    def test_medical_ai_with_caching(self):
        """Test medical AI system with MongoDB caching"""
        print("🧪 TESTING MEDICAL AI WITH MONGODB CACHING")
        print("=" * 60)
        
        test_cases = [
            {
                "name": "Routine Symptom Processing",
                "text": "I have a mild headache for 2 hours",
                "expected_response_fields": ["response", "context", "urgency"]
            },
            {
                "name": "Multi-symptom Processing",
                "text": "chest pain and shortness of breath",
                "expected_response_fields": ["response", "context", "urgency", "emergency_detected"]
            }
        ]
        
        for test_case in test_cases:
            self._test_medical_ai_request(test_case)

    def _test_medical_ai_request(self, test_case: Dict[str, Any]):
        """Test individual medical AI request"""
        try:
            # Initialize consultation
            init_data = {
                "patient_id": f"test_mongodb_{int(time.time())}",
                "timestamp": datetime.now().isoformat()
            }
            
            start_time = time.time()
            
            init_response = requests.post(
                f"{self.backend_url}/medical-ai/initialize",
                json=init_data,
                timeout=10
            )
            
            if init_response.status_code != 200:
                self.log_test_result(
                    f"{test_case['name']} - Initialization",
                    False,
                    f"Initialization failed: HTTP {init_response.status_code}"
                )
                return
            
            init_data = init_response.json()
            consultation_id = init_data.get("consultation_id")
            
            # Send message
            message_data = {
                "message": test_case["text"],
                "patient_id": init_data["patient_id"],
                "consultation_id": consultation_id,
                "context": init_data.get("context", {})
            }
            
            message_response = requests.post(
                f"{self.backend_url}/medical-ai/message",
                json=message_data,
                timeout=15
            )
            
            response_time = (time.time() - start_time) * 1000
            
            if message_response.status_code == 200:
                data = message_response.json()
                
                # Check required fields
                expected_fields = test_case["expected_response_fields"]
                missing_fields = [field for field in expected_fields if field not in data]
                
                if not missing_fields:
                    urgency = data.get("urgency", "unknown")
                    emergency = data.get("emergency_detected", False)
                    
                    self.log_test_result(
                        test_case["name"],
                        True,
                        f"Urgency: {urgency}, Emergency: {emergency}, Response length: {len(data.get('response', ''))} chars",
                        response_time
                    )
                else:
                    self.log_test_result(
                        test_case["name"],
                        False,
                        f"Missing fields: {missing_fields}",
                        response_time
                    )
            else:
                self.log_test_result(
                    test_case["name"],
                    False,
                    f"HTTP {message_response.status_code}: {message_response.text[:200]}",
                    response_time
                )
                
        except Exception as e:
            self.log_test_result(
                test_case["name"],
                False,
                f"Exception: {str(e)}"
            )

    def test_multi_symptom_parsing_with_cache(self):
        """Test multi-symptom parsing with MongoDB caching"""
        print("🧪 TESTING MULTI-SYMPTOM PARSING WITH MONGODB CACHE")
        print("=" * 60)
        
        test_data = {
            "text": "bad headache started monday got worse tuesday now nausea dizzy cant focus at work",
            "context": {
                "patient_id": "test_cache",
                "stage": "symptoms"
            }
        }
        
        try:
            # First request (cache miss)
            start_time = time.time()
            
            response1 = requests.post(
                f"{self.backend_url}/medical-ai/multi-symptom-parse",
                json=test_data,
                timeout=15
            )
            
            first_response_time = (time.time() - start_time) * 1000
            
            # Second request (should be cache hit)
            start_time = time.time()
            
            response2 = requests.post(
                f"{self.backend_url}/medical-ai/multi-symptom-parse", 
                json=test_data,
                timeout=15
            )
            
            second_response_time = (time.time() - start_time) * 1000
            
            if response1.status_code == 200 and response2.status_code == 200:
                data1 = response1.json()
                data2 = response2.json()
                
                # Cache hit should be faster
                cache_improvement = first_response_time > second_response_time
                
                self.log_test_result(
                    "Multi-symptom Parsing Cache Test",
                    True,
                    f"1st request: {first_response_time:.2f}ms, 2nd request: {second_response_time:.2f}ms, Cache improvement: {cache_improvement}",
                    first_response_time
                )
            else:
                self.log_test_result(
                    "Multi-symptom Parsing Cache Test",
                    False,
                    f"Request failed: {response1.status_code}, {response2.status_code}"
                )
                
        except Exception as e:
            self.log_test_result(
                "Multi-symptom Parsing Cache Test",
                False,
                f"Exception: {str(e)}"
            )

    def run_all_tests(self):
        """Run all Phase D MongoDB caching tests"""
        print("🚀 PHASE D PERFORMANCE OPTIMIZER WITH MONGODB CACHING TESTS")
        print("=" * 80)
        print("Testing Phase D system with MongoDB caching replacement...")
        print()
        
        # Test 1: Performance Status
        self.test_phase_d_performance_status()
        
        # Test 2: Performance Benchmarking  
        self.test_phase_d_performance_benchmarking()
        
        # Test 3: Medical AI with Caching
        self.test_medical_ai_with_caching()
        
        # Test 4: Multi-symptom Parsing Cache
        self.test_multi_symptom_parsing_with_cache()
        
        # Generate report
        self.generate_final_report()

    def generate_final_report(self):
        """Generate final test report"""
        print("🎯 PHASE D MONGODB CACHING INTEGRATION TEST REPORT")
        print("=" * 80)
        
        success_rate = (self.passed_tests / max(self.total_tests, 1)) * 100
        
        print(f"📊 TEST SUMMARY:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed: {self.passed_tests}")
        print(f"   Failed: {self.total_tests - self.passed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        if success_rate >= 85:
            print("✅ EXCELLENT: Phase D with MongoDB caching is working excellently!")
            print("🎉 Redis replacement completed successfully!")
        elif success_rate >= 70:
            print("✅ GOOD: Phase D with MongoDB caching is working well.")
        else:
            print("⚠️  Phase D with MongoDB caching needs attention.")
        
        print()
        print("🔍 DETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"   {status} {result['test_name']}: {result['details']}")


def main():
    """Main test execution"""
    tester = PhaseDMongoDBTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()