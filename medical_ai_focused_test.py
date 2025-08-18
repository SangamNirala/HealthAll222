#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime
import uuid

class MedicalAIFocusedTester:
    def __init__(self, base_url="https://medreasoning.preview.emergentagent.com/api"):
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
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)

            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response keys: {list(response_data.keys())}")
                    return True, response_data
                except:
                    print(f"   Response: {response.text[:200]}...")
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:500]}...")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_medical_ai_initialization_response_structure(self):
        """
        FOCUSED TEST: Medical AI Initialization Response Structure Validation
        
        This test validates that the POST /api/medical-ai/initialize endpoint
        returns ALL 9 required keys for 100% success rate as requested in review.
        
        Required keys:
        1. consultation_id ✓
        2. patient_id ✓ (NEWLY ADDED)
        3. current_stage ✓ (NEWLY ADDED)  
        4. response ✓
        5. next_questions ✓
        6. stage ✓
        7. urgency ✓
        8. emergency_detected ✓
        9. context ✓
        """
        print("\n🏥 FOCUSED TEST: Medical AI Initialization Response Structure Validation")
        print("=" * 80)
        print("Testing POST /api/medical-ai/initialize for ALL 9 required keys")
        print("Expected 100% success rate with complete response structure")
        print("=" * 80)
        
        # Test data as specified in review request
        test_data = {
            "patient_id": "demo-patient-123"
        }
        
        success, response_data = self.run_test(
            "Medical AI Initialize - Complete Response Structure Validation",
            "POST",
            "medical-ai/initialize",
            200,
            data=test_data
        )
        
        if not success:
            print("❌ CRITICAL FAILURE: API endpoint failed to respond")
            return False
        
        # Define ALL 9 required keys as specified in review request
        required_keys = [
            'consultation_id',    # ✓ Original key
            'patient_id',         # ✓ NEWLY ADDED key
            'current_stage',      # ✓ NEWLY ADDED key
            'response',           # ✓ Original key
            'next_questions',     # ✓ Original key
            'stage',              # ✓ Original key
            'urgency',            # ✓ Original key
            'emergency_detected', # ✓ Original key
            'context'             # ✓ Original key
        ]
        
        print(f"\n📋 VALIDATION: Checking for ALL {len(required_keys)} required keys...")
        print("=" * 60)
        
        # Check each required key
        missing_keys = []
        present_keys = []
        
        for key in required_keys:
            if key in response_data:
                present_keys.append(key)
                print(f"   ✅ {key}: PRESENT")
            else:
                missing_keys.append(key)
                print(f"   ❌ {key}: MISSING")
        
        print("=" * 60)
        
        # Calculate success rate
        success_rate = (len(present_keys) / len(required_keys)) * 100
        
        print(f"\n📊 VALIDATION RESULTS:")
        print(f"   Required keys: {len(required_keys)}")
        print(f"   Present keys: {len(present_keys)}")
        print(f"   Missing keys: {len(missing_keys)}")
        print(f"   SUCCESS RATE: {success_rate:.1f}%")
        
        if missing_keys:
            print(f"\n❌ MISSING KEYS: {missing_keys}")
            print("   These keys were expected but not found in response")
        
        if present_keys:
            print(f"\n✅ PRESENT KEYS: {present_keys}")
        
        # Validate specific key values for newly added keys
        if 'patient_id' in response_data:
            patient_id = response_data.get('patient_id')
            print(f"\n🔍 NEWLY ADDED KEY VALIDATION:")
            print(f"   patient_id: '{patient_id}' (Expected: 'demo-patient-123')")
            patient_id_valid = patient_id == "demo-patient-123"
            print(f"   patient_id validation: {'✅' if patient_id_valid else '❌'}")
        
        if 'current_stage' in response_data:
            current_stage = response_data.get('current_stage')
            print(f"   current_stage: '{current_stage}' (Expected: valid stage)")
            stage_valid = current_stage and len(str(current_stage)) > 0
            print(f"   current_stage validation: {'✅' if stage_valid else '❌'}")
        
        # Display sample response data for verification
        print(f"\n📄 SAMPLE RESPONSE DATA:")
        for key in required_keys:
            if key in response_data:
                value = response_data[key]
                if isinstance(value, str) and len(value) > 100:
                    print(f"   {key}: '{value[:100]}...' (truncated)")
                else:
                    print(f"   {key}: {value}")
        
        # Final validation
        validation_success = len(missing_keys) == 0
        target_success_rate = 100.0
        
        print(f"\n🎯 FINAL VALIDATION:")
        print(f"   Target success rate: {target_success_rate}%")
        print(f"   Actual success rate: {success_rate:.1f}%")
        print(f"   Validation result: {'✅ PASS' if validation_success else '❌ FAIL'}")
        
        if validation_success:
            print(f"\n🎉 SUCCESS: Medical AI initialization response includes ALL {len(required_keys)} required keys!")
            print("   The response structure improvements have been successfully implemented.")
            print("   100% validation success achieved as requested.")
        else:
            print(f"\n⚠️  FAILURE: Medical AI initialization response is missing {len(missing_keys)} required keys.")
            print("   The response structure needs to be updated to include all required keys.")
            print("   Current success rate is below the target 100%.")
        
        return validation_success

    def run_focused_test(self):
        """Run the focused Medical AI initialization test"""
        print("🚀 Starting Medical AI Response Structure Validation Test")
        print("Focus: Verify ALL 9 required keys are present in initialization response")
        print("Expected: 100% success rate with complete response structure")
        
        # Run the focused test
        test_success = self.test_medical_ai_initialization_response_structure()
        
        # Summary
        print(f"\n" + "=" * 80)
        print("📊 FOCUSED TEST SUMMARY")
        print("=" * 80)
        print(f"Tests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Overall success: {'✅ PASS' if test_success else '❌ FAIL'}")
        
        if test_success:
            print("\n🎯 CONCLUSION: Medical AI initialization endpoint validation SUCCESSFUL")
            print("   ✅ All 9 required keys are present in the response")
            print("   ✅ Response structure improvements have been implemented")
            print("   ✅ 100% validation success rate achieved")
        else:
            print("\n⚠️  CONCLUSION: Medical AI initialization endpoint validation FAILED")
            print("   ❌ Some required keys are missing from the response")
            print("   ❌ Response structure needs further improvements")
            print("   ❌ Success rate is below 100% target")
        
        return test_success

if __name__ == "__main__":
    tester = MedicalAIFocusedTester()
    success = tester.run_focused_test()
    sys.exit(0 if success else 1)