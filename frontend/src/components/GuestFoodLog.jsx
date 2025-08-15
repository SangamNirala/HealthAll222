import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import RealTimeFeedback from './shared/RealTimeFeedback';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { 
  Search, Plus, Clock, Trash2, Target, Apple, 
  Lightbulb, Heart, CheckCircle, Sparkles, 
  TrendingUp, Info, AlertCircle, Zap, Crown
} from 'lucide-react';

const GuestFoodLog = () => {
  const { switchRole } = useRole();
  const [searchQuery, setSearchQuery] = useState('');
  const [loggedFoods, setLoggedFoods] = useState([]);
  const [newFood, setNewFood] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [isLogging, setIsLogging] = useState(false);
  const [sessionId, setSessionId] = useState('');
  const [sessionTotals, setSessionTotals] = useState({
    today_calories: 0,
    meals_logged: 0,
    session_time: '0 minutes'
  });
  const [lastFeedback, setLastFeedback] = useState(null);
  const [learningMoment, setLearningMoment] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [realtimeFeedback, setRealtimeFeedback] = useState(null);
  const [streakDays, setStreakDays] = useState(0);
  const [showUpgradePrompt, setShowUpgradePrompt] = useState(false);

  // Initialize guest session
  useEffect(() => {
    switchRole('guest');
    initializeGuestSession();
  }, [switchRole]);

  const initializeGuestSession = async () => {
    try {
      // Check if session exists in localStorage
      let guestSession = localStorage.getItem('guest_session_id');
      
      if (!guestSession) {
        // Create new session via API
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/guest/session`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        if (response.ok) {
          const sessionData = await response.json();
          guestSession = sessionData.session_id;
          localStorage.setItem('guest_session_id', guestSession);
          localStorage.setItem('guest_session_expires', sessionData.expires_at);
        } else {
          // Fallback session ID
          guestSession = `guest_${Date.now()}_${Math.random().toString(36).substr(2, 8)}`;
          localStorage.setItem('guest_session_id', guestSession);
        }
      }
      
      setSessionId(guestSession);
      
      // Load existing logged foods from localStorage for this session
      const savedFoods = localStorage.getItem(`guest_foods_${guestSession}`);
      if (savedFoods) {
        const foods = JSON.parse(savedFoods);
        setLoggedFoods(foods);
        updateSessionTotals(foods);
      }
    } catch (error) {
      console.error('Failed to initialize guest session:', error);
      // Fallback session ID
      const fallbackSession = `guest_${Date.now()}_${Math.random().toString(36).substr(2, 8)}`;
      setSessionId(fallbackSession);
      localStorage.setItem('guest_session_id', fallbackSession);
    }
  };

  const updateSessionTotals = (foods) => {
    const totalCalories = foods.reduce((sum, food) => sum + (food.calories || 0), 0);
    setSessionTotals({
      today_calories: totalCalories,
      meals_logged: foods.length,
      session_time: calculateSessionTime()
    });
  };

  const calculateSessionTime = () => {
    const sessionStart = localStorage.getItem('guest_session_start');
    if (sessionStart) {
      const startTime = new Date(sessionStart);
      const currentTime = new Date();
      const diffMinutes = Math.floor((currentTime - startTime) / (1000 * 60));
      return `${diffMinutes} minutes`;
    } else {
      localStorage.setItem('guest_session_start', new Date().toISOString());
      return '0 minutes';
    }
  };

  const handleAddFood = async () => {
    if (!newFood.trim()) return;

    setIsLogging(true);
    
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/guest/instant-food-log`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          food_name: newFood.trim(),
          session_id: sessionId,
          calories: estimateCalories(newFood), // Basic estimation
          meal_time: getMealTime(),
          logged_at: new Date().toISOString()
        }),
      });

      if (response.ok) {
        const result = await response.json();
        
        // Create new food entry with API response data
        const newEntry = {
          id: Date.now(),
          name: result.food_recognized,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          calories: result.estimated_nutrition.calories,
          protein: result.estimated_nutrition.protein,
          carbs: result.estimated_nutrition.carbs,
          fat: result.estimated_nutrition.fat,
          fiber: result.estimated_nutrition.fiber,
          meal: getMealTime(),
          api_feedback: result.instant_feedback,
          suggestions: result.simple_suggestions
        };

        // Update state
        const updatedFoods = [...loggedFoods, newEntry];
        setLoggedFoods(updatedFoods);
        setLastFeedback(result.instant_feedback);
        setLearningMoment(result.learning_moment);
        setSuggestions(result.simple_suggestions);
        
        // Update session totals from API response
        if (result.session_totals) {
          setSessionTotals(result.session_totals);
        } else {
          updateSessionTotals(updatedFoods);
        }

        // Save to localStorage
        localStorage.setItem(`guest_foods_${sessionId}`, JSON.stringify(updatedFoods));
        
        // Update streak tracking
        const today = new Date().toDateString();
        const lastLogDate = localStorage.getItem('last_log_date');
        const currentStreak = parseInt(localStorage.getItem('current_streak') || '0');
        
        if (lastLogDate !== today) {
          const newStreak = lastLogDate === new Date(Date.now() - 86400000).toDateString() ? currentStreak + 1 : 1;
          setStreakDays(newStreak);
          localStorage.setItem('current_streak', newStreak.toString());
          localStorage.setItem('last_log_date', today);
          
          // Show streak achievement feedback
          if (newStreak > 1) {
            setTimeout(() => {
              setRealtimeFeedback({
                type: 'streak_achievement',
                streakDays: newStreak,
                message: `${newStreak} day logging streak!`
              });
            }, 1500);
          }
        }
        
        // Show food logged feedback
        setRealtimeFeedback({
          type: 'food_logged',
          foodName: result.food_recognized,
          calories: result.estimated_nutrition.calories,
          insights: result.instant_feedback.slice(0, 2)
        });
        
        // Reset form
        setNewFood('');
        setShowAddForm(false);
        
        // Show success feedback briefly
        setTimeout(() => setLastFeedback(null), 10000); // Clear after 10 seconds
        
      } else {
        throw new Error('Failed to log food');
      }
    } catch (error) {
      console.error('Error logging food:', error);
      
      // Fallback to local storage if API fails
      const fallbackEntry = {
        id: Date.now(),
        name: newFood.trim(),
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        calories: estimateCalories(newFood),
        meal: getMealTime(),
        api_feedback: ['Food logged successfully! Keep up the great work.'],
        suggestions: ['Try adding some vegetables to make it even healthier!']
      };
      
      const updatedFoods = [...loggedFoods, fallbackEntry];
      setLoggedFoods(updatedFoods);
      updateSessionTotals(updatedFoods);
      localStorage.setItem(`guest_foods_${sessionId}`, JSON.stringify(updatedFoods));
      
      setNewFood('');
      setShowAddForm(false);
      setLastFeedback(['Food logged successfully! (Offline mode)']);
    } finally {
      setIsLogging(false);
    }
  };

  const estimateCalories = (foodName) => {
    // Simple calorie estimation based on food keywords
    const foodLower = foodName.toLowerCase();
    if (foodLower.includes('salad') || foodLower.includes('vegetable')) return 50;
    if (foodLower.includes('fruit') || foodLower.includes('apple') || foodLower.includes('banana')) return 80;
    if (foodLower.includes('chicken') || foodLower.includes('fish')) return 200;
    if (foodLower.includes('rice') || foodLower.includes('pasta')) return 220;
    if (foodLower.includes('bread') || foodLower.includes('toast')) return 150;
    if (foodLower.includes('egg')) return 70;
    if (foodLower.includes('yogurt')) return 100;
    return 180; // Default estimate
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
    updateSessionTotals(updatedFoods);
    localStorage.setItem(`guest_foods_${sessionId}`, JSON.stringify(updatedFoods));
  };

  const getTotalCalories = () => {
    return sessionTotals.today_calories || loggedFoods.reduce((total, food) => total + (food.calories || 0), 0);
  };

  const getMealColor = (meal) => {
    switch (meal) {
      case 'Breakfast': return 'bg-yellow-100 text-yellow-800';
      case 'Lunch': return 'bg-green-100 text-green-800';
      case 'Dinner': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const handleQuickAdd = async (foodName) => {
    setNewFood(foodName);
    setShowAddForm(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-violet-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Smart Food Log</h1>
          <p className="text-gray-600">Instant food tracking with AI-powered feedback and insights</p>
        </div>

        {/* Instant Feedback Section */}
        {lastFeedback && (
          <Card className="mb-6 border-2 border-green-200 bg-green-50">
            <CardContent className="pt-6">
              <div className="flex items-start space-x-3">
                <CheckCircle className="w-6 h-6 text-green-600 mt-1 flex-shrink-0" />
                <div className="flex-1">
                  <h3 className="font-semibold text-green-900 mb-2">Instant Feedback</h3>
                  <div className="space-y-1">
                    {lastFeedback.map((feedback, index) => (
                      <p key={index} className="text-sm text-green-800">{feedback}</p>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Learning Moment */}
        {learningMoment && (
          <Card className="mb-6 border-2 border-blue-200 bg-blue-50">
            <CardContent className="pt-6">
              <div className="flex items-start space-x-3">
                <Lightbulb className="w-6 h-6 text-blue-600 mt-1 flex-shrink-0" />
                <div>
                  <h3 className="font-semibold text-blue-900 mb-1">{learningMoment.tip}</h3>
                  <p className="text-sm text-blue-800">{learningMoment.content}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="border-2 border-purple-200 bg-purple-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 flex items-center">
                <Apple className="w-4 h-4 mr-2 text-purple-600" />
                Total Calories
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-purple-600">{getTotalCalories()}</div>
              <p className="text-xs text-gray-500">logged today</p>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-green-200 bg-green-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 flex items-center">
                <Clock className="w-4 h-4 mr-2 text-green-600" />
                Meals Logged
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{sessionTotals.meals_logged}</div>
              <p className="text-xs text-gray-500">entries today</p>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-orange-200 bg-orange-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 flex items-center">
                <Target className="w-4 h-4 mr-2 text-orange-600" />
                Session Time
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-lg font-bold text-orange-600">{sessionTotals.session_time}</div>
              <p className="text-xs text-gray-500">active tracking</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Quick Add Food */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <Plus className="w-5 h-5 mr-2 text-purple-600" />
                    Add Food
                  </span>
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
                      placeholder="What did you eat?"
                      value={newFood}
                      onChange={(e) => setNewFood(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleAddFood()}
                      disabled={isLogging}
                    />
                    <div className="flex space-x-2">
                      <Button 
                        onClick={handleAddFood} 
                        disabled={isLogging || !newFood.trim()}
                        className="bg-purple-600 hover:bg-purple-700"
                      >
                        {isLogging ? (
                          <>
                            <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                            Logging...
                          </>
                        ) : (
                          <>
                            <Sparkles className="w-4 h-4 mr-2" />
                            Log Food
                          </>
                        )}
                      </Button>
                      <Button variant="outline" onClick={() => setShowAddForm(false)} disabled={isLogging}>
                        Cancel
                      </Button>
                    </div>
                  </div>
                ) : (
                  <Button 
                    onClick={() => setShowAddForm(true)}
                    className="w-full bg-purple-600 hover:bg-purple-700"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Quick Add
                  </Button>
                )}

                <div className="border-t pt-4">
                  <h3 className="font-semibold text-gray-900 mb-2">Popular Foods</h3>
                  <div className="grid grid-cols-1 gap-2">
                    {[
                      'Scrambled eggs', 'Greek yogurt', 'Banana', 'Chicken breast', 
                      'Brown rice', 'Salmon', 'Mixed salad', 'Oatmeal'
                    ].map((food) => (
                      <Button
                        key={food}
                        variant="outline"
                        size="sm"
                        onClick={() => handleQuickAdd(food)}
                        className="text-xs justify-start hover:bg-purple-50"
                        disabled={isLogging}
                      >
                        {food}
                      </Button>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Suggestions Card */}
            {suggestions.length > 0 && (
              <Card className="mt-6">
                <CardHeader>
                  <CardTitle className="flex items-center text-sm">
                    <TrendingUp className="w-4 h-4 mr-2 text-green-600" />
                    Smart Suggestions
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {suggestions.map((suggestion, index) => (
                      <div key={index} className="flex items-start text-xs">
                        <Info className="w-3 h-3 text-blue-500 mr-2 mt-0.5 flex-shrink-0" />
                        <span className="text-gray-600">{suggestion}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Food Log Entries */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <Clock className="w-5 h-5 mr-2 text-purple-600" />
                    Today's Food Log
                  </span>
                  <Badge variant="secondary" className="bg-purple-100 text-purple-800">
                    {loggedFoods.length} entries
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {loggedFoods.length === 0 ? (
                  <div className="text-center py-12">
                    <Apple className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                    <div className="text-gray-400 mb-2">No food logged yet</div>
                    <p className="text-sm text-gray-500">Start by adding your first meal to get instant feedback!</p>
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
                          <Button 
                            variant="ghost" 
                            size="sm"
                            onClick={() => removeFood(food.id)}
                            className="text-red-500 hover:text-red-700"
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                        
                        <div className="flex items-center justify-between mb-3">
                          <h3 className="font-semibold text-gray-900">{food.name}</h3>
                          <div className="text-lg font-bold text-purple-600">
                            {food.calories} <span className="text-sm text-gray-500">cal</span>
                          </div>
                        </div>

                        {/* Nutrition breakdown if available */}
                        {food.protein && (
                          <div className="grid grid-cols-4 gap-2 text-xs text-gray-600 mb-3">
                            <div>Protein: {food.protein}g</div>
                            <div>Carbs: {food.carbs}g</div>
                            <div>Fat: {food.fat}g</div>
                            <div>Fiber: {food.fiber}g</div>
                          </div>
                        )}

                        {/* API Feedback for this specific food */}
                        {food.api_feedback && (
                          <div className="mt-3 p-3 bg-green-50 rounded-lg">
                            <div className="flex items-start space-x-2">
                              <Heart className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                              <div className="space-y-1">
                                {food.api_feedback.slice(0, 2).map((feedback, index) => (
                                  <p key={index} className="text-xs text-green-800">{feedback}</p>
                                ))}
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
                
                {loggedFoods.length > 0 && (
                  <div className="mt-6 p-4 bg-purple-50 rounded-lg">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-gray-900">Daily Total</span>
                      <span className="text-xl font-bold text-purple-600">
                        {getTotalCalories()} calories
                      </span>
                    </div>
                    <div className="mt-2 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-purple-600 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${Math.min((getTotalCalories() / 2000) * 100, 100)}%` }}
                      ></div>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      {Math.round((getTotalCalories() / 2000) * 100)}% of daily goal
                    </p>
                    
                    {/* Smart upgrade prompt based on progress */}
                    {getTotalCalories() > 1000 && (
                      <div className="mt-3 p-3 bg-gradient-to-r from-purple-100 to-violet-100 rounded-lg">
                        <div className="flex items-center space-x-2">
                          <Crown className="w-4 h-4 text-purple-600" />
                          <div className="text-xs">
                            <div className="font-semibold text-purple-900">Great progress!</div>
                            <div className="text-purple-700">Upgrade to track macros, get AI insights, and never lose your data.</div>
                          </div>
                        </div>
                        <Button
                          size="sm"
                          className="w-full mt-2 bg-gray-200 hover:bg-gray-300 text-gray-600 text-xs"
                        >
                          <Info className="w-3 h-3 mr-1" />
                          Learn About Premium
                        </Button>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Real-time Feedback */}
        {realtimeFeedback && (
          <RealTimeFeedback
            type={realtimeFeedback.type}
            data={realtimeFeedback}
            onAction={(action) => {
              console.log('Food log feedback action:', action);
            }}
            onDismiss={() => setRealtimeFeedback(null)}
            position="bottom-right"
          />
        )}
      </div>
    </div>
  );
};

export default GuestFoodLog;