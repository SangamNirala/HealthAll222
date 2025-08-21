#!/usr/bin/env python3
"""
🔄 FOCUSED CONVERSATION LOOP DEBUGGING TEST 🔄

Test the exact conversation flow that's causing the loop issue to get detailed debugging output.
Follow this conversation:

1. POST /api/medical-ai/initialize with patient_id='anonymous'
2. POST /api/medical-ai/message with message='hi' and full context from step 1
3. POST /api/medical-ai/message with message='I have a headache' and full context from step 2  
4. POST /api/medical-ai/message with message='it has started 2 days before' and full context from step 3
5. POST /api/medical-ai/message with message='it is dull' and full context from step 4
6. POST /api/medical-ai/message with message='food' and full context from step 5
7. POST /api/medical-ai/message with message='position' and full context from step 6

For each request, pass the complete "context" object from the previous response (not just consultation_id).
Focus on capturing the HPI DEBUG messages to see exactly what's happening in the _get_next_hpi_element_smart function.

Author: Testing Agent
Date: 2025-01-19
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://mediq-followup.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def test_conversation_flow():
    """Test the exact conversation flow mentioned in the review request"""
    
    print("🔄 TESTING EXACT CONVERSATION FLOW FROM REVIEW REQUEST")
    print("=" * 80)
    print(f"Backend URL: {API_BASE}")
    print()
    
    # Step 1: Initialize conversation
    print("📋 STEP 1: POST /api/medical-ai/initialize with patient_id='anonymous'")
    print("-" * 60)
    
    try:
        init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
            json={
                "patient_id": "anonymous",
                "timestamp": datetime.now().isoformat()
            },
            timeout=30
        )
        
        if init_response.status_code != 200:
            print(f"❌ FAILED: HTTP {init_response.status_code}")
            print(f"Response: {init_response.text}")
            return False
            
        init_data = init_response.json()
        print(f"✅ SUCCESS: Consultation ID: {init_data.get('consultation_id')}")
        print(f"   Stage: {init_data.get('current_stage')}")
        print(f"   Context keys: {list(init_data.get('context', {}).keys())}")
        print()
        
        # Store the complete context for next request
        current_context = init_data.get('context', {})
        
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False
    
    # Define conversation steps
    conversation_steps = [
        "hi",
        "I have a headache", 
        "it has started 2 days before",
        "it is dull",
        "food",
        "position"
    ]
    
    # Execute each conversation step
    for step_num, message in enumerate(conversation_steps, 2):
        print(f"📋 STEP {step_num}: POST /api/medical-ai/message with message='{message}' and full context")
        print("-" * 60)
        
        try:
            # Prepare request with FULL context object (not just consultation_id)
            request_payload = {
                "message": message,
                "context": current_context  # Pass the complete context object
            }
            
            print(f"🔍 Request context keys: {list(current_context.keys())}")
            print(f"🔍 Consultation ID in context: {current_context.get('consultation_id', 'NOT FOUND')}")
            
            message_response = requests.post(f"{API_BASE}/medical-ai/message",
                json=request_payload,
                timeout=30
            )
            
            if message_response.status_code != 200:
                print(f"❌ FAILED: HTTP {message_response.status_code}")
                print(f"Response: {message_response.text}")
                return False
                
            message_data = message_response.json()
            
            # Check for generic fallback response
            response_text = message_data.get('response', '')
            is_generic_fallback = 'I understand you\'d like to discuss something health-related' in response_text
            
            print(f"✅ SUCCESS: Stage: {message_data.get('current_stage')}")
            print(f"   Consultation ID: {message_data.get('consultation_id')}")
            print(f"   Urgency: {message_data.get('urgency', 'N/A')}")
            print(f"   Response length: {len(response_text)} chars")
            print(f"   Generic fallback: {'YES ❌' if is_generic_fallback else 'NO ✅'}")
            print(f"   Response preview: {response_text[:150]}...")
            
            if is_generic_fallback:
                print(f"⚠️  ISSUE DETECTED: Generic fallback response at step {step_num}")
                print(f"   This indicates conversation context is not being maintained properly")
            
            # Update context for next step - use the complete context object
            new_context = message_data.get('context', {})
            if new_context:
                current_context = new_context
                print(f"   Updated context keys: {list(current_context.keys())}")
            else:
                print(f"   ⚠️  WARNING: No context returned from API")
            
            print()
            
        except Exception as e:
            print(f"❌ EXCEPTION: {str(e)}")
            return False
    
    print("🎯 CONVERSATION FLOW TEST COMPLETED")
    print("=" * 80)
    print()
    print("📊 ANALYSIS:")
    print("- If you see generic fallback responses after step 3 ('I have a headache'),")
    print("  this indicates the conversation context is not being maintained properly.")
    print("- The issue is likely in the backend's context processing or conversation history handling.")
    print("- Check backend logs for HPI DEBUG messages to see what's happening in _get_next_hpi_element_smart.")
    print()
    
    return True

def test_context_passing_methodology():
    """Test different context passing methodologies to identify the correct approach"""
    
    print("🧪 TESTING CONTEXT PASSING METHODOLOGIES")
    print("=" * 80)
    
    # Initialize conversation first
    init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
        json={"patient_id": "anonymous"},
        timeout=30
    )
    
    if init_response.status_code != 200:
        print("❌ Failed to initialize conversation")
        return False
    
    init_data = init_response.json()
    consultation_id = init_data.get('consultation_id')
    full_context = init_data.get('context', {})
    
    print(f"✅ Initialized: {consultation_id}")
    print()
    
    # Test Method 1: Pass only consultation_id
    print("📋 METHOD 1: Pass only consultation_id")
    print("-" * 40)
    
    try:
        response1 = requests.post(f"{API_BASE}/medical-ai/message",
            json={
                "message": "I have a headache",
                "consultation_id": consultation_id
            },
            timeout=30
        )
        
        if response1.status_code == 200:
            data1 = response1.json()
            is_generic1 = 'I understand you\'d like to discuss something health-related' in data1.get('response', '')
            print(f"   Result: {'Generic fallback ❌' if is_generic1 else 'Proper response ✅'}")
            print(f"   Stage: {data1.get('current_stage')}")
        else:
            print(f"   Failed: HTTP {response1.status_code}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    
    print()
    
    # Test Method 2: Pass full context object
    print("📋 METHOD 2: Pass full context object")
    print("-" * 40)
    
    try:
        response2 = requests.post(f"{API_BASE}/medical-ai/message",
            json={
                "message": "I have a headache",
                "context": full_context
            },
            timeout=30
        )
        
        if response2.status_code == 200:
            data2 = response2.json()
            is_generic2 = 'I understand you\'d like to discuss something health-related' in data2.get('response', '')
            print(f"   Result: {'Generic fallback ❌' if is_generic2 else 'Proper response ✅'}")
            print(f"   Stage: {data2.get('current_stage')}")
        else:
            print(f"   Failed: HTTP {response2.status_code}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    
    print()
    
    # Test Method 3: Pass both consultation_id and context
    print("📋 METHOD 3: Pass both consultation_id and context")
    print("-" * 40)
    
    try:
        response3 = requests.post(f"{API_BASE}/medical-ai/message",
            json={
                "message": "I have a headache",
                "consultation_id": consultation_id,
                "context": full_context
            },
            timeout=30
        )
        
        if response3.status_code == 200:
            data3 = response3.json()
            is_generic3 = 'I understand you\'d like to discuss something health-related' in data3.get('response', '')
            print(f"   Result: {'Generic fallback ❌' if is_generic3 else 'Proper response ✅'}")
            print(f"   Stage: {data3.get('current_stage')}")
        else:
            print(f"   Failed: HTTP {response3.status_code}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    
    print()
    return True

if __name__ == "__main__":
    print("🔄 FOCUSED CONVERSATION LOOP DEBUGGING TEST")
    print("Testing the exact conversation flow from the review request")
    print()
    
    # Test the exact conversation flow
    flow_success = test_conversation_flow()
    
    print()
    
    # Test different context passing methodologies
    methodology_success = test_context_passing_methodology()
    
    if flow_success and methodology_success:
        print("✅ All tests completed successfully")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)