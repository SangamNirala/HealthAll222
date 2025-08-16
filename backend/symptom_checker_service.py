# Comprehensive Symptom Checker & Wellness Advisor Service
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import uuid
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Emergency Alert Levels
class AlertLevel(str, Enum):
    GREEN = "green"      # Continue home remedies
    YELLOW = "yellow"    # Monitor for 24-48 hours  
    RED = "red"         # Seek medical attention within 24 hours
    EMERGENCY = "emergency"  # Contact emergency services immediately

# Symptom Categories and Red Flags
SYMPTOM_CATEGORIES = {
    "pain_discomfort": ["headache", "muscle_aches", "joint_pain", "abdominal_pain"],
    "digestive": ["bloating", "nausea", "stomach_ache", "indigestion", "constipation"],
    "energy_mood": ["fatigue", "low_energy", "mood_swings", "irritability"],
    "neurological": ["brain_fog", "dizziness", "memory_issues", "concentration_problems"],
    "respiratory": ["shortness_of_breath", "cough", "chest_tightness"],
    "cardiovascular": ["chest_pain", "heart_palpitations", "rapid_heartbeat"],
    "dermatological": ["skin_rash", "itching", "skin_irritation"],
    "sleep": ["insomnia", "poor_sleep_quality", "restless_sleep"]
}

RED_FLAG_SYMPTOMS = {
    'chest_pain': AlertLevel.EMERGENCY,
    'difficulty_breathing': AlertLevel.EMERGENCY,
    'severe_headache_sudden': AlertLevel.EMERGENCY,
    'persistent_vomiting': AlertLevel.RED,
    'high_fever_confusion': AlertLevel.EMERGENCY,
    'severe_abdominal_pain': AlertLevel.RED,
    'bleeding_unusual': AlertLevel.RED,
    'loss_of_consciousness': AlertLevel.EMERGENCY,
    'severe_allergic_reaction': AlertLevel.EMERGENCY
}

