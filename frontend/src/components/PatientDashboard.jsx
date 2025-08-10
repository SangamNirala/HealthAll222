import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Progress } from './ui/progress';
import { 
  Activity, Apple, Target, TrendingUp, Camera, 
  Scale, Heart, Droplets, Plus, Clock, Award, ChevronRight 
} from 'lucide-react';

// Component: Welcome Card
const WelcomeCard = () => (
  <Card className="col-span-full lg:col-span-2">
    <CardContent className="p-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome back, Sarah!</h2>
          <p className="text-gray-600">You're making great progress on your health journey</p>
        </div>
        <div className="text-4xl">👋</div>
      </div>
    </CardContent>
  </Card>
);

// Component: Today's Nutrition Summary
const TodayNutritionSummary = () => (
  <Card className="col-span-full lg:col-span-2">
    <CardHeader>
      <CardTitle className="flex items-center">
        <Activity className="w-5 h-5 mr-2 text-blue-500" />
        Today's Nutrition Summary
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="text-center p-4 bg-blue-50 rounded-lg">
          <div className="text-2xl font-bold text-blue-600">1,847</div>
          <div className="text-sm text-gray-600">Calories</div>
          <div className="text-xs text-green-600">-153 remaining</div>
        </div>
        <div className="text-center p-4 bg-green-50 rounded-lg">
          <div className="text-2xl font-bold text-green-600">98g</div>
          <div className="text-sm text-gray-600">Protein</div>
          <div className="text-xs text-green-600">Target: 120g</div>
        </div>
        <div className="text-center p-4 bg-orange-50 rounded-lg">
          <div className="text-2xl font-bold text-orange-600">147g</div>
          <div className="text-sm text-gray-600">Carbs</div>
          <div className="text-xs text-blue-600">Target: 200g</div>
        </div>
        <div className="text-center p-4 bg-purple-50 rounded-lg">
          <div className="text-2xl font-bold text-purple-600">52g</div>
          <div className="text-sm text-gray-600">Fat</div>
          <div className="text-xs text-green-600">Target: 65g</div>
        </div>
      </div>
    </CardContent>
  </Card>
);

// Component: Quick Food Logging
const QuickFoodLogging = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <Camera className="w-5 h-5 mr-2 text-green-500" />
        Quick Food Logging
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-3">
      <Button className="w-full justify-start bg-blue-500 hover:bg-blue-600">
        <Camera className="w-4 h-4 mr-3" />
        Take Photo
      </Button>
      <Button className="w-full justify-start bg-green-500 hover:bg-green-600">
        <Apple className="w-4 h-4 mr-3" />
        Search Food
      </Button>
      <Button className="w-full justify-start bg-purple-500 hover:bg-purple-600">
        <Plus className="w-4 h-4 mr-3" />
        Manual Entry
      </Button>
    </CardContent>
  </Card>
);

// Component: Health Metrics Overview
const HealthMetricsOverview = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <Heart className="w-5 h-5 mr-2 text-red-500" />
        Health Metrics
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-4">
      <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
        <div className="flex items-center space-x-3">
          <Heart className="w-5 h-5 text-red-500" />
          <div>
            <div className="font-semibold">Blood Pressure</div>
            <div className="text-sm text-gray-600">120/80 mmHg</div>
          </div>
        </div>
        <div className="text-green-600 text-sm">Normal</div>
      </div>
      <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
        <div className="flex items-center space-x-3">
          <Scale className="w-5 h-5 text-blue-500" />
          <div>
            <div className="font-semibold">Weight</div>
            <div className="text-sm text-gray-600">68.5 kg</div>
          </div>
        </div>
        <div className="text-blue-600 text-sm">-0.3kg</div>
      </div>
      <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
        <div className="flex items-center space-x-3">
          <Droplets className="w-5 h-5 text-purple-500" />
          <div>
            <div className="font-semibold">Glucose</div>
            <div className="text-sm text-gray-600">95 mg/dL</div>
          </div>
        </div>
        <div className="text-green-600 text-sm">Normal</div>
      </div>
    </CardContent>
  </Card>
);

