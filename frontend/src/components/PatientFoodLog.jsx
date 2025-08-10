import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { 
  Search, 
  Plus, 
  Clock, 
  Trash2, 
  Edit3, 
  Zap, 
  TrendingUp,
  Camera,
  Sparkles,
  Brain,
  Target
} from 'lucide-react';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

const PatientFoodLog = () => {
  const { switchRole } = useRole();
  const [searchQuery, setSearchQuery] = useState('');
  const [loggedFoods, setLoggedFoods] = useState([]);
  const [dailyTotals, setDailyTotals] = useState({
    calories: 0, protein: 0, carbs: 0, fat: 0, fiber: 0
  });
  const [aiInsights, setAiInsights] = useState([]);
  const [smartSuggestions, setSmartSuggestions] = useState(null);
  const [patternRecognition, setPatternRecognition] = useState(null);
  const [newFood, setNewFood] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [actionMessage, setActionMessage] = useState('');
  const [loading, setLoading] = useState(false);

  // Switch to patient role when component mounts
  useEffect(() => {
    switchRole('patient');
  }, [switchRole]);

  // Load initial data
  useEffect(() => {
    loadFoodLog();
  }, []);

  const loadFoodLog = async () => {
    // In a real app, this would load existing food log entries
    // For demo, we'll start with some sample data
    const sampleFoods = [
      {
        id: 1,
        food_name: 'Greek Yogurt with Berries',
        time: '8:00 AM',
        calories: 180,
        meal_type: 'Breakfast',
        protein: 15,
        carbs: 20,
        fat: 8,
        fiber: 4,
        ai_enhanced: true
      },
      {
        id: 2,
        food_name: 'Grilled Chicken Salad',
        time: '1:00 PM', 
        calories: 320,
        meal_type: 'Lunch',
        protein: 35,
        carbs: 15,
        fat: 12,
        fiber: 8,
        ai_enhanced: true
      }
    ];
    
    setLoggedFoods(sampleFoods);
    updateDailyTotals(sampleFoods);
  };

  const updateDailyTotals = (foods) => {
    const totals = foods.reduce((acc, food) => ({
      calories: acc.calories + food.calories,
      protein: acc.protein + food.protein,
      carbs: acc.carbs + food.carbs,
      fat: acc.fat + food.fat,
      fiber: acc.fiber + (food.fiber || 0)
    }), { calories: 0, protein: 0, carbs: 0, fat: 0, fiber: 0 });
    
    setDailyTotals(totals);
  };

  const handleAddFood = async () => {
    if (!newFood.trim()) return;
    
    setLoading(true);
    setActionMessage('Adding food with AI analysis...');
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/patient/food-log`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          food_name: newFood,
          meal_type: getMealTime()
        })
      });
      
      const data = await response.json();
      if (!data.success) throw new Error('Failed to add food');
      
      // Add the new food entry
      const newEntry = {
        id: loggedFoods.length + 1,
        ...data.food_entry,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        meal_type: data.food_entry.meal_type || getMealTime()
      };
      
      const updatedFoods = [...loggedFoods, newEntry];
      setLoggedFoods(updatedFoods);
      updateDailyTotals(updatedFoods);
      
      // Update AI insights and suggestions
      setAiInsights(data.ai_insights || []);
      setSmartSuggestions(data.smart_suggestions || null);
      setPatternRecognition(data.pattern_recognition || null);
      
      setNewFood('');
      setShowAddForm(false);
      setActionMessage('✓ Food added with AI insights!');
      setTimeout(() => setActionMessage(''), 3000);
      
    } catch (error) {
      setActionMessage(`Error: ${error.message}`);
      setTimeout(() => setActionMessage(''), 3000);
    } finally {
      setLoading(false);
    }
  };

  const getMealTime = () => {
    const hour = new Date().getHours();
    if (hour < 11) return 'Breakfast';
    if (hour < 16) return 'Lunch'; 
    if (hour < 20) return 'Dinner';
    return 'Snack';
  };

  const removeFood = (id) => {
    const updatedFoods = loggedFoods.filter(food => food.id !== id);
    setLoggedFoods(updatedFoods);
    updateDailyTotals(updatedFoods);
  };

  const getMealColor = (meal) => {
    switch (meal) {
      case 'Breakfast': return 'bg-yellow-100 text-yellow-800';
      case 'Lunch': return 'bg-green-100 text-green-800';
      case 'Dinner': return 'bg-blue-100 text-blue-800';
      default: return 'bg-purple-100 text-purple-800';
    }
  };

  const getProgressPercentage = (current, target) => {
    return Math.min((current / target) * 100, 100);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Smart Food Log</h1>
          <p className="text-gray-600">AI-powered nutrition tracking with pattern recognition and smart insights</p>
          {actionMessage && (
            <div className="mt-2 p-3 bg-blue-50 border border-blue-200 text-blue-700 rounded-lg flex items-center">
              {loading && <div className="animate-spin mr-2">⚡</div>}
              {actionMessage}
            </div>
          )}
        </div>

        {/* Enhanced Daily Summary */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
          <Card className="border-2 border-blue-200 bg-blue-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Calories</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">{dailyTotals.calories}</div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${getProgressPercentage(dailyTotals.calories, 2000)}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">of 2000 goal</p>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-purple-200 bg-purple-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Protein</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-purple-600">{dailyTotals.protein}g</div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-purple-600 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${getProgressPercentage(dailyTotals.protein, 150)}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">of 150g goal</p>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-orange-200 bg-orange-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Carbs</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-orange-600">{dailyTotals.carbs}g</div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-orange-600 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${getProgressPercentage(dailyTotals.carbs, 250)}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">of 250g goal</p>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-green-200 bg-green-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Fat</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{dailyTotals.fat}g</div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-green-600 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${getProgressPercentage(dailyTotals.fat, 65)}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">of 65g goal</p>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-cyan-200 bg-cyan-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Fiber</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-cyan-600">{dailyTotals.fiber}g</div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-cyan-600 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${getProgressPercentage(dailyTotals.fiber, 25)}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">of 25g goal</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Smart Food Add */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Plus className="w-5 h-5 mr-2 text-blue-600" />
                  Smart Food Add
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="relative">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    placeholder="Search or describe food..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
                
                {showAddForm ? (
                  <div className="space-y-3">
                    <Input
                      placeholder="e.g., grilled chicken breast, apple, pasta..."
                      value={newFood}
                      onChange={(e) => setNewFood(e.target.value)}
                    />
                    <div className="flex space-x-2">
                      <Button onClick={handleAddFood} className="bg-blue-600 hover:bg-blue-700" disabled={loading}>
                        {loading ? (
                          <div className="animate-spin mr-2">⚡</div>
                        ) : (
                          <Zap className="w-4 h-4 mr-2" />
                        )}
                        AI Analyze & Add
                      </Button>
                      <Button variant="outline" onClick={() => setShowAddForm(false)}>
                        Cancel
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <Button 
                      onClick={() => setShowAddForm(true)}
                      className="w-full bg-blue-600 hover:bg-blue-700"
                    >
                      <Plus className="w-4 h-4 mr-2" />
                      Smart Food Add
                    </Button>
                    
                    <Button 
                      className="w-full bg-purple-600 hover:bg-purple-700"
                      variant="outline"
                    >
                      <Camera className="w-4 h-4 mr-2" />
                      Photo Recognition
                    </Button>
                  </div>
                )}

                <div className="border-t pt-4">
                  <h3 className="font-semibold text-gray-900 mb-2">Quick Options</h3>
                  <div className="grid grid-cols-2 gap-2">
                    {['Apple', 'Banana', 'Water', 'Coffee', 'Almonds', 'Yogurt'].map((food) => (
                      <Button
                        key={food}
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setNewFood(food);
                          setShowAddForm(true);
                        }}
                        className="text-xs"
                      >
                        {food}
                      </Button>
                    ))}
                  </div>
                </div>

                {/* AI Insights Panel */}
                {aiInsights.length > 0 && (
                  <div className="border-t pt-4">
                    <h3 className="font-semibold text-gray-900 mb-2 flex items-center">
                      <Brain className="w-4 h-4 mr-2 text-purple-600" />
                      AI Insights
                    </h3>
                    <div className="space-y-2">
                      {aiInsights.map((insight, idx) => (
                        <div key={idx} className="p-2 bg-purple-50 rounded text-sm text-purple-800">
                          {insight}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Food Log Entries */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <Clock className="w-5 h-5 mr-2 text-blue-600" />
                    Today's Food Log
                  </span>
                  <Badge variant="secondary">{loggedFoods.length} entries</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {loggedFoods.length === 0 ? (
                  <div className="text-center py-8">
                    <div className="text-gray-400 mb-2">No food logged yet</div>
                    <p className="text-sm text-gray-500">Start logging your meals to get AI-powered insights</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {loggedFoods.map((food) => (
                      <div key={food.id} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center space-x-3">
                            <Badge className={getMealColor(food.meal_type)}>{food.meal_type}</Badge>
                            <span className="text-sm text-gray-500">{food.time}</span>
                            {food.ai_enhanced && (
                              <Badge className="bg-purple-100 text-purple-800 text-xs">
                                <Sparkles className="w-3 h-3 mr-1" />
                                AI Enhanced
                              </Badge>
                            )}
                          </div>
                          <div className="flex space-x-1">
                            <Button variant="ghost" size="sm">
                              <Edit3 className="w-4 h-4" />
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => removeFood(food.id)}
                              className="text-red-500 hover:text-red-700"
                            >
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>
                        
                        <div className="mb-3">
                          <h3 className="font-semibold text-gray-900">{food.food_name}</h3>
                        </div>
                        
                        <div className="grid grid-cols-5 gap-4 text-sm">
                          <div>
                            <div className="text-gray-500">Calories</div>
                            <div className="font-semibold text-orange-600">{food.calories}</div>
                          </div>
                          <div>
                            <div className="text-gray-500">Protein</div>
                            <div className="font-semibold text-purple-600">{food.protein}g</div>
                          </div>
                          <div>
                            <div className="text-gray-500">Carbs</div>
                            <div className="font-semibold text-blue-600">{food.carbs}g</div>
                          </div>
                          <div>
                            <div className="text-gray-500">Fat</div>
                            <div className="font-semibold text-green-600">{food.fat}g</div>
                          </div>
                          <div>
                            <div className="text-gray-500">Fiber</div>
                            <div className="font-semibold text-cyan-600">{food.fiber || 0}g</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Pattern Recognition Insights */}
            {patternRecognition && (
              <Card className="mt-6">
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <TrendingUp className="w-5 h-5 mr-2 text-green-600" />
                    Pattern Recognition
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-3 bg-green-50 rounded-lg">
                      <div className="font-medium text-gray-900 text-sm mb-1">Meal Timing</div>
                      <div className="text-sm text-green-800">{patternRecognition.meal_timing_pattern}</div>
                    </div>
                    <div className="p-3 bg-blue-50 rounded-lg">
                      <div className="font-medium text-gray-900 text-sm mb-1">Nutrition Balance</div>
                      <div className="text-sm text-blue-800">{patternRecognition.nutrition_balance}</div>
                    </div>
                    <div className="p-3 bg-amber-50 rounded-lg">
                      <div className="font-medium text-gray-900 text-sm mb-1">Frequency</div>
                      <div className="text-sm text-amber-800">{patternRecognition.frequency_insight}</div>
                    </div>
                    <div className="p-3 bg-purple-50 rounded-lg">
                      <div className="font-medium text-gray-900 text-sm mb-1">Smart Suggestions</div>
                      <div className="text-sm text-purple-800 space-y-1">
                        {patternRecognition.suggestions.slice(0, 2).map((suggestion, idx) => (
                          <div key={idx}>• {suggestion}</div>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Food Log</h1>
          <p className="text-gray-600">Track your daily nutrition and maintain healthy eating habits</p>
        </div>

        {/* Daily Summary */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Total Calories</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">{getTotalCalories()}</div>
              <p className="text-xs text-gray-500">of 2000 goal</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Meals Logged</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{loggedFoods.length}</div>
              <p className="text-xs text-gray-500">entries today</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Protein</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-purple-600">
                {loggedFoods.reduce((total, food) => total + food.protein, 0)}g
              </div>
              <p className="text-xs text-gray-500">of 150g goal</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Water</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-cyan-600">6</div>
              <p className="text-xs text-gray-500">glasses today</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Food Search and Add */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Plus className="w-5 h-5 mr-2 text-blue-600" />
                  Add Food
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="relative">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    placeholder="Search for food..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
                
                {showAddForm ? (
                  <div className="space-y-3">
                    <Input
                      placeholder="Enter food name..."
                      value={newFood}
                      onChange={(e) => setNewFood(e.target.value)}
                    />
                    <div className="flex space-x-2">
                      <Button onClick={handleAddFood} className="bg-blue-600 hover:bg-blue-700">
                        Add Food
                      </Button>
                      <Button variant="outline" onClick={() => setShowAddForm(false)}>
                        Cancel
                      </Button>
                    </div>
                  </div>
                ) : (
                  <Button 
                    onClick={() => setShowAddForm(true)}
                    className="w-full bg-blue-600 hover:bg-blue-700"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Quick Add
                  </Button>
                )}

                <div className="border-t pt-4">
                  <h3 className="font-semibold text-gray-900 mb-2">Quick Options</h3>
                  <div className="grid grid-cols-2 gap-2">
                    {['Apple', 'Banana', 'Water', 'Coffee', 'Almonds', 'Yogurt'].map((food) => (
                      <Button
                        key={food}
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setNewFood(food);
                          setShowAddForm(true);
                        }}
                        className="text-xs"
                      >
                        {food}
                      </Button>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Food Log Entries */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <Clock className="w-5 h-5 mr-2 text-blue-600" />
                    Today's Food Log
                  </span>
                  <Badge variant="secondary">{loggedFoods.length} entries</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {loggedFoods.length === 0 ? (
                  <div className="text-center py-8">
                    <div className="text-gray-400 mb-2">No food logged yet</div>
                    <p className="text-sm text-gray-500">Start logging your meals to track your nutrition</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {loggedFoods.map((food) => (
                      <div key={food.id} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center space-x-3">
                            <Badge className={getMealColor(food.meal)}>{food.meal}</Badge>
                            <span className="text-sm text-gray-500">{food.time}</span>
                          </div>
                          <div className="flex space-x-1">
                            <Button variant="ghost" size="sm">
                              <Edit3 className="w-4 h-4" />
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => removeFood(food.id)}
                              className="text-red-500 hover:text-red-700"
                            >
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>
                        
                        <div className="mb-3">
                          <h3 className="font-semibold text-gray-900">{food.name}</h3>
                        </div>
                        
                        <div className="grid grid-cols-4 gap-4 text-sm">
                          <div>
                            <div className="text-gray-500">Calories</div>
                            <div className="font-semibold text-orange-600">{food.calories}</div>
                          </div>
                          <div>
                            <div className="text-gray-500">Protein</div>
                            <div className="font-semibold text-purple-600">{food.protein}g</div>
                          </div>
                          <div>
                            <div className="text-gray-500">Carbs</div>
                            <div className="font-semibold text-blue-600">{food.carbs}g</div>
                          </div>
                          <div>
                            <div className="text-gray-500">Fat</div>
                            <div className="font-semibold text-green-600">{food.fat}g</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientFoodLog;