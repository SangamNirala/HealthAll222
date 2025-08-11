import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  Zap, 
  Clock, 
  TrendingUp, 
  Coffee,
  Apple,
  Sandwich,
  RefreshCw
} from 'lucide-react';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

const QuickAddButtons = ({ userId, onFoodAdd }) => {
  const [quickSuggestions, setQuickSuggestions] = useState([]);
  const [frequentFoods, setFrequentFoods] = useState([]);
  const [recentFoods, setRecentFoods] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchQuickSuggestions();
  }, [userId]);

  const fetchQuickSuggestions = async () => {
    setLoading(true);
    try {
      // Fetch suggestions from backend
      const response = await fetch(`${API_BASE_URL}/api/patient/smart-suggestions/${userId}`);
      if (response.ok) {
        const data = await response.json();
        setQuickSuggestions(data.quick_add_suggestions || []);
      }
      
      // Generate context-aware suggestions
      generateContextualSuggestions();
      generateFrequentFoods();
      generateRecentFoods();
    } catch (error) {
      console.error('Failed to fetch quick suggestions:', error);
      // Fallback to default suggestions
      generateDefaultSuggestions();
    } finally {
      setLoading(false);
    }
  };

  const generateContextualSuggestions = () => {
    const hour = new Date().getHours();
    const dayOfWeek = new Date().getDay();
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
    
    let contextualFoods = [];

    // Time-based suggestions
    if (hour >= 6 && hour <= 10) {
      // Breakfast suggestions
      contextualFoods = [
        { name: 'Oatmeal with Berries', calories: 220, protein: 8, carbs: 45, fat: 4, icon: '🥣', reason: 'Perfect breakfast fuel' },
        { name: 'Greek Yogurt', calories: 130, protein: 15, carbs: 8, fat: 0, icon: '🥛', reason: 'High protein start' },
        { name: 'Banana', calories: 105, protein: 1, carbs: 27, fat: 0, icon: '🍌', reason: 'Quick energy boost' },
        { name: 'Avocado Toast', calories: 250, protein: 8, carbs: 25, fat: 16, icon: '🥑', reason: 'Healthy fats' }
      ];
    } else if (hour >= 11 && hour <= 15) {
      // Lunch suggestions
      contextualFoods = [
        { name: 'Grilled Chicken Salad', calories: 320, protein: 35, carbs: 12, fat: 15, icon: '🥗', reason: 'Lean protein boost' },
        { name: 'Quinoa Bowl', calories: 280, protein: 12, carbs: 42, fat: 8, icon: '🍲', reason: 'Complete nutrition' },
        { name: 'Turkey Sandwich', calories: 350, protein: 25, carbs: 38, fat: 12, icon: '🥪', reason: 'Balanced meal' },
        { name: 'Salmon Fillet', calories: 230, protein: 25, carbs: 0, fat: 14, icon: '🐟', reason: 'Omega-3 rich' }
      ];
    } else if (hour >= 17 && hour <= 22) {
      // Dinner suggestions
      contextualFoods = [
        { name: 'Grilled Chicken Breast', calories: 165, protein: 31, carbs: 0, fat: 4, icon: '🍗', reason: 'Lean dinner protein' },
        { name: 'Sweet Potato', calories: 112, protein: 2, carbs: 26, fat: 0, icon: '🍠', reason: 'Complex carbs' },
        { name: 'Steamed Broccoli', calories: 25, protein: 3, carbs: 5, fat: 0, icon: '🥦', reason: 'Nutrient dense' },
        { name: 'Brown Rice', calories: 110, protein: 3, carbs: 22, fat: 1, icon: '🍚', reason: 'Whole grain energy' }
      ];
    } else {
      // Snack suggestions
      contextualFoods = [
        { name: 'Mixed Nuts', calories: 170, protein: 6, carbs: 6, fat: 15, icon: '🥜', reason: 'Healthy snack' },
        { name: 'Apple Slices', calories: 80, protein: 0, carbs: 21, fat: 0, icon: '🍎', reason: 'Natural sweetness' },
        { name: 'Protein Bar', calories: 200, protein: 20, carbs: 15, fat: 8, icon: '🍫', reason: 'Quick protein' },
        { name: 'Carrots with Hummus', calories: 100, protein: 4, carbs: 12, fat: 4, icon: '🥕', reason: 'Crunchy & satisfying' }
      ];
    }

    // Weekend vs weekday adjustments
    if (isWeekend && (hour >= 9 && hour <= 12)) {
      contextualFoods = [
        { name: 'Pancakes (2 medium)', calories: 340, protein: 8, carbs: 58, fat: 10, icon: '🥞', reason: 'Weekend treat' },
        { name: 'Fresh Fruit Bowl', calories: 120, protein: 2, carbs: 30, fat: 1, icon: '🍓', reason: 'Light & fresh' },
        { name: 'Eggs Benedict', calories: 450, protein: 20, carbs: 25, fat: 32, icon: '🍳', reason: 'Brunch special' }
      ];
    }

    setQuickSuggestions(contextualFoods.slice(0, 6));
  };

  const generateFrequentFoods = () => {
    // Mock frequent foods based on typical patterns
    const mockFrequent = [
      { name: 'Chicken Breast', calories: 165, protein: 31, carbs: 0, fat: 4, frequency: 12, icon: '🍗' },
      { name: 'Brown Rice', calories: 110, protein: 3, carbs: 22, fat: 1, frequency: 10, icon: '🍚' },
      { name: 'Greek Yogurt', calories: 130, protein: 15, carbs: 8, fat: 0, frequency: 8, icon: '🥛' },
      { name: 'Banana', calories: 105, protein: 1, carbs: 27, fat: 0, frequency: 7, icon: '🍌' },
      { name: 'Almonds (1 oz)', calories: 164, protein: 6, carbs: 6, fat: 14, frequency: 6, icon: '🥜' }
    ];
    setFrequentFoods(mockFrequent);
  };

  const generateRecentFoods = () => {
    // Mock recent foods
    const mockRecent = [
      { name: 'Grilled Salmon', calories: 230, protein: 25, carbs: 0, fat: 14, lastEaten: '2 hours ago', icon: '🐟' },
      { name: 'Caesar Salad', calories: 270, protein: 12, carbs: 15, fat: 20, lastEaten: 'Yesterday', icon: '🥗' },
      { name: 'Protein Smoothie', calories: 180, protein: 25, carbs: 12, fat: 3, lastEaten: 'Yesterday', icon: '🥤' },
      { name: 'Oatmeal', calories: 150, protein: 5, carbs: 27, fat: 3, lastEaten: '2 days ago', icon: '🥣' }
    ];
    setRecentFoods(mockRecent);
  };

  const generateDefaultSuggestions = () => {
    const defaultFoods = [
      { name: 'Water (8 oz)', calories: 0, protein: 0, carbs: 0, fat: 0, icon: '💧', reason: 'Stay hydrated' },
      { name: 'Apple', calories: 95, protein: 0, carbs: 25, fat: 0, icon: '🍎', reason: 'Natural energy' },
      { name: 'Banana', calories: 105, protein: 1, carbs: 27, fat: 0, icon: '🍌', reason: 'Quick fuel' },
      { name: 'Greek Yogurt', calories: 130, protein: 15, carbs: 8, fat: 0, icon: '🥛', reason: 'Protein boost' }
    ];
    setQuickSuggestions(defaultFoods);
  };

  const QuickButton = ({ food, showReason = false, size = 'default' }) => (
    <Button
      variant="outline"
      size={size}
      onClick={() => onFoodAdd(food)}
      className={`h-auto ${size === 'sm' ? 'p-2' : 'p-3'} text-left justify-start hover:bg-blue-50 hover:border-blue-300 transition-colors`}
    >
      <div className="flex items-start gap-2 w-full">
        <span className="text-lg">{food.icon}</span>
        <div className="flex-1 min-w-0">
          <div className="font-medium text-sm truncate">{food.name}</div>
          <div className="text-xs text-gray-600">
            {food.calories} cal • {food.protein}P
          </div>
          {showReason && food.reason && (
            <div className="text-xs text-blue-600 mt-1">
              {food.reason}
            </div>
          )}
          {food.frequency && (
            <div className="text-xs text-gray-500 mt-1">
              Added {food.frequency} times
            </div>
          )}
          {food.lastEaten && (
            <div className="text-xs text-gray-500 mt-1">
              Last: {food.lastEaten}
            </div>
          )}
        </div>
      </div>
    </Button>
  );

  if (loading) {
    return (
      <Card>
        <CardContent className="p-4">
          <div className="animate-pulse">
            <div className="h-4 bg-gray-200 rounded mb-3 w-1/3"></div>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <div key={i} className="h-16 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {/* Smart Quick Add */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Zap className="h-5 w-5" />
              Smart Quick Add
            </CardTitle>
            <Button
              variant="ghost"
              size="sm"
              onClick={fetchQuickSuggestions}
              disabled={loading}
            >
              <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            </Button>
          </div>
          <p className="text-sm text-gray-600">
            Context-aware suggestions based on time and patterns
          </p>
        </CardHeader>
        <CardContent className="pt-0">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
            {quickSuggestions.map((food, index) => (
              <QuickButton key={index} food={food} showReason={true} size="sm" />
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Frequent Foods */}
        {frequentFoods.length > 0 && (
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-4 w-4" />
                Frequently Added
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-0">
              <div className="space-y-2">
                {frequentFoods.slice(0, 4).map((food, index) => (
                  <QuickButton key={index} food={food} size="sm" />
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Recent Foods */}
        {recentFoods.length > 0 && (
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2">
                <Clock className="h-4 w-4" />
                Recently Added
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-0">
              <div className="space-y-2">
                {recentFoods.slice(0, 4).map((food, index) => (
                  <QuickButton key={index} food={food} size="sm" />
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Meal Type Quick Access */}
      <Card className="bg-gradient-to-r from-green-50 to-blue-50 border-green-200">
        <CardContent className="p-4">
          <div className="flex items-center justify-between mb-3">
            <h4 className="font-medium text-green-900">Quick Meal Categories</h4>
            <Badge className="bg-green-100 text-green-800">
              One-tap logging
            </Badge>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <Button
              variant="outline"
              className="h-auto p-3 flex-col bg-white hover:bg-green-50"
              onClick={() => onFoodAdd({
                name: 'Morning Coffee',
                calories: 5,
                protein: 0,
                carbs: 1,
                fat: 0,
                icon: '☕'
              })}
            >
              <Coffee className="h-6 w-6 mb-1 text-amber-600" />
              <span className="text-sm">Coffee</span>
            </Button>
            
            <Button
              variant="outline"
              className="h-auto p-3 flex-col bg-white hover:bg-green-50"
              onClick={() => onFoodAdd({
                name: 'Mixed Fruit Bowl',
                calories: 150,
                protein: 2,
                carbs: 38,
                fat: 1,
                icon: '🍎'
              })}
            >
              <Apple className="h-6 w-6 mb-1 text-red-500" />
              <span className="text-sm">Fruit</span>
            </Button>
            
            <Button
              variant="outline"
              className="h-auto p-3 flex-col bg-white hover:bg-green-50"
              onClick={() => onFoodAdd({
                name: 'Deli Sandwich',
                calories: 400,
                protein: 20,
                carbs: 45,
                fat: 15,
                icon: '🥪'
              })}
            >
              <Sandwich className="h-6 w-6 mb-1 text-yellow-600" />
              <span className="text-sm">Sandwich</span>
            </Button>
            
            <Button
              variant="outline"
              className="h-auto p-3 flex-col bg-white hover:bg-green-50"
              onClick={() => onFoodAdd({
                name: 'Water (16 oz)',
                calories: 0,
                protein: 0,
                carbs: 0,
                fat: 0,
                icon: '💧'
              })}
            >
              <div className="h-6 w-6 mb-1 text-blue-500 flex items-center justify-center text-lg">💧</div>
              <span className="text-sm">Water</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default QuickAddButtons;