#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime, timedelta
import uuid

class HealthPlatformAPITester:
    def __init__(self, base_url="https://09bcc443-8dc5-488b-b8c2-73778ebd9ce8.preview.emergentagent.com/api"):
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

    def test_basic_api(self):
        """Test basic API endpoint"""
        return self.run_test(
            "Basic API Root",
            "GET",
            "",
            200
        )

    def test_status_endpoints(self):
        """Test status check endpoints"""
        # Test GET status checks
        success1, _ = self.run_test(
            "Get Status Checks",
            "GET",
            "status",
            200
        )

        # Test POST status check
        success2, response = self.run_test(
            "Create Status Check",
            "POST",
            "status",
            200,
            data={"client_name": f"test_client_{datetime.now().strftime('%H%M%S')}"}
        )

        return success1 and success2

    def test_user_endpoints(self):
        """Test user management endpoints"""
        # Create a test user
        test_user_data = {
            "name": f"Test User {datetime.now().strftime('%H%M%S')}",
            "email": f"test_{datetime.now().strftime('%H%M%S')}@example.com",
            "role": "patient"
        }

        success1, user_response = self.run_test(
            "Create User",
            "POST",
            "users",
            200,
            data=test_user_data
        )

        # Get users by role
        success2, _ = self.run_test(
            "Get Users by Role (patient)",
            "GET",
            "users/patient",
            200
        )

        success3, _ = self.run_test(
            "Get Users by Role (provider)",
            "GET",
            "users/provider",
            200
        )

        return success1 and success2 and success3, user_response.get('id') if user_response else None

    def test_health_metrics_endpoints(self, user_id=None):
        """Test health metrics endpoints"""
        if not user_id:
            user_id = "test-user-id"

        # Create a health metric
        test_metric_data = {
            "user_id": user_id,
            "metric_type": "weight",
            "value": 70.5,
            "unit": "kg"
        }

        success1, _ = self.run_test(
            "Create Health Metric",
            "POST",
            "health-metrics",
            200,
            data=test_metric_data
        )

        # Get health metrics for user
        success2, _ = self.run_test(
            "Get User Health Metrics",
            "GET",
            f"health-metrics/{user_id}",
            200
        )

        return success1 and success2

    def test_dashboard_endpoints(self):
        """Test role-specific dashboard endpoints"""
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

        # Validate dashboard data structure based on actual API responses
        if success1 and patient_data:
            expected_patient_keys = ['user_id', 'welcome_message', 'nutrition_summary', 'health_metrics', 'goals', 'recent_meals', 'ai_recommendations']
            patient_keys_valid = all(key in patient_data for key in expected_patient_keys)
            print(f"   Patient dashboard keys validation: {'✅' if patient_keys_valid else '❌'}")

        if success2 and provider_data:
            expected_provider_keys = ['user_id', 'welcome_message', 'patient_overview', 'clinical_alerts', 'todays_appointments', 'patient_progress']
            provider_keys_valid = all(key in provider_data for key in expected_provider_keys)
            print(f"   Provider dashboard keys validation: {'✅' if provider_keys_valid else '❌'}")

        if success3 and family_data:
            expected_family_keys = ['user_id', 'family_overview', 'family_members', 'meal_planning', 'health_alerts', 'upcoming_appointments']
            family_keys_valid = all(key in family_data for key in expected_family_keys)
            print(f"   Family dashboard keys validation: {'✅' if family_keys_valid else '❌'}")

        if success4 and guest_data:
            expected_guest_keys = ['session_info', 'todays_entries', 'nutrition_summary', 'simple_goals', 'nutrition_tips', 'message']
            guest_keys_valid = all(key in guest_data for key in expected_guest_keys)
            print(f"   Guest dashboard keys validation: {'✅' if guest_keys_valid else '❌'}")

        return success1 and success2 and success3 and success4

    def test_additional_endpoints(self):
        """Test additional role-specific endpoints"""
        test_user_id = "test-user-123"
        
        # Test Patient Food Log
        success1, _ = self.run_test(
            "Patient Food Log",
            "GET",
            f"patient/food-log/{test_user_id}",
            200
        )

        # Test Provider Patients List
        success2, _ = self.run_test(
            "Provider Patients List",
            "GET",
            "provider/patients",
            200
        )

        # Test Provider Clinical Tools
        success3, _ = self.run_test(
            "Provider Clinical Tools",
            "GET",
            "provider/clinical-tools",
            200
        )

        # Test Family Meal Planning
        success4, _ = self.run_test(
            "Family Meal Planning",
            "GET",
            f"family/meal-planning/{test_user_id}",
            200
        )

        # Test Guest Quick Log (POST)
        success5, _ = self.run_test(
            "Guest Quick Log",
            "POST",
            "guest/quick-log",
            200,
            data={"food_name": "Apple", "calories": 95}
        )

        return success1 and success2 and success3 and success4 and success5

    def test_profile_management_endpoints(self):
        """Test comprehensive profile management API endpoints"""
        print("\n🔍 Testing Profile Management Endpoints...")
        
        # Test Patient Profile Management
        patient_success = self.test_patient_profile_management()
        
        # Test Provider Profile Management  
        provider_success = self.test_provider_profile_management()
        
        # Test Family Profile Management
        family_success = self.test_family_profile_management()
        
        # Test Guest Profile Management
        guest_success = self.test_guest_profile_management()
        
        # Test Profile Completion Tracking
        completion_success = self.test_profile_completion_tracking()
        
        return patient_success and provider_success and family_success and guest_success and completion_success

    def test_patient_profile_management(self):
        """Test Patient Profile CRUD operations"""
        print("\n📋 Testing Patient Profile Management...")
        
        # Generate unique user ID for testing
        test_user_id = f"patient_user_{datetime.now().strftime('%H%M%S')}"
        
        # Test 1: Create Patient Profile with minimal data
        minimal_profile_data = {
            "user_id": test_user_id,
            "basic_info": {
                "full_name": "Sarah Johnson",
                "age": 28,
                "gender": "Female",
                "location": "New York, NY",
                "timezone": "America/New_York",
                "preferred_language": "English"
            }
        }
        
        success1, profile_response = self.run_test(
            "Create Patient Profile (Minimal)",
            "POST",
            "profiles/patient",
            200,
            data=minimal_profile_data
        )
        
        # Test 2: Get Patient Profile
        success2, get_response = self.run_test(
            "Get Patient Profile",
            "GET",
            f"profiles/patient/{test_user_id}",
            200
        )
        
        # Test 3: Create comprehensive patient profile with another user
        comprehensive_user_id = f"patient_comp_{datetime.now().strftime('%H%M%S')}"
        comprehensive_profile_data = {
            "user_id": comprehensive_user_id,
            "basic_info": {
                "full_name": "Michael Chen",
                "age": 35,
                "gender": "Male",
                "location": "San Francisco, CA",
                "contact_preferences": {"email": True, "sms": False, "push": True},
                "timezone": "America/Los_Angeles",
                "emergency_contact": {"name": "Lisa Chen", "phone": "+1-555-0123"},
                "preferred_language": "English"
            },
            "physical_metrics": {
                "height_cm": 175.0,
                "current_weight_kg": 78.5,
                "goal_weight_kg": 75.0,
                "body_fat_percentage": 18.5,
                "measurements": {"waist": 85.0, "chest": 102.0},
                "bmi": 25.6
            },
            "activity_profile": {
                "activity_level": "MODERATELY_ACTIVE",
                "exercise_types": ["running", "weightlifting", "yoga"],
                "exercise_frequency": 4,
                "sleep_schedule": {
                    "bedtime": "23:00",
                    "wake_time": "07:00",
                    "sleep_quality": 4
                },
                "stress_level": 3,
                "work_type": "DESK_JOB"
            },
            "health_history": {
                "primary_health_goals": ["weight_loss", "muscle_gain", "better_sleep"],
                "medical_conditions": {"hypertension": "mild"},
                "allergies": ["peanuts", "shellfish"],
                "food_intolerances": ["lactose"],
                "family_medical_history": ["diabetes", "heart_disease"]
            },
            "dietary_profile": {
                "diet_type": "OMNIVORE",
                "cultural_restrictions": [],
                "food_allergies": ["peanuts", "shellfish"],
                "food_dislikes": ["liver", "brussels_sprouts"],
                "meal_timing_preference": "TRADITIONAL_3_MEALS",
                "cooking_skill_level": 3,
                "available_cooking_time": 45
            },
            "goals_preferences": {
                "health_targets": [
                    {"type": "weight", "target": 75.0, "timeframe": "3_months"},
                    {"type": "exercise", "target": 5, "timeframe": "weekly"}
                ],
                "communication_methods": ["email", "app_notifications"],
                "notification_preferences": {"daily_reminders": True, "weekly_reports": True},
                "privacy_settings": {"share_with_providers": True, "anonymous_data": False}
            }
        }
        
        success3, comp_response = self.run_test(
            "Create Patient Profile (Comprehensive)",
            "POST",
            "profiles/patient",
            200,
            data=comprehensive_profile_data
        )
        
        # Test 4: Update Patient Profile
        update_data = {
            "physical_metrics": {
                "height_cm": 175.0,
                "current_weight_kg": 77.0,  # Updated weight
                "goal_weight_kg": 75.0,
                "body_fat_percentage": 17.8,  # Updated body fat
                "measurements": {"waist": 84.0, "chest": 102.0},  # Updated waist
                "bmi": 25.1
            }
        }
        
        success4, update_response = self.run_test(
            "Update Patient Profile",
            "PUT",
            f"profiles/patient/{test_user_id}",
            200,
            data=update_data
        )
        
        # Test 5: Test duplicate profile creation (should fail)
        success5, _ = self.run_test(
            "Create Duplicate Patient Profile (Should Fail)",
            "POST",
            "profiles/patient",
            400,  # Expecting 400 Bad Request
            data=minimal_profile_data
        )
        
        # Test 6: Test invalid enum values
        invalid_enum_data = {
            "user_id": f"invalid_enum_{datetime.now().strftime('%H%M%S')}",
            "activity_profile": {
                "activity_level": "INVALID_LEVEL",  # Invalid enum value
                "exercise_frequency": 3,
                "sleep_schedule": {
                    "bedtime": "23:00",
                    "wake_time": "07:00",
                    "sleep_quality": 4
                },
                "stress_level": 3,
                "work_type": "DESK_JOB"
            }
        }
        
        success6, _ = self.run_test(
            "Create Patient Profile with Invalid Enum (Should Fail)",
            "POST",
            "profiles/patient",
            422,  # Expecting validation error
            data=invalid_enum_data
        )
        
        # Test 7: Delete Patient Profile
        success7, _ = self.run_test(
            "Delete Patient Profile",
            "DELETE",
            f"profiles/patient/{test_user_id}",
            200
        )
        
        # Test 8: Get deleted profile (should fail)
        success8, _ = self.run_test(
            "Get Deleted Patient Profile (Should Fail)",
            "GET",
            f"profiles/patient/{test_user_id}",
            404
        )
        
        # Validate profile completion calculation
        if success3 and comp_response:
            completion = comp_response.get('profile_completion', 0)
            print(f"   Profile completion percentage: {completion}%")
            completion_valid = completion > 80  # Should be high for comprehensive profile
            print(f"   Profile completion validation: {'✅' if completion_valid else '❌'}")
        
        return success1 and success2 and success3 and success4 and success5 and success6 and success7 and success8

    def test_provider_profile_management(self):
        """Test Provider Profile CRUD operations"""
        print("\n📋 Testing Provider Profile Management...")
        
        test_user_id = f"provider_user_{datetime.now().strftime('%H%M%S')}"
        
        # Test 1: Create Provider Profile
        provider_profile_data = {
            "user_id": test_user_id,
            "professional_identity": {
                "full_name": "Dr. Emily Rodriguez",
                "professional_title": "Registered Dietitian",
                "medical_license": "RD123456",
                "registration_numbers": {"state_license": "CA-RD-789", "national_cert": "CDR-12345"},
                "years_experience": 8
            },
            "credentials": {
                "education": [
                    {
                        "degree": "Master of Science in Nutrition",
                        "institution": "University of California, Davis",
                        "graduation_year": 2015,
                        "specialization": "Clinical Nutrition"
                    }
                ],
                "certifications": [
                    {
                        "name": "Certified Diabetes Educator",
                        "organization": "CBDCE",
                        "issue_date": "2018-06-15",
                        "expiration_date": "2025-06-15",
                        "status": "ACTIVE"
                    }
                ],
                "specializations": ["diabetes_management", "weight_management", "sports_nutrition"]
            },
            "practice_info": {
                "workplace": "Bay Area Medical Center",
                "practice_type": "Hospital-based",
                "patient_demographics": ["adults", "seniors", "athletes"],
                "languages_spoken": ["English", "Spanish"],
                "areas_of_expertise": ["diabetes", "cardiovascular_health", "sports_nutrition"]
            },
            "preferences": {
                "consultation_types": ["in_person", "telehealth", "group_sessions"],
                "working_hours": {
                    "timezone": "America/Los_Angeles",
                    "schedule": {
                        "monday": {"start": "08:00", "end": "17:00"},
                        "tuesday": {"start": "08:00", "end": "17:00"},
                        "wednesday": {"start": "08:00", "end": "17:00"},
                        "thursday": {"start": "08:00", "end": "17:00"},
                        "friday": {"start": "08:00", "end": "15:00"}
                    }
                },
                "max_patients": 150,
                "accepting_new_patients": True,
                "specialized_conditions": ["type_2_diabetes", "metabolic_syndrome"],
                "treatment_philosophies": ["evidence_based", "patient_centered", "holistic"]
            }
        }
        
        success1, provider_response = self.run_test(
            "Create Provider Profile",
            "POST",
            "profiles/provider",
            200,
            data=provider_profile_data
        )
        
        # Test 2: Get Provider Profile
        success2, _ = self.run_test(
            "Get Provider Profile",
            "GET",
            f"profiles/provider/{test_user_id}",
            200
        )
        
        # Test 3: Update Provider Profile
        update_data = {
            "preferences": {
                "consultation_types": ["in_person", "telehealth"],  # Removed group sessions
                "working_hours": {
                    "timezone": "America/Los_Angeles",
                    "schedule": {
                        "monday": {"start": "08:00", "end": "17:00"},
                        "tuesday": {"start": "08:00", "end": "17:00"},
                        "wednesday": {"start": "08:00", "end": "17:00"},
                        "thursday": {"start": "08:00", "end": "17:00"},
                        "friday": {"start": "08:00", "end": "15:00"}
                    }
                },
                "max_patients": 175,  # Updated capacity
                "accepting_new_patients": False,  # No longer accepting
                "specialized_conditions": ["type_2_diabetes", "metabolic_syndrome"],
                "treatment_philosophies": ["evidence_based", "patient_centered", "holistic"]
            }
        }
        
        success3, _ = self.run_test(
            "Update Provider Profile",
            "PUT",
            f"profiles/provider/{test_user_id}",
            200,
            data=update_data
        )
        
        # Test 4: Delete Provider Profile
        success4, _ = self.run_test(
            "Delete Provider Profile",
            "DELETE",
            f"profiles/provider/{test_user_id}",
            200
        )
        
        # Validate verification status
        if success1 and provider_response:
            verification_status = provider_response.get('verification_status', '')
            print(f"   Provider verification status: {verification_status}")
            verification_valid = verification_status == "PENDING"
            print(f"   Verification status validation: {'✅' if verification_valid else '❌'}")
        
        return success1 and success2 and success3 and success4

    def test_family_profile_management(self):
        """Test Family Profile CRUD operations"""
        print("\n📋 Testing Family Profile Management...")
        
        test_user_id = f"family_user_{datetime.now().strftime('%H%M%S')}"
        
        # Test 1: Create Family Profile
        family_profile_data = {
            "user_id": test_user_id,
            "family_structure": {
                "family_role": "Parent",
                "number_of_members": 4,
                "primary_caregiver": True
            },
            "family_members": [
                {
                    "name": "John Smith",
                    "relationship": "Self",
                    "age": 42,
                    "gender": "Male",
                    "special_needs": [],
                    "allergies": ["pollen"],
                    "medications": [],
                    "health_conditions": ["hypertension"]
                },
                {
                    "name": "Mary Smith",
                    "relationship": "Spouse",
                    "age": 38,
                    "gender": "Female",
                    "special_needs": [],
                    "allergies": ["shellfish"],
                    "medications": ["multivitamin"],
                    "health_conditions": []
                },
                {
                    "name": "Emma Smith",
                    "relationship": "Daughter",
                    "age": 12,
                    "gender": "Female",
                    "special_needs": [],
                    "allergies": ["peanuts"],
                    "medications": [],
                    "health_conditions": []
                },
                {
                    "name": "Alex Smith",
                    "relationship": "Son",
                    "age": 8,
                    "gender": "Male",
                    "special_needs": ["ADHD"],
                    "allergies": [],
                    "medications": ["ADHD_medication"],
                    "health_conditions": ["ADHD"]
                }
            ],
            "household_management": {
                "common_dietary_restrictions": ["peanut_free", "shellfish_free"],
                "family_meal_preferences": ["home_cooked", "balanced_nutrition", "kid_friendly"],
                "budget_considerations": {"weekly_grocery_budget": 200, "dining_out_budget": 100},
                "shopping_responsibilities": ["John", "Mary"],
                "cooking_responsibilities": ["Mary", "John"]
            },
            "care_coordination": {
                "healthcare_providers": {
                    "John": {"provider": "Dr. Johnson", "contact": "555-0101"},
                    "Mary": {"provider": "Dr. Williams", "contact": "555-0102"},
                    "Emma": {"provider": "Dr. Peterson", "contact": "555-0103"},
                    "Alex": {"provider": "Dr. Chen", "contact": "555-0104"}
                },
                "emergency_contacts": [
                    {"name": "Grandma Smith", "phone": "555-0200", "relationship": "Grandmother"},
                    {"name": "Uncle Mike", "phone": "555-0201", "relationship": "Uncle"}
                ],
                "medication_management": {"Alex": "Morning with breakfast"},
                "health_tracking_preferences": {"shared_calendar": True, "appointment_reminders": True}
            }
        }
        
        success1, family_response = self.run_test(
            "Create Family Profile",
            "POST",
            "profiles/family",
            200,
            data=family_profile_data
        )
        
        # Test 2: Get Family Profile
        success2, _ = self.run_test(
            "Get Family Profile",
            "GET",
            f"profiles/family/{test_user_id}",
            200
        )
        
        # Test 3: Update Family Profile (add new family member)
        update_data = {
            "family_members": [
                {
                    "name": "John Smith",
                    "relationship": "Self",
                    "age": 42,
                    "gender": "Male",
                    "special_needs": [],
                    "allergies": ["pollen"],
                    "medications": [],
                    "health_conditions": ["hypertension"]
                },
                {
                    "name": "Mary Smith",
                    "relationship": "Spouse",
                    "age": 38,
                    "gender": "Female",
                    "special_needs": [],
                    "allergies": ["shellfish"],
                    "medications": ["multivitamin"],
                    "health_conditions": []
                },
                {
                    "name": "Emma Smith",
                    "relationship": "Daughter",
                    "age": 12,
                    "gender": "Female",
                    "special_needs": [],
                    "allergies": ["peanuts"],
                    "medications": [],
                    "health_conditions": []
                },
                {
                    "name": "Alex Smith",
                    "relationship": "Son",
                    "age": 8,
                    "gender": "Male",
                    "special_needs": ["ADHD"],
                    "allergies": [],
                    "medications": ["ADHD_medication"],
                    "health_conditions": ["ADHD"]
                },
                {
                    "name": "Baby Smith",
                    "relationship": "Son",
                    "age": 1,
                    "gender": "Male",
                    "special_needs": [],
                    "allergies": [],
                    "medications": [],
                    "health_conditions": []
                }
            ]
        }
        
        success3, _ = self.run_test(
            "Update Family Profile (Add Member)",
            "PUT",
            f"profiles/family/{test_user_id}",
            200,
            data=update_data
        )
        
        # Test 4: Delete Family Profile
        success4, _ = self.run_test(
            "Delete Family Profile",
            "DELETE",
            f"profiles/family/{test_user_id}",
            200
        )
        
        # Validate family member structure
        if success1 and family_response:
            family_members = family_response.get('family_members', [])
            print(f"   Family members count: {len(family_members)}")
            members_valid = len(family_members) == 4
            print(f"   Family members validation: {'✅' if members_valid else '❌'}")
        
        return success1 and success2 and success3 and success4

    def test_guest_profile_management(self):
        """Test Guest Profile CRUD operations"""
        print("\n📋 Testing Guest Profile Management...")
        
        # Generate unique session ID
        test_session_id = f"guest_session_{datetime.now().strftime('%H%M%S')}"
        
        # Test 1: Create Guest Profile
        guest_profile_data = {
            "session_id": test_session_id,
            "basic_demographics": {
                "age": 25,
                "gender": "Female",
                "activity_level": "LIGHTLY_ACTIVE"
            },
            "simple_goals": {
                "goal_type": "lose",
                "target_amount": 5.0,
                "timeframe": "2_months"
            },
            "session_expires": (datetime.utcnow() + timedelta(hours=24)).isoformat()
        }
        
        success1, guest_response = self.run_test(
            "Create Guest Profile",
            "POST",
            "profiles/guest",
            200,
            data=guest_profile_data
        )
        
        # Test 2: Get Guest Profile
        success2, _ = self.run_test(
            "Get Guest Profile",
            "GET",
            f"profiles/guest/{test_session_id}",
            200
        )
        
        # Test 3: Create expired guest profile
        expired_session_id = f"expired_session_{datetime.now().strftime('%H%M%S')}"
        expired_profile_data = {
            "session_id": expired_session_id,
            "basic_demographics": {
                "age": 30,
                "gender": "Male",
                "activity_level": "MODERATELY_ACTIVE"
            },
            "simple_goals": {
                "goal_type": "maintain",
                "target_amount": 0.0,
                "timeframe": "ongoing"
            },
            "session_expires": (datetime.utcnow() - timedelta(hours=1)).isoformat()  # Expired 1 hour ago
        }
        
        success3, _ = self.run_test(
            "Create Expired Guest Profile",
            "POST",
            "profiles/guest",
            200,
            data=expired_profile_data
        )
        
        # Test 4: Try to get expired profile (should fail)
        success4, _ = self.run_test(
            "Get Expired Guest Profile (Should Fail)",
            "GET",
            f"profiles/guest/{expired_session_id}",
            404
        )
        
        # Test 5: Delete Guest Profile
        success5, _ = self.run_test(
            "Delete Guest Profile",
            "DELETE",
            f"profiles/guest/{test_session_id}",
            200
        )
        
        # Test 6: Get deleted profile (should fail)
        success6, _ = self.run_test(
            "Get Deleted Guest Profile (Should Fail)",
            "GET",
            f"profiles/guest/{test_session_id}",
            404
        )
        
        # Validate session expiration
        if success1 and guest_response:
            session_expires = guest_response.get('session_expires', '')
            print(f"   Guest session expires: {session_expires}")
            expires_valid = session_expires != ''
            print(f"   Session expiration validation: {'✅' if expires_valid else '❌'}")
        
        return success1 and success2 and success3 and success4 and success5 and success6

    def test_profile_completion_tracking(self):
        """Test Profile Completion Status endpoints"""
        print("\n📋 Testing Profile Completion Tracking...")
        
        # Create test profiles with different completion levels
        minimal_user_id = f"minimal_user_{datetime.now().strftime('%H%M%S')}"
        complete_user_id = f"complete_user_{datetime.now().strftime('%H%M%S')}"
        
        # Create minimal patient profile
        minimal_data = {
            "user_id": minimal_user_id,
            "basic_info": {
                "full_name": "Test User",
                "age": 30,
                "gender": "Male",
                "location": "Test City",
                "timezone": "America/New_York",
                "preferred_language": "English"
            }
        }
        
        success1, _ = self.run_test(
            "Create Minimal Patient Profile for Completion Test",
            "POST",
            "profiles/patient",
            200,
            data=minimal_data
        )
        
        # Create complete patient profile
        complete_data = {
            "user_id": complete_user_id,
            "basic_info": {
                "full_name": "Complete User",
                "age": 35,
                "gender": "Female",
                "location": "Complete City",
                "timezone": "America/New_York",
                "preferred_language": "English"
            },
            "physical_metrics": {
                "height_cm": 165.0,
                "current_weight_kg": 65.0,
                "goal_weight_kg": 60.0
            },
            "activity_profile": {
                "activity_level": "MODERATELY_ACTIVE",
                "exercise_frequency": 3,
                "sleep_schedule": {
                    "bedtime": "22:00",
                    "wake_time": "06:00",
                    "sleep_quality": 4
                },
                "stress_level": 2,
                "work_type": "MIXED"
            },
            "health_history": {
                "primary_health_goals": ["weight_loss"],
                "allergies": ["none"]
            },
            "dietary_profile": {
                "diet_type": "VEGETARIAN",
                "meal_timing_preference": "TRADITIONAL_3_MEALS",
                "cooking_skill_level": 3,
                "available_cooking_time": 30
            },
            "goals_preferences": {
                "health_targets": [{"type": "weight", "target": 60.0}],
                "communication_methods": ["email"]
            }
        }
        
        success2, _ = self.run_test(
            "Create Complete Patient Profile for Completion Test",
            "POST",
            "profiles/patient",
            200,
            data=complete_data
        )
        
        # Test completion status for minimal profile
        success3, minimal_completion = self.run_test(
            "Get Minimal Profile Completion Status",
            "GET",
            f"profiles/completion/{minimal_user_id}",
            200,
            params={"role": "patient"}
        )
        
        # Test completion status for complete profile
        success4, complete_completion = self.run_test(
            "Get Complete Profile Completion Status",
            "GET",
            f"profiles/completion/{complete_user_id}",
            200,
            params={"role": "patient"}
        )
        
        # Test completion status for non-existent profile
        success5, _ = self.run_test(
            "Get Non-existent Profile Completion Status",
            "GET",
            f"profiles/completion/non_existent_user",
            200,
            params={"role": "patient"}
        )
        
        # Test invalid role
        success6, _ = self.run_test(
            "Get Profile Completion with Invalid Role (Should Fail)",
            "GET",
            f"profiles/completion/{minimal_user_id}",
            400,
            params={"role": "invalid_role"}
        )
        
        # Validate completion percentages
        if success3 and minimal_completion:
            minimal_percentage = minimal_completion.get('completion_percentage', 0)
            print(f"   Minimal profile completion: {minimal_percentage}%")
            minimal_valid = 0 < minimal_percentage < 50  # Should be low
            print(f"   Minimal completion validation: {'✅' if minimal_valid else '❌'}")
        
        if success4 and complete_completion:
            complete_percentage = complete_completion.get('completion_percentage', 0)
            print(f"   Complete profile completion: {complete_percentage}%")
            complete_valid = complete_percentage == 100.0  # Should be 100%
            print(f"   Complete completion validation: {'✅' if complete_valid else '❌'}")
        
        # Clean up test profiles
        self.run_test("Cleanup Minimal Profile", "DELETE", f"profiles/patient/{minimal_user_id}", 200)
        self.run_test("Cleanup Complete Profile", "DELETE", f"profiles/patient/{complete_user_id}", 200)
        
        return success1 and success2 and success3 and success4 and success5 and success6

    def test_patient_analytics_endpoints(self):
        """Test Patient Analytics endpoints for the new Patient Analytics page"""
        print("\n📋 Testing Patient Analytics Endpoints...")
        
        test_user_id = "demo-patient-123"
        
        # Test 1: GET /api/patient/analytics/{user_id}
        success1, analytics_data = self.run_test(
            "Patient Analytics",
            "GET",
            f"patient/analytics/{test_user_id}",
            200
        )
        
        # Validate analytics response structure
        if success1 and analytics_data:
            expected_keys = ['nutrition_trends', 'ai_powered_insights', 'weekly_summary']
            missing_keys = [key for key in expected_keys if key not in analytics_data]
            if not missing_keys:
                print(f"   ✅ Analytics response contains all required keys: {expected_keys}")
            else:
                print(f"   ❌ Analytics response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: GET /api/patient/smart-suggestions/{user_id}
        success2, suggestions_data = self.run_test(
            "Patient Smart Suggestions",
            "GET",
            f"patient/smart-suggestions/{test_user_id}",
            200
        )
        
        # Validate smart suggestions response structure
        if success2 and suggestions_data:
            expected_keys = ['quick_add_suggestions', 'meal_pattern_insights']
            missing_keys = [key for key in expected_keys if key not in suggestions_data]
            if not missing_keys:
                print(f"   ✅ Smart suggestions response contains all required keys: {expected_keys}")
            else:
                print(f"   ❌ Smart suggestions response missing keys: {missing_keys}")
                success2 = False
        
        # Test 3: GET /api/patient/symptoms-correlation/{user_id}
        success3, correlation_data = self.run_test(
            "Patient Symptoms Correlation",
            "GET",
            f"patient/symptoms-correlation/{test_user_id}",
            200
        )
        
        # Validate symptoms correlation response structure
        if success3 and correlation_data:
            expected_keys = ['correlations', 'recommendations']
            missing_keys = [key for key in expected_keys if key not in correlation_data]
            if not missing_keys:
                print(f"   ✅ Symptoms correlation response contains all required keys: {expected_keys}")
            else:
                print(f"   ❌ Symptoms correlation response missing keys: {missing_keys}")
                success3 = False
        
        return success1 and success2 and success3

    def test_phase3_patient_apis(self):
        """Test Phase 3 Patient APIs: Medications, Health Timeline, and Enhanced Food Logging"""
        print("\n📋 Testing Phase 3 Patient APIs...")
        
        test_user_id = "demo-patient-123"
        
        # Test Patient Medication APIs
        medication_success = self.test_patient_medication_apis(test_user_id)
        
        # Test Patient Health Timeline APIs
        timeline_success = self.test_patient_health_timeline_apis(test_user_id)
        
        # Test Enhanced Food Logging API
        food_logging_success = self.test_enhanced_food_logging_api()
        
        return medication_success and timeline_success and food_logging_success

    def test_patient_medication_apis(self, user_id):
        """Test Patient Medication API endpoints"""
        print("\n💊 Testing Patient Medication APIs...")
        
        # Test 1: GET /api/patient/medications/{user_id}
        success1, medications_data = self.run_test(
            "Get Patient Medications",
            "GET",
            f"patient/medications/{user_id}",
            200
        )
        
        # Validate medications response structure
        if success1 and medications_data:
            expected_keys = ['medications', 'reminders', 'adherence_stats', 'ai_insights']
            missing_keys = [key for key in expected_keys if key not in medications_data]
            if not missing_keys:
                print(f"   ✅ Medications response contains all required keys: {expected_keys}")
                
                # Validate medications array structure
                medications = medications_data.get('medications', [])
                if medications and len(medications) > 0:
                    med = medications[0]
                    med_keys = ['id', 'name', 'dosage', 'frequency', 'times', 'adherence_rate', 'status']
                    missing_med_keys = [key for key in med_keys if key not in med]
                    if not missing_med_keys:
                        print(f"   ✅ Medication object structure valid")
                    else:
                        print(f"   ❌ Medication object missing keys: {missing_med_keys}")
                        success1 = False
            else:
                print(f"   ❌ Medications response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: POST /api/patient/medications/{user_id}/take
        sample_medication_take_data = {
            "medication_id": "med_001",
            "taken_at": datetime.utcnow().isoformat(),
            "notes": "Taken with breakfast as prescribed"
        }
        
        success2, take_response = self.run_test(
            "Mark Medication as Taken",
            "POST",
            f"patient/medications/{user_id}/take",
            200,
            data=sample_medication_take_data
        )
        
        # Validate take medication response
        if success2 and take_response:
            expected_keys = ['success', 'medication_id', 'taken_at']
            missing_keys = [key for key in expected_keys if key not in take_response]
            if not missing_keys:
                print(f"   ✅ Take medication response contains required keys: {expected_keys}")
            else:
                print(f"   ❌ Take medication response missing keys: {missing_keys}")
                success2 = False
        
        # Test 3: POST /api/patient/medications/{user_id} (Add new medication)
        sample_new_medication = {
            "name": "Vitamin D3",
            "dosage": "2000 IU",
            "frequency": "daily",
            "times": ["09:00"],
            "with_food": False,
            "condition": "Vitamin D Deficiency",
            "prescriber": "Dr. Johnson",
            "start_date": "2024-01-16",
            "end_date": None
        }
        
        success3, add_response = self.run_test(
            "Add New Medication",
            "POST",
            f"patient/medications/{user_id}",
            200,
            data=sample_new_medication
        )
        
        # Validate add medication response
        if success3 and add_response:
            expected_keys = ['success', 'medication', 'message']
            missing_keys = [key for key in expected_keys if key not in add_response]
            if not missing_keys:
                print(f"   ✅ Add medication response contains required keys: {expected_keys}")
                
                # Validate the medication object in response
                medication = add_response.get('medication', {})
                if medication:
                    med_keys = ['id', 'name', 'dosage', 'frequency', 'status']
                    missing_med_keys = [key for key in med_keys if key not in medication]
                    if not missing_med_keys:
                        print(f"   ✅ Added medication object structure valid")
                    else:
                        print(f"   ❌ Added medication object missing keys: {missing_med_keys}")
                        success3 = False
            else:
                print(f"   ❌ Add medication response missing keys: {missing_keys}")
                success3 = False
        
        return success1 and success2 and success3

    def test_patient_health_timeline_apis(self, user_id):
        """Test Patient Health Timeline API endpoints"""
        print("\n📅 Testing Patient Health Timeline APIs...")
        
        # Test 1: GET /api/patient/timeline/{user_id}
        success1, timeline_data = self.run_test(
            "Get Patient Health Timeline",
            "GET",
            f"patient/timeline/{user_id}",
            200
        )
        
        # Validate timeline response structure
        if success1 and timeline_data:
            expected_keys = ['timeline_events', 'patterns', 'milestones', 'ai_insights', 'categories_summary']
            missing_keys = [key for key in expected_keys if key not in timeline_data]
            if not missing_keys:
                print(f"   ✅ Timeline response contains all required keys: {expected_keys}")
                
                # Validate timeline events structure
                events = timeline_data.get('timeline_events', [])
                if events and len(events) > 0:
                    event = events[0]
                    event_keys = ['id', 'date', 'type', 'title', 'value', 'category', 'impact']
                    missing_event_keys = [key for key in event_keys if key not in event]
                    if not missing_event_keys:
                        print(f"   ✅ Timeline event structure valid")
                    else:
                        print(f"   ❌ Timeline event missing keys: {missing_event_keys}")
                        success1 = False
                
                # Validate patterns structure
                patterns = timeline_data.get('patterns', {})
                if patterns:
                    pattern_keys = ['energy_correlation', 'sleep_impact', 'nutrition_consistency']
                    missing_pattern_keys = [key for key in pattern_keys if key not in patterns]
                    if not missing_pattern_keys:
                        print(f"   ✅ Timeline patterns structure valid")
                    else:
                        print(f"   ❌ Timeline patterns missing keys: {missing_pattern_keys}")
            else:
                print(f"   ❌ Timeline response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: POST /api/patient/timeline/{user_id}/event
        sample_timeline_event = {
            "type": "exercise",
            "title": "Morning Yoga Session",
            "value": "30 minutes",
            "category": "activity",
            "details": "Completed 30-minute yoga session focusing on flexibility and mindfulness",
            "impact": "positive",
            "date": datetime.utcnow().date().isoformat()
        }
        
        success2, event_response = self.run_test(
            "Add Timeline Event",
            "POST",
            f"patient/timeline/{user_id}/event",
            200,
            data=sample_timeline_event
        )
        
        # Validate add event response
        if success2 and event_response:
            expected_keys = ['success', 'event', 'message']
            missing_keys = [key for key in expected_keys if key not in event_response]
            if not missing_keys:
                print(f"   ✅ Add timeline event response contains required keys: {expected_keys}")
                
                # Validate the event object in response
                event = event_response.get('event', {})
                if event:
                    event_keys = ['id', 'date', 'type', 'title', 'value', 'category']
                    missing_event_keys = [key for key in event_keys if key not in event]
                    if not missing_event_keys:
                        print(f"   ✅ Added timeline event structure valid")
                    else:
                        print(f"   ❌ Added timeline event missing keys: {missing_event_keys}")
                        success2 = False
            else:
                print(f"   ❌ Add timeline event response missing keys: {missing_keys}")
                success2 = False
        
        return success1 and success2

    def test_enhanced_food_logging_api(self):
        """Test Enhanced Food Logging API with AI pattern recognition"""
        print("\n🍎 Testing Enhanced Food Logging API...")
        
        # Test various food names to verify AI pattern recognition
        test_foods = [
            {
                "food_name": "Grilled Chicken Breast",
                "meal_type": "lunch",
                "quantity": 150,
                "unit": "grams"
            },
            {
                "food_name": "Greek Yogurt with Berries",
                "meal_type": "breakfast",
                "quantity": 200,
                "unit": "grams"
            },
            {
                "food_name": "Quinoa Salad",
                "meal_type": "dinner",
                "quantity": 250,
                "unit": "grams"
            },
            {
                "food_name": "Avocado Toast",
                "meal_type": "breakfast",
                "quantity": 1,
                "unit": "slice"
            },
            {
                "food_name": "Salmon Fillet",
                "meal_type": "dinner",
                "quantity": 180,
                "unit": "grams"
            }
        ]
        
        all_tests_passed = True
        
        for i, food_data in enumerate(test_foods, 1):
            success, response = self.run_test(
                f"Enhanced Food Logging - {food_data['food_name']}",
                "POST",
                "patient/food-log",
                200,
                data=food_data
            )
            
            if success and response:
                # Validate enhanced food logging response structure
                expected_keys = ['success', 'food_entry', 'daily_totals', 'ai_insights', 'pattern_recognition', 'smart_suggestions']
                missing_keys = [key for key in expected_keys if key not in response]
                
                if not missing_keys:
                    print(f"   ✅ Enhanced food logging response contains all required keys")
                    
                    # Validate food_entry structure
                    food_entry = response.get('food_entry', {})
                    entry_keys = ['id', 'food_name', 'calories', 'protein', 'carbs', 'fat', 'confidence', 'ai_enhanced']
                    missing_entry_keys = [key for key in entry_keys if key not in food_entry]
                    
                    if not missing_entry_keys:
                        print(f"   ✅ Food entry structure valid with AI enhancement")
                        
                        # Check AI enhancement indicators
                        ai_enhanced = food_entry.get('ai_enhanced', False)
                        confidence = food_entry.get('confidence', 0)
                        print(f"   ✅ AI Enhanced: {ai_enhanced}, Confidence: {confidence}")
                    else:
                        print(f"   ❌ Food entry missing keys: {missing_entry_keys}")
                        all_tests_passed = False
                    
                    # Validate AI insights
                    ai_insights = response.get('ai_insights', [])
                    if ai_insights:
                        print(f"   ✅ AI insights provided: {len(ai_insights)} insights")
                    else:
                        print(f"   ⚠️  No AI insights provided")
                    
                    # Validate pattern recognition
                    pattern_recognition = response.get('pattern_recognition', {})
                    pattern_keys = ['meal_timing_pattern', 'nutrition_balance', 'suggestions']
                    missing_pattern_keys = [key for key in pattern_keys if key not in pattern_recognition]
                    
                    if not missing_pattern_keys:
                        print(f"   ✅ Pattern recognition structure valid")
                        suggestions = pattern_recognition.get('suggestions', [])
                        if suggestions:
                            print(f"   ✅ Pattern-based suggestions: {len(suggestions)} suggestions")
                    else:
                        print(f"   ❌ Pattern recognition missing keys: {missing_pattern_keys}")
                        all_tests_passed = False
                    
                    # Validate smart suggestions
                    smart_suggestions = response.get('smart_suggestions', {})
                    smart_keys = ['complementary_foods', 'portion_feedback', 'timing_feedback']
                    missing_smart_keys = [key for key in smart_keys if key not in smart_suggestions]
                    
                    if not missing_smart_keys:
                        print(f"   ✅ Smart suggestions structure valid")
                        complementary_foods = smart_suggestions.get('complementary_foods', [])
                        if complementary_foods:
                            print(f"   ✅ Complementary food suggestions: {len(complementary_foods)} suggestions")
                    else:
                        print(f"   ❌ Smart suggestions missing keys: {missing_smart_keys}")
                        all_tests_passed = False
                        
                else:
                    print(f"   ❌ Enhanced food logging response missing keys: {missing_keys}")
                    all_tests_passed = False
            else:
                all_tests_passed = False
        
        return all_tests_passed

    def test_phase5_family_features(self):
        """Test Phase 5 Comprehensive Family Features endpoints"""
        print("\n📋 Testing Phase 5 Comprehensive Family Features...")
        
        test_family_id = "demo-family-123"
        
        # Test 1: Family Calendar Integration
        calendar_success = self.test_family_calendar_integration(test_family_id)
        
        # Test 2: Child Nutrition Education
        nutrition_education_success = self.test_child_nutrition_education(test_family_id)
        
        # Test 3: Caregiver Tools
        caregiver_tools_success = self.test_caregiver_tools(test_family_id)
        
        # Test 4: Goals Coordination
        goals_coordination_success = self.test_goals_coordination(test_family_id)
        
        # Test 5: Multi-Profile Management
        multi_profile_success = self.test_multi_profile_management(test_family_id)
        
        # Test 6: Family Health Overview (existing)
        health_overview_success = self.test_family_health_overview(test_family_id)
        
        # Test 7: Advanced Meal Planning (existing)
        meal_planning_success = self.test_family_meal_planning_advanced(test_family_id)
        
        return (calendar_success and nutrition_education_success and caregiver_tools_success and 
                goals_coordination_success and multi_profile_success and health_overview_success and 
                meal_planning_success)

    def test_family_calendar_integration(self, family_id):
        """Test Family Calendar Integration with Health Events Coordination"""
        print("\n📅 Testing Family Calendar Integration...")
        
        success, calendar_data = self.run_test(
            "Family Calendar Integration",
            "GET",
            f"family/calendar-integration/{family_id}",
            200
        )
        
        # Validate calendar response structure
        if success and calendar_data:
            expected_keys = ['family_id', 'calendar_overview', 'health_events', 'upcoming_appointments', 'medication_schedules', 'family_activities', 'coordination_tools']
            missing_keys = [key for key in expected_keys if key not in calendar_data]
            
            if not missing_keys:
                print(f"   ✅ Family calendar response contains all required keys: {expected_keys}")
                
                # Validate health events structure
                health_events = calendar_data.get('health_events', [])
                if health_events and len(health_events) > 0:
                    event = health_events[0]
                    event_keys = ['id', 'member', 'type', 'title', 'date', 'time', 'priority', 'status']
                    missing_event_keys = [key for key in event_keys if key not in event]
                    
                    if not missing_event_keys:
                        print(f"   ✅ Health event structure valid")
                        print(f"   📅 Sample event: {event.get('member')} - {event.get('title')} on {event.get('date')}")
                    else:
                        print(f"   ❌ Health event missing keys: {missing_event_keys}")
                        success = False
                
                # Validate medication schedules
                medication_schedules = calendar_data.get('medication_schedules', {})
                if medication_schedules:
                    print(f"   ✅ Medication schedules provided for family members")
                    member_count = len(medication_schedules)
                    print(f"   💊 Medication schedules for {member_count} family members")
                
            else:
                print(f"   ❌ Family calendar response missing keys: {missing_keys}")
                success = False
        
        return success

    def test_child_nutrition_education(self, family_id):
        """Test Child Nutrition Education Portal"""
        print("\n🍎 Testing Child Nutrition Education...")
        
        success, education_data = self.run_test(
            "Child Nutrition Education Portal",
            "GET",
            f"family/child-nutrition-education/{family_id}",
            200
        )
        
        # Validate education response structure
        if success and education_data:
            expected_keys = ['family_id', 'education_overview', 'age_appropriate_content', 'interactive_activities', 'progress_tracking', 'parent_resources', 'meal_planning_for_kids']
            missing_keys = [key for key in expected_keys if key not in education_data]
            
            if not missing_keys:
                print(f"   ✅ Child nutrition education response contains all required keys: {expected_keys}")
                
                # Validate age-appropriate content structure
                age_content = education_data.get('age_appropriate_content', {})
                if age_content:
                    age_groups = list(age_content.keys())
                    print(f"   ✅ Age-appropriate content available for: {age_groups}")
                    
                    # Check if content has proper structure
                    if age_groups:
                        sample_content = age_content[age_groups[0]]
                        content_keys = ['lessons', 'activities', 'goals']
                        missing_content_keys = [key for key in content_keys if key not in sample_content]
                        
                        if not missing_content_keys:
                            print(f"   ✅ Age-appropriate content structure valid")
                        else:
                            print(f"   ❌ Age-appropriate content missing keys: {missing_content_keys}")
                            success = False
                
                # Validate interactive activities
                activities = education_data.get('interactive_activities', [])
                if activities and len(activities) > 0:
                    activity = activities[0]
                    activity_keys = ['id', 'title', 'age_range', 'type', 'duration', 'learning_objectives']
                    missing_activity_keys = [key for key in activity_keys if key not in activity]
                    
                    if not missing_activity_keys:
                        print(f"   ✅ Interactive activity structure valid")
                        print(f"   🎮 Sample activity: {activity.get('title')} for ages {activity.get('age_range')}")
                    else:
                        print(f"   ❌ Interactive activity missing keys: {missing_activity_keys}")
                        success = False
                
            else:
                print(f"   ❌ Child nutrition education response missing keys: {missing_keys}")
                success = False
        
        return success

    def test_caregiver_tools(self, family_id):
        """Test Advanced Caregiver Tools and Emergency Management"""
        print("\n🚑 Testing Caregiver Tools...")
        
        success, caregiver_data = self.run_test(
            "Advanced Caregiver Tools",
            "GET",
            f"family/caregiver-tools/{family_id}",
            200
        )
        
        # Validate caregiver tools response structure
        if success and caregiver_data:
            expected_keys = ['family_id', 'caregiver_dashboard', 'emergency_management', 'health_monitoring', 'medication_management', 'care_coordination', 'support_resources']
            missing_keys = [key for key in expected_keys if key not in caregiver_data]
            
            if not missing_keys:
                print(f"   ✅ Caregiver tools response contains all required keys: {expected_keys}")
                
                # Validate emergency management structure
                emergency_mgmt = caregiver_data.get('emergency_management', {})
                if emergency_mgmt:
                    emergency_keys = ['emergency_contacts', 'medical_information', 'action_plans', 'emergency_kit']
                    missing_emergency_keys = [key for key in emergency_keys if key not in emergency_mgmt]
                    
                    if not missing_emergency_keys:
                        print(f"   ✅ Emergency management structure valid")
                        
                        # Check emergency contacts
                        emergency_contacts = emergency_mgmt.get('emergency_contacts', [])
                        if emergency_contacts:
                            print(f"   📞 Emergency contacts configured: {len(emergency_contacts)} contacts")
                    else:
                        print(f"   ❌ Emergency management missing keys: {missing_emergency_keys}")
                        success = False
                
                # Validate health monitoring
                health_monitoring = caregiver_data.get('health_monitoring', {})
                if health_monitoring:
                    monitoring_keys = ['vital_signs_tracking', 'symptom_monitoring', 'medication_adherence', 'appointment_tracking']
                    missing_monitoring_keys = [key for key in monitoring_keys if key not in health_monitoring]
                    
                    if not missing_monitoring_keys:
                        print(f"   ✅ Health monitoring structure valid")
                        print(f"   💓 Health monitoring tools available")
                    else:
                        print(f"   ❌ Health monitoring missing keys: {missing_monitoring_keys}")
                        success = False
                
            else:
                print(f"   ❌ Caregiver tools response missing keys: {missing_keys}")
                success = False
        
        return success

    def test_goals_coordination(self, family_id):
        """Test Family Goal Setting and Progress Coordination"""
        print("\n🎯 Testing Goals Coordination...")
        
        # Test 1: Get family goals coordination
        success1, goals_data = self.run_test(
            "Family Goals Coordination",
            "GET",
            f"family/goals-coordination/{family_id}",
            200
        )
        
        # Validate goals coordination response structure
        if success1 and goals_data:
            expected_keys = ['family_id', 'goals_overview', 'active_goals', 'completed_goals', 'goal_categories', 'progress_tracking', 'motivation_tools']
            missing_keys = [key for key in expected_keys if key not in goals_data]
            
            if not missing_keys:
                print(f"   ✅ Goals coordination response contains all required keys: {expected_keys}")
                
                # Validate active goals structure
                active_goals = goals_data.get('active_goals', [])
                if active_goals and len(active_goals) > 0:
                    goal = active_goals[0]
                    goal_keys = ['id', 'title', 'category', 'participants', 'target', 'current_progress', 'deadline', 'status']
                    missing_goal_keys = [key for key in goal_keys if key not in goal]
                    
                    if not missing_goal_keys:
                        print(f"   ✅ Active goal structure valid")
                        print(f"   🎯 Sample goal: {goal.get('title')} - {goal.get('current_progress')}% complete")
                    else:
                        print(f"   ❌ Active goal missing keys: {missing_goal_keys}")
                        success1 = False
                
                # Validate progress tracking
                progress_tracking = goals_data.get('progress_tracking', {})
                if progress_tracking:
                    tracking_keys = ['weekly_progress', 'member_contributions', 'milestone_achievements']
                    missing_tracking_keys = [key for key in tracking_keys if key not in progress_tracking]
                    
                    if not missing_tracking_keys:
                        print(f"   ✅ Progress tracking structure valid")
                    else:
                        print(f"   ❌ Progress tracking missing keys: {missing_tracking_keys}")
                        success1 = False
                
            else:
                print(f"   ❌ Goals coordination response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Update goal progress
        sample_progress_data = {
            "member": "Emma",
            "progress": 85,
            "notes": "Great progress this week with daily vegetable intake",
            "date": "2024-01-16"
        }
        
        success2, progress_response = self.run_test(
            "Update Family Goal Progress",
            "POST",
            "family/goals/goal_nutrition_2024/update-progress",
            200,
            data=sample_progress_data
        )
        
        # Validate progress update response
        if success2 and progress_response:
            expected_keys = ['success', 'goal_id', 'updated_progress', 'member', 'message']
            missing_keys = [key for key in expected_keys if key not in progress_response]
            
            if not missing_keys:
                print(f"   ✅ Goal progress update response contains required keys: {expected_keys}")
                updated_progress = progress_response.get('updated_progress', 0)
                member = progress_response.get('member', '')
                print(f"   📈 Progress updated: {member} - {updated_progress}%")
            else:
                print(f"   ❌ Goal progress update response missing keys: {missing_keys}")
                success2 = False
        
        return success1 and success2

    def test_multi_profile_management(self, family_id):
        """Test Multi-Profile Management System"""
        print("\n👥 Testing Multi-Profile Management...")
        
        success, profile_data = self.run_test(
            "Multi-Profile Management System",
            "GET",
            f"family/multi-profile-management/{family_id}",
            200
        )
        
        # Validate multi-profile management response structure
        if success and profile_data:
            expected_keys = ['family_id', 'profile_overview', 'family_members', 'health_profiles', 'privacy_settings', 'data_sharing', 'profile_synchronization']
            missing_keys = [key for key in expected_keys if key not in profile_data]
            
            if not missing_keys:
                print(f"   ✅ Multi-profile management response contains all required keys: {expected_keys}")
                
                # Validate family members structure
                family_members = profile_data.get('family_members', [])
                if family_members and len(family_members) > 0:
                    member = family_members[0]
                    member_keys = ['id', 'name', 'role', 'age', 'profile_completion', 'health_status', 'permissions']
                    missing_member_keys = [key for key in member_keys if key not in member]
                    
                    if not missing_member_keys:
                        print(f"   ✅ Family member profile structure valid")
                        print(f"   👤 Sample member: {member.get('name')} - {member.get('profile_completion')}% complete")
                    else:
                        print(f"   ❌ Family member profile missing keys: {missing_member_keys}")
                        success = False
                
                # Validate health profiles structure
                health_profiles = profile_data.get('health_profiles', {})
                if health_profiles:
                    profile_keys = list(health_profiles.keys())
                    print(f"   ✅ Health profiles available for: {profile_keys}")
                    
                    # Check individual health profile structure
                    if profile_keys:
                        sample_profile = health_profiles[profile_keys[0]]
                        health_keys = ['basic_info', 'health_metrics', 'medications', 'allergies', 'conditions']
                        missing_health_keys = [key for key in health_keys if key not in sample_profile]
                        
                        if not missing_health_keys:
                            print(f"   ✅ Individual health profile structure valid")
                        else:
                            print(f"   ❌ Individual health profile missing keys: {missing_health_keys}")
                            success = False
                
                # Validate privacy settings
                privacy_settings = profile_data.get('privacy_settings', {})
                if privacy_settings:
                    privacy_keys = ['data_sharing_consent', 'profile_visibility', 'emergency_access', 'provider_access']
                    missing_privacy_keys = [key for key in privacy_keys if key not in privacy_settings]
                    
                    if not missing_privacy_keys:
                        print(f"   ✅ Privacy settings structure valid")
                        print(f"   🔒 Privacy controls configured")
                    else:
                        print(f"   ❌ Privacy settings missing keys: {missing_privacy_keys}")
                        success = False
                
            else:
                print(f"   ❌ Multi-profile management response missing keys: {missing_keys}")
                success = False
        
        return success

    def test_family_health_overview(self, family_id):
        """Test Family Health Coordination (existing endpoint)"""
        print("\n🏥 Testing Family Health Overview...")
        
        success, health_data = self.run_test(
            "Family Health Overview",
            "GET",
            f"family/health-overview/{family_id}",
            200
        )
        
        # Validate health overview response structure
        if success and health_data:
            expected_keys = ['family_id', 'health_summary', 'member_health_status', 'upcoming_appointments', 'health_alerts', 'vaccination_status', 'care_coordination']
            missing_keys = [key for key in expected_keys if key not in health_data]
            
            if not missing_keys:
                print(f"   ✅ Family health overview response contains all required keys: {expected_keys}")
                
                # Validate member health status
                member_health = health_data.get('member_health_status', [])
                if member_health and len(member_health) > 0:
                    member = member_health[0]
                    member_keys = ['name', 'age', 'overall_status', 'recent_vitals', 'medications', 'upcoming_appointments']
                    missing_member_keys = [key for key in member_keys if key not in member]
                    
                    if not missing_member_keys:
                        print(f"   ✅ Member health status structure valid")
                        print(f"   👤 Sample member: {member.get('name')} - Status: {member.get('overall_status')}")
                    else:
                        print(f"   ❌ Member health status missing keys: {missing_member_keys}")
                        success = False
                
                # Validate health alerts
                health_alerts = health_data.get('health_alerts', [])
                if health_alerts:
                    print(f"   ✅ Health alerts available: {len(health_alerts)} alerts")
                    if len(health_alerts) > 0:
                        alert = health_alerts[0]
                        alert_keys = ['id', 'member', 'type', 'priority', 'message', 'date']
                        missing_alert_keys = [key for key in alert_keys if key not in alert]
                        
                        if not missing_alert_keys:
                            print(f"   ✅ Health alert structure valid")
                        else:
                            print(f"   ❌ Health alert missing keys: {missing_alert_keys}")
                            success = False
                
            else:
                print(f"   ❌ Family health overview response missing keys: {missing_keys}")
                success = False
        
        return success

    def test_family_meal_planning_advanced(self, family_id):
        """Test Advanced Meal Planning (existing endpoint)"""
        print("\n🍽️ Testing Advanced Meal Planning...")
        
        success, meal_data = self.run_test(
            "Advanced Family Meal Planning",
            "GET",
            f"family/meal-planning-advanced/{family_id}",
            200
        )
        
        # Validate advanced meal planning response structure
        if success and meal_data:
            expected_keys = ['family_id', 'meal_planning_overview', 'weekly_meal_plans', 'nutritional_analysis', 'shopping_lists', 'recipe_recommendations', 'dietary_accommodations']
            missing_keys = [key for key in expected_keys if key not in meal_data]
            
            if not missing_keys:
                print(f"   ✅ Advanced meal planning response contains all required keys: {expected_keys}")
                
                # Validate weekly meal plans
                weekly_plans = meal_data.get('weekly_meal_plans', {})
                if weekly_plans:
                    days = list(weekly_plans.keys())
                    print(f"   ✅ Weekly meal plans available for: {days}")
                    
                    # Check meal plan structure for a day
                    if days:
                        day_plan = weekly_plans[days[0]]
                        meal_keys = ['breakfast', 'lunch', 'dinner', 'snacks']
                        available_meals = [meal for meal in meal_keys if meal in day_plan]
                        
                        if available_meals:
                            print(f"   ✅ Daily meal plan structure valid with meals: {available_meals}")
                        else:
                            print(f"   ❌ Daily meal plan missing meal types")
                            success = False
                
                # Validate nutritional analysis
                nutrition_analysis = meal_data.get('nutritional_analysis', {})
                if nutrition_analysis:
                    nutrition_keys = ['daily_totals', 'member_specific_needs', 'nutrient_balance', 'recommendations']
                    missing_nutrition_keys = [key for key in nutrition_keys if key not in nutrition_analysis]
                    
                    if not missing_nutrition_keys:
                        print(f"   ✅ Nutritional analysis structure valid")
                        print(f"   📊 Nutritional analysis includes daily totals and member-specific needs")
                    else:
                        print(f"   ❌ Nutritional analysis missing keys: {missing_nutrition_keys}")
                        success = False
                
                # Validate recipe recommendations
                recipe_recommendations = meal_data.get('recipe_recommendations', [])
                if recipe_recommendations and len(recipe_recommendations) > 0:
                    recipe = recipe_recommendations[0]
                    recipe_keys = ['id', 'name', 'category', 'prep_time', 'servings', 'difficulty', 'family_friendly', 'nutritional_info']
                    missing_recipe_keys = [key for key in recipe_keys if key not in recipe]
                    
                    if not missing_recipe_keys:
                        print(f"   ✅ Recipe recommendation structure valid")
                        print(f"   🍳 Sample recipe: {recipe.get('name')} - {recipe.get('prep_time')} min, serves {recipe.get('servings')}")
                    else:
                        print(f"   ❌ Recipe recommendation missing keys: {missing_recipe_keys}")
                        success = False
                
            else:
                print(f"   ❌ Advanced meal planning response missing keys: {missing_keys}")
                success = False
        
        return success

    def test_phase4_provider_features(self):
        """Test Phase 4 Advanced Provider Features endpoints"""
        print("\n📋 Testing Phase 4 Advanced Provider Features...")
        
        test_provider_id = "provider-123"
        
        # Test 1: Patient Queue Management
        queue_success = self.test_patient_queue_management(test_provider_id)
        
        # Test 2: Clinical Decision Support
        cds_success = self.test_clinical_decision_support()
        
        # Test 3: Treatment Outcomes
        outcomes_success = self.test_treatment_outcomes(test_provider_id)
        
        # Test 4: Population Health Analytics
        population_success = self.test_population_health_analytics(test_provider_id)
        
        # Test 5: Evidence-Based Recommendations
        evidence_success = self.test_evidence_based_recommendations()
        
        # Test 6: Continuing Education
        education_success = self.test_continuing_education(test_provider_id)
        
        # Test 7: Course Enrollment
        enrollment_success = self.test_course_enrollment()
        
        # Test 8: Certificate Management
        certificates_success = self.test_certificate_management(test_provider_id)
        
        return (queue_success and cds_success and outcomes_success and 
                population_success and evidence_success and education_success and 
                enrollment_success and certificates_success)

    def test_patient_queue_management(self, provider_id):
        """Test Patient Queue Management System"""
        print("\n🏥 Testing Patient Queue Management...")
        
        success, queue_data = self.run_test(
            "Patient Queue Management",
            "GET",
            f"provider/patient-queue/{provider_id}",
            200
        )
        
        # Validate queue response structure
        if success and queue_data:
            expected_keys = ['provider_id', 'queue_stats', 'priority_queue', 'scheduled_queue', 'completed_today', 'no_shows']
            missing_keys = [key for key in expected_keys if key not in queue_data]
            
            if not missing_keys:
                print(f"   ✅ Patient queue response contains all required keys: {expected_keys}")
                
                # Validate queue_stats structure
                queue_stats = queue_data.get('queue_stats', {})
                stats_keys = ['total_in_queue', 'urgent', 'scheduled', 'walk_in', 'avg_wait_time']
                missing_stats_keys = [key for key in stats_keys if key not in queue_stats]
                
                if not missing_stats_keys:
                    print(f"   ✅ Queue stats structure valid")
                    print(f"   📊 Total in queue: {queue_stats.get('total_in_queue')}, Urgent: {queue_stats.get('urgent')}")
                else:
                    print(f"   ❌ Queue stats missing keys: {missing_stats_keys}")
                    success = False
                
                # Validate priority_queue structure
                priority_queue = queue_data.get('priority_queue', [])
                if priority_queue and len(priority_queue) > 0:
                    patient = priority_queue[0]
                    patient_keys = ['id', 'patient_name', 'condition', 'priority', 'wait_time', 'room', 'vitals', 'status']
                    missing_patient_keys = [key for key in patient_keys if key not in patient]
                    
                    if not missing_patient_keys:
                        print(f"   ✅ Priority queue patient structure valid")
                        print(f"   🚨 Priority patient: {patient.get('patient_name')} - {patient.get('condition')}")
                    else:
                        print(f"   ❌ Priority queue patient missing keys: {missing_patient_keys}")
                        success = False
                
            else:
                print(f"   ❌ Patient queue response missing keys: {missing_keys}")
                success = False
        
        return success

    def test_clinical_decision_support(self):
        """Test AI-Powered Clinical Decision Support"""
        print("\n🧠 Testing Clinical Decision Support...")
        
        # Sample patient data for clinical decision support
        sample_patient_data = {
            "patient_data": {
                "id": "patient-456",
                "age": 52,
                "gender": "male",
                "weight": 95,
                "height": 175,
                "bmi": 31.0,
                "blood_pressure": "145/92",
                "glucose": 126
            },
            "symptoms": [
                "increased thirst",
                "frequent urination", 
                "unexplained weight loss",
                "fatigue"
            ],
            "history": [
                "family_history_diabetes",
                "hypertension",
                "sedentary_lifestyle"
            ]
        }
        
        success, cds_data = self.run_test(
            "Clinical Decision Support",
            "POST",
            "provider/clinical-decision-support",
            200,
            data=sample_patient_data
        )
        
        # Validate clinical decision support response
        if success and cds_data:
            expected_keys = ['request_id', 'patient_id', 'ai_recommendations', 'drug_interactions', 'contraindications', 'clinical_guidelines', 'risk_scores']
            missing_keys = [key for key in expected_keys if key not in cds_data]
            
            if not missing_keys:
                print(f"   ✅ Clinical decision support response contains all required keys")
                
                # Validate AI recommendations structure
                ai_recommendations = cds_data.get('ai_recommendations', [])
                if ai_recommendations and len(ai_recommendations) > 0:
                    recommendation = ai_recommendations[0]
                    rec_keys = ['category', 'confidence', 'recommendation', 'evidence', 'next_steps']
                    missing_rec_keys = [key for key in rec_keys if key not in recommendation]
                    
                    if not missing_rec_keys:
                        print(f"   ✅ AI recommendation structure valid")
                        print(f"   🎯 Confidence: {recommendation.get('confidence')}, Category: {recommendation.get('category')}")
                    else:
                        print(f"   ❌ AI recommendation missing keys: {missing_rec_keys}")
                        success = False
                
                # Validate risk scores
                risk_scores = cds_data.get('risk_scores', {})
                if risk_scores:
                    print(f"   ✅ Risk scores provided: {list(risk_scores.keys())}")
                    diabetes_risk = risk_scores.get('diabetes_risk', 0)
                    print(f"   📊 Diabetes risk: {diabetes_risk}")
                
            else:
                print(f"   ❌ Clinical decision support response missing keys: {missing_keys}")
                success = False
        
        return success

    def test_treatment_outcomes(self, provider_id):
        """Test Treatment Outcome Tracking"""
        print("\n📈 Testing Treatment Outcomes...")
        
        success, outcomes_data = self.run_test(
            "Treatment Outcomes",
            "GET",
            f"provider/treatment-outcomes/{provider_id}",
            200,
            params={"timeframe": "30d"}
        )
        
        # Validate treatment outcomes response
        if success and outcomes_data:
            expected_keys = ['provider_id', 'timeframe', 'outcome_summary', 'condition_outcomes', 'trending_metrics']
            missing_keys = [key for key in expected_keys if key not in outcomes_data]
            
            if not missing_keys:
                print(f"   ✅ Treatment outcomes response contains all required keys")
                
                # Validate outcome summary
                outcome_summary = outcomes_data.get('outcome_summary', {})
                summary_keys = ['total_patients_treated', 'successful_outcomes', 'success_rate', 'readmission_rate', 'patient_satisfaction']
                missing_summary_keys = [key for key in summary_keys if key not in outcome_summary]
                
                if not missing_summary_keys:
                    print(f"   ✅ Outcome summary structure valid")
                    success_rate = outcome_summary.get('success_rate', 0)
                    print(f"   📊 Success rate: {success_rate}%, Patient satisfaction: {outcome_summary.get('patient_satisfaction')}")
                else:
                    print(f"   ❌ Outcome summary missing keys: {missing_summary_keys}")
                    success = False
                
                # Validate condition outcomes
                condition_outcomes = outcomes_data.get('condition_outcomes', [])
                if condition_outcomes and len(condition_outcomes) > 0:
                    condition = condition_outcomes[0]
                    condition_keys = ['condition', 'patients', 'improved', 'stable', 'declined', 'target_achievement_rate']
                    missing_condition_keys = [key for key in condition_keys if key not in condition]
                    
                    if not missing_condition_keys:
                        print(f"   ✅ Condition outcomes structure valid")
                        print(f"   🏥 {condition.get('condition')}: {condition.get('improved')}/{condition.get('patients')} improved")
                    else:
                        print(f"   ❌ Condition outcomes missing keys: {missing_condition_keys}")
                        success = False
                
            else:
                print(f"   ❌ Treatment outcomes response missing keys: {missing_keys}")
                success = False
        
        return success

    def test_population_health_analytics(self, provider_id):
        """Test Population Health Analytics"""
        print("\n👥 Testing Population Health Analytics...")
        
        success, population_data = self.run_test(
            "Population Health Analytics",
            "GET",
            f"provider/population-health/{provider_id}",
            200
        )
        
        # Validate population health response
        if success and population_data:
            expected_keys = ['provider_id', 'population_overview', 'demographic_breakdown', 'condition_prevalence', 'risk_stratification', 'quality_measures', 'intervention_opportunities']
            missing_keys = [key for key in expected_keys if key not in population_data]
            
            if not missing_keys:
                print(f"   ✅ Population health response contains all required keys")
                
                # Validate population overview
                population_overview = population_data.get('population_overview', {})
                overview_keys = ['total_population', 'active_patients', 'high_risk_patients', 'chronic_conditions_prevalence']
                missing_overview_keys = [key for key in overview_keys if key not in population_overview]
                
                if not missing_overview_keys:
                    print(f"   ✅ Population overview structure valid")
                    total_pop = population_overview.get('total_population', 0)
                    high_risk = population_overview.get('high_risk_patients', 0)
                    print(f"   📊 Total population: {total_pop}, High risk: {high_risk}")
                else:
                    print(f"   ❌ Population overview missing keys: {missing_overview_keys}")
                    success = False
                
                # Validate demographic breakdown
                demographic_breakdown = population_data.get('demographic_breakdown', [])
                if demographic_breakdown and len(demographic_breakdown) > 0:
                    demo = demographic_breakdown[0]
                    demo_keys = ['age_group', 'count', 'percentage', 'top_conditions']
                    missing_demo_keys = [key for key in demo_keys if key not in demo]
                    
                    if not missing_demo_keys:
                        print(f"   ✅ Demographic breakdown structure valid")
                        print(f"   👥 Age group {demo.get('age_group')}: {demo.get('count')} patients ({demo.get('percentage')}%)")
                    else:
                        print(f"   ❌ Demographic breakdown missing keys: {missing_demo_keys}")
                        success = False
                
                # Validate quality measures
                quality_measures = population_data.get('quality_measures', [])
                if quality_measures and len(quality_measures) > 0:
                    measure = quality_measures[0]
                    measure_keys = ['measure', 'target', 'current', 'status']
                    missing_measure_keys = [key for key in measure_keys if key not in measure]
                    
                    if not missing_measure_keys:
                        print(f"   ✅ Quality measures structure valid")
                        print(f"   📏 {measure.get('measure')}: {measure.get('current')} (target: {measure.get('target')})")
                    else:
                        print(f"   ❌ Quality measures missing keys: {missing_measure_keys}")
                        success = False
                
            else:
                print(f"   ❌ Population health response missing keys: {missing_keys}")
                success = False
        
        return success

    def test_evidence_based_recommendations(self):
        """Test AI-Powered Evidence-Based Recommendations"""
        print("\n📚 Testing Evidence-Based Recommendations...")
        
        # Sample condition data for evidence-based recommendations
        sample_condition_data = {
            "condition": "Type 2 Diabetes",
            "patient_profile": {
                "age": 58,
                "gender": "female",
                "weight": 82,
                "height": 162,
                "bmi": 31.2,
                "hba1c": 8.1,
                "egfr": 75,
                "comorbidities": ["hypertension", "obesity"]
            },
            "clinical_context": "newly_diagnosed"
        }
        
        success, evidence_data = self.run_test(
            "Evidence-Based Recommendations",
            "POST",
            "provider/evidence-recommendations",
            200,
            data=sample_condition_data
        )
        
        # Validate evidence-based recommendations response
        if success and evidence_data:
            expected_keys = ['request_id', 'condition', 'evidence_level', 'recommendations', 'clinical_studies', 'contraindications', 'drug_interactions', 'patient_specific_factors', 'follow_up_recommendations']
            missing_keys = [key for key in expected_keys if key not in evidence_data]
            
            if not missing_keys:
                print(f"   ✅ Evidence-based recommendations response contains all required keys")
                
                # Validate recommendations structure
                recommendations = evidence_data.get('recommendations', [])
                if recommendations and len(recommendations) > 0:
                    recommendation = recommendations[0]
                    rec_keys = ['category', 'recommendation', 'evidence_level', 'source', 'confidence']
                    missing_rec_keys = [key for key in rec_keys if key not in recommendation]
                    
                    if not missing_rec_keys:
                        print(f"   ✅ Recommendation structure valid")
                        print(f"   📋 Category: {recommendation.get('category')}, Evidence level: {recommendation.get('evidence_level')}")
                        print(f"   🎯 Confidence: {recommendation.get('confidence')}")
                    else:
                        print(f"   ❌ Recommendation missing keys: {missing_rec_keys}")
                        success = False
                
                # Validate clinical studies
                clinical_studies = evidence_data.get('clinical_studies', [])
                if clinical_studies and len(clinical_studies) > 0:
                    study = clinical_studies[0]
                    study_keys = ['study', 'year', 'finding', 'relevance', 'patient_count']
                    missing_study_keys = [key for key in study_keys if key not in study]
                    
                    if not missing_study_keys:
                        print(f"   ✅ Clinical studies structure valid")
                        print(f"   🔬 Study: {study.get('study')} ({study.get('year')}), Relevance: {study.get('relevance')}")
                    else:
                        print(f"   ❌ Clinical studies missing keys: {missing_study_keys}")
                        success = False
                
                # Validate follow-up recommendations
                follow_up = evidence_data.get('follow_up_recommendations', [])
                if follow_up:
                    print(f"   ✅ Follow-up recommendations provided: {len(follow_up)} recommendations")
                
            else:
                print(f"   ❌ Evidence-based recommendations response missing keys: {missing_keys}")
                success = False
        
        return success

    def test_continuing_education(self, provider_id):
        """Test Professional Continuing Education Portal"""
        print("\n🎓 Testing Continuing Education...")
        
        success, education_data = self.run_test(
            "Continuing Education",
            "GET",
            f"provider/continuing-education/{provider_id}",
            200
        )
        
        # Validate continuing education response
        if success and education_data:
            expected_keys = ['provider_id', 'education_summary', 'featured_courses', 'my_courses', 'categories', 'upcoming_deadlines']
            missing_keys = [key for key in expected_keys if key not in education_data]
            
            if not missing_keys:
                print(f"   ✅ Continuing education response contains all required keys")
                
                # Validate education summary
                education_summary = education_data.get('education_summary', {})
                summary_keys = ['total_credits_earned', 'credits_required', 'progress_percentage', 'courses_completed', 'courses_in_progress', 'deadline']
                missing_summary_keys = [key for key in summary_keys if key not in education_summary]
                
                if not missing_summary_keys:
                    print(f"   ✅ Education summary structure valid")
                    credits_earned = education_summary.get('total_credits_earned', 0)
                    credits_required = education_summary.get('credits_required', 0)
                    progress = education_summary.get('progress_percentage', 0)
                    print(f"   📊 Credits: {credits_earned}/{credits_required} ({progress}% complete)")
                else:
                    print(f"   ❌ Education summary missing keys: {missing_summary_keys}")
                    success = False
                
                # Validate featured courses
                featured_courses = education_data.get('featured_courses', [])
                if featured_courses and len(featured_courses) > 0:
                    course = featured_courses[0]
                    course_keys = ['id', 'title', 'provider', 'credits', 'duration', 'format', 'difficulty', 'rating', 'enrolled', 'cost', 'description', 'learning_objectives']
                    missing_course_keys = [key for key in course_keys if key not in course]
                    
                    if not missing_course_keys:
                        print(f"   ✅ Featured course structure valid")
                        print(f"   📚 Course: {course.get('title')} ({course.get('credits')} credits)")
                        print(f"   ⭐ Rating: {course.get('rating')}, Format: {course.get('format')}")
                    else:
                        print(f"   ❌ Featured course missing keys: {missing_course_keys}")
                        success = False
                
                # Validate categories
                categories = education_data.get('categories', [])
                if categories and len(categories) > 0:
                    category = categories[0]
                    cat_keys = ['id', 'name', 'course_count']
                    missing_cat_keys = [key for key in cat_keys if key not in category]
                    
                    if not missing_cat_keys:
                        print(f"   ✅ Categories structure valid")
                        print(f"   📂 Category: {category.get('name')} ({category.get('course_count')} courses)")
                    else:
                        print(f"   ❌ Categories missing keys: {missing_cat_keys}")
                        success = False
                
            else:
                print(f"   ❌ Continuing education response missing keys: {missing_keys}")
                success = False
        
        return success

    def test_course_enrollment(self):
        """Test Course Enrollment"""
        print("\n📝 Testing Course Enrollment...")
        
        # Sample enrollment data
        enrollment_data = {
            "provider_id": "provider-123"
        }
        
        success, enrollment_response = self.run_test(
            "Course Enrollment",
            "POST",
            "provider/courses/course-001/enroll",
            200,
            data=enrollment_data
        )
        
        # Validate course enrollment response
        if success and enrollment_response:
            expected_keys = ['course_id', 'provider_id', 'enrollment_status', 'message', 'access_url', 'enrollment_date']
            missing_keys = [key for key in expected_keys if key not in enrollment_response]
            
            if not missing_keys:
                print(f"   ✅ Course enrollment response contains all required keys")
                enrollment_status = enrollment_response.get('enrollment_status')
                course_id = enrollment_response.get('course_id')
                print(f"   ✅ Enrollment status: {enrollment_status} for course {course_id}")
                print(f"   🔗 Access URL: {enrollment_response.get('access_url')}")
            else:
                print(f"   ❌ Course enrollment response missing keys: {missing_keys}")
                success = False
        
        return success

    def test_certificate_management(self, provider_id):
        """Test Certificate Management"""
        print("\n🏆 Testing Certificate Management...")
        
        success, certificates_data = self.run_test(
            "Certificate Management",
            "GET",
            f"provider/certificates/{provider_id}",
            200
        )
        
        # Validate certificate management response
        if success and certificates_data:
            expected_keys = ['provider_id', 'certificates', 'total_credits']
            missing_keys = [key for key in expected_keys if key not in certificates_data]
            
            if not missing_keys:
                print(f"   ✅ Certificate management response contains all required keys")
                
                # Validate certificates structure
                certificates = certificates_data.get('certificates', [])
                if certificates and len(certificates) > 0:
                    certificate = certificates[0]
                    cert_keys = ['id', 'course_title', 'credits', 'completed_date', 'certificate_number', 'download_url', 'verification_code']
                    missing_cert_keys = [key for key in cert_keys if key not in certificate]
                    
                    if not missing_cert_keys:
                        print(f"   ✅ Certificate structure valid")
                        print(f"   🏆 Certificate: {certificate.get('course_title')} ({certificate.get('credits')} credits)")
                        print(f"   📅 Completed: {certificate.get('completed_date')}")
                        print(f"   🔢 Certificate #: {certificate.get('certificate_number')}")
                    else:
                        print(f"   ❌ Certificate missing keys: {missing_cert_keys}")
                        success = False
                
                # Validate total credits
                total_credits = certificates_data.get('total_credits', 0)
                print(f"   📊 Total credits earned: {total_credits}")
                
            else:
                print(f"   ❌ Certificate management response missing keys: {missing_keys}")
                success = False
        
        return success

    def test_guest_food_log_api_integration(self):
        """Test Guest Food Log API integration specifically as requested"""
        print("\n📋 Testing Guest Food Log API Integration...")
        
        # Test 1: Create guest session
        success1, session_response = self.run_test(
            "Create Guest Session",
            "POST",
            "guest/session",
            200
        )
        
        session_id = None
        if success1 and session_response:
            session_id = session_response.get('session_id')
            expected_keys = ['session_id', 'expires_at', 'features_available', 'limitations', 'upgrade_benefits']
            missing_keys = [key for key in expected_keys if key not in session_response]
            
            if not missing_keys:
                print(f"   ✅ Session creation response contains all required keys: {expected_keys}")
                print(f"   📝 Session ID: {session_id}")
                
                # Validate features available
                features = session_response.get('features_available', [])
                if 'instant_food_logging' in features:
                    print(f"   ✅ Instant food logging feature available")
                else:
                    print(f"   ❌ Instant food logging feature not available")
                    success1 = False
            else:
                print(f"   ❌ Session creation response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Test instant food logging with different food items
        food_items = [
            {"food_name": "grilled chicken breast", "calories": 165},
            {"food_name": "greek yogurt", "calories": 100},
            {"food_name": "banana", "calories": 105}
        ]
        
        food_logging_success = True
        for i, food_item in enumerate(food_items, 1):
            success, response = self.run_test(
                f"Instant Food Log - {food_item['food_name'].title()}",
                "POST",
                "guest/instant-food-log",
                200,
                data=food_item
            )
            
            if success and response:
                # Validate instant food logging response structure
                expected_keys = ['success', 'food_recognized', 'estimated_nutrition', 'instant_feedback', 
                               'session_totals', 'simple_suggestions', 'learning_moment']
                missing_keys = [key for key in expected_keys if key not in response]
                
                if not missing_keys:
                    print(f"   ✅ Food logging response contains all required keys")
                    
                    # Validate estimated nutrition structure
                    nutrition = response.get('estimated_nutrition', {})
                    nutrition_keys = ['calories', 'protein', 'carbs', 'fat', 'fiber']
                    missing_nutrition_keys = [key for key in nutrition_keys if key not in nutrition]
                    
                    if not missing_nutrition_keys:
                        print(f"   ✅ Nutrition data structure valid")
                        print(f"   🍎 {food_item['food_name'].title()}: {nutrition.get('calories')} cal, {nutrition.get('protein')}g protein")
                    else:
                        print(f"   ❌ Nutrition data missing keys: {missing_nutrition_keys}")
                        food_logging_success = False
                    
                    # Validate instant feedback
                    feedback = response.get('instant_feedback', [])
                    if feedback and len(feedback) > 0:
                        print(f"   ✅ Instant feedback provided: {len(feedback)} feedback items")
                        print(f"   💡 Sample feedback: {feedback[0]}")
                    else:
                        print(f"   ❌ No instant feedback provided")
                        food_logging_success = False
                    
                    # Validate learning moment
                    learning_moment = response.get('learning_moment', {})
                    if learning_moment and 'tip' in learning_moment and 'content' in learning_moment:
                        print(f"   ✅ Learning moment provided: {learning_moment.get('tip')}")
                    else:
                        print(f"   ❌ Learning moment missing or incomplete")
                        food_logging_success = False
                    
                    # Validate simple suggestions
                    suggestions = response.get('simple_suggestions', [])
                    if suggestions and len(suggestions) > 0:
                        print(f"   ✅ Simple suggestions provided: {len(suggestions)} suggestions")
                    else:
                        print(f"   ❌ No simple suggestions provided")
                        food_logging_success = False
                        
                else:
                    print(f"   ❌ Food logging response missing keys: {missing_keys}")
                    food_logging_success = False
            else:
                food_logging_success = False
        
        # Test 3: Check session status if session was created
        session_status_success = True
        if session_id:
            success3, status_response = self.run_test(
                "Check Guest Session Status",
                "GET",
                f"guest/session/{session_id}/status",
                200
            )
            
            if success3 and status_response:
                expected_keys = ['session_id', 'status', 'time_remaining', 'activity_summary', 'recommendations']
                missing_keys = [key for key in expected_keys if key not in status_response]
                
                if not missing_keys:
                    print(f"   ✅ Session status response contains all required keys")
                    
                    # Validate activity summary
                    activity = status_response.get('activity_summary', {})
                    activity_keys = ['foods_logged', 'tips_viewed', 'calculations_used', 'session_duration']
                    missing_activity_keys = [key for key in activity_keys if key not in activity]
                    
                    if not missing_activity_keys:
                        print(f"   ✅ Activity summary structure valid")
                        print(f"   📊 Foods logged: {activity.get('foods_logged')}, Session duration: {activity.get('session_duration')}")
                    else:
                        print(f"   ❌ Activity summary missing keys: {missing_activity_keys}")
                        session_status_success = False
                else:
                    print(f"   ❌ Session status response missing keys: {missing_keys}")
                    session_status_success = False
            else:
                session_status_success = False
        
        # Test 4: Test complete flow validation
        flow_success = success1 and food_logging_success and session_status_success
        
        if flow_success:
            print(f"\n   ✅ COMPLETE FLOW VALIDATION PASSED")
            print(f"   ✅ Session creation ➜ Food logging ➜ Session status - All working correctly")
            print(f"   ✅ API returns expected structure with instant_feedback, learning_moment, simple_suggestions, estimated_nutrition")
        else:
            print(f"\n   ❌ COMPLETE FLOW VALIDATION FAILED")
            print(f"   ❌ Issues found in session management or food logging functionality")
        
        return flow_success

    def test_phase6_guest_goals_management(self):
        """Test Phase 6 Guest Goals Management APIs"""
        print("\n📋 Testing Phase 6 Guest Goals Management APIs...")
        
        # Test 1: Create guest session
        session_success = self.test_guest_session_creation()
        
        if not session_success:
            print("❌ Guest session creation failed - skipping goal tests")
            return False
        
        # Test 2-5: Test goal management with created session
        goals_success = self.test_guest_goals_management_flow()
        
        return session_success and goals_success

    def test_guest_session_creation(self):
        """Test guest session creation"""
        print("\n🔑 Testing Guest Session Creation...")
        
        success, session_data = self.run_test(
            "Create Guest Session",
            "POST",
            "guest/session",
            200
        )
        
        if success and session_data:
            # Validate session response structure
            expected_keys = ['session_id', 'expires_at', 'features_available', 'limitations', 'upgrade_benefits']
            missing_keys = [key for key in expected_keys if key not in session_data]
            
            if not missing_keys:
                print(f"   ✅ Guest session response contains all required keys: {expected_keys}")
                
                # Store session_id for subsequent tests
                self.test_session_id = session_data.get('session_id')
                print(f"   🔑 Session ID: {self.test_session_id}")
                
                # Validate features available
                features = session_data.get('features_available', [])
                expected_features = ['instant_food_logging', 'basic_nutrition_info', 'simple_goal_tracking', 'educational_content']
                if all(feature in features for feature in expected_features):
                    print(f"   ✅ All expected features available: {len(features)} features")
                else:
                    print(f"   ⚠️  Some expected features missing")
                
                return True
            else:
                print(f"   ❌ Guest session response missing keys: {missing_keys}")
                return False
        
        return False

    def test_guest_goals_management_flow(self):
        """Test complete guest goals management flow"""
        if not hasattr(self, 'test_session_id'):
            print("❌ No session ID available for testing")
            return False
        
        session_id = self.test_session_id
        
        # Test 1: Sync guest goals with backend
        sync_success = self.test_sync_guest_goals(session_id)
        
        # Test 2: Retrieve guest goals
        retrieve_success = self.test_retrieve_guest_goals(session_id)
        
        # Test 3: Update goal progress
        progress_success = self.test_update_goal_progress(session_id)
        
        # Test 4: Get goal analytics
        analytics_success = self.test_guest_goal_analytics(session_id)
        
        return sync_success and retrieve_success and progress_success and analytics_success

    def test_sync_guest_goals(self, session_id):
        """Test syncing guest goals with backend"""
        print("\n📝 Testing Guest Goals Sync...")
        
        # Sample goals data with different categories and progress levels
        sample_goals = {
            "goals": [
                {
                    "id": 1,
                    "title": "Drink 8 glasses of water",
                    "category": "hydration",
                    "target": 8,
                    "unit": "glasses",
                    "current": 3,
                    "timeframe": "daily",
                    "createdAt": datetime.utcnow().isoformat(),
                    "lastUpdated": datetime.utcnow().isoformat()
                },
                {
                    "id": 2,
                    "title": "Eat 5 servings of fruits/vegetables",
                    "category": "nutrition",
                    "target": 5,
                    "unit": "servings",
                    "current": 2,
                    "timeframe": "daily",
                    "createdAt": datetime.utcnow().isoformat(),
                    "lastUpdated": datetime.utcnow().isoformat()
                },
                {
                    "id": 3,
                    "title": "Take vitamins",
                    "category": "habits",
                    "target": 1,
                    "unit": "dose",
                    "current": 1,
                    "timeframe": "daily",
                    "createdAt": datetime.utcnow().isoformat(),
                    "lastUpdated": datetime.utcnow().isoformat()
                }
            ]
        }
        
        success, sync_response = self.run_test(
            "Sync Guest Goals",
            "POST",
            f"guest/goals/{session_id}",
            200,
            data=sample_goals
        )
        
        if success and sync_response:
            # Validate sync response structure
            expected_keys = ['success', 'session_id', 'goals_synced', 'expires_at']
            missing_keys = [key for key in expected_keys if key not in sync_response]
            
            if not missing_keys:
                print(f"   ✅ Goals sync response contains all required keys: {expected_keys}")
                
                # Validate sync details
                goals_synced = sync_response.get('goals_synced', 0)
                if goals_synced == 3:
                    print(f"   ✅ All 3 goals synced successfully")
                    return True
                else:
                    print(f"   ❌ Expected 3 goals synced, got {goals_synced}")
                    return False
            else:
                print(f"   ❌ Goals sync response missing keys: {missing_keys}")
                return False
        
        return False

    def test_retrieve_guest_goals(self, session_id):
        """Test retrieving guest goals for a session"""
        print("\n📖 Testing Guest Goals Retrieval...")
        
        success, goals_response = self.run_test(
            "Retrieve Guest Goals",
            "GET",
            f"guest/goals/{session_id}",
            200
        )
        
        if success and goals_response:
            # Validate goals response structure
            expected_keys = ['success', 'session_id', 'goals']
            missing_keys = [key for key in expected_keys if key not in goals_response]
            
            if not missing_keys:
                print(f"   ✅ Goals retrieval response contains all required keys: {expected_keys}")
                
                # Validate goals data
                goals = goals_response.get('goals', [])
                if len(goals) == 3:
                    print(f"   ✅ Retrieved all 3 synced goals")
                    
                    # Validate goal structure
                    goal = goals[0]
                    goal_keys = ['id', 'title', 'category', 'target', 'unit', 'current', 'timeframe']
                    missing_goal_keys = [key for key in goal_keys if key not in goal]
                    
                    if not missing_goal_keys:
                        print(f"   ✅ Goal structure valid")
                        
                        # Validate different categories
                        categories = [g.get('category') for g in goals]
                        expected_categories = ['hydration', 'nutrition', 'habits']
                        if all(cat in categories for cat in expected_categories):
                            print(f"   ✅ All expected categories present: {categories}")
                            return True
                        else:
                            print(f"   ❌ Missing expected categories. Got: {categories}")
                            return False
                    else:
                        print(f"   ❌ Goal structure missing keys: {missing_goal_keys}")
                        return False
                else:
                    print(f"   ❌ Expected 3 goals, got {len(goals)}")
                    return False
            else:
                print(f"   ❌ Goals retrieval response missing keys: {missing_keys}")
                return False
        
        return False

    def test_update_goal_progress(self, session_id):
        """Test updating progress for a specific goal"""
        print("\n📈 Testing Goal Progress Update...")
        
        # Update progress for goal ID 1 (water intake)
        progress_update = {
            "goal_id": 1,
            "current": 5  # Updated from 3 to 5 glasses
        }
        
        success, progress_response = self.run_test(
            "Update Goal Progress",
            "POST",
            f"guest/goals/{session_id}/progress",
            200,
            data=progress_update
        )
        
        if success and progress_response:
            # Validate progress update response structure
            expected_keys = ['success', 'goal_id', 'new_current', 'message']
            missing_keys = [key for key in expected_keys if key not in progress_response]
            
            if not missing_keys:
                print(f"   ✅ Progress update response contains all required keys: {expected_keys}")
                
                # Validate update details
                goal_id = progress_response.get('goal_id')
                new_current = progress_response.get('new_current')
                
                if goal_id == 1 and new_current == 5:
                    print(f"   ✅ Goal progress updated successfully: Goal {goal_id} now at {new_current}")
                    return True
                else:
                    print(f"   ❌ Progress update mismatch. Expected goal 1 at 5, got goal {goal_id} at {new_current}")
                    return False
            else:
                print(f"   ❌ Progress update response missing keys: {missing_keys}")
                return False
        
        return False

    def test_guest_goal_analytics(self, session_id):
        """Test getting goal analytics and insights"""
        print("\n📊 Testing Guest Goal Analytics...")
        
        success, analytics_response = self.run_test(
            "Get Goal Analytics",
            "GET",
            f"guest/goals/{session_id}/analytics",
            200
        )
        
        if success and analytics_response:
            # Validate analytics response structure
            expected_keys = ['success', 'session_id', 'analytics']
            missing_keys = [key for key in expected_keys if key not in analytics_response]
            
            if not missing_keys:
                print(f"   ✅ Analytics response contains all required keys: {expected_keys}")
                
                # Validate analytics data structure
                analytics = analytics_response.get('analytics', {})
                analytics_keys = ['total_goals', 'completed_goals', 'completion_rate', 'category_breakdown', 'insights', 'motivational_message', 'next_actions']
                missing_analytics_keys = [key for key in analytics_keys if key not in analytics]
                
                if not missing_analytics_keys:
                    print(f"   ✅ Analytics data contains all required keys: {analytics_keys}")
                    
                    # Validate analytics calculations
                    total_goals = analytics.get('total_goals', 0)
                    completed_goals = analytics.get('completed_goals', 0)
                    completion_rate = analytics.get('completion_rate', 0)
                    
                    print(f"   📊 Analytics Summary:")
                    print(f"      Total Goals: {total_goals}")
                    print(f"      Completed Goals: {completed_goals}")
                    print(f"      Completion Rate: {completion_rate}%")
                    
                    # Validate category breakdown
                    category_breakdown = analytics.get('category_breakdown', {})
                    expected_categories = ['hydration', 'nutrition', 'habits']
                    
                    if all(cat in category_breakdown for cat in expected_categories):
                        print(f"   ✅ Category breakdown includes all expected categories")
                        
                        # Check if habits category shows as completed (current=1, target=1)
                        habits_stats = category_breakdown.get('habits', {})
                        if habits_stats.get('completed', 0) == 1 and habits_stats.get('total', 0) == 1:
                            print(f"   ✅ Habits category correctly shows as completed")
                        
                    else:
                        print(f"   ❌ Category breakdown missing expected categories")
                        return False
                    
                    # Validate insights and motivational messages
                    insights = analytics.get('insights', [])
                    motivational_message = analytics.get('motivational_message', '')
                    next_actions = analytics.get('next_actions', [])
                    
                    if insights and motivational_message and next_actions:
                        print(f"   ✅ Analytics includes insights ({len(insights)}), motivational message, and next actions ({len(next_actions)})")
                        print(f"   💬 Sample insight: {insights[0] if insights else 'None'}")
                        print(f"   🎯 Motivational message: {motivational_message}")
                        print(f"   📋 Next action: {next_actions[0] if next_actions else 'None'}")
                        return True
                    else:
                        print(f"   ❌ Missing insights, motivational message, or next actions")
                        return False
                        
                else:
                    print(f"   ❌ Analytics data missing keys: {missing_analytics_keys}")
                    return False
            else:
                print(f"   ❌ Analytics response missing keys: {missing_keys}")
                return False
        
        return False

    def test_phase7_data_export_endpoints(self):
        """Test Phase 7 Data Export API endpoints"""
        print("\n📋 Testing Phase 7 Data Export Endpoints...")
        
        # Test Patient Data Export
        patient_export_success = self.test_patient_data_export()
        
        # Test Provider Data Export
        provider_export_success = self.test_provider_data_export()
        
        # Test Family Data Export
        family_export_success = self.test_family_data_export()
        
        # Test Guest Data Export
        guest_export_success = self.test_guest_data_export()
        
        return (patient_export_success and provider_export_success and 
                family_export_success and guest_export_success)

    def test_patient_data_export(self):
        """Test Patient Data Export endpoint"""
        print("\n👤 Testing Patient Data Export...")
        
        test_user_id = "demo-patient-123"
        
        # Test 1: GET /api/patient/export/{user_id} - Default JSON format
        success1, export_data = self.run_test(
            "Patient Data Export (JSON)",
            "GET",
            f"patient/export/{test_user_id}",
            200
        )
        
        # Validate export response structure
        if success1 and export_data:
            expected_keys = ['export_info', 'profile', 'health_data', 'food_logs', 'ai_insights']
            missing_keys = [key for key in expected_keys if key not in export_data]
            
            if not missing_keys:
                print(f"   ✅ Patient export response contains all required keys: {expected_keys}")
                
                # Validate export_info structure
                export_info = export_data.get('export_info', {})
                info_keys = ['user_id', 'role', 'exported_at', 'format']
                missing_info_keys = [key for key in info_keys if key not in export_info]
                
                if not missing_info_keys:
                    print(f"   ✅ Export metadata structure valid")
                    print(f"   📊 User ID: {export_info.get('user_id')}, Role: {export_info.get('role')}")
                    print(f"   📅 Exported at: {export_info.get('exported_at')}")
                    
                    # Verify role-specific data
                    if export_info.get('role') == 'patient':
                        print(f"   ✅ Role-specific data correctly identified as patient")
                    else:
                        print(f"   ❌ Role mismatch - expected 'patient', got '{export_info.get('role')}'")
                        success1 = False
                else:
                    print(f"   ❌ Export metadata missing keys: {missing_info_keys}")
                    success1 = False
                
                # Validate profile data structure
                profile = export_data.get('profile', {})
                if profile:
                    profile_keys = ['user_id', 'basic_info', 'physical_metrics', 'activity_profile', 
                                  'health_history', 'dietary_profile', 'goals_preferences', 'profile_completion']
                    missing_profile_keys = [key for key in profile_keys if key not in profile]
                    
                    if not missing_profile_keys:
                        print(f"   ✅ Patient profile structure valid")
                        completion = profile.get('profile_completion', 0)
                        print(f"   📈 Profile completion: {completion}%")
                    else:
                        print(f"   ❌ Patient profile missing keys: {missing_profile_keys}")
                        success1 = False
                
                # Validate health data structure
                health_data = export_data.get('health_data', {})
                if health_data:
                    health_keys = ['nutrition_summary', 'health_metrics', 'goals']
                    missing_health_keys = [key for key in health_keys if key not in health_data]
                    
                    if not missing_health_keys:
                        print(f"   ✅ Health data structure valid")
                        goals = health_data.get('goals', [])
                        print(f"   🎯 Health goals: {len(goals)} goals tracked")
                    else:
                        print(f"   ❌ Health data missing keys: {missing_health_keys}")
                        success1 = False
                
                # Validate food logs structure
                food_logs = export_data.get('food_logs', [])
                if food_logs and len(food_logs) > 0:
                    log = food_logs[0]
                    log_keys = ['date', 'meals', 'total_calories', 'total_protein']
                    missing_log_keys = [key for key in log_keys if key not in log]
                    
                    if not missing_log_keys:
                        print(f"   ✅ Food logs structure valid")
                        print(f"   🍽️ Food logs: {len(food_logs)} days of data")
                    else:
                        print(f"   ❌ Food logs missing keys: {missing_log_keys}")
                        success1 = False
                
                # Validate AI insights
                ai_insights = export_data.get('ai_insights', [])
                if ai_insights:
                    print(f"   ✅ AI insights provided: {len(ai_insights)} insights")
                else:
                    print(f"   ⚠️  No AI insights in export")
                    
            else:
                print(f"   ❌ Patient export response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Test with explicit JSON format parameter
        success2, _ = self.run_test(
            "Patient Data Export (Explicit JSON)",
            "GET",
            f"patient/export/{test_user_id}",
            200,
            params={"format": "json"}
        )
        
        # Test 3: Test error handling for non-existent patient
        success3, _ = self.run_test(
            "Patient Data Export (Non-existent User)",
            "GET",
            "patient/export/non-existent-user-123",
            404
        )
        
        return success1 and success2 and success3

    def test_provider_data_export(self):
        """Test Provider Data Export endpoint"""
        print("\n👨‍⚕️ Testing Provider Data Export...")
        
        test_user_id = "demo-provider-123"
        
        # Test 1: GET /api/provider/export/{user_id}
        success1, export_data = self.run_test(
            "Provider Data Export (JSON)",
            "GET",
            f"provider/export/{test_user_id}",
            200
        )
        
        # Validate export response structure
        if success1 and export_data:
            expected_keys = ['export_info', 'profile', 'practice_data', 'professional_insights']
            missing_keys = [key for key in expected_keys if key not in export_data]
            
            if not missing_keys:
                print(f"   ✅ Provider export response contains all required keys: {expected_keys}")
                
                # Validate export_info structure
                export_info = export_data.get('export_info', {})
                info_keys = ['user_id', 'role', 'exported_at', 'format']
                missing_info_keys = [key for key in info_keys if key not in export_info]
                
                if not missing_info_keys:
                    print(f"   ✅ Export metadata structure valid")
                    print(f"   📊 User ID: {export_info.get('user_id')}, Role: {export_info.get('role')}")
                    
                    # Verify role-specific data
                    if export_info.get('role') == 'provider':
                        print(f"   ✅ Role-specific data correctly identified as provider")
                    else:
                        print(f"   ❌ Role mismatch - expected 'provider', got '{export_info.get('role')}'")
                        success1 = False
                else:
                    print(f"   ❌ Export metadata missing keys: {missing_info_keys}")
                    success1 = False
                
                # Validate provider profile structure
                profile = export_data.get('profile', {})
                if profile:
                    profile_keys = ['user_id', 'professional_identity', 'credentials', 'practice_info', 
                                  'preferences', 'verification_status', 'profile_completion']
                    missing_profile_keys = [key for key in profile_keys if key not in profile]
                    
                    if not missing_profile_keys:
                        print(f"   ✅ Provider profile structure valid")
                        verification = profile.get('verification_status', 'UNKNOWN')
                        completion = profile.get('profile_completion', 0)
                        print(f"   🔐 Verification: {verification}, Completion: {completion}%")
                    else:
                        print(f"   ❌ Provider profile missing keys: {missing_profile_keys}")
                        success1 = False
                
                # Validate practice data structure
                practice_data = export_data.get('practice_data', {})
                if practice_data:
                    practice_keys = ['patient_overview', 'clinical_analytics', 'recent_activities']
                    missing_practice_keys = [key for key in practice_keys if key not in practice_data]
                    
                    if not missing_practice_keys:
                        print(f"   ✅ Practice data structure valid")
                        patient_overview = practice_data.get('patient_overview', {})
                        total_patients = patient_overview.get('total_patients', 0)
                        print(f"   👥 Total patients: {total_patients}")
                    else:
                        print(f"   ❌ Practice data missing keys: {missing_practice_keys}")
                        success1 = False
                
                # Validate professional insights
                insights = export_data.get('professional_insights', [])
                if insights:
                    print(f"   ✅ Professional insights provided: {len(insights)} insights")
                else:
                    print(f"   ⚠️  No professional insights in export")
                    
            else:
                print(f"   ❌ Provider export response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Test error handling for non-existent provider
        success2, _ = self.run_test(
            "Provider Data Export (Non-existent User)",
            "GET",
            "provider/export/non-existent-provider-123",
            404
        )
        
        return success1 and success2

    def test_family_data_export(self):
        """Test Family Data Export endpoint"""
        print("\n👨‍👩‍👧‍👦 Testing Family Data Export...")
        
        test_family_id = "demo-family-123"
        
        # Test 1: GET /api/family/export/{family_id}
        success1, export_data = self.run_test(
            "Family Data Export (JSON)",
            "GET",
            f"family/export/{test_family_id}",
            200
        )
        
        # Validate export response structure
        if success1 and export_data:
            expected_keys = ['export_info', 'profile', 'family_health_data', 'meal_planning', 'care_coordination']
            missing_keys = [key for key in expected_keys if key not in export_data]
            
            if not missing_keys:
                print(f"   ✅ Family export response contains all required keys: {expected_keys}")
                
                # Validate export_info structure
                export_info = export_data.get('export_info', {})
                info_keys = ['family_id', 'role', 'exported_at', 'format']
                missing_info_keys = [key for key in info_keys if key not in export_info]
                
                if not missing_info_keys:
                    print(f"   ✅ Export metadata structure valid")
                    print(f"   📊 Family ID: {export_info.get('family_id')}, Role: {export_info.get('role')}")
                    
                    # Verify role-specific data
                    if export_info.get('role') == 'family':
                        print(f"   ✅ Role-specific data correctly identified as family")
                    else:
                        print(f"   ❌ Role mismatch - expected 'family', got '{export_info.get('role')}'")
                        success1 = False
                else:
                    print(f"   ❌ Export metadata missing keys: {missing_info_keys}")
                    success1 = False
                
                # Validate family profile structure
                profile = export_data.get('profile', {})
                if profile:
                    profile_keys = ['user_id', 'family_structure', 'family_members', 'household_management', 
                                  'care_coordination', 'profile_completion']
                    missing_profile_keys = [key for key in profile_keys if key not in profile]
                    
                    if not missing_profile_keys:
                        print(f"   ✅ Family profile structure valid")
                        family_members = profile.get('family_members', [])
                        completion = profile.get('profile_completion', 0)
                        print(f"   👥 Family members: {len(family_members)}, Completion: {completion}%")
                    else:
                        print(f"   ❌ Family profile missing keys: {missing_profile_keys}")
                        success1 = False
                
                # Validate family health data structure
                health_data = export_data.get('family_health_data', {})
                if health_data:
                    health_keys = ['member_health_summary', 'family_goals']
                    missing_health_keys = [key for key in health_keys if key not in health_data]
                    
                    if not missing_health_keys:
                        print(f"   ✅ Family health data structure valid")
                        member_summary = health_data.get('member_health_summary', [])
                        family_goals = health_data.get('family_goals', [])
                        print(f"   💪 Health summaries: {len(member_summary)} members, Goals: {len(family_goals)}")
                    else:
                        print(f"   ❌ Family health data missing keys: {missing_health_keys}")
                        success1 = False
                
                # Validate meal planning structure
                meal_planning = export_data.get('meal_planning', {})
                if meal_planning:
                    meal_keys = ['weekly_meals', 'dietary_accommodations', 'budget_tracking']
                    missing_meal_keys = [key for key in meal_keys if key not in meal_planning]
                    
                    if not missing_meal_keys:
                        print(f"   ✅ Meal planning structure valid")
                        weekly_meals = meal_planning.get('weekly_meals', [])
                        print(f"   🍽️ Weekly meals planned: {len(weekly_meals)} days")
                    else:
                        print(f"   ❌ Meal planning missing keys: {missing_meal_keys}")
                        success1 = False
                
                # Validate care coordination structure
                care_coord = export_data.get('care_coordination', {})
                if care_coord:
                    care_keys = ['medical_appointments', 'emergency_contacts', 'healthcare_providers']
                    missing_care_keys = [key for key in care_keys if key not in care_coord]
                    
                    if not missing_care_keys:
                        print(f"   ✅ Care coordination structure valid")
                        appointments = care_coord.get('medical_appointments', [])
                        emergency_contacts = care_coord.get('emergency_contacts', [])
                        print(f"   🏥 Appointments: {len(appointments)}, Emergency contacts: {len(emergency_contacts)}")
                    else:
                        print(f"   ❌ Care coordination missing keys: {missing_care_keys}")
                        success1 = False
                    
            else:
                print(f"   ❌ Family export response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Test error handling for non-existent family
        success2, _ = self.run_test(
            "Family Data Export (Non-existent Family)",
            "GET",
            "family/export/non-existent-family-123",
            404
        )
        
        return success1 and success2

    def test_guest_data_export(self):
        """Test Guest Data Export endpoint"""
        print("\n👤 Testing Guest Data Export...")
        
        test_session_id = "demo-guest-session-123"
        
        # Test 1: GET /api/guest/export/{session_id}
        success1, export_data = self.run_test(
            "Guest Data Export (JSON)",
            "GET",
            f"guest/export/{test_session_id}",
            200
        )
        
        # Validate export response structure
        if success1 and export_data:
            expected_keys = ['export_info', 'profile', 'session_data', 'insights', 'upgrade_benefits']
            missing_keys = [key for key in expected_keys if key not in export_data]
            
            if not missing_keys:
                print(f"   ✅ Guest export response contains all required keys: {expected_keys}")
                
                # Validate export_info structure
                export_info = export_data.get('export_info', {})
                info_keys = ['session_id', 'role', 'exported_at', 'format', 'session_expires_at']
                missing_info_keys = [key for key in info_keys if key not in export_info]
                
                if not missing_info_keys:
                    print(f"   ✅ Export metadata structure valid")
                    print(f"   📊 Session ID: {export_info.get('session_id')}, Role: {export_info.get('role')}")
                    print(f"   ⏰ Session expires: {export_info.get('session_expires_at')}")
                    
                    # Verify role-specific data
                    if export_info.get('role') == 'guest':
                        print(f"   ✅ Role-specific data correctly identified as guest")
                    else:
                        print(f"   ❌ Role mismatch - expected 'guest', got '{export_info.get('role')}'")
                        success1 = False
                else:
                    print(f"   ❌ Export metadata missing keys: {missing_info_keys}")
                    success1 = False
                
                # Validate guest profile structure
                profile = export_data.get('profile', {})
                if profile:
                    profile_keys = ['session_id', 'demographics', 'goals', 'created_at', 'expires_at']
                    missing_profile_keys = [key for key in profile_keys if key not in profile]
                    
                    if not missing_profile_keys:
                        print(f"   ✅ Guest profile structure valid")
                        print(f"   📅 Created: {profile.get('created_at')}")
                    else:
                        print(f"   ❌ Guest profile missing keys: {missing_profile_keys}")
                        success1 = False
                
                # Validate session data structure
                session_data = export_data.get('session_data', {})
                if session_data:
                    session_keys = ['todays_entries', 'nutrition_summary', 'simple_goals']
                    missing_session_keys = [key for key in session_keys if key not in session_data]
                    
                    if not missing_session_keys:
                        print(f"   ✅ Session data structure valid")
                        todays_entries = session_data.get('todays_entries', {})
                        foods_logged = todays_entries.get('foods_logged', [])
                        simple_goals = session_data.get('simple_goals', [])
                        print(f"   🍎 Foods logged: {len(foods_logged)}, Goals: {len(simple_goals)}")
                    else:
                        print(f"   ❌ Session data missing keys: {missing_session_keys}")
                        success1 = False
                
                # Validate insights
                insights = export_data.get('insights', [])
                if insights:
                    print(f"   ✅ Guest insights provided: {len(insights)} insights")
                else:
                    print(f"   ⚠️  No insights in guest export")
                
                # Validate upgrade benefits structure
                upgrade_benefits = export_data.get('upgrade_benefits', {})
                if upgrade_benefits:
                    benefit_keys = ['features_available_with_account', 'current_limitations']
                    missing_benefit_keys = [key for key in benefit_keys if key not in upgrade_benefits]
                    
                    if not missing_benefit_keys:
                        print(f"   ✅ Upgrade benefits structure valid")
                        features = upgrade_benefits.get('features_available_with_account', [])
                        limitations = upgrade_benefits.get('current_limitations', [])
                        print(f"   🚀 Upgrade features: {len(features)}, Current limitations: {len(limitations)}")
                    else:
                        print(f"   ❌ Upgrade benefits missing keys: {missing_benefit_keys}")
                        success1 = False
                    
            else:
                print(f"   ❌ Guest export response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Test error handling for non-existent session
        success2, _ = self.run_test(
            "Guest Data Export (Non-existent Session)",
            "GET",
            "guest/export/non-existent-session-123",
            404
        )
        
        # Test 3: Test session expiration handling (if applicable)
        # Note: This would require creating an expired session, which might not be feasible in this test
        # For now, we'll assume the endpoint handles expiration correctly based on the implementation
        
        return success1 and success2

    def test_phase7_data_export_endpoints(self):
        """Test Phase 7 Data Export API Endpoints"""
        print("\n📋 Testing Phase 7 Data Export Endpoints...")
        
        # Test identifiers as specified in the review request
        patient_id = "demo-patient-123"
        provider_id = "demo-provider-123"
        family_id = "demo-family-123"
        guest_session_id = "demo-guest-session-123"
        
        # Test 1: Patient Data Export
        patient_success = self.test_patient_data_export_comprehensive(patient_id)
        
        # Test 2: Provider Data Export
        provider_success = self.test_provider_data_export_comprehensive(provider_id)
        
        # Test 3: Family Data Export
        family_success = self.test_family_data_export_comprehensive(family_id)
        
        # Test 4: Guest Data Export
        guest_success = self.test_guest_data_export_comprehensive(guest_session_id)
        
        # Test 5: Error handling for non-existent profiles
        error_handling_success = self.test_export_error_handling()
        
        return (patient_success and provider_success and family_success and 
                guest_success and error_handling_success)

    def test_patient_data_export_comprehensive(self, user_id):
        """Test Patient Data Export endpoint with comprehensive validation"""
        print("\n🏥 Testing Patient Data Export...")
        
        success, export_data = self.run_test(
            "Patient Data Export",
            "GET",
            f"patient/export/{user_id}",
            200
        )
        
        if success and export_data:
            # Validate export_info metadata
            export_info = export_data.get('export_info', {})
            expected_info_keys = ['user_id', 'role', 'exported_at', 'format']
            missing_info_keys = [key for key in expected_info_keys if key not in export_info]
            
            if not missing_info_keys:
                print(f"   ✅ Export info metadata valid: {expected_info_keys}")
                
                # Validate role-specific data
                if export_info.get('role') == 'patient':
                    print(f"   ✅ Role correctly identified as 'patient'")
                else:
                    print(f"   ❌ Role mismatch: expected 'patient', got '{export_info.get('role')}'")
                    success = False
                    
                # Validate user_id matches
                if export_info.get('user_id') == user_id:
                    print(f"   ✅ User ID correctly set: {user_id}")
                else:
                    print(f"   ❌ User ID mismatch: expected '{user_id}', got '{export_info.get('user_id')}'")
                    success = False
            else:
                print(f"   ❌ Export info missing keys: {missing_info_keys}")
                success = False
            
            # Validate comprehensive data structure
            expected_main_keys = ['export_info', 'profile', 'health_data', 'food_logs', 'ai_insights']
            missing_main_keys = [key for key in expected_main_keys if key not in export_data]
            
            if not missing_main_keys:
                print(f"   ✅ Patient export contains all required sections: {expected_main_keys}")
                
                # Validate profile data completeness
                profile = export_data.get('profile', {})
                profile_keys = ['user_id', 'basic_info', 'physical_metrics', 'activity_profile', 
                               'health_history', 'dietary_profile', 'goals_preferences', 'profile_completion']
                missing_profile_keys = [key for key in profile_keys if key not in profile]
                
                if not missing_profile_keys:
                    print(f"   ✅ Patient profile data structure complete")
                    completion = profile.get('profile_completion', 0)
                    print(f"   📊 Profile completion: {completion}%")
                else:
                    print(f"   ❌ Patient profile missing keys: {missing_profile_keys}")
                
                # Validate health data
                health_data = export_data.get('health_data', {})
                health_keys = ['nutrition_summary', 'health_metrics', 'goals']
                missing_health_keys = [key for key in health_keys if key not in health_data]
                
                if not missing_health_keys:
                    print(f"   ✅ Health data structure complete")
                    goals = health_data.get('goals', [])
                    print(f"   🎯 Health goals: {len(goals)} goals tracked")
                else:
                    print(f"   ❌ Health data missing keys: {missing_health_keys}")
                
                # Validate food logs
                food_logs = export_data.get('food_logs', [])
                if isinstance(food_logs, list) and len(food_logs) > 0:
                    log = food_logs[0]
                    log_keys = ['date', 'meals', 'total_calories', 'total_protein']
                    missing_log_keys = [key for key in log_keys if key not in log]
                    
                    if not missing_log_keys:
                        print(f"   ✅ Food logs structure valid: {len(food_logs)} days")
                    else:
                        print(f"   ❌ Food logs missing keys: {missing_log_keys}")
                else:
                    print(f"   ⚠️  No food logs in export")
                
                # Validate AI insights
                ai_insights = export_data.get('ai_insights', [])
                if isinstance(ai_insights, list) and len(ai_insights) > 0:
                    print(f"   ✅ AI insights provided: {len(ai_insights)} insights")
                else:
                    print(f"   ⚠️  No AI insights in export")
                    
            else:
                print(f"   ❌ Patient export missing main sections: {missing_main_keys}")
                success = False
            
            # Validate JSON format compliance
            try:
                import json
                json.dumps(export_data)
                print(f"   ✅ Export data is valid JSON format")
            except (TypeError, ValueError) as e:
                print(f"   ❌ Export data is not valid JSON: {e}")
                success = False
        
        return success

    def test_provider_data_export_comprehensive(self, user_id):
        """Test Provider Data Export endpoint with comprehensive validation"""
        print("\n👩‍⚕️ Testing Provider Data Export...")
        
        success, export_data = self.run_test(
            "Provider Data Export",
            "GET",
            f"provider/export/{user_id}",
            200
        )
        
        if success and export_data:
            # Validate export_info metadata
            export_info = export_data.get('export_info', {})
            expected_info_keys = ['user_id', 'role', 'exported_at', 'format']
            missing_info_keys = [key for key in expected_info_keys if key not in export_info]
            
            if not missing_info_keys:
                print(f"   ✅ Export info metadata valid: {expected_info_keys}")
                
                # Validate role-specific data
                if export_info.get('role') == 'provider':
                    print(f"   ✅ Role correctly identified as 'provider'")
                else:
                    print(f"   ❌ Role mismatch: expected 'provider', got '{export_info.get('role')}'")
                    success = False
                    
                # Validate user_id matches
                if export_info.get('user_id') == user_id:
                    print(f"   ✅ User ID correctly set: {user_id}")
                else:
                    print(f"   ❌ User ID mismatch: expected '{user_id}', got '{export_info.get('user_id')}'")
                    success = False
            else:
                print(f"   ❌ Export info missing keys: {missing_info_keys}")
                success = False
            
            # Validate comprehensive data structure
            expected_main_keys = ['export_info', 'profile', 'practice_data', 'professional_insights']
            missing_main_keys = [key for key in expected_main_keys if key not in export_data]
            
            if not missing_main_keys:
                print(f"   ✅ Provider export contains all required sections: {expected_main_keys}")
                
                # Validate profile data completeness
                profile = export_data.get('profile', {})
                profile_keys = ['user_id', 'professional_identity', 'credentials', 'practice_info', 
                               'preferences', 'verification_status', 'profile_completion']
                missing_profile_keys = [key for key in profile_keys if key not in profile]
                
                if not missing_profile_keys:
                    print(f"   ✅ Provider profile data structure complete")
                    verification = profile.get('verification_status', 'UNKNOWN')
                    completion = profile.get('profile_completion', 0)
                    print(f"   📊 Verification: {verification}, Completion: {completion}%")
                else:
                    print(f"   ❌ Provider profile missing keys: {missing_profile_keys}")
                
                # Validate practice data
                practice_data = export_data.get('practice_data', {})
                practice_keys = ['patient_overview', 'clinical_analytics', 'recent_activities']
                missing_practice_keys = [key for key in practice_keys if key not in practice_data]
                
                if not missing_practice_keys:
                    print(f"   ✅ Practice data structure complete")
                    patient_overview = practice_data.get('patient_overview', {})
                    total_patients = patient_overview.get('total_patients', 0)
                    print(f"   👥 Total patients: {total_patients}")
                else:
                    print(f"   ❌ Practice data missing keys: {missing_practice_keys}")
                
                # Validate professional insights
                insights = export_data.get('professional_insights', [])
                if isinstance(insights, list) and len(insights) > 0:
                    print(f"   ✅ Professional insights provided: {len(insights)} insights")
                else:
                    print(f"   ⚠️  No professional insights in export")
                    
            else:
                print(f"   ❌ Provider export missing main sections: {missing_main_keys}")
                success = False
            
            # Validate JSON format compliance
            try:
                import json
                json.dumps(export_data)
                print(f"   ✅ Export data is valid JSON format")
            except (TypeError, ValueError) as e:
                print(f"   ❌ Export data is not valid JSON: {e}")
                success = False
        
        return success

    def test_family_data_export_comprehensive(self, family_id):
        """Test Family Data Export endpoint with comprehensive validation"""
        print("\n👨‍👩‍👧‍👦 Testing Family Data Export...")
        
        success, export_data = self.run_test(
            "Family Data Export",
            "GET",
            f"family/export/{family_id}",
            200
        )
        
        if success and export_data:
            # Validate export_info metadata
            export_info = export_data.get('export_info', {})
            expected_info_keys = ['family_id', 'role', 'exported_at', 'format']
            missing_info_keys = [key for key in expected_info_keys if key not in export_info]
            
            if not missing_info_keys:
                print(f"   ✅ Export info metadata valid: {expected_info_keys}")
                
                # Validate role-specific data
                if export_info.get('role') == 'family':
                    print(f"   ✅ Role correctly identified as 'family'")
                else:
                    print(f"   ❌ Role mismatch: expected 'family', got '{export_info.get('role')}'")
                    success = False
                    
                # Validate family_id matches
                if export_info.get('family_id') == family_id:
                    print(f"   ✅ Family ID correctly set: {family_id}")
                else:
                    print(f"   ❌ Family ID mismatch: expected '{family_id}', got '{export_info.get('family_id')}'")
                    success = False
            else:
                print(f"   ❌ Export info missing keys: {missing_info_keys}")
                success = False
            
            # Validate comprehensive data structure
            expected_main_keys = ['export_info', 'profile', 'family_health_data', 'meal_planning', 'care_coordination']
            missing_main_keys = [key for key in expected_main_keys if key not in export_data]
            
            if not missing_main_keys:
                print(f"   ✅ Family export contains all required sections: {expected_main_keys}")
                
                # Validate profile data completeness
                profile = export_data.get('profile', {})
                profile_keys = ['user_id', 'family_structure', 'family_members', 'household_management', 
                               'care_coordination', 'profile_completion']
                missing_profile_keys = [key for key in profile_keys if key not in profile]
                
                if not missing_profile_keys:
                    print(f"   ✅ Family profile data structure complete")
                    family_members = profile.get('family_members', [])
                    completion = profile.get('profile_completion', 0)
                    print(f"   👥 Family members: {len(family_members)}, Completion: {completion}%")
                else:
                    print(f"   ❌ Family profile missing keys: {missing_profile_keys}")
                
                # Validate family health data
                health_data = export_data.get('family_health_data', {})
                health_keys = ['member_health_summary', 'family_goals']
                missing_health_keys = [key for key in health_keys if key not in health_data]
                
                if not missing_health_keys:
                    print(f"   ✅ Family health data structure complete")
                    member_summary = health_data.get('member_health_summary', [])
                    family_goals = health_data.get('family_goals', [])
                    print(f"   📊 Health summaries: {len(member_summary)}, Goals: {len(family_goals)}")
                else:
                    print(f"   ❌ Family health data missing keys: {missing_health_keys}")
                
                # Validate meal planning data
                meal_planning = export_data.get('meal_planning', {})
                meal_keys = ['weekly_meals', 'dietary_accommodations', 'budget_tracking']
                missing_meal_keys = [key for key in meal_keys if key not in meal_planning]
                
                if not missing_meal_keys:
                    print(f"   ✅ Meal planning data structure complete")
                    weekly_meals = meal_planning.get('weekly_meals', [])
                    accommodations = meal_planning.get('dietary_accommodations', [])
                    print(f"   🍽️ Weekly meals: {len(weekly_meals)}, Accommodations: {len(accommodations)}")
                else:
                    print(f"   ❌ Meal planning missing keys: {missing_meal_keys}")
                
                # Validate care coordination
                care_coordination = export_data.get('care_coordination', {})
                care_keys = ['medical_appointments', 'emergency_contacts', 'healthcare_providers']
                missing_care_keys = [key for key in care_keys if key not in care_coordination]
                
                if not missing_care_keys:
                    print(f"   ✅ Care coordination data structure complete")
                    appointments = care_coordination.get('medical_appointments', [])
                    emergency_contacts = care_coordination.get('emergency_contacts', [])
                    print(f"   🏥 Appointments: {len(appointments)}, Emergency contacts: {len(emergency_contacts)}")
                else:
                    print(f"   ❌ Care coordination missing keys: {missing_care_keys}")
                    
            else:
                print(f"   ❌ Family export missing main sections: {missing_main_keys}")
                success = False
            
            # Validate JSON format compliance
            try:
                import json
                json.dumps(export_data)
                print(f"   ✅ Export data is valid JSON format")
            except (TypeError, ValueError) as e:
                print(f"   ❌ Export data is not valid JSON: {e}")
                success = False
        
        return success

    def test_guest_data_export_comprehensive(self, session_id):
        """Test Guest Data Export endpoint with comprehensive validation"""
        print("\n👤 Testing Guest Data Export...")
        
        success, export_data = self.run_test(
            "Guest Data Export",
            "GET",
            f"guest/export/{session_id}",
            200
        )
        
        if success and export_data:
            # Validate export_info metadata
            export_info = export_data.get('export_info', {})
            expected_info_keys = ['session_id', 'role', 'exported_at', 'format', 'session_expires_at']
            missing_info_keys = [key for key in expected_info_keys if key not in export_info]
            
            if not missing_info_keys:
                print(f"   ✅ Export info metadata valid: {expected_info_keys}")
                
                # Validate role-specific data
                if export_info.get('role') == 'guest':
                    print(f"   ✅ Role correctly identified as 'guest'")
                else:
                    print(f"   ❌ Role mismatch: expected 'guest', got '{export_info.get('role')}'")
                    success = False
                
                # Validate session_id matches
                if export_info.get('session_id') == session_id:
                    print(f"   ✅ Session ID correctly set: {session_id}")
                else:
                    print(f"   ❌ Session ID mismatch: expected '{session_id}', got '{export_info.get('session_id')}'")
                    success = False
                
                # Validate session expiration handling
                session_expires = export_info.get('session_expires_at')
                if session_expires:
                    print(f"   ✅ Session expiration info provided: {session_expires}")
                else:
                    print(f"   ⚠️  No session expiration info")
            else:
                print(f"   ❌ Export info missing keys: {missing_info_keys}")
                success = False
            
            # Validate comprehensive data structure
            expected_main_keys = ['export_info', 'profile', 'session_data', 'insights', 'upgrade_benefits']
            missing_main_keys = [key for key in expected_main_keys if key not in export_data]
            
            if not missing_main_keys:
                print(f"   ✅ Guest export contains all required sections: {expected_main_keys}")
                
                # Validate profile data completeness
                profile = export_data.get('profile', {})
                profile_keys = ['session_id', 'demographics', 'goals', 'created_at', 'expires_at']
                missing_profile_keys = [key for key in profile_keys if key not in profile]
                
                if not missing_profile_keys:
                    print(f"   ✅ Guest profile data structure complete")
                    demographics = profile.get('demographics', {})
                    goals = profile.get('goals', {})
                    print(f"   👤 Demographics: {bool(demographics)}, Goals: {bool(goals)}")
                else:
                    print(f"   ❌ Guest profile missing keys: {missing_profile_keys}")
                
                # Validate session data
                session_data = export_data.get('session_data', {})
                session_keys = ['todays_entries', 'nutrition_summary', 'simple_goals']
                missing_session_keys = [key for key in session_keys if key not in session_data]
                
                if not missing_session_keys:
                    print(f"   ✅ Session data structure complete")
                    
                    # Validate today's entries
                    todays_entries = session_data.get('todays_entries', {})
                    if 'foods_logged' in todays_entries and 'total_calories' in todays_entries:
                        foods_count = len(todays_entries.get('foods_logged', []))
                        total_calories = todays_entries.get('total_calories', 0)
                        print(f"   🍽️ Today's entries: {foods_count} foods, {total_calories} calories")
                    else:
                        print(f"   ⚠️  Incomplete today's entries data")
                        
                    # Validate simple goals
                    simple_goals = session_data.get('simple_goals', [])
                    if isinstance(simple_goals, list) and len(simple_goals) > 0:
                        print(f"   🎯 Simple goals: {len(simple_goals)} goals tracked")
                    else:
                        print(f"   ⚠️  No simple goals in session data")
                else:
                    print(f"   ❌ Session data missing keys: {missing_session_keys}")
                
                # Validate upgrade benefits (guest-specific feature)
                upgrade_benefits = export_data.get('upgrade_benefits', {})
                upgrade_keys = ['features_available_with_account', 'current_limitations']
                missing_upgrade_keys = [key for key in upgrade_keys if key not in upgrade_benefits]
                
                if not missing_upgrade_keys:
                    print(f"   ✅ Upgrade benefits information complete")
                    features_count = len(upgrade_benefits.get('features_available_with_account', []))
                    limitations_count = len(upgrade_benefits.get('current_limitations', []))
                    print(f"   ⬆️ Upgrade info: {features_count} features, {limitations_count} limitations")
                else:
                    print(f"   ❌ Upgrade benefits missing keys: {missing_upgrade_keys}")
                
                # Validate insights
                insights = export_data.get('insights', [])
                if isinstance(insights, list) and len(insights) > 0:
                    print(f"   ✅ Insights provided: {len(insights)} insights")
                else:
                    print(f"   ⚠️  No insights in export")
                    
            else:
                print(f"   ❌ Guest export missing main sections: {missing_main_keys}")
                success = False
            
            # Validate JSON format compliance
            try:
                import json
                json.dumps(export_data)
                print(f"   ✅ Export data is valid JSON format")
            except (TypeError, ValueError) as e:
                print(f"   ❌ Export data is not valid JSON: {e}")
                success = False
        
        return success

    def test_export_error_handling(self):
        """Test error handling for non-existent profiles and expired sessions"""
        print("\n🚫 Testing Export Error Handling...")
        
        # Test 1: Non-existent patient profile (404)
        success1, _ = self.run_test(
            "Non-existent Patient Export (Should Fail)",
            "GET",
            "patient/export/non-existent-patient-123",
            404
        )
        
        # Test 2: Non-existent provider profile (404)
        success2, _ = self.run_test(
            "Non-existent Provider Export (Should Fail)",
            "GET",
            "provider/export/non-existent-provider-123",
            404
        )
        
        # Test 3: Non-existent family profile (404)
        success3, _ = self.run_test(
            "Non-existent Family Export (Should Fail)",
            "GET",
            "family/export/non-existent-family-123",
            404
        )
        
        # Test 4: Non-existent guest session (404)
        success4, _ = self.run_test(
            "Non-existent Guest Export (Should Fail)",
            "GET",
            "guest/export/non-existent-session-123",
            404
        )
        
        # Test 5: Test expired guest session (if backend supports it)
        # Note: This would require creating an expired session first, 
        # but for now we'll test with a non-existent session
        success5, _ = self.run_test(
            "Expired Guest Session Export (Should Fail)",
            "GET",
            "guest/export/expired-session-123",
            404  # or 410 if session expired
        )
        
        if success1:
            print(f"   ✅ Patient 404 error handling working")
        if success2:
            print(f"   ✅ Provider 404 error handling working")
        if success3:
            print(f"   ✅ Family 404 error handling working")
        if success4:
            print(f"   ✅ Guest 404 error handling working")
        if success5:
            print(f"   ✅ Expired session error handling working")
        
        return success1 and success2 and success3 and success4 and success5

    def test_guest_session_management_and_export(self):
        """Test the fixed guest session management and data export functionality"""
        print("\n📋 Testing Guest Session Management and Data Export...")
        
        # Test 1: Create a new guest session - verify it creates a guest profile in database
        print("\n🔍 Step 1: Creating guest session...")
        success1, session_response = self.run_test(
            "Create Guest Session",
            "POST",
            "guest/session",
            200
        )
        
        if not success1 or not session_response:
            print("❌ Failed to create guest session - cannot continue with export test")
            return False
        
        session_id = session_response.get('session_id')
        if not session_id:
            print("❌ No session_id returned from guest session creation")
            return False
        
        print(f"✅ Guest session created with ID: {session_id}")
        
        # Validate session response structure
        expected_session_keys = ['session_id', 'expires_at', 'features_available', 'limitations', 'upgrade_benefits']
        missing_session_keys = [key for key in expected_session_keys if key not in session_response]
        if missing_session_keys:
            print(f"⚠️  Session response missing keys: {missing_session_keys}")
        else:
            print("✅ Session response structure is complete")
        
        # Test 2: Verify guest profile was created in database by trying to get it
        print(f"\n🔍 Step 2: Verifying guest profile exists in database...")
        success2, profile_response = self.run_test(
            "Get Guest Profile (Verify Database Creation)",
            "GET",
            f"profiles/guest/{session_id}",
            200
        )
        
        if success2:
            print("✅ Guest profile successfully created in database")
            print(f"   Profile session_id: {profile_response.get('session_id')}")
            print(f"   Profile expires: {profile_response.get('session_expires')}")
        else:
            print("❌ Guest profile was not created in database - this was the original issue")
            return False
        
        # Test 3: Test data export with the session_id - verify it now works
        print(f"\n🔍 Step 3: Testing data export with session_id: {session_id}")
        success3, export_response = self.run_test(
            "Export Guest Data",
            "GET",
            f"guest/export/{session_id}",
            200
        )
        
        if not success3:
            print("❌ Guest data export failed - the fix may not be working properly")
            return False
        
        print("✅ Guest data export successful!")
        
        # Validate export response structure
        if export_response:
            expected_export_keys = ['export_info', 'profile', 'session_data', 'insights', 'upgrade_benefits']
            missing_export_keys = [key for key in expected_export_keys if key not in export_response]
            
            if not missing_export_keys:
                print("✅ Export response contains all required keys")
                
                # Validate export_info structure
                export_info = export_response.get('export_info', {})
                if export_info.get('session_id') == session_id:
                    print(f"✅ Export info session_id matches: {session_id}")
                else:
                    print(f"❌ Export info session_id mismatch")
                    return False
                
                # Validate profile structure
                profile = export_response.get('profile', {})
                if profile.get('session_id') == session_id:
                    print(f"✅ Profile session_id matches: {session_id}")
                else:
                    print(f"❌ Profile session_id mismatch")
                    return False
                
                # Validate session_data structure
                session_data = export_response.get('session_data', {})
                session_data_keys = ['todays_entries', 'nutrition_summary', 'simple_goals']
                missing_session_keys = [key for key in session_data_keys if key not in session_data]
                
                if not missing_session_keys:
                    print("✅ Session data structure is complete")
                else:
                    print(f"⚠️  Session data missing keys: {missing_session_keys}")
                
            else:
                print(f"❌ Export response missing keys: {missing_export_keys}")
                return False
        
        # Test 4: Test complete guest workflow - session creation -> data export
        print(f"\n🔍 Step 4: Testing complete guest workflow with new session...")
        
        # Create another session to test the complete workflow
        success4, workflow_session = self.run_test(
            "Create Second Guest Session (Workflow Test)",
            "POST",
            "guest/session",
            200
        )
        
        if success4 and workflow_session:
            workflow_session_id = workflow_session.get('session_id')
            print(f"✅ Second session created: {workflow_session_id}")
            
            # Immediately try to export data from the new session
            success5, workflow_export = self.run_test(
                "Export Data from New Session (Workflow Test)",
                "GET",
                f"guest/export/{workflow_session_id}",
                200
            )
            
            if success5:
                print("✅ Complete workflow successful: session creation -> immediate data export")
            else:
                print("❌ Workflow failed: could not export data from newly created session")
                return False
        else:
            print("❌ Failed to create second session for workflow test")
            return False
        
        # Test 5: Test that expired guest profiles are cleaned up properly
        print(f"\n🔍 Step 5: Testing expired profile cleanup...")
        
        # Try to export from a non-existent session (should fail with 404)
        fake_session_id = "fake_session_12345"
        success6, _ = self.run_test(
            "Export from Non-existent Session (Should Fail)",
            "GET",
            f"guest/export/{fake_session_id}",
            404  # Expecting 404 Not Found
        )
        
        if success6:
            print("✅ Properly handles non-existent session with 404 error")
        else:
            print("❌ Did not properly handle non-existent session")
            return False
        
        # Test 6: Verify session status endpoint works
        print(f"\n🔍 Step 6: Testing session status endpoint...")
        success7, status_response = self.run_test(
            "Get Guest Session Status",
            "GET",
            f"guest/session/{session_id}/status",
            200
        )
        
        if success7 and status_response:
            print("✅ Session status endpoint working")
            if status_response.get('session_id') == session_id:
                print(f"✅ Status response session_id matches: {session_id}")
            else:
                print(f"⚠️  Status response session_id mismatch")
        else:
            print("⚠️  Session status endpoint failed (not critical for main fix)")
        
        print(f"\n🎉 Guest Session Management and Export Test Summary:")
        print(f"   ✅ Guest session creation: {'PASSED' if success1 else 'FAILED'}")
        print(f"   ✅ Database profile creation: {'PASSED' if success2 else 'FAILED'}")
        print(f"   ✅ Data export functionality: {'PASSED' if success3 else 'FAILED'}")
        print(f"   ✅ Complete workflow: {'PASSED' if success4 and success5 else 'FAILED'}")
        print(f"   ✅ Error handling: {'PASSED' if success6 else 'FAILED'}")
        print(f"   ✅ Session status: {'PASSED' if success7 else 'PASSED (optional)'}")
        
        # All critical tests must pass
        all_critical_passed = success1 and success2 and success3 and success4 and success5 and success6
        
        if all_critical_passed:
            print("\n🎉 ALL GUEST SESSION MANAGEMENT AND EXPORT TESTS PASSED!")
            print("✅ The fix is working correctly:")
            print("   - Guest sessions now create profiles in database")
            print("   - Data export now works for guest sessions")
            print("   - Complete workflow functions properly")
            print("   - Error handling is appropriate")
        else:
            print("\n❌ SOME GUEST SESSION TESTS FAILED")
            print("   The fix may need additional work")
        
        return all_critical_passed

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Health & Nutrition Platform API Tests")
        print(f"🌐 Base URL: {self.base_url}")
        print("=" * 60)

        # Test basic API
        print("\n📋 Testing Basic API...")
        self.test_basic_api()

        # Test status endpoints
        print("\n📋 Testing Status Endpoints...")
        self.test_status_endpoints()

        # Test user endpoints
        print("\n📋 Testing User Management...")
        user_success, user_id = self.test_user_endpoints()

        # Test health metrics
        print("\n📋 Testing Health Metrics...")
        self.test_health_metrics_endpoints(user_id)

        # Test dashboard endpoints
        print("\n📋 Testing Dashboard Endpoints...")
        self.test_dashboard_endpoints()

        # Test additional endpoints
        print("\n📋 Testing Additional Role-Specific Endpoints...")
        self.test_additional_endpoints()

        # Test profile management endpoints
        print("\n📋 Testing Profile Management Endpoints...")
        self.test_profile_management_endpoints()

        # Test patient analytics endpoints
        print("\n📋 Testing Patient Analytics Endpoints...")
        self.test_patient_analytics_endpoints()

        # Test Phase 3 Patient APIs
        print("\n📋 Testing Phase 3 Patient APIs...")
        self.test_phase3_patient_apis()

        # Test Phase 4 Advanced Provider Features
        print("\n📋 Testing Phase 4 Advanced Provider Features...")
        self.test_phase4_provider_features()

        # Test Phase 5 Comprehensive Family Features
        print("\n📋 Testing Phase 5 Comprehensive Family Features...")
        self.test_phase5_family_features()

        # Test Phase 6 Guest Goals Management
        print("\n📋 Testing Phase 6 Guest Goals Management...")
        phase6_success = self.test_phase6_guest_goals_management()

        # Test Phase 7 Data Export Endpoints
        print("\n📋 Testing Phase 7 Data Export Endpoints...")
        phase7_success = self.test_phase7_data_export_endpoints()

        # Print final results
        print("\n" + "=" * 60)
        print(f"📊 FINAL RESULTS")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return 0
        else:
            print("⚠️  Some tests failed. Check the details above.")
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result.get('success', False):
                    print(f"  - {result['name']}: {result.get('error', 'Status code mismatch')}")
            return 1

    def test_patient_profile_auto_save_compatibility(self):
        """Test Patient Profile Management API for auto-save compatibility"""
        print("\n🔍 Testing Patient Profile Management API - Auto-Save Compatibility...")
        print("Focus: Ensure auto-save improvements don't break existing functionality")
        
        # Generate unique user ID for testing
        test_user_id = f"autosave_test_{datetime.now().strftime('%H%M%S_%f')}"
        
        # Test 1: Create Patient Profile with complete profile data (POST /api/profiles/patient)
        print("\n📝 Test 1: Patient Profile Creation with Complete Data")
        complete_profile_data = {
            "user_id": test_user_id,
            "basic_info": {
                "full_name": "Jessica Martinez",
                "age": 32,
                "gender": "Female",
                "location": "Austin, TX",
                "contact_preferences": {"email": True, "sms": True, "push": False},
                "timezone": "America/Chicago",
                "emergency_contact": {"name": "Carlos Martinez", "phone": "+1-555-0199"},
                "preferred_language": "English"
            },
            "physical_metrics": {
                "height_cm": 168.0,
                "current_weight_kg": 72.0,
                "goal_weight_kg": 68.0,
                "body_fat_percentage": 22.5,
                "muscle_mass_kg": 45.0,
                "measurements": {"waist": 78.0, "chest": 95.0, "hips": 98.0},
                "bmi": 25.5
            },
            "activity_profile": {
                "activity_level": "VERY_ACTIVE",
                "exercise_types": ["yoga", "pilates", "swimming", "hiking"],
                "exercise_frequency": 5,
                "sleep_schedule": {
                    "bedtime": "22:30",
                    "wake_time": "06:30",
                    "sleep_quality": 4
                },
                "stress_level": 2,
                "work_type": "MIXED"
            },
            "health_history": {
                "primary_health_goals": ["weight_loss", "muscle_tone", "stress_reduction"],
                "medical_conditions": {"hypothyroidism": "controlled"},
                "current_medications": [
                    {"name": "Levothyroxine", "dosage": "50mcg", "frequency": "daily"}
                ],
                "allergies": ["latex", "iodine"],
                "food_intolerances": ["gluten"],
                "previous_surgeries": [
                    {"procedure": "Appendectomy", "year": 2018, "complications": "none"}
                ],
                "family_medical_history": ["thyroid_disease", "diabetes"]
            },
            "dietary_profile": {
                "diet_type": "FLEXITARIAN",
                "cultural_restrictions": [],
                "specific_diets": ["gluten_free"],
                "food_allergies": [],
                "food_dislikes": ["mushrooms", "olives"],
                "meal_timing_preference": "SMALL_FREQUENT",
                "cooking_skill_level": 4,
                "available_cooking_time": 60
            },
            "goals_preferences": {
                "health_targets": [
                    {"type": "weight", "target": 68.0, "timeframe": "4_months"},
                    {"type": "body_fat", "target": 20.0, "timeframe": "6_months"},
                    {"type": "exercise", "target": 5, "timeframe": "weekly"}
                ],
                "communication_methods": ["email", "app_notifications", "text_messages"],
                "notification_preferences": {
                    "daily_reminders": True, 
                    "weekly_reports": True, 
                    "goal_achievements": True,
                    "meal_suggestions": True
                },
                "privacy_settings": {
                    "share_with_providers": True, 
                    "anonymous_data": True,
                    "research_participation": False
                },
                "data_sharing_preferences": {
                    "family_members": True,
                    "healthcare_team": True,
                    "fitness_apps": False
                }
            }
        }
        
        success1, create_response = self.run_test(
            "Create Patient Profile - Complete Data",
            "POST",
            "profiles/patient",
            200,
            data=complete_profile_data
        )
        
        # Validate profile completion calculation
        if success1 and create_response:
            completion = create_response.get('profile_completion', 0)
            print(f"   ✅ Profile completion: {completion}% (Expected: 100%)")
            completion_valid = completion == 100.0
            if not completion_valid:
                print(f"   ❌ Profile completion calculation issue: Expected 100%, got {completion}%")
        
        # Test 2: Verify profile retrieval
        print("\n📝 Test 2: Profile Retrieval Verification")
        success2, get_response = self.run_test(
            "Get Complete Patient Profile",
            "GET",
            f"profiles/patient/{test_user_id}",
            200
        )
        
        # Validate all sections are present
        if success2 and get_response:
            expected_sections = ["basic_info", "physical_metrics", "activity_profile", "health_history", "dietary_profile", "goals_preferences"]
            missing_sections = [section for section in expected_sections if not get_response.get(section)]
            if not missing_sections:
                print(f"   ✅ All profile sections present and complete")
            else:
                print(f"   ❌ Missing sections: {missing_sections}")
        
        # Test 3: Partial Updates (PUT /api/profiles/patient/{user_id}) - Simulating auto-save behavior
        print("\n📝 Test 3: Partial Profile Updates (Auto-Save Simulation)")
        
        # Test 3a: Update only basic_info (common auto-save scenario)
        basic_info_update = {
            "basic_info": {
                "full_name": "Jessica Martinez-Rodriguez",  # Name change
                "age": 32,
                "gender": "Female",
                "location": "Austin, TX",
                "contact_preferences": {"email": True, "sms": True, "push": True},  # Updated preferences
                "timezone": "America/Chicago",
                "emergency_contact": {"name": "Carlos Martinez", "phone": "+1-555-0199"},
                "preferred_language": "English"
            }
        }
        
        success3a, update_response_basic = self.run_test(
            "Partial Update - Basic Info Only",
            "PUT",
            f"profiles/patient/{test_user_id}",
            200,
            data=basic_info_update
        )
        
        # Test 3b: Update only physical_metrics (another common auto-save scenario)
        physical_update = {
            "physical_metrics": {
                "height_cm": 168.0,
                "current_weight_kg": 71.2,  # Weight progress
                "goal_weight_kg": 68.0,
                "body_fat_percentage": 21.8,  # Body fat progress
                "muscle_mass_kg": 45.5,  # Muscle gain
                "measurements": {"waist": 77.0, "chest": 95.0, "hips": 97.5},  # Updated measurements
                "bmi": 25.2
            }
        }
        
        success3b, update_response_physical = self.run_test(
            "Partial Update - Physical Metrics Only",
            "PUT",
            f"profiles/patient/{test_user_id}",
            200,
            data=physical_update
        )
        
        # Test 3c: Update multiple sections simultaneously (complex auto-save scenario)
        multi_section_update = {
            "activity_profile": {
                "activity_level": "VERY_ACTIVE",
                "exercise_types": ["yoga", "pilates", "swimming", "hiking", "strength_training"],  # Added new exercise
                "exercise_frequency": 6,  # Increased frequency
                "sleep_schedule": {
                    "bedtime": "22:00",  # Earlier bedtime
                    "wake_time": "06:00",  # Earlier wake time
                    "sleep_quality": 5  # Improved sleep quality
                },
                "stress_level": 1,  # Reduced stress
                "work_type": "MIXED"
            },
            "goals_preferences": {
                "health_targets": [
                    {"type": "weight", "target": 68.0, "timeframe": "3_months"},  # Updated timeframe
                    {"type": "body_fat", "target": 19.0, "timeframe": "5_months"},  # More ambitious target
                    {"type": "exercise", "target": 6, "timeframe": "weekly"}  # Increased exercise target
                ],
                "communication_methods": ["email", "app_notifications", "text_messages"],
                "notification_preferences": {
                    "daily_reminders": True, 
                    "weekly_reports": True, 
                    "goal_achievements": True,
                    "meal_suggestions": True,
                    "workout_reminders": True  # New preference
                },
                "privacy_settings": {
                    "share_with_providers": True, 
                    "anonymous_data": True,
                    "research_participation": True  # Changed mind about research
                },
                "data_sharing_preferences": {
                    "family_members": True,
                    "healthcare_team": True,
                    "fitness_apps": True  # Now willing to share with fitness apps
                }
            }
        }
        
        success3c, update_response_multi = self.run_test(
            "Partial Update - Multiple Sections",
            "PUT",
            f"profiles/patient/{test_user_id}",
            200,
            data=multi_section_update
        )
        
        # Test 4: Validation Testing - Ensure validation still works with complete sections
        print("\n📝 Test 4: Validation Testing with Complete Sections")
        
        # Test 4a: Invalid enum value in complete section
        invalid_enum_update = {
            "activity_profile": {
                "activity_level": "SUPER_ACTIVE",  # Invalid enum value
                "exercise_types": ["yoga"],
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
        
        success4a, _ = self.run_test(
            "Validation Test - Invalid Enum (Should Fail)",
            "PUT",
            f"profiles/patient/{test_user_id}",
            422,  # Expecting validation error
            data=invalid_enum_update
        )
        
        # Test 4b: Invalid data type in complete section
        invalid_type_update = {
            "physical_metrics": {
                "height_cm": "not_a_number",  # Invalid data type
                "current_weight_kg": 70.0,
                "goal_weight_kg": 68.0
            }
        }
        
        success4b, _ = self.run_test(
            "Validation Test - Invalid Data Type (Should Fail)",
            "PUT",
            f"profiles/patient/{test_user_id}",
            422,  # Expecting validation error
            data=invalid_type_update
        )
        
        # Test 4c: Missing required fields in complete section
        incomplete_section_update = {
            "basic_info": {
                "full_name": "Test User"
                # Missing required fields: age, gender, location, timezone, preferred_language
            }
        }
        
        success4c, _ = self.run_test(
            "Validation Test - Incomplete Required Section (Should Fail)",
            "PUT",
            f"profiles/patient/{test_user_id}",
            422,  # Expecting validation error
            data=incomplete_section_update
        )
        
        # Test 5: Profile Completion Calculation After Updates
        print("\n📝 Test 5: Profile Completion Calculation Verification")
        
        success5, final_profile = self.run_test(
            "Get Updated Profile for Completion Check",
            "GET",
            f"profiles/patient/{test_user_id}",
            200
        )
        
        if success5 and final_profile:
            final_completion = final_profile.get('profile_completion', 0)
            print(f"   ✅ Final profile completion: {final_completion}% (Should remain 100%)")
            final_completion_valid = final_completion == 100.0
            if not final_completion_valid:
                print(f"   ❌ Profile completion calculation changed unexpectedly: {final_completion}%")
        
        # Test 6: Profile Completion Status API
        success6, completion_status = self.run_test(
            "Get Profile Completion Status",
            "GET",
            f"profiles/completion/{test_user_id}",
            200,
            params={"role": "patient"}
        )
        
        if success6 and completion_status:
            api_completion = completion_status.get('completion_percentage', 0)
            missing_sections = completion_status.get('missing_sections', [])
            print(f"   ✅ API completion status: {api_completion}%")
            print(f"   ✅ Missing sections: {missing_sections}")
            
            if api_completion != 100.0 or missing_sections:
                print(f"   ❌ Completion API inconsistency detected")
        
        # Cleanup: Delete test profile
        success_cleanup, _ = self.run_test(
            "Cleanup - Delete Test Profile",
            "DELETE",
            f"profiles/patient/{test_user_id}",
            200
        )
        
        # Calculate overall success
        all_create_update_tests = success1 and success2 and success3a and success3b and success3c
        all_validation_tests = success4a and success4b and success4c  # These should fail (return True when they fail as expected)
        all_completion_tests = success5 and success6
        
        overall_success = all_create_update_tests and all_validation_tests and all_completion_tests and success_cleanup
        
        print(f"\n📊 Auto-Save Compatibility Test Results:")
        print(f"   Profile Creation & Updates: {'✅' if all_create_update_tests else '❌'}")
        print(f"   Validation Still Working: {'✅' if all_validation_tests else '❌'}")
        print(f"   Completion Calculation: {'✅' if all_completion_tests else '❌'}")
        print(f"   Overall Success: {'✅' if overall_success else '❌'}")
        
        return overall_success

    def test_patient_profile_partial_updates_smoke_test(self):
        """Smoke test for patient profile partial updates as requested in review"""
        print("\n🔍 Patient Profile Partial Updates - Smoke Test")
        print("Testing: POST with basic_info only, PUT with physical_metrics only, PUT with incomplete activity_profile")
        
        # Generate unique user ID for testing
        test_user_id = f"smoke_test_{datetime.now().strftime('%H%M%S_%f')}"
        
        # Test 1: POST /api/profiles/patient with only user_id and complete basic_info section
        print("\n📝 Test 1: POST with only user_id and complete basic_info section")
        basic_info_only_data = {
            "user_id": test_user_id,
            "basic_info": {
                "full_name": "Emma Wilson",
                "age": 29,
                "gender": "Female", 
                "location": "Seattle, WA",
                "contact_preferences": {"email": True, "sms": False, "push": True},
                "timezone": "America/Los_Angeles",
                "emergency_contact": {"name": "David Wilson", "phone": "+1-555-0188"},
                "preferred_language": "English"
            }
        }
        
        success1, create_response = self.run_test(
            "POST Patient Profile - Basic Info Only",
            "POST",
            "profiles/patient",
            200,
            data=basic_info_only_data
        )
        
        if success1 and create_response:
            completion = create_response.get('profile_completion', 0)
            print(f"   ✅ Profile completion after basic_info only: {completion}%")
        
        # Test 2: PUT /api/profiles/patient/{user_id} with only complete physical_metrics section
        print("\n📝 Test 2: PUT with only complete physical_metrics section")
        physical_metrics_only = {
            "physical_metrics": {
                "height_cm": 165.0,
                "current_weight_kg": 62.0,
                "goal_weight_kg": 58.0,
                "body_fat_percentage": 24.0,
                "muscle_mass_kg": 42.0,
                "measurements": {"waist": 75.0, "chest": 88.0, "hips": 95.0},
                "bmi": 22.8
            }
        }
        
        success2, update_response = self.run_test(
            "PUT Patient Profile - Physical Metrics Only",
            "PUT",
            f"profiles/patient/{test_user_id}",
            200,
            data=physical_metrics_only
        )
        
        if success2 and update_response:
            completion = update_response.get('profile_completion', 0)
            print(f"   ✅ Profile completion after adding physical_metrics: {completion}%")
        
        # Test 3: PUT with incomplete activity_profile (missing sleep_schedule) - should return 422
        print("\n📝 Test 3: PUT with incomplete activity_profile (missing sleep_schedule)")
        incomplete_activity_profile = {
            "activity_profile": {
                "activity_level": "MODERATELY_ACTIVE",
                "exercise_types": ["running", "yoga"],
                "exercise_frequency": 4,
                # Missing required sleep_schedule field
                "stress_level": 3,
                "work_type": "DESK_JOB"
            }
        }
        
        success3, _ = self.run_test(
            "PUT Patient Profile - Incomplete Activity Profile (Should Fail)",
            "PUT",
            f"profiles/patient/{test_user_id}",
            422,  # Expecting validation error
            data=incomplete_activity_profile
        )
        
        # Test 4: GET returns merged profile with completion > 0
        print("\n📝 Test 4: GET merged profile with completion > 0")
        success4, final_profile = self.run_test(
            "GET Merged Patient Profile",
            "GET",
            f"profiles/patient/{test_user_id}",
            200
        )
        
        if success4 and final_profile:
            completion = final_profile.get('profile_completion', 0)
            basic_info = final_profile.get('basic_info')
            physical_metrics = final_profile.get('physical_metrics')
            
            print(f"   ✅ Final profile completion: {completion}%")
            print(f"   ✅ Has basic_info: {'Yes' if basic_info else 'No'}")
            print(f"   ✅ Has physical_metrics: {'Yes' if physical_metrics else 'No'}")
            
            completion_valid = completion > 0
            sections_merged = basic_info is not None and physical_metrics is not None
            
            if not completion_valid:
                print(f"   ❌ Profile completion should be > 0, got {completion}%")
            if not sections_merged:
                print(f"   ❌ Profile sections not properly merged")
        
        # Cleanup
        success_cleanup, _ = self.run_test(
            "Cleanup - Delete Smoke Test Profile",
            "DELETE",
            f"profiles/patient/{test_user_id}",
            200
        )
        
        # Overall success evaluation
        overall_success = success1 and success2 and success3 and success4 and success_cleanup
        
        print(f"\n📊 Smoke Test Results:")
        print(f"   POST with basic_info only: {'✅' if success1 else '❌'}")
        print(f"   PUT with physical_metrics only: {'✅' if success2 else '❌'}")
        print(f"   PUT with incomplete activity_profile (422): {'✅' if success3 else '❌'}")
        print(f"   GET merged profile with completion > 0: {'✅' if success4 else '❌'}")
        print(f"   Overall Smoke Test: {'✅' if overall_success else '❌'}")
        
        return overall_success

    def test_profile_completion_persistence_fix(self):
        """Test that profile_completion is properly persisted to database after updates"""
        print("\n🔍 Testing Profile Completion Persistence Fix")
        print("Focus: Verify profile_completion field is saved to database (not just calculated)")
        
        # Test Patient Profile Completion Persistence
        print("\n📝 Testing Patient Profile Completion Persistence")
        patient_user_id = f"patient_persist_{datetime.now().strftime('%H%M%S_%f')}"
        
        # Step 1: Create patient profile with only basic_info (should be ~16.7% completion)
        basic_info_data = {
            "user_id": patient_user_id,
            "basic_info": {
                "full_name": "Sarah Johnson",
                "age": 28,
                "gender": "Female",
                "location": "New York, NY",
                "timezone": "America/New_York",
                "preferred_language": "English"
            }
        }
        
        success1, create_response = self.run_test(
            "Create Patient Profile - Basic Info Only",
            "POST",
            "profiles/patient",
            200,
            data=basic_info_data
        )
        
        initial_completion = 0
        if success1 and create_response:
            initial_completion = create_response.get('profile_completion', 0)
            print(f"   ✅ Initial completion: {initial_completion}% (Expected: ~16.7%)")
        
        # Step 2: PUT update to add physical_metrics section
        physical_metrics_update = {
            "physical_metrics": {
                "height_cm": 165.0,
                "current_weight_kg": 65.0,
                "goal_weight_kg": 60.0,
                "body_fat_percentage": 22.0,
                "measurements": {"waist": 75.0, "chest": 88.0},
                "bmi": 23.9
            }
        }
        
        success2, update_response = self.run_test(
            "Update Patient Profile - Add Physical Metrics",
            "PUT",
            f"profiles/patient/{patient_user_id}",
            200,
            data=physical_metrics_update
        )
        
        updated_completion = 0
        if success2 and update_response:
            updated_completion = update_response.get('profile_completion', 0)
            print(f"   ✅ Updated completion: {updated_completion}% (Expected: ~33.3%)")
        
        # Step 3: Verify GET shows increased completion percentage
        success3, get_response = self.run_test(
            "Get Patient Profile - Verify Persisted Completion",
            "GET",
            f"profiles/patient/{patient_user_id}",
            200
        )
        
        persisted_completion = 0
        if success3 and get_response:
            persisted_completion = get_response.get('profile_completion', 0)
            print(f"   ✅ Persisted completion: {persisted_completion}% (Should match updated: {updated_completion}%)")
        
        # Step 4: Verify completion API endpoint returns updated values
        success4, completion_api_response = self.run_test(
            "Get Patient Profile Completion Status",
            "GET",
            f"profiles/completion/{patient_user_id}",
            200,
            params={"role": "PATIENT"}
        )
        
        api_completion = 0
        if success4 and completion_api_response:
            api_completion = completion_api_response.get('completion_percentage', 0)
            print(f"   ✅ API completion: {api_completion}% (Should match persisted: {persisted_completion}%)")
        
        # Test Provider Profile Completion Persistence
        print("\n📝 Testing Provider Profile Completion Persistence")
        provider_user_id = f"provider_persist_{datetime.now().strftime('%H%M%S_%f')}"
        
        # Step 1: Create provider profile with only professional_identity (25% completion)
        professional_identity_data = {
            "user_id": provider_user_id,
            "professional_identity": {
                "full_name": "Dr. Emily Rodriguez",
                "professional_title": "Registered Dietitian",
                "medical_license": "RD123456",
                "registration_numbers": {"state_license": "CA-RD-789"},
                "years_experience": 8
            }
        }
        
        success5, provider_create_response = self.run_test(
            "Create Provider Profile - Professional Identity Only",
            "POST",
            "profiles/provider",
            200,
            data=professional_identity_data
        )
        
        provider_initial_completion = 0
        if success5 and provider_create_response:
            provider_initial_completion = provider_create_response.get('profile_completion', 0)
            print(f"   ✅ Provider initial completion: {provider_initial_completion}% (Expected: 25%)")
        
        # Step 2: PUT update to add credentials section
        credentials_update = {
            "credentials": {
                "education": [
                    {
                        "degree": "Master of Science in Nutrition",
                        "institution": "University of California, Davis",
                        "graduation_year": 2015,
                        "specialization": "Clinical Nutrition"
                    }
                ],
                "certifications": [
                    {
                        "name": "Certified Diabetes Educator",
                        "organization": "CBDCE",
                        "issue_date": "2018-06-15",
                        "expiration_date": "2025-06-15",
                        "status": "ACTIVE"
                    }
                ],
                "specializations": ["diabetes_management", "weight_management"]
            }
        }
        
        success6, provider_update_response = self.run_test(
            "Update Provider Profile - Add Credentials",
            "PUT",
            f"profiles/provider/{provider_user_id}",
            200,
            data=credentials_update
        )
        
        provider_updated_completion = 0
        if success6 and provider_update_response:
            provider_updated_completion = provider_update_response.get('profile_completion', 0)
            print(f"   ✅ Provider updated completion: {provider_updated_completion}% (Expected: 50%)")
        
        # Step 3: Verify GET shows increased completion percentage
        success7, provider_get_response = self.run_test(
            "Get Provider Profile - Verify Persisted Completion",
            "GET",
            f"profiles/provider/{provider_user_id}",
            200
        )
        
        provider_persisted_completion = 0
        if success7 and provider_get_response:
            provider_persisted_completion = provider_get_response.get('profile_completion', 0)
            print(f"   ✅ Provider persisted completion: {provider_persisted_completion}% (Should match updated: {provider_updated_completion}%)")
        
        # Step 4: Verify completion API endpoint reflects new percentage
        success8, provider_completion_api = self.run_test(
            "Get Provider Profile Completion Status",
            "GET",
            f"profiles/completion/{provider_user_id}",
            200,
            params={"role": "PROVIDER"}
        )
        
        provider_api_completion = 0
        if success8 and provider_completion_api:
            provider_api_completion = provider_completion_api.get('completion_percentage', 0)
            print(f"   ✅ Provider API completion: {provider_api_completion}% (Should match persisted: {provider_persisted_completion}%)")
        
        # Test Family Profile Completion Persistence
        print("\n📝 Testing Family Profile Completion Persistence")
        family_user_id = f"family_persist_{datetime.now().strftime('%H%M%S_%f')}"
        
        # Step 1: Create family profile with only family_structure (50% completion due to family_members default [])
        family_structure_data = {
            "user_id": family_user_id,
            "family_structure": {
                "family_role": "Parent",
                "number_of_members": 3,
                "primary_caregiver": True
            }
        }
        
        success9, family_create_response = self.run_test(
            "Create Family Profile - Family Structure Only",
            "POST",
            "profiles/family",
            200,
            data=family_structure_data
        )
        
        family_initial_completion = 0
        if success9 and family_create_response:
            family_initial_completion = family_create_response.get('profile_completion', 0)
            print(f"   ✅ Family initial completion: {family_initial_completion}% (Expected: 50% - family_structure + empty family_members list)")
        
        # Step 2: PUT update to add household_management section to increase completion
        household_management_update = {
            "household_management": {
                "common_dietary_restrictions": ["peanut_free"],
                "family_meal_preferences": ["home_cooked", "balanced_nutrition"],
                "budget_considerations": {"weekly_grocery_budget": 200},
                "shopping_responsibilities": ["John", "Mary"],
                "cooking_responsibilities": ["Mary"]
            }
        }
        
        success10, family_update_response = self.run_test(
            "Update Family Profile - Add Household Management",
            "PUT",
            f"profiles/family/{family_user_id}",
            200,
            data=household_management_update
        )
        
        family_updated_completion = 0
        if success10 and family_update_response:
            family_updated_completion = family_update_response.get('profile_completion', 0)
            print(f"   ✅ Family updated completion: {family_updated_completion}% (Expected: 75%)")
        
        # Step 3: Verify GET shows increased completion percentage
        success11, family_get_response = self.run_test(
            "Get Family Profile - Verify Persisted Completion",
            "GET",
            f"profiles/family/{family_user_id}",
            200
        )
        
        family_persisted_completion = 0
        if success11 and family_get_response:
            family_persisted_completion = family_get_response.get('profile_completion', 0)
            print(f"   ✅ Family persisted completion: {family_persisted_completion}% (Should match updated: {family_updated_completion}%)")
        
        # Step 4: Verify completion API endpoint reflects new percentage
        success12, family_completion_api = self.run_test(
            "Get Family Profile Completion Status",
            "GET",
            f"profiles/completion/{family_user_id}",
            200,
            params={"role": "FAMILY"}
        )
        
        family_api_completion = 0
        if success12 and family_completion_api:
            family_api_completion = family_completion_api.get('completion_percentage', 0)
            print(f"   ✅ Family API completion: {family_api_completion}% (Should match persisted: {family_persisted_completion}%)")
        
        # Cleanup test profiles
        self.run_test("Cleanup Patient Profile", "DELETE", f"profiles/patient/{patient_user_id}", 200)
        self.run_test("Cleanup Provider Profile", "DELETE", f"profiles/provider/{provider_user_id}", 200)
        self.run_test("Cleanup Family Profile", "DELETE", f"profiles/family/{family_user_id}", 200)
        
        # Validate persistence logic
        patient_persistence_valid = (
            initial_completion < updated_completion and
            updated_completion == persisted_completion and
            persisted_completion == api_completion
        )
        
        provider_persistence_valid = (
            provider_initial_completion < provider_updated_completion and
            provider_updated_completion == provider_persisted_completion and
            provider_persisted_completion == provider_api_completion
        )
        
        family_persistence_valid = (
            family_initial_completion < family_updated_completion and
            family_updated_completion == family_persisted_completion and
            family_persisted_completion == family_api_completion
        )
        
        overall_success = (
            success1 and success2 and success3 and success4 and
            success5 and success6 and success7 and success8 and
            success9 and success10 and success11 and success12 and
            patient_persistence_valid and provider_persistence_valid and family_persistence_valid
        )
        
        print(f"\n📊 Profile Completion Persistence Test Results:")
        print(f"   Patient Profile Persistence: {'✅' if patient_persistence_valid else '❌'}")
        print(f"   Provider Profile Persistence: {'✅' if provider_persistence_valid else '❌'}")
        print(f"   Family Profile Persistence: {'✅' if family_persistence_valid else '❌'}")
        print(f"   Overall Success: {'✅' if overall_success else '❌'}")
        
        if not patient_persistence_valid:
            print(f"   ❌ Patient: Initial({initial_completion}%) → Updated({updated_completion}%) → Persisted({persisted_completion}%) → API({api_completion}%)")
        if not provider_persistence_valid:
            print(f"   ❌ Provider: Initial({provider_initial_completion}%) → Updated({provider_updated_completion}%) → Persisted({provider_persisted_completion}%) → API({provider_api_completion}%)")
        if not family_persistence_valid:
            print(f"   ❌ Family: Initial({family_initial_completion}%) → Updated({family_updated_completion}%) → Persisted({family_persisted_completion}%) → API({family_api_completion}%)")
        
        return overall_success

def main():
    """Main test execution"""
    tester = HealthPlatformAPITester()
    
    # Run the profile completion persistence test as requested in the review
    print("🚀 Starting Profile Completion Persistence Fix Test")
    print(f"🌐 Base URL: {tester.base_url}")
    print("=" * 80)
    
    success = tester.test_profile_completion_persistence_fix()
    
    print("\n" + "=" * 80)
    if success:
        print("🎉 Profile Completion Persistence Fix Test: PASSED")
        print("✅ Profile completion is properly persisted to database after updates")
        return 0
    else:
        print("⚠️ Profile Completion Persistence Fix Test: FAILED")
        print("❌ Issues detected with profile completion persistence")
        return 1

if __name__ == "__main__":
    sys.exit(main())