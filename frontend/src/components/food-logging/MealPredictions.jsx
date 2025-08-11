import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  Sparkles, 
  Clock, 
  TrendingUp, 
  Target,
  ChefHat,
  Brain,
  Calendar
} from 'lucide-react';
import geminiService from '../../services/geminiService';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

const MealPredictions = ({ userId, onMealSelected }) => {
  const [predictions, setPredictions] = useState([]);
  const [nutritionGaps, setNutritionGaps] = useState([]);
  const [mealPatterns, setMealPatterns] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedTimeFrame, setSelectedTimeFrame] = useState('today');
  const [personalizedSuggestions, setPersonalizedSuggestions] = useState([]);

  useEffect(() => {
    fetchMealPredictions();
  }, [userId, selectedTimeFrame]);

  const fetchMealPredictions = async () => {
    setLoading(true);
    try {
      // Fetch smart suggestions from backend
      const response = await fetch(`${API_BASE_URL}/api/patient/smart-suggestions/${userId}`);
      if (response.ok) {
        const data = await response.json();
        setPredictions(data.quick_add_suggestions || []);
        setMealPatterns(data.meal_pattern_insights || {});
        setNutritionGaps(data.nutrition_gaps || []);
      }

      // Generate AI-powered personalized suggestions
      await generatePersonalizedSuggestions();
    } catch (error) {
      console.error('Failed to fetch meal predictions:', error);
    } finally {
      setLoading(false);
    }
  };

  const generatePersonalizedSuggestions = async () => {
    try {
      // Mock nutrition history for AI analysis
      const nutritionHistory = {
        recentMeals: [
          { name: 'Greek Yogurt with Berries', calories: 150, protein: 15, carbs: 20, fat: 5 },
          { name: 'Grilled Chicken Salad', calories: 350, protein: 35, carbs: 15, fat: 18 },
          { name: 'Salmon with Quinoa', calories: 420, protein: 30, carbs: 35, fat: 20 }
        ],
        dailyTargets: { calories: 2000, protein: 150, carbs: 200, fat: 65 },
        preferences: { dietary: 'balanced', activity_level: 'moderate' }
      };

      const result = await geminiService.generateMealSuggestions(nutritionHistory, {
        timeframe: selectedTimeFrame,
        goal: 'balanced_nutrition'
      });

      if (result.success) {
        setPersonalizedSuggestions(result.suggestions || []);
      }
    } catch (error) {
      console.error('AI meal suggestions error:', error);
    }
  };

  const getCurrentMealType = () => {
    const hour = new Date().getHours();
    if (hour >= 5 && hour <= 10) return { type: 'breakfast', icon: '🌅', label: 'Breakfast' };
    if (hour >= 11 && hour <= 15) return { type: 'lunch', icon: '☀️', label: 'Lunch' };
    if (hour >= 17 && hour <= 22) return { type: 'dinner', icon: '🌙', label: 'Dinner' };
    return { type: 'snack', icon: '🍎', label: 'Snack' };
  };

  const currentMeal = getCurrentMealType();

  const handleMealSelect = (meal) => {
    if (onMealSelected) {
      onMealSelected({
        name: meal.name,
        brand: meal.brand || 'Predicted Meal',
        nutrition: {
          calories: meal.calories || 0,
          protein: meal.protein || 0,
          carbs: meal.carbs || 0,
          fat: meal.fat || 0,
          fiber: meal.fiber || 0,
          sodium: meal.sodium || 0,
          servingSize: meal.serving_size || '1 serving'
        },
        source: 'meal_prediction',
        prediction_reason: meal.reason || meal.benefits
      });
    }
  };

  const MealCard = ({ meal, type = 'prediction' }) => (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h4 className="font-medium text-gray-900 mb-1">{meal.name}</h4>
            {meal.description && (
              <p className="text-sm text-gray-600 mb-2">{meal.description}</p>
            )}
            
            {/* Nutrition Info */}
            <div className="grid grid-cols-2 gap-2 text-sm text-gray-700 mb-2">
              <span>🔥 {meal.calories || 0} cal</span>
              <span>🥩 {meal.protein || 0}g protein</span>
              <span>🌾 {meal.carbs || 0}g carbs</span>
              <span>🥑 {meal.fat || 0}g fat</span>
            </div>

            {/* Prediction Reason */}
            {meal.reason && (
              <div className="bg-blue-50 border border-blue-200 rounded p-2 mb-2">
                <p className="text-xs text-blue-800">
                  <Brain className="h-3 w-3 inline mr-1" />
                  {meal.reason}
                </p>
              </div>
            )}

            {/* Benefits */}
            {meal.benefits && Array.isArray(meal.benefits) && (
              <div className="flex flex-wrap gap-1 mb-2">
                {meal.benefits.slice(0, 2).map((benefit, index) => (
                  <Badge key={index} variant="secondary" className="text-xs">
                    {benefit}
                  </Badge>
                ))}
              </div>
            )}

            {/* Timing and Pattern Info */}
            {meal.timing && (
              <div className="flex items-center gap-1 text-xs text-gray-500">
                <Clock className="h-3 w-3" />
                <span>Best time: {meal.timing}</span>
              </div>
            )}
          </div>
          
          <Button 
            size="sm"
            onClick={() => handleMealSelect(meal)}
            className="ml-3"
          >
            Add
          </Button>
        </div>
      </CardContent>
    </Card>
  );

  const PatternInsight = ({ pattern, value }) => (
    <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
      <div>
        <p className="font-medium text-sm text-gray-900 capitalize">
          {pattern.replace('_', ' ')}
        </p>
        <p className="text-xs text-gray-600">Based on your history</p>
      </div>
      <div className="text-right">
        <p className="font-bold text-blue-600">{value}</p>
      </div>
    </div>
  );

  if (loading) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="animate-pulse space-y-4">
            <div className="h-4 bg-gray-200 rounded w-1/3"></div>
            <div className="space-y-2">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-20 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Current Meal Context */}
      <Card className="bg-gradient-to-r from-purple-50 to-pink-50 border-purple-200">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="text-2xl">{currentMeal.icon}</div>
              <div>
                <h3 className="font-semibold text-purple-900">
                  {currentMeal.label} Suggestions
                </h3>
                <p className="text-sm text-purple-700">
                  AI-powered meal predictions based on your patterns
                </p>
              </div>
            </div>
            <Badge className="bg-purple-100 text-purple-800">
              <Sparkles className="h-3 w-3 mr-1" />
              Smart Predictions
            </Badge>
          </div>
        </CardContent>
      </Card>

      {/* Time Frame Selector */}
      <div className="flex gap-2">
        {[
          { value: 'today', label: 'Today', icon: <Calendar className="h-4 w-4" /> },
          { value: 'week', label: 'This Week', icon: <TrendingUp className="h-4 w-4" /> },
          { value: 'patterns', label: 'Pattern-Based', icon: <Brain className="h-4 w-4" /> }
        ].map((timeframe) => (
          <Button
            key={timeframe.value}
            variant={selectedTimeFrame === timeframe.value ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSelectedTimeFrame(timeframe.value)}
            className="flex items-center gap-1"
          >
            {timeframe.icon}
            {timeframe.label}
          </Button>
        ))}
      </div>

      {/* Quick Predictions */}
      {predictions.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5" />
              Quick Add Predictions
            </CardTitle>
            <p className="text-sm text-gray-600">
              Based on your eating patterns and current nutrition needs
            </p>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {predictions.slice(0, 4).map((meal, index) => (
                <MealCard key={index} meal={meal} type="quick" />
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* AI Personalized Suggestions */}
      {personalizedSuggestions.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ChefHat className="h-5 w-5" />
              AI Personalized Suggestions
            </CardTitle>
            <p className="text-sm text-gray-600">
              Custom meal recommendations powered by Gemini AI
            </p>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {personalizedSuggestions.map((meal, index) => (
                <MealCard key={index} meal={meal} type="ai" />
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Nutrition Gaps */}
      {nutritionGaps.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5" />
              Fill Nutrition Gaps
            </CardTitle>
            <p className="text-sm text-gray-600">
              Foods to help you reach your daily nutrition targets
            </p>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {nutritionGaps.map((gap, index) => (
                <div key={index} className="p-3 bg-amber-50 border border-amber-200 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium text-amber-900 capitalize">
                      {gap.nutrient}
                    </span>
                    <Badge variant="outline" className="text-amber-700 border-amber-300">
                      {gap.current}/{gap.target}
                    </Badge>
                  </div>
                  <p className="text-sm text-amber-800 mb-2">{gap.suggestion}</p>
                  {gap.foods && (
                    <div className="flex flex-wrap gap-1">
                      {gap.foods.slice(0, 3).map((food, foodIndex) => (
                        <Button
                          key={foodIndex}
                          size="sm"
                          variant="outline"
                          onClick={() => handleMealSelect({
                            name: food,
                            calories: gap.estimated_calories || 100,
                            protein: gap.nutrient === 'protein' ? 20 : 5,
                            carbs: gap.nutrient === 'carbs' ? 25 : 10,
                            fat: gap.nutrient === 'fat' ? 15 : 5,
                            reason: `Recommended to increase ${gap.nutrient} intake`
                          })}
                          className="text-xs"
                        >
                          + {food}
                        </Button>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Meal Pattern Insights */}
      {Object.keys(mealPatterns).length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Your Meal Patterns
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {mealPatterns.breakfast_time && (
                <PatternInsight 
                  pattern="breakfast_time" 
                  value={mealPatterns.breakfast_time} 
                />
              )}
              {mealPatterns.lunch_time && (
                <PatternInsight 
                  pattern="lunch_time" 
                  value={mealPatterns.lunch_time} 
                />
              )}
              {mealPatterns.dinner_time && (
                <PatternInsight 
                  pattern="dinner_time" 
                  value={mealPatterns.dinner_time} 
                />
              )}
              {mealPatterns.snack_preferences && (
                <PatternInsight 
                  pattern="snack_preferences" 
                  value={mealPatterns.snack_preferences} 
                />
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Tips for Better Predictions */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-medium text-blue-900 mb-2">
          💡 Tips for Better Meal Predictions:
        </h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Log your meals consistently for more accurate predictions</li>
          <li>• Set your nutrition goals to get targeted suggestions</li>
          <li>• Rate suggested meals to improve future recommendations</li>
          <li>• Update your dietary preferences and restrictions</li>
          <li>• The AI learns from your eating patterns over time</li>
        </ul>
      </div>
    </div>
  );
};

export default MealPredictions;