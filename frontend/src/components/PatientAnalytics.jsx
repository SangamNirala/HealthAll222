import React, { useEffect, useMemo, useState } from 'react';
import SmartNavigation from './shared/SmartNavigation';
import { useRole } from '../context/RoleContext';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { BarChart3, Sparkles, Brain, Activity, Target, Calendar, Clock, Plus, TrendingUp, Camera, Mic } from 'lucide-react';

// Import our new enhanced analytics components
import NutritionTrends from './analytics/NutritionTrends';
import HealthMetricsCorrelation from './analytics/HealthMetricsCorrelation';
import PersonalInsights from './analytics/PersonalInsights';
import SmartFoodLogging from './food-logging/SmartFoodLogging';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

const getPatientUserId = () => {
  try {
    const saved = localStorage.getItem('patient_user_id');
    if (saved && typeof saved === 'string' && saved.trim().length > 0) return saved;
  } catch (e) {}
  return 'demo-patient-123';
};

const StatTile = ({ title, value, subtitle, color = 'blue' }) => (
  <Card className={`border-2 bg-${color}-50 border-${color}-200`} >
    <CardContent className="pt-5">
      <div className={`text-2xl font-bold text-${color}-600`}>{value}</div>
      <div className="text-sm text-gray-600">{title}</div>
      {subtitle ? <div className={`text-xs text-${color}-700 mt-1`}>{subtitle}</div> : null}
    </CardContent>
  </Card>
);

