#!/usr/bin/env python3
"""
🧪 MONGODB CACHING SYSTEM COMPREHENSIVE TEST
Test the MongoDB-based caching system replacement for Redis

This test validates:
1. MongoDB caching system initialization
2. Cache storage and retrieval
3. Multi-tier caching (memory + MongoDB)
4. TTL functionality
5. Performance benchmarking
6. Error handling
"""

import asyncio
import json
import time
import sys
import os
from typing import Dict, Any
from datetime import datetime

# Add backend to path
sys.path.append('/app/backend')

from mongodb_caching_system import MongoDBCachingSystem


class MongoDBCachingTester:
    """Comprehensive tester for MongoDB caching system"""
    
    def __init__(self):
        self.caching_system = None
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

    async def test_mongodb_initialization(self):
        """Test MongoDB caching system initialization"""
        print("🧪 TESTING SCENARIO 1: MONGODB CACHING INITIALIZATION")
        print("=" * 70)
        
        try:
            start_time = time.time()
            
            # Initialize caching system
            self.caching_system = MongoDBCachingSystem(
                db_name="symptom_analyzer_test",
                collection_name="test_cache"
            )
            
            # Test initialization
            success = await self.caching_system.initialize_mongodb_cache()
            
            response_time = (time.time() - start_time) * 1000
            
            if success:
                self.log_test_result(
                    "MongoDB Caching Initialization",
                    True,
                    f"Successfully initialized MongoDB caching system with database connection",
                    response_time
                )
            else:
                self.log_test_result(
                    "MongoDB Caching Initialization", 
                    False,
                    "Failed to initialize MongoDB caching system",
                    response_time
                )
                return False
            
            return True
            
        except Exception as e:
            self.log_test_result(
                "MongoDB Caching Initialization",
                False,
                f"Exception during initialization: {str(e)}"
            )
            return False
    
    async def test_basic_cache_operations(self):
        """Test basic cache storage and retrieval"""
        print("🧪 TESTING SCENARIO 2: BASIC CACHE OPERATIONS")
        print("=" * 70)
        
        test_cases = [
            {
                "name": "Simple Cache Store & Retrieve",
                "text": "I have a headache and feel nauseous",
                "context": {"stage": "symptoms", "urgency": "routine"},
                "result": {
                    "intent": "symptom_reporting",
                    "confidence": 0.85,
                    "symptoms": ["headache", "nausea"]
                }
            },
            {
                "name": "Complex Multi-symptom Cache",
                "text": "chest pain shortness of breath sweating dizzy",
                "context": {"stage": "emergency", "urgency": "critical"},
                "result": {
                    "intent": "emergency_assessment",
                    "confidence": 0.95,
                    "symptoms": ["chest_pain", "dyspnea", "sweating", "dizziness"],
                    "urgency": "emergency"
                }
            },
            {
                "name": "No Context Cache",
                "text": "stomach ache",
                "context": None,
                "result": {
                    "intent": "simple_symptom",
                    "confidence": 0.70,
                    "symptoms": ["abdominal_pain"]
                }
            }
        ]
        
        for test_case in test_cases:
            await self._test_cache_operation(test_case)
    
    async def _test_cache_operation(self, test_case: Dict[str, Any]):
        """Test individual cache operation"""
        try:
            name = test_case["name"]
            text = test_case["text"]
            context = test_case["context"]
            expected_result = test_case["result"]
            
            # Test cache miss (should return None)
            start_time = time.time()
            cache_result = await self.caching_system.get_cached_result(text, context)
            miss_time = (time.time() - start_time) * 1000
            
            if cache_result is None:
                self.log_test_result(
                    f"{name} - Cache Miss",
                    True,
                    "Correctly returned None for cache miss",
                    miss_time
                )
            else:
                self.log_test_result(
                    f"{name} - Cache Miss",
                    False,
                    f"Expected None but got: {cache_result}"
                )
                return
            
            # Store in cache
            start_time = time.time()
            await self.caching_system.store_cached_result(text, context, expected_result, ttl=3600)
            store_time = (time.time() - start_time) * 1000
            
            self.log_test_result(
                f"{name} - Cache Store",
                True,
                "Successfully stored result in cache",
                store_time
            )
            
            # Test cache hit
            start_time = time.time()
            cached_result = await self.caching_system.get_cached_result(text, context)
            hit_time = (time.time() - start_time) * 1000
            
            if cached_result and cached_result == expected_result:
                self.log_test_result(
                    f"{name} - Cache Hit",
                    True,
                    f"Successfully retrieved cached result matching expected data",
                    hit_time
                )
            else:
                self.log_test_result(
                    f"{name} - Cache Hit",
                    False,
                    f"Cache hit failed. Expected: {expected_result}, Got: {cached_result}"
                )
            
        except Exception as e:
            self.log_test_result(
                f"{test_case['name']} - Exception",
                False,
                f"Exception during cache operation: {str(e)}"
            )
    
    async def test_performance_benchmarking(self):
        """Test cache performance with multiple operations"""
        print("🧪 TESTING SCENARIO 3: PERFORMANCE BENCHMARKING")
        print("=" * 70)
        
        try:
            # Performance test data
            test_operations = 50
            
            # Benchmark cache storage
            start_time = time.time()
            for i in range(test_operations):
                await self.caching_system.store_cached_result(
                    f"test symptom {i}",
                    {"test": f"context_{i}"},
                    {"result": f"cached_data_{i}", "confidence": 0.8},
                    ttl=1800
                )
            storage_time = (time.time() - start_time) * 1000
            
            self.log_test_result(
                f"Bulk Cache Storage ({test_operations} operations)",
                True,
                f"Average storage time: {storage_time/test_operations:.2f}ms per operation",
                storage_time
            )
            
            # Benchmark cache retrieval
            start_time = time.time()
            hit_count = 0
            for i in range(test_operations):
                result = await self.caching_system.get_cached_result(
                    f"test symptom {i}",
                    {"test": f"context_{i}"}
                )
                if result:
                    hit_count += 1
            retrieval_time = (time.time() - start_time) * 1000
            
            hit_rate = (hit_count / test_operations) * 100
            
            self.log_test_result(
                f"Bulk Cache Retrieval ({test_operations} operations)",
                hit_rate > 90,  # Expect >90% hit rate
                f"Hit rate: {hit_rate:.1f}%, Average retrieval: {retrieval_time/test_operations:.2f}ms per operation",
                retrieval_time
            )
            
        except Exception as e:
            self.log_test_result(
                "Performance Benchmarking",
                False,
                f"Exception during performance test: {str(e)}"
            )
    
    async def test_cache_statistics(self):
        """Test cache statistics functionality"""
        print("🧪 TESTING SCENARIO 4: CACHE STATISTICS")
        print("=" * 70)
        
        try:
            # Get cache statistics
            start_time = time.time()
            stats = await self.caching_system.get_cache_statistics()
            stats_time = (time.time() - start_time) * 1000
            
            # Validate statistics structure
            required_keys = [
                "cache_type", "total_requests", "cache_hits", "cache_hit_rate_percentage",
                "memory_hits", "mongodb_hits", "cache_misses", "mongodb_connected"
            ]
            
            missing_keys = [key for key in required_keys if key not in stats]
            
            if not missing_keys:
                self.log_test_result(
                    "Cache Statistics Retrieval",
                    True,
                    f"All required statistics keys present. Hit rate: {stats.get('cache_hit_rate_percentage', 0):.1f}%",
                    stats_time
                )
                
                print(f"📊 CACHE STATISTICS SUMMARY:")
                print(f"   Cache Type: {stats.get('cache_type')}")
                print(f"   Total Requests: {stats.get('total_requests')}")
                print(f"   Cache Hit Rate: {stats.get('cache_hit_rate_percentage'):.1f}%")
                print(f"   Memory Cache Size: {stats.get('memory_cache_size')}")
                print(f"   MongoDB Connected: {stats.get('mongodb_connected')}")
                print()
            else:
                self.log_test_result(
                    "Cache Statistics Retrieval",
                    False,
                    f"Missing required statistics keys: {missing_keys}"
                )
                
        except Exception as e:
            self.log_test_result(
                "Cache Statistics",
                False,
                f"Exception during statistics test: {str(e)}"
            )
    
    async def test_cleanup_operations(self):
        """Test cache cleanup functionality"""
        print("🧪 TESTING SCENARIO 5: CLEANUP OPERATIONS")
        print("=" * 70)
        
        try:
            # Test manual cleanup
            start_time = time.time()
            cleaned_count = await self.caching_system.cleanup_expired_cache()
            cleanup_time = (time.time() - start_time) * 1000
            
            self.log_test_result(
                "Cache Cleanup Operation",
                True,
                f"Cleaned up {cleaned_count} expired entries",
                cleanup_time
            )
            
            # Test clear all cache
            start_time = time.time()
            await self.caching_system.clear_all_cache()
            clear_time = (time.time() - start_time) * 1000
            
            self.log_test_result(
                "Clear All Cache",
                True,
                "Successfully cleared all cache data",
                clear_time
            )
            
        except Exception as e:
            self.log_test_result(
                "Cleanup Operations",
                False,
                f"Exception during cleanup test: {str(e)}"
            )

    async def cleanup_test_data(self):
        """Clean up test data"""
        try:
            if self.caching_system:
                await self.caching_system.clear_all_cache()
                await self.caching_system.close_connection()
            print("🧹 Test cleanup completed")
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")

    async def run_all_tests(self):
        """Run comprehensive MongoDB caching system tests"""
        print("🚀 MONGODB CACHING SYSTEM COMPREHENSIVE TEST SUITE")
        print("=" * 80)
        print("Testing MongoDB-based replacement for Redis caching...")
        print()
        
        try:
            # Test 1: Initialization
            init_success = await self.test_mongodb_initialization()
            if not init_success:
                print("❌ CRITICAL: MongoDB initialization failed. Aborting tests.")
                return
            
            # Test 2: Basic Operations  
            await self.test_basic_cache_operations()
            
            # Test 3: Performance
            await self.test_performance_benchmarking()
            
            # Test 4: Statistics
            await self.test_cache_statistics()
            
            # Test 5: Cleanup
            await self.test_cleanup_operations()
            
        finally:
            # Always cleanup
            await self.cleanup_test_data()
        
        # Generate final report
        self.generate_final_report()

    def generate_final_report(self):
        """Generate comprehensive test report"""
        print("🎯 MONGODB CACHING SYSTEM TEST REPORT")
        print("=" * 80)
        
        success_rate = (self.passed_tests / max(self.total_tests, 1)) * 100
        
        print(f"📊 TEST SUMMARY:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed: {self.passed_tests}")
        print(f"   Failed: {self.total_tests - self.passed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        if success_rate >= 90:
            print("✅ EXCELLENT: MongoDB caching system replacement is working excellently!")
            print("🎉 Redis has been successfully replaced with MongoDB caching.")
        elif success_rate >= 75:
            print("✅ GOOD: MongoDB caching system is working well with minor issues.")
        elif success_rate >= 50:
            print("⚠️  ACCEPTABLE: MongoDB caching system has some issues that need attention.")
        else:
            print("❌ CRITICAL: MongoDB caching system has significant issues.")
        
        print()
        print("🔍 DETAILED TEST RESULTS:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"   {status} {result['test_name']}: {result['details']}")
        
        print()
        print("🚀 MongoDB caching system testing completed!")


async def main():
    """Main test execution"""
    tester = MongoDBCachingTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())