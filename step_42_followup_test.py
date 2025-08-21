#!/usr/bin/env python3
"""
COMPREHENSIVE TESTING OF STEP 4.2 INTELLIGENT FOLLOW-UP QUESTION GENERATION SYSTEM

This test suite validates the revolutionary Step 4.2 intelligent follow-up question generation system
for the medical chatbot that dramatically improves its ability to handle incomplete medical information.

Testing Focus:
- 8 Types of Medical Incompleteness Detection
- Enhanced Question Generation Functions
- Context-aware medical domain knowledge
- Empathetic and clinically appropriate language
- Conversation flow testing
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Configuration
BACKEND_URL = "https://medbot-query.preview.emergentagent.com/api"

class Step42FollowUpTester:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.test_results = []
        self.consultation_id = None
        
    def log_test(self, test_name: str, success: bool, details: str, response_data: Dict = None):
        """Log test results"""
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        print(f"   Details: {details}")
        if response_data and 'response' in response_data:
            print(f"   Response: {response_data['response'][:200]}...")
        print()

    def initialize_consultation(self) -> bool:
        """Initialize a medical consultation"""
        try:
            url = f"{self.backend_url}/medical-ai/initialize"
            payload = {
                "patient_id": "step42_test_patient",
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.consultation_id = data.get('consultation_id')
                self.log_test(
                    "Medical AI Consultation Initialization",
                    True,
                    f"Successfully initialized consultation with ID: {self.consultation_id}",
                    data
                )
                return True
            else:
                self.log_test(
                    "Medical AI Consultation Initialization",
                    False,
                    f"Failed with status {response.status_code}: {response.text}",
                    {"status_code": response.status_code, "response": response.text}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Medical AI Consultation Initialization",
                False,
                f"Exception occurred: {str(e)}",
                {"error": str(e)}
            )
            return False

    def send_message(self, message: str, context: Dict = None) -> Dict:
        """Send a message to the medical AI"""
        try:
            url = f"{self.backend_url}/medical-ai/message"
            
            payload = {
                "message": message,
                "consultation_id": self.consultation_id,
                "patient_id": "step42_test_patient",
                "timestamp": datetime.now().isoformat()
            }
            
            if context:
                payload["context"] = context
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "status_code": response.status_code
                }
                
        except Exception as e:
            return {"error": f"Exception: {str(e)}"}

    def test_vague_symptom_detection(self):
        """Test PRIORITY 1: Vague symptom detection and follow-up"""
        print("🧪 TESTING PRIORITY 1: VAGUE SYMPTOM DETECTION & FOLLOW-UP")
        
        vague_symptoms = [
            "feeling bad",
            "not well", 
            "something is wrong",
            "I'm sick",
            "not good",
            "terrible",
            "uncomfortable"
        ]
        
        for symptom in vague_symptoms:
            # First establish conversation context
            greeting_response = self.send_message("hi")
            if 'error' in greeting_response:
                self.log_test(
                    f"Vague Symptom Test Setup - {symptom}",
                    False,
                    f"Failed to establish conversation: {greeting_response['error']}"
                )
                continue
            
            # Send vague symptom
            response = self.send_message(symptom)
            
            if 'error' in response:
                self.log_test(
                    f"Vague Symptom Detection - '{symptom}'",
                    False,
                    f"API error: {response['error']}"
                )
                continue
            
            # Check if follow-up was triggered
            response_text = response.get('response', '').lower()
            
            # Look for follow-up indicators
            follow_up_indicators = [
                'can you help me understand',
                'what specific symptoms',
                'could you describe',
                'for example',
                'more specific',
                'tell me more',
                'what exactly'
            ]
            
            has_follow_up = any(indicator in response_text for indicator in follow_up_indicators)
            
            # Check for empathetic language
            empathetic_phrases = [
                'i understand',
                'i hear that',
                'completely natural',
                'understandable'
            ]
            
            has_empathy = any(phrase in response_text for phrase in empathetic_phrases)
            
            success = has_follow_up and len(response_text) > 50
            
            details = f"Vague symptom '{symptom}' "
            if has_follow_up:
                details += "✅ triggered intelligent follow-up "
            else:
                details += "❌ did not trigger follow-up "
                
            if has_empathy:
                details += "✅ with empathetic language"
            else:
                details += "⚠️ without empathetic language"
            
            self.log_test(
                f"Vague Symptom Detection - '{symptom}'",
                success,
                details,
                response
            )
            
            time.sleep(1)  # Rate limiting

    def test_incomplete_pain_descriptions(self):
        """Test PRIORITY 2: Incomplete pain descriptions"""
        print("🧪 TESTING PRIORITY 2: INCOMPLETE PAIN DESCRIPTIONS")
        
        pain_scenarios = [
            ("chest pain", "cardiovascular"),
            ("my head hurts", "neurological"),
            ("stomach ache", "gastrointestinal"), 
            ("back pain", "musculoskeletal"),
            ("really bad pain", "general")
        ]
        
        for pain_description, expected_domain in pain_scenarios:
            # Reset conversation
            self.initialize_consultation()
            greeting_response = self.send_message("hi")
            
            # Send incomplete pain description
            response = self.send_message(pain_description)
            
            if 'error' in response:
                self.log_test(
                    f"Incomplete Pain Test - '{pain_description}'",
                    False,
                    f"API error: {response['error']}"
                )
                continue
            
            response_text = response.get('response', '').lower()
            
            # Check for domain-specific follow-ups
            domain_indicators = {
                'cardiovascular': ['crushing', 'pressure', 'radiating', 'arm', 'jaw'],
                'neurological': ['throbbing', 'pounding', 'temples', 'one side'],
                'gastrointestinal': ['cramping', 'gnawing', 'burning', 'belly button'],
                'musculoskeletal': ['aching', 'stiff', 'muscle'],
                'general': ['scale of 1 to 10', 'what does it feel like']
            }
            
            expected_indicators = domain_indicators.get(expected_domain, [])
            has_domain_specific = any(indicator in response_text for indicator in expected_indicators)
            
            # Check for pain characteristic questions
            pain_questions = [
                'what does it feel like',
                'how would you rate',
                'scale of 1 to 10',
                'where exactly',
                'can you describe'
            ]
            
            has_pain_questions = any(question in response_text for question in pain_questions)
            
            success = has_pain_questions and len(response_text) > 50
            
            details = f"Pain '{pain_description}' "
            if has_pain_questions:
                details += "✅ triggered appropriate follow-up "
            else:
                details += "❌ did not trigger pain follow-up "
                
            if has_domain_specific:
                details += f"✅ with {expected_domain} domain knowledge"
            else:
                details += f"⚠️ without {expected_domain} domain specificity"
            
            self.log_test(
                f"Incomplete Pain Description - '{pain_description}'",
                success,
                details,
                response
            )
            
            time.sleep(1)

    def test_vague_temporal_responses(self):
        """Test PRIORITY 3: Vague temporal responses"""
        print("🧪 TESTING PRIORITY 3: VAGUE TEMPORAL RESPONSES")
        
        temporal_responses = [
            "recently",
            "for a while",
            "lately",
            "some time ago", 
            "not long ago"
        ]
        
        for temporal_response in temporal_responses:
            # Reset and establish context
            self.initialize_consultation()
            greeting_response = self.send_message("hi")
            symptom_response = self.send_message("I have a headache")
            
            # Send vague temporal response
            response = self.send_message(temporal_response)
            
            if 'error' in response:
                self.log_test(
                    f"Vague Temporal Test - '{temporal_response}'",
                    False,
                    f"API error: {response['error']}"
                )
                continue
            
            response_text = response.get('response', '').lower()
            
            # Check for temporal clarification requests
            temporal_clarifiers = [
                'more specific about the timing',
                'hours ago, days ago',
                'when exactly',
                'sudden or gradual',
                'came on quickly',
                'developed slowly'
            ]
            
            has_temporal_followup = any(clarifier in response_text for clarifier in temporal_clarifiers)
            
            success = has_temporal_followup and len(response_text) > 50
            
            details = f"Temporal response '{temporal_response}' "
            if has_temporal_followup:
                details += "✅ triggered temporal clarification request"
            else:
                details += "❌ did not trigger temporal follow-up"
            
            self.log_test(
                f"Vague Temporal Response - '{temporal_response}'",
                success,
                details,
                response
            )
            
            time.sleep(1)

    def test_single_word_anatomical_responses(self):
        """Test PRIORITY 4: Single word anatomical responses"""
        print("🧪 TESTING PRIORITY 4: SINGLE WORD ANATOMICAL RESPONSES")
        
        anatomical_words = [
            ("chest", "cardiovascular"),
            ("stomach", "gastrointestinal"),
            ("head", "neurological"),
            ("heart", "cardiovascular"),
            ("breathing", "pulmonary"),
            ("joints", "musculoskeletal")
        ]
        
        for anatomical_word, expected_domain in anatomical_words:
            # Reset and establish context
            self.initialize_consultation()
            greeting_response = self.send_message("hi")
            
            # Send single anatomical word
            response = self.send_message(anatomical_word)
            
            if 'error' in response:
                self.log_test(
                    f"Single Word Anatomical Test - '{anatomical_word}'",
                    False,
                    f"API error: {response['error']}"
                )
                continue
            
            response_text = response.get('response', '').lower()
            
            # Check for domain-specific symptom questions
            domain_questions = {
                'cardiovascular': ['chest pain', 'palpitations', 'shortness of breath', 'heart-related'],
                'gastrointestinal': ['stomach-related', 'nausea', 'vomiting', 'digestive'],
                'neurological': ['head-related', 'headache', 'dizziness', 'neurological'],
                'pulmonary': ['breathing problems', 'shortness of breath', 'wheezing'],
                'musculoskeletal': ['joint pain', 'stiffness', 'swelling']
            }
            
            expected_questions = domain_questions.get(expected_domain, [])
            has_domain_questions = any(question in response_text for question in expected_questions)
            
            # Check for general symptom inquiry
            general_questions = [
                'what specific symptoms',
                'what are you experiencing',
                'can you describe',
                'what exactly are you feeling'
            ]
            
            has_symptom_inquiry = any(question in response_text for question in general_questions)
            
            success = has_symptom_inquiry and len(response_text) > 50
            
            details = f"Anatomical word '{anatomical_word}' "
            if has_symptom_inquiry:
                details += "✅ triggered symptom inquiry "
            else:
                details += "❌ did not trigger symptom inquiry "
                
            if has_domain_questions:
                details += f"✅ with {expected_domain} domain specificity"
            else:
                details += f"⚠️ without {expected_domain} domain specificity"
            
            self.log_test(
                f"Single Word Anatomical - '{anatomical_word}'",
                success,
                details,
                response
            )
            
            time.sleep(1)

    def test_emotional_responses(self):
        """Test PRIORITY 5: Emotional responses without medical details"""
        print("🧪 TESTING PRIORITY 5: EMOTIONAL RESPONSES WITHOUT MEDICAL DETAILS")
        
        emotional_responses = [
            "scared",
            "worried", 
            "anxious",
            "nervous",
            "frightened"
        ]
        
        for emotion in emotional_responses:
            # Reset and establish context
            self.initialize_consultation()
            greeting_response = self.send_message("hi")
            
            # Send emotional response
            response = self.send_message(emotion)
            
            if 'error' in response:
                self.log_test(
                    f"Emotional Response Test - '{emotion}'",
                    False,
                    f"API error: {response['error']}"
                )
                continue
            
            response_text = response.get('response', '').lower()
            
            # Check for supportive language
            supportive_phrases = [
                'i understand',
                'completely natural',
                'understandable',
                'normal to feel',
                'i can understand'
            ]
            
            has_support = any(phrase in response_text for phrase in supportive_phrases)
            
            # Check for underlying symptom inquiry
            symptom_inquiry = [
                'what specific symptoms',
                'what are you experiencing',
                'what is worrying you',
                'causing you concern',
                'making you feel'
            ]
            
            has_inquiry = any(inquiry in response_text for inquiry in symptom_inquiry)
            
            success = has_support and has_inquiry and len(response_text) > 50
            
            details = f"Emotional response '{emotion}' "
            if has_support:
                details += "✅ received supportive response "
            else:
                details += "❌ lacked supportive language "
                
            if has_inquiry:
                details += "✅ with symptom inquiry"
            else:
                details += "❌ without symptom inquiry"
            
            self.log_test(
                f"Emotional Response - '{emotion}'",
                success,
                details,
                response
            )
            
            time.sleep(1)

    def test_comprehensive_conversation_flow(self):
        """Test PRIORITY 6: Comprehensive conversation flow testing"""
        print("🧪 TESTING PRIORITY 6: COMPREHENSIVE CONVERSATION FLOW")
        
        # Test complete conversation flow with multiple incomplete responses
        conversation_steps = [
            ("hi", "greeting"),
            ("I'm not feeling well", "vague_symptom"),
            ("chest pain", "incomplete_pain"),
            ("really bad", "vague_severity")
        ]
        
        # Initialize fresh conversation
        self.initialize_consultation()
        
        conversation_context = None
        all_steps_successful = True
        conversation_log = []
        
        for step_message, step_type in conversation_steps:
            response = self.send_message(step_message, conversation_context)
            
            if 'error' in response:
                self.log_test(
                    f"Conversation Flow - {step_type}",
                    False,
                    f"API error at step '{step_message}': {response['error']}"
                )
                all_steps_successful = False
                break
            
            response_text = response.get('response', '')
            conversation_context = response.get('context')
            
            # Log this step
            conversation_log.append({
                "user_message": step_message,
                "ai_response": response_text[:200] + "..." if len(response_text) > 200 else response_text,
                "step_type": step_type
            })
            
            # Validate step-specific requirements
            step_success = True
            step_details = ""
            
            if step_type == "greeting":
                step_success = len(response_text) > 20
                step_details = "Greeting response received"
                
            elif step_type == "vague_symptom":
                follow_up_indicators = ['specific symptoms', 'can you help', 'what exactly']
                has_followup = any(indicator in response_text.lower() for indicator in follow_up_indicators)
                step_success = has_followup
                step_details = "Vague symptom triggered follow-up" if has_followup else "No follow-up for vague symptom"
                
            elif step_type == "incomplete_pain":
                pain_followup = ['what does it feel like', 'can you describe', 'where exactly']
                has_pain_followup = any(followup in response_text.lower() for followup in pain_followup)
                step_success = has_pain_followup
                step_details = "Pain description triggered follow-up" if has_pain_followup else "No follow-up for incomplete pain"
                
            elif step_type == "vague_severity":
                severity_followup = ['scale of 1 to 10', 'how severe', 'daily activities']
                has_severity_followup = any(followup in response_text.lower() for followup in severity_followup)
                step_success = has_severity_followup
                step_details = "Severity inquiry triggered follow-up" if has_severity_followup else "No follow-up for vague severity"
            
            if not step_success:
                all_steps_successful = False
            
            self.log_test(
                f"Conversation Flow Step - {step_type}",
                step_success,
                step_details,
                response
            )
            
            time.sleep(1)
        
        # Overall conversation flow assessment
        self.log_test(
            "Complete Conversation Flow",
            all_steps_successful,
            f"Multi-step conversation with {len(conversation_steps)} interactions completed. All steps successful: {all_steps_successful}",
            {"conversation_log": conversation_log}
        )

    def test_false_positive_prevention(self):
        """Test that complete responses don't trigger unnecessary follow-ups"""
        print("🧪 TESTING FALSE POSITIVE PREVENTION")
        
        complete_responses = [
            "I have a sharp, stabbing chest pain on the left side that started 2 hours ago and rates 7/10 in severity",
            "My headache is a throbbing pain on both sides of my head that started yesterday morning and gets worse with bright lights",
            "I'm experiencing burning stomach pain in my upper abdomen that occurs 30 minutes after eating spicy foods",
            "The back pain is a dull ache in my lower back that started after lifting heavy boxes at work three days ago"
        ]
        
        for complete_response in complete_responses:
            # Reset conversation
            self.initialize_consultation()
            greeting_response = self.send_message("hi")
            
            # Send complete response
            response = self.send_message(complete_response)
            
            if 'error' in response:
                self.log_test(
                    f"False Positive Test - Complete Response",
                    False,
                    f"API error: {response['error']}"
                )
                continue
            
            response_text = response.get('response', '').lower()
            
            # Check that it doesn't trigger follow-up questions
            followup_indicators = [
                'can you tell me more',
                'more specific',
                'what exactly',
                'can you describe',
                'help me understand'
            ]
            
            has_unnecessary_followup = any(indicator in response_text for indicator in followup_indicators)
            
            # Should progress conversation instead
            progression_indicators = [
                'thank you for',
                'i understand',
                'based on what you',
                'let me ask about',
                'next question'
            ]
            
            has_progression = any(indicator in response_text for indicator in progression_indicators)
            
            success = not has_unnecessary_followup and len(response_text) > 30
            
            details = f"Complete response "
            if not has_unnecessary_followup:
                details += "✅ did not trigger unnecessary follow-up "
            else:
                details += "❌ triggered unnecessary follow-up "
                
            if has_progression:
                details += "✅ progressed conversation appropriately"
            else:
                details += "⚠️ did not show clear progression"
            
            self.log_test(
                f"False Positive Prevention - Complete Response",
                success,
                details,
                response
            )
            
            time.sleep(1)

    def run_all_tests(self):
        """Run all Step 4.2 follow-up system tests"""
        print("🚀 STARTING COMPREHENSIVE STEP 4.2 INTELLIGENT FOLLOW-UP QUESTION GENERATION TESTING")
        print("=" * 80)
        
        start_time = time.time()
        
        # Initialize consultation for testing
        if not self.initialize_consultation():
            print("❌ Failed to initialize consultation. Aborting tests.")
            return
        
        # Run all test categories
        self.test_vague_symptom_detection()
        self.test_incomplete_pain_descriptions()
        self.test_vague_temporal_responses()
        self.test_single_word_anatomical_responses()
        self.test_emotional_responses()
        self.test_comprehensive_conversation_flow()
        self.test_false_positive_prevention()
        
        # Calculate results
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("=" * 80)
        print("🏁 STEP 4.2 INTELLIGENT FOLLOW-UP SYSTEM TESTING COMPLETE")
        print(f"📊 RESULTS: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}% success rate)")
        print(f"⏱️ Duration: {duration:.1f} seconds")
        print("=" * 80)
        
        # Detailed results summary
        print("\n📋 DETAILED TEST RESULTS:")
        
        categories = {
            "Vague Symptom Detection": [r for r in self.test_results if "Vague Symptom" in r['test_name']],
            "Incomplete Pain Descriptions": [r for r in self.test_results if "Incomplete Pain" in r['test_name']],
            "Vague Temporal Responses": [r for r in self.test_results if "Vague Temporal" in r['test_name']],
            "Single Word Anatomical": [r for r in self.test_results if "Single Word Anatomical" in r['test_name']],
            "Emotional Responses": [r for r in self.test_results if "Emotional Response" in r['test_name']],
            "Conversation Flow": [r for r in self.test_results if "Conversation Flow" in r['test_name']],
            "False Positive Prevention": [r for r in self.test_results if "False Positive" in r['test_name']]
        }
        
        for category, results in categories.items():
            if results:
                category_passed = sum(1 for r in results if r['success'])
                category_total = len(results)
                category_rate = (category_passed / category_total) * 100 if category_total > 0 else 0
                status = "✅" if category_rate >= 80 else "⚠️" if category_rate >= 60 else "❌"
                print(f"{status} {category}: {category_passed}/{category_total} ({category_rate:.1f}%)")
        
        # Key success metrics validation
        print("\n🎯 KEY SUCCESS METRICS VALIDATION:")
        
        # Check incompleteness detection
        vague_tests = [r for r in self.test_results if "Vague Symptom" in r['test_name'] or "Incomplete Pain" in r['test_name']]
        incompleteness_rate = (sum(1 for r in vague_tests if r['success']) / len(vague_tests)) * 100 if vague_tests else 0
        print(f"{'✅' if incompleteness_rate >= 90 else '❌'} Incompleteness Detection: {incompleteness_rate:.1f}% (Target: 100%)")
        
        # Check medical domain accuracy
        domain_tests = [r for r in self.test_results if "domain" in r['details'].lower()]
        domain_rate = (sum(1 for r in domain_tests if "✅" in r['details'] and "domain" in r['details']) / len(domain_tests)) * 100 if domain_tests else 0
        print(f"{'✅' if domain_rate >= 80 else '❌'} Medical Domain Accuracy: {domain_rate:.1f}% (Target: Medical appropriateness)")
        
        # Check empathetic language
        empathy_tests = [r for r in self.test_results if "empathetic" in r['details'].lower() or "supportive" in r['details'].lower()]
        empathy_rate = (sum(1 for r in empathy_tests if "✅" in r['details'] and ("empathetic" in r['details'] or "supportive" in r['details'])) / len(empathy_tests)) * 100 if empathy_tests else 0
        print(f"{'✅' if empathy_rate >= 70 else '❌'} Empathetic Language: {empathy_rate:.1f}% (Target: Professional and supportive)")
        
        # Check false positive prevention
        false_positive_tests = [r for r in self.test_results if "False Positive" in r['test_name']]
        false_positive_rate = (sum(1 for r in false_positive_tests if r['success']) / len(false_positive_tests)) * 100 if false_positive_tests else 0
        print(f"{'✅' if false_positive_rate >= 90 else '❌'} False Positive Prevention: {false_positive_rate:.1f}% (Target: No unnecessary follow-ups)")
        
        # Overall production readiness assessment
        overall_ready = (success_rate >= 80 and incompleteness_rate >= 90 and false_positive_rate >= 90)
        print(f"\n🚀 PRODUCTION READINESS: {'✅ READY' if overall_ready else '⚠️ NEEDS IMPROVEMENT'}")
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "success_rate": success_rate,
            "duration": duration,
            "production_ready": overall_ready,
            "detailed_results": self.test_results
        }

def main():
    """Main test execution"""
    print("🧪 STEP 4.2 INTELLIGENT FOLLOW-UP QUESTION GENERATION SYSTEM TESTING")
    print("Testing the revolutionary medical AI follow-up system...")
    print()
    
    tester = Step42FollowUpTester()
    results = tester.run_all_tests()
    
    # Save results to file
    with open('/app/step_42_test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to: /app/step_42_test_results.json")
    
    return results

if __name__ == "__main__":
    main()