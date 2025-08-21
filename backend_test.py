#!/usr/bin/env python3
"""
🚀 STEP 6.2: AI-POWERED PROGRESSIVE QUESTIONING ENGINE COMPREHENSIVE TESTING
===========================================================================

Comprehensive testing of the newly implemented AI-powered progressive questioning engine 
with Gemini LLM integration as requested in the review. This system enhances the existing 
Task 6.1 clarification system with revolutionary AI capabilities.

TESTING SCOPE:

**Phase 1: Core API Endpoints Testing (Priority 1)**
1. POST /api/medical-ai/ai-progressive-questioning-analysis
2. POST /api/medical-ai/generate-ai-progressive-question  
3. POST /api/medical-ai/ai-conversation-optimization

**Phase 2: Integration Testing (Priority 2)**
1. Medical AI Service Integration
2. Task 6.1 Integration

**Key Test Cases:**
- Mandatory examples: "sick", "pain", "bad"
- Additional AI test cases: "weird feeling", "something's wrong with my body", etc.
- Integration scenarios

TARGET: Validate Step 6.2 AI-Powered Progressive Questioning Engine
"""

import requests
import json
import time
import os
from typing import Dict, Any, List
from datetime import datetime

class AIProgressiveQuestioningTester:
    def __init__(self):
        # Get backend URL from environment
        self.backend_url = os.getenv('REACT_APP_BACKEND_URL', 'https://medchattest.preview.emergentagent.com')
        if not self.backend_url.endswith('/api'):
            self.backend_url = f"{self.backend_url}/api"
        
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
        print(f"🚀 STEP 6.2: AI-POWERED PROGRESSIVE QUESTIONING ENGINE TESTING")
        print(f"Backend URL: {self.backend_url}")
        print(f"Test Start Time: {datetime.now().isoformat()}")
        print("=" * 80)

    def log_test_result(self, test_name: str, success: bool, details: str, response_time: float = 0, response_data: Dict = None):
        """Log individual test results"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "response_time_ms": round(response_time * 1000, 2),
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        print(f"   Details: {details}")
        if response_time > 0:
            print(f"   Response Time: {result['response_time_ms']}ms")
        print()

    def test_ai_progressive_questioning_analysis(self, patient_input: str, test_name: str = None) -> Dict[str, Any]:
        """Test the AI Progressive Questioning Analysis API"""
        
        if not test_name:
            test_name = f"AI Progressive Questioning Analysis - {patient_input}"
        
        print(f"🧪 Testing AI Progressive Questioning Analysis API")
        print(f"Input: '{patient_input}'")
        
        # Prepare request payload
        payload = {
            "patient_input": patient_input,
            "medical_context": {
                "patient_demographics": {"age": 35, "gender": "female"},
                "medical_history": [],
                "current_medications": []
            },
            "conversation_history": []
        }
        
        # Measure processing time
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.backend_url}/medical-ai/ai-progressive-questioning-analysis",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = [
                    "symptom_analysis", "generated_questions", "conversation_strategy",
                    "recommended_next_action", "should_escalate", "conversation_efficiency_score",
                    "total_processing_time_ms", "algorithm_version"
                ]
                
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    self.log_test_result(
                        test_name,
                        False,
                        f"Missing required fields: {missing_fields}",
                        processing_time,
                        data
                    )
                    return data
                
                # Validate symptom analysis structure
                symptom_analysis = data.get('symptom_analysis', {})
                required_analysis_fields = [
                    "original_input", "vagueness_type", "missing_information",
                    "clinical_priority", "medical_domains", "confidence_score"
                ]
                
                missing_analysis_fields = [field for field in required_analysis_fields if field not in symptom_analysis]
                if missing_analysis_fields:
                    self.log_test_result(
                        test_name,
                        False,
                        f"Missing symptom analysis fields: {missing_analysis_fields}",
                        processing_time,
                        data
                    )
                    return data
                
                # Validate generated questions
                generated_questions = data.get('generated_questions', [])
                if not generated_questions:
                    self.log_test_result(
                        test_name,
                        False,
                        "No questions generated",
                        processing_time,
                        data
                    )
                    return data
                
                # Validate question structure
                first_question = generated_questions[0] if generated_questions else {}
                required_question_fields = [
                    "question_text", "medical_reasoning", "expected_information_type",
                    "clinical_priority", "confidence_score"
                ]
                
                missing_question_fields = [field for field in required_question_fields if field not in first_question]
                if missing_question_fields:
                    self.log_test_result(
                        test_name,
                        False,
                        f"Missing question fields: {missing_question_fields}",
                        processing_time,
                        data
                    )
                    return data
                
                # Validate content quality
                confidence_score = symptom_analysis.get('confidence_score', 0)
                vagueness_type = symptom_analysis.get('vagueness_type', '')
                num_questions = len(generated_questions)
                
                if confidence_score < 0.3:
                    self.log_test_result(
                        test_name,
                        False,
                        f"Very low confidence score: {confidence_score} (expected >= 0.3)",
                        processing_time,
                        data
                    )
                    return data
                
                # Success
                details = f"Vagueness: {vagueness_type}, Questions: {num_questions}, Confidence: {confidence_score:.3f}, Processing: {processing_time*1000:.1f}ms"
                self.log_test_result(test_name, True, details, processing_time, data)
                return data
                
            else:
                self.log_test_result(
                    test_name,
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    processing_time
                )
                return {}
                
        except Exception as e:
            end_time = time.time()
            processing_time = end_time - start_time
            
            self.log_test_result(
                test_name,
                False,
                f"Exception: {str(e)}",
                processing_time
            )
            return {}

    def test_generate_ai_progressive_question(self, symptom_analysis: Dict[str, Any], test_name: str = None) -> Dict[str, Any]:
        """Test the Generate AI Progressive Question API"""
        
        if not test_name:
            test_name = f"Generate AI Progressive Question"
        
        print(f"🧪 Testing Generate AI Progressive Question API")
        
        # Prepare request payload
        payload = {
            "symptom_analysis": symptom_analysis,
            "conversation_state": {
                "current_stage": "initial_questioning",
                "questions_asked": 0,
                "information_gathered": []
            },
            "patient_profile": {
                "communication_style": "balanced",
                "medical_literacy": "moderate"
            }
        }
        
        # Measure processing time
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.backend_url}/medical-ai/generate-ai-progressive-question",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=20
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = [
                    "generated_questions", "total_questions", "highest_priority_question",
                    "generation_reasoning", "processing_time_ms"
                ]
                
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    self.log_test_result(
                        test_name,
                        False,
                        f"Missing required fields: {missing_fields}",
                        processing_time,
                        data
                    )
                    return data
                
                # Validate content
                generated_questions = data.get('generated_questions', [])
                total_questions = data.get('total_questions', 0)
                highest_priority_question = data.get('highest_priority_question', {})
                
                if total_questions == 0 or not generated_questions:
                    self.log_test_result(
                        test_name,
                        False,
                        "No questions generated",
                        processing_time,
                        data
                    )
                    return data
                
                if not highest_priority_question.get('question_text'):
                    self.log_test_result(
                        test_name,
                        False,
                        "No highest priority question provided",
                        processing_time,
                        data
                    )
                    return data
                
                # Success
                details = f"Questions generated: {total_questions}, Processing: {processing_time*1000:.1f}ms"
                self.log_test_result(test_name, True, details, processing_time, data)
                return data
                
            else:
                self.log_test_result(
                    test_name,
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    processing_time
                )
                return {}
                
        except Exception as e:
            end_time = time.time()
            processing_time = end_time - start_time
            
            self.log_test_result(
                test_name,
                False,
                f"Exception: {str(e)}",
                processing_time
            )
            return {}

    def test_ai_conversation_optimization(self, conversation_history: List[Dict], patient_response: str, test_name: str = None) -> Dict[str, Any]:
        """Test the AI Conversation Optimization API"""
        
        if not test_name:
            test_name = f"AI Conversation Optimization"
        
        print(f"🧪 Testing AI Conversation Optimization API")
        print(f"Patient Response: '{patient_response}'")
        
        # Prepare request payload
        payload = {
            "conversation_history": conversation_history,
            "patient_response": patient_response,
            "medical_objectives": [
                "clarify_symptom_location",
                "assess_severity",
                "identify_triggers",
                "determine_urgency"
            ]
        }
        
        # Measure processing time
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.backend_url}/medical-ai/ai-conversation-optimization",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=20
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = [
                    "recommended_question", "reasoning", "conversation_efficiency_score",
                    "patient_engagement_level", "information_completeness",
                    "should_continue_questioning", "should_escalate_to_assessment"
                ]
                
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    self.log_test_result(
                        test_name,
                        False,
                        f"Missing required fields: {missing_fields}",
                        processing_time,
                        data
                    )
                    return data
                
                # Validate content
                recommended_question = data.get('recommended_question', '')
                reasoning = data.get('reasoning', '')
                efficiency_score = data.get('conversation_efficiency_score', 0)
                engagement_level = data.get('patient_engagement_level', '')
                
                if not recommended_question:
                    self.log_test_result(
                        test_name,
                        False,
                        "No recommended question provided",
                        processing_time,
                        data
                    )
                    return data
                
                if not reasoning:
                    self.log_test_result(
                        test_name,
                        False,
                        "No reasoning provided",
                        processing_time,
                        data
                    )
                    return data
                
                # Success
                details = f"Efficiency: {efficiency_score:.3f}, Engagement: {engagement_level}, Processing: {processing_time*1000:.1f}ms"
                self.log_test_result(test_name, True, details, processing_time, data)
                return data
                
            else:
                self.log_test_result(
                    test_name,
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    processing_time
                )
                return {}
                
        except Exception as e:
            end_time = time.time()
            processing_time = end_time - start_time
            
            self.log_test_result(
                test_name,
                False,
                f"Exception: {str(e)}",
                processing_time
            )
            return {}

    def test_mandatory_examples(self):
        """Test the mandatory examples from the review request"""
        
        print(f"\n🎯 TESTING MANDATORY EXAMPLES (MUST WORK PERFECT)")
        print("=" * 60)
        
        mandatory_examples = [
            {
                "input": "sick",
                "description": "Should trigger AI questioning with symptom specification"
            },
            {
                "input": "pain",
                "description": "Should trigger AI with location/character inquiry"
            },
            {
                "input": "bad",
                "description": "Should trigger AI with physical vs emotional differentiation"
            }
        ]
        
        for i, example in enumerate(mandatory_examples, 1):
            print(f"\n{i}. MANDATORY EXAMPLE: {example['description']}")
            print("-" * 50)
            
            # Test AI Progressive Questioning Analysis
            analysis_result = self.test_ai_progressive_questioning_analysis(
                example["input"],
                f"Mandatory Example {i} - {example['input']}"
            )
            
            # If analysis successful, test question generation
            if analysis_result and analysis_result.get('symptom_analysis'):
                self.test_generate_ai_progressive_question(
                    analysis_result['symptom_analysis'],
                    f"Mandatory Example {i} - Question Generation"
                )

    def test_additional_ai_cases(self):
        """Test additional AI test cases from the review request"""
        
        print(f"\n🤖 TESTING ADDITIONAL AI TEST CASES")
        print("=" * 60)
        
        additional_cases = [
            "weird feeling",
            "something's wrong with my body",
            "I don't feel normal",
            "having issues",
            "everything feels off"
        ]
        
        for i, case in enumerate(additional_cases, 1):
            print(f"\n{i}. AI TEST CASE: {case}")
            print("-" * 40)
            
            # Test AI Progressive Questioning Analysis
            analysis_result = self.test_ai_progressive_questioning_analysis(
                case,
                f"AI Test Case {i} - {case}"
            )
            
            # If analysis successful, test question generation
            if analysis_result and analysis_result.get('symptom_analysis'):
                self.test_generate_ai_progressive_question(
                    analysis_result['symptom_analysis'],
                    f"AI Test Case {i} - Question Generation"
                )

    def test_integration_scenarios(self):
        """Test integration scenarios from the review request"""
        
        print(f"\n🔗 TESTING INTEGRATION SCENARIOS")
        print("=" * 60)
        
        integration_scenarios = [
            {
                "input": "I feel sick",
                "description": "Should activate AI progressive questioning",
                "should_activate_ai": True
            },
            {
                "input": "I have sharp chest pain radiating to my left arm",
                "description": "Should NOT activate AI (specific enough)",
                "should_activate_ai": False
            }
        ]
        
        for i, scenario in enumerate(integration_scenarios, 1):
            print(f"\n{i}. INTEGRATION SCENARIO: {scenario['description']}")
            print("-" * 50)
            
            # Test AI Progressive Questioning Analysis
            analysis_result = self.test_ai_progressive_questioning_analysis(
                scenario["input"],
                f"Integration Scenario {i} - {scenario['input']}"
            )
            
            # Validate AI activation based on expectation
            if analysis_result:
                symptom_analysis = analysis_result.get('symptom_analysis', {})
                vagueness_type = symptom_analysis.get('vagueness_type', '')
                confidence_score = symptom_analysis.get('confidence_score', 0)
                
                # Check if AI should have been activated
                ai_activated = vagueness_type in ['general_vague', 'symptom_vague', 'emotional_vague'] or confidence_score < 0.7
                
                if scenario['should_activate_ai'] and not ai_activated:
                    self.log_test_result(
                        f"Integration Scenario {i} - AI Activation Check",
                        False,
                        f"Expected AI activation but got vagueness_type: {vagueness_type}, confidence: {confidence_score}",
                        0
                    )
                elif not scenario['should_activate_ai'] and ai_activated:
                    self.log_test_result(
                        f"Integration Scenario {i} - AI Activation Check",
                        False,
                        f"Expected NO AI activation but got vagueness_type: {vagueness_type}, confidence: {confidence_score}",
                        0
                    )
                else:
                    self.log_test_result(
                        f"Integration Scenario {i} - AI Activation Check",
                        True,
                        f"Correct AI activation decision: vagueness_type: {vagueness_type}, confidence: {confidence_score}",
                        0
                    )

    def test_medical_ai_service_integration(self):
        """Test integration with Medical AI Service"""
        
        print(f"\n🏥 TESTING MEDICAL AI SERVICE INTEGRATION")
        print("=" * 60)
        
        # Test with vague input that should trigger AI progressive questioning
        vague_input = "I don't feel well"
        
        print(f"Testing Medical AI Service with vague input: '{vague_input}'")
        
        # Test medical AI message endpoint
        payload = {
            "patient_id": "test-patient-123",
            "message": vague_input,
            "context": {
                "consultation_id": "test-consultation-456",
                "stage": "chief_complaint"
            }
        }
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.backend_url}/medical-ai/message",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if response indicates AI progressive questioning was used
                response_text = data.get('response', '').lower()
                
                # Look for indicators of progressive questioning
                progressive_indicators = [
                    'can you tell me more',
                    'could you describe',
                    'what specifically',
                    'where exactly',
                    'how would you describe'
                ]
                
                has_progressive_questioning = any(indicator in response_text for indicator in progressive_indicators)
                
                if has_progressive_questioning:
                    self.log_test_result(
                        "Medical AI Service Integration",
                        True,
                        f"AI progressive questioning detected in response, Processing: {processing_time*1000:.1f}ms",
                        processing_time,
                        data
                    )
                else:
                    self.log_test_result(
                        "Medical AI Service Integration",
                        False,
                        f"No AI progressive questioning detected in response: {response_text[:100]}...",
                        processing_time,
                        data
                    )
                    
            else:
                self.log_test_result(
                    "Medical AI Service Integration",
                    False,
                    f"HTTP {response.status_code}: {response.text[:200]}",
                    processing_time
                )
                
        except Exception as e:
            processing_time = time.time() - start_time
            self.log_test_result(
                "Medical AI Service Integration",
                False,
                f"Exception: {str(e)}",
                processing_time
            )

    def test_conversation_optimization_flow(self):
        """Test conversation optimization with realistic flow"""
        
        print(f"\n💬 TESTING CONVERSATION OPTIMIZATION FLOW")
        print("=" * 60)
        
        # Simulate a conversation flow
        conversation_history = [
            {
                "role": "assistant",
                "message": "Hello! I'm here to help with your health concerns. What brings you here today?",
                "timestamp": "2024-01-15T10:00:00Z"
            },
            {
                "role": "patient",
                "message": "I feel weird",
                "timestamp": "2024-01-15T10:00:30Z"
            },
            {
                "role": "assistant", 
                "message": "I understand you're feeling unusual. Can you tell me more about what specifically feels different?",
                "timestamp": "2024-01-15T10:01:00Z"
            }
        ]
        
        patient_responses = [
            "It's hard to explain, just not right",
            "My stomach feels funny and I'm tired",
            "The pain is getting worse"
        ]
        
        for i, patient_response in enumerate(patient_responses, 1):
            print(f"\n{i}. CONVERSATION TURN: {patient_response}")
            print("-" * 40)
            
            self.test_ai_conversation_optimization(
                conversation_history,
                patient_response,
                f"Conversation Optimization Turn {i}"
            )
            
            # Add this turn to conversation history for next iteration
            conversation_history.append({
                "role": "patient",
                "message": patient_response,
                "timestamp": f"2024-01-15T10:0{i+1}:30Z"
            })

    def test_error_handling_and_edge_cases(self):
        """Test error handling and edge cases"""
        
        print(f"\n🔧 TESTING ERROR HANDLING AND EDGE CASES")
        print("=" * 60)
        
        edge_cases = [
            {
                "input": "",
                "test_name": "Empty Input",
                "should_handle_gracefully": True
            },
            {
                "input": "xyz abc nonsense",
                "test_name": "Non-medical Input",
                "should_handle_gracefully": True
            },
            {
                "input": "I feel sick " * 50,  # Very long input
                "test_name": "Very Long Input",
                "should_handle_gracefully": True
            },
            {
                "input": "I feel sick!!! @#$% ???",
                "test_name": "Special Characters",
                "should_handle_gracefully": True
            }
        ]
        
        for i, case in enumerate(edge_cases, 1):
            print(f"\n{i}. EDGE CASE: {case['test_name']}")
            print("-" * 40)
            
            # Test AI Progressive Questioning Analysis with edge case
            result = self.test_ai_progressive_questioning_analysis(
                case["input"],
                f"Edge Case {i} - {case['test_name']}"
            )
            
            # For edge cases, we mainly care that the system doesn't crash
            # and provides some reasonable response

    def run_comprehensive_tests(self):
        """Run all comprehensive tests for AI Progressive Questioning Engine"""
        
        print(f"🚀 STEP 6.2: AI-POWERED PROGRESSIVE QUESTIONING ENGINE COMPREHENSIVE TESTING")
        print("=" * 80)
        print(f"Testing AI-Powered Progressive Questioning Engine with Gemini LLM Integration")
        print(f"Backend URL: {self.backend_url}")
        print(f"Test Start Time: {datetime.now().isoformat()}")
        print("=" * 80)
        print()
        
        # Run all test scenarios
        self.test_mandatory_examples()
        self.test_additional_ai_cases()
        self.test_integration_scenarios()
        self.test_medical_ai_service_integration()
        self.test_conversation_optimization_flow()
        self.test_error_handling_and_edge_cases()
        
        # Generate final report
        self.generate_final_report()

    def generate_final_report(self):
        """Generate comprehensive final test report"""
        
        print("=" * 80)
        print("🎯 STEP 6.2: AI-POWERED PROGRESSIVE QUESTIONING ENGINE - FINAL TEST REPORT")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed Tests: {self.passed_tests}")
        print(f"   Failed Tests: {self.total_tests - self.passed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        # Categorize results by test type
        categories = {
            "Mandatory Examples": [],
            "Additional AI Cases": [],
            "Integration Scenarios": [],
            "Medical AI Service Integration": [],
            "Conversation Optimization": [],
            "Edge Cases": []
        }
        
        for result in self.test_results:
            test_name = result["test_name"]
            if "Mandatory Example" in test_name:
                categories["Mandatory Examples"].append(result)
            elif "AI Test Case" in test_name:
                categories["Additional AI Cases"].append(result)
            elif "Integration Scenario" in test_name:
                categories["Integration Scenarios"].append(result)
            elif "Medical AI Service" in test_name:
                categories["Medical AI Service Integration"].append(result)
            elif "Conversation Optimization" in test_name:
                categories["Conversation Optimization"].append(result)
            elif "Edge Case" in test_name:
                categories["Edge Cases"].append(result)
        
        # Report by category
        for category_name, results in categories.items():
            if results:
                passed = sum(1 for r in results if r["success"])
                total = len(results)
                rate = (passed / total) * 100 if total > 0 else 0
                
                print(f"📋 {category_name.upper()}: {passed}/{total} passed ({rate:.1f}%)")
                for result in results:
                    status = "✅" if result["success"] else "❌"
                    print(f"   {status} {result['test_name']}")
                print()
        
        # Critical success criteria assessment
        print("🎯 CRITICAL SUCCESS CRITERIA ASSESSMENT:")
        
        # Check if mandatory examples work
        mandatory_tests = [r for r in categories["Mandatory Examples"] if r["success"]]
        mandatory_working = len(mandatory_tests) >= 3  # All 3 mandatory examples should work
        print(f"   ✅ Mandatory Examples Working: {'YES' if mandatory_working else 'NO'}")
        
        # Check if AI Progressive Questioning Analysis API is functional
        analysis_tests = [r for r in self.test_results if "AI Progressive Questioning Analysis" in r["test_name"] and r["success"]]
        analysis_functional = len(analysis_tests) > 0
        print(f"   ✅ AI Progressive Questioning Analysis API Functional: {'YES' if analysis_functional else 'NO'}")
        
        # Check if AI Question Generation API is functional
        generation_tests = [r for r in self.test_results if "Question Generation" in r["test_name"] and r["success"]]
        generation_functional = len(generation_tests) > 0
        print(f"   ✅ AI Question Generation API Functional: {'YES' if generation_functional else 'NO'}")
        
        # Check if AI Conversation Optimization API is functional
        optimization_tests = [r for r in categories["Conversation Optimization"] if r["success"]]
        optimization_functional = len(optimization_tests) > 0
        print(f"   ✅ AI Conversation Optimization API Functional: {'YES' if optimization_functional else 'NO'}")
        
        # Check if Medical AI Service integration works
        integration_tests = [r for r in categories["Medical AI Service Integration"] if r["success"]]
        integration_working = len(integration_tests) > 0
        print(f"   ✅ Medical AI Service Integration Working: {'YES' if integration_working else 'NO'}")
        
        # Check if error handling works
        edge_case_tests = [r for r in categories["Edge Cases"] if r["success"]]
        error_handling_works = len(edge_case_tests) >= 2  # At least half of edge cases should be handled
        print(f"   ✅ Error Handling Works: {'YES' if error_handling_works else 'NO'}")
        
        print()
        
        # Performance analysis
        response_times = [r["response_time_ms"] for r in self.test_results if r["response_time_ms"] > 0]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            print(f"⏱️  PERFORMANCE ANALYSIS:")
            print(f"   Average Response Time: {avg_response_time:.2f}ms")
            print(f"   Maximum Response Time: {max_response_time:.2f}ms")
            print(f"   Performance Target (<5000ms): {'✅ MET' if max_response_time < 5000 else '❌ EXCEEDED'}")
            print()
        
        # Final assessment
        critical_criteria_met = sum([
            mandatory_working,
            analysis_functional,
            generation_functional,
            optimization_functional,
            integration_working,
            error_handling_works
        ])
        
        if success_rate >= 80 and critical_criteria_met >= 5:
            print("🎉 ASSESSMENT: STEP 6.2 AI-POWERED PROGRESSIVE QUESTIONING ENGINE IS PRODUCTION-READY!")
            print("   The system demonstrates excellent AI-powered progressive questioning capabilities")
            print("   with comprehensive Gemini LLM integration and medical reasoning.")
        elif success_rate >= 60 and critical_criteria_met >= 4:
            print("⚠️  ASSESSMENT: STEP 6.2 SYSTEM IS FUNCTIONAL BUT NEEDS IMPROVEMENTS")
            print("   Core AI progressive questioning functionality is working but some components need attention.")
        else:
            print("❌ ASSESSMENT: STEP 6.2 SYSTEM NEEDS SIGNIFICANT WORK")
            print("   Multiple critical issues detected that prevent production deployment.")
        
        print()
        print(f"Test Completion Time: {datetime.now().isoformat()}")
        print("=" * 80)
        
        return {
            'total_tests': self.total_tests,
            'passed_tests': self.passed_tests,
            'success_rate': success_rate,
            'critical_criteria_met': critical_criteria_met,
            'mandatory_working': mandatory_working,
            'analysis_functional': analysis_functional,
            'generation_functional': generation_functional,
            'optimization_functional': optimization_functional,
            'integration_working': integration_working,
            'production_ready': success_rate >= 80 and critical_criteria_met >= 5
        }

def main():
    """Main test execution function"""
    tester = AIProgressiveQuestioningTester()
    results = tester.run_comprehensive_tests()
    
    print(f"\n🎉 STEP 6.2 AI-POWERED PROGRESSIVE QUESTIONING ENGINE TESTING COMPLETE!")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    main()