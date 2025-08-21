#!/usr/bin/env python3
"""
🔍 RESPONSE ANALYSIS TEST 🔍

Detailed analysis of conversation responses to understand the "meaningful_responses" failure.

Author: Testing Agent
Date: 2025-01-17
"""

import requests
import json
import time
import sys
import os
from datetime import datetime

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://ai-test-suite.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def analyze_conversation_responses():
    """Analyze the actual conversation responses in detail"""
    print("🔍 DETAILED RESPONSE ANALYSIS")
    print("=" * 60)
    
    # Initialize conversation
    init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
        json={
            "patient_id": "anonymous",
            "timestamp": datetime.now().isoformat()
        },
        timeout=30
    )
    
    if init_response.status_code != 200:
        print(f"❌ Failed to initialize: {init_response.status_code}")
        return
    
    init_data = init_response.json()
    consultation_id = init_data.get("consultation_id")
    full_context = init_data.get("context", {})
    
    print(f"✅ Initialized: {consultation_id}")
    
    # Test each message
    messages = [
        "hi",
        "I have a headache", 
        "it has started 2 days before",
        "it is dull",
        "food",
        "position"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n--- STEP {i+1}: '{message}' ---")
        
        request_payload = {
            "message": message,
            "context": full_context,
            "consultation_id": consultation_id,
            "conversation_history": []
        }
        
        response = requests.post(f"{API_BASE}/medical-ai/message",
            json=request_payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            full_context = data.get("context", full_context)
            
            response_text = data.get("response", "")
            current_stage = data.get("current_stage", "")
            urgency = data.get("urgency", "")
            
            print(f"Stage: {current_stage}")
            print(f"Urgency: {urgency}")
            print(f"Response Length: {len(response_text)} characters")
            print(f"Response: {response_text}")
            
            # Check for issues
            has_technical_issue = "technical issue" in response_text.lower()
            has_generic_fallback = "I understand you'd like to discuss something health-related" in response_text
            is_too_short = len(response_text) < 30
            
            print(f"Technical Issue: {has_technical_issue}")
            print(f"Generic Fallback: {has_generic_fallback}")
            print(f"Too Short: {is_too_short}")
            
            if has_technical_issue or has_generic_fallback or is_too_short:
                print("❌ RESPONSE ISSUE DETECTED")
            else:
                print("✅ Response looks good")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")

if __name__ == "__main__":
    analyze_conversation_responses()