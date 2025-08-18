#!/usr/bin/env python3
"""
Step 1.3 Colloquial Medical Expression Handler - Comprehensive Testing
Task: Handle informal/colloquial medical expressions with robust conversion to medical standards

This test file validates that Task 1.3 implementation can handle:
- The 5 core required examples
- Many additional colloquial expressions beyond the basic examples
- Complex compound expressions
- Real-world patient language variations
"""

import sys
import os
sys.path.append('/app/backend')

from nlp_processor import IntelligentTextNormalizer

def test_step_1_3_core_requirements():
    """Test the specific Step 1.3 core requirements"""
    
    normalizer = IntelligentTextNormalizer()
    
    # The 5 core required examples from Task 1.3
    core_test_cases = [
        {"input": "tummy hurt", "expected_contains": "abdominal pain"},
        {"input": "feeling crappy", "expected_contains": "feeling unwell"},
        {"input": "can't poop", "expected_contains": "experiencing constipation"},
        {"input": "throwing up", "expected_contains": "vomiting"},
        {"input": "dizzy spells", "expected_contains": "episodes of dizziness"},
    ]
    
    print("🎯 STEP 1.3 CORE REQUIREMENTS TEST")
    print("=" * 50)
    
    successful_core = 0
    
    for i, test in enumerate(core_test_cases, 1):
        result = normalizer.normalize_medical_text(test["input"])
        success = test["expected_contains"].lower() in result.normalized_text.lower()
        
        print(f"{i}. Input: '{test['input']}'")
        print(f"   Expected: should contain '{test['expected_contains']}'")
        print(f"   Output: '{result.normalized_text}'")
        print(f"   ✅ SUCCESS: {success}")
        
        # Show colloquial corrections applied
        colloquial_corrections = [c for c in result.corrections_applied 
                                if 'Colloquial' in c or 'colloquial' in c]
        if colloquial_corrections:
            print(f"   Colloquial Corrections: {colloquial_corrections}")
        
        print()
        
        if success:
            successful_core += 1
    
    core_success_rate = (successful_core / len(core_test_cases)) * 100
    print(f"📊 CORE REQUIREMENTS RESULTS: {successful_core}/{len(core_test_cases)} ({core_success_rate:.1f}%)")
    
    return successful_core, len(core_test_cases)


def test_step_1_3_robustness():
    """Test robustness beyond core requirements - demonstrating 'super coding power and intelligence'"""
    
    normalizer = IntelligentTextNormalizer()
    
    # Extended test cases demonstrating robustness
    robustness_test_cases = [
        # Digestive variations
        {"input": "belly really hurts", "expected_contains": "abdominal pain"},
        {"input": "gut pain", "expected_contains": "abdominal pain"},
        {"input": "tummy ache", "expected_contains": "abdominal pain"},
        
        # Bowel movement variations
        {"input": "cant poop", "expected_contains": "experiencing constipation"},
        {"input": "cannot poop", "expected_contains": "experiencing constipation"},
        {"input": "trouble pooping", "expected_contains": "difficulty with bowel movements"},
        {"input": "backed up", "expected_contains": "experiencing constipation"},
        {"input": "the runs", "expected_contains": "experiencing diarrhea"},
        
        # Nausea variations
        {"input": "puking", "expected_contains": "vomiting"},
        {"input": "feeling sick", "expected_contains": "experiencing nausea"},
        {"input": "queasy", "expected_contains": "nauseous"},
        {"input": "gonna be sick", "expected_contains": "feeling nauseous"},
        
        # Feeling unwell variations
        {"input": "feel awful", "expected_contains": "feel unwell"},
        {"input": "feeling lousy", "expected_contains": "feeling unwell"},
        {"input": "under the weather", "expected_contains": "feeling unwell"},
        {"input": "not feeling good", "expected_contains": "feeling unwell"},
        
        # Dizziness variations
        {"input": "head spinning", "expected_contains": "experiencing dizziness"},
        {"input": "lightheaded", "expected_contains": "experiencing lightheadedness"},
        {"input": "woozy", "expected_contains": "dizzy"},
        {"input": "room spinning", "expected_contains": "experiencing vertigo"},
        
        # Pain descriptors
        {"input": "terrible pain", "expected_contains": "severe pain"},
        {"input": "killing me", "expected_contains": "severe pain"},
        {"input": "stabbing pain", "expected_contains": "sharp stabbing pain"},
        
        # Breathing
        {"input": "can't breathe", "expected_contains": "difficulty breathing"},
        {"input": "short of breath", "expected_contains": "experiencing shortness of breath"},
        {"input": "wheezing", "expected_contains": "experiencing wheezing"},
        
        # Fatigue
        {"input": "wiped out", "expected_contains": "extremely fatigued"},
        {"input": "dead tired", "expected_contains": "extremely fatigued"},
        {"input": "no energy", "expected_contains": "experiencing fatigue"},
    ]
    
    print("\n🚀 STEP 1.3 ROBUSTNESS TEST - Beyond Core Requirements")
    print("=" * 60)
    
    successful_robust = 0
    
    for i, test in enumerate(robustness_test_cases, 1):
        result = normalizer.normalize_medical_text(test["input"])
        success = test["expected_contains"].lower() in result.normalized_text.lower()
        
        if success:
            successful_robust += 1
            print(f"✅ {i:2d}. '{test['input']}' → '{result.normalized_text}'")
        else:
            print(f"❌ {i:2d}. '{test['input']}' → '{result.normalized_text}' (expected: {test['expected_contains']})")
    
    robust_success_rate = (successful_robust / len(robustness_test_cases)) * 100
    print(f"\n📊 ROBUSTNESS RESULTS: {successful_robust}/{len(robustness_test_cases)} ({robust_success_rate:.1f}%)")
    
    return successful_robust, len(robustness_test_cases)