const SimpleBarChart = ({ data = [], dataKey = 'calories', labelKey = 'date', barColor = '#3b82f6' }) => {
  // Pure CSS lightweight bars
  const maxVal = useMemo(() => (data.length ? Math.max(...data.map(d => d[dataKey] || 0)) : 0), [data, dataKey]);
  return (
    <div className="w-full">
      <div className="grid grid-cols-5 gap-3 items-end h-40">
        {data.map((d, idx) => (
          <div key={idx} className="flex flex-col items-center justify-end">
            <div
              className="w-8 rounded-md"
              style={{
                height: maxVal ? `${Math.max(8, (d[dataKey] / maxVal) * 100)}%` : '8%',
                background: barColor,
                opacity: 0.9
              }}
              title={`${d[labelKey]}: ${d[dataKey]}`}
            />
            <div className="text-[10px] text-gray-500 mt-1">{(d[labelKey] || '').slice(5)}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

const PatientAnalytics = () => {
  const { switchRole } = useRole();
  const [userId, setUserId] = useState(getPatientUserId());

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [analytics, setAnalytics] = useState(null);
  const [suggestions, setSuggestions] = useState(null);
  const [correlations, setCorrelations] = useState(null);
  const [actionMessage, setActionMessage] = useState('');

  useEffect(() => {
    switchRole('patient');
    setUserId(getPatientUserId());
  }, [switchRole]);

  useEffect(() => {
    let ignore = false;
    const fetchAll = async () => {
      setLoading(true);
      setError('');
      try {
        const [a, s, c] = await Promise.all([
          fetch(`${API_BASE_URL}/api/patient/analytics/${userId}`).then(r => r.json()),
          fetch(`${API_BASE_URL}/api/patient/smart-suggestions/${userId}`).then(r => r.json()),
          fetch(`${API_BASE_URL}/api/patient/symptoms-correlation/${userId}`).then(r => r.json())
        ]);
        if (ignore) return;
        setAnalytics(a);
        setSuggestions(s);
        setCorrelations(c);
      } catch (e) {
        console.error(e);
        setError('Failed to load analytics. Please try again later.');
      } finally {
        if (!ignore) setLoading(false);
      }
    };
    fetchAll();
    return () => { ignore = true; };
  }, [userId]);

  const handleQuickAdd = async (item) => {
    try {
      setActionMessage('Adding food...');
      const res = await fetch(`${API_BASE_URL}/api/patient/food-log`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          food_name: item.name || item.food || 'Food',
          calories: item.calories || 0,
          protein: item.protein || undefined,
          carbs: item.carbs || undefined,
          fat: item.fat || undefined
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data?.detail || 'Save failed');
      setActionMessage('✓ Added to today\'s log');
      setTimeout(() => setActionMessage(''), 2000);
    } catch (e) {
      setActionMessage(`Save failed: ${e.message}`);
      setTimeout(() => setActionMessage(''), 3000);
    }
  };

  const nutritionTrends = analytics?.nutrition_trends || [];
  const weekly = analytics?.weekly_summary;
  const ai = analytics?.ai_powered_insights;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <SmartNavigation />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-1">Patient Analytics</h1>
          <p className="text-gray-600">Personal health analytics, AI insights, and smart suggestions</p>
        </div>

        {loading && (
          <div className="p-6 bg-white rounded-lg border text-gray-600">Loading analytics...</div>
        )}
        {!!error && (
          <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg mb-6">{error}</div>
        )}

        {!loading && !error && (
          <div className="space-y-8">
            {/* Top stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <StatTile title="Avg Calories" value={(weekly?.average_calories || 0)} subtitle="last 7 days" color="blue" />
              <StatTile title="Protein Goal Met" value={`${weekly?.protein_goal_met || 0}/7`} subtitle="days this week" color="purple" />
              <StatTile title="Exercise Sessions" value={weekly?.exercise_sessions || 0} subtitle="this week" color="green" />
              <StatTile title="Weight Change" value={`${weekly?.weight_change || 0} kg`} subtitle="last 7 days" color="indigo" />
            </div>

            {/* Enhanced Analytics Dashboard */}
            <Tabs defaultValue="trends" className="w-full">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="trends" className="flex items-center gap-2">
                  <TrendingUp className="h-4 w-4" />
                  Nutrition Trends
                </TabsTrigger>
                <TabsTrigger value="correlation" className="flex items-center gap-2">
                  <Activity className="h-4 w-4" />
                  Health Correlations
                </TabsTrigger>
                <TabsTrigger value="logging" className="flex items-center gap-2">
                  <Camera className="h-4 w-4" />
                  Smart Logging
                </TabsTrigger>
                <TabsTrigger value="insights" className="flex items-center gap-2">
                  <Brain className="h-4 w-4" />
                  AI Insights
                </TabsTrigger>
              </TabsList>

              <TabsContent value="trends" className="mt-6">
                <NutritionTrends userId={userId} />
              </TabsContent>

              <TabsContent value="correlation" className="mt-6">
                <HealthMetricsCorrelation userId={userId} />
              </TabsContent>

              <TabsContent value="logging" className="mt-6">
                <SmartFoodLogging 
                  userId={userId} 
                  onFoodLogged={(food) => {
                    setActionMessage(`✓ Added ${food.name} to your food log`);
                    setTimeout(() => setActionMessage(''), 3000);
                  }} 
                />
              </TabsContent>

              <TabsContent value="insights" className="mt-6">
                {/* Original AI Insights Content */}
                <div className="space-y-6">
                  {/* AI Insights */}
                  <Card className="bg-gradient-to-r from-purple-50 to-pink-50 border-purple-200">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2 text-purple-900">
                        <Brain className="h-5 w-5" />
                        AI-Powered Insights
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      {ai?.insights?.length > 0 ? (
                        <div className="space-y-4">
                          {ai.insights.map((insight, idx) => (
                            <div key={idx} className="bg-white border border-purple-200 rounded-lg p-4">
                              <div className="flex items-start gap-3">
                                <Brain className="h-5 w-5 text-purple-600 mt-0.5 flex-shrink-0" />
                                <div>
                                  <p className="text-purple-900 font-medium">{insight.title || insight}</p>
                                  {insight.description && (
                                    <p className="text-purple-700 text-sm mt-1">{insight.description}</p>
                                  )}
                                  {insight.confidence && (
                                    <Badge className="mt-2 bg-purple-100 text-purple-800">
                                      {Math.round(insight.confidence * 100)}% confidence
                                    </Badge>
                                  )}
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p className="text-purple-700">AI insights will appear here as you log more data.</p>
                      )}
                    </CardContent>
                  </Card>

                  {/* Enhanced Personal Insights Widget */}
                  <PersonalInsights userId={userId} isWidget={true} className="mt-6" />
                </div>
              </TabsContent>
            </Tabs>

            {/* Nutrition trends chart */}
            <Card className="col-span-full">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BarChart3 className="w-5 h-5 mr-2 text-blue-600" />
                  Calories - Last 5 Days
                </CardTitle>
              </CardHeader>
              <CardContent>
                <SimpleBarChart data={nutritionTrends} dataKey="calories" labelKey="date" />
              </CardContent>
            </Card>

            {/* AI Insights and Recommendations */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Brain className="w-5 h-5 mr-2 text-purple-600" />
                    AI Insights
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="text-sm text-gray-500">
                    Source: {ai?.source || 'default'} • Confidence: {(ai?.confidence ?? 0) * 100}%
                  </div>
                  <div className="space-y-2">
                    {(ai?.insights || []).map((msg, idx) => (
                      <div key={idx} className="p-3 bg-purple-50 rounded-md text-purple-900">{typeof msg === 'string' ? msg : JSON.stringify(msg)}</div>
                    ))}
                  </div>
                  <div className="pt-2">
                    <div className="text-xs uppercase text-gray-500 mb-2">Recommendations</div>
                    <div className="grid gap-2">
                      {(ai?.recommendations || []).map((r, idx) => (
                        <div key={idx} className="p-3 bg-blue-50 rounded-md text-blue-900">{typeof r === 'string' ? r : JSON.stringify(r)}</div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Sparkles className="w-5 h-5 mr-2 text-amber-600" />
                    Personal Insights
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  {(analytics?.personal_insights || []).map((it, idx) => (
                    <div key={idx} className="p-3 bg-amber-50 rounded-md">
                      <div className="text-sm font-medium text-amber-900">{it.title || it.type || 'Insight'}</div>
                      <div className="text-sm text-amber-800">{it.message || (typeof it === 'string' ? it : JSON.stringify(it))}</div>
                      {it.date ? <div className="text-xs text-amber-700 mt-1">{it.date}</div> : null}
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>

            {/* Action Message */}
            {actionMessage && (
              <div className="fixed bottom-4 right-4 bg-green-600 text-white px-4 py-2 rounded-lg shadow-lg z-50">
                {actionMessage}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default PatientAnalytics;