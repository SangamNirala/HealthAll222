import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { 
  Timeline, 
  Calendar, 
  TrendingUp, 
  TrendingDown,
  Activity, 
  Apple,
  Pill,
  Heart,
  Target,
  Plus,
  Filter,
  Award,
  Zap,
  Clock,
  ChevronDown,
  ChevronRight
} from 'lucide-react';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

const getPatientUserId = () => {
  try {
    const saved = localStorage.getItem('patient_user_id');
    if (saved && typeof saved === 'string' && saved.trim().length > 0) return saved;
  } catch (e) {}
  return 'demo-patient-123';
};

const PatientHealthTimeline = () => {
  const { switchRole } = useRole();
  const [userId, setUserId] = useState(getPatientUserId());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [timelineEvents, setTimelineEvents] = useState([]);
  const [patterns, setPatterns] = useState({});
  const [milestones, setMilestones] = useState([]);
  const [aiInsights, setAiInsights] = useState([]);
  const [categoriesSummary, setCategoriesSummary] = useState({});
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [showAddForm, setShowAddForm] = useState(false);
  const [expandedPatterns, setExpandedPatterns] = useState(false);
  const [actionMessage, setActionMessage] = useState('');

  const [newEvent, setNewEvent] = useState({
    type: 'custom',
    title: '',
    value: '',
    category: 'metrics',
    details: '',
    impact: 'neutral'
  });

  useEffect(() => {
    switchRole('patient');
    setUserId(getPatientUserId());
  }, [switchRole]);

  useEffect(() => {
    fetchTimelineData();
  }, [userId]);

  const fetchTimelineData = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/api/patient/timeline/${userId}`);
      const data = await response.json();
      
      if (!response.ok) throw new Error(data?.detail || 'Failed to load timeline');
      
      setTimelineEvents(data.timeline_events || []);
      setPatterns(data.patterns || {});
      setMilestones(data.milestones || []);
      setAiInsights(data.ai_insights || []);
      setCategoriesSummary(data.categories_summary || {});
    } catch (e) {
      console.error(e);
      setError('Failed to load health timeline. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const addTimelineEvent = async () => {
    if (!newEvent.title || !newEvent.value) {
      setActionMessage('Please fill in title and value');
      setTimeout(() => setActionMessage(''), 3000);
      return;
    }

    try {
      setActionMessage('Adding event...');
      const response = await fetch(`${API_BASE_URL}/api/patient/timeline/${userId}/event`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newEvent)
      });
      
      const data = await response.json();
      if (!response.ok) throw new Error(data?.detail || 'Failed to add event');
      
      setActionMessage('✓ Event added!');
      setShowAddForm(false);
      setNewEvent({
        type: 'custom',
        title: '',
        value: '',
        category: 'metrics',
        details: '',
        impact: 'neutral'
      });
      setTimeout(() => setActionMessage(''), 2000);
      
      // Refresh data
      await fetchTimelineData();
      
    } catch (e) {
      setActionMessage(`Error: ${e.message}`);
      setTimeout(() => setActionMessage(''), 3000);
    }
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'metrics': return Heart;
      case 'activity': return Activity;
      case 'nutrition': return Apple;
      case 'symptoms': return Target;
      case 'medication': return Pill;
      case 'goals': return Award;
      default: return Calendar;
    }
  };

  const getCategoryColor = (category) => {
    switch (category) {
      case 'metrics': return 'text-red-600 bg-red-50 border-red-200';
      case 'activity': return 'text-green-600 bg-green-50 border-green-200';
      case 'nutrition': return 'text-orange-600 bg-orange-50 border-orange-200';
      case 'symptoms': return 'text-purple-600 bg-purple-50 border-purple-200';
      case 'medication': return 'text-blue-600 bg-blue-50 border-blue-200';
      case 'goals': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getImpactIcon = (impact) => {
    switch (impact) {
      case 'positive': return <TrendingUp className="w-4 h-4 text-green-600" />;
      case 'negative': return <TrendingDown className="w-4 h-4 text-red-600" />;
      default: return <Clock className="w-4 h-4 text-gray-600" />;
    }
  };

  const filteredEvents = selectedCategory === 'all' 
    ? timelineEvents 
    : timelineEvents.filter(event => event.category === selectedCategory);

  const categories = ['all', 'metrics', 'activity', 'nutrition', 'symptoms', 'medication', 'goals'];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Health Timeline</h1>
          <p className="text-gray-600">Track your health journey with AI-powered insights and pattern recognition</p>
          {actionMessage && (
            <div className="mt-2 p-3 bg-blue-50 border border-blue-200 text-blue-700 rounded-lg">
              {actionMessage}
            </div>
          )}
        </div>

        {loading && (
          <div className="p-6 bg-white rounded-lg border text-gray-600">Loading health timeline...</div>
        )}
        
        {error && (
          <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg mb-6">{error}</div>
        )}

        {!loading && !error && (
          <div className="space-y-8">
            {/* Categories Summary */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
              {Object.entries(categoriesSummary).map(([category, stats]) => {
                const IconComponent = getCategoryIcon(category);
                const colorClass = getCategoryColor(category);
                return (
                  <Card key={category} className={`border-2 ${colorClass} cursor-pointer hover:shadow-lg transition-shadow`}>
                    <CardContent className="pt-4 pb-3">
                      <div className="text-center">
                        <div className="flex items-center justify-center mb-2">
                          <IconComponent className="w-6 h-6" />
                        </div>
                        <div className="text-lg font-bold">{stats.total || 0}</div>
                        <div className="text-xs text-gray-600 capitalize">{category}</div>
                        {stats.positive_trend && (
                          <div className="text-xs text-green-600 mt-1">
                            {stats.positive_trend} positive
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>

            {/* Milestones */}
            {milestones.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Award className="w-5 h-5 mr-2 text-yellow-600" />
                    Recent Milestones
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {milestones.map((milestone, idx) => (
                      <div key={idx} className="p-4 bg-gradient-to-r from-yellow-50 to-amber-50 border border-yellow-200 rounded-lg">
                        <div className="flex items-start justify-between">
                          <div className="flex items-start space-x-3">
                            <div className="w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center">
                              <Award className="w-5 h-5 text-yellow-600" />
                            </div>
                            <div>
                              <div className="font-semibold text-gray-900">{milestone.title}</div>
                              <div className="text-sm text-gray-600 mt-1">{milestone.description}</div>
                              <div className="text-sm text-yellow-700 mt-2 font-medium">{milestone.celebration}</div>
                            </div>
                          </div>
                          <Badge variant="secondary">{milestone.date}</Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Timeline Events */}
              <div className="lg:col-span-2">
                <Card>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="flex items-center">
                        <Timeline className="w-5 h-5 mr-2 text-blue-600" />
                        Health Events
                      </CardTitle>
                      <div className="flex items-center space-x-2">
                        <select 
                          className="text-sm border border-gray-300 rounded-md px-3 py-1"
                          value={selectedCategory}
                          onChange={(e) => setSelectedCategory(e.target.value)}
                        >
                          {categories.map(cat => (
                            <option key={cat} value={cat}>
                              {cat === 'all' ? 'All Categories' : cat.charAt(0).toUpperCase() + cat.slice(1)}
                            </option>
                          ))}
                        </select>
                        <Button onClick={() => setShowAddForm(true)} size="sm" className="bg-blue-600 hover:bg-blue-700">
                          <Plus className="w-4 h-4 mr-2" />
                          Add Event
                        </Button>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {filteredEvents.map((event, idx) => {
                        const IconComponent = getCategoryIcon(event.category);
                        const colorClass = getCategoryColor(event.category);
                        return (
                          <div key={event.id} className="relative pl-8">
                            {/* Timeline Line */}
                            {idx < filteredEvents.length - 1 && (
                              <div className="absolute left-4 top-8 w-0.5 h-16 bg-gray-200"></div>
                            )}
                            
                            {/* Event Icon */}
                            <div className={`absolute left-0 top-2 w-8 h-8 rounded-full flex items-center justify-center ${colorClass} border-2`}>
                              <IconComponent className="w-4 h-4" />
                            </div>
                            
                            {/* Event Content */}
                            <div className="bg-white border rounded-lg p-4 hover:shadow-md transition-shadow">
                              <div className="flex items-start justify-between mb-2">
                                <div className="flex-1">
                                  <div className="flex items-center space-x-2">
                                    <div className="font-semibold text-gray-900">{event.title}</div>
                                    {getImpactIcon(event.impact)}
                                  </div>
                                  <div className="text-sm text-blue-600 font-medium">{event.value}</div>
                                  {event.details && (
                                    <div className="text-sm text-gray-600 mt-1">{event.details}</div>
                                  )}
                                </div>
                                <Badge variant="secondary">{event.date}</Badge>
                              </div>
                              
                              {event.ai_note && (
                                <div className="mt-3 p-2 bg-purple-50 border border-purple-200 rounded text-sm">
                                  <div className="flex items-start space-x-2">
                                    <Zap className="w-4 h-4 text-purple-600 mt-0.5 flex-shrink-0" />
                                    <div className="text-purple-800">{event.ai_note}</div>
                                  </div>
                                </div>
                              )}
                            </div>
                          </div>
                        );
                      })}
                      
                      {filteredEvents.length === 0 && (
                        <div className="text-center py-8 text-gray-500">
                          <Timeline className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                          <div>No events found for the selected category.</div>
                          <div className="text-sm mt-1">Start tracking your health journey!</div>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* AI Insights & Patterns */}
              <div className="space-y-6">
                {/* AI Insights */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <Zap className="w-5 h-5 mr-2 text-purple-600" />
                      AI Insights
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {aiInsights.map((insight, idx) => (
                        <div key={idx} className="p-3 bg-purple-50 rounded-md border-l-4 border-purple-400">
                          <div className="text-sm text-purple-900">{insight}</div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Health Patterns */}
                <Card>
                  <CardHeader>
                    <CardTitle 
                      className="flex items-center justify-between cursor-pointer"
                      onClick={() => setExpandedPatterns(!expandedPatterns)}
                    >
                      <span className="flex items-center">
                        <TrendingUp className="w-5 h-5 mr-2 text-green-600" />
                        Health Patterns
                      </span>
                      {expandedPatterns ? <ChevronDown className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
                    </CardTitle>
                  </CardHeader>
                  {expandedPatterns && (
                    <CardContent>
                      <div className="space-y-4">
                        {Object.entries(patterns).map(([key, pattern]) => (
                          <div key={key} className="border rounded-lg p-3">
                            <div className="font-medium text-gray-900 text-sm mb-1">
                              {key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                            </div>
                            <div className="text-sm text-gray-700 mb-2">{pattern.pattern}</div>
                            <div className="flex items-center justify-between">
                              <div className="text-xs text-gray-500">
                                Confidence: {Math.round(pattern.confidence * 100)}%
                              </div>
                              <div className="text-xs text-blue-600">{pattern.recommendation}</div>
                            </div>
                          </div>
                        ))}
                        
                        {Object.keys(patterns).length === 0 && (
                          <div className="text-center py-4 text-gray-500 text-sm">
                            Keep tracking to discover patterns!
                          </div>
                        )}
                      </div>
                    </CardContent>
                  )}
                </Card>
              </div>
            </div>
          </div>
        )}

        {/* Add Event Modal */}
        {showAddForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <Card className="w-full max-w-md mx-4">
              <CardHeader>
                <CardTitle>Add Health Event</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Event Title</label>
                  <Input
                    placeholder="e.g., Morning workout, Blood pressure check..."
                    value={newEvent.title}
                    onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Value/Measurement</label>
                  <Input
                    placeholder="e.g., 68kg, 30 minutes, 7/10..."
                    value={newEvent.value}
                    onChange={(e) => setNewEvent({ ...newEvent, value: e.target.value })}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
                  <select 
                    className="w-full border border-gray-300 rounded-md px-3 py-2"
                    value={newEvent.category}
                    onChange={(e) => setNewEvent({ ...newEvent, category: e.target.value })}
                  >
                    <option value="metrics">Health Metrics</option>
                    <option value="activity">Physical Activity</option>
                    <option value="nutrition">Nutrition</option>
                    <option value="symptoms">Symptoms</option>
                    <option value="medication">Medication</option>
                    <option value="goals">Goals</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Impact</label>
                  <select 
                    className="w-full border border-gray-300 rounded-md px-3 py-2"
                    value={newEvent.impact}
                    onChange={(e) => setNewEvent({ ...newEvent, impact: e.target.value })}
                  >
                    <option value="positive">Positive</option>
                    <option value="neutral">Neutral</option>
                    <option value="negative">Negative</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Details (Optional)</label>
                  <Input
                    placeholder="Additional notes or context..."
                    value={newEvent.details}
                    onChange={(e) => setNewEvent({ ...newEvent, details: e.target.value })}
                  />
                </div>
                
                <div className="flex space-x-3 pt-4">
                  <Button onClick={addTimelineEvent} className="bg-blue-600 hover:bg-blue-700">
                    Add Event
                  </Button>
                  <Button variant="outline" onClick={() => setShowAddForm(false)}>
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

export default PatientHealthTimeline;