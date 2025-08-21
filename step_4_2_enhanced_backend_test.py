#!/usr/bin/env python3
"""
🧠 STEP 4.2 ENHANCED INTELLIGENT FOLLOW-UP QUESTION GENERATION SYSTEM TESTING

This comprehensive test suite validates the enhanced Step 4.2 intelligent follow-up question 
generation system with comprehensive scenarios as requested in the review.

TESTING FOCUS: Validate the enhanced incompleteness detection and intelligent follow-up generation system

TEST SCENARIOS:
1. **Enhanced Temporal Vagueness**: Test "recently", "lately", "for a while", "maybe recently", "about lately"
2. **Enhanced Pain Descriptions**: Test "chest pain", "my head hurts", "stomach ache", "back pain"
3. **New Medical Abbreviation Handling**: Test "bp", "meds", "doc", "hr"
4. **New Trigger Without Context**: Test "ate pizza", "took pills", "drank coffee"
5. **New Family History**: Test "family history", "my mom", "dad had"
6. **New Frequency Pattern**: Test "always", "sometimes", "often", "rarely", "usually"

VALIDATION CRITERIA:
- Each scenario should trigger appropriate incompleteness detection
- Follow-up questions should be contextually relevant and medically appropriate
- Enhanced detection patterns should work better than before
- New incompleteness types should generate proper follow-up questions
- Response quality should be comprehensive and empathetic

EXPECTED IMPROVEMENTS:
- Better temporal vagueness detection with context-aware follow-ups
- More comprehensive pain description analysis
- Handle medical abbreviations appropriately
- Connect triggers to symptom context
- Elaborate on family history relevance
- Clarify frequency patterns with specific questions
"""

import asyncio
import json
import time
import requests
import sys
from typing import Dict, Any, List
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://followup-testing.preview.emergentagent.com/api"

