import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';

import RealTimeFeedback from './shared/RealTimeFeedback';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import {
  Heart, Activity, Brain, Utensils, Clock, Star,
  ChevronRight, ChevronLeft, CheckCircle, Zap,
  TrendingUp, Target, Award, Calendar, Timer,
  Sparkles, ArrowRight, Users, Crown, Play
} from 'lucide-react';

const InstantHealthAssessment = () => {
  const { switchRole } = useRole();
  
  // Assessment flow state
  const [currentStep, setCurrentStep] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [feedbackData, setFeedbackData] = useState(null);
  
  // Assessment responses
  const [responses, setResponses] = useState({
    age_range: '',
    activity_level: '',
    health_goal: '',
    dietary_preferences: [],
    stress_level: ''
  });
  
  // Assessment results
  const [results, setResults] = useState(null);

  // Switch to guest role when component mounts
  useEffect(() => {
    switchRole('guest');
  }, [switchRole]);

  // Assessment steps configuration
  const assessmentSteps = [
    {
      id: 'welcome',
      title: 'Welcome to Your Health Snapshot',
      subtitle: 'Get personalized insights in just 2 minutes',
      icon: Heart,
      color: 'text-purple-600'
    },
    {
      id: 'age_range',
      title: 'What\'s your age range?',
      subtitle: 'This helps us personalize your health recommendations',
      icon: Users,
      color: 'text-blue-600'
    },
    {
      id: 'activity_level',
      title: 'How active are you?',
      subtitle: 'Choose the option that best describes your weekly activity',
      icon: Activity,
      color: 'text-green-600'
    },
    {
      id: 'health_goal',
      title: 'What\'s your main health goal?',
      subtitle: 'We\'ll tailor recommendations to help you achieve it',
      icon: Target,
      color: 'text-orange-600'
    },
    {
      id: 'dietary_preferences',
      title: 'Any dietary preferences?',
      subtitle: 'Select all that apply to get relevant meal suggestions',
      icon: Utensils,
      color: 'text-pink-600'
    },
    {
      id: 'stress_level',
      title: 'How would you rate your stress?',
      subtitle: 'Understanding stress helps us provide complete wellness advice',
      icon: Brain,
      color: 'text-indigo-600'
    }
  ];

  // Options for each step
  const stepOptions = {
    age_range: [
      { value: '18-25', label: '18-25', description: 'Young adult' },
      { value: '26-35', label: '26-35', description: 'Early career' },
      { value: '36-45', label: '36-45', description: 'Mid-life' },
      { value: '46-55', label: '46-55', description: 'Pre-retirement' },
      { value: '55+', label: '55+', description: 'Senior' }
    ],
    activity_level: [
      { 
        value: 'sedentary', 
        label: 'Sedentary', 
        description: 'Little to no exercise',
        icon: '🪑',
        detail: 'Mostly sitting, minimal physical activity'
      },
      { 
        value: 'light', 
        label: 'Lightly Active', 
        description: '1-3 days/week light exercise',
        icon: '🚶‍♀️',
        detail: 'Light walking, occasional activity'
      },
      { 
        value: 'moderate', 
        label: 'Moderately Active', 
        description: '3-5 days/week moderate exercise',
        icon: '🏃‍♀️',
        detail: 'Regular workouts, sports, active lifestyle'
      },
      { 
        value: 'active', 
        label: 'Very Active', 
        description: '6-7 days/week intense exercise',
        icon: '🏋️‍♀️',
        detail: 'Daily exercise, competitive sports'
      },
      { 
        value: 'very_active', 
        label: 'Extremely Active', 
        description: 'Athlete-level training',
        icon: '🏆',
        detail: 'Professional training, multiple daily sessions'
      }
    ],
    health_goal: [
      { value: 'weight_loss', label: 'Weight Loss', icon: '⚖️', description: 'Lose weight safely and sustainably' },
      { value: 'muscle_gain', label: 'Muscle Gain', icon: '💪', description: 'Build strength and muscle mass' },
      { value: 'general_wellness', label: 'General Wellness', icon: '✨', description: 'Overall health improvement' },
      { value: 'disease_prevention', label: 'Disease Prevention', icon: '🛡️', description: 'Prevent chronic diseases' },
      { value: 'energy_boost', label: 'Energy Boost', icon: '⚡', description: 'Increase daily energy levels' }
    ],
    dietary_preferences: [
      { value: 'none', label: 'No Restrictions', icon: '🍽️' },
      { value: 'vegetarian', label: 'Vegetarian', icon: '🥬' },
      { value: 'vegan', label: 'Vegan', icon: '🌱' },
      { value: 'keto', label: 'Keto', icon: '🥑' },
      { value: 'mediterranean', label: 'Mediterranean', icon: '🫒' },
      { value: 'gluten_free', label: 'Gluten-Free', icon: '🌾' },
      { value: 'diabetic_friendly', label: 'Diabetic-Friendly', icon: '📊' }
    ],
    stress_level: [
      { value: 'low', label: 'Low Stress', emoji: '😌', description: 'Generally calm and relaxed' },
      { value: 'moderate', label: 'Moderate Stress', emoji: '😐', description: 'Some daily stress, manageable' },
      { value: 'high', label: 'High Stress', emoji: '😰', description: 'Frequent stress, impacts daily life' },
      { value: 'very_high', label: 'Very High Stress', emoji: '😫', description: 'Overwhelming stress, needs attention' }
    ]
  };

  const handleResponseUpdate = (field, value) => {
    if (field === 'dietary_preferences') {
      // Handle multiple selections for dietary preferences
      setResponses(prev => ({
        ...prev,
        [field]: prev[field].includes(value) 
          ? prev[field].filter(item => item !== value)
          : [...prev[field], value]
      }));
    } else {
      setResponses(prev => ({
        ...prev,
        [field]: value
      }));
    }
  };

  const nextStep = (event) => {
    // Prevent default form submission behavior and event bubbling
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    
    console.log('nextStep called, currentStep:', currentStep, 'assessmentSteps.length:', assessmentSteps.length);
    
    if (currentStep === 0) {
      // Skip welcome screen
      setCurrentStep(1);
    } else if (currentStep < assessmentSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      // Process assessment - final step
      console.log('Final step reached, calling processAssessment...');
      processAssessment();
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const processAssessment = async () => {
    console.log('processAssessment called with responses:', responses);
    setIsProcessing(true);
    
    // Show processing animation with health messages
    const processingMessages = [
      'Analyzing your responses...',
      'Calculating your health score...',
      'Generating personalized recommendations...',
      'Preparing your meal suggestions...',
      'Finalizing your health snapshot...'
    ];

    let messageIndex = 0;
    const messageInterval = setInterval(() => {
      if (messageIndex < processingMessages.length) {
        setFeedbackData({
          type: 'processing',
          title: 'Creating Your Health Snapshot',
          insights: [processingMessages[messageIndex]]
        });
        messageIndex++;
      }
    }, 600);

    try {
      // Generate session ID for guest
      const sessionId = `guest_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      
      // Call backend API
      const backendUrl = process.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/guest/health-assessment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: sessionId,
          responses: responses
        })
      });

      if (!response.ok) {
        throw new Error('Failed to process assessment');
      }

      const assessmentResults = await response.json();
      
      clearInterval(messageInterval);
      setIsProcessing(false);
      setResults(assessmentResults);
      setShowResults(true);
      
      // Show success feedback
      setFeedbackData({
        type: 'success',
        title: 'Health Snapshot Complete!',
        insights: [
          `Your health score: ${assessmentResults.health_score}/100`,
          `Health age: ${assessmentResults.health_age} years`,
          'Personalized recommendations ready!'
        ]
      });

    } catch (error) {
      clearInterval(messageInterval);
      setIsProcessing(false);
      console.error('Assessment processing error:', error);
      
      setFeedbackData({
        type: 'error',
        title: 'Assessment Processing Error',
        insights: ['Please try again or check your connection']
      });
    }
  };

  const restartAssessment = () => {
    setCurrentStep(0);
    setShowResults(false);
    setResults(null);
    setResponses({
      age_range: '',
      activity_level: '',
      health_goal: '',
      dietary_preferences: [],
      stress_level: ''
    });
    setFeedbackData(null);
  };

  const getCurrentStepField = () => {
    if (currentStep === 0) return null;
    return assessmentSteps[currentStep].id;
  };

  const isStepComplete = () => {
    const field = getCurrentStepField();
    if (!field) return true; // Welcome step is always complete
    
    if (field === 'dietary_preferences') {
      return responses[field].length > 0;
    }
    return responses[field] !== '';
  };

  const getHealthScoreColor = (score) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 75) return 'text-lime-600';
    if (score >= 60) return 'text-yellow-600';
    if (score >= 40) return 'text-orange-600';
    return 'text-red-600';
  };

  const getHealthScoreBadge = (score) => {
    if (score >= 90) return { text: 'Excellent', class: 'bg-green-100 text-green-800' };
    if (score >= 75) return { text: 'Good', class: 'bg-lime-100 text-lime-800' };
    if (score >= 60) return { text: 'Fair', class: 'bg-yellow-100 text-yellow-800' };
    if (score >= 40) return { text: 'Needs Improvement', class: 'bg-orange-100 text-orange-800' };
    return { text: 'High Risk', class: 'bg-red-100 text-red-800' };
  };

  const renderWelcomeStep = () => (
    <Card className="max-w-2xl mx-auto">
      <CardContent className="pt-8 pb-8 text-center">
        <div className="mb-8">
          <div className="w-20 h-20 bg-gradient-to-r from-purple-500 to-violet-600 rounded-full flex items-center justify-center mx-auto mb-6">
            <Heart className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Get Your Instant Health Snapshot
          </h1>
          <p className="text-xl text-gray-600 mb-6">
            Discover your personalized health score and get instant recommendations in just 2 minutes
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="text-center p-4">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <Clock className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">2 Minutes</h3>
            <p className="text-sm text-gray-600">Quick 5-question assessment</p>
          </div>
          <div className="text-center p-4">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <Target className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Personalized</h3>
            <p className="text-sm text-gray-600">Tailored to your lifestyle</p>
          </div>
          <div className="text-center p-4">
            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <Sparkles className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Actionable</h3>
            <p className="text-sm text-gray-600">Instant recommendations</p>
          </div>
        </div>

        <div className="bg-gradient-to-r from-purple-50 to-violet-50 rounded-lg p-6 mb-8">
          <h4 className="font-semibold text-purple-900 mb-3">What You'll Get:</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-purple-700">
            <div className="flex items-center">
              <CheckCircle className="w-4 h-4 text-purple-600 mr-2" />
              Your personalized health score (0-100)
            </div>
            <div className="flex items-center">
              <CheckCircle className="w-4 h-4 text-purple-600 mr-2" />
              Health age vs. actual age analysis
            </div>
            <div className="flex items-center">
              <CheckCircle className="w-4 h-4 text-purple-600 mr-2" />
              5 prioritized health recommendations
            </div>
            <div className="flex items-center">
              <CheckCircle className="w-4 h-4 text-purple-600 mr-2" />
              Custom meal suggestions for today
            </div>
          </div>
        </div>

        <Button 
          type="button"
          onClick={nextStep}
          size="lg"
          className="bg-gradient-to-r from-purple-600 to-violet-600 hover:from-purple-700 hover:to-violet-700 text-white px-8"
        >
          <Play className="w-5 h-5 mr-2" />
          Start Your Health Assessment
        </Button>
      </CardContent>
    </Card>
  );

  const renderQuestionStep = () => {
    const step = assessmentSteps[currentStep];
    const field = step.id;
    const options = stepOptions[field];
    const StepIcon = step.icon;

    return (
      <Card className="max-w-3xl mx-auto">
        <CardHeader>
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className={`w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center ${step.color}`}>
                <StepIcon className="w-6 h-6" />
              </div>
              <div>
                <CardTitle className="text-xl">{step.title}</CardTitle>
                <p className="text-gray-600 mt-1">{step.subtitle}</p>
              </div>
            </div>
            <Badge variant="outline" className="px-3 py-1">
              {currentStep}/{assessmentSteps.length - 1}
            </Badge>
          </div>
          <Progress value={(currentStep / (assessmentSteps.length - 1)) * 100} className="h-2" />
        </CardHeader>
        
        <CardContent className="pb-8">
          <div className="space-y-3">
            {field === 'dietary_preferences' ? (
              // Multi-select for dietary preferences
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {options.map((option) => (
                  <Button
                    key={option.value}
                    variant={responses[field].includes(option.value) ? "default" : "outline"}
                    onClick={() => handleResponseUpdate(field, option.value)}
                    className={`h-auto p-4 justify-start text-left ${
                      responses[field].includes(option.value) 
                        ? 'bg-purple-600 hover:bg-purple-700 text-white' 
                        : 'hover:bg-purple-50'
                    }`}
                  >
                    <div className="flex items-center space-x-3">
                      <span className="text-2xl">{option.icon}</span>
                      <span className="font-medium">{option.label}</span>
                    </div>
                  </Button>
                ))}
              </div>
            ) : (
              // Single select for other options
              <div className="space-y-3">
                {options.map((option) => (
                  <Button
                    key={option.value}
                    variant={responses[field] === option.value ? "default" : "outline"}
                    onClick={() => handleResponseUpdate(field, option.value)}
                    className={`w-full h-auto p-4 justify-start text-left ${
                      responses[field] === option.value 
                        ? 'bg-purple-600 hover:bg-purple-700 text-white' 
                        : 'hover:bg-purple-50'
                    }`}
                  >
                    <div className="flex items-center justify-between w-full">
                      <div className="flex items-center space-x-3">
                        {option.emoji && <span className="text-2xl">{option.emoji}</span>}
                        {option.icon && <span className="text-xl">{option.icon}</span>}
                        <div>
                          <div className="font-medium">{option.label}</div>
                          {option.description && (
                            <div className="text-sm opacity-75 mt-1">{option.description}</div>
                          )}
                          {option.detail && (
                            <div className="text-xs opacity-60 mt-1">{option.detail}</div>
                          )}
                        </div>
                      </div>
                      {responses[field] === option.value && (
                        <CheckCircle className="w-5 h-5 ml-2" />
                      )}
                    </div>
                  </Button>
                ))}
              </div>
            )}
          </div>

          <div className="flex justify-between mt-8">
            <Button
              variant="outline"
              onClick={prevStep}
              disabled={currentStep === 0}
            >
              <ChevronLeft className="w-4 h-4 mr-2" />
              Previous
            </Button>
            
            <Button
              type="button"
              onClick={nextStep}
              disabled={!isStepComplete()}
              className="bg-purple-600 hover:bg-purple-700"
            >
              {currentStep === assessmentSteps.length - 1 ? (
                <>
                  <Zap className="w-4 h-4 mr-2" />
                  Get My Health Snapshot
                </>
              ) : (
                <>
                  Next
                  <ChevronRight className="w-4 h-4 ml-2" />
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  };

  const renderProcessingStep = () => (
    <Card className="max-w-2xl mx-auto">
      <CardContent className="pt-8 pb-8 text-center">
        <div className="mb-8">
          <div className="w-20 h-20 bg-gradient-to-r from-purple-500 to-violet-600 rounded-full flex items-center justify-center mx-auto mb-6 animate-pulse">
            <Sparkles className="w-10 h-10 text-white animate-spin" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Creating Your Health Snapshot
          </h2>
          <p className="text-gray-600 mb-6">
            Analyzing your responses and generating personalized insights...
          </p>
        </div>

        <div className="space-y-4 mb-8">
          <div className="flex items-center justify-center space-x-3 text-green-600">
            <CheckCircle className="w-5 h-5" />
            <span>Responses analyzed</span>
          </div>
          <div className="flex items-center justify-center space-x-3 text-blue-600">
            <div className="animate-spin rounded-full h-5 w-5 border-2 border-blue-600 border-t-transparent"></div>
            <span>Calculating health metrics...</span>
          </div>
        </div>

        <Progress value={75} className="h-3 mb-6" />
        
        <div className="bg-purple-50 rounded-lg p-4">
          <p className="text-sm text-purple-700">
            💡 <strong>Did you know?</strong> Your health age can be different from your actual age based on lifestyle factors!
          </p>
        </div>
      </CardContent>
    </Card>
  );

  const renderResultsStep = () => {
    if (!results) return null;

    const scoreBadge = getHealthScoreBadge(results.health_score);
    const healthAgeDifference = results.health_age - parseInt(results.actual_age_range.split('-')[0]);

    return (
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Health Score Overview */}
        <Card className="border-2 border-purple-200">
          <CardContent className="pt-8">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">Your Health Snapshot</h1>
              <div className="flex items-center justify-center space-x-8 mb-6">
                <div className="text-center">
                  <div className={`text-6xl font-bold mb-2 ${getHealthScoreColor(results.health_score)}`}>
                    {results.health_score}
                  </div>
                  <div className="text-sm text-gray-600 mb-2">Health Score</div>
                  <Badge className={scoreBadge.class}>
                    {scoreBadge.text}
                  </Badge>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-bold mb-2 text-blue-600">
                    {results.health_age}
                  </div>
                  <div className="text-sm text-gray-600 mb-2">Health Age</div>
                  <div className="text-xs text-gray-500">
                    {healthAgeDifference > 0 
                      ? `${healthAgeDifference} years older` 
                      : healthAgeDifference < 0 
                      ? `${Math.abs(healthAgeDifference)} years younger`
                      : 'Matches actual age'
                    }
                  </div>
                </div>
              </div>
            </div>

            {/* Score Breakdown */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <Activity className="w-6 h-6 text-blue-600 mx-auto mb-2" />
                <div className="font-semibold text-blue-900">{results.score_breakdown.activity}</div>
                <div className="text-xs text-blue-700">Activity</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <Utensils className="w-6 h-6 text-green-600 mx-auto mb-2" />
                <div className="font-semibold text-green-900">{results.score_breakdown.nutrition}</div>
                <div className="text-xs text-green-700">Nutrition</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <Brain className="w-6 h-6 text-purple-600 mx-auto mb-2" />
                <div className="font-semibold text-purple-900">{results.score_breakdown.stress_management}</div>
                <div className="text-xs text-purple-700">Stress</div>
              </div>
              <div className="text-center p-4 bg-orange-50 rounded-lg">
                <Heart className="w-6 h-6 text-orange-600 mx-auto mb-2" />
                <div className="font-semibold text-orange-900">{results.score_breakdown.lifestyle}</div>
                <div className="text-xs text-orange-700">Lifestyle</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Personalized Recommendations */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Target className="w-5 h-5 mr-2 text-green-600" />
                Your Personalized Recommendations
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {results.recommendations.map((rec, index) => (
                  <div key={index} className="p-4 border rounded-lg">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-gray-900">{rec.title}</h4>
                      <Badge 
                        className={
                          rec.priority === 'high' ? 'bg-red-100 text-red-800' :
                          rec.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }
                      >
                        {rec.priority} priority
                      </Badge>
                    </div>
                    <p className="text-sm text-gray-600 mb-3">{rec.description}</p>
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span className="flex items-center">
                        <Timer className="w-3 h-3 mr-1" />
                        {rec.time_estimate}
                      </span>
                      <span className="flex items-center">
                        <TrendingUp className="w-3 h-3 mr-1" />
                        {rec.impact}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Custom Meal Suggestions */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Utensils className="w-5 h-5 mr-2 text-pink-600" />
                Today's Meal Suggestions
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {results.meal_suggestions.map((meal, index) => (
                  <div key={index} className="p-4 border rounded-lg">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h4 className="font-semibold text-gray-900">{meal.name}</h4>
                        <Badge variant="outline" className="mt-1 text-xs">
                          {meal.meal_type}
                        </Badge>
                      </div>
                      <div className="text-right text-xs text-gray-500">
                        <div className="flex items-center">
                          <Clock className="w-3 h-3 mr-1" />
                          {meal.prep_time}
                        </div>
                        <div className="mt-1">{meal.difficulty}</div>
                      </div>
                    </div>
                    
                    <div className="mb-3">
                      <div className="text-xs text-gray-600 mb-2">Health Benefits:</div>
                      <div className="flex flex-wrap gap-1">
                        {meal.health_benefits.map((benefit, i) => (
                          <Badge key={i} variant="outline" className="text-xs">
                            {benefit}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    
                    <div className="text-xs text-gray-600">
                      <span className="font-medium">Ingredients:</span> {meal.ingredients_preview.join(', ')}
                    </div>
                    
                    <div className="mt-2 text-xs text-gray-500">
                      ~{meal.estimated_nutrition.calories} cal | {meal.estimated_nutrition.protein}g protein
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Next Steps */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <ArrowRight className="w-5 h-5 mr-2 text-purple-600" />
              Your Next Steps
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold text-gray-900 mb-3">Immediate Actions</h4>
                <div className="space-y-2">
                  {results.next_steps.map((step, index) => (
                    <div key={index} className="flex items-start text-sm">
                      <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span>{step}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-3">Areas to Improve</h4>
                <div className="space-y-2">
                  {results.improvement_areas.map((area, index) => (
                    <div key={index} className="flex items-start text-sm">
                      <Target className="w-4 h-4 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span>{area}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Action Buttons */}
        <div className="text-center space-y-4">
          <div className="space-x-4">
            <Button 
              onClick={restartAssessment}
              variant="outline"
              size="lg"
            >
              Take Assessment Again
            </Button>
          </div>
          
          <div className="bg-gradient-to-r from-purple-50 to-violet-50 rounded-lg p-6 mt-6">
            <div className="text-center">
              <Award className="w-12 h-12 text-purple-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Ready for the Next Level?</h3>
              <p className="text-gray-600 mb-4">
                Create a free account to save your results, track progress over time, and get advanced health insights.
              </p>
              <div className="flex justify-center space-x-6 text-sm text-gray-600">
                <div className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-1" />
                  Progress tracking
                </div>
                <div className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-1" />
                  Advanced insights
                </div>
                <div className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-1" />
                  Meal planning
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-violet-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!showResults && !isProcessing && (
          <>
            {currentStep === 0 && renderWelcomeStep()}
            {currentStep > 0 && renderQuestionStep()}
          </>
        )}
        
        {isProcessing && renderProcessingStep()}
        
        {showResults && renderResultsStep()}
      </div>

      {/* Real-time Feedback */}
      {feedbackData && (
        <RealTimeFeedback
          type={feedbackData.type}
          data={feedbackData}
          onAction={(action) => {
            console.log('Assessment feedback action:', action);
            if (action === 'learn_more') {
              setShowUpgradePrompt(true);
            }
          }}
          onDismiss={() => setFeedbackData(null)}
          position="bottom-right"
        />
      )}

      {/* Upgrade Prompt Modal */}
      {showUpgradePrompt && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="max-w-lg">
            <UpgradePrompt
              type="health_assessment_results"
              context={results ? `Your health score of ${results.health_score} shows great potential! Unlock advanced tracking and personalized coaching with a free account.` : 'Create a free account to save your progress and get advanced health insights.'}
              triggerAction={() => console.log('Upgrade from health assessment')}
              onClose={() => setShowUpgradePrompt(false)}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default InstantHealthAssessment;