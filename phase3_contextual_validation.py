#!/usr/bin/env python3
"""
🧠 PHASE 3: CLINICAL VALIDATION & OPTIMIZATION 🧠

Comprehensive testing suite for Step 2.2 Context-Aware Medical Reasoning Engine
that validates ultra-challenging contextual reasoning scenarios, performance requirements,
and clinical logic consistency.

TESTING OBJECTIVES:
✅ TEST all 3 ultra-challenging contextual reasoning scenarios  
✅ VALIDATE clinical logic consistency and medical coherence >0.97
✅ VERIFY causal relationship accuracy >94% and diagnostic reasoning quality
✅ OPTIMIZE for <25ms contextual processing performance
✅ ENSURE zero disruption to existing Phase 1-4 functionality

Algorithm Version: 4.0_contextual_reasoning (Phase 3 validation)
"""

import asyncio
import json
import time
import requests
from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Comprehensive validation result for contextual reasoning scenarios"""
    scenario_id: str
    scenario_name: str
    input_text: str
    processing_time_ms: float
    
    # Contextual reasoning validation
    contextual_factors_detected: Dict[str, List[str]]
    causal_relationships_found: List[Dict[str, Any]]
    clinical_hypotheses_generated: List[str]
    contextual_significance: str
    reasoning_confidence: float
    
    # Performance metrics
    response_structure_valid: bool
    contextual_fields_populated: bool
    performance_target_met: bool  # <25ms
    
    # Clinical validation
    medical_coherence_score: float
    causal_accuracy_assessment: float
    clinical_reasoning_quality: str
    specialist_referral_appropriate: bool
    
    # Pass/fail indicators
    scenario_passed: bool
    validation_errors: List[str]

class Phase3ContextualValidator:
    """
    🎯 PHASE 3: ULTRA-CHALLENGING CONTEXTUAL REASONING VALIDATOR 🎯
    
    Master clinician-level validation system that tests Step 2.2 Context-Aware 
    Medical Reasoning against the most challenging clinical scenarios.
    """
    
    def __init__(self):
        self.backend_url = "http://localhost:8001"
        self.test_results = []
        
        # Ultra-challenging scenarios for Phase 3 validation
        self.ultra_challenging_scenarios = {
            "scenario_1": {
                "name": "Complex Positional Context Mastery",
                "description": "Morning orthostatic hypotension with multiple triggering factors",
                "input_text": "Every morning when I get out of bed I feel dizzy and nauseous, sometimes I even feel like I'm going to faint, but it goes away after I sit back down for a few minutes. This also happens when I stand up quickly from a chair or get up from squatting down.",
                "expected_contextual_factors": {
                    "positional_factors": ["morning_orthostatic_challenge", "rapid_position_change", "orthostatic_symptom_trigger"],
                    "temporal_factors": ["morning_predominance", "immediate_onset", "rapid_resolution"],
                    "activity_relationships": ["positional_change_trigger", "sitting_relief_pattern"]
                },
                "expected_causal_relationships": {
                    "trigger": "morning_orthostatic_challenge",
                    "symptom": "orthostatic_symptom_complex",
                    "relationship_type": "positional",
                    "clinical_significance": "urgent"
                },
                "expected_clinical_hypotheses": [
                    "Orthostatic hypotension with morning predominance",
                    "cardiovascular evaluation",
                    "tilt table testing"
                ],
                "expected_performance": {"processing_time_ms": 25, "confidence": 0.92}
            },
            
            "scenario_2": {
                "name": "Exertional Context with Cardiac Implications", 
                "description": "Classic exertional angina with precise temporal and relief patterns",
                "input_text": "I get this crushing chest pain whenever I walk uphill or climb more than one flight of stairs, feels like an elephant sitting on my chest, but it completely goes away within 2-3 minutes of resting. Never happens when I'm just sitting or doing light activities around the house.",
                "expected_contextual_factors": {
                    "activity_relationships": ["enhanced_exertional_cardiac", "specific_exertion_trigger", "rest_relief_pattern"],
                    "temporal_factors": ["exertional_onset", "rapid_resolution_with_rest", "activity_correlation"],
                    "environmental_factors": ["physical_exertion_trigger", "rest_environment_relief"]
                },
                "expected_causal_relationships": {
                    "trigger": "enhanced_exertional_cardiac_trigger",
                    "symptom": "classic_crushing_angina",
                    "relationship_type": "enhanced_exertional_cardiac", 
                    "clinical_significance": "emergency"
                },
                "expected_clinical_hypotheses": [
                    "Enhanced Cardiac Analysis: Classic exertional angina",
                    "EMERGENCY coronary artery disease",
                    "urgent cardiology consultation"
                ],
                "expected_performance": {"processing_time_ms": 25, "confidence": 0.96}
            },
            
            "scenario_3": {
                "name": "Multi-Context Dietary/Stress/Temporal",
                "description": "Stress-modulated lactose intolerance with environmental variability",
                "input_text": "I've noticed that I get really bad stomach cramps and loose stools about 30-60 minutes after eating ice cream or drinking milk, but only when I'm stressed out at work. When I'm relaxed at home on weekends, I can sometimes tolerate small amounts of dairy without problems.",
                "expected_contextual_factors": {
                    "environmental_factors": ["stress_trigger", "workplace_stress", "relaxed_environment"],
                    "temporal_factors": ["postprandial_timing", "30_60_minute_onset", "conditional_tolerance"],
                    "activity_relationships": ["dietary_stress_interaction", "environmental_modulation"]
                },
                "expected_causal_relationships": {
                    "trigger": "stress_modulated_dairy_intake",
                    "symptom": "conditional_lactose_intolerance",
                    "relationship_type": "dietary_stress_interaction",
                    "clinical_significance": "moderate"
                },
                "expected_clinical_hypotheses": [
                    "Stress-modulated lactose intolerance",
                    "psychosomatic component",
                    "gut-brain axis dysfunction"
                ],
                "expected_performance": {"processing_time_ms": 25, "confidence": 0.92}
            }
        }
    
    async def run_comprehensive_phase3_validation(self) -> Dict[str, Any]:
        """
        🚀 MAIN PHASE 3 VALIDATION RUNNER 🚀
        
        Execute comprehensive validation of Step 2.2 Context-Aware Medical Reasoning
        against ultra-challenging clinical scenarios with performance optimization.
        """
        
        print("🧠 STARTING PHASE 3: CLINICAL VALIDATION & OPTIMIZATION")
        print("=" * 80)
        
        validation_results = {
            "phase3_summary": {
                "total_scenarios": len(self.ultra_challenging_scenarios),
                "scenarios_passed": 0,
                "average_processing_time": 0.0,
                "performance_target_met": False,
                "clinical_coherence_achieved": 0.0,
                "causal_accuracy_overall": 0.0,
                "validation_timestamp": datetime.now().isoformat()
            },
            "scenario_results": [],
            "performance_metrics": {},
            "clinical_validation": {},
            "recommendations": []
        }
        
        total_processing_time = 0.0
        total_coherence_score = 0.0
        total_causal_accuracy = 0.0
        
        # Test each ultra-challenging scenario
        for scenario_id, scenario_data in self.ultra_challenging_scenarios.items():
            print(f"\n🎯 TESTING {scenario_data['name'].upper()}")
            print(f"Description: {scenario_data['description']}")
            print(f"Input: {scenario_data['input_text'][:100]}...")
            
            try:
                result = await self._validate_contextual_scenario(scenario_id, scenario_data)
                validation_results["scenario_results"].append(result)
                
                # Aggregate metrics
                if result.scenario_passed:
                    validation_results["phase3_summary"]["scenarios_passed"] += 1
                
                total_processing_time += result.processing_time_ms
                total_coherence_score += result.medical_coherence_score
                total_causal_accuracy += result.causal_accuracy_assessment
                
                # Display results
                print(f"✅ RESULT: {'PASSED' if result.scenario_passed else 'FAILED'}")
                print(f"⚡ Processing Time: {result.processing_time_ms:.2f}ms")
                print(f"🧠 Clinical Coherence: {result.medical_coherence_score:.3f}")
                print(f"🎯 Causal Accuracy: {result.causal_accuracy_assessment:.3f}")
                print(f"🏥 Reasoning Quality: {result.clinical_reasoning_quality}")
                
                if result.validation_errors:
                    print(f"❌ Validation Errors: {', '.join(result.validation_errors)}")
                
            except Exception as e:
                print(f"❌ SCENARIO {scenario_id} FAILED WITH ERROR: {str(e)}")
                validation_results["scenario_results"].append(
                    self._create_error_result(scenario_id, scenario_data, str(e))
                )
        
        # Calculate final metrics
        num_scenarios = len(self.ultra_challenging_scenarios)
        validation_results["phase3_summary"]["average_processing_time"] = total_processing_time / num_scenarios
        validation_results["phase3_summary"]["performance_target_met"] = (
            validation_results["phase3_summary"]["average_processing_time"] < 25.0
        )
        validation_results["phase3_summary"]["clinical_coherence_achieved"] = total_coherence_score / num_scenarios
        validation_results["phase3_summary"]["causal_accuracy_overall"] = total_causal_accuracy / num_scenarios
        
        # Generate recommendations
        validation_results["recommendations"] = self._generate_phase3_recommendations(validation_results)
        
        # Final validation summary
        self._print_phase3_summary(validation_results)
        
        return validation_results
    
    async def _validate_contextual_scenario(self, scenario_id: str, scenario_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate individual contextual reasoning scenario against expected outcomes
        """
        
        # Record start time for performance measurement
        start_time = time.time()
        
        try:
            # Call medical AI service contextual reasoning endpoint
            response = requests.post(
                f"{self.backend_url}/api/medical-ai/contextual-analysis",
                json={
                    "text": scenario_data["input_text"],
                    "analysis_type": "comprehensive_contextual"
                },
                timeout=60  # Increased timeout for complex scenarios
            )
            
            processing_time_ms = (time.time() - start_time) * 1000
            
            if response.status_code != 200:
                raise Exception(f"API returned status {response.status_code}: {response.text}")
            
            result_data = response.json()
            
            # Validate response structure
            contextual_reasoning = result_data.get("contextual_reasoning", {})
            
            # Extract contextual factors
            contextual_factors = {
                "positional_factors": contextual_reasoning.get("contextual_factors", {}).get("positional", []),
                "temporal_factors": contextual_reasoning.get("contextual_factors", {}).get("temporal", []),
                "environmental_factors": contextual_reasoning.get("contextual_factors", {}).get("environmental", []),
                "activity_relationships": contextual_reasoning.get("contextual_factors", {}).get("activity", [])
            }
            
            # Extract causal relationships
            causal_relationships = contextual_reasoning.get("causal_relationships", [])
            
            # Extract clinical hypotheses
            clinical_hypotheses = contextual_reasoning.get("clinical_hypotheses", [])
            
            # Validate scenario-specific expectations
            validation_errors = []
            
            # Check contextual factors
            expected_factors = scenario_data["expected_contextual_factors"]
            contextual_fields_populated = all(
                len(contextual_factors.get(key, [])) > 0 for key in expected_factors.keys()
            )
            
            if not contextual_fields_populated:
                validation_errors.append("Missing expected contextual factors")
            
            # Check causal relationships
            expected_causal = scenario_data["expected_causal_relationships"]
            causal_found = any(
                rel.get("clinical_significance") == expected_causal.get("clinical_significance")
                for rel in causal_relationships
            )
            
            if not causal_found:
                validation_errors.append("Expected causal relationship not detected")
            
            # Check clinical hypotheses
            expected_hypotheses = scenario_data["expected_clinical_hypotheses"]
            hypotheses_quality = any(
                any(expected in hyp.lower() for expected in expected_hypotheses)
                for hyp in clinical_hypotheses
            )
            
            if not hypotheses_quality:
                validation_errors.append("Clinical hypotheses do not meet expectations")
            
            # Performance validation
            performance_target_met = processing_time_ms < 25.0
            if not performance_target_met:
                validation_errors.append(f"Processing time {processing_time_ms:.2f}ms exceeds 25ms target")
            
            # Calculate validation scores
            medical_coherence_score = self._calculate_medical_coherence(result_data)
            causal_accuracy = self._assess_causal_accuracy(causal_relationships, expected_causal)
            clinical_reasoning_quality = self._assess_clinical_reasoning_quality(clinical_hypotheses)
            
            # Determine overall pass/fail
            scenario_passed = (
                len(validation_errors) == 0 and
                medical_coherence_score >= 0.97 and
                causal_accuracy >= 0.94 and
                performance_target_met
            )
            
            return ValidationResult(
                scenario_id=scenario_id,
                scenario_name=scenario_data["name"],
                input_text=scenario_data["input_text"],
                processing_time_ms=processing_time_ms,
                contextual_factors_detected=contextual_factors,
                causal_relationships_found=causal_relationships,
                clinical_hypotheses_generated=clinical_hypotheses,
                contextual_significance=contextual_reasoning.get("contextual_significance", ""),
                reasoning_confidence=contextual_reasoning.get("reasoning_confidence", 0.0),
                response_structure_valid=bool(contextual_reasoning),
                contextual_fields_populated=contextual_fields_populated,
                performance_target_met=performance_target_met,
                medical_coherence_score=medical_coherence_score,
                causal_accuracy_assessment=causal_accuracy,
                clinical_reasoning_quality=clinical_reasoning_quality,
                specialist_referral_appropriate=self._validate_specialist_referral(result_data),
                scenario_passed=scenario_passed,
                validation_errors=validation_errors
            )
            
        except Exception as e:
            processing_time_ms = (time.time() - start_time) * 1000
            return self._create_error_result(scenario_id, scenario_data, str(e), processing_time_ms)
    
    def _calculate_medical_coherence(self, result_data: Dict[str, Any]) -> float:
        """Calculate medical coherence score based on result consistency"""
        coherence_factors = []
        
        # Check consistency between entities and contextual reasoning
        entities = result_data.get("entities", {})
        contextual_reasoning = result_data.get("contextual_reasoning", {})
        
        # Factor 1: Entity-context alignment (0.4 weight)
        symptoms_detected = len(entities.get("symptoms", []))
        contextual_factors_count = sum(
            len(factors) for factors in contextual_reasoning.get("contextual_factors", {}).values()
        )
        
        if symptoms_detected > 0 and contextual_factors_count > 0:
            coherence_factors.append(0.4)
        else:
            coherence_factors.append(0.0)
        
        # Factor 2: Causal relationship plausibility (0.3 weight) 
        causal_relationships = contextual_reasoning.get("causal_relationships", [])
        if causal_relationships:
            avg_causality_strength = sum(
                rel.get("causality_strength", 0.0) for rel in causal_relationships
            ) / len(causal_relationships)
            coherence_factors.append(0.3 * avg_causality_strength)
        else:
            coherence_factors.append(0.0)
        
        # Factor 3: Clinical hypothesis quality (0.3 weight)
        clinical_hypotheses = contextual_reasoning.get("clinical_hypotheses", [])
        if clinical_hypotheses and any(len(hyp) > 20 for hyp in clinical_hypotheses):
            coherence_factors.append(0.3)
        else:
            coherence_factors.append(0.1)
        
        return min(sum(coherence_factors), 1.0)
    
    def _assess_causal_accuracy(self, found_relationships: List[Dict[str, Any]], 
                              expected_relationship: Dict[str, Any]) -> float:
        """Assess accuracy of detected causal relationships"""
        if not found_relationships:
            return 0.0
        
        accuracy_score = 0.0
        
        # Check if expected relationship type is found
        expected_type = expected_relationship.get("relationship_type")
        if any(rel.get("relationship_type") == expected_type for rel in found_relationships):
            accuracy_score += 0.4
        
        # Check clinical significance alignment
        expected_significance = expected_relationship.get("clinical_significance")
        if any(rel.get("clinical_significance") == expected_significance for rel in found_relationships):
            accuracy_score += 0.3
        
        # Check causality strength
        avg_strength = sum(rel.get("causality_strength", 0.0) for rel in found_relationships) / len(found_relationships)
        accuracy_score += 0.3 * avg_strength
        
        return min(accuracy_score, 1.0)
    
    def _assess_clinical_reasoning_quality(self, clinical_hypotheses: List[str]) -> str:
        """Assess quality of clinical reasoning and hypotheses"""
        if not clinical_hypotheses:
            return "poor"
        
        # Check for specialist-level content
        specialist_indicators = [
            "evaluation", "assessment", "consultation", "workup", "differential",
            "emergency", "urgent", "cardiology", "neurology", "gastroenterology"
        ]
        
        specialist_count = sum(
            1 for hyp in clinical_hypotheses 
            for indicator in specialist_indicators
            if indicator.lower() in hyp.lower()
        )
        
        if specialist_count >= 3:
            return "excellent"
        elif specialist_count >= 2:
            return "good"
        elif specialist_count >= 1:
            return "fair"
        else:
            return "poor"
    
    def _validate_specialist_referral(self, result_data: Dict[str, Any]) -> bool:
        """Validate appropriateness of specialist referral recommendations"""
        contextual_reasoning = result_data.get("contextual_reasoning", {})
        specialist_referral = contextual_reasoning.get("specialist_referral_context")
        
        # Check if emergency/urgent cases have appropriate referrals
        causal_relationships = contextual_reasoning.get("causal_relationships", [])
        has_emergency = any(
            rel.get("clinical_significance") == "emergency" for rel in causal_relationships
        )
        
        if has_emergency:
            return specialist_referral is not None and "urgent" in str(specialist_referral).lower()
        
        return True  # Non-emergency cases are flexible
    
    def _create_error_result(self, scenario_id: str, scenario_data: Dict[str, Any], 
                           error_msg: str, processing_time_ms: float = 0.0) -> ValidationResult:
        """Create error result for failed scenarios"""
        return ValidationResult(
            scenario_id=scenario_id,
            scenario_name=scenario_data["name"],
            input_text=scenario_data["input_text"],
            processing_time_ms=processing_time_ms,
            contextual_factors_detected={},
            causal_relationships_found=[],
            clinical_hypotheses_generated=[],
            contextual_significance="",
            reasoning_confidence=0.0,
            response_structure_valid=False,
            contextual_fields_populated=False,
            performance_target_met=False,
            medical_coherence_score=0.0,
            causal_accuracy_assessment=0.0,
            clinical_reasoning_quality="error",
            specialist_referral_appropriate=False,
            scenario_passed=False,
            validation_errors=[error_msg]
        )
    
    def _generate_phase3_recommendations(self, validation_results: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations based on validation results"""
        recommendations = []
        
        summary = validation_results["phase3_summary"]
        
        # Performance recommendations
        if not summary["performance_target_met"]:
            recommendations.append(
                f"OPTIMIZE processing performance - current average {summary['average_processing_time']:.2f}ms exceeds 25ms target"
            )
        
        # Clinical coherence recommendations
        if summary["clinical_coherence_achieved"] < 0.97:
            recommendations.append(
                f"ENHANCE clinical coherence - current {summary['clinical_coherence_achieved']:.3f} below 0.97 target"
            )
        
        # Causal accuracy recommendations  
        if summary["causal_accuracy_overall"] < 0.94:
            recommendations.append(
                f"IMPROVE causal relationship accuracy - current {summary['causal_accuracy_overall']:.3f} below 0.94 target"
            )
        
        # Scenario-specific recommendations
        failed_scenarios = [
            result for result in validation_results["scenario_results"]
            if not result.scenario_passed
        ]
        
        for result in failed_scenarios:
            recommendations.append(
                f"FIX {result.scenario_name}: {', '.join(result.validation_errors)}"
            )
        
        if not recommendations:
            recommendations.append("🎉 ALL PHASE 3 VALIDATION TARGETS MET - SYSTEM OPTIMIZED")
        
        return recommendations
    
    def _print_phase3_summary(self, validation_results: Dict[str, Any]):
        """Print comprehensive Phase 3 validation summary"""
        
        print("\n" + "="*80)
        print("🏆 PHASE 3: CLINICAL VALIDATION & OPTIMIZATION SUMMARY")
        print("="*80)
        
        summary = validation_results["phase3_summary"]
        
        print(f"📊 SCENARIOS TESTED: {summary['total_scenarios']}")
        print(f"✅ SCENARIOS PASSED: {summary['scenarios_passed']}")
        print(f"📈 SUCCESS RATE: {(summary['scenarios_passed']/summary['total_scenarios']*100):.1f}%")
        
        print(f"\n⚡ PERFORMANCE METRICS:")
        print(f"   Average Processing Time: {summary['average_processing_time']:.2f}ms")
        print(f"   Performance Target (<25ms): {'✅ MET' if summary['performance_target_met'] else '❌ NOT MET'}")
        
        print(f"\n🧠 CLINICAL VALIDATION:")
        print(f"   Medical Coherence: {summary['clinical_coherence_achieved']:.3f}")
        print(f"   Coherence Target (>0.97): {'✅ MET' if summary['clinical_coherence_achieved'] >= 0.97 else '❌ NOT MET'}")
        print(f"   Causal Accuracy: {summary['causal_accuracy_overall']:.3f}")
        print(f"   Accuracy Target (>0.94): {'✅ MET' if summary['causal_accuracy_overall'] >= 0.94 else '❌ NOT MET'}")
        
        print(f"\n🔧 RECOMMENDATIONS:")
        for rec in validation_results["recommendations"]:
            print(f"   • {rec}")
        
        print("\n" + "="*80)

async def main():
    """Main Phase 3 validation runner"""
    validator = Phase3ContextualValidator()
    results = await validator.run_comprehensive_phase3_validation()
    
    # Save detailed results
    with open("/app/phase3_validation_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to: /app/phase3_validation_results.json")

if __name__ == "__main__":
    asyncio.run(main())