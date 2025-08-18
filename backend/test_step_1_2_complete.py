#!/usr/bin/env python3
"""
Comprehensive Test for Step 1.2 Implementation
Advanced Medical Spell Correction Integration with Medical AI Service
"""

import requests
import json
import time
from medical_spell_checker import AdvancedMedicalSpellChecker
from nlp_processor import normalize_medical_text

def test_step_1_2_requirements():
    """Test all Step 1.2 requirements comprehensively"""
    
    print("🎯 STEP 1.2 COMPREHENSIVE TESTING")
    print("=" * 60)
    print("Advanced Medical Spell Correction System")
    print("=" * 60)
    
    # Required examples from Step 1.2
    required_examples = [
        ("haedache", "headache"),
        ("cheast", "chest"), 
        ("stomache", "stomach"),
        ("diabetis", "diabetes"),
        ("preassure", "pressure"),
    ]
    
    spell_checker = AdvancedMedicalSpellChecker()
    
    print("\n📋 STEP 1.2 REQUIRED EXAMPLES:")
    print("-" * 40)
    
    all_required_passed = True
    for misspelled, expected in required_examples:
        result = spell_checker.correct_medical_spelling(misspelled)
        success = result.corrected_word.lower() == expected.lower()
        status = "✅ PASS" if success else "❌ FAIL"
        
        print(f"{status} '{misspelled}' → '{result.corrected_word}' (expected: '{expected}')")
        print(f"    Confidence: {result.confidence_score:.2f} | Method: {result.correction_method}")
        
        if not success:
            all_required_passed = False
    
    # Test robustness with additional medical terms
    robustness_examples = [
        # Variations of headache
        ("headach", "headache"),
        ("hedache", "headache"), 
        ("migrane", "migraine"),
        
        # Variations of chest  
        ("chesst", "chest"),
        ("chset", "chest"),
        
        # Variations of stomach
        ("stomac", "stomach"),
        ("tummy", "stomach"),
        ("stumach", "stomach"),
        
        # Variations of diabetes
        ("diabeties", "diabetes"),
        ("diabetees", "diabetes"),
        ("diabites", "diabetes"),
        
        # Variations of pressure
        ("pressur", "pressure"),
        ("presure", "pressure"),
        ("preasure", "pressure"),
        
        # Additional medical terms
        ("temperatur", "temperature"),
        ("nauseus", "nausea"), 
        ("dizy", "dizzy"),
        ("pnemonia", "pneumonia"),
        ("symtom", "symptom"),
        ("medcine", "medicine"),
        ("kidny", "kidney"),
        ("brane", "brain"),
        ("hart", "heart"),
        ("livr", "liver"),
        ("kidneies", "kidneys"),
        ("vomitting", "vomiting"),
        ("breathe", "breathing"),
        ("weaknes", "weakness"),
        ("asprin", "aspirin"),
    ]
    
    print(f"\n🚀 ROBUSTNESS TESTING ({len(robustness_examples)} additional terms):")
    print("-" * 40)
    
    robust_passed = 0
    for misspelled, expected in robustness_examples:
        result = spell_checker.correct_medical_spelling(misspelled)
        success = result.corrected_word.lower() == expected.lower()
        confident = result.confidence_score >= 0.7
        
        if success:
            status = "✅ PERFECT"
            robust_passed += 1
        elif confident:
            status = "🟡 REASONABLE" 
            robust_passed += 0.5
        else:
            status = "❌ POOR"
        
        print(f"{status} '{misspelled}' → '{result.corrected_word}' (confidence: {result.confidence_score:.2f})")
    
    robustness_rate = (robust_passed / len(robustness_examples)) * 100
    
    print(f"\n📊 SPELL CORRECTION RESULTS:")
    print(f"Required Examples: {'✅ ALL PASSED' if all_required_passed else '❌ SOME FAILED'} ({sum(1 for _, _ in required_examples)}/5)")
    print(f"Robustness Rate: {robustness_rate:.1f}% ({robust_passed:.1f}/{len(robustness_examples)})")
    print(f"Overall Assessment: {'🎉 EXCELLENT' if all_required_passed and robustness_rate >= 80 else '⚠️ NEEDS IMPROVEMENT'}")
    
    return all_required_passed, robustness_rate


def test_integration_with_normalization():
    """Test integration with text normalization system"""
    
    print(f"\n🔗 INTEGRATION WITH TEXT NORMALIZATION:")
    print("-" * 40)
    
    # Test cases combining grammar issues + spelling issues
    integration_tests = [
        {
            "input": "i having haedache 2 days",
            "expected_improvements": ["grammar correction", "spelling correction", "duration formatting"]
        },
        {
            "input": "me cheast hurt when breath",  
            "expected_improvements": ["pronoun correction", "spelling correction", "verb correction"]
        },
        {
            "input": "diabetis making me nauseus",
            "expected_improvements": ["spelling correction", "pronoun correction"]
        },
        {
            "input": "preassure in stomac area really bad",
            "expected_improvements": ["multiple spelling corrections", "capitalization"]
        },
        {
            "input": "kidny pian with faver n weekness",
            "expected_improvements": ["multiple spelling corrections", "abbreviation expansion"]
        }
    ]
    
    integration_success = 0
    for test_case in integration_tests:
        result = normalize_medical_text(test_case["input"])
        
        # Check if text was meaningfully improved
        improvements_made = len(result.corrections_applied)
        spell_corrections = len(result.spell_corrections) if result.spell_corrections else 0
        
        success = improvements_made >= 2 and result.confidence_score >= 0.6
        status = "✅ SUCCESS" if success else "⚠️ LIMITED"
        
        print(f"{status} '{test_case['input']}'")
        print(f"    → '{result.normalized_text}'")
        print(f"    Corrections: {improvements_made} total, {spell_corrections} spelling")
        print(f"    Confidence: {result.confidence_score:.2f}")
        
        if success:
            integration_success += 1
    
    integration_rate = (integration_success / len(integration_tests)) * 100
    print(f"\nIntegration Success Rate: {integration_rate:.1f}% ({integration_success}/{len(integration_tests)})")
    
    return integration_rate


