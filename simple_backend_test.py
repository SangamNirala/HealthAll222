#!/usr/bin/env python3
"""
Simple backend test to verify basic functionality
"""

import requests
import json
import os
from datetime import datetime

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://med-intent-flow.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def test_basic_functionality():
    print("🔍 TESTING BASIC BACKEND FUNCTIONALITY")
    print("=" * 50)
    
    # Test 1: Initialize consultation
    print("\n1. Testing consultation initialization...")
    init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
        json={
            "patient_id": "test-patient-simple",
            "timestamp": datetime.now().isoformat()
        },
        timeout=30
    )
    
    print(f"   Status: {init_response.status_code}")
    if init_response.status_code == 200:
        init_data = init_response.json()
        consultation_id = init_data.get("consultation_id")
        print(f"   ✅ Success - Consultation ID: {consultation_id}")
        print(f"   Stage: {init_data.get('current_stage')}")
    else:
        print(f"   ❌ Failed: {init_response.text}")
        return
    
    # Test 2: Send clear symptom message
    print("\n2. Testing clear symptom message...")
    clear_messages = [
        "I have a severe headache",
        "My head hurts really bad",
        "I am experiencing headache pain",
        "headache"
    ]
    
    for message in clear_messages:
        print(f"\n   Testing message: '{message}'")
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
            response_text = data.get("response", "")
            stage = data.get("current_stage", "")
            
            print(f"   Status: {response.status_code}")
            print(f"   Stage: {stage}")
            print(f"   Response: {response_text[:150]}...")
            
            # Check if it's the generic response
            if "I understand you'd like to discuss something health-related" in response_text:
                print("   ❌ Getting generic response - symptom not recognized")
            else:
                print("   ✅ Specific response - symptom recognized")
        else:
            print(f"   ❌ Failed: {response.status_code} - {response.text}")

    # Test 3: Check if backend endpoints are working
    print("\n3. Testing other endpoints...")
    
    # Test medical AI intent classification
    print("\n   Testing intent classification...")
    intent_response = requests.post(f"{API_BASE}/medical-ai/intent-classification",
        json={
            "message": "I have a headache",
            "context": {}
        },
        timeout=30
    )
    
    print(f"   Intent classification status: {intent_response.status_code}")
    if intent_response.status_code == 200:
        intent_data = intent_response.json()
        print(f"   Intent: {intent_data.get('primary_intent')}")
        print(f"   Confidence: {intent_data.get('confidence_score')}")
    else:
        print(f"   Intent classification failed: {intent_response.text}")

if __name__ == "__main__":
    test_basic_functionality()