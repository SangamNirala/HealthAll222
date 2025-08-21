#!/usr/bin/env python3
"""
🎯 STEP 4.1 CONVERSATION CONTEXT TESTING
Test the ConversationContext implementation for Step 4.1 requirements

This test validates that the ConversationContext class meets the exact specifications:
- symptom_history = []
- patient_demographics = {}  
- previous_responses = []
- medical_context = {}
- conversation_stage = "initial"
"""

import sys
import os
sys.path.append('/app/backend')

from conversation_context import ConversationContext, ConversationContextManager, conversation_manager
from datetime import datetime
import json


def test_step_4_1_core_specifications():
    """Test the core Step 4.1 specifications exactly as requested"""
    
    print("🎯 TESTING STEP 4.1 CORE SPECIFICATIONS")
    print("=" * 60)
    
    # Test 1: Create ConversationContext with default values
    print("1. Testing ConversationContext creation with Step 4.1 defaults...")
    
    context = ConversationContext()
    
    # Verify exact Step 4.1 specifications
    assert context.symptom_history == [], f"symptom_history should be [], got {context.symptom_history}"
    assert context.patient_demographics == {}, f"patient_demographics should be {{}}, got {context.patient_demographics}"
    assert context.previous_responses == [], f"previous_responses should be [], got {context.previous_responses}"
    assert context.medical_context == {}, f"medical_context should be {{}}, got {context.medical_context}"
    assert context.conversation_stage == "initial", f"conversation_stage should be 'initial', got {context.conversation_stage}"
    
    print("   ✅ All Step 4.1 core specifications verified!")
    
    # Test 2: Test symptom_history functionality
    print("2. Testing symptom_history management...")
    
    sample_symptom = {
        "name": "headache",
        "description": "throbbing pain in temples",
        "severity": 7,
        "onset": "2 hours ago",
        "duration": "ongoing"
    }
    
    context.add_symptom_to_history(sample_symptom)
    
    assert len(context.symptom_history) == 1, f"Expected 1 symptom, got {len(context.symptom_history)}"
    assert context.symptom_history[0]["symptom_data"] == sample_symptom
    
    print("   ✅ symptom_history functionality working correctly!")
    
    # Test 3: Test patient_demographics functionality  
    print("3. Testing patient_demographics management...")
    
    sample_demographics = {
        "age": 35,
        "gender": "female",
        "medical_history": ["hypertension"],
        "allergies": ["penicillin"]
    }
    
    context.update_patient_demographics(sample_demographics)
    
    assert context.patient_demographics == sample_demographics
    
    print("   ✅ patient_demographics functionality working correctly!")
    
    # Test 4: Test previous_responses functionality
    print("4. Testing previous_responses management...")
    
    sample_response = {
        "content": "I understand you have a headache. Can you tell me more about when it started?",
        "type": "clarifying_question",
        "confidence": 0.85,
        "reasoning": "Gathering temporal information for headache assessment"
    }
    
    context.add_response_to_history(sample_response)
    
    assert len(context.previous_responses) == 1, f"Expected 1 response, got {len(context.previous_responses)}"
    assert context.previous_responses[0]["response_data"] == sample_response
    
    print("   ✅ previous_responses functionality working correctly!")
    
    # Test 5: Test medical_context functionality
    print("5. Testing medical_context management...")
    
    sample_medical_context = {
        "chief_complaint": "headache",
        "current_medications": ["ibuprofen"],
        "risk_factors": ["stress", "lack of sleep"],
        "vital_signs": {"bp": "120/80", "hr": 72}
    }
    
    context.update_medical_context(sample_medical_context)
    
    assert context.medical_context == sample_medical_context
    
    print("   ✅ medical_context functionality working correctly!")
    
    # Test 6: Test conversation_stage management
    print("6. Testing conversation_stage advancement...")
    
    assert context.conversation_stage == "initial"
    
    context.advance_conversation_stage("symptom_gathering")
    assert context.conversation_stage == "symptom_gathering"
    
    context.advance_conversation_stage("detailed_assessment")
    assert context.conversation_stage == "detailed_assessment"
    
    print("   ✅ conversation_stage functionality working correctly!")
    
    print("\n🎉 ALL STEP 4.1 CORE SPECIFICATIONS PASSED!")
    return True


