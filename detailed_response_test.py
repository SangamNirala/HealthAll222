#!/usr/bin/env python3
"""
Detailed response examination for Step 4.2 testing
"""

import requests
import json
from datetime import datetime

BACKEND_URL = "https://medchat-enhance-1.preview.emergentagent.com/api"

def test_scenario(scenario_name, message):
    print(f"\n🔍 TESTING: {scenario_name}")
    print("=" * 60)
    
    # Initialize consultation
    init_response = requests.post(
        f"{BACKEND_URL}/medical-ai/initialize",
        json={"patient_id": "anonymous", "timestamp": datetime.now().isoformat()},
        timeout=30
    )
    
    if init_response.status_code != 200:
        print(f"❌ Initialization failed: {init_response.status_code}")
        return
    
    init_data = init_response.json()
    consultation_id = init_data.get("consultation_id", "")
    print(f"✅ Consultation ID: {consultation_id}")
    
    # Send greeting
    greeting_response = requests.post(
        f"{BACKEND_URL}/medical-ai/message",
        json={
            "message": "hi",
            "consultation_id": consultation_id,
            "patient_id": "anonymous"
        },
        timeout=30
    )
    
    if greeting_response.status_code != 200:
        print(f"❌ Greeting failed: {greeting_response.status_code}")
        return
    
    # Send test message
    test_response = requests.post(
        f"{BACKEND_URL}/medical-ai/message",
        json={
            "message": message,
            "consultation_id": consultation_id,
            "patient_id": "anonymous"
        },
        timeout=30
    )
    
    if test_response.status_code != 200:
        print(f"❌ Test message failed: {test_response.status_code}")
        return
    
    response_data = test_response.json()
    response_text = response_data.get("response", "")
    
    print(f"📝 INPUT: '{message}'")
    print(f"🤖 RESPONSE: {response_text}")
    print(f"🎯 URGENCY: {response_data.get('urgency', 'N/A')}")
    print(f"📊 STAGE: {response_data.get('current_stage', 'N/A')}")
    
    # Check for next questions
    next_questions = response_data.get("next_questions", [])
    if next_questions:
        print(f"❓ NEXT QUESTIONS: {next_questions}")
    
    return response_data

# Test all scenarios
scenarios = [
    ("Incomplete Pain - chest pain", "chest pain"),
    ("Emotional Response - scared", "scared"), 
    ("Temporal Vagueness - recently", "recently"),
    ("Working Case - not feeling well", "I'm not feeling well"),
    ("Working Case - chest", "chest")
]

for scenario_name, message in scenarios:
    test_scenario(scenario_name, message)