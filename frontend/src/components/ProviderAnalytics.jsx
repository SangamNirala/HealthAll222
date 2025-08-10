import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { BarChart3, TrendingUp, Users, Calendar, Target, AlertTriangle, Download, Filter } from 'lucide-react';

const ProviderAnalytics = () => {
  const { switchRole } = useRole();
  const [timeRange, setTimeRange] = useState('30d');

  useEffect(() => {
    switchRole('provider');
  }, [switchRole]);

  const analyticsData = {
    totalPatients: 247,
    activePatients: 198,
    newPatients: 12,
    appointmentCompletionRate: 94,
    patientSatisfaction: 4.7,
    avgTreatmentDuration: 6.2
  };

  const patientOutcomes = [
    { condition: 'Type 2 Diabetes', patients: 45, improved: 38, stable: 5, declined: 2 },
    { condition: 'Hypertension', patients: 62, improved: 48, stable: 12, declined: 2 },
    { condition: 'Obesity', patients: 33, improved: 28, stable: 4, declined: 1 },
    { condition: 'Heart Disease', patients: 28, improved: 22, stable: 5, declined: 1 }
  ];

  const riskDistribution = [
    { level: 'Low Risk', count: 145, percentage: 59 },
    { level: 'Medium Risk', count: 78, percentage: 32 },
    { level: 'High Risk', count: 24, percentage: 9 }
  ];

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
      case 'Medium Risk': return 'bg-yellow-100 text-yellow-800';
      case 'High Risk': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
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
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Practice Analytics</h1>
              <p className="text-gray-600">Monitor patient outcomes and practice performance</p>
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

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Patient Outcomes */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Target className="w-5 h-5 mr-2 text-emerald-600" />
                Patient Outcomes by Condition
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {patientOutcomes.map((outcome) => (
                  <div key={outcome.condition} className="border rounded-lg p-4">
                    <div className="flex justify-between items-center mb-2">
                      <h4 className="font-semibold text-gray-900">{outcome.condition}</h4>
                      <Badge variant="secondary">{outcome.patients} patients</Badge>
                    </div>
                    
                    <div className="grid grid-cols-3 gap-4 text-sm">
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

          {/* Risk Distribution */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <AlertTriangle className="w-5 h-5 mr-2 text-emerald-600" />
                Patient Risk Distribution
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {riskDistribution.map((risk) => (
                  <div key={risk.level} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center space-x-3">
                      <Badge className={getRiskColor(risk.level)}>
                        {risk.level}
                      </Badge>
                      <span className="font-medium text-gray-900">{risk.count} patients</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="text-lg font-bold text-gray-700">{risk.percentage}%</div>
                      <div className="w-16 bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${
                            risk.level === 'Low Risk' ? 'bg-green-500' :
                            risk.level === 'Medium Risk' ? 'bg-yellow-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${risk.percentage}%` }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
                
                <div className="mt-6 p-4 bg-emerald-50 rounded-lg">
                  <h4 className="font-semibold text-emerald-900 mb-2">Performance Summary</h4>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <div className="text-gray-600">Patient Satisfaction</div>
                      <div className="text-xl font-bold text-emerald-600">{analyticsData.patientSatisfaction}/5.0</div>
                    </div>
                    <div>
                      <div className="text-gray-600">Avg Treatment Duration</div>
                      <div className="text-xl font-bold text-emerald-600">{analyticsData.avgTreatmentDuration} weeks</div>
                    </div>
                  </div>
                </div>
              </div>
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
      </div>
    </div>
  );
};

export default ProviderAnalytics;