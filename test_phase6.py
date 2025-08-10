#!/usr/bin/env python3

import sys
import os
sys.path.append('/app')

from backend_test import HealthPlatformAPITester

def main():
    """Run Phase 6 Guest Goals Management tests"""
    tester = HealthPlatformAPITester()
    
    print("🚀 Starting Phase 6 Guest Goals Management API Tests")
    print(f"🌐 Base URL: {tester.base_url}")
    print("=" * 80)
    
    # Run Phase 6 Guest Goals Management tests
    success = tester.test_phase6_guest_goals_management()
    
    print("\n" + "=" * 80)
    print(f"📊 PHASE 6 TEST RESULTS")
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if success:
        print("🎉 Phase 6 Guest Goals Management Tests: PASSED")
        print("✅ All Phase 6 API endpoints are working correctly")
        return 0
    else:
        print("⚠️ Phase 6 Guest Goals Management Tests: FAILED")
        print("❌ Issues detected with Phase 6 API endpoints")
        
        # Show failed tests
        print("\nFailed Tests:")
        for result in tester.test_results:
            if not result.get('success', False):
                print(f"  - {result['name']}: {result.get('error', 'Status code mismatch')}")
        return 1

if __name__ == "__main__":
    sys.exit(main())