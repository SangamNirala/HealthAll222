"""
AI Services Integration Module
Provides intelligent suggestions and insights using multiple AI APIs
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# AI Service Imports
import openai
from groq import Groq
import google.generativeai as genai
from huggingface_hub import InferenceClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIServiceManager:
    def __init__(self):
        """Initialize AI service clients with API keys from environment"""
        self.groq_client = None
        self.gemini_client = None
        self.openrouter_client = None
        self.hf_client = None
        
        # Initialize clients with API keys
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize AI service clients"""
        try:
            # Groq Client (Fast inference)
            if os.getenv('GROQ_API_KEY'):
                self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
                logger.info("Groq client initialized successfully")
            
            # Gemini Client
            if os.getenv('GEMINI_API_KEY'):
                genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
                self.gemini_client = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini client initialized successfully")
            
            # OpenRouter Client
            if os.getenv('OPENROUTER_API_KEY'):
                self.openrouter_client = openai.OpenAI(
                    api_key=os.getenv('OPENROUTER_API_KEY'),
                    base_url="https://openrouter.ai/api/v1"
                )
                logger.info("OpenRouter client initialized successfully")
            
            # Hugging Face Client
            if os.getenv('HUGGING_FACE_API_KEY'):
                self.hf_client = InferenceClient(token=os.getenv('HUGGING_FACE_API_KEY'))
                logger.info("Hugging Face client initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing AI clients: {str(e)}")

    async def generate_nutrition_insights(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized nutrition insights using AI"""
        try:
            # Create context from user data
            context = self._build_nutrition_context(user_data)
            
            # Use Groq for fast inference
            if self.groq_client:
                response = await self._groq_nutrition_analysis(context)
                return response
            
            # Fallback to Gemini
            elif self.gemini_client:
                response = await self._gemini_nutrition_analysis(context)
                return response
            
            # Default fallback
            return self._default_nutrition_insights(user_data)
            
        except Exception as e:
            logger.error(f"Error generating nutrition insights: {str(e)}")
            return self._default_nutrition_insights(user_data)

    async def _groq_nutrition_analysis(self, context: str) -> Dict[str, Any]:
        """Use Groq for nutrition analysis"""
        try:
            completion = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a professional nutritionist AI. Provide personalized nutrition insights, recommendations, and correlations based on user data. Respond in JSON format with 'insights', 'recommendations', 'correlations', and 'action_items' keys."
                    },
                    {"role": "user", "content": context}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            response_text = completion.choices[0].message.content
            
            # Try to parse JSON response
            try:
                parsed_response = json.loads(response_text)
                return {
                    "source": "groq",
                    "model": "llama3-8b-8192",
                    "insights": parsed_response.get("insights", []),
                    "recommendations": parsed_response.get("recommendations", []),
                    "correlations": parsed_response.get("correlations", []),
                    "action_items": parsed_response.get("action_items", []),
                    "confidence": 0.85
                }
            except json.JSONDecodeError:
                # If not JSON, extract key insights from text
                return self._extract_insights_from_text(response_text, "groq")
                
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            raise

    async def _gemini_nutrition_analysis(self, context: str) -> Dict[str, Any]:
        """Use Gemini for nutrition analysis"""
        try:
            prompt = f"""
            As a professional nutritionist AI, analyze the following user data and provide personalized insights:
            
            {context}
            
            Please provide:
            1. Key nutritional insights
            2. Personalized recommendations
            3. Health correlations identified
            4. Actionable next steps
            
            Format your response as clear, actionable advice.
            """
            
            response = self.gemini_client.generate_content(prompt)
            
            return {
                "source": "gemini",
                "model": "gemini-pro",
                "insights": self._parse_gemini_response(response.text),
                "recommendations": [],
                "correlations": [],
                "action_items": [],
                "confidence": 0.80
            }
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise

    async def generate_smart_food_suggestions(self, user_profile: Dict[str, Any], current_intake: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate AI-powered food suggestions based on user patterns"""
        try:
            context = self._build_food_suggestion_context(user_profile, current_intake)
            
            if self.groq_client:
                suggestions = await self._groq_food_suggestions(context)
                return suggestions
            elif self.gemini_client:
                suggestions = await self._gemini_food_suggestions(context)
                return suggestions
            else:
                return self._default_food_suggestions(user_profile, current_intake)
                
        except Exception as e:
            logger.error(f"Error generating food suggestions: {str(e)}")
            return self._default_food_suggestions(user_profile, current_intake)

    async def _groq_food_suggestions(self, context: str) -> List[Dict[str, Any]]:
        """Generate food suggestions using Groq"""
        try:
            completion = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a nutrition AI that suggests foods based on user preferences, nutritional needs, and eating patterns. Provide 4-6 specific food suggestions with reasons. Respond in JSON format with 'suggestions' array containing objects with 'name', 'calories', 'reason', 'nutrition_benefits', and 'meal_type' keys."
                    },
                    {"role": "user", "content": context}
                ],
                max_tokens=800,
                temperature=0.6
            )
            
            response_text = completion.choices[0].message.content
            
            try:
                parsed_response = json.loads(response_text)
                return parsed_response.get("suggestions", [])
            except json.JSONDecodeError:
                return self._extract_food_suggestions_from_text(response_text)
                
        except Exception as e:
            logger.error(f"Groq food suggestions error: {str(e)}")
            return []

    async def generate_health_correlations(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate health correlations and patterns using AI"""
        try:
            context = self._build_correlation_context(health_data)
            
            if self.openrouter_client:
                correlations = await self._openrouter_correlations(context)
                return correlations
            elif self.gemini_client:
                correlations = await self._gemini_correlations(context)
                return correlations
            else:
                return self._default_correlations(health_data)
                
        except Exception as e:
            logger.error(f"Error generating correlations: {str(e)}")
            return self._default_correlations(health_data)

    async def _openrouter_correlations(self, context: str) -> Dict[str, Any]:
        """Generate correlations using OpenRouter"""
        try:
            response = self.openrouter_client.chat.completions.create(
                model="anthropic/claude-3-haiku",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a health data analyst AI. Identify correlations between dietary habits, lifestyle factors, and health outcomes. Provide statistical insights and actionable recommendations."
                    },
                    {"role": "user", "content": context}
                ],
                max_tokens=600,
                temperature=0.4
            )
            
            content = response.choices[0].message.content
            
            return {
                "source": "openrouter",
                "model": "claude-3-haiku",
                "correlations": self._parse_correlation_response(content),
                "confidence": 0.82
            }
            
        except Exception as e:
            logger.error(f"OpenRouter correlations error: {str(e)}")
            return {}

    async def generate_clinical_insights(self, provider_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate clinical insights for healthcare providers"""
        try:
            context = self._build_clinical_context(provider_data)
            
            if self.openrouter_client:
                insights = await self._openrouter_clinical_analysis(context)
                return insights
            elif self.gemini_client:
                insights = await self._gemini_clinical_analysis(context)
                return insights
            else:
                return self._default_clinical_insights(provider_data)
                
        except Exception as e:
            logger.error(f"Error generating clinical insights: {str(e)}")
            return self._default_clinical_insights(provider_data)

    def _build_nutrition_context(self, user_data: Dict[str, Any]) -> str:
        """Build context string for nutrition analysis"""
        return f"""
        User Profile Analysis Request:
        
        Demographics: Age {user_data.get('age', 'N/A')}, Gender: {user_data.get('gender', 'N/A')}
        Activity Level: {user_data.get('activity_level', 'N/A')}
        Health Goals: {user_data.get('goals', [])}
        Current Diet: {user_data.get('diet_type', 'N/A')}
        
        Recent Nutrition Data:
        - Calories: {user_data.get('avg_calories', 'N/A')}
        - Protein: {user_data.get('avg_protein', 'N/A')}g
        - Carbs: {user_data.get('avg_carbs', 'N/A')}g
        - Fat: {user_data.get('avg_fat', 'N/A')}g
        
        Health Metrics:
        - Weight: {user_data.get('weight', 'N/A')}kg
        - Energy Level: {user_data.get('energy_level', 'N/A')}/10
        - Sleep Quality: {user_data.get('sleep_quality', 'N/A')}/10
        
        Please provide personalized nutrition insights and recommendations.
        """

    def _build_food_suggestion_context(self, profile: Dict[str, Any], intake: Dict[str, Any]) -> str:
        """Build context for food suggestions"""
        return f"""
        Food Suggestion Request:
        
        User Profile:
        - Dietary Preferences: {profile.get('diet_type', 'N/A')}
        - Allergies: {profile.get('allergies', [])}
        - Favorite Foods: {profile.get('favorite_foods', [])}
        - Cooking Time Available: {profile.get('cooking_time', 'N/A')} minutes
        
        Current Daily Intake:
        - Calories consumed: {intake.get('calories', 0)}
        - Protein: {intake.get('protein', 0)}g
        - Remaining calories needed: {intake.get('calories_remaining', 'N/A')}
        
        Time of day: {intake.get('time_of_day', 'N/A')}
        
        Suggest 4-6 appropriate foods that fit their preferences and nutritional needs.
        """

    def _build_correlation_context(self, health_data: Dict[str, Any]) -> str:
        """Build context for health correlations"""
        return f"""
        Health Correlation Analysis Request:
        
        Historical Data Available:
        - {len(health_data.get('daily_logs', []))} days of food/health logs
        - Sleep patterns: {health_data.get('sleep_patterns', 'N/A')}
        - Exercise frequency: {health_data.get('exercise_frequency', 'N/A')}
        - Stress levels: {health_data.get('stress_levels', 'N/A')}
        
        Health Outcomes:
        - Energy levels trend: {health_data.get('energy_trend', 'N/A')}
        - Weight trend: {health_data.get('weight_trend', 'N/A')}
        - Mood patterns: {health_data.get('mood_patterns', 'N/A')}
        - Digestive health: {health_data.get('digestive_health', 'N/A')}
        
        Identify significant correlations between lifestyle factors and health outcomes.
        """

    def _default_nutrition_insights(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Provide default nutrition insights when AI services are unavailable"""
        return {
            "source": "default",
            "insights": [
                "Based on your current intake, consider balancing your macronutrients",
                "Ensure adequate hydration throughout the day",
                "Include variety in your food choices for optimal nutrient coverage"
            ],
            "recommendations": [
                "Aim for 0.8-1g protein per kg body weight",
                "Include 5-7 servings of fruits and vegetables daily",
                "Stay hydrated with 8-10 glasses of water"
            ],
            "correlations": [],
            "action_items": [
                "Track your meals consistently",
                "Monitor energy levels after meals",
                "Plan meals in advance"
            ],
            "confidence": 0.60
        }

    def _default_food_suggestions(self, profile: Dict[str, Any], intake: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Provide default food suggestions"""
        return [
            {
                "name": "Greek Yogurt with Berries",
                "calories": 150,
                "reason": "High in protein and probiotics",
                "nutrition_benefits": ["Protein", "Calcium", "Probiotics"],
                "meal_type": "snack"
            },
            {
                "name": "Mixed Green Salad with Chickpeas",
                "calories": 250,
                "reason": "Rich in fiber and plant protein",
                "nutrition_benefits": ["Fiber", "Iron", "Folate"],
                "meal_type": "lunch"
            },
            {
                "name": "Grilled Salmon with Vegetables",
                "calories": 400,
                "reason": "Omega-3 fatty acids and complete protein",
                "nutrition_benefits": ["Omega-3", "Protein", "Vitamins"],
                "meal_type": "dinner"
            }
        ]

    def _extract_insights_from_text(self, text: str, source: str) -> Dict[str, Any]:
        """Extract insights from AI text response"""
        # Simple text parsing for insights
        lines = text.split('\n')
        insights = []
        recommendations = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['insight', 'notice', 'observe']):
                insights.append(line.strip())
            elif any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'try']):
                recommendations.append(line.strip())
        
        return {
            "source": source,
            "insights": insights[:3] if insights else ["Analysis completed successfully"],
            "recommendations": recommendations[:3] if recommendations else ["Continue current healthy practices"],
            "correlations": [],
            "action_items": ["Monitor progress", "Stay consistent", "Adjust as needed"],
            "confidence": 0.75
        }

# Global AI service manager instance
ai_service_manager = AIServiceManager()

# Utility functions for easy access
async def get_nutrition_insights(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Get AI-powered nutrition insights"""
    return await ai_service_manager.generate_nutrition_insights(user_data)

async def get_smart_food_suggestions(user_profile: Dict[str, Any], current_intake: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get AI-powered food suggestions"""
    return await ai_service_manager.generate_smart_food_suggestions(user_profile, current_intake)

async def get_health_correlations(health_data: Dict[str, Any]) -> Dict[str, Any]:
    """Get AI-powered health correlations"""
    return await ai_service_manager.generate_health_correlations(health_data)

async def get_clinical_insights(provider_data: Dict[str, Any]) -> Dict[str, Any]:
    """Get AI-powered clinical insights"""
    return await ai_service_manager.generate_clinical_insights(provider_data)