import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ScatterChart, Scatter, BarChart, Bar } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { 
  BarChart3, TrendingUp, TrendingDown, Zap, 
  Target, Activity, Brain, Link2, AlertCircle,
  CheckCircle2, ArrowRight, Sparkles
} from 'lucide-react';

const GoalCorrelation = ({ goals = [], achievements = [] }) => {
  const [correlationData, setCorrelationData] = useState({});
  const [selectedCorrelation, setSelectedCorrelation] = useState('fitness-nutrition');
  const [timeRange, setTimeRange] = useState('7days');
  const [insights, setInsights] = useState([]);

  useEffect(() => {
    generateCorrelationData();
  }, [goals, achievements, timeRange]);

  const generateCorrelationData = () => {
    // Generate mock correlation data - in production, this would analyze real data
    const correlations = {
      'fitness-nutrition': {
        name: 'Fitness ↔ Nutrition Goals',
        correlation: 0.73,
        strength: 'strong',
        direction: 'positive',
        data: [
          { day: 'Day 1', fitness: 2, nutrition: 6.5, combined: 8.5 },
          { day: 'Day 2', fitness: 3, nutrition: 7.2, combined: 10.2 },
          { day: 'Day 3', fitness: 1, nutrition: 5.8, combined: 6.8 },
          { day: 'Day 4', fitness: 4, nutrition: 8.1, combined: 12.1 },
          { day: 'Day 5', fitness: 3, nutrition: 7.5, combined: 10.5 },
          { day: 'Day 6', fitness: 2, nutrition: 6.8, combined: 8.8 },
          { day: 'Day 7', fitness: 3, nutrition: 7.2, combined: 10.2 }
        ],
        insights: [
          'Higher workout intensity correlates with better nutrition choices',
          'Rest days show 15% decrease in nutrition goal adherence',
          'Morning workouts lead to 23% better daily nutrition compliance'
        ]
      },
      'fitness-wellness': {
        name: 'Fitness ↔ Wellness Goals',
        correlation: 0.68,
        strength: 'moderate',
        direction: 'positive',
        data: [
          { day: 'Day 1', fitness: 2, wellness: 7.1, combined: 9.1 },
          { day: 'Day 2', fitness: 3, wellness: 7.8, combined: 10.8 },
          { day: 'Day 3', fitness: 1, wellness: 6.2, combined: 7.2 },
          { day: 'Day 4', fitness: 4, wellness: 8.3, combined: 12.3 },
          { day: 'Day 5', fitness: 3, wellness: 7.9, combined: 10.9 },
          { day: 'Day 6', fitness: 2, wellness: 7.2, combined: 9.2 },
          { day: 'Day 7', fitness: 3, wellness: 7.7, combined: 10.7 }
        ],
        insights: [
          'Exercise positively impacts sleep quality scores',
          'Consistent workouts improve stress management ratings',
          'Recovery days still maintain wellness momentum'
        ]
      },
      'nutrition-wellness': {
        name: 'Nutrition ↔ Wellness Goals',
        correlation: 0.59,
        strength: 'moderate',
        direction: 'positive',
        data: [
          { day: 'Day 1', nutrition: 6.5, wellness: 7.1, combined: 13.6 },
          { day: 'Day 2', nutrition: 7.2, wellness: 7.8, combined: 15.0 },
          { day: 'Day 3', nutrition: 5.8, wellness: 6.2, combined: 12.0 },
          { day: 'Day 4', nutrition: 8.1, wellness: 8.3, combined: 16.4 },
          { day: 'Day 5', nutrition: 7.5, wellness: 7.9, combined: 15.4 },
          { day: 'Day 6', nutrition: 6.8, wellness: 7.2, combined: 14.0 },
          { day: 'Day 7', nutrition: 7.2, wellness: 7.7, combined: 14.9 }
        ],
        insights: [
          'Better hydration correlates with improved sleep quality',
          'Consistent meal timing supports circadian rhythm',
          'Nutrient-dense meals boost energy levels throughout day'
        ]
      }
    };

    setCorrelationData(correlations);

    // Generate overall insights
    const overallInsights = [
      {
        id: 'insight_1',
        type: 'positive',
        title: 'Synergistic Goal Achievement',
        description: 'Your fitness and nutrition goals show strong positive correlation (73%), suggesting they reinforce each other.',
        impact: 'high',
        actionable: true,
        recommendation: 'Continue pairing workout days with nutrition focus for maximum benefit.'
      },
      {
        id: 'insight_2',
        type: 'opportunity',
        title: 'Wellness Integration Opportunity',
        description: 'Moderate correlations suggest room for improvement in connecting wellness practices with other goals.',
        impact: 'medium',
        actionable: true,
        recommendation: 'Try scheduling meditation right after workouts to strengthen the connection.'
      },
      {
        id: 'insight_3',
        type: 'pattern',
        title: 'Compound Effect Detected',
        description: 'Days with progress on 2+ goals show 40% higher satisfaction scores.',
        impact: 'high',
        actionable: false,
        recommendation: 'Focus on achieving at least 2 goals daily for optimal motivation.'
      }
    ];

    setInsights(overallInsights);
  };

  const getCorrelationStrength = (value) => {
    const abs = Math.abs(value);
    if (abs >= 0.7) return { strength: 'Strong', color: 'text-green-600', bgColor: 'bg-green-100' };
    if (abs >= 0.5) return { strength: 'Moderate', color: 'text-yellow-600', bgColor: 'bg-yellow-100' };
    if (abs >= 0.3) return { strength: 'Weak', color: 'text-orange-600', bgColor: 'bg-orange-100' };
    return { strength: 'Very Weak', color: 'text-red-600', bgColor: 'bg-red-100' };
  };

  const currentData = correlationData[selectedCorrelation];

  const CorrelationChart = () => {
    if (!currentData) return null;

    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Link2 className="w-5 h-5 text-blue-600" />
            Correlation Analysis: {currentData.name}
          </CardTitle>
          <div className="flex items-center gap-4">
            <Badge className={`${getCorrelationStrength(currentData.correlation).bgColor} ${getCorrelationStrength(currentData.correlation).color} border-0`}>
              {getCorrelationStrength(currentData.correlation).strength} ({currentData.correlation > 0 ? '+' : ''}{currentData.correlation.toFixed(2)})
            </Badge>
            <span className="text-sm text-gray-500">
              {currentData.direction === 'positive' ? 'Goals reinforce each other' : 'Goals compete for resources'}
            </span>
          </div>
        </CardHeader>
        <CardContent>
          <div className="h-80 mb-6">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={currentData.data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Line 
                  type="monotone" 
                  dataKey="fitness" 
                  stroke="#3b82f6" 
                  strokeWidth={2}
                  dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
                  name="Fitness Progress"
                />
                <Line 
                  type="monotone" 
                  dataKey="nutrition" 
                  stroke="#10b981" 
                  strokeWidth={2}
                  dot={{ fill: '#10b981', strokeWidth: 2, r: 4 }}
                  name="Nutrition Progress"
                />
                <Line 
                  type="monotone" 
                  dataKey="wellness" 
                  stroke="#8b5cf6" 
                  strokeWidth={2}
                  dot={{ fill: '#8b5cf6', strokeWidth: 2, r: 4 }}
                  name="Wellness Progress"
                />
                <Line 
                  type="monotone" 
                  dataKey="combined" 
                  stroke="#f59e0b" 
                  strokeWidth={3}
                  strokeDasharray="5 5"
                  dot={{ fill: '#f59e0b', strokeWidth: 2, r: 3 }}
                  name="Combined Score"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="space-y-3">
            <h4 className="font-semibold text-gray-900 flex items-center gap-2">
              <Brain className="w-4 h-4 text-purple-600" />
              Key Insights
            </h4>
            {currentData.insights.map((insight, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg"
              >
                <CheckCircle2 className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-gray-700">{insight}</p>
              </motion.div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  };

  const InsightCard = ({ insight, index }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
    >
      <Card className="hover:shadow-lg transition-shadow duration-300">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className={`p-2 rounded-lg ${
                insight.type === 'positive' ? 'bg-green-100 text-green-600' :
                insight.type === 'opportunity' ? 'bg-yellow-100 text-yellow-600' :
                'bg-blue-100 text-blue-600'
              }`}>
                {insight.type === 'positive' ? <TrendingUp className="w-5 h-5" /> :
                 insight.type === 'opportunity' ? <Target className="w-5 h-5" /> :
                 <BarChart3 className="w-5 h-5" />}
              </div>
              <div>
                <CardTitle className="text-lg">{insight.title}</CardTitle>
                <Badge variant={insight.impact === 'high' ? 'destructive' : 'secondary'} className="mt-1">
                  {insight.impact.toUpperCase()} IMPACT
                </Badge>
              </div>
            </div>
            {insight.actionable && (
              <div className="flex items-center gap-1 text-sm text-blue-600">
                <Sparkles className="w-4 h-4" />
                <span>Actionable</span>
              </div>
            )}
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-gray-600 mb-4">{insight.description}</p>
          {insight.recommendation && (
            <div className="bg-gray-50 rounded-lg p-3">
              <div className="flex items-start gap-2">
                <ArrowRight className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-gray-700">{insight.recommendation}</p>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );

  const CorrelationMatrix = () => {
    const matrixData = [
      { goals: 'Fitness & Nutrition', correlation: 0.73, strength: 'strong' },
      { goals: 'Fitness & Wellness', correlation: 0.68, strength: 'moderate' },
      { goals: 'Nutrition & Wellness', correlation: 0.59, strength: 'moderate' }
    ];

    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-purple-600" />
            Goal Correlation Matrix
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={matrixData} margin={{ left: 20, right: 20 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="goals" 
                  angle={-45}
                  textAnchor="end" 
                  height={80}
                  fontSize={12}
                />
                <YAxis domain={[0, 1]} />
                <Tooltip />
                <Bar 
                  dataKey="correlation" 
                  fill="#8884d8"
                  radius={[4, 4, 0, 0]}
                >
                  {matrixData.map((entry, index) => (
                    <motion.rect
                      key={index}
                      initial={{ height: 0 }}
                      animate={{ height: entry.correlation * 200 }}
                      transition={{ delay: index * 0.2, duration: 0.5 }}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header and Controls */}
      <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Link2 className="w-8 h-8 text-blue-600" />
            Goal Correlations
          </h2>
          <p className="text-gray-600">
            Discover how your health goals influence each other
          </p>
        </div>
        
        <div className="flex gap-2">
          <Select value={selectedCorrelation} onValueChange={setSelectedCorrelation}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Select correlation" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="fitness-nutrition">Fitness ↔ Nutrition</SelectItem>
              <SelectItem value="fitness-wellness">Fitness ↔ Wellness</SelectItem>
              <SelectItem value="nutrition-wellness">Nutrition ↔ Wellness</SelectItem>
            </SelectContent>
          </Select>
          
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-32">
              <SelectValue placeholder="Time range" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7days">7 Days</SelectItem>
              <SelectItem value="30days">30 Days</SelectItem>
              <SelectItem value="90days">90 Days</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Correlation Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center">
                <TrendingUp className="w-8 h-8 text-green-600 mr-3" />
                <div>
                  <p className="text-sm text-gray-500">Strongest Correlation</p>
                  <p className="text-lg font-bold text-gray-900">Fitness ↔ Nutrition</p>
                  <p className="text-sm text-green-600">+0.73 (Strong)</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center">
                <Zap className="w-8 h-8 text-yellow-600 mr-3" />
                <div>
                  <p className="text-sm text-gray-500">Synergy Score</p>
                  <p className="text-lg font-bold text-gray-900">8.4/10</p>
                  <p className="text-sm text-yellow-600">Excellent</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center">
                <Target className="w-8 h-8 text-blue-600 mr-3" />
                <div>
                  <p className="text-sm text-gray-500">Compound Days</p>
                  <p className="text-lg font-bold text-gray-900">5/7</p>
                  <p className="text-sm text-blue-600">Multi-goal success</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Main Correlation Chart */}
      <CorrelationChart />

      {/* Correlation Matrix */}
      <CorrelationMatrix />

      {/* Insights */}
      <div>
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Correlation Insights ({insights.length})
        </h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {insights.map((insight, index) => (
            <InsightCard
              key={insight.id}
              insight={insight}
              index={index}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default GoalCorrelation;