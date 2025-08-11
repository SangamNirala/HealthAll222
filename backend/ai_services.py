"""
AI Services Integration Module
Provides intelligent suggestions and insights using multiple AI APIs
"""

import os
import json
import asyncio
import random
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

class GeminiAPIRotator:
    """Handles rotation and fallback for multiple Gemini API keys"""
    
    def __init__(self):
        """Initialize with multiple Gemini API keys"""
        self.api_keys = self._load_gemini_keys()
        self.current_key_index = 0
        self.failed_keys = set()
        
    def _load_gemini_keys(self) -> List[str]:
        """Load Gemini API keys from environment"""
        keys_str = os.getenv('GEMINI_API_KEYS', '')
        if keys_str:
            return [key.strip() for key in keys_str.split(',') if key.strip()]
        
        # Fallback to single key if no multiple keys provided
        single_key = os.getenv('GEMINI_API_KEY')
        return [single_key] if single_key else []
    
    def get_current_key(self) -> Optional[str]:
        """Get current working API key"""
        if not self.api_keys:
            return None
            
        # Try to find a working key
        attempts = 0
        while attempts < len(self.api_keys):
            current_key = self.api_keys[self.current_key_index]
            
            if current_key not in self.failed_keys:
                return current_key
                
            # Move to next key
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            attempts += 1
        
        # If all keys failed, reset and try again
        if len(self.failed_keys) >= len(self.api_keys):
            logger.warning("All Gemini API keys failed. Resetting failed keys list.")
            self.failed_keys.clear()
            return self.api_keys[0] if self.api_keys else None
            
        return None
    
    def mark_key_failed(self, api_key: str):
        """Mark an API key as failed"""
        self.failed_keys.add(api_key)
        logger.warning(f"Marked Gemini API key as failed: {api_key[:20]}...")
        
    def rotate_key(self):
        """Rotate to next API key"""
        if len(self.api_keys) > 1:
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            logger.info(f"Rotated to Gemini API key index: {self.current_key_index}")

