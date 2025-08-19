#!/usr/bin/env python3
"""
Debug test for Step 2.2 Context-Aware Medical Reasoning Engine
"""

import requests
import json
import os
from datetime import datetime

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://clinical-ai-4.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def debug_medical_ai_flow():
    """Debug the medical AI consultation flow"""
    
    print("🔍 DEBUGGING MEDICAL AI CONSULTATION FLOW")
    print("=" * 50)
    
    # Step 1: Initialize consultation
    print("Step 1: Initializing consultation...")
    init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
        json={
            "patient_id": "debug-test",
            "timestamp": datetime.now().isoformat()
        },
        timeout=30
    )
    
    print(f"Initialize Status: {init_response.status_code}")
    if init_response.status_code == 200:
        init_data = init_response.json()
        print(f"Consultation ID: {init_data.get('consultation_id')}")
        print(f"Current Stage: {init_data.get('current_stage')}")
        print(f"Response: {init_data.get('response')[:100]}...")
        
        consultation_id = init_data.get('consultation_id')
        
        # Step 2: Send contextual symptom message
        print("\nStep 2: Sending contextual symptom message...")
        contextual_message = "Every morning when I get out of bed I feel dizzy and nauseous, sometimes I even feel like I'm going to faint, but it goes away after I sit back down for a few minutes"
        
        message_response = requests.post(f"{API_BASE}/medical-ai/message",
            json={
                "consultation_id": consultation_id,
                "message": contextual_message,
                "timestamp": datetime.now().isoformat()
            },
            timeout=30
        )
        
        print(f"Message Status: {message_response.status_code}")
        if message_response.status_code == 200:
            message_data = message_response.json()
            print(f"Stage: {message_data.get('stage')}")
            print(f"Urgency: {message_data.get('urgency')}")
            print(f"Emergency Detected: {message_data.get('emergency_detected')}")
            print(f"Response: {message_data.get('response')[:200]}...")
            
            # Check for contextual reasoning in context
            context = message_data.get('context', {})
            print(f"\nContext keys: {list(context.keys())}")
            
            # Check symptom data
            symptom_data = context.get('symptom_data', {})
            print(f"Symptoms detected: {len(symptom_data.get('symptoms', []))}")
            
            # Look for contextual reasoning indicators
            full_response = json.dumps(message_data, indent=2)
            contextual_keywords = ['positional', 'orthostatic', 'standing', 'sitting', 'context', 'trigger', 'causal']
            found_keywords = [kw for kw in contextual_keywords if kw.lower() in full_response.lower()]
            print(f"Contextual keywords found: {found_keywords}")
            
            # Print full response for analysis
            print(f"\nFull Response Structure:")
            print(json.dumps(message_data, indent=2)[:1000] + "...")
            
        else:
            print(f"Message failed: {message_response.text}")
    else:
        print(f"Initialize failed: {init_response.text}")

def test_direct_symptom_processing():
    """Test direct symptom processing without consultation flow"""
    
    print("\n🔍 TESTING DIRECT SYMPTOM PROCESSING")
    print("=" * 50)
    
    # Try to send a message without proper initialization
    direct_message = "I get crushing chest pain when I climb stairs but it goes away with rest"
    
    try:
        # This should fail or give us insight into the flow
        response = requests.post(f"{API_BASE}/medical-ai/message",
            json={
                "consultation_id": "test-direct",
                "message": direct_message,
                "timestamp": datetime.now().isoformat()
            },
            timeout=30
        )
        
        print(f"Direct message status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data.get('response')[:200]}...")
            print(f"Urgency: {data.get('urgency')}")
        else:
            print(f"Direct message failed: {response.text}")
            
    except Exception as e:
        print(f"Direct message exception: {str(e)}")

def test_multiple_conversation_turns():
    """Test multiple conversation turns to see when contextual reasoning kicks in"""
    
    print("\n🔍 TESTING MULTIPLE CONVERSATION TURNS")
    print("=" * 50)
    
    # Initialize
    init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
        json={
            "patient_id": "multi-turn-test",
            "timestamp": datetime.now().isoformat()
        },
        timeout=30
    )
    
    if init_response.status_code != 200:
        print("Failed to initialize")
        return
        
    consultation_id = init_response.json().get('consultation_id')
    
    # Multiple turns
    messages = [
        "I have been having some health issues",
        "I get dizzy",
        "It happens when I stand up",
        "Every morning when I get out of bed I feel dizzy and nauseous"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\nTurn {i}: '{message}'")
        
        response = requests.post(f"{API_BASE}/medical-ai/message",
            json={
                "consultation_id": consultation_id,
                "message": message,
                "timestamp": datetime.now().isoformat()
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"Stage: {data.get('stage')}")
            print(f"Urgency: {data.get('urgency')}")
            print(f"Response: {data.get('response')[:150]}...")
            
            # Check for contextual reasoning
            response_text = data.get('response', '').lower()
            contextual_found = any(kw in response_text for kw in ['positional', 'orthostatic', 'standing', 'context'])
            print(f"Contextual reasoning detected: {contextual_found}")
        else:
            print(f"Failed: {response.status_code}")

if __name__ == "__main__":
    debug_medical_ai_flow()
    test_direct_symptom_processing()
    test_multiple_conversation_turns()