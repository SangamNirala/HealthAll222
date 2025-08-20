#!/usr/bin/env python3
"""
🔍 DEBUG CONVERSATION FLOW TEST 🔍

Simple test to debug the conversation flow issue where the chatbot
falls back to generic responses after the HPI stage.
"""

import requests
import json
import os
from datetime import datetime

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://symptom-analyzer-5.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def test_conversation_debug():
    """Test the conversation flow with detailed debugging"""
    
    print("🔍 DEBUG CONVERSATION FLOW TEST")
    print("=" * 50)
    
    # Step 1: Initialize
    print("\n1. Initializing conversation...")
    init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
        json={
            "patient_id": "anonymous",
            "timestamp": datetime.now().isoformat()
        },
        timeout=30
    )
    
    if init_response.status_code != 200:
        print(f"❌ Initialization failed: {init_response.status_code}")
        return
    
    init_data = init_response.json()
    consultation_id = init_data.get("consultation_id")
    print(f"✅ Initialized: {consultation_id}")
    print(f"   Stage: {init_data.get('current_stage')}")
    
    # Step 2: Send "hi"
    print("\n2. Sending 'hi'...")
    hi_response = requests.post(f"{API_BASE}/medical-ai/message",
        json={
            "consultation_id": consultation_id,
            "message": "hi",
            "conversation_history": []
        },
        timeout=30
    )
    
    if hi_response.status_code != 200:
        print(f"❌ Hi message failed: {hi_response.status_code}")
        return
    
    hi_data = hi_response.json()
    print(f"✅ Hi processed")
    print(f"   Stage: {hi_data.get('current_stage')}")
    print(f"   Response: {hi_data.get('response')[:100]}...")
    
    # Step 3: Send "I have a headache"
    print("\n3. Sending 'I have a headache'...")
    headache_response = requests.post(f"{API_BASE}/medical-ai/message",
        json={
            "consultation_id": consultation_id,
            "message": "I have a headache",
            "conversation_history": [
                {"role": "user", "content": "hi", "timestamp": datetime.now().isoformat()},
                {"role": "assistant", "content": hi_data.get('response', ''), "timestamp": datetime.now().isoformat()}
            ]
        },
        timeout=30
    )
    
    if headache_response.status_code != 200:
        print(f"❌ Headache message failed: {headache_response.status_code}")
        return
    
    headache_data = headache_response.json()
    print(f"✅ Headache processed")
    print(f"   Stage: {headache_data.get('current_stage')}")
    print(f"   Response: {headache_data.get('response')[:100]}...")
    
    # Step 4: Send "it has started 2 days before" - This is where it fails
    print("\n4. Sending 'it has started 2 days before'...")
    timing_response = requests.post(f"{API_BASE}/medical-ai/message",
        json={
            "consultation_id": consultation_id,
            "message": "it has started 2 days before",
            "conversation_history": [
                {"role": "user", "content": "hi", "timestamp": datetime.now().isoformat()},
                {"role": "assistant", "content": hi_data.get('response', ''), "timestamp": datetime.now().isoformat()},
                {"role": "user", "content": "I have a headache", "timestamp": datetime.now().isoformat()},
                {"role": "assistant", "content": headache_data.get('response', ''), "timestamp": datetime.now().isoformat()}
            ]
        },
        timeout=30
    )
    
    if timing_response.status_code != 200:
        print(f"❌ Timing message failed: {timing_response.status_code}")
        return
    
    timing_data = timing_response.json()
    print(f"✅ Timing processed")
    print(f"   Stage: {timing_data.get('current_stage')}")
    print(f"   Response: {timing_data.get('response')[:200]}...")
    
    # Check if it's the generic fallback response
    if "I understand you'd like to discuss something health-related" in timing_data.get('response', ''):
        print("❌ ISSUE DETECTED: Generic fallback response returned!")
        print("   This indicates the HPI stage is not processing the message correctly")
    else:
        print("✅ Proper HPI response returned")
    
    # Step 5: Send "it is dull"
    print("\n5. Sending 'it is dull'...")
    dull_response = requests.post(f"{API_BASE}/medical-ai/message",
        json={
            "consultation_id": consultation_id,
            "message": "it is dull",
            "conversation_history": [
                {"role": "user", "content": "hi", "timestamp": datetime.now().isoformat()},
                {"role": "assistant", "content": hi_data.get('response', ''), "timestamp": datetime.now().isoformat()},
                {"role": "user", "content": "I have a headache", "timestamp": datetime.now().isoformat()},
                {"role": "assistant", "content": headache_data.get('response', ''), "timestamp": datetime.now().isoformat()},
                {"role": "user", "content": "it has started 2 days before", "timestamp": datetime.now().isoformat()},
                {"role": "assistant", "content": timing_data.get('response', ''), "timestamp": datetime.now().isoformat()}
            ]
        },
        timeout=30
    )
    
    if dull_response.status_code != 200:
        print(f"❌ Dull message failed: {dull_response.status_code}")
        return
    
    dull_data = dull_response.json()
    print(f"✅ Dull processed")
    print(f"   Stage: {dull_data.get('current_stage')}")
    print(f"   Response: {dull_data.get('response')[:200]}...")
    
    # Check if it's the generic fallback response
    if "I understand you'd like to discuss something health-related" in dull_data.get('response', ''):
        print("❌ ISSUE DETECTED: Generic fallback response returned!")
    else:
        print("✅ Proper HPI response returned")
    
    print("\n" + "=" * 50)
    print("🔍 DEBUG SUMMARY:")
    print(f"   Step 1 (Initialize): Stage = {init_data.get('current_stage')}")
    print(f"   Step 2 (Hi): Stage = {hi_data.get('current_stage')}")
    print(f"   Step 3 (Headache): Stage = {headache_data.get('current_stage')}")
    print(f"   Step 4 (Timing): Stage = {timing_data.get('current_stage')}")
    print(f"   Step 5 (Dull): Stage = {dull_data.get('current_stage')}")
    
    # Check for stage regression
    if (headache_data.get('current_stage') == 'history_present_illness' and 
        timing_data.get('current_stage') == 'chief_complaint'):
        print("\n❌ CRITICAL ISSUE: Stage regressed from HPI back to chief_complaint!")
        print("   This indicates an exception or error in the HPI stage processing.")
    
if __name__ == "__main__":
    test_conversation_debug()