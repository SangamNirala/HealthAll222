import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  BarChart3, TrendingUp, TrendingDown, Users, 
  Target, Activity, Heart, Download, Filter,
  Calendar, AlertTriangle, CheckCircle
} from 'lucide-react';

const TreatmentOutcomeTracking = () => {
  const [outcomesData, setOutcomesData] = useState(null);
  const [timeframe, setTimeframe] = useState('30d');
  const [loading, setLoading] = useState(true);
  const [selectedCondition, setSelectedCondition] = useState('all');

  const providerId = 'provider-123';

  useEffect(() => {
    fetchOutcomesData();
  }, [timeframe]);

  const fetchOutcomesData = async () => {
    try {
      setLoading(true);
      const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/provider/treatment-outcomes/${providerId}?timeframe=${timeframe}`);
      const data = await response.json();
      setOutcomesData(data);
    } catch (error) {
      console.error('Error fetching outcomes data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getOutcomeColor = (type) => {
    switch (type) {
      case 'improved': return 'text-green-600';
      case 'stable': return 'text-yellow-600';
      case 'declined': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getTrendIcon = (trend) => {
    if (trend === 'improving') return <TrendingUp className="w-4 h-4 text-green-600" />;
    if (trend === 'declining') return <TrendingDown className="w-4 h-4 text-red-600" />;
    return <Activity className="w-4 h-4 text-yellow-600" />;
  };

  const getTrendColor = (trend) => {
    switch (trend) {
      case 'improving': return 'text-green-600';
      case 'stable': return 'text-yellow-600';
      case 'declining': return 'text-red-600';
      default: return 'text-gray-600';
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
            value={timeframe}
            onChange={(e) => setTimeframe(e.target.value)}
          >
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 3 months</option>
            <option value="1y">Last year</option>
          </select>
          
          <select 
            className="border border-gray-300 rounded-md px-3 py-2 bg-white"
            value={selectedCondition}
            onChange={(e) => setSelectedCondition(e.target.value)}
          >
            <option value="all">All Conditions</option>
            <option value="diabetes">Diabetes</option>
            <option value="hypertension">Hypertension</option>
            <option value="obesity">Obesity</option>
          </select>
        </div>
        
        <div className="flex space-x-2">
          <Button variant="outline">
            <Filter className="w-4 h-4 mr-2" />
            Advanced Filters
          </Button>
          <Button variant="outline">
            <Download className="w-4 h-4 mr-2" />
            Export Report
          </Button>
        </div>
      </div>

      {/* Outcome Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="border-2 border-emerald-200 bg-emerald-50">
          <CardContent className="pt-6">
            <div className="flex items-center">
              <Activity className="w-8 h-8 text-emerald-600 mr-3" />
              <div>
                <div className="text-2xl font-bold text-emerald-600">
                  {Math.round(outcomesData?.outcome_summary?.success_rate || 0)}%
                </div>
                <p className="text-sm text-gray-600">Treatment Success Rate</p>
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
                  {outcomesData?.outcome_summary?.total_patients_treated || 0}
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
                  {outcomesData?.outcome_summary?.patient_satisfaction || 0}
                </div>
                <p className="text-sm text-gray-600">Patient Satisfaction</p>
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
                  {outcomesData?.outcome_summary?.readmission_rate || 0}%
                </div>
                <p className="text-sm text-gray-600">Readmission Rate</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Condition Outcomes */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Target className="w-5 h-5 mr-2 text-emerald-600" />
              Treatment Outcomes by Condition
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {outcomesData?.condition_outcomes?.map((outcome) => (
                <div key={outcome.condition} className="border rounded-lg p-4">
                  <div className="flex justify-between items-center mb-3">
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
                  
                  <div className="flex justify-between items-center text-sm mb-3">
                    <span className="text-gray-600">Target Achievement</span>
                    <span className="font-medium text-emerald-600">
                      {Math.round(outcome.target_achievement_rate || 0)}%
                    </span>
                  </div>
                  
                  {/* Progress Bar */}
                  <div className="bg-gray-200 rounded-full h-2">
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
                  
                  {/* Additional Metrics */}
                  <div className="mt-3 grid grid-cols-2 gap-4 text-xs text-gray-600">
                    {outcome.avg_hba1c_reduction && (
                      <div>
                        <span className="font-medium">HbA1c Reduction:</span> {outcome.avg_hba1c_reduction}%
                      </div>
                    )}
                    {outcome.avg_bp_reduction && (
                      <div>
                        <span className="font-medium">BP Reduction:</span> {outcome.avg_bp_reduction}
                      </div>
                    )}
                    {outcome.avg_weight_loss && (
                      <div>
                        <span className="font-medium">Weight Loss:</span> {outcome.avg_weight_loss} lbs
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Trending Performance Metrics */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-emerald-600" />
              Performance Trends
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {outcomesData?.trending_metrics?.map((metric) => (
                <div key={metric.metric} className="border rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h5 className="font-medium text-gray-900">{metric.metric}</h5>
                    <div className="flex items-center space-x-1">
                      {getTrendIcon(metric.trend)}
                      <span className={`text-sm font-medium ${getTrendColor(metric.trend)}`}>
                        {metric.trend}
                      </span>
                    </div>
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
                        <div className="text-sm text-gray-500">vs Previous Period</div>
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

      {/* Key Insights */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <CheckCircle className="w-5 h-5 mr-2 text-emerald-600" />
            Key Treatment Insights
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div className="p-4 bg-green-50 rounded-lg border-l-4 border-green-500">
              <div className="flex items-center mb-2">
                <TrendingUp className="w-5 h-5 text-green-600 mr-2" />
                <h4 className="font-semibold text-green-900">Best Performers</h4>
              </div>
              <p className="text-sm text-green-700">
                Diabetes management showing 84% target achievement with new protocol
              </p>
            </div>
            
            <div className="p-4 bg-yellow-50 rounded-lg border-l-4 border-yellow-500">
              <div className="flex items-center mb-2">
                <AlertTriangle className="w-5 h-5 text-yellow-600 mr-2" />
                <h4 className="font-semibold text-yellow-900">Areas for Improvement</h4>
              </div>
              <p className="text-sm text-yellow-700">
                Hypertension management could benefit from increased follow-up frequency
              </p>
            </div>
            
            <div className="p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
              <div className="flex items-center mb-2">
                <Target className="w-5 h-5 text-blue-600 mr-2" />
                <h4 className="font-semibold text-blue-900">Quality Metrics</h4>
              </div>
              <p className="text-sm text-blue-700">
                Patient satisfaction scores consistently above national average
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default TreatmentOutcomeTracking;