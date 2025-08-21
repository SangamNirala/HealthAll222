"""
🚀 PHASE 5: ENHANCED MEDICAL RESPONSE GENERATION TESTING
Test the new symptom-specific response template system
"""

import asyncio
import json
import requests
from enhanced_medical_response_generator import get_enhanced_medical_response_template

def test_enhanced_template_generator_direct():
    """Test the enhanced template generator directly"""
    print("🚀 TESTING ENHANCED MEDICAL RESPONSE TEMPLATE GENERATOR (DIRECT)")
    print("=" * 70)
    
    test_symptoms = [
        "chest pain",
        "severe headache",
        "shortness of breath", 
        "abdominal pain",
        "crushing chest pain with sweating",
        "sudden severe headache with neck stiffness",
        "difficulty breathing after exercise",
        "sharp stabbing chest pain",
        "migraine with visual changes",
        "joint pain and swelling"
    ]
    
    for i, symptom in enumerate(test_symptoms, 1):
        print(f"\n{i}. SYMPTOM: '{symptom}'")
        print("-" * 50)
        
        try:
            template = get_enhanced_medical_response_template(symptom)
            
            print(f"✅ Category: {template['category']}")
            print(f"✅ Identified as: {template['symptom_name']}")
            print(f"✅ Questions ({len(template['questions'])}): {template['questions'][:2]}...")
            print(f"✅ Red Flags ({len(template['red_flags'])}): {template['red_flags'][:2]}...")
            print(f"✅ Protocol: {template['follow_up_protocol']}")
            print(f"✅ Urgency Indicators: {len(template['urgency_indicators'])} levels")
            print(f"✅ Assessment Timeline: {template['assessment_timeline']}")
            print(f"✅ Confidence: {template['confidence_score']}")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            
    print("\n" + "=" * 70)
    print("✅ DIRECT TEMPLATE GENERATION TEST COMPLETE")

def test_api_endpoints():
    """Test the new API endpoints"""
    print("\n🚀 TESTING ENHANCED MEDICAL RESPONSE API ENDPOINTS")
    print("=" * 70)
    
    base_url = "http://localhost:8001"
    
    # Test cases
    test_cases = [
        {
            "symptom": "chest pain",
            "context": {"demographics": {"age": 45, "gender": "male"}}
        },
        {
            "symptom": "severe headache with nausea",
            "context": {"demographics": {"age": 35, "gender": "female"}}
        },
        {
            "symptom": "shortness of breath",
            "context": None
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. TESTING API: '{test_case['symptom']}'")
        print("-" * 50)
        
        try:
            # Test enhanced response template endpoint
            template_payload = {
                "symptom_description": test_case["symptom"],
                "patient_context": test_case["context"]
            }
            
            response = requests.post(
                f"{base_url}/api/medical-ai/enhanced-response-template",
                json=template_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Template API SUCCESS")
                print(f"   Category: {data['category']}")
                print(f"   Questions: {len(data['questions'])}")
                print(f"   Red Flags: {len(data['red_flags'])}")
                print(f"   Confidence: {data['confidence_score']}")
            else:
                print(f"❌ Template API FAILED: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ API ERROR: {e}")
    
    # Test symptom categorization endpoint
    print(f"\n4. TESTING SYMPTOM CATEGORIZATION API")
    print("-" * 50)
    
    try:
        category_payload = {"symptom_description": "crushing chest pain with radiation to arm"}
        
        response = requests.post(
            f"{base_url}/api/medical-ai/symptom-category-analysis",
            json=category_payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Categorization API SUCCESS")
            print(f"   Identified: {data['identified_symptom']}")
            print(f"   Category: {data['category']}")
            print(f"   Confidence: {data['confidence']}")
            print(f"   Related: {data['related_symptoms'][:3]}...")
        else:
            print(f"❌ Categorization API FAILED: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Categorization API ERROR: {e}")
    
    print("\n" + "=" * 70)
    print("✅ API ENDPOINT TESTING COMPLETE")

def test_integration_with_medical_ai():
    """Test integration with existing medical AI service"""
    print("\n🚀 TESTING INTEGRATION WITH MEDICAL AI SERVICE")
    print("=" * 70)
    
    base_url = "http://localhost:8001"
    
    # Test complete medical consultation flow with enhanced templates
    test_conversations = [
        {
            "name": "Chest Pain Emergency",
            "messages": [
                "Hello",
                "I have crushing chest pain",
                "It started suddenly about 30 minutes ago",
                "It feels like pressure and goes to my left arm",
                "10 out of 10 severe",
                "Yes, I'm sweating and feel nauseous"
            ]
        },
        {
            "name": "Headache Assessment", 
            "messages": [
                "Hi",
                "I have a severe headache",
                "It started this morning suddenly",
                "It's throbbing on the right side",
                "8 out of 10 pain level",
                "No neck stiffness or fever"
            ]
        }
    ]
    
    for conversation in test_conversations:
        print(f"\n📋 TESTING: {conversation['name']}")
        print("-" * 40)
        
        try:
            # Initialize consultation
            init_response = requests.post(
                f"{base_url}/api/medical-ai/initialize",
                json={"patient_id": "test_patient", "demographics": {}},
                timeout=10
            )
            
            if init_response.status_code != 200:
                print(f"❌ Failed to initialize: {init_response.status_code}")
                continue
                
            context = init_response.json()["context"]
            consultation_id = init_response.json()["consultation_id"]
            
            # Send messages
            for j, message in enumerate(conversation["messages"], 1):
                print(f"  {j}. User: '{message}'")
                
                response = requests.post(
                    f"{base_url}/api/medical-ai/message",
                    json={
                        "message": message,
                        "patient_id": "test_patient",
                        "consultation_id": consultation_id,
                        "context": context
                    },
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data["response"][:100] + "..." if len(data["response"]) > 100 else data["response"]
                    print(f"     AI: {ai_response}")
                    print(f"     Stage: {data['stage']}, Urgency: {data.get('urgency', 'N/A')}")
                    context = data["context"]
                    
                    # Check if enhanced template data is present
                    if "enhanced_template_data" in context:
                        template_data = context["enhanced_template_data"]
                        print(f"     ✅ Template Applied: {template_data.get('category', 'N/A')}")
                    
                else:
                    print(f"     ❌ Message failed: {response.status_code}")
                    break
                    
        except Exception as e:
            print(f"❌ Conversation ERROR: {e}")
    
    print("\n" + "=" * 70)
    print("✅ MEDICAL AI INTEGRATION TESTING COMPLETE")

if __name__ == "__main__":
    # Run all tests
    test_enhanced_template_generator_direct()
    test_api_endpoints()
    test_integration_with_medical_ai()
    
    print("\n🎯 PHASE 5 ENHANCED MEDICAL RESPONSE GENERATION TESTING COMPLETE! 🎯")
    print("=" * 70)