// Component: Goal Progress
const GoalProgress = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <Target className="w-5 h-5 mr-2 text-green-500" />
        Goal Progress
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-4">
      <div>
        <div className="flex justify-between text-sm mb-2">
          <span>Daily Steps</span>
          <span>8,432 / 10,000</span>
        </div>
        <Progress value={84} />
      </div>
      <div>
        <div className="flex justify-between text-sm mb-2">
          <span>Water Intake</span>
          <span>6 / 8 glasses</span>
        </div>
        <Progress value={75} />
      </div>
      <div>
        <div className="flex justify-between text-sm mb-2">
          <span>Weekly Exercise</span>
          <span>3 / 5 sessions</span>
        </div>
        <Progress value={60} />
      </div>
    </CardContent>
  </Card>
);

// Component: Recent Meals
const RecentMeals = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <Clock className="w-5 h-5 mr-2 text-orange-500" />
        Recent Meals
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-3">
      <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
        <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
          <Apple className="w-6 h-6 text-orange-500" />
        </div>
        <div className="flex-1">
          <div className="font-medium">Breakfast</div>
          <div className="text-sm text-gray-600">Oatmeal with berries</div>
          <div className="text-xs text-gray-500">350 calories</div>
        </div>
        <ChevronRight className="w-4 h-4 text-gray-400" />
      </div>
      <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
        <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
          <Apple className="w-6 h-6 text-green-500" />
        </div>
        <div className="flex-1">
          <div className="font-medium">Lunch</div>
          <div className="text-sm text-gray-600">Grilled chicken salad</div>
          <div className="text-xs text-gray-500">425 calories</div>
        </div>
        <ChevronRight className="w-4 h-4 text-gray-400" />
      </div>
    </CardContent>
  </Card>
);

// Component: AI Recommendations
const AIRecommendations = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <Award className="w-5 h-5 mr-2 text-purple-500" />
        AI Recommendations
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-3">
      <div className="p-3 bg-purple-50 rounded-lg">
        <div className="font-medium text-purple-900">Meal Suggestion</div>
        <div className="text-sm text-purple-700 mt-1">
          Try a protein-rich snack like Greek yogurt to reach your daily protein goal.
        </div>
      </div>
      <div className="p-3 bg-blue-50 rounded-lg">
        <div className="font-medium text-blue-900">Hydration Reminder</div>
        <div className="text-sm text-blue-700 mt-1">
          You're 2 glasses behind your water goal. Have a glass now!
        </div>
      </div>
      <div className="p-3 bg-green-50 rounded-lg">
        <div className="font-medium text-green-900">Activity Boost</div>
        <div className="text-sm text-green-700 mt-1">
          A 15-minute walk would help you reach your step goal.
        </div>
      </div>
    </CardContent>
  </Card>
);

// Component: Progress Charts
const ProgressCharts = () => (
  <Card className="col-span-full lg:col-span-2">
    <CardHeader>
      <CardTitle className="flex items-center">
        <TrendingUp className="w-5 h-5 mr-2 text-blue-500" />
        Progress Charts
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div className="h-64 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg flex items-center justify-center">
        <div className="text-center">
          <TrendingUp className="w-12 h-12 text-blue-500 mx-auto mb-4" />
          <div className="text-lg font-medium text-gray-900">Weight Progress</div>
          <div className="text-sm text-gray-600">Chart visualization coming soon</div>
        </div>
      </div>
    </CardContent>
  </Card>
);

// Main Patient Dashboard Component
const PatientDashboard = () => {
  const { switchRole } = useRole();

  // Set role to patient when component mounts
  useEffect(() => {
    switchRole('patient');
  }, [switchRole]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <SmartNavigation />
      <div className="max-w-7xl mx-auto p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <WelcomeCard />
          <TodayNutritionSummary />
          <QuickFoodLogging />
          <HealthMetricsOverview />
          <GoalProgress />
          <RecentMeals />
          <AIRecommendations />
          <ProgressCharts />
        </div>
      </div>
    </div>
  );
};

export default PatientDashboard;