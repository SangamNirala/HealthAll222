#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime, timedelta
import uuid

class MLPredictiveAnalyticsAPITester:
    def __init__(self, base_url="http://localhost:8001/api"):
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
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=15)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=15)

            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:300]}...")
                except:
                    print(f"   Response: {response.text[:300]}...")
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

    def test_energy_prediction_endpoint(self):
        """Test POST /api/ai/energy-prediction - Daily Energy Level Predictor with ML model"""
        print("\n🔋 Testing Energy Prediction Endpoint...")
        
        # Test 1: Realistic high-energy scenario
        high_energy_data = {
            "user_id": "demo-patient-123",
            "intake_data": {
                "calories": 2200,
                "protein_g": 120,
                "carbs_g": 275,
                "fat_g": 75,
                "sleep_hours": 8.0,
                "exercise_minutes": 45,
                "stress_level": 2,
                "water_intake_ml": 2500,
                "caffeine_mg": 100,
                "meal_timing_consistency": 0.9
            }
        }
        
        success1, response1 = self.run_test(
            "Energy Prediction - High Energy Scenario",
            "POST",
            "ai/energy-prediction",
            200,
            data=high_energy_data
        )
        
        # Validate response structure
        if success1 and response1:
            expected_keys = ['predicted_energy', 'confidence', 'factors', 'recommendations', 'model_accuracy']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Response contains all required keys: {expected_keys}")
                
                predicted_energy = response1.get('predicted_energy', 0)
                confidence = response1.get('confidence', 0)
                factors = response1.get('factors', [])
                recommendations = response1.get('recommendations', [])
                model_accuracy = response1.get('model_accuracy', 0)
                
                print(f"   🔋 Predicted energy: {predicted_energy}/10")
                print(f"   📊 Confidence: {confidence:.2f}")
                print(f"   📈 Model accuracy: {model_accuracy:.1f}%")
                print(f"   🎯 Top factors: {[f.get('factor', '') for f in factors[:3]]}")
                print(f"   💡 Recommendations: {len(recommendations)}")
                
                # Validate energy is in expected range (1-10)
                energy_valid = 1 <= predicted_energy <= 10
                print(f"   ✅ Energy range validation: {'PASS' if energy_valid else 'FAIL'}")
                
                # High energy scenario should predict higher energy (>6)
                high_energy_valid = predicted_energy > 6
                print(f"   ✅ High energy scenario validation: {'PASS' if high_energy_valid else 'FAIL'}")
                
            else:
                print(f"   ❌ Response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Low energy scenario
        low_energy_data = {
            "user_id": "demo-patient-123",
            "intake_data": {
                "calories": 1200,
                "protein_g": 40,
                "carbs_g": 150,
                "fat_g": 35,
                "sleep_hours": 5.0,
                "exercise_minutes": 0,
                "stress_level": 8,
                "water_intake_ml": 1000,
                "caffeine_mg": 300,
                "meal_timing_consistency": 0.3
            }
        }
        
        success2, response2 = self.run_test(
            "Energy Prediction - Low Energy Scenario",
            "POST",
            "ai/energy-prediction",
            200,
            data=low_energy_data
        )
        
        if success2 and response2:
            predicted_energy_low = response2.get('predicted_energy', 0)
            print(f"   🔋 Low energy prediction: {predicted_energy_low}/10")
            
            # Low energy scenario should predict lower energy (<5)
            low_energy_valid = predicted_energy_low < 5
            print(f"   ✅ Low energy scenario validation: {'PASS' if low_energy_valid else 'FAIL'}")
        
        # Test 3: Invalid data (missing required fields)
        invalid_data = {
            "user_id": "demo-patient-123",
            "intake_data": {
                "calories": 2000
                # Missing other required fields
            }
        }
        
        success3, _ = self.run_test(
            "Energy Prediction - Invalid Data (Should Fail)",
            "POST",
            "ai/energy-prediction",
            422,
            data=invalid_data
        )
        
        return success1 and success2 and success3

    def test_mood_food_correlation_endpoint(self):
        """Test POST /api/ai/mood-food-correlation - Advanced Mood-Food Correlation Engine"""
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
                
                correlations = response1.get('correlations', {})
                trigger_foods = response1.get('trigger_foods', [])
                mood_predictors = response1.get('mood_predictors', [])
                recommendations = response1.get('recommendations', [])
                
                print(f"   📊 Correlations found: {len(correlations)}")
                print(f"   🚨 Trigger foods: {trigger_foods}")
                print(f"   🎯 Mood predictors: {mood_predictors}")
                print(f"   💡 Recommendations: {len(recommendations)}")
                
                # Display correlation strengths
                for correlation_type, value in correlations.items():
                    if isinstance(value, (int, float)):
                        strength = "strong" if abs(value) > 0.7 else "moderate" if abs(value) > 0.4 else "weak"
                        print(f"   📈 {correlation_type}: {value:.2f} ({strength})")
                
            else:
                print(f"   ❌ Response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: 7-day correlation analysis
        short_correlation_data = {
            "user_id": "demo-patient-123",
            "timeframe_days": 7
        }
        
        success2, response2 = self.run_test(
            "Mood-Food Correlation - 7 Day Analysis",
            "POST",
            "ai/mood-food-correlation",
            200,
            data=short_correlation_data
        )
        
        # Test 3: Invalid timeframe
        invalid_timeframe_data = {
            "user_id": "demo-patient-123",
            "timeframe_days": 0  # Invalid timeframe
        }
        
        success3, _ = self.run_test(
            "Mood-Food Correlation - Invalid Timeframe (Should Fail)",
            "POST",
            "ai/mood-food-correlation",
            422,
            data=invalid_timeframe_data
        )
        
        return success1 and success2 and success3

    def test_sleep_impact_analysis_endpoint(self):
        """Test POST /api/ai/sleep-impact-analysis - Sleep Quality Impact Calculator"""
        print("\n😴 Testing Sleep Impact Analysis Endpoint...")
        
        # Test 1: Good sleep habits scenario
        good_sleep_data = {
            "user_id": "demo-patient-123",
            "daily_choices": {
                "caffeine_timing": "morning",  # Good - early caffeine
                "caffeine_amount": 100,
                "last_meal_time": "18:00",  # Good - early dinner
                "exercise_timing": "afternoon",
                "exercise_intensity": "moderate",
                "screen_time_before_bed": 30,  # Good - minimal screen time
                "alcohol_consumption": 0,
                "stress_level": 3,
                "bedroom_temperature": 20,
                "sleep_environment_score": 8
            }
        }
        
        success1, response1 = self.run_test(
            "Sleep Impact Analysis - Good Sleep Habits",
            "POST",
            "ai/sleep-impact-analysis",
            200,
            data=good_sleep_data
        )
        
        # Validate response structure
        if success1 and response1:
            expected_keys = ['predicted_sleep_quality', 'improvement_potential', 'factor_analysis', 'recommendations']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Response contains all required keys: {expected_keys}")
                
                predicted_sleep_quality = response1.get('predicted_sleep_quality', 0)
                improvement_potential = response1.get('improvement_potential', 0)
                factor_analysis = response1.get('factor_analysis', [])
                recommendations = response1.get('recommendations', [])
                
                print(f"   😴 Predicted sleep quality: {predicted_sleep_quality}/10")
                print(f"   📈 Improvement potential: {improvement_potential:.1f}%")
                print(f"   🔍 Factors analyzed: {len(factor_analysis)}")
                print(f"   💡 Recommendations: {len(recommendations)}")
                
                # Good habits should predict good sleep (>6)
                good_sleep_valid = predicted_sleep_quality > 6
                print(f"   ✅ Good sleep habits validation: {'PASS' if good_sleep_valid else 'FAIL'}")
                
                # Display top factors
                for factor in factor_analysis[:3]:
                    factor_name = factor.get('factor', '')
                    impact = factor.get('impact', 0)
                    print(f"   📊 {factor_name}: {impact:.2f} impact")
                
            else:
                print(f"   ❌ Response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Poor sleep habits scenario
        poor_sleep_data = {
            "user_id": "demo-patient-123",
            "daily_choices": {
                "caffeine_timing": "evening",  # Bad - late caffeine
                "caffeine_amount": 300,
                "last_meal_time": "22:00",  # Bad - late dinner
                "exercise_timing": "evening",  # Bad - late exercise
                "exercise_intensity": "high",
                "screen_time_before_bed": 120,  # Bad - lots of screen time
                "alcohol_consumption": 3,
                "stress_level": 8,
                "bedroom_temperature": 26,  # Too warm
                "sleep_environment_score": 3
            }
        }
        
        success2, response2 = self.run_test(
            "Sleep Impact Analysis - Poor Sleep Habits",
            "POST",
            "ai/sleep-impact-analysis",
            200,
            data=poor_sleep_data
        )
        
        if success2 and response2:
            predicted_sleep_quality_poor = response2.get('predicted_sleep_quality', 0)
            print(f"   😴 Poor habits sleep prediction: {predicted_sleep_quality_poor}/10")
            
            # Poor habits should predict worse sleep (<6)
            poor_sleep_valid = predicted_sleep_quality_poor < 6
            print(f"   ✅ Poor sleep habits validation: {'PASS' if poor_sleep_valid else 'FAIL'}")
        
        # Test 3: Missing required fields
        invalid_data = {
            "user_id": "demo-patient-123",
            "daily_choices": {
                "caffeine_timing": "morning"
                # Missing other required fields
            }
        }
        
        success3, _ = self.run_test(
            "Sleep Impact Analysis - Invalid Data (Should Fail)",
            "POST",
            "ai/sleep-impact-analysis",
            422,
            data=invalid_data
        )
        
        return success1 and success2 and success3

    def test_what_if_scenarios_endpoint(self):
        """Test POST /api/ai/what-if-scenarios - Interactive 'What-If' Scenario Engine"""
        print("\n🤔 Testing What-If Scenarios Endpoint...")
        
        # Test 1: Protein increase scenario
        protein_scenario_data = {
            "user_id": "demo-patient-123",
            "base_data": {
                "current_calories": 2000,
                "current_protein": 80,
                "current_carbs": 250,
                "current_fat": 70,
                "current_exercise": 30,
                "current_sleep": 7.0,
                "current_stress": 5
            },
            "proposed_changes": {
                "protein_increase": 40,  # Increase protein by 40g
                "change_description": "Increase daily protein intake"
            }
        }
        
        success1, response1 = self.run_test(
            "What-If Scenarios - Protein Increase",
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
                
                scenario_id = response1.get('scenario_id', '')
                changes_applied = response1.get('changes_applied', {})
                current_state = response1.get('current_state', {})
                predicted_state = response1.get('predicted_state', {})
                impact_analysis = response1.get('impact_analysis', {})
                recommendations = response1.get('recommendations', [])
                
                print(f"   🆔 Scenario ID: {scenario_id}")
                print(f"   🔄 Changes applied: {len(changes_applied)}")
                print(f"   📊 Current energy: {current_state.get('energy_level', 0)}")
                print(f"   📈 Predicted energy: {predicted_state.get('energy_level', 0)}")
                
                # Display impact analysis
                for metric, impact in impact_analysis.items():
                    if isinstance(impact, dict) and 'percentage_change' in impact:
                        percentage = impact.get('percentage_change', 0)
                        print(f"   📊 {metric}: {percentage:+.1f}% change")
                
                print(f"   💡 Recommendations: {len(recommendations)}")
                
            else:
                print(f"   ❌ Response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Exercise increase scenario
        exercise_scenario_data = {
            "user_id": "demo-patient-123",
            "base_data": {
                "current_calories": 1800,
                "current_protein": 90,
                "current_carbs": 200,
                "current_fat": 60,
                "current_exercise": 15,
                "current_sleep": 6.5,
                "current_stress": 6
            },
            "proposed_changes": {
                "exercise_increase": 30,  # Increase exercise by 30 minutes
                "sleep_increase": 1.0,    # Increase sleep by 1 hour
                "change_description": "Increase exercise and sleep"
            }
        }
        
        success2, response2 = self.run_test(
            "What-If Scenarios - Exercise & Sleep Increase",
            "POST",
            "ai/what-if-scenarios",
            200,
            data=exercise_scenario_data
        )
        
        if success2 and response2:
            impact_analysis = response2.get('impact_analysis', {})
            print(f"   📊 Multiple changes impact analysis: {len(impact_analysis)} metrics")
        
        # Test 3: Invalid scenario data
        invalid_scenario_data = {
            "user_id": "demo-patient-123",
            "base_data": {
                "current_calories": 2000
                # Missing other required base data
            },
            "proposed_changes": {}  # Empty changes
        }
        
        success3, _ = self.run_test(
            "What-If Scenarios - Invalid Data (Should Fail)",
            "POST",
            "ai/what-if-scenarios",
            422,
            data=invalid_scenario_data
        )
        
        return success1 and success2 and success3

    def test_weekly_health_patterns_endpoint(self):
        """Test GET /api/ai/weekly-health-patterns/{user_id} - Weekly Health Pattern Analysis Dashboard"""
        print("\n📅 Testing Weekly Health Patterns Endpoint...")
        
        # Test 1: 4-week pattern analysis
        success1, response1 = self.run_test(
            "Weekly Health Patterns - 4 Week Analysis",
            "GET",
            "ai/weekly-health-patterns/demo-patient-123",
            200,
            params={"weeks_back": 4}
        )
        
        # Validate response structure
        if success1 and response1:
            expected_keys = ['user_id', 'analysis_period', 'patterns', 'insights', 'anomalies', 'trend_direction']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Response contains all required keys: {expected_keys}")
                
                user_id = response1.get('user_id', '')
                analysis_period = response1.get('analysis_period', {})
                patterns = response1.get('patterns', {})
                insights = response1.get('insights', [])
                anomalies = response1.get('anomalies', [])
                trend_direction = response1.get('trend_direction', '')
                
                print(f"   👤 User ID: {user_id}")
                print(f"   📅 Analysis period: {analysis_period.get('weeks_analyzed', 0)} weeks")
                print(f"   📊 Pattern types: {len(patterns)}")
                print(f"   💡 Insights: {len(insights)}")
                print(f"   🚨 Anomalies: {len(anomalies)}")
                print(f"   📈 Trend direction: {trend_direction}")
                
                # Display pattern analysis
                for pattern_type, pattern_data in patterns.items():
                    if isinstance(pattern_data, dict) and 'score' in pattern_data:
                        score = pattern_data.get('score', 0)
                        print(f"   📊 {pattern_type}: {score}/10")
                
                # Display insights
                for i, insight in enumerate(insights[:3]):
                    print(f"   💡 Insight {i+1}: {insight[:60]}...")
                
            else:
                print(f"   ❌ Response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: 2-week pattern analysis
        success2, response2 = self.run_test(
            "Weekly Health Patterns - 2 Week Analysis",
            "GET",
            "ai/weekly-health-patterns/demo-patient-123",
            200,
            params={"weeks_back": 2}
        )
        
        if success2 and response2:
            weeks_analyzed = response2.get('analysis_period', {}).get('weeks_analyzed', 0)
            print(f"   📅 Short analysis period: {weeks_analyzed} weeks")
        
        # Test 3: Non-existent user
        success3, _ = self.run_test(
            "Weekly Health Patterns - Non-existent User (Should Fail)",
            "GET",
            "ai/weekly-health-patterns/non-existent-user",
            404
        )
        
        # Test 4: Invalid weeks_back parameter
        success4, _ = self.run_test(
            "Weekly Health Patterns - Invalid Weeks Parameter (Should Fail)",
            "GET",
            "ai/weekly-health-patterns/demo-patient-123",
            422,
            params={"weeks_back": 0}
        )
        
        return success1 and success2 and success3 and success4

    def test_health_insights_endpoint(self):
        """Test GET /api/ai/health-insights - Personal AI Insights component support"""
        print("\n🧠 Testing Health Insights Endpoint...")
        
        # Test 1: Health insights for demo patient
        health_insights_data = {
            "user_id": "demo-patient-123",
            "analysis_type": "comprehensive",
            "timeframe": "30_days"
        }
        
        success1, response1 = self.run_test(
            "Health Insights - Comprehensive Analysis",
            "POST",
            "ai/health-insights",
            200,
            data=health_insights_data
        )
        
        # Validate response structure
        if success1 and response1:
            expected_keys = ['insights', 'recommendations', 'patterns', 'confidence']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Response contains all required keys: {expected_keys}")
                
                insights = response1.get('insights', [])
                recommendations = response1.get('recommendations', [])
                patterns = response1.get('patterns', {})
                confidence = response1.get('confidence', 0)
                
                print(f"   🧠 Insights generated: {len(insights)}")
                print(f"   💡 Recommendations: {len(recommendations)}")
                print(f"   📊 Patterns identified: {len(patterns)}")
                print(f"   📈 Confidence score: {confidence:.2f}")
                
                # Display sample insights
                for i, insight in enumerate(insights[:2]):
                    print(f"   💡 Insight {i+1}: {insight[:80]}...")
                
            else:
                print(f"   ❌ Response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Weekly analysis
        weekly_insights_data = {
            "user_id": "demo-patient-123",
            "analysis_type": "weekly_summary",
            "timeframe": "7_days"
        }
        
        success2, response2 = self.run_test(
            "Health Insights - Weekly Summary",
            "POST",
            "ai/health-insights",
            200,
            data=weekly_insights_data
        )
        
        return success1 and success2

    def run_all_tests(self):
        """Run all ML Predictive Analytics API tests"""
        print("🚀 Starting ML Predictive Analytics API Testing...")
        print(f"📍 Base URL: {self.base_url}")
        print("=" * 80)
        
        # Test all 5 ML-powered predictive analytics endpoints
        energy_success = self.test_energy_prediction_endpoint()
        mood_success = self.test_mood_food_correlation_endpoint()
        sleep_success = self.test_sleep_impact_analysis_endpoint()
        whatif_success = self.test_what_if_scenarios_endpoint()
        patterns_success = self.test_weekly_health_patterns_endpoint()
        
        # Test health insights endpoint
        insights_success = self.test_health_insights_endpoint()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 ML PREDICTIVE ANALYTICS API TEST SUMMARY")
        print("=" * 80)
        print(f"🔋 Energy Prediction: {'✅ PASS' if energy_success else '❌ FAIL'}")
        print(f"😊 Mood-Food Correlation: {'✅ PASS' if mood_success else '❌ FAIL'}")
        print(f"😴 Sleep Impact Analysis: {'✅ PASS' if sleep_success else '❌ FAIL'}")
        print(f"🤔 What-If Scenarios: {'✅ PASS' if whatif_success else '❌ FAIL'}")
        print(f"📅 Weekly Health Patterns: {'✅ PASS' if patterns_success else '❌ FAIL'}")
        print(f"🧠 Health Insights: {'✅ PASS' if insights_success else '❌ FAIL'}")
        print("-" * 80)
        print(f"📈 Overall Success Rate: {self.tests_passed}/{self.tests_run} ({(self.tests_passed/self.tests_run)*100:.1f}%)")
        
        # Check for 422 errors specifically
        error_422_tests = [result for result in self.test_results if result.get('status_code') == 422]
        if error_422_tests:
            print(f"\n🚨 422 UNPROCESSABLE ENTITY ERRORS DETECTED:")
            for test in error_422_tests:
                print(f"   ❌ {test['name']}: {test.get('response', '')[:100]}...")
        
        overall_success = (energy_success and mood_success and sleep_success and 
                          whatif_success and patterns_success and insights_success)
        
        if overall_success:
            print("\n🎉 ALL ML PREDICTIVE ANALYTICS ENDPOINTS ARE WORKING CORRECTLY!")
        else:
            print("\n⚠️  SOME ML PREDICTIVE ANALYTICS ENDPOINTS HAVE ISSUES")
        
        return overall_success

if __name__ == "__main__":
    tester = MLPredictiveAnalyticsAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)