import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Input } from '../ui/input';
import { Textarea } from '../ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Checkbox } from '../ui/checkbox';
import { 
  ChefHat, 
  Apple, 
  Heart, 
  Calculator, 
  ShoppingCart,
  Calendar,
  Star,
  Clock,
  Users,
  Utensils,
  AlertCircle,
  CheckCircle,
  TrendingUp,
  Loader2,
  Download,
  RefreshCw,
  Target,
  Award
} from 'lucide-react';
import SmartNavigation from '../shared/SmartNavigation';

const IntelligentMealPlanGenerator = () => {
  const [mealPlans, setMealPlans] = useState([]);
  const [currentPlan, setCurrentPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedPatient, setSelectedPatient] = useState('patient-456');

  // Meal plan creation form
  const [planForm, setPlanForm] = useState({
    duration_weeks: 1,
    target_calories: 2000,
    dietary_restrictions: [],
    allergies: [],
    cultural_preferences: 'american',
    meal_types: ['breakfast', 'lunch', 'dinner'],
    budget_range: 'moderate',
    cooking_skill: 'intermediate',
    prep_time_limit: 60,
    health_goals: []
  });

  // Available options
  const dietaryRestrictions = [
    'vegetarian', 'vegan', 'gluten-free', 'dairy-free', 'keto', 
    'paleo', 'low-sodium', 'diabetic', 'heart-healthy'
  ];
  
  const allergies = [
    'nuts', 'dairy', 'eggs', 'soy', 'shellfish', 'fish', 'wheat', 'sesame'
  ];
  
  const healthGoals = [
    'weight_loss', 'muscle_gain', 'heart_health', 'diabetes_management',
    'digestive_health', 'energy_boost', 'immune_support'
  ];

  const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;

  // Fetch existing meal plans
  const fetchMealPlans = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/provider/patient-management/meal-plans/${selectedPatient}`);
      if (response.ok) {
        const data = await response.json();
        setMealPlans(data.meal_plans || []);
        if (data.meal_plans && data.meal_plans.length > 0) {
          setCurrentPlan(data.meal_plans[0]);
        }
      } else {
        throw new Error('Failed to fetch meal plans');
      }
    } catch (err) {
      setError(`Error fetching meal plans: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Generate new meal plan
  const generateMealPlan = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/provider/patient-management/meal-plans`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_id: selectedPatient,
          provider_id: 'provider-123',
          meal_plan_preferences: planForm
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setCurrentPlan(data);
        await fetchMealPlans(); // Refresh list
      } else {
        throw new Error('Failed to generate meal plan');
      }
    } catch (err) {
      setError(`Error generating meal plan: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMealPlans();
  }, [selectedPatient]);

  // Handle form changes
  const handleFormChange = (field, value) => {
    setPlanForm(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleArrayToggle = (field, item) => {
    setPlanForm(prev => ({
      ...prev,
      [field]: prev[field].includes(item)
        ? prev[field].filter(i => i !== item)
        : [...prev[field], item]
    }));
  };

  // Calculate nutritional completeness score
  const calculateNutritionalScore = (plan) => {
    if (!plan || !plan.nutritional_analysis) return 0;
    const analysis = plan.nutritional_analysis;
    
    // Simple scoring based on balanced macros
    const proteinScore = Math.min(analysis.protein_percentage / 25, 1) * 30;
    const carbScore = Math.min(analysis.carb_percentage / 50, 1) * 40;
    const fatScore = Math.min(analysis.fat_percentage / 30, 1) * 30;
    
    return Math.round(proteinScore + carbScore + fatScore);
  };

  const getMealVarietyScore = (plan) => {
    if (!plan || !plan.weekly_meals) return 0;
    const uniqueIngredients = new Set();
    plan.weekly_meals.forEach(meal => {
      meal.ingredients?.forEach(ingredient => uniqueIngredients.add(ingredient.name));
    });
    return Math.min(Math.round(uniqueIngredients.size / 5), 100);
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
        <SmartNavigation />
        <div className="container mx-auto px-4 py-8">
          <Card className="max-w-md mx-auto">
            <CardContent className="p-6 text-center">
              <AlertCircle className="mx-auto mb-4 h-12 w-12 text-red-500" />
              <p className="text-red-600">{error}</p>
              <Button onClick={() => window.location.reload()} className="mt-4">
                Try Again
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
      <SmartNavigation />
      
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <ChefHat className="h-8 w-8 text-emerald-600" />
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Intelligent Meal Plan Generator</h1>
                <p className="text-gray-600">AI-powered meal planning with USDA nutrition data integration</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <Select value={selectedPatient} onValueChange={setSelectedPatient}>
                <SelectTrigger className="w-48">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="patient-456">Patient 456 (Demo)</SelectItem>
                  <SelectItem value="patient-789">Patient 789</SelectItem>
                  <SelectItem value="patient-123">Patient 123</SelectItem>
                </SelectContent>
              </Select>
              
              <Button
                onClick={fetchMealPlans}
                disabled={loading}
                className="bg-emerald-600 hover:bg-emerald-700"
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <RefreshCw className="h-4 w-4" />}
              </Button>
            </div>
          </div>
        </div>

        <Tabs defaultValue="generator" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 bg-white">
            <TabsTrigger value="generator">Plan Generator</TabsTrigger>
            <TabsTrigger value="current">Current Plan</TabsTrigger>
            <TabsTrigger value="nutrition">Nutrition Analysis</TabsTrigger>
            <TabsTrigger value="shopping">Shopping List</TabsTrigger>
          </TabsList>

          {/* Plan Generator Tab */}
          <TabsContent value="generator" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Plan Configuration */}
              <div className="lg:col-span-2 space-y-6">
                {/* Basic Settings */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Target className="h-5 w-5" />
                      Plan Configuration
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div>
                        <label className="text-sm font-medium">Duration (weeks)</label>
                        <Select 
                          value={planForm.duration_weeks.toString()} 
                          onValueChange={(value) => handleFormChange('duration_weeks', parseInt(value))}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="1">1 Week</SelectItem>
                            <SelectItem value="2">2 Weeks</SelectItem>
                            <SelectItem value="4">1 Month</SelectItem>
                            <SelectItem value="8">2 Months</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      
                      <div>
                        <label className="text-sm font-medium">Target Calories/Day</label>
                        <Input
                          type="number"
                          value={planForm.target_calories}
                          onChange={(e) => handleFormChange('target_calories', parseInt(e.target.value))}
                          placeholder="2000"
                        />
                      </div>
                      
                      <div>
                        <label className="text-sm font-medium">Budget Range</label>
                        <Select 
                          value={planForm.budget_range} 
                          onValueChange={(value) => handleFormChange('budget_range', value)}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="budget">Budget-friendly</SelectItem>
                            <SelectItem value="moderate">Moderate</SelectItem>
                            <SelectItem value="premium">Premium</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="text-sm font-medium">Cultural Preference</label>
                        <Select 
                          value={planForm.cultural_preferences} 
                          onValueChange={(value) => handleFormChange('cultural_preferences', value)}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="american">American</SelectItem>
                            <SelectItem value="mediterranean">Mediterranean</SelectItem>
                            <SelectItem value="asian">Asian</SelectItem>
                            <SelectItem value="mexican">Mexican</SelectItem>
                            <SelectItem value="indian">Indian</SelectItem>
                            <SelectItem value="italian">Italian</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      
                      <div>
                        <label className="text-sm font-medium">Cooking Skill Level</label>
                        <Select 
                          value={planForm.cooking_skill} 
                          onValueChange={(value) => handleFormChange('cooking_skill', value)}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="beginner">Beginner</SelectItem>
                            <SelectItem value="intermediate">Intermediate</SelectItem>
                            <SelectItem value="advanced">Advanced</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Dietary Restrictions */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Heart className="h-5 w-5" />
                      Dietary Restrictions & Allergies
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <label className="text-sm font-medium mb-2 block">Dietary Restrictions</label>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                        {dietaryRestrictions.map(restriction => (
                          <div key={restriction} className="flex items-center space-x-2">
                            <Checkbox
                              checked={planForm.dietary_restrictions.includes(restriction)}
                              onCheckedChange={() => handleArrayToggle('dietary_restrictions', restriction)}
                            />
                            <label className="text-sm capitalize">{restriction.replace('_', ' ')}</label>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <label className="text-sm font-medium mb-2 block">Allergies</label>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                        {allergies.map(allergy => (
                          <div key={allergy} className="flex items-center space-x-2">
                            <Checkbox
                              checked={planForm.allergies.includes(allergy)}
                              onCheckedChange={() => handleArrayToggle('allergies', allergy)}
                            />
                            <label className="text-sm capitalize">{allergy}</label>
                          </div>
                        ))}
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Health Goals */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5" />
                      Health Goals
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                      {healthGoals.map(goal => (
                        <div key={goal} className="flex items-center space-x-2">
                          <Checkbox
                            checked={planForm.health_goals.includes(goal)}
                            onCheckedChange={() => handleArrayToggle('health_goals', goal)}
                          />
                          <label className="text-sm capitalize">{goal.replace('_', ' ')}</label>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Generate Plan Sidebar */}
              <div className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Generate Plan</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <Button
                      onClick={generateMealPlan}
                      disabled={loading}
                      className="w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700"
                      size="lg"
                    >
                      {loading ? (
                        <>
                          <Loader2 className="h-5 w-5 animate-spin mr-2" />
                          Generating...
                        </>
                      ) : (
                        <>
                          <ChefHat className="h-5 w-5 mr-2" />
                          Generate AI Meal Plan
                        </>
                      )}
                    </Button>
                    
                    <div className="text-sm text-gray-600 space-y-2">
                      <div className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-600" />
                        USDA Nutrition Database
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-600" />
                        AI-Optimized Macros
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-600" />
                        Cost-Efficient Shopping
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-600" />
                        Cultural Preferences
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Quick Stats */}
                {currentPlan && (
                  <Card>
                    <CardHeader>
                      <CardTitle>Plan Overview</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-600">Nutritional Score</span>
                        <Badge className="bg-emerald-100 text-emerald-800">
                          {calculateNutritionalScore(currentPlan)}/100
                        </Badge>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-600">Meal Variety</span>
                        <Badge className="bg-blue-100 text-blue-800">
                          {getMealVarietyScore(currentPlan)}/100
                        </Badge>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-600">Weekly Cost</span>
                        <span className="font-semibold">
                          ${currentPlan.estimated_cost?.weekly || 85}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-600">Prep Time</span>
                        <span className="font-semibold">
                          {currentPlan.avg_prep_time || 45} min/meal
                        </span>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>
            </div>
          </TabsContent>

          {/* Current Plan Tab */}
          <TabsContent value="current" className="space-y-6">
            {currentPlan ? (
              <div className="space-y-6">
                {/* Plan Header */}
                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h2 className="text-2xl font-bold">{currentPlan.plan_name || 'Custom Meal Plan'}</h2>
                        <p className="text-gray-600">
                          Generated on {currentPlan.created_at ? new Date(currentPlan.created_at).toLocaleDateString() : 'Recently'}
                        </p>
                      </div>
                      <div className="flex gap-2">
                        <Button variant="outline">
                          <Download className="h-4 w-4 mr-2" />
                          Export Plan
                        </Button>
                        <Button className="bg-emerald-600 hover:bg-emerald-700">
                          <Calendar className="h-4 w-4 mr-2" />
                          Schedule Meals
                        </Button>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="text-center p-3 bg-emerald-50 rounded-lg">
                        <Calculator className="h-6 w-6 text-emerald-600 mx-auto mb-2" />
                        <p className="text-sm text-gray-600">Daily Calories</p>
                        <p className="font-bold text-emerald-600">
                          {currentPlan.daily_calories || planForm.target_calories}
                        </p>
                      </div>
                      <div className="text-center p-3 bg-blue-50 rounded-lg">
                        <Users className="h-6 w-6 text-blue-600 mx-auto mb-2" />
                        <p className="text-sm text-gray-600">Servings</p>
                        <p className="font-bold text-blue-600">
                          {currentPlan.servings || 1}
                        </p>
                      </div>
                      <div className="text-center p-3 bg-yellow-50 rounded-lg">
                        <Clock className="h-6 w-6 text-yellow-600 mx-auto mb-2" />
                        <p className="text-sm text-gray-600">Avg Prep Time</p>
                        <p className="font-bold text-yellow-600">
                          {currentPlan.avg_prep_time || 45}m
                        </p>
                      </div>
                      <div className="text-center p-3 bg-purple-50 rounded-lg">
                        <ShoppingCart className="h-6 w-6 text-purple-600 mx-auto mb-2" />
                        <p className="text-sm text-gray-600">Weekly Cost</p>
                        <p className="font-bold text-purple-600">
                          ${currentPlan.estimated_cost?.weekly || 85}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Weekly Meals */}
                <div className="grid gap-4">
                  {(currentPlan.weekly_meals || [
                    { day: 'Monday', breakfast: 'Oatmeal with berries', lunch: 'Grilled chicken salad', dinner: 'Salmon with vegetables' },
                    { day: 'Tuesday', breakfast: 'Greek yogurt parfait', lunch: 'Quinoa bowl', dinner: 'Lean beef stir-fry' },
                    { day: 'Wednesday', breakfast: 'Avocado toast', lunch: 'Turkey sandwich', dinner: 'Baked cod with rice' },
                    { day: 'Thursday', breakfast: 'Smoothie bowl', lunch: 'Lentil soup', dinner: 'Chicken breast with sweet potato' },
                    { day: 'Friday', breakfast: 'Egg scramble', lunch: 'Tuna salad', dinner: 'Vegetable curry with naan' },
                    { day: 'Saturday', breakfast: 'Pancakes with fruit', lunch: 'Chicken wrap', dinner: 'Grilled shrimp pasta' },
                    { day: 'Sunday', breakfast: 'French toast', lunch: 'Buddha bowl', dinner: 'Roast chicken with vegetables' }
                  ]).map((day, index) => (
                    <Card key={index}>
                      <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                          <Calendar className="h-5 w-5" />
                          {day.day}
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          <div className="p-3 bg-yellow-50 rounded-lg">
                            <div className="flex items-center gap-2 mb-2">
                              <Utensils className="h-4 w-4 text-yellow-600" />
                              <span className="font-semibold">Breakfast</span>
                            </div>
                            <p className="text-sm">{day.breakfast}</p>
                            <div className="mt-2 text-xs text-gray-600">
                              ~350 calories • 15 min prep
                            </div>
                          </div>
                          
                          <div className="p-3 bg-green-50 rounded-lg">
                            <div className="flex items-center gap-2 mb-2">
                              <Utensils className="h-4 w-4 text-green-600" />
                              <span className="font-semibold">Lunch</span>
                            </div>
                            <p className="text-sm">{day.lunch}</p>
                            <div className="mt-2 text-xs text-gray-600">
                              ~500 calories • 25 min prep
                            </div>
                          </div>
                          
                          <div className="p-3 bg-blue-50 rounded-lg">
                            <div className="flex items-center gap-2 mb-2">
                              <Utensils className="h-4 w-4 text-blue-600" />
                              <span className="font-semibold">Dinner</span>
                            </div>
                            <p className="text-sm">{day.dinner}</p>
                            <div className="mt-2 text-xs text-gray-600">
                              ~650 calories • 35 min prep
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            ) : (
              <div className="text-center py-12">
                <ChefHat className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <p className="text-gray-600 mb-4">No meal plan generated yet</p>
                <Button 
                  onClick={() => document.querySelector('[value="generator"]').click()}
                  className="bg-emerald-600 hover:bg-emerald-700"
                >
                  Create Your First Plan
                </Button>
              </div>
            )}
          </TabsContent>

          {/* Nutrition Analysis Tab */}
          <TabsContent value="nutrition" className="space-y-6">
            {currentPlan ? (
              <>
                {/* Macro Breakdown */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-center">Protein</CardTitle>
                    </CardHeader>
                    <CardContent className="text-center">
                      <div className="text-3xl font-bold text-blue-600 mb-2">
                        {currentPlan.nutritional_analysis?.protein_percentage || 25}%
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3 mb-2">
                        <div 
                          className="bg-blue-600 h-3 rounded-full"
                          style={{ width: `${currentPlan.nutritional_analysis?.protein_percentage || 25}%` }}
                        />
                      </div>
                      <p className="text-sm text-gray-600">
                        {Math.round((currentPlan.daily_calories || 2000) * 0.25 / 4)}g daily
                      </p>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-center">Carbohydrates</CardTitle>
                    </CardHeader>
                    <CardContent className="text-center">
                      <div className="text-3xl font-bold text-emerald-600 mb-2">
                        {currentPlan.nutritional_analysis?.carb_percentage || 45}%
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3 mb-2">
                        <div 
                          className="bg-emerald-600 h-3 rounded-full"
                          style={{ width: `${currentPlan.nutritional_analysis?.carb_percentage || 45}%` }}
                        />
                      </div>
                      <p className="text-sm text-gray-600">
                        {Math.round((currentPlan.daily_calories || 2000) * 0.45 / 4)}g daily
                      </p>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-center">Fats</CardTitle>
                    </CardHeader>
                    <CardContent className="text-center">
                      <div className="text-3xl font-bold text-yellow-600 mb-2">
                        {currentPlan.nutritional_analysis?.fat_percentage || 30}%
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3 mb-2">
                        <div 
                          className="bg-yellow-600 h-3 rounded-full"
                          style={{ width: `${currentPlan.nutritional_analysis?.fat_percentage || 30}%` }}
                        />
                      </div>
                      <p className="text-sm text-gray-600">
                        {Math.round((currentPlan.daily_calories || 2000) * 0.30 / 9)}g daily
                      </p>
                    </CardContent>
                  </Card>
                </div>

                {/* Micronutrients */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Award className="h-5 w-5" />
                      Micronutrient Goals
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      {[
                        { name: 'Vitamin C', current: 85, target: 90, unit: 'mg' },
                        { name: 'Iron', current: 15, target: 18, unit: 'mg' },
                        { name: 'Calcium', current: 950, target: 1000, unit: 'mg' },
                        { name: 'Fiber', current: 28, target: 35, unit: 'g' }
                      ].map((nutrient, index) => (
                        <div key={index} className="text-center p-3 bg-gray-50 rounded-lg">
                          <h4 className="font-semibold text-sm">{nutrient.name}</h4>
                          <div className="mt-2">
                            <span className="text-lg font-bold text-emerald-600">
                              {nutrient.current}
                            </span>
                            <span className="text-sm text-gray-600">/{nutrient.target}{nutrient.unit}</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                            <div 
                              className="bg-emerald-600 h-2 rounded-full"
                              style={{ width: `${(nutrient.current / nutrient.target) * 100}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </>
            ) : (
              <div className="text-center py-12">
                <Calculator className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <p className="text-gray-600">Generate a meal plan to see nutrition analysis</p>
              </div>
            )}
          </TabsContent>

          {/* Shopping List Tab */}
          <TabsContent value="shopping" className="space-y-6">
            {currentPlan ? (
              <>
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <ShoppingCart className="h-5 w-5" />
                        Smart Shopping List
                      </div>
                      <Badge className="bg-emerald-100 text-emerald-800">
                        Estimated: ${currentPlan.estimated_cost?.weekly || 85}/week
                      </Badge>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {[
                        {
                          category: 'Proteins',
                          items: ['Chicken breast (2 lbs)', 'Salmon fillet (1 lb)', 'Ground turkey (1 lb)', 'Greek yogurt (32oz)'],
                          cost: 28
                        },
                        {
                          category: 'Vegetables & Fruits',
                          items: ['Mixed greens (2 bags)', 'Broccoli (2 heads)', 'Bell peppers (3)', 'Bananas (bunch)', 'Berries (2 containers)'],
                          cost: 22
                        },
                        {
                          category: 'Grains & Starches',
                          items: ['Brown rice (2 lbs)', 'Quinoa (1 lb)', 'Sweet potatoes (3 lbs)', 'Whole grain bread (1 loaf)'],
                          cost: 15
                        },
                        {
                          category: 'Pantry Items',
                          items: ['Olive oil', 'Spices & herbs', 'Nuts & seeds', 'Coconut milk'],
                          cost: 20
                        }
                      ].map((category, index) => (
                        <Card key={index} className="border-emerald-200">
                          <CardHeader>
                            <CardTitle className="text-lg flex items-center justify-between">
                              {category.category}
                              <Badge variant="outline">${category.cost}</Badge>
                            </CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="space-y-2">
                              {category.items.map((item, itemIndex) => (
                                <div key={itemIndex} className="flex items-center space-x-2">
                                  <Checkbox />
                                  <span className="text-sm">{item}</span>
                                </div>
                              ))}
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                    
                    <div className="mt-6 flex gap-4">
                      <Button className="bg-emerald-600 hover:bg-emerald-700">
                        <Download className="h-4 w-4 mr-2" />
                        Download Shopping List
                      </Button>
                      <Button variant="outline">
                        <ShoppingCart className="h-4 w-4 mr-2" />
                        Send to Grocery App
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </>
            ) : (
              <div className="text-center py-12">
                <ShoppingCart className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <p className="text-gray-600">Generate a meal plan to create shopping list</p>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default IntelligentMealPlanGenerator;