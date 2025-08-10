import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { 
  Calculator, Activity, Heart, TrendingUp, Info, 
  User, Ruler, Weight, Target, AlertTriangle, 
  CheckCircle, Zap, Clock, Apple
} from 'lucide-react';

const GuestHealthCalculator = () => {
  const { switchRole } = useRole();
  
  // Form state
  const [formData, setFormData] = useState({
    age: '',
    gender: '',
    height: '',
    weight: '',
    activityLevel: ''
  });
  
  // Results state
  const [results, setResults] = useState(null);
  const [isCalculating, setIsCalculating] = useState(false);

  // Switch to guest role when component mounts
  useEffect(() => {
    switchRole('guest');
  }, [switchRole]);

  // Activity level options
  const activityLevels = [
    { value: 'sedentary', label: 'Sedentary', description: 'Little or no exercise', multiplier: 1.2 },
    { value: 'lightly_active', label: 'Lightly Active', description: 'Light exercise 1-3 days/week', multiplier: 1.375 },
    { value: 'moderately_active', label: 'Moderately Active', description: 'Moderate exercise 3-5 days/week', multiplier: 1.55 },
    { value: 'very_active', label: 'Very Active', description: 'Hard exercise 6-7 days/week', multiplier: 1.725 },
    { value: 'extra_active', label: 'Extra Active', description: 'Very hard exercise, physical job', multiplier: 1.9 }
  ];

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const calculateBMI = (weight, height) => {
    const heightInM = height / 100; // Convert cm to meters
    return weight / (heightInM * heightInM);
  };

  const calculateBMR = (weight, height, age, gender) => {
    if (gender === 'male') {
      return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age);
    } else {
      return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age);
    }
  };

  const getBMICategory = (bmi) => {
    if (bmi < 18.5) return { category: 'Underweight', color: 'bg-blue-100 text-blue-800', risk: 'low' };
    if (bmi < 25) return { category: 'Normal weight', color: 'bg-green-100 text-green-800', risk: 'low' };
    if (bmi < 30) return { category: 'Overweight', color: 'bg-yellow-100 text-yellow-800', risk: 'moderate' };
    if (bmi < 35) return { category: 'Obesity Class I', color: 'bg-orange-100 text-orange-800', risk: 'high' };
    if (bmi < 40) return { category: 'Obesity Class II', color: 'bg-red-100 text-red-800', risk: 'high' };
    return { category: 'Obesity Class III', color: 'bg-red-100 text-red-800', risk: 'very_high' };
  };

  const getHealthRecommendations = (bmi, bmr, dailyCalories) => {
    const bmiInfo = getBMICategory(bmi);
    const recommendations = [];

    if (bmiInfo.risk === 'low') {
      recommendations.push("Great job! Your BMI is in the healthy range.");
      recommendations.push("Focus on maintaining your current weight with balanced nutrition.");
      recommendations.push("Continue regular physical activity to stay healthy.");
    } else if (bmiInfo.risk === 'moderate') {
      recommendations.push("Consider gradual weight loss through diet and exercise.");
      recommendations.push("Aim for 1-2 pounds of weight loss per week.");
      recommendations.push("Increase physical activity and focus on portion control.");
    } else {
      recommendations.push("Consider consulting with a healthcare provider about weight management.");
      recommendations.push("Focus on creating a sustainable caloric deficit.");
      recommendations.push("Incorporate both cardiovascular and strength training exercises.");
    }

    return recommendations;
  };

  const handleCalculate = () => {
    const { age, gender, height, weight, activityLevel } = formData;
    
    if (!age || !gender || !height || !weight || !activityLevel) {
      alert('Please fill in all fields to calculate your health metrics.');
      return;
    }

    setIsCalculating(true);
    
    // Simulate calculation delay for better UX
    setTimeout(() => {
      const ageNum = parseInt(age);
      const heightNum = parseFloat(height);
      const weightNum = parseFloat(weight);
      const activityData = activityLevels.find(level => level.value === activityLevel);
      
      const bmi = calculateBMI(weightNum, heightNum);
      const bmr = calculateBMR(weightNum, heightNum, ageNum, gender);
      const dailyCalories = Math.round(bmr * activityData.multiplier);
      const bmiInfo = getBMICategory(bmi);
      const recommendations = getHealthRecommendations(bmi, bmr, dailyCalories);
      
      setResults({
        bmi: bmi.toFixed(1),
        bmr: Math.round(bmr),
        dailyCalories,
        bmiCategory: bmiInfo,
        recommendations,
        proteinNeeds: `${Math.round(weightNum * 0.8)}-${Math.round(weightNum * 1.2)}g`,
        waterNeeds: `${Math.round(weightNum * 0.035)} liters`,
        activityInfo: activityData
      });
      
      setIsCalculating(false);
    }, 1000);
  };

  const resetCalculator = () => {
    setFormData({
      age: '',
      gender: '',
      height: '',
      weight: '',
      activityLevel: ''
    });
    setResults(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-violet-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Health Calculator</h1>
          <p className="text-gray-600">Calculate your BMI, BMR, and daily calorie needs instantly</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Calculator Form */}
          <div className="lg:col-span-1">
            <Card className="sticky top-6">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Calculator className="w-5 h-5 mr-2 text-purple-600" />
                  Your Information
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Age */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <User className="w-4 h-4 inline mr-1" />
                    Age (years)
                  </label>
                  <Input
                    type="number"
                    placeholder="Enter your age"
                    value={formData.age}
                    onChange={(e) => handleInputChange('age', e.target.value)}
                    min="16"
                    max="100"
                  />
                </div>

                {/* Gender */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Gender</label>
                  <div className="grid grid-cols-2 gap-2">
                    {['male', 'female'].map((gender) => (
                      <Button
                        key={gender}
                        variant={formData.gender === gender ? "default" : "outline"}
                        onClick={() => handleInputChange('gender', gender)}
                        className={formData.gender === gender ? 'bg-purple-600 hover:bg-purple-700' : ''}
                      >
                        {gender.charAt(0).toUpperCase() + gender.slice(1)}
                      </Button>
                    ))}
                  </div>
                </div>

                {/* Height */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <Ruler className="w-4 h-4 inline mr-1" />
                    Height (cm)
                  </label>
                  <Input
                    type="number"
                    placeholder="Enter your height in cm"
                    value={formData.height}
                    onChange={(e) => handleInputChange('height', e.target.value)}
                    min="120"
                    max="250"
                  />
                </div>

                {/* Weight */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <Weight className="w-4 h-4 inline mr-1" />
                    Weight (kg)
                  </label>
                  <Input
                    type="number"
                    placeholder="Enter your weight in kg"
                    value={formData.weight}
                    onChange={(e) => handleInputChange('weight', e.target.value)}
                    min="30"
                    max="300"
                    step="0.1"
                  />
                </div>

                {/* Activity Level */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <Activity className="w-4 h-4 inline mr-1" />
                    Activity Level
                  </label>
                  <div className="space-y-2">
                    {activityLevels.map((level) => (
                      <Button
                        key={level.value}
                        variant={formData.activityLevel === level.value ? "default" : "outline"}
                        onClick={() => handleInputChange('activityLevel', level.value)}
                        className={`w-full text-left justify-start h-auto py-3 ${
                          formData.activityLevel === level.value ? 'bg-purple-600 hover:bg-purple-700' : ''
                        }`}
                      >
                        <div>
                          <div className="font-medium">{level.label}</div>
                          <div className="text-xs opacity-75">{level.description}</div>
                        </div>
                      </Button>
                    ))}
                  </div>
                </div>

                {/* Calculate Button */}
                <div className="pt-4">
                  <Button 
                    onClick={handleCalculate}
                    disabled={isCalculating}
                    className="w-full bg-purple-600 hover:bg-purple-700"
                    size="lg"
                  >
                    {isCalculating ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                        Calculating...
                      </>
                    ) : (
                      <>
                        <Calculator className="w-4 h-4 mr-2" />
                        Calculate Health Metrics
                      </>
                    )}
                  </Button>
                  
                  {results && (
                    <Button 
                      onClick={resetCalculator}
                      variant="outline"
                      className="w-full mt-2"
                    >
                      Reset Calculator
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Results */}
          <div className="lg:col-span-2">
            {!results ? (
              <Card className="h-full flex items-center justify-center">
                <CardContent className="text-center py-12">
                  <Calculator className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-gray-600 mb-2">Ready to Calculate</h3>
                  <p className="text-gray-500">Fill in your information and click calculate to see your health metrics</p>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-6">
                {/* Key Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Card className="border-2 border-purple-200 bg-purple-50">
                    <CardContent className="pt-6">
                      <div className="text-center">
                        <div className="text-3xl font-bold text-purple-600 mb-1">{results.bmi}</div>
                        <div className="text-sm text-gray-600 mb-2">Body Mass Index</div>
                        <Badge className={results.bmiCategory.color}>
                          {results.bmiCategory.category}
                        </Badge>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="border-2 border-blue-200 bg-blue-50">
                    <CardContent className="pt-6">
                      <div className="text-center">
                        <div className="text-3xl font-bold text-blue-600 mb-1">{results.bmr}</div>
                        <div className="text-sm text-gray-600 mb-2">Basal Metabolic Rate</div>
                        <div className="text-xs text-blue-700">calories at rest</div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="border-2 border-green-200 bg-green-50">
                    <CardContent className="pt-6">
                      <div className="text-center">
                        <div className="text-3xl font-bold text-green-600 mb-1">{results.dailyCalories}</div>
                        <div className="text-sm text-gray-600 mb-2">Daily Calorie Needs</div>
                        <div className="text-xs text-green-700">{results.activityInfo.label.toLowerCase()}</div>
                      </div>
                    </CardContent>
                  </Card>
                </div>

                {/* Detailed Information */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <Info className="w-5 h-5 mr-2 text-blue-600" />
                      Your Health Profile
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                          <Target className="w-4 h-4 mr-2 text-green-600" />
                          Daily Nutrition Targets
                        </h4>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span>Calories:</span>
                            <span className="font-medium">{results.dailyCalories} cal</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Protein:</span>
                            <span className="font-medium">{results.proteinNeeds}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Water:</span>
                            <span className="font-medium">{results.waterNeeds}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Activity Level:</span>
                            <span className="font-medium">{results.activityInfo.label}</span>
                          </div>
                        </div>
                      </div>

                      <div>
                        <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                          <Heart className="w-4 h-4 mr-2 text-red-600" />
                          Health Recommendations
                        </h4>
                        <div className="space-y-2">
                          {results.recommendations.map((rec, index) => (
                            <div key={index} className="flex items-start text-sm">
                              <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                              <span>{rec}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* BMI Chart Reference */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <TrendingUp className="w-5 h-5 mr-2 text-purple-600" />
                      BMI Reference Chart
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="text-center p-3 rounded-lg bg-blue-50">
                        <div className="font-semibold text-blue-800">&lt; 18.5</div>
                        <div className="text-sm text-blue-600">Underweight</div>
                      </div>
                      <div className="text-center p-3 rounded-lg bg-green-50">
                        <div className="font-semibold text-green-800">18.5 - 24.9</div>
                        <div className="text-sm text-green-600">Normal</div>
                      </div>
                      <div className="text-center p-3 rounded-lg bg-yellow-50">
                        <div className="font-semibold text-yellow-800">25 - 29.9</div>
                        <div className="text-sm text-yellow-600">Overweight</div>
                      </div>
                      <div className="text-center p-3 rounded-lg bg-red-50">
                        <div className="font-semibold text-red-800">&ge; 30</div>
                        <div className="text-sm text-red-600">Obese</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Upgrade Prompt */}
                <Card className="border-2 border-purple-200 bg-gradient-to-r from-purple-50 to-violet-50">
                  <CardContent className="pt-6">
                    <div className="text-center">
                      <Zap className="w-12 h-12 text-purple-600 mx-auto mb-4" />
                      <h3 className="text-xl font-semibold text-gray-900 mb-2">Want More Detailed Analysis?</h3>
                      <p className="text-gray-600 mb-4">
                        Create a free account to track your progress over time, get personalized meal plans, 
                        and receive AI-powered health insights.
                      </p>
                      <div className="flex justify-center space-x-3">
                        <Button className="bg-purple-600 hover:bg-purple-700">
                          <Heart className="w-4 h-4 mr-2" />
                          Create Free Account
                        </Button>
                        <Button variant="outline">
                          <Apple className="w-4 h-4 mr-2" />
                          Learn More
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default GuestHealthCalculator;