REMEDY_DATABASE = {
    "headache": {
        "instant_relief": [
            "Drink 16oz water immediately - dehydration is a common cause",
            "Apply cold compress to forehead for 15 minutes", 
            "Practice deep breathing: 4 counts in, hold 7, exhale 8",
            "Gentle neck and shoulder stretches"
        ],
        "action_plan": {
            "day_1": [
                "Morning: Start with 2 glasses water + light stretching",
                "Mid-day: Check posture, take screen breaks every hour", 
                "Evening: Herbal tea (peppermint/chamomile), early dinner",
                "Track: Headache intensity (1-10) every 4 hours"
            ],
            "day_2": [
                "Continue hydration protocol (10+ glasses water)",
                "Add magnesium-rich foods (spinach, almonds, dark chocolate)",
                "20-minute walk in fresh air",
                "Track: Triggers, stress levels, sleep quality"
            ],
            "day_3": [
                "Evaluate improvement - if <50% better, consider medical consult",
                "Identify successful interventions to continue",
                "Plan prevention strategy based on triggers identified"
            ]
        },
        "triggers": ["dehydration", "stress", "poor_posture", "screen_time", "sleep_deprivation"],
        "prevention": ["Regular hydration", "Stress management", "Ergonomic workspace"]
    },
    
    "fatigue": {
        "instant_relief": [
            "10-minute brisk walk or light movement",
            "Drink water + pinch of sea salt for electrolytes",
            "5-minute power nap if possible (no longer)",
            "Eat protein-rich snack (nuts, Greek yogurt)"
        ],
        "action_plan": {
            "day_1": [
                "Morning: Protein breakfast within 1 hour of waking",
                "Mid-day: Balanced lunch with complex carbs + protein",
                "Afternoon: Brief 10-min walk, avoid caffeine after 2 PM",
                "Evening: Iron-rich dinner (spinach, lean meat, beans)"
            ],
            "day_2": [
                "Add B-vitamin rich foods (eggs, nutritional yeast)",
                "20-minute gentle exercise (yoga, walking)",
                "Optimize sleep environment (cool, dark, quiet)",
                "Track energy levels hourly on 1-10 scale"
            ],
            "day_3": [
                "Assess energy patterns - identify best/worst times",
                "If no improvement, check for underlying conditions",
                "Create sustainable energy management routine"
            ]
        },
        "triggers": ["poor_sleep", "dehydration", "blood_sugar_swings", "sedentary_lifestyle"],
        "prevention": ["Consistent sleep schedule", "Balanced nutrition", "Regular movement"]
    },
    
    "bloating": {
        "instant_relief": [
            "Warm peppermint tea or ginger tea",
            "Gentle abdominal massage in clockwise circles",
            "5-10 minute walk to aid digestion",
            "Avoid carbonated drinks and gum"
        ],
        "action_plan": {
            "day_1": [
                "Morning: Start with warm lemon water",
                "Meals: Eat slowly, chew thoroughly, smaller portions",
                "Avoid: High FODMAP foods (onions, garlic, beans)",
                "Evening: Herbal digestive tea, gentle yoga poses"
            ],
            "day_2": [
                "Continue anti-inflammatory foods (ginger, turmeric)",
                "Add probiotics (kefir, sauerkraut, yogurt)",
                "Stay upright 2-3 hours after meals",
                "Track foods that trigger vs. help symptoms"
            ],
            "day_3": [
                "Identify trigger food patterns",
                "If persistent, consider food sensitivity testing",
                "Develop personalized dietary approach"
            ]
        },
        "triggers": ["overeating", "eating_too_fast", "food_sensitivities", "stress"],
        "prevention": ["Mindful eating", "Regular meal times", "Stress reduction"]
    },
    
    "brain_fog": {
        "instant_relief": [
            "Deep breathing exercise for 5 minutes",
            "Drink cold water + brief cold exposure (cold face wash)",
            "5-minute meditation or mindfulness",
            "Light physical movement to increase circulation"
        ],
        "action_plan": {
            "day_1": [
                "Morning: Omega-3 rich breakfast (walnuts, chia seeds)",
                "Mid-day: Brain-boosting lunch (blueberries, leafy greens)",
                "Afternoon: 15-minute walk, avoid processed foods",
                "Evening: Limit screens 1 hour before bed"
            ],
            "day_2": [
                "Add cognitive exercises (puzzles, reading)",
                "Ensure 7-9 hours quality sleep",
                "Stay hydrated (brain is 75% water)",
                "Track mental clarity on 1-10 scale"
            ],
            "day_3": [
                "Evaluate cognitive improvement",
                "Identify lifestyle factors that help/hinder",
                "Consider stress reduction techniques if needed"
            ]
        },
        "triggers": ["poor_sleep", "dehydration", "stress", "blood_sugar_imbalance"],
        "prevention": ["Quality sleep", "Regular exercise", "Stress management"]
    }
}

class SymptomAssessmentEngine:
    """Advanced symptom assessment with pattern recognition"""
    
    def __init__(self):
        self.symptom_weights = {
            "severity": 0.4,      # How severe (1-10)
            "frequency": 0.25,    # How often
            "duration": 0.20,     # How long
            "impact": 0.15        # Life impact
        }
    
    def assess_symptoms(self, symptom_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive symptom assessment"""
        symptoms = symptom_data.get("symptoms", [])
        
        # Calculate overall severity score
        severity_score = self._calculate_severity_score(symptoms)
        
        # Detect symptom patterns and combinations
        patterns = self._detect_symptom_patterns(symptoms)
        
        # Check for red flags
        alert_level = self._check_red_flags(symptoms)
        
        # Generate symptom profile
        symptom_profile = {
            "assessment_id": str(uuid.uuid4()),
            "severity_score": severity_score,
            "alert_level": alert_level.value,
            "primary_symptoms": self._get_primary_symptoms(symptoms),
            "symptom_patterns": patterns,
            "affected_systems": self._identify_affected_systems(symptoms),
            "complexity_level": self._assess_complexity(symptoms),
            "timestamp": datetime.utcnow()
        }
        
        return symptom_profile
    
    def _calculate_severity_score(self, symptoms: List[Dict]) -> float:
        """Calculate weighted severity score"""
        if not symptoms:
            return 0.0
        
        total_score = 0.0
        for symptom in symptoms:
            severity = symptom.get("severity", 1)  # 1-10
            frequency = symptom.get("frequency", 1)  # 1-5 
            duration = symptom.get("duration_days", 1)  # days
            impact = symptom.get("life_impact", 1)  # 1-5
            
            # Normalize scores
            normalized_severity = severity / 10.0
            normalized_frequency = frequency / 5.0
            normalized_duration = min(duration / 30.0, 1.0)  # Cap at 30 days
            normalized_impact = impact / 5.0
            
            # Calculate weighted score
            symptom_score = (
                normalized_severity * self.symptom_weights["severity"] +
                normalized_frequency * self.symptom_weights["frequency"] +
                normalized_duration * self.symptom_weights["duration"] +
                normalized_impact * self.symptom_weights["impact"]
            )
            
            total_score += symptom_score
        
        # Average and convert to 0-100 scale
        return min((total_score / len(symptoms)) * 100, 100)
    
    def _detect_symptom_patterns(self, symptoms: List[Dict]) -> List[str]:
        """Detect common symptom combination patterns"""
        symptom_names = [s.get("name", "").lower() for s in symptoms]
        patterns = []
        
        # Digestive pattern
        digestive_symptoms = ["bloating", "nausea", "abdominal_pain", "indigestion"]
        if len(set(symptom_names) & set(digestive_symptoms)) >= 2:
            patterns.append("digestive_dysfunction")
        
        # Inflammatory pattern
        inflammatory_symptoms = ["joint_pain", "muscle_aches", "fatigue", "headache"]
        if len(set(symptom_names) & set(inflammatory_symptoms)) >= 3:
            patterns.append("inflammatory_response")
        
        # Stress pattern
        stress_symptoms = ["headache", "muscle_tension", "fatigue", "sleep_issues"]
        if len(set(symptom_names) & set(stress_symptoms)) >= 2:
            patterns.append("stress_related")
        
        # Hormonal pattern
        hormonal_symptoms = ["mood_swings", "fatigue", "bloating", "headache"]
        if len(set(symptom_names) & set(hormonal_symptoms)) >= 3:
            patterns.append("hormonal_imbalance")
        
        return patterns
    
    def _check_red_flags(self, symptoms: List[Dict]) -> AlertLevel:
        """Check for emergency or urgent symptoms"""
        for symptom in symptoms:
            symptom_name = symptom.get("name", "").lower()
            severity = symptom.get("severity", 1)
            
            # Check direct red flags
            if symptom_name in RED_FLAG_SYMPTOMS:
                return RED_FLAG_SYMPTOMS[symptom_name]
            
            # Check severity-based red flags
            if severity >= 9:  # Severe symptoms
                if "chest" in symptom_name or "heart" in symptom_name:
                    return AlertLevel.EMERGENCY
                elif "head" in symptom_name and "sudden" in symptom.get("description", ""):
                    return AlertLevel.EMERGENCY
                elif severity == 10:  # Maximum severity
                    return AlertLevel.RED
        
        # Check for concerning combinations
        high_severity_count = sum(1 for s in symptoms if s.get("severity", 1) >= 7)
        if high_severity_count >= 3:
            return AlertLevel.YELLOW
        
        return AlertLevel.GREEN
    
    def _get_primary_symptoms(self, symptoms: List[Dict]) -> List[str]:
        """Identify primary symptoms based on severity and impact"""
        sorted_symptoms = sorted(
            symptoms, 
            key=lambda x: x.get("severity", 1) * x.get("life_impact", 1), 
            reverse=True
        )
        return [s.get("name", "") for s in sorted_symptoms[:3]]
    
    def _identify_affected_systems(self, symptoms: List[Dict]) -> List[str]:
        """Identify which body systems are affected"""
        systems = set()
        
        for symptom in symptoms:
            symptom_name = symptom.get("name", "").lower()
            
            for category, symptom_list in SYMPTOM_CATEGORIES.items():
                if any(s in symptom_name for s in symptom_list):
                    systems.add(category)
        
        return list(systems)
    
    def _assess_complexity(self, symptoms: List[Dict]) -> str:
        """Assess symptom complexity level"""
        num_symptoms = len(symptoms)
        num_systems = len(self._identify_affected_systems(symptoms))
        avg_severity = sum(s.get("severity", 1) for s in symptoms) / max(len(symptoms), 1)
        
        if num_symptoms >= 5 or num_systems >= 3 or avg_severity >= 7:
            return "complex"
        elif num_symptoms >= 3 or num_systems >= 2 or avg_severity >= 5:
            return "moderate"
        else:
            return "simple"

class ReliefRecommendationSystem:
    """AI-powered relief recommendation engine"""
    
    def __init__(self, ai_service_manager):
        self.ai_service = ai_service_manager
        
    async def generate_relief_recommendations(self, symptom_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive relief recommendations"""
        
        # Get instant relief suggestions
        instant_relief = self._get_instant_relief(symptom_profile)
        
        # Generate AI-powered recommendations
        ai_recommendations = await self._get_ai_recommendations(symptom_profile)
        
        # Create targeted interventions
        interventions = self._create_targeted_interventions(symptom_profile)
        
        # Timing-specific protocols
        timing_protocols = self._get_timing_protocols(symptom_profile)
        
        return {
            "instant_relief": instant_relief,
            "ai_recommendations": ai_recommendations,
            "targeted_interventions": interventions,
            "timing_protocols": timing_protocols,
            "estimated_relief_time": self._estimate_relief_time(symptom_profile),
            "confidence_score": self._calculate_confidence(symptom_profile)
        }
    
    def _get_instant_relief(self, symptom_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get immediate relief suggestions based on symptoms"""
        primary_symptoms = symptom_profile.get("primary_symptoms", [])
        instant_relief = []
        
        for symptom in primary_symptoms:
            symptom_key = symptom.lower()
            if symptom_key in REMEDY_DATABASE:
                relief_items = REMEDY_DATABASE[symptom_key]["instant_relief"]
                for item in relief_items:
                    instant_relief.append({
                        "action": item,
                        "target_symptom": symptom,
                        "time_to_effect": "5-15 minutes",
                        "evidence_level": "moderate"
                    })
        
        # Add universal relief measures
        instant_relief.extend([
            {
                "action": "Deep breathing: 4-7-8 technique for 5 cycles",
                "target_symptom": "general_relief",
                "time_to_effect": "2-5 minutes",
                "evidence_level": "high"
            },
            {
                "action": "Hydrate with 16oz room temperature water",
                "target_symptom": "general_wellbeing",
                "time_to_effect": "10-30 minutes", 
                "evidence_level": "high"
            }
        ])
        
        return instant_relief[:6]  # Limit to top 6 recommendations
    
    async def _get_ai_recommendations(self, symptom_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered personalized recommendations"""
        try:
            context = self._build_symptom_context(symptom_profile)
            
            # Use Groq for fast inference, fallback to Gemini
            if hasattr(self.ai_service, 'groq_client') and self.ai_service.groq_client:
                recommendations = await self._groq_symptom_analysis(context)
            else:
                recommendations = await self._gemini_symptom_analysis(context)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating AI recommendations: {e}")
            return self._fallback_recommendations(symptom_profile)
    
    async def _groq_symptom_analysis(self, context: str) -> Dict[str, Any]:
        """Use Groq for symptom analysis"""
        try:
            completion = self.ai_service.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert medical advisor AI specialized in symptom relief and wellness recommendations. Provide evidence-based, safe, and practical advice. Always include medical disclaimer. Respond in JSON format with 'dietary_interventions', 'lifestyle_modifications', 'natural_remedies', 'when_to_seek_help', and 'disclaimer' keys."
                    },
                    {"role": "user", "content": context}
                ],
                max_tokens=1200,
                temperature=0.6
            )
            
            response_text = completion.choices[0].message.content
            
            try:
                parsed_response = json.loads(response_text)
                return {
                    "source": "groq_ai",
                    "dietary_interventions": parsed_response.get("dietary_interventions", []),
                    "lifestyle_modifications": parsed_response.get("lifestyle_modifications", []),
                    "natural_remedies": parsed_response.get("natural_remedies", []),
                    "when_to_seek_help": parsed_response.get("when_to_seek_help", []),
                    "disclaimer": parsed_response.get("disclaimer", "This is not medical advice. Consult healthcare provider for persistent symptoms.")
                }
            except json.JSONDecodeError:
                return self._parse_text_recommendations(response_text)
                
        except Exception as e:
            logger.error(f"Groq symptom analysis error: {e}")
            raise
    
    def _build_symptom_context(self, symptom_profile: Dict[str, Any]) -> str:
        """Build context for AI symptom analysis"""
        return f"""
        Symptom Analysis Request:
        
        Primary Symptoms: {symptom_profile.get('primary_symptoms', [])}
        Severity Score: {symptom_profile.get('severity_score', 0)}/100
        Affected Systems: {symptom_profile.get('affected_systems', [])}
        Symptom Patterns: {symptom_profile.get('symptom_patterns', [])}
        Complexity Level: {symptom_profile.get('complexity_level', 'simple')}
        
        Please provide:
        1. Dietary interventions that may help
        2. Lifestyle modifications for relief
        3. Evidence-based natural remedies
        4. Clear guidance on when to seek medical help
        5. Appropriate medical disclaimer
        
        Focus on safe, evidence-based recommendations suitable for home care.
        """
    
    def _create_targeted_interventions(self, symptom_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create targeted interventions based on symptom patterns"""
        patterns = symptom_profile.get("symptom_patterns", [])
        interventions = []
        
        if "digestive_dysfunction" in patterns:
            interventions.append({
                "type": "digestive_support",
                "intervention": "FODMAP elimination trial + digestive enzymes",
                "duration": "7-14 days",
                "expected_improvement": "60-80%",
                "monitoring": "Track symptoms before/after meals"
            })
        
        if "inflammatory_response" in patterns:
            interventions.append({
                "type": "anti_inflammatory",
                "intervention": "Anti-inflammatory diet + omega-3 supplementation",
                "duration": "2-3 weeks",
                "expected_improvement": "50-70%",
                "monitoring": "Track pain levels and energy daily"
            })
        
        if "stress_related" in patterns:
            interventions.append({
                "type": "stress_management", 
                "intervention": "Daily meditation + adaptogenic herbs",
                "duration": "3-4 weeks",
                "expected_improvement": "40-60%",
                "monitoring": "Track stress levels and sleep quality"
            })
        
        return interventions
    
    def _get_timing_protocols(self, symptom_profile: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate timing-specific protocols"""
        return {
            "morning": [
                "Hydrate with 16-20oz water + lemon",
                "Gentle movement/stretching for 5-10 minutes",
                "Anti-inflammatory breakfast if digestive symptoms"
            ],
            "afternoon": [
                "Check in with symptom levels (1-10 scale)",
                "Apply targeted relief measures as needed",
                "Take short walk or movement break"
            ],
            "evening": [
                "Herbal tea for symptom-specific relief",
                "Relaxation techniques (breathing, meditation)",
                "Early, light dinner if digestive issues present"
            ]
        }

class ActionPlanGenerator:
    """Generate structured 3-day action plans"""
    
    def generate_action_plan(self, symptom_profile: Dict[str, Any], recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive 3-day action plan"""
        
        primary_symptoms = symptom_profile.get("primary_symptoms", [])
        complexity = symptom_profile.get("complexity_level", "simple")
        
        # Generate daily plans
        daily_plans = {}
        for day in range(1, 4):
            daily_plans[f"day_{day}"] = self._generate_daily_plan(
                day, primary_symptoms, recommendations, complexity
            )
        
        # Generate progress tracking milestones
        milestones = self._generate_milestones(symptom_profile)
        
        # Create success metrics
        success_metrics = self._define_success_metrics(symptom_profile)
        
        return {
            "plan_id": str(uuid.uuid4()),
            "title": f"{len(primary_symptoms)}-Symptom Relief Protocol",
            "duration": "72 hours",
            "daily_plans": daily_plans,
            "progress_milestones": milestones,
            "success_metrics": success_metrics,
            "adjustment_triggers": self._get_adjustment_triggers(),
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(hours=72)
        }
    
    def _generate_daily_plan(self, day: int, symptoms: List[str], recommendations: Dict, complexity: str) -> Dict[str, Any]:
        """Generate plan for specific day"""
        
        base_plan = {
            "day_focus": self._get_day_focus(day),
            "morning_routine": self._get_morning_routine(day, symptoms),
            "midday_checkpoints": self._get_midday_checkpoints(day),
            "evening_routine": self._get_evening_routine(day, symptoms),
            "tracking_requirements": self._get_tracking_requirements(day)
        }
        
        # Add complexity-specific elements
        if complexity in ["moderate", "complex"]:
            base_plan["additional_interventions"] = self._get_additional_interventions(day, complexity)
        
        return base_plan
    
    def _get_day_focus(self, day: int) -> str:
        """Get primary focus for each day"""
        focuses = {
            1: "Immediate symptom relief and baseline assessment",
            2: "Progressive intervention and pattern identification", 
            3: "Evaluation and long-term strategy development"
        }
        return focuses.get(day, "General wellness")
    
    def _get_morning_routine(self, day: int, symptoms: List[str]) -> List[str]:
        """Generate morning routine based on day and symptoms"""
        base_routine = [
            "Rate symptom intensity (0-10 scale) upon waking",
            "Hydrate with 16-20oz water",
            "5-10 minutes gentle movement or stretching"
        ]
        
        # Add symptom-specific items
        if "headache" in [s.lower() for s in symptoms]:
            base_routine.append("Check neck/shoulder tension, apply cold/heat as needed")
        
        if "fatigue" in [s.lower() for s in symptoms]:
            base_routine.append("Protein-rich breakfast within 1 hour of waking")
        
        if "bloating" in [s.lower() for s in symptoms]:
            base_routine.append("Warm lemon water, avoid inflammatory foods")
        
        # Day-specific additions
        if day == 1:
            base_routine.append("Establish baseline measurements and triggers")
        elif day == 2:
            base_routine.append("Review day 1 patterns, adjust interventions")
        elif day == 3:
            base_routine.append("Evaluate overall improvement and plan next steps")
        
        return base_routine
    
    def _get_midday_checkpoints(self, day: int) -> List[str]:
        """Generate midday checkpoint tasks"""
        checkpoints = [
            "Symptom intensity check (0-10 scale)",
            "Hydration check (aim for 6+ glasses by midday)",
            "Apply targeted relief measures if needed",
            "10-minute movement break or walk"
        ]
        
        if day >= 2:
            checkpoints.append("Compare symptoms to previous day same time")
        
        return checkpoints
    
    def _get_evening_routine(self, day: int, symptoms: List[str]) -> List[str]:
        """Generate evening routine"""
        routine = [
            "Final symptom intensity rating for the day",
            "Reflect on what helped/hindered today",
            "Prepare for optimal sleep (cool, dark, quiet)",
            "Relaxation technique (breathing, meditation, gentle yoga)"
        ]
        
        # Add symptom-specific evening care
        if any("sleep" in s.lower() for s in symptoms):
            routine.append("No screens 1 hour before bed, herbal tea")
        
        if any("digestive" in s.lower() or "bloat" in s.lower() for s in symptoms):
            routine.append("Light, early dinner (3+ hours before bed)")
        
        return routine
    
    def _get_tracking_requirements(self, day: int) -> Dict[str, str]:
        """Define what needs to be tracked each day"""
        return {
            "symptom_intensity": "Rate 0-10 scale, 3x daily (morning, midday, evening)",
            "interventions_used": "Note which remedies/activities were tried",
            "effectiveness": "Rate effectiveness of each intervention (0-10)",
            "triggers_identified": "Note potential triggers or patterns",
            "sleep_quality": "Rate sleep quality and duration",
            "energy_levels": "Rate energy throughout day (1-10)"
        }
    
    def _generate_milestones(self, symptom_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate progress milestones"""
        return [
            {
                "milestone": "24-Hour Initial Relief",
                "target_time": "Day 1 Evening",
                "success_criteria": "25-50% symptom improvement",
                "measurement": "Symptom intensity decreased by 2+ points"
            },
            {
                "milestone": "Pattern Recognition",
                "target_time": "Day 2 Midday", 
                "success_criteria": "Identified at least 2 triggers or helpful interventions",
                "measurement": "Clear correlation between actions and symptom changes"
            },
            {
                "milestone": "Sustainable Improvement",
                "target_time": "Day 3 Evening",
                "success_criteria": "50-70% overall improvement with plan for maintenance",
                "measurement": "Consistent symptom reduction + personalized strategy"
            }
        ]
    
    def _define_success_metrics(self, symptom_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Define success metrics for the plan"""
        return {
            "primary_metric": "Overall symptom intensity reduction",
            "target_improvement": "50-70% reduction in primary symptoms",
            "secondary_metrics": [
                "Improved sleep quality (if sleep affected)",
                "Increased energy levels (if fatigue present)", 
                "Enhanced daily functioning",
                "Reduced impact on life activities"
            ],
            "minimum_acceptable": "25% improvement in primary symptoms",
            "excellent_outcome": "75%+ improvement with clear maintenance strategy"
        }
    
    def _get_adjustment_triggers(self) -> List[str]:
        """Define when plan should be adjusted"""
        return [
            "No improvement after 24 hours",
            "Worsening symptoms despite interventions",
            "New symptoms appear",
            "Inability to complete plan activities",
            "Severe side effects from any intervention"
        ]

class MedicalAdvisorySystem:
    """Medical advisory and emergency detection system"""
    
    def __init__(self):
        self.emergency_contacts = {
            "emergency_services": "911", 
            "poison_control": "1-800-222-1222",
            "crisis_hotline": "988"
        }
        self.telemedicine_options = [
            {"name": "Teladoc", "availability": "24/7", "type": "General consultation"},
            {"name": "MDLive", "availability": "24/7", "type": "Urgent care"},
            {"name": "PlushCare", "availability": "Mon-Fri 8am-10pm", "type": "Primary care"}
        ]
    
    def assess_medical_urgency(self, symptom_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Assess medical urgency and provide guidance"""
        
        alert_level = AlertLevel(symptom_profile.get("alert_level", "green"))
        severity_score = symptom_profile.get("severity_score", 0)
        symptoms = symptom_profile.get("primary_symptoms", [])
        
        # Generate medical advisory
        advisory = {
            "alert_level": alert_level.value,
            "urgency_assessment": self._get_urgency_message(alert_level),
            "recommended_action": self._get_recommended_action(alert_level),
            "timeline": self._get_action_timeline(alert_level),
            "emergency_contacts": self._get_relevant_contacts(alert_level),
            "telemedicine_options": self._get_telemedicine_recommendations(alert_level),
            "red_flags_to_watch": self._get_red_flags_to_monitor(),
            "disclaimer": "This is not medical advice. Always consult healthcare professionals for medical concerns."
        }
        
        return advisory
    
    def _get_urgency_message(self, alert_level: AlertLevel) -> str:
        """Get urgency message based on alert level"""
        messages = {
            AlertLevel.GREEN: "Your symptoms appear manageable with home care. Continue monitoring and self-care measures.",
            AlertLevel.YELLOW: "Your symptoms warrant monitoring. If they persist or worsen, consider medical consultation within 24-48 hours.",
            AlertLevel.RED: "Your symptoms are concerning and should be evaluated by a healthcare provider within 24 hours.",
            AlertLevel.EMERGENCY: "Your symptoms require immediate medical attention. Seek emergency care or call 911 now."
        }
        return messages.get(alert_level, "Please consult with a healthcare provider.")
    
    def _get_recommended_action(self, alert_level: AlertLevel) -> List[str]:
        """Get recommended actions based on alert level"""
        actions = {
            AlertLevel.GREEN: [
                "Continue with self-care and symptom monitoring",
                "Follow the 3-day action plan provided",
                "Track symptoms and response to interventions",
                "Seek medical advice if symptoms worsen or persist beyond 3 days"
            ],
            AlertLevel.YELLOW: [
                "Begin self-care measures while monitoring closely",
                "Schedule appointment with healthcare provider if no improvement in 24-48 hours",
                "Avoid strenuous activities until symptoms improve",
                "Keep emergency contacts readily available"
            ],
            AlertLevel.RED: [
                "Contact healthcare provider or urgent care within 24 hours",
                "Do not delay seeking medical attention",
                "Continue safe symptom management while arranging care",
                "Inform someone about your symptoms"
            ],
            AlertLevel.EMERGENCY: [
                "Call 911 or go to emergency room immediately",
                "Do not drive yourself - call emergency services or have someone drive you",
                "If alone, call someone to be with you",
                "Bring list of current medications and medical history"
            ]
        }
        return actions.get(alert_level, ["Consult healthcare provider"])
    
    def _get_action_timeline(self, alert_level: AlertLevel) -> str:
        """Get action timeline based on alert level"""
        timelines = {
            AlertLevel.GREEN: "Monitor for 72 hours, seek help if no improvement",
            AlertLevel.YELLOW: "Seek medical advice within 24-48 hours if no improvement",
            AlertLevel.RED: "Seek medical attention within 24 hours",
            AlertLevel.EMERGENCY: "Seek immediate medical attention now"
        }
        return timelines.get(alert_level, "Consult healthcare provider as appropriate")
    
    def _get_relevant_contacts(self, alert_level: AlertLevel) -> Dict[str, str]:
        """Get relevant emergency contacts"""
        if alert_level == AlertLevel.EMERGENCY:
            return self.emergency_contacts
        elif alert_level == AlertLevel.RED:
            return {"urgent_care": "Contact local urgent care", "primary_doctor": "Call your primary care physician"}
        else:
            return {"primary_doctor": "Contact your primary care physician if symptoms persist"}
    
    def _get_telemedicine_recommendations(self, alert_level: AlertLevel) -> List[Dict]:
        """Get telemedicine options based on urgency"""
        if alert_level in [AlertLevel.GREEN, AlertLevel.YELLOW]:
            return self.telemedicine_options
        else:
            return []  # In-person care recommended for red/emergency
    
    def _get_red_flags_to_monitor(self) -> List[str]:
        """Get red flag symptoms to watch for"""
        return [
            "Chest pain or pressure",
            "Difficulty breathing or shortness of breath",
            "Severe headache with sudden onset",
            "High fever with confusion or altered mental state",
            "Persistent vomiting or inability to keep fluids down",
            "Severe abdominal pain",
            "Signs of allergic reaction (rash, swelling, difficulty breathing)",
            "Loss of consciousness or fainting",
            "Severe bleeding",
            "Symptoms that rapidly worsen despite treatment"
        ]