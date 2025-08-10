import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import UpgradePrompt from './shared/UpgradePrompt';
import RealTimeFeedback from './shared/RealTimeFeedback';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { 
  Zap, Clock, Eye, UserX, Plus, Apple, 
  Target, Info, BookOpen, TrendingUp, Award,
  Camera, Search, Edit, Heart, Calculator, Crown
} from 'lucide-react';

// Component: Quick Start Guide
const QuickStart = () => (
  <Card className="col-span-full lg:col-span-2">
    <CardHeader>
      <CardTitle className="flex items-center">
        <Zap className="w-5 h-5 mr-2 text-purple-500" />
        Quick Start Guide
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div className="bg-purple-100 border border-purple-200 rounded-lg p-6 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <UserX className="w-6 h-6 text-purple-600" />
            <div>
              <h3 className="text-lg font-semibold text-purple-900">Guest Mode Active</h3>
              <p className="text-purple-700">Your data is temporarily stored and will not be saved permanently.</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Clock className="w-4 h-4 text-purple-600" />
            <span className="text-sm text-purple-700">{Math.floor(sessionTime / 60)}:{(sessionTime % 60).toString().padStart(2, '0')}</span>
          </div>
        </div>
        <div className="mt-3">
          <Button
            size="sm"
            className="bg-purple-600 hover:bg-purple-700 text-white"
            onClick={() => setShowUpgradePrompt(true)}
          >
            <Crown className="w-4 h-4 mr-2" />
            Save Progress - Create Free Account
          </Button>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="text-center p-4">
          <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
            <Apple className="w-6 h-6 text-blue-600" />
          </div>
          <h4 className="font-semibold text-gray-900 mb-2">1. Log Food</h4>
          <p className="text-sm text-gray-600">Start by logging what you eat today</p>
        </div>
        <div className="text-center p-4">
          <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
            <Target className="w-6 h-6 text-green-600" />
          </div>
          <h4 className="font-semibold text-gray-900 mb-2">2. Set Goals</h4>
          <p className="text-sm text-gray-600">Set simple health and nutrition goals</p>
        </div>
        <div className="text-center p-4">
          <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
            <TrendingUp className="w-6 h-6 text-purple-600" />
          </div>
          <h4 className="font-semibold text-gray-900 mb-2">3. Track Progress</h4>
          <p className="text-sm text-gray-600">See your nutrition insights instantly</p>
        </div>
      </div>
    </CardContent>
  </Card>
);