class Step42EnhancedFollowUpTester:
    """Comprehensive tester for Step 4.2 Enhanced Intelligent Follow-up Question Generation System"""
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_test_result(self, test_name: str, success: bool, details: str, response_time: float = 0):
        """Log individual test results"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "response_time_ms": response_time,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        print(f"   Details: {details}")
        if response_time > 0:
            print(f"   Response Time: {response_time:.2f}ms")
        print()

    async def initialize_conversation(self) -> str:
        """Initialize a new conversation and return consultation_id"""
        try:
            init_data = {
                "patient_id": "anonymous",
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.backend_url}/medical-ai/initialize",
                json=init_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("consultation_id")
            return None
        except Exception as e:
            print(f"Initialization error: {e}")
            return None

    async def send_message(self, consultation_id: str, message: str) -> Dict[str, Any]:
        """Send a message and return the response"""
        try:
            message_data = {
                "message": message,
                "consultation_id": consultation_id,
                "patient_id": "anonymous"
            }
            
            start_time = time.time()
            response = requests.post(
                f"{self.backend_url}/medical-ai/message",
                json=message_data,
                timeout=30
            )
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                result["_response_time"] = response_time
                return result
            else:
                return {"error": f"HTTP {response.status_code}", "_response_time": response_time}
        except Exception as e:
            return {"error": str(e), "_response_time": 0}

    async def test_enhanced_temporal_vagueness(self):
        """
        TEST SCENARIO 1: Enhanced Temporal Vagueness
        Test "recently", "lately", "for a while", "maybe recently", "about lately"
        """
        print("🕐 TESTING SCENARIO 1: ENHANCED TEMPORAL VAGUENESS")
        print("=" * 80)
        
        temporal_expressions = [
            "recently",
            "lately", 
            "for a while",
            "maybe recently",
            "about lately"
        ]
        
        for expression in temporal_expressions:
            consultation_id = await self.initialize_conversation()
            if not consultation_id:
                self.log_test_result(
                    f"Temporal Vagueness - {expression} (Init)",
                    False,
                    "Failed to initialize conversation",
                    0
                )
                continue
            
            # Establish context first
            context_response = await self.send_message(consultation_id, "I have a headache")
            if "error" in context_response:
                self.log_test_result(
                    f"Temporal Vagueness - {expression} (Context)",
                    False,
                    f"Context establishment failed: {context_response['error']}",
                    context_response.get("_response_time", 0)
                )
                continue
            
            # Test temporal vagueness
            response = await self.send_message(consultation_id, expression)
            if "error" in response:
                self.log_test_result(
                    f"Temporal Vagueness - {expression}",
                    False,
                    f"Request failed: {response['error']}",
                    response.get("_response_time", 0)
                )
                continue
            
            response_text = response.get("response", "").lower()
            
            # Check for temporal clarification indicators
            temporal_clarification_keywords = [
                "when exactly", "how long ago", "specific", "timing", "hours ago", 
                "days ago", "weeks ago", "months ago", "when you say", "more specific",
                "came on quickly", "developed slowly", "sudden", "gradual"
            ]
            
            has_temporal_clarification = any(keyword in response_text for keyword in temporal_clarification_keywords)
            
            # Check for context awareness (headache reference)
            has_context_awareness = any(keyword in response_text for keyword in ["headache", "symptoms", "what you mentioned"])
            
            # Check for empathetic language
            has_empathy = any(phrase in response_text for phrase in ["understand", "help me", "can you", "tell me more"])
            
            success_indicators = []
            if has_temporal_clarification:
                success_indicators.append("✅ Temporal clarification detected")
            else:
                success_indicators.append("❌ Temporal clarification missing")
                
            if has_context_awareness:
                success_indicators.append("✅ Context awareness present")
            else:
                success_indicators.append("❌ Context awareness missing")
                
            if has_empathy:
                success_indicators.append("✅ Empathetic language present")
            else:
                success_indicators.append("❌ Empathetic language missing")
            
            # Success if at least 2 out of 3 indicators pass
            passed_indicators = sum(1 for indicator in success_indicators if indicator.startswith("✅"))
            success = passed_indicators >= 2
            
            details = f"Expression: '{expression}' | Response: '{response_text[:150]}...' | Indicators: {'; '.join(success_indicators)}"
            
            self.log_test_result(
                f"Temporal Vagueness - {expression}",
                success,
                details,
                response.get("_response_time", 0)
            )

    async def test_enhanced_pain_descriptions(self):
        """
        TEST SCENARIO 2: Enhanced Pain Descriptions
        Test "chest pain", "my head hurts", "stomach ache", "back pain"
        """
        print("💔 TESTING SCENARIO 2: ENHANCED PAIN DESCRIPTIONS")
        print("=" * 80)
        
        pain_expressions = [
            "chest pain",
            "my head hurts",
            "stomach ache", 
            "back pain"
        ]
        
        for expression in pain_expressions:
            consultation_id = await self.initialize_conversation()
            if not consultation_id:
                self.log_test_result(
                    f"Pain Description - {expression} (Init)",
                    False,
                    "Failed to initialize conversation",
                    0
                )
                continue
            
            response = await self.send_message(consultation_id, expression)
            if "error" in response:
                self.log_test_result(
                    f"Pain Description - {expression}",
                    False,
                    f"Request failed: {response['error']}",
                    response.get("_response_time", 0)
                )
                continue
            
            response_text = response.get("response", "").lower()
            
            # Check for pain quality questions
            pain_quality_keywords = [
                "sharp", "dull", "crushing", "pressure", "burning", "throbbing", 
                "stabbing", "aching", "what does it feel like", "describe", "quality"
            ]
            has_pain_quality = any(keyword in response_text for keyword in pain_quality_keywords)
            
            # Check for severity questions
            severity_keywords = [
                "scale", "1 to 10", "1-10", "rate", "severe", "severity", 
                "how bad", "interfere", "daily activities", "intensity"
            ]
            has_severity = any(keyword in response_text for keyword in severity_keywords)
            
            # Check for location specificity
            location_keywords = [
                "where", "location", "point to", "specific area", "exactly", "radiates"
            ]
            has_location = any(keyword in response_text for keyword in location_keywords)
            
            # Check for medical domain awareness
            domain_keywords = {
                "chest pain": ["chest", "heart", "cardiac", "cardiovascular"],
                "my head hurts": ["head", "headache", "migraine", "neurological"],
                "stomach ache": ["stomach", "abdominal", "gastric", "digestive"],
                "back pain": ["back", "spine", "musculoskeletal", "lumbar"]
            }
            
            relevant_domain_keywords = domain_keywords.get(expression, [])
            has_domain_awareness = any(keyword in response_text for keyword in relevant_domain_keywords)
            
            success_indicators = []
            if has_pain_quality:
                success_indicators.append("✅ Pain quality inquiry detected")
            else:
                success_indicators.append("❌ Pain quality inquiry missing")
                
            if has_severity:
                success_indicators.append("✅ Severity assessment detected")
            else:
                success_indicators.append("❌ Severity assessment missing")
                
            if has_location:
                success_indicators.append("✅ Location specificity detected")
            else:
                success_indicators.append("❌ Location specificity missing")
                
            if has_domain_awareness:
                success_indicators.append("✅ Medical domain awareness present")
            else:
                success_indicators.append("❌ Medical domain awareness missing")
            
            # Success if at least 3 out of 4 indicators pass
            passed_indicators = sum(1 for indicator in success_indicators if indicator.startswith("✅"))
            success = passed_indicators >= 3
            
            details = f"Expression: '{expression}' | Response: '{response_text[:150]}...' | Indicators: {'; '.join(success_indicators)}"
            
            self.log_test_result(
                f"Pain Description - {expression}",
                success,
                details,
                response.get("_response_time", 0)
            )

    async def test_medical_abbreviation_handling(self):
        """
        TEST SCENARIO 3: New Medical Abbreviation Handling
        Test "bp", "meds", "doc", "hr"
        """
        print("🔤 TESTING SCENARIO 3: MEDICAL ABBREVIATION HANDLING")
        print("=" * 80)
        
        abbreviations = {
            "bp": "blood pressure",
            "meds": "medications",
            "doc": "doctor",
            "hr": "heart rate"
        }
        
        for abbrev, full_term in abbreviations.items():
            consultation_id = await self.initialize_conversation()
            if not consultation_id:
                self.log_test_result(
                    f"Medical Abbreviation - {abbrev} (Init)",
                    False,
                    "Failed to initialize conversation",
                    0
                )
                continue
            
            response = await self.send_message(consultation_id, abbrev)
            if "error" in response:
                self.log_test_result(
                    f"Medical Abbreviation - {abbrev}",
                    False,
                    f"Request failed: {response['error']}",
                    response.get("_response_time", 0)
                )
                continue
            
            response_text = response.get("response", "").lower()
            
            # Check for abbreviation recognition/expansion
            has_expansion = full_term.lower() in response_text or abbrev in response_text
            
            # Check for clarification request
            clarification_keywords = [
                "can you clarify", "what do you mean", "more specific", "tell me more",
                "elaborate", "explain", "which", "about your"
            ]
            has_clarification = any(keyword in response_text for keyword in clarification_keywords)
            
            # Check for medical context awareness
            medical_context_keywords = [
                "medical", "health", "symptoms", "condition", "concern", "issue"
            ]
            has_medical_context = any(keyword in response_text for keyword in medical_context_keywords)
            
            success_indicators = []
            if has_expansion:
                success_indicators.append("✅ Abbreviation recognition detected")
            else:
                success_indicators.append("❌ Abbreviation recognition missing")
                
            if has_clarification:
                success_indicators.append("✅ Clarification request present")
            else:
                success_indicators.append("❌ Clarification request missing")
                
            if has_medical_context:
                success_indicators.append("✅ Medical context awareness present")
            else:
                success_indicators.append("❌ Medical context awareness missing")
            
            # Success if at least 2 out of 3 indicators pass
            passed_indicators = sum(1 for indicator in success_indicators if indicator.startswith("✅"))
            success = passed_indicators >= 2
            
            details = f"Abbreviation: '{abbrev}' ({full_term}) | Response: '{response_text[:150]}...' | Indicators: {'; '.join(success_indicators)}"
            
            self.log_test_result(
                f"Medical Abbreviation - {abbrev}",
                success,
                details,
                response.get("_response_time", 0)
            )

    async def test_trigger_without_context(self):
        """
        TEST SCENARIO 4: New Trigger Without Context
        Test "ate pizza", "took pills", "drank coffee"
        """
        print("🎯 TESTING SCENARIO 4: TRIGGER WITHOUT CONTEXT")
        print("=" * 80)
        
        triggers = [
            "ate pizza",
            "took pills", 
            "drank coffee"
        ]
        
        for trigger in triggers:
            consultation_id = await self.initialize_conversation()
            if not consultation_id:
                self.log_test_result(
                    f"Trigger Without Context - {trigger} (Init)",
                    False,
                    "Failed to initialize conversation",
                    0
                )
                continue
            
            response = await self.send_message(consultation_id, trigger)
            if "error" in response:
                self.log_test_result(
                    f"Trigger Without Context - {trigger}",
                    False,
                    f"Request failed: {response['error']}",
                    response.get("_response_time", 0)
                )
                continue
            
            response_text = response.get("response", "").lower()
            
            # Check for symptom connection inquiry
            symptom_connection_keywords = [
                "symptoms", "feeling", "experiencing", "bothering", "concerns",
                "health", "after", "before", "related", "connection"
            ]
            has_symptom_connection = any(keyword in response_text for keyword in symptom_connection_keywords)
            
            # Check for timing inquiry
            timing_keywords = [
                "when", "timing", "before", "after", "how long", "recently", "ago"
            ]
            has_timing_inquiry = any(keyword in response_text for keyword in timing_keywords)
            
            # Check for context building
            context_building_keywords = [
                "tell me more", "can you describe", "what happened", "help me understand",
                "elaborate", "explain", "details"
            ]
            has_context_building = any(keyword in response_text for keyword in context_building_keywords)
            
            success_indicators = []
            if has_symptom_connection:
                success_indicators.append("✅ Symptom connection inquiry detected")
            else:
                success_indicators.append("❌ Symptom connection inquiry missing")
                
            if has_timing_inquiry:
                success_indicators.append("✅ Timing inquiry present")
            else:
                success_indicators.append("❌ Timing inquiry missing")
                
            if has_context_building:
                success_indicators.append("✅ Context building detected")
            else:
                success_indicators.append("❌ Context building missing")
            
            # Success if at least 2 out of 3 indicators pass
            passed_indicators = sum(1 for indicator in success_indicators if indicator.startswith("✅"))
            success = passed_indicators >= 2
            
            details = f"Trigger: '{trigger}' | Response: '{response_text[:150]}...' | Indicators: {'; '.join(success_indicators)}"
            
            self.log_test_result(
                f"Trigger Without Context - {trigger}",
                success,
                details,
                response.get("_response_time", 0)
            )

    async def test_family_history(self):
        """
        TEST SCENARIO 5: New Family History
        Test "family history", "my mom", "dad had"
        """
        print("👨‍👩‍👧‍👦 TESTING SCENARIO 5: FAMILY HISTORY")
        print("=" * 80)
        
        family_expressions = [
            "family history",
            "my mom",
            "dad had"
        ]
        
        for expression in family_expressions:
            consultation_id = await self.initialize_conversation()
            if not consultation_id:
                self.log_test_result(
                    f"Family History - {expression} (Init)",
                    False,
                    "Failed to initialize conversation",
                    0
                )
                continue
            
            response = await self.send_message(consultation_id, expression)
            if "error" in response:
                self.log_test_result(
                    f"Family History - {expression}",
                    False,
                    f"Request failed: {response['error']}",
                    response.get("_response_time", 0)
                )
                continue
            
            response_text = response.get("response", "").lower()
            
            # Check for family history elaboration
            family_elaboration_keywords = [
                "family history", "family member", "relatives", "genetic", "hereditary",
                "runs in family", "family medical", "inherited"
            ]
            has_family_elaboration = any(keyword in response_text for keyword in family_elaboration_keywords)
            
            # Check for specific condition inquiry
            condition_inquiry_keywords = [
                "condition", "disease", "illness", "medical problem", "health issue",
                "what condition", "what did", "diagnosed with"
            ]
            has_condition_inquiry = any(keyword in response_text for keyword in condition_inquiry_keywords)
            
            # Check for relevance connection
            relevance_keywords = [
                "relevant", "related", "concern", "important", "affects", "risk",
                "because", "since", "given"
            ]
            has_relevance_connection = any(keyword in response_text for keyword in relevance_keywords)
            
            # Check for empathetic response
            empathy_keywords = [
                "understand", "appreciate", "thank you", "helpful", "important information"
            ]
            has_empathy = any(keyword in response_text for keyword in empathy_keywords)
            
            success_indicators = []
            if has_family_elaboration:
                success_indicators.append("✅ Family history elaboration detected")
            else:
                success_indicators.append("❌ Family history elaboration missing")
                
            if has_condition_inquiry:
                success_indicators.append("✅ Specific condition inquiry present")
            else:
                success_indicators.append("❌ Specific condition inquiry missing")
                
            if has_relevance_connection:
                success_indicators.append("✅ Relevance connection detected")
            else:
                success_indicators.append("❌ Relevance connection missing")
                
            if has_empathy:
                success_indicators.append("✅ Empathetic response present")
            else:
                success_indicators.append("❌ Empathetic response missing")
            
            # Success if at least 3 out of 4 indicators pass
            passed_indicators = sum(1 for indicator in success_indicators if indicator.startswith("✅"))
            success = passed_indicators >= 3
            
            details = f"Expression: '{expression}' | Response: '{response_text[:150]}...' | Indicators: {'; '.join(success_indicators)}"
            
            self.log_test_result(
                f"Family History - {expression}",
                success,
                details,
                response.get("_response_time", 0)
            )

    async def test_frequency_patterns(self):
        """
        TEST SCENARIO 6: New Frequency Pattern
        Test "always", "sometimes", "often", "rarely", "usually"
        """
        print("📊 TESTING SCENARIO 6: FREQUENCY PATTERNS")
        print("=" * 80)
        
        frequency_expressions = [
            "always",
            "sometimes",
            "often", 
            "rarely",
            "usually"
        ]
        
        for expression in frequency_expressions:
            consultation_id = await self.initialize_conversation()
            if not consultation_id:
                self.log_test_result(
                    f"Frequency Pattern - {expression} (Init)",
                    False,
                    "Failed to initialize conversation",
                    0
                )
                continue
            
            # Establish context first
            context_response = await self.send_message(consultation_id, "I have headaches")
            if "error" in context_response:
                self.log_test_result(
                    f"Frequency Pattern - {expression} (Context)",
                    False,
                    f"Context establishment failed: {context_response['error']}",
                    context_response.get("_response_time", 0)
                )
                continue
            
            response = await self.send_message(consultation_id, expression)
            if "error" in response:
                self.log_test_result(
                    f"Frequency Pattern - {expression}",
                    False,
                    f"Request failed: {response['error']}",
                    response.get("_response_time", 0)
                )
                continue
            
            response_text = response.get("response", "").lower()
            
            # Check for frequency clarification
            frequency_clarification_keywords = [
                "how often", "frequency", "times per", "daily", "weekly", "monthly",
                "specific", "more precise", "exactly how", "pattern"
            ]
            has_frequency_clarification = any(keyword in response_text for keyword in frequency_clarification_keywords)
            
            # Check for quantification request
            quantification_keywords = [
                "times", "days", "hours", "number", "count", "how many", "per day", "per week"
            ]
            has_quantification = any(keyword in response_text for keyword in quantification_keywords)
            
            # Check for pattern analysis
            pattern_keywords = [
                "pattern", "trigger", "when", "circumstances", "situation", "causes"
            ]
            has_pattern_analysis = any(keyword in response_text for keyword in pattern_keywords)
            
            # Check for context reference (headaches)
            has_context_reference = any(keyword in response_text for keyword in ["headache", "symptoms", "what you mentioned"])
            
            success_indicators = []
            if has_frequency_clarification:
                success_indicators.append("✅ Frequency clarification detected")
            else:
                success_indicators.append("❌ Frequency clarification missing")
                
            if has_quantification:
                success_indicators.append("✅ Quantification request present")
            else:
                success_indicators.append("❌ Quantification request missing")
                
            if has_pattern_analysis:
                success_indicators.append("✅ Pattern analysis detected")
            else:
                success_indicators.append("❌ Pattern analysis missing")
                
            if has_context_reference:
                success_indicators.append("✅ Context reference present")
            else:
                success_indicators.append("❌ Context reference missing")
            
            # Success if at least 3 out of 4 indicators pass
            passed_indicators = sum(1 for indicator in success_indicators if indicator.startswith("✅"))
            success = passed_indicators >= 3
            
            details = f"Expression: '{expression}' | Response: '{response_text[:150]}...' | Indicators: {'; '.join(success_indicators)}"
            
            self.log_test_result(
                f"Frequency Pattern - {expression}",
                success,
                details,
                response.get("_response_time", 0)
            )

    async def run_comprehensive_tests(self):
        """Run all comprehensive tests for Step 4.2 Enhanced Intelligent Follow-up Question Generation System"""
        print("🧠 STEP 4.2 ENHANCED INTELLIGENT FOLLOW-UP QUESTION GENERATION SYSTEM TESTING")
        print("=" * 100)
        print(f"Backend URL: {self.backend_url}")
        print(f"Test Start Time: {datetime.now().isoformat()}")
        print("=" * 100)
        print()
        
        # Run all test scenarios
        await self.test_enhanced_temporal_vagueness()
        await self.test_enhanced_pain_descriptions()
        await self.test_medical_abbreviation_handling()
        await self.test_trigger_without_context()
        await self.test_family_history()
        await self.test_frequency_patterns()
        
        # Generate final report
        self.generate_final_report()

    def generate_final_report(self):
        """Generate comprehensive final test report"""
        print("=" * 100)
        print("🎯 STEP 4.2 ENHANCED INTELLIGENT FOLLOW-UP SYSTEM - FINAL TEST REPORT")
        print("=" * 100)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed Tests: {self.passed_tests}")
        print(f"   Failed Tests: {self.total_tests - self.passed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        # Categorize results by scenario
        scenarios = {
            "Enhanced Temporal Vagueness": [],
            "Enhanced Pain Descriptions": [],
            "Medical Abbreviation Handling": [],
            "Trigger Without Context": [],
            "Family History": [],
            "Frequency Patterns": []
        }
        
        for result in self.test_results:
            test_name = result["test_name"]
            if "Temporal Vagueness" in test_name:
                scenarios["Enhanced Temporal Vagueness"].append(result)
            elif "Pain Description" in test_name:
                scenarios["Enhanced Pain Descriptions"].append(result)
            elif "Medical Abbreviation" in test_name:
                scenarios["Medical Abbreviation Handling"].append(result)
            elif "Trigger Without Context" in test_name:
                scenarios["Trigger Without Context"].append(result)
            elif "Family History" in test_name:
                scenarios["Family History"].append(result)
            elif "Frequency Pattern" in test_name:
                scenarios["Frequency Patterns"].append(result)
        
        # Report by scenario
        for scenario_name, results in scenarios.items():
            if results:
                passed = sum(1 for r in results if r["success"])
                total = len(results)
                rate = (passed / total) * 100 if total > 0 else 0
                
                print(f"📋 {scenario_name.upper()}: {passed}/{total} passed ({rate:.1f}%)")
                for result in results:
                    status = "✅" if result["success"] else "❌"
                    print(f"   {status} {result['test_name']}")
                print()
        
        # Critical success criteria assessment
        print("🎯 STEP 4.2 ENHANCED CRITICAL SUCCESS CRITERIA:")
        
        # Check each scenario type
        temporal_working = any("Temporal Vagueness" in r["test_name"] and r["success"] for r in self.test_results)
        pain_working = any("Pain Description" in r["test_name"] and r["success"] for r in self.test_results)
        abbreviation_working = any("Medical Abbreviation" in r["test_name"] and r["success"] for r in self.test_results)
        trigger_working = any("Trigger Without Context" in r["test_name"] and r["success"] for r in self.test_results)
        family_working = any("Family History" in r["test_name"] and r["success"] for r in self.test_results)
        frequency_working = any("Frequency Pattern" in r["test_name"] and r["success"] for r in self.test_results)
        
        print(f"   ✅ Enhanced Temporal Vagueness Detection: {'WORKING' if temporal_working else 'FAILING'}")
        print(f"   ✅ Enhanced Pain Description Analysis: {'WORKING' if pain_working else 'FAILING'}")
        print(f"   ✅ Medical Abbreviation Handling: {'WORKING' if abbreviation_working else 'FAILING'}")
        print(f"   ✅ Trigger Without Context Processing: {'WORKING' if trigger_working else 'FAILING'}")
        print(f"   ✅ Family History Elaboration: {'WORKING' if family_working else 'FAILING'}")
        print(f"   ✅ Frequency Pattern Clarification: {'WORKING' if frequency_working else 'FAILING'}")
        
        print()
        
        # Final assessment
        working_scenarios = sum([temporal_working, pain_working, abbreviation_working, 
                               trigger_working, family_working, frequency_working])
        
        if success_rate >= 85 and working_scenarios >= 5:
            print("🎉 ASSESSMENT: STEP 4.2 ENHANCED INTELLIGENT FOLLOW-UP SYSTEM IS FULLY FUNCTIONAL!")
            print("   The enhanced incompleteness detection and intelligent follow-up generation")
            print("   system is working correctly across all major scenario types with")
            print("   contextually relevant and medically appropriate responses.")
        elif success_rate >= 70 and working_scenarios >= 4:
            print("✅ ASSESSMENT: STEP 4.2 ENHANCED SYSTEM IS MOSTLY FUNCTIONAL")
            print("   Most enhanced scenarios are working but some areas need refinement.")
        elif success_rate >= 50 and working_scenarios >= 3:
            print("⚠️  ASSESSMENT: STEP 4.2 ENHANCED SYSTEM IS PARTIALLY FUNCTIONAL")
            print("   Some enhanced scenarios are working but significant improvements needed.")
        else:
            print("❌ ASSESSMENT: STEP 4.2 ENHANCED SYSTEM NEEDS MAJOR IMPROVEMENTS")
            print("   Most enhanced scenarios are not working as expected.")
        
        print()
        print(f"Test Completion Time: {datetime.now().isoformat()}")
        print("=" * 100)

async def main():
    """Main test execution function"""
    tester = Step42EnhancedFollowUpTester()
    await tester.run_comprehensive_tests()

if __name__ == "__main__":
    asyncio.run(main())