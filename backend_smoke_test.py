#!/usr/bin/env python3

import requests
import json
from datetime import datetime

class BackendSmokeTest:
    def __init__(self, base_url="https://medical-classifier.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}" if endpoint else self.base_url
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)

            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:300]}...")
                except:
                    print(f"   Response: {response.text[:200]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")

            return success, response.json() if success and response.text else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_api_health_check(self):
        """Test basic API health"""
        print("\n📋 1. API Health Check")
        return self.run_test(
            "Basic API Root",
            "GET",
            "",
            200
        )

    def test_profile_endpoint_404(self):
        """Test profile endpoint returns proper 404"""
        print("\n📋 2. Profile Endpoint 404 Test")
        return self.run_test(
            "GET /api/profiles/patient/test-user-123 (Should return 404)",
            "GET",
            "profiles/patient/test-user-123",
            404
        )

    def test_dashboard_endpoints(self):
        """Test all 4 role dashboard endpoints"""
        print("\n📋 3. Role-based Dashboard APIs")
        
        test_user_id = "test-user-123"
        
        # Test Patient Dashboard
        success1, patient_data = self.run_test(
            "Patient Dashboard",
            "GET",
            f"patient/dashboard/{test_user_id}",
            200
        )

        # Test Provider Dashboard
        success2, provider_data = self.run_test(
            "Provider Dashboard",
            "GET",
            f"provider/dashboard/{test_user_id}",
            200
        )

        # Test Family Dashboard
        success3, family_data = self.run_test(
            "Family Dashboard",
            "GET",
            f"family/dashboard/{test_user_id}",
            200
        )

        # Test Guest Dashboard
        success4, guest_data = self.run_test(
            "Guest Dashboard",
            "GET",
            "guest/dashboard",
            200
        )

        # Validate dashboard data structure
        if success1 and patient_data:
            expected_keys = ['user_id', 'welcome_message', 'nutrition_summary', 'health_metrics', 'goals', 'recent_meals', 'ai_recommendations']
            has_expected_keys = all(key in patient_data for key in expected_keys)
            print(f"   Patient dashboard structure: {'✅' if has_expected_keys else '❌'}")

        if success2 and provider_data:
            expected_keys = ['user_id', 'welcome_message', 'patient_overview', 'clinical_alerts', 'todays_appointments', 'patient_progress']
            has_expected_keys = all(key in provider_data for key in expected_keys)
            print(f"   Provider dashboard structure: {'✅' if has_expected_keys else '❌'}")

        if success3 and family_data:
            expected_keys = ['user_id', 'family_overview', 'family_members', 'meal_planning', 'health_alerts', 'upcoming_appointments']
            has_expected_keys = all(key in family_data for key in expected_keys)
            print(f"   Family dashboard structure: {'✅' if has_expected_keys else '❌'}")

        if success4 and guest_data:
            expected_keys = ['session_info', 'todays_entries', 'nutrition_summary', 'simple_goals', 'nutrition_tips', 'message']
            has_expected_keys = all(key in guest_data for key in expected_keys)
            print(f"   Guest dashboard structure: {'✅' if has_expected_keys else '❌'}")

        return success1 and success2 and success3 and success4

    def run_smoke_test(self):
        """Run the requested smoke tests"""
        print("🚀 Starting Backend API Smoke Test")
        print(f"🌐 Base URL: {self.base_url}")
        print("=" * 60)
        print("Focus: Quick smoke test to ensure Phase 2 frontend changes haven't broken backend APIs")

        # Run the specific tests requested
        health_success, _ = self.test_api_health_check()
        profile_404_success, _ = self.test_profile_endpoint_404()
        dashboard_success = self.test_dashboard_endpoints()

        # Print final results
        print("\n" + "=" * 60)
        print(f"📊 SMOKE TEST RESULTS")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        overall_success = health_success and profile_404_success and dashboard_success
        
        if overall_success:
            print("🎉 All smoke tests passed! Backend APIs are responding properly.")
            print("✅ Backend is functioning correctly after Phase 2 frontend changes.")
            return 0
        else:
            print("⚠️  Some smoke tests failed. Backend may have issues.")
            return 1

if __name__ == "__main__":
    tester = BackendSmokeTest()
    exit_code = tester.run_smoke_test()
    exit(exit_code)