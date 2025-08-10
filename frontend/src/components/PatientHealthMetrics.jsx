import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Activity, Heart, Weight, Ruler, Target, Plus, TrendingUp, Calendar } from 'lucide-react';

const PatientHealthMetrics = () => {
  const { switchRole } = useRole();
  const [activeTab, setActiveTab] = useState('overview');
  const [showAddMetric, setShowAddMetric] = useState(false);
  
  const [metrics, setMetrics] = useState({
    weight: { value: 70, unit: 'kg', date: '2024-01-15', trend: 'stable' },
    height: { value: 170, unit: 'cm', date: '2024-01-01', trend: 'stable' },
    bloodPressure: { systolic: 120, diastolic: 80, date: '2024-01-15', trend: 'normal' },
    heartRate: { value: 72, unit: 'bpm', date: '2024-01-15', trend: 'normal' },
    bodyFat: { value: 18, unit: '%', date: '2024-01-15', trend: 'improving' },
    steps: { value: 8500, unit: 'steps', date: 'Today', trend: 'up' }
  });

  const [newMetric, setNewMetric] = useState({
    type: '',
    value: '',
    date: new Date().toISOString().split('T')[0]
  });

  // Switch to patient role when component mounts
  useEffect(() => {
    switchRole('patient');
  }, [switchRole]);

  const metricCards = [
    {
      key: 'weight',
      title: 'Weight',
      icon: Weight,
      color: 'blue',
      value: metrics.weight.value,
      unit: metrics.weight.unit,
      trend: metrics.weight.trend
    },
    {
      key: 'bloodPressure', 
      title: 'Blood Pressure',
      icon: Heart,
      color: 'red',
      value: `${metrics.bloodPressure.systolic}/${metrics.bloodPressure.diastolic}`,
      unit: 'mmHg',
      trend: metrics.bloodPressure.trend
    },
    {
      key: 'heartRate',
      title: 'Heart Rate',
      icon: Activity,
      color: 'purple',
      value: metrics.heartRate.value,
      unit: metrics.heartRate.unit,
      trend: metrics.heartRate.trend
    },
    {
      key: 'bodyFat',
      title: 'Body Fat',
      icon: Target,
      color: 'green',
      value: metrics.bodyFat.value,
      unit: metrics.bodyFat.unit,
      trend: metrics.bodyFat.trend
    },
    {
      key: 'steps',
      title: 'Daily Steps',
      icon: TrendingUp,
      color: 'orange',
      value: metrics.steps.value.toLocaleString(),
      unit: metrics.steps.unit,
      trend: metrics.steps.trend
    },
    {
      key: 'height',
      title: 'Height',
      icon: Ruler,
      color: 'indigo',
      value: metrics.height.value,
      unit: metrics.height.unit,
      trend: metrics.height.trend
    }
  ];

  const getTrendColor = (trend) => {
    switch (trend) {
      case 'up': case 'improving': return 'text-green-600';
      case 'down': case 'concerning': return 'text-red-600';
      case 'normal': case 'stable': return 'text-gray-600';
      default: return 'text-gray-600';
    }
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'up': case 'improving': return '↗';
      case 'down': case 'concerning': return '↘';
      case 'normal': case 'stable': return '→';
      default: return '→';
    }
  };

  const getCardColorClass = (color) => {
    switch (color) {
      case 'blue': return 'border-blue-200 bg-blue-50';
      case 'red': return 'border-red-200 bg-red-50';
      case 'purple': return 'border-purple-200 bg-purple-50';
      case 'green': return 'border-green-200 bg-green-50';
      case 'orange': return 'border-orange-200 bg-orange-50';
      case 'indigo': return 'border-indigo-200 bg-indigo-50';
      default: return 'border-gray-200 bg-gray-50';
    }
  };

  const getIconColorClass = (color) => {
    switch (color) {
      case 'blue': return 'text-blue-600';
      case 'red': return 'text-red-600'; 
      case 'purple': return 'text-purple-600';
      case 'green': return 'text-green-600';
      case 'orange': return 'text-orange-600';
      case 'indigo': return 'text-indigo-600';
      default: return 'text-gray-600';
    }
  };

  const handleAddMetric = () => {
    if (newMetric.type && newMetric.value) {
      // Logic to add new metric would go here
      console.log('Adding metric:', newMetric);
      setShowAddMetric(false);
      setNewMetric({ type: '', value: '', date: new Date().toISOString().split('T')[0] });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Health Metrics</h1>
          <p className="text-gray-600">Monitor and track your key health indicators over time</p>
        </div>

        {/* Action Bar */}
        <div className="flex justify-between items-center mb-8">
          <div className="flex space-x-2">
            <Button
              variant={activeTab === 'overview' ? 'default' : 'outline'}
              onClick={() => setActiveTab('overview')}
              className="bg-blue-600 hover:bg-blue-700"
            >
              Overview
            </Button>
            <Button
              variant={activeTab === 'history' ? 'default' : 'outline'}
              onClick={() => setActiveTab('history')}
            >
              History
            </Button>
            <Button
              variant={activeTab === 'goals' ? 'default' : 'outline'}
              onClick={() => setActiveTab('goals')}
            >
              Goals
            </Button>
          </div>
          
          <Button onClick={() => setShowAddMetric(true)} className="bg-blue-600 hover:bg-blue-700">
            <Plus className="w-4 h-4 mr-2" />
            Add Metric
          </Button>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {metricCards.map((metric) => {
            const IconComponent = metric.icon;
            return (
              <Card key={metric.key} className={`${getCardColorClass(metric.color)} border-2 hover:shadow-lg transition-shadow cursor-pointer`}>
                <CardHeader className="pb-2">
                  <CardTitle className="flex items-center justify-between text-sm">
                    <div className="flex items-center">
                      <IconComponent className={`w-5 h-5 mr-2 ${getIconColorClass(metric.color)}`} />
                      {metric.title}
                    </div>
                    <Badge variant="secondary" className="text-xs">
                      {metrics[metric.key].date}
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-2xl font-bold text-gray-900">
                        {metric.value} <span className="text-lg text-gray-500">{metric.unit}</span>
                      </div>
                      <div className={`text-sm flex items-center ${getTrendColor(metric.trend)}`}>
                        <span className="mr-1">{getTrendIcon(metric.trend)}</span>
                        {metric.trend}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Content based on active tab */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Health Score */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Target className="w-5 h-5 mr-2 text-green-600" />
                  Health Score
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center">
                  <div className="text-4xl font-bold text-green-600 mb-2">8.2/10</div>
                  <p className="text-gray-600 mb-4">Overall health is good</p>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Cardiovascular</span>
                      <Badge className="bg-green-100 text-green-800">Excellent</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Body Composition</span>
                      <Badge className="bg-blue-100 text-blue-800">Good</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Activity Level</span>
                      <Badge className="bg-green-100 text-green-800">Very Good</Badge>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Recent Changes */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <TrendingUp className="w-5 h-5 mr-2 text-blue-600" />
                  Recent Changes
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                    <div className="flex items-center">
                      <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">Weight decreased</div>
                        <div className="text-xs text-gray-500">2 lbs down from last week</div>
                      </div>
                    </div>
                    <div className="text-sm text-green-600">↓ 2 lbs</div>
                  </div>
                  
                  <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                    <div className="flex items-center">
                      <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">Steps increased</div>
                        <div className="text-xs text-gray-500">Daily average up 15%</div>
                      </div>
                    </div>
                    <div className="text-sm text-blue-600">↑ 15%</div>
                  </div>
                  
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center">
                      <div className="w-2 h-2 bg-gray-500 rounded-full mr-3"></div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">Blood pressure stable</div>
                        <div className="text-xs text-gray-500">Within normal range</div>
                      </div>
                    </div>
                    <div className="text-sm text-gray-600">→</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Add Metric Modal */}
        {showAddMetric && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <Card className="w-full max-w-md mx-4">
              <CardHeader>
                <CardTitle>Add New Metric</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Metric Type</label>
                  <select 
                    className="w-full border border-gray-300 rounded-md px-3 py-2"
                    value={newMetric.type}
                    onChange={(e) => setNewMetric({ ...newMetric, type: e.target.value })}
                  >
                    <option value="">Select metric...</option>
                    <option value="weight">Weight</option>
                    <option value="blood_pressure">Blood Pressure</option>
                    <option value="heart_rate">Heart Rate</option>
                    <option value="body_fat">Body Fat %</option>
                    <option value="steps">Steps</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Value</label>
                  <Input
                    type="number"
                    placeholder="Enter value..."
                    value={newMetric.value}
                    onChange={(e) => setNewMetric({ ...newMetric, value: e.target.value })}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Date</label>
                  <Input
                    type="date"
                    value={newMetric.date}
                    onChange={(e) => setNewMetric({ ...newMetric, date: e.target.value })}
                  />
                </div>
                
                <div className="flex space-x-3 pt-4">
                  <Button onClick={handleAddMetric} className="bg-blue-600 hover:bg-blue-700">
                    Add Metric
                  </Button>
                  <Button variant="outline" onClick={() => setShowAddMetric(false)}>
                    Cancel
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default PatientHealthMetrics;