"""
Simple test to verify Phase 5 integration with medical AI
"""

import requests
import json

def test_simple_integration():
    """Test basic medical AI with enhanced templates"""
    
    base_url = "http://localhost:8001"
    
    print("🚀 TESTING SIMPLE ENHANCED TEMPLATE INTEGRATION")
    print("=" * 60)
    
    # Test just the template endpoint quickly
    try:
        print("\n1. Testing Enhanced Response Template API...")
        template_payload = {
            "symptom_description": "chest pain",
            "patient_context": None
        }
        
        response = requests.post(
            f"{base_url}/api/medical-ai/enhanced-response-template",
            json=template_payload,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: Template generated for chest pain")
            print(f"   Category: {data['category']}")
            print(f"   Questions: {len(data['questions'])}")
            print(f"   Sample Question: {data['questions'][0]}")
            print(f"   Red Flags: {len(data['red_flags'])}")
            print(f"   Sample Red Flag: {data['red_flags'][0]}")
            print(f"   Protocol: {data['follow_up_protocol']}")
            
            # Validate the chest_pain template as requested
            expected_structure = {
                "questions": [
                    "Can you describe the chest discomfort? Is it sharp, dull, or pressure-like?",
                    "Does the pain radiate to your arm, jaw, neck, or back?",
                    "When did this start, and what were you doing when it began?"
                ],
                "red_flags": ["crushing", "radiating", "shortness of breath"],
                "follow_up_protocol": "chest_pain_assessment"
            }
            
            print(f"\n✅ CHEST PAIN TEMPLATE VALIDATION:")
            print(f"   Questions match expected: {'YES' if 'chest discomfort' in data['questions'][0] else 'NO'}")
            print(f"   Radiation question present: {'YES' if 'radiate' in str(data['questions']) else 'NO'}")
            print(f"   Red flags appropriate: {'YES' if 'crushing' in str(data['red_flags']) else 'NO'}")
            print(f"   Protocol correct: {'YES' if 'chest_pain' in data['follow_up_protocol'] else 'NO'}")
            
        else:
            print(f"❌ FAILED: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test symptom categorization
    try:
        print(f"\n2. Testing Symptom Categorization...")
        category_payload = {"symptom_description": "headache"}
        
        response = requests.post(
            f"{base_url}/api/medical-ai/symptom-category-analysis", 
            json=category_payload,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: Headache categorized as {data['category']}")
            print(f"   Confidence: {data['confidence']}")
            print(f"   Related symptoms: {data['related_symptoms'][:3]}")
        else:
            print(f"❌ FAILED: {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        
    print("\n" + "=" * 60)
    print("🎯 PHASE 5 SIMPLE INTEGRATION TEST COMPLETE")

if __name__ == "__main__":
    test_simple_integration()