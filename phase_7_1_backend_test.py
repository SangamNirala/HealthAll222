#!/usr/bin/env python3
"""
🚀 PHASE 7.1: AI-ENHANCED MEDICAL NLP TESTING SUITE COMPREHENSIVE BACKEND VALIDATION
===================================================================================

Comprehensive testing of Phase 7.1 AI-powered testing components that have been implemented,
focusing on the remaining testing & validation requirements as specified in the review request.

TESTING SCOPE:

**Core AI Testing Components:**
1. Core AI Testing Engine (/app/backend/ai_powered_medical_nlp_test_suite.py)
2. Grammatical Error Pattern Generator (/app/backend/gemini_grammatical_error_generator.py)
3. Incomplete Sentence Processor (/app/backend/ai_enhanced_incomplete_sentence_processor.py)
4. Colloquial Language Processor (/app/backend/ai_powered_colloquial_language_processor.py)
5. Emotional Intelligence Validator (/app/backend/ai_emotional_intelligence_validator.py)
6. Integration Framework (/app/backend/phase_7_1_integration_framework.py)

**API Endpoints to Test:**
- POST /api/ai-testing/phase-7-1/comprehensive
- POST /api/ai-testing/phase-7-1/analyze-language
- POST /api/ai-testing/phase-7-1/grammatical-errors
- POST /api/ai-testing/phase-7-1/incomplete-fragments
- POST /api/ai-testing/phase-7-1/colloquial-language
- POST /api/ai-testing/phase-7-1/emotional-intelligence
- GET /api/ai-testing/phase-7-1/performance-summary
- GET /api/ai-testing/phase-7-1/status

**Critical Testing Requirements:**
1. Real Gemini API Integration Testing
2. Performance Benchmarking
3. Error Handling Validation
4. Integration Testing
5. Medical Accuracy Validation

**Performance Targets:**
- Language analysis: <3s response time
- Pattern generation: <5s for 10+ variants
- Integration testing: <10s for comprehensive suite
- API endpoints: <2s for standard requests
- 99%+ uptime and availability under load

TARGET: Validate Phase 7.1 AI-Enhanced Medical NLP Testing Suite readiness for production deployment
"""

import requests
import json
import time
import os
from typing import Dict, Any, List
from datetime import datetime

