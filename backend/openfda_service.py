"""
OpenFDA API Integration Service for Drug Information and Interactions
"""
import os
import requests
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class OpenFDAService:
    def __init__(self):
        self.api_key = os.getenv("OPENFDA_API_KEY")
        self.base_url = "https://api.fda.gov"
        
    async def get_drug_interactions(self, drug_name: str) -> Dict[str, Any]:
        """Get drug interaction information from OpenFDA"""
        try:
            async with aiohttp.ClientSession() as session:
                # Search for drug information
                url = f"{self.base_url}/drug/label.json"
                params = {
                    "api_key": self.api_key,
                    "search": f"openfda.brand_name:{drug_name}",
                    "limit": 1
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_drug_interactions(data)
                    else:
                        logger.warning(f"OpenFDA API error: {response.status}")
                        return self._fallback_drug_info(drug_name)
                        
        except Exception as e:
            logger.error(f"Error fetching drug interactions: {e}")
            return self._fallback_drug_info(drug_name)
    
    async def get_adverse_events(self, drug_name: str, limit: int = 10) -> Dict[str, Any]:
        """Get adverse event reports for a drug"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/drug/event.json"
                params = {
                    "api_key": self.api_key,
                    "search": f"patient.drug.medicinalproduct:{drug_name}",
                    "count": "patient.reaction.reactionmeddrapt.exact",
                    "limit": limit
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_adverse_events(data)
                    else:
                        return {"adverse_events": [], "total_reports": 0}
                        
        except Exception as e:
            logger.error(f"Error fetching adverse events: {e}")
            return {"adverse_events": [], "total_reports": 0}
    
    async def check_drug_food_interactions(self, drug_name: str) -> Dict[str, Any]:
        """Check for drug-food interactions"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/drug/label.json"
                params = {
                    "api_key": self.api_key,
                    "search": f"openfda.brand_name:{drug_name}",
                    "limit": 1
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_food_interactions(data)
                    else:
                        return self._fallback_food_interactions(drug_name)
                        
        except Exception as e:
            logger.error(f"Error checking food interactions: {e}")
            return self._fallback_food_interactions(drug_name)
    
    async def get_drug_safety_info(self, drug_name: str) -> Dict[str, Any]:
        """Get comprehensive drug safety information"""
        try:
            # Run multiple requests concurrently
            interactions_task = self.get_drug_interactions(drug_name)
            adverse_events_task = self.get_adverse_events(drug_name)
            food_interactions_task = self.check_drug_food_interactions(drug_name)
            
            interactions, adverse_events, food_interactions = await asyncio.gather(
                interactions_task, adverse_events_task, food_interactions_task
            )
            
            return {
                "drug_name": drug_name,
                "interactions": interactions,
                "adverse_events": adverse_events,
                "food_interactions": food_interactions,
                "safety_score": self._calculate_safety_score(interactions, adverse_events),
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting drug safety info: {e}")
            return self._fallback_safety_info(drug_name)
    
    def _process_drug_interactions(self, data: Dict) -> Dict[str, Any]:
        """Process drug interaction data from OpenFDA response"""
        if not data.get("results"):
            return {"interactions": [], "warnings": []}
        
        result = data["results"][0]
        interactions = []
        warnings = []
        
        # Extract drug interactions
        if "drug_interactions" in result:
            for interaction in result["drug_interactions"][:5]:  # Limit to top 5
                interactions.append({
                    "type": "drug_interaction",
                    "description": interaction,
                    "severity": "moderate"  # Default severity
                })
        
        # Extract warnings
        if "warnings" in result:
            for warning in result["warnings"][:3]:  # Limit to top 3
                warnings.append({
                    "type": "warning",
                    "description": warning,
                    "severity": "high"
                })
        
        return {
            "interactions": interactions,
            "warnings": warnings,
            "total_interactions": len(interactions)
        }
    
    def _process_adverse_events(self, data: Dict) -> Dict[str, Any]:
        """Process adverse event data"""
        if not data.get("results"):
            return {"adverse_events": [], "total_reports": 0}
        
        adverse_events = []
        for event in data["results"][:10]:  # Top 10 adverse events
            adverse_events.append({
                "reaction": event.get("term", "Unknown reaction"),
                "count": event.get("count", 0),
                "severity": self._classify_severity(event.get("term", ""))
            })
        
        return {
            "adverse_events": adverse_events,
            "total_reports": sum(event["count"] for event in adverse_events)
        }
    
    def _process_food_interactions(self, data: Dict) -> Dict[str, Any]:
        """Process food interaction data"""
        if not data.get("results"):
            return self._fallback_food_interactions("unknown")
        
        result = data["results"][0]
        food_interactions = []
        
        # Look for food-related warnings in various fields
        food_keywords = ["food", "meal", "dairy", "alcohol", "grapefruit", "caffeine"]
        
        # Check precautions and warnings
        for field in ["precautions", "warnings", "drug_interactions"]:
            if field in result:
                for item in result[field]:
                    if any(keyword.lower() in item.lower() for keyword in food_keywords):
                        food_interactions.append({
                            "type": "food_interaction",
                            "description": item,
                            "recommendation": self._get_food_recommendation(item)
                        })
        
        return {
            "food_interactions": food_interactions[:5],  # Limit to 5 most relevant
            "general_advice": "Take as directed by healthcare provider"
        }
    
    def _calculate_safety_score(self, interactions: Dict, adverse_events: Dict) -> float:
        """Calculate overall safety score (0-100, higher is safer)"""
        base_score = 85.0
        
        # Reduce score based on interactions
        interaction_count = interactions.get("total_interactions", 0)
        base_score -= min(interaction_count * 5, 30)
        
        # Reduce score based on adverse events
        total_reports = adverse_events.get("total_reports", 0)
        if total_reports > 1000:
            base_score -= 10
        elif total_reports > 100:
            base_score -= 5
        
        return max(base_score, 0)
    
    def _classify_severity(self, reaction: str) -> str:
        """Classify reaction severity based on keywords"""
        severe_keywords = ["death", "fatal", "severe", "serious", "hospitalization"]
        moderate_keywords = ["nausea", "headache", "dizziness", "rash", "pain"]
        
        reaction_lower = reaction.lower()
        
        if any(keyword in reaction_lower for keyword in severe_keywords):
            return "severe"
        elif any(keyword in reaction_lower for keyword in moderate_keywords):
            return "moderate"
        else:
            return "mild"
    
    def _get_food_recommendation(self, interaction: str) -> str:
        """Generate food recommendation based on interaction text"""
        interaction_lower = interaction.lower()
        
        if "food" in interaction_lower:
            return "Take with food to reduce stomach irritation"
        elif "empty stomach" in interaction_lower:
            return "Take on empty stomach for better absorption"
        elif "dairy" in interaction_lower:
            return "Avoid dairy products 2 hours before/after taking"
        elif "alcohol" in interaction_lower:
            return "Avoid alcohol while taking this medication"
        elif "grapefruit" in interaction_lower:
            return "Avoid grapefruit and grapefruit juice"
        else:
            return "Follow prescriber's instructions regarding food"
    
    def _fallback_drug_info(self, drug_name: str) -> Dict[str, Any]:
        """Fallback drug information when OpenFDA is unavailable"""
        return {
            "interactions": [
                {
                    "type": "general_warning",
                    "description": f"Consult healthcare provider about potential interactions with {drug_name}",
                    "severity": "moderate"
                }
            ],
            "warnings": [
                {
                    "type": "general_precaution",
                    "description": "Follow prescribed dosage and timing",
                    "severity": "low"
                }
            ],
            "total_interactions": 1
        }
    
    def _fallback_food_interactions(self, drug_name: str) -> Dict[str, Any]:
        """Fallback food interaction info"""
        return {
            "food_interactions": [
                {
                    "type": "general_advice",
                    "description": "Take as directed by healthcare provider",
                    "recommendation": "Follow medication instructions regarding food"
                }
            ],
            "general_advice": "Consult pharmacist or doctor about food interactions"
        }
    
    def _fallback_safety_info(self, drug_name: str) -> Dict[str, Any]:
        """Fallback safety information"""
        return {
            "drug_name": drug_name,
            "interactions": self._fallback_drug_info(drug_name),
            "adverse_events": {"adverse_events": [], "total_reports": 0},
            "food_interactions": self._fallback_food_interactions(drug_name),
            "safety_score": 75.0,  # Neutral safety score
            "last_updated": datetime.utcnow().isoformat()
        }

# Global instance
openfda_service = OpenFDAService()