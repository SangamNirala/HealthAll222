#!/usr/bin/env python3
"""
Comprehensive Backend Testing Suite for Step 1.3 Colloquial Medical Expression Handler
Integration with Medical AI Service

This test validates the complete Step 1.3 implementation as requested in the review:
1. Core Step 1.3 Requirements (5 required examples)
2. Medical AI Integration with colloquial expressions  
3. Extended Robustness Testing (additional colloquial expressions)
4. Integration with Steps 1.1 & 1.2 (combined normalization)
5. Performance & Reliability testing
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Backend configuration
BACKEND_URL = "https://healthchat-genius.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

class Step13BackendTester:
    """Comprehensive backend tester for Step 1.3 Colloquial Medical Expression Handler"""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_result(self, test_name: str, passed: bool, details: Dict[str, Any]):
        """Log test result"""
        self.test_results.append({
            'test_name': test_name,
            'passed': passed,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
        
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} - {test_name}")
        
        if not passed and 'error' in details:
            print(f"      Error: {details['error']}")
    
    def test_medical_ai_colloquial_integration(self, expression: str, expected_terms: List[str]) -> Tuple[bool, Dict[str, Any]]:
        """Test Medical AI integration with colloquial expressions"""
        try:
            # Initialize consultation
            init_response = requests.post(
                f"{API_BASE}/medical-ai/initialize",
                json={
                    "patient_id": f"test-{int(time.time())}",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if init_response.status_code != 200:
                return False, {'error': f'Initialization failed: {init_response.status_code}'}
            
            init_data = init_response.json()
            consultation_id = init_data.get('consultation_id')
            
            # Send colloquial message
            message_response = requests.post(
                f"{API_BASE}/medical-ai/message",
                json={
                    "consultation_id": consultation_id,
                    "message": expression,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if message_response.status_code != 200:
                return False, {'error': f'Message processing failed: {message_response.status_code}'}
            
            message_data = message_response.json()
            
            # Analyze response for colloquial conversion
            response_text = message_data.get('response', '')
            context = message_data.get('context', {})
            chief_complaint = context.get('chief_complaint', '')
            
            # Check for expected terms in response, context, and chief complaint
            combined_text = (response_text + " " + str(context) + " " + chief_complaint).lower()
            
            found_terms = []
            for term in expected_terms:
                if term.lower() in combined_text:
                    found_terms.append(term)
            
            # Success if at least one expected term is found
            conversion_success = len(found_terms) > 0
            
            # Validate Medical AI response structure
            required_keys = ['response', 'context', 'stage', 'urgency']
            missing_keys = [key for key in required_keys if key not in message_data]
            
            # Check if AI provides appropriate medical response
            has_medical_response = len(response_text) > 50
            urgency_appropriate = message_data.get('urgency', 'none') in ['none', 'routine', 'urgent', 'emergency']
            
            overall_success = conversion_success and not missing_keys and has_medical_response and urgency_appropriate
            
            return overall_success, {
                'conversion_success': conversion_success,
                'found_terms': found_terms,
                'expected_terms': expected_terms,
                'response_length': len(response_text),
                'chief_complaint': chief_complaint,
                'urgency': message_data.get('urgency', 'none'),
                'missing_keys': missing_keys,
                'consultation_id': consultation_id,
                'has_medical_response': has_medical_response
            }
            
        except Exception as e:
            return False, {'error': str(e)}
    
    def test_core_step_1_3_requirements(self) -> Dict[str, Any]:
        """Test all 5 core Step 1.3 required examples"""
        print("\n🎯 TESTING CORE STEP 1.3 REQUIREMENTS (5 Required Examples)")
        print("="*80)
        
        # Core required examples from the review request
        core_examples = [
            ("tummy hurt", ["abdominal pain", "stomach pain", "belly pain"]),
            ("feeling crappy", ["feeling unwell", "feel unwell", "not feeling well", "unwell"]),
            ("can't poop", ["experiencing constipation", "constipation", "bowel movement"]),
            ("throwing up", ["vomiting", "nausea", "sick"]),
            ("dizzy spells", ["episodes of dizziness", "dizziness", "dizzy"])
        ]
        
        results = {
            'total_tests': len(core_examples),
            'passed': 0,
            'failed': 0,
            'examples': []
        }
        
        for original, expected_terms in core_examples:
            success, details = self.test_medical_ai_colloquial_integration(original, expected_terms)
            
            example_result = {
                'original': original,
                'expected_terms': expected_terms,
                'success': success,
                'details': details
            }
            
            results['examples'].append(example_result)
            
            if success:
                results['passed'] += 1
            else:
                results['failed'] += 1
            
            found_terms = details.get('found_terms', [])
            self.log_result(
                f"Core Example: '{original}' → Found: {found_terms}",
                success,
                details
            )
        
        success_rate = (results['passed'] / results['total_tests']) * 100
        print(f"\n📊 Core Step 1.3 Results: {results['passed']}/{results['total_tests']} ({success_rate:.1f}%)")
        
        return results
    
    def test_extended_robustness(self) -> Dict[str, Any]:
        """Test extended robustness with additional colloquial expressions"""
        print("\n🚀 TESTING EXTENDED ROBUSTNESS (Additional Colloquial Expressions)")
        print("="*80)
        
        # Extended robustness test cases from review request
        extended_examples = [
            # Digestive variations
            ("belly ache", ["abdominal pain", "stomach pain", "belly pain"]),
            ("gut pain really bad", ["severe abdominal pain", "abdominal pain", "gut pain"]),
            
            # Bowel movements
            ("cant poop for days", ["experiencing constipation", "constipation"]),
            ("backed up", ["experiencing constipation", "constipation"]),
            
            # Feeling unwell
            ("feel awful", ["feel unwell", "feeling unwell", "awful"]),
            ("under the weather", ["feeling unwell", "feel unwell", "weather"]),
            
            # Breathing
            ("can't breathe", ["difficulty breathing", "breathing", "shortness of breath"]),
            ("short of breath", ["experiencing shortness of breath", "shortness of breath", "breathing"]),
            
            # Fatigue
            ("wiped out", ["extremely fatigued", "fatigue", "tired", "exhausted"]),
            ("dead tired", ["extremely fatigued", "fatigue", "tired"]),
            
            # Compound expressions
            ("tummy hurt and throwing up", ["abdominal pain", "vomiting", "nausea"]),
        ]
        
        results = {
            'total_tests': len(extended_examples),
            'passed': 0,
            'failed': 0,
            'examples': []
        }
        
        for original, expected_terms in extended_examples:
            success, details = self.test_medical_ai_colloquial_integration(original, expected_terms)
            
            example_result = {
                'original': original,
                'expected_terms': expected_terms,
                'success': success,
                'details': details
            }
            
            results['examples'].append(example_result)
            
            if success:
                results['passed'] += 1
            else:
                results['failed'] += 1
            
            found_terms = details.get('found_terms', [])
            self.log_result(
                f"Extended: '{original}' → Found: {found_terms}",
                success,
                details
            )
        
        success_rate = (results['passed'] / results['total_tests']) * 100
        print(f"\n📊 Extended Robustness Results: {results['passed']}/{results['total_tests']} ({success_rate:.1f}%)")
        
        return results
    
    def test_integration_with_steps_1_1_and_1_2(self) -> Dict[str, Any]:
        """Test integration with Steps 1.1 & 1.2 (combined normalization)"""
        print("\n🔗 TESTING INTEGRATION WITH STEPS 1.1 & 1.2 (Combined Normalization)")
        print("="*80)
        
        # Combined test cases from review request
        combined_examples = [
            # Grammar + colloquial
            ("i having tummy hurt 2 days", ["I have been having", "abdominal pain", "2 days", "fever"]),
            
            # Spelling + colloquial  
            ("haedache and dizzy spells", ["headache", "episodes of dizziness", "dizziness"]),
            
            # Complex combination
            ("me belly really hurt when breath", ["my", "abdominal pain", "when I breathe", "breathing"]),
        ]
        
        results = {
            'total_tests': len(combined_examples),
            'passed': 0,
            'failed': 0,
            'examples': []
        }
        
        for original, expected_elements in combined_examples:
            success, details = self.test_medical_ai_colloquial_integration(original, expected_elements)
            
            example_result = {
                'original': original,
                'expected_elements': expected_elements,
                'success': success,
                'details': details
            }
            
            results['examples'].append(example_result)
            
            if success:
                results['passed'] += 1
            else:
                results['failed'] += 1
            
            found_terms = details.get('found_terms', [])
            self.log_result(
                f"Combined: '{original}' → Found: {found_terms}",
                success,
                details
            )
        
        success_rate = (results['passed'] / results['total_tests']) * 100
        print(f"\n📊 Combined Integration Results: {results['passed']}/{results['total_tests']} ({success_rate:.1f}%)")
        
        return results
    
    def test_performance_and_reliability(self) -> Dict[str, Any]:
        """Test performance and reliability of the system"""
        print("\n⚡ TESTING PERFORMANCE & RELIABILITY")
        print("="*80)
        
        # Performance test cases
        test_cases = [
            ("tummy hurt", ["abdominal pain"]),
            ("feeling crappy", ["feeling unwell"]),
            ("dizzy spells", ["dizziness"]),
            ("wiped out", ["fatigue"]),
            ("belly ache", ["abdominal pain"])
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
        
        for test_case, expected_terms in test_cases:
            try:
                start_time = time.time()
                
                success, details = self.test_medical_ai_colloquial_integration(test_case, expected_terms)
                
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
                
                if success:
                    results['passed'] += 1
                    results['reliability_metrics']['successful_requests'] += 1
                else:
                    results['failed'] += 1
                    results['reliability_metrics']['failed_requests'] += 1
                
                self.log_result(
                    f"Performance: '{test_case}' ({response_time:.2f}s)",
                    success,
                    {'response_time': response_time, 'details': details}
                )
                
            except Exception as e:
                results['failed'] += 1
                results['reliability_metrics']['failed_requests'] += 1
                
                self.log_result(
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
    
    def run_comprehensive_test_suite(self) -> Dict[str, Any]:
        """Run the complete Step 1.3 test suite"""
        print("🚀 COMPREHENSIVE STEP 1.3 COLLOQUIAL MEDICAL EXPRESSION HANDLER TESTING")
        print("="*100)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*100)
        
        try:
            # Run all test categories
            core_results = self.test_core_step_1_3_requirements()
            extended_results = self.test_extended_robustness()
            integration_results = self.test_integration_with_steps_1_1_and_1_2()
            performance_results = self.test_performance_and_reliability()
            
            # Generate comprehensive report
            final_report = self.generate_final_report(
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
                    'total_failed': self.total_tests - self.passed_tests,
                    'overall_success_rate': (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
                }
            }
    
    def generate_final_report(self, core_results: Dict, extended_results: Dict, 
                            integration_results: Dict, performance_results: Dict) -> Dict[str, Any]:
        """Generate comprehensive final report"""
        
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
                'status': 'PASS' if core_results['passed'] >= 4 else 'PARTIAL' if core_results['passed'] >= 2 else 'FAIL',
                'details': core_results
            },
            'extended_robustness': {
                'success_rate': (extended_results['passed'] / extended_results['total_tests']) * 100,
                'status': 'PASS' if extended_results['passed'] >= extended_results['total_tests'] * 0.7 else 'PARTIAL' if extended_results['passed'] >= extended_results['total_tests'] * 0.4 else 'FAIL',
                'details': extended_results
            },
            'integration_testing': {
                'success_rate': (integration_results['passed'] / integration_results['total_tests']) * 100,
                'status': 'PASS' if integration_results['passed'] >= integration_results['total_tests'] * 0.7 else 'PARTIAL' if integration_results['passed'] >= 1 else 'FAIL',
                'details': integration_results
            },
            'performance_reliability': {
                'success_rate': (performance_results['passed'] / performance_results['total_tests']) * 100,
                'average_response_time': performance_results['performance_metrics']['average_response_time'],
                'error_rate': performance_results['reliability_metrics']['error_rate'],
                'status': 'PASS' if (performance_results['passed'] >= performance_results['total_tests'] * 0.6 and 
                                   performance_results['performance_metrics']['average_response_time'] < 10.0) else 'FAIL',
                'details': performance_results
            }
        }
        
        return report
    
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
        status_emoji = "✅" if core['status'] == 'PASS' else "🔶" if core['status'] == 'PARTIAL' else "❌"
        print(f"   {status_emoji} Core Step 1.3 Requirements: {core['success_rate']:.1f}% ({core['status']})")
        
        # Extended Robustness
        extended = report['extended_robustness']
        status_emoji = "✅" if extended['status'] == 'PASS' else "🔶" if extended['status'] == 'PARTIAL' else "❌"
        print(f"   {status_emoji} Extended Robustness: {extended['success_rate']:.1f}% ({extended['status']})")
        
        # Integration Testing
        integration = report['integration_testing']
        status_emoji = "✅" if integration['status'] == 'PASS' else "🔶" if integration['status'] == 'PARTIAL' else "❌"
        print(f"   {status_emoji} Steps 1.1 & 1.2 Integration: {integration['success_rate']:.1f}% ({integration['status']})")
        
        # Performance & Reliability
        performance = report['performance_reliability']
        status_emoji = "✅" if performance['status'] == 'PASS' else "❌"
        print(f"   {status_emoji} Performance & Reliability: {performance['success_rate']:.1f}% ({performance['status']})")
        print(f"      Average Response Time: {performance['average_response_time']:.2f}s")
        print(f"      Error Rate: {performance['error_rate']:.1f}%")
        
        # Overall Assessment
        print(f"\n🏆 OVERALL ASSESSMENT:")
        if summary['overall_success_rate'] >= 80:
            print("   ✅ GOOD - Step 1.3 implementation shows strong colloquial expression handling")
        elif summary['overall_success_rate'] >= 60:
            print("   🔶 PARTIAL - Step 1.3 implementation works for some expressions but needs improvement")
        else:
            print("   ❌ NEEDS IMPROVEMENT - Step 1.3 implementation requires significant fixes")
        
        print("="*100)


def main():
    """Main test execution function"""
    tester = Step13BackendTester()
    
    try:
        # Run comprehensive test suite
        final_report = tester.run_comprehensive_test_suite()
        
        # Save results to file for analysis
        with open('/app/step_1_3_backend_test_results.json', 'w') as f:
            json.dump(final_report, f, indent=2, default=str)
        
        print(f"\n📄 Detailed test results saved to: /app/step_1_3_backend_test_results.json")
        
        return final_report
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        return {'error': str(e)}


if __name__ == "__main__":
    # Run the comprehensive test suite
    main()