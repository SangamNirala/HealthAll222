#!/usr/bin/env python3
"""
Detailed test for Step 1.3 Colloquial Medical Expression Handler
"""

import requests
import json
from datetime import datetime

BACKEND_URL = "https://medical-intents.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

def test_colloquial_expression_detailed(expression: str, expected_terms: list):
    """Test a colloquial expression with detailed analysis"""
    print(f"\n🧪 Testing: '{expression}'")
    print(f"   Expected terms: {expected_terms}")
    
    try:
        # Initialize consultation
        init_response = requests.post(
            f"{API_BASE}/medical-ai/initialize",
            json={
                "patient_id": "detailed-test",
                "timestamp": datetime.now().isoformat()
            },
            timeout=30
        )
        
        if init_response.status_code != 200:
            print(f"   ❌ Init failed: {init_response.text}")
            return False, {}
        
        init_data = init_response.json()
        consultation_id = init_data.get('consultation_id')
        
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
        
        if message_response.status_code != 200:
            print(f"   ❌ Message failed: {message_response.text}")
            return False, {}
        
        message_data = message_response.json()
        
        # Analyze response
        response_text = message_data.get('response', '')
        context = message_data.get('context', {})
        chief_complaint = context.get('chief_complaint', '')
        
        print(f"   Response: {response_text[:150]}...")
        print(f"   Chief complaint: {chief_complaint}")
        
        # Check for expected terms
        combined_text = (response_text + " " + str(context) + " " + chief_complaint).lower()
        
        found_terms = []
        for term in expected_terms:
            if term.lower() in combined_text:
                found_terms.append(term)
        
        success = len(found_terms) > 0
        
        print(f"   Found terms: {found_terms}")
        print(f"   Success: {success}")
        
        return success, {
            'response': response_text,
            'context': context,
            'found_terms': found_terms,
            'consultation_id': consultation_id
        }
        
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False, {'error': str(e)}

def main():
    """Run detailed tests"""
    print("🔍 DETAILED TESTING - Step 1.3 Colloquial Medical Expression Handler")
    print("="*80)
    
    # Test cases with multiple possible terms
    test_cases = [
        # Core examples
        ("tummy hurt", ["abdominal pain", "stomach pain", "belly pain"]),
        ("feeling crappy", ["feeling unwell", "feel unwell", "not feeling well"]),
        ("can't poop", ["experiencing constipation", "constipation", "bowel movement"]),
        ("throwing up", ["vomiting", "nausea", "sick"]),
        ("dizzy spells", ["episodes of dizziness", "dizziness", "dizzy"]),
        
        # Additional tests
        ("belly ache", ["abdominal pain", "stomach pain", "belly pain"]),
        ("wiped out", ["extremely fatigued", "fatigue", "tired", "exhausted"]),
        ("can't breathe", ["difficulty breathing", "breathing", "shortness of breath"]),
        
        # Compound expressions
        ("tummy hurt and throwing up", ["abdominal pain", "vomiting", "nausea"]),
    ]
    
    results = []
    
    for expression, expected_terms in test_cases:
        success, details = test_colloquial_expression_detailed(expression, expected_terms)
        results.append((expression, expected_terms, success, details))
    
    # Summary
    print("\n" + "="*80)
    print("📊 DETAILED TEST RESULTS")
    print("="*80)
    
    passed = sum(1 for _, _, success, _ in results if success)
    total = len(results)
    
    for expression, expected_terms, success, details in results:
        status = "✅ PASS" if success else "❌ FAIL"
        found = details.get('found_terms', [])
        print(f"{status} - '{expression}' → Found: {found}")
    
    print(f"\nOverall: {passed}/{total} ({passed/total*100:.1f}%)")
    
    # Analysis
    print("\n🔍 ANALYSIS:")
    working_expressions = [expr for expr, _, success, _ in results if success]
    failing_expressions = [expr for expr, _, success, _ in results if not success]
    
    print(f"✅ Working expressions: {working_expressions}")
    print(f"❌ Failing expressions: {failing_expressions}")

if __name__ == "__main__":
    main()