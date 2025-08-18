#!/usr/bin/env python3
"""
Simple test for cardiac scenario
"""

import requests
import json
import os
from datetime import datetime

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://medical-validation.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def test_cardiac_scenario():
    """Test cardiac scenario specifically"""
    
    # Initialize consultation
    print("Initializing consultation...")
    init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
        json={
            "patient_id": "cardiac-test",
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
    
    # Test cardiac scenario
    scenario_text = "I get this crushing chest pain whenever I walk uphill or climb more than one flight of stairs, feels like an elephant sitting on my chest, but it completely goes away within 2-3 minutes of resting."
    
    print(f"\nTesting cardiac scenario...")
    
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
        
        print(f"✅ API Response received")
        print(f"- Urgency: {data.get('urgency')}")
        print(f"- Emergency detected: {data.get('emergency_detected')}")
        
        # Check contextual fields
        causal_relationships = data.get('causal_relationships', [])
        clinical_hypotheses = data.get('clinical_hypotheses', [])
        contextual_factors = data.get('contextual_factors', {})
        context_based_recommendations = data.get('context_based_recommendations', [])
        trigger_avoidance_strategies = data.get('trigger_avoidance_strategies', [])
        specialist_referral_context = data.get('specialist_referral_context')
        
        print(f"\n📊 CONTEXTUAL ANALYSIS RESULTS:")
        print(f"- Causal relationships: {len(causal_relationships)} items")
        print(f"- Clinical hypotheses: {len(clinical_hypotheses)} items")
        print(f"- Contextual factors: {len(contextual_factors)} keys")
        print(f"- Context-based recommendations: {len(context_based_recommendations)} items")
        print(f"- Trigger avoidance strategies: {len(trigger_avoidance_strategies)} items")
        print(f"- Specialist referral context: {'Present' if specialist_referral_context else 'None'}")
        
        # Check for enhanced cardiac analysis
        has_enhanced_cardiac = any('Enhanced Cardiac Analysis' in str(hyp) for hyp in clinical_hypotheses)
        has_exertional_trigger = any('exertion' in str(rel).lower() or 'stairs' in str(rel).lower() 
                                   for rel in causal_relationships)
        has_emergency_protocols = any('911' in str(rec) or 'CRITICAL' in str(rec) 
                                    for rec in context_based_recommendations)
        
        print(f"\n🔍 ENHANCED FEATURES VALIDATION:")
        print(f"- Enhanced cardiac analysis: {'✅ FOUND' if has_enhanced_cardiac else '❌ MISSING'}")
        print(f"- Exertional trigger detected: {'✅ FOUND' if has_exertional_trigger else '❌ MISSING'}")
        print(f"- Emergency protocols: {'✅ FOUND' if has_emergency_protocols else '❌ MISSING'}")
        
        if causal_relationships:
            print(f"\n📋 FIRST CAUSAL RELATIONSHIP:")
            print(f"   {causal_relationships[0]}")
            
        if clinical_hypotheses:
            print(f"\n🧠 FIRST CLINICAL HYPOTHESIS:")
            print(f"   {clinical_hypotheses[0]}")
            
        if context_based_recommendations:
            print(f"\n💡 FIRST RECOMMENDATION:")
            print(f"   {context_based_recommendations[0]}")
        
        # Overall assessment
        all_fields_populated = all([
            len(causal_relationships) > 0,
            len(clinical_hypotheses) > 0,
            len(contextual_factors) > 0,
            len(context_based_recommendations) > 0,
            len(trigger_avoidance_strategies) > 0,
            specialist_referral_context is not None
        ])
        
        print(f"\n🎯 OVERALL ASSESSMENT:")
        print(f"- All contextual fields populated: {'✅ PASS' if all_fields_populated else '❌ FAIL'}")
        print(f"- Enhanced cardiac features: {'✅ PASS' if has_enhanced_cardiac else '❌ FAIL'}")
        print(f"- Emergency detection: {'✅ PASS' if data.get('urgency') == 'emergency' else '❌ FAIL'}")
        
        success = all_fields_populated and has_enhanced_cardiac and data.get('urgency') == 'emergency'
        print(f"- Scenario 2 SUCCESS: {'✅ PASS' if success else '❌ FAIL'}")
        
    else:
        print(f"❌ API call failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_cardiac_scenario()