def test_step_1_3_compound_expressions():
    """Test complex compound colloquial expressions"""
    
    normalizer = IntelligentTextNormalizer()
    
    compound_test_cases = [
        {"input": "tummy hurt and throwing up", "expected": ["abdominal pain", "vomiting"]},
        {"input": "feeling crappy with dizzy spells", "expected": ["feeling unwell", "episodes of dizziness"]},
        {"input": "can't poop and belly ache", "expected": ["experiencing constipation", "abdominal pain"]},
        {"input": "head spinning and gonna be sick", "expected": ["experiencing dizziness", "feeling nauseous"]},
        {"input": "wiped out and can't breathe", "expected": ["extremely fatigued", "difficulty breathing"]},
    ]
    
    print("\n🔬 STEP 1.3 COMPOUND EXPRESSIONS TEST")
    print("=" * 50)
    
    successful_compound = 0
    
    for i, test in enumerate(compound_test_cases, 1):
        result = normalizer.normalize_medical_text(test["input"])
        
        # Check if all expected terms are present
        all_present = all(expected.lower() in result.normalized_text.lower() 
                         for expected in test["expected"])
        
        print(f"{i}. Input: '{test['input']}'")
        print(f"   Expected: {test['expected']}")
        print(f"   Output: '{result.normalized_text}'")
        print(f"   ✅ All Terms Present: {all_present}")
        
        if all_present:
            successful_compound += 1
        
        # Show compound corrections
        compound_corrections = [c for c in result.corrections_applied 
                              if 'Compound' in c or 'compound' in c]
        if compound_corrections:
            print(f"   Compound Corrections: {compound_corrections}")
        
        print()
    
    compound_success_rate = (successful_compound / len(compound_test_cases)) * 100
    print(f"📊 COMPOUND EXPRESSIONS RESULTS: {successful_compound}/{len(compound_test_cases)} ({compound_success_rate:.1f}%)")
    
    return successful_compound, len(compound_test_cases)


