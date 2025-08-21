#!/usr/bin/env python3
"""
🎯 ENHANCED INCOMPLETENESS DETECTION SYSTEM - PERFORMANCE VALIDATION
===================================================================

Final performance validation for the ultra-optimized Enhanced Incompleteness Detection System.
Testing for <50ms processing time target while maintaining 100% functionality.
"""

import subprocess
import json
import time
import statistics
from typing import Dict, Any, List

class IncompletenessPerformanceTester:
    def __init__(self):
        self.backend_url = "https://mediq-2.preview.emergentagent.com/api"
        self.test_results = []
        self.performance_metrics = []
        
        print("🎯 ENHANCED INCOMPLETENESS DETECTION SYSTEM - PERFORMANCE VALIDATION")
        print("=" * 70)
        print(f"Backend URL: {self.backend_url}")
        print(f"Target: <50ms processing time")
        print()

    def test_endpoint_with_curl(self, test_name: str, patient_message: str) -> Dict[str, Any]:
        """Test endpoint using curl for better reliability"""
        
        print(f"🧪 Testing: {test_name}")
        print(f"Input: '{patient_message}'")
        
        # Prepare curl command
        payload = {
            "patient_message": patient_message,
            "conversation_context": {
                "previous_messages": [],
                "current_stage": "chief_complaint",
                "patient_id": "test-patient-performance"
            },
            "analysis_dimensions": [
                "Linguistic",
                "Medical Reasoning", 
                "Psychological",
                "Cultural",
                "Temporal"
            ],
            "patient_type": "balanced_patient"
        }
        
        # Measure processing time
        start_time = time.time()
        
        try:
            # Use curl for the request
            curl_cmd = [
                'curl', '-s', '-X', 'POST',
                f'{self.backend_url}/medical-ai/incompleteness-detection/analyze',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps(payload),
                '-w', '%{http_code}|%{time_total}'
            ]
            
            result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=10)
            
            end_time = time.time()
            processing_time_ms = (end_time - start_time) * 1000
            
            if result.returncode == 0:
                # Split response and status
                output_parts = result.stdout.rsplit('|', 1)
                if len(output_parts) == 2:
                    response_text, curl_info = output_parts
                    status_code, curl_time = curl_info.split('|') if '|' in curl_info else (curl_info, '0')
                    curl_time_ms = float(curl_time) * 1000
                else:
                    response_text = result.stdout
                    status_code = "200"
                    curl_time_ms = processing_time_ms
                
                print(f"⏱️  Processing Time: {processing_time_ms:.2f}ms")
                print(f"🌐 Network Time: {curl_time_ms:.2f}ms")
                
                if status_code == "200":
                    try:
                        data = json.loads(response_text)
                        
                        # Extract key metrics
                        incompleteness_score = data.get('incompleteness_score', 0)
                        priority_gaps = data.get('priority_gaps', [])
                        immediate_follow_ups = data.get('immediate_follow_ups', [])
                        analysis_confidence = data.get('analysis_confidence', 0)
                        algorithm_version = data.get('algorithm_version', 'unknown')
                        reported_processing_time = data.get('processing_time_ms', 0)
                        
                        print(f"✅ Status: SUCCESS")
                        print(f"📊 Incompleteness Score: {incompleteness_score:.3f}")
                        print(f"🔍 Priority Gaps: {len(priority_gaps)}")
                        print(f"❓ Follow-up Questions: {len(immediate_follow_ups)}")
                        print(f"🎯 Confidence: {analysis_confidence}")
                        print(f"🔧 Algorithm: {algorithm_version}")
                        print(f"⚡ Reported Processing Time: {reported_processing_time:.2f}ms")
                        
                        # Performance validation
                        performance_target_met = reported_processing_time < 50
                        print(f"🎯 <50ms Target: {'✅ PASS' if performance_target_met else '❌ FAIL'}")
                        
                        # Functionality validation
                        has_gaps = len(priority_gaps) > 0
                        has_follow_ups = len(immediate_follow_ups) > 0
                        has_confidence = analysis_confidence > 0
                        
                        functionality_score = sum([has_gaps, has_follow_ups, has_confidence]) / 3
                        print(f"🔧 Functionality Score: {functionality_score:.1%}")
                        
                        # Store results
                        test_result = {
                            'test_name': test_name,
                            'patient_message': patient_message,
                            'processing_time_ms': processing_time_ms,
                            'network_time_ms': curl_time_ms,
                            'reported_processing_time_ms': reported_processing_time,
                            'performance_target_met': performance_target_met,
                            'incompleteness_score': incompleteness_score,
                            'priority_gaps_count': len(priority_gaps),
                            'follow_ups_count': len(immediate_follow_ups),
                            'analysis_confidence': analysis_confidence,
                            'algorithm_version': algorithm_version,
                            'functionality_score': functionality_score,
                            'success': True,
                            'response_data': data
                        }
                        
                        self.test_results.append(test_result)
                        self.performance_metrics.append(reported_processing_time)
                        
                        return test_result
                        
                    except json.JSONDecodeError as e:
                        print(f"❌ Status: JSON DECODE ERROR")
                        print(f"Error: {str(e)}")
                        print(f"Response: {response_text[:200]}...")
                        
                else:
                    print(f"❌ Status: HTTP {status_code}")
                    print(f"Response: {response_text[:200]}...")
                    
            else:
                print(f"❌ Status: CURL ERROR")
                print(f"Error: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Status: EXCEPTION")
            print(f"Error: {str(e)}")
        
        # Return failed result
        test_result = {
            'test_name': test_name,
            'patient_message': patient_message,
            'success': False,
            'error': 'Request failed'
        }
        
        self.test_results.append(test_result)
        return test_result

    def test_system_performance_endpoint(self):
        """Test the system performance endpoint"""
        print("🔧 Testing System Performance Endpoint")
        
        try:
            curl_cmd = [
                'curl', '-s',
                f'{self.backend_url}/medical-ai/incompleteness-detection/system-performance',
                '-w', '%{http_code}'
            ]
            
            result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                output_parts = result.stdout.rsplit('200', 1)
                if len(output_parts) == 2:
                    response_text = output_parts[0]
                    status_code = "200"
                else:
                    response_text = result.stdout
                    status_code = "unknown"
                
                if status_code == "200":
                    try:
                        data = json.loads(response_text)
                        print(f"✅ System Performance Endpoint: WORKING")
                        print(f"📊 System Status: {data.get('system_status', 'unknown')}")
                        print(f"🔧 Algorithm Version: {data.get('algorithm_version', 'unknown')}")
                        print(f"🎯 Analysis Dimensions: {len(data.get('analysis_dimensions', []))}")
                        print(f"👥 Patient Types: {len(data.get('patient_types', []))}")
                        return True
                    except json.JSONDecodeError:
                        print(f"❌ System Performance Endpoint: JSON ERROR")
                        return False
                else:
                    print(f"❌ System Performance Endpoint: HTTP {status_code}")
                    return False
            else:
                print(f"❌ System Performance Endpoint: CURL ERROR")
                return False
                
        except Exception as e:
            print(f"❌ System Performance Endpoint: EXCEPTION - {str(e)}")
            return False

    def run_performance_tests(self):
        """Run the specific test scenarios from the review request"""
        
        print("\n🚀 RUNNING PERFORMANCE VALIDATION TESTS")
        print("=" * 50)
        
        # Test Scenario 1: Simple vague symptom
        self.test_endpoint_with_curl(
            "Simple Vague Symptom",
            "I have chest pain"
        )
        
        print()
        
        # Test Scenario 2: Complex symptom
        self.test_endpoint_with_curl(
            "Complex Symptom",
            "I've been having headaches and feeling tired lately"
        )
        
        print()
        
        # Test Scenario 3: Anxiety-related
        self.test_endpoint_with_curl(
            "Anxiety-Related Symptom",
            "I'm worried about this chest discomfort I've been having"
        )
        
        print()
        
        # Additional Test Scenario 4: Very vague
        self.test_endpoint_with_curl(
            "Very Vague Symptom",
            "I'm not feeling well"
        )
        
        print()
        
        # Additional Test Scenario 5: Temporal vagueness
        self.test_endpoint_with_curl(
            "Temporal Vagueness",
            "My stomach has been bothering me recently"
        )

    def analyze_results(self):
        """Analyze and report results"""
        
        print(f"\n📊 PERFORMANCE ANALYSIS RESULTS")
        print("=" * 50)
        
        successful_tests = [t for t in self.test_results if t.get('success', False)]
        
        if not successful_tests:
            print("❌ No successful tests to analyze")
            return
        
        if not self.performance_metrics:
            print("❌ No performance data collected")
            return
        
        # Calculate statistics
        avg_time = statistics.mean(self.performance_metrics)
        min_time = min(self.performance_metrics)
        max_time = max(self.performance_metrics)
        median_time = statistics.median(self.performance_metrics)
        
        # Performance target analysis
        target_met_count = sum(1 for t in self.performance_metrics if t < 50)
        target_met_percentage = (target_met_count / len(self.performance_metrics)) * 100
        
        print(f"⏱️  Average Processing Time: {avg_time:.2f}ms")
        print(f"⚡ Fastest Processing Time: {min_time:.2f}ms")
        print(f"🐌 Slowest Processing Time: {max_time:.2f}ms")
        print(f"📊 Median Processing Time: {median_time:.2f}ms")
        print(f"🎯 <50ms Target Met: {target_met_count}/{len(self.performance_metrics)} ({target_met_percentage:.1f}%)")
        
        # Overall performance assessment
        if avg_time < 50:
            print(f"✅ PERFORMANCE TARGET ACHIEVED: Average {avg_time:.2f}ms < 50ms")
        else:
            print(f"❌ PERFORMANCE TARGET MISSED: Average {avg_time:.2f}ms > 50ms")
            print(f"   Gap: {avg_time - 50:.2f}ms over target")
        
        # Functionality metrics
        avg_incompleteness_score = statistics.mean([t['incompleteness_score'] for t in successful_tests])
        avg_gaps_count = statistics.mean([t['priority_gaps_count'] for t in successful_tests])
        avg_follow_ups_count = statistics.mean([t['follow_ups_count'] for t in successful_tests])
        avg_confidence = statistics.mean([t['analysis_confidence'] for t in successful_tests])
        avg_functionality_score = statistics.mean([t['functionality_score'] for t in successful_tests])
        
        print(f"\n🔧 FUNCTIONALITY ANALYSIS:")
        print(f"📊 Average Incompleteness Score: {avg_incompleteness_score:.3f}")
        print(f"🔍 Average Priority Gaps: {avg_gaps_count:.1f}")
        print(f"❓ Average Follow-up Questions: {avg_follow_ups_count:.1f}")
        print(f"🎯 Average Analysis Confidence: {avg_confidence:.3f}")
        print(f"🔧 Average Functionality Score: {avg_functionality_score:.1%}")
        
        # Check if core functionality is working
        gaps_working = avg_gaps_count > 0
        follow_ups_working = avg_follow_ups_count > 0
        confidence_working = avg_confidence > 0
        
        print(f"\n🔧 CORE FUNCTIONALITY STATUS:")
        print(f"   Gap Detection: {'✅ WORKING' if gaps_working else '❌ NOT WORKING'}")
        print(f"   Follow-up Generation: {'✅ WORKING' if follow_ups_working else '❌ NOT WORKING'}")
        print(f"   Confidence Scoring: {'✅ WORKING' if confidence_working else '❌ NOT WORKING'}")

    def generate_final_report(self):
        """Generate final validation report"""
        
        print(f"\n🎉 FINAL PERFORMANCE VALIDATION REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = len([t for t in self.test_results if t.get('success', False)])
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Successful Tests: {successful_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        if self.performance_metrics:
            avg_time = statistics.mean(self.performance_metrics)
            target_met_count = sum(1 for t in self.performance_metrics if t < 50)
            target_met_percentage = (target_met_count / len(self.performance_metrics)) * 100
            
            print(f"\n⏱️  PERFORMANCE SUMMARY:")
            print(f"   Average Processing Time: {avg_time:.2f}ms")
            print(f"   Target <50ms Achievement: {target_met_percentage:.1f}%")
            
            if avg_time < 50 and target_met_percentage >= 80:
                print(f"✅ PERFORMANCE TARGET ACHIEVED")
            else:
                print(f"❌ PERFORMANCE TARGET NOT FULLY ACHIEVED")
        
        print(f"\n🎯 CRITICAL SUCCESS CRITERIA STATUS:")
        
        # Performance criteria
        if self.performance_metrics:
            avg_time = statistics.mean(self.performance_metrics)
            performance_ok = avg_time < 50
            print(f"   Processing time <50ms: {'✅ PASS' if performance_ok else '❌ FAIL'} ({avg_time:.2f}ms avg)")
        else:
            print(f"   Processing time <50ms: ❌ NO DATA")
        
        # Functionality criteria
        successful_tests = [t for t in self.test_results if t.get('success', False)]
        if successful_tests:
            avg_functionality = statistics.mean([t['functionality_score'] for t in successful_tests])
            functionality_ok = avg_functionality > 0.5
            print(f"   Core functionality intact: {'✅ PASS' if functionality_ok else '❌ FAIL'} ({avg_functionality:.1%})")
        else:
            print(f"   Core functionality intact: ❌ NO DATA")
        
        # Response structure criteria
        structure_ok = successful_tests and all('response_data' in t for t in successful_tests)
        print(f"   Response structure complete: {'✅ PASS' if structure_ok else '❌ FAIL'}")
        
        print(f"\n🚀 REVOLUTIONARY PERFORMANCE BREAKTHROUGH:")
        if self.performance_metrics:
            avg_time = statistics.mean(self.performance_metrics)
            improvement_factor = 26900 / avg_time if avg_time > 0 else 0
            print(f"   Original: 26.9 seconds (26,900ms)")
            print(f"   Current: {avg_time:.2f}ms")
            print(f"   Improvement: {improvement_factor:.0f}x faster")
        
        return {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'success_rate': success_rate,
            'average_processing_time': statistics.mean(self.performance_metrics) if self.performance_metrics else None,
            'performance_target_met': statistics.mean(self.performance_metrics) < 50 if self.performance_metrics else False
        }

def main():
    """Main testing function"""
    
    tester = IncompletenessPerformanceTester()
    
    # Test system performance endpoint first
    tester.test_system_performance_endpoint()
    
    # Run the main performance validation tests
    tester.run_performance_tests()
    
    # Analyze results
    tester.analyze_results()
    
    # Generate final report
    final_results = tester.generate_final_report()
    
    print(f"\n🎉 TESTING COMPLETE!")
    print("=" * 40)
    
    return final_results

if __name__ == "__main__":
    main()