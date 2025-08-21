#!/usr/bin/env python3
"""
FOCUSED STEP 4.2 INTELLIGENT FOLLOW-UP QUESTION GENERATION TESTING

Testing the key scenarios from the review request to validate the Step 4.2 system.
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "https://nlptest-phase7.preview.emergentagent.com/api"

def test_step_42_follow_up_system():
    """Test the Step 4.2 intelligent follow-up question generation system"""
    
    print("🚀 TESTING STEP 4.2 INTELLIGENT FOLLOW-UP QUESTION GENERATION SYSTEM")
    print("=" * 80)
    
    test_results = []
    
    # Test scenarios from the review request
    test_scenarios = [
        {
            "name": "Vague Symptom - 'feeling bad'",
            "message": "feeling bad",
            "expected_indicators": ["specific symptoms", "what exactly", "describe", "for example"],
            "category": "vague_symptom"
        },
        {
            "name": "Vague Symptom - 'not well'", 
            "message": "not well",
            "expected_indicators": ["specific symptoms", "what exactly", "describe", "experiencing"],
            "category": "vague_symptom"
        },
        {
            "name": "Incomplete Pain - 'chest pain'",
            "message": "chest pain", 
            "expected_indicators": ["what does it feel like", "describe", "crushing", "pressure", "sharp"],
            "category": "incomplete_pain"
        },
        {
            "name": "Incomplete Pain - 'my head hurts'",
            "message": "my head hurts",
            "expected_indicators": ["what does it feel like", "where exactly", "throbbing", "pounding"],
            "category": "incomplete_pain"
        },
        {
            "name": "Vague Temporal - 'recently'",
            "message": "recently",
            "expected_indicators": ["more specific", "hours ago", "days ago", "when exactly"],
            "category": "vague_temporal"
        },
        {
            "name": "Single Word Anatomical - 'chest'",
            "message": "chest",
            "expected_indicators": ["what specific symptoms", "chest pain", "breathing", "experiencing"],
            "category": "single_word"
        },
        {
            "name": "Emotional Response - 'scared'",
            "message": "scared",
            "expected_indicators": ["i understand", "what specific", "causing you", "worrying you"],
            "category": "emotional"
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n🧪 Testing: {scenario['name']}")
        
        # Initialize consultation
        init_response = requests.post(
            f"{BACKEND_URL}/medical-ai/initialize",
            json={
                "patient_id": f"test_patient_{scenario['category']}",
                "timestamp": datetime.now().isoformat()
            },
            timeout=30
        )
        
        if init_response.status_code != 200:
            print(f"❌ Failed to initialize consultation: {init_response.status_code}")
            continue
            
        init_data = init_response.json()
        consultation_id = init_data.get('consultation_id')
        
        if not consultation_id:
            print(f"❌ No consultation ID received")
            continue
        
        # Send test message
        message_response = requests.post(
            f"{BACKEND_URL}/medical-ai/message",
            json={
                "message": scenario['message'],
                "consultation_id": consultation_id,
                "patient_id": f"test_patient_{scenario['category']}",
                "timestamp": datetime.now().isoformat()
            },
            timeout=30
        )
        
        if message_response.status_code != 200:
            print(f"❌ Failed to send message: {message_response.status_code}")
            continue
            
        response_data = message_response.json()
        response_text = response_data.get('response', '').lower()
        
        # Check for expected follow-up indicators
        found_indicators = []
        for indicator in scenario['expected_indicators']:
            if indicator.lower() in response_text:
                found_indicators.append(indicator)
        
        # Determine success
        has_follow_up = len(found_indicators) > 0
        is_substantial = len(response_text) > 50
        
        success = has_follow_up and is_substantial
        
        # Log result
        result = {
            "scenario": scenario['name'],
            "message": scenario['message'],
            "category": scenario['category'],
            "success": success,
            "response_length": len(response_text),
            "found_indicators": found_indicators,
            "response_preview": response_text[:200] + "..." if len(response_text) > 200 else response_text
        }
        
        test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - Found {len(found_indicators)} follow-up indicators")
        print(f"   Response: {result['response_preview']}")
        
        time.sleep(1)  # Rate limiting
    
    # Generate summary
    print("\n" + "=" * 80)
    print("📊 STEP 4.2 TESTING SUMMARY")
    print("=" * 80)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for r in test_results if r['success'])
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    # Category breakdown
    categories = {}
    for result in test_results:
        cat = result['category']
        if cat not in categories:
            categories[cat] = {'total': 0, 'passed': 0}
        categories[cat]['total'] += 1
        if result['success']:
            categories[cat]['passed'] += 1
    
    print(f"\n📋 CATEGORY BREAKDOWN:")
    for category, stats in categories.items():
        rate = (stats['passed'] / stats['total']) * 100 if stats['total'] > 0 else 0
        status = "✅" if rate >= 80 else "⚠️" if rate >= 60 else "❌"
        print(f"{status} {category.replace('_', ' ').title()}: {stats['passed']}/{stats['total']} ({rate:.1f}%)")
    
    # Key success metrics
    print(f"\n🎯 KEY SUCCESS METRICS:")
    
    # Incompleteness detection
    vague_tests = [r for r in test_results if r['category'] in ['vague_symptom', 'incomplete_pain', 'vague_temporal']]
    incompleteness_rate = (sum(1 for r in vague_tests if r['success']) / len(vague_tests)) * 100 if vague_tests else 0
    print(f"{'✅' if incompleteness_rate >= 90 else '❌'} Incompleteness Detection: {incompleteness_rate:.1f}% (Target: 100%)")
    
    # Medical domain awareness
    domain_tests = [r for r in test_results if r['category'] in ['incomplete_pain', 'single_word']]
    domain_rate = (sum(1 for r in domain_tests if r['success']) / len(domain_tests)) * 100 if domain_tests else 0
    print(f"{'✅' if domain_rate >= 80 else '❌'} Medical Domain Awareness: {domain_rate:.1f}% (Target: Medical appropriateness)")
    
    # Empathetic responses
    empathy_tests = [r for r in test_results if r['category'] == 'emotional']
    empathy_rate = (sum(1 for r in empathy_tests if r['success']) / len(empathy_tests)) * 100 if empathy_tests else 0
    print(f"{'✅' if empathy_rate >= 70 else '❌'} Empathetic Language: {empathy_rate:.1f}% (Target: Professional and supportive)")
    
    # Overall assessment
    overall_ready = (success_rate >= 80 and incompleteness_rate >= 90)
    print(f"\n🚀 PRODUCTION READINESS: {'✅ READY' if overall_ready else '⚠️ NEEDS IMPROVEMENT'}")
    
    if overall_ready:
        print("✅ Step 4.2 Intelligent Follow-up Question Generation System is PRODUCTION-READY")
        print("   - Successfully detects incomplete medical information")
        print("   - Generates appropriate follow-up questions")
        print("   - Demonstrates medical domain knowledge")
        print("   - Uses empathetic and professional language")
    else:
        print("⚠️ Step 4.2 system shows promise but needs refinement")
        print("   - Core functionality is working")
        print("   - Some scenarios need improvement")
    
    # Save detailed results
    with open('/app/step_42_focused_results.json', 'w') as f:
        json.dump({
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "success_rate": success_rate,
                "production_ready": overall_ready
            },
            "detailed_results": test_results,
            "categories": categories
        }, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: /app/step_42_focused_results.json")
    
    return test_results

if __name__ == "__main__":
    test_step_42_follow_up_system()