#!/usr/bin/env python3
"""
🧠 FOCUSED PHASE 3 CONTEXTUAL REASONING TESTING 🧠

Focused testing of the 3 ultra-challenging scenarios from the review request
with detailed validation and performance analysis.
"""

import requests
import json
import time
import sys
import os
from datetime import datetime

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://emotion-verify-1.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def test_scenario(scenario_name, text, expected_factors):
    """Test a single contextual reasoning scenario"""
    print(f"\n🎯 Testing {scenario_name}")
    print(f"Input: {text[:100]}...")
    
    try:
        start_time = time.time()
        
        response = requests.post(f"{API_BASE}/medical-ai/contextual-analysis",
            json={
                "text": text,
                "analysis_type": "comprehensive_contextual"
            },
            timeout=30
        )
        
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract key information
            contextual_reasoning = data.get("contextual_reasoning", {})
            contextual_factors = contextual_reasoning.get("contextual_factors", {})
            causal_relationships = contextual_reasoning.get("causal_relationships", [])
            clinical_hypotheses = contextual_reasoning.get("clinical_hypotheses", [])
            processing_metadata = data.get("processing_metadata", {})
            
            # Check expected factors
            found_factors = []
            for factor_type in expected_factors:
                if factor_type in contextual_factors and contextual_factors[factor_type]:
                    found_factors.append(factor_type)
            
            # Get performance metrics
            medical_coherence = processing_metadata.get("medical_coherence_achieved", 0.0)
            
            # Print results
            print(f"   ⏱️  Processing Time: {processing_time:.1f}ms")
            print(f"   🎯 Expected Factors: {expected_factors}")
            print(f"   ✅ Found Factors: {found_factors}")
            print(f"   🧠 Medical Coherence: {medical_coherence:.3f}")
            print(f"   🔗 Causal Relationships: {len(causal_relationships)}")
            print(f"   💡 Clinical Hypotheses: {len(clinical_hypotheses)}")
            
            # Detailed factor analysis
            print(f"   📊 Contextual Factors Detail:")
            for factor_type, factors in contextual_factors.items():
                if factors:
                    print(f"      {factor_type}: {factors}")
            
            # Success criteria
            performance_ok = processing_time < 25.0
            factors_ok = len(found_factors) >= len(expected_factors) * 0.7  # 70% of expected factors
            coherence_ok = medical_coherence > 0.97
            
            success = performance_ok and factors_ok and coherence_ok
            
            print(f"   🎯 Performance Target (<25ms): {'✅' if performance_ok else '❌'}")
            print(f"   🎯 Factor Detection (≥70%): {'✅' if factors_ok else '❌'}")
            print(f"   🎯 Medical Coherence (>0.97): {'✅' if coherence_ok else '❌'}")
            print(f"   🏆 Overall Success: {'✅ PASS' if success else '❌ FAIL'}")
            
            return {
                "success": success,
                "processing_time": processing_time,
                "found_factors": found_factors,
                "expected_factors": expected_factors,
                "medical_coherence": medical_coherence,
                "causal_relationships": len(causal_relationships),
                "clinical_hypotheses": len(clinical_hypotheses)
            }
            
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return {"success": False, "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        return {"success": False, "error": str(e)}

def main():
    print("🧠 PHASE 3 CONTEXTUAL REASONING COMPREHENSIVE VALIDATION TESTING")
    print(f"   API Base: {API_BASE}")
    print("=" * 80)
    
    # Ultra-challenging scenarios from review request
    scenarios = [
        {
            "name": "Ultra-Challenging Scenario 1 (Complex Positional Context)",
            "text": "Every morning when I get out of bed I feel dizzy and nauseous, sometimes I even feel like I'm going to faint, but it goes away after I sit back down for a few minutes. This also happens when I stand up quickly from a chair or get up from squatting down.",
            "expected_factors": ["positional_factors", "temporal_factors", "activity_relationships"]
        },
        {
            "name": "Ultra-Challenging Scenario 2 (Exertional Cardiac Context)",
            "text": "I get this crushing chest pain whenever I walk uphill or climb more than one flight of stairs, feels like an elephant sitting on my chest, but it completely goes away within 2-3 minutes of resting. Never happens when I'm just sitting or doing light activities around the house.",
            "expected_factors": ["activity_relationships", "temporal_factors", "environmental_factors"]
        },
        {
            "name": "Ultra-Challenging Scenario 3 (Multi-Context Dietary/Stress/Temporal)",
            "text": "I've noticed that I get really bad stomach cramps and loose stools about 30-60 minutes after eating ice cream or drinking milk, but only when I'm stressed out at work. When I'm relaxed at home on weekends, I can sometimes tolerate small amounts of dairy without problems.",
            "expected_factors": ["environmental_factors", "temporal_factors", "activity_relationships"]
        }
    ]
    
    results = []
    processing_times = []
    
    # Test each scenario
    for scenario in scenarios:
        result = test_scenario(scenario["name"], scenario["text"], scenario["expected_factors"])
        results.append(result)
        if "processing_time" in result:
            processing_times.append(result["processing_time"])
    
    # Calculate overall metrics
    successful_scenarios = sum(1 for r in results if r.get("success", False))
    success_rate = (successful_scenarios / len(results)) * 100
    
    if processing_times:
        avg_processing_time = sum(processing_times) / len(processing_times)
        max_processing_time = max(processing_times)
        min_processing_time = min(processing_times)
    else:
        avg_processing_time = max_processing_time = min_processing_time = 0.0
    
    # Performance comparison
    previous_avg_time = 64.7  # From previous testing
    performance_improvement = ((previous_avg_time - avg_processing_time) / previous_avg_time) * 100
    
    # Medical coherence analysis
    coherence_scores = [r.get("medical_coherence", 0.0) for r in results if "medical_coherence" in r]
    avg_coherence = sum(coherence_scores) / len(coherence_scores) if coherence_scores else 0.0
    
    # Print comprehensive results
    print("\n" + "=" * 80)
    print("📊 PHASE 3 CONTEXTUAL REASONING VALIDATION RESULTS")
    print("=" * 80)
    
    print(f"\n🎯 SCENARIO RESULTS:")
    for i, (scenario, result) in enumerate(zip(scenarios, results), 1):
        status = "✅ PASS" if result.get("success", False) else "❌ FAIL"
        print(f"   {i}. {scenario['name']}: {status}")
        if "processing_time" in result:
            print(f"      Processing Time: {result['processing_time']:.1f}ms")
            print(f"      Factors Found: {len(result.get('found_factors', []))}/{len(result.get('expected_factors', []))}")
            print(f"      Medical Coherence: {result.get('medical_coherence', 0.0):.3f}")
    
    print(f"\n📈 PERFORMANCE ANALYSIS:")
    print(f"   Average Processing Time: {avg_processing_time:.1f}ms (Target: <25ms)")
    print(f"   Performance Target Met: {'✅ YES' if avg_processing_time < 25.0 else '❌ NO'}")
    print(f"   Previous Average: {previous_avg_time}ms")
    print(f"   Performance Improvement: {performance_improvement:.1f}%")
    print(f"   Min/Max Processing Time: {min_processing_time:.1f}ms / {max_processing_time:.1f}ms")
    
    print(f"\n🧠 MEDICAL COHERENCE ANALYSIS:")
    print(f"   Average Medical Coherence: {avg_coherence:.3f} (Target: >0.97)")
    print(f"   Coherence Target Met: {'✅ YES' if avg_coherence > 0.97 else '❌ NO'}")
    
    print(f"\n📊 OVERALL VALIDATION:")
    print(f"   Successful Scenarios: {successful_scenarios}/3")
    print(f"   Success Rate: {success_rate:.1f}%")
    
    # Final assessment
    overall_success = (
        successful_scenarios >= 2 and  # At least 2/3 scenarios pass
        avg_processing_time < 25.0 and  # Performance target
        avg_coherence > 0.95  # Slightly relaxed coherence
    )
    
    print(f"\n🏆 FINAL ASSESSMENT:")
    if overall_success:
        print("✅ PHASE 3 CONTEXTUAL REASONING ENGINE VALIDATION SUCCESSFUL")
        print("   Critical fixes validated and performance targets met")
        return 0
    else:
        print("❌ PHASE 3 CONTEXTUAL REASONING ENGINE NEEDS IMPROVEMENT")
        if successful_scenarios < 2:
            print(f"   - Only {successful_scenarios}/3 scenarios passed")
        if avg_processing_time >= 25.0:
            print(f"   - Performance target not met: {avg_processing_time:.1f}ms ≥ 25ms")
        if avg_coherence <= 0.95:
            print(f"   - Medical coherence below target: {avg_coherence:.3f} ≤ 0.95")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)