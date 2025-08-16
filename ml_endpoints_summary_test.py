#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def test_ml_endpoints_summary():
    """Test the 5 ML-powered predictive analytics endpoints with realistic data"""
    base_url = "http://localhost:8001/api"
    results = {}
    
    print("🧪 TESTING ML PREDICTIVE ANALYTICS ENDPOINTS")
    print("=" * 60)
    
    # Test 1: Energy Prediction
    print("\n🔋 Testing Energy Prediction...")
    energy_data = {
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
    
    try:
        response = requests.post(f"{base_url}/ai/energy-prediction", json=energy_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            predicted_energy = data.get('predicted_energy', 0)
            confidence = data.get('confidence', 0)
            model_accuracy = data.get('model_accuracy', 0)
            print(f"   ✅ SUCCESS - Energy: {predicted_energy}/10, Confidence: {confidence:.2f}, Accuracy: {model_accuracy:.1f}%")
            results['energy_prediction'] = True
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
            results['energy_prediction'] = False
    except Exception as e:
        print(f"   ❌ ERROR - {str(e)}")
        results['energy_prediction'] = False
    
    # Test 2: Mood-Food Correlation
    print("\n😊 Testing Mood-Food Correlation...")
    mood_data = {
        "user_id": "demo-patient-123",
        "timeframe_days": 30
    }
    
    try:
        response = requests.post(f"{base_url}/ai/mood-food-correlation", json=mood_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            correlations = data.get('correlations', {})
            trigger_foods = data.get('trigger_foods', {})
            mood_predictors = data.get('mood_predictors', {})
            print(f"   ✅ SUCCESS - Correlations: {len(correlations)}, Triggers: {len(trigger_foods)}, Predictors: {len(mood_predictors)}")
            results['mood_correlation'] = True
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
            results['mood_correlation'] = False
    except Exception as e:
        print(f"   ❌ ERROR - {str(e)}")
        results['mood_correlation'] = False
    
    # Test 3: Sleep Impact Analysis
    print("\n😴 Testing Sleep Impact Analysis...")
    sleep_data = {
        "user_id": "demo-patient-123",
        "daily_choices": {
            "caffeine_timing": "morning",
            "caffeine_amount": 100,
            "last_meal_time": "18:00",
            "exercise_timing": "afternoon",
            "exercise_intensity": "moderate",
            "screen_time_before_bed": 30,
            "alcohol_consumption": 0,
            "stress_level": 3,
            "bedroom_temperature": 20,
            "sleep_environment_score": 8
        }
    }
    
    try:
        response = requests.post(f"{base_url}/ai/sleep-impact-analysis", json=sleep_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            sleep_quality = data.get('predicted_sleep_quality', 0)
            improvement_potential = data.get('improvement_potential', 0)
            factor_analysis = data.get('factor_analysis', {})
            print(f"   ✅ SUCCESS - Sleep Quality: {sleep_quality}/10, Improvement: {improvement_potential:.1f}%, Factors: {len(factor_analysis)}")
            results['sleep_analysis'] = True
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
            results['sleep_analysis'] = False
    except Exception as e:
        print(f"   ❌ ERROR - {str(e)}")
        results['sleep_analysis'] = False
    
    # Test 4: What-If Scenarios
    print("\n🤔 Testing What-If Scenarios...")
    whatif_data = {
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
            "protein_increase": 40,
            "change_description": "Increase daily protein intake"
        }
    }
    
    try:
        response = requests.post(f"{base_url}/ai/what-if-scenarios", json=whatif_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            scenario_id = data.get('scenario_id', '')
            impact_analysis = data.get('impact_analysis', {})
            recommendations = data.get('recommendations', [])
            print(f"   ✅ SUCCESS - Scenario ID: {scenario_id}, Impacts: {len(impact_analysis)}, Recommendations: {len(recommendations)}")
            results['what_if_scenarios'] = True
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
            results['what_if_scenarios'] = False
    except Exception as e:
        print(f"   ❌ ERROR - {str(e)}")
        results['what_if_scenarios'] = False
    
    # Test 5: Weekly Health Patterns
    print("\n📅 Testing Weekly Health Patterns...")
    try:
        response = requests.get(f"{base_url}/ai/weekly-health-patterns/demo-patient-123", 
                              params={"weeks_back": 4}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            patterns = data.get('patterns', {})
            insights = data.get('insights', [])
            anomalies = data.get('anomalies', [])
            print(f"   ✅ SUCCESS - Patterns: {len(patterns)}, Insights: {len(insights)}, Anomalies: {len(anomalies)}")
            results['weekly_patterns'] = True
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
            results['weekly_patterns'] = False
    except Exception as e:
        print(f"   ❌ ERROR - {str(e)}")
        results['weekly_patterns'] = False
    
    # Test 6: Health Insights (for PersonalInsights component)
    print("\n🧠 Testing Health Insights...")
    insights_data = {
        "user_id": "demo-patient-123",
        "healthData": {
            "demographics": {
                "age": 35,
                "gender": "male",
                "activity_level": "moderately_active"
            },
            "nutrition_data": {
                "daily_calories": 2000,
                "protein_intake": 100,
                "carb_intake": 250,
                "fat_intake": 70
            },
            "health_metrics": {
                "weight": 75,
                "height": 175,
                "bmi": 24.5
            },
            "goals": ["weight_loss", "muscle_gain"],
            "daily_logs": [
                {
                    "date": "2025-08-15",
                    "calories": 1950,
                    "exercise_minutes": 45,
                    "sleep_hours": 7.5,
                    "stress_level": 3
                }
            ]
        },
        "analysis_type": "comprehensive"
    }
    
    try:
        response = requests.post(f"{base_url}/ai/health-insights", json=insights_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            insights = data.get('insights', [])
            recommendations = data.get('recommendations', [])
            confidence = data.get('confidence', 0)
            print(f"   ✅ SUCCESS - Insights: {len(insights)}, Recommendations: {len(recommendations)}, Confidence: {confidence:.2f}")
            results['health_insights'] = True
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
            results['health_insights'] = False
    except Exception as e:
        print(f"   ❌ ERROR - {str(e)}")
        results['health_insights'] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY RESULTS")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    success_rate = (passed_tests / total_tests) * 100
    
    for endpoint, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {endpoint.replace('_', ' ').title()}: {'PASS' if status else 'FAIL'}")
    
    print(f"\n📈 Overall Success Rate: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL ML PREDICTIVE ANALYTICS ENDPOINTS ARE WORKING CORRECTLY!")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} ENDPOINT(S) HAVE ISSUES")
        return False

if __name__ == "__main__":
    success = test_ml_endpoints_summary()
    exit(0 if success else 1)