// Component: Simple Food Logging
const SimpleFoodLogging = () => {
  const [todayMeals, setTodayMeals] = useState([
    { id: 1, name: 'Coffee with milk', time: '8:00 AM', calories: 50 },
    { id: 2, name: 'Toast with avocado', time: '8:30 AM', calories: 320 }
  ]);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <Plus className="w-5 h-5 mr-2 text-green-500" />
          Simple Food Logging
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-3">
          <Button className="w-full justify-start bg-green-500 hover:bg-green-600">
            <Search className="w-4 h-4 mr-3" />
            Search Food
          </Button>
          <Button className="w-full justify-start bg-purple-500 hover:bg-purple-600">
            <Edit className="w-4 h-4 mr-3" />
            Quick Add
          </Button>
        </div>
        
        <div className="mt-6">
          <h4 className="font-semibold text-gray-900 mb-3">Today's Entries</h4>
          <div className="space-y-2">
            {todayMeals.map((meal) => (
              <div key={meal.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <div className="font-medium">{meal.name}</div>
                  <div className="text-sm text-gray-600">{meal.time}</div>
                </div>
                <div className="text-sm font-semibold text-blue-600">{meal.calories} cal</div>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

// Component: Basic Nutrition Info
const BasicNutritionInfo = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <Info className="w-5 h-5 mr-2 text-blue-500" />
        Basic Nutrition Info
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-4">
      <div className="p-3 bg-blue-50 rounded-lg">
        <div className="font-medium text-blue-900 mb-2">Daily Recommendations</div>
        <div className="space-y-1 text-sm text-blue-700">
          <div>Calories: 2000-2500</div>
          <div>Protein: 50-100g</div>
          <div>Fiber: 25-35g</div>
          <div>Water: 8-10 glasses</div>
        </div>
      </div>
      
      <div className="p-3 bg-green-50 rounded-lg">
        <div className="font-medium text-green-900 mb-2">Quick Tips</div>
        <div className="space-y-1 text-sm text-green-700">
          <div>• Fill half your plate with vegetables</div>
          <div>• Choose whole grains over refined</div>
          <div>• Include protein in every meal</div>
        </div>
      </div>
      
      <Button className="w-full bg-blue-500 hover:bg-blue-600">
        <BookOpen className="w-4 h-4 mr-2" />
        Learn More
      </Button>
    </CardContent>
  </Card>
);

// Component: Today's Calories
const TodayCalories = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <TrendingUp className="w-5 h-5 mr-2 text-orange-500" />
        Today's Calories
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-4">
      <div className="text-center p-6 bg-gradient-to-r from-orange-50 to-red-50 rounded-lg">
        <div className="text-3xl font-bold text-orange-600 mb-2">370</div>
        <div className="text-sm text-gray-600 mb-4">Calories logged today</div>
        <div className="text-xs text-gray-500">
          Based on your logged meals
        </div>
      </div>
      
      <div className="space-y-3">
        <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
          <span className="text-sm">Breakfast</span>
          <span className="font-semibold text-orange-600">370 cal</span>
        </div>
        <div className="flex justify-between items-center p-3 bg-gray-100 rounded-lg">
          <span className="text-sm text-gray-500">Lunch</span>
          <span className="text-sm text-gray-500">Not logged</span>
        </div>
        <div className="flex justify-between items-center p-3 bg-gray-100 rounded-lg">
          <span className="text-sm text-gray-500">Dinner</span>
          <span className="text-sm text-gray-500">Not logged</span>
        </div>
      </div>
    </CardContent>
  </Card>
);

// Component: Simple Goals
const SimpleGoals = () => {
  const navigate = useNavigate();
  
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span className="flex items-center">
            <Target className="w-5 h-5 mr-2 text-green-500" />
            Simple Goals
          </span>
          <Button 
            variant="ghost" 
            size="sm"
            onClick={() => navigate('/guest-goals')}
            className="text-xs text-purple-600 hover:text-purple-800"
          >
            View All →
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="p-3 bg-green-50 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <span className="font-medium text-green-900">Eat 5 servings of fruits/vegetables</span>
            <Badge className="bg-green-100 text-green-800">2/5</Badge>
          </div>
          <div className="w-full bg-green-200 rounded-full h-2">
            <div className="bg-green-500 h-2 rounded-full w-2/5"></div>
          </div>
        </div>
        
        <div className="p-3 bg-blue-50 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <span className="font-medium text-blue-900">Drink 8 glasses of water</span>
            <Badge className="bg-blue-100 text-blue-800">3/8</Badge>
          </div>
          <div className="w-full bg-blue-200 rounded-full h-2">
            <div className="bg-blue-500 h-2 rounded-full w-3/8"></div>
          </div>
        </div>
        
        <div className="p-3 bg-purple-50 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <span className="font-medium text-purple-900">Log all meals today</span>
            <Badge className="bg-purple-100 text-purple-800">1/3</Badge>
          </div>
          <div className="w-full bg-purple-200 rounded-full h-2">
            <div className="bg-purple-500 h-2 rounded-full w-1/3"></div>
          </div>
        </div>
        
        <Button 
          onClick={() => navigate('/guest-goals')}
          className="w-full bg-green-500 hover:bg-green-600"
        >
          <Target className="w-4 h-4 mr-2" />
          Manage Goals
        </Button>
      </CardContent>
    </Card>
  );
};

// Component: Nutrition Tips
const NutritionTips = () => (
  <Card className="col-span-full lg:col-span-2">
    <CardHeader>
      <CardTitle className="flex items-center">
        <BookOpen className="w-5 h-5 mr-2 text-green-500" />
        Nutrition Tips
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <h4 className="font-semibold text-gray-900">Today's Tip</h4>
          <div className="p-4 bg-green-50 rounded-lg border-l-4 border-green-500">
            <div className="flex items-start space-x-3">
              <Award className="w-6 h-6 text-green-600 mt-1 flex-shrink-0" />
              <div>
                <div className="font-medium text-green-900 mb-2">Stay Hydrated</div>
                <div className="text-sm text-green-700">
                  Drinking water before meals can help with portion control and digestion. 
                  Aim for at least 8 glasses throughout the day.
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="space-y-4">
          <h4 className="font-semibold text-gray-900">Quick Facts</h4>
          <div className="space-y-3">
            <div className="p-3 bg-blue-50 rounded-lg">
              <div className="font-medium text-blue-900">🥗 Fiber Fact</div>
              <div className="text-sm text-blue-700 mt-1">
                Adults need 25-35g of fiber daily for optimal digestive health.
              </div>
            </div>
            <div className="p-3 bg-purple-50 rounded-lg">
              <div className="font-medium text-purple-900">💪 Protein Power</div>
              <div className="text-sm text-purple-700 mt-1">
                Include protein in every meal to help maintain stable blood sugar levels.
              </div>
            </div>
            <div className="p-3 bg-orange-50 rounded-lg">
              <div className="font-medium text-orange-900">🌈 Color Variety</div>
              <div className="text-sm text-orange-700 mt-1">
                Eating different colored fruits and vegetables ensures diverse nutrients.
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="mt-6 text-center">
        <Button 
          className="bg-gradient-to-r from-purple-500 to-violet-600 hover:from-purple-600 hover:to-violet-700"
          onClick={handleUpgradeAction}
        >
          <Heart className="w-4 h-4 mr-2" />
          Create Free Account to Save Progress
        </Button>
      </div>
    </CardContent>
  </Card>
);

// Component: Health Calculator Quick Access
const HealthCalculatorCard = () => {
  const navigate = useNavigate();

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <Calculator className="w-5 h-5 mr-2 text-orange-500" />
          Health Calculator
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="p-3 bg-orange-50 rounded-lg">
          <div className="font-medium text-orange-900 mb-2">Calculate Your Health Metrics</div>
          <div className="space-y-1 text-sm text-orange-700">
            <div>• BMI (Body Mass Index)</div>
            <div>• BMR (Basal Metabolic Rate)</div>
            <div>• Daily Calorie Needs</div>
            <div>• Nutrition Recommendations</div>
          </div>
        </div>
        
        <div className="p-3 bg-gradient-to-r from-purple-100 to-violet-100 rounded-lg">
          <div className="font-medium text-purple-900 mb-1">Instant Results</div>
          <div className="text-sm text-purple-700">
            Get personalized health insights based on your age, gender, height, weight, and activity level.
          </div>
        </div>
        
        <Button 
          onClick={() => navigate('/guest-calculator')}
          className="w-full bg-orange-500 hover:bg-orange-600"
        >
          <Calculator className="w-4 h-4 mr-2" />
          Calculate Now
        </Button>
      </CardContent>
    </Card>
  );
};

// Main Guest Dashboard Component
const GuestDashboard = () => {
  const { switchRole } = useRole();
  const [sessionTime, setSessionTime] = useState(0);
  const [showUpgradePrompt, setShowUpgradePrompt] = useState(false);
  const [realtimeFeedback, setRealtimeFeedback] = useState(null);
  const [visitCount, setVisitCount] = useState(0);

  // Set role to guest when component mounts
  useEffect(() => {
    switchRole('guest');
    
    // Track session time and visit count for upgrade triggers
    const startTime = Date.now();
    const currentVisits = parseInt(localStorage.getItem('guest_visit_count') || '0') + 1;
    setVisitCount(currentVisits);
    localStorage.setItem('guest_visit_count', currentVisits.toString());
    
    // Update session time every 30 seconds
    const sessionTimer = setInterval(() => {
      setSessionTime(Math.floor((Date.now() - startTime) / 1000));
    }, 30000);
    
    // Show upgrade prompt after 2 minutes or 3rd visit
    const timer = setTimeout(() => {
      if (currentVisits >= 3) {
        setShowUpgradePrompt(true);
      }
    }, 120000); // 2 minutes
    
    // Show welcome feedback for new users
    if (currentVisits === 1) {
      setTimeout(() => {
        setRealtimeFeedback({
          type: 'welcome_tip',
          title: 'Welcome to Guest Mode!',
          insights: [
            'Start by calculating your BMI for personalized insights',
            'Log your first meal to see instant nutrition feedback',
            'Set simple goals to track your progress'
          ]
        });
      }, 3000);
    }
    
    return () => {
      clearTimeout(timer);
      clearInterval(sessionTimer);
    };
  }, [switchRole]);

  const handleUpgradeAction = () => {
    console.log('Upgrade action triggered from dashboard');
    // Implement upgrade flow
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-violet-100">
      <SmartNavigation />
      <div className="max-w-7xl mx-auto p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <QuickStart />
          <SimpleFoodLogging />
          <HealthCalculatorCard />
          <BasicNutritionInfo />
          <TodayCalories />
          <SimpleGoals />
          <NutritionTips />
        </div>
      </div>
    </div>
  );
};

export default GuestDashboard;