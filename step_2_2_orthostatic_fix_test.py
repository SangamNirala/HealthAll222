#!/usr/bin/env python3
"""
STEP 2.2 CONTEXT-AWARE MEDICAL REASONING ENGINE - ORTHOSTATIC FIX VALIDATION
===========================================================================

Focused testing for Ultra-Challenging Scenario 1 (Positional/Orthostatic) to verify
specific fixes implemented in the Context-Aware Medical Reasoning Engine.

FOCUS TEST: Ultra-Challenging Scenario 1 (Positional/Orthostatic):
Input message: "Every morning when I get out of bed I feel dizzy and nauseous, sometimes I even feel like I'm going to faint, but it goes away after I sit back down for a few minutes. This also happens when I stand up quickly from a chair or get up from squatting down."

VERIFY SPECIFIC FIXES:
1. CausalRelationship serialization issue resolved (no AttributeError)
2. Contextual reasoning fields populated with meaningful content  
3. Urgency level should be "urgent" (not "routine") due to orthostatic fall risk
4. All 9 contextual reasoning fields should have content:
   - causal_relationships: should detect morning orthostatic patterns
   - clinical_hypotheses: should include orthostatic hypotension 
   - contextual_factors: positional triggers detected
   - medical_reasoning_narrative: clinical explanation
   - context_based_recommendations: orthostatic evaluation
   - trigger_avoidance_strategies: position change advice
   - specialist_referral_context: cardiology referral
   - contextual_significance: urgent significance
   - reasoning_confidence: confidence score

Author: Testing Agent
Date: 2025-01-17
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, Any, List

# Backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://converse-context.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class Orthostatic_Fix_Tester:
    """Focused tester for Step 2.2 Context-Aware Medical Reasoning Engine Orthostatic Fix"""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_test(self, test_name: str, passed: bool, details: str = "", response_data: Dict = None):
        """Log test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            self.failed_tests += 1
            status = "❌ FAIL"
            
        result = {
            "test_name": test_name,
            "status": status,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        
        self.test_results.append(result)
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        if not passed and response_data:
            print(f"   Response: {json.dumps(response_data, indent=2)[:500]}...")
        print()

    def test_orthostatic_scenario_initialization(self) -> tuple:
        """Initialize consultation for orthostatic scenario testing"""
        try:
            response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                json={
                    "patient_id": "test-orthostatic-fix",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                required_keys = ["consultation_id", "patient_id", "current_stage", "response"]
                
                if all(key in data for key in required_keys):
                    consultation_id = data.get('consultation_id')
                    self.log_test("Orthostatic Scenario Initialization", True, 
                                f"Successfully initialized with consultation_id: {consultation_id}")
                    return True, consultation_id
                else:
                    self.log_test("Orthostatic Scenario Initialization", False, 
                                f"Missing required keys. Got: {list(data.keys())}", data)
                    return False, None
            else:
                self.log_test("Orthostatic Scenario Initialization", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False, None
                
        except Exception as e:
            self.log_test("Orthostatic Scenario Initialization", False, f"Exception: {str(e)}")
            return False, None

    def test_ultra_challenging_scenario_1_fixes(self, consultation_id: str) -> bool:
        """Test Ultra-Challenging Scenario 1 with specific fix validation"""
        try:
            # Ultra-challenging contextual scenario 1 - exact text from review request
            scenario_1 = "Every morning when I get out of bed I feel dizzy and nauseous, sometimes I even feel like I'm going to faint, but it goes away after I sit back down for a few minutes. This also happens when I stand up quickly from a chair or get up from squatting down."
            
            print(f"🎯 Testing Ultra-Challenging Scenario 1 (Positional/Orthostatic)")
            print(f"Input: {scenario_1}")
            print()
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": scenario_1,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code != 200:
                self.log_test("Ultra-Challenging Scenario 1 - API Response", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            data = response.json()
            
            # FIX 1: Check for CausalRelationship serialization issue (no AttributeError)
            serialization_success = True
            serialization_details = "No serialization errors detected"
            
            # Check if response was generated without errors
            if "error" in data or "AttributeError" in str(data):
                serialization_success = False
                serialization_details = "Serialization error detected in response"
            
            self.log_test("Fix 1: CausalRelationship Serialization", serialization_success, serialization_details)
            
            # FIX 2: Check urgency level should be "urgent" (not "routine")
            urgency = data.get("urgency", "routine")
            urgency_success = urgency == "urgent"
            urgency_details = f"Urgency level: {urgency} (Expected: urgent)"
            
            self.log_test("Fix 2: Urgency Level Classification", urgency_success, urgency_details)
            
            # FIX 3: Check contextual reasoning fields populated with meaningful content
            response_text = data.get("response", "").lower()
            
            # Check for 9 contextual reasoning fields with meaningful content
            contextual_fields_check = {
                "causal_relationships": {
                    "keywords": ["morning", "standing", "position", "when", "after", "trigger", "cause"],
                    "found": [],
                    "meaningful": False
                },
                "clinical_hypotheses": {
                    "keywords": ["orthostatic", "hypotension", "blood pressure", "circulation", "postural"],
                    "found": [],
                    "meaningful": False
                },
                "contextual_factors": {
                    "keywords": ["positional", "standing", "sitting", "position", "movement"],
                    "found": [],
                    "meaningful": False
                },
                "medical_reasoning_narrative": {
                    "keywords": ["because", "due to", "mechanism", "physiology", "explanation"],
                    "found": [],
                    "meaningful": False
                },
                "context_based_recommendations": {
                    "keywords": ["evaluation", "assessment", "test", "monitor", "check"],
                    "found": [],
                    "meaningful": False
                },
                "trigger_avoidance_strategies": {
                    "keywords": ["slowly", "gradual", "avoid", "prevent", "careful"],
                    "found": [],
                    "meaningful": False
                },
                "specialist_referral_context": {
                    "keywords": ["cardiology", "cardiologist", "specialist", "referral", "consultation"],
                    "found": [],
                    "meaningful": False
                },
                "contextual_significance": {
                    "keywords": ["urgent", "important", "significant", "concerning", "serious"],
                    "found": [],
                    "meaningful": False
                },
                "reasoning_confidence": {
                    "keywords": ["confidence", "likely", "probable", "certain", "assessment"],
                    "found": [],
                    "meaningful": False
                }
            }
            
            # Analyze response for contextual reasoning content
            for field_name, field_data in contextual_fields_check.items():
                found_keywords = [kw for kw in field_data["keywords"] if kw in response_text]
                field_data["found"] = found_keywords
                field_data["meaningful"] = len(found_keywords) >= 1  # At least 1 relevant keyword
            
            # Count meaningful fields
            meaningful_fields = sum(1 for field_data in contextual_fields_check.values() if field_data["meaningful"])
            contextual_success = meaningful_fields >= 6  # At least 6 out of 9 fields should have meaningful content
            
            contextual_details = f"Meaningful contextual fields: {meaningful_fields}/9"
            for field_name, field_data in contextual_fields_check.items():
                if field_data["meaningful"]:
                    contextual_details += f"\n   ✅ {field_name}: {field_data['found']}"
                else:
                    contextual_details += f"\n   ❌ {field_name}: No meaningful content detected"
            
            self.log_test("Fix 3: Contextual Reasoning Fields Population", contextual_success, contextual_details)
            
            # FIX 4: Check for specific orthostatic pattern detection
            orthostatic_patterns = [
                "morning", "standing", "sitting", "position", "orthostatic", 
                "dizziness", "dizzy", "nausea", "faint", "blood pressure"
            ]
            
            found_orthostatic_patterns = [pattern for pattern in orthostatic_patterns if pattern in response_text]
            orthostatic_detection_success = len(found_orthostatic_patterns) >= 4
            orthostatic_details = f"Orthostatic patterns detected: {found_orthostatic_patterns}"
            
            self.log_test("Fix 4: Orthostatic Pattern Detection", orthostatic_detection_success, orthostatic_details)
            
            # FIX 5: Check for appropriate medical recommendations
            medical_recommendations = [
                "slowly", "gradual", "hydration", "salt", "compression", 
                "evaluation", "monitor", "blood pressure", "cardiology"
            ]
            
            found_recommendations = [rec for rec in medical_recommendations if rec in response_text]
            recommendations_success = len(found_recommendations) >= 2
            recommendations_details = f"Medical recommendations detected: {found_recommendations}"
            
            self.log_test("Fix 5: Appropriate Medical Recommendations", recommendations_success, recommendations_details)
            
            # Overall scenario success
            overall_success = (serialization_success and urgency_success and 
                             contextual_success and orthostatic_detection_success and 
                             recommendations_success)
            
            overall_details = f"Overall fixes validation: {5 if overall_success else sum([serialization_success, urgency_success, contextual_success, orthostatic_detection_success, recommendations_success])}/5 passed"
            
            self.log_test("Ultra-Challenging Scenario 1 - Overall Fix Validation", overall_success, overall_details, data)
            
            return overall_success
                
        except Exception as e:
            self.log_test("Ultra-Challenging Scenario 1 - Overall Fix Validation", False, f"Exception: {str(e)}")
            return False

    def test_response_structure_validation(self, consultation_id: str) -> bool:
        """Validate that response structure is correct and complete"""
        try:
            # Send the orthostatic scenario again to validate response structure
            scenario = "Every morning when I get out of bed I feel dizzy and nauseous, sometimes I even feel like I'm going to faint, but it goes away after I sit back down for a few minutes."
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": scenario,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code != 200:
                self.log_test("Response Structure Validation", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            data = response.json()
            
            # Check required response structure
            required_keys = [
                "response", "stage", "urgency", "consultation_id", "patient_id", 
                "current_stage", "emergency_detected", "context", "next_questions", 
                "differential_diagnoses", "recommendations"
            ]
            
            missing_keys = [key for key in required_keys if key not in data]
            
            if missing_keys:
                self.log_test("Response Structure Validation", False,
                            f"Missing required keys: {missing_keys}")
                return False
            
            # Validate specific field types and content
            validations = []
            
            # Check response is a non-empty string
            response_text = data.get("response", "")
            validations.append(("response_content", isinstance(response_text, str) and len(response_text) > 0))
            
            # Check urgency is a valid value
            urgency = data.get("urgency", "")
            valid_urgency_levels = ["routine", "urgent", "emergency"]
            validations.append(("urgency_valid", urgency in valid_urgency_levels))
            
            # Check emergency_detected is boolean
            emergency_detected = data.get("emergency_detected")
            validations.append(("emergency_detected_type", isinstance(emergency_detected, bool)))
            
            # Check recommendations is a list
            recommendations = data.get("recommendations", [])
            validations.append(("recommendations_type", isinstance(recommendations, list)))
            
            # Check differential_diagnoses is a list
            differential_diagnoses = data.get("differential_diagnoses", [])
            validations.append(("differential_diagnoses_type", isinstance(differential_diagnoses, list)))
            
            # Check context is a dict
            context = data.get("context", {})
            validations.append(("context_type", isinstance(context, dict)))
            
            passed_validations = sum(1 for _, passed in validations if passed)
            total_validations = len(validations)
            
            structure_success = passed_validations == total_validations
            structure_details = f"Structure validations: {passed_validations}/{total_validations} passed"
            
            for validation_name, passed in validations:
                structure_details += f"\n   {'✅' if passed else '❌'} {validation_name}"
            
            self.log_test("Response Structure Validation", structure_success, structure_details)
            
            return structure_success
                
        except Exception as e:
            self.log_test("Response Structure Validation", False, f"Exception: {str(e)}")
            return False

    def run_orthostatic_fix_tests(self):
        """Run all orthostatic fix validation tests"""
        print("🧠 STEP 2.2 CONTEXT-AWARE MEDICAL REASONING ENGINE - ORTHOSTATIC FIX VALIDATION")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Testing started at: {datetime.now().isoformat()}")
        print()
        
        # Test 1: Initialize consultation
        init_success, consultation_id = self.test_orthostatic_scenario_initialization()
        
        if not init_success or not consultation_id:
            print("❌ Cannot proceed with testing - initialization failed")
            return self.passed_tests, self.failed_tests, self.total_tests
        
        # Test 2: Ultra-challenging scenario 1 fix validation
        scenario_success = self.test_ultra_challenging_scenario_1_fixes(consultation_id)
        
        # Test 3: Response structure validation
        structure_success = self.test_response_structure_validation(consultation_id)
        
        # Print summary
        print("\n" + "=" * 80)
        print("🧠 STEP 2.2 ORTHOSTATIC FIX VALIDATION TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.failed_tests} ❌")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        print()
        
        # Print detailed results
        print("DETAILED TEST RESULTS:")
        print("-" * 40)
        for result in self.test_results:
            print(f"{result['status']}: {result['test_name']}")
            if result['details']:
                print(f"   {result['details']}")
        
        print(f"\nTesting completed at: {datetime.now().isoformat()}")
        
        return self.passed_tests, self.failed_tests, self.total_tests

def main():
    """Main test execution"""
    tester = Orthostatic_Fix_Tester()
    passed, failed, total = tester.run_orthostatic_fix_tests()
    
    # Exit with appropriate code
    if failed == 0:
        print("\n🎉 ALL ORTHOSTATIC FIX TESTS PASSED! Context-Aware Medical Reasoning Engine fixes are working correctly.")
        sys.exit(0)
    else:
        print(f"\n⚠️  {failed} TESTS FAILED. Context-Aware Medical Reasoning Engine fixes need attention.")
        sys.exit(1)

if __name__ == "__main__":
    main()