#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime, timedelta
import uuid

class ProfileWizardEnhancementsTester:
    def __init__(self, base_url="https://530c05ea-1599-4fd0-83d4-3b33fe32d971.preview.emergentagent.com/api"):
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
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)

            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                except:
                    print(f"   Response: {response.text[:200]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")

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

    def test_previous_surgeries_support(self):
        """Test Patient Profile APIs for previous_surgeries field support"""
        print("\n🏥 Testing Previous Surgeries Field Support...")
        
        test_user_id = f"surgery_test_{datetime.now().strftime('%H%M%S')}"
        
        # Test 1: Create patient profile with health_history containing previous_surgeries
        profile_with_surgeries = {
            "user_id": test_user_id,
            "basic_info": {
                "full_name": "John Surgery Patient",
                "age": 45,
                "gender": "Male",
                "location": "Boston, MA",
                "timezone": "America/New_York",
                "preferred_language": "English"
            },
            "health_history": {
                "primary_health_goals": ["recovery", "maintain_health"],
                "medical_conditions": {"post_surgical": "recovering"},
                "previous_surgeries": [
                    {
                        "id": "surg_001",
                        "name": "Appendectomy",
                        "date": "2020-03-15",
                        "details": "Laparoscopic appendix removal, no complications, full recovery"
                    },
                    {
                        "id": "surg_002", 
                        "name": "Knee Arthroscopy",
                        "date": "2022-08-10",
                        "details": "Meniscus repair, successful procedure, 6 weeks recovery"
                    },
                    {
                        "id": "surg_003",
                        "name": "Gallbladder Removal",
                        "date": "2023-01-20",
                        "details": "Cholecystectomy due to gallstones, minimally invasive"
                    }
                ],
                "allergies": ["penicillin"],
                "family_medical_history": ["heart_disease"]
            }
        }
        
        success1, create_response = self.run_test(
            "Create Patient Profile with Previous Surgeries",
            "POST",
            "profiles/patient",
            200,
            data=profile_with_surgeries
        )
        
        # Validate previous_surgeries were stored correctly
        if success1 and create_response:
            health_history = create_response.get('health_history', {})
            previous_surgeries = health_history.get('previous_surgeries', [])
            print(f"   Previous surgeries stored: {len(previous_surgeries)} procedures")
            
            if len(previous_surgeries) == 3:
                print(f"   ✅ All 3 surgeries stored correctly")
                # Validate surgery structure
                surgery = previous_surgeries[0]
                required_fields = ['id', 'name', 'date', 'details']
                missing_fields = [field for field in required_fields if field not in surgery]
                if not missing_fields:
                    print(f"   ✅ Surgery data structure valid: {surgery['name']} on {surgery['date']}")
                else:
                    print(f"   ❌ Surgery missing fields: {missing_fields}")
                    success1 = False
            else:
                print(f"   ❌ Expected 3 surgeries, got {len(previous_surgeries)}")
                success1 = False
        
        # Test 2: Retrieve patient profile and verify previous_surgeries data is preserved
        success2, get_response = self.run_test(
            "Retrieve Patient Profile with Previous Surgeries",
            "GET",
            f"profiles/patient/{test_user_id}",
            200
        )
        
        if success2 and get_response:
            health_history = get_response.get('health_history', {})
            previous_surgeries = health_history.get('previous_surgeries', [])
            
            if len(previous_surgeries) == 3:
                print(f"   ✅ Previous surgeries preserved on retrieval")
                # Verify specific surgery details
                appendectomy = next((s for s in previous_surgeries if s['name'] == 'Appendectomy'), None)
                if appendectomy and appendectomy['date'] == '2020-03-15':
                    print(f"   ✅ Surgery details preserved: {appendectomy['name']} - {appendectomy['details'][:50]}...")
                else:
                    print(f"   ❌ Surgery details not preserved correctly")
                    success2 = False
            else:
                print(f"   ❌ Previous surgeries not preserved on retrieval")
                success2 = False
        
        # Test 3: Update existing patient profile with previous_surgeries modifications
        surgery_update = {
            "health_history": {
                "primary_health_goals": ["recovery", "maintain_health"],
                "medical_conditions": {"post_surgical": "recovering"},
                "previous_surgeries": [
                    {
                        "id": "surg_001",
                        "name": "Appendectomy",
                        "date": "2020-03-15",
                        "details": "Laparoscopic appendix removal, no complications, full recovery - UPDATED"
                    },
                    {
                        "id": "surg_002", 
                        "name": "Knee Arthroscopy",
                        "date": "2022-08-10",
                        "details": "Meniscus repair, successful procedure, 6 weeks recovery"
                    },
                    {
                        "id": "surg_003",
                        "name": "Gallbladder Removal",
                        "date": "2023-01-20",
                        "details": "Cholecystectomy due to gallstones, minimally invasive"
                    },
                    {
                        "id": "surg_004",
                        "name": "Cataract Surgery",
                        "date": "2023-11-05",
                        "details": "Left eye cataract removal, outpatient procedure, excellent results"
                    }
                ],
                "allergies": ["penicillin"],
                "family_medical_history": ["heart_disease"]
            }
        }
        
        success3, update_response = self.run_test(
            "Update Patient Profile - Modify Previous Surgeries",
            "PUT",
            f"profiles/patient/{test_user_id}",
            200,
            data=surgery_update
        )
        
        if success3 and update_response:
            health_history = update_response.get('health_history', {})
            previous_surgeries = health_history.get('previous_surgeries', [])
            
            if len(previous_surgeries) == 4:
                print(f"   ✅ Surgery modifications successful - now {len(previous_surgeries)} procedures")
                # Verify updated details
                appendectomy = next((s for s in previous_surgeries if s['name'] == 'Appendectomy'), None)
                if appendectomy and 'UPDATED' in appendectomy['details']:
                    print(f"   ✅ Surgery details updated successfully")
                else:
                    print(f"   ❌ Surgery details update failed")
                    success3 = False
                
                # Verify new surgery added
                cataract = next((s for s in previous_surgeries if s['name'] == 'Cataract Surgery'), None)
                if cataract:
                    print(f"   ✅ New surgery added: {cataract['name']} on {cataract['date']}")
                else:
                    print(f"   ❌ New surgery not added")
                    success3 = False
            else:
                print(f"   ❌ Expected 4 surgeries after update, got {len(previous_surgeries)}")
                success3 = False
        
        # Clean up
        cleanup_success, _ = self.run_test(
            "Cleanup Previous Surgeries Test Profile",
            "DELETE",
            f"profiles/patient/{test_user_id}",
            200
        )
        
        print(f"\n📊 Previous Surgeries Support Test Summary:")
        print(f"   ✅ Create with surgeries: {'PASS' if success1 else 'FAIL'}")
        print(f"   ✅ Retrieve surgeries: {'PASS' if success2 else 'FAIL'}")
        print(f"   ✅ Update surgeries: {'PASS' if success3 else 'FAIL'}")
        print(f"   ✅ Cleanup: {'PASS' if cleanup_success else 'FAIL'}")
        
        return success1 and success2 and success3 and cleanup_success

    def test_profile_completion_tracking(self):
        """Test enhanced profile completion tracking for Patient, Provider, and Family profiles"""
        print("\n📊 Testing Enhanced Profile Completion Tracking...")
        
        # Test Patient Profile Completion
        patient_success = self.test_patient_completion_tracking()
        
        # Test Provider Profile Completion  
        provider_success = self.test_provider_completion_tracking()
        
        # Test Family Profile Completion
        family_success = self.test_family_completion_tracking()
        
        return patient_success and provider_success and family_success

    def test_patient_completion_tracking(self):
        """Test Patient profile completion calculation and persistence"""
        print("\n👤 Testing Patient Profile Completion Tracking...")
        
        test_user_id = f"patient_completion_{datetime.now().strftime('%H%M%S')}"
        
        # Test 1: Create profile with 1 section (basic_info) - should be 16.7%
        basic_profile = {
            "user_id": test_user_id,
            "basic_info": {
                "full_name": "Completion Test User",
                "age": 30,
                "gender": "Female",
                "location": "Test City",
                "timezone": "America/New_York",
                "preferred_language": "English"
            }
        }
        
        success1, response1 = self.run_test(
            "Patient Profile - 1 Section (16.7%)",
            "POST",
            "profiles/patient",
            200,
            data=basic_profile
        )
        
        if success1 and response1:
            completion = response1.get('profile_completion', 0)
            expected = 16.7
            if abs(completion - expected) < 1.0:
                print(f"   ✅ 1 section completion: {completion}% (expected ~{expected}%)")
            else:
                print(f"   ❌ 1 section completion: {completion}% (expected ~{expected}%)")
                success1 = False
        
        # Test 2: Add physical_metrics section - should be 33.3%
        physical_update = {
            "physical_metrics": {
                "height_cm": 165.0,
                "current_weight_kg": 65.0,
                "goal_weight_kg": 60.0
            }
        }
        
        success2, response2 = self.run_test(
            "Patient Profile - Add Physical Metrics (33.3%)",
            "PUT",
            f"profiles/patient/{test_user_id}",
            200,
            data=physical_update
        )
        
        if success2 and response2:
            completion = response2.get('profile_completion', 0)
            expected = 33.3
            if abs(completion - expected) < 1.0:
                print(f"   ✅ 2 sections completion: {completion}% (expected ~{expected}%)")
            else:
                print(f"   ❌ 2 sections completion: {completion}% (expected ~{expected}%)")
                success2 = False
        
        # Test 3: Add activity_profile section - should be 50.0%
        activity_update = {
            "activity_profile": {
                "activity_level": "MODERATELY_ACTIVE",
                "exercise_frequency": 3,
                "sleep_schedule": {
                    "bedtime": "22:00",
                    "wake_time": "06:00",
                    "sleep_quality": 4
                },
                "stress_level": 2,
                "work_type": "DESK_JOB"
            }
        }
        
        success3, response3 = self.run_test(
            "Patient Profile - Add Activity Profile (50.0%)",
            "PUT",
            f"profiles/patient/{test_user_id}",
            200,
            data=activity_update
        )
        
        if success3 and response3:
            completion = response3.get('profile_completion', 0)
            expected = 50.0
            if abs(completion - expected) < 1.0:
                print(f"   ✅ 3 sections completion: {completion}% (expected ~{expected}%)")
            else:
                print(f"   ❌ 3 sections completion: {completion}% (expected ~{expected}%)")
                success3 = False
        
        # Test 4: Verify completion is persisted in database
        success4, get_response = self.run_test(
            "Patient Profile - Verify Completion Persisted",
            "GET",
            f"profiles/patient/{test_user_id}",
            200
        )
        
        if success4 and get_response:
            persisted_completion = get_response.get('profile_completion', 0)
            expected = 50.0
            if abs(persisted_completion - expected) < 1.0:
                print(f"   ✅ Completion persisted: {persisted_completion}% (expected ~{expected}%)")
            else:
                print(f"   ❌ Completion not persisted: {persisted_completion}% (expected ~{expected}%)")
                success4 = False
        
        # Clean up
        cleanup_success, _ = self.run_test(
            "Cleanup Patient Completion Test",
            "DELETE",
            f"profiles/patient/{test_user_id}",
            200
        )
        
        return success1 and success2 and success3 and success4 and cleanup_success

    def test_provider_completion_tracking(self):
        """Test Provider profile completion calculation and persistence"""
        print("\n👨‍⚕️ Testing Provider Profile Completion Tracking...")
        
        test_user_id = f"provider_completion_{datetime.now().strftime('%H%M%S')}"
        
        # Test 1: Create profile with 1 section (professional_identity) - should be 25%
        identity_profile = {
            "user_id": test_user_id,
            "professional_identity": {
                "full_name": "Dr. Completion Test",
                "professional_title": "Registered Dietitian",
                "medical_license": "RD123456",
                "years_experience": 5
            }
        }
        
        success1, response1 = self.run_test(
            "Provider Profile - 1 Section (25%)",
            "POST",
            "profiles/provider",
            200,
            data=identity_profile
        )
        
        if success1 and response1:
            completion = response1.get('profile_completion', 0)
            expected = 25.0
            if abs(completion - expected) < 1.0:
                print(f"   ✅ 1 section completion: {completion}% (expected ~{expected}%)")
            else:
                print(f"   ❌ 1 section completion: {completion}% (expected ~{expected}%)")
                success1 = False
        
        # Test 2: Add credentials section - should be 50%
        credentials_update = {
            "credentials": {
                "education": [
                    {
                        "degree": "Master of Science in Nutrition",
                        "institution": "Test University",
                        "graduation_year": 2018,
                        "specialization": "Clinical Nutrition"
                    }
                ],
                "certifications": [
                    {
                        "name": "Certified Diabetes Educator",
                        "organization": "CBDCE",
                        "issue_date": "2020-01-01",
                        "expiration_date": "2025-01-01",
                        "status": "ACTIVE"
                    }
                ],
                "specializations": ["diabetes_management"]
            }
        }
        
        success2, response2 = self.run_test(
            "Provider Profile - Add Credentials (50%)",
            "PUT",
            f"profiles/provider/{test_user_id}",
            200,
            data=credentials_update
        )
        
        if success2 and response2:
            completion = response2.get('profile_completion', 0)
            expected = 50.0
            if abs(completion - expected) < 1.0:
                print(f"   ✅ 2 sections completion: {completion}% (expected ~{expected}%)")
            else:
                print(f"   ❌ 2 sections completion: {completion}% (expected ~{expected}%)")
                success2 = False
        
        # Clean up
        cleanup_success, _ = self.run_test(
            "Cleanup Provider Completion Test",
            "DELETE",
            f"profiles/provider/{test_user_id}",
            200
        )
        
        return success1 and success2 and cleanup_success

    def test_family_completion_tracking(self):
        """Test Family profile completion calculation and persistence"""
        print("\n👨‍👩‍👧‍👦 Testing Family Profile Completion Tracking...")
        
        test_user_id = f"family_completion_{datetime.now().strftime('%H%M%S')}"
        
        # Test 1: Create profile with 1 section (family_structure) - should be 25%
        structure_profile = {
            "user_id": test_user_id,
            "family_structure": {
                "family_role": "Parent",
                "number_of_members": 3,
                "primary_caregiver": True
            }
        }
        
        success1, response1 = self.run_test(
            "Family Profile - 1 Section (25%)",
            "POST",
            "profiles/family",
            200,
            data=structure_profile
        )
        
        if success1 and response1:
            completion = response1.get('profile_completion', 0)
            expected = 25.0
            if abs(completion - expected) < 1.0:
                print(f"   ✅ 1 section completion: {completion}% (expected ~{expected}%)")
            else:
                print(f"   ❌ 1 section completion: {completion}% (expected ~{expected}%)")
                success1 = False
        
        # Test 2: Add family_members section - should be 50%
        members_update = {
            "family_members": [
                {
                    "name": "Parent Test",
                    "relationship": "Self",
                    "age": 35,
                    "gender": "Female",
                    "allergies": [],
                    "medications": [],
                    "health_conditions": []
                },
                {
                    "name": "Child Test",
                    "relationship": "Child",
                    "age": 8,
                    "gender": "Male",
                    "allergies": ["peanuts"],
                    "medications": [],
                    "health_conditions": []
                }
            ]
        }
        
        success2, response2 = self.run_test(
            "Family Profile - Add Family Members (50%)",
            "PUT",
            f"profiles/family/{test_user_id}",
            200,
            data=members_update
        )
        
        if success2 and response2:
            completion = response2.get('profile_completion', 0)
            expected = 50.0
            if abs(completion - expected) < 1.0:
                print(f"   ✅ 2 sections completion: {completion}% (expected ~{expected}%)")
            else:
                print(f"   ❌ 2 sections completion: {completion}% (expected ~{expected}%)")
                success2 = False
        
        # Clean up
        cleanup_success, _ = self.run_test(
            "Cleanup Family Completion Test",
            "DELETE",
            f"profiles/family/{test_user_id}",
            200
        )
        
        return success1 and success2 and cleanup_success

    def test_cross_session_profile_support(self):
        """Test profile retrieval by user_id works correctly for cross-session editing"""
        print("\n🔄 Testing Cross-Session Profile Support...")
        
        test_user_id = f"cross_session_{datetime.now().strftime('%H%M%S')}"
        
        # Session 1: Create initial profile
        initial_profile = {
            "user_id": test_user_id,
            "basic_info": {
                "full_name": "Cross Session Patient",
                "age": 32,
                "gender": "Female",
                "location": "Seattle, WA",
                "timezone": "America/Los_Angeles",
                "preferred_language": "English"
            },
            "physical_metrics": {
                "height_cm": 168.0,
                "current_weight_kg": 70.0,
                "goal_weight_kg": 65.0
            }
        }
        
        success1, _ = self.run_test(
            "Session 1 - Create Initial Patient Profile",
            "POST",
            "profiles/patient",
            200,
            data=initial_profile
        )
        
        # Session 2: Retrieve existing profile by user_id
        success2, retrieved_profile = self.run_test(
            "Session 2 - Retrieve Patient Profile by User ID",
            "GET",
            f"profiles/patient/{test_user_id}",
            200
        )
        
        if success2 and retrieved_profile:
            # Verify all original data is present
            basic_info = retrieved_profile.get('basic_info', {})
            physical_metrics = retrieved_profile.get('physical_metrics', {})
            
            if (basic_info.get('full_name') == 'Cross Session Patient' and 
                physical_metrics.get('height_cm') == 168.0):
                print(f"   ✅ Profile data retrieved correctly across sessions")
            else:
                print(f"   ❌ Profile data not retrieved correctly")
                success2 = False
        
        # Session 2: Continue editing - add health history
        health_update = {
            "health_history": {
                "primary_health_goals": ["weight_loss", "fitness"],
                "allergies": ["shellfish"],
                "previous_surgeries": [
                    {
                        "id": "cross_surg_001",
                        "name": "Tonsillectomy",
                        "date": "2015-06-10",
                        "details": "Childhood tonsil removal, no complications"
                    }
                ]
            }
        }
        
        success3, updated_profile = self.run_test(
            "Session 2 - Continue Editing (Add Health History)",
            "PUT",
            f"profiles/patient/{test_user_id}",
            200,
            data=health_update
        )
        
        if success3 and updated_profile:
            # Verify original data is still present
            basic_info = updated_profile.get('basic_info', {})
            health_history = updated_profile.get('health_history', {})
            
            if (basic_info.get('full_name') == 'Cross Session Patient' and 
                len(health_history.get('previous_surgeries', [])) == 1):
                print(f"   ✅ Cross-session editing preserved existing data")
            else:
                print(f"   ❌ Cross-session editing lost existing data")
                success3 = False
        
        # Clean up
        cleanup_success, _ = self.run_test(
            "Cleanup Cross-Session Test",
            "DELETE",
            f"profiles/patient/{test_user_id}",
            200
        )
        
        return success1 and success2 and success3 and cleanup_success

    def test_section_based_updates(self):
        """Test that partial profile updates work properly for each profile type"""
        print("\n📝 Testing Section-Based Updates...")
        
        test_user_id = f"section_updates_{datetime.now().strftime('%H%M%S')}"
        
        # Create initial profile with basic_info only
        initial_profile = {
            "user_id": test_user_id,
            "basic_info": {
                "full_name": "Section Update Patient",
                "age": 29,
                "gender": "Female",
                "location": "Portland, OR",
                "timezone": "America/Los_Angeles",
                "preferred_language": "English"
            }
        }
        
        success1, _ = self.run_test(
            "Create Initial Patient Profile (Basic Info Only)",
            "POST",
            "profiles/patient",
            200,
            data=initial_profile
        )
        
        # Test 1: Update only physical_metrics section
        physical_only_update = {
            "physical_metrics": {
                "height_cm": 162.0,
                "current_weight_kg": 58.0,
                "goal_weight_kg": 55.0,
                "body_fat_percentage": 24.0
            }
        }
        
        success2, response2 = self.run_test(
            "Update Only Physical Metrics Section",
            "PUT",
            f"profiles/patient/{test_user_id}",
            200,
            data=physical_only_update
        )
        
        if success2 and response2:
            # Verify basic_info is still present
            basic_info = response2.get('basic_info', {})
            physical_metrics = response2.get('physical_metrics', {})
            
            if (basic_info.get('full_name') == 'Section Update Patient' and 
                physical_metrics.get('height_cm') == 162.0):
                print(f"   ✅ Physical metrics section updated independently")
            else:
                print(f"   ❌ Section update affected other sections")
                success2 = False
        
        # Test 2: Update only health_history section with previous_surgeries
        health_only_update = {
            "health_history": {
                "primary_health_goals": ["fitness", "energy"],
                "allergies": ["dust"],
                "previous_surgeries": [
                    {
                        "id": "section_surg_001",
                        "name": "Dental Surgery",
                        "date": "2021-09-15",
                        "details": "Wisdom tooth extraction, routine procedure"
                    }
                ]
            }
        }
        
        success3, response3 = self.run_test(
            "Update Only Health History Section (with Previous Surgeries)",
            "PUT",
            f"profiles/patient/{test_user_id}",
            200,
            data=health_only_update
        )
        
        if success3 and response3:
            # Verify other sections are still present
            basic_info = response3.get('basic_info', {})
            physical_metrics = response3.get('physical_metrics', {})
            health_history = response3.get('health_history', {})
            
            if (basic_info.get('full_name') == 'Section Update Patient' and 
                physical_metrics.get('height_cm') == 162.0 and
                len(health_history.get('previous_surgeries', [])) == 1):
                print(f"   ✅ Health history section updated independently")
                print(f"   ✅ Previous surgeries preserved in section update")
            else:
                print(f"   ❌ Health history update affected other sections")
                success3 = False
        
        # Clean up
        cleanup_success, _ = self.run_test(
            "Cleanup Section Updates Test",
            "DELETE",
            f"profiles/patient/{test_user_id}",
            200
        )
        
        return success1 and success2 and success3 and cleanup_success

    def run_profile_wizard_tests(self):
        """Run all profile wizard enhancement tests"""
        print("🚀 Starting Profile Wizard Enhancements Backend Tests")
        print(f"🌐 Base URL: {self.base_url}")
        print("=" * 80)

        # Test 1: Previous Surgeries Field Support
        print("\n" + "="*80)
        print("TEST 1: PREVIOUS SURGERIES FIELD SUPPORT")
        print("="*80)
        surgeries_success = self.test_previous_surgeries_support()

        # Test 2: Profile Completion Tracking
        print("\n" + "="*80)
        print("TEST 2: PROFILE COMPLETION TRACKING")
        print("="*80)
        completion_success = self.test_profile_completion_tracking()

        # Test 3: Cross-Session Profile Support
        print("\n" + "="*80)
        print("TEST 3: CROSS-SESSION PROFILE SUPPORT")
        print("="*80)
        cross_session_success = self.test_cross_session_profile_support()

        # Test 4: Section-Based Updates
        print("\n" + "="*80)
        print("TEST 4: SECTION-BASED UPDATES")
        print("="*80)
        section_updates_success = self.test_section_based_updates()

        # Print final results
        print("\n" + "=" * 80)
        print(f"📊 PROFILE WIZARD ENHANCEMENTS TEST RESULTS")
        print("=" * 80)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        print()
        print(f"✅ Previous Surgeries Support: {'PASS' if surgeries_success else 'FAIL'}")
        print(f"✅ Profile Completion Tracking: {'PASS' if completion_success else 'FAIL'}")
        print(f"✅ Cross-Session Profile Support: {'PASS' if cross_session_success else 'FAIL'}")
        print(f"✅ Section-Based Updates: {'PASS' if section_updates_success else 'FAIL'}")
        print()
        
        overall_success = (surgeries_success and completion_success and 
                          cross_session_success and section_updates_success)
        
        if overall_success:
            print("🎉 ALL PROFILE WIZARD ENHANCEMENT TESTS PASSED!")
            print("✅ Backend fully supports profile wizard enhancements")
        else:
            print("❌ SOME TESTS FAILED - Backend needs fixes")
        
        return overall_success

if __name__ == "__main__":
    tester = ProfileWizardEnhancementsTester()
    success = tester.run_profile_wizard_tests()
    sys.exit(0 if success else 1)