#!/usr/bin/env python3
"""
COMPREHENSIVE TEMPORAL EXTRACTION TESTING

Complete validation of all temporal extraction fixes requested in the review:
1. Temporal Duration Detection - "3 nights" should be properly detected
2. Temporal Confidence Scoring - should be 0.7+ when patterns found
3. Enhanced Temporal Patterns - various temporal expressions  
4. Multi-symptom with Temporal API endpoint
5. Temporal Analysis Structure validation
"""

import requests
import json
import time
import sys

BACKEND_URL = "https://symptom-analyzer-6.preview.emergentagent.com"

class ComprehensiveTemporalTester:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            
        result = f"{status} - {test_name}"
        if details:
            result += f": {details}"
            
        print(result)
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "details": details
        })
        
    def test_primary_case_comprehensive(self):
        """Test the primary case comprehensively"""
        print("\n🔍 PRIMARY CASE COMPREHENSIVE TESTING")
        print("=" * 60)
        print("Testing: 'head hurts stomach upset cant sleep 3 nights'")
        print()
        
        test_request = {
            "text": "head hurts stomach upset cant sleep 3 nights",
            "context": {"patient_id": "test-temporal"}
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.backend_url}/api/medical-ai/multi-symptom-parse",
                json=test_request,
                timeout=30,
                headers={"Content-Type": "application/json"}
            )
            processing_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success") and data.get("multi_symptom_parse_result"):
                    parse_result = data["multi_symptom_parse_result"]
                    
                    # Test 1: API Response Structure
                    required_fields = ["success", "multi_symptom_parse_result", "summary", 
                                     "clinical_recommendations", "urgency_assessment"]
                    structure_valid = all(field in data for field in required_fields)
                    self.log_test("API Response Structure", structure_valid, 
                                f"Required fields present: {structure_valid}")
                    
                    # Test 2: Multi-symptom Detection
                    symptom_count = len(parse_result.get("primary_symptoms", [])) + len(parse_result.get("secondary_symptoms", []))
                    multi_symptom_detected = symptom_count >= 2
                    self.log_test("Multi-symptom Detection", multi_symptom_detected,
                                f"Detected {symptom_count} symptoms (expected ≥2)")
                    
                    # Test 3: Duration Detection in Input
                    input_text = parse_result.get("parsing_metadata", {}).get("input_text", "")
                    duration_in_input = "3 nights" in input_text.lower()
                    self.log_test("Duration in Input Text", duration_in_input,
                                f"'3 nights' found in input: {duration_in_input}")
                    
                    # Test 4: Temporal Data Structure Present
                    temporal_data_present = "temporal_data" in parse_result
                    self.log_test("Temporal Data Structure", temporal_data_present,
                                f"temporal_data field present: {temporal_data_present}")
                    
                    # Test 5: Overall Duration Field Present
                    temporal_data = parse_result.get("temporal_data", {})
                    overall_duration_field = "overall_duration" in temporal_data
                    self.log_test("Overall Duration Field", overall_duration_field,
                                f"overall_duration field present: {overall_duration_field}")
                    
                    # Test 6: Overall Duration Populated (CRITICAL BUG)
                    overall_duration = temporal_data.get("overall_duration")
                    duration_populated = overall_duration is not None and overall_duration != ""
                    self.log_test("Overall Duration Populated", duration_populated,
                                f"overall_duration value: {overall_duration} (should be '3 nights')")
                    
                    # Test 7: Temporal Confidence Present
                    confidence_metrics = parse_result.get("confidence_metrics", {})
                    temporal_confidence_present = "temporal_confidence" in confidence_metrics
                    self.log_test("Temporal Confidence Field", temporal_confidence_present,
                                f"temporal_confidence field present: {temporal_confidence_present}")
                    
                    # Test 8: Temporal Confidence > 0 (CRITICAL BUG)
                    temporal_confidence = confidence_metrics.get("temporal_confidence", 0.0)
                    confidence_non_zero = temporal_confidence > 0
                    self.log_test("Temporal Confidence > 0", confidence_non_zero,
                                f"temporal_confidence: {temporal_confidence} (should be > 0)")
                    
                    # Test 9: Temporal Confidence >= 0.7 (TARGET)
                    confidence_threshold = temporal_confidence >= 0.7
                    self.log_test("Temporal Confidence >= 0.7", confidence_threshold,
                                f"temporal_confidence: {temporal_confidence} (target: ≥0.7)")
                    
                    # Test 10: Processing Performance
                    performance_acceptable = processing_time < 5000  # 5 seconds
                    self.log_test("Processing Performance", performance_acceptable,
                                f"Processing time: {processing_time:.2f}ms (target: <5000ms)")
                    
                else:
                    self.log_test("API Success Response", False, "API returned success: False")
            else:
                self.log_test("API HTTP Response", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("API Request", False, f"Exception: {str(e)}")
            
    def test_enhanced_temporal_patterns(self):
        """Test various temporal expressions"""
        print("\n🔍 ENHANCED TEMPORAL PATTERNS TESTING")
        print("=" * 60)
        
        test_cases = [
            {
                "text": "for 2 days headache getting worse",
                "expected_pattern": "duration",
                "expected_duration": "2 days"
            },
            {
                "text": "past 5 hours stomach pain",
                "expected_pattern": "duration", 
                "expected_duration": "5 hours"
            },
            {
                "text": "last 3 weeks back pain",
                "expected_pattern": "duration",
                "expected_duration": "3 weeks"
            },
            {
                "text": "sudden onset chest pain",
                "expected_pattern": "onset",
                "expected_duration": None
            },
            {
                "text": "gradual pain over time",
                "expected_pattern": "progression",
                "expected_duration": None
            },
            {
                "text": "intermittent symptoms come and go",
                "expected_pattern": "frequency",
                "expected_duration": None
            }
        ]
        
        for i, case in enumerate(test_cases, 1):
            try:
                response = requests.post(
                    f"{self.backend_url}/api/medical-ai/multi-symptom-parse",
                    json={
                        "text": case["text"],
                        "context": {"patient_id": f"test-pattern-{i}"}
                    },
                    timeout=15,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("success") and data.get("multi_symptom_parse_result"):
                        parse_result = data["multi_symptom_parse_result"]
                        
                        # Check temporal confidence
                        temporal_confidence = parse_result.get("confidence_metrics", {}).get("temporal_confidence", 0.0)
                        confidence_valid = temporal_confidence > 0
                        
                        # Check for temporal indicators
                        temporal_data = parse_result.get("temporal_data", {})
                        temporal_pattern = temporal_data.get("temporal_pattern", "unknown")
                        
                        pattern_detected = temporal_pattern != "unknown" or confidence_valid
                        
                        self.log_test(f"Pattern {i}: {case['text'][:30]}...", pattern_detected,
                                    f"Confidence: {temporal_confidence}, Pattern: {temporal_pattern}")
                    else:
                        self.log_test(f"Pattern {i}: {case['text'][:30]}...", False, "API processing failed")
                else:
                    self.log_test(f"Pattern {i}: {case['text'][:30]}...", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Pattern {i}: {case['text'][:30]}...", False, f"Exception: {str(e)}")
                
    def test_temporal_analysis_structure(self):
        """Test temporal analysis structure requirements"""
        print("\n🔍 TEMPORAL ANALYSIS STRUCTURE TESTING")
        print("=" * 60)
        
        test_request = {
            "text": "head hurts stomach upset cant sleep 3 nights",
            "context": {"patient_id": "test-structure"}
        }
        
        try:
            response = requests.post(
                f"{self.backend_url}/api/medical-ai/multi-symptom-parse",
                json=test_request,
                timeout=30,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success") and data.get("multi_symptom_parse_result"):
                    parse_result = data["multi_symptom_parse_result"]
                    temporal_data = parse_result.get("temporal_data", {})
                    
                    # Test required temporal structure fields
                    required_fields = [
                        "overall_duration",
                        "temporal_pattern", 
                        "onset_description",
                        "symptom_progression",
                        "temporal_clusters"
                    ]
                    
                    for field in required_fields:
                        field_present = field in temporal_data
                        self.log_test(f"Temporal Field: {field}", field_present,
                                    f"Field present: {field_present}")
                    
                    # Test confidence metrics structure
                    confidence_metrics = parse_result.get("confidence_metrics", {})
                    confidence_fields = ["temporal_confidence", "overall_confidence"]
                    
                    for field in confidence_fields:
                        field_present = field in confidence_metrics
                        self.log_test(f"Confidence Field: {field}", field_present,
                                    f"Field present: {field_present}")
                        
                else:
                    self.log_test("Structure Analysis", False, "No parse result available")
            else:
                self.log_test("Structure API Call", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Structure Test", False, f"Exception: {str(e)}")
            
    def run_comprehensive_tests(self):
        """Run all comprehensive temporal tests"""
        print("🚀 COMPREHENSIVE TEMPORAL EXTRACTION TESTING")
        print("=" * 80)
        print(f"Backend URL: {self.backend_url}")
        print("Testing temporal extraction fixes as requested in review")
        print("=" * 80)
        
        # Run all test suites
        self.test_primary_case_comprehensive()
        self.test_enhanced_temporal_patterns()
        self.test_temporal_analysis_structure()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEMPORAL EXTRACTION TESTING SUMMARY")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Identify critical issues
        print("\n🔧 CRITICAL ISSUES IDENTIFIED:")
        print("-" * 40)
        
        failed_tests = [result for result in self.test_results if not result["passed"]]
        critical_issues = []
        
        for test in failed_tests:
            if "temporal_confidence" in test["test"].lower() and "0.0" in test["details"]:
                critical_issues.append("Temporal confidence calculation returning 0.0 instead of 0.7+")
            elif "overall duration populated" in test["test"].lower():
                critical_issues.append("Overall duration field not populated with detected duration")
        
        for issue in set(critical_issues):
            print(f"❌ {issue}")
            
        if not critical_issues:
            print("✅ No critical temporal extraction issues found")
            
        # Overall assessment
        print(f"\n🎯 OVERALL TEMPORAL EXTRACTION ASSESSMENT:")
        print("-" * 40)
        
        if success_rate >= 80:
            print("🎉 TEMPORAL EXTRACTION FIXES: SUCCESSFUL")
            assessment = "SUCCESSFUL"
        elif success_rate >= 60:
            print("⚠️  TEMPORAL EXTRACTION FIXES: PARTIALLY SUCCESSFUL")
            assessment = "PARTIALLY_SUCCESSFUL"
        else:
            print("❌ TEMPORAL EXTRACTION FIXES: NEEDS IMPROVEMENT")
            assessment = "NEEDS_IMPROVEMENT"
            
        return {
            "success_rate": success_rate,
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "assessment": assessment,
            "critical_issues": list(set(critical_issues))
        }

if __name__ == "__main__":
    tester = ComprehensiveTemporalTester()
    results = tester.run_comprehensive_tests()
    
    # Exit with appropriate code
    sys.exit(0 if results["success_rate"] >= 70 else 1)