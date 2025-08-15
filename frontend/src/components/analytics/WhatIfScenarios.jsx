import React, { useState, useEffect, useMemo } from 'react';
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
  Info
} from 'lucide-react';
import predictiveAnalyticsService from '../../services/predictiveAnalyticsService';

const WhatIfScenarios = ({ userId = 'demo-patient-123', className = '' }) => {
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
        adjustments
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
                <div className="space-y-4">
                  {/* Confidence Score */}
                  <div className="text-center pb-3 border-b">
                    <Badge className="bg-blue-100 text-blue-800">
                      Confidence: {Math.round((prediction.confidence || 0.7) * 100)}%
                    </Badge>
                  </div>

                  {/* Main Impacts */}
                  {prediction.impact_analysis && (
                    <div className="space-y-3">
                      <h4 className="font-semibold text-sm text-gray-700">Predicted Changes:</h4>
                      
                      {/* Energy Impact */}
                      {prediction.current_state?.energy && prediction.predicted_state?.energy && (
                        <div className={`p-3 rounded-lg border ${getImpactColor(prediction.impact_analysis.energy_change || 0)}`}>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <Zap className="h-4 w-4" />
                              <span className="font-medium text-sm">Energy Level</span>
                            </div>
                            <div className="flex items-center gap-1">
                              {getImpactIcon(prediction.impact_analysis.energy_change || 0)}
                              <span className="text-sm font-semibold">
                                {formatImpact(
                                  prediction.current_state.energy,
                                  prediction.predicted_state.energy
                                ).formatted}
                              </span>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Sleep Impact */}
                      {prediction.current_state?.sleep && prediction.predicted_state?.sleep && (
                        <div className={`p-3 rounded-lg border ${getImpactColor(prediction.impact_analysis.sleep_change || 0)}`}>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <Moon className="h-4 w-4" />
                              <span className="font-medium text-sm">Sleep Quality</span>
                            </div>
                            <div className="flex items-center gap-1">
                              {getImpactIcon(prediction.impact_analysis.sleep_change || 0)}
                              <span className="text-sm font-semibold">
                                {formatImpact(
                                  prediction.current_state.sleep,
                                  prediction.predicted_state.sleep
                                ).formatted}
                              </span>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Mood Impact */}
                      {prediction.current_state?.mood && prediction.predicted_state?.mood && (
                        <div className={`p-3 rounded-lg border ${getImpactColor(prediction.impact_analysis.mood_change || 0)}`}>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <Heart className="h-4 w-4" />
                              <span className="font-medium text-sm">Mood Stability</span>
                            </div>
                            <div className="flex items-center gap-1">
                              {getImpactIcon(prediction.impact_analysis.mood_change || 0)}
                              <span className="text-sm font-semibold">
                                {formatImpact(
                                  prediction.current_state.mood,
                                  prediction.predicted_state.mood
                                ).formatted}
                              </span>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Recommendations */}
                  {prediction.recommendations && prediction.recommendations.length > 0 && (
                    <div className="pt-3 border-t">
                      <h4 className="font-semibold text-sm text-gray-700 mb-2">AI Recommendations:</h4>
                      <div className="space-y-2">
                        {prediction.recommendations.slice(0, 3).map((rec, idx) => (
                          <div key={idx} className="flex items-start gap-2 p-2 bg-blue-50 rounded-lg">
                            <CheckCircle className="h-3 w-3 text-blue-600 mt-0.5 flex-shrink-0" />
                            <span className="text-xs text-blue-800">{rec}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Action Button */}
                  <Button className="w-full mt-4" size="sm">
                    Apply These Changes
                    <ArrowRight className="h-3 w-3 ml-2" />
                  </Button>
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