def test_step_1_3_integration_with_medical_ai():
    """Test Step 1.3 integration with existing medical AI system"""
    
    # Test cases that combine Step 1.1, 1.2, and 1.3 features
    integration_test_cases = [
        {
            "input": "i having tummy hurt 2 days",
            "expected_grammar": True,  # Should fix "i having"
            "expected_colloquial": "abdominal pain",  # Should convert "tummy hurt"
            "expected_duration": "2 days"  # Should preserve medical info
        },
        {
            "input": "me chest hurt when breath and feeling crappy",
            "expected_grammar": True,  # Should fix "me chest hurt when breath"
            "expected_colloquial": "feeling unwell",  # Should convert "feeling crappy"
        },
        {
            "input": "haedache really bad and dizzy spells",
            "expected_spelling": "headache",  # Should fix spelling
            "expected_colloquial": "episodes of dizziness",  # Should convert "dizzy spells"
        }
    ]
    
    normalizer = IntelligentTextNormalizer()
    
    print("\n🔗 STEP 1.3 INTEGRATION TEST with Steps 1.1 & 1.2")
    print("=" * 55)
    
    successful_integration = 0
    
    for i, test in enumerate(integration_test_cases, 1):
        result = normalizer.normalize_medical_text(test["input"])
        
        # Check different aspects
        checks_passed = 0
        total_checks = 0
        
        print(f"{i}. Input: '{test['input']}'")
        print(f"   Output: '{result.normalized_text}'")
        
        if "expected_grammar" in test:
            grammar_fixed = any("Grammar" in c for c in result.corrections_applied)
            print(f"   ✅ Grammar Fixed: {grammar_fixed}")
            total_checks += 1
            if grammar_fixed:
                checks_passed += 1
                
        if "expected_colloquial" in test:
            colloquial_present = test["expected_colloquial"].lower() in result.normalized_text.lower()
            print(f"   ✅ Colloquial Converted: {colloquial_present} (expected: '{test['expected_colloquial']}')")
            total_checks += 1
            if colloquial_present:
                checks_passed += 1
                
        if "expected_spelling" in test:
            spelling_present = test["expected_spelling"].lower() in result.normalized_text.lower()
            print(f"   ✅ Spelling Fixed: {spelling_present} (expected: '{test['expected_spelling']}')")
            total_checks += 1
            if spelling_present:
                checks_passed += 1
                
        if "expected_duration" in test:
            duration_present = test["expected_duration"] in result.normalized_text
            print(f"   ✅ Duration Preserved: {duration_present}")
            total_checks += 1
            if duration_present:
                checks_passed += 1
        
        # Show all corrections applied
        print(f"   All Corrections: {result.corrections_applied}")
        
        success = checks_passed == total_checks
        if success:
            successful_integration += 1
        
        print(f"   📊 Integration Success: {checks_passed}/{total_checks} checks passed")
        print()
    
    integration_success_rate = (successful_integration / len(integration_test_cases)) * 100
    print(f"📊 INTEGRATION RESULTS: {successful_integration}/{len(integration_test_cases)} ({integration_success_rate:.1f}%)")
    
    return successful_integration, len(integration_test_cases)


def main():
    """Run comprehensive Step 1.3 testing suite"""
    
    print("🚀 STEP 1.3 COMPREHENSIVE TEST SUITE")
    print("Task: Handle informal/colloquial medical expressions")
    print("Goal: Robust conversion beyond the 4 basic examples")
    print("=" * 70)
    
    # Run all test suites
    core_success, core_total = test_step_1_3_core_requirements()
    robust_success, robust_total = test_step_1_3_robustness()
    compound_success, compound_total = test_step_1_3_compound_expressions()
    integration_success, integration_total = test_step_1_3_integration_with_medical_ai()
    
    # Calculate overall results
    total_success = core_success + robust_success + compound_success + integration_success
    total_tests = core_total + robust_total + compound_total + integration_total
    overall_success_rate = (total_success / total_tests) * 100
    
    print("\n" + "="*70)
    print("🎯 FINAL STEP 1.3 IMPLEMENTATION RESULTS")
    print("="*70)
    print(f"Core Requirements:    {core_success:2d}/{core_total:2d} ({core_success/core_total*100:5.1f}%)")
    print(f"Robustness Test:      {robust_success:2d}/{robust_total:2d} ({robust_success/robust_total*100:5.1f}%)")
    print(f"Compound Expressions: {compound_success:2d}/{compound_total:2d} ({compound_success/compound_total*100:5.1f}%)")
    print(f"Integration Test:     {integration_success:2d}/{integration_total:2d} ({integration_success/integration_total*100:5.1f}%)")
    print("-" * 70)
    print(f"OVERALL SUCCESS:      {total_success:2d}/{total_tests:2d} ({overall_success_rate:5.1f}%)")
    
    if overall_success_rate >= 85:
        print("\n✅ TASK 1.3 IMPLEMENTATION: SUCCESS!")
        print("🎉 Robust colloquial medical expression handling achieved!")
        print("💪 'Super coding power and intelligence' demonstrated with comprehensive coverage!")
    elif overall_success_rate >= 70:
        print("\n⚠️  TASK 1.3 IMPLEMENTATION: GOOD but could be improved")
        print("Some edge cases may need refinement")
    else:
        print("\n❌ TASK 1.3 IMPLEMENTATION: Needs significant improvement")
    
    return overall_success_rate >= 85


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)