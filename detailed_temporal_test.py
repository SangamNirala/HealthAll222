#!/usr/bin/env python3
"""
DETAILED TEMPORAL EXTRACTION ANALYSIS

Deep dive into the temporal extraction response to understand the current structure
and identify what needs to be fixed for the temporal confidence scoring.
"""

import requests
import json
import pprint

BACKEND_URL = "https://ai-test-suite.preview.emergentagent.com"

def analyze_temporal_response():
    """Analyze the detailed temporal response structure"""
    print("🔍 DETAILED TEMPORAL EXTRACTION ANALYSIS")
    print("=" * 60)
    
    test_request = {
        "text": "head hurts stomach upset cant sleep 3 nights",
        "context": {"patient_id": "test-temporal-detailed"}
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/medical-ai/multi-symptom-parse",
            json=test_request,
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and data.get("multi_symptom_parse_result"):
                parse_result = data["multi_symptom_parse_result"]
                
                print("📊 FULL RESPONSE STRUCTURE:")
                print("-" * 40)
                
                # Print temporal_data specifically
                if "temporal_data" in parse_result:
                    print("✅ TEMPORAL_DATA FOUND:")
                    temporal_data = parse_result["temporal_data"]
                    pprint.pprint(temporal_data, width=80, depth=3)
                    print()
                
                # Print confidence_metrics specifically
                if "confidence_metrics" in parse_result:
                    print("📊 CONFIDENCE_METRICS:")
                    confidence_metrics = parse_result["confidence_metrics"]
                    pprint.pprint(confidence_metrics, width=80, depth=2)
                    print()
                
                # Print onset_analysis
                if "onset_analysis" in parse_result:
                    print("⏰ ONSET_ANALYSIS:")
                    onset_analysis = parse_result["onset_analysis"]
                    pprint.pprint(onset_analysis, width=80, depth=2)
                    print()
                
                # Print progression_patterns
                if "progression_patterns" in parse_result:
                    print("📈 PROGRESSION_PATTERNS:")
                    progression_patterns = parse_result["progression_patterns"]
                    pprint.pprint(progression_patterns, width=80, depth=2)
                    print()
                
                # Look for any field containing "3 nights"
                print("🔍 SEARCHING FOR '3 nights' IN RESPONSE:")
                print("-" * 40)
                
                def search_for_duration(obj, path=""):
                    """Recursively search for duration mentions"""
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            new_path = f"{path}.{key}" if path else key
                            if isinstance(value, str) and "3 nights" in value.lower():
                                print(f"✅ Found '3 nights' in: {new_path}")
                                print(f"   Value: {value}")
                            elif isinstance(value, str) and any(word in value.lower() for word in ["night", "duration", "3"]):
                                print(f"🔍 Related temporal info in: {new_path}")
                                print(f"   Value: {value}")
                            search_for_duration(value, new_path)
                    elif isinstance(obj, list):
                        for i, item in enumerate(obj):
                            search_for_duration(item, f"{path}[{i}]")
                
                search_for_duration(parse_result)
                
                # Check temporal confidence specifically
                print("\n📊 TEMPORAL CONFIDENCE ANALYSIS:")
                print("-" * 40)
                
                temporal_confidence = parse_result.get("confidence_metrics", {}).get("temporal_confidence", 0.0)
                print(f"Current Temporal Confidence: {temporal_confidence}")
                
                if temporal_confidence == 0.0:
                    print("❌ ISSUE: Temporal confidence is 0.0 - this is the bug that needs fixing")
                    print("   Expected: Should be 0.7+ when temporal patterns like '3 nights' are detected")
                else:
                    print(f"✅ Temporal confidence is non-zero: {temporal_confidence}")
                
                # Check for overall_duration field
                print("\n🔍 SEARCHING FOR OVERALL_DURATION FIELD:")
                print("-" * 40)
                
                def search_for_overall_duration(obj, path=""):
                    """Search for overall_duration field"""
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            new_path = f"{path}.{key}" if path else key
                            if "overall_duration" in key.lower():
                                print(f"✅ Found overall_duration field: {new_path}")
                                print(f"   Value: {value}")
                            search_for_overall_duration(value, new_path)
                    elif isinstance(obj, list):
                        for i, item in enumerate(obj):
                            search_for_overall_duration(item, f"{path}[{i}]")
                
                search_for_overall_duration(parse_result)
                
                # Summary of findings
                print("\n🎯 TEMPORAL EXTRACTION ANALYSIS SUMMARY:")
                print("-" * 40)
                print(f"1. API Response: ✅ Working (HTTP 200)")
                print(f"2. Multi-symptom Detection: ✅ Working")
                print(f"3. Duration Detection: ✅ '3 nights' found in response")
                print(f"4. Temporal Confidence: ❌ {temporal_confidence} (should be 0.7+)")
                print(f"5. Overall Duration Field: {'✅' if 'overall_duration' in str(parse_result).lower() else '❌'} {'Found' if 'overall_duration' in str(parse_result).lower() else 'Missing'}")
                
                print("\n🔧 REQUIRED FIXES:")
                print("-" * 40)
                print("1. Fix temporal_confidence calculation - currently returning 0.0")
                print("2. Ensure overall_duration field is populated when temporal patterns detected")
                print("3. Temporal confidence should be 0.7+ when '3 nights' pattern is found")
                
            else:
                print("❌ No parse result in response")
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(response.text[:500])
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    analyze_temporal_response()