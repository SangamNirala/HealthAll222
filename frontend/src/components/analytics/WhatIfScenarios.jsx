import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useRole } from '../../context/RoleContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Slider } from '../ui/slider';
import { 
  Calculator,
  TrendingUp,
  TrendingDown,
  Zap,
  Moon,
  Heart,
  Target,
  Play,
  RotateCcw,
  AlertCircle,
  CheckCircle,
  Sparkles,
  ArrowRight,
  Info,
  Clock
} from 'lucide-react';
import predictiveAnalyticsService from '../../services/predictiveAnalyticsService';

const WhatIfScenarios = ({ userId = 'demo-patient-123', className = '' }) => {
  const navigate = useNavigate();
  const [baselineData, setBaselineData] = useState({
    calories: 2000,
    protein_g: 100,
    carbs_g: 250,
    fat_g: 70,
    sugar_g: 50,
    fiber_g: 25,
    sleep_hours: 7.5,
    exercise_minutes: 30,
    stress_level: 5,
    water_intake_ml: 2500,
    caffeine_mg: 100
  });

  const [adjustments, setAdjustments] = useState({
    calories: 0,
    protein_g: 0,
    carbs_g: 0,
    fat_g: 0,
    sugar_g: 0,
    fiber_g: 0,
    sleep_hours: 0,
    exercise_minutes: 0,
    stress_level: 0,
    water_intake_ml: 0,
    caffeine_mg: 0
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedScenario, setSelectedScenario] = useState(null);

  const modifiedData = useMemo(() => {
    const result = {};
    Object.keys(baselineData).forEach(key => {
      result[key] = baselineData[key] + adjustments[key];
    });
    return result;
  }, [baselineData, adjustments]);

  useEffect(() => {
    // Auto-predict when adjustments change (debounced)
    const timeoutId = setTimeout(() => {
      if (Object.values(adjustments).some(val => val !== 0)) {
        handlePredict();
      }
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [adjustments]);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const result = await predictiveAnalyticsService.processWhatIfScenarios(
        baselineData,
        adjustments,
        userId
      );

      if (result.success) {
        setPrediction(result.data);
      } else {
        console.error('Prediction failed:', result.error);
      }
    } catch (error) {
      console.error('Error running scenario:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setAdjustments({
      calories: 0,
      protein_g: 0,
      carbs_g: 0,
      fat_g: 0,
      sugar_g: 0,
      fiber_g: 0,
      sleep_hours: 0,
      exercise_minutes: 0,
      stress_level: 0,
      water_intake_ml: 0,
      caffeine_mg: 0
    });
    setPrediction(null);
    setSelectedScenario(null);
  };

  const applyPresetScenario = (scenario) => {
    setSelectedScenario(scenario.id);
    const newAdjustments = { ...adjustments };
    
    Object.keys(scenario.changes).forEach(key => {
      newAdjustments[key] = scenario.changes[key];
    });
    
    setAdjustments(newAdjustments);
  };

  const getImpactColor = (change) => {
    if (change > 10) return 'text-green-600 bg-green-50';
    if (change > 0) return 'text-blue-600 bg-blue-50';
    if (change > -10) return 'text-orange-600 bg-orange-50';
    return 'text-red-600 bg-red-50';
  };

  const getImpactIcon = (change) => {
    if (change > 0) return <TrendingUp className="h-4 w-4" />;
    if (change < 0) return <TrendingDown className="h-4 w-4" />;
    return null;
  };

  const formatImpact = (current, predicted, unit = '') => {
    const change = predicted - current;
    const percentage = current > 0 ? ((change / current) * 100) : 0;
    return {
      absolute: change,
      percentage: percentage,
      formatted: `${change > 0 ? '+' : ''}${change.toFixed(1)}${unit} (${percentage > 0 ? '+' : ''}${percentage.toFixed(1)}%)`
    };
  };

  const presetScenarios = predictiveAnalyticsService.generateSampleScenarios();

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calculator className="h-6 w-6 text-purple-600" />
            Interactive "What-If" Health Scenarios
          </CardTitle>
          <p className="text-gray-600">
            Adjust your lifestyle factors and see real-time predictions of how they'll impact your health
          </p>
        </CardHeader>
      </Card>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Adjustment Controls */}
        <div className="lg:col-span-2 space-y-6">
          {/* Preset Scenarios */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Quick Scenarios</CardTitle>
              <p className="text-sm text-gray-600">Try these common health optimization scenarios</p>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {presetScenarios.map((scenario) => (
                  <Button
                    key={scenario.id}
                    variant={selectedScenario === scenario.id ? "default" : "outline"}
                    className="h-auto p-3 text-left justify-start"
                    onClick={() => applyPresetScenario(scenario)}
                  >
                    <div>
                      <div className="font-semibold text-sm">{scenario.name}</div>
                      <div className="text-xs opacity-75">{scenario.description}</div>
                    </div>
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Nutrition Adjustments */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                🍎 Nutrition Adjustments
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {[
                { key: 'calories', label: 'Daily Calories', min: -500, max: 500, step: 50, unit: ' kcal' },
                { key: 'protein_g', label: 'Protein', min: -50, max: 50, step: 5, unit: 'g' },
                { key: 'carbs_g', label: 'Carbohydrates', min: -100, max: 100, step: 10, unit: 'g' },
                { key: 'fat_g', label: 'Fat', min: -30, max: 30, step: 5, unit: 'g' },
                { key: 'sugar_g', label: 'Sugar', min: -30, max: 30, step: 5, unit: 'g' },
                { key: 'fiber_g', label: 'Fiber', min: -15, max: 15, step: 2, unit: 'g' }
              ].map(({ key, label, min, max, step, unit }) => (
                <div key={key}>
                  <div className="flex justify-between items-center mb-2">
                    <label className="text-sm font-medium">{label}</label>
                    <div className="flex items-center gap-2">
                      <Badge variant="outline" className="text-xs">
                        {baselineData[key]}{unit} → {modifiedData[key]}{unit}
                      </Badge>
                      <span className={`text-sm px-2 py-1 rounded ${
                        adjustments[key] > 0 ? 'text-green-600 bg-green-50' :
                        adjustments[key] < 0 ? 'text-red-600 bg-red-50' : 'text-gray-600'
                      }`}>
                        {adjustments[key] > 0 ? '+' : ''}{adjustments[key]}{unit}
                      </span>
                    </div>
                  </div>
                  <Slider
                    value={[adjustments[key]]}
                    onValueChange={(value) => setAdjustments(prev => ({ ...prev, [key]: value[0] }))}
                    min={min}
                    max={max}
                    step={step}
                    className="w-full"
                  />
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Lifestyle Adjustments */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                🏃‍♀️ Lifestyle Adjustments
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {[
                { key: 'sleep_hours', label: 'Sleep Duration', min: -2, max: 2, step: 0.5, unit: ' hrs', baseline: 7.5 },
                { key: 'exercise_minutes', label: 'Exercise', min: -60, max: 120, step: 15, unit: ' min' },
                { key: 'stress_level', label: 'Stress Level', min: -3, max: 3, step: 1, unit: '', baseline: 5, inverted: true },
                { key: 'water_intake_ml', label: 'Water Intake', min: -1000, max: 1000, step: 250, unit: 'ml' },
                { key: 'caffeine_mg', label: 'Caffeine', min: -150, max: 150, step: 25, unit: 'mg' }
              ].map(({ key, label, min, max, step, unit, inverted }) => (
                <div key={key}>
                  <div className="flex justify-between items-center mb-2">
                    <label className="text-sm font-medium">{label}</label>
                    <div className="flex items-center gap-2">
                      <Badge variant="outline" className="text-xs">
                        {baselineData[key]}{unit} → {modifiedData[key]}{unit}
                      </Badge>
                      <span className={`text-sm px-2 py-1 rounded ${
                        (inverted ? adjustments[key] < 0 : adjustments[key] > 0) ? 'text-green-600 bg-green-50' :
                        (inverted ? adjustments[key] > 0 : adjustments[key] < 0) ? 'text-red-600 bg-red-50' : 'text-gray-600'
                      }`}>
                        {adjustments[key] > 0 ? '+' : ''}{adjustments[key]}{unit}
                      </span>
                    </div>
                  </div>
                  <Slider
                    value={[adjustments[key]]}
                    onValueChange={(value) => setAdjustments(prev => ({ ...prev, [key]: value[0] }))}
                    min={min}
                    max={max}
                    step={step}
                    className="w-full"
                  />
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Prediction Results */}
        <div className="space-y-6">
          <Card className="sticky top-6">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-purple-600" />
                  Predicted Impact
                </CardTitle>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleReset}
                  className="text-xs"
                >
                  <RotateCcw className="h-3 w-3 mr-1" />
                  Reset
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {loading && (
                <div className="animate-pulse space-y-4">
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                  <div className="h-4 bg-gray-200 rounded w-2/3"></div>
                </div>
              )}

              {!loading && !prediction && (
                <div className="text-center py-8 text-gray-500">
                  <Calculator className="h-8 w-8 mx-auto mb-3 opacity-50" />
                  <p className="text-sm">Make adjustments above to see predicted health impacts</p>
                </div>
              )}

              {!loading && prediction && (
                <div className="space-y-6">
                  {/* Header with Confidence and Timeframe */}
                  <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-4 rounded-lg">
                    <div className="flex justify-between items-center mb-2">
                      <Badge className="bg-green-100 text-green-800 font-semibold">
                        Confidence: {Math.round((prediction.confidence || 0.7) * 100)}%
                      </Badge>
                      <span className="text-xs text-gray-600">Based on ML analysis</span>
                    </div>
                    <h4 className="font-semibold text-gray-800">Predicted Health Impact Analysis</h4>
                    <p className="text-xs text-gray-600 mt-1">
                      Personalized predictions based on scientific research and your health profile
                    </p>
                  </div>

                  {/* Main Impacts - Enhanced Display */}
                  {prediction.impact_analysis && (
                    <div className="space-y-3">
                      <h4 className="font-semibold text-sm text-gray-700 flex items-center gap-2">
                        <Target className="h-4 w-4" />
                        Detailed Impact Analysis:
                      </h4>
                      
                      {/* Render each impact metric */}
                      {Object.entries(prediction.impact_analysis).map(([metric, data]) => {
                        const isPositive = data.percentage_change > 0;
                        const isSignificant = Math.abs(data.percentage_change) > 5;
                        
                        const metricConfig = {
                          'energy_level': { icon: Zap, label: 'Energy Level', color: 'orange' },
                          'sleep_quality': { icon: Moon, label: 'Sleep Quality', color: 'indigo' },
                          'mood_stability': { icon: Heart, label: 'Mood Stability', color: 'pink' }
                        };
                        
                        const config = metricConfig[metric] || { icon: Target, label: metric.replace('_', ' '), color: 'gray' };
                        const Icon = config.icon;
                        
                        return (
                          <div key={metric} className={`p-4 rounded-lg border-l-4 ${
                            isPositive 
                              ? `bg-green-50 border-green-400 ${isSignificant ? 'ring-1 ring-green-200' : ''}` 
                              : data.percentage_change < 0 
                              ? `bg-red-50 border-red-400 ${isSignificant ? 'ring-1 ring-red-200' : ''}` 
                              : 'bg-gray-50 border-gray-300'
                          }`}>
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex items-center gap-2">
                                <Icon className={`h-5 w-5 text-${config.color}-600`} />
                                <span className="font-semibold text-sm text-gray-800">{config.label}</span>
                                {isSignificant && (
                                  <Badge variant="outline" className="text-xs">
                                    {data.impact_level} impact
                                  </Badge>
                                )}
                              </div>
                              <div className="text-right">
                                <div className="flex items-center gap-1">
                                  {getImpactIcon(data.percentage_change)}
                                  <span className="font-bold text-sm">
                                    {data.percentage_change > 0 ? '+' : ''}{data.percentage_change.toFixed(1)}%
                                  </span>
                                </div>
                                <span className="text-xs text-gray-500">
                                  {data.current_value} → {data.predicted_value}/10
                                </span>
                              </div>
                            </div>
                            
                            {/* Impact Explanation */}
                            <div className="text-xs text-gray-600 mt-2">
                              {Math.abs(data.percentage_change) > 10 
                                ? `This represents a ${isPositive ? 'significant improvement' : 'notable decrease'} that you would likely notice in daily activities.`
                                : Math.abs(data.percentage_change) > 3
                                ? `This is a ${isPositive ? 'moderate improvement' : 'small decrease'} that may be subtle but meaningful over time.`
                                : 'This change represents a minimal impact on this health metric.'
                              }
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}

                  {/* Scientific Justification */}
                  {prediction.scientific_basis && Object.keys(prediction.scientific_basis).length > 0 && (
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <h4 className="font-semibold text-sm text-blue-900 mb-3 flex items-center gap-2">
                        <Sparkles className="h-4 w-4" />
                        Scientific Evidence:
                      </h4>
                      <div className="space-y-2">
                        {Object.entries(prediction.scientific_basis).map(([key, evidence], idx) => (
                          <div key={key} className="flex items-start gap-2 text-xs">
                            <div className="w-1.5 h-1.5 bg-blue-400 rounded-full mt-2 flex-shrink-0"></div>
                            <span className="text-blue-800">{evidence}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Expected Timeframes */}
                  {prediction.timeframe && Object.keys(prediction.timeframe).length > 0 && (
                    <div className="bg-purple-50 p-4 rounded-lg">
                      <h4 className="font-semibold text-sm text-purple-900 mb-3 flex items-center gap-2">
                        <Clock className="h-4 w-4" />
                        Expected Timeline:
                      </h4>
                      <div className="space-y-2">
                        {Object.entries(prediction.timeframe).map(([key, timeline], idx) => (
                          <div key={key} className="flex items-start gap-2 text-xs">
                            <div className="w-1.5 h-1.5 bg-purple-400 rounded-full mt-2 flex-shrink-0"></div>
                            <span className="text-purple-800">
                              <span className="font-medium capitalize">{key.replace('_', ' ')}:</span> {timeline}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* AI Recommendations - Enhanced */}
                  {prediction.recommendations && prediction.recommendations.length > 0 && (
                    <div className="border-t pt-4">
                      <h4 className="font-semibold text-sm text-gray-700 mb-3 flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-600" />
                        AI-Powered Insights & Recommendations:
                      </h4>
                      <div className="space-y-2">
                        {prediction.recommendations.map((rec, idx) => {
                          const isJustification = rec.includes('└─');
                          return (
                            <div key={idx} className={`
                              ${isJustification 
                                ? 'ml-4 text-xs text-gray-600 italic bg-gray-50 p-2 rounded-md border-l-2 border-gray-200' 
                                : 'p-3 bg-green-50 rounded-lg border-l-3 border-green-400'
                              }
                            `}>
                              {isJustification ? (
                                <span>{rec.replace('└─ ', '💡 ')}</span>
                              ) : (
                                <div className="flex items-start gap-2">
                                  <span className="text-sm text-green-800 font-medium">{rec}</span>
                                </div>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  )}

                  {/* Risk Factors & Considerations */}
                  {prediction.risk_factors && prediction.risk_factors.length > 0 && (
                    <div className="bg-amber-50 p-4 rounded-lg">
                      <h4 className="font-semibold text-sm text-amber-900 mb-3 flex items-center gap-2">
                        <AlertCircle className="h-4 w-4" />
                        Important Considerations:
                      </h4>
                      <div className="space-y-2">
                        {prediction.risk_factors.map((risk, idx) => (
                          <div key={idx} className="flex items-start gap-2 text-xs text-amber-800">
                            <span>{risk}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Action Button - Enhanced */}
                  <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-4 rounded-lg text-white">
                    <div className="flex justify-between items-center">
                      <div>
                        <h5 className="font-semibold text-sm">Ready to implement these changes?</h5>
                        <p className="text-xs opacity-90 mt-1">Track your progress and adjust as needed</p>
                      </div>
                      <Button className="bg-white text-blue-600 hover:bg-gray-100" size="sm">
                        Start Tracking
                        <ArrowRight className="h-3 w-3 ml-2" />
                      </Button>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default WhatIfScenarios;