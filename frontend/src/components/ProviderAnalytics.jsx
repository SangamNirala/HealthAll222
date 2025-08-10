import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { BarChart3, TrendingUp, Users, Calendar, Target, AlertTriangle, Download, Filter, Activity, Heart, Brain, Lightbulb } from 'lucide-react';

const ProviderAnalytics = () => {
  const { switchRole } = useRole();
  const [timeRange, setTimeRange] = useState('30d');
  const [activeTab, setActiveTab] = useState('overview');
  const [treatmentOutcomes, setTreatmentOutcomes] = useState(null);
  const [populationHealth, setPopulationHealth] = useState(null);

  useEffect(() => {
    switchRole('provider');
    
    // Fetch treatment outcomes and population health data
    const fetchAnalyticsData = async () => {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;
      
      try {
        const [outcomesResponse, populationResponse] = await Promise.all([
          fetch(`${backendUrl}/api/provider/treatment-outcomes/provider-123?timeframe=${timeRange}`),
          fetch(`${backendUrl}/api/provider/population-health/provider-123`)
        ]);
        
        const outcomesData = await outcomesResponse.json();
        const populationData = await populationResponse.json();
        
        setTreatmentOutcomes(outcomesData);
        setPopulationHealth(populationData);
      } catch (error) {
        console.error('Error fetching analytics data:', error);
      }
    };
    
    fetchAnalyticsData();
  }, [switchRole, timeRange]);

  const analyticsData = {
    totalPatients: 247,
    activePatients: 198,
    newPatients: 12,
    appointmentCompletionRate: 94,
    patientSatisfaction: 4.7,
    avgTreatmentDuration: 6.2
  };

  const getOutcomeColor = (type) => {
    switch (type) {
      case 'improved': return 'text-green-600';
      case 'stable': return 'text-yellow-600';
      case 'declined': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getRiskColor = (level) => {
    switch (level) {
      case 'Low Risk': return 'bg-green-100 text-green-800';
      case 'low_risk': return 'bg-green-100 text-green-800';
      case 'Medium Risk': return 'bg-yellow-100 text-yellow-800';
      case 'medium_risk': return 'bg-yellow-100 text-yellow-800';
      case 'High Risk': return 'bg-red-100 text-red-800';
      case 'high_risk': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTrendColor = (trend) => {
    switch (trend) {
      case 'improving': return 'text-green-600';
      case 'stable': return 'text-yellow-600';
      case 'increasing': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Advanced Practice Analytics</h1>
              <p className="text-gray-600">Monitor treatment outcomes and population health analytics</p>
            </div>
            <div className="flex space-x-3">
              <select 
                className="border border-gray-300 rounded-md px-3 py-2 bg-white"
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
              >
                <option value="7d">Last 7 days</option>
                <option value="30d">Last 30 days</option>
                <option value="90d">Last 3 months</option>
                <option value="1y">Last year</option>
              </select>
              <Button variant="outline">
                <Filter className="w-4 h-4 mr-2" />
                Filter
              </Button>
              <Button className="bg-emerald-600 hover:bg-emerald-700">
                <Download className="w-4 h-4 mr-2" />
                Export
              </Button>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('overview')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'overview'
                    ? 'border-emerald-500 text-emerald-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Practice Overview
              </button>
              <button
                onClick={() => setActiveTab('outcomes')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'outcomes'
                    ? 'border-emerald-500 text-emerald-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Treatment Outcomes
              </button>
              <button
                onClick={() => setActiveTab('population')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'population'
                    ? 'border-emerald-500 text-emerald-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Population Health
              </button>
            </nav>
          </div>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <>
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              <Card className="border-2 border-emerald-200 bg-emerald-50">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600 flex items-center">
                    <Users className="w-4 h-4 mr-2 text-emerald-600" />
                    Active Patients
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-emerald-600">{analyticsData.activePatients}</div>
                  <p className="text-sm text-gray-500">of {analyticsData.totalPatients} total</p>
                  <div className="mt-2">
                    <div className="bg-emerald-200 rounded-full h-2">
                      <div 
                        className="bg-emerald-600 h-2 rounded-full"
                        style={{ width: `${(analyticsData.activePatients / analyticsData.totalPatients) * 100}%` }}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-blue-200 bg-blue-50">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600 flex items-center">
                    <TrendingUp className="w-4 h-4 mr-2 text-blue-600" />
                    New Patients (30d)
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-blue-600">{analyticsData.newPatients}</div>
                  <p className="text-sm text-green-600">↑ 20% vs last month</p>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-purple-200 bg-purple-50">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600 flex items-center">
                    <Calendar className="w-4 h-4 mr-2 text-purple-600" />
                    Appointment Rate
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-purple-600">{analyticsData.appointmentCompletionRate}%</div>
                  <p className="text-sm text-gray-500">Completion rate</p>
                </CardContent>
              </Card>
            </div>

            {/* Trending Insights */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BarChart3 className="w-5 h-5 mr-2 text-emerald-600" />
                  Key Insights & Trends
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="p-4 bg-green-50 rounded-lg border-l-4 border-green-500">
                    <div className="flex items-center mb-2">
                      <TrendingUp className="w-5 h-5 text-green-600 mr-2" />
                      <h4 className="font-semibold text-green-900">Positive Trend</h4>
                    </div>
                    <p className="text-sm text-green-700">
                      Diabetes patients showing 84% improvement in HbA1c levels over the last quarter.
                    </p>
                  </div>
                  
                  <div className="p-4 bg-yellow-50 rounded-lg border-l-4 border-yellow-500">
                    <div className="flex items-center mb-2">
                      <AlertTriangle className="w-5 h-5 text-yellow-600 mr-2" />
                      <h4 className="font-semibold text-yellow-900">Attention Needed</h4>
                    </div>
                    <p className="text-sm text-yellow-700">
                      15% increase in missed appointments in the obesity patient group.
                    </p>
                  </div>
                  
                  <div className="p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                    <div className="flex items-center mb-2">
                      <Target className="w-5 h-5 text-blue-600 mr-2" />
                      <h4 className="font-semibold text-blue-900">Goal Achievement</h4>
                    </div>
                    <p className="text-sm text-blue-700">
                      78% of patients achieved their weight loss goals within the target timeframe.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </>
        )}

        {/* Treatment Outcomes Tab */}
        {activeTab === 'outcomes' && treatmentOutcomes && (
          <>
            {/* Outcome Summary */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <Card className="border-2 border-emerald-200 bg-emerald-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Activity className="w-8 h-8 text-emerald-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-emerald-600">
                        {Math.round(treatmentOutcomes.outcome_summary.success_rate)}%
                      </div>
                      <p className="text-sm text-gray-600">Success Rate</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-blue-200 bg-blue-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Users className="w-8 h-8 text-blue-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-blue-600">
                        {treatmentOutcomes.outcome_summary.total_patients_treated}
                      </div>
                      <p className="text-sm text-gray-600">Patients Treated</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-purple-200 bg-purple-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Heart className="w-8 h-8 text-purple-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-purple-600">
                        {treatmentOutcomes.outcome_summary.patient_satisfaction}
                      </div>
                      <p className="text-sm text-gray-600">Satisfaction</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-orange-200 bg-orange-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <AlertTriangle className="w-8 h-8 text-orange-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-orange-600">
                        {treatmentOutcomes.outcome_summary.readmission_rate}%
                      </div>
                      <p className="text-sm text-gray-600">Readmission Rate</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Condition Outcomes */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Target className="w-5 h-5 mr-2 text-emerald-600" />
                    Treatment Outcomes by Condition
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {treatmentOutcomes.condition_outcomes.map((outcome) => (
                      <div key={outcome.condition} className="border rounded-lg p-4">
                        <div className="flex justify-between items-center mb-2">
                          <h4 className="font-semibold text-gray-900">{outcome.condition}</h4>
                          <Badge variant="secondary">{outcome.patients} patients</Badge>
                        </div>
                        
                        <div className="grid grid-cols-3 gap-4 text-sm mb-3">
                          <div className="text-center">
                            <div className={`text-lg font-bold ${getOutcomeColor('improved')}`}>
                              {outcome.improved}
                            </div>
                            <div className="text-gray-500">Improved</div>
                          </div>
                          <div className="text-center">
                            <div className={`text-lg font-bold ${getOutcomeColor('stable')}`}>
                              {outcome.stable}
                            </div>
                            <div className="text-gray-500">Stable</div>
                          </div>
                          <div className="text-center">
                            <div className={`text-lg font-bold ${getOutcomeColor('declined')}`}>
                              {outcome.declined}
                            </div>
                            <div className="text-gray-500">Declined</div>
                          </div>
                        </div>
                        
                        <div className="flex justify-between items-center text-sm">
                          <span className="text-gray-600">Target Achievement</span>
                          <span className="font-medium text-emerald-600">
                            {Math.round(outcome.target_achievement_rate)}%
                          </span>
                        </div>
                        
                        <div className="mt-3 bg-gray-200 rounded-full h-2">
                          <div className="flex h-full rounded-full overflow-hidden">
                            <div 
                              className="bg-green-500" 
                              style={{ width: `${(outcome.improved / outcome.patients) * 100}%` }}
                            />
                            <div 
                              className="bg-yellow-500" 
                              style={{ width: `${(outcome.stable / outcome.patients) * 100}%` }}
                            />
                            <div 
                              className="bg-red-500" 
                              style={{ width: `${(outcome.declined / outcome.patients) * 100}%` }}
                            />
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Trending Metrics */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <TrendingUp className="w-5 h-5 mr-2 text-emerald-600" />
                    Trending Performance Metrics
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {treatmentOutcomes.trending_metrics.map((metric) => (
                      <div key={metric.metric} className="border rounded-lg p-4">
                        <div className="flex justify-between items-start mb-2">
                          <h5 className="font-medium text-gray-900">{metric.metric}</h5>
                          <Badge className={`${getTrendColor(metric.trend) === 'text-green-600' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                            {metric.trend}
                          </Badge>
                        </div>
                        
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-4">
                            <div>
                              <div className="text-2xl font-bold text-emerald-600">{metric.current}%</div>
                              <div className="text-sm text-gray-500">Current</div>
                            </div>
                            <div className="text-right">
                              <div className={`text-lg font-medium ${getTrendColor(metric.trend)}`}>
                                {metric.change}
                              </div>
                              <div className="text-sm text-gray-500">vs Previous</div>
                            </div>
                          </div>
                          <div className="w-20 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-emerald-500 h-2 rounded-full"
                              style={{ width: `${metric.current}%` }}
                            />
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </>
        )}

        {/* Population Health Tab */}
        {activeTab === 'population' && populationHealth && (
          <>
            {/* Population Overview */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <Card className="border-2 border-blue-200 bg-blue-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Users className="w-8 h-8 text-blue-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-blue-600">
                        {populationHealth.population_overview.total_population.toLocaleString()}
                      </div>
                      <p className="text-sm text-gray-600">Total Population</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-emerald-200 bg-emerald-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Activity className="w-8 h-8 text-emerald-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-emerald-600">
                        {populationHealth.population_overview.active_patients.toLocaleString()}
                      </div>
                      <p className="text-sm text-gray-600">Active Patients</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-red-200 bg-red-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <AlertTriangle className="w-8 h-8 text-red-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-red-600">
                        {populationHealth.population_overview.high_risk_patients}
                      </div>
                      <p className="text-sm text-gray-600">High Risk</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-purple-200 bg-purple-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Brain className="w-8 h-8 text-purple-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-purple-600">
                        {Math.round(populationHealth.population_overview.chronic_conditions_prevalence)}%
                      </div>
                      <p className="text-sm text-gray-600">Chronic Conditions</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              {/* Condition Prevalence */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <BarChart3 className="w-5 h-5 mr-2 text-emerald-600" />
                    Condition Prevalence
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {populationHealth.condition_prevalence.map((condition) => (
                      <div key={condition.condition} className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <div className="font-medium text-gray-900">{condition.condition}</div>
                          <div className="text-sm text-gray-600">{condition.count} patients</div>
                        </div>
                        <div className="flex items-center space-x-3">
                          <Badge className={getTrendColor(condition.trend) === 'text-green-600' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                            {condition.trend}
                          </Badge>
                          <div className="text-lg font-bold text-gray-700">{condition.prevalence}%</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Risk Stratification */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <AlertTriangle className="w-5 h-5 mr-2 text-emerald-600" />
                    Risk Stratification
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {Object.entries(populationHealth.risk_stratification).map(([key, value]) => (
                      <div key={key} className="flex items-center justify-between p-3 border rounded-lg">
                        <div className="flex items-center space-x-3">
                          <Badge className={getRiskColor(key)}>
                            {key.replace('_', ' ').replace(/^\w/, c => c.toUpperCase())}
                          </Badge>
                          <span className="font-medium text-gray-900">{value.count} patients</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <div className="text-lg font-bold text-gray-700">{value.percentage}%</div>
                          <div className="w-16 bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full ${
                                key === 'low_risk' ? 'bg-green-500' :
                                key === 'medium_risk' ? 'bg-yellow-500' : 'bg-red-500'
                              }`}
                              style={{ width: `${value.percentage}%` }}
                            />
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Quality Measures & Interventions */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Target className="w-5 h-5 mr-2 text-emerald-600" />
                    Quality Measures
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {populationHealth.quality_measures.map((measure) => (
                      <div key={measure.measure} className="p-3 border rounded-lg">
                        <div className="flex justify-between items-center mb-2">
                          <h5 className="font-medium text-gray-900">{measure.measure}</h5>
                          <Badge className={measure.status === 'meeting_target' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                            {measure.status.replace('_', ' ')}
                          </Badge>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">Target: {measure.target}</span>
                          <span className="font-medium text-emerald-600">{measure.current}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Lightbulb className="w-5 h-5 mr-2 text-emerald-600" />
                    Intervention Opportunities
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {populationHealth.intervention_opportunities.map((intervention) => (
                      <div key={intervention.intervention} className="p-4 border rounded-lg">
                        <div className="flex justify-between items-start mb-2">
                          <h5 className="font-medium text-gray-900">{intervention.intervention}</h5>
                          <Badge className={intervention.priority === 'high' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}>
                            {intervention.priority} priority
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">
                          {intervention.eligible_patients} eligible patients
                        </p>
                        <p className="text-sm font-medium text-emerald-700">
                          Potential Impact: {intervention.potential_impact}
                        </p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default ProviderAnalytics;