#!/usr/bin/env python3
"""
Debug script to test contextual extraction directly
"""

import sys
import os
sys.path.append('/app/backend')

from medical_ai_service import AdvancedSymptomRecognizer

def test_contextual_extraction():
    """Test contextual extraction with the ultra-challenging scenarios"""
    
    recognizer = AdvancedSymptomRecognizer()
    
    scenarios = [
        {
            "name": "Scenario 1 - Orthostatic",
            "text": "Every morning when I get out of bed I feel dizzy and nauseous, sometimes I even feel like I'm going to faint, but it goes away after I sit back down for a few minutes."
        },
        {
            "name": "Scenario 2 - Enhanced Cardiac", 
            "text": "I get this crushing chest pain whenever I walk uphill or climb more than one flight of stairs, feels like an elephant sitting on my chest, but it completely goes away within 2-3 minutes of resting."
        },
        {
            "name": "Scenario 3 - Stress-Dietary",
            "text": "I've noticed that I get really bad stomach cramps and loose stools about 30-60 minutes after eating ice cream or drinking milk, but only when I'm stressed out at work."
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{'='*60}")
        print(f"TESTING: {scenario['name']}")
        print(f"{'='*60}")
        print(f"Input: {scenario['text']}")
        print()
        
        try:
            # Extract medical entities
            result = recognizer.extract_medical_entities(scenario['text'])
            
            print("EXTRACTION RESULT:")
            print(f"- Entities found: {len(result.get('entities', {}).get('symptoms', []))}")
            print(f"- Overall confidence: {result.get('overall_confidence', 0.0)}")
            
            # Check contextual reasoning
            contextual_reasoning = result.get('contextual_reasoning', {})
            print(f"\nCONTEXTUAL REASONING:")
            print(f"- Causal relationships: {len(contextual_reasoning.get('causal_relationships', []))}")
            print(f"- Clinical hypotheses: {len(contextual_reasoning.get('clinical_hypotheses', []))}")
            print(f"- Contextual factors: {contextual_reasoning.get('contextual_factors', {})}")
            print(f"- Context-based recommendations: {len(contextual_reasoning.get('context_based_recommendations', []))}")
            print(f"- Trigger avoidance strategies: {len(contextual_reasoning.get('trigger_avoidance_strategies', []))}")
            print(f"- Specialist referral context: {contextual_reasoning.get('specialist_referral_context', 'None')}")
            
            # Print details if available
            if contextual_reasoning.get('causal_relationships'):
                print(f"\nCAUSAL RELATIONSHIPS:")
                for i, rel in enumerate(contextual_reasoning['causal_relationships'][:3]):
                    print(f"  {i+1}. {rel}")
            
            if contextual_reasoning.get('clinical_hypotheses'):
                print(f"\nCLINICAL HYPOTHESES:")
                for i, hyp in enumerate(contextual_reasoning['clinical_hypotheses'][:3]):
                    print(f"  {i+1}. {hyp}")
                    
        except Exception as e:
            print(f"ERROR: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_contextual_extraction()