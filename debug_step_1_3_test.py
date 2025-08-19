#!/usr/bin/env python3
"""
Debug test for Step 1.3 Colloquial Medical Expression Handler
"""

import requests
import json
from datetime import datetime

BACKEND_URL = "https://symptom-tracker-fix.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

def test_single_colloquial_expression(expression: str, expected: str):
    """Test a single colloquial expression"""
    print(f"\n🧪 Testing: '{expression}' → should contain '{expected}'")
    
    try:
        # Initialize consultation
        init_response = requests.post(
            f"{API_BASE}/medical-ai/initialize",
            json={
                "patient_id": "debug-test",
                "timestamp": datetime.now().isoformat()
            },
            timeout=30
        )
        
        print(f"   Init Status: {init_response.status_code}")
        
        if init_response.status_code != 200:
            print(f"   ❌ Init failed: {init_response.text}")
            return False
        
        init_data = init_response.json()
        consultation_id = init_data.get('consultation_id')
        print(f"   Consultation ID: {consultation_id}")
        
        # Send colloquial message
        message_response = requests.post(
            f"{API_BASE}/medical-ai/message",
            json={
                "consultation_id": consultation_id,
                "message": expression,
                "timestamp": datetime.now().isoformat()
            },
            timeout=30
        )
        
        print(f"   Message Status: {message_response.status_code}")
        
        if message_response.status_code != 200:
            print(f"   ❌ Message failed: {message_response.text}")
            return False
        
        message_data = message_response.json()
        
        # Check response
        response_text = message_data.get('response', '')
        context = str(message_data.get('context', {}))
        
        print(f"   Response length: {len(response_text)}")
        print(f"   Response preview: {response_text[:200]}...")
        
        # Look for expected conversion
        combined_text = (response_text + " " + context).lower()
        conversion_found = expected.lower() in combined_text
        
        print(f"   Expected '{expected}' found: {conversion_found}")
        
        if conversion_found:
            print(f"   ✅ SUCCESS: Colloquial expression converted correctly")
        else:
            print(f"   ❌ FAILED: Expected conversion not found")
            print(f"   Full response: {response_text}")
        
        return conversion_found
        
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def main():
    """Run debug tests"""
    print("🔍 DEBUG TESTING - Step 1.3 Colloquial Medical Expression Handler")
    print("="*80)
    
    # Test the 5 core examples
    core_examples = [
        ("tummy hurt", "abdominal pain"),
        ("feeling crappy", "feeling unwell"),
        ("can't poop", "experiencing constipation"),
        ("throwing up", "vomiting"),
        ("dizzy spells", "episodes of dizziness")
    ]
    
    results = []
    
    for expression, expected in core_examples:
        result = test_single_colloquial_expression(expression, expected)
        results.append((expression, expected, result))
    
    # Summary
    print("\n" + "="*80)
    print("📊 DEBUG TEST RESULTS")
    print("="*80)
    
    passed = sum(1 for _, _, result in results if result)
    total = len(results)
    
    for expression, expected, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - '{expression}' → '{expected}'")
    
    print(f"\nOverall: {passed}/{total} ({passed/total*100:.1f}%)")

if __name__ == "__main__":
    main()