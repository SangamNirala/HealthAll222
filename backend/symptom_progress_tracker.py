# Symptom Progress Tracking and Analytics
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from motor.motor_asyncio import AsyncIOMotorClient
import uuid
import numpy as np
from statistics import mean, median

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SymptomProgressTracker:
    """Track progress and effectiveness of symptom relief plans"""
    
    def __init__(self, db):
        self.db = db
        
    async def log_progress_update(self, plan_id: str, user_id: str, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Log progress update for an action plan"""
        
        progress_entry = {
            "id": str(uuid.uuid4()),
            "plan_id": plan_id,
            "user_id": user_id,
            "timestamp": datetime.utcnow(),
            "day": progress_data.get("day", 1),
            "time_of_day": progress_data.get("time_of_day", "unknown"),
            "symptom_ratings": progress_data.get("symptom_ratings", {}),
            "interventions_used": progress_data.get("interventions_used", []),
            "intervention_effectiveness": progress_data.get("intervention_effectiveness", {}),
            "side_effects": progress_data.get("side_effects", []),
            "triggers_identified": progress_data.get("triggers_identified", []),
            "notes": progress_data.get("notes", ""),
            "overall_improvement": progress_data.get("overall_improvement", 0),
            "quality_of_life_impact": progress_data.get("quality_of_life_impact", 5),
            "sleep_quality": progress_data.get("sleep_quality", 5),
            "energy_level": progress_data.get("energy_level", 5)
        }
        
        # Store in database
        await self.db.symptom_progress.insert_one(progress_entry)
        
        # Calculate progress analytics
        analytics = await self.calculate_progress_analytics(plan_id, user_id)
        
        # Check if plan needs adjustment
        adjustment_needed = await self.assess_plan_adjustment_need(plan_id, user_id)
        
        return {
            "progress_logged": True,
            "entry_id": progress_entry["id"],
            "current_analytics": analytics,
            "adjustment_needed": adjustment_needed,
            "next_milestone": await self.get_next_milestone(plan_id)
        }
    
    async def calculate_progress_analytics(self, plan_id: str, user_id: str) -> Dict[str, Any]:
        """Calculate comprehensive progress analytics"""
        
        # Get all progress entries for this plan
        cursor = self.db.symptom_progress.find({
            "plan_id": plan_id,
            "user_id": user_id
        }).sort("timestamp", 1)
        
        entries = await cursor.to_list(length=None)
        
        if not entries:
            return {"status": "no_data"}
        
        # Calculate various analytics
        analytics = {
            "total_entries": len(entries),
            "days_tracked": len(set(e.get("day", 1) for e in entries)),
            "symptom_trends": self._calculate_symptom_trends(entries),
            "intervention_effectiveness": self._calculate_intervention_effectiveness(entries),
            "overall_improvement_trend": self._calculate_improvement_trend(entries),
            "adherence_rate": self._calculate_adherence_rate(entries),
            "quality_metrics": self._calculate_quality_metrics(entries),
            "pattern_insights": self._identify_patterns(entries),
            "success_probability": self._calculate_success_probability(entries)
        }
        
        return analytics
    
    def _calculate_symptom_trends(self, entries: List[Dict]) -> Dict[str, Any]:
        """Calculate symptom intensity trends"""
        symptom_data = {}
        
        for entry in entries:
            ratings = entry.get("symptom_ratings", {})
            day = entry.get("day", 1)
            time_of_day = entry.get("time_of_day", "unknown")
            
            for symptom, rating in ratings.items():
                if symptom not in symptom_data:
                    symptom_data[symptom] = []
                
                symptom_data[symptom].append({
                    "day": day,
                    "time": time_of_day,
                    "rating": rating,
                    "timestamp": entry.get("timestamp")
                })
        
        # Calculate trends for each symptom
        trends = {}
        for symptom, data_points in symptom_data.items():
            if len(data_points) >= 2:
                ratings = [d["rating"] for d in data_points]
                initial_rating = ratings[0]
                latest_rating = ratings[-1]
                
                trends[symptom] = {
                    "initial_rating": initial_rating,
                    "latest_rating": latest_rating,
                    "improvement": initial_rating - latest_rating,
                    "percent_improvement": ((initial_rating - latest_rating) / initial_rating * 100) if initial_rating > 0 else 0,
                    "trend_direction": self._get_trend_direction(ratings),
                    "average_rating": mean(ratings),
                    "best_rating": min(ratings),
                    "consistency": self._calculate_rating_consistency(ratings)
                }
        
        return trends
    
    def _calculate_intervention_effectiveness(self, entries: List[Dict]) -> Dict[str, Any]:
        """Calculate effectiveness of different interventions"""
        intervention_data = {}
        
        for entry in entries:
            interventions = entry.get("interventions_used", [])
            effectiveness = entry.get("intervention_effectiveness", {})
            overall_improvement = entry.get("overall_improvement", 0)
            
            for intervention in interventions:
                if intervention not in intervention_data:
                    intervention_data[intervention] = {
                        "usage_count": 0,
                        "effectiveness_ratings": [],
                        "associated_improvements": []
                    }
                
                intervention_data[intervention]["usage_count"] += 1
                
                if intervention in effectiveness:
                    intervention_data[intervention]["effectiveness_ratings"].append(effectiveness[intervention])
                
                intervention_data[intervention]["associated_improvements"].append(overall_improvement)
        
        # Calculate effectiveness metrics
        effectiveness_summary = {}
        for intervention, data in intervention_data.items():
            if data["effectiveness_ratings"]:
                avg_effectiveness = mean(data["effectiveness_ratings"])
                avg_improvement = mean(data["associated_improvements"])
                
                effectiveness_summary[intervention] = {
                    "usage_count": data["usage_count"],
                    "average_effectiveness": round(avg_effectiveness, 2),
                    "average_improvement_when_used": round(avg_improvement, 2),
                    "reliability_score": self._calculate_reliability_score(data["effectiveness_ratings"]),
                    "recommendation_level": self._get_recommendation_level(avg_effectiveness, data["usage_count"])
                }
        
        return effectiveness_summary
    
    def _calculate_improvement_trend(self, entries: List[Dict]) -> Dict[str, Any]:
        """Calculate overall improvement trend"""
        if len(entries) < 2:
            return {"status": "insufficient_data"}
        
        improvements = [entry.get("overall_improvement", 0) for entry in entries]
        timestamps = [entry.get("timestamp") for entry in entries]
        
        # Calculate trend
        initial_improvement = improvements[0]
        latest_improvement = improvements[-1]
        peak_improvement = max(improvements)
        
        return {
            "initial_improvement": initial_improvement,
            "latest_improvement": latest_improvement,
            "peak_improvement": peak_improvement,
            "average_improvement": round(mean(improvements), 2),
            "improvement_velocity": self._calculate_improvement_velocity(improvements, timestamps),
            "trend_direction": self._get_trend_direction(improvements),
            "consistency": self._calculate_rating_consistency(improvements),
            "trajectory": self._analyze_improvement_trajectory(improvements)
        }
    
    def _calculate_adherence_rate(self, entries: List[Dict]) -> Dict[str, Any]:
        """Calculate plan adherence rate"""
        expected_entries_per_day = 3  # morning, midday, evening
        days_in_plan = max([entry.get("day", 1) for entry in entries]) if entries else 0
        expected_total_entries = days_in_plan * expected_entries_per_day
        
        actual_entries = len(entries)
        adherence_rate = (actual_entries / expected_total_entries * 100) if expected_total_entries > 0 else 0
        
        # Calculate daily adherence
        daily_adherence = {}
        for entry in entries:
            day = entry.get("day", 1)
            if day not in daily_adherence:
                daily_adherence[day] = 0
            daily_adherence[day] += 1
        
        daily_adherence_rates = {
            day: (count / expected_entries_per_day * 100) 
            for day, count in daily_adherence.items()
        }
        
        return {
            "overall_adherence_rate": round(adherence_rate, 2),
            "daily_adherence_rates": daily_adherence_rates,
            "expected_entries": expected_total_entries,
            "actual_entries": actual_entries,
            "adherence_level": self._get_adherence_level(adherence_rate)
        }
    
    def _calculate_quality_metrics(self, entries: List[Dict]) -> Dict[str, Any]:
        """Calculate quality of life and related metrics"""
        qol_scores = [entry.get("quality_of_life_impact", 5) for entry in entries]
        sleep_scores = [entry.get("sleep_quality", 5) for entry in entries]
        energy_scores = [entry.get("energy_level", 5) for entry in entries]
        
        return {
            "quality_of_life": {
                "average": round(mean(qol_scores), 2) if qol_scores else 5,
                "trend": self._get_trend_direction(qol_scores),
                "improvement": qol_scores[-1] - qol_scores[0] if len(qol_scores) >= 2 else 0
            },
            "sleep_quality": {
                "average": round(mean(sleep_scores), 2) if sleep_scores else 5,
                "trend": self._get_trend_direction(sleep_scores),
                "improvement": sleep_scores[-1] - sleep_scores[0] if len(sleep_scores) >= 2 else 0
            },
            "energy_level": {
                "average": round(mean(energy_scores), 2) if energy_scores else 5,
                "trend": self._get_trend_direction(energy_scores),
                "improvement": energy_scores[-1] - energy_scores[0] if len(energy_scores) >= 2 else 0
            }
        }
    
    def _identify_patterns(self, entries: List[Dict]) -> List[Dict[str, Any]]:
        """Identify patterns in symptoms and interventions"""
        patterns = []
        
        # Time-of-day patterns
        time_patterns = self._analyze_time_patterns(entries)
        if time_patterns:
            patterns.extend(time_patterns)
        
        # Intervention patterns
        intervention_patterns = self._analyze_intervention_patterns(entries)
        if intervention_patterns:
            patterns.extend(intervention_patterns)
        
        # Trigger patterns
        trigger_patterns = self._analyze_trigger_patterns(entries)
        if trigger_patterns:
            patterns.extend(trigger_patterns)
        
        return patterns
    
    def _calculate_success_probability(self, entries: List[Dict]) -> Dict[str, Any]:
        """Calculate probability of plan success"""
        if len(entries) < 3:
            return {"status": "insufficient_data", "probability": 50}
        
        # Factors that indicate success
        improvement_trend = self._get_improvement_trend_score(entries)
        adherence_score = self._calculate_adherence_rate(entries)["overall_adherence_rate"]
        intervention_effectiveness_score = self._get_average_intervention_effectiveness(entries)
        
        # Weighted success probability
        success_probability = (
            improvement_trend * 0.4 +
            adherence_score * 0.3 +
            intervention_effectiveness_score * 0.3
        )
        
        return {
            "probability": round(min(success_probability, 95), 1),  # Cap at 95%
            "confidence": self._calculate_prediction_confidence(entries),
            "factors": {
                "improvement_trend": improvement_trend,
                "adherence": adherence_score,
                "intervention_effectiveness": intervention_effectiveness_score
            },
            "recommendation": self._get_success_recommendation(success_probability)
        }
    
    async def assess_plan_adjustment_need(self, plan_id: str, user_id: str) -> Dict[str, Any]:
        """Assess if the action plan needs adjustment"""
        
        analytics = await self.calculate_progress_analytics(plan_id, user_id)
        
        if analytics.get("status") == "no_data":
            return {"adjustment_needed": False, "reason": "insufficient_data"}
        
        adjustment_indicators = []
        
        # Check improvement trend
        improvement_trend = analytics.get("overall_improvement_trend", {})
        if improvement_trend.get("trend_direction") == "declining":
            adjustment_indicators.append("declining_improvement")
        
        # Check adherence
        adherence = analytics.get("adherence_rate", {})
        if adherence.get("overall_adherence_rate", 0) < 60:
            adjustment_indicators.append("low_adherence")
        
        # Check intervention effectiveness
        effectiveness = analytics.get("intervention_effectiveness", {})
        low_effectiveness_count = sum(
            1 for data in effectiveness.values() 
            if data.get("average_effectiveness", 0) < 4
        )
        if low_effectiveness_count > len(effectiveness) / 2:
            adjustment_indicators.append("low_intervention_effectiveness")
        
        # Check symptom trends
        symptom_trends = analytics.get("symptom_trends", {})
        worsening_symptoms = sum(
            1 for trend in symptom_trends.values()
            if trend.get("improvement", 0) < 0
        )
        if worsening_symptoms > len(symptom_trends) / 2:
            adjustment_indicators.append("worsening_symptoms")
        
        adjustment_needed = len(adjustment_indicators) > 0
        
        return {
            "adjustment_needed": adjustment_needed,
            "indicators": adjustment_indicators,
            "severity": self._assess_adjustment_severity(adjustment_indicators),
            "recommendations": self._get_adjustment_recommendations(adjustment_indicators)
        }
    
    async def get_next_milestone(self, plan_id: str) -> Dict[str, Any]:
        """Get the next milestone for the plan"""
        
        # Get plan details
        plan = await self.db.action_plans.find_one({"plan_id": plan_id})
        
        if not plan:
            return {"status": "plan_not_found"}
        
        milestones = plan.get("progress_milestones", [])
        current_time = datetime.utcnow()
        
        # Find next upcoming milestone
        for milestone in milestones:
            milestone_time = self._parse_milestone_time(milestone.get("target_time", ""))
            if milestone_time and milestone_time > current_time:
                return {
                    "milestone": milestone.get("milestone", ""),
                    "target_time": milestone.get("target_time", ""),
                    "success_criteria": milestone.get("success_criteria", ""),
                    "measurement": milestone.get("measurement", ""),
                    "time_remaining": self._calculate_time_remaining(milestone_time)
                }
        
        return {"status": "no_upcoming_milestones"}
    
    # Helper methods
    def _get_trend_direction(self, values: List[float]) -> str:
        """Determine trend direction from a list of values"""
        if len(values) < 2:
            return "stable"
        
        # Simple linear trend analysis
        x = list(range(len(values)))
        correlation = np.corrcoef(x, values)[0, 1] if len(values) > 1 else 0
        
        if correlation > 0.3:
            return "improving"
        elif correlation < -0.3:
            return "declining"
        else:
            return "stable"
    
    def _calculate_rating_consistency(self, ratings: List[float]) -> float:
        """Calculate consistency score for ratings"""
        if len(ratings) < 2:
            return 1.0
        
        variance = np.var(ratings)
        mean_rating = np.mean(ratings)
        
        # Normalize consistency score (lower variance = higher consistency)
        consistency = max(0, 1 - (variance / (mean_rating + 1)))
        return round(consistency, 3)
    
    def _calculate_reliability_score(self, ratings: List[float]) -> float:
        """Calculate reliability score for intervention effectiveness"""
        if not ratings:
            return 0
        
        consistency = self._calculate_rating_consistency(ratings)
        average = mean(ratings) / 10  # Normalize to 0-1
        usage_factor = min(len(ratings) / 5, 1)  # More usage = more reliable
        
        return round((consistency + average + usage_factor) / 3, 3)
    
    def _get_recommendation_level(self, effectiveness: float, usage_count: int) -> str:
        """Get recommendation level for intervention"""
        if effectiveness >= 7 and usage_count >= 3:
            return "highly_recommended"
        elif effectiveness >= 5 and usage_count >= 2:
            return "recommended"
        elif effectiveness >= 3:
            return "neutral"
        else:
            return "not_recommended"
    
    def _calculate_improvement_velocity(self, improvements: List[float], timestamps: List[datetime]) -> float:
        """Calculate rate of improvement over time"""
        if len(improvements) < 2:
            return 0
        
        time_diff = (timestamps[-1] - timestamps[0]).total_seconds() / 3600  # Hours
        improvement_diff = improvements[-1] - improvements[0]
        
        return round(improvement_diff / max(time_diff, 1), 4)  # Improvement per hour
    
    def _analyze_improvement_trajectory(self, improvements: List[float]) -> str:
        """Analyze the trajectory of improvement"""
        if len(improvements) < 3:
            return "insufficient_data"
        
        # Check if improvement is accelerating, decelerating, or steady
        recent_slope = improvements[-1] - improvements[-2]
        early_slope = improvements[1] - improvements[0]
        
        if recent_slope > early_slope * 1.2:
            return "accelerating"
        elif recent_slope < early_slope * 0.8:
            return "decelerating"
        else:
            return "steady"
    
    def _get_adherence_level(self, adherence_rate: float) -> str:
        """Get adherence level description"""
        if adherence_rate >= 90:
            return "excellent"
        elif adherence_rate >= 75:
            return "good"
        elif adherence_rate >= 60:
            return "fair"
        else:
            return "poor"
    
    def _analyze_time_patterns(self, entries: List[Dict]) -> List[Dict]:
        """Analyze time-of-day patterns"""
        patterns = []
        
        # Group by time of day
        time_groups = {}
        for entry in entries:
            time = entry.get("time_of_day", "unknown")
            if time not in time_groups:
                time_groups[time] = []
            time_groups[time].append(entry)
        
        # Analyze patterns
        for time, time_entries in time_groups.items():
            if len(time_entries) >= 3:
                improvements = [e.get("overall_improvement", 0) for e in time_entries]
                avg_improvement = mean(improvements)
                
                if avg_improvement >= 6:
                    patterns.append({
                        "type": "time_pattern",
                        "pattern": f"Symptoms tend to be better in the {time}",
                        "confidence": min(len(time_entries) / 5, 1.0),
                        "recommendation": f"Focus relief efforts during {time} period"
                    })
        
        return patterns
    
    def _analyze_intervention_patterns(self, entries: List[Dict]) -> List[Dict]:
        """Analyze intervention effectiveness patterns"""
        patterns = []
        
        # Find consistently effective interventions
        intervention_effectiveness = {}
        for entry in entries:
            effectiveness = entry.get("intervention_effectiveness", {})
            for intervention, rating in effectiveness.items():
                if intervention not in intervention_effectiveness:
                    intervention_effectiveness[intervention] = []
                intervention_effectiveness[intervention].append(rating)
        
        for intervention, ratings in intervention_effectiveness.items():
            if len(ratings) >= 3 and mean(ratings) >= 7:
                patterns.append({
                    "type": "intervention_pattern",
                    "pattern": f"{intervention} consistently provides good relief",
                    "confidence": min(len(ratings) / 5, 1.0),
                    "recommendation": f"Continue using {intervention} regularly"
                })
        
        return patterns
    
    def _analyze_trigger_patterns(self, entries: List[Dict]) -> List[Dict]:
        """Analyze trigger patterns"""
        patterns = []
        
        # Collect all triggers mentioned
        trigger_count = {}
        for entry in entries:
            triggers = entry.get("triggers_identified", [])
            for trigger in triggers:
                trigger_count[trigger] = trigger_count.get(trigger, 0) + 1
        
        # Identify frequently mentioned triggers
        total_entries = len(entries)
        for trigger, count in trigger_count.items():
            if count >= max(3, total_entries * 0.3):  # At least 3 times or 30% of entries
                patterns.append({
                    "type": "trigger_pattern",
                    "pattern": f"'{trigger}' frequently triggers symptoms",
                    "confidence": min(count / total_entries, 1.0),
                    "recommendation": f"Focus on avoiding or managing '{trigger}'"
                })
        
        return patterns
    
    def _get_improvement_trend_score(self, entries: List[Dict]) -> float:
        """Get numeric score for improvement trend"""
        improvements = [entry.get("overall_improvement", 0) for entry in entries]
        
        if not improvements:
            return 50
        
        trend = self._get_trend_direction(improvements)
        latest_improvement = improvements[-1]
        
        if trend == "improving":
            return min(latest_improvement * 10 + 20, 100)
        elif trend == "declining":
            return max(latest_improvement * 10 - 20, 0)
        else:
            return latest_improvement * 10
    
    def _get_average_intervention_effectiveness(self, entries: List[Dict]) -> float:
        """Get average intervention effectiveness score"""
        all_ratings = []
        
        for entry in entries:
            effectiveness = entry.get("intervention_effectiveness", {})
            all_ratings.extend(effectiveness.values())
        
        if not all_ratings:
            return 50
        
        return mean(all_ratings) * 10  # Convert to 0-100 scale
    
    def _calculate_prediction_confidence(self, entries: List[Dict]) -> float:
        """Calculate confidence in success prediction"""
        factors = [
            len(entries) / 10,  # More data = higher confidence
            min(max([entry.get("day", 1) for entry in entries]) / 3, 1),  # More days = higher confidence
        ]
        
        return round(min(mean(factors), 1.0) * 100, 1)
    
    def _get_success_recommendation(self, probability: float) -> str:
        """Get recommendation based on success probability"""
        if probability >= 80:
            return "Continue current plan - excellent progress trajectory"
        elif probability >= 60:
            return "Continue with minor adjustments - good progress"
        elif probability >= 40:
            return "Consider plan modifications - moderate progress"
        else:
            return "Significant plan adjustments recommended - limited progress"
    
    def _assess_adjustment_severity(self, indicators: List[str]) -> str:
        """Assess severity of needed adjustments"""
        if "worsening_symptoms" in indicators:
            return "high"
        elif len(indicators) >= 3:
            return "moderate"
        elif len(indicators) >= 1:
            return "low"
        else:
            return "none"
    
    def _get_adjustment_recommendations(self, indicators: List[str]) -> List[str]:
        """Get specific adjustment recommendations"""
        recommendations = []
        
        if "declining_improvement" in indicators:
            recommendations.append("Review and modify intervention strategies")
        
        if "low_adherence" in indicators:
            recommendations.append("Simplify plan to improve adherence")
        
        if "low_intervention_effectiveness" in indicators:
            recommendations.append("Try alternative relief methods")
        
        if "worsening_symptoms" in indicators:
            recommendations.append("Consider medical consultation")
        
        return recommendations
    
    def _parse_milestone_time(self, target_time: str) -> Optional[datetime]:
        """Parse milestone target time"""
        # Simple parsing - in real implementation would be more sophisticated
        try:
            if "Day 1" in target_time:
                return datetime.utcnow() + timedelta(hours=12)
            elif "Day 2" in target_time:
                return datetime.utcnow() + timedelta(days=1, hours=12)
            elif "Day 3" in target_time:
                return datetime.utcnow() + timedelta(days=2, hours=12)
        except:
            pass
        return None
    
    def _calculate_time_remaining(self, milestone_time: datetime) -> str:
        """Calculate human-readable time remaining"""
        diff = milestone_time - datetime.utcnow()
        hours = diff.total_seconds() / 3600
        
        if hours < 1:
            return f"{int(diff.total_seconds() / 60)} minutes"
        elif hours < 24:
            return f"{int(hours)} hours"
        else:
            return f"{int(hours / 24)} days"