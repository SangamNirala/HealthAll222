import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Input } from '../ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Progress } from '../ui/progress';
import { 
  Activity, 
  AlertTriangle, 
  Brain, 
  Calendar, 
  Clock, 
  Heart,
  TrendingUp,
  TrendingDown,
  Target,
  Bell,
  CheckCircle,
  XCircle,
  Users,
  Loader2,
  Filter,
  Search,
  BarChart3,
  Settings,
  Zap,
  Shield
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts';
import SmartNavigation from '../shared/SmartNavigation';

const AdvancedAdherenceMonitor = () => {
  const [adherenceData, setAdherenceData] = useState(null);
  const [patientList, setPatientList] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState('patient-456');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Filters and settings
  const [timeframe, setTimeframe] = useState('30');
  const [adherenceType, setAdherenceType] = useState('ALL');
  const [riskLevel, setRiskLevel] = useState('ALL');

  const providerId = 'provider-123';
  const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;

  // Fetch adherence data for selected patient
  const fetchAdherenceData = async (patientId = selectedPatient) => {
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/provider/patient-management/adherence/${patientId}`);
      if (response.ok) {
        const data = await response.json();
        setAdherenceData(data);
      } else {
        throw new Error('Failed to fetch adherence data');
      }
    } catch (err) {
      setError(`Error fetching adherence data: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Create adherence monitoring for patient
  const createAdherenceMonitoring = async (patientId, monitoringConfig) => {
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/provider/patient-management/adherence`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          provider_id: providerId,
          patient_id: patientId,
          monitoring_config: monitoringConfig,
          alert_thresholds: {
            low_adherence: 0.7,
            critical_adherence: 0.5,
            missed_doses: 3
          }
        })
      });
      
      if (response.ok) {
        await fetchAdherenceData(patientId);
      } else {
        throw new Error('Failed to create adherence monitoring');
      }
    } catch (err) {
      setError(`Error creating monitoring: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedPatient) {
      fetchAdherenceData(selectedPatient);
    }
  }, [selectedPatient]);

  // Sample data for demo purposes
  const sampleAdherenceData = {
    overall_adherence: 0.78,
    risk_score: 0.35,
    confidence_level: 0.82,
    adherence_types: {
      medication: { percentage: 0.85, trend: 'improving' },
      diet: { percentage: 0.72, trend: 'stable' },
      exercise: { percentage: 0.65, trend: 'declining' },
      appointments: { percentage: 0.90, trend: 'improving' }
    },
    trend_data: [
      { date: '2024-01-01', adherence: 0.65, medication: 0.70, diet: 0.60, exercise: 0.55 },
      { date: '2024-01-08', adherence: 0.72, medication: 0.75, diet: 0.68, exercise: 0.60 },
      { date: '2024-01-15', adherence: 0.75, medication: 0.80, diet: 0.70, exercise: 0.62 },
      { date: '2024-01-22', adherence: 0.78, medication: 0.85, diet: 0.72, exercise: 0.65 },
      { date: '2024-01-29', adherence: 0.82, medication: 0.88, diet: 0.75, exercise: 0.68 }
    ],
    barriers: [
      { barrier: 'Forgets to take medication', frequency: 0.4, severity: 'high', solution: 'Set up smart reminders' },
      { barrier: 'Busy schedule conflicts', frequency: 0.3, severity: 'medium', solution: 'Flexible scheduling options' },
      { barrier: 'Side effects concerns', frequency: 0.2, severity: 'high', solution: 'Provider consultation needed' }
    ],
    interventions: [
      { strategy: 'Daily reminder notifications', priority: 'HIGH', effectiveness: 0.85, timeline: '1-2 weeks' },
      { strategy: 'Weekly check-in calls', priority: 'MEDIUM', effectiveness: 0.72, timeline: '2-4 weeks' },
      { strategy: 'Medication timing adjustment', priority: 'HIGH', effectiveness: 0.78, timeline: '1 week' }
    ],
    population_comparison: {
      patient_percentile: 65,
      similar_conditions: 0.74,
      age_group: 0.76,
      overall_average: 0.72
    }
  };

  const displayData = adherenceData || sampleAdherenceData;

  // Add safety checks for nested objects
  const safeDisplayData = {
    overall_adherence: displayData?.overall_adherence || 0.78,
    risk_score: displayData?.risk_score || 0.35,
    confidence_level: displayData?.confidence_level || 0.82,
    adherence_types: {
      medication: displayData?.adherence_types?.medication || { percentage: 0.85, trend: 'improving' },
      diet: displayData?.adherence_types?.diet || { percentage: 0.72, trend: 'stable' },
      exercise: displayData?.adherence_types?.exercise || { percentage: 0.65, trend: 'declining' },
      appointments: displayData?.adherence_types?.appointments || { percentage: 0.90, trend: 'improving' }
    },
    trend_data: displayData?.trend_data || sampleAdherenceData.trend_data,
    barriers: displayData?.barriers || sampleAdherenceData.barriers,
    interventions: displayData?.interventions || sampleAdherenceData.interventions,
    population_comparison: displayData?.population_comparison || sampleAdherenceData.population_comparison
  };

  const getRiskColor = (risk) => {
    if (risk < 0.3) return 'text-green-600 bg-green-100';
    if (risk < 0.6) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'improving': return <TrendingUp className="h-4 w-4 text-green-600" />;
      case 'declining': return <TrendingDown className="h-4 w-4 text-red-600" />;
      default: return <Activity className="h-4 w-4 text-blue-600" />;
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'HIGH': return 'bg-red-100 text-red-800';
      case 'MEDIUM': return 'bg-yellow-100 text-yellow-800';
      case 'LOW': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
        <SmartNavigation />
        <div className="container mx-auto px-4 py-8">
          <Card className="max-w-md mx-auto">
            <CardContent className="p-6 text-center">
              <AlertTriangle className="mx-auto mb-4 h-12 w-12 text-red-500" />
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
          <div className="flex items-center gap-3 mb-4">
            <Activity className="h-8 w-8 text-emerald-600" />
            <h1 className="text-3xl font-bold text-gray-900">Advanced Adherence Monitor</h1>
          </div>
          <p className="text-gray-600 text-lg">
            Smart compliance tracking with predictive analytics and intervention recommendations
          </p>
        </div>

        {/* Patient Selection and Controls */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="h-5 w-5" />
              Patient Selection & Filters
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Select value={selectedPatient} onValueChange={setSelectedPatient}>
                <SelectTrigger>
                  <SelectValue placeholder="Select Patient" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="patient-456">John Doe (456)</SelectItem>
                  <SelectItem value="patient-789">Jane Smith (789)</SelectItem>
                  <SelectItem value="patient-012">Bob Johnson (012)</SelectItem>
                </SelectContent>
              </Select>
              
              <Select value={timeframe} onValueChange={setTimeframe}>
                <SelectTrigger>
                  <SelectValue placeholder="Timeframe" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="7">Last 7 Days</SelectItem>
                  <SelectItem value="30">Last 30 Days</SelectItem>
                  <SelectItem value="90">Last 90 Days</SelectItem>
                </SelectContent>
              </Select>
              
              <Select value={adherenceType} onValueChange={setAdherenceType}>
                <SelectTrigger>
                  <SelectValue placeholder="Adherence Type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="ALL">All Types</SelectItem>
                  <SelectItem value="medication">Medication</SelectItem>
                  <SelectItem value="diet">Diet</SelectItem>
                  <SelectItem value="exercise">Exercise</SelectItem>
                  <SelectItem value="appointments">Appointments</SelectItem>
                </SelectContent>
              </Select>
              
              <Button 
                onClick={() => fetchAdherenceData(selectedPatient)} 
                disabled={loading}
                className="bg-emerald-600 hover:bg-emerald-700"
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Refresh'}
              </Button>
            </div>
          </CardContent>
        </Card>

        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-5 bg-white">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="trends">Trends</TabsTrigger>
            <TabsTrigger value="interventions">Interventions</TabsTrigger>
            <TabsTrigger value="barriers">Barriers</TabsTrigger>
            <TabsTrigger value="comparison">Comparison</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            {/* Key Metrics */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
              {/* Overall Adherence */}
              <Card>
                <CardHeader className="pb-4">
                  <CardTitle className="text-sm font-medium">Overall Adherence</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-center mb-4">
                    <div className="relative w-20 h-20">
                      <svg className="w-20 h-20 transform -rotate-90" viewBox="0 0 100 100">
                        <circle
                          cx="50"
                          cy="50"
                          r="40"
                          stroke="currentColor"
                          strokeWidth="10"
                          fill="transparent"
                          className="text-gray-300"
                        />
                        <circle
                          cx="50"
                          cy="50"
                          r="40"
                          stroke="currentColor"
                          strokeWidth="10"
                          fill="transparent"
                          strokeDasharray={`${2 * Math.PI * 40}`}
                          strokeDashoffset={`${2 * Math.PI * 40 * (1 - safeDisplayData.overall_adherence)}`}
                          className="text-emerald-600"
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-lg font-bold text-emerald-600">
                          {(safeDisplayData.overall_adherence * 100).toFixed(0)}%
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-600">Patient Adherence</p>
                  </div>
                </CardContent>
              </Card>

              {/* Risk Score */}
              <Card>
                <CardHeader className="pb-4">
                  <CardTitle className="text-sm font-medium">Risk Score</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center">
                    <div className={`inline-flex px-3 py-1 rounded-full text-sm font-semibold ${getRiskColor(safeDisplayData.risk_score)}`}>
                      {(safeDisplayData.risk_score * 100).toFixed(0)}% Risk
                    </div>
                    <p className="text-xs text-gray-600 mt-2">
                      Confidence: {(safeDisplayData.confidence_level * 100).toFixed(0)}%
                    </p>
                    <div className="mt-3">
                      <Progress value={safeDisplayData.risk_score * 100} className="h-2" />
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Medication Adherence */}
              <Card>
                <CardHeader className="pb-4">
                  <CardTitle className="text-sm font-medium flex items-center gap-2">
                    <Heart className="h-4 w-4" />
                    Medications
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-bold text-blue-600">
                      {(safeDisplayData.adherence_types.medication.percentage * 100).toFixed(0)}%
                    </span>
                    {getTrendIcon(safeDisplayData.adherence_types.medication.trend)}
                  </div>
                  <Progress value={safeDisplayData.adherence_types.medication.percentage * 100} className="h-2 mt-2" />
                </CardContent>
              </Card>

              {/* Appointments */}
              <Card>
                <CardHeader className="pb-4">
                  <CardTitle className="text-sm font-medium flex items-center gap-2">
                    <Calendar className="h-4 w-4" />
                    Appointments
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-bold text-green-600">
                      {(safeDisplayData.adherence_types.appointments.percentage * 100).toFixed(0)}%
                    </span>
                    {getTrendIcon(safeDisplayData.adherence_types.appointments.trend)}
                  </div>
                  <Progress value={safeDisplayData.adherence_types.appointments.percentage * 100} className="h-2 mt-2" />
                </CardContent>
              </Card>
            </div>

            {/* Adherence Breakdown */}
            <Card>
              <CardHeader>
                <CardTitle>Adherence Breakdown</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid gap-4 md:grid-cols-2">
                  <div>
                    <h4 className="font-semibold mb-3">By Category</h4>
                    <div className="space-y-3">
                      {Object.entries(safeDisplayData.adherence_types).map(([type, data]) => (
                        <div key={type} className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <span className="capitalize font-medium">{type}</span>
                            {getTrendIcon(data.trend)}
                          </div>
                          <div className="text-right">
                            <span className="font-semibold">{(data.percentage * 100).toFixed(0)}%</span>
                            <Progress value={data.percentage * 100} className="h-2 w-20" />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-center">
                    <ResponsiveContainer width="100%" height={200}>
                      <PieChart>
                        <Pie
                          data={Object.entries(safeDisplayData.adherence_types).map(([type, data]) => ({
                            name: type,
                            value: data.percentage,
                            color: type === 'medication' ? '#3B82F6' : 
                                  type === 'diet' ? '#10B981' : 
                                  type === 'exercise' ? '#F59E0B' : '#8B5CF6'
                          }))}
                          cx="50%"
                          cy="50%"
                          outerRadius={80}
                          dataKey="value"
                          label={({name, value}) => `${name}: ${(value * 100).toFixed(0)}%`}
                        >
                          {Object.entries(safeDisplayData.adherence_types).map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={
                              entry[0] === 'medication' ? '#3B82F6' : 
                              entry[0] === 'diet' ? '#10B981' : 
                              entry[0] === 'exercise' ? '#F59E0B' : '#8B5CF6'
                            } />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Trends Tab */}
          <TabsContent value="trends" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Adherence Trends Analysis
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={safeDisplayData.trend_data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis domain={[0, 1]} tickFormatter={(value) => `${(value * 100).toFixed(0)}%`} />
                    <Tooltip formatter={(value) => `${(value * 100).toFixed(1)}%`} />
                    <Legend />
                    <Line type="monotone" dataKey="adherence" stroke="#10B981" strokeWidth={3} name="Overall" />
                    <Line type="monotone" dataKey="medication" stroke="#3B82F6" strokeWidth={2} name="Medication" />
                    <Line type="monotone" dataKey="diet" stroke="#F59E0B" strokeWidth={2} name="Diet" />
                    <Line type="monotone" dataKey="exercise" stroke="#8B5CF6" strokeWidth={2} name="Exercise" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Interventions Tab */}
          <TabsContent value="interventions" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="h-5 w-5" />
                  Recommended Interventions
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {safeDisplayData.interventions.map((intervention, index) => (
                    <Card key={index} className="border-emerald-200">
                      <CardContent className="p-4">
                        <div className="flex justify-between items-start mb-3">
                          <Badge className={getPriorityColor(intervention.priority)}>
                            {intervention.priority}
                          </Badge>
                          <div className="text-right">
                            <span className="text-sm font-semibold text-emerald-600">
                              {(intervention.effectiveness * 100).toFixed(0)}% effective
                            </span>
                          </div>
                        </div>
                        
                        <h4 className="font-semibold mb-2">{intervention.strategy}</h4>
                        <p className="text-sm text-gray-600 mb-3">Timeline: {intervention.timeline}</p>
                        
                        <div className="mt-3">
                          <div className="flex justify-between items-center mb-1">
                            <span className="text-xs text-gray-500">Effectiveness</span>
                            <span className="text-xs font-medium">{(intervention.effectiveness * 100).toFixed(0)}%</span>
                          </div>
                          <Progress value={intervention.effectiveness * 100} className="h-2" />
                        </div>
                        
                        <Button size="sm" className="w-full mt-3 bg-emerald-600 hover:bg-emerald-700">
                          Implement Strategy
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Barriers Tab */}
          <TabsContent value="barriers" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5" />
                  Identified Barriers & Solutions
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {safeDisplayData.barriers.map((barrier, index) => (
                    <Card key={index} className="border-yellow-200">
                      <CardContent className="p-4">
                        <div className="flex justify-between items-start mb-3">
                          <div className="flex-1">
                            <h4 className="font-semibold">{barrier.barrier}</h4>
                            <p className="text-sm text-gray-600 mt-1">Frequency: {(barrier.frequency * 100).toFixed(0)}%</p>
                          </div>
                          <Badge className={
                            barrier.severity === 'high' ? 'bg-red-100 text-red-800' :
                            barrier.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-green-100 text-green-800'
                          }>
                            {barrier.severity} severity
                          </Badge>
                        </div>
                        
                        <div className="bg-emerald-50 p-3 rounded-md">
                          <p className="text-sm">
                            <span className="font-medium text-emerald-700">Solution:</span> {barrier.solution}
                          </p>
                        </div>
                        
                        <div className="mt-3">
                          <Progress value={barrier.frequency * 100} className="h-2" />
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Comparison Tab */}
          <TabsContent value="comparison" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="h-5 w-5" />
                  Population Comparison
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid gap-6 md:grid-cols-2">
                  <div>
                    <h4 className="font-semibold mb-4">Patient Percentile</h4>
                    <div className="text-center">
                      <div className="text-4xl font-bold text-emerald-600 mb-2">
                        {safeDisplayData.population_comparison.patient_percentile}th
                      </div>
                      <p className="text-gray-600">percentile</p>
                      <div className="mt-4 bg-gray-200 rounded-full h-3">
                        <div 
                          className="bg-emerald-600 h-3 rounded-full"
                          style={{ width: `${safeDisplayData.population_comparison.patient_percentile}%` }}
                        />
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold mb-4">Comparative Metrics</h4>
                    <ResponsiveContainer width="100%" height={200}>
                      <BarChart data={[
                        { category: 'Patient', value: displayData.overall_adherence },
                        { category: 'Similar Conditions', value: displayData.population_comparison.similar_conditions },
                        { category: 'Age Group', value: displayData.population_comparison.age_group },
                        { category: 'Overall Average', value: displayData.population_comparison.overall_average }
                      ]}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="category" />
                        <YAxis domain={[0, 1]} tickFormatter={(value) => `${(value * 100).toFixed(0)}%`} />
                        <Tooltip formatter={(value) => `${(value * 100).toFixed(1)}%`} />
                        <Bar dataKey="value" fill="#10B981" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default AdvancedAdherenceMonitor;