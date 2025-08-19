#!/usr/bin/env python3
"""
Focused test to examine the exact responses for intelligent follow-up scenarios
"""

import requests
import json
import os
from datetime import datetime

BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://medpro-testing.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def test_followup_scenarios():
    print("🔍 FOCUSED INTELLIGENT FOLLOW-UP TESTING")
    print("=" * 60)
    
    # Initialize consultation
    print("\n1. Initializing consultation...")
    init_response = requests.post(f"{API_BASE}/medical-ai/initialize",
        json={"patient_id": "anonymous", "timestamp": datetime.now().isoformat()},
        timeout=30
    )
    
    if init_response.status_code != 200:
        print(f"❌ Failed to initialize: {init_response.status_code}")
        return
    
    context = init_response.json().get("context", {})
    conversation_history = []
    
    def send_and_analyze(message, step_name):
        print(f"\n{step_name}")
        print(f"Sending: '{message}'")
        
        response = requests.post(f"{API_BASE}/medical-ai/message",
            json={
                "message": message,
                "context": context,
                "conversation_history": conversation_history
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data.get("response", "")
            
            # Update context
            if "context" in data:
                context.update(data["context"])
            else:
                context.update(data)
            
            # Update conversation history
            conversation_history.extend([
                {"role": "user", "message": message, "timestamp": datetime.now().isoformat()},
                {"role": "assistant", "message": ai_response, "timestamp": datetime.now().isoformat()}
            ])
            
            print(f"AI Response: {ai_response}")
            print(f"Current Stage: {data.get('current_stage', 'unknown')}")
            
            return ai_response
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return ""
    
    # Test the exact conversation flow from the review request
    send_and_analyze("hi", "2. Greeting")
    send_and_analyze("I have a headache", "3. Chief Complaint")
    send_and_analyze("2 days ago", "4. Timing Information")
    
    # Critical test: vague "food" response
    food_response = send_and_analyze("food", "5. CRITICAL: Vague 'food' response")
    
    # Analyze the food response
    print(f"\n🔍 ANALYZING FOOD RESPONSE:")
    print(f"Full response: {food_response}")
    
    food_keywords = [
        "what specific foods", "which foods", "what type of food", 
        "what kind of food", "specific food", "particular food",
        "can you tell me more about how food relates", "how food relates",
        "for example, do", "what foods trigger", "which foods cause",
        "tell me more about", "more about", "more details"
    ]
    
    found_keywords = [kw for kw in food_keywords if kw in food_response.lower()]
    
    if found_keywords:
        print(f"✅ INTELLIGENT FOLLOW-UP DETECTED!")
        print(f"Found keywords: {found_keywords}")
    else:
        print(f"❌ NO INTELLIGENT FOLLOW-UP DETECTED")
        print(f"Response does not contain expected follow-up keywords")
    
    # Continue with detailed response
    send_and_analyze("spicy foods and caffeine", "6. Detailed Food Response")
    
    # Progress through conversation to test surgery follow-up
    print(f"\n🔍 PROGRESSING TO SURGERY TEST...")
    
    # Send several responses to progress
    send_and_analyze("it's throbbing", "7. Quality")
    send_and_analyze("on the right side", "8. Location") 
    send_and_analyze("about 4 hours", "9. Duration")
    send_and_analyze("nothing makes it better", "10. Alleviating factors")
    send_and_analyze("stress makes it worse", "11. Aggravating factors")
    send_and_analyze("no other symptoms", "12. Associated symptoms")
    
    # Test surgery follow-up
    surgery_response = send_and_analyze("surgeries", "13. CRITICAL: Vague 'surgeries' response")
    
    print(f"\n🔍 ANALYZING SURGERY RESPONSE:")
    print(f"Full response: {surgery_response}")
    
    surgery_keywords = [
        "what type of surgery", "which surgery", "what kind of surgery",
        "when was the surgery", "where was the surgery", "surgery details",
        "what surgery", "type of surgery", "tell me more about", "more about",
        "can you provide more details", "more information about", "which surgeries"
    ]
    
    found_surgery_keywords = [kw for kw in surgery_keywords if kw in surgery_response.lower()]
    
    if found_surgery_keywords:
        print(f"✅ INTELLIGENT SURGERY FOLLOW-UP DETECTED!")
        print(f"Found keywords: {found_surgery_keywords}")
    else:
        print(f"❌ NO INTELLIGENT SURGERY FOLLOW-UP DETECTED")
        print(f"Response does not contain expected surgery follow-up keywords")
    
    # Test medication follow-up
    medication_response = send_and_analyze("yes i am taking medications", "14. CRITICAL: Vague medication response")
    
    print(f"\n🔍 ANALYZING MEDICATION RESPONSE:")
    print(f"Full response: {medication_response}")
    
    medication_keywords = [
        "what medications", "which medications", "what type of medication",
        "medication names", "specific medications", "what are you taking",
        "medication details", "name of the medication", "tell me more about",
        "can you provide more details", "more information about", "which ones"
    ]
    
    found_med_keywords = [kw for kw in medication_keywords if kw in medication_response.lower()]
    
    if found_med_keywords:
        print(f"✅ INTELLIGENT MEDICATION FOLLOW-UP DETECTED!")
        print(f"Found keywords: {found_med_keywords}")
    else:
        print(f"❌ NO INTELLIGENT MEDICATION FOLLOW-UP DETECTED")
        print(f"Response does not contain expected medication follow-up keywords")

if __name__ == "__main__":
    test_followup_scenarios()