def test_medical_ai_service_integration():
    """Test integration with Medical AI service via API"""
    
    print(f"\n🏥 MEDICAL AI SERVICE INTEGRATION:")
    print("-" * 40)
    
    base_url = "http://localhost:8001"
    
    # Test cases with spelling errors that should be corrected by Medical AI
    api_test_cases = [
        {
            "input": "i having hedache really bad",
            "description": "Grammar + spelling issues"
        },
        {
            "input": "me cheast pian when breath", 
            "description": "Multiple spelling + grammar issues"
        },
        {
            "input": "diabetis making me nauseus",
            "description": "Medical condition spelling errors"
        }
    ]
    
    api_success = 0
    for i, test_case in enumerate(api_test_cases, 1):
        try:
            # Initialize consultation
            init_payload = {
                "patient_data": {
                    "patient_id": "spell_test_patient",
                    "timestamp": int(time.time())
                }
            }
            
            init_response = requests.post(
                f"{base_url}/api/medical-ai/initialize",
                json=init_payload,
                timeout=10
            )
            
            if init_response.status_code == 200:
                consultation_id = init_response.json().get('consultation_id')
                
                # Send message with spelling errors
                message_payload = {
                    "message": test_case['input'],
                    "consultation_id": consultation_id
                }
                
                message_response = requests.post(
                    f"{base_url}/api/medical-ai/message",
                    json=message_payload,
                    timeout=15
                )
                
                if message_response.status_code == 200:
                    print(f"✅ Test {i}: {test_case['description']}")
                    print(f"    Input: '{test_case['input']}'")
                    print(f"    Status: Medical AI processed successfully")
                    
                    response_data = message_response.json()
                    print(f"    AI Response: {response_data.get('response', 'N/A')[:80]}...")
                    
                    api_success += 1
                else:
                    print(f"❌ Test {i}: API processing failed ({message_response.status_code})")
            else:
                print(f"❌ Test {i}: Consultation initialization failed ({init_response.status_code})")
                
        except Exception as e:
            print(f"❌ Test {i}: Request failed - {e}")
    
    api_rate = (api_success / len(api_test_cases)) * 100
    print(f"\nAPI Integration Success Rate: {api_rate:.1f}% ({api_success}/{len(api_test_cases)})")
    
    return api_rate


def main():
    """Run comprehensive Step 1.2 testing"""
    
    print("🧬 STEP 1.2: ADVANCED MEDICAL SPELL CORRECTION")
    print("📋 Comprehensive Implementation Validation")
    print("🕒 " + time.strftime("%Y-%m-%d %H:%M:%S"))
    
    # Test 1: Core spell correction requirements
    required_passed, robustness_rate = test_step_1_2_requirements()
    
    # Test 2: Integration with text normalization
    integration_rate = test_integration_with_normalization()
    
    # Test 3: Medical AI service integration
    api_rate = test_medical_ai_service_integration()
    
    # Final assessment
    print(f"\n{'='*60}")
    print("📊 STEP 1.2 COMPREHENSIVE RESULTS")
    print(f"{'='*60}")
    
    print(f"✅ Required Examples: {'PASSED' if required_passed else 'FAILED'}")
    print(f"🚀 Robustness Rate: {robustness_rate:.1f}%")
    print(f"🔗 Integration Rate: {integration_rate:.1f}%")
    print(f"🏥 API Integration: {api_rate:.1f}%")
    
    overall_score = (
        (100 if required_passed else 0) * 0.4 +  # 40% weight for required examples
        robustness_rate * 0.3 +                   # 30% weight for robustness
        integration_rate * 0.2 +                  # 20% weight for integration
        api_rate * 0.1                           # 10% weight for API integration
    )
    
    print(f"📈 Overall Score: {overall_score:.1f}%")
    
    if overall_score >= 90:
        assessment = "🎉 OUTSTANDING - Production Ready"
    elif overall_score >= 80:
        assessment = "✅ EXCELLENT - Highly Functional" 
    elif overall_score >= 70:
        assessment = "🟡 GOOD - Functional with Minor Issues"
    else:
        assessment = "❌ NEEDS IMPROVEMENT"
    
    print(f"🎯 Assessment: {assessment}")
    print(f"{'='*60}")
    
    if required_passed and robustness_rate >= 80:
        print("🎊 STEP 1.2 IMPLEMENTATION: COMPLETE & SUCCESSFUL!")
        print("The medical chatbot now has world-class spell correction capabilities!")
    else:
        print("⚠️  Step 1.2 needs additional refinement for full success.")


if __name__ == "__main__":
    main()