import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  Calendar,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  Target,
  Zap,
  Moon,
  Heart,
  Activity,
  Apple,
  RefreshCw,
  BarChart3,
  CheckCircle2,
  XCircle,
  ArrowRight,
  Info
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
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Cell,
  PieChart,
  Pie
} from 'recharts';
import predictiveAnalyticsService from '../../services/predictiveAnalyticsService';

const WeeklyHealthDashboard = ({ userId = 'demo-patient-123', className = '' }) => {
  const [weeklyData, setWeeklyData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedWeeks, setSelectedWeeks] = useState(4);
  const [selectedPattern, setSelectedPattern] = useState('overview');

  useEffect(() => {
    fetchWeeklyPatterns();
  }, [userId, selectedWeeks]);

  const fetchWeeklyPatterns = async () => {
    try {
      setLoading(true);
      setError(null);

      const result = await predictiveAnalyticsService.getWeeklyHealthPatterns(userId, selectedWeeks);
      
      if (result.success) {
        setWeeklyData(result.data);
      } else {
        setError(result.error);
      }
    } catch (error) {
      console.error('Error fetching weekly patterns:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const getPatternScore = (score) => {
    if (score >= 8.5) return { color: 'text-green-600 bg-green-100', label: 'Excellent' };
    if (score >= 7.0) return { color: 'text-blue-600 bg-blue-100', label: 'Good' };
    if (score >= 5.5) return { color: 'text-yellow-600 bg-yellow-100', label: 'Fair' };
    return { color: 'text-red-600 bg-red-100', label: 'Needs Attention' };
  };

  const getTrendIcon = (direction) => {
    switch (direction) {
      case 'improving':
        return <TrendingUp className="h-4 w-4 text-green-600" />;
      case 'declining':
        return <TrendingDown className="h-4 w-4 text-red-600" />;
      default:
        return <Activity className="h-4 w-4 text-gray-600" />;
    }
  };

  const getAnomalySeverityColor = (severity) => {
    switch (severity) {
      case 'high':
        return 'border-l-red-500 bg-red-50';
      case 'moderate':
        return 'border-l-yellow-500 bg-yellow-50';
      case 'low':
        return 'border-l-blue-500 bg-blue-50';
      default:
        return 'border-l-gray-500 bg-gray-50';
    }
  };

  // Generate mock trend data for visualization
  const generateTrendData = () => {
    const weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
    return weeks.map(week => ({
      week,
      nutrition_consistency: Math.random() * 3 + 7,
      energy_patterns: Math.random() * 3 + 6,
      sleep_trends: Math.random() * 3 + 6.5,
      activity_levels: Math.random() * 3 + 6.5,
      mood_stability: Math.random() * 3 + 6.8
    }));
  };

  const trendData = generateTrendData();

  // Convert patterns object to array for radar chart
  const radarData = weeklyData?.patterns ? Object.entries(weeklyData.patterns).map(([key, value]) => ({
    pattern: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
    score: value,
    fullMark: 10
  })) : [];

  if (loading) {
    return (
      <div className={`space-y-6 ${className}`}>
        <Card>
          <CardContent className="p-6">
            <div className="animate-pulse space-y-4">
              <div className="h-6 bg-gray-200 rounded w-1/3"></div>
              <div className="grid grid-cols-2 gap-4">
                <div className="h-20 bg-gray-200 rounded"></div>
                <div className="h-20 bg-gray-200 rounded"></div>
              </div>
              <div className="h-64 bg-gray-200 rounded"></div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error) {
    return (
      <div className={className}>
        <Card>
          <CardContent className="p-6 text-center">
            <AlertTriangle className="h-8 w-8 text-red-500 mx-auto mb-4" />
            <p className="text-red-600 mb-4">Error loading weekly health patterns: {error}</p>
            <Button onClick={fetchWeeklyPatterns} variant="outline">
              <RefreshCw className="h-4 w-4 mr-2" />
              Try Again
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header Controls */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-6 w-6 text-indigo-600" />
                Weekly Health Pattern Analysis
              </CardTitle>
              <p className="text-gray-600">AI-powered insights into your health trends and patterns</p>
            </div>
            <div className="flex items-center gap-2">
              <select
                value={selectedWeeks}
                onChange={(e) => setSelectedWeeks(parseInt(e.target.value))}
                className="px-3 py-1 border border-gray-300 rounded-md text-sm"
              >
                <option value={2}>2 Weeks</option>
                <option value={4}>4 Weeks</option>
                <option value={8}>8 Weeks</option>
                <option value={12}>12 Weeks</option>
              </select>
              <Button
                variant="outline"
                size="sm"
                onClick={fetchWeeklyPatterns}
                disabled={loading}
              >
                <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
              </Button>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Overall Trend & Score */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 text-center">
            <div className="flex items-center justify-center gap-2 mb-2">
              {getTrendIcon(weeklyData?.trend_direction)}
              <span className="font-semibold text-lg">
                {weeklyData?.trend_direction || 'stable'}
              </span>
            </div>
            <p className="text-sm text-gray-600">Overall Trend</p>
            <Badge className="mt-2 bg-blue-100 text-blue-800">
              Confidence: {Math.round((weeklyData?.confidence || 0.8) * 100)}%
            </Badge>
          </CardContent>
        </Card>

        {weeklyData?.patterns && Object.entries(weeklyData.patterns).slice(0, 3).map(([key, value]) => {
          const patternInfo = getPatternScore(value);
          const icon = {
            nutrition_consistency: <Apple className="h-5 w-5" />,
            energy_patterns: <Zap className="h-5 w-5" />,
            sleep_trends: <Moon className="h-5 w-5" />,
            activity_levels: <Activity className="h-5 w-5" />,
            mood_stability: <Heart className="h-5 w-5" />
          }[key] || <BarChart3 className="h-5 w-5" />;

          return (
            <Card key={key}>
              <CardContent className="p-4 text-center">
                <div className="flex items-center justify-center mb-2">
                  {icon}
                </div>
                <div className={`text-lg font-bold ${patternInfo.color.split(' ')[0]} mb-1`}>
                  {value.toFixed(1)}/10
                </div>
                <p className="text-sm text-gray-600 capitalize">
                  {key.replace(/_/g, ' ')}
                </p>
                <Badge className={`text-xs mt-1 ${patternInfo.color}`}>
                  {patternInfo.label}
                </Badge>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Pattern Visualizations */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Radar Chart - Pattern Overview */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Health Pattern Overview</CardTitle>
            <p className="text-sm text-gray-600">Your health dimensions at a glance</p>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="pattern" className="text-xs" />
                  <PolarRadiusAxis 
                    angle={90} 
                    domain={[0, 10]} 
                    className="text-xs"
                    tick={false}
                  />
                  <Radar
                    name="Score"
                    dataKey="score"
                    stroke="#8884d8"
                    fill="#8884d8"
                    fillOpacity={0.3}
                    strokeWidth={2}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Trend Lines */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">4-Week Trend Analysis</CardTitle>
            <p className="text-sm text-gray-600">How your patterns evolved over time</p>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="week" />
                  <YAxis domain={[0, 10]} />
                  <Tooltip />
                  <Line 
                    type="monotone" 
                    dataKey="nutrition_consistency" 
                    stroke="#10b981" 
                    strokeWidth={2}
                    name="Nutrition"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="energy_patterns" 
                    stroke="#f59e0b" 
                    strokeWidth={2}
                    name="Energy"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="sleep_trends" 
                    stroke="#3b82f6" 
                    strokeWidth={2}
                    name="Sleep"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Insights and Anomalies */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Key Insights */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Target className="h-5 w-5 text-green-600" />
              Key Insights
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {weeklyData?.insights?.map((insight, idx) => (
                <div key={idx} className="flex items-start gap-3 p-3 bg-green-50 border-l-4 border-green-400 rounded-r-lg">
                  <CheckCircle2 className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                  <span className="text-sm text-green-800">{insight}</span>
                </div>
              )) || (
                <p className="text-gray-500 text-sm">No specific insights available for this period.</p>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Anomalies & Alerts */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-orange-600" />
              Anomalies Detected
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {weeklyData?.anomalies?.length > 0 ? (
                weeklyData.anomalies.map((anomaly, idx) => (
                  <div 
                    key={idx} 
                    className={`p-3 border-l-4 rounded-r-lg ${getAnomalySeverityColor(anomaly.severity)}`}
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="font-semibold text-sm capitalize">
                          {anomaly.type?.replace(/_/g, ' ')}
                        </div>
                        <p className="text-xs text-gray-600 mt-1">
                          {anomaly.description}
                        </p>
                        {anomaly.date && (
                          <Badge variant="outline" className="text-xs mt-2">
                            {new Date(anomaly.date).toLocaleDateString()}
                          </Badge>
                        )}
                      </div>
                      <Badge 
                        className={`text-xs ${
                          anomaly.severity === 'high' ? 'bg-red-100 text-red-800' :
                          anomaly.severity === 'moderate' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-blue-100 text-blue-800'
                        }`}
                      >
                        {anomaly.severity}
                      </Badge>
                    </div>
                  </div>
                ))
              ) : (
                <div className="flex items-center gap-2 p-3 bg-green-50 rounded-lg">
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                  <span className="text-sm text-green-800">No anomalies detected - great job!</span>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* AI Recommendations */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Target className="h-5 w-5 text-purple-600" />
            Actionable Recommendations
          </CardTitle>
          <p className="text-sm text-gray-600">
            Personalized suggestions based on your weekly health patterns
          </p>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-4">
            {weeklyData?.recommendations?.map((rec, idx) => (
              <div key={idx} className="p-4 border border-gray-200 rounded-lg hover:border-purple-200 transition-colors">
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-semibold text-sm">{rec.title || `Recommendation ${idx + 1}`}</h4>
                  <ArrowRight className="h-4 w-4 text-gray-400" />
                </div>
                <p className="text-sm text-gray-600 mb-3">{rec}</p>
                <div className="flex items-center gap-2">
                  <Badge variant="outline" className="text-xs">
                    Week {idx + 1} Focus
                  </Badge>
                </div>
              </div>
            )) || (
              <div className="col-span-2 text-center py-8 text-gray-500">
                <Info className="h-8 w-8 mx-auto mb-3 opacity-50" />
                <p className="text-sm">Continue your excellent health patterns!</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default WeeklyHealthDashboard;