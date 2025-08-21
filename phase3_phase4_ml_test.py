#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime, timedelta
import uuid

class Phase3Phase4MLTester:
    def __init__(self, base_url="https://converse-context.preview.emergentagent.com/api"):
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

    def test_enhanced_energy_prediction(self):
        """Test POST /api/ai/enhanced-energy-prediction - A/B testing functionality"""
        print("\n🔋 Testing Enhanced Energy Prediction with A/B Testing...")
        
        # Test 1: Enhanced energy prediction with A/B testing
        test_data = {
            "user_id": "demo-patient-123",
            "intake_data": {
                "calories": 2000,
                "protein_g": 100,
                "carbs_g": 250,
                "fat_g": 70,
                "sleep_hours": 7.5,
                "exercise_minutes": 30,
                "stress_level": 5,
                "water_intake_ml": 2000,
                "caffeine_mg": 150,
                "meal_timing_consistency": 0.8
            },
            "model_variant": "random_forest",
            "include_confidence_intervals": True,
            "include_feature_contributions": True
        }
        
        success1, response1 = self.run_test(
            "Enhanced Energy Prediction - A/B Testing",
            "POST",
            "ai/enhanced-energy-prediction",
            200,
            data=test_data
        )
        
        # Validate enhanced response structure
        if success1 and response1:
            expected_keys = ['predicted_energy', 'confidence_intervals', 'feature_contributions', 
                           'model_variant_used', 'ab_test_group', 'prediction_explanation']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Enhanced response contains all required keys: {expected_keys}")
                
                predicted_energy = response1.get('predicted_energy', 0)
                confidence_intervals = response1.get('confidence_intervals', {})
                feature_contributions = response1.get('feature_contributions', [])
                model_variant = response1.get('model_variant_used', '')
                ab_test_group = response1.get('ab_test_group', '')
                
                print(f"   🔋 Predicted energy: {predicted_energy}/10")
                print(f"   📊 Confidence interval: {confidence_intervals.get('lower', 0):.2f} - {confidence_intervals.get('upper', 0):.2f}")
                print(f"   🧠 Model variant: {model_variant}")
                print(f"   🧪 A/B test group: {ab_test_group}")
                print(f"   📈 Feature contributions: {len(feature_contributions)} factors")
                
            else:
                print(f"   ❌ Enhanced response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: Different model variant
        test_data_2 = {
            "user_id": "demo-patient-123",
            "intake_data": {
                "calories": 1800,
                "protein_g": 120,
                "carbs_g": 200,
                "fat_g": 60,
                "sleep_hours": 8.0,
                "exercise_minutes": 45,
                "stress_level": 3,
                "water_intake_ml": 2500,
                "caffeine_mg": 100,
                "meal_timing_consistency": 0.9
            },
            "model_variant": "linear",
            "include_confidence_intervals": True,
            "include_feature_contributions": True
        }
        
        success2, response2 = self.run_test(
            "Enhanced Energy Prediction - Linear Model",
            "POST",
            "ai/enhanced-energy-prediction",
            200,
            data=test_data_2
        )
        
        if success2 and response2:
            model_variant_2 = response2.get('model_variant_used', '')
            predicted_energy_2 = response2.get('predicted_energy', 0)
            print(f"   🔋 Linear model prediction: {predicted_energy_2}/10")
            print(f"   🧠 Model variant confirmed: {model_variant_2}")
        
        return success1 and success2

    def test_model_feedback(self):
        """Test POST /api/ai/model-feedback - User feedback submission"""
        print("\n📝 Testing Model Feedback Submission...")
        
        # Test 1: Submit user feedback for model improvement
        feedback_data = {
            "user_id": "demo-patient-123",
            "prediction_id": f"pred_{datetime.now().strftime('%H%M%S')}",
            "model_name": "energy_prediction",
            "actual_outcome": 7.8,
            "user_rating": 4.5,
            "feedback_text": "The prediction was quite accurate, felt energetic throughout the day"
        }
        
        success1, response1 = self.run_test(
            "Model Feedback - Energy Prediction",
            "POST",
            "ai/model-feedback",
            200,
            data=feedback_data
        )
        
        # Validate feedback response
        if success1 and response1:
            expected_keys = ['feedback_id', 'status', 'model_updated', 'improvement_impact']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Feedback response contains all required keys: {expected_keys}")
                
                feedback_id = response1.get('feedback_id', '')
                status = response1.get('status', '')
                model_updated = response1.get('model_updated', False)
                improvement_impact = response1.get('improvement_impact', {})
                
                print(f"   📝 Feedback ID: {feedback_id}")
                print(f"   ✅ Status: {status}")
                print(f"   🔄 Model updated: {model_updated}")
                print(f"   📈 Improvement impact: {improvement_impact.get('accuracy_change', 0):.3f}")
                
            else:
                print(f"   ❌ Feedback response missing keys: {missing_keys}")
                success1 = False
        
        return success1

    def test_model_performance(self):
        """Test GET /api/ai/model-performance - Performance metrics retrieval"""
        print("\n📊 Testing Model Performance Metrics...")
        
        # Test 1: Get overall model performance
        success1, response1 = self.run_test(
            "Model Performance - Overall Metrics",
            "GET",
            "ai/model-performance",
            200
        )
        
        # Validate performance response
        if success1 and response1:
            expected_keys = ['model_metrics', 'user_satisfaction', 'continuous_learning_status', 
                           'ab_test_summary', 'performance_trends']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Performance response contains all required keys: {expected_keys}")
                
                model_metrics = response1.get('model_metrics', {})
                user_satisfaction = response1.get('user_satisfaction', {})
                cl_status = response1.get('continuous_learning_status', {})
                ab_test_summary = response1.get('ab_test_summary', {})
                
                # Display key metrics
                accuracy = model_metrics.get('accuracy', 0)
                mae = model_metrics.get('mean_absolute_error', 0)
                avg_rating = user_satisfaction.get('average_rating', 0)
                total_feedback = user_satisfaction.get('total_feedback_count', 0)
                learning_enabled = cl_status.get('enabled', False)
                active_tests = ab_test_summary.get('active_tests', 0)
                
                print(f"   🎯 Model accuracy: {accuracy:.3f}")
                print(f"   📏 Mean absolute error: {mae:.3f}")
                print(f"   ⭐ Average user rating: {avg_rating:.2f}/5")
                print(f"   📝 Total feedback: {total_feedback}")
                print(f"   🔄 Continuous learning: {'Enabled' if learning_enabled else 'Disabled'}")
                print(f"   🧪 Active A/B tests: {active_tests}")
                
            else:
                print(f"   ❌ Performance response missing keys: {missing_keys}")
                success1 = False
        
        return success1

    def test_ab_test_results(self):
        """Test GET /api/ai/ab-test-results/{test_name} - A/B test analysis"""
        print("\n🧪 Testing A/B Test Results Analysis...")
        
        # Test 1: Get A/B test results for energy model variants
        success1, response1 = self.run_test(
            "A/B Test Results - Energy Model Variants",
            "GET",
            "ai/ab-test-results/energy_model_variants",
            200
        )
        
        # Validate A/B test response
        if success1 and response1:
            expected_keys = ['test_name', 'test_status', 'variant_performance', 
                           'statistical_significance', 'recommendations']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ A/B test response contains all required keys: {expected_keys}")
                
                test_name = response1.get('test_name', '')
                test_status = response1.get('test_status', '')
                variant_performance = response1.get('variant_performance', {})
                statistical_significance = response1.get('statistical_significance', {})
                recommendations = response1.get('recommendations', [])
                
                print(f"   🧪 Test name: {test_name}")
                print(f"   📊 Test status: {test_status}")
                print(f"   📈 Variants tested: {len(variant_performance)}")
                
                # Display variant performance
                for variant, performance in variant_performance.items():
                    accuracy = performance.get('accuracy', 0)
                    user_satisfaction = performance.get('user_satisfaction', 0)
                    sample_size = performance.get('sample_size', 0)
                    print(f"      {variant}: Accuracy {accuracy:.3f}, Satisfaction {user_satisfaction:.2f}, Samples {sample_size}")
                
                # Display statistical significance
                p_value = statistical_significance.get('p_value', 1.0)
                is_significant = statistical_significance.get('is_significant', False)
                confidence_level = statistical_significance.get('confidence_level', 0)
                
                print(f"   📊 P-value: {p_value:.4f}")
                print(f"   ✅ Statistically significant: {is_significant}")
                print(f"   🎯 Confidence level: {confidence_level}%")
                print(f"   💡 Recommendations: {len(recommendations)}")
                
            else:
                print(f"   ❌ A/B test response missing keys: {missing_keys}")
                success1 = False
        
        return success1

    def test_continuous_learning_update(self):
        """Test POST /api/ai/continuous-learning-update - Manual continuous learning triggers"""
        print("\n🔄 Testing Continuous Learning Update...")
        
        # Test 1: Trigger continuous learning update
        update_data = {
            "user_id": "demo-patient-123",
            "model_name": "energy_prediction",
            "input_data": {
                "calories": 2000,
                "protein_g": 100,
                "carbs_g": 250,
                "fat_g": 70,
                "sleep_hours": 7.5,
                "exercise_minutes": 30,
                "stress_level": 5
            },
            "actual_outcome": 7.8
        }
        
        success1, response1 = self.run_test(
            "Continuous Learning Update - Energy Model",
            "POST",
            "ai/continuous-learning-update",
            200,
            data=update_data
        )
        
        # Validate continuous learning response
        if success1 and response1:
            expected_keys = ['update_id', 'model_type', 'data_points_processed', 
                           'retraining_triggered', 'performance_impact']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Continuous learning response contains all required keys: {expected_keys}")
                
                update_id = response1.get('update_id', '')
                model_type = response1.get('model_type', '')
                data_points = response1.get('data_points_processed', 0)
                retraining_triggered = response1.get('retraining_triggered', False)
                performance_impact = response1.get('performance_impact', {})
                
                print(f"   🔄 Update ID: {update_id}")
                print(f"   🧠 Model type: {model_type}")
                print(f"   📊 Data points processed: {data_points}")
                print(f"   🔄 Retraining triggered: {retraining_triggered}")
                
                if performance_impact:
                    accuracy_change = performance_impact.get('accuracy_change', 0)
                    mae_change = performance_impact.get('mae_change', 0)
                    print(f"   📈 Accuracy change: {accuracy_change:+.4f}")
                    print(f"   📏 MAE change: {mae_change:+.4f}")
                
            else:
                print(f"   ❌ Continuous learning response missing keys: {missing_keys}")
                success1 = False
        
        return success1

    def test_model_health_check(self):
        """Test GET /api/ai/model-health-check - Comprehensive model health monitoring"""
        print("\n🏥 Testing Model Health Check...")
        
        # Test 1: Comprehensive model health check
        success1, response1 = self.run_test(
            "Model Health Check - All Models",
            "GET",
            "ai/model-health-check",
            200
        )
        
        # Validate health check response
        if success1 and response1:
            expected_keys = ['overall_health', 'model_status', 'performance_alerts', 
                           'system_metrics', 'recommendations']
            missing_keys = [key for key in expected_keys if key not in response1]
            if not missing_keys:
                print(f"   ✅ Health check response contains all required keys: {expected_keys}")
                
                overall_health = response1.get('overall_health', {})
                model_status = response1.get('model_status', {})
                performance_alerts = response1.get('performance_alerts', [])
                system_metrics = response1.get('system_metrics', {})
                recommendations = response1.get('recommendations', [])
                
                # Display overall health
                health_score = overall_health.get('health_score', 0)
                status = overall_health.get('status', 'unknown')
                last_check = overall_health.get('last_health_check', '')
                
                print(f"   🏥 Overall health score: {health_score}/100")
                print(f"   ✅ System status: {status}")
                print(f"   ⏰ Last check: {last_check}")
                
                # Display model status
                print(f"   🧠 Models monitored: {len(model_status)}")
                for model_name, status_info in model_status.items():
                    model_health = status_info.get('health', 'unknown')
                    last_prediction = status_info.get('last_prediction', 'never')
                    accuracy = status_info.get('current_accuracy', 0)
                    print(f"      {model_name}: {model_health} (Accuracy: {accuracy:.3f}, Last: {last_prediction})")
                
                # Display alerts
                print(f"   ⚠️ Performance alerts: {len(performance_alerts)}")
                for alert in performance_alerts[:3]:  # Show first 3 alerts
                    alert_type = alert.get('type', 'unknown')
                    severity = alert.get('severity', 'low')
                    message = alert.get('message', '')
                    print(f"      {severity.upper()}: {alert_type} - {message}")
                
                # Display system metrics
                cpu_usage = system_metrics.get('cpu_usage', 0)
                memory_usage = system_metrics.get('memory_usage', 0)
                prediction_latency = system_metrics.get('avg_prediction_latency_ms', 0)
                
                print(f"   💻 CPU usage: {cpu_usage:.1f}%")
                print(f"   🧠 Memory usage: {memory_usage:.1f}%")
                print(f"   ⚡ Avg prediction latency: {prediction_latency:.1f}ms")
                
                print(f"   💡 Health recommendations: {len(recommendations)}")
                
            else:
                print(f"   ❌ Health check response missing keys: {missing_keys}")
                success1 = False
        
        return success1

    def test_existing_ml_apis(self):
        """Test existing ML APIs to verify they still work"""
        print("\n🔄 Testing Existing ML APIs...")
        
        # Test original energy prediction
        energy_success = self.test_energy_prediction()
        
        # Test mood-food correlation
        mood_success = self.test_mood_food_correlation()
        
        # Test sleep impact analysis
        sleep_success = self.test_sleep_impact_analysis()
        
        # Test what-if scenarios
        whatif_success = self.test_what_if_scenarios()
        
        # Test weekly health patterns
        weekly_success = self.test_weekly_health_patterns()
        
        return energy_success and mood_success and sleep_success and whatif_success and weekly_success

    def test_energy_prediction(self):
        """Test POST /api/ai/energy-prediction - Original energy prediction"""
        print("\n🔋 Testing Original Energy Prediction...")
        
        test_data = {
            "user_id": "demo-patient-123",
            "intake_data": {
                "calories": 2000,
                "protein_g": 100,
                "carbs_g": 250,
                "fat_g": 70,
                "sleep_hours": 7.5,
                "exercise_minutes": 30,
                "stress_level": 5,
                "water_intake_ml": 2000,
                "caffeine_mg": 150,
                "meal_timing_consistency": 0.8
            }
        }
        
        success, response = self.run_test(
            "Energy Prediction - Original API",
            "POST",
            "ai/energy-prediction",
            200,
            data=test_data
        )
        
        if success and response:
            predicted_energy = response.get('predicted_energy', 0)
            confidence = response.get('confidence', 0)
            factors = response.get('factors', [])
            print(f"   🔋 Predicted energy: {predicted_energy}/10")
            print(f"   📊 Confidence: {confidence:.3f}")
            print(f"   📈 Top factors: {len(factors)}")
        
        return success

    def test_mood_food_correlation(self):
        """Test POST /api/ai/mood-food-correlation - Mood correlation analysis"""
        print("\n😊 Testing Mood-Food Correlation...")
        
        test_data = {
            "user_id": "demo-patient-123",
            "timeframe_days": 30
        }
        
        success, response = self.run_test(
            "Mood-Food Correlation Analysis",
            "POST",
            "ai/mood-food-correlation",
            200,
            data=test_data
        )
        
        if success and response:
            correlations = response.get('correlations', [])
            trigger_foods = response.get('trigger_foods', [])
            mood_predictors = response.get('mood_predictors', [])
            print(f"   😊 Correlations found: {len(correlations)}")
            print(f"   🚨 Trigger foods: {len(trigger_foods)}")
            print(f"   🎯 Mood predictors: {len(mood_predictors)}")
        
        return success

    def test_sleep_impact_analysis(self):
        """Test POST /api/ai/sleep-impact-analysis - Sleep impact predictions"""
        print("\n😴 Testing Sleep Impact Analysis...")
        
        test_data = {
            "user_id": "demo-patient-123",
            "daily_choices": {
                "caffeine_timing": "morning",
                "meal_timing": "regular",
                "exercise_timing": "afternoon",
                "screen_time_before_bed": 1.5,
                "alcohol_consumption": 0,
                "stress_level": 4
            }
        }
        
        success, response = self.run_test(
            "Sleep Impact Analysis",
            "POST",
            "ai/sleep-impact-analysis",
            200,
            data=test_data
        )
        
        if success and response:
            predicted_sleep_quality = response.get('predicted_sleep_quality', 0)
            improvement_potential = response.get('improvement_potential', 0)
            factor_analysis = response.get('factor_analysis', [])
            print(f"   😴 Predicted sleep quality: {predicted_sleep_quality}/10")
            print(f"   📈 Improvement potential: {improvement_potential:.1f}%")
            print(f"   📊 Factors analyzed: {len(factor_analysis)}")
        
        return success

    def test_what_if_scenarios(self):
        """Test POST /api/ai/what-if-scenarios - Scenario processing"""
        print("\n🤔 Testing What-If Scenarios...")
        
        test_data = {
            "user_id": "demo-patient-123",
            "base_data": {
                "calories": 2000,
                "protein_g": 100,
                "carbs_g": 250,
                "fat_g": 70,
                "sleep_hours": 7.5,
                "exercise_minutes": 30,
                "stress_level": 5
            },
            "proposed_changes": {
                "protein_g": 120,
                "exercise_minutes": 45,
                "stress_level": 3
            }
        }
        
        success, response = self.run_test(
            "What-If Scenario Analysis",
            "POST",
            "ai/what-if-scenarios",
            200,
            data=test_data
        )
        
        if success and response:
            scenario_id = response.get('scenario_id', '')
            impact_analysis = response.get('impact_analysis', {})
            current_state = response.get('current_state', {})
            predicted_state = response.get('predicted_state', {})
            
            print(f"   🤔 Scenario ID: {scenario_id}")
            print(f"   📊 Impact analysis: {len(impact_analysis)} metrics")
            
            if impact_analysis:
                for metric, change in impact_analysis.items():
                    if isinstance(change, dict) and 'percentage_change' in change:
                        pct_change = change['percentage_change']
                        print(f"      {metric}: {pct_change:+.1f}%")
        
        return success

    def test_weekly_health_patterns(self):
        """Test GET /api/ai/weekly-health-patterns/{user_id} - Weekly pattern analysis"""
        print("\n📅 Testing Weekly Health Patterns...")
        
        success, response = self.run_test(
            "Weekly Health Patterns Analysis",
            "GET",
            "ai/weekly-health-patterns/demo-patient-123",
            200,
            params={"weeks_back": 4}
        )
        
        if success and response:
            patterns = response.get('patterns', {})
            insights = response.get('insights', [])
            anomalies = response.get('anomalies', [])
            trend_direction = response.get('trend_direction', '')
            
            print(f"   📅 Pattern types analyzed: {len(patterns)}")
            print(f"   💡 Insights generated: {len(insights)}")
            print(f"   ⚠️ Anomalies detected: {len(anomalies)}")
            print(f"   📈 Overall trend: {trend_direction}")
            
            # Display pattern scores
            for pattern_type, score in patterns.items():
                if isinstance(score, (int, float)):
                    print(f"      {pattern_type}: {score:.1f}/10")
        
        return success

    def run_all_tests(self):
        """Run all Phase 3 & 4 ML Pipeline tests"""
        print("🚀 Starting Phase 3 & 4 ML Pipeline API Testing...")
        print(f"📍 Base URL: {self.base_url}")
        print("=" * 80)

        # Test Phase 4 Enhanced ML Pipeline APIs (Priority Testing)
        print("\n🧠 PHASE 4 ENHANCED ML PIPELINE APIs (PRIORITY TESTING)")
        print("=" * 60)
        
        enhanced_energy_success = self.test_enhanced_energy_prediction()
        model_feedback_success = self.test_model_feedback()
        model_performance_success = self.test_model_performance()
        ab_test_results_success = self.test_ab_test_results()
        continuous_learning_success = self.test_continuous_learning_update()
        model_health_success = self.test_model_health_check()
        
        # Test Existing ML APIs Verification
        print("\n🔄 EXISTING ML APIS VERIFICATION")
        print("=" * 60)
        
        existing_ml_success = self.test_existing_ml_apis()

        print("\n" + "=" * 80)
        print("📊 PHASE 3 & 4 ML PIPELINE TEST RESULTS SUMMARY")
        print("=" * 80)
        
        print(f"\n🧠 PHASE 4 ENHANCED ML PIPELINE APIs:")
        print(f"   ✅ Enhanced Energy Prediction: {'PASS' if enhanced_energy_success else 'FAIL'}")
        print(f"   ✅ Model Feedback: {'PASS' if model_feedback_success else 'FAIL'}")
        print(f"   ✅ Model Performance: {'PASS' if model_performance_success else 'FAIL'}")
        print(f"   ✅ A/B Test Results: {'PASS' if ab_test_results_success else 'FAIL'}")
        print(f"   ✅ Continuous Learning: {'PASS' if continuous_learning_success else 'FAIL'}")
        print(f"   ✅ Model Health Check: {'PASS' if model_health_success else 'FAIL'}")
        
        print(f"\n🔄 EXISTING ML APIS VERIFICATION:")
        print(f"   ✅ All Existing ML APIs: {'PASS' if existing_ml_success else 'FAIL'}")
        
        print(f"\n📈 Overall Results: {self.tests_passed}/{self.tests_run} tests passed")
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        print(f"📊 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT: Phase 3 & 4 ML Pipeline is performing very well!")
        elif success_rate >= 75:
            print("✅ GOOD: Phase 3 & 4 ML Pipeline is mostly functional with minor issues")
        elif success_rate >= 50:
            print("⚠️ MODERATE: Phase 3 & 4 ML Pipeline has significant issues that need attention")
        else:
            print("❌ CRITICAL: Phase 3 & 4 ML Pipeline has major problems requiring immediate attention")
        
        # Show failed tests if any
        failed_tests = [result for result in self.test_results if not result.get('success', False)]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for result in failed_tests:
                print(f"   - {result['name']}: {result.get('error', 'Status code mismatch')}")
        
        return success_rate >= 75

if __name__ == "__main__":
    tester = Phase3Phase4MLTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)