#!/usr/bin/env python3
"""
FOCUSED TEMPORAL EXTRACTION FIXES TESTING

Testing the specific temporal extraction fixes requested in the review:
1. Temporal Duration Detection - "3 nights" should be properly detected
2. Temporal Confidence Scoring - should be 0.7+ when patterns found  
3. Enhanced Temporal Patterns - various temporal expressions
4. Multi-symptom with Temporal API endpoint
5. Temporal Analysis Structure validation

Using backend URL from review request: https://symptom-analyzer-6.preview.emergentagent.com
"""

import requests
import json
import time
import sys

# Backend URL from review request
BACKEND_URL = "https://symptom-analyzer-6.preview.emergentagent.com"

def test_temporal_extraction():
    """Test the specific temporal extraction fixes"""
    print("🔍 TEMPORAL EXTRACTION FIXES TESTING")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print()
    
    # Test the specific case from the review request
    test_request = {
        "text": "head hurts stomach upset cant sleep 3 nights",
        "context": {"patient_id": "test-temporal"}
    }
    
    print("📋 Testing Primary Case: 'head hurts stomach upset cant sleep 3 nights'")
    print("-" * 60)
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BACKEND_URL}/api/medical-ai/multi-symptom-parse",
            json=test_request,
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        processing_time = (time.time() - start_time) * 1000
        
        print(f"⏱️  Response Time: {processing_time:.2f}ms")
        print(f"📡 HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Response Received Successfully")
            
            # Pretty print the response structure
            print("\n📊 RESPONSE STRUCTURE ANALYSIS:")
            print("-" * 40)
            
            if data.get("success"):
                print("✅ Success: True")
                
                # Check for temporal analysis
                if data.get("multi_symptom_parse_result"):
                    parse_result = data["multi_symptom_parse_result"]
                    print(f"📋 Parse Result Keys: {list(parse_result.keys())}")
                    
                    # Look for temporal analysis
                    temporal_found = False
                    temporal_confidence = 0.0
                    overall_duration = None
                    
                    if "temporal_analysis" in parse_result:
                        temporal_analysis = parse_result["temporal_analysis"]
                        temporal_found = True
                        print("✅ Temporal Analysis Found")
                        print(f"   Keys: {list(temporal_analysis.keys())}")
                        
                        if "temporal_confidence" in temporal_analysis:
                            temporal_confidence = temporal_analysis["temporal_confidence"]
                            print(f"   Temporal Confidence: {temporal_confidence}")
                        
                        if "overall_duration" in temporal_analysis:
                            overall_duration = temporal_analysis["overall_duration"]
                            print(f"   Overall Duration: {overall_duration}")
                            
                    elif "contextual_analysis" in parse_result:
                        contextual = parse_result["contextual_analysis"]
                        if "temporal" in contextual:
                            temporal_data = contextual["temporal"]
                            temporal_found = True
                            print("✅ Temporal Data in Contextual Analysis")
                            print(f"   Keys: {list(temporal_data.keys())}")
                    
                    if not temporal_found:
                        print("❌ No Temporal Analysis Found")
                        
                    # Check confidence metrics
                    if "confidence_metrics" in parse_result:
                        confidence_metrics = parse_result["confidence_metrics"]
                        print(f"📊 Confidence Metrics: {list(confidence_metrics.keys())}")
                        
                        if "temporal_confidence" in confidence_metrics:
                            temporal_confidence = confidence_metrics["temporal_confidence"]
                            print(f"   Temporal Confidence: {temporal_confidence}")
                
                # Print summary
                print(f"\n📈 Summary: {data.get('summary', {})}")
                print(f"🚨 Urgency: {data.get('urgency_assessment', 'N/A')}")
                
                # Validate temporal extraction fixes
                print("\n🔍 TEMPORAL EXTRACTION VALIDATION:")
                print("-" * 40)
                
                # Test 1: Duration Detection
                duration_detected = overall_duration is not None or "3 nights" in str(data).lower()
                print(f"1. Duration Detection ('3 nights'): {'✅ PASS' if duration_detected else '❌ FAIL'}")
                
                # Test 2: Temporal Confidence > 0
                confidence_valid = temporal_confidence > 0
                print(f"2. Temporal Confidence > 0: {'✅ PASS' if confidence_valid else '❌ FAIL'} ({temporal_confidence})")
                
                # Test 3: Temporal Confidence >= 0.7
                confidence_threshold = temporal_confidence >= 0.7
                print(f"3. Temporal Confidence >= 0.7: {'✅ PASS' if confidence_threshold else '❌ FAIL'} ({temporal_confidence})")
                
                # Test 4: Temporal Analysis Present
                print(f"4. Temporal Analysis Present: {'✅ PASS' if temporal_found else '❌ FAIL'}")
                
                # Test 5: Multi-symptom Detection
                multi_symptom = "head" in str(data).lower() and "stomach" in str(data).lower()
                print(f"5. Multi-symptom Detection: {'✅ PASS' if multi_symptom else '❌ FAIL'}")
                
                # Overall assessment
                tests_passed = sum([duration_detected, confidence_valid, confidence_threshold, temporal_found, multi_symptom])
                success_rate = (tests_passed / 5) * 100
                
                print(f"\n🎯 OVERALL ASSESSMENT: {tests_passed}/5 tests passed ({success_rate:.1f}%)")
                
                if success_rate >= 80:
                    print("🎉 TEMPORAL EXTRACTION FIXES: SUCCESSFUL")
                elif success_rate >= 60:
                    print("⚠️  TEMPORAL EXTRACTION FIXES: PARTIALLY SUCCESSFUL")
                else:
                    print("❌ TEMPORAL EXTRACTION FIXES: NEEDS IMPROVEMENT")
                    
            else:
                print("❌ API returned success: False")
                print(f"Error: {data.get('error', 'Unknown error')}")
                
        elif response.status_code == 405:
            print("❌ Method Not Allowed - Endpoint might not support POST")
            
        elif response.status_code == 502:
            print("❌ Bad Gateway - Backend service might be down")
            
        else:
            print(f"❌ HTTP Error {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
    except requests.exceptions.Timeout:
        print("❌ Request Timeout (30s)")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - Cannot reach backend")
        
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def test_additional_temporal_patterns():
    """Test additional temporal patterns"""
    print("\n🔍 ADDITIONAL TEMPORAL PATTERNS TESTING")
    print("=" * 60)
    
    test_cases = [
        "for 2 days headache getting worse",
        "past 5 hours stomach pain",
        "last 3 weeks back pain",
        "sudden onset chest pain",
        "gradual pain over time",
        "intermittent symptoms come and go"
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: '{text}'")
        print("-" * 40)
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/medical-ai/multi-symptom-parse",
                json={"text": text, "context": {"patient_id": f"test-pattern-{i}"}},
                timeout=15,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print("✅ Successfully processed")
                    
                    # Check for temporal indicators
                    temporal_found = False
                    if data.get("multi_symptom_parse_result"):
                        result_str = str(data["multi_symptom_parse_result"]).lower()
                        if any(word in result_str for word in ["temporal", "duration", "time", "pattern"]):
                            temporal_found = True
                    
                    print(f"   Temporal indicators: {'✅ Found' if temporal_found else '❌ Not found'}")
                else:
                    print(f"❌ Processing failed: {data.get('error', 'Unknown')}")
            else:
                print(f"❌ HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 TEMPORAL EXTRACTION FIXES TESTING FOR MEDICAL AI")
    print("=" * 80)
    
    # Test the primary case
    test_temporal_extraction()
    
    # Test additional patterns
    test_additional_temporal_patterns()
    
    print("\n" + "=" * 80)
    print("✅ TEMPORAL EXTRACTION TESTING COMPLETED")
    print("=" * 80)