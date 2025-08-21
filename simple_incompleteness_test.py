#!/usr/bin/env python3
"""
🧠 ENHANCED INCOMPLETENESS DETECTION SYSTEM - FUNCTIONALITY TEST
Testing core functionality of the Enhanced Incompleteness Detection System
"""

import requests
import json
import time

# Backend URL
BACKEND_URL = "https://medchattest.preview.emergentagent.com/api"

def test_incompleteness_detection():
    """Test the core incompleteness detection functionality"""
    print("🧠 ENHANCED INCOMPLETENESS DETECTION SYSTEM - FUNCTIONALITY TEST")
    print("=" * 70)
    
    # Test scenarios from the review request
    test_scenarios = [
        {
            "name": "Reserved Patient - Linguistic Incompleteness",
            "data": {
                "patient_message": "I hurt",
                "conversation_context": {"messages": [], "topic": "medical_consultation"},
                "medical_context": {"chief_complaint": "", "current_symptoms": {}},
                "analysis_depth": "comprehensive"
            }
        },
        {
            "name": "Anxious Patient - Medical Reasoning",
            "data": {
                "patient_message": "I'm so worried about this chest pain, what if it's my heart?",
                "conversation_context": {"messages": [{"role": "patient", "content": "chest pain"}]},
                "medical_context": {"chief_complaint": "chest pain", "current_symptoms": {"chest_pain": True}},
                "analysis_depth": "comprehensive"
            }
        },
        {
            "name": "Detailed Patient - Complete Information",
            "data": {
                "patient_message": "I've been having a sharp, stabbing chest pain that started suddenly 2 hours ago on the left side, worse when I breathe deeply, with no radiation to arms, no shortness of breath, rate it 7/10, nothing makes it better, aspirin didn't help",
                "conversation_context": {"messages": []},
                "medical_context": {"chief_complaint": "chest pain"},
                "analysis_depth": "comprehensive"
            }
        },
        {
            "name": "Psychological Incompleteness",
            "data": {
                "patient_message": "Everything is fine, just some stomach issues, nothing serious",
                "conversation_context": {"messages": [{"role": "patient", "content": "I'm embarrassed"}, {"role": "doctor", "content": "What's bothering you?"}]},
                "medical_context": {"chief_complaint": "stomach issues"},
                "analysis_depth": "comprehensive"
            }
        }
    ]
    
    results = []
    
    for scenario in test_scenarios:
        print(f"\n🔍 Testing: {scenario['name']}")
        print("-" * 50)
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{BACKEND_URL}/medical-ai/incompleteness-detection/analyze",
                json=scenario['data'],
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            processing_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                # Check key functionality
                success = data.get("success", False)
                incompleteness_score = data.get("incompleteness_score", 0)
                priority_gaps = data.get("priority_gaps", [])
                follow_ups = data.get("immediate_follow_ups", [])
                profile = data.get("patient_communication_profile", {})
                strategy = data.get("adaptive_strategy", {})
                confidence = data.get("analysis_confidence", 0)
                
                print(f"✅ SUCCESS: {scenario['name']}")
                print(f"   Processing Time: {processing_time:.1f}ms")
                print(f"   Incompleteness Score: {incompleteness_score:.2f}")
                print(f"   Analysis Confidence: {confidence:.2f}")
                print(f"   Priority Gaps Detected: {len(priority_gaps)}")
                print(f"   Follow-up Questions: {len(follow_ups)}")
                
                if priority_gaps:
                    print(f"   Gap Types: {[gap.get('gap_type') for gap in priority_gaps[:3]]}")
                
                if follow_ups:
                    print(f"   Sample Follow-up: {follow_ups[0][:100]}...")
                
                # Check for 5 dimensions of incompleteness detection
                gap_types = [gap.get("gap_type", "") for gap in priority_gaps]
                detected_dimensions = []
                if any("linguistic" in gt for gt in gap_types):
                    detected_dimensions.append("linguistic")
                if any("medical" in gt for gt in gap_types):
                    detected_dimensions.append("medical_reasoning")
                if any("psychological" in gt for gt in gap_types):
                    detected_dimensions.append("psychological")
                if any("cultural" in gt for gt in gap_types):
                    detected_dimensions.append("cultural")
                if any("temporal" in gt for gt in gap_types):
                    detected_dimensions.append("temporal")
                
                print(f"   Detected Dimensions: {detected_dimensions}")
                
                results.append({
                    "scenario": scenario['name'],
                    "success": True,
                    "processing_time": processing_time,
                    "incompleteness_score": incompleteness_score,
                    "confidence": confidence,
                    "gaps": len(priority_gaps),
                    "follow_ups": len(follow_ups),
                    "dimensions": detected_dimensions
                })
                
            else:
                print(f"❌ FAILED: {scenario['name']} - HTTP {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                results.append({
                    "scenario": scenario['name'],
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                })
                
        except Exception as e:
            print(f"❌ ERROR: {scenario['name']} - {str(e)}")
            results.append({
                "scenario": scenario['name'],
                "success": False,
                "error": str(e)
            })
    
    # Test System Performance Endpoint
    print(f"\n🔍 Testing: System Performance Endpoint")
    print("-" * 50)
    
    try:
        response = requests.get(
            f"{BACKEND_URL}/medical-ai/incompleteness-detection/system-performance",
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS: System Performance API")
            print(f"   Algorithm Version: {data.get('algorithm_version', 'N/A')}")
            print(f"   Integration Status: {data.get('integration_status', 'N/A')}")
            print(f"   System Capabilities: {len(data.get('system_capabilities', {}))}")
            results.append({"scenario": "System Performance API", "success": True})
        else:
            print(f"❌ FAILED: System Performance API - HTTP {response.status_code}")
            results.append({"scenario": "System Performance API", "success": False})
            
    except Exception as e:
        print(f"❌ ERROR: System Performance API - {str(e)}")
        results.append({"scenario": "System Performance API", "success": False})
    
    # Summary
    print("\n" + "=" * 70)
    print("🎯 ENHANCED INCOMPLETENESS DETECTION SYSTEM - TEST SUMMARY")
    print("=" * 70)
    
    successful_tests = sum(1 for r in results if r.get("success", False))
    total_tests = len(results)
    success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    # Analyze functionality
    functional_tests = [r for r in results if r.get("success") and "processing_time" in r]
    if functional_tests:
        avg_time = sum(r["processing_time"] for r in functional_tests) / len(functional_tests)
        avg_confidence = sum(r["confidence"] for r in functional_tests) / len(functional_tests)
        total_gaps = sum(r["gaps"] for r in functional_tests)
        total_follow_ups = sum(r["follow_ups"] for r in functional_tests)
        
        print(f"\nFunctionality Analysis:")
        print(f"  Average Processing Time: {avg_time:.1f}ms")
        print(f"  Average Confidence: {avg_confidence:.2f}")
        print(f"  Total Gaps Detected: {total_gaps}")
        print(f"  Total Follow-ups Generated: {total_follow_ups}")
        
        # Check if all 5 dimensions are being detected
        all_dimensions = set()
        for r in functional_tests:
            all_dimensions.update(r.get("dimensions", []))
        
        print(f"  Incompleteness Dimensions Detected: {list(all_dimensions)}")
        
        expected_dimensions = ["linguistic", "medical_reasoning", "psychological", "cultural", "temporal"]
        detected_expected = len(all_dimensions.intersection(expected_dimensions))
        print(f"  Expected Dimensions Found: {detected_expected}/5")
    
    if success_rate >= 80:
        print("\n🎉 EXCELLENT: Enhanced Incompleteness Detection System is functional!")
        if functional_tests and avg_confidence > 0.6:
            print("✅ Analysis confidence meets requirements (>0.6)")
        if functional_tests and total_gaps > 0:
            print("✅ Incompleteness gaps are being detected")
        if functional_tests and total_follow_ups > 0:
            print("✅ Follow-up questions are being generated")
    elif success_rate >= 60:
        print("\n✅ GOOD: System is mostly functional with some issues")
    else:
        print("\n❌ CRITICAL: System has significant functionality issues")
    
    return success_rate >= 60

if __name__ == "__main__":
    success = test_incompleteness_detection()
    if success:
        print("\n🎉 ENHANCED INCOMPLETENESS DETECTION SYSTEM: FUNCTIONALITY TEST PASSED")
    else:
        print("\n❌ ENHANCED INCOMPLETENESS DETECTION SYSTEM: FUNCTIONALITY TEST FAILED")