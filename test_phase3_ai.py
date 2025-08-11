#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend_test import HealthPlatformAPITester

def main():
    """Run Phase 3 AI Integration tests specifically"""
    tester = HealthPlatformAPITester()
    
    print("🚀 Starting Phase 3 AI Integration Backend Tests")
    print(f"🌐 Base URL: {tester.base_url}")
    print("=" * 80)
    
    # Test existing AI API endpoints first
    print("\n📋 Testing AI API Endpoints...")
    ai_success = tester.test_ai_api_endpoints()
    
    # Test Phase 3 AI Integration for PersonalInsights
    print("\n📋 Testing Phase 3 AI Integration - PersonalInsights...")
    phase3_ai_success = tester.test_phase3_ai_integration_personalinsights()
    
    # Print final results
    print("\n" + "=" * 80)
    print(f"📊 PHASE 3 AI INTEGRATION TEST RESULTS")
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    print(f"\n🎯 DETAILED RESULTS:")
    print(f"   AI API Endpoints: {'✅ PASSED' if ai_success else '❌ FAILED'}")
    print(f"   Phase 3 AI Integration - PersonalInsights: {'✅ PASSED' if phase3_ai_success else '❌ FAILED'}")
    
    overall_success = ai_success and phase3_ai_success
    
    if overall_success:
        print("\n🎉 All Phase 3 AI Integration tests passed!")
        return 0
    else:
        print("\n⚠️ Some Phase 3 AI Integration tests failed. Check the details above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())