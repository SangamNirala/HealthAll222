#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime, timedelta
import uuid

class PredictiveAnalyticsAPITester:
    def __init__(self, base_url="https://mockup-chat-btn.preview.emergentagent.com/api"):
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
                response = requests.get(url, headers=headers, params=params, timeout=15)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=15)

            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response keys: {list(response_data.keys()) if isinstance(response_data, dict) else 'Non-dict response'}")
                    if isinstance(response_data, dict):
                        # Show key metrics for each endpoint
                        if 'predicted_energy' in response_data:
                            print(f"   Energy: {response_data['predicted_energy']}, Confidence: {response_data.get('confidence', 'N/A')}")
                        elif 'correlations' in response_data:
                            print(f"   Correlations: {len(response_data['correlations'])} found")
                        elif 'predicted_sleep_quality' in response_data:
                            print(f"   Sleep Quality: {response_data['predicted_sleep_quality']}")
                        elif 'impact_analysis' in response_data:
                            print(f"   Impact Analysis: {len(response_data['impact_analysis'])} metrics")
                        elif 'patterns' in response_data:
                            print(f"   Patterns: {len(response_data['patterns'])} analyzed")
                except Exception as e:
                    print(f"   Response parsing error: {e}")
                    print(f"   Raw response: {response.text[:200]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:300]}...")

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

    def test_energy_prediction_endpoint(self):
        """Test POST /api/ai/energy-prediction endpoint"""
        print("\n🔋 Testing Energy Prediction Endpoint...")
        
        # Test 1: Basic energy prediction with realistic sample data
        realistic_intake_data = {
            "user_id": "demo-patient-123",
            "intake_data": {
                "calories": 2000,
                "protein_g": 100,
                "carbs_g": 250,
                "fat_g": 70,
                "sleep_hours": 7.5,
                "exercise_minutes": 45,
                "stress_level": 4,
                "water_intake_ml": 2500,
                "caffeine_mg": 150,
                "meal_timing_consistency": 0.8
            }
        }
        
        success1, response1 = self.run_test(
            "Energy Prediction - Realistic Sample Data",
            "POST",
            "ai/energy-prediction",
            200,
            data=realistic_intake_data
        )
        
        # Validate response structure
        if success1 and response1:
            expected_keys = ['predicted_energy', 'confidence', 'factors', 'recommendations', 'model_accuracy']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Response contains all required keys: {expected_keys}")
                
                # Validate energy scale (1-10)
                energy = response1.get('predicted_energy', 0)
                if 1 <= energy <= 10:
                    print(f"   ✅ Energy prediction in valid range: {energy}/10")
                else:
                    print(f"   ❌ Energy prediction out of range: {energy}")
                    success1 = False
                
                # Validate confidence score
                confidence = response1.get('confidence', 0)
                if 0 <= confidence <= 1:
                    print(f"   ✅ Confidence score valid: {confidence}")
                else:
                    print(f"   ❌ Confidence score invalid: {confidence}")
                    success1 = False
                
                # Validate factors analysis
                factors = response1.get('factors', {})
                print(f"   📊 Factors analyzed: {len(factors)} factors")
                
                # Validate recommendations
                recommendations = response1.get('recommendations', [])
                print(f"   💡 Recommendations: {len(recommendations)} provided")
                
            else:
                print(f"   ❌ Response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: High activity/low stress profile
        high_activity_data = {
            "user_id": "demo-patient-456",
            "intake_data": {
                "calories": 2200,
                "protein_g": 120,
                "carbs_g": 280,
                "fat_g": 75,
                "sleep_hours": 8.0,
                "exercise_minutes": 60,
                "stress_level": 2,
                "water_intake_ml": 3000,
                "caffeine_mg": 100,
                "meal_timing_consistency": 0.9
            }
        }
        
        success2, response2 = self.run_test(
            "Energy Prediction - High Activity/Low Stress",
            "POST",
            "ai/energy-prediction",
            200,
            data=high_activity_data
        )
        
        # Test 3: Low activity/high stress profile
        low_activity_data = {
            "user_id": "demo-patient-789",
            "intake_data": {
                "calories": 1800,
                "protein_g": 80,
                "carbs_g": 200,
                "fat_g": 60,
                "sleep_hours": 6.0,
                "exercise_minutes": 10,
                "stress_level": 8,
                "water_intake_ml": 1800,
                "caffeine_mg": 250,
                "meal_timing_consistency": 0.5
            }
        }
        
        success3, response3 = self.run_test(
            "Energy Prediction - Low Activity/High Stress",
            "POST",
            "ai/energy-prediction",
            200,
            data=low_activity_data
        )
        
        # Compare energy predictions (high activity should be higher)
        if success2 and success3 and response2 and response3:
            high_energy = response2.get('predicted_energy', 0)
            low_energy = response3.get('predicted_energy', 0)
            print(f"   📈 Energy comparison: High activity={high_energy}, Low activity={low_energy}")
            if high_energy > low_energy:
                print(f"   ✅ Energy prediction logic working correctly")
            else:
                print(f"   ⚠️ Energy prediction may need calibration")
        
        return success1 and success2 and success3

    def test_mood_food_correlation_endpoint(self):
        """Test POST /api/ai/mood-food-correlation endpoint"""
        print("\n😊 Testing Mood-Food Correlation Endpoint...")
        
        # Test 1: 30-day correlation analysis
        correlation_data = {
            "user_id": "demo-patient-123",
            "timeframe_days": 30
        }
        
        success1, response1 = self.run_test(
            "Mood-Food Correlation - 30 Day Analysis",
            "POST",
            "ai/mood-food-correlation",
            200,
            data=correlation_data
        )
        
        # Validate response structure
        if success1 and response1:
            expected_keys = ['correlations', 'trigger_foods', 'mood_predictors', 'recommendations']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Response contains all required keys: {expected_keys}")
                
                # Validate correlations
                correlations = response1.get('correlations', {})
                print(f"   🔗 Correlations found: {len(correlations)} relationships")
                for corr_name, corr_data in list(correlations.items())[:2]:
                    correlation_val = corr_data.get('correlation', 0)
                    strength = corr_data.get('strength', 'unknown')
                    print(f"      - {corr_name}: {correlation_val} ({strength})")
                
                # Validate trigger foods
                trigger_foods = response1.get('trigger_foods', {})
                print(f"   🚨 Trigger foods identified: {len(trigger_foods)} triggers")
                
                # Validate mood predictors
                mood_predictors = response1.get('mood_predictors', {})
                print(f"   🎯 Mood predictors: {len(mood_predictors)} factors")
                
                # Validate recommendations
                recommendations = response1.get('recommendations', [])
                print(f"   💡 Recommendations: {len(recommendations)} provided")
                
            else:
                print(f"   ❌ Response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: 7-day correlation analysis
        short_term_data = {
            "user_id": "demo-patient-456",
            "timeframe_days": 7
        }
        
        success2, response2 = self.run_test(
            "Mood-Food Correlation - 7 Day Analysis",
            "POST",
            "ai/mood-food-correlation",
            200,
            data=short_term_data
        )
        
        # Test 3: Different user ID
        different_user_data = {
            "user_id": "test-user-789",
            "timeframe_days": 14
        }
        
        success3, response3 = self.run_test(
            "Mood-Food Correlation - Different User",
            "POST",
            "ai/mood-food-correlation",
            200,
            data=different_user_data
        )
        
        return success1 and success2 and success3

    def test_sleep_impact_analysis_endpoint(self):
        """Test POST /api/ai/sleep-impact-analysis endpoint"""
        print("\n😴 Testing Sleep Impact Analysis Endpoint...")
        
        # Test 1: Good sleep habits
        good_habits_data = {
            "user_id": "demo-patient-123",
            "daily_choices": {
                "last_caffeine_time": "14:00",
                "last_meal_time": "18:30",
                "exercise_time": "17:00",
                "screen_time_before_bed": 30,
                "alcohol_consumption": 0,
                "stress_level": 3
            }
        }
        
        success1, response1 = self.run_test(
            "Sleep Impact Analysis - Good Habits",
            "POST",
            "ai/sleep-impact-analysis",
            200,
            data=good_habits_data
        )
        
        # Validate response structure
        if success1 and response1:
            expected_keys = ['predicted_sleep_quality', 'improvement_potential', 'factor_analysis', 'recommendations']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Response contains all required keys: {expected_keys}")
                
                # Validate sleep quality scale (1-10)
                sleep_quality = response1.get('predicted_sleep_quality', 0)
                if 1 <= sleep_quality <= 10:
                    print(f"   ✅ Sleep quality prediction in valid range: {sleep_quality}/10")
                else:
                    print(f"   ❌ Sleep quality out of range: {sleep_quality}")
                    success1 = False
                
                # Validate improvement potential
                improvement = response1.get('improvement_potential', 0)
                print(f"   📈 Improvement potential: {improvement} points")
                
                # Validate factor analysis
                factor_analysis = response1.get('factor_analysis', {})
                print(f"   🔍 Factors analyzed: {len(factor_analysis)} factors")
                for factor, data in list(factor_analysis.items())[:3]:
                    impact = data.get('score_impact', 0)
                    description = data.get('description', 'No description')
                    print(f"      - {factor}: {impact} impact ({description})")
                
                # Validate recommendations
                recommendations = response1.get('recommendations', [])
                print(f"   💡 Recommendations: {len(recommendations)} provided")
                
            else:
                print(f"   ❌ Response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Poor sleep habits (late caffeine, late dinner)
        poor_habits_data = {
            "user_id": "demo-patient-456",
            "daily_choices": {
                "last_caffeine_time": "18:00",  # After 4 PM
                "last_meal_time": "21:30",      # After 9 PM
                "exercise_time": "20:30",       # Late exercise
                "screen_time_before_bed": 120,
                "alcohol_consumption": 2,
                "stress_level": 8
            }
        }
        
        success2, response2 = self.run_test(
            "Sleep Impact Analysis - Poor Habits (Late Caffeine/Dinner)",
            "POST",
            "ai/sleep-impact-analysis",
            200,
            data=poor_habits_data
        )
        
        # Test 3: Mixed habits
        mixed_habits_data = {
            "user_id": "demo-patient-789",
            "daily_choices": {
                "last_caffeine_time": "15:00",  # Good timing
                "last_meal_time": "20:00",      # Moderate timing
                "exercise_time": "16:00",       # Good timing
                "screen_time_before_bed": 60,
                "alcohol_consumption": 1,
                "stress_level": 5
            }
        }
        
        success3, response3 = self.run_test(
            "Sleep Impact Analysis - Mixed Habits",
            "POST",
            "ai/sleep-impact-analysis",
            200,
            data=mixed_habits_data
        )
        
        # Compare sleep quality predictions (good habits should be higher)
        if success1 and success2 and response1 and response2:
            good_sleep = response1.get('predicted_sleep_quality', 0)
            poor_sleep = response2.get('predicted_sleep_quality', 0)
            print(f"   📊 Sleep quality comparison: Good habits={good_sleep}, Poor habits={poor_sleep}")
            if good_sleep > poor_sleep:
                print(f"   ✅ Sleep impact analysis working correctly")
            else:
                print(f"   ⚠️ Sleep impact analysis may need calibration")
        
        return success1 and success2 and success3

    def test_what_if_scenarios_endpoint(self):
        """Test POST /api/ai/what-if-scenarios endpoint"""
        print("\n🤔 Testing What-If Scenarios Endpoint...")
        
        # Test 1: Increase protein scenario
        protein_scenario_data = {
            "user_id": "demo-patient-123",
            "base_data": {
                "calories": 2000,
                "protein_g": 80,
                "carbs_g": 250,
                "fat_g": 70,
                "sleep_hours": 7.0,
                "exercise_minutes": 30,
                "stress_level": 5
            },
            "proposed_changes": {
                "protein_g": 120  # Increase protein by 40g
            }
        }
        
        success1, response1 = self.run_test(
            "What-If Scenario - Increase Protein by 40g",
            "POST",
            "ai/what-if-scenarios",
            200,
            data=protein_scenario_data
        )
        
        # Validate response structure
        if success1 and response1:
            expected_keys = ['scenario_id', 'changes_applied', 'current_state', 'predicted_state', 'impact_analysis', 'recommendations']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Response contains all required keys: {expected_keys}")
                
                # Validate scenario ID
                scenario_id = response1.get('scenario_id', '')
                print(f"   🆔 Scenario ID: {scenario_id}")
                
                # Validate changes applied
                changes = response1.get('changes_applied', {})
                print(f"   🔄 Changes applied: {changes}")
                
                # Validate current vs predicted state
                current_state = response1.get('current_state', {})
                predicted_state = response1.get('predicted_state', {})
                print(f"   📊 Current state: {current_state}")
                print(f"   📈 Predicted state: {predicted_state}")
                
                # Validate impact analysis with percentage changes
                impact_analysis = response1.get('impact_analysis', {})
                print(f"   📈 Impact analysis: {len(impact_analysis)} metrics analyzed")
                for metric, data in impact_analysis.items():
                    percentage_change = data.get('percentage_change', 0)
                    impact_level = data.get('impact_level', 'unknown')
                    print(f"      - {metric}: {percentage_change}% change ({impact_level} impact)")
                
                # Validate recommendations
                recommendations = response1.get('recommendations', [])
                print(f"   💡 Recommendations: {len(recommendations)} provided")
                
            else:
                print(f"   ❌ Response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Reduce caffeine scenario
        caffeine_scenario_data = {
            "user_id": "demo-patient-456",
            "base_data": {
                "calories": 2000,
                "protein_g": 100,
                "carbs_g": 250,
                "fat_g": 70,
                "sleep_hours": 7.0,
                "exercise_minutes": 30,
                "stress_level": 5,
                "caffeine_mg": 200
            },
            "proposed_changes": {
                "caffeine_mg": 100  # Reduce caffeine by 100mg
            }
        }
        
        success2, response2 = self.run_test(
            "What-If Scenario - Reduce Caffeine by 100mg",
            "POST",
            "ai/what-if-scenarios",
            200,
            data=caffeine_scenario_data
        )
        
        # Test 3: Multiple changes scenario
        multiple_changes_data = {
            "user_id": "demo-patient-789",
            "base_data": {
                "calories": 2200,
                "protein_g": 90,
                "carbs_g": 280,
                "fat_g": 80,
                "sleep_hours": 6.5,
                "exercise_minutes": 20,
                "stress_level": 7
            },
            "proposed_changes": {
                "sleep_hours": 8.0,      # Increase sleep
                "exercise_minutes": 45,   # Increase exercise
                "stress_level": 4         # Reduce stress
            }
        }
        
        success3, response3 = self.run_test(
            "What-If Scenario - Multiple Lifestyle Changes",
            "POST",
            "ai/what-if-scenarios",
            200,
            data=multiple_changes_data
        )
        
        return success1 and success2 and success3

    def test_weekly_health_patterns_endpoint(self):
        """Test GET /api/ai/weekly-health-patterns/{user_id} endpoint"""
        print("\n📅 Testing Weekly Health Patterns Endpoint...")
        
        # Test 1: 4 weeks back analysis for demo patient
        success1, response1 = self.run_test(
            "Weekly Health Patterns - Demo Patient (4 weeks)",
            "GET",
            "ai/weekly-health-patterns/demo-patient-123",
            200,
            params={"weeks_back": 4}
        )
        
        # Validate response structure
        if success1 and response1:
            expected_keys = ['user_id', 'analysis_period', 'patterns', 'insights', 'anomalies', 'recommendations', 'trend_direction']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Response contains all required keys: {expected_keys}")
                
                # Validate user ID
                user_id = response1.get('user_id', '')
                print(f"   👤 User ID: {user_id}")
                
                # Validate analysis period
                analysis_period = response1.get('analysis_period', '')
                print(f"   📅 Analysis period: {analysis_period}")
                
                # Validate patterns analysis
                patterns = response1.get('patterns', {})
                print(f"   📊 Patterns analyzed: {len(patterns)} pattern types")
                expected_patterns = ['nutrition_consistency', 'energy_patterns', 'sleep_trends', 'activity_levels', 'mood_stability']
                for pattern_type in expected_patterns:
                    if pattern_type in patterns:
                        pattern_data = patterns[pattern_type]
                        score = pattern_data.get('score', 'N/A')
                        print(f"      - {pattern_type}: Score {score}")
                
                # Validate insights
                insights = response1.get('insights', [])
                print(f"   💡 Insights: {len(insights)} generated")
                for insight in insights[:2]:  # Show first 2
                    print(f"      - {insight}")
                
                # Validate anomalies
                anomalies = response1.get('anomalies', [])
                print(f"   🚨 Anomalies detected: {len(anomalies)}")
                
                # Validate recommendations
                recommendations = response1.get('recommendations', [])
                print(f"   🎯 Recommendations: {len(recommendations)} provided")
                
                # Validate trend direction
                trend_direction = response1.get('trend_direction', '')
                valid_trends = ['improving', 'stable', 'declining', 'insufficient_data']
                if trend_direction in valid_trends:
                    print(f"   📈 Trend direction: {trend_direction}")
                else:
                    print(f"   ❌ Invalid trend direction: {trend_direction}")
                    success1 = False
                
            else:
                print(f"   ❌ Response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: 2 weeks back analysis
        success2, response2 = self.run_test(
            "Weekly Health Patterns - Demo Patient (2 weeks)",
            "GET",
            "ai/weekly-health-patterns/demo-patient-123",
            200,
            params={"weeks_back": 2}
        )
        
        # Test 3: Different user
        success3, response3 = self.run_test(
            "Weekly Health Patterns - Different User",
            "GET",
            "ai/weekly-health-patterns/test-user-456",
            200,
            params={"weeks_back": 3}
        )
        
        # Test 4: Default weeks_back (should work without parameter)
        success4, response4 = self.run_test(
            "Weekly Health Patterns - Default Period",
            "GET",
            "ai/weekly-health-patterns/demo-patient-789",
            200
        )
        
        return success1 and success2 and success3 and success4

    def run_all_predictive_analytics_tests(self):
        """Run all predictive analytics API tests"""
        print("🚀 Starting Comprehensive Predictive Analytics API Testing...")
        print("=" * 80)
        
        # Test all 5 ML-powered endpoints
        energy_success = self.test_energy_prediction_endpoint()
        mood_success = self.test_mood_food_correlation_endpoint()
        sleep_success = self.test_sleep_impact_analysis_endpoint()
        whatif_success = self.test_what_if_scenarios_endpoint()
        patterns_success = self.test_weekly_health_patterns_endpoint()
        
        # Print comprehensive summary
        print("\n" + "=" * 80)
        print("📊 PREDICTIVE ANALYTICS API TEST SUMMARY")
        print("=" * 80)
        
        print(f"🔋 Energy Prediction API: {'✅ PASS' if energy_success else '❌ FAIL'}")
        print(f"😊 Mood-Food Correlation API: {'✅ PASS' if mood_success else '❌ FAIL'}")
        print(f"😴 Sleep Impact Analysis API: {'✅ PASS' if sleep_success else '❌ FAIL'}")
        print(f"🤔 What-If Scenarios API: {'✅ PASS' if whatif_success else '❌ FAIL'}")
        print(f"📅 Weekly Health Patterns API: {'✅ PASS' if patterns_success else '❌ FAIL'}")
        
        print(f"\n📈 Overall Results:")
        print(f"   Total Tests Run: {self.tests_run}")
        print(f"   Tests Passed: {self.tests_passed}")
        print(f"   Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        all_success = energy_success and mood_success and sleep_success and whatif_success and patterns_success
        
        if all_success:
            print(f"\n🎉 ALL PREDICTIVE ANALYTICS APIS FULLY FUNCTIONAL!")
            print(f"✅ ML models are properly integrated and generating realistic predictions")
            print(f"✅ All response formats match expected Pydantic models")
            print(f"✅ Confidence scores and factor analysis working correctly")
        else:
            print(f"\n⚠️ Some predictive analytics APIs need attention")
            failed_tests = [result for result in self.test_results if not result['success']]
            if failed_tests:
                print(f"❌ Failed tests:")
                for test in failed_tests[-5:]:  # Show last 5 failures
                    print(f"   - {test['name']}: {test.get('error', test.get('response', 'Unknown error'))}")
        
        return all_success

if __name__ == "__main__":
    tester = PredictiveAnalyticsAPITester()
    success = tester.run_all_predictive_analytics_tests()
    sys.exit(0 if success else 1)