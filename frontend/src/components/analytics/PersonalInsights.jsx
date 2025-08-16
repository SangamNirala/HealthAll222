import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { 
  Brain,
  TrendingUp,
  Target,
  Activity,
  Heart,
  Zap,
  AlertCircle,
  CheckCircle,
  Info,
  Calendar,
  BarChart3,
  Lightbulb,
  ArrowRight,
  Sparkles,
  RefreshCw,
  Calculator,
  Moon,
  Apple
} from 'lucide-react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import SmartNavigation from '../shared/SmartNavigation';
import predictiveAnalyticsService from '../../services/predictiveAnalyticsService';
import WhatIfScenarios from './WhatIfScenarios';
import WeeklyHealthDashboard from './WeeklyHealthDashboard';

const PersonalInsights = ({ 
  userId = 'demo-patient-123', 
  isWidget = false, 
  className = '' 
}) => {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTimeframe, setActiveTimeframe] = useState('weekly');
  const [selectedPattern, setSelectedPattern] = useState('nutrition');
  const [activeTab, setActiveTab] = useState('overview');
  
  // ML Predictions State
  const [energyPrediction, setEnergyPrediction] = useState(null);
  const [moodCorrelation, setMoodCorrelation] = useState(null);
  const [sleepImpact, setSleepImpact] = useState(null);
  const [weeklyPatterns, setWeeklyPatterns] = useState(null);

  const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

  useEffect(() => {
    fetchPersonalInsights();
    fetchMLPredictions();
  }, [userId, activeTimeframe]);

  const fetchMLPredictions = async () => {
    try {
      // Sample intake data for predictions
      const sampleIntakeData = {
        calories: 2000,
        protein_g: 100,
        carbs_g: 250,
        fat_g: 70,
        sleep_hours: 7.5,
        exercise_minutes: 30,
        stress_level: 5,
        water_intake_ml: 2500,
        caffeine_mg: 100,
        meal_timing_consistency: 0.8
      };

      const sampleDailyChoices = {
        caffeine_timing: 'morning',
        meal_timing: 'regular',
        exercise_timing: 'afternoon',
        screen_time: 2,
        stress_level: 5,
        alcohol_intake: 0
      };

      // Fetch all ML predictions
      const [energyResult, moodResult, sleepResult, weeklyResult] = await Promise.all([
        predictiveAnalyticsService.predictEnergy(sampleIntakeData, userId),
        predictiveAnalyticsService.analyzeMoodFoodCorrelation(userId, 30),
        predictiveAnalyticsService.analyzeSleepImpact(sampleDailyChoices, userId),
        predictiveAnalyticsService.getWeeklyHealthPatterns(userId, 4)
      ]);

      if (energyResult.success) setEnergyPrediction(energyResult.data);
      if (moodResult.success) setMoodCorrelation(moodResult.data);
      if (sleepResult.success) setSleepImpact(sleepResult.data);
      if (weeklyResult.success) setWeeklyPatterns(weeklyResult.data);

    } catch (error) {
      console.error('Error fetching ML predictions:', error);
    }
  };

  const fetchPersonalInsights = async () => {
    try {
      setLoading(true);
      setError(null);

      // Generate comprehensive user data for AI analysis
      const healthData = {
        user_id: userId,
        timeframe: activeTimeframe,
        age: 32,
        gender: 'female',
        activity_level: 'moderately_active',
        goals: ['weight_loss', 'energy_boost'],
        diet_type: 'balanced',
        avg_calories: 1850,
        avg_protein: 95,
        avg_carbs: 220,
        avg_fat: 65,
        weight: 68,
        energy_level: 7,
        sleep_quality: 6,
        stress_levels: 'moderate',
        exercise_frequency: '4_times_week',
        daily_logs: Array.from({ length: 14 }, (_, i) => ({
          date: new Date(Date.now() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          calories: 1800 + Math.random() * 200,
          energy: 6 + Math.random() * 3,
          sleep_hours: 6.5 + Math.random() * 2,
          exercise_minutes: Math.random() * 60,
          mood: 6 + Math.random() * 3
        }))
      };

      // Call AI health insights endpoint
      const response = await fetch(`${API_BASE_URL}/api/ai/health-insights`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ healthData })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const aiResponse = await response.json();

      // Process and structure the insights data
      const processedInsights = {
        summary: {
          overall_score: 78,
          trend: 'improving',
          key_achievements: [
            'Consistent protein intake above target',
            'Improved sleep consistency over 2 weeks',
            'Regular exercise routine established'
          ],
          areas_for_improvement: [
            'Increase daily water intake',
            'Reduce late-night snacking',
            'Add more fiber-rich foods'
          ]
        },
        patterns: {
          nutrition: {
            title: 'Nutrition Patterns',
            confidence: 0.87,
            insights: aiResponse.insights || [
              'Your protein intake shows excellent consistency, averaging 95g daily',
              'Energy dips occur around 3 PM, correlating with lower carb intake at lunch',
              'Weekend calorie intake increases by 15% compared to weekdays'
            ],
            data: healthData.daily_logs.map(log => ({
              date: log.date,
              calories: log.calories,
              energy: log.energy,
              trend: log.calories > 1900 ? 'high' : log.calories < 1700 ? 'low' : 'normal'
            }))
          },
          activity: {
            title: 'Activity & Energy Patterns',
            confidence: 0.82,
            insights: [
              'Exercise sessions on Tuesday and Thursday boost energy levels by 20%',
              'Sleep quality directly impacts next-day energy levels (correlation: 0.74)',
              'Post-workout meals show better nutrient absorption patterns'
            ],
            data: healthData.daily_logs.map(log => ({
              date: log.date,
              energy: log.energy,
              exercise: log.exercise_minutes,
              sleep: log.sleep_hours
            }))
          },
          behavioral: {
            title: 'Behavioral Insights',
            confidence: 0.79,
            insights: [
              'Meal timing consistency improved by 30% over the past two weeks',
              'Stress levels correlate with increased snacking frequency',
              'Planning meals in advance leads to better nutritional choices'
            ],
            data: healthData.daily_logs.map(log => ({
              date: log.date,
              mood: log.mood,
              consistency: 7 + Math.random() * 2
            }))
          }
        },
        recommendations: aiResponse.recommendations || [
          {
            category: 'Nutrition',
            priority: 'high',
            title: 'Optimize Afternoon Energy',
            description: 'Add complex carbohydrates to lunch to prevent 3 PM energy dips',
            action: 'Include quinoa, sweet potato, or brown rice in lunch meals',
            impact: 'Expected 25% improvement in afternoon energy levels',
            timeline: '1-2 weeks'
          },
          {
            category: 'Hydration',
            priority: 'medium',
            title: 'Increase Daily Water Intake',
            description: 'Current intake below optimal levels for your activity',
            action: 'Add 2 additional glasses of water, especially pre-workout',
            impact: 'Better workout performance and recovery',
            timeline: '1 week'
          },
          {
            category: 'Sleep',
            priority: 'high',
            title: 'Optimize Sleep Schedule',
            description: 'Inconsistent bedtime affecting recovery and energy',
            action: 'Set consistent bedtime routine 30 minutes earlier',
            impact: 'Improved recovery and morning energy levels',
            timeline: '2-3 weeks'
          }
        ],
        correlations: [
          {
            factor1: 'Sleep Quality',
            factor2: 'Next Day Energy',
            correlation: 0.74,
            strength: 'Strong',
            insight: 'Better sleep quality significantly predicts higher energy levels the following day'
          },
          {
            factor1: 'Protein Intake',
            factor2: 'Workout Performance',
            correlation: 0.68,
            strength: 'Moderate',
            insight: 'Higher protein intake correlates with better strength training performance'
          },
          {
            factor1: 'Meal Timing',
            factor2: 'Energy Stability',
            correlation: 0.61,
            strength: 'Moderate',
            insight: 'Consistent meal timing helps maintain stable energy levels throughout the day'
          }
        ],
        trend_data: healthData.daily_logs.slice(-7).map(log => ({
          date: new Date(log.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
          overall_score: Math.round(65 + Math.random() * 20),
          nutrition_score: Math.round(70 + Math.random() * 20),
          energy_score: Math.round(log.energy * 10),
          consistency_score: Math.round(75 + Math.random() * 15)
        }))
      };

      setInsights(processedInsights);
    } catch (error) {
      console.error('Error fetching personal insights:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getCorrelationStrength = (correlation) => {
    const abs = Math.abs(correlation);
    if (abs >= 0.7) return { label: 'Strong', color: 'text-green-600' };
    if (abs >= 0.5) return { label: 'Moderate', color: 'text-yellow-600' };
    return { label: 'Weak', color: 'text-gray-600' };
  };

  const renderSummaryCard = () => (
    <Card className="mb-6">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Brain className="h-5 w-5 text-blue-600" />
            AI Health Summary
          </CardTitle>
          <Badge variant="outline" className="bg-blue-50 text-blue-700">
            Score: {insights?.summary.overall_score}/100
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-semibold text-green-700 flex items-center gap-2 mb-3">
              <CheckCircle className="h-4 w-4" />
              Key Achievements
            </h4>
            <ul className="space-y-2">
              {insights?.summary.key_achievements.map((achievement, idx) => (
                <li key={idx} className="flex items-start gap-2 text-sm">
                  <div className="w-1.5 h-1.5 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                  {achievement}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-amber-700 flex items-center gap-2 mb-3">
              <Target className="h-4 w-4" />
              Areas for Improvement
            </h4>
            <ul className="space-y-2">
              {insights?.summary.areas_for_improvement.map((area, idx) => (
                <li key={idx} className="flex items-start gap-2 text-sm">
                  <div className="w-1.5 h-1.5 bg-amber-500 rounded-full mt-2 flex-shrink-0"></div>
                  {area}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  const renderPatternAnalysis = () => (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BarChart3 className="h-5 w-5 text-purple-600" />
          Pattern Analysis
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="mb-4">
          <div className="flex gap-2 mb-4">
            {Object.keys(insights?.patterns || {}).map((patternKey) => (
              <Button
                key={patternKey}
                variant={selectedPattern === patternKey ? "default" : "outline"}
                size="sm"
                onClick={() => setSelectedPattern(patternKey)}
                className="capitalize"
              >
                {patternKey}
              </Button>
            ))}
          </div>
        </div>

        {insights?.patterns[selectedPattern] && (
          <div>
            <div className="flex items-center justify-between mb-4">
              <h4 className="font-semibold">{insights.patterns[selectedPattern].title}</h4>
              <Badge variant="outline">
                Confidence: {Math.round(insights.patterns[selectedPattern].confidence * 100)}%
              </Badge>
            </div>

            <div className="space-y-3 mb-6">
              {insights.patterns[selectedPattern].insights.map((insight, idx) => (
                <div key={idx} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                  <Lightbulb className="h-4 w-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                  <span className="text-sm">{insight}</span>
                </div>
              ))}
            </div>

            {/* Pattern visualization based on selected pattern */}
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                {selectedPattern === 'nutrition' && (
                  <LineChart data={insights.patterns[selectedPattern].data.slice(-7)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Line 
                      type="monotone" 
                      dataKey="calories" 
                      stroke="#8884d8" 
                      strokeWidth={2}
                      name="Calories"
                    />
                    <Line 
                      type="monotone" 
                      dataKey="energy" 
                      stroke="#82ca9d" 
                      strokeWidth={2}
                      name="Energy Level"
                    />
                  </LineChart>
                )}
                {selectedPattern === 'activity' && (
                  <AreaChart data={insights.patterns[selectedPattern].data.slice(-7)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Area 
                      type="monotone" 
                      dataKey="energy" 
                      stackId="1"
                      stroke="#8884d8" 
                      fill="#8884d8"
                      name="Energy"
                    />
                    <Area 
                      type="monotone" 
                      dataKey="exercise" 
                      stackId="1"
                      stroke="#82ca9d" 
                      fill="#82ca9d"
                      name="Exercise (min)"
                    />
                  </AreaChart>
                )}
                {selectedPattern === 'behavioral' && (
                  <BarChart data={insights.patterns[selectedPattern].data.slice(-7)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="mood" fill="#8884d8" name="Mood Score" />
                    <Bar dataKey="consistency" fill="#82ca9d" name="Consistency Score" />
                  </BarChart>
                )}
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );

  const renderRecommendations = () => (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-indigo-600" />
          AI Recommendations
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {insights?.recommendations.map((rec, idx) => (
            <div key={idx} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className="font-semibold">{rec.title}</h4>
                    <Badge className={getPriorityColor(rec.priority)}>
                      {rec.priority}
                    </Badge>
                  </div>
                  <Badge variant="outline" className="text-xs">
                    {rec.category}
                  </Badge>
                </div>
              </div>
              
              <p className="text-gray-600 mb-3">{rec.description}</p>
              
              <div className="bg-blue-50 p-3 rounded-lg mb-3">
                <div className="flex items-start gap-2">
                  <ArrowRight className="h-4 w-4 text-blue-600 mt-0.5" />
                  <div>
                    <p className="font-medium text-blue-900">Action Plan:</p>
                    <p className="text-blue-800 text-sm">{rec.action}</p>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium text-gray-500">Expected Impact:</span>
                  <p className="text-gray-700">{rec.impact}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-500">Timeline:</span>
                  <p className="text-gray-700">{rec.timeline}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );

  const renderCorrelations = () => (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Activity className="h-5 w-5 text-orange-600" />
          Health Correlations
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {insights?.correlations.map((corr, idx) => (
            <div key={idx} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="font-medium">{corr.factor1}</span>
                  <ArrowRight className="h-4 w-4 text-gray-400" />
                  <span className="font-medium">{corr.factor2}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Badge 
                    variant="outline" 
                    className={getCorrelationStrength(corr.correlation).color}
                  >
                    {corr.strength}
                  </Badge>
                  <span className="text-sm font-mono">
                    r = {corr.correlation.toFixed(2)}
                  </span>
                </div>
              </div>
              <p className="text-gray-600 text-sm">{corr.insight}</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );

  const renderMLPredictionsCard = () => (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Zap className="h-5 w-5 text-orange-600" />
          AI Health Predictions
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid md:grid-cols-3 gap-4">
          {/* Energy Prediction */}
          {energyPrediction && (
            <div className="p-4 border border-orange-200 rounded-lg bg-orange-50">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold text-orange-800">Energy Level</h4>
                <Badge className="bg-orange-100 text-orange-700">
                  {energyPrediction.predicted_energy}/10
                </Badge>
              </div>
              <p className="text-sm text-orange-700 mb-2">
                Predicted based on your intake and lifestyle
              </p>
              <div className="text-xs text-orange-600">
                Confidence: {Math.round((energyPrediction.confidence || 0) * 100)}%
              </div>
              {energyPrediction.recommendations && (
                <div className="mt-2">
                  <p className="text-xs font-medium text-orange-800">Top tip:</p>
                  <p className="text-xs text-orange-700">
                    {energyPrediction.recommendations[0]}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Sleep Quality Prediction */}
          {sleepImpact && (
            <div className="p-4 border border-blue-200 rounded-lg bg-blue-50">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold text-blue-800">Sleep Quality</h4>
                <Badge className="bg-blue-100 text-blue-700">
                  {sleepImpact.predicted_sleep_quality}/10
                </Badge>
              </div>
              <p className="text-sm text-blue-700 mb-2">
                Based on your daily choices
              </p>
              <div className="text-xs text-blue-600">
                Improvement potential: +{sleepImpact.improvement_potential || 0}
              </div>
              {sleepImpact.recommendations && (
                <div className="mt-2">
                  <p className="text-xs font-medium text-blue-800">Top tip:</p>
                  <p className="text-xs text-blue-700">
                    {sleepImpact.recommendations[0]}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Mood Correlation */}
          {moodCorrelation && (
            <div className="p-4 border border-purple-200 rounded-lg bg-purple-50">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold text-purple-800">Mood Patterns</h4>
                <Badge className="bg-purple-100 text-purple-700">
                  {Math.round((moodCorrelation.confidence || 0) * 100)}% confident
                </Badge>
              </div>
              <p className="text-sm text-purple-700 mb-2">
                Food-mood correlations identified
              </p>
              {moodCorrelation.correlations && Object.keys(moodCorrelation.correlations).length > 0 && (
                <div className="text-xs text-purple-600">
                  Strongest: {Object.keys(moodCorrelation.correlations)[0]?.replace(/_/g, ' ')}
                </div>
              )}
              {moodCorrelation.recommendations && (
                <div className="mt-2">
                  <p className="text-xs font-medium text-purple-800">Top tip:</p>
                  <p className="text-xs text-purple-700">
                    {moodCorrelation.recommendations[0]}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );

  const renderTrendChart = () => (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <TrendingUp className="h-5 w-5 text-green-600" />
          Trend Analysis
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={insights?.trend_data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="overall_score" 
                stroke="#8884d8" 
                strokeWidth={2}
                name="Overall Score"
              />
              <Line 
                type="monotone" 
                dataKey="nutrition_score" 
                stroke="#82ca9d" 
                strokeWidth={2}
                name="Nutrition Score"
              />
              <Line 
                type="monotone" 
                dataKey="energy_score" 
                stroke="#ffc658" 
                strokeWidth={2}
                name="Energy Score"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );

  // Widget version (compact)
  if (isWidget) {
    if (loading) {
      return (
        <Card className={className}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Brain className="h-5 w-5 text-blue-600" />
              AI Insights
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="animate-pulse space-y-3">
              <div className="h-4 bg-gray-200 rounded w-3/4"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              <div className="h-4 bg-gray-200 rounded w-2/3"></div>
            </div>
          </CardContent>
        </Card>
      );
    }

    if (error) {
      return (
        <Card className={className}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Brain className="h-5 w-5 text-blue-600" />
              AI Insights
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2 text-red-600">
              <AlertCircle className="h-4 w-4" />
              <span>Unable to load insights</span>
            </div>
          </CardContent>
        </Card>
      );
    }

    return (
      <Card className={className}>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Brain className="h-5 w-5 text-blue-600" />
              AI Insights
            </CardTitle>
            <Badge variant="outline" className="bg-blue-50 text-blue-700">
              Score: {insights?.summary.overall_score}/100
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Top Insight */}
            {insights?.recommendations[0] && (
              <div className="p-3 bg-blue-50 rounded-lg">
                <div className="flex items-start gap-2">
                  <Lightbulb className="h-4 w-4 text-blue-600 mt-0.5" />
                  <div>
                    <p className="font-medium text-blue-900 text-sm">
                      {insights.recommendations[0].title}
                    </p>
                    <p className="text-blue-700 text-xs mt-1">
                      {insights.recommendations[0].description}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Key Achievement */}
            {insights?.summary.key_achievements[0] && (
              <div className="flex items-start gap-2">
                <CheckCircle className="h-4 w-4 text-green-600 mt-0.5" />
                <span className="text-sm text-gray-700">
                  {insights.summary.key_achievements[0]}
                </span>
              </div>
            )}

            <Button 
              variant="outline" 
              size="sm" 
              className="w-full"
              onClick={() => window.location.href = '/personal-insights'}
            >
              View Full Insights
              <ArrowRight className="h-4 w-4 ml-2" />
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  // Full page version
  return (
    <div className="min-h-screen bg-gray-50">
      <SmartNavigation role="patient" />
      
      <div className="container mx-auto px-4 py-6">
        <div className="mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Personal AI Insights</h1>
              <p className="text-gray-600">AI-powered health analytics and personalized recommendations</p>
            </div>
            <div className="flex items-center gap-2">
              <div className="flex gap-1">
                <Button
                  variant={activeTimeframe === 'weekly' ? "default" : "outline"}
                  size="sm"
                  onClick={() => setActiveTimeframe('weekly')}
                >
                  <Calendar className="h-4 w-4 mr-1" />
                  Weekly
                </Button>
                <Button
                  variant={activeTimeframe === 'monthly' ? "default" : "outline"}
                  size="sm"
                  onClick={() => setActiveTimeframe('monthly')}
                >
                  <Calendar className="h-4 w-4 mr-1" />
                  Monthly
                </Button>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  fetchPersonalInsights();
                  fetchMLPredictions();
                }}
                disabled={loading}
              >
                <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
              </Button>
            </div>
          </div>
        </div>

        {loading && (
          <div className="space-y-6">
            {[1, 2, 3].map((i) => (
              <Card key={i}>
                <CardContent className="p-6">
                  <div className="animate-pulse space-y-4">
                    <div className="h-6 bg-gray-200 rounded w-1/3"></div>
                    <div className="space-y-2">
                      <div className="h-4 bg-gray-200 rounded"></div>
                      <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {error && (
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-2 text-red-600">
                <AlertCircle className="h-5 w-5" />
                <span>Error loading insights: {error}</span>
              </div>
              <Button 
                variant="outline" 
                className="mt-4"
                onClick={fetchPersonalInsights}
              >
                Try Again
              </Button>
            </CardContent>
          </Card>
        )}

        {insights && !loading && (
          <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
            <div className="border-b">
              <TabsList className="grid w-full grid-cols-5">
                <TabsTrigger value="overview" className="flex items-center gap-2">
                  <Brain className="h-4 w-4" />
                  Overview
                </TabsTrigger>
                <TabsTrigger value="predictions" className="flex items-center gap-2">
                  <Zap className="h-4 w-4" />
                  Predictions
                </TabsTrigger>
                <TabsTrigger value="whatif" className="flex items-center gap-2">
                  <Calculator className="h-4 w-4" />
                  What-If
                </TabsTrigger>
                <TabsTrigger value="weekly" className="flex items-center gap-2">
                  <Calendar className="h-4 w-4" />
                  Weekly Patterns
                </TabsTrigger>
                <TabsTrigger value="correlations" className="flex items-center gap-2">
                  <Activity className="h-4 w-4" />
                  Correlations
                </TabsTrigger>
              </TabsList>
            </div>

            <TabsContent value="overview" className="space-y-6">
              {renderSummaryCard()}
              {renderMLPredictionsCard()}
              {renderPatternAnalysis()}
              {renderRecommendations()}
            </TabsContent>

            <TabsContent value="predictions" className="space-y-6">
              {renderMLPredictionsCard()}
              {renderTrendChart()}
              
              {/* Energy Prediction Details */}
              {energyPrediction && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Zap className="h-5 w-5 text-orange-600" />
                      Detailed Energy Analysis
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-semibold mb-3">Key Factors</h4>
                        <div className="space-y-2">
                          {energyPrediction.factors && Object.entries(energyPrediction.factors).map(([key, factor]) => (
                            <div key={key} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                              <span className="text-sm capitalize">{key.replace(/_/g, ' ')}</span>
                              <div className="flex items-center gap-2">
                                <Badge variant="outline">{factor.value}</Badge>
                                <Badge className={
                                  factor.impact === 'positive' ? 'bg-green-100 text-green-800' :
                                  factor.impact === 'negative' ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'
                                }>
                                  {factor.impact}
                                </Badge>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-3">Recommendations</h4>
                        <div className="space-y-2">
                          {energyPrediction.recommendations?.map((rec, idx) => (
                            <div key={idx} className="p-3 bg-blue-50 rounded-lg">
                              <div className="flex items-start gap-2">
                                <CheckCircle className="h-4 w-4 text-blue-600 mt-0.5" />
                                <span className="text-sm text-blue-800">{rec}</span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}
            </TabsContent>

            <TabsContent value="whatif" className="space-y-6">
              <WhatIfScenarios userId={userId} />
            </TabsContent>

            <TabsContent value="weekly" className="space-y-6">
              <WeeklyHealthDashboard userId={userId} />
            </TabsContent>

            <TabsContent value="correlations" className="space-y-6">
              {renderCorrelations()}
              
              {/* Mood-Food Correlation Details */}
              {moodCorrelation && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Heart className="h-5 w-5 text-purple-600" />
                      Mood-Food Analysis
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid md:grid-cols-3 gap-6">
                      {/* Correlations */}
                      <div>
                        <h4 className="font-semibold mb-3">Food Correlations</h4>
                        <div className="space-y-2">
                          {moodCorrelation.correlations && Object.entries(moodCorrelation.correlations).map(([key, corr]) => (
                            <div key={key} className="p-2 border rounded">
                              <div className="flex items-center justify-between">
                                <span className="text-sm capitalize">{key.replace(/_/g, ' ')}</span>
                                <Badge variant="outline">{corr.correlation?.toFixed(2)}</Badge>
                              </div>
                              <p className="text-xs text-gray-600 mt-1">{corr.strength} correlation</p>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Trigger Foods */}
                      <div>
                        <h4 className="font-semibold mb-3">Trigger Foods</h4>
                        <div className="space-y-2">
                          {moodCorrelation.trigger_foods && Object.entries(moodCorrelation.trigger_foods).map(([key, trigger]) => (
                            <div key={key} className="p-2 border border-red-200 rounded bg-red-50">
                              <div className="flex items-center justify-between">
                                <span className="text-sm capitalize text-red-800">{key.replace(/_/g, ' ')}</span>
                                <Badge className="bg-red-100 text-red-800">Impact: {trigger.impact}</Badge>
                              </div>
                              <p className="text-xs text-red-600 mt-1">{trigger.description}</p>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Mood Predictors */}
                      <div>
                        <h4 className="font-semibold mb-3">Mood Predictors</h4>
                        <div className="space-y-2">
                          {moodCorrelation.mood_predictors && Object.entries(moodCorrelation.mood_predictors).map(([key, predictor]) => (
                            <div key={key} className="p-2 border border-green-200 rounded bg-green-50">
                              <div className="flex items-center justify-between">
                                <span className="text-sm capitalize text-green-800">{key.replace(/_/g, ' ')}</span>
                                <Badge className="bg-green-100 text-green-800">
                                  {Math.round((predictor.importance || 0) * 100)}%
                                </Badge>
                              </div>
                              <p className="text-xs text-green-600 mt-1">{predictor.description}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}
            </TabsContent>
          </Tabs>
        )}
      </div>
    </div>
  );
};

export default PersonalInsights;