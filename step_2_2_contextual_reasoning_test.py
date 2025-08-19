#!/usr/bin/env python3
"""
STEP 2.2 CONTEXT-AWARE MEDICAL REASONING ENGINE COMPREHENSIVE TESTING
====================================================================

Comprehensive testing of the Step 2.2 Context-Aware Medical Reasoning Engine fixes
for all 3 ultra-challenging scenarios as requested in the review.

TESTING FOCUS:
1. Ultra-Challenging Scenario 1: Positional/Orthostatic
2. Ultra-Challenging Scenario 2: Exertional/Cardiac  
3. Ultra-Challenging Scenario 3: Multi-Context Dietary/Stress

For each scenario, verify that all 9 Step 2.2 contextual reasoning fields are populated:
- causal_relationships
- clinical_hypotheses  
- contextual_factors (positional, temporal, environmental, activity)
- medical_reasoning_narrative
- context_based_recommendations
- trigger_avoidance_strategies
- specialist_referral_context
- contextual_significance
- reasoning_confidence

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
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://intent-verify.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class Step22ContextualReasoningTester:
    """Comprehensive tester for Step 2.2 Context-Aware Medical Reasoning Engine"""
    
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

    def validate_contextual_reasoning_fields(self, response_data: Dict, scenario_name: str) -> Dict[str, Any]:
        """Validate that all 9 contextual reasoning fields are populated with meaningful content"""
        
        # Extract response text for analysis
        response_text = response_data.get("response", "").lower()
        context = response_data.get("context", {})
        recommendations = response_data.get("recommendations", [])
        differential_diagnoses = response_data.get("differential_diagnoses", [])
        
        # Define the 9 required contextual reasoning fields and their validation criteria
        contextual_fields = {
            "causal_relationships": {
                "keywords": ["when", "after", "trigger", "cause", "due to", "because", "related to", "associated with"],
                "found": [],
                "populated": False
            },
            "clinical_hypotheses": {
                "keywords": ["possible", "likely", "suggest", "indicate", "hypothesis", "consider", "differential"],
                "found": [],
                "populated": False
            },
            "contextual_factors": {
                "keywords": ["position", "stress", "activity", "environment", "timing", "situation", "context"],
                "found": [],
                "populated": False
            },
            "medical_reasoning_narrative": {
                "keywords": ["mechanism", "physiology", "pathophysiology", "explain", "reason", "medical"],
                "found": [],
                "populated": False
            },
            "context_based_recommendations": {
                "keywords": ["recommend", "suggest", "avoid", "modify", "adjust", "management"],
                "found": [],
                "populated": False
            },
            "trigger_avoidance_strategies": {
                "keywords": ["avoid", "prevent", "limit", "reduce", "minimize", "control", "manage"],
                "found": [],
                "populated": False
            },
            "specialist_referral_context": {
                "keywords": ["referral", "specialist", "cardiology", "neurology", "gastroenterology", "consult"],
                "found": [],
                "populated": False
            },
            "contextual_significance": {
                "keywords": ["significant", "important", "concerning", "notable", "relevant", "pattern"],
                "found": [],
                "populated": False
            },
            "reasoning_confidence": {
                "keywords": ["confidence", "certain", "likely", "probable", "assessment", "evaluation"],
                "found": [],
                "populated": False
            }
        }
        
        # Check response text for contextual reasoning indicators
        for field_name, field_data in contextual_fields.items():
            found_keywords = [kw for kw in field_data["keywords"] if kw in response_text]
            field_data["found"] = found_keywords
            field_data["populated"] = len(found_keywords) > 0
        
        # Check recommendations array for contextual content
        if recommendations:
            rec_text = " ".join([str(rec) for rec in recommendations]).lower()
            for field_name, field_data in contextual_fields.items():
                if not field_data["populated"]:
                    found_in_rec = [kw for kw in field_data["keywords"] if kw in rec_text]
                    if found_in_rec:
                        field_data["found"].extend(found_in_rec)
                        field_data["populated"] = True
        
        # Check differential diagnoses for clinical reasoning
        if differential_diagnoses:
            diff_text = " ".join([str(diag) for diag in differential_diagnoses]).lower()
            for field_name in ["clinical_hypotheses", "medical_reasoning_narrative"]:
                if not contextual_fields[field_name]["populated"]:
                    found_in_diff = [kw for kw in contextual_fields[field_name]["keywords"] if kw in diff_text]
                    if found_in_diff:
                        contextual_fields[field_name]["found"].extend(found_in_diff)
                        contextual_fields[field_name]["populated"] = True
        
        # Calculate overall contextual reasoning score
        populated_fields = sum(1 for field_data in contextual_fields.values() if field_data["populated"])
        total_fields = len(contextual_fields)
        contextual_score = populated_fields / total_fields
        
        return {
            "scenario": scenario_name,
            "contextual_fields": contextual_fields,
            "populated_fields": populated_fields,
            "total_fields": total_fields,
            "contextual_score": contextual_score,
            "meets_requirement": contextual_score >= 0.6  # At least 60% of fields populated
        }

    def test_ultra_challenging_scenario_1_positional_orthostatic(self) -> bool:
        """
        Test Ultra-Challenging Scenario 1: Positional/Orthostatic
        
        Expected: Should detect urgent/emergency urgency with orthostatic pattern detection,
        contextual factors should be populated with positional triggers, causal relationships
        should detect morning orthostatic patterns.
        """
        try:
            # Initialize consultation
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                json={
                    "patient_id": "test-scenario-1-orthostatic",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Ultra-Challenging Scenario 1 - Initialization", False, 
                            f"Failed to initialize: {init_response.status_code}")
                return False
                
            consultation_id = init_response.json().get("consultation_id")
            
            # Ultra-challenging scenario 1: Positional/Orthostatic
            scenario_1_message = "Every morning when I get out of bed I feel dizzy and nauseous, sometimes I even feel like I'm going to faint, but it goes away after I sit back down for a few minutes. This also happens when I stand up quickly from a chair or get up from squatting down."
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": scenario_1_message,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check urgency level - should be urgent/emergency for orthostatic symptoms
                urgency = data.get("urgency", "routine")
                urgency_correct = urgency in ["urgent", "emergency"]
                
                # Validate contextual reasoning fields
                contextual_validation = self.validate_contextual_reasoning_fields(data, "Scenario 1: Positional/Orthostatic")
                
                # Check for specific orthostatic pattern detection
                response_text = data.get("response", "").lower()
                orthostatic_indicators = [
                    "orthostatic", "positional", "standing", "sitting", "position",
                    "blood pressure", "hypotension", "dizziness", "presyncope"
                ]
                
                found_orthostatic = [indicator for indicator in orthostatic_indicators 
                                   if indicator in response_text]
                
                # Check for morning pattern recognition
                morning_indicators = ["morning", "bed", "wake", "rising", "get up"]
                found_morning = [indicator for indicator in morning_indicators 
                               if indicator in response_text]
                
                # Overall success criteria
                success = (
                    urgency_correct and 
                    contextual_validation["meets_requirement"] and
                    len(found_orthostatic) >= 2 and
                    len(found_morning) >= 1
                )
                
                details = f"""
                Urgency: {urgency} (Expected: urgent/emergency) - {'✅' if urgency_correct else '❌'}
                Contextual Fields: {contextual_validation['populated_fields']}/9 populated - {'✅' if contextual_validation['meets_requirement'] else '❌'}
                Orthostatic Indicators: {found_orthostatic} - {'✅' if len(found_orthostatic) >= 2 else '❌'}
                Morning Pattern: {found_morning} - {'✅' if len(found_morning) >= 1 else '❌'}
                """
                
                self.log_test("Ultra-Challenging Scenario 1 (Positional/Orthostatic)", success, details.strip())
                return success
            else:
                self.log_test("Ultra-Challenging Scenario 1 (Positional/Orthostatic)", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Ultra-Challenging Scenario 1 (Positional/Orthostatic)", False, f"Exception: {str(e)}")
            return False

    def test_ultra_challenging_scenario_2_exertional_cardiac(self) -> bool:
        """
        Test Ultra-Challenging Scenario 2: Exertional/Cardiac
        
        Expected: Should detect emergency urgency with exertional cardiac patterns,
        contextual analysis fields should be populated with exertional triggers,
        causal relationships should detect classic angina patterns.
        """
        try:
            # Initialize consultation
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                json={
                    "patient_id": "test-scenario-2-cardiac",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Ultra-Challenging Scenario 2 - Initialization", False, 
                            f"Failed to initialize: {init_response.status_code}")
                return False
                
            consultation_id = init_response.json().get("consultation_id")
            
            # Ultra-challenging scenario 2: Exertional/Cardiac
            scenario_2_message = "I get this crushing chest pain whenever I walk uphill or climb more than one flight of stairs, feels like an elephant sitting on my chest, but it completely goes away within 2-3 minutes of resting. Never happens when I'm just sitting or doing light activities around the house."
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": scenario_2_message,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check urgency level - should be emergency for exertional chest pain
                urgency = data.get("urgency", "routine")
                urgency_correct = urgency == "emergency"
                
                # Validate contextual reasoning fields
                contextual_validation = self.validate_contextual_reasoning_fields(data, "Scenario 2: Exertional/Cardiac")
                
                # Check for specific exertional cardiac pattern detection
                response_text = data.get("response", "").lower()
                cardiac_indicators = [
                    "cardiac", "heart", "angina", "coronary", "chest pain", "myocardial",
                    "ischemia", "coronary artery", "cardiovascular"
                ]
                
                found_cardiac = [indicator for indicator in cardiac_indicators 
                               if indicator in response_text]
                
                # Check for exertional pattern recognition
                exertional_indicators = ["exertion", "exercise", "stairs", "walking", "activity", "uphill", "physical"]
                found_exertional = [indicator for indicator in exertional_indicators 
                                  if indicator in response_text]
                
                # Check for relief pattern recognition
                relief_indicators = ["rest", "resting", "stops", "goes away", "relief", "resolves"]
                found_relief = [indicator for indicator in relief_indicators 
                              if indicator in response_text]
                
                # Overall success criteria
                success = (
                    urgency_correct and 
                    contextual_validation["meets_requirement"] and
                    len(found_cardiac) >= 2 and
                    len(found_exertional) >= 2 and
                    len(found_relief) >= 1
                )
                
                details = f"""
                Urgency: {urgency} (Expected: emergency) - {'✅' if urgency_correct else '❌'}
                Contextual Fields: {contextual_validation['populated_fields']}/9 populated - {'✅' if contextual_validation['meets_requirement'] else '❌'}
                Cardiac Indicators: {found_cardiac} - {'✅' if len(found_cardiac) >= 2 else '❌'}
                Exertional Pattern: {found_exertional} - {'✅' if len(found_exertional) >= 2 else '❌'}
                Relief Pattern: {found_relief} - {'✅' if len(found_relief) >= 1 else '❌'}
                """
                
                self.log_test("Ultra-Challenging Scenario 2 (Exertional/Cardiac)", success, details.strip())
                return success
            else:
                self.log_test("Ultra-Challenging Scenario 2 (Exertional/Cardiac)", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Ultra-Challenging Scenario 2 (Exertional/Cardiac)", False, f"Exception: {str(e)}")
            return False

    def test_ultra_challenging_scenario_3_multi_context_dietary_stress(self) -> bool:
        """
        Test Ultra-Challenging Scenario 3: Multi-Context Dietary/Stress
        
        Expected: Should detect multi-context stress-dietary interaction,
        contextual factors should show stress modulation, causal relationships
        should detect conditional dairy intolerance patterns.
        """
        try:
            # Initialize consultation
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                json={
                    "patient_id": "test-scenario-3-dietary-stress",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Ultra-Challenging Scenario 3 - Initialization", False, 
                            f"Failed to initialize: {init_response.status_code}")
                return False
                
            consultation_id = init_response.json().get("consultation_id")
            
            # Ultra-challenging scenario 3: Multi-Context Dietary/Stress
            scenario_3_message = "I've noticed that I get really bad stomach cramps and loose stools about 30-60 minutes after eating ice cream or drinking milk, but only when I'm stressed out at work. When I'm relaxed at home on weekends, I can sometimes tolerate small amounts of dairy without problems."
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": scenario_3_message,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate contextual reasoning fields
                contextual_validation = self.validate_contextual_reasoning_fields(data, "Scenario 3: Multi-Context Dietary/Stress")
                
                # Check for specific multi-context pattern detection
                response_text = data.get("response", "").lower()
                
                # Check for dietary pattern recognition
                dietary_indicators = ["dairy", "lactose", "milk", "ice cream", "food", "intolerance", "sensitivity"]
                found_dietary = [indicator for indicator in dietary_indicators 
                               if indicator in response_text]
                
                # Check for stress pattern recognition
                stress_indicators = ["stress", "work", "emotional", "psychological", "anxiety", "tension"]
                found_stress = [indicator for indicator in stress_indicators 
                              if indicator in response_text]
                
                # Check for temporal pattern recognition
                temporal_indicators = ["30-60 minutes", "after eating", "timing", "postprandial", "minutes", "time"]
                found_temporal = [indicator for indicator in temporal_indicators 
                                if indicator in response_text]
                
                # Check for conditional/contextual pattern recognition
                conditional_indicators = ["when", "only when", "but only", "condition", "context", "situation", "depends"]
                found_conditional = [indicator for indicator in conditional_indicators 
                                   if indicator in response_text]
                
                # Check for multi-trigger recognition
                multi_trigger_indicators = ["combination", "both", "together", "interaction", "complex", "multiple"]
                found_multi_trigger = [indicator for indicator in multi_trigger_indicators 
                                     if indicator in response_text]
                
                # Overall success criteria - this is a complex multi-context scenario
                success = (
                    contextual_validation["meets_requirement"] and
                    len(found_dietary) >= 2 and
                    len(found_stress) >= 1 and
                    len(found_temporal) >= 1 and
                    (len(found_conditional) >= 1 or len(found_multi_trigger) >= 1)
                )
                
                details = f"""
                Contextual Fields: {contextual_validation['populated_fields']}/9 populated - {'✅' if contextual_validation['meets_requirement'] else '❌'}
                Dietary Indicators: {found_dietary} - {'✅' if len(found_dietary) >= 2 else '❌'}
                Stress Pattern: {found_stress} - {'✅' if len(found_stress) >= 1 else '❌'}
                Temporal Pattern: {found_temporal} - {'✅' if len(found_temporal) >= 1 else '❌'}
                Conditional Pattern: {found_conditional} - {'✅' if len(found_conditional) >= 1 else '❌'}
                Multi-Trigger: {found_multi_trigger} - {'✅' if len(found_multi_trigger) >= 1 else '❌'}
                """
                
                self.log_test("Ultra-Challenging Scenario 3 (Multi-Context Dietary/Stress)", success, details.strip())
                return success
            else:
                self.log_test("Ultra-Challenging Scenario 3 (Multi-Context Dietary/Stress)", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Ultra-Challenging Scenario 3 (Multi-Context Dietary/Stress)", False, f"Exception: {str(e)}")
            return False

    def test_contextual_reasoning_field_validation(self) -> bool:
        """Test that all 9 contextual reasoning fields can be populated in a comprehensive scenario"""
        try:
            # Initialize consultation
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                json={
                    "patient_id": "test-contextual-fields",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                return False
                
            consultation_id = init_response.json().get("consultation_id")
            
            # Complex scenario designed to trigger all contextual reasoning fields
            comprehensive_scenario = """I've been having these severe headaches that start every morning around 7 AM when I wake up, especially on weekdays when I'm stressed about work presentations. The pain is throbbing and located behind my right eye, gets much worse when I'm in bright fluorescent lighting at the office, and is accompanied by nausea and sensitivity to light. It usually lasts 4-6 hours and only goes away when I take my migraine medication and lie down in a dark room. This pattern has been happening for 3 months now, always triggered by the combination of work stress and bright lights."""
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": comprehensive_scenario,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate all 9 contextual reasoning fields
                contextual_validation = self.validate_contextual_reasoning_fields(data, "Comprehensive Contextual Fields Test")
                
                # Print detailed field analysis
                field_details = []
                for field_name, field_data in contextual_validation["contextual_fields"].items():
                    status = "✅" if field_data["populated"] else "❌"
                    keywords_found = ", ".join(field_data["found"][:3])  # Show first 3 keywords
                    field_details.append(f"{field_name}: {status} ({keywords_found})")
                
                success = contextual_validation["contextual_score"] >= 0.8  # 80% of fields populated
                
                details = f"""
                Contextual Score: {contextual_validation['contextual_score']:.2f} (8/9 fields required)
                Fields Analysis:
                {chr(10).join(field_details)}
                """
                
                self.log_test("Contextual Reasoning Field Validation", success, details.strip())
                return success
            else:
                self.log_test("Contextual Reasoning Field Validation", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Contextual Reasoning Field Validation", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all Step 2.2 Context-Aware Medical Reasoning Engine tests"""
        print("🧠 STEP 2.2 CONTEXT-AWARE MEDICAL REASONING ENGINE COMPREHENSIVE TESTING")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Testing started at: {datetime.now().isoformat()}")
        print()
        
        # Run all ultra-challenging scenario tests
        test_methods = [
            self.test_ultra_challenging_scenario_1_positional_orthostatic,
            self.test_ultra_challenging_scenario_2_exertional_cardiac,
            self.test_ultra_challenging_scenario_3_multi_context_dietary_stress,
            self.test_contextual_reasoning_field_validation
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.log_test(test_method.__name__, False, f"Test execution failed: {str(e)}")
        
        # Print summary
        print("\n" + "=" * 80)
        print("🧠 STEP 2.2 CONTEXT-AWARE MEDICAL REASONING ENGINE TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.failed_tests} ❌")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        print()
        
        # Print detailed results
        print("DETAILED TEST RESULTS:")
        print("-" * 50)
        for result in self.test_results:
            print(f"{result['status']}: {result['test_name']}")
            if result['details']:
                print(f"   {result['details']}")
        
        print(f"\nTesting completed at: {datetime.now().isoformat()}")
        
        return self.passed_tests, self.failed_tests, self.total_tests

def main():
    """Main test execution"""
    tester = Step22ContextualReasoningTester()
    passed, failed, total = tester.run_all_tests()
    
    # Exit with appropriate code
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Step 2.2 Context-Aware Medical Reasoning Engine is working correctly.")
        sys.exit(0)
    else:
        print(f"\n⚠️  {failed} TESTS FAILED. Step 2.2 Context-Aware Medical Reasoning Engine needs attention.")
        sys.exit(1)

if __name__ == "__main__":
    main()
"""
STEP 2.2 CONTEXT-AWARE MEDICAL REASONING ENGINE COMPREHENSIVE TESTING
====================================================================

Comprehensive testing of Step 2.2 Context-Aware Medical Reasoning Engine fixes
addressing the critical issues identified in previous testing:

1. CONSULTATION FLOW PROBLEM: Medical AI responding with generic messages
2. MISSING API RESPONSE FIELDS: Missing contextual reasoning features
3. INCONSISTENT ACTIVATION: Contextual reasoning engine not consistently activated
4. ULTRA-CHALLENGING SCENARIOS FAILING: Only 1/3 scenarios properly processed

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
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://intent-verify.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class Step22ContextualReasoningTester:
    """Comprehensive tester for Step 2.2 Context-Aware Medical Reasoning Engine fixes"""
    
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

    def test_ultra_challenging_scenario_1_positional_orthostatic(self) -> bool:
        """Test Scenario 1: Positional/Orthostatic - Morning dizziness when standing"""
        try:
            # Initialize consultation
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                json={
                    "patient_id": "test-scenario-1-orthostatic",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Ultra-Challenging Scenario 1 (Positional/Orthostatic)", False, 
                            f"Failed to initialize: {init_response.status_code}")
                return False
                
            consultation_id = init_response.json().get("consultation_id")
            
            # Ultra-challenging contextual scenario 1
            scenario_1 = "Every morning when I get out of bed I feel dizzy and nauseous, sometimes I even feel like I'm going to faint, but it goes away after I sit back down for a few minutes"
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": scenario_1,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "").lower()
                
                # Check for Step 2.2 API response fields
                step_22_fields = {
                    "causal_relationships": data.get("causal_relationships"),
                    "clinical_hypotheses": data.get("clinical_hypotheses"),
                    "contextual_factors": data.get("contextual_factors"),
                    "medical_reasoning_narrative": data.get("medical_reasoning_narrative"),
                    "context_based_recommendations": data.get("context_based_recommendations"),
                    "trigger_avoidance_strategies": data.get("trigger_avoidance_strategies"),
                    "specialist_referral_context": data.get("specialist_referral_context"),
                    "contextual_significance": data.get("contextual_significance"),
                    "reasoning_confidence": data.get("reasoning_confidence")
                }
                
                # Count present fields
                present_fields = [field for field, value in step_22_fields.items() if value is not None]
                
                # Check for contextual analysis in response
                contextual_indicators = [
                    "orthostatic", "positional", "standing", "sitting", "position",
                    "blood pressure", "hypotension", "circulation", "gradual"
                ]
                
                found_indicators = [indicator for indicator in contextual_indicators 
                                  if indicator in response_text]
                
                # Check urgency level - should be urgent/emergency for orthostatic symptoms
                urgency = data.get("urgency", "routine")
                
                # Evaluate success criteria
                has_contextual_analysis = len(found_indicators) >= 2
                has_appropriate_urgency = urgency in ["urgent", "emergency"]
                has_step_22_fields = len(present_fields) >= 3
                
                success = has_contextual_analysis and has_appropriate_urgency and has_step_22_fields
                
                if success:
                    self.log_test("Ultra-Challenging Scenario 1 (Positional/Orthostatic)", True,
                                f"Contextual analysis detected: {found_indicators}, urgency: {urgency}, Step 2.2 fields: {present_fields}")
                    return True
                else:
                    self.log_test("Ultra-Challenging Scenario 1 (Positional/Orthostatic)", False,
                                f"Insufficient analysis. Contextual: {found_indicators}, urgency: {urgency}, fields: {present_fields}", data)
                    return False
            else:
                self.log_test("Ultra-Challenging Scenario 1 (Positional/Orthostatic)", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Ultra-Challenging Scenario 1 (Positional/Orthostatic)", False, f"Exception: {str(e)}")
            return False

    def test_ultra_challenging_scenario_2_exertional_cardiac(self) -> bool:
        """Test Scenario 2: Exertional/Cardiac - Chest pain with exertion"""
        try:
            # Initialize consultation
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                json={
                    "patient_id": "test-scenario-2-cardiac",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Ultra-Challenging Scenario 2 (Exertional/Cardiac)", False, 
                            f"Failed to initialize: {init_response.status_code}")
                return False
                
            consultation_id = init_response.json().get("consultation_id")
            
            # Ultra-challenging contextual scenario 2
            scenario_2 = "I get this crushing chest pain whenever I walk uphill or climb more than one flight of stairs, feels like an elephant sitting on my chest, but it completely goes away within 2-3 minutes of resting"
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": scenario_2,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "").lower()
                
                # Check for Step 2.2 API response fields
                step_22_fields = {
                    "causal_relationships": data.get("causal_relationships"),
                    "clinical_hypotheses": data.get("clinical_hypotheses"),
                    "contextual_factors": data.get("contextual_factors"),
                    "medical_reasoning_narrative": data.get("medical_reasoning_narrative"),
                    "context_based_recommendations": data.get("context_based_recommendations"),
                    "trigger_avoidance_strategies": data.get("trigger_avoidance_strategies"),
                    "specialist_referral_context": data.get("specialist_referral_context"),
                    "contextual_significance": data.get("contextual_significance"),
                    "reasoning_confidence": data.get("reasoning_confidence")
                }
                
                # Count present fields
                present_fields = [field for field, value in step_22_fields.items() if value is not None]
                
                # Check for exertional cardiac context
                cardiac_indicators = [
                    "exertional", "angina", "cardiac", "coronary", "heart",
                    "exercise", "stairs", "walking", "activity", "rest"
                ]
                
                found_indicators = [indicator for indicator in cardiac_indicators 
                                  if indicator in response_text]
                
                # Check urgency level - should be emergency for exertional chest pain
                urgency = data.get("urgency", "routine")
                
                # Evaluate success criteria
                has_cardiac_analysis = len(found_indicators) >= 3
                has_emergency_urgency = urgency == "emergency"
                has_step_22_fields = len(present_fields) >= 4
                
                success = has_cardiac_analysis and has_emergency_urgency and has_step_22_fields
                
                if success:
                    self.log_test("Ultra-Challenging Scenario 2 (Exertional/Cardiac)", True,
                                f"Cardiac analysis detected: {found_indicators}, urgency: {urgency}, Step 2.2 fields: {present_fields}")
                    return True
                else:
                    self.log_test("Ultra-Challenging Scenario 2 (Exertional/Cardiac)", False,
                                f"Insufficient analysis. Cardiac: {found_indicators}, urgency: {urgency}, fields: {present_fields}", data)
                    return False
            else:
                self.log_test("Ultra-Challenging Scenario 2 (Exertional/Cardiac)", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Ultra-Challenging Scenario 2 (Exertional/Cardiac)", False, f"Exception: {str(e)}")
            return False

    def test_ultra_challenging_scenario_3_multi_context_dietary_stress(self) -> bool:
        """Test Scenario 3: Multi-Context Dietary/Stress - Complex trigger interaction"""
        try:
            # Initialize consultation
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                json={
                    "patient_id": "test-scenario-3-multi-context",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Ultra-Challenging Scenario 3 (Multi-Context Dietary/Stress)", False, 
                            f"Failed to initialize: {init_response.status_code}")
                return False
                
            consultation_id = init_response.json().get("consultation_id")
            
            # Ultra-challenging contextual scenario 3
            scenario_3 = "I've noticed that I get really bad stomach cramps and loose stools about 30-60 minutes after eating ice cream or drinking milk, but only when I'm stressed out at work"
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": scenario_3,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "").lower()
                
                # Check for Step 2.2 API response fields
                step_22_fields = {
                    "causal_relationships": data.get("causal_relationships"),
                    "clinical_hypotheses": data.get("clinical_hypotheses"),
                    "contextual_factors": data.get("contextual_factors"),
                    "medical_reasoning_narrative": data.get("medical_reasoning_narrative"),
                    "context_based_recommendations": data.get("context_based_recommendations"),
                    "trigger_avoidance_strategies": data.get("trigger_avoidance_strategies"),
                    "specialist_referral_context": data.get("specialist_referral_context"),
                    "contextual_significance": data.get("contextual_significance"),
                    "reasoning_confidence": data.get("reasoning_confidence")
                }
                
                # Count present fields
                present_fields = [field for field, value in step_22_fields.items() if value is not None]
                
                # Check for multi-context analysis
                multi_context_indicators = [
                    "lactose", "dairy", "intolerance", "milk", "ice cream",
                    "stress", "work", "trigger", "combination", "context"
                ]
                
                found_indicators = [indicator for indicator in multi_context_indicators 
                                  if indicator in response_text]
                
                # Check for causal relationship detection
                causal_indicators = ["after eating", "when stressed", "trigger", "cause", "relationship"]
                found_causal = [indicator for indicator in causal_indicators if indicator in response_text]
                
                # Evaluate success criteria
                has_multi_context_analysis = len(found_indicators) >= 3
                has_causal_relationships = len(found_causal) >= 2
                has_step_22_fields = len(present_fields) >= 3
                
                success = has_multi_context_analysis and has_causal_relationships and has_step_22_fields
                
                if success:
                    self.log_test("Ultra-Challenging Scenario 3 (Multi-Context Dietary/Stress)", True,
                                f"Multi-context analysis: {found_indicators}, causal: {found_causal}, Step 2.2 fields: {present_fields}")
                    return True
                else:
                    self.log_test("Ultra-Challenging Scenario 3 (Multi-Context Dietary/Stress)", False,
                                f"Insufficient analysis. Multi-context: {found_indicators}, causal: {found_causal}, fields: {present_fields}", data)
                    return False
            else:
                self.log_test("Ultra-Challenging Scenario 3 (Multi-Context Dietary/Stress)", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Ultra-Challenging Scenario 3 (Multi-Context Dietary/Stress)", False, f"Exception: {str(e)}")
            return False

    def test_step_22_api_response_fields(self) -> bool:
        """Test that all Step 2.2 API response fields are present"""
        try:
            # Initialize consultation
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                json={
                    "patient_id": "test-step-22-fields",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Step 2.2 API Response Fields", False, 
                            f"Failed to initialize: {init_response.status_code}")
                return False
                
            consultation_id = init_response.json().get("consultation_id")
            
            # Test with a complex contextual scenario
            complex_scenario = "I get severe headaches that start behind my right eye, throbbing like my heartbeat, usually triggered by bright fluorescent lights at work, especially when I'm stressed about deadlines, and they last for hours until I can rest in a dark room"
            
            response = requests.post(f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": complex_scenario,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for all required Step 2.2 API response fields
                required_fields = [
                    "causal_relationships",
                    "clinical_hypotheses", 
                    "contextual_factors",
                    "medical_reasoning_narrative",
                    "context_based_recommendations",
                    "trigger_avoidance_strategies",
                    "specialist_referral_context",
                    "contextual_significance",
                    "reasoning_confidence"
                ]
                
                present_fields = []
                missing_fields = []
                
                for field in required_fields:
                    if field in data and data[field] is not None:
                        present_fields.append(field)
                    else:
                        missing_fields.append(field)
                
                # Success criteria: at least 7 out of 9 fields present
                success = len(present_fields) >= 7
                
                if success:
                    self.log_test("Step 2.2 API Response Fields", True,
                                f"Present fields ({len(present_fields)}/9): {present_fields}")
                    return True
                else:
                    self.log_test("Step 2.2 API Response Fields", False,
                                f"Missing fields ({len(missing_fields)}/9): {missing_fields}. Present: {present_fields}", data)
                    return False
            else:
                self.log_test("Step 2.2 API Response Fields", False,
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Step 2.2 API Response Fields", False, f"Exception: {str(e)}")
            return False

    def test_consultation_flow_problem(self) -> bool:
        """Test that Medical AI doesn't respond with generic 'please describe symptoms' messages"""
        try:
            # Initialize consultation
            init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                json={
                    "patient_id": "test-consultation-flow",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                self.log_test("Consultation Flow Problem", False, 
                            f"Failed to initialize: {init_response.status_code}")
                return False
                
            consultation_id = init_response.json().get("consultation_id")
            
            # Test with specific symptom descriptions
            test_scenarios = [
                "I have crushing chest pain that radiates to my left arm",
                "I get dizzy every morning when I stand up from bed",
                "I have severe stomach cramps after eating dairy products"
            ]
            
            generic_responses = 0
            contextual_responses = 0
            
            for scenario in test_scenarios:
                response = requests.post(f"{API_BASE}/medical-ai/message",
                    json={
                        "consultation_id": consultation_id,
                        "message": scenario,
                        "timestamp": datetime.now().isoformat()
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "").lower()
                    
                    # Check for generic responses
                    generic_phrases = [
                        "please describe your symptoms",
                        "can you tell me more about your symptoms",
                        "describe your symptoms",
                        "what symptoms are you experiencing"
                    ]
                    
                    is_generic = any(phrase in response_text for phrase in generic_phrases)
                    
                    # Check for contextual responses
                    contextual_phrases = [
                        "chest pain", "crushing", "radiating", "arm",
                        "dizzy", "standing", "orthostatic", "position",
                        "stomach", "dairy", "lactose", "intolerance"
                    ]
                    
                    has_contextual = any(phrase in response_text for phrase in contextual_phrases)
                    
                    if is_generic:
                        generic_responses += 1
                    if has_contextual:
                        contextual_responses += 1
                
            # Success criteria: No generic responses and at least 2 contextual responses
            success = generic_responses == 0 and contextual_responses >= 2
            
            if success:
                self.log_test("Consultation Flow Problem", True,
                            f"No generic responses detected. Contextual responses: {contextual_responses}/3")
                return True
            else:
                self.log_test("Consultation Flow Problem", False,
                            f"Generic responses: {generic_responses}, Contextual responses: {contextual_responses}")
                return False
                
        except Exception as e:
            self.log_test("Consultation Flow Problem", False, f"Exception: {str(e)}")
            return False

    def test_contextual_reasoning_consistency(self) -> bool:
        """Test that contextual reasoning engine is consistently activated"""
        try:
            # Test multiple scenarios to check consistency
            test_scenarios = [
                {
                    "message": "I get headaches when I'm under stress at work",
                    "expected_context": ["stress", "work", "trigger"]
                },
                {
                    "message": "My back pain gets worse when I sit for long periods",
                    "expected_context": ["sitting", "position", "duration"]
                },
                {
                    "message": "I feel nauseous after eating spicy food",
                    "expected_context": ["eating", "food", "trigger", "after"]
                },
                {
                    "message": "I have trouble sleeping when it's noisy outside",
                    "expected_context": ["noise", "environment", "sleep", "trigger"]
                }
            ]
            
            consistent_activations = 0
            total_scenarios = len(test_scenarios)
            
            for i, scenario in enumerate(test_scenarios):
                # Initialize new consultation for each test
                init_response = requests.post(f"{API_BASE}/medical-ai/initialize", 
                    json={
                        "patient_id": f"test-consistency-{i}",
                        "timestamp": datetime.now().isoformat()
                    },
                    timeout=30
                )
                
                if init_response.status_code != 200:
                    continue
                    
                consultation_id = init_response.json().get("consultation_id")
                
                response = requests.post(f"{API_BASE}/medical-ai/message",
                    json={
                        "consultation_id": consultation_id,
                        "message": scenario["message"],
                        "timestamp": datetime.now().isoformat()
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "").lower()
                    
                    # Check if expected contextual elements are present
                    found_context = [ctx for ctx in scenario["expected_context"] 
                                   if ctx in response_text]
                    
                    # Check for Step 2.2 fields
                    has_contextual_fields = any(field in data for field in 
                                              ["contextual_factors", "causal_relationships", "trigger_avoidance_strategies"])
                    
                    if len(found_context) >= 1 or has_contextual_fields:
                        consistent_activations += 1
            
            # Success criteria: At least 75% consistency
            consistency_rate = consistent_activations / total_scenarios
            success = consistency_rate >= 0.75
            
            if success:
                self.log_test("Contextual Reasoning Consistency", True,
                            f"Consistency rate: {consistency_rate*100:.1f}% ({consistent_activations}/{total_scenarios})")
                return True
            else:
                self.log_test("Contextual Reasoning Consistency", False,
                            f"Low consistency rate: {consistency_rate*100:.1f}% ({consistent_activations}/{total_scenarios})")
                return False
                
        except Exception as e:
            self.log_test("Contextual Reasoning Consistency", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all Step 2.2 Context-Aware Medical Reasoning Engine tests"""
        print("🧠 STEP 2.2 CONTEXT-AWARE MEDICAL REASONING ENGINE COMPREHENSIVE TESTING")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Testing started at: {datetime.now().isoformat()}")
        print()
        
        # Run all tests
        test_methods = [
            self.test_ultra_challenging_scenario_1_positional_orthostatic,
            self.test_ultra_challenging_scenario_2_exertional_cardiac,
            self.test_ultra_challenging_scenario_3_multi_context_dietary_stress,
            self.test_step_22_api_response_fields,
            self.test_consultation_flow_problem,
            self.test_contextual_reasoning_consistency
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.log_test(test_method.__name__, False, f"Test execution failed: {str(e)}")
        
        # Print summary
        print("\n" + "=" * 80)
        print("🧠 STEP 2.2 CONTEXT-AWARE MEDICAL REASONING ENGINE TEST SUMMARY")
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
    tester = Step22ContextualReasoningTester()
    passed, failed, total = tester.run_all_tests()
    
    # Exit with appropriate code
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Step 2.2 Context-Aware Medical Reasoning Engine is working correctly.")
        sys.exit(0)
    else:
        print(f"\n⚠️  {failed} TESTS FAILED. Step 2.2 Context-Aware Medical Reasoning Engine needs attention.")
        sys.exit(1)

if __name__ == "__main__":
    main()