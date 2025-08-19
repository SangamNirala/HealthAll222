#!/usr/bin/env python3
"""
🔍 QUICK CONVERSATION LOOP DIAGNOSIS TEST 🔍

Quick test to diagnose the exact issue with the conversation loop
"""

import requests
import json
import os

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://medemo-ai.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def test_conversation_issue():
    print("🔍 DIAGNOSING CONVERSATION LOOP ISSUE")
    print("=" * 50)
    
    # Step 1: Initialize
    print("1. Initializing conversation...")
    init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
        json={"patient_id": "test-diagnosis", "timestamp": "2025-01-19T02:00:00Z"},
        timeout=30
    )
    
    if init_response.status_code != 200:
        print(f"❌ Initialization failed: {init_response.status_code}")
        return
    
    init_data = init_response.json()
    consultation_id = init_data.get("consultation_id")
    print(f"✅ Initialized: {consultation_id}, Stage: {init_data.get('current_stage')}")
    
    # Step 2: Send "hi"
    print("\n2. Sending 'hi'...")
    hi_response = requests.post(f"{API_BASE}/medical-ai/message",
        json={
            "message": "hi",
            "consultation_id": consultation_id,
            "conversation_history": []
        },
        timeout=30
    )
    
    if hi_response.status_code == 200:
        hi_data = hi_response.json()
        print(f"✅ Hi response: Stage: {hi_data.get('current_stage')}")
        print(f"   Response: {hi_data.get('response', '')[:100]}...")
    else:
        print(f"❌ Hi failed: {hi_response.status_code}")
        return
    
    # Step 3: Send "I have a headache"
    print("\n3. Sending 'I have a headache'...")
    headache_response = requests.post(f"{API_BASE}/medical-ai/message",
        json={
            "message": "I have a headache",
            "consultation_id": consultation_id,
            "conversation_history": [
                {"role": "user", "content": "hi"},
                {"role": "assistant", "content": hi_data.get('response', '')}
            ]
        },
        timeout=30
    )
    
    if headache_response.status_code == 200:
        headache_data = headache_response.json()
        print(f"✅ Headache response: Stage: {headache_data.get('current_stage')}")
        print(f"   Response: {headache_data.get('response', '')[:100]}...")
    else:
        print(f"❌ Headache failed: {headache_response.status_code}")
        print(f"   Error: {headache_response.text}")
        return
    
    # Step 4: Send "it has started 2 days before" 
    print("\n4. Sending 'it has started 2 days before'...")
    timing_response = requests.post(f"{API_BASE}/medical-ai/message",
        json={
            "message": "it has started 2 days before",
            "consultation_id": consultation_id,
            "conversation_history": [
                {"role": "user", "content": "hi"},
                {"role": "assistant", "content": hi_data.get('response', '')},
                {"role": "user", "content": "I have a headache"},
                {"role": "assistant", "content": headache_data.get('response', '')}
            ]
        },
        timeout=30
    )
    
    if timing_response.status_code == 200:
        timing_data = timing_response.json()
        print(f"✅ Timing response: Stage: {timing_data.get('current_stage')}")
        print(f"   Response: {timing_data.get('response', '')[:100]}...")
        
        # Check if this is the problematic generic response
        if "I understand you'd like to discuss something health-related" in timing_data.get('response', ''):
            print("🚨 ISSUE DETECTED: Generic fallback response detected!")
            print("   This indicates the HPI stage handler is failing and falling back to chief complaint")
    else:
        print(f"❌ Timing failed: {timing_response.status_code}")
        print(f"   Error: {timing_response.text}")

if __name__ == "__main__":
    test_conversation_issue()