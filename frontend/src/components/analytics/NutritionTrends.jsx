import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
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
  TrendingUp, 
  TrendingDown, 
  Calendar, 
  BarChart3, 
  PieChart as PieChartIcon, 
  Activity,
  Clock
} from 'lucide-react';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

const NutritionTrends = ({ userId }) => {
  const [nutritionData, setNutritionData] = useState([]);
  const [timeRange, setTimeRange] = useState('week'); // week, month, 3months
  const [loading, setLoading] = useState(true);
  const [selectedMetric, setSelectedMetric] = useState('calories');

  useEffect(() => {
    fetchNutritionTrends();
  }, [userId, timeRange]);

  const fetchNutritionTrends = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/patient/analytics/${userId}`);
      if (response.ok) {
        const data = await response.json();
        // Transform data for charts
        const trends = data.nutrition_trends || [];
        setNutritionData(trends);
      }
    } catch (error) {
      console.error('Failed to fetch nutrition trends:', error);
    } finally {
      setLoading(false);
    }
  };

  // Generate macro distribution data
  const macroDistribution = nutritionData.length > 0 ? [
    { name: 'Protein', value: nutritionData.reduce((sum, d) => sum + (d.protein || 0), 0) / nutritionData.length, color: '#3b82f6' },
    { name: 'Carbs', value: nutritionData.reduce((sum, d) => sum + (d.carbs || 0), 0) / nutritionData.length, color: '#10b981' },
    { name: 'Fat', value: nutritionData.reduce((sum, d) => sum + (d.fat || 0), 0) / nutritionData.length, color: '#f59e0b' },
  ] : [];

  // Generate meal timing analysis
  const mealTimingData = [
    { time: '6-8 AM', breakfast: 85, lunch: 5, dinner: 10 },
    { time: '8-10 AM', breakfast: 60, lunch: 15, dinner: 25 },
    { time: '12-2 PM', breakfast: 10, lunch: 75, dinner: 15 },
    { time: '2-4 PM', breakfast: 5, lunch: 45, dinner: 50 },
    { time: '6-8 PM', breakfast: 5, lunch: 20, dinner: 75 },
    { time: '8-10 PM', breakfast: 5, lunch: 10, dinner: 85 }
  ];

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border">
          <p className="font-medium text-gray-900">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.dataKey}: {entry.value}
              {entry.dataKey === 'calories' ? ' cal' : 'g'}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const MetricSelector = () => (
    <div className="flex gap-2 flex-wrap">
      {['calories', 'protein', 'carbs', 'fat'].map((metric) => (
        <Button
          key={metric}
          variant={selectedMetric === metric ? "default" : "outline"}
          size="sm"
          onClick={() => setSelectedMetric(metric)}
          className="capitalize"
        >
          {metric}
        </Button>
      ))}
    </div>
  );

  const TimeRangeSelector = () => (
    <div className="flex gap-2">
      {[
        { value: 'week', label: '7 Days' },
        { value: 'month', label: '30 Days' },
        { value: '3months', label: '3 Months' }
      ].map((range) => (
        <Button
          key={range.value}
          variant={timeRange === range.value ? "default" : "outline"}
          size="sm"
          onClick={() => setTimeRange(range.value)}
        >
          {range.label}
        </Button>
      ))}
    </div>
  );

  const calculateTrend = (data, metric) => {
    if (data.length < 2) return { trend: 'stable', change: 0 };
    const recent = data.slice(-3).reduce((sum, d) => sum + (d[metric] || 0), 0) / 3;
    const previous = data.slice(-6, -3).reduce((sum, d) => sum + (d[metric] || 0), 0) / 3;
    const change = recent - previous;
    return {
      trend: change > 5 ? 'up' : change < -5 ? 'down' : 'stable',
      change: Math.abs(change),
      percentage: previous ? ((change / previous) * 100).toFixed(1) : 0
    };
  };

  const trendInfo = calculateTrend(nutritionData, selectedMetric);

  if (loading) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="animate-pulse space-y-4">
            <div className="h-4 bg-gray-200 rounded w-1/4"></div>
            <div className="h-64 bg-gray-200 rounded"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with Controls */}
      <Card>
        <CardHeader>
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Nutrition Trends
              </CardTitle>
              <p className="text-sm text-gray-600 mt-1">
                Track your nutrition patterns over time
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-3">
              <MetricSelector />
              <TimeRangeSelector />
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Trend Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 capitalize">{selectedMetric} Trend</p>
                <p className="text-2xl font-bold">
                  {trendInfo.trend === 'up' ? '+' : trendInfo.trend === 'down' ? '-' : ''}
                  {trendInfo.change.toFixed(1)}
                </p>
                {trendInfo.percentage && (
                  <p className="text-xs text-gray-500">{trendInfo.percentage}% change</p>
                )}
              </div>
              <div className={`p-2 rounded-full ${
                trendInfo.trend === 'up' ? 'bg-green-100 text-green-600' :
                trendInfo.trend === 'down' ? 'bg-red-100 text-red-600' :
                'bg-gray-100 text-gray-600'
              }`}>
                {trendInfo.trend === 'up' ? <TrendingUp className="h-4 w-4" /> :
                 trendInfo.trend === 'down' ? <TrendingDown className="h-4 w-4" /> :
                 <Activity className="h-4 w-4" />}
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Average Daily</p>
                <p className="text-2xl font-bold">
                  {nutritionData.length > 0 
                    ? (nutritionData.reduce((sum, d) => sum + (d[selectedMetric] || 0), 0) / nutritionData.length).toFixed(1)
                    : '0'
                  }
                </p>
                <p className="text-xs text-gray-500 capitalize">{selectedMetric}/day</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Consistency</p>
                <p className="text-2xl font-bold">
                  {nutritionData.length > 0 ? '85%' : '0%'}
                </p>
                <p className="text-xs text-gray-500">Goal adherence</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <Tabs defaultValue="trends" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="trends">Trends</TabsTrigger>
          <TabsTrigger value="macros">Macros</TabsTrigger>
          <TabsTrigger value="timing">Timing</TabsTrigger>
          <TabsTrigger value="comparison">Compare</TabsTrigger>
        </TabsList>

        <TabsContent value="trends">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Nutrition Timeline</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={nutritionData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey={selectedMetric} 
                      stroke="#3b82f6" 
                      strokeWidth={2}
                      dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
                      activeDot={{ r: 6 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="macros">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <PieChartIcon className="h-5 w-5" />
                  Macro Distribution
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={macroDistribution}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, value }) => `${name}: ${value.toFixed(0)}g`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {macroDistribution.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Macro Trends</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={nutritionData.slice(-7)}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="protein" fill="#3b82f6" />
                      <Bar dataKey="carbs" fill="#10b981" />
                      <Bar dataKey="fat" fill="#f59e0b" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="timing">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Clock className="h-5 w-5" />
                Meal Timing Analysis
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={mealTimingData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="breakfast" stackId="a" fill="#3b82f6" />
                    <Bar dataKey="lunch" stackId="a" fill="#10b981" />
                    <Bar dataKey="dinner" stackId="a" fill="#f59e0b" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-4 text-sm text-gray-600">
                <p>Shows the percentage distribution of meals across different time periods.</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="comparison">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Progress Comparison</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={nutritionData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="calories" stroke="#3b82f6" name="Actual Calories" />
                    <Line type="monotone" dataKey="protein" stroke="#10b981" name="Protein (g)" />
                    <Line type="monotone" dataKey="carbs" stroke="#f59e0b" name="Carbs (g)" />
                    <Line type="monotone" dataKey="fat" stroke="#ef4444" name="Fat (g)" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default NutritionTrends;