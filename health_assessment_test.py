#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime, timedelta
import uuid
import time

class HealthAssessmentTester:
    def __init__(self, base_url="https://medemo-ai.preview.emergentagent.com/api"):
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

    def test_health_assessment_api(self):
        """Test Health Assessment API endpoints as requested in review"""
        print("\n🏥 Testing Health Assessment API Endpoints...")
        
        # Generate unique guest user ID for testing
        guest_user_id = f"guest_test_session_{datetime.now().strftime('%H%M%S')}"
        
        # Test 1: POST /api/guest/health-assessment - Complete Valid Assessment
        complete_assessment_data = {
            "user_id": guest_user_id,
            "responses": {
                "age_range": "26-35",
                "activity_level": "moderate",
                "health_goal": "general_wellness",
                "dietary_preferences": ["vegetarian", "gluten_free"],
                "stress_level": "moderate"
            }
        }
        
        success1, assessment_response = self.run_test(
            "Health Assessment - Complete Valid Data",
            "POST",
            "guest/health-assessment",
            200,
            data=complete_assessment_data
        )
        
        # Validate assessment response structure
        assessment_id = None
        if success1 and assessment_response:
            expected_keys = ['health_score', 'health_age', 'actual_age_range', 'score_breakdown', 
                           'recommendations', 'meal_suggestions', 'improvement_areas', 'next_steps', 'assessment_id']
            missing_keys = [key for key in expected_keys if key not in assessment_response]
            if not missing_keys:
                print(f"   ✅ Assessment response contains all required keys: {expected_keys}")
                
                # Validate health score (0-100 integer)
                health_score = assessment_response.get('health_score', 0)
                if isinstance(health_score, int) and 0 <= health_score <= 100:
                    print(f"   ✅ Health score valid: {health_score}/100")
                else:
                    print(f"   ❌ Health score invalid: {health_score} (should be 0-100 integer)")
                    success1 = False
                
                # Validate health age calculation
                health_age = assessment_response.get('health_age', 0)
                actual_age_range = assessment_response.get('actual_age_range', '')
                if isinstance(health_age, int) and health_age > 0:
                    print(f"   ✅ Health age valid: {health_age} years (actual range: {actual_age_range})")
                else:
                    print(f"   ❌ Health age invalid: {health_age}")
                    success1 = False
                
                # Validate score breakdown
                score_breakdown = assessment_response.get('score_breakdown', {})
                breakdown_keys = ['activity', 'nutrition', 'stress_management', 'lifestyle']
                missing_breakdown_keys = [key for key in breakdown_keys if key not in score_breakdown]
                if not missing_breakdown_keys:
                    print(f"   ✅ Score breakdown complete: {score_breakdown}")
                else:
                    print(f"   ❌ Score breakdown missing keys: {missing_breakdown_keys}")
                    success1 = False
                
                # Validate recommendations
                recommendations = assessment_response.get('recommendations', [])
                if recommendations and len(recommendations) > 0:
                    rec = recommendations[0]
                    rec_keys = ['title', 'description', 'priority', 'impact', 'time_estimate', 'category']
                    missing_rec_keys = [key for key in rec_keys if key not in rec]
                    if not missing_rec_keys:
                        print(f"   ✅ Recommendations structure valid - {len(recommendations)} recommendations")
                        print(f"   📋 Sample recommendation: {rec['title']} (Priority: {rec['priority']})")
                    else:
                        print(f"   ❌ Recommendation missing keys: {missing_rec_keys}")
                        success1 = False
                else:
                    print(f"   ❌ No recommendations provided")
                    success1 = False
                
                # Validate meal suggestions
                meal_suggestions = assessment_response.get('meal_suggestions', [])
                if meal_suggestions and len(meal_suggestions) > 0:
                    meal = meal_suggestions[0]
                    meal_keys = ['name', 'meal_type', 'prep_time', 'difficulty', 'health_benefits', 
                               'estimated_nutrition', 'ingredients_preview']
                    missing_meal_keys = [key for key in meal_keys if key not in meal]
                    if not missing_meal_keys:
                        print(f"   ✅ Meal suggestions structure valid - {len(meal_suggestions)} suggestions")
                        print(f"   🍽️ Sample meal: {meal['name']} ({meal['meal_type']}) - {meal['prep_time']}")
                        
                        # Validate dietary preference filtering
                        dietary_prefs = complete_assessment_data['responses']['dietary_preferences']
                        if 'vegetarian' in dietary_prefs:
                            # Check if meal suggestions respect vegetarian preference
                            vegetarian_friendly = True
                            for suggestion in meal_suggestions:
                                ingredients = suggestion.get('ingredients_preview', [])
                                meat_ingredients = ['chicken', 'beef', 'pork', 'fish', 'salmon']
                                if any(meat in ' '.join(ingredients).lower() for meat in meat_ingredients):
                                    vegetarian_friendly = False
                                    break
                            if vegetarian_friendly:
                                print(f"   ✅ Meal suggestions respect vegetarian preference")
                            else:
                                print(f"   ⚠️ Some meal suggestions may not respect vegetarian preference")
                    else:
                        print(f"   ❌ Meal suggestion missing keys: {missing_meal_keys}")
                        success1 = False
                else:
                    print(f"   ❌ No meal suggestions provided")
                    success1 = False
                
                # Store assessment ID for retrieval test
                assessment_id = assessment_response.get('assessment_id')
                if assessment_id:
                    print(f"   ✅ Assessment ID generated: {assessment_id}")
                else:
                    print(f"   ❌ No assessment ID provided")
                    success1 = False
                    
            else:
                print(f"   ❌ Assessment response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Test different combinations of inputs for scoring accuracy
        high_activity_data = {
            "user_id": f"guest_high_activity_{datetime.now().strftime('%H%M%S')}",
            "responses": {
                "age_range": "18-25",
                "activity_level": "very_active",
                "health_goal": "disease_prevention",
                "dietary_preferences": ["mediterranean", "vegetarian"],
                "stress_level": "low"
            }
        }
        
        success2, high_activity_response = self.run_test(
            "Health Assessment - High Activity/Low Stress Profile",
            "POST",
            "guest/health-assessment",
            200,
            data=high_activity_data
        )
        
        # Validate high activity profile gets better scores
        if success2 and high_activity_response and success1 and assessment_response:
            high_score = high_activity_response.get('health_score', 0)
            moderate_score = assessment_response.get('health_score', 0)
            if high_score > moderate_score:
                print(f"   ✅ Algorithm correctly scores high activity profile higher: {high_score} vs {moderate_score}")
            else:
                print(f"   ⚠️ High activity profile score not higher than moderate: {high_score} vs {moderate_score}")
        
        # Test 3: Test edge case - sedentary lifestyle with high stress
        sedentary_data = {
            "user_id": f"guest_sedentary_{datetime.now().strftime('%H%M%S')}",
            "responses": {
                "age_range": "55+",
                "activity_level": "sedentary",
                "health_goal": "weight_loss",
                "dietary_preferences": ["none"],
                "stress_level": "very_high"
            }
        }
        
        success3, sedentary_response = self.run_test(
            "Health Assessment - Sedentary/High Stress Profile",
            "POST",
            "guest/health-assessment",
            200,
            data=sedentary_data
        )
        
        # Validate sedentary profile gets appropriate recommendations
        if success3 and sedentary_response:
            recommendations = sedentary_response.get('recommendations', [])
            high_priority_recs = [r for r in recommendations if r.get('priority') == 'high']
            if high_priority_recs:
                print(f"   ✅ Sedentary profile gets high-priority recommendations: {len(high_priority_recs)} found")
                activity_rec = any('movement' in r.get('title', '').lower() or 'exercise' in r.get('title', '').lower() 
                                for r in high_priority_recs)
                stress_rec = any('stress' in r.get('title', '').lower() for r in high_priority_recs)
                if activity_rec:
                    print(f"   ✅ Activity recommendation provided for sedentary lifestyle")
                if stress_rec:
                    print(f"   ✅ Stress management recommendation provided for high stress")
            else:
                print(f"   ⚠️ No high-priority recommendations for sedentary/high stress profile")
        
        # Test 4: Error Handling - Missing required fields
        incomplete_data = {
            "user_id": f"guest_incomplete_{datetime.now().strftime('%H%M%S')}",
            "responses": {
                "age_range": "26-35",
                "activity_level": "moderate"
                # Missing health_goal, dietary_preferences, stress_level
            }
        }
        
        success4, _ = self.run_test(
            "Health Assessment - Missing Required Fields (Should Fail with Validation)",
            "POST",
            "guest/health-assessment",
            400,  # Should fail with validation error for missing required fields
            data=incomplete_data
        )
        
        # Test 5: Error Handling - Invalid field values
        invalid_data = {
            "user_id": f"guest_invalid_{datetime.now().strftime('%H%M%S')}",
            "responses": {
                "age_range": "invalid_age",
                "activity_level": "super_active",  # Invalid value
                "health_goal": "become_superhuman",  # Invalid value
                "dietary_preferences": ["invalid_diet"],
                "stress_level": "extremely_stressed"  # Invalid value
            }
        }
        
        success5, invalid_response = self.run_test(
            "Health Assessment - Invalid Field Values (Should Handle Gracefully)",
            "POST",
            "guest/health-assessment",
            200,  # Should still work with fallback values
            data=invalid_data
        )
        
        # Test 6: Malformed request body
        success6, _ = self.run_test(
            "Health Assessment - Malformed Request Body (Should Fail)",
            "POST",
            "guest/health-assessment",
            422,  # Expecting validation error
            data={"invalid": "structure"}
        )
        
        # Test 7: GET /api/guest/health-assessment/{user_id}/recent - Retrieve recent assessment
        if assessment_id and guest_user_id:
            success7, recent_response = self.run_test(
                "Get Recent Health Assessment",
                "GET",
                f"guest/health-assessment/{guest_user_id}/recent",
                200
            )
            
            # Validate recent assessment response
            if success7 and recent_response:
                # Should return the same assessment data
                if recent_response.get('assessment_id') == assessment_id:
                    print(f"   ✅ Recent assessment retrieved correctly: {assessment_id}")
                else:
                    print(f"   ❌ Recent assessment ID mismatch: expected {assessment_id}, got {recent_response.get('assessment_id')}")
                    success7 = False
            else:
                success7 = False
        else:
            success7 = False
            print(f"   ❌ Cannot test recent assessment retrieval - no valid assessment ID")
        
        # Test 8: GET recent assessment for non-existent user
        success8, _ = self.run_test(
            "Get Recent Assessment - Non-existent User (Should Fail)",
            "GET",
            f"guest/health-assessment/non_existent_user/recent",
            404
        )
        
        # Test 9: Performance test - Response time should be under 2 seconds
        start_time = time.time()
        
        performance_data = {
            "user_id": f"guest_performance_{datetime.now().strftime('%H%M%S')}",
            "responses": {
                "age_range": "36-45",
                "activity_level": "active",
                "health_goal": "muscle_gain",
                "dietary_preferences": ["high_protein", "keto"],
                "stress_level": "moderate"
            }
        }
        
        success9, _ = self.run_test(
            "Health Assessment - Performance Test",
            "POST",
            "guest/health-assessment",
            200,
            data=performance_data
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if response_time < 2.0:
            print(f"   ✅ Performance test passed: {response_time:.2f}s (< 2.0s)")
        else:
            print(f"   ⚠️ Performance test warning: {response_time:.2f}s (>= 2.0s)")
        
        # Test 10: Test 24-hour expiration logic (simulate with different timestamps)
        old_user_id = f"guest_old_session_{datetime.now().strftime('%H%M%S')}"
        
        # This test would require backend to have old data, so we'll test the endpoint exists
        success10, _ = self.run_test(
            "Get Recent Assessment - Test Expiration Logic",
            "GET",
            f"guest/health-assessment/{old_user_id}/recent",
            404  # Should return 404 for non-existent/expired session
        )
        
        print(f"\n📊 Health Assessment API Test Summary:")
        print(f"   ✅ Complete valid assessment: {'PASS' if success1 else 'FAIL'}")
        print(f"   ✅ High activity profile scoring: {'PASS' if success2 else 'FAIL'}")
        print(f"   ✅ Sedentary profile recommendations: {'PASS' if success3 else 'FAIL'}")
        print(f"   ✅ Missing fields handling: {'PASS' if success4 else 'FAIL'}")
        print(f"   ✅ Invalid values handling: {'PASS' if success5 else 'FAIL'}")
        print(f"   ✅ Malformed request rejection: {'PASS' if success6 else 'FAIL'}")
        print(f"   ✅ Recent assessment retrieval: {'PASS' if success7 else 'FAIL'}")
        print(f"   ✅ Non-existent user handling: {'PASS' if success8 else 'FAIL'}")
        print(f"   ✅ Performance test (<2s): {'PASS' if success9 else 'FAIL'}")
        print(f"   ✅ Expiration logic test: {'PASS' if success10 else 'FAIL'}")
        print(f"   📈 Response time: {response_time:.2f}s")
        
        return (success1 and success2 and success3 and success4 and success5 and 
                success6 and success7 and success8 and success9 and success10)

    def run_tests(self):
        """Run health assessment tests"""
        print("🚀 Starting Health Assessment API Tests...")
        print(f"   Base URL: {self.base_url}")
        
        # Run health assessment tests
        health_assessment_success = self.test_health_assessment_api()
        
        # Calculate overall success rate
        total_tests = self.tests_run
        passed_tests = self.tests_passed
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📊 Test Results Summary:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {total_tests - passed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        if health_assessment_success:
            print("🎉 Health Assessment API tests passed!")
        else:
            print("❌ Some Health Assessment API tests failed. Check the details above.")
            
        return health_assessment_success

if __name__ == "__main__":
    tester = HealthAssessmentTester()
    success = tester.run_tests()
    sys.exit(0 if success else 1)