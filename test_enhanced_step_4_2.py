#!/usr/bin/env python3
"""
Test Enhanced Step 4.2 Intelligent Follow-up Question Generation System
"""

import requests
import json
from datetime import datetime

BACKEND_URL = "https://ai-test-suite.preview.emergentagent.com/api"

def test_enhanced_step_4_2():
    """Test the enhanced Step 4.2 system with proper context handling"""
    
    print("🧠 Testing Enhanced Step 4.2 Intelligent Follow-up Question Generation System")
    print("=" * 80)
    
    # Step 1: Initialize consultation
    print("1. Initializing consultation...")
    init_response = requests.post(
        f"{BACKEND_URL}/medical-ai/initialize",
        json={"patient_id": "test_step42", "timestamp": datetime.now().isoformat()}
    )
    
    if init_response.status_code != 200:
        print(f"❌ Initialization failed: {init_response.status_code}")
        return False
    
    init_data = init_response.json()
    consultation_id = init_data['context']['consultation_id']
    print(f"✅ Consultation initialized: {consultation_id}")
    
    # Step 2: Establish context with chest pain (should trigger enhanced pain analysis)
    print("\n2. Testing enhanced pain description analysis...")
    message_data = {
        "message": "chest pain",
        "consultation_id": consultation_id,
        "patient_id": "test_step42",
        "context": init_data['context']
    }
    
    response = requests.post(
        f"{BACKEND_URL}/medical-ai/message",
        json=message_data
    )
    
    if response.status_code != 200:
        print(f"❌ Message failed: {response.status_code}")
        return False
    
    response_data = response.json()
    response_text = response_data['response'].lower()
    
    print(f"Response: {response_data['response'][:200]}...")
    print(f"Stage: {response_data.get('stage')}")
    print(f"Consultation ID: {response_data['context']['consultation_id']}")
    
    # Check for enhanced pain follow-up indicators
    pain_followup_keywords = [
        "what does it feel like", "describe", "quality", "crushing", "pressure", 
        "sharp", "dull", "burning", "severity", "scale", "1 to 10"
    ]
    
    has_enhanced_followup = any(keyword in response_text for keyword in pain_followup_keywords)
    
    if has_enhanced_followup:
        print("✅ Enhanced pain follow-up detected!")
        return True
    else:
        print("❌ Enhanced pain follow-up NOT detected")
        print(f"Looking for keywords: {pain_followup_keywords}")
        return False

def test_temporal_vagueness():
    """Test enhanced temporal vagueness detection"""
    
    print("\n3. Testing enhanced temporal vagueness detection...")
    
    # Initialize new consultation
    init_response = requests.post(
        f"{BACKEND_URL}/medical-ai/initialize",
        json={"patient_id": "test_temporal", "timestamp": datetime.now().isoformat()}
    )
    
    init_data = init_response.json()
    consultation_id = init_data['context']['consultation_id']
    
    # Establish context with headache
    context_message = {
        "message": "I have a headache",
        "consultation_id": consultation_id,
        "patient_id": "test_temporal", 
        "context": init_data['context']
    }
    
    context_response = requests.post(
        f"{BACKEND_URL}/medical-ai/message",
        json=context_message
    )
    
    context_data = context_response.json()
    print(f"Context established. Stage: {context_data.get('stage')}")
    
    # Test temporal vagueness with "recently"
    temporal_message = {
        "message": "recently",
        "consultation_id": consultation_id,
        "patient_id": "test_temporal",
        "context": context_data['context']
    }
    
    temporal_response = requests.post(
        f"{BACKEND_URL}/medical-ai/message",
        json=temporal_message
    )
    
    temporal_data = temporal_response.json()
    response_text = temporal_data['response'].lower()
    
    print(f"Temporal Response: {temporal_data['response'][:200]}...")
    
    # Check for enhanced temporal clarification
    temporal_keywords = [
        "when you say", "more specific", "timing", "hours ago", "days ago", 
        "weeks ago", "sudden", "gradual", "exactly when"
    ]
    
    has_temporal_clarification = any(keyword in response_text for keyword in temporal_keywords)
    
    if has_temporal_clarification:
        print("✅ Enhanced temporal clarification detected!")
        return True
    else:
        print("❌ Enhanced temporal clarification NOT detected")
        print(f"Looking for keywords: {temporal_keywords}")
        return False

if __name__ == "__main__":
    pain_test = test_enhanced_step_4_2()
    temporal_test = test_temporal_vagueness()
    
    print("\n" + "=" * 80)
    print("ENHANCED STEP 4.2 TEST RESULTS:")
    print(f"Pain Description Enhancement: {'✅ PASS' if pain_test else '❌ FAIL'}")
    print(f"Temporal Vagueness Enhancement: {'✅ PASS' if temporal_test else '❌ FAIL'}")
    
    if pain_test and temporal_test:
        print("\n🎉 Enhanced Step 4.2 System is WORKING!")
    else:
        print("\n⚠️  Enhanced Step 4.2 System needs debugging")