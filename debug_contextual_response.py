#!/usr/bin/env python3
"""
Debug script to examine the actual API response structure for contextual reasoning
"""

import requests
import json
import os
from datetime import datetime

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://medical-validation.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def debug_api_response():
    """Debug the actual API response structure"""
    
    print("🔍 DEBUGGING CONTEXTUAL REASONING API RESPONSE")
    print("=" * 60)
    
    try:
        # Initialize consultation
        print("1. Initializing consultation...")
        init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
            json={
                "patient_id": "debug-contextual",
                "timestamp": datetime.now().isoformat()
            },
            timeout=30
        )
        
        if init_response.status_code != 200:
            print(f"❌ Initialization failed: {init_response.status_code}")
            return
            
        init_data = init_response.json()
        consultation_id = init_data.get("consultation_id")
        print(f"✅ Consultation initialized: {consultation_id}")
        
        # Test with the first ultra-challenging scenario
        print("\n2. Testing Ultra-Challenging Scenario 1...")
        scenario_1 = "Every morning when I get out of bed I feel dizzy and nauseous, sometimes I even feel like I'm going to faint, but it goes away after I sit back down for a few minutes"
        
        response = requests.post(f"{API_BASE}/medical-ai/message",
            json={
                "consultation_id": consultation_id,
                "message": scenario_1,
                "timestamp": datetime.now().isoformat()
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Response received successfully")
            
            print("\n3. FULL API RESPONSE STRUCTURE:")
            print("-" * 40)
            print(json.dumps(data, indent=2))
            
            print("\n4. RESPONSE KEYS ANALYSIS:")
            print("-" * 40)
            print(f"Top-level keys: {list(data.keys())}")
            
            # Check for contextual reasoning fields
            contextual_fields = [
                "contextual_reasoning",
                "causal_relationships", 
                "clinical_hypotheses",
                "context_based_recommendations",
                "trigger_avoidance_strategies",
                "specialist_referral_context"
            ]
            
            print("\n5. CONTEXTUAL REASONING FIELDS CHECK:")
            print("-" * 40)
            for field in contextual_fields:
                if field in data:
                    print(f"✅ {field}: PRESENT")
                    if isinstance(data[field], (dict, list)) and data[field]:
                        print(f"   Content: {json.dumps(data[field], indent=2)[:200]}...")
                    else:
                        print(f"   Content: {data[field]}")
                else:
                    print(f"❌ {field}: MISSING")
            
            # Check if contextual_reasoning is nested
            if "contextual_reasoning" in data and isinstance(data["contextual_reasoning"], dict):
                print("\n6. NESTED CONTEXTUAL REASONING FIELDS:")
                print("-" * 40)
                contextual_data = data["contextual_reasoning"]
                for field in contextual_fields[1:]:  # Skip contextual_reasoning itself
                    if field in contextual_data:
                        print(f"✅ contextual_reasoning.{field}: PRESENT")
                        print(f"   Content: {json.dumps(contextual_data[field], indent=2)[:200]}...")
                    else:
                        print(f"❌ contextual_reasoning.{field}: MISSING")
            
            print("\n7. URGENCY AND EMERGENCY DETECTION:")
            print("-" * 40)
            print(f"Urgency: {data.get('urgency', 'NOT FOUND')}")
            print(f"Emergency Detected: {data.get('emergency_detected', 'NOT FOUND')}")
            print(f"Current Stage: {data.get('current_stage', 'NOT FOUND')}")
            
        else:
            print(f"❌ Message request failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Debug failed with exception: {str(e)}")

if __name__ == "__main__":
    debug_api_response()