#!/usr/bin/env python3
"""
🔮 WEEK 4 PREDICTIVE MODELING & SUBSPECIALTY CLINICAL REASONING TESTING

Focused testing of Week 4 implementations that are actually available.
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Any

# Test configuration
BACKEND_URL = "https://symptom-parse.preview.emergentagent.com/api"
TEST_TIMEOUT = 30

class Week4TestSuite:
    """Week 4 focused test suite"""
    
    def __init__(self):
        self.session = None
        self.test_results = {
            "predictive_modeling": {},
            "subspecialty_reasoning": {},
            "overall_status": "pending"
        }
        self.start_time = time.time()
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT))
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def run_week4_tests(self):
        """Run Week 4 specific tests"""
        print("🔮 WEEK 4 PREDICTIVE MODELING & SUBSPECIALTY CLINICAL REASONING TESTING")
        print("=" * 70)
        
        try:
            await self.test_predictive_modeling()
            await self.test_subspecialty_reasoning()
            await self.generate_report()
            
        except Exception as e:
            print(f"❌ CRITICAL ERROR: {str(e)}")
            self.test_results["overall_status"] = "failed"
    
    async def test_predictive_modeling(self):
        """Test predictive modeling endpoints"""
        print("\n🎯 Testing Predictive Intent Modeling...")
        
        # Test basic predictive modeling endpoint
        try:
            payload = {
                "conversation_history": [
                    {"message": "I have chest pain", "intent": "symptom_reporting", "timestamp": "2024-01-15T10:00:00Z"}
                ],
                "current_context": {"patient_data": {"age": 45}},
                "prediction_horizon": "next_3_intents"
            }
            
            start_time = time.time()
            async with self.session.post(
                f"{BACKEND_URL}/medical-ai/predictive-intent-modeling",
                json=payload
            ) as response:
                processing_time = (time.time() - start_time) * 1000
                
                if response.status == 200:
                    data = await response.json()
                    print(f"  ✅ Predictive Intent Modeling: SUCCESS ({processing_time:.1f}ms)")
                    print(f"      Response keys: {list(data.keys())}")
                    
                    self.test_results["predictive_modeling"]["basic_test"] = {
                        "status": "success",
                        "processing_time_ms": processing_time,
                        "response_keys": list(data.keys())
                    }
                else:
                    error_text = await response.text()
                    print(f"  ❌ Predictive Intent Modeling: HTTP {response.status}")
                    print(f"      Error: {error_text}")
                    
                    self.test_results["predictive_modeling"]["basic_test"] = {
                        "status": "failed",
                        "error": f"HTTP {response.status}",
                        "details": error_text
                    }
                    
        except Exception as e:
            print(f"  ❌ Predictive Intent Modeling: Exception - {str(e)}")
            self.test_results["predictive_modeling"]["basic_test"] = {
                "status": "error",
                "error": str(e)
            }
        
        # Test performance metrics endpoint
        try:
            async with self.session.get(f"{BACKEND_URL}/medical-ai/predictive-modeling-performance") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"  ✅ Performance Metrics: SUCCESS")
                    print(f"      Metrics: {list(data.keys())}")
                    
                    self.test_results["predictive_modeling"]["performance_metrics"] = {
                        "status": "success",
                        "metrics": list(data.keys())
                    }
                else:
                    error_text = await response.text()
                    print(f"  ❌ Performance Metrics: HTTP {response.status}")
                    self.test_results["predictive_modeling"]["performance_metrics"] = {
                        "status": "failed",
                        "error": f"HTTP {response.status}"
                    }
                    
        except Exception as e:
            print(f"  ❌ Performance Metrics: Exception - {str(e)}")
    
    async def test_subspecialty_reasoning(self):
        """Test subspecialty reasoning endpoints"""
        print("\n🏥 Testing Subspecialty Clinical Reasoning...")
        
        subspecialties = ["cardiology", "neurology", "emergency_medicine"]
        
        for subspecialty in subspecialties:
            try:
                payload = {
                    "subspecialty": subspecialty,
                    "intents": [{"intent_name": f"{subspecialty}_assessment", "confidence": 0.9}],
                    "context": {
                        "patient_data": {"age": 50},
                        "message": f"Testing {subspecialty} reasoning",
                        "urgency_level": "moderate"
                    }
                }
                
                start_time = time.time()
                async with self.session.post(
                    f"{BACKEND_URL}/medical-ai/subspecialty-reasoning",
                    json=payload
                ) as response:
                    processing_time = (time.time() - start_time) * 1000
                    
                    if response.status == 200:
                        data = await response.json()
                        print(f"  ✅ {subspecialty.title()}: SUCCESS ({processing_time:.1f}ms)")
                        print(f"      Response keys: {list(data.keys())}")
                        
                        self.test_results["subspecialty_reasoning"][subspecialty] = {
                            "status": "success",
                            "processing_time_ms": processing_time,
                            "response_keys": list(data.keys())
                        }
                    else:
                        error_text = await response.text()
                        print(f"  ❌ {subspecialty.title()}: HTTP {response.status}")
                        print(f"      Error: {error_text}")
                        
                        self.test_results["subspecialty_reasoning"][subspecialty] = {
                            "status": "failed",
                            "error": f"HTTP {response.status}",
                            "details": error_text
                        }
                        
            except Exception as e:
                print(f"  ❌ {subspecialty.title()}: Exception - {str(e)}")
                self.test_results["subspecialty_reasoning"][subspecialty] = {
                    "status": "error",
                    "error": str(e)
                }
    
    async def generate_report(self):
        """Generate test report"""
        print("\n" + "=" * 70)
        print("📋 WEEK 4 TEST REPORT")
        print("=" * 70)
        
        total_time = time.time() - self.start_time
        
        # Count successes
        predictive_success = sum(1 for result in self.test_results["predictive_modeling"].values() 
                               if isinstance(result, dict) and result.get("status") == "success")
        predictive_total = len(self.test_results["predictive_modeling"])
        
        subspecialty_success = sum(1 for result in self.test_results["subspecialty_reasoning"].values() 
                                 if isinstance(result, dict) and result.get("status") == "success")
        subspecialty_total = len(self.test_results["subspecialty_reasoning"])
        
        total_success = predictive_success + subspecialty_success
        total_tests = predictive_total + subspecialty_total
        success_rate = (total_success / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n🎯 RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Successful: {total_success}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Total Time: {total_time:.1f}s")
        
        if predictive_total > 0:
            print(f"\n📊 Predictive Modeling: {predictive_success}/{predictive_total} ({predictive_success/predictive_total*100:.1f}%)")
        
        if subspecialty_total > 0:
            print(f"🏥 Subspecialty Reasoning: {subspecialty_success}/{subspecialty_total} ({subspecialty_success/subspecialty_total*100:.1f}%)")
        
        # Set overall status
        if success_rate >= 50:
            self.test_results["overall_status"] = "partial_success"
            status_emoji = "⚠️"
            status_text = "PARTIAL SUCCESS"
        else:
            self.test_results["overall_status"] = "failed"
            status_emoji = "❌"
            status_text = "FAILED"
        
        if success_rate >= 80:
            self.test_results["overall_status"] = "success"
            status_emoji = "✅"
            status_text = "SUCCESS"
        
        print(f"\n{status_emoji} Overall Status: {status_text}")
        
        print(f"\n📝 Detailed Results:")
        print(json.dumps(self.test_results, indent=2, default=str))

async def main():
    """Main test execution"""
    async with Week4TestSuite() as test_suite:
        await test_suite.run_week4_tests()

if __name__ == "__main__":
    asyncio.run(main())