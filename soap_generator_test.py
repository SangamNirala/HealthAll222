#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime, timedelta
import uuid

class SOAPGeneratorTester:
    def __init__(self, base_url="https://followup-testing.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}" if endpoint else self.base_url
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)

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
                print(f"   Response: {response.text[:500]}...")

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

    def test_soap_generator_import(self):
        """Test 1: Verify ProfessionalSOAPGenerator imports correctly in server.py"""
        print("\n🔍 Testing SOAP Generator Import...")
        
        # Test basic API to ensure server is running and imports are working
        success, response = self.run_test(
            "Server Running with SOAP Generator Import",
            "GET",
            "",
            200
        )
        
        if success:
            print("   ✅ Server is running - SOAP Generator import successful")
            return True
        else:
            print("   ❌ Server not responding - possible import error")
            return False

    def test_medical_report_generation_headache(self):
        """Test 2: Medical Report Generation - Headache Scenario"""
        print("\n🩺 Testing Medical Report Generation - Headache Scenario...")
        
        # Step 1: Initialize consultation
        init_data = {
            "patient_id": "headache_patient_test",
            "demographics": {
                "age": 32,
                "sex": "Female"
            }
        }
        
        init_success, init_response = self.run_test(
            "Initialize Headache Consultation",
            "POST",
            "medical-ai/initialize",
            200,
            data=init_data
        )
        
        if not init_success:
            return False
        
        consultation_id = init_response.get('consultation_id', '')
        print(f"   📋 Consultation ID: {consultation_id}")
        
        # Step 2: Add comprehensive consultation data with OLDCARTS elements
        consultation_messages = [
            {
                "consultation_id": consultation_id,
                "message": "I've been having severe headaches for the past 3 days. The pain started gradually on Monday morning."
            },
            {
                "consultation_id": consultation_id,
                "message": "The headache is a throbbing pain, mainly on the right side of my head, around my temple area. It's about 7 out of 10 in severity."
            },
            {
                "consultation_id": consultation_id,
                "message": "The pain gets worse with bright lights and loud noises. It feels better when I rest in a dark, quiet room."
            },
            {
                "consultation_id": consultation_id,
                "message": "I also have some nausea and sensitivity to light. I've tried taking ibuprofen but it only helps a little."
            },
            {
                "consultation_id": consultation_id,
                "message": "I have a history of occasional headaches, but nothing this severe. My mother has migraines."
            }
        ]
        
        # Send messages to build consultation context
        for i, msg_data in enumerate(consultation_messages):
            msg_success, msg_response = self.run_test(
                f"Add Headache Context Message {i+1}",
                "POST",
                "medical-ai/message",
                200,
                data=msg_data
            )
            
            if not msg_success:
                return False
        
        # Step 3: Generate comprehensive SOAP report
        report_data = {
            "consultation_id": consultation_id,
            "messages": consultation_messages,
            "context": {
                "demographics": {"age": 32, "sex": "Female"},
                "chief_complaint": "severe headaches for 3 days",
                "symptom_data": {
                    "onset": "gradual, started Monday morning",
                    "duration": "3 days",
                    "character": "throbbing pain",
                    "location": "right side of head, temple area",
                    "severity": "7/10",
                    "alleviating": "rest in dark, quiet room",
                    "aggravating": "bright lights, loud noises",
                    "timing": "continuous for 3 days",
                    "associated_symptoms": ["nausea", "photophobia", "phonophobia"],
                    "treatments_tried": "ibuprofen with minimal relief"
                },
                "past_medical_history": {
                    "conditions": ["occasional headaches"]
                },
                "family_history": {
                    "mother": "migraines"
                },
                "clinical_hypotheses": [
                    {
                        "condition": "Migraine headache",
                        "probability": 85,
                        "reasoning": "Unilateral throbbing headache with photophobia, phonophobia, nausea, and family history of migraines"
                    },
                    {
                        "condition": "Tension-type headache",
                        "probability": 15,
                        "reasoning": "Possible tension component, though clinical features more consistent with migraine"
                    }
                ],
                "emergency_level": "routine"
            }
        }
        
        report_success, report_response = self.run_test(
            "Generate Comprehensive SOAP Report - Headache",
            "POST",
            "medical-ai/report",
            200,
            data=report_data
        )
        
        if report_success and report_response:
            return self.validate_soap_structure(report_response, "headache")
        
        return False

    def test_medical_report_generation_chest_pain(self):
        """Test 3: Medical Report Generation - Emergency Chest Pain Scenario"""
        print("\n🚨 Testing Medical Report Generation - Emergency Chest Pain Scenario...")
        
        # Step 1: Initialize consultation
        init_data = {
            "patient_id": "chest_pain_emergency_test",
            "demographics": {
                "age": 58,
                "sex": "Male"
            }
        }
        
        init_success, init_response = self.run_test(
            "Initialize Chest Pain Emergency Consultation",
            "POST",
            "medical-ai/initialize",
            200,
            data=init_data
        )
        
        if not init_success:
            return False
        
        consultation_id = init_response.get('consultation_id', '')
        print(f"   📋 Consultation ID: {consultation_id}")
        
        # Step 2: Add emergency consultation data
        consultation_messages = [
            {
                "consultation_id": consultation_id,
                "message": "I'm having severe chest pain that started suddenly about 30 minutes ago while I was walking upstairs."
            },
            {
                "consultation_id": consultation_id,
                "message": "The pain is crushing and feels like someone is sitting on my chest. It's radiating down my left arm and up to my jaw."
            },
            {
                "consultation_id": consultation_id,
                "message": "I'm also feeling short of breath, nauseous, and I'm sweating a lot. The pain is about 9 out of 10."
            },
            {
                "consultation_id": consultation_id,
                "message": "I have high blood pressure and high cholesterol. I take lisinopril and atorvastatin daily."
            },
            {
                "consultation_id": consultation_id,
                "message": "My father had a heart attack at age 60. I'm a former smoker - quit 5 years ago."
            }
        ]
        
        # Send messages to build consultation context
        for i, msg_data in enumerate(consultation_messages):
            msg_success, msg_response = self.run_test(
                f"Add Chest Pain Emergency Context Message {i+1}",
                "POST",
                "medical-ai/message",
                200,
                data=msg_data
            )
            
            if not msg_success:
                return False
        
        # Step 3: Generate emergency SOAP report
        report_data = {
            "consultation_id": consultation_id,
            "messages": consultation_messages,
            "context": {
                "demographics": {"age": 58, "sex": "Male"},
                "chief_complaint": "severe chest pain with radiation",
                "symptom_data": {
                    "onset": "sudden, 30 minutes ago",
                    "duration": "30 minutes",
                    "character": "crushing, pressure-like",
                    "location": "chest",
                    "radiation": "left arm and jaw",
                    "severity": "9/10",
                    "aggravating": "physical exertion (walking upstairs)",
                    "associated_symptoms": ["shortness of breath", "nausea", "diaphoresis"],
                    "impact_daily_activities": "unable to continue normal activities"
                },
                "past_medical_history": {
                    "conditions": ["hypertension", "hyperlipidemia"]
                },
                "medications": ["lisinopril", "atorvastatin"],
                "social_history": {
                    "smoking": "former smoker, quit 5 years ago"
                },
                "family_history": {
                    "father": "myocardial infarction at age 60"
                },
                "clinical_hypotheses": [
                    {
                        "condition": "Acute coronary syndrome",
                        "probability": 90,
                        "reasoning": "Classic presentation of crushing chest pain with radiation, associated symptoms, and multiple cardiac risk factors"
                    },
                    {
                        "condition": "Unstable angina",
                        "probability": 8,
                        "reasoning": "Possible unstable angina given risk factors and presentation"
                    },
                    {
                        "condition": "Aortic dissection",
                        "probability": 2,
                        "reasoning": "Less likely but must be considered with severe chest pain"
                    }
                ],
                "emergency_level": "emergency",
                "red_flags": ["crushing chest pain", "radiation to arm and jaw", "diaphoresis", "shortness of breath"]
            }
        }
        
        report_success, report_response = self.run_test(
            "Generate Emergency SOAP Report - Chest Pain",
            "POST",
            "medical-ai/report",
            200,
            data=report_data
        )
        
        if report_success and report_response:
            return self.validate_soap_structure(report_response, "chest_pain_emergency")
        
        return False

    def test_medical_report_generation_multi_symptom(self):
        """Test 4: Medical Report Generation - Multi-symptom Complex Case"""
        print("\n🔬 Testing Medical Report Generation - Multi-symptom Complex Case...")
        
        # Step 1: Initialize consultation
        init_data = {
            "patient_id": "multi_symptom_test",
            "demographics": {
                "age": 45,
                "sex": "Female"
            }
        }
        
        init_success, init_response = self.run_test(
            "Initialize Multi-symptom Consultation",
            "POST",
            "medical-ai/initialize",
            200,
            data=init_data
        )
        
        if not init_success:
            return False
        
        consultation_id = init_response.get('consultation_id', '')
        print(f"   📋 Consultation ID: {consultation_id}")
        
        # Step 2: Add complex multi-symptom consultation data
        consultation_messages = [
            {
                "consultation_id": consultation_id,
                "message": "I've been feeling unwell for about 2 weeks with multiple symptoms that seem to be getting worse."
            },
            {
                "consultation_id": consultation_id,
                "message": "I have joint pain in my hands, wrists, and knees that's worse in the morning and lasts for about an hour."
            },
            {
                "consultation_id": consultation_id,
                "message": "I'm also experiencing extreme fatigue - I feel tired even after a full night's sleep. I've also noticed a rash on my cheeks."
            },
            {
                "consultation_id": consultation_id,
                "message": "I've had low-grade fevers on and off, usually in the evenings. My hair has been falling out more than usual."
            },
            {
                "consultation_id": consultation_id,
                "message": "I have a history of hypothyroidism and take levothyroxine. My aunt has rheumatoid arthritis and my mother has lupus."
            }
        ]
        
        # Send messages to build consultation context
        for i, msg_data in enumerate(consultation_messages):
            msg_success, msg_response = self.run_test(
                f"Add Multi-symptom Context Message {i+1}",
                "POST",
                "medical-ai/message",
                200,
                data=msg_data
            )
            
            if not msg_success:
                return False
        
        # Step 3: Generate complex SOAP report
        report_data = {
            "consultation_id": consultation_id,
            "messages": consultation_messages,
            "context": {
                "demographics": {"age": 45, "sex": "Female"},
                "chief_complaint": "joint pain, fatigue, rash, and fever for 2 weeks",
                "symptom_data": {
                    "onset": "gradual over 2 weeks",
                    "duration": "2 weeks, worsening",
                    "location": "hands, wrists, knees (joint pain); cheeks (rash)",
                    "character": "joint stiffness and pain, malar rash",
                    "timing": "morning stiffness lasting 1 hour, evening fevers",
                    "associated_symptoms": ["extreme fatigue", "hair loss", "low-grade fever"],
                    "impact_daily_activities": "significant fatigue affecting daily function"
                },
                "past_medical_history": {
                    "conditions": ["hypothyroidism"]
                },
                "medications": ["levothyroxine"],
                "family_history": {
                    "aunt": "rheumatoid arthritis",
                    "mother": "systemic lupus erythematosus"
                },
                "clinical_hypotheses": [
                    {
                        "condition": "Systemic lupus erythematosus",
                        "probability": 70,
                        "reasoning": "Classic presentation with malar rash, joint pain, fatigue, fever, hair loss, and strong family history of lupus"
                    },
                    {
                        "condition": "Rheumatoid arthritis",
                        "probability": 20,
                        "reasoning": "Morning stiffness and joint pain pattern, family history of RA"
                    },
                    {
                        "condition": "Mixed connective tissue disease",
                        "probability": 10,
                        "reasoning": "Overlapping features of multiple autoimmune conditions"
                    }
                ],
                "emergency_level": "urgent"
            }
        }
        
        report_success, report_response = self.run_test(
            "Generate Complex Multi-symptom SOAP Report",
            "POST",
            "medical-ai/report",
            200,
            data=report_data
        )
        
        if report_success and report_response:
            return self.validate_soap_structure(report_response, "multi_symptom")
        
        return False

    def validate_soap_structure(self, report_response, scenario_type):
        """Validate comprehensive SOAP structure and content"""
        print(f"\n📋 Validating SOAP Structure for {scenario_type}...")
        
        # Check required response fields
        required_fields = ['report_id', 'soap_note', 'summary', 'recommendations', 'generated_at']
        missing_fields = [field for field in required_fields if field not in report_response]
        
        if missing_fields:
            print(f"   ❌ Missing response fields: {missing_fields}")
            return False
        
        print(f"   ✅ All required response fields present: {required_fields}")
        
        # Validate SOAP note content
        soap_note = report_response.get('soap_note', '')
        soap_sections = ['SUBJECTIVE', 'OBJECTIVE', 'ASSESSMENT', 'PLAN']
        
        missing_sections = []
        for section in soap_sections:
            if section not in soap_note:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"   ❌ Missing SOAP sections: {missing_sections}")
            return False
        
        print(f"   ✅ All SOAP sections present: {soap_sections}")
        
        # Validate professional medical content
        medical_content_checks = self.validate_medical_content(soap_note, scenario_type)
        
        # Validate AI Consult Summary (Doctronic.ai style)
        summary_checks = self.validate_ai_summary(report_response.get('summary', ''), scenario_type)
        
        # Validate recommendations
        recommendations = report_response.get('recommendations', [])
        if not recommendations or len(recommendations) < 3:
            print(f"   ❌ Insufficient recommendations: {len(recommendations)} (expected at least 3)")
            return False
        
        print(f"   ✅ Adequate recommendations provided: {len(recommendations)}")
        
        # Print key metrics
        print(f"\n📊 SOAP Note Metrics:")
        print(f"   📝 Total length: {len(soap_note)} characters")
        print(f"   📋 Report ID: {report_response.get('report_id', 'N/A')}")
        print(f"   🕒 Generated at: {report_response.get('generated_at', 'N/A')}")
        print(f"   💡 Summary length: {len(report_response.get('summary', ''))} characters")
        print(f"   📌 Recommendations count: {len(recommendations)}")
        
        return medical_content_checks and summary_checks

    def validate_medical_content(self, soap_note, scenario_type):
        """Validate professional medical content and terminology"""
        print(f"\n🩺 Validating Medical Content Quality...")
        
        validation_results = []
        
        # Check for professional medical header
        header_elements = ['PATIENT INFORMATION', 'Consultation Type', 'Provider']
        header_present = all(element in soap_note for element in header_elements)
        validation_results.append(('Professional Header', header_present))
        
        # Check for comprehensive subjective section
        subjective_elements = ['Chief Complaint', 'History of Present Illness', 'Past Medical History']
        subjective_complete = all(element in soap_note for element in subjective_elements)
        validation_results.append(('Comprehensive Subjective', subjective_complete))
        
        # Check for proper assessment with differential diagnosis
        assessment_elements = ['Clinical Impression', 'Differential Diagnosis', 'Clinical Reasoning']
        assessment_complete = all(element in soap_note for element in assessment_elements)
        validation_results.append(('Detailed Assessment', assessment_complete))
        
        # Check for comprehensive plan
        plan_elements = ['Diagnostic Workup', 'Therapeutic Interventions', 'Follow-up Plan', 'Patient Education', 'Return Precautions']
        plan_complete = all(element in soap_note for element in plan_elements)
        validation_results.append(('Comprehensive Plan', plan_complete))
        
        # Check for ICD codes (scenario-specific)
        icd_present = 'ICD-10:' in soap_note
        validation_results.append(('ICD-10 Codes', icd_present))
        
        # Check for medical disclaimer
        disclaimer_present = 'MEDICAL DISCLAIMER' in soap_note
        validation_results.append(('Medical Disclaimer', disclaimer_present))
        
        # Scenario-specific validations
        if scenario_type == "headache":
            headache_specific = ['migraine' in soap_note.lower() or 'headache' in soap_note.lower(),
                               'photophobia' in soap_note.lower() or 'light sensitivity' in soap_note.lower()]
            validation_results.append(('Headache-specific Content', all(headache_specific)))
        
        elif scenario_type == "chest_pain_emergency":
            emergency_specific = ['emergency' in soap_note.lower(),
                                'ECG' in soap_note or 'electrocardiogram' in soap_note.lower(),
                                'cardiac' in soap_note.lower()]
            validation_results.append(('Emergency-specific Content', all(emergency_specific)))
        
        elif scenario_type == "multi_symptom":
            autoimmune_specific = ['lupus' in soap_note.lower() or 'autoimmune' in soap_note.lower(),
                                 'joint' in soap_note.lower(),
                                 'rash' in soap_note.lower()]
            validation_results.append(('Multi-symptom Content', all(autoimmune_specific)))
        
        # Print validation results
        all_passed = True
        for check_name, passed in validation_results:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}: {'PASS' if passed else 'FAIL'}")
            if not passed:
                all_passed = False
        
        return all_passed

    def validate_ai_summary(self, summary, scenario_type):
        """Validate AI Consult Summary (Doctronic.ai style)"""
        print(f"\n🤖 Validating AI Consult Summary...")
        
        if not summary:
            print("   ❌ No AI summary provided")
            return False
        
        validation_results = []
        
        # Check for summary structure
        summary_elements = ['AI Consult Summary', 'year-old', 'experiencing', 'recommended plan']
        summary_structure = all(element in summary for element in summary_elements)
        validation_results.append(('Summary Structure', summary_structure))
        
        # Check for appropriate length (should be concise but informative)
        appropriate_length = 100 <= len(summary) <= 1000
        validation_results.append(('Appropriate Length', appropriate_length))
        
        # Check for patient-friendly language
        patient_friendly = not any(term in summary.lower() for term in ['differential diagnosis', 'pathophysiology', 'etiology'])
        validation_results.append(('Patient-friendly Language', patient_friendly))
        
        # Print validation results
        all_passed = True
        for check_name, passed in validation_results:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}: {'PASS' if passed else 'FAIL'}")
            if not passed:
                all_passed = False
        
        print(f"   📝 Summary preview: {summary[:200]}...")
        
        return all_passed

    def run_comprehensive_soap_tests(self):
        """Run all SOAP generator tests"""
        print("🚀 Starting Phase 3.1 Advanced SOAP Note Generator Integration Tests")
        print(f"🌐 Base URL: {self.base_url}")
        print("=" * 80)

        # Test 1: SOAP Generator Import Verification
        print("\n" + "="*50)
        print("TEST 1: SOAP GENERATOR IMPORT VERIFICATION")
        print("="*50)
        import_success = self.test_soap_generator_import()

        # Test 2: Medical Report Generation - Headache Scenario
        print("\n" + "="*50)
        print("TEST 2: MEDICAL REPORT GENERATION - HEADACHE")
        print("="*50)
        headache_success = self.test_medical_report_generation_headache()

        # Test 3: Medical Report Generation - Emergency Chest Pain
        print("\n" + "="*50)
        print("TEST 3: MEDICAL REPORT GENERATION - EMERGENCY CHEST PAIN")
        print("="*50)
        chest_pain_success = self.test_medical_report_generation_chest_pain()

        # Test 4: Medical Report Generation - Multi-symptom Complex Case
        print("\n" + "="*50)
        print("TEST 4: MEDICAL REPORT GENERATION - MULTI-SYMPTOM COMPLEX")
        print("="*50)
        multi_symptom_success = self.test_medical_report_generation_multi_symptom()

        # Final Results Summary
        print("\n" + "="*80)
        print("🏁 PHASE 3.1 SOAP GENERATOR INTEGRATION TEST RESULTS")
        print("="*80)
        
        test_results = [
            ("SOAP Generator Import", import_success),
            ("Headache SOAP Generation", headache_success),
            ("Emergency Chest Pain SOAP", chest_pain_success),
            ("Multi-symptom Complex SOAP", multi_symptom_success)
        ]
        
        passed_tests = sum(1 for _, success in test_results if success)
        total_tests = len(test_results)
        
        for test_name, success in test_results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {status} {test_name}")
        
        print(f"\n📊 Overall Results: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)")
        print(f"📈 API Calls: {self.tests_run} total, {self.tests_passed} successful ({self.tests_passed/self.tests_run*100:.1f}%)")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED - Phase 3.1 Advanced SOAP Note Generator is fully functional!")
            return True
        else:
            print(f"\n⚠️  {total_tests - passed_tests} TEST(S) FAILED - Review implementation")
            return False

if __name__ == "__main__":
    tester = SOAPGeneratorTester()
    success = tester.run_comprehensive_soap_tests()
    sys.exit(0 if success else 1)