import React, { useEffect, useMemo, useState } from 'react';
import SmartNavigation from './shared/SmartNavigation';
import { useRole } from '../context/RoleContext';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { BarChart3, Sparkles, Brain, Activity, Target, Calendar, Clock, Plus } from 'lucide-react';

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

            {/* Smart Food Suggestions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <Activity className="w-5 h-5 mr-2 text-green-600" />
                    Smart Food Suggestions
                  </span>
                  {actionMessage ? <Badge variant="secondary">{actionMessage}</Badge> : null}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {(suggestions?.quick_add_suggestions || []).map((sug, idx) => (
                    <div key={idx} className="border rounded-lg p-4 bg-white hover:bg-gray-50">
                      <div className="font-semibold text-gray-900">{sug.name}</div>
                      <div className="text-sm text-gray-600">{sug.reason}</div>
                      <div className="text-xs text-gray-500 mt-1">{sug.calories} kcal</div>
                      <Button onClick={() => handleQuickAdd(sug)} className="mt-3 bg-blue-600 hover:bg-blue-700" size="sm">
                        <Plus className="w-4 h-4 mr-2" />
                        Quick Add
                      </Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Symptom Correlations */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Target className="w-5 h-5 mr-2 text-red-600" />
                  Symptom Correlation Tracker
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {(correlations?.correlations || []).map((co, idx) => (
                  <div key={idx} className="border rounded-lg p-4 bg-gray-50">
                    <div className="font-semibold text-gray-900 mb-1">{co.symptom}</div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
                      <div>
                        <div className="text-gray-600 mb-1">Strong Positive</div>
                        <div className="flex flex-wrap gap-2">
                          {(co.strong_positive || []).map((t, i) => (
                            <Badge key={i} variant="secondary">{t}</Badge>
                          ))}
                        </div>
                      </div>
                      <div>
                        <div className="text-gray-600 mb-1">Strong Negative</div>
                        <div className="flex flex-wrap gap-2">
                          {(co.strong_negative || []).map((t, i) => (
                            <Badge key={i} className="bg-red-100 text-red-800">{t}</Badge>
                          ))}
                        </div>
                      </div>
                      <div>
                        <div className="text-gray-600 mb-1">Insights</div>
                        <ul className="list-disc pl-5 text-gray-800">
                          {(co.insights || []).map((t, i) => (
                            <li key={i}>{t}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default PatientAnalytics;