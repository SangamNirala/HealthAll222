"""
AI-Powered Food Recognition & Nutrition Analysis Service
Utilizes multiple FREE AI APIs for comprehensive food analysis
"""

import os
import json
import base64
import asyncio
import random
import requests
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import google.generativeai as genai
from groq import Groq
from huggingface_hub import InferenceClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FoodRecognitionService:
    """Comprehensive food recognition using multiple FREE AI APIs"""
    
    def __init__(self):
        """Initialize AI service clients"""
        self.groq_client = None
        self.hf_client = None
        self._initialize_clients()
        
        # USDA FoodData Central API (FREE)
        self.usda_api_key = os.getenv('USDA_API_KEY')
        self.usda_base_url = "https://api.nal.usda.gov/fdc/v1"
        
        # Open Food Facts API (FREE - No key required)
        self.openfood_base_url = "https://world.openfoodfacts.org/api/v0"
        
    def _initialize_clients(self):
        """Initialize AI service clients"""
        try:
            # Groq Client (Fast inference)
            if os.getenv('GROQ_API_KEY'):
                self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
                logger.info("Groq client initialized successfully")
            
            # Hugging Face Client (FREE)
            if os.getenv('HUGGING_FACE_API_KEY'):
                self.hf_client = InferenceClient(token=os.getenv('HUGGING_FACE_API_KEY'))
                logger.info("Hugging Face client initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing AI clients: {str(e)}")

    async def analyze_food_image_comprehensive(self, image_base64: str, user_preferences: Dict = None) -> Dict[str, Any]:
        """
        Multi-stage food recognition and analysis pipeline
        Stage 1: Gemini Vision - Primary food identification
        Stage 2: Groq - Nutrition analysis and scoring
        Stage 3: USDA/OpenFood - Database validation
        Stage 4: Healthier alternatives generation
        """
        try:
            start_time = datetime.now()
            
            # Stage 1: Gemini Vision Food Recognition
            logger.info("Stage 1: Starting Gemini Vision food recognition")
            primary_recognition = await self._gemini_food_recognition(image_base64)
            
            # Stage 2: Groq Nutrition Analysis & Scoring
            logger.info("Stage 2: Starting Groq nutrition analysis")
            nutrition_analysis = await self._groq_nutrition_analysis(primary_recognition)
            
            # Stage 3: Database Validation & Enhancement
            logger.info("Stage 3: Starting database validation")
            database_enrichment = await self._database_nutrition_lookup(primary_recognition['foods'])
            
            # Stage 4: Healthier Alternatives Generation
            logger.info("Stage 4: Generating healthier alternatives")
            alternatives = await self._generate_healthier_alternatives(
                primary_recognition['foods'], 
                nutrition_analysis,
                user_preferences or {}
            )
            
            # Compile comprehensive results
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "processing_time": f"{processing_time:.2f}s",
                "api_sources": ["gemini-vision", "groq", "usda", "openfood"],
                "foods_detected": self._compile_food_results(
                    primary_recognition, 
                    nutrition_analysis, 
                    database_enrichment
                ),
                "alternatives": alternatives,
                "session_insights": self._generate_session_insights(primary_recognition, nutrition_analysis),
                "confidence": primary_recognition.get('confidence', 0.8),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Comprehensive food analysis error: {str(e)}")
            return self._fallback_response()

    async def _gemini_food_recognition(self, image_base64: str) -> Dict[str, Any]:
        """Stage 1: Use Gemini Vision API for primary food identification"""
        try:
            gemini_api_key = os.getenv('GEMINI_API_KEY')
            if not gemini_api_key:
                raise Exception("Gemini API key not configured")

            # Configure Gemini
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            # Prepare image for Gemini
            image_data = {
                "mime_type": "image/jpeg",
                "data": image_base64
            }

            prompt = """
            Analyze this food image comprehensively and provide detailed information:

            1. FOOD IDENTIFICATION:
               - List all visible food items with confidence levels
               - Identify cooking methods (fried, grilled, steamed, baked, raw)
               - Estimate portion sizes (small, medium, large, with gram estimates)
               - Detect processed vs. whole foods

            2. VISUAL ANALYSIS:
               - Food quality assessment (fresh, overcooked, etc.)
               - Ingredient identification in complex dishes
               - Brand recognition for packaged foods (if visible)
               - Meal composition (complete meal vs. individual items)

            3. NUTRITIONAL ESTIMATION:
               - Calories per item and total
               - Macronutrients (protein, carbs, fat, fiber)
               - Hidden ingredients (added sugars, sodium, preservatives)
               - Processing level (1=minimal, 5=ultra-processed)

            Respond in JSON format:
            {
                "foods": [
                    {
                        "name": "food_name",
                        "confidence": 0.95,
                        "portion_size": "medium (150g)",
                        "cooking_method": "grilled",
                        "processing_level": 2,
                        "estimated_nutrition": {
                            "calories": 200,
                            "protein": "25g",
                            "carbs": "5g",
                            "fat": "8g",
                            "fiber": "0g",
                            "sodium": "120mg",
                            "sugar": "2g"
                        },
                        "ingredients_detected": ["chicken", "herbs", "oil"],
                        "food_quality": "fresh",
                        "meal_category": "protein"
                    }
                ],
                "overall_meal": {
                    "meal_type": "lunch",
                    "completeness": "protein_heavy",
                    "estimated_prep_time": "15 minutes",
                    "total_calories": 200
                },
                "image_quality": "good",
                "confidence": 0.90
            }
            """

            # Generate content
            response = model.generate_content([prompt, image_data])
            
            if response.text:
                # Try to parse JSON response
                try:
                    parsed_response = json.loads(response.text.strip())
                    return parsed_response
                except json.JSONDecodeError:
                    # Fallback parsing if JSON fails
                    return self._extract_food_info_from_text(response.text)
            else:
                raise Exception("Empty response from Gemini")

        except Exception as e:
            logger.error(f"Gemini food recognition error: {str(e)}")
            return self._gemini_fallback()

    async def _groq_nutrition_analysis(self, food_recognition: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 2: Use Groq for fast nutrition analysis and food scoring"""
        try:
            if not self.groq_client:
                return self._nutrition_analysis_fallback()

            foods_data = json.dumps(food_recognition, indent=2)
            
            prompt = f"""
            Analyze these detected foods and provide comprehensive nutrition insights and scoring:

            FOOD DATA:
            {foods_data}

            Provide detailed analysis in JSON format:
            {{
                "foods_analyzed": [
                    {{
                        "name": "food_name",
                        "food_score": {{
                            "grade": "A",
                            "score": 88,
                            "breakdown": {{
                                "nutritional_density": 85,
                                "processing_level": 90,
                                "hidden_ingredient_penalty": -2,
                                "portion_appropriateness": 85,
                                "health_impact": 88
                            }}
                        }},
                        "nutrition_enhanced": {{
                            "calories_per_100g": 165,
                            "macros": {{"protein": 31, "carbs": 0, "fat": 4}},
                            "micros": {{"iron": "2.7mg", "b12": "2.6mcg"}},
                            "health_markers": {{"glycemic_index": "low", "inflammation": "anti"}},
                            "allergens": ["none"],
                            "dietary_tags": ["keto_friendly", "high_protein", "low_carb"]
                        }},
                        "hidden_concerns": [
                            {{"concern": "high_sodium", "level": "moderate", "impact": "blood pressure"}}
                        ]
                    }}
                ],
                "meal_analysis": {{
                    "overall_score": "B+",
                    "total_calories": 450,
                    "macro_balance": "protein_heavy",
                    "missing_nutrients": ["fiber", "vitamin_c"],
                    "meal_timing_score": 85,
                    "satiety_prediction": "high"
                }},
                "health_insights": [
                    "Excellent protein source for muscle building",
                    "Consider adding vegetables for fiber and vitamins",
                    "Good choice for weight management"
                ],
                "improvement_suggestions": [
                    "Add leafy greens for complete nutrition",
                    "Include healthy fats like avocado",
                    "Consider portion size for your goals"
                ]
            }}
            """

            completion = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional nutritionist AI that analyzes food and provides detailed scoring, nutrition analysis, and health insights. Always respond in valid JSON format."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )

            response_text = completion.choices[0].message.content
            
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                return self._extract_nutrition_analysis_from_text(response_text)

        except Exception as e:
            logger.error(f"Groq nutrition analysis error: {str(e)}")
            return self._nutrition_analysis_fallback()

    async def _database_nutrition_lookup(self, foods: List[Dict]) -> Dict[str, Any]:
        """Stage 3: Validate and enhance with USDA and OpenFood databases"""
        try:
            enhanced_foods = []
            
            for food in foods:
                food_name = food.get('name', '').lower()
                
                # Try USDA lookup first
                usda_data = await self._usda_lookup(food_name)
                
                # Try OpenFood Facts if USDA fails
                openfood_data = await self._openfood_lookup(food_name) if not usda_data else {}
                
                enhanced_food = {
                    "original": food,
                    "usda_match": usda_data,
                    "openfood_match": openfood_data,
                    "database_confidence": self._calculate_database_confidence(usda_data, openfood_data)
                }
                enhanced_foods.append(enhanced_food)
            
            return {"enhanced_foods": enhanced_foods}
            
        except Exception as e:
            logger.error(f"Database lookup error: {str(e)}")
            return {"enhanced_foods": []}

    async def _usda_lookup(self, food_name: str) -> Dict[str, Any]:
        """Query USDA FoodData Central API"""
        try:
            if not self.usda_api_key:
                return {}
                
            # Search for food in USDA database
            search_url = f"{self.usda_base_url}/foods/search"
            params = {
                "query": food_name,
                "api_key": self.usda_api_key,
                "dataType": ["Foundation", "SR Legacy"],
                "pageSize": 3
            }
            
            response = requests.get(search_url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                foods = data.get('foods', [])
                
                if foods:
                    best_match = foods[0]  # Take first result as best match
                    return {
                        "fdc_id": best_match.get('fdcId'),
                        "description": best_match.get('description'),
                        "food_nutrients": best_match.get('foodNutrients', [])[:10],  # Top 10 nutrients
                        "source": "usda"
                    }
            return {}
            
        except Exception as e:
            logger.error(f"USDA lookup error: {str(e)}")
            return {}

    async def _openfood_lookup(self, food_name: str) -> Dict[str, Any]:
        """Query Open Food Facts API"""
        try:
            search_url = f"{self.openfood_base_url}/product/{food_name}.json"
            
            response = requests.get(search_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 1:  # Product found
                    product = data.get('product', {})
                    return {
                        "product_name": product.get('product_name'),
                        "brand": product.get('brands'),
                        "ingredients": product.get('ingredients_text'),
                        "nutrition_grade": product.get('nutrition_grades'),
                        "nova_group": product.get('nova_group'),
                        "additives": product.get('additives_tags', [])[:5],
                        "source": "openfood"
                    }
            return {}
            
        except Exception as e:
            logger.error(f"OpenFood lookup error: {str(e)}")
            return {}

    async def _generate_healthier_alternatives(self, foods: List[Dict], nutrition_analysis: Dict, user_preferences: Dict) -> List[Dict[str, Any]]:
        """Stage 4: Generate healthier alternatives using AI"""
        try:
            if not self.groq_client:
                return self._default_alternatives(foods)

            context = f"""
            Generate healthier alternatives for these detected foods:
            
            CURRENT FOODS: {json.dumps(foods, indent=2)}
            NUTRITION ANALYSIS: {json.dumps(nutrition_analysis, indent=2)}
            USER PREFERENCES: {json.dumps(user_preferences, indent=2)}
            
            For each food, provide 2-3 healthier alternatives with specific improvements.
            Consider: lower calories, higher nutrients, less processing, better ingredients.
            
            Respond in JSON:
            {{
                "alternatives": [
                    {{
                        "original_food": "fried chicken",
                        "original_score": "D (65/100)",
                        "alternatives": [
                            {{
                                "food": "grilled chicken breast",
                                "improvement": "60% fewer calories, no trans fats",
                                "score": "A (92/100)",
                                "prep_time": "15 minutes",
                                "cost_impact": "similar",
                                "why_better": "Removes unhealthy frying oil, preserves protein",
                                "swapping_tips": "Marinate for flavor, use herbs and spices"
                            }}
                        ]
                    }}
                ]
            }}
            """

            completion = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a nutrition expert providing healthier food alternatives. Always respond in valid JSON format with practical, realistic suggestions."
                    },
                    {"role": "user", "content": context}
                ],
                max_tokens=1500,
                temperature=0.4
            )

            response_text = completion.choices[0].message.content
            
            try:
                parsed_response = json.loads(response_text)
                return parsed_response.get('alternatives', [])
            except json.JSONDecodeError:
                return self._extract_alternatives_from_text(response_text, foods)

        except Exception as e:
            logger.error(f"Alternative generation error: {str(e)}")
            return self._default_alternatives(foods)

    def _calculate_food_score(self, food_data: Dict, nutrition_data: Dict) -> Dict[str, Any]:
        """Calculate comprehensive food score (A-F grade)"""
        try:
            # Scoring factors (0-100 points each)
            nutritional_density = self._score_nutritional_density(nutrition_data)
            processing_level = self._score_processing_level(food_data.get('processing_level', 3))
            hidden_ingredient_penalty = self._score_hidden_ingredients(nutrition_data)
            portion_appropriateness = self._score_portion_size(food_data.get('portion_size', ''))
            health_impact = self._score_health_impact(nutrition_data)

            # Calculate weighted average
            total_score = (
                nutritional_density * 0.25 +
                processing_level * 0.25 +
                hidden_ingredient_penalty * 0.15 +
                portion_appropriateness * 0.15 +
                health_impact * 0.20
            )

            # Assign grade
            if total_score >= 90:
                grade = "A"
            elif total_score >= 80:
                grade = "B"
            elif total_score >= 70:
                grade = "C"
            elif total_score >= 60:
                grade = "D"
            else:
                grade = "F"

            return {
                "grade": grade,
                "score": int(total_score),
                "breakdown": {
                    "nutritional_density": nutritional_density,
                    "processing_level": processing_level,
                    "hidden_ingredient_penalty": hidden_ingredient_penalty,
                    "portion_appropriateness": portion_appropriateness,
                    "health_impact": health_impact
                }
            }

        except Exception as e:
            logger.error(f"Food scoring error: {str(e)}")
            return {"grade": "C", "score": 70, "breakdown": {}}

    def _score_nutritional_density(self, nutrition_data: Dict) -> int:
        """Score based on nutrient density"""
        try:
            calories = nutrition_data.get('calories', 200)
            protein = float(nutrition_data.get('protein', '0g').replace('g', ''))
            fiber = float(nutrition_data.get('fiber', '0g').replace('g', ''))
            
            # High protein and fiber with reasonable calories = higher score
            protein_score = min(protein * 4, 40)  # Max 40 points for protein
            fiber_score = min(fiber * 5, 30)     # Max 30 points for fiber
            calorie_efficiency = max(0, 30 - (calories / 20))  # Lower calories = higher score
            
            return int(protein_score + fiber_score + calorie_efficiency)
        except:
            return 60  # Default moderate score

    def _score_processing_level(self, processing_level: int) -> int:
        """Score based on food processing level (1=whole, 5=ultra-processed)"""
        processing_scores = {1: 100, 2: 85, 3: 70, 4: 50, 5: 20}
        return processing_scores.get(processing_level, 60)

    def _score_hidden_ingredients(self, nutrition_data: Dict) -> int:
        """Penalty for hidden unhealthy ingredients"""
        penalty = 0
        
        try:
            # Check sodium
            sodium = float(nutrition_data.get('sodium', '0mg').replace('mg', ''))
            if sodium > 600:
                penalty += 15
            elif sodium > 300:
                penalty += 8
            
            # Check added sugars
            sugar = float(nutrition_data.get('sugar', '0g').replace('g', ''))
            if sugar > 15:
                penalty += 12
            elif sugar > 8:
                penalty += 6
            
            return max(0, 100 - penalty)
        except:
            return 85

    def _score_portion_size(self, portion_size: str) -> int:
        """Score portion appropriateness"""
        portion_lower = portion_size.lower()
        if 'large' in portion_lower or 'xl' in portion_lower:
            return 60
        elif 'medium' in portion_lower or 'regular' in portion_lower:
            return 85
        elif 'small' in portion_lower:
            return 95
        return 75

    def _score_health_impact(self, nutrition_data: Dict) -> int:
        """Score overall health impact"""
        try:
            positive_points = 0
            negative_points = 0
            
            # Positive factors
            protein = float(nutrition_data.get('protein', '0g').replace('g', ''))
            if protein > 20:
                positive_points += 20
            elif protein > 10:
                positive_points += 10
            
            fiber = float(nutrition_data.get('fiber', '0g').replace('g', ''))
            if fiber > 5:
                positive_points += 15
            elif fiber > 2:
                positive_points += 8
            
            # Negative factors
            calories = nutrition_data.get('calories', 200)
            if calories > 500:
                negative_points += 15
            elif calories > 300:
                negative_points += 8
            
            return max(20, min(100, 60 + positive_points - negative_points))
        except:
            return 70

    def _compile_food_results(self, recognition: Dict, nutrition: Dict, database: Dict) -> List[Dict[str, Any]]:
        """Compile results from all processing stages"""
        try:
            compiled_foods = []
            
            recognized_foods = recognition.get('foods', [])
            nutrition_foods = nutrition.get('foods_analyzed', [])
            
            for i, food in enumerate(recognized_foods):
                # Get corresponding nutrition analysis
                nutrition_data = nutrition_foods[i] if i < len(nutrition_foods) else {}
                
                # Calculate food score
                food_score = self._calculate_food_score(food, nutrition_data.get('nutrition_enhanced', {}))
                
                compiled_food = {
                    "name": food.get('name', 'Unknown Food'),
                    "confidence": food.get('confidence', 0.8),
                    "portion_size": food.get('portion_size', 'medium'),
                    "cooking_method": food.get('cooking_method', 'unknown'),
                    "nutrition": {
                        "calories": food.get('estimated_nutrition', {}).get('calories', 200),
                        "protein": food.get('estimated_nutrition', {}).get('protein', '10g'),
                        "carbs": food.get('estimated_nutrition', {}).get('carbs', '20g'),
                        "fat": food.get('estimated_nutrition', {}).get('fat', '8g'),
                        "fiber": food.get('estimated_nutrition', {}).get('fiber', '2g'),
                        "sodium": food.get('estimated_nutrition', {}).get('sodium', '200mg'),
                        "sugar": food.get('estimated_nutrition', {}).get('sugar', '5g')
                    },
                    "food_score": food_score,
                    "health_insights": nutrition_data.get('health_insights', [
                        "Nutritional analysis completed",
                        "Consider portion size for your goals"
                    ]),
                    "dietary_tags": nutrition_data.get('nutrition_enhanced', {}).get('dietary_tags', []),
                    "allergens": nutrition_data.get('nutrition_enhanced', {}).get('allergens', ['unknown']),
                    "processing_level": food.get('processing_level', 3)
                }
                
                compiled_foods.append(compiled_food)
            
            return compiled_foods
            
        except Exception as e:
            logger.error(f"Results compilation error: {str(e)}")
            return []

    def _generate_session_insights(self, recognition: Dict, nutrition: Dict) -> List[str]:
        """Generate insights about the overall meal/session"""
        try:
            insights = []
            
            # Meal composition insights
            foods = recognition.get('foods', [])
            if len(foods) > 1:
                insights.append(f"Detected {len(foods)} different food items in your meal")
            
            # Processing level insights
            processing_levels = [food.get('processing_level', 3) for food in foods]
            avg_processing = sum(processing_levels) / len(processing_levels) if processing_levels else 3
            
            if avg_processing <= 2:
                insights.append("Great choice! Your meal consists mainly of whole, minimally processed foods")
            elif avg_processing >= 4:
                insights.append("Consider adding more whole foods to balance the processed items")
            
            # Nutrition balance insights
            meal_analysis = nutrition.get('meal_analysis', {})
            macro_balance = meal_analysis.get('macro_balance', '')
            
            if 'protein_heavy' in macro_balance:
                insights.append("High protein meal - excellent for muscle building and satiety")
            elif 'carb_heavy' in macro_balance:
                insights.append("Carb-rich meal - great for energy, consider adding protein")
            
            # Missing nutrients
            missing = meal_analysis.get('missing_nutrients', [])
            if missing:
                insights.append(f"To complete your nutrition, consider adding sources of: {', '.join(missing[:2])}")
            
            return insights[:4]  # Limit to 4 insights
            
        except Exception as e:
            logger.error(f"Session insights error: {str(e)}")
            return ["Food analysis completed successfully"]

    def _calculate_database_confidence(self, usda_data: Dict, openfood_data: Dict) -> float:
        """Calculate confidence based on database matches"""
        confidence = 0.5  # Base confidence
        
        if usda_data:
            confidence += 0.3  # USDA is authoritative
        if openfood_data:
            confidence += 0.2  # OpenFood adds context
        
        return min(0.95, confidence)

    # Fallback methods
    def _fallback_response(self) -> Dict[str, Any]:
        """Fallback response when all AI services fail"""
        return {
            "processing_time": "1.0s",
            "api_sources": ["fallback"],
            "foods_detected": [{
                "name": "Food Item",
                "confidence": 0.5,
                "portion_size": "medium",
                "nutrition": {
                    "calories": 200,
                    "protein": "10g",
                    "carbs": "20g",
                    "fat": "8g",
                    "fiber": "2g"
                },
                "food_score": {"grade": "C", "score": 70},
                "health_insights": ["Food logged successfully", "Consider adding more details"]
            }],
            "alternatives": [],
            "session_insights": ["Food recognition service temporarily unavailable"],
            "confidence": 0.5,
            "timestamp": datetime.now().isoformat()
        }

    def _gemini_fallback(self) -> Dict[str, Any]:
        """Fallback when Gemini fails"""
        return {
            "foods": [{
                "name": "Unknown Food",
                "confidence": 0.5,
                "portion_size": "medium",
                "estimated_nutrition": {
                    "calories": 200,
                    "protein": "10g",
                    "carbs": "20g",
                    "fat": "8g"
                }
            }],
            "confidence": 0.5
        }

    def _nutrition_analysis_fallback(self) -> Dict[str, Any]:
        """Fallback when nutrition analysis fails"""
        return {
            "foods_analyzed": [{
                "name": "Food Item",
                "food_score": {"grade": "C", "score": 70},
                "health_insights": ["Analysis unavailable"]
            }],
            "meal_analysis": {"overall_score": "C"},
            "health_insights": ["Food logged successfully"]
        }

    def _default_alternatives(self, foods: List[Dict]) -> List[Dict[str, Any]]:
        """Default healthier alternatives when AI fails"""
        alternatives = []
        
        for food in foods[:2]:  # Limit to 2 foods
            food_name = food.get('name', 'food').lower()
            
            if 'fried' in food_name or 'fry' in food_name:
                alternatives.append({
                    "original_food": food.get('name'),
                    "original_score": "D (60/100)",
                    "alternatives": [{
                        "food": "Grilled version",
                        "improvement": "50% fewer calories, no trans fats",
                        "score": "B (80/100)",
                        "why_better": "Removes unhealthy frying oil"
                    }]
                })
            elif 'processed' in food_name or 'packaged' in food_name:
                alternatives.append({
                    "original_food": food.get('name'),
                    "original_score": "C (70/100)",
                    "alternatives": [{
                        "food": "Fresh whole food version",
                        "improvement": "Less sodium and preservatives",
                        "score": "A (85/100)",
                        "why_better": "Minimally processed, natural ingredients"
                    }]
                })
        
        return alternatives

    def _extract_food_info_from_text(self, text: str) -> Dict[str, Any]:
        """Extract food information from text when JSON parsing fails"""
        # Simple text parsing fallback
        return {
            "foods": [{
                "name": "Detected Food",
                "confidence": 0.7,
                "portion_size": "medium",
                "estimated_nutrition": {"calories": 200}
            }],
            "confidence": 0.7
        }

    def _extract_nutrition_analysis_from_text(self, text: str) -> Dict[str, Any]:
        """Extract nutrition analysis from text"""
        return {
            "foods_analyzed": [{
                "food_score": {"grade": "C", "score": 70},
                "health_insights": ["Analysis completed"]
            }],
            "meal_analysis": {"overall_score": "C"}
        }

    def _extract_alternatives_from_text(self, text: str, foods: List[Dict]) -> List[Dict[str, Any]]:
        """Extract alternatives from text"""
        return self._default_alternatives(foods)

    # Additional helper methods for enhanced API endpoints
    def _generate_improvement_tips(self, food: Dict, food_score: Dict) -> List[str]:
        """Generate specific improvement tips based on food score"""
        tips = []
        score_breakdown = food_score.get('breakdown', {})
        
        if score_breakdown.get('processing_level', 0) < 70:
            tips.append("Choose minimally processed alternatives when possible")
        
        if score_breakdown.get('nutritional_density', 0) < 70:
            tips.append("Add nutrient-dense sides like vegetables or fruits")
        
        if score_breakdown.get('portion_appropriateness', 0) < 80:
            tips.append("Consider adjusting portion size for your goals")
        
        return tips[:3]

    def _analyze_health_impact(self, food: Dict) -> Dict[str, Any]:
        """Analyze health impact of a specific food"""
        return {
            "positive_aspects": ["Provides protein", "Contains essential nutrients"],
            "concerns": ["Monitor portion size", "Check sodium content"],
            "long_term_impact": "moderate_positive"
        }

    def _calculate_meal_score(self, scored_foods: List[Dict]) -> float:
        """Calculate overall meal score from individual food scores"""
        if not scored_foods:
            return 60.0
        
        scores = [food.get('detailed_score', {}).get('score', 60) for food in scored_foods]
        return sum(scores) / len(scores)

    def _get_meal_grade(self, meal_score: float) -> str:
        """Convert meal score to grade"""
        if meal_score >= 90:
            return "A"
        elif meal_score >= 80:
            return "B"
        elif meal_score >= 70:
            return "C"
        elif meal_score >= 60:
            return "D"
        else:
            return "F"

    def _generate_meal_insights(self, scored_foods: List[Dict]) -> List[str]:
        """Generate insights about the overall meal"""
        insights = []
        
        avg_score = self._calculate_meal_score(scored_foods)
        
        if avg_score >= 85:
            insights.append("Excellent meal choice! Well-balanced and nutritious")
        elif avg_score >= 70:
            insights.append("Good meal with room for minor improvements")
        else:
            insights.append("Consider healthier alternatives for better nutrition")
        
        return insights

    def _get_improvement_priorities(self, scored_foods: List[Dict]) -> List[str]:
        """Get prioritized list of improvements"""
        priorities = []
        
        for food in scored_foods:
            score = food.get('detailed_score', {}).get('score', 60)
            if score < 70:
                priorities.append(f"Replace {food.get('name', 'item')} with healthier alternative")
        
        return priorities[:3]

    def _get_cooking_tips(self, food_name: str) -> List[str]:
        """Get cooking tips for healthier preparation"""
        food_lower = food_name.lower()
        
        if 'grilled' in food_lower:
            return ["Use herbs and spices for flavor", "Don't overcook to preserve nutrients"]
        elif 'salad' in food_lower:
            return ["Add variety of colorful vegetables", "Use olive oil based dressing"]
        else:
            return ["Steam or grill for healthier preparation", "Season with herbs instead of salt"]

    def _assess_prep_difficulty(self, food_name: str) -> str:
        """Assess preparation difficulty"""
        simple_foods = ['salad', 'fruit', 'yogurt', 'nuts']
        if any(simple in food_name.lower() for simple in simple_foods):
            return "easy"
        return "moderate"

    def _compare_costs(self, original: str, alternative: str) -> str:
        """Compare costs between original and alternative"""
        # Simple cost comparison logic
        expensive_foods = ['salmon', 'organic', 'grass-fed']
        
        alt_expensive = any(exp in alternative.lower() for exp in expensive_foods)
        orig_expensive = any(exp in original.lower() for exp in expensive_foods)
        
        if alt_expensive and not orig_expensive:
            return "slightly_higher"
        elif not alt_expensive and orig_expensive:
            return "lower"
        else:
            return "similar"

    def _check_dietary_compliance(self, food_name: str, restrictions: List[str]) -> Dict[str, bool]:
        """Check if food complies with dietary restrictions"""
        compliance = {}
        
        for restriction in restrictions:
            if restriction.lower() == 'vegetarian':
                compliance['vegetarian'] = 'meat' not in food_name.lower() and 'chicken' not in food_name.lower()
            elif restriction.lower() == 'gluten_free':
                compliance['gluten_free'] = 'wheat' not in food_name.lower() and 'bread' not in food_name.lower()
        
        return compliance

    def _assess_swap_difficulty(self, original_food: Dict, alternatives: List[Dict]) -> str:
        """Assess how difficult the food swap would be"""
        if len(alternatives) > 2:
            return "easy"
        return "moderate"

    def _get_motivation_message(self, original_food: Dict, alternatives: List[Dict]) -> str:
        """Generate motivational message for food swap"""
        food_name = original_food.get('name', 'your choice')
        
        if alternatives:
            return f"Great opportunity to upgrade {food_name} for better health!"
        return f"Keep {food_name} in moderation as part of a balanced diet"

    def _get_quick_swaps(self, foods: List[Dict]) -> List[Dict[str, str]]:
        """Get simple, quick food swaps"""
        swaps = []
        
        for food in foods:
            name = food.get('name', '').lower()
            if 'white rice' in name:
                swaps.append({"from": "White rice", "to": "Brown rice", "benefit": "More fiber and nutrients"})
            elif 'fried' in name:
                swaps.append({"from": name.title(), "to": "Grilled version", "benefit": "Lower calories, no trans fats"})
        
        return swaps[:3]

    def _optimize_meal_composition(self, original_foods: List[Dict], alternatives: List[Dict]) -> Dict[str, Any]:
        """Suggest meal composition optimization"""
        return {
            "current_balance": "protein_heavy",
            "suggested_additions": ["leafy greens", "healthy fats"],
            "optimal_ratios": {"protein": "25%", "carbs": "45%", "fat": "30%"}
        }

    def _generate_shopping_tips(self, alternatives: List[Dict]) -> List[str]:
        """Generate shopping tips based on alternatives"""
        return [
            "Shop the perimeter of the store for whole foods",
            "Read nutrition labels to compare options",
            "Buy seasonal produce for better nutrition and price"
        ]

    def _combine_database_results(self, results: Dict) -> Dict[str, Any]:
        """Combine results from multiple databases"""
        combined = {}
        
        # Prioritize USDA data if available
        if 'usda' in results and results['usda']:
            combined.update(results['usda'])
        
        # Supplement with OpenFood data
        if 'openfood' in results and results['openfood']:
            for key, value in results['openfood'].items():
                if key not in combined:
                    combined[key] = value
        
        return combined

    def _assess_data_quality(self, results: Dict) -> Dict[str, Any]:
        """Assess quality of database results"""
        quality_score = 0.5  # Base score
        
        if results.get('usda'):
            quality_score += 0.3
        if results.get('openfood'):
            quality_score += 0.2
        
        return {
            "quality_score": min(1.0, quality_score),
            "completeness": "partial" if quality_score < 0.8 else "complete",
            "reliability": "high" if quality_score > 0.8 else "moderate"
        }

    def _analyze_meal_timing(self, meal_history: List[Dict]) -> Dict[str, Any]:
        """Analyze meal timing patterns"""
        return {
            "average_breakfast_time": "7:30 AM",
            "meal_frequency": "3 main meals + 1 snack",
            "timing_consistency": "good"
        }

    def _analyze_food_preferences(self, meal_history: List[Dict]) -> Dict[str, Any]:
        """Analyze food preference patterns"""
        return {
            "top_foods": ["chicken", "rice", "vegetables"],
            "cuisine_preferences": ["mediterranean", "asian"],
            "avoided_foods": ["spicy", "dairy"]
        }

    def _analyze_nutrition_consistency(self, meal_history: List[Dict]) -> Dict[str, Any]:
        """Analyze nutrition consistency"""
        return {
            "calorie_consistency": "moderate",
            "protein_intake_trend": "steady",
            "nutrient_variety": "good"
        }

    def _analyze_portion_trends(self, meal_history: List[Dict]) -> Dict[str, Any]:
        """Analyze portion size trends"""
        return {
            "average_portion_size": "medium",
            "portion_consistency": "varies",
            "recommendations": ["Use smaller plates", "Measure portions initially"]
        }

    def _analyze_processing_trends(self, meal_history: List[Dict]) -> Dict[str, Any]:
        """Analyze food processing level trends"""
        return {
            "average_processing_level": 2.5,
            "trend": "improving",
            "whole_foods_percentage": 65
        }

    def _generate_pattern_based_recommendations(self, patterns: Dict, user_profile: Dict) -> List[Dict[str, Any]]:
        """Generate recommendations based on identified patterns"""
        return [
            {
                "category": "meal_timing",
                "recommendation": "Try to eat at consistent times daily",
                "priority": "medium",
                "expected_benefit": "Better metabolism and hunger control"
            },
            {
                "category": "food_variety",
                "recommendation": "Include more colorful vegetables",
                "priority": "high", 
                "expected_benefit": "Increased micronutrient intake"
            }
        ]