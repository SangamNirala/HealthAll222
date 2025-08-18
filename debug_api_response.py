#!/usr/bin/env python3
"""
Debug script to test API response structure
"""

import requests
import json
import os
from datetime import datetime

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://medical-intents.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def test_api_response():
    """Test API response structure with ultra-challenging scenarios"""
    
    # Initialize consultation
    print("Initializing consultation...")
    init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
        json={
            "patient_id": "debug-test",
            "timestamp": datetime.now().isoformat()
        },
        timeout=30
    )
    
    if init_response.status_code != 200:
        print(f"Initialization failed: {init_response.status_code} - {init_response.text}")
        return
    
    init_data = init_response.json()
    consultation_id = init_data.get('consultation_id')
    print(f"Consultation ID: {consultation_id}")
    
    # Test scenario 2 - Enhanced Cardiac
    scenario_text = "I get this crushing chest pain whenever I walk uphill or climb more than one flight of stairs, feels like an elephant sitting on my chest, but it completely goes away within 2-3 minutes of resting."
    
    print(f"\nTesting scenario: {scenario_text}")
    
    response = requests.post(f"{API_BASE}/medical-ai/message", 
        json={
            "consultation_id": consultation_id,
            "message": scenario_text,
            "timestamp": datetime.now().isoformat()
        },
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"\nAPI Response Structure:")
        print(f"- Response keys: {list(data.keys())}")
        print(f"- Urgency: {data.get('urgency')}")
        print(f"- Emergency detected: {data.get('emergency_detected')}")
        
        # Check contextual fields
        contextual_fields = [
            'causal_relationships', 'clinical_hypotheses', 'contextual_factors',
            'context_based_recommendations', 'trigger_avoidance_strategies', 
            'specialist_referral_context'
        ]
        
        print(f"\nContextual Fields:")
        for field in contextual_fields:
            value = data.get(field)
            if value is None:
                print(f"- {field}: None")
            elif isinstance(value, list):
                print(f"- {field}: {len(value)} items")
                if len(value) > 0:
                    print(f"  First item: {value[0]}")
            elif isinstance(value, dict):
                print(f"- {field}: {len(value)} keys - {list(value.keys())}")
            else:
                print(f"- {field}: {value}")
        
        # Check context object
        context = data.get('context', {})
        print(f"\nContext object keys: {list(context.keys())}")
        
        # Check if contextual reasoning is in context
        if 'contextual_reasoning' in context:
            contextual_reasoning = context['contextual_reasoning']
            print(f"\nContextual reasoning in context:")
            print(f"- Keys: {list(contextual_reasoning.keys())}")
            print(f"- Causal relationships: {len(contextual_reasoning.get('causal_relationships', []))}")
            print(f"- Clinical hypotheses: {len(contextual_reasoning.get('clinical_hypotheses', []))}")
        else:
            print(f"\nNo contextual_reasoning found in context")
            
        # Print full response for debugging (truncated)
        print(f"\nFull response (first 1000 chars):")
        print(json.dumps(data, indent=2)[:1000] + "...")
        
    else:
        print(f"API call failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_api_response()