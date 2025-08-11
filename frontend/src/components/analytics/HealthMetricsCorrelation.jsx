import React, { useState, useEffect } from 'react';
import {
  ScatterChart,
  Scatter,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { 
  Activity, 
  Heart, 
  Scale, 
  Moon, 
  Zap,
  TrendingUp,
  AlertCircle
} from 'lucide-react';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

const HealthMetricsCorrelation = ({ userId }) => {
  const [correlationData, setCorrelationData] = useState([]);
  const [correlations, setCorrelations] = useState([]);
  const [selectedCorrelation, setSelectedCorrelation] = useState('weight_calories');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCorrelationData();
  }, [userId]);

  const fetchCorrelationData = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/patient/symptoms-correlation/${userId}`);
      if (response.ok) {
        const data = await response.json();
        setCorrelations(data.correlations || []);
        
        // Generate sample correlation data for demonstration
        generateSampleData();
      }
    } catch (error) {
      console.error('Failed to fetch correlation data:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateSampleData = () => {
    // Generate sample data for different correlations
    const sampleData = {
      weight_calories: generateScatterData(30, 1800, 2400, 150, 180, 0.7),
      bp_sodium: generateScatterData(25, 2000, 4000, 110, 140, 0.6),
      exercise_energy: generateScatterData(28, 30, 120, 3, 9, 0.8),
      sleep_nutrition: generateScatterData(30, 1600, 2200, 5, 9, -0.3),
    };
    setCorrelationData(sampleData);
  };

  const generateScatterData = (count, xMin, xMax, yMin, yMax, correlation) => {
    const data = [];
    for (let i = 0; i < count; i++) {
      const x = Math.random() * (xMax - xMin) + xMin;
      const noise = (Math.random() - 0.5) * (yMax - yMin) * 0.3;
      const y = yMin + (yMax - yMin) * (correlation > 0 ? 
        ((x - xMin) / (xMax - xMin)) : 
        (1 - (x - xMin) / (xMax - xMin))) + noise;
      
      data.push({
        x: Math.round(x),
        y: Math.round(Math.max(yMin, Math.min(yMax, y))),
        date: new Date(Date.now() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
      });
    }
    return data.reverse();
  };

  // Calculate Pearson correlation coefficient
  const calculateCorrelation = (data) => {
    if (data.length < 2) return 0;
    
    const n = data.length;
    const sumX = data.reduce((sum, d) => sum + d.x, 0);
    const sumY = data.reduce((sum, d) => sum + d.y, 0);
    const sumXY = data.reduce((sum, d) => sum + d.x * d.y, 0);
    const sumX2 = data.reduce((sum, d) => sum + d.x * d.x, 0);
    const sumY2 = data.reduce((sum, d) => sum + d.y * d.y, 0);
    
    const numerator = n * sumXY - sumX * sumY;
    const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));
    
    return denominator === 0 ? 0 : numerator / denominator;
  };

  const correlationTypes = {
    weight_calories: {
      title: 'Weight vs Calorie Intake',
      xLabel: 'Daily Calories',
      yLabel: 'Weight (lbs)',
      icon: <Scale className="h-4 w-4" />,
      color: '#3b82f6',
      description: 'Relationship between daily caloric intake and body weight changes'
    },
    bp_sodium: {
      title: 'Blood Pressure vs Sodium',
      xLabel: 'Sodium Intake (mg)',
      yLabel: 'Systolic BP',
      icon: <Heart className="h-4 w-4" />,
      color: '#ef4444',
      description: 'How sodium intake affects blood pressure readings'
    },
    exercise_energy: {
      title: 'Exercise vs Energy Level',
      xLabel: 'Exercise Minutes',
      yLabel: 'Energy Level (1-10)',
      icon: <Activity className="h-4 w-4" />,
      color: '#10b981',
      description: 'Correlation between daily exercise and energy levels'
    },
    sleep_nutrition: {
      title: 'Sleep vs Nutrition Quality',
      xLabel: 'Daily Calories',
      yLabel: 'Sleep Hours',
      icon: <Moon className="h-4 w-4" />,
      color: '#8b5cf6',
      description: 'How nutrition quality impacts sleep duration and quality'
    }
  };

  const getCorrelationStrength = (value) => {
    const abs = Math.abs(value);
    if (abs >= 0.7) return { strength: 'Strong', color: 'green' };
    if (abs >= 0.4) return { strength: 'Moderate', color: 'yellow' };
    return { strength: 'Weak', color: 'red' };
  };

  const getCorrelationDirection = (value) => {
    if (value > 0.1) return { direction: 'Positive', icon: <TrendingUp className="h-3 w-3" /> };
    if (value < -0.1) return { direction: 'Negative', icon: <TrendingUp className="h-3 w-3 rotate-180" /> };
    return { direction: 'No correlation', icon: <AlertCircle className="h-3 w-3" /> };
  };

  const currentData = correlationData[selectedCorrelation] || [];
  const currentCorr = calculateCorrelation(currentData);
  const corrStrength = getCorrelationStrength(currentCorr);
  const corrDirection = getCorrelationDirection(currentCorr);
  const currentType = correlationTypes[selectedCorrelation];

  if (loading) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="animate-pulse space-y-4">
            <div className="h-4 bg-gray-200 rounded w-1/3"></div>
            <div className="h-64 bg-gray-200 rounded"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-5 w-5" />
            Health Metrics Correlation
          </CardTitle>
          <p className="text-sm text-gray-600">
            Discover relationships between your lifestyle choices and health outcomes
          </p>
        </CardHeader>
      </Card>

      {/* Correlation Selection */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {Object.entries(correlationTypes).map(([key, type]) => (
          <Card 
            key={key}
            className={`cursor-pointer transition-all ${
              selectedCorrelation === key 
                ? 'ring-2 ring-blue-500 bg-blue-50' 
                : 'hover:shadow-md'
            }`}
            onClick={() => setSelectedCorrelation(key)}
          >
            <CardContent className="p-4">
              <div className="flex items-center gap-2 mb-2">
                {type.icon}
                <h3 className="font-medium text-sm">{type.title}</h3>
              </div>
              <p className="text-xs text-gray-600">{type.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Current Correlation Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              {currentType?.icon}
              {currentType?.title}
            </CardTitle>
            <p className="text-sm text-gray-600">{currentType?.description}</p>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <ScatterChart
                  data={currentData}
                  margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="x" 
                    name={currentType?.xLabel}
                    type="number"
                    domain={['dataMin', 'dataMax']}
                  />
                  <YAxis 
                    dataKey="y" 
                    name={currentType?.yLabel}
                    type="number"
                    domain={['dataMin', 'dataMax']}
                  />
                  <Tooltip 
                    cursor={{ strokeDasharray: '3 3' }}
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const data = payload[0].payload;
                        return (
                          <div className="bg-white p-3 rounded-lg shadow-lg border">
                            <p className="text-sm text-gray-600">{data.date}</p>
                            <p className="font-medium">
                              {currentType?.xLabel}: {data.x}
                            </p>
                            <p className="font-medium">
                              {currentType?.yLabel}: {data.y}
                            </p>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                  <Scatter 
                    data={currentData} 
                    fill={currentType?.color}
                    strokeWidth={2}
                  />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <div className="space-y-4">
          {/* Correlation Strength */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Correlation Analysis</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Coefficient:</span>
                <span className="font-mono font-bold">{currentCorr.toFixed(3)}</span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Strength:</span>
                <Badge variant={corrStrength.color === 'green' ? 'default' : 'secondary'}>
                  {corrStrength.strength}
                </Badge>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Direction:</span>
                <div className="flex items-center gap-1">
                  {corrDirection.icon}
                  <span className="text-sm">{corrDirection.direction}</span>
                </div>
              </div>

              <div className="pt-2 border-t">
                <div className="text-xs text-gray-600 space-y-1">
                  <p><strong>Strong:</strong> ≥ 0.7</p>
                  <p><strong>Moderate:</strong> 0.4 - 0.7</p>
                  <p><strong>Weak:</strong> < 0.4</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Insights */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Zap className="h-5 w-5" />
                Insights
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm">
                {Math.abs(currentCorr) > 0.5 && (
                  <div className="p-3 bg-blue-50 rounded-lg">
                    <p className="text-blue-800">
                      <strong>Strong relationship detected!</strong> Your {currentType?.title.toLowerCase()} shows a significant correlation.
                    </p>
                  </div>
                )}
                
                {currentCorr > 0.3 && (
                  <div className="p-3 bg-green-50 rounded-lg">
                    <p className="text-green-800">
                      Positive trend: As one metric increases, the other tends to increase too.
                    </p>
                  </div>
                )}
                
                {currentCorr < -0.3 && (
                  <div className="p-3 bg-amber-50 rounded-lg">
                    <p className="text-amber-800">
                      Negative trend: As one metric increases, the other tends to decrease.
                    </p>
                  </div>
                )}
                
                {Math.abs(currentCorr) < 0.3 && (
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <p className="text-gray-700">
                      No strong correlation found. These metrics appear to be independent.
                    </p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Summary Statistics */}
      <Card>
        <CardHeader>
          <CardTitle>Correlation Matrix Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {Object.entries(correlationTypes).map(([key, type]) => {
              const data = correlationData[key] || [];
              const corr = calculateCorrelation(data);
              const strength = getCorrelationStrength(corr);
              
              return (
                <div key={key} className="p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    {type.icon}
                    <span className="font-medium text-sm">{type.title}</span>
                  </div>
                  <div className="space-y-1">
                    <div className="flex justify-between">
                      <span className="text-xs text-gray-600">r =</span>
                      <span className="font-mono text-xs">{corr.toFixed(3)}</span>
                    </div>
                    <Badge 
                      size="sm" 
                      variant={strength.color === 'green' ? 'default' : 'secondary'}
                    >
                      {strength.strength}
                    </Badge>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default HealthMetricsCorrelation;