def test_enhanced_functionality():
    """Test enhanced functionality beyond Step 4.1 core requirements"""
    
    print("\n🚀 TESTING ENHANCED CONVERSATION CONTEXT FUNCTIONALITY")
    print("=" * 60)
    
    # Test conversation summary
    print("1. Testing conversation summary generation...")
    
    context = ConversationContext()
    context.increment_turn()
    context.increment_turn()
    
    # Add some test data
    context.add_symptom_to_history({
        "name": "chest pain",
        "severity": 8
    })
    
    context.add_response_to_history({
        "content": "This sounds concerning. Let me ask about the chest pain.",
        "type": "assessment"
    })
    
    summary = context.get_conversation_summary()
    
    assert summary["current_stage"] == "initial"
    assert summary["total_turns"] == 2
    assert summary["symptoms_discussed"] == 1
    assert summary["responses_generated"] == 1
    
    print("   ✅ Conversation summary generation working!")
    
    # Test conversation search
    print("2. Testing conversation history search...")
    
    search_results = context.search_conversation_history("chest pain")
    assert len(search_results) > 0, "Should find chest pain in conversation history"
    
    print("   ✅ Conversation search functionality working!")
    
    # Test serialization/deserialization
    print("3. Testing context serialization...")
    
    context_dict = context.to_dict()
    restored_context = ConversationContext.from_dict(context_dict)
    
    assert restored_context.conversation_stage == context.conversation_stage
    assert restored_context.total_turns == context.total_turns
    assert len(restored_context.symptom_history) == len(context.symptom_history)
    
    print("   ✅ Serialization/deserialization working!")
    
    print("\n🎉 ALL ENHANCED FUNCTIONALITY TESTS PASSED!")
    return True


def test_conversation_manager():
    """Test the ConversationContextManager functionality"""
    
    print("\n🔧 TESTING CONVERSATION CONTEXT MANAGER")
    print("=" * 60)
    
    manager = ConversationContextManager()
    
    # Test context creation
    print("1. Testing context creation and retrieval...")
    
    context1 = manager.create_context("patient_123")
    context2 = manager.create_context("patient_456")
    
    assert context1.patient_id == "patient_123"
    assert context2.patient_id == "patient_456"
    
    # Test retrieval
    retrieved_context1 = manager.get_context(context1.conversation_id)
    assert retrieved_context1 == context1
    
    print("   ✅ Context creation and retrieval working!")
    
    # Test patient-specific context retrieval
    print("2. Testing patient-specific context retrieval...")
    
    patient_contexts = manager.get_contexts_by_patient("patient_123")
    assert len(patient_contexts) == 1
    assert patient_contexts[0].patient_id == "patient_123"
    
    print("   ✅ Patient-specific retrieval working!")
    
    # Test context removal
    print("3. Testing context removal...")
    
    removed = manager.remove_context(context1.conversation_id)
    assert removed == True
    
    retrieved_again = manager.get_context(context1.conversation_id)
    assert retrieved_again is None
    
    print("   ✅ Context removal working!")
    
    print("\n🎉 ALL CONVERSATION MANAGER TESTS PASSED!")
    return True


def test_integration_with_medical_ai():
    """Test how ConversationContext integrates with existing medical AI system"""
    
    print("\n🩺 TESTING INTEGRATION WITH MEDICAL AI SYSTEM")
    print("=" * 60)
    
    # Create a context that simulates medical AI integration
    context = ConversationContext(patient_id="test_patient")
    
    # Simulate a medical conversation flow
    print("1. Simulating medical conversation flow...")
    
    # Stage 1: Initial greeting
    context.advance_conversation_stage("greeting")
    context.add_response_to_history({
        "content": "Hello! I'm here to help with your health concerns. What brings you in today?",
        "type": "greeting",
        "confidence": 0.95
    })
    context.increment_turn()
    
    # Stage 2: Symptom gathering
    context.advance_conversation_stage("symptom_gathering")
    context.add_symptom_to_history({
        "name": "headache",
        "description": "severe throbbing pain",
        "location": "temples",
        "severity": 8,
        "onset": "this morning"
    })
    context.increment_turn()
    
    # Stage 3: Detailed assessment
    context.advance_conversation_stage("detailed_assessment")
    context.update_medical_context({
        "chief_complaint": "severe headache",
        "hpi_elements": {
            "onset": "this morning",
            "location": "bilateral temples",
            "quality": "throbbing",
            "severity": "8/10"
        }
    })
    context.increment_turn()
    
    # Test AI context generation
    ai_context = context.get_conversation_context_for_ai()
    
    assert ai_context["conversation_stage"] == "detailed_assessment"
    assert ai_context["total_turns"] == 3
    assert len(ai_context["recent_symptoms"]) > 0
    assert "chief_complaint" in ai_context["medical_context"]
    
    print("   ✅ Medical AI integration context generation working!")
    
    # Test conversation memory for AI
    print("2. Testing conversation memory for AI processing...")
    
    memory = ai_context["key_conversation_memory"]
    assert "headache" in memory["symptoms_mentioned"]
    
    print("   ✅ Conversation memory for AI working!")
    
    # Test context confidence scoring
    print("3. Testing context confidence scoring...")
    
    context.update_context_confidence(0.87)
    updated_ai_context = context.get_conversation_context_for_ai()
    
    assert updated_ai_context["session_metadata"]["confidence_score"] == 0.87
    
    print("   ✅ Context confidence scoring working!")
    
    print("\n🎉 ALL MEDICAL AI INTEGRATION TESTS PASSED!")
    return True


def main():
    """Run all Step 4.1 ConversationContext tests"""
    
    print("🎯 STEP 4.1: CONVERSATION MEMORY AND CONTEXT TRACKING - COMPREHENSIVE TESTING")
    print("=" * 80)
    print("Testing ConversationContext implementation as specified in Step 4.1")
    print("Core requirements: symptom_history, patient_demographics, previous_responses,")
    print("medical_context, conversation_stage")
    print("=" * 80)
    
    try:
        # Test core Step 4.1 specifications
        test_step_4_1_core_specifications()
        
        # Test enhanced functionality
        test_enhanced_functionality()
        
        # Test conversation manager
        test_conversation_manager()
        
        # Test integration with medical AI
        test_integration_with_medical_ai()
        
        print("\n" + "=" * 80)
        print("🎉 STEP 4.1 IMPLEMENTATION COMPLETE AND FULLY TESTED!")
        print("✅ All core specifications implemented correctly")
        print("✅ Enhanced functionality working properly") 
        print("✅ ConversationContextManager operational")
        print("✅ Medical AI integration ready")
        print("=" * 80)
        
        # Display example usage
        print("\n📋 EXAMPLE USAGE:")
        print("-" * 40)
        
        example_context = ConversationContext()
        
        print("# Create new conversation context")
        print(f"context = ConversationContext()")
        print(f"# Initial state: {example_context.conversation_stage}")
        
        print("\n# Add symptom to history")  
        example_context.add_symptom_to_history({"name": "headache", "severity": 7})
        print(f"context.add_symptom_to_history({{'name': 'headache', 'severity': 7}})")
        print(f"# Symptoms tracked: {len(example_context.symptom_history)}")
        
        print("\n# Update demographics")
        example_context.update_patient_demographics({"age": 30, "gender": "female"})
        print(f"context.update_patient_demographics({{'age': 30, 'gender': 'female'}})")
        print(f"# Demographics: {example_context.patient_demographics}")
        
        print("\n# Add AI response")
        example_context.add_response_to_history({"content": "Tell me more about your headache"})
        print(f"context.add_response_to_history({{'content': 'Tell me more about your headache'}})")
        print(f"# Responses tracked: {len(example_context.previous_responses)}")
        
        print("\n# Advance conversation stage")
        example_context.advance_conversation_stage("symptom_gathering")
        print(f"context.advance_conversation_stage('symptom_gathering')")
        print(f"# Current stage: {example_context.conversation_stage}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)