class AIServiceManager:
    def __init__(self):
        """Initialize AI service clients with API keys from environment"""
        self.groq_client = None
        self.gemini_rotator = GeminiAPIRotator()
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
            
            # Initialize Gemini with current key
            self._initialize_gemini_client()
            
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
    
    def _initialize_gemini_client(self):
        """Initialize Gemini client with current API key"""
        try:
            current_key = self.gemini_rotator.get_current_key()
            if current_key:
                genai.configure(api_key=current_key)
                self.gemini_client = genai.GenerativeModel('gemini-pro')
                logger.info(f"Gemini client initialized with key index: {self.gemini_rotator.current_key_index}")
            else:
                logger.error("No valid Gemini API key available")
                self.gemini_client = None
        except Exception as e:
            logger.error(f"Error initializing Gemini client: {str(e)}")
            self.gemini_client = None
    
    def _retry_with_gemini_rotation(self, func, *args, **kwargs):
        """Retry function with Gemini API key rotation on failure"""
        max_retries = len(self.gemini_rotator.api_keys)
        
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = str(e).lower()
                
                # Check if it's a rate limit or quota error
                if any(keyword in error_msg for keyword in ['quota', 'rate limit', 'exceeded', 'resource_exhausted']):
                    current_key = self.gemini_rotator.get_current_key()
                    if current_key:
                        self.gemini_rotator.mark_key_failed(current_key)
                        self.gemini_rotator.rotate_key()
                        self._initialize_gemini_client()
                        
                        if attempt < max_retries - 1:
                            logger.info(f"Retrying with next Gemini API key (attempt {attempt + 1}/{max_retries})")
                            continue
                
                # If not a rotation-worthy error or last attempt, raise the error
                if attempt == max_retries - 1:
                    raise e
        
        raise Exception("All Gemini API keys exhausted")

    async def generate_nutrition_insights(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized nutrition insights using AI"""
        try:
            # Create context from user data
            context = self._build_nutrition_context(user_data)
            
            # Use Groq for fast inference
            if self.groq_client:
                response = await self._groq_nutrition_analysis(context)
                return response
            
            # Fallback to Gemini with rotation
            elif self.gemini_client:
                response = await self._gemini_nutrition_analysis_with_rotation(context)
                return response
            
            # Default fallback
            return self._default_nutrition_insights(user_data)
            
        except Exception as e:
            logger.error(f"Error generating nutrition insights: {str(e)}")
            return self._default_nutrition_insights(user_data)

    async def _gemini_nutrition_analysis_with_rotation(self, context: str) -> Dict[str, Any]:
        """Use Gemini for nutrition analysis with API key rotation"""
        def _gemini_call():
            if not self.gemini_client:
                raise Exception("Gemini client not initialized")
                
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
            return response
        
        try:
            response = self._retry_with_gemini_rotation(_gemini_call)
            
            return {
                "source": "gemini",
                "model": "gemini-pro", 
                "api_key_index": self.gemini_rotator.current_key_index,
                "insights": self._parse_gemini_response(response.text),
                "recommendations": [],
                "correlations": [],
                "action_items": [],
                "confidence": 0.80
            }
            
        except Exception as e:
            logger.error(f"Gemini API error with rotation: {str(e)}")
            raise

    async def generate_goal_insights(self, goal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered goal insights and suggestions"""
        try:
            context = self._build_goal_context(goal_data)
            
            # Prefer Gemini for goal analysis
            if self.gemini_client:
                response = await self._gemini_goal_analysis_with_rotation(context)
                return response
            elif self.groq_client:
                response = await self._groq_goal_analysis(context)
                return response
            else:
                return self._default_goal_insights(goal_data)
                
        except Exception as e:
            logger.error(f"Error generating goal insights: {str(e)}")
            return self._default_goal_insights(goal_data)
    
    async def _gemini_goal_analysis_with_rotation(self, context: str) -> Dict[str, Any]:
        """Use Gemini for goal analysis with API key rotation"""
        def _gemini_goal_call():
            if not self.gemini_client:
                raise Exception("Gemini client not initialized")
                
            prompt = f"""
            As an AI goal optimization expert, analyze the user's goal data and provide intelligent insights:
            
            {context}
            
            Provide a JSON response with the following structure:
            {{
                "insights": ["insight1", "insight2", "insight3"],
                "recommendations": [
                    {{
                        "title": "recommendation title",
                        "description": "detailed description", 
                        "priority": "high|medium|low",
                        "timeline": "timeframe",
                        "success_probability": 0.85
                    }}
                ],
                "goal_adjustments": [
                    {{
                        "current_goal": "current goal",
                        "suggested_adjustment": "adjustment",
                        "reason": "why adjust"
                    }}
                ],
                "milestone_suggestions": [
                    {{
                        "milestone": "milestone name",
                        "target_date": "date",
                        "success_criteria": "criteria"
                    }}
                ]
            }}
            """
            
            response = self.gemini_client.generate_content(prompt)
            return response
        
        try:
            response = self._retry_with_gemini_rotation(_gemini_goal_call)
            
            # Try to parse JSON response
            try:
                parsed_response = json.loads(response.text)
                return {
                    "source": "gemini",
                    "model": "gemini-pro",
                    "api_key_index": self.gemini_rotator.current_key_index,
                    "insights": parsed_response.get("insights", []),
                    "recommendations": parsed_response.get("recommendations", []),
                    "goal_adjustments": parsed_response.get("goal_adjustments", []),
                    "milestone_suggestions": parsed_response.get("milestone_suggestions", []),
                    "confidence": 0.85
                }
            except json.JSONDecodeError:
                return self._parse_goal_text_response(response.text)
                
        except Exception as e:
            logger.error(f"Gemini goal analysis error: {str(e)}")
            raise

    async def generate_achievement_insights(self, achievement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights for achievement milestones"""
        try:
            context = self._build_achievement_context(achievement_data)
            
            if self.gemini_client:
                response = await self._gemini_achievement_analysis_with_rotation(context)
                return response
            else:
                return self._default_achievement_insights(achievement_data)
                
        except Exception as e:
            logger.error(f"Error generating achievement insights: {str(e)}")
            return self._default_achievement_insights(achievement_data)
    
    async def _gemini_achievement_analysis_with_rotation(self, context: str) -> Dict[str, Any]:
        """Use Gemini for achievement analysis with API key rotation"""
        def _gemini_achievement_call():
            if not self.gemini_client:
                raise Exception("Gemini client not initialized")
                
            prompt = f"""
            As an AI achievement specialist, analyze the user's progress and suggest meaningful achievement milestones:
            
            {context}
            
            Provide insights on:
            1. Recent achievements and their significance
            2. Upcoming milestone opportunities
            3. Motivation strategies based on progress patterns
            4. Achievement badge suggestions with descriptions
            5. Social sharing recommendations
            
            Format as actionable insights and specific achievement recommendations.
            """
            
            response = self.gemini_client.generate_content(prompt)
            return response
        
        try:
            response = self._retry_with_gemini_rotation(_gemini_achievement_call)
            
            return {
                "source": "gemini",
                "model": "gemini-pro",
                "api_key_index": self.gemini_rotator.current_key_index,
                "achievement_insights": self._parse_achievement_response(response.text),
                "confidence": 0.82
            }
            
        except Exception as e:
            logger.error(f"Gemini achievement analysis error: {str(e)}")
            raise

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

    def _build_goal_context(self, goal_data: Dict[str, Any]) -> str:
        """Build context string for goal analysis"""
        return f"""
        Goal Analysis Request:
        
        Current Goals:
        {json.dumps(goal_data.get('current_goals', []), indent=2)}
        
        User Profile:
        - Age: {goal_data.get('age', 'N/A')}
        - Activity Level: {goal_data.get('activity_level', 'N/A')}
        - Health Conditions: {goal_data.get('health_conditions', [])}
        
        Progress Data:
        - Goal completion rate: {goal_data.get('completion_rate', 'N/A')}%
        - Average time to complete goals: {goal_data.get('avg_completion_time', 'N/A')} days
        - Most successful goal types: {goal_data.get('successful_types', [])}
        - Challenging areas: {goal_data.get('challenging_areas', [])}
        
        Recent Performance:
        - Last 7 days goal adherence: {goal_data.get('week_adherence', 'N/A')}%
        - Longest streak: {goal_data.get('longest_streak', 'N/A')} days
        - Current streak: {goal_data.get('current_streak', 'N/A')} days
        
        Please provide intelligent goal insights and optimization recommendations.
        """
    
    def _build_achievement_context(self, achievement_data: Dict[str, Any]) -> str:
        """Build context string for achievement analysis"""
        return f"""
        Achievement Analysis Request:
        
        Recent Achievements:
        {json.dumps(achievement_data.get('recent_achievements', []), indent=2)}
        
        User Progress:
        - Total achievements unlocked: {achievement_data.get('total_achievements', 0)}
        - Current level/tier: {achievement_data.get('current_level', 'N/A')}
        - Points/score: {achievement_data.get('total_points', 0)}
        
        Goal Categories:
        - Nutrition goals: {achievement_data.get('nutrition_goals', 0)} completed
        - Fitness goals: {achievement_data.get('fitness_goals', 0)} completed  
        - Wellness goals: {achievement_data.get('wellness_goals', 0)} completed
        - Learning goals: {achievement_data.get('learning_goals', 0)} completed
        
        Progress Patterns:
        - Most active day of week: {achievement_data.get('most_active_day', 'N/A')}
        - Average daily goal progress: {achievement_data.get('daily_progress', 'N/A')}%
        - Motivation level trend: {achievement_data.get('motivation_trend', 'N/A')}
        
        Please suggest meaningful achievements, milestones, and motivation strategies.
        """
    
    def _parse_goal_text_response(self, text: str) -> Dict[str, Any]:
        """Parse goal insights from text response"""
        return {
            "source": "gemini",
            "model": "gemini-pro", 
            "api_key_index": self.gemini_rotator.current_key_index,
            "insights": ["Goal analysis completed successfully"],
            "recommendations": [{"title": "Continue Progress", "description": text[:200] + "...", "priority": "medium", "timeline": "1-2 weeks", "success_probability": 0.75}],
            "goal_adjustments": [],
            "milestone_suggestions": [],
            "confidence": 0.70
        }
    
    def _parse_achievement_response(self, text: str) -> Dict[str, Any]:
        """Parse achievement insights from text response"""
        lines = text.split('\n')
        insights = []
        recommendations = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['achievement', 'milestone', 'badge']):
                insights.append(line.strip())
            elif any(keyword in line.lower() for keyword in ['suggest', 'recommend', 'try']):
                recommendations.append(line.strip())
        
        return {
            "achievements": insights[:3] if insights else ["You're making great progress!"],
            "milestone_suggestions": recommendations[:3] if recommendations else ["Keep up the great work!"],
            "motivation_tips": ["Stay consistent", "Celebrate small wins", "Track your progress"],
            "social_sharing_ideas": ["Share your latest achievement", "Inspire others with your progress"]
        }
    
    def _default_goal_insights(self, goal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Provide default goal insights when AI services are unavailable"""
        return {
            "source": "default",
            "insights": [
                "Your goal progress shows consistent effort",
                "Consider breaking large goals into smaller milestones",
                "Regular review and adjustment improve success rates"
            ],
            "recommendations": [
                {
                    "title": "Weekly Goal Review",
                    "description": "Set aside time each week to review progress and adjust goals as needed",
                    "priority": "high",
                    "timeline": "Weekly",
                    "success_probability": 0.80
                },
                {
                    "title": "Milestone Tracking",
                    "description": "Break larger goals into smaller, achievable milestones",
                    "priority": "medium", 
                    "timeline": "2-4 weeks",
                    "success_probability": 0.75
                }
            ],
            "goal_adjustments": [],
            "milestone_suggestions": [
                {
                    "milestone": "Complete 7 days of consistent progress",
                    "target_date": "Next week",
                    "success_criteria": "Daily goal completion"
                }
            ],
            "confidence": 0.60
        }
    
    def _default_achievement_insights(self, achievement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Provide default achievement insights when AI services are unavailable"""
        return {
            "source": "default",
            "achievement_insights": {
                "achievements": [
                    "You're building healthy habits consistently",
                    "Your progress shows dedication to your goals",
                    "Every small step counts toward your larger objectives"
                ],
                "milestone_suggestions": [
                    "Celebrate completing your current goal streak", 
                    "Share your progress with friends and family",
                    "Set a new personal best for goal completion"
                ],
                "motivation_tips": [
                    "Focus on progress, not perfection",
                    "Reward yourself for milestones achieved",
                    "Connect with others who share similar goals"
                ],
                "social_sharing_ideas": [
                    "Share your weekly goal completion rate",
                    "Post about a healthy habit you've maintained",
                    "Inspire others by sharing your goal journey"
                ]
            },
            "confidence": 0.60
        }

    async def _groq_goal_analysis(self, context: str) -> Dict[str, Any]:
        """Use Groq for goal analysis"""
        try:
            completion = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI goal optimization expert. Analyze user goal data and provide intelligent insights, recommendations, and milestone suggestions. Respond in JSON format with 'insights', 'recommendations', 'goal_adjustments', and 'milestone_suggestions' keys."
                    },
                    {"role": "user", "content": context}
                ],
                max_tokens=1200,
                temperature=0.7
            )
            
            response_text = completion.choices[0].message.content
            
            try:
                parsed_response = json.loads(response_text)
                return {
                    "source": "groq",
                    "model": "llama3-8b-8192",
                    "insights": parsed_response.get("insights", []),
                    "recommendations": parsed_response.get("recommendations", []),
                    "goal_adjustments": parsed_response.get("goal_adjustments", []),
                    "milestone_suggestions": parsed_response.get("milestone_suggestions", []),
                    "confidence": 0.85
                }
            except json.JSONDecodeError:
                return self._parse_goal_text_response(response_text)
                
        except Exception as e:
            logger.error(f"Groq goal analysis error: {str(e)}")
            raise

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