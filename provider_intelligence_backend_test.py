#!/usr/bin/env python3
"""
COMPREHENSIVE PROVIDER INTELLIGENCE SYSTEM PHASE C.3 TESTING

🚀 MISSION: Test all newly implemented Provider Intelligence System components including 
Provider Intelligence, Clinical Documentation AI, and Workflow Optimization endpoints.

TESTING SCOPE - 12 NEW API ENDPOINTS:
1. Provider Intelligence System Endpoints (4 endpoints)
2. Clinical Documentation AI Endpoints (4 endpoints) 
3. Workflow Optimization Endpoints (3 endpoints)

Author: Testing Agent
Date: 2025-01-17
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

# Get backend URL from frontend environment
BACKEND_URL = "http://localhost:8001"
try:
    with open('/app/frontend/.env', 'r') as f:
        for line in f:
            if line.startswith('REACT_APP_BACKEND_URL='):
                BACKEND_URL = line.split('=')[1].strip()
                break
except:
    pass

BASE_URL = f"{BACKEND_URL}/api"

class ProviderIntelligenceSystemTester:
    """Comprehensive tester for Provider Intelligence System Phase C.3"""
    
    def __init__(self):
        self.session = None
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_test_result(self, test_name: str, success: bool, details: str, response_time: float = 0):
        """Log test result with details"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test_name": test_name,
            "status": status,
            "success": success,
            "details": details,
            "response_time_ms": response_time,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        self.total_tests += 1
        if success:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
        print(f"{status} {test_name}: {details}")
    
    async def test_endpoint(self, endpoint: str, method: str, data: Dict[str, Any], test_name: str) -> Dict[str, Any]:
        """Generic endpoint testing method"""
        try:
            start_time = time.time()
            url = f"{BASE_URL}{endpoint}"
            
            if method.upper() == "POST":
                async with self.session.post(url, json=data) as response:
                    response_time = (time.time() - start_time) * 1000
                    response_data = await response.json()
                    
                    if response.status == 200:
                        self.log_test_result(test_name, True, 
                                           f"Status: {response.status}, Response time: {response_time:.2f}ms", 
                                           response_time)
                        return response_data
                    else:
                        self.log_test_result(test_name, False, 
                                           f"Status: {response.status}, Error: {response_data.get('detail', 'Unknown error')}")
                        return response_data
            elif method.upper() == "GET":
                async with self.session.get(url) as response:
                    response_time = (time.time() - start_time) * 1000
                    response_data = await response.json()
                    
                    if response.status == 200:
                        self.log_test_result(test_name, True, 
                                           f"Status: {response.status}, Response time: {response_time:.2f}ms", 
                                           response_time)
                        return response_data
                    else:
                        self.log_test_result(test_name, False, 
                                           f"Status: {response.status}, Error: {response_data.get('detail', 'Unknown error')}")
                        return response_data
                        
        except Exception as e:
            self.log_test_result(test_name, False, f"Exception: {str(e)}")
            return {"error": str(e)}

    # ===========================
    # PROVIDER INTELLIGENCE SYSTEM TESTS (4 ENDPOINTS)
    # ===========================
    
    async def test_create_provider_profile(self):
        """Test POST /api/medical-ai/provider-intelligence/create-profile"""
        test_data = {
            "provider_data": {
                "provider_id": "dr-emergency-001",
                "name": "Dr. Sarah Johnson",
                "specialty": "EMERGENCY_MEDICINE",
                "years_experience": 5,
                "education": {
                    "medical_school": "Johns Hopkins University",
                    "residency": "Emergency Medicine - Mayo Clinic",
                    "board_certifications": ["Emergency Medicine", "Advanced Cardiac Life Support"]
                },
                "current_position": {
                    "hospital": "Metropolitan General Hospital",
                    "department": "Emergency Department",
                    "role": "Attending Physician"
                },
                "clinical_interests": ["Trauma Care", "Cardiac Emergencies", "Toxicology"],
                "patient_demographics": ["Adult", "Pediatric"],
                "languages": ["English", "Spanish"]
            },
            "performance_history": [
                {
                    "date": "2024-12-01",
                    "metrics": {
                        "patient_satisfaction": 4.8,
                        "diagnostic_accuracy": 0.92,
                        "treatment_efficiency": 0.88,
                        "cases_handled": 45
                    }
                },
                {
                    "date": "2024-11-01", 
                    "metrics": {
                        "patient_satisfaction": 4.7,
                        "diagnostic_accuracy": 0.89,
                        "treatment_efficiency": 0.85,
                        "cases_handled": 42
                    }
                }
            ]
        }
        
        response = await self.test_endpoint(
            "/medical-ai/provider-intelligence/create-profile",
            "POST",
            test_data,
            "Provider Profile Creation"
        )
        
        # Validate response structure
        if response and "success" in response and response["success"]:
            if "provider_profile" in response and "processing_time_ms" in response:
                self.log_test_result("Provider Profile Response Structure", True, 
                                   "All required fields present in response")
            else:
                self.log_test_result("Provider Profile Response Structure", False, 
                                   "Missing required fields in response")
        
        return response
    
    async def test_clinical_coaching(self):
        """Test POST /api/medical-ai/provider-intelligence/clinical-coaching"""
        test_data = {
            "provider_id": "dr-emergency-001",
            "recent_cases": [
                {
                    "case_id": "case-001",
                    "patient_age": 45,
                    "chief_complaint": "Chest pain",
                    "diagnosis": "Acute coronary syndrome",
                    "treatment_outcome": "Successful PCI, patient stable",
                    "decision_points": [
                        "ECG interpretation",
                        "Troponin level assessment", 
                        "Catheterization timing"
                    ],
                    "time_to_diagnosis": 25,
                    "complications": None
                },
                {
                    "case_id": "case-002",
                    "patient_age": 28,
                    "chief_complaint": "Shortness of breath",
                    "diagnosis": "Pulmonary embolism",
                    "treatment_outcome": "Anticoagulation started, patient improved",
                    "decision_points": [
                        "D-dimer interpretation",
                        "CT-PA ordering",
                        "Risk stratification"
                    ],
                    "time_to_diagnosis": 45,
                    "complications": None
                }
            ],
            "focus_areas": [
                "diagnostic_accuracy",
                "workflow_efficiency",
                "patient_communication"
            ]
        }
        
        response = await self.test_endpoint(
            "/medical-ai/provider-intelligence/clinical-coaching",
            "POST", 
            test_data,
            "Clinical Coaching Recommendations"
        )
        
        # Validate coaching recommendations
        if response and "success" in response and response["success"]:
            if "coaching_recommendations" in response and "total_recommendations" in response:
                recommendations = response["coaching_recommendations"]
                if isinstance(recommendations, list) and len(recommendations) > 0:
                    self.log_test_result("Coaching Recommendations Content", True,
                                       f"Generated {len(recommendations)} coaching recommendations")
                else:
                    self.log_test_result("Coaching Recommendations Content", False,
                                       "No coaching recommendations generated")
            else:
                self.log_test_result("Coaching Response Structure", False,
                                   "Missing coaching recommendations in response")
        
        return response
    
    async def test_provider_analytics(self):
        """Test POST /api/medical-ai/provider-intelligence/analytics"""
        test_data = {
            "provider_id": "dr-emergency-001",
            "analysis_period_days": 30,
            "include_benchmarking": True
        }
        
        response = await self.test_endpoint(
            "/medical-ai/provider-intelligence/analytics",
            "POST",
            test_data,
            "Provider Analytics Generation"
        )
        
        # Validate analytics structure
        if response and "success" in response and response["success"]:
            if "analytics" in response:
                analytics = response["analytics"]
                expected_fields = ["performance_metrics", "benchmarking_data", "trends_analysis"]
                missing_fields = [field for field in expected_fields if field not in str(analytics)]
                
                if not missing_fields:
                    self.log_test_result("Analytics Content Validation", True,
                                       "All expected analytics fields present")
                else:
                    self.log_test_result("Analytics Content Validation", False,
                                       f"Missing fields: {missing_fields}")
            else:
                self.log_test_result("Analytics Response Structure", False,
                                   "Missing analytics data in response")
        
        return response
    
    async def test_cognitive_load_assessment(self):
        """Test POST /api/medical-ai/provider-intelligence/cognitive-load"""
        test_data = {
            "provider_id": "dr-emergency-001",
            "current_workload": {
                "active_patients": 8,
                "pending_consultations": 3,
                "urgent_cases": 2,
                "administrative_tasks": 5,
                "shift_hours_remaining": 4.5,
                "interruptions_last_hour": 12,
                "multitasking_level": "high"
            },
            "recent_decisions": [
                {
                    "decision_id": "dec-001",
                    "timestamp": "2025-01-17T10:30:00Z",
                    "decision_type": "diagnostic",
                    "complexity": "high",
                    "time_taken_minutes": 8,
                    "confidence_level": 0.85,
                    "outcome": "correct_diagnosis"
                },
                {
                    "decision_id": "dec-002", 
                    "timestamp": "2025-01-17T11:15:00Z",
                    "decision_type": "treatment",
                    "complexity": "medium",
                    "time_taken_minutes": 5,
                    "confidence_level": 0.92,
                    "outcome": "effective_treatment"
                },
                {
                    "decision_id": "dec-003",
                    "timestamp": "2025-01-17T11:45:00Z", 
                    "decision_type": "triage",
                    "complexity": "low",
                    "time_taken_minutes": 2,
                    "confidence_level": 0.95,
                    "outcome": "appropriate_priority"
                }
            ]
        }
        
        response = await self.test_endpoint(
            "/medical-ai/provider-intelligence/cognitive-load",
            "POST",
            test_data,
            "Cognitive Load Assessment"
        )
        
        # Validate cognitive assessment
        if response and "success" in response and response["success"]:
            if "cognitive_assessment" in response:
                assessment = response["cognitive_assessment"]
                if isinstance(assessment, dict):
                    self.log_test_result("Cognitive Assessment Content", True,
                                       "Cognitive load assessment data received")
                else:
                    self.log_test_result("Cognitive Assessment Content", False,
                                       "Invalid cognitive assessment format")
            else:
                self.log_test_result("Cognitive Assessment Structure", False,
                                   "Missing cognitive assessment in response")
        
        return response

    # ===========================
    # CLINICAL DOCUMENTATION AI TESTS (4 ENDPOINTS)
    # ===========================
    
    async def test_generate_soap_note(self):
        """Test POST /api/medical-ai/clinical-documentation/generate-soap"""
        test_data = {
            "provider_id": "dr-emergency-001",
            "patient_id": "patient-12345",
            "conversation_data": {
                "chief_complaint": "Chest pain for 2 hours",
                "history_present_illness": "45-year-old male presents with acute onset substernal chest pain that started 2 hours ago while at rest. Pain is described as crushing, 8/10 severity, radiating to left arm and jaw. Associated with shortness of breath and diaphoresis. No relief with rest.",
                "past_medical_history": "Hypertension, hyperlipidemia, family history of CAD",
                "medications": "Lisinopril 10mg daily, Atorvastatin 40mg daily",
                "allergies": "NKDA",
                "social_history": "Smoker 1 PPD x 20 years, occasional alcohol use",
                "review_of_systems": "Positive for chest pain, shortness of breath, diaphoresis. Negative for nausea, vomiting, palpitations."
            },
            "clinical_findings": {
                "vital_signs": {
                    "blood_pressure": "160/95",
                    "heart_rate": 105,
                    "respiratory_rate": 22,
                    "temperature": "98.6°F",
                    "oxygen_saturation": "96% on room air"
                },
                "physical_exam": {
                    "general": "Anxious appearing male in moderate distress",
                    "cardiovascular": "Tachycardic, regular rhythm, no murmurs",
                    "pulmonary": "Clear to auscultation bilaterally",
                    "extremities": "No edema, pulses intact"
                },
                "diagnostic_tests": {
                    "ecg": "ST elevation in leads II, III, aVF",
                    "chest_xray": "No acute cardiopulmonary process",
                    "labs": "Troponin I elevated at 2.5 ng/mL"
                }
            },
            "template_preferences": {
                "format": "comprehensive",
                "include_differential": True,
                "include_plan_details": True
            }
        }
        
        response = await self.test_endpoint(
            "/medical-ai/clinical-documentation/generate-soap",
            "POST",
            test_data,
            "SOAP Note Generation"
        )
        
        # Validate SOAP note structure
        if response and "success" in response and response["success"]:
            if "documentation" in response:
                documentation = response["documentation"]
                soap_sections = ["subjective", "objective", "assessment", "plan"]
                present_sections = [section for section in soap_sections if section in str(documentation).lower()]
                
                if len(present_sections) >= 3:
                    self.log_test_result("SOAP Note Structure", True,
                                       f"SOAP note contains {len(present_sections)} sections")
                else:
                    self.log_test_result("SOAP Note Structure", False,
                                       f"SOAP note missing sections, only found: {present_sections}")
            else:
                self.log_test_result("SOAP Documentation Structure", False,
                                   "Missing documentation in response")
        
        return response
    
    async def test_suggest_icd10_codes(self):
        """Test POST /api/medical-ai/clinical-documentation/suggest-icd10"""
        test_data = {
            "clinical_content": {
                "chief_complaint": "Chest pain",
                "diagnosis": "ST-elevation myocardial infarction",
                "symptoms": ["chest pain", "shortness of breath", "diaphoresis"],
                "clinical_findings": ["ST elevation on ECG", "elevated troponin"],
                "comorbidities": ["hypertension", "hyperlipidemia"]
            },
            "provider_specialty": "EMERGENCY_MEDICINE"
        }
        
        response = await self.test_endpoint(
            "/medical-ai/clinical-documentation/suggest-icd10",
            "POST",
            test_data,
            "ICD-10 Code Suggestions"
        )
        
        # Validate ICD-10 suggestions
        if response and "success" in response and response["success"]:
            if "icd10_suggestions" in response and "total_suggestions" in response:
                suggestions = response["icd10_suggestions"]
                if isinstance(suggestions, list) and len(suggestions) > 0:
                    self.log_test_result("ICD-10 Suggestions Content", True,
                                       f"Generated {len(suggestions)} ICD-10 code suggestions")
                    
                    # Check if suggestions contain expected fields
                    if suggestions and isinstance(suggestions[0], dict):
                        expected_fields = ["code", "description"]
                        first_suggestion = suggestions[0]
                        has_required_fields = all(field in first_suggestion for field in expected_fields)
                        
                        if has_required_fields:
                            self.log_test_result("ICD-10 Suggestion Format", True,
                                               "ICD-10 suggestions have proper format")
                        else:
                            self.log_test_result("ICD-10 Suggestion Format", False,
                                               "ICD-10 suggestions missing required fields")
                else:
                    self.log_test_result("ICD-10 Suggestions Content", False,
                                       "No ICD-10 suggestions generated")
            else:
                self.log_test_result("ICD-10 Response Structure", False,
                                   "Missing ICD-10 suggestions in response")
        
        return response
    
    async def test_suggest_cpt_codes(self):
        """Test POST /api/medical-ai/clinical-documentation/suggest-cpt"""
        test_data = {
            "clinical_content": {
                "procedures_performed": ["ECG", "Chest X-ray", "Cardiac catheterization"],
                "diagnosis": "ST-elevation myocardial infarction",
                "treatment_provided": ["PCI", "Stent placement", "Medication administration"],
                "complexity_level": "high"
            },
            "encounter_data": {
                "encounter_type": "emergency_department",
                "duration_minutes": 180,
                "provider_time_minutes": 90,
                "decision_making_complexity": "high",
                "counseling_time_minutes": 15
            },
            "provider_specialty": "EMERGENCY_MEDICINE"
        }
        
        response = await self.test_endpoint(
            "/medical-ai/clinical-documentation/suggest-cpt",
            "POST",
            test_data,
            "CPT Code Suggestions"
        )
        
        # Validate CPT suggestions
        if response and "success" in response and response["success"]:
            if "cpt_suggestions" in response and "total_suggestions" in response:
                suggestions = response["cpt_suggestions"]
                if isinstance(suggestions, list) and len(suggestions) > 0:
                    self.log_test_result("CPT Suggestions Content", True,
                                       f"Generated {len(suggestions)} CPT code suggestions")
                else:
                    self.log_test_result("CPT Suggestions Content", False,
                                       "No CPT suggestions generated")
            else:
                self.log_test_result("CPT Response Structure", False,
                                   "Missing CPT suggestions in response")
        
        return response
    
    async def test_documentation_analytics(self):
        """Test POST /api/medical-ai/clinical-documentation/analytics"""
        test_data = {
            "provider_id": "dr-emergency-001",
            "timeframe_days": 30
        }
        
        response = await self.test_endpoint(
            "/medical-ai/clinical-documentation/analytics",
            "POST",
            test_data,
            "Documentation Analytics"
        )
        
        # Validate documentation analytics
        if response and "success" in response and response["success"]:
            if "analytics" in response:
                analytics = response["analytics"]
                if isinstance(analytics, dict):
                    self.log_test_result("Documentation Analytics Content", True,
                                       "Documentation analytics data received")
                else:
                    self.log_test_result("Documentation Analytics Content", False,
                                       "Invalid documentation analytics format")
            else:
                self.log_test_result("Documentation Analytics Structure", False,
                                   "Missing analytics in response")
        
        return response

    # ===========================
    # WORKFLOW OPTIMIZATION TESTS (3 ENDPOINTS)
    # ===========================
    
    async def test_analyze_workflow_metrics(self):
        """Test POST /api/medical-ai/workflow-optimization/analyze-metrics"""
        test_data = {
            "provider_id": "dr-emergency-001",
            "analysis_period_days": 7,
            "include_real_time": True
        }
        
        response = await self.test_endpoint(
            "/medical-ai/workflow-optimization/analyze-metrics",
            "POST",
            test_data,
            "Workflow Metrics Analysis"
        )
        
        # Validate workflow metrics
        if response and "success" in response and response["success"]:
            if "workflow_metrics" in response:
                metrics = response["workflow_metrics"]
                if isinstance(metrics, dict):
                    self.log_test_result("Workflow Metrics Content", True,
                                       "Workflow metrics data received")
                else:
                    self.log_test_result("Workflow Metrics Content", False,
                                       "Invalid workflow metrics format")
            else:
                self.log_test_result("Workflow Metrics Structure", False,
                                   "Missing workflow metrics in response")
        
        return response
    
    async def test_generate_workflow_recommendations(self):
        """Test POST /api/medical-ai/workflow-optimization/generate-recommendations"""
        test_data = {
            "provider_id": "dr-emergency-001",
            "focus_areas": [
                "patient_throughput",
                "documentation_efficiency", 
                "decision_support",
                "communication_optimization"
            ]
        }
        
        response = await self.test_endpoint(
            "/medical-ai/workflow-optimization/generate-recommendations",
            "POST",
            test_data,
            "Workflow Optimization Recommendations"
        )
        
        # Validate workflow recommendations
        if response and "success" in response and response["success"]:
            if "workflow_optimizations" in response and "total_optimizations" in response:
                optimizations = response["workflow_optimizations"]
                if isinstance(optimizations, list) and len(optimizations) > 0:
                    self.log_test_result("Workflow Recommendations Content", True,
                                       f"Generated {len(optimizations)} workflow optimization recommendations")
                else:
                    self.log_test_result("Workflow Recommendations Content", False,
                                       "No workflow optimization recommendations generated")
            else:
                self.log_test_result("Workflow Recommendations Structure", False,
                                   "Missing workflow optimizations in response")
        
        return response
    
    async def test_detect_workflow_bottlenecks(self):
        """Test POST /api/medical-ai/workflow-optimization/detect-bottlenecks"""
        test_data = {
            "provider_id": "dr-emergency-001",
            "current_workload": {
                "active_patients": 12,
                "waiting_room_count": 8,
                "bed_occupancy_rate": 0.95,
                "average_wait_time_minutes": 45,
                "staff_utilization": {
                    "physicians": 0.90,
                    "nurses": 0.85,
                    "technicians": 0.75
                },
                "equipment_availability": {
                    "ct_scanner": 0.60,
                    "xray_machines": 0.80,
                    "ultrasound": 0.90
                },
                "current_bottlenecks": [
                    "lab_results_delay",
                    "radiology_backlog",
                    "discharge_processing"
                ],
                "peak_hours": True,
                "shift_change_impact": False
            }
        }
        
        response = await self.test_endpoint(
            "/medical-ai/workflow-optimization/detect-bottlenecks",
            "POST",
            test_data,
            "Workflow Bottleneck Detection"
        )
        
        # Validate bottleneck detection
        if response and "success" in response and response["success"]:
            if "bottleneck_analysis" in response:
                analysis = response["bottleneck_analysis"]
                if isinstance(analysis, dict):
                    self.log_test_result("Bottleneck Analysis Content", True,
                                       "Bottleneck analysis data received")
                else:
                    self.log_test_result("Bottleneck Analysis Content", False,
                                       "Invalid bottleneck analysis format")
            else:
                self.log_test_result("Bottleneck Analysis Structure", False,
                                   "Missing bottleneck analysis in response")
        
        return response

    # ===========================
    # COMPREHENSIVE TEST EXECUTION
    # ===========================
    
    async def run_all_tests(self):
        """Execute all Provider Intelligence System tests"""
        print("🚀 STARTING COMPREHENSIVE PROVIDER INTELLIGENCE SYSTEM PHASE C.3 TESTING")
        print("=" * 80)
        
        # Provider Intelligence System Tests (4 endpoints)
        print("\n📋 TESTING PROVIDER INTELLIGENCE SYSTEM ENDPOINTS (4/12)")
        print("-" * 60)
        await self.test_create_provider_profile()
        await self.test_clinical_coaching()
        await self.test_provider_analytics()
        await self.test_cognitive_load_assessment()
        
        # Clinical Documentation AI Tests (4 endpoints)
        print("\n📋 TESTING CLINICAL DOCUMENTATION AI ENDPOINTS (4/12)")
        print("-" * 60)
        await self.test_generate_soap_note()
        await self.test_suggest_icd10_codes()
        await self.test_suggest_cpt_codes()
        await self.test_documentation_analytics()
        
        # Workflow Optimization Tests (3 endpoints)
        print("\n📋 TESTING WORKFLOW OPTIMIZATION ENDPOINTS (3/12)")
        print("-" * 60)
        await self.test_analyze_workflow_metrics()
        await self.test_generate_workflow_recommendations()
        await self.test_detect_workflow_bottlenecks()
        
        # Performance Analysis
        print("\n📊 PERFORMANCE ANALYSIS")
        print("-" * 40)
        self.analyze_performance()
        
        # Final Results Summary
        print("\n🎯 FINAL TEST RESULTS SUMMARY")
        print("=" * 80)
        self.print_final_summary()
    
    def analyze_performance(self):
        """Analyze performance metrics from all tests"""
        response_times = [result["response_time_ms"] for result in self.test_results 
                         if result["success"] and result["response_time_ms"] > 0]
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            
            print(f"Average Response Time: {avg_response_time:.2f}ms")
            print(f"Maximum Response Time: {max_response_time:.2f}ms")
            print(f"Minimum Response Time: {min_response_time:.2f}ms")
            
            # Check if all responses are under 30 seconds (30,000ms)
            slow_responses = [t for t in response_times if t > 30000]
            if not slow_responses:
                print("✅ All responses under 30 second target")
            else:
                print(f"⚠️  {len(slow_responses)} responses exceeded 30 second target")
        else:
            print("No successful responses to analyze")
    
    def print_final_summary(self):
        """Print comprehensive test results summary"""
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.failed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT: Provider Intelligence System is production-ready!")
        elif success_rate >= 75:
            print("✅ GOOD: Provider Intelligence System is mostly functional")
        elif success_rate >= 50:
            print("⚠️  MODERATE: Provider Intelligence System needs improvements")
        else:
            print("❌ CRITICAL: Provider Intelligence System has major issues")
        
        # Print failed tests for debugging
        failed_tests = [result for result in self.test_results if not result["success"]]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  - {test['test_name']}: {test['details']}")
        
        print("\n" + "=" * 80)
        print("PROVIDER INTELLIGENCE SYSTEM PHASE C.3 TESTING COMPLETE")

async def main():
    """Main test execution function"""
    async with ProviderIntelligenceSystemTester() as tester:
        await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())