#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend_test import HealthPlatformAPITester

def main():
    """Test Patient Management APIs specifically"""
    tester = HealthPlatformAPITester()
    
    print("🚀 Testing Patient Management API Endpoints")
    print(f"🌐 Base URL: {tester.base_url}")
    print("=" * 80)
    
    # Test the Patient Management APIs as requested in the review
    success = tester.test_patient_management_apis()
    
    print("\n" + "=" * 80)
    if success:
        print("🎉 Patient Management API Tests: PASSED")
        print("✅ All Patient Management endpoints are working correctly")
        return 0
    else:
        print("⚠️ Patient Management API Tests: FAILED")
        print("❌ Issues detected with Patient Management endpoints")
        return 1

if __name__ == "__main__":
    sys.exit(main())