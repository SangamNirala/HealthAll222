#!/usr/bin/env python3
"""
Debug script to examine actual chatbot responses and understand the conversation flow issues
"""

import requests
import json
import os
from datetime import datetime

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://context-flow-check.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def debug_conversation_flow():
    print("🔍 DEBUGGING CHATBOT CONVERSATION FLOW")
    print("=" * 60)
    
    # Initialize consultation
    print("\n1. Initializing consultation...")
    init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
        json={
            "patient_id": "debug-test-patient",
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
    print(f"   Initial stage: {init_data.get('current_stage')}")
    print(f"   Initial response: {init_data.get('response', '')[:100]}...")
    
    # Test the exact conversation flow
    conversation_steps = [
        "hi",
        "I have a headache", 
        "it has started 2 days before",
        "it is dull",
        "food",
        "position"
    ]
    
    conversation_history = []
    
    for i, message in enumerate(conversation_steps):
        print(f"\n{i+2}. Sending message: '{message}'")
        
        # Build conversation history
        conversation_history_payload = []
        for j, entry in enumerate(conversation_history):
            conversation_history_payload.append({
                "role": "user" if j % 2 == 0 else "assistant",
                "content": entry
            })
        
        payload = {
            "consultation_id": consultation_id,
            "message": message,
            "conversation_history": conversation_history_payload
        }
        
        response = requests.post(f"{API_BASE}/medical-ai/message",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Add to conversation history
            conversation_history.append(message)
            conversation_history.append(data.get("response", ""))
            
            print(f"   ✅ Response received")
            print(f"   Stage: {data.get('current_stage')}")
            print(f"   Urgency: {data.get('urgency')}")
            print(f"   Emergency: {data.get('emergency_detected')}")
            print(f"   Response: {data.get('response', '')[:200]}...")
            
            # Check for context
            context = data.get('context', {})
            if context:
                print(f"   Context keys: {list(context.keys())}")
            
            # Check next questions
            next_questions = data.get('next_questions', [])
            if next_questions:
                print(f"   Next questions: {next_questions[:2]}")  # Show first 2
                
        else:
            print(f"   ❌ Request failed: {response.status_code} - {response.text}")
            break
    
    print(f"\n📊 Final conversation history length: {len(conversation_history)}")

if __name__ == "__main__":
    debug_conversation_flow()