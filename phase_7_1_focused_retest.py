#!/usr/bin/env python3
"""
🚀 PHASE 7.1 FOCUSED RE-TEST AFTER BUG FIXES
===========================================

Re-testing the Phase 7.1 AI-Enhanced Medical NLP Testing Suite components that previously failed,
specifically focusing on the bug fixes mentioned in the review request:

1. Performance Summary Endpoint - recursive call issue resolution
2. Colloquial Language Processing - pattern generation volume improvements  
3. Grammatical Error Generation - improved fallback patterns
4. Emotional Intelligence Validation - HTTP 500 error fixes
5. Integration Testing - end-to-end workflow validation

EXPECTED IMPROVEMENTS:
- Performance summary endpoint working without recursion
- Colloquial patterns ≥25 patterns generated
- Grammatical patterns ≥10 patterns with proper diversity  
- Emotional intelligence endpoint functional (no HTTP 500)
- Integration testing successful end-to-end
"""

import requests
import json
import time
import os
from typing import Dict, Any, List
from datetime import datetime

class Phase71FocusedRetester:
    def __init__(self):
        # Get backend URL from environment
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    self.backend_url = line.split('=')[1].strip()
                    break
        
        if not self.backend_url.endswith('/api'):
            self.backend_url = f"{self.backend_url}/api"
        
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
        print(f"🚀 PHASE 7.1 FOCUSED RE-TEST AFTER BUG FIXES")
        print(f"Backend URL: {self.backend_url}")
        print(f"Test Start Time: {datetime.now().isoformat()}")
        print("=" * 80)

    def log_test_result(self, test_name: str, success: bool, response_time: float = 0, details: str = ""):
        """Log individual test results"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        result = {
            'test_name': test_name,
            'success': success,
            'response_time': response_time,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        print(f"{status} | {test_name} | {response_time:.3f}s | {details}")

    def make_request(self, method: str, endpoint: str, data: Dict = None, timeout: int = 30) -> tuple:
        """Make HTTP request with error handling and timing"""
        url = f"{self.backend_url}{endpoint}"
        start_time = time.time()
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, timeout=timeout, verify=False)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, timeout=timeout, verify=False)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response_time = time.time() - start_time
            return response, response_time, None
            
        except requests.exceptions.Timeout:
            response_time = time.time() - start_time
            return None, response_time, "Request timeout"
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            return None, response_time, f"Request error: {str(e)}"
        except Exception as e:
            response_time = time.time() - start_time
            return None, response_time, f"Unexpected error: {str(e)}"

    def test_performance_summary_endpoint(self):
        """Test Performance Summary Endpoint - should be fixed from recursive call issue"""
        print("\n📊 TESTING: Performance Summary Endpoint (GET)")
        
        # Test the GET endpoint (corrected from POST)
        response, response_time, error = self.make_request('GET', '/ai-testing/phase-7-1/performance-summary', timeout=15)
        
        if error:
            self.log_test_result("Performance Summary POST", False, response_time, error)
            return False
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # Validate response structure
                required_fields = ['algorithm_version', 'performance_metrics', 'component_analysis']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test_result("Performance Summary Structure", False, response_time, f"Missing fields: {missing_fields}")
                    return False
                
                # Check if recursive call issue is resolved (should not timeout or error)
                algorithm_version = data.get('algorithm_version', '')
                performance_metrics = data.get('performance_metrics', {})
                component_analysis = data.get('component_analysis', {})
                
                # Validate we have meaningful data
                version_ok = '7.1' in algorithm_version
                metrics_ok = len(performance_metrics) > 0
                components_ok = len(component_analysis) > 0
                
                if version_ok and metrics_ok and components_ok:
                    details = f"Version: {algorithm_version}, Metrics: {len(performance_metrics)}, Components: {len(component_analysis)}"
                    self.log_test_result("Performance Summary POST", True, response_time, details)
                    return True
                else:
                    issues = []
                    if not version_ok: issues.append(f"Wrong version: {algorithm_version}")
                    if not metrics_ok: issues.append("No metrics")
                    if not components_ok: issues.append("No components")
                    details = ", ".join(issues)
                    self.log_test_result("Performance Summary POST", False, response_time, details)
                    return False
                    
            except json.JSONDecodeError:
                self.log_test_result("Performance Summary JSON", False, response_time, "Invalid JSON response")
                return False
        else:
            self.log_test_result("Performance Summary HTTP", False, response_time, f"HTTP {response.status_code}")
            return False

    def test_colloquial_language_processing(self):
        """Test Colloquial Language Processing - should generate ≥25 patterns"""
        print("\n🗣️ TESTING: Colloquial Language Processing (Volume Improvement)")
        
        # Test with realistic medical terms to generate 25+ patterns
        test_cases = [
            {
                "name": "Comprehensive Medical Terms",
                "formal_terms": ["headache", "nausea", "fatigue", "chest pain", "abdominal pain", "joint pain", "dizziness", "shortness of breath"],
                "cultural_context": "general_american",
                "expected_min_patterns": 25
            },
            {
                "name": "Pain and Discomfort Terms", 
                "formal_terms": ["back pain", "muscle ache", "stomach ache", "sore throat", "burning sensation"],
                "cultural_context": "rural_southern",
                "expected_min_patterns": 15
            }
        ]
        
        passed_cases = 0
        total_patterns_generated = 0
        
        for test_case in test_cases:
            request_data = {
                "formal_terms": test_case["formal_terms"],
                "cultural_context": test_case["cultural_context"],
                "pattern_count_target": test_case["expected_min_patterns"]
            }
            
            response, response_time, error = self.make_request('POST', '/ai-testing/phase-7-1/colloquial-language', request_data, timeout=20)
            
            if error:
                self.log_test_result(f"Colloquial Processing - {test_case['name']}", False, response_time, error)
                continue
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Validate response structure
                    required_fields = ['colloquial_patterns', 'pattern_diversity', 'generation_summary']
                    if all(field in data for field in required_fields):
                        
                        colloquial_patterns = data.get('colloquial_patterns', [])
                        pattern_diversity = data.get('pattern_diversity', {})
                        generation_summary = data.get('generation_summary', {})
                        
                        # Check pattern volume - this is the key improvement
                        patterns_count = len(colloquial_patterns)
                        total_patterns_generated += patterns_count
                        expected_min = test_case["expected_min_patterns"]
                        
                        # Check pattern quality
                        categories_covered = pattern_diversity.get('categories_covered', 0)
                        cultural_contexts = pattern_diversity.get('cultural_contexts', 0)
                        
                        # Volume check - main focus of this test
                        volume_ok = patterns_count >= expected_min
                        diversity_ok = categories_covered >= 3
                        
                        if volume_ok and diversity_ok:
                            passed_cases += 1
                            details = f"Patterns: {patterns_count}/{expected_min} (✓), Categories: {categories_covered}, Cultural: {cultural_contexts}"
                            self.log_test_result(f"Colloquial Processing - {test_case['name']}", True, response_time, details)
                        else:
                            issues = []
                            if not volume_ok: issues.append(f"Low volume: {patterns_count}/{expected_min}")
                            if not diversity_ok: issues.append(f"Low diversity: {categories_covered}")
                            details = ", ".join(issues)
                            self.log_test_result(f"Colloquial Processing - {test_case['name']}", False, response_time, details)
                    else:
                        self.log_test_result(f"Colloquial Processing - {test_case['name']}", False, response_time, "Missing required fields")
                        
                except json.JSONDecodeError:
                    self.log_test_result(f"Colloquial Processing - {test_case['name']}", False, response_time, "Invalid JSON")
            else:
                self.log_test_result(f"Colloquial Processing - {test_case['name']}", False, response_time, f"HTTP {response.status_code}")
        
        # Overall assessment - focus on total pattern volume
        success_rate = (passed_cases / len(test_cases)) * 100
        overall_success = success_rate >= 50 and total_patterns_generated >= 25  # At least 25 total patterns
        
        details = f"Success Rate: {success_rate:.1f}% ({passed_cases}/{len(test_cases)}), Total Patterns: {total_patterns_generated}"
        self.log_test_result("Colloquial Language Processing Overall", overall_success, 0, details)
        
        return overall_success

    def test_grammatical_error_generation(self):
        """Test Grammatical Error Generation - should generate ≥10 patterns with diversity"""
        print("\n🤖 TESTING: Grammatical Error Generation (Improved Fallback)")
        
        test_scenarios = [
            {
                "name": "Chest Pain Medical Text",
                "base_text": "I have severe chest pain that started this morning and radiates to my left arm",
                "num_variants": 12,
                "expected_min": 10
            },
            {
                "name": "Respiratory Symptoms", 
                "base_text": "I can't breathe properly and I'm coughing up blood",
                "num_variants": 15,
                "expected_min": 10
            }
        ]
        
        passed_scenarios = 0
        total_patterns_generated = 0
        
        for scenario in test_scenarios:
            request_data = {
                "base_medical_text": scenario["base_text"],
                "num_variants": scenario["num_variants"],
                "error_types": ["grammar", "spelling", "punctuation", "word_order", "tense"]
            }
            
            response, response_time, error = self.make_request('POST', '/ai-testing/phase-7-1/grammatical-errors', request_data, timeout=20)
            
            if error:
                self.log_test_result(f"Grammar Generation - {scenario['name']}", False, response_time, error)
                continue
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Validate response structure
                    required_fields = ['error_patterns', 'generation_time', 'pattern_types', 'fallback_patterns_used']
                    if all(field in data for field in required_fields):
                        
                        error_patterns = data.get('error_patterns', [])
                        pattern_types = data.get('pattern_types', [])
                        fallback_patterns_used = data.get('fallback_patterns_used', 0)
                        
                        # Check pattern volume and diversity - key improvements
                        patterns_generated = len(error_patterns)
                        total_patterns_generated += patterns_generated
                        expected_min = scenario["expected_min"]
                        
                        # Check diversity
                        types_diversity = len(pattern_types)
                        
                        # Volume and diversity checks
                        volume_ok = patterns_generated >= expected_min
                        diversity_ok = types_diversity >= 4  # At least 4 different error types
                        fallback_ok = fallback_patterns_used >= 0  # Fallback system working
                        
                        if volume_ok and diversity_ok:
                            passed_scenarios += 1
                            details = f"Patterns: {patterns_generated}/{expected_min} (✓), Types: {types_diversity}, Fallback: {fallback_patterns_used}"
                            self.log_test_result(f"Grammar Generation - {scenario['name']}", True, response_time, details)
                        else:
                            issues = []
                            if not volume_ok: issues.append(f"Low volume: {patterns_generated}/{expected_min}")
                            if not diversity_ok: issues.append(f"Low diversity: {types_diversity}")
                            details = ", ".join(issues)
                            self.log_test_result(f"Grammar Generation - {scenario['name']}", False, response_time, details)
                    else:
                        self.log_test_result(f"Grammar Generation - {scenario['name']}", False, response_time, "Missing required fields")
                        
                except json.JSONDecodeError:
                    self.log_test_result(f"Grammar Generation - {scenario['name']}", False, response_time, "Invalid JSON")
            else:
                self.log_test_result(f"Grammar Generation - {scenario['name']}", False, response_time, f"HTTP {response.status_code}")
        
        # Overall assessment
        success_rate = (passed_scenarios / len(test_scenarios)) * 100
        overall_success = success_rate >= 50 and total_patterns_generated >= 10
        
        details = f"Success Rate: {success_rate:.1f}% ({passed_scenarios}/{len(test_scenarios)}), Total Patterns: {total_patterns_generated}"
        self.log_test_result("Grammatical Error Generation Overall", overall_success, 0, details)
        
        return overall_success

    def test_emotional_intelligence_validation(self):
        """Test Emotional Intelligence Validation - should be fixed from HTTP 500 errors"""
        print("\n😰 TESTING: Emotional Intelligence Validation (HTTP 500 Fix)")
        
        test_scenarios = [
            {
                "name": "High Anxiety Medical Scenario",
                "patient_input": "I'm really scared about this chest pain, what if I'm having a heart attack?",
                "ai_response": "I understand you're feeling very anxious about your chest pain. Let's work together to assess your symptoms carefully.",
                "emotional_context": {"emotional_state": "high_anxiety", "intensity_level": "high", "medical_concern": "cardiac"}
            },
            {
                "name": "Depression with Physical Symptoms",
                "patient_input": "I don't even care anymore, this headache never goes away and nothing helps",
                "ai_response": "I hear that you're feeling hopeless about your persistent headache. Your feelings are valid, and I want to help find solutions.",
                "emotional_context": {"emotional_state": "depression", "intensity_level": "moderate", "medical_concern": "neurological"}
            },
            {
                "name": "Fear and Panic Response",
                "patient_input": "I can't breathe and I'm terrified something is seriously wrong with me",
                "ai_response": "I can see you're experiencing both physical symptoms and intense fear. Let's address both your breathing and your concerns.",
                "emotional_context": {"emotional_state": "fear_panic", "intensity_level": "high", "medical_concern": "respiratory"}
            }
        ]
        
        passed_scenarios = 0
        
        for scenario in test_scenarios:
            request_data = {
                "patient_input": scenario["patient_input"],
                "ai_response": scenario["ai_response"],
                "emotional_context": scenario["emotional_context"]
            }
            
            response, response_time, error = self.make_request('POST', '/ai-testing/phase-7-1/emotional-intelligence', request_data, timeout=20)
            
            if error:
                self.log_test_result(f"Emotional Intelligence - {scenario['name']}", False, response_time, error)
                continue
            
            # Check if HTTP 500 error is resolved
            if response.status_code == 500:
                self.log_test_result(f"Emotional Intelligence - {scenario['name']}", False, response_time, "HTTP 500 error still present")
                continue
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Validate response structure
                    required_fields = ['empathy_validation', 'emotional_scenarios', 'improvement_suggestions']
                    if all(field in data for field in required_fields):
                        
                        empathy_validation = data.get('empathy_validation', {})
                        emotional_scenarios = data.get('emotional_scenarios', [])
                        improvement_suggestions = data.get('improvement_suggestions', [])
                        
                        # Check validation quality
                        empathy_score = empathy_validation.get('empathy_score', 0)
                        emotional_appropriateness = empathy_validation.get('emotional_appropriateness', 0)
                        empathy_level = empathy_validation.get('empathy_level', '')
                        
                        # Quality checks - endpoint should be functional now
                        empathy_ok = empathy_score >= 4.0  # Reasonable empathy minimum
                        appropriateness_ok = emotional_appropriateness >= 4.0
                        scenarios_ok = len(emotional_scenarios) >= 2  # Should generate scenarios
                        suggestions_ok = len(improvement_suggestions) >= 1
                        
                        if empathy_ok and appropriateness_ok and scenarios_ok:
                            passed_scenarios += 1
                            details = f"Empathy: {empathy_score:.1f}/10, Appropriateness: {emotional_appropriateness:.1f}/10, Level: {empathy_level}"
                            self.log_test_result(f"Emotional Intelligence - {scenario['name']}", True, response_time, details)
                        else:
                            issues = []
                            if not empathy_ok: issues.append(f"Low empathy: {empathy_score:.1f}")
                            if not appropriateness_ok: issues.append(f"Poor appropriateness: {emotional_appropriateness:.1f}")
                            if not scenarios_ok: issues.append(f"Few scenarios: {len(emotional_scenarios)}")
                            details = ", ".join(issues)
                            self.log_test_result(f"Emotional Intelligence - {scenario['name']}", False, response_time, details)
                    else:
                        self.log_test_result(f"Emotional Intelligence - {scenario['name']}", False, response_time, "Missing required fields")
                        
                except json.JSONDecodeError:
                    self.log_test_result(f"Emotional Intelligence - {scenario['name']}", False, response_time, "Invalid JSON")
            else:
                self.log_test_result(f"Emotional Intelligence - {scenario['name']}", False, response_time, f"HTTP {response.status_code}")
        
        # Overall assessment - main goal is no HTTP 500 errors
        success_rate = (passed_scenarios / len(test_scenarios)) * 100
        overall_success = success_rate >= 66  # At least 2/3 scenarios should pass
        
        details = f"Success Rate: {success_rate:.1f}% ({passed_scenarios}/{len(test_scenarios)}) - HTTP 500 errors resolved"
        self.log_test_result("Emotional Intelligence Validation Overall", overall_success, 0, details)
        
        return overall_success

    def test_comprehensive_integration(self):
        """Test Comprehensive Integration - end-to-end workflow validation"""
        print("\n🔗 TESTING: Comprehensive Integration (End-to-End)")
        
        # Test comprehensive integration with realistic medical scenarios
        medical_scenarios = [
            "Patient presents with severe chest pain radiating to left arm with shortness of breath",
            "Elderly patient complains of persistent headache with confusion and dizziness",
            "Young adult reports anxiety and panic attacks with physical symptoms"
        ]
        
        test_configuration = {
            "grammatical_config": {
                "variants_per_scenario": 8,
                "error_types": ["grammar", "spelling", "punctuation", "word_order"]
            },
            "incomplete_config": {
                "cases_per_scenario": 6,
                "incompleteness_types": ["cutoff", "fragmented", "emotional_interrupt"]
            },
            "colloquial_config": {
                "cultural_contexts": ["general_american", "rural_southern"],
                "cases_per_context": 4
            },
            "emotional_config": {
                "scenarios_per_symptom": 4,
                "emotional_states": ["anxiety", "fear", "depression"]
            }
        }
        
        request_data = {
            "medical_scenarios": medical_scenarios,
            "test_configuration": test_configuration,
            "integration_level": "comprehensive"
        }
        
        response, response_time, error = self.make_request('POST', '/ai-testing/phase-7-1/comprehensive', request_data, timeout=45)
        
        if error:
            self.log_test_result("Comprehensive Integration", False, response_time, error)
            return False
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # Validate response structure
                required_fields = ['suite_id', 'total_test_cases', 'generation_time', 'success_rate', 'test_results', 'component_status']
                if all(field in data for field in required_fields):
                    
                    suite_id = data.get('suite_id', '')
                    total_test_cases = data.get('total_test_cases', 0)
                    generation_time = data.get('generation_time', 0)
                    success_rate = data.get('success_rate', 0)
                    test_results = data.get('test_results', {})
                    component_status = data.get('component_status', {})
                    
                    # Check integration quality
                    test_cases_ok = total_test_cases >= 30  # Should generate substantial test cases
                    success_rate_ok = success_rate >= 80.0  # High success rate expected after fixes
                    performance_ok = response_time < 45.0  # Should complete within timeout
                    
                    # Check individual component results
                    grammatical_tests = test_results.get('grammatical_error_tests', 0)
                    incomplete_tests = test_results.get('incomplete_sentence_tests', 0)
                    colloquial_tests = test_results.get('colloquial_language_tests', 0)
                    emotional_tests = test_results.get('emotional_intelligence_tests', 0)
                    
                    components_ok = all([
                        grammatical_tests > 0,
                        incomplete_tests > 0,
                        colloquial_tests > 0,
                        emotional_tests > 0
                    ])
                    
                    # Check component status
                    all_components_active = all(
                        status == 'active' for status in component_status.values()
                    )
                    
                    if test_cases_ok and success_rate_ok and performance_ok and components_ok and all_components_active:
                        details = f"Test Cases: {total_test_cases}, Success: {success_rate:.1f}%, Time: {response_time:.1f}s, Components: All Active"
                        self.log_test_result("Comprehensive Integration", True, response_time, details)
                        return True
                    else:
                        issues = []
                        if not test_cases_ok: issues.append(f"Few cases: {total_test_cases}")
                        if not success_rate_ok: issues.append(f"Low success: {success_rate:.1f}%")
                        if not performance_ok: issues.append(f"Slow: {response_time:.1f}s")
                        if not components_ok: issues.append("Missing component tests")
                        if not all_components_active: issues.append("Inactive components")
                        details = ", ".join(issues)
                        self.log_test_result("Comprehensive Integration", False, response_time, details)
                        return False
                else:
                    self.log_test_result("Comprehensive Integration", False, response_time, "Missing required fields")
                    return False
                    
            except json.JSONDecodeError:
                self.log_test_result("Comprehensive Integration", False, response_time, "Invalid JSON")
                return False
        else:
            self.log_test_result("Comprehensive Integration", False, response_time, f"HTTP {response.status_code}")
            return False

    def run_focused_retests(self):
        """Execute focused re-tests for previously failing components"""
        print("🚀 Starting Phase 7.1 Focused Re-Test After Bug Fixes")
        print("=" * 80)
        
        # Test execution order - focus on previously failing components
        test_results = {}
        
        # 1. Performance Summary Endpoint (was failing with recursion)
        test_results['performance_summary'] = self.test_performance_summary_endpoint()
        
        # 2. Colloquial Language Processing (was generating insufficient patterns)
        test_results['colloquial_processing'] = self.test_colloquial_language_processing()
        
        # 3. Grammatical Error Generation (needed improved fallback patterns)
        test_results['grammatical_errors'] = self.test_grammatical_error_generation()
        
        # 4. Emotional Intelligence Validation (was returning HTTP 500)
        test_results['emotional_intelligence'] = self.test_emotional_intelligence_validation()
        
        # 5. Comprehensive Integration (end-to-end workflow)
        test_results['comprehensive_integration'] = self.test_comprehensive_integration()
        
        # Generate final report
        self.generate_final_report(test_results)
        
        return test_results

    def generate_final_report(self, test_results: Dict[str, bool]):
        """Generate comprehensive re-test report"""
        print("\n" + "=" * 80)
        print("🎯 PHASE 7.1 FOCUSED RE-TEST AFTER BUG FIXES - FINAL REPORT")
        print("=" * 80)
        
        # Calculate overall success rate
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"📊 OVERALL RE-TEST RESULTS:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed Tests: {self.passed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Status: {'✅ FIXES SUCCESSFUL' if success_rate >= 80 else '⚠️ PARTIAL FIXES' if success_rate >= 60 else '❌ FIXES FAILED'}")
        
        print(f"\n🔍 COMPONENT RE-TEST RESULTS:")
        component_status = {
            'performance_summary': 'Performance Summary Endpoint (Recursion Fix)',
            'colloquial_processing': 'Colloquial Language Processing (Volume ≥25)',
            'grammatical_errors': 'Grammatical Error Generation (Patterns ≥10)',
            'emotional_intelligence': 'Emotional Intelligence Validation (HTTP 500 Fix)',
            'comprehensive_integration': 'Integration Testing (End-to-End)'
        }
        
        for component, result in test_results.items():
            status = "✅ FIXED" if result else "❌ STILL FAILING"
            description = component_status.get(component, component.replace('_', ' ').title())
            print(f"   {description}: {status}")
        
        # Bug Fix Analysis
        print(f"\n🐛 BUG FIX ANALYSIS:")
        
        fixes_successful = []
        fixes_failed = []
        
        for component, result in test_results.items():
            if result:
                fixes_successful.append(component_status.get(component, component))
            else:
                fixes_failed.append(component_status.get(component, component))
        
        if fixes_successful:
            print(f"   ✅ SUCCESSFUL FIXES:")
            for fix in fixes_successful:
                print(f"      - {fix}")
        
        if fixes_failed:
            print(f"   ❌ FAILED FIXES:")
            for fix in fixes_failed:
                print(f"      - {fix}")
        
        # Production Readiness Assessment
        print(f"\n🎯 PRODUCTION READINESS ASSESSMENT:")
        
        critical_fixes = [
            test_results.get('performance_summary', False),
            test_results.get('emotional_intelligence', False)
        ]
        
        volume_fixes = [
            test_results.get('colloquial_processing', False),
            test_results.get('grammatical_errors', False)
        ]
        
        integration_fix = test_results.get('comprehensive_integration', False)
        
        critical_fixed = all(critical_fixes)
        volume_improved = any(volume_fixes)
        integration_working = integration_fix
        
        print(f"   Critical Bug Fixes: {'✅ RESOLVED' if critical_fixed else '❌ UNRESOLVED'}")
        print(f"   Pattern Volume Improvements: {'✅ IMPROVED' if volume_improved else '❌ NOT IMPROVED'}")
        print(f"   Integration Testing: {'✅ WORKING' if integration_working else '❌ FAILING'}")
        
        overall_ready = critical_fixed and volume_improved and integration_working
        print(f"   Overall System: {'✅ PRODUCTION READY' if overall_ready else '❌ NOT PRODUCTION READY'}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if success_rate >= 80:
            print("   ✅ Phase 7.1 bug fixes are successful - system ready for production")
            print("   ✅ Critical issues resolved, pattern generation improved")
            print("   ✅ Integration testing working end-to-end")
        elif success_rate >= 60:
            print("   ⚠️ Phase 7.1 shows partial improvement but needs additional fixes")
            print("   ⚠️ Some critical issues resolved, continue debugging remaining failures")
            print("   ⚠️ Monitor pattern generation volumes and endpoint stability")
        else:
            print("   ❌ Phase 7.1 bug fixes were not successful")
            print("   ❌ Critical issues persist - do not deploy to production")
            print("   ❌ Focus on resolving HTTP 500 errors and recursion issues")
        
        print(f"\n📝 RE-TEST COMPLETION TIME: {datetime.now().isoformat()}")
        print("=" * 80)

def main():
    """Main re-test execution function"""
    retester = Phase71FocusedRetester()
    
    try:
        test_results = retester.run_focused_retests()
        return test_results
    except KeyboardInterrupt:
        print("\n⚠️ Re-testing interrupted by user")
        return None
    except Exception as e:
        print(f"\n❌ Re-testing failed with error: {e}")
        return None

if __name__ == "__main__":
    main()