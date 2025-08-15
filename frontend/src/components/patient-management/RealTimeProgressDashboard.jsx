import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { 
  TrendingUp, 
  Activity, 
  Heart, 
  Target, 
  AlertTriangle,
  Download,
  RefreshCw,
  Calendar,
  BarChart3,
  Loader2,
  AlertCircle,
  Trophy,
  Award,
  TrendingDown
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  RadialBarChart,
  RadialBar
} from 'recharts';
import SmartNavigation from '../shared/SmartNavigation';

const RealTimeProgressDashboard = () => {
  const [progressData, setProgressData] = useState([]);
  const [analyticsData, setAnalyticsData] = useState(null);
  const [selectedPatient, setSelectedPatient] = useState('patient-456');
  const [selectedTimeframe, setSelectedTimeframe] = useState('30_days');
  const [selectedMetric, setSelectedMetric] = useState('all');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [realTimeUpdates, setRealTimeUpdates] = useState(true);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;

  // Fetch progress data
  const fetchProgressData = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `${backendUrl}/api/provider/patient-management/progress/${selectedPatient}?metric_type=${selectedMetric}&days=${selectedTimeframe.split('_')[0]}`
      );
      if (response.ok) {
        const data = await response.json();
        setProgressData(data.progress_data || []);
      } else {
        throw new Error('Failed to fetch progress data');
      }
    } catch (err) {
      setError(`Error fetching progress: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Fetch comprehensive analytics
  const fetchAnalytics = async () => {
    try {
      const response = await fetch(
        `${backendUrl}/api/provider/patient-management/progress-analytics/${selectedPatient}?timeframe=${selectedTimeframe}`
      );
      if (response.ok) {
        const data = await response.json();
        setAnalyticsData(data);
      } else {
        throw new Error('Failed to fetch analytics');
      }
    } catch (err) {
      setError(`Error fetching analytics: ${err.message}`);
    }
  };

  // Record new progress
  const recordProgress = async (progressEntry) => {
    try {
      const response = await fetch(`${backendUrl}/api/provider/patient-management/progress`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_id: selectedPatient,
          provider_id: 'provider-123',
          ...progressEntry
        })
      });
      
      if (response.ok) {
        await fetchProgressData(); // Refresh data
        await fetchAnalytics();
      } else {
        throw new Error('Failed to record progress');
      }
    } catch (err) {
      setError(`Error recording progress: ${err.message}`);
    }
  };

  useEffect(() => {
    fetchProgressData();
    fetchAnalytics();
  }, [selectedPatient, selectedTimeframe, selectedMetric]);

  // Real-time update simulation
  useEffect(() => {
    if (!realTimeUpdates) return;
    
    const interval = setInterval(() => {
      fetchProgressData();
      fetchAnalytics();
    }, 30000); // Update every 30 seconds
    
    return () => clearInterval(interval);
  }, [realTimeUpdates, selectedPatient, selectedTimeframe, selectedMetric]);

  // Chart colors
  const COLORS = ['#10b981', '#f59e0b', '#ef4444', '#3b82f6', '#8b5cf6'];

  // Sample milestone data
  const milestones = [
    { name: 'Weight Loss Goal', progress: 75, target: 100, status: 'in_progress' },
    { name: 'Blood Pressure Control', progress: 90, target: 100, status: 'achieved' },
    { name: 'Exercise Routine', progress: 60, target: 100, status: 'in_progress' },
    { name: 'Medication Adherence', progress: 95, target: 100, status: 'achieved' }
  ];

  // Risk assessment data
  const riskAssessment = analyticsData?.risk_assessment || {
    overall_risk: 'LOW',
    risk_factors: ['Hypertension', 'Sedentary lifestyle'],
    confidence_score: 0.85,
    recommendations: ['Increase physical activity', 'Monitor blood pressure regularly']
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
              <TrendingUp className="h-8 w-8 text-emerald-600" />
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Real-Time Progress Dashboard</h1>
                <p className="text-gray-600">Live patient progress tracking with AI-powered analytics</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <div className={`w-3 h-3 rounded-full ${realTimeUpdates ? 'bg-green-500 animate-pulse' : 'bg-gray-400'}`} />
                <span className="text-sm text-gray-600">
                  {realTimeUpdates ? 'Live Updates' : 'Paused'}
                </span>
              </div>
              
              <Button
                variant="outline"
                onClick={() => setRealTimeUpdates(!realTimeUpdates)}
                className="border-emerald-300"
              >
                {realTimeUpdates ? 'Pause' : 'Resume'} Updates
              </Button>
              
              <Button
                onClick={() => {
                  fetchProgressData();
                  fetchAnalytics();
                }}
                disabled={loading}
                className="bg-emerald-600 hover:bg-emerald-700"
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <RefreshCw className="h-4 w-4" />}
              </Button>
            </div>
          </div>
        </div>

        {/* Controls */}
        <Card className="mb-6">
          <CardContent className="p-4">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-700">Patient</label>
                <Select value={selectedPatient} onValueChange={setSelectedPatient}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="patient-456">Patient 456 (Demo)</SelectItem>
                    <SelectItem value="patient-789">Patient 789</SelectItem>
                    <SelectItem value="patient-123">Patient 123</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <label className="text-sm font-medium text-gray-700">Timeframe</label>
                <Select value={selectedTimeframe} onValueChange={setSelectedTimeframe}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="7_days">Last 7 Days</SelectItem>
                    <SelectItem value="30_days">Last 30 Days</SelectItem>
                    <SelectItem value="90_days">Last 90 Days</SelectItem>
                    <SelectItem value="180_days">Last 6 Months</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <label className="text-sm font-medium text-gray-700">Metric Type</label>
                <Select value={selectedMetric} onValueChange={setSelectedMetric}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Metrics</SelectItem>
                    <SelectItem value="weight">Weight</SelectItem>
                    <SelectItem value="blood_pressure">Blood Pressure</SelectItem>
                    <SelectItem value="exercise">Exercise</SelectItem>
                    <SelectItem value="medication">Medication</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <Button className="self-end bg-emerald-600 hover:bg-emerald-700">
                <Download className="h-4 w-4 mr-2" />
                Export Report
              </Button>
            </div>
          </CardContent>
        </Card>

        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 bg-white">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="trends">Trends</TabsTrigger>
            <TabsTrigger value="milestones">Milestones</TabsTrigger>
            <TabsTrigger value="predictions">Predictions</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">Overall Progress</p>
                      <p className="text-2xl font-bold text-emerald-600">
                        {analyticsData?.overall_progress || 78}%
                      </p>
                    </div>
                    <TrendingUp className="h-8 w-8 text-emerald-600" />
                  </div>
                  <div className="mt-4">
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-emerald-600 h-2 rounded-full"
                        style={{ width: `${analyticsData?.overall_progress || 78}%` }}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">Active Goals</p>
                      <p className="text-2xl font-bold text-blue-600">
                        {analyticsData?.active_goals || 4}
                      </p>
                    </div>
                    <Target className="h-8 w-8 text-blue-600" />
                  </div>
                  <p className="text-sm text-gray-600 mt-2">
                    {analyticsData?.completed_goals || 2} completed this month
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">Risk Level</p>
                      <p className={`text-2xl font-bold ${
                        riskAssessment.overall_risk === 'LOW' ? 'text-green-600' :
                        riskAssessment.overall_risk === 'MEDIUM' ? 'text-yellow-600' : 'text-red-600'
                      }`}>
                        {riskAssessment.overall_risk}
                      </p>
                    </div>
                    <AlertTriangle className={`h-8 w-8 ${
                      riskAssessment.overall_risk === 'LOW' ? 'text-green-600' :
                      riskAssessment.overall_risk === 'MEDIUM' ? 'text-yellow-600' : 'text-red-600'
                    }`} />
                  </div>
                  <p className="text-sm text-gray-600 mt-2">
                    Confidence: {(riskAssessment.confidence_score * 100).toFixed(0)}%
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">Adherence Rate</p>
                      <p className="text-2xl font-bold text-purple-600">
                        {analyticsData?.adherence_rate || 92}%
                      </p>
                    </div>
                    <Heart className="h-8 w-8 text-purple-600" />
                  </div>
                  <p className="text-sm text-gray-600 mt-2">
                    +5% from last month
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Main Progress Chart */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="h-5 w-5" />
                  Progress Overview
                </CardTitle>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="flex justify-center items-center h-64">
                    <Loader2 className="h-8 w-8 animate-spin text-emerald-600" />
                    <span className="ml-2">Loading chart data...</span>
                  </div>
                ) : (
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={progressData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Line 
                        type="monotone" 
                        dataKey="progress_score" 
                        stroke="#10b981" 
                        strokeWidth={3}
                        name="Progress Score"
                      />
                      <Line 
                        type="monotone" 
                        dataKey="target_score" 
                        stroke="#ef4444" 
                        strokeWidth={2}
                        strokeDasharray="5 5"
                        name="Target"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Trends Tab */}
          <TabsContent value="trends" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Metric Trends */}
              <Card>
                <CardHeader>
                  <CardTitle>Metric Trends</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={250}>
                    <AreaChart data={progressData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Area 
                        type="monotone" 
                        dataKey="weight" 
                        stackId="1"
                        stroke="#3b82f6" 
                        fill="#3b82f6" 
                        fillOpacity={0.6}
                      />
                      <Area 
                        type="monotone" 
                        dataKey="exercise_minutes" 
                        stackId="1"
                        stroke="#10b981" 
                        fill="#10b981" 
                        fillOpacity={0.6}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Progress Distribution */}
              <Card>
                <CardHeader>
                  <CardTitle>Progress Distribution</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={250}>
                    <PieChart>
                      <Pie
                        data={[
                          { name: 'Completed', value: 60, fill: '#10b981' },
                          { name: 'In Progress', value: 25, fill: '#f59e0b' },
                          { name: 'Pending', value: 15, fill: '#ef4444' }
                        ]}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {COLORS.map((color, index) => (
                          <Cell key={`cell-${index}`} fill={color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>

            {/* Weekly Comparison */}
            <Card>
              <CardHeader>
                <CardTitle>Weekly Performance Comparison</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={progressData.slice(-7)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="daily_progress" fill="#10b981" name="Daily Progress" />
                    <Bar dataKey="daily_target" fill="#ef4444" name="Daily Target" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Milestones Tab */}
          <TabsContent value="milestones" className="space-y-6">
            <div className="grid gap-6">
              {milestones.map((milestone, index) => (
                <Card key={index} className={`border-l-4 ${
                  milestone.status === 'achieved' ? 'border-green-500' : 'border-yellow-500'
                }`}>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-3">
                        {milestone.status === 'achieved' ? (
                          <Trophy className="h-6 w-6 text-yellow-500" />
                        ) : (
                          <Target className="h-6 w-6 text-emerald-600" />
                        )}
                        <div>
                          <h3 className="text-lg font-semibold">{milestone.name}</h3>
                          <Badge className={milestone.status === 'achieved' ? 
                            'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                          }>
                            {milestone.status === 'achieved' ? 'Achieved' : 'In Progress'}
                          </Badge>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-2xl font-bold text-emerald-600">
                          {milestone.progress}%
                        </p>
                        <p className="text-sm text-gray-600">of {milestone.target}%</p>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Progress</span>
                        <span>{milestone.progress}% / {milestone.target}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div 
                          className={`h-3 rounded-full ${
                            milestone.status === 'achieved' ? 'bg-green-600' : 'bg-emerald-600'
                          }`}
                          style={{ width: `${milestone.progress}%` }}
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* Predictions Tab */}
          <TabsContent value="predictions" className="space-y-6">
            {/* Risk Assessment */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5" />
                  AI Risk Assessment
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-semibold mb-3">Risk Factors</h4>
                    <div className="space-y-2">
                      {riskAssessment.risk_factors.map((factor, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
                          <span>{factor}</span>
                          <Badge className="bg-yellow-100 text-yellow-800">Medium</Badge>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold mb-3">AI Recommendations</h4>
                    <div className="space-y-2">
                      {riskAssessment.recommendations.map((rec, index) => (
                        <div key={index} className="flex items-start gap-3 p-3 bg-emerald-50 rounded-lg">
                          <Award className="h-5 w-5 text-emerald-600 mt-0.5" />
                          <span className="text-sm">{rec}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Predictive Chart */}
            <Card>
              <CardHeader>
                <CardTitle>Predictive Insights</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={[
                    ...progressData,
                    ...Array.from({ length: 7 }, (_, i) => ({
                      date: `Pred ${i + 1}`,
                      progress_score: 78 + (i * 2),
                      predicted: true
                    }))
                  ]}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Line 
                      type="monotone" 
                      dataKey="progress_score" 
                      stroke="#10b981" 
                      strokeWidth={3}
                      name="Current Progress"
                    />
                    <Line 
                      type="monotone" 
                      dataKey="predicted" 
                      stroke="#3b82f6" 
                      strokeWidth={2}
                      strokeDasharray="5 5"
                      name="Predicted"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default RealTimeProgressDashboard;