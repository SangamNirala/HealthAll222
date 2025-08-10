import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { 
  Target, Plus, Edit, Trash2, CheckCircle, Clock, 
  TrendingUp, Award, Zap, Heart, Droplets, Apple,
  Activity, Calendar, AlertCircle, Star, Trophy,
  PieChart, BarChart3, User
} from 'lucide-react';

const GuestGoals = () => {
  const { switchRole } = useRole();
  const [goals, setGoals] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingGoal, setEditingGoal] = useState(null);
  const [sessionId, setSessionId] = useState('');
  const [newGoal, setNewGoal] = useState({
    title: '',
    category: 'nutrition',
    target: '',
    unit: 'servings',
    current: 0,
    timeframe: 'daily'
  });
  const [sessionStats, setSessionStats] = useState({
    totalGoals: 0,
    completedToday: 0,
    streakDays: 0,
    sessionTime: '0 minutes'
  });

  // Goal categories with icons and colors
  const goalCategories = {
    nutrition: { 
      icon: Apple, 
      color: 'bg-green-100 text-green-800', 
      label: 'Nutrition',
      examples: ['Eat 5 servings of vegetables', 'Include protein in every meal']
    },
    hydration: { 
      icon: Droplets, 
      color: 'bg-blue-100 text-blue-800', 
      label: 'Hydration',
      examples: ['Drink 8 glasses of water', 'Have herbal tea twice daily']
    },
    activity: { 
      icon: Activity, 
      color: 'bg-orange-100 text-orange-800', 
      label: 'Activity',
      examples: ['Walk 10,000 steps', 'Exercise for 30 minutes']
    },
    habits: { 
      icon: Clock, 
      color: 'bg-purple-100 text-purple-800', 
      label: 'Healthy Habits',
      examples: ['Log all meals', 'Eat breakfast daily']
    },
    wellness: { 
      icon: Heart, 
      color: 'bg-pink-100 text-pink-800', 
      label: 'Wellness',
      examples: ['Get 8 hours of sleep', 'Take vitamins daily']
    }
  };

  // Initialize guest session and load goals
  useEffect(() => {
    switchRole('guest');
    initializeGuestGoals();
  }, [switchRole]);

  const initializeGuestGoals = async () => {
    try {
      // Get or create session ID
      let guestSession = localStorage.getItem('guest_session_id');
      
      if (!guestSession) {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/guest/session`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        });
        
        if (response.ok) {
          const sessionData = await response.json();
          guestSession = sessionData.session_id;
          localStorage.setItem('guest_session_id', guestSession);
          localStorage.setItem('guest_session_expires', sessionData.expires_at);
        } else {
          guestSession = `guest_${Date.now()}_${Math.random().toString(36).substr(2, 8)}`;
          localStorage.setItem('guest_session_id', guestSession);
        }
      }
      
      setSessionId(guestSession);
      
      // Load existing goals from localStorage
      const savedGoals = localStorage.getItem(`guest_goals_${guestSession}`);
      if (savedGoals) {
        const parsedGoals = JSON.parse(savedGoals);
        setGoals(parsedGoals);
        updateSessionStats(parsedGoals);
      } else {
        // Initialize with sample goals for new sessions
        initializeSampleGoals(guestSession);
      }
    } catch (error) {
      console.error('Failed to initialize guest goals:', error);
      const fallbackSession = `guest_${Date.now()}_${Math.random().toString(36).substr(2, 8)}`;
      setSessionId(fallbackSession);
      localStorage.setItem('guest_session_id', fallbackSession);
      initializeSampleGoals(fallbackSession);
    }
  };

  const initializeSampleGoals = (sessionId) => {
    const sampleGoals = [
      {
        id: Date.now() + 1,
        title: 'Eat 5 servings of fruits/vegetables',
        category: 'nutrition',
        target: 5,
        unit: 'servings',
        current: 0,
        timeframe: 'daily',
        createdAt: new Date().toISOString(),
        lastUpdated: new Date().toISOString()
      },
      {
        id: Date.now() + 2,
        title: 'Drink 8 glasses of water',
        category: 'hydration',
        target: 8,
        unit: 'glasses',
        current: 0,
        timeframe: 'daily',
        createdAt: new Date().toISOString(),
        lastUpdated: new Date().toISOString()
      },
      {
        id: Date.now() + 3,
        title: 'Log all meals today',
        category: 'habits',
        target: 3,
        unit: 'meals',
        current: 0,
        timeframe: 'daily',
        createdAt: new Date().toISOString(),
        lastUpdated: new Date().toISOString()
      }
    ];
    
    setGoals(sampleGoals);
    updateSessionStats(sampleGoals);
    localStorage.setItem(`guest_goals_${sessionId}`, JSON.stringify(sampleGoals));
  };

  const updateSessionStats = (goalsList) => {
    const totalGoals = goalsList.length;
    const completedToday = goalsList.filter(goal => goal.current >= goal.target).length;
    const sessionStart = localStorage.getItem('guest_session_start') || new Date().toISOString();
    const sessionTime = calculateSessionTime(sessionStart);
    
    setSessionStats({
      totalGoals,
      completedToday,
      streakDays: calculateStreak(goalsList),
      sessionTime
    });
  };

  const calculateSessionTime = (startTime) => {
    const start = new Date(startTime);
    const now = new Date();
    const diffMinutes = Math.floor((now - start) / (1000 * 60));
    
    if (diffMinutes < 60) return `${diffMinutes} minutes`;
    const hours = Math.floor(diffMinutes / 60);
    const minutes = diffMinutes % 60;
    return `${hours}h ${minutes}m`;
  };

  const calculateStreak = (goalsList) => {
    // Simple streak calculation based on completed goals
    return goalsList.filter(goal => goal.current > 0).length;
  };

  const saveGoals = (updatedGoals) => {
    setGoals(updatedGoals);
    updateSessionStats(updatedGoals);
    localStorage.setItem(`guest_goals_${sessionId}`, JSON.stringify(updatedGoals));
    
    // Sync with backend if available
    syncGoalsWithBackend(updatedGoals);
  };

  const syncGoalsWithBackend = async (goalsList) => {
    try {
      await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/guest/goals/${sessionId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goals: goalsList })
      });
    } catch (error) {
      console.log('Backend sync failed, using local storage only:', error);
    }
  };

  const addGoal = () => {
    if (!newGoal.title || !newGoal.target) return;
    
    const goal = {
      id: Date.now(),
      ...newGoal,
      target: parseInt(newGoal.target),
      current: 0,
      createdAt: new Date().toISOString(),
      lastUpdated: new Date().toISOString()
    };
    
    const updatedGoals = [...goals, goal];
    saveGoals(updatedGoals);
    
    // Reset form
    setNewGoal({
      title: '',
      category: 'nutrition',
      target: '',
      unit: 'servings',
      current: 0,
      timeframe: 'daily'
    });
    setShowAddForm(false);
  };

  const updateGoalProgress = (goalId, increment = 1) => {
    const updatedGoals = goals.map(goal => {
      if (goal.id === goalId) {
        const newCurrent = Math.max(0, Math.min(goal.current + increment, goal.target));
        return {
          ...goal,
          current: newCurrent,
          lastUpdated: new Date().toISOString()
        };
      }
      return goal;
    });
    
    saveGoals(updatedGoals);
  };

  const deleteGoal = (goalId) => {
    const updatedGoals = goals.filter(goal => goal.id !== goalId);
    saveGoals(updatedGoals);
  };

  const resetDailyGoals = () => {
    const updatedGoals = goals.map(goal => ({
      ...goal,
      current: 0,
      lastUpdated: new Date().toISOString()
    }));
    saveGoals(updatedGoals);
  };

  const getProgressPercentage = (current, target) => {
    return Math.min((current / target) * 100, 100);
  };

  const getProgressColor = (percentage) => {
    if (percentage >= 100) return 'bg-green-500';
    if (percentage >= 75) return 'bg-blue-500';
    if (percentage >= 50) return 'bg-yellow-500';
    return 'bg-gray-300';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-violet-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Smart Goal Tracking</h1>
          <p className="text-gray-600">Set and track your daily nutrition and wellness goals</p>
        </div>

        {/* Session Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-2 border-purple-200 bg-purple-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 flex items-center">
                <Target className="w-4 h-4 mr-2 text-purple-600" />
                Active Goals
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-purple-600">{sessionStats.totalGoals}</div>
              <p className="text-xs text-gray-500">goals set</p>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-green-200 bg-green-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 flex items-center">
                <CheckCircle className="w-4 h-4 mr-2 text-green-600" />
                Completed Today
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{sessionStats.completedToday}</div>
              <p className="text-xs text-gray-500">goals achieved</p>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-orange-200 bg-orange-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 flex items-center">
                <Trophy className="w-4 h-4 mr-2 text-orange-600" />
                Progress Streak
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-orange-600">{sessionStats.streakDays}</div>
              <p className="text-xs text-gray-500">active goals</p>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-blue-200 bg-blue-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 flex items-center">
                <Clock className="w-4 h-4 mr-2 text-blue-600" />
                Session Time
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-lg font-bold text-blue-600">{sessionStats.sessionTime}</div>
              <p className="text-xs text-gray-500">tracking time</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Goal Management */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <Plus className="w-5 h-5 mr-2 text-purple-600" />
                    Add New Goal
                  </span>
                  {goals.length > 0 && (
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={resetDailyGoals}
                      className="text-xs"
                    >
                      Reset Daily
                    </Button>
                  )}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {showAddForm ? (
                  <div className="space-y-3">
                    <Input
                      placeholder="Goal title (e.g., Drink 8 glasses of water)"
                      value={newGoal.title}
                      onChange={(e) => setNewGoal({...newGoal, title: e.target.value})}
                    />
                    
                    <select
                      className="w-full p-2 border rounded-md"
                      value={newGoal.category}
                      onChange={(e) => setNewGoal({...newGoal, category: e.target.value})}
                    >
                      {Object.entries(goalCategories).map(([key, cat]) => (
                        <option key={key} value={key}>{cat.label}</option>
                      ))}
                    </select>
                    
                    <div className="grid grid-cols-2 gap-2">
                      <Input
                        type="number"
                        placeholder="Target"
                        value={newGoal.target}
                        onChange={(e) => setNewGoal({...newGoal, target: e.target.value})}
                        min="1"
                      />
                      <select
                        className="p-2 border rounded-md"
                        value={newGoal.unit}
                        onChange={(e) => setNewGoal({...newGoal, unit: e.target.value})}
                      >
                        <option value="servings">servings</option>
                        <option value="glasses">glasses</option>
                        <option value="meals">meals</option>
                        <option value="minutes">minutes</option>
                        <option value="times">times</option>
                        <option value="hours">hours</option>
                      </select>
                    </div>
                    
                    <div className="flex space-x-2">
                      <Button 
                        onClick={addGoal}
                        disabled={!newGoal.title || !newGoal.target}
                        className="bg-purple-600 hover:bg-purple-700"
                      >
                        Add Goal
                      </Button>
                      <Button 
                        variant="outline" 
                        onClick={() => setShowAddForm(false)}
                      >
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
                    Set New Goal
                  </Button>
                )}

                {/* Goal Categories Preview */}
                <div className="border-t pt-4">
                  <h3 className="font-semibold text-gray-900 mb-2">Goal Categories</h3>
                  <div className="space-y-2">
                    {Object.entries(goalCategories).map(([key, category]) => {
                      const Icon = category.icon;
                      return (
                        <div key={key} className="flex items-center text-sm">
                          <Icon className="w-4 h-4 mr-2 text-gray-600" />
                          <span className="text-gray-700">{category.label}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Upgrade Prompt */}
            <Card className="mt-6 border-2 border-purple-200 bg-gradient-to-r from-purple-50 to-violet-50">
              <CardContent className="pt-6">
                <div className="text-center">
                  <Zap className="w-8 h-8 text-purple-600 mx-auto mb-3" />
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Unlock Advanced Goal Tracking</h3>
                  <p className="text-sm text-gray-600 mb-4">
                    Create an account to save your progress permanently, set weekly/monthly goals, and get AI-powered recommendations.
                  </p>
                  <Button className="bg-purple-600 hover:bg-purple-700">
                    <Star className="w-4 h-4 mr-2" />
                    Create Free Account
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Goals List */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <BarChart3 className="w-5 h-5 mr-2 text-purple-600" />
                    Today's Goals ({goals.length})
                  </span>
                  <Badge variant="secondary" className="bg-purple-100 text-purple-800">
                    {sessionStats.completedToday}/{sessionStats.totalGoals} completed
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {goals.length === 0 ? (
                  <div className="text-center py-12">
                    <Target className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                    <div className="text-gray-400 mb-2">No goals set yet</div>
                    <p className="text-sm text-gray-500">Create your first goal to start tracking your progress!</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {goals.map((goal) => {
                      const category = goalCategories[goal.category];
                      const Icon = category.icon;
                      const progress = getProgressPercentage(goal.current, goal.target);
                      const isCompleted = goal.current >= goal.target;
                      
                      return (
                        <div key={goal.id} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
                          <div className="flex items-center justify-between mb-3">
                            <div className="flex items-center space-x-3">
                              <div className="flex items-center space-x-2">
                                <Icon className="w-5 h-5 text-gray-600" />
                                <Badge className={category.color} size="sm">
                                  {category.label}
                                </Badge>
                              </div>
                              {isCompleted && (
                                <CheckCircle className="w-5 h-5 text-green-600" />
                              )}
                            </div>
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => deleteGoal(goal.id)}
                              className="text-red-500 hover:text-red-700"
                            >
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                          
                          <h3 className="font-semibold text-gray-900 mb-2">{goal.title}</h3>
                          
                          <div className="flex items-center justify-between mb-3">
                            <div className="flex items-center space-x-2">
                              <span className="text-2xl font-bold text-purple-600">
                                {goal.current}
                              </span>
                              <span className="text-gray-500">/ {goal.target} {goal.unit}</span>
                            </div>
                            <div className="text-right">
                              <div className="text-sm font-semibold text-gray-700">
                                {Math.round(progress)}%
                              </div>
                              <div className="text-xs text-gray-500">complete</div>
                            </div>
                          </div>

                          {/* Progress Bar */}
                          <div className="w-full bg-gray-200 rounded-full h-3 mb-3">
                            <div 
                              className={`h-3 rounded-full transition-all duration-500 ${getProgressColor(progress)}`}
                              style={{ width: `${progress}%` }}
                            ></div>
                          </div>

                          {/* Progress Controls */}
                          <div className="flex items-center justify-between">
                            <div className="flex space-x-2">
                              <Button 
                                variant="outline" 
                                size="sm"
                                onClick={() => updateGoalProgress(goal.id, -1)}
                                disabled={goal.current <= 0}
                                className="text-xs"
                              >
                                -1
                              </Button>
                              <Button 
                                variant="outline" 
                                size="sm"
                                onClick={() => updateGoalProgress(goal.id, 1)}
                                disabled={goal.current >= goal.target}
                                className="text-xs bg-purple-50 hover:bg-purple-100 text-purple-700"
                              >
                                +1
                              </Button>
                            </div>
                            
                            {isCompleted && (
                              <div className="flex items-center text-green-600 text-sm">
                                <Award className="w-4 h-4 mr-1" />
                                Goal Achieved!
                              </div>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
                
                {/* Daily Summary */}
                {goals.length > 0 && (
                  <div className="mt-6 p-4 bg-gradient-to-r from-purple-50 to-violet-50 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold text-gray-900">Daily Progress</span>
                      <span className="text-lg font-bold text-purple-600">
                        {Math.round((sessionStats.completedToday / sessionStats.totalGoals) * 100)}%
                      </span>
                    </div>
                    <div className="bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-purple-600 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${(sessionStats.completedToday / sessionStats.totalGoals) * 100}%` }}
                      ></div>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      {sessionStats.completedToday} of {sessionStats.totalGoals} goals completed today
                    </p>
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

export default GuestGoals;