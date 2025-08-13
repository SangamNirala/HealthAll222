import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  Users, TrendingUp, TrendingDown, BarChart3, 
  AlertTriangle, Target, Activity, Heart,
  MapPin, Calendar, Download, Filter, Lightbulb
} from 'lucide-react';

const PopulationHealthAnalytics = () => {
  const [populationData, setPopulationData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedMetric, setSelectedMetric] = useState('overview');
  const [timeRange, setTimeRange] = useState('1y');

  const providerId = 'provider-123';

  useEffect(() => {
    fetchPopulationData();
  }, [timeRange]);

  const fetchPopulationData = async () => {
    try {
      setLoading(true);
      const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/provider/population-health/${providerId}`);
      const data = await response.json();
      setPopulationData(data);
    } catch (error) {
      console.error('Error fetching population data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level) => {
    if (typeof level === 'string') {
      switch (level.toLowerCase()) {
        case 'low':
        case 'low_risk': return 'bg-green-100 text-green-800';
        case 'medium':
        case 'medium_risk': return 'bg-yellow-100 text-yellow-800';
        case 'high':
        case 'high_risk': return 'bg-red-100 text-red-800';
        default: return 'bg-gray-100 text-gray-800';
      }
    }
    return 'bg-gray-100 text-gray-800';
  };

  const getTrendColor = (trend) => {
    switch (trend) {
      case 'improving': return 'text-green-600';
      case 'stable': return 'text-yellow-600';
      case 'increasing': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'improving': return <TrendingUp className="w-4 h-4 text-green-600" />;
      case 'increasing': return <TrendingUp className="w-4 h-4 text-red-600" />;
      default: return <Activity className="w-4 h-4 text-yellow-600" />;
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <Card>
          <CardContent className="pt-6">
            <div className="animate-pulse space-y-4">
              <div className="h-4 bg-gray-200 rounded w-1/4"></div>
              <div className="grid grid-cols-4 gap-4">
                {[...Array(4)].map((_, i) => (
                  <div key={i} className="h-20 bg-gray-200 rounded"></div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="flex justify-between items-center">
        <div className="flex space-x-2">
          <select 
            className="border border-gray-300 rounded-md px-3 py-2 bg-white"
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
          >
            <option value="3m">Last 3 months</option>
            <option value="6m">Last 6 months</option>
            <option value="1y">Last year</option>
            <option value="2y">Last 2 years</option>
          </select>
          
          <select 
            className="border border-gray-300 rounded-md px-3 py-2 bg-white"
            value={selectedMetric}
            onChange={(e) => setSelectedMetric(e.target.value)}
          >
            <option value="overview">Overview</option>
            <option value="conditions">Condition Analysis</option>
            <option value="demographics">Demographics</option>
            <option value="quality">Quality Measures</option>
          </select>
        </div>
        
        <div className="flex space-x-2">
          <Button variant="outline">
            <Filter className="w-4 h-4 mr-2" />
            Advanced Filters
          </Button>
          <Button variant="outline">
            <Download className="w-4 h-4 mr-2" />
            Export Analysis
          </Button>
        </div>
      </div>

      {/* Population Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="border-2 border-blue-200 bg-blue-50">
          <CardContent className="pt-6">
            <div className="flex items-center">
              <Users className="w-8 h-8 text-blue-600 mr-3" />
              <div>
                <div className="text-2xl font-bold text-blue-600">
                  {populationData?.population_overview?.total_population?.toLocaleString() || 0}
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
                  {populationData?.population_overview?.active_patients?.toLocaleString() || 0}
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
                  {populationData?.population_overview?.high_risk_patients || 0}
                </div>
                <p className="text-sm text-gray-600">High Risk Patients</p>
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
                  {Math.round(populationData?.population_overview?.chronic_conditions_prevalence || 0)}%
                </div>
                <p className="text-sm text-gray-600">Chronic Conditions</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Condition Prevalence */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <BarChart3 className="w-5 h-5 mr-2 text-emerald-600" />
              Condition Prevalence & Trends
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {populationData?.condition_prevalence?.map((condition) => (
                <div key={condition.condition} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <div>
                      <div className="font-medium text-gray-900">{condition.condition}</div>
                      <div className="text-sm text-gray-600">{condition.count} patients</div>
                    </div>
                    <div className="flex items-center space-x-3">
                      <div className="flex items-center space-x-1">
                        {getTrendIcon(condition.trend)}
                        <Badge className={
                          condition.trend === 'improving' ? 'bg-green-100 text-green-800' : 
                          condition.trend === 'stable' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }>
                          {condition.trend}
                        </Badge>
                      </div>
                      <div className="text-lg font-bold text-gray-700">{condition.prevalence}%</div>
                    </div>
                  </div>
                  
                  {/* Prevalence Bar */}
                  <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                    <div 
                      className={`h-2 rounded-full ${
                        condition.trend === 'increasing' ? 'bg-red-500' :
                        condition.trend === 'stable' ? 'bg-yellow-500' : 'bg-green-500'
                      }`}
                      style={{ width: `${Math.min(condition.prevalence, 100)}%` }}
                    />
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
              Risk Stratification Analysis
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {Object.entries(populationData?.risk_stratification || {}).map(([key, value]) => (
                <div key={key} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-3">
                      <Badge className={getRiskColor(key)}>
                        {key.replace('_', ' ').replace(/^\w/, c => c.toUpperCase())} Risk
                      </Badge>
                      <span className="font-medium text-gray-900">{value.count} patients</span>
                    </div>
                    <div className="text-lg font-bold text-gray-700">{value.percentage}%</div>
                  </div>
                  
                  <div className="w-full bg-gray-200 rounded-full h-3 mt-2">
                    <div 
                      className={`h-3 rounded-full ${
                        key === 'low_risk' ? 'bg-green-500' :
                        key === 'medium_risk' ? 'bg-yellow-500' : 'bg-red-500'
                      }`}
                      style={{ width: `${value.percentage}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
            
            {/* Risk Distribution Chart Placeholder */}
            <div className="mt-6 p-6 bg-gray-50 rounded-lg text-center">
              <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-2" />
              <p className="text-sm text-gray-600">Risk distribution visualization</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Demographics Breakdown */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Users className="w-5 h-5 mr-2 text-emerald-600" />
            Demographic Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {populationData?.demographic_breakdown?.map((demo) => (
              <div key={demo.age_group} className="border rounded-lg p-4">
                <div className="text-center mb-3">
                  <div className="text-2xl font-bold text-emerald-600">{demo.count}</div>
                  <div className="text-sm text-gray-600">{demo.age_group} years</div>
                  <div className="text-xs text-gray-500">{demo.percentage}% of population</div>
                </div>
                
                <div className="space-y-1">
                  <div className="text-xs font-medium text-gray-700 mb-1">Top Conditions:</div>
                  {demo.top_conditions?.map((condition, index) => (
                    <Badge key={index} variant="outline" className="text-xs mr-1 mb-1">
                      {condition}
                    </Badge>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Quality Measures & Interventions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Target className="w-5 h-5 mr-2 text-emerald-600" />
              Quality Performance Measures
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {populationData?.quality_measures?.map((measure) => (
                <div key={measure.measure} className="border rounded-lg p-4">
                  <div className="flex justify-between items-center mb-2">
                    <h5 className="font-medium text-gray-900">{measure.measure}</h5>
                    <Badge className={
                      measure.status === 'meeting_target' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }>
                      {measure.status.replace('_', ' ')}
                    </Badge>
                  </div>
                  
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm text-gray-600">Target: {measure.target}</span>
                    <span className="font-medium text-emerald-600">{measure.current}</span>
                  </div>
                  
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${
                        measure.status === 'meeting_target' ? 'bg-green-500' : 'bg-red-500'
                      }`}
                      style={{ 
                        width: `${Math.min(
                          (parseFloat(measure.current) / parseFloat(measure.target.replace('%', '').replace('>', ''))) * 100, 
                          100
                        )}%` 
                      }}
                    />
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
              {populationData?.intervention_opportunities?.map((intervention) => (
                <div key={intervention.intervention} className="border rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h5 className="font-medium text-gray-900">{intervention.intervention}</h5>
                    <Badge className={
                      intervention.priority === 'high' ? 'bg-red-100 text-red-800' : 
                      intervention.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-blue-100 text-blue-800'
                    }>
                      {intervention.priority} priority
                    </Badge>
                  </div>
                  
                  <p className="text-sm text-gray-600 mb-2">
                    <strong>{intervention.eligible_patients}</strong> eligible patients
                  </p>
                  
                  <div className="bg-emerald-50 p-3 rounded-lg">
                    <p className="text-sm font-medium text-emerald-700">
                      Potential Impact: {intervention.potential_impact}
                    </p>
                  </div>
                  
                  <Button size="sm" className="mt-3 bg-emerald-600 hover:bg-emerald-700">
                    View Eligible Patients
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default PopulationHealthAnalytics;