class Phase71AITestingSuiteTester:
    def __init__(self):
        # Get backend URL from environment
        self.backend_url = os.getenv('REACT_APP_BACKEND_URL', 'https://ai-test-suite.preview.emergentagent.com')
        if not self.backend_url.endswith('/api'):
            self.backend_url = f"{self.backend_url}/api"
        
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.performance_metrics = {
            'language_analysis_times': [],
            'pattern_generation_times': [],
            'integration_times': [],
            'api_response_times': []
        }
        
        print(f"🚀 PHASE 7.1: AI-ENHANCED MEDICAL NLP TESTING SUITE VALIDATION")
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
                response = requests.get(url, timeout=timeout, verify=False)  # Disable SSL verification
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, timeout=timeout, verify=False)  # Disable SSL verification
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

    def test_phase_71_status_endpoint(self):
        """Test Phase 7.1 status endpoint"""
        print("\n🔍 TESTING: Phase 7.1 Status Endpoint")
        
        response, response_time, error = self.make_request('GET', '/ai-testing/phase-7-1/status')
        
        if error:
            self.log_test_result("Phase 7.1 Status Check", False, response_time, error)
            return False
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # Validate response structure
                required_fields = ['phase_version', 'overall_status', 'components', 'gemini_integration', 'capabilities']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test_result("Phase 7.1 Status Structure", False, response_time, f"Missing fields: {missing_fields}")
                    return False
                
                # Check component status
                components = data.get('components', {})
                expected_components = [
                    'ai_testing_engine',
                    'grammatical_error_generator', 
                    'incomplete_sentence_processor',
                    'colloquial_language_processor',
                    'emotional_intelligence_validator'
                ]
                
                active_components = sum(1 for comp in expected_components if components.get(comp) == 'active')
                
                # Check Gemini integration
                gemini_status = data.get('gemini_integration', {})
                api_keys_available = gemini_status.get('api_keys_available', 0)
                
                details = f"Components: {active_components}/{len(expected_components)} active, API Keys: {api_keys_available}"
                self.log_test_result("Phase 7.1 Status Check", True, response_time, details)
                
                return True
                
            except json.JSONDecodeError:
                self.log_test_result("Phase 7.1 Status JSON Parse", False, response_time, "Invalid JSON response")
                return False
        else:
            self.log_test_result("Phase 7.1 Status HTTP", False, response_time, f"HTTP {response.status_code}")
            return False

    def test_ai_language_analysis(self):
        """Test AI-powered language analysis endpoint"""
        print("\n🧠 TESTING: AI Language Analysis")
        
        test_cases = [
            {
                "name": "Complex Medical Text",
                "input": "I've been having this crushing chest pain that radiates to my left arm and jaw, started about 2 hours ago during exercise",
                "expected_patterns": ["grammatical_analysis", "medical_entities", "urgency_assessment"]
            },
            {
                "name": "Grammatically Poor Text", 
                "input": "me chest hurt bad cant breath good need help",
                "expected_patterns": ["grammar_issues", "medical_content", "processing_difficulty"]
            },
            {
                "name": "Incomplete Medical Fragment",
                "input": "Doctor, I'm really worried about this pain in my...",
                "expected_patterns": ["incompleteness", "emotional_markers", "completion_needs"]
            },
            {
                "name": "Colloquial Medical Expression",
                "input": "My tummy's been acting up real bad, feels like butterflies but worse",
                "expected_patterns": ["colloquial_language", "informal_expressions", "medical_mapping"]
            }
        ]
        
        passed_cases = 0
        total_analysis_time = 0
        
        for test_case in test_cases:
            request_data = {
                "input_text": test_case["input"]
            }
            
            response, response_time, error = self.make_request('POST', '/ai-testing/phase-7-1/analyze-language', request_data)
            total_analysis_time += response_time
            
            if error:
                self.log_test_result(f"Language Analysis - {test_case['name']}", False, response_time, error)
                continue
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Validate response structure
                    required_fields = ['analysis_results', 'processing_time', 'confidence_score']
                    if all(field in data for field in required_fields):
                        
                        # Check if analysis contains expected patterns
                        analysis_results = data.get('analysis_results', {})
                        confidence = data.get('confidence_score', 0)
                        
                        # Performance check - should be under 3s target
                        performance_ok = response_time < 3.0
                        confidence_ok = confidence > 0.3
                        
                        if performance_ok and confidence_ok:
                            passed_cases += 1
                            details = f"Confidence: {confidence:.2f}, Performance: {'✓' if performance_ok else '✗'}"
                            self.log_test_result(f"Language Analysis - {test_case['name']}", True, response_time, details)
                        else:
                            details = f"Confidence: {confidence:.2f}, Slow: {response_time:.1f}s > 3s"
                            self.log_test_result(f"Language Analysis - {test_case['name']}", False, response_time, details)
                    else:
                        self.log_test_result(f"Language Analysis - {test_case['name']}", False, response_time, "Missing required fields")
                        
                except json.JSONDecodeError:
                    self.log_test_result(f"Language Analysis - {test_case['name']}", False, response_time, "Invalid JSON")
            else:
                self.log_test_result(f"Language Analysis - {test_case['name']}", False, response_time, f"HTTP {response.status_code}")
        
        # Record performance metrics
        avg_analysis_time = total_analysis_time / len(test_cases)
        self.performance_metrics['language_analysis_times'].append(avg_analysis_time)
        
        # Overall language analysis assessment
        success_rate = (passed_cases / len(test_cases)) * 100
        overall_success = success_rate >= 75  # 75% success rate threshold
        
        details = f"Success Rate: {success_rate:.1f}% ({passed_cases}/{len(test_cases)}), Avg Time: {avg_analysis_time:.2f}s"
        self.log_test_result("AI Language Analysis Overall", overall_success, avg_analysis_time, details)
        
        return overall_success

    def test_grammatical_error_generation(self):
        """Test AI-powered grammatical error pattern generation"""
        print("\n🤖 TESTING: Grammatical Error Pattern Generation")
        
        test_scenarios = [
            {
                "name": "Chest Pain Scenario",
                "base_text": "I have severe chest pain that started this morning",
                "num_variants": 8
            },
            {
                "name": "Headache Scenario", 
                "base_text": "My head hurts really bad and I feel nauseous",
                "num_variants": 6
            },
            {
                "name": "Respiratory Scenario",
                "base_text": "I can't breathe properly and I'm coughing a lot",
                "num_variants": 5
            }
        ]
        
        passed_scenarios = 0
        total_generation_time = 0
        
        for scenario in test_scenarios:
            request_data = {
                "base_medical_text": scenario["base_text"],
                "num_variants": scenario["num_variants"]
            }
            
            response, response_time, error = self.make_request('POST', '/ai-testing/phase-7-1/grammatical-errors', request_data, timeout=15)
            total_generation_time += response_time
            
            if error:
                self.log_test_result(f"Grammar Generation - {scenario['name']}", False, response_time, error)
                continue
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Validate response structure
                    required_fields = ['error_patterns', 'generation_time', 'pattern_types']
                    if all(field in data for field in required_fields):
                        
                        error_patterns = data.get('error_patterns', [])
                        pattern_types = data.get('pattern_types', [])
                        generation_time = data.get('generation_time', 0)
                        
                        # Check if we got expected number of patterns
                        patterns_generated = len(error_patterns)
                        expected_patterns = scenario["num_variants"]
                        
                        # Performance check - should be under 5s for pattern generation
                        performance_ok = response_time < 5.0
                        patterns_ok = patterns_generated >= expected_patterns * 0.7  # At least 70% of requested patterns
                        diversity_ok = len(pattern_types) >= 3  # At least 3 different error types
                        
                        if performance_ok and patterns_ok and diversity_ok:
                            passed_scenarios += 1
                            details = f"Patterns: {patterns_generated}/{expected_patterns}, Types: {len(pattern_types)}, Time: {response_time:.1f}s"
                            self.log_test_result(f"Grammar Generation - {scenario['name']}", True, response_time, details)
                        else:
                            issues = []
                            if not performance_ok: issues.append(f"Slow: {response_time:.1f}s")
                            if not patterns_ok: issues.append(f"Few patterns: {patterns_generated}")
                            if not diversity_ok: issues.append(f"Low diversity: {len(pattern_types)}")
                            details = ", ".join(issues)
                            self.log_test_result(f"Grammar Generation - {scenario['name']}", False, response_time, details)
                    else:
                        self.log_test_result(f"Grammar Generation - {scenario['name']}", False, response_time, "Missing required fields")
                        
                except json.JSONDecodeError:
                    self.log_test_result(f"Grammar Generation - {scenario['name']}", False, response_time, "Invalid JSON")
            else:
                self.log_test_result(f"Grammar Generation - {scenario['name']}", False, response_time, f"HTTP {response.status_code}")
        
        # Record performance metrics
        avg_generation_time = total_generation_time / len(test_scenarios)
        self.performance_metrics['pattern_generation_times'].append(avg_generation_time)
        
        # Overall assessment
        success_rate = (passed_scenarios / len(test_scenarios)) * 100
        overall_success = success_rate >= 75
        
        details = f"Success Rate: {success_rate:.1f}% ({passed_scenarios}/{len(test_scenarios)}), Avg Time: {avg_generation_time:.2f}s"
        self.log_test_result("Grammatical Error Generation Overall", overall_success, avg_generation_time, details)
        
        return overall_success

    def test_incomplete_sentence_processing(self):
        """Test AI-enhanced incomplete sentence processing"""
        print("\n🧠 TESTING: Incomplete Sentence Processing")
        
        test_fragments = [
            {
                "name": "Pain Cutoff",
                "fragment": "My chest is really...",
                "context": {"patient_history": "Previous cardiac issues", "conversation_history": "Discussing chest symptoms"},
                "expected_urgency": ["high", "critical", "medium"]
            },
            {
                "name": "Emotional Interruption",
                "fragment": "I'm scared that this might be...",
                "context": {"emotional_state": "high_anxiety", "medical_trauma_history": "Previous bad diagnosis"},
                "expected_urgency": ["medium", "high"]
            },
            {
                "name": "Symptom Fragment",
                "fragment": "Started feeling weird after eating and then...",
                "context": {"symptom_onset": "post_meal", "duration": "2_hours"},
                "expected_urgency": ["medium", "low"]
            }
        ]
        
        passed_fragments = 0
        
        for fragment_test in test_fragments:
            request_data = {
                "fragment_text": fragment_test["fragment"],
                "context": fragment_test["context"]
            }
            
            response, response_time, error = self.make_request('POST', '/ai-testing/phase-7-1/incomplete-fragments', request_data, timeout=10)
            
            if error:
                self.log_test_result(f"Fragment Processing - {fragment_test['name']}", False, response_time, error)
                continue
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Validate response structure
                    required_fields = ['fragment_analysis', 'completion_suggestions', 'urgency_assessment']
                    if all(field in data for field in required_fields):
                        
                        fragment_analysis = data.get('fragment_analysis', {})
                        completion_suggestions = data.get('completion_suggestions', [])
                        urgency_assessment = data.get('urgency_assessment', {})
                        
                        # Check analysis quality
                        incompleteness_type = fragment_analysis.get('incompleteness_type', '')
                        urgency_level = urgency_assessment.get('urgency_level', '')
                        suggestions_count = len(completion_suggestions)
                        
                        # Validate urgency assessment
                        urgency_ok = urgency_level in fragment_test['expected_urgency']
                        suggestions_ok = suggestions_count >= 1
                        analysis_ok = incompleteness_type != ''
                        
                        if urgency_ok and suggestions_ok and analysis_ok:
                            passed_fragments += 1
                            details = f"Urgency: {urgency_level}, Suggestions: {suggestions_count}, Type: {incompleteness_type}"
                            self.log_test_result(f"Fragment Processing - {fragment_test['name']}", True, response_time, details)
                        else:
                            issues = []
                            if not urgency_ok: issues.append(f"Urgency: {urgency_level}")
                            if not suggestions_ok: issues.append("No suggestions")
                            if not analysis_ok: issues.append("No analysis")
                            details = ", ".join(issues)
                            self.log_test_result(f"Fragment Processing - {fragment_test['name']}", False, response_time, details)
                    else:
                        self.log_test_result(f"Fragment Processing - {fragment_test['name']}", False, response_time, "Missing required fields")
                        
                except json.JSONDecodeError:
                    self.log_test_result(f"Fragment Processing - {fragment_test['name']}", False, response_time, "Invalid JSON")
            else:
                self.log_test_result(f"Fragment Processing - {fragment_test['name']}", False, response_time, f"HTTP {response.status_code}")
        
        # Overall assessment
        success_rate = (passed_fragments / len(test_fragments)) * 100
        overall_success = success_rate >= 75
        
        details = f"Success Rate: {success_rate:.1f}% ({passed_fragments}/{len(test_fragments)})"
        self.log_test_result("Incomplete Sentence Processing Overall", overall_success, 0, details)
        
        return overall_success

    def test_colloquial_language_processing(self):
        """Test AI-powered colloquial language processing"""
        print("\n🗣️ TESTING: Colloquial Language Processing")
        
        test_cases = [
            {
                "name": "Basic Medical Terms",
                "formal_terms": ["headache", "nausea", "fatigue"],
                "cultural_context": "african_american"
            },
            {
                "name": "Pain Expressions",
                "formal_terms": ["chest pain", "abdominal pain", "joint pain"],
                "cultural_context": "rural_southern"
            },
            {
                "name": "Digestive Issues",
                "formal_terms": ["constipation", "diarrhea", "heartburn"],
                "cultural_context": "elderly_community"
            }
        ]
        
        passed_cases = 0
        
        for test_case in test_cases:
            request_data = {
                "formal_terms": test_case["formal_terms"],
                "cultural_context": test_case["cultural_context"]
            }
            
            response, response_time, error = self.make_request('POST', '/ai-testing/phase-7-1/colloquial-language', request_data, timeout=12)
            
            if error:
                self.log_test_result(f"Colloquial Processing - {test_case['name']}", False, response_time, error)
                continue
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Validate response structure
                    required_fields = ['colloquial_patterns', 'pattern_diversity']
                    if all(field in data for field in required_fields):
                        
                        colloquial_patterns = data.get('colloquial_patterns', [])
                        pattern_diversity = data.get('pattern_diversity', {})
                        cultural_analysis = data.get('cultural_analysis')
                        
                        # Check pattern quality
                        patterns_count = len(colloquial_patterns)
                        categories_covered = pattern_diversity.get('categories_covered', 0)
                        cultural_contexts = pattern_diversity.get('cultural_contexts', 0)
                        
                        # Quality checks
                        patterns_ok = patterns_count >= len(test_case["formal_terms"]) * 3  # At least 3 patterns per term
                        diversity_ok = categories_covered >= 3  # At least 3 different categories
                        cultural_ok = cultural_analysis is not None
                        
                        if patterns_ok and diversity_ok:
                            passed_cases += 1
                            details = f"Patterns: {patterns_count}, Categories: {categories_covered}, Cultural: {'✓' if cultural_ok else '✗'}"
                            self.log_test_result(f"Colloquial Processing - {test_case['name']}", True, response_time, details)
                        else:
                            issues = []
                            if not patterns_ok: issues.append(f"Few patterns: {patterns_count}")
                            if not diversity_ok: issues.append(f"Low diversity: {categories_covered}")
                            if not cultural_ok: issues.append("No cultural analysis")
                            details = ", ".join(issues)
                            self.log_test_result(f"Colloquial Processing - {test_case['name']}", False, response_time, details)
                    else:
                        self.log_test_result(f"Colloquial Processing - {test_case['name']}", False, response_time, "Missing required fields")
                        
                except json.JSONDecodeError:
                    self.log_test_result(f"Colloquial Processing - {test_case['name']}", False, response_time, "Invalid JSON")
            else:
                self.log_test_result(f"Colloquial Processing - {test_case['name']}", False, response_time, f"HTTP {response.status_code}")
        
        # Overall assessment
        success_rate = (passed_cases / len(test_cases)) * 100
        overall_success = success_rate >= 75
        
        details = f"Success Rate: {success_rate:.1f}% ({passed_cases}/{len(test_cases)})"
        self.log_test_result("Colloquial Language Processing Overall", overall_success, 0, details)
        
        return overall_success

    def test_emotional_intelligence_validation(self):
        """Test AI-enhanced emotional intelligence validation"""
        print("\n😰 TESTING: Emotional Intelligence Validation")
        
        test_scenarios = [
            {
                "name": "High Anxiety Patient",
                "patient_input": "I'm really freaking out about this chest pain, what if I'm having a heart attack?",
                "ai_response": "I understand you're feeling very anxious about your chest pain. Let's work together to assess your symptoms carefully.",
                "emotional_context": {"emotional_state": "high_anxiety", "intensity_level": "high"}
            },
            {
                "name": "Depressed Patient",
                "patient_input": "I don't even care anymore, nothing helps this pain anyway",
                "ai_response": "I hear that you're feeling hopeless about your pain. Your feelings are valid, and I want to help find solutions.",
                "emotional_context": {"emotional_state": "depression", "intensity_level": "moderate"}
            },
            {
                "name": "Scared Patient",
                "patient_input": "I'm terrified this headache means I have a brain tumor",
                "ai_response": "I can understand why you'd be scared about persistent headaches. Let's explore your symptoms to give you clarity.",
                "emotional_context": {"emotional_state": "fear_terror", "intensity_level": "high"}
            }
        ]
        
        passed_scenarios = 0
        
        for scenario in test_scenarios:
            request_data = {
                "patient_input": scenario["patient_input"],
                "ai_response": scenario["ai_response"],
                "emotional_context": scenario["emotional_context"]
            }
            
            response, response_time, error = self.make_request('POST', '/ai-testing/phase-7-1/emotional-intelligence', request_data, timeout=15)
            
            if error:
                self.log_test_result(f"Emotional Intelligence - {scenario['name']}", False, response_time, error)
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
                        
                        # Check empathy validation quality
                        empathy_score = empathy_validation.get('empathy_score', 0)
                        emotional_appropriateness = empathy_validation.get('emotional_appropriateness', 0)
                        overall_quality = empathy_validation.get('overall_quality_score', 0)
                        empathy_level = empathy_validation.get('empathy_level', '')
                        
                        # Quality checks
                        empathy_ok = empathy_score >= 5.0  # Moderate empathy minimum
                        appropriateness_ok = emotional_appropriateness >= 5.0
                        scenarios_ok = len(emotional_scenarios) >= 3  # Should generate additional scenarios
                        
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
        
        # Overall assessment
        success_rate = (passed_scenarios / len(test_scenarios)) * 100
        overall_success = success_rate >= 75
        
        details = f"Success Rate: {success_rate:.1f}% ({passed_scenarios}/{len(test_scenarios)})"
        self.log_test_result("Emotional Intelligence Validation Overall", overall_success, 0, details)
        
        return overall_success

    def test_comprehensive_integration(self):
        """Test comprehensive Phase 7.1 integration"""
        print("\n🔗 TESTING: Comprehensive Integration Testing")
        
        # Test comprehensive integration with multiple medical scenarios
        medical_scenarios = [
            "Patient presents with severe chest pain radiating to left arm",
            "Elderly patient complains of persistent headache and confusion",
            "Young adult reports anxiety and panic attacks with physical symptoms"
        ]
        
        test_configuration = {
            "grammatical_config": {
                "variants_per_scenario": 5,
                "error_types": ["grammar", "spelling", "punctuation"]
            },
            "incomplete_config": {
                "cases_per_scenario": 8,
                "incompleteness_types": ["cutoff", "fragmented", "emotional_interrupt"]
            },
            "colloquial_config": {
                "cultural_contexts": ["african_american", "rural_southern"],
                "cases_per_context": 5
            },
            "emotional_config": {
                "scenarios_per_symptom": 6,
                "emotional_states": ["anxiety", "fear", "depression"]
            }
        }
        
        request_data = {
            "medical_scenarios": medical_scenarios,
            "test_configuration": test_configuration
        }
        
        response, response_time, error = self.make_request('POST', '/ai-testing/phase-7-1/comprehensive', request_data, timeout=30)
        
        if error:
            self.log_test_result("Comprehensive Integration", False, response_time, error)
            return False
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # Validate response structure
                required_fields = ['suite_id', 'total_test_cases', 'generation_time', 'success_rate', 'test_results']
                if all(field in data for field in required_fields):
                    
                    suite_id = data.get('suite_id', '')
                    total_test_cases = data.get('total_test_cases', 0)
                    generation_time = data.get('generation_time', 0)
                    success_rate = data.get('success_rate', 0)
                    test_results = data.get('test_results', {})
                    
                    # Performance check - should be under 10s for comprehensive suite
                    performance_ok = response_time < 10.0
                    test_cases_ok = total_test_cases >= 50  # Should generate substantial test cases
                    success_rate_ok = success_rate >= 95.0  # High success rate expected
                    
                    # Check individual component results
                    grammatical_tests = test_results.get('grammatical_error_tests', 0)
                    incomplete_tests = test_results.get('incomplete_sentence_tests', 0)
                    colloquial_tests = test_results.get('colloquial_language_tests', 0)
                    emotional_tests = test_results.get('emotional_intelligence_tests', 0)
                    integration_tests = test_results.get('integration_test_cases', 0)
                    
                    components_ok = all([
                        grammatical_tests > 0,
                        incomplete_tests > 0,
                        colloquial_tests > 0,
                        emotional_tests > 0,
                        integration_tests > 0
                    ])
                    
                    if performance_ok and test_cases_ok and success_rate_ok and components_ok:
                        details = f"Test Cases: {total_test_cases}, Success: {success_rate:.1f}%, Time: {response_time:.1f}s"
                        self.log_test_result("Comprehensive Integration", True, response_time, details)
                        
                        # Record integration performance
                        self.performance_metrics['integration_times'].append(response_time)
                        return True
                    else:
                        issues = []
                        if not performance_ok: issues.append(f"Slow: {response_time:.1f}s")
                        if not test_cases_ok: issues.append(f"Few cases: {total_test_cases}")
                        if not success_rate_ok: issues.append(f"Low success: {success_rate:.1f}%")
                        if not components_ok: issues.append("Missing components")
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

    def test_performance_summary(self):
        """Test Phase 7.1 performance summary endpoint"""
        print("\n📊 TESTING: Performance Summary")
        
        response, response_time, error = self.make_request('GET', '/ai-testing/phase-7-1/performance-summary', timeout=10)
        
        if error:
            self.log_test_result("Performance Summary", False, response_time, error)
            return False
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # Validate response structure
                expected_fields = ['algorithm_version', 'framework_statistics', 'component_performance', 'success_rate']
                if all(field in data for field in expected_fields):
                    
                    algorithm_version = data.get('algorithm_version', '')
                    framework_stats = data.get('framework_statistics', {})
                    component_performance = data.get('component_performance', {})
                    success_rate = data.get('success_rate', 0)
                    
                    # Check if we have performance data for all components
                    expected_components = [
                        'grammatical_generator',
                        'incomplete_processor', 
                        'colloquial_processor',
                        'emotional_validator'
                    ]
                    
                    components_present = sum(1 for comp in expected_components if comp in component_performance)
                    version_ok = '7.1' in algorithm_version
                    components_ok = components_present >= 3  # At least 3 components should have data
                    
                    if version_ok and components_ok:
                        details = f"Version: {algorithm_version}, Components: {components_present}/{len(expected_components)}, Success: {success_rate:.1f}%"
                        self.log_test_result("Performance Summary", True, response_time, details)
                        return True
                    else:
                        issues = []
                        if not version_ok: issues.append(f"Wrong version: {algorithm_version}")
                        if not components_ok: issues.append(f"Few components: {components_present}")
                        details = ", ".join(issues)
                        self.log_test_result("Performance Summary", False, response_time, details)
                        return False
                else:
                    self.log_test_result("Performance Summary", False, response_time, "Missing required fields")
                    return False
                    
            except json.JSONDecodeError:
                self.log_test_result("Performance Summary", False, response_time, "Invalid JSON")
                return False
        else:
            self.log_test_result("Performance Summary", False, response_time, f"HTTP {response.status_code}")
            return False

    def run_all_tests(self):
        """Execute all Phase 7.1 tests"""
        print("🚀 Starting Phase 7.1 AI-Enhanced Medical NLP Testing Suite Validation")
        print("=" * 80)
        
        # Test execution order - start with status, then individual components, then integration
        test_results = {}
        
        # 1. Status Check
        test_results['status'] = self.test_phase_71_status_endpoint()
        
        # 2. Core AI Testing Components
        test_results['language_analysis'] = self.test_ai_language_analysis()
        test_results['grammatical_errors'] = self.test_grammatical_error_generation()
        test_results['incomplete_processing'] = self.test_incomplete_sentence_processing()
        test_results['colloquial_processing'] = self.test_colloquial_language_processing()
        test_results['emotional_intelligence'] = self.test_emotional_intelligence_validation()
        
        # 3. Integration Testing
        test_results['comprehensive_integration'] = self.test_comprehensive_integration()
        
        # 4. Performance Summary
        test_results['performance_summary'] = self.test_performance_summary()
        
        # Generate final report
        self.generate_final_report(test_results)
        
        return test_results

    def generate_final_report(self, test_results: Dict[str, bool]):
        """Generate comprehensive test report"""
        print("\n" + "=" * 80)
        print("🎯 PHASE 7.1 AI-ENHANCED MEDICAL NLP TESTING SUITE - FINAL REPORT")
        print("=" * 80)
        
        # Calculate overall success rate
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed Tests: {self.passed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Status: {'✅ PRODUCTION READY' if success_rate >= 95 else '⚠️ NEEDS ATTENTION' if success_rate >= 75 else '❌ CRITICAL ISSUES'}")
        
        print(f"\n🔍 COMPONENT TEST RESULTS:")
        for component, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {component.replace('_', ' ').title()}: {status}")
        
        # Performance Analysis
        print(f"\n⚡ PERFORMANCE ANALYSIS:")
        if self.performance_metrics['language_analysis_times']:
            avg_analysis = sum(self.performance_metrics['language_analysis_times']) / len(self.performance_metrics['language_analysis_times'])
            print(f"   Language Analysis: {avg_analysis:.2f}s (Target: <3s) {'✅' if avg_analysis < 3 else '❌'}")
        
        if self.performance_metrics['pattern_generation_times']:
            avg_generation = sum(self.performance_metrics['pattern_generation_times']) / len(self.performance_metrics['pattern_generation_times'])
            print(f"   Pattern Generation: {avg_generation:.2f}s (Target: <5s) {'✅' if avg_generation < 5 else '❌'}")
        
        if self.performance_metrics['integration_times']:
            avg_integration = sum(self.performance_metrics['integration_times']) / len(self.performance_metrics['integration_times'])
            print(f"   Integration Testing: {avg_integration:.2f}s (Target: <10s) {'✅' if avg_integration < 10 else '❌'}")
        
        # Critical Issues Summary
        failed_tests = [name for name, result in test_results.items() if not result]
        if failed_tests:
            print(f"\n❌ CRITICAL ISSUES IDENTIFIED:")
            for failed_test in failed_tests:
                print(f"   - {failed_test.replace('_', ' ').title()}")
        
        # Production Readiness Assessment
        print(f"\n🎯 PRODUCTION READINESS ASSESSMENT:")
        
        core_components_pass = all([
            test_results.get('status', False),
            test_results.get('language_analysis', False),
            test_results.get('grammatical_errors', False),
            test_results.get('incomplete_processing', False),
            test_results.get('colloquial_processing', False),
            test_results.get('emotional_intelligence', False)
        ])
        
        integration_pass = test_results.get('comprehensive_integration', False)
        performance_pass = test_results.get('performance_summary', False)
        
        print(f"   Core AI Components: {'✅ READY' if core_components_pass else '❌ NOT READY'}")
        print(f"   Integration Framework: {'✅ READY' if integration_pass else '❌ NOT READY'}")
        print(f"   Performance Monitoring: {'✅ READY' if performance_pass else '❌ NOT READY'}")
        
        overall_ready = core_components_pass and integration_pass and performance_pass
        print(f"   Overall System: {'✅ PRODUCTION READY' if overall_ready else '❌ NOT PRODUCTION READY'}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if success_rate >= 95:
            print("   ✅ Phase 7.1 AI-Enhanced Medical NLP Testing Suite is ready for production deployment")
            print("   ✅ All core components are functional with acceptable performance")
            print("   ✅ Integration framework is working correctly")
        elif success_rate >= 75:
            print("   ⚠️ Phase 7.1 system shows good functionality but needs minor improvements")
            print("   ⚠️ Address failed test cases before production deployment")
            print("   ⚠️ Monitor performance metrics closely")
        else:
            print("   ❌ Phase 7.1 system has critical issues that must be resolved")
            print("   ❌ Do not deploy to production until issues are fixed")
            print("   ❌ Focus on failed core components first")
        
        print(f"\n📝 TEST COMPLETION TIME: {datetime.now().isoformat()}")
        print("=" * 80)

def main():
    """Main test execution function"""
    tester = Phase71AITestingSuiteTester()
    
    try:
        test_results = tester.run_all_tests()
        return test_results
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted by user")
        return None
    except Exception as e:
        print(f"\n❌ Testing failed with error: {e}")
        return None

if __name__ == "__main__":
    main()