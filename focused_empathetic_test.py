#!/usr/bin/env python3
"""
🚀 FOCUSED EMPATHETIC COMMUNICATION TESTING
===========================================

Quick focused test of the empathetic communication endpoints to validate functionality.
"""

import requests
import json
import time
import os
from datetime import datetime

def test_empathetic_endpoints():
    backend_url = "https://medbot-query.preview.emergentagent.com/api"
    
    print("🚀 FOCUSED EMPATHETIC COMMUNICATION TESTING")
    print("=" * 60)
    
    # Test 1: Empathetic Communication Transform
    print("\n1. Testing Empathetic Communication Transform")
    print("-" * 40)
    
    payload1 = {
        "medical_text": "Patient presents with myocardial infarction. Immediate coronary angiography indicated.",
        "patient_anxiety_level": 0.8,
        "communication_style": "emotional",
        "age_group": "adult",
        "is_emergency": True,
        "symptom_severity": "critical"
    }
    
    try:
        response1 = requests.post(
            f"{backend_url}/medical-ai/empathetic-communication-transform",
            json=payload1,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response1.status_code == 200:
            data1 = response1.json()
            print(f"✅ SUCCESS - Empathetic Transform API")
            print(f"   Original: {data1.get('original_text', '')[:50]}...")
            print(f"   Empathetic: {data1.get('empathetic_text', '')[:100]}...")
            print(f"   Empathy Score: {data1.get('empathy_score', 0):.3f}")
            print(f"   Readability Score: {data1.get('readability_score', 0):.3f}")
            print(f"   Transformations: {len(data1.get('transformations_applied', []))}")
        else:
            print(f"❌ FAILED - HTTP {response1.status_code}: {response1.text[:100]}")
            
    except Exception as e:
        print(f"❌ FAILED - Exception: {str(e)}")
    
    # Test 2: Patient-Friendly Explanation
    print("\n2. Testing Patient-Friendly Explanation")
    print("-" * 40)
    
    payload2 = {
        "medical_concepts": ["myocardial_infarction", "coronary_angiography"],
        "patient_context": {
            "anxiety_level": 0.7,
            "communication_style": "emotional",
            "age_group": "adult"
        },
        "explanation_depth": "simple",
        "include_analogies": True
    }
    
    try:
        response2 = requests.post(
            f"{backend_url}/medical-ai/patient-friendly-explanation",
            json=payload2,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"✅ SUCCESS - Patient-Friendly Explanation API")
            print(f"   Concepts Explained: {len(data2.get('explanations', {}))}")
            print(f"   Overall Empathy Score: {data2.get('overall_empathy_score', 0):.3f}")
            explanations = data2.get('explanations', {})
            for concept, explanation in explanations.items():
                print(f"   {concept}: {explanation.get('simple_explanation', '')[:60]}...")
        else:
            print(f"❌ FAILED - HTTP {response2.status_code}: {response2.text[:100]}")
            
    except Exception as e:
        print(f"❌ FAILED - Exception: {str(e)}")
    
    # Test 3: Empathy Metrics
    print("\n3. Testing Empathy Metrics")
    print("-" * 40)
    
    payload3 = {
        "text_samples": [
            "Patient presents with myocardial infarction. Immediate treatment required.",
            "I understand you're experiencing chest pain, and I want you to know we're here to help you through this."
        ],
        "baseline_comparison": "Patient presents with myocardial infarction."
    }
    
    try:
        response3 = requests.post(
            f"{backend_url}/medical-ai/empathy-metrics",
            json=payload3,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response3.status_code == 200:
            data3 = response3.json()
            print(f"✅ SUCCESS - Empathy Metrics API")
            print(f"   Samples Analyzed: {len(data3.get('empathy_scores', []))}")
            print(f"   Average Empathy Score: {data3.get('overall_metrics', {}).get('average_empathy_score', 0):.3f}")
            print(f"   Recommendations: {len(data3.get('recommendations', []))}")
            for i, score in enumerate(data3.get('empathy_scores', [])[:2]):
                print(f"   Sample {i+1} Empathy: {score.get('empathy_score', 0):.3f}")
        else:
            print(f"❌ FAILED - HTTP {response3.status_code}: {response3.text[:100]}")
            
    except Exception as e:
        print(f"❌ FAILED - Exception: {str(e)}")
    
    # Test 4: Enhanced Medical Consultation
    print("\n4. Testing Enhanced Medical Consultation")
    print("-" * 40)
    
    # Initialize consultation first
    init_payload = {
        "patient_id": "empathy_test_patient",
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        init_response = requests.post(
            f"{backend_url}/medical-ai/initialize",
            json=init_payload,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        if init_response.status_code == 200:
            init_data = init_response.json()
            consultation_id = init_data.get('consultation_id')
            
            # Send symptoms message
            message_payload = {
                "consultation_id": consultation_id,
                "message": "I have severe chest pain that started an hour ago, it feels like crushing pressure",
                "patient_context": {
                    "anxiety_level": 0.9,
                    "communication_style": "emotional",
                    "age_group": "adult",
                    "is_emergency": True
                }
            }
            
            message_response = requests.post(
                f"{backend_url}/medical-ai/message",
                json=message_payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if message_response.status_code == 200:
                data4 = message_response.json()
                print(f"✅ SUCCESS - Enhanced Medical Consultation")
                print(f"   Consultation ID: {data4.get('consultation_id', '')}")
                print(f"   Urgency: {data4.get('urgency', '')}")
                print(f"   Response: {data4.get('response', '')[:100]}...")
                
                # Check for empathetic elements
                response_text = data4.get('response', '').lower()
                empathy_indicators = ['understand', 'feel', 'concern', 'support', 'help', 'care', 'worry', 'comfort']
                empathy_count = sum(1 for indicator in empathy_indicators if indicator in response_text)
                print(f"   Empathy Indicators Found: {empathy_count}")
            else:
                print(f"❌ FAILED - Message HTTP {message_response.status_code}: {message_response.text[:100]}")
        else:
            print(f"❌ FAILED - Init HTTP {init_response.status_code}: {init_response.text[:100]}")
            
    except Exception as e:
        print(f"❌ FAILED - Exception: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎉 FOCUSED EMPATHETIC COMMUNICATION TESTING COMPLETE!")

if __name__ == "__main__":
    test_empathetic_endpoints()