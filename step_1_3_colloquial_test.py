#!/usr/bin/env python3
"""
Comprehensive Testing Suite for Step 1.3 Colloquial Medical Expression Handler
Integration with Medical AI Service

This test suite validates:
1. Core Step 1.3 Requirements (5 required examples)
2. Medical AI Integration with colloquial expressions
3. Extended Robustness Testing (additional colloquial expressions)
4. Integration with Steps 1.1 & 1.2 (combined normalization)
5. Performance & Reliability testing

Test Environment: Uses production backend URL for realistic testing
"""

import asyncio
import json
import time
import requests
from typing import Dict, List, Any, Tuple
from datetime import datetime
import os

# Backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://medai-personalize.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class Step13ColloquialTester:
    """Comprehensive tester for Step 1.3 Colloquial Medical Expression Handler"""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_test_result(self, test_name: str, passed: bool, details: Dict[str, Any]):
        """Log individual test result"""
        self.test_results.append({
            'test_name': test_name,
            'passed': passed,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
        
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
            
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not passed:
            print(f"   Details: {details.get('error', 'Unknown error')}")
    
    async def test_core_step_1_3_requirements(self) -> Dict[str, Any]:
        """Test all 5 core Step 1.3 required examples"""
        print("\n" + "="*80)
        print("🎯 TESTING CORE STEP 1.3 REQUIREMENTS (5 Required Examples)")
        print("="*80)
        
        # Core required examples from the review request
        core_examples = [
            ("tummy hurt", "abdominal pain"),
            ("feeling crappy", "feeling unwell"),
            ("can't poop", "experiencing constipation"),
            ("throwing up", "vomiting"),
            ("dizzy spells", "episodes of dizziness")
        ]
        
        results = {
            'total_tests': len(core_examples),
            'passed': 0,
            'failed': 0,
            'examples': []
        }
        
        for original, expected_conversion in core_examples:
            try:
                # Test direct normalization first
                normalization_result = await self.test_direct_normalization(original, expected_conversion)
                
                # Test Medical AI integration
                medical_ai_result = await self.test_medical_ai_integration(original, expected_conversion)
                
                # Combine results
                overall_passed = normalization_result['passed'] and medical_ai_result['passed']
                
                example_result = {
                    'original': original,
                    'expected': expected_conversion,
                    'normalization': normalization_result,
                    'medical_ai': medical_ai_result,
                    'overall_passed': overall_passed
                }
                
                results['examples'].append(example_result)
                
                if overall_passed:
                    results['passed'] += 1
                else:
                    results['failed'] += 1
                
                self.log_test_result(
                    f"Core Example: '{original}' → '{expected_conversion}'",
                    overall_passed,
                    example_result
                )
                
            except Exception as e:
                error_result = {
                    'original': original,
                    'expected': expected_conversion,
                    'error': str(e),
                    'overall_passed': False
                }
                results['examples'].append(error_result)
                results['failed'] += 1
                
                self.log_test_result(
                    f"Core Example: '{original}' → '{expected_conversion}'",
                    False,
                    {'error': str(e)}
                )
        
        success_rate = (results['passed'] / results['total_tests']) * 100
        print(f"\n📊 Core Step 1.3 Results: {results['passed']}/{results['total_tests']} ({success_rate:.1f}%)")
        
        return results
    
    async def test_direct_normalization(self, original: str, expected: str) -> Dict[str, Any]:
        """Test direct text normalization for colloquial expressions"""
        try:
            # We'll test this by sending to Medical AI and checking the normalization
            # Since we don't have a direct normalization endpoint, we'll use the medical AI
            response = requests.post(
                f"{API_BASE}/medical-ai/initialize",
                json={
                    "patient_id": "test-colloquial-patient",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code != 200:
                return {'passed': False, 'error': f'Initialization failed: {response.status_code}'}
            
            init_data = response.json()
            consultation_id = init_data.get('consultation_id')
            
            # Send the colloquial message
            message_response = requests.post(
                f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": original,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if message_response.status_code != 200:
                return {'passed': False, 'error': f'Message processing failed: {message_response.status_code}'}
            
            message_data = message_response.json()
            
            # Check if the expected conversion appears in the response or context
            response_text = message_data.get('response', '').lower()
            context = str(message_data.get('context', {})).lower()
            
            # Look for the expected conversion in the processed text
            conversion_found = expected.lower() in response_text or expected.lower() in context
            
            return {
                'passed': conversion_found,
                'original': original,
                'expected': expected,
                'response': message_data.get('response', ''),
                'consultation_id': consultation_id,
                'conversion_detected': conversion_found
            }
            
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    async def test_medical_ai_integration(self, original: str, expected: str) -> Dict[str, Any]:
        """Test Medical AI integration with colloquial expressions"""
        try:
            # Initialize consultation
            response = requests.post(
                f"{API_BASE}/medical-ai/initialize",
                json={
                    "patient_id": "test-medical-ai-integration",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code != 200:
                return {'passed': False, 'error': f'Medical AI initialization failed: {response.status_code}'}
            
            init_data = response.json()
            consultation_id = init_data.get('consultation_id')
            
            # Send colloquial message
            message_response = requests.post(
                f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": original,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if message_response.status_code != 200:
                return {'passed': False, 'error': f'Medical AI message processing failed: {message_response.status_code}'}
            
            message_data = message_response.json()
            
            # Validate Medical AI response structure
            required_keys = ['response', 'context', 'stage', 'urgency']
            missing_keys = [key for key in required_keys if key not in message_data]
            
            if missing_keys:
                return {'passed': False, 'error': f'Missing response keys: {missing_keys}'}
            
            # Check if AI provides appropriate medical response
            response_text = message_data.get('response', '')
            has_medical_response = len(response_text) > 50  # Reasonable medical response length
            
            # Check urgency detection works with colloquial expressions
            urgency = message_data.get('urgency', 'none')
            urgency_appropriate = urgency in ['none', 'routine', 'urgent', 'emergency']
            
            integration_success = has_medical_response and urgency_appropriate and not missing_keys
            
            return {
                'passed': integration_success,
                'original': original,
                'expected': expected,
                'response_length': len(response_text),
                'urgency': urgency,
                'consultation_id': consultation_id,
                'has_medical_response': has_medical_response,
                'urgency_appropriate': urgency_appropriate
            }
            
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    async def test_extended_robustness(self) -> Dict[str, Any]:
        """Test extended robustness with additional colloquial expressions"""
        print("\n" + "="*80)
        print("🚀 TESTING EXTENDED ROBUSTNESS (Additional Colloquial Expressions)")
        print("="*80)
        
        # Extended robustness test cases from review request
        extended_examples = [
            # Digestive variations
            ("belly ache", "abdominal pain"),
            ("gut pain really bad", "severe abdominal pain"),
            
            # Bowel movements
            ("cant poop for days", "experiencing constipation"),
            ("backed up", "experiencing constipation"),
            
            # Feeling unwell
            ("feel awful", "feel unwell"),
            ("under the weather", "feeling unwell"),
            
            # Breathing
            ("can't breathe", "difficulty breathing"),
            ("short of breath", "experiencing shortness of breath"),
            
            # Fatigue
            ("wiped out", "extremely fatigued"),
            ("dead tired", "extremely fatigued"),
            
            # Compound expressions
            ("tummy hurt and throwing up", ["abdominal pain", "vomiting"]),
        ]
        
        results = {
            'total_tests': len(extended_examples),
            'passed': 0,
            'failed': 0,
            'examples': []
        }
        
        for original, expected in extended_examples:
            try:
                # Handle compound expressions (multiple expected terms)
                if isinstance(expected, list):
                    expected_terms = expected
                    test_name = f"Extended Compound: '{original}' → {expected_terms}"
                else:
                    expected_terms = [expected]
                    test_name = f"Extended: '{original}' → '{expected}'"
                
                # Test with Medical AI
                integration_result = await self.test_extended_expression(original, expected_terms)
                
                example_result = {
                    'original': original,
                    'expected': expected,
                    'result': integration_result,
                    'passed': integration_result['passed']
                }
                
                results['examples'].append(example_result)
                
                if integration_result['passed']:
                    results['passed'] += 1
                else:
                    results['failed'] += 1
                
                self.log_test_result(test_name, integration_result['passed'], example_result)
                
            except Exception as e:
                error_result = {
                    'original': original,
                    'expected': expected,
                    'error': str(e),
                    'passed': False
                }
                results['examples'].append(error_result)
                results['failed'] += 1
                
                self.log_test_result(f"Extended: '{original}'", False, {'error': str(e)})
        
        success_rate = (results['passed'] / results['total_tests']) * 100
        print(f"\n📊 Extended Robustness Results: {results['passed']}/{results['total_tests']} ({success_rate:.1f}%)")
        
        return results
    
    async def test_extended_expression(self, original: str, expected_terms: List[str]) -> Dict[str, Any]:
        """Test extended colloquial expression with Medical AI"""
        try:
            # Initialize consultation
            response = requests.post(
                f"{API_BASE}/medical-ai/initialize",
                json={
                    "patient_id": "test-extended-expression",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code != 200:
                return {'passed': False, 'error': f'Initialization failed: {response.status_code}'}
            
            init_data = response.json()
            consultation_id = init_data.get('consultation_id')
            
            # Send message
            message_response = requests.post(
                f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": original,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if message_response.status_code != 200:
                return {'passed': False, 'error': f'Message processing failed: {message_response.status_code}'}
            
            message_data = message_response.json()
            
            # Check for expected terms in response or context
            response_text = message_data.get('response', '').lower()
            context = str(message_data.get('context', {})).lower()
            combined_text = response_text + " " + context
            
            # For compound expressions, check if at least one expected term is found
            terms_found = []
            for term in expected_terms:
                if term.lower() in combined_text:
                    terms_found.append(term)
            
            # Success if at least one term found for compound, or the single term for simple expressions
            conversion_success = len(terms_found) > 0
            
            return {
                'passed': conversion_success,
                'original': original,
                'expected_terms': expected_terms,
                'terms_found': terms_found,
                'response': message_data.get('response', ''),
                'consultation_id': consultation_id
            }
            
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    async def test_integration_with_steps_1_1_and_1_2(self) -> Dict[str, Any]:
        """Test integration with Steps 1.1 & 1.2 (combined normalization)"""
        print("\n" + "="*80)
        print("🔗 TESTING INTEGRATION WITH STEPS 1.1 & 1.2 (Combined Normalization)")
        print("="*80)
        
        # Combined test cases from review request
        combined_examples = [
            # Grammar + colloquial
            ("i having tummy hurt 2 days", ["I have been having", "abdominal pain", "2 days"]),
            
            # Spelling + colloquial  
            ("haedache and dizzy spells", ["headache", "episodes of dizziness"]),
            
            # Complex combination
            ("me belly really hurt when breath", ["my", "abdominal pain", "when I breathe"]),
        ]
        
        results = {
            'total_tests': len(combined_examples),
            'passed': 0,
            'failed': 0,
            'examples': []
        }
        
        for original, expected_elements in combined_examples:
            try:
                integration_result = await self.test_combined_normalization(original, expected_elements)
                
                example_result = {
                    'original': original,
                    'expected_elements': expected_elements,
                    'result': integration_result,
                    'passed': integration_result['passed']
                }
                
                results['examples'].append(example_result)
                
                if integration_result['passed']:
                    results['passed'] += 1
                else:
                    results['failed'] += 1
                
                self.log_test_result(
                    f"Combined: '{original}' → {expected_elements}",
                    integration_result['passed'],
                    example_result
                )
                
            except Exception as e:
                error_result = {
                    'original': original,
                    'expected_elements': expected_elements,
                    'error': str(e),
                    'passed': False
                }
                results['examples'].append(error_result)
                results['failed'] += 1
                
                self.log_test_result(f"Combined: '{original}'", False, {'error': str(e)})
        
        success_rate = (results['passed'] / results['total_tests']) * 100
        print(f"\n📊 Combined Integration Results: {results['passed']}/{results['total_tests']} ({success_rate:.1f}%)")
        
        return results
    
    async def test_combined_normalization(self, original: str, expected_elements: List[str]) -> Dict[str, Any]:
        """Test combined normalization (Steps 1.1, 1.2, and 1.3)"""
        try:
            # Initialize consultation
            response = requests.post(
                f"{API_BASE}/medical-ai/initialize",
                json={
                    "patient_id": "test-combined-normalization",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if response.status_code != 200:
                return {'passed': False, 'error': f'Initialization failed: {response.status_code}'}
            
            init_data = response.json()
            consultation_id = init_data.get('consultation_id')
            
            # Send message with combined issues
            message_response = requests.post(
                f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": original,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if message_response.status_code != 200:
                return {'passed': False, 'error': f'Message processing failed: {message_response.status_code}'}
            
            message_data = message_response.json()
            
            # Check for expected elements in response or context
            response_text = message_data.get('response', '').lower()
            context = str(message_data.get('context', {})).lower()
            combined_text = response_text + " " + context
            
            # Check how many expected elements are found
            elements_found = []
            for element in expected_elements:
                if element.lower() in combined_text:
                    elements_found.append(element)
            
            # Success if at least 60% of expected elements are found
            success_threshold = max(1, len(expected_elements) * 0.6)
            normalization_success = len(elements_found) >= success_threshold
            
            return {
                'passed': normalization_success,
                'original': original,
                'expected_elements': expected_elements,
                'elements_found': elements_found,
                'success_threshold': success_threshold,
                'response': message_data.get('response', ''),
                'consultation_id': consultation_id
            }
            
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    async def test_performance_and_reliability(self) -> Dict[str, Any]:
        """Test performance and reliability of the system"""
        print("\n" + "="*80)
        print("⚡ TESTING PERFORMANCE & RELIABILITY")
        print("="*80)
        
        # Performance test cases
        test_cases = [
            "tummy hurt",
            "feeling crappy and dizzy spells",
            "can't poop for 3 days",
            "throwing up all morning",
            "i having belly ache when breath"
        ]
        
        results = {
            'total_tests': len(test_cases),
            'passed': 0,
            'failed': 0,
            'performance_metrics': {
                'response_times': [],
                'average_response_time': 0,
                'max_response_time': 0,
                'min_response_time': float('inf')
            },
            'reliability_metrics': {
                'successful_requests': 0,
                'failed_requests': 0,
                'error_rate': 0
            }
        }
        
        for test_case in test_cases:
            try:
                start_time = time.time()
                
                # Test the full flow
                performance_result = await self.test_performance_case(test_case)
                
                end_time = time.time()
                response_time = end_time - start_time
                
                # Record performance metrics
                results['performance_metrics']['response_times'].append(response_time)
                results['performance_metrics']['max_response_time'] = max(
                    results['performance_metrics']['max_response_time'], 
                    response_time
                )
                results['performance_metrics']['min_response_time'] = min(
                    results['performance_metrics']['min_response_time'], 
                    response_time
                )
                
                if performance_result['passed']:
                    results['passed'] += 1
                    results['reliability_metrics']['successful_requests'] += 1
                else:
                    results['failed'] += 1
                    results['reliability_metrics']['failed_requests'] += 1
                
                self.log_test_result(
                    f"Performance: '{test_case}' ({response_time:.2f}s)",
                    performance_result['passed'],
                    {'response_time': response_time, 'result': performance_result}
                )
                
            except Exception as e:
                results['failed'] += 1
                results['reliability_metrics']['failed_requests'] += 1
                
                self.log_test_result(
                    f"Performance: '{test_case}'",
                    False,
                    {'error': str(e)}
                )
        
        # Calculate final metrics
        if results['performance_metrics']['response_times']:
            results['performance_metrics']['average_response_time'] = sum(
                results['performance_metrics']['response_times']
            ) / len(results['performance_metrics']['response_times'])
        
        total_requests = results['reliability_metrics']['successful_requests'] + results['reliability_metrics']['failed_requests']
        if total_requests > 0:
            results['reliability_metrics']['error_rate'] = (
                results['reliability_metrics']['failed_requests'] / total_requests
            ) * 100
        
        success_rate = (results['passed'] / results['total_tests']) * 100
        avg_time = results['performance_metrics']['average_response_time']
        error_rate = results['reliability_metrics']['error_rate']
        
        print(f"\n📊 Performance & Reliability Results:")
        print(f"   Success Rate: {results['passed']}/{results['total_tests']} ({success_rate:.1f}%)")
        print(f"   Average Response Time: {avg_time:.2f}s")
        print(f"   Error Rate: {error_rate:.1f}%")
        
        return results
    
    async def test_performance_case(self, test_case: str) -> Dict[str, Any]:
        """Test individual performance case"""
        try:
            # Initialize consultation
            response = requests.post(
                f"{API_BASE}/medical-ai/initialize",
                json={
                    "patient_id": "test-performance",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=10  # Shorter timeout for performance testing
            )
            
            if response.status_code != 200:
                return {'passed': False, 'error': f'Initialization failed: {response.status_code}'}
            
            init_data = response.json()
            consultation_id = init_data.get('consultation_id')
            
            # Send message
            message_response = requests.post(
                f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": test_case,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=10
            )
            
            if message_response.status_code != 200:
                return {'passed': False, 'error': f'Message processing failed: {message_response.status_code}'}
            
            message_data = message_response.json()
            
            # Basic validation - response should exist and be reasonable length
            response_text = message_data.get('response', '')
            has_response = len(response_text) > 20
            
            return {
                'passed': has_response,
                'response_length': len(response_text),
                'consultation_id': consultation_id
            }
            
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    def generate_comprehensive_report(self, core_results: Dict, extended_results: Dict, 
                                    integration_results: Dict, performance_results: Dict) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        
        # Calculate overall statistics
        total_tests = (core_results['total_tests'] + extended_results['total_tests'] + 
                      integration_results['total_tests'] + performance_results['total_tests'])
        total_passed = (core_results['passed'] + extended_results['passed'] + 
                       integration_results['passed'] + performance_results['passed'])
        
        overall_success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
        
        report = {
            'test_summary': {
                'total_tests': total_tests,
                'total_passed': total_passed,
                'total_failed': total_tests - total_passed,
                'overall_success_rate': overall_success_rate,
                'timestamp': datetime.now().isoformat()
            },
            'core_requirements': {
                'success_rate': (core_results['passed'] / core_results['total_tests']) * 100,
                'status': 'PASS' if core_results['passed'] == core_results['total_tests'] else 'FAIL',
                'details': core_results
            },
            'extended_robustness': {
                'success_rate': (extended_results['passed'] / extended_results['total_tests']) * 100,
                'status': 'PASS' if extended_results['passed'] >= extended_results['total_tests'] * 0.8 else 'FAIL',
                'details': extended_results
            },
            'integration_testing': {
                'success_rate': (integration_results['passed'] / integration_results['total_tests']) * 100,
                'status': 'PASS' if integration_results['passed'] >= integration_results['total_tests'] * 0.7 else 'FAIL',
                'details': integration_results
            },
            'performance_reliability': {
                'success_rate': (performance_results['passed'] / performance_results['total_tests']) * 100,
                'average_response_time': performance_results['performance_metrics']['average_response_time'],
                'error_rate': performance_results['reliability_metrics']['error_rate'],
                'status': 'PASS' if (performance_results['passed'] >= performance_results['total_tests'] * 0.8 and 
                                   performance_results['performance_metrics']['average_response_time'] < 10.0) else 'FAIL',
                'details': performance_results
            }
        }
        
        return report
    
    async def run_comprehensive_test_suite(self) -> Dict[str, Any]:
        """Run the complete Step 1.3 test suite"""
        print("🚀 STARTING COMPREHENSIVE STEP 1.3 COLLOQUIAL MEDICAL EXPRESSION HANDLER TESTING")
        print("="*100)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*100)
        
        try:
            # Run all test categories
            core_results = await self.test_core_step_1_3_requirements()
            extended_results = await self.test_extended_robustness()
            integration_results = await self.test_integration_with_steps_1_1_and_1_2()
            performance_results = await self.test_performance_and_reliability()
            
            # Generate comprehensive report
            final_report = self.generate_comprehensive_report(
                core_results, extended_results, integration_results, performance_results
            )
            
            # Print final summary
            self.print_final_summary(final_report)
            
            return final_report
            
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR during testing: {str(e)}")
            return {
                'error': str(e),
                'test_summary': {
                    'total_tests': self.total_tests,
                    'total_passed': self.passed_tests,
                    'total_failed': self.failed_tests,
                    'overall_success_rate': (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
                }
            }
    
    def print_final_summary(self, report: Dict[str, Any]):
        """Print comprehensive final summary"""
        print("\n" + "="*100)
        print("🎯 STEP 1.3 COLLOQUIAL MEDICAL EXPRESSION HANDLER - FINAL TEST RESULTS")
        print("="*100)
        
        summary = report['test_summary']
        print(f"📊 OVERALL RESULTS:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   Passed: {summary['total_passed']}")
        print(f"   Failed: {summary['total_failed']}")
        print(f"   Success Rate: {summary['overall_success_rate']:.1f}%")
        
        print(f"\n🎯 DETAILED CATEGORY RESULTS:")
        
        # Core Requirements
        core = report['core_requirements']
        status_emoji = "✅" if core['status'] == 'PASS' else "❌"
        print(f"   {status_emoji} Core Step 1.3 Requirements: {core['success_rate']:.1f}% ({core['status']})")
        
        # Extended Robustness
        extended = report['extended_robustness']
        status_emoji = "✅" if extended['status'] == 'PASS' else "❌"
        print(f"   {status_emoji} Extended Robustness: {extended['success_rate']:.1f}% ({extended['status']})")
        
        # Integration Testing
        integration = report['integration_testing']
        status_emoji = "✅" if integration['status'] == 'PASS' else "❌"
        print(f"   {status_emoji} Steps 1.1 & 1.2 Integration: {integration['success_rate']:.1f}% ({integration['status']})")
        
        # Performance & Reliability
        performance = report['performance_reliability']
        status_emoji = "✅" if performance['status'] == 'PASS' else "❌"
        print(f"   {status_emoji} Performance & Reliability: {performance['success_rate']:.1f}% ({performance['status']})")
        print(f"      Average Response Time: {performance['average_response_time']:.2f}s")
        print(f"      Error Rate: {performance['error_rate']:.1f}%")
        
        # Overall Assessment
        print(f"\n🏆 OVERALL ASSESSMENT:")
        if summary['overall_success_rate'] >= 90:
            print("   ✅ EXCELLENT - Step 1.3 implementation demonstrates superior colloquial expression handling")
        elif summary['overall_success_rate'] >= 80:
            print("   ✅ GOOD - Step 1.3 implementation shows strong colloquial expression handling with minor issues")
        elif summary['overall_success_rate'] >= 70:
            print("   ⚠️  ACCEPTABLE - Step 1.3 implementation works but needs improvement in some areas")
        else:
            print("   ❌ NEEDS IMPROVEMENT - Step 1.3 implementation requires significant fixes")
        
        # Specific recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if core['status'] != 'PASS':
            print("   🔧 CRITICAL: Fix core Step 1.3 requirements - all 5 examples must work perfectly")
        if extended['status'] != 'PASS':
            print("   🔧 IMPORTANT: Improve extended robustness for comprehensive colloquial coverage")
        if integration['status'] != 'PASS':
            print("   🔧 IMPORTANT: Fix integration with Steps 1.1 & 1.2 for seamless normalization")
        if performance['status'] != 'PASS':
            print("   🔧 OPTIMIZE: Improve performance and reliability metrics")
        
        if all(cat['status'] == 'PASS' for cat in [core, extended, integration, performance]):
            print("   🎉 CONGRATULATIONS: Step 1.3 Colloquial Medical Expression Handler is production-ready!")
        
        print("="*100)


async def main():
    """Main test execution function"""
    tester = Step13ColloquialTester()
    
    try:
        # Run comprehensive test suite
        final_report = await tester.run_comprehensive_test_suite()
        
        # Save results to file for analysis
        with open('/app/step_1_3_test_results.json', 'w') as f:
            json.dump(final_report, f, indent=2, default=str)
        
        print(f"\n📄 Detailed test results saved to: /app/step_1_3_test_results.json")
        
        return final_report
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        return {'error': str(e)}


if __name__ == "__main__":
    # Run the comprehensive test suite
    asyncio.run(main())