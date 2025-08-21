#!/usr/bin/env python3
"""
Debug script to test symptom extraction directly
"""

import requests
import json
import os
from datetime import datetime

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://mediq-engine.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def test_symptom_extraction():
    print("🔍 DEBUGGING SYMPTOM EXTRACTION")
    print("=" * 50)
    
    # Initialize consultation
    print("\n1. Initializing consultation...")
    init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
        json={
            "patient_id": "debug-extraction-test",
            "timestamp": datetime.now().isoformat()
        },
        timeout=30
    )
    
    if init_response.status_code != 200:
        print(f"❌ Initialization failed: {init_response.status_code} - {init_response.text}")
        return
    
    init_data = init_response.json()
    consultation_id = init_data.get("consultation_id")
    print(f"✅ Consultation initialized: {consultation_id}")
    
    # Test symptom messages
    test_messages = [
        "I have a headache",
        "My head hurts",
        "I am experiencing headache pain",
        "headache",
        "I have chest pain",
        "I have a fever"
    ]
    
    for message in test_messages:
        print(f"\n2. Testing message: '{message}'")
        
        response = requests.post(f"{API_BASE}/medical-ai/message",
            json={
                "consultation_id": consultation_id,
                "message": message,
                "conversation_history": []
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"   Stage: {data.get('current_stage')}")
            print(f"   Chief Complaint: {data.get('context', {}).get('chief_complaint', 'None')}")
            print(f"   Response: {data.get('response', '')[:100]}...")
            
            # Check symptom data
            symptom_data = data.get('context', {}).get('symptom_data', {})
            if symptom_data:
                print(f"   Symptom Data Keys: {list(symptom_data.keys())}")
                symptoms = symptom_data.get('symptoms', [])
                if symptoms:
                    print(f"   Detected Symptoms: {symptoms}")
                else:
                    print("   No symptoms detected in symptom_data")
            else:
                print("   No symptom_data in context")
                
            # Check contextual reasoning
            contextual_reasoning = data.get('contextual_reasoning', {})
            if contextual_reasoning:
                print(f"   Contextual Reasoning Keys: {list(contextual_reasoning.keys())}")
            
        else:
            print(f"   ❌ Request failed: {response.status_code} - {response.text}")
        
        print("-" * 30)

if __name__ == "__main__":
    test_symptom_extraction()