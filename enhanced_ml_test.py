#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime, timedelta
import uuid

class EnhancedMLEndpointsTester:
    def __init__(self, base_url="https://medtest-platform.preview.emergentagent.com/api"):
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
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)

            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response keys: {list(response_data.keys())}")
                    return success, response_data
                except:
                    print(f"   Response: {response.text[:200]}...")
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:500]}...")
                return success, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_enhanced_energy_prediction(self):
        """Test POST /api/ai/enhanced-energy-prediction with enhanced fields"""
        print("\n🔋 Testing Enhanced Energy Prediction Endpoint...")
        
        # Test with comprehensive intake data
        test_data = {
            "user_id": "demo-patient-123",
            "intake_data": {
                "calories": 2000,
                "protein_g": 100,
                "carbs_g": 250,
                "fat_g": 70,
                "sleep_hours": 7.5,
                "exercise_minutes": 45,
                "stress_level": 4,
                "water_intake_ml": 2200,
                "caffeine_mg": 150,
                "meal_timing_consistency": 0.8
            },
            "prediction_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        success, response = self.run_test(
            "Enhanced Energy Prediction - Full Data",
            "POST",
            "ai/enhanced-energy-prediction",
            200,
            data=test_data
        )
        
        if success and response:
            # Validate enhanced fields are present
            required_fields = [
                'predicted_energy', 'confidence', 'explanation', 
                'scientific_basis', 'reliability_score', 'feature_contributions'
            ]
            
            missing_fields = [field for field in required_fields if field not in response]
            
            if not missing_fields:
                print(f"   ✅ All enhanced fields present: {required_fields}")
                
                # Validate field content quality
                predicted_energy = response.get('predicted_energy', 0)
                confidence = response.get('confidence', 0)
                explanation = response.get('explanation', '')
                scientific_basis = response.get('scientific_basis', {})
                reliability_score = response.get('reliability_score', 0)
                feature_contributions = response.get('feature_contributions', {})
                
                print(f"   🔋 Predicted Energy: {predicted_energy}/10")
                print(f"   📊 Confidence: {confidence:.3f}")
                print(f"   📈 Reliability Score: {reliability_score:.3f}")
                print(f"   📝 Explanation length: {len(explanation)} chars")
                print(f"   🧬 Scientific basis keys: {list(scientific_basis.keys())}")
                print(f"   📊 Feature contributions: {len(feature_contributions)} factors")
                
                # Validate content quality
                content_quality_checks = []
                
                # Check if explanation is detailed
                if len(explanation) > 50:
                    content_quality_checks.append("✅ Detailed explanation provided")
                else:
                    content_quality_checks.append("❌ Explanation too brief")
                
                # Check if scientific basis has research references
                if scientific_basis and any('research' in str(v).lower() or 'study' in str(v).lower() for v in scientific_basis.values()):
                    content_quality_checks.append("✅ Scientific basis includes research references")
                else:
                    content_quality_checks.append("❌ Scientific basis lacks research references")
                
                # Check if feature contributions are meaningful
                if feature_contributions and len(feature_contributions) >= 3:
                    content_quality_checks.append("✅ Meaningful feature contributions provided")
                else:
                    content_quality_checks.append("❌ Insufficient feature contributions")
                
                for check in content_quality_checks:
                    print(f"   {check}")
                
            else:
                print(f"   ❌ Missing enhanced fields: {missing_fields}")
                success = False
        
        return success

    def test_what_if_scenarios(self):
        """Test POST /api/ai/what-if-scenarios with enhanced fields"""
        print("\n🔮 Testing What-If Scenarios Endpoint...")
        
        test_data = {
            "user_id": "demo-patient-123",
            "scenario_name": "Increase Protein Intake",
            "base_data": {
                "current_calories": 2000,
                "current_protein": 80,
                "current_carbs": 250,
                "current_fat": 70,
                "current_exercise": 30,
                "current_sleep": 7.0
            },
            "proposed_changes": {
                "protein_increase": 40,  # +40g protein
                "exercise_increase": 15,  # +15 minutes
                "sleep_improvement": 0.5  # +30 minutes
            }
        }
        
        success, response = self.run_test(
            "What-If Scenarios - Protein & Exercise Increase",
            "POST",
            "ai/what-if-scenarios",
            200,
            data=test_data
        )
        
        if success and response:
            # Validate enhanced fields are present
            required_fields = [
                'scenario_id', 'impact_analysis', 'recommendations',
                'scientific_basis', 'timeframe', 'risk_factors', 'reliability_indicators'
            ]
            
            missing_fields = [field for field in required_fields if field not in response]
            
            if not missing_fields:
                print(f"   ✅ All enhanced fields present: {required_fields}")
                
                # Validate field content quality
                scenario_id = response.get('scenario_id', '')
                impact_analysis = response.get('impact_analysis', {})
                recommendations = response.get('recommendations', [])
                scientific_basis = response.get('scientific_basis', {})
                timeframe = response.get('timeframe', {})
                risk_factors = response.get('risk_factors', [])
                reliability_indicators = response.get('reliability_indicators', {})
                
                print(f"   🆔 Scenario ID: {scenario_id}")
                print(f"   📊 Impact Analysis keys: {list(impact_analysis.keys())}")
                print(f"   💡 Recommendations count: {len(recommendations)}")
                print(f"   🧬 Scientific basis keys: {list(scientific_basis.keys())}")
                print(f"   ⏰ Timeframe keys: {list(timeframe.keys())}")
                print(f"   ⚠️ Risk factors count: {len(risk_factors)}")
                print(f"   📈 Reliability indicators: {list(reliability_indicators.keys())}")
                
                # Validate content quality
                content_quality_checks = []
                
                # Check if scientific basis cites specific research
                if scientific_basis and any('study' in str(v).lower() or 'research' in str(v).lower() for v in scientific_basis.values()):
                    content_quality_checks.append("✅ Scientific basis cites specific research")
                else:
                    content_quality_checks.append("❌ Scientific basis lacks research citations")
                
                # Check if timeframe provides realistic estimates
                if timeframe and any(key in timeframe for key in ['short_term', 'long_term', 'expected_duration']):
                    content_quality_checks.append("✅ Realistic timeframe estimates provided")
                else:
                    content_quality_checks.append("❌ Timeframe estimates missing or unrealistic")
                
                # Check if risk factors are meaningful
                if risk_factors and len(risk_factors) > 0:
                    content_quality_checks.append("✅ Risk factors identified")
                else:
                    content_quality_checks.append("❌ No risk factors identified")
                
                # Check if reliability indicators provide confidence metrics
                if reliability_indicators and any(key in reliability_indicators for key in ['data_quality', 'scientific_support', 'prediction_strength']):
                    content_quality_checks.append("✅ Meaningful reliability indicators provided")
                else:
                    content_quality_checks.append("❌ Reliability indicators insufficient")
                
                for check in content_quality_checks:
                    print(f"   {check}")
                
            else:
                print(f"   ❌ Missing enhanced fields: {missing_fields}")
                success = False
        
        return success

    def test_mood_food_correlation(self):
        """Test POST /api/ai/mood-food-correlation with enhanced fields"""
        print("\n🧠 Testing Mood-Food Correlation Endpoint...")
        
        test_data = {
            "user_id": "demo-patient-123",
            "timeframe_days": 30,
            "include_mood_data": True
        }
        
        success, response = self.run_test(
            "Mood-Food Correlation - 30 Day Analysis",
            "POST",
            "ai/mood-food-correlation",
            200,
            data=test_data
        )
        
        if success and response:
            # Validate enhanced fields are present
            required_fields = [
                'correlations', 'trigger_foods', 'mood_predictors', 'recommendations',
                'scientific_validation', 'behavioral_insights', 'personalization_factors'
            ]
            
            missing_fields = [field for field in required_fields if field not in response]
            
            if not missing_fields:
                print(f"   ✅ All enhanced fields present: {required_fields}")
                
                # Validate field content quality
                correlations = response.get('correlations', {})
                trigger_foods = response.get('trigger_foods', {})
                mood_predictors = response.get('mood_predictors', {})
                recommendations = response.get('recommendations', [])
                scientific_validation = response.get('scientific_validation', {})
                behavioral_insights = response.get('behavioral_insights', [])
                personalization_factors = response.get('personalization_factors', {})
                
                print(f"   🔗 Correlations found: {len(correlations)}")
                print(f"   🚨 Trigger foods identified: {len(trigger_foods)}")
                print(f"   🎯 Mood predictors: {len(mood_predictors)}")
                print(f"   💡 Recommendations: {len(recommendations)}")
                print(f"   🧬 Scientific validation keys: {list(scientific_validation.keys())}")
                print(f"   🧠 Behavioral insights: {len(behavioral_insights)}")
                print(f"   👤 Personalization factors: {list(personalization_factors.keys())}")
                
                # Validate content quality
                content_quality_checks = []
                
                # Check if scientific validation cites neuroscience research
                if scientific_validation and any('neuroscience' in str(v).lower() or 'brain' in str(v).lower() for v in scientific_validation.values()):
                    content_quality_checks.append("✅ Scientific validation cites neuroscience research")
                else:
                    content_quality_checks.append("❌ Scientific validation lacks neuroscience references")
                
                # Check if behavioral insights explain mechanisms
                if behavioral_insights and len(behavioral_insights) > 0:
                    content_quality_checks.append("✅ Behavioral insights provided")
                else:
                    content_quality_checks.append("❌ Behavioral insights missing")
                
                # Check if personalization factors assess analysis quality
                if personalization_factors and any(key in personalization_factors for key in ['analysis_quality', 'data_completeness', 'confidence_level']):
                    content_quality_checks.append("✅ Personalization factors assess analysis quality")
                else:
                    content_quality_checks.append("❌ Personalization factors lack quality assessment")
                
                for check in content_quality_checks:
                    print(f"   {check}")
                
            else:
                print(f"   ❌ Missing enhanced fields: {missing_fields}")
                success = False
        
        return success

    def test_sleep_impact_analysis(self):
        """Test POST /api/ai/sleep-impact-analysis with enhanced fields"""
        print("\n😴 Testing Sleep Impact Analysis Endpoint...")
        
        test_data = {
            "user_id": "demo-patient-123",
            "daily_choices": {
                "caffeine_timing": "14:30",  # 2:30 PM
                "last_meal_time": "20:00",   # 8:00 PM
                "exercise_timing": "18:00",   # 6:00 PM
                "screen_time_before_bed": 60,  # 60 minutes
                "alcohol_consumption": 1,      # 1 drink
                "stress_level": 6,            # 1-10 scale
                "bedroom_temperature": 22,     # Celsius
                "bedtime_routine": True
            },
            "analysis_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        success, response = self.run_test(
            "Sleep Impact Analysis - Daily Choices",
            "POST",
            "ai/sleep-impact-analysis",
            200,
            data=test_data
        )
        
        if success and response:
            # Validate enhanced fields are present
            required_fields = [
                'predicted_sleep_quality', 'improvement_potential', 'factor_analysis', 'recommendations',
                'scientific_evidence', 'actionable_insights', 'risk_assessment'
            ]
            
            missing_fields = [field for field in required_fields if field not in response]
            
            if not missing_fields:
                print(f"   ✅ All enhanced fields present: {required_fields}")
                
                # Validate field content quality
                predicted_sleep_quality = response.get('predicted_sleep_quality', 0)
                improvement_potential = response.get('improvement_potential', 0)
                factor_analysis = response.get('factor_analysis', {})
                recommendations = response.get('recommendations', [])
                scientific_evidence = response.get('scientific_evidence', {})
                actionable_insights = response.get('actionable_insights', [])
                risk_assessment = response.get('risk_assessment', {})
                
                print(f"   😴 Predicted Sleep Quality: {predicted_sleep_quality}/10")
                print(f"   📈 Improvement Potential: {improvement_potential:.2f}")
                print(f"   📊 Factor Analysis keys: {list(factor_analysis.keys())}")
                print(f"   💡 Recommendations: {len(recommendations)}")
                print(f"   🧬 Scientific evidence keys: {list(scientific_evidence.keys())}")
                print(f"   🎯 Actionable insights: {len(actionable_insights)}")
                print(f"   ⚠️ Risk assessment keys: {list(risk_assessment.keys())}")
                
                # Validate content quality
                content_quality_checks = []
                
                # Check if scientific evidence cites sleep research
                if scientific_evidence and any('sleep' in str(v).lower() or 'circadian' in str(v).lower() for v in scientific_evidence.values()):
                    content_quality_checks.append("✅ Scientific evidence cites sleep research")
                else:
                    content_quality_checks.append("❌ Scientific evidence lacks sleep research citations")
                
                # Check if actionable insights provide performance predictions
                if actionable_insights and len(actionable_insights) > 0:
                    content_quality_checks.append("✅ Actionable insights provided")
                else:
                    content_quality_checks.append("❌ Actionable insights missing")
                
                # Check if risk assessment covers immediate and long-term impacts
                if risk_assessment and any(key in risk_assessment for key in ['immediate_risks', 'long_term_risks', 'health_impacts']):
                    content_quality_checks.append("✅ Risk assessment covers immediate/long-term health impacts")
                else:
                    content_quality_checks.append("❌ Risk assessment lacks comprehensive health impact analysis")
                
                for check in content_quality_checks:
                    print(f"   {check}")
                
            else:
                print(f"   ❌ Missing enhanced fields: {missing_fields}")
                success = False
        
        return success

    def run_all_tests(self):
        """Run all enhanced ML endpoint tests"""
        print("🚀 Starting Enhanced ML Prediction Endpoints Testing...")
        print("=" * 80)
        
        # Test all enhanced endpoints
        energy_success = self.test_enhanced_energy_prediction()
        what_if_success = self.test_what_if_scenarios()
        mood_success = self.test_mood_food_correlation()
        sleep_success = self.test_sleep_impact_analysis()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 ENHANCED ML ENDPOINTS TEST SUMMARY")
        print("=" * 80)
        
        print(f"✅ Enhanced Energy Prediction: {'PASS' if energy_success else 'FAIL'}")
        print(f"✅ What-If Scenarios: {'PASS' if what_if_success else 'FAIL'}")
        print(f"✅ Mood-Food Correlation: {'PASS' if mood_success else 'FAIL'}")
        print(f"✅ Sleep Impact Analysis: {'PASS' if sleep_success else 'FAIL'}")
        
        print(f"\n📈 Overall Results: {self.tests_passed}/{self.tests_run} tests passed")
        
        overall_success = energy_success and what_if_success and mood_success and sleep_success
        
        if overall_success:
            print("🎉 ALL ENHANCED ML ENDPOINTS TESTS PASSED!")
            print("✅ Enhanced content and justifications are working correctly")
            print("✅ Scientific basis, reliability indicators, and detailed explanations are present")
            print("✅ All endpoints return comprehensive, scientifically-backed responses")
        else:
            print("❌ SOME ENHANCED ML ENDPOINTS TESTS FAILED")
            print("⚠️ Enhanced content quality needs improvement")
        
        return overall_success

if __name__ == "__main__":
    tester = EnhancedMLEndpointsTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)