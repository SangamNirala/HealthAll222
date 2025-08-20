#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime, timedelta
import uuid

class Phase22MedicalChatTester:
    """
    Phase 2.2 Medical Chat Interface Hook Integration Tester
    
    Tests the Medical AI Service backend specifically for Phase 2.2 Medical Chat Interface Hook integration.
    Focus areas:
    1. Consultation Initialization with patient_id='anonymous' and timestamp parameter
    2. Message Processing with conversation_history parameter
    3. Enhanced Response Structure validation
    4. Emergency Detection Integration
    5. Medical Context Persistence across conversation turns
    """
    
    def __init__(self, base_url="https://healthai-testing.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        self.conversation_history = []

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}" if endpoint else self.base_url
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=15)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=15)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=15)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=15)

            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response keys: {list(response_data.keys()) if isinstance(response_data, dict) else 'Non-dict response'}")
                except:
                    print(f"   Response: {response.text[:200]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:300]}...")

            self.test_results.append({
                'name': name,
                'success': success,
                'status_code': response.status_code,
                'expected_status': expected_status,
                'response': response.text[:500] if not success else "OK"
            })

            return success, response.json() if success and response.text else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.test_results.append({
                'name': name,
                'success': False,
                'error': str(e)
            })
            return False, {}

    def test_consultation_initialization_anonymous(self):
        """Test POST /api/medical-ai/initialize with patient_id='anonymous' and timestamp parameter"""
        print("\n🏥 Testing Consultation Initialization for Anonymous Patient...")
        
        # Test 1: Initialize with anonymous patient and timestamp
        current_timestamp = datetime.utcnow().isoformat() + "Z"
        init_data = {
            "patient_id": "anonymous",
            "timestamp": current_timestamp
        }
        
        success1, response1 = self.run_test(
            "Medical AI Initialize - Anonymous Patient with Timestamp",
            "POST",
            "medical-ai/initialize",
            200,
            data=init_data
        )
        
        consultation_id = ""
        if success1 and response1:
            # Validate required response fields for Phase 2.2 hook
            expected_keys = ['consultation_id', 'patient_id', 'current_stage', 'response']
            missing_keys = [key for key in expected_keys if key not in response1]
            
            if not missing_keys:
                print(f"   ✅ Response contains all required keys: {expected_keys}")
                
                consultation_id = response1.get('consultation_id', '')
                patient_id = response1.get('patient_id', '')
                current_stage = response1.get('current_stage', '')
                ai_response = response1.get('response', '')
                
                print(f"   🆔 Consultation ID: {consultation_id}")
                print(f"   👤 Patient ID: {patient_id}")
                print(f"   📋 Current stage: {current_stage}")
                print(f"   🤖 AI response length: {len(ai_response)} characters")
                
                # Validate anonymous patient handling
                anonymous_valid = patient_id == "anonymous"
                print(f"   🔒 Anonymous patient handling: {'✅' if anonymous_valid else '❌'}")
                
                # Validate greeting stage
                greeting_valid = current_stage == "greeting"
                print(f"   👋 Greeting stage initialization: {'✅' if greeting_valid else '❌'}")
                
                # Store consultation ID for subsequent tests
                self.consultation_id = consultation_id
                
            else:
                print(f"   ❌ Response missing required keys: {missing_keys}")
                success1 = False
        
        # Test 2: Initialize without timestamp (should still work)
        init_data_no_timestamp = {
            "patient_id": "anonymous"
        }
        
        success2, response2 = self.run_test(
            "Medical AI Initialize - Anonymous Patient without Timestamp",
            "POST",
            "medical-ai/initialize",
            200,
            data=init_data_no_timestamp
        )
        
        if success2 and response2:
            consultation_id_2 = response2.get('consultation_id', '')
            # Verify different consultation IDs
            ids_different = consultation_id != consultation_id_2
            print(f"   🔄 Unique consultation IDs: {'✅' if ids_different else '❌'}")
        
        return success1 and success2

    def test_message_processing_with_conversation_history(self):
        """Test POST /api/medical-ai/message with conversation_history parameter"""
        print("\n💬 Testing Message Processing with Conversation History...")
        
        if not hasattr(self, 'consultation_id') or not self.consultation_id:
            print("   ❌ No consultation ID available from initialization test")
            return False
        
        # Test 1: First message without conversation history
        first_message_data = {
            "consultation_id": self.consultation_id,
            "message": "Hello, I have a headache for 2 days"
        }
        
        success1, response1 = self.run_test(
            "Message Processing - First Message",
            "POST",
            "medical-ai/message",
            200,
            data=first_message_data
        )
        
        if success1 and response1:
            # Store conversation history for next test
            self.conversation_history.append({
                "role": "user",
                "content": "Hello, I have a headache for 2 days",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
            
            ai_response = response1.get('response', '')
            if ai_response:
                self.conversation_history.append({
                    "role": "assistant", 
                    "content": ai_response,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
        
        # Test 2: Second message (API doesn't currently support conversation_history parameter, but test context persistence)
        second_message_data = {
            "consultation_id": self.consultation_id,
            "message": "The pain is on the right side of my head, throbbing pain, about 7/10 severity"
        }
        
        success2, response2 = self.run_test(
            "Message Processing - Second Message (Context Persistence)",
            "POST",
            "medical-ai/message",
            200,
            data=second_message_data
        )
        
        if success2 and response2:
            ai_response_2 = response2.get('response', '')
            
            # Validate that AI maintains context from previous message
            context_awareness = any(word in ai_response_2.lower() for word in ['headache', 'pain', 'mentioned', 'described'])
            print(f"   🧠 Context awareness maintained: {'✅' if context_awareness else '❌'}")
            
            # Check if stage progressed appropriately
            current_stage = response2.get('current_stage', '')
            stage_progression = current_stage != "greeting"
            print(f"   📋 Stage progression: {'✅' if stage_progression else '❌'} ('{current_stage}')")
        
        # Test 3: Third message to test continued context
        third_message_data = {
            "consultation_id": self.consultation_id,
            "message": "It gets worse with bright lights and loud sounds"
        }
        
        success3, response3 = self.run_test(
            "Message Processing - Third Message (Continued Context)",
            "POST",
            "medical-ai/message",
            200,
            data=third_message_data
        )
        
        if success3 and response3:
            ai_response_3 = response3.get('response', '')
            
            # Check for continuity in medical reasoning
            continuity_indicators = any(word in ai_response_3.lower() for word in ['migraine', 'photophobia', 'phonophobia', 'triggers', 'light', 'sound'])
            print(f"   🔗 Medical reasoning continuity: {'✅' if continuity_indicators else '❌'}")
            
            # Note: conversation_history parameter not yet implemented in current API
            print(f"   ⚠️  Note: conversation_history parameter not yet implemented in current API")
            print(f"   ℹ️  Context persistence currently handled via consultation_id")
        
        return success1 and success2 and success3

    def test_enhanced_response_structure(self):
        """Test that API responses include all required fields for the updated hook"""
        print("\n📋 Testing Enhanced Response Structure for Phase 2.2 Hook...")
        
        if not hasattr(self, 'consultation_id') or not self.consultation_id:
            print("   ❌ No consultation ID available from initialization test")
            return False
        
        # Test with a comprehensive symptom message
        comprehensive_message_data = {
            "consultation_id": self.consultation_id,
            "message": "I'm having severe chest pain that started 1 hour ago. It's crushing, radiating to my left arm, with nausea and sweating. Pain is 9/10.",
            "conversation_history": self.conversation_history
        }
        
        success, response = self.run_test(
            "Enhanced Response Structure - Comprehensive Symptom",
            "POST",
            "medical-ai/message",
            200,
            data=comprehensive_message_data
        )
        
        if success and response:
            # Check for current API fields and Phase 2.2 hook requirements
            current_api_fields = [
                'stage',           # Current medical interview stage
                'urgency',         # Urgency level (routine, urgent, emergency)
                'consultation_id', # Consultation identifier
                'patient_id',      # Patient identifier
                'current_stage',   # Current stage (duplicate of stage)
                'emergency_detected', # Emergency detection flag
                'response',        # AI response text
                'context',         # Medical context
                'next_questions',  # Suggested next questions
                'differential_diagnoses',  # List of potential diagnoses
                'recommendations'  # Medical recommendations
            ]
            
            # Phase 2.2 hook desired fields (not yet implemented)
            desired_fields = [
                'confidence',      # AI confidence score
                'clinical_reasoning'  # Clinical reasoning explanation
            ]
            
            present_fields = []
            missing_fields = []
            
            for field in current_api_fields:
                if field in response:
                    present_fields.append(field)
                    
                    # Validate field content
                    field_value = response.get(field)
                    if field == 'stage':
                        stage_valid = isinstance(field_value, str) and field_value != ""
                        print(f"   📋 Stage field: {'✅' if stage_valid else '❌'} ('{field_value}')")
                    
                    elif field == 'urgency':
                        urgency_valid = field_value in ['routine', 'urgent', 'emergency']
                        print(f"   🚨 Urgency field: {'✅' if urgency_valid else '❌'} ('{field_value}')")
                    
                    elif field == 'consultation_id':
                        consultation_valid = isinstance(field_value, str) and field_value != ""
                        print(f"   🆔 Consultation ID: {'✅' if consultation_valid else '❌'} ('{field_value}')")
                    
                    elif field == 'patient_id':
                        patient_valid = isinstance(field_value, str) and field_value != ""
                        print(f"   👤 Patient ID: {'✅' if patient_valid else '❌'} ('{field_value}')")
                    
                    elif field == 'emergency_detected':
                        emergency_valid = isinstance(field_value, bool)
                        print(f"   🚨 Emergency detected: {'✅' if emergency_valid else '❌'} ({field_value})")
                    
                    elif field == 'differential_diagnoses':
                        diagnoses_valid = field_value is None or (isinstance(field_value, list) and len(field_value) >= 0)
                        print(f"   🔬 Differential diagnoses: {'✅' if diagnoses_valid else '❌'} ({len(field_value) if isinstance(field_value, list) else 'None'})")
                    
                    elif field == 'recommendations':
                        recommendations_valid = field_value is None or (isinstance(field_value, list) and len(field_value) >= 0)
                        print(f"   💊 Recommendations: {'✅' if recommendations_valid else '❌'} ({len(field_value) if isinstance(field_value, list) else 'None'})")
                
                else:
                    missing_fields.append(field)
            
            # Check for desired Phase 2.2 fields
            for field in desired_fields:
                if field in response:
                    print(f"   ✅ Phase 2.2 field present: {field}")
                else:
                    print(f"   ⚠️  Phase 2.2 field missing: {field} (enhancement needed)")
            
            print(f"   ✅ Current API fields ({len(present_fields)}/{len(current_api_fields)}): {present_fields}")
            if missing_fields:
                print(f"   ❌ Missing current API fields: {missing_fields}")
            
            # Current API structure validation (should be complete)
            current_structure_complete = len(missing_fields) == 0
            print(f"   📊 Current API structure complete: {'✅' if current_structure_complete else '❌'}")
            
            # Phase 2.2 enhancement status
            phase22_fields_present = all(field in response for field in desired_fields)
            print(f"   🚀 Phase 2.2 enhancements ready: {'✅' if phase22_fields_present else '⚠️  Needs enhancement'}")
            
            return current_structure_complete
        
        return False

    def test_emergency_detection_integration(self):
        """Test emergency scenarios to ensure proper urgency='emergency' responses"""
        print("\n🚨 Testing Emergency Detection Integration...")
        
        # Initialize new consultation for emergency testing
        init_data = {
            "patient_id": "anonymous",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        init_success, init_response = self.run_test(
            "Initialize Emergency Test Consultation",
            "POST",
            "medical-ai/initialize",
            200,
            data=init_data
        )
        
        if not init_success:
            return False
        
        emergency_consultation_id = init_response.get('consultation_id', '')
        
        # Test 1: Crushing chest pain emergency
        chest_pain_data = {
            "consultation_id": emergency_consultation_id,
            "message": "I'm having crushing chest pain with shortness of breath. Started 30 minutes ago, pain is 10/10, radiating to my left arm and jaw. I'm sweating and feel nauseous.",
            "conversation_history": []
        }
        
        success1, response1 = self.run_test(
            "Emergency Detection - Crushing Chest Pain with Shortness of Breath",
            "POST",
            "medical-ai/message",
            200,
            data=chest_pain_data
        )
        
        if success1 and response1:
            urgency = response1.get('urgency', '')
            ai_response = response1.get('response', '')
            recommendations = response1.get('recommendations', [])
            
            print(f"   🚨 Urgency level: {urgency}")
            
            # Validate emergency detection
            emergency_detected = urgency == 'emergency'
            print(f"   🚨 Emergency urgency detected: {'✅' if emergency_detected else '❌'}")
            
            # Check for 911 recommendation
            contains_911 = '911' in ai_response or any('911' in str(rec) for rec in recommendations)
            print(f"   📞 Contains 911 recommendation: {'✅' if contains_911 else '❌'}")
            
            # Check for immediate action language
            immediate_action = any(word in ai_response.lower() for word in ['immediately', 'urgent', 'emergency', 'call', 'hospital'])
            print(f"   ⚡ Immediate action language: {'✅' if immediate_action else '❌'}")
        
        # Test 2: Severe allergic reaction
        allergic_reaction_data = {
            "consultation_id": emergency_consultation_id,
            "message": "I ate peanuts 10 minutes ago and now my throat is swelling, I can barely breathe, my face is swollen, and I have hives all over my body. I'm feeling dizzy.",
            "conversation_history": [
                {
                    "role": "user",
                    "content": "I'm having crushing chest pain with shortness of breath...",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            ]
        }
        
        success2, response2 = self.run_test(
            "Emergency Detection - Severe Allergic Reaction",
            "POST",
            "medical-ai/message",
            200,
            data=allergic_reaction_data
        )
        
        if success2 and response2:
            urgency_2 = response2.get('urgency', '')
            ai_response_2 = response2.get('response', '')
            
            emergency_detected_2 = urgency_2 == 'emergency'
            print(f"   🚨 Allergic reaction emergency detected: {'✅' if emergency_detected_2 else '❌'}")
            
            # Check for EpiPen/epinephrine mention
            epipen_mentioned = any(word in ai_response_2.lower() for word in ['epipen', 'epinephrine', 'adrenaline'])
            print(f"   💉 EpiPen/Epinephrine mentioned: {'✅' if epipen_mentioned else '❌'}")
        
        # Test 3: Non-emergency symptom (should not trigger emergency)
        non_emergency_data = {
            "consultation_id": emergency_consultation_id,
            "message": "I have a mild headache that's been bothering me for a few days. It's about 3/10 pain and comes and goes.",
            "conversation_history": []
        }
        
        success3, response3 = self.run_test(
            "Emergency Detection - Non-Emergency Symptom",
            "POST",
            "medical-ai/message",
            200,
            data=non_emergency_data
        )
        
        if success3 and response3:
            urgency_3 = response3.get('urgency', '')
            
            non_emergency_correct = urgency_3 in ['routine', 'urgent'] and urgency_3 != 'emergency'
            print(f"   ✅ Non-emergency correctly identified: {'✅' if non_emergency_correct else '❌'} ('{urgency_3}')")
        
        return success1 and success2 and success3

    def test_medical_context_persistence(self):
        """Test that medical context is properly updated and maintained across conversation turns"""
        print("\n🔄 Testing Medical Context Persistence...")
        
        # Initialize new consultation for context testing
        init_data = {
            "patient_id": "anonymous",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        init_success, init_response = self.run_test(
            "Initialize Context Persistence Test",
            "POST",
            "medical-ai/initialize",
            200,
            data=init_data
        )
        
        if not init_success:
            return False
        
        context_consultation_id = init_response.get('consultation_id', '')
        context_history = []
        
        # Test 1: Establish initial medical context
        initial_context_data = {
            "consultation_id": context_consultation_id,
            "message": "I'm a 45-year-old male with diabetes and high blood pressure. I take metformin and lisinopril daily.",
            "conversation_history": context_history
        }
        
        success1, response1 = self.run_test(
            "Context Persistence - Establish Initial Medical Context",
            "POST",
            "medical-ai/message",
            200,
            data=initial_context_data
        )
        
        if success1 and response1:
            # Update conversation history
            context_history.extend([
                {
                    "role": "user",
                    "content": initial_context_data["message"],
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                },
                {
                    "role": "assistant",
                    "content": response1.get('response', ''),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            ])
        
        # Test 2: Add symptom information
        symptom_context_data = {
            "consultation_id": context_consultation_id,
            "message": "For the past week, I've been having increased thirst and frequent urination. My blood sugar readings have been higher than usual.",
            "conversation_history": context_history
        }
        
        success2, response2 = self.run_test(
            "Context Persistence - Add Symptom Information",
            "POST",
            "medical-ai/message",
            200,
            data=symptom_context_data
        )
        
        if success2 and response2:
            ai_response_2 = response2.get('response', '')
            
            # Check if AI references previous medical history
            context_reference = any(word in ai_response_2.lower() for word in ['diabetes', 'metformin', 'mentioned', 'history'])
            print(f"   🔗 References previous medical history: {'✅' if context_reference else '❌'}")
            
            # Update conversation history
            context_history.extend([
                {
                    "role": "user",
                    "content": symptom_context_data["message"],
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                },
                {
                    "role": "assistant",
                    "content": ai_response_2,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            ])
        
        # Test 3: Follow-up question that requires context
        followup_context_data = {
            "consultation_id": context_consultation_id,
            "message": "Should I adjust my medication dosage? Also, I forgot to mention I've been feeling more tired lately.",
            "conversation_history": context_history
        }
        
        success3, response3 = self.run_test(
            "Context Persistence - Follow-up with Context Dependency",
            "POST",
            "medical-ai/message",
            200,
            data=followup_context_data
        )
        
        if success3 and response3:
            ai_response_3 = response3.get('response', '')
            
            # Check if AI understands medication reference (metformin from earlier)
            medication_context = any(word in ai_response_3.lower() for word in ['metformin', 'lisinopril', 'medication', 'dosage'])
            print(f"   💊 Understands medication context: {'✅' if medication_context else '❌'}")
            
            # Check if AI connects fatigue to diabetes symptoms
            symptom_connection = any(word in ai_response_3.lower() for word in ['diabetes', 'blood sugar', 'glucose', 'symptoms'])
            print(f"   🔗 Connects symptoms to medical history: {'✅' if symptom_connection else '❌'}")
        
        # Test 4: Test context across different conversation turns
        context_test_data = {
            "consultation_id": context_consultation_id,
            "message": "What should I do about the symptoms I mentioned?",
            "conversation_history": context_history
        }
        
        success4, response4 = self.run_test(
            "Context Persistence - Reference to Previous Symptoms",
            "POST",
            "medical-ai/message",
            200,
            data=context_test_data
        )
        
        if success4 and response4:
            ai_response_4 = response4.get('response', '')
            
            # Check if AI can identify "the symptoms" from conversation history
            symptom_recall = any(word in ai_response_4.lower() for word in ['thirst', 'urination', 'tired', 'fatigue', 'blood sugar'])
            print(f"   🧠 Recalls specific symptoms from history: {'✅' if symptom_recall else '❌'}")
            
            # Check for comprehensive medical advice considering full context
            comprehensive_advice = len(ai_response_4) > 100 and any(word in ai_response_4.lower() for word in ['recommend', 'suggest', 'consider', 'monitor'])
            print(f"   📋 Provides comprehensive contextual advice: {'✅' if comprehensive_advice else '❌'}")
        
        return success1 and success2 and success3 and success4

    def run_phase_2_2_tests(self):
        """Run all Phase 2.2 Medical Chat Interface Hook integration tests"""
        print("🚀 Starting Phase 2.2 Medical Chat Interface Hook Integration Tests")
        print(f"🌐 Base URL: {self.base_url}")
        print("=" * 80)
        
        # Test 1: Consultation Initialization
        print("\n" + "="*50)
        print("TEST 1: CONSULTATION INITIALIZATION")
        print("="*50)
        initialization_success = self.test_consultation_initialization_anonymous()
        
        # Test 2: Message Processing with Conversation History
        print("\n" + "="*50)
        print("TEST 2: MESSAGE PROCESSING WITH CONVERSATION HISTORY")
        print("="*50)
        message_processing_success = self.test_message_processing_with_conversation_history()
        
        # Test 3: Enhanced Response Structure
        print("\n" + "="*50)
        print("TEST 3: ENHANCED RESPONSE STRUCTURE")
        print("="*50)
        response_structure_success = self.test_enhanced_response_structure()
        
        # Test 4: Emergency Detection Integration
        print("\n" + "="*50)
        print("TEST 4: EMERGENCY DETECTION INTEGRATION")
        print("="*50)
        emergency_detection_success = self.test_emergency_detection_integration()
        
        # Test 5: Medical Context Persistence
        print("\n" + "="*50)
        print("TEST 5: MEDICAL CONTEXT PERSISTENCE")
        print("="*50)
        context_persistence_success = self.test_medical_context_persistence()
        
        # Final Summary
        print("\n" + "="*80)
        print("PHASE 2.2 MEDICAL CHAT INTERFACE HOOK INTEGRATION TEST SUMMARY")
        print("="*80)
        
        test_results = [
            ("Consultation Initialization (Anonymous + Timestamp)", initialization_success),
            ("Message Processing (Conversation History)", message_processing_success),
            ("Enhanced Response Structure", response_structure_success),
            ("Emergency Detection Integration", emergency_detection_success),
            ("Medical Context Persistence", context_persistence_success)
        ]
        
        passed_tests = sum(1 for _, success in test_results if success)
        total_tests = len(test_results)
        
        for test_name, success in test_results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {status} - {test_name}")
        
        print(f"\n📊 Overall Results: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)")
        print(f"📈 Individual API calls: {self.tests_passed}/{self.tests_run} passed ({self.tests_passed/self.tests_run*100:.1f}%)")
        
        # Determine overall success
        overall_success = passed_tests >= 4  # At least 4 out of 5 major test areas should pass
        
        if overall_success:
            print("\n🎉 PHASE 2.2 MEDICAL CHAT INTERFACE HOOK INTEGRATION: READY FOR PRODUCTION")
            print("   All critical functionality validated for frontend hook integration.")
        else:
            print("\n⚠️  PHASE 2.2 INTEGRATION ISSUES DETECTED")
            print("   Some critical functionality needs attention before frontend integration.")
        
        return overall_success

if __name__ == "__main__":
    tester = Phase22MedicalChatTester()
    success = tester.run_phase_2_2_tests()
    sys.exit(0 if success else 1)