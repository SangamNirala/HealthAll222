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
    if (saved && typeof saved === 'string' && saved.trim().length &gt; 0) return saved;
  } catch (e) {}
  return 'demo-patient-123';
};

const StatTile = ({ title, value, subtitle, color = 'blue' }) =&gt; (
  &lt;Card className={`border-2 bg-${color}-50 border-${color}-200`} &gt;
    &lt;CardContent className="pt-5"&gt;
      &lt;div className={`text-2xl font-bold text-${color}-600`}&gt;{value}&lt;/div&gt;
      &lt;div className="text-sm text-gray-600"&gt;{title}&lt;/div&gt;
      {subtitle ? &lt;div className={`text-xs text-${color}-700 mt-1`}&gt;{subtitle}&lt;/div&gt; : null}
    &lt;/CardContent&gt;
  &lt;/Card&gt;
);

const SimpleBarChart = ({ data = [], dataKey = 'calories', labelKey = 'date', barColor = '#3b82f6' }) =&gt; {
  // Pure CSS lightweight bars
  const maxVal = useMemo(() =&gt; (data.length ? Math.max(...data.map(d =&gt; d[dataKey] || 0)) : 0), [data, dataKey]);
  return (
    &lt;div className="w-full"&gt;
      &lt;div className="grid grid-cols-5 gap-3 items-end h-40"&gt;
        {data.map((d, idx) =&gt; (
          &lt;div key={idx} className="flex flex-col items-center justify-end"&gt;
            &lt;div
              className="w-8 rounded-md"
              style={{
                height: maxVal ? `${Math.max(8, (d[dataKey] / maxVal) * 100)}%` : '8%',
                background: barColor,
                opacity: 0.9
              }}
              title={`${d[labelKey]}: ${d[dataKey]}`}
            /&gt;
            &lt;div className="text-[10px] text-gray-500 mt-1"&gt;{(d[labelKey] || '').slice(5)}&lt;/div&gt;
          &lt;/div&gt;
        ))}
      &lt;/div&gt;
    &lt;/div&gt;
  );
};

const PatientAnalytics = () =&gt; {
  const { switchRole } = useRole();
  const [userId, setUserId] = useState(getPatientUserId());

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [analytics, setAnalytics] = useState(null);
  const [suggestions, setSuggestions] = useState(null);
  const [correlations, setCorrelations] = useState(null);
  const [actionMessage, setActionMessage] = useState('');

  useEffect(() =&gt; {
    switchRole('patient');
    setUserId(getPatientUserId());
  }, [switchRole]);

  useEffect(() =&gt; {
    let ignore = false;
    const fetchAll = async () =&gt; {
      setLoading(true);
      setError('');
      try {
        const [a, s, c] = await Promise.all([
          fetch(`${API_BASE_URL}/api/patient/analytics/${userId}`).then(r =&gt; r.json()),
          fetch(`${API_BASE_URL}/api/patient/smart-suggestions/${userId}`).then(r =&gt; r.json()),
          fetch(`${API_BASE_URL}/api/patient/symptoms-correlation/${userId}`).then(r =&gt; r.json())
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
    return () =&gt; { ignore = true; };
  }, [userId]);

  const handleQuickAdd = async (item) =&gt; {
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
      setTimeout(() =&gt; setActionMessage(''), 2000);
    } catch (e) {
      setActionMessage(`Save failed: ${e.message}`);
      setTimeout(() =&gt; setActionMessage(''), 3000);
    }
  };

  const nutritionTrends = analytics?.nutrition_trends || [];
  const weekly = analytics?.weekly_summary;
  const ai = analytics?.ai_powered_insights;

  return (
    &lt;div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100"&gt;
      &lt;SmartNavigation /&gt;

      &lt;div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8"&gt;
        &lt;div className="mb-6"&gt;
          &lt;h1 className="text-3xl font-bold text-gray-900 mb-1"&gt;Patient Analytics&lt;/h1&gt;
          &lt;p className="text-gray-600"&gt;Personal health analytics, AI insights, and smart suggestions&lt;/p&gt;
        &lt;/div&gt;

        {loading &amp;&amp; (
          &lt;div className="p-6 bg-white rounded-lg border text-gray-600"&gt;Loading analytics...&lt;/div&gt;
        )}
        {!!error &amp;&amp; (
          &lt;div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg mb-6"&gt;{error}&lt;/div&gt;
        )}

        {!loading &amp;&amp; !error &amp;&amp; (
          &lt;div className="space-y-8"&gt;
            {/* Top stats */}
            &lt;div className="grid grid-cols-1 md:grid-cols-4 gap-6"&gt;
              &lt;StatTile title="Avg Calories" value={(weekly?.average_calories || 0)} subtitle="last 7 days" color="blue" /&gt;
              &lt;StatTile title="Protein Goal Met" value={`${weekly?.protein_goal_met || 0}/7`} subtitle="days this week" color="purple" /&gt;
              &lt;StatTile title="Exercise Sessions" value={weekly?.exercise_sessions || 0} subtitle="this week" color="green" /&gt;
              &lt;StatTile title="Weight Change" value={`${weekly?.weight_change || 0} kg`} subtitle="last 7 days" color="indigo" /&gt;
            &lt;/div&gt;

            {/* Nutrition trends chart */}
            &lt;Card className="col-span-full"&gt;
              &lt;CardHeader&gt;
                &lt;CardTitle className="flex items-center"&gt;
                  &lt;BarChart3 className="w-5 h-5 mr-2 text-blue-600" /&gt;
                  Calories - Last 5 Days
                &lt;/CardTitle&gt;
              &lt;/CardHeader&gt;
              &lt;CardContent&gt;
                &lt;SimpleBarChart data={nutritionTrends} dataKey="calories" labelKey="date" /&gt;
              &lt;/CardContent&gt;
            &lt;/Card&gt;

            {/* AI Insights and Recommendations */}
            &lt;div className="grid grid-cols-1 lg:grid-cols-2 gap-6"&gt;
              &lt;Card&gt;
                &lt;CardHeader&gt;
                  &lt;CardTitle className="flex items-center"&gt;
                    &lt;Brain className="w-5 h-5 mr-2 text-purple-600" /&gt;
                    AI Insights
                  &lt;/CardTitle&gt;
                &lt;/CardHeader&gt;
                &lt;CardContent className="space-y-3"&gt;
                  &lt;div className="text-sm text-gray-500"&gt;
                    Source: {ai?.source || 'default'} • Confidence: {(ai?.confidence ?? 0) * 100}%
                  &lt;/div&gt;
                  &lt;div className="space-y-2"&gt;
                    {(ai?.insights || []).map((msg, idx) =&gt; (
                      &lt;div key={idx} className="p-3 bg-purple-50 rounded-md text-purple-900"&gt;{typeof msg === 'string' ? msg : JSON.stringify(msg)}&lt;/div&gt;
                    ))}
                  &lt;/div&gt;
                  &lt;div className="pt-2"&gt;
                    &lt;div className="text-xs uppercase text-gray-500 mb-2"&gt;Recommendations&lt;/div&gt;
                    &lt;div className="grid gap-2"&gt;
                      {(ai?.recommendations || []).map((r, idx) =&gt; (
                        &lt;div key={idx} className="p-3 bg-blue-50 rounded-md text-blue-900"&gt;{typeof r === 'string' ? r : JSON.stringify(r)}&lt;/div&gt;
                      ))}
                    &lt;/div&gt;
                  &lt;/div&gt;
                &lt;/CardContent&gt;
              &lt;/Card&gt;

              &lt;Card&gt;
                &lt;CardHeader&gt;
                  &lt;CardTitle className="flex items-center"&gt;
                    &lt;Sparkles className="w-5 h-5 mr-2 text-amber-600" /&gt;
                    Personal Insights
                  &lt;/CardTitle&gt;
                &lt;/CardHeader&gt;
                &lt;CardContent className="space-y-2"&gt;
                  {(analytics?.personal_insights || []).map((it, idx) =&gt; (
                    &lt;div key={idx} className="p-3 bg-amber-50 rounded-md"&gt;
                      &lt;div className="text-sm font-medium text-amber-900"&gt;{it.title || it.type || 'Insight'}&lt;/div&gt;
                      &lt;div className="text-sm text-amber-800"&gt;{it.message || (typeof it === 'string' ? it : JSON.stringify(it))}&lt;/div&gt;
                      {it.date ? &lt;div className="text-xs text-amber-700 mt-1"&gt;{it.date}&lt;/div&gt; : null}
                    &lt;/div&gt;
                  ))}
                &lt;/CardContent&gt;
              &lt;/Card&gt;
            &lt;/div&gt;

            {/* Smart Food Suggestions */}
            &lt;Card&gt;
              &lt;CardHeader&gt;
                &lt;CardTitle className="flex items-center justify-between"&gt;
                  &lt;span className="flex items-center"&gt;
                    &lt;Activity className="w-5 h-5 mr-2 text-green-600" /&gt;
                    Smart Food Suggestions
                  &lt;/span&gt;
                  {actionMessage ? &lt;Badge variant="secondary"&gt;{actionMessage}&lt;/Badge&gt; : null}
                &lt;/CardTitle&gt;
              &lt;/CardHeader&gt;
              &lt;CardContent&gt;
                &lt;div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"&gt;
                  {(suggestions?.quick_add_suggestions || []).map((sug, idx) =&gt; (
                    &lt;div key={idx} className="border rounded-lg p-4 bg-white hover:bg-gray-50"&gt;
                      &lt;div className="font-semibold text-gray-900"&gt;{sug.name}&lt;/div&gt;
                      &lt;div className="text-sm text-gray-600"&gt;{sug.reason}&lt;/div&gt;
                      &lt;div className="text-xs text-gray-500 mt-1"&gt;{sug.calories} kcal&lt;/div&gt;
                      &lt;Button onClick={() =&gt; handleQuickAdd(sug)} className="mt-3 bg-blue-600 hover:bg-blue-700" size="sm"&gt;
                        &lt;Plus className="w-4 h-4 mr-2" /&gt;
                        Quick Add
                      &lt;/Button&gt;
                    &lt;/div&gt;
                  ))}
                &lt;/div&gt;
              &lt;/CardContent&gt;
            &lt;/Card&gt;

            {/* Symptom Correlations */}
            &lt;Card&gt;
              &lt;CardHeader&gt;
                &lt;CardTitle className="flex items-center"&gt;
                  &lt;Target className="w-5 h-5 mr-2 text-red-600" /&gt;
                  Symptom Correlation Tracker
                &lt;/CardTitle&gt;
              &lt;/CardHeader&gt;
              &lt;CardContent className="space-y-4"&gt;
                {(correlations?.correlations || []).map((co, idx) =&gt; (
                  &lt;div key={idx} className="border rounded-lg p-4 bg-gray-50"&gt;
                    &lt;div className="font-semibold text-gray-900 mb-1"&gt;{co.symptom}&lt;/div&gt;
                    &lt;div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm"&gt;
                      &lt;div&gt;
                        &lt;div className="text-gray-600 mb-1"&gt;Strong Positive&lt;/div&gt;
                        &lt;div className="flex flex-wrap gap-2"&gt;
                          {(co.strong_positive || []).map((t, i) =&gt; (
                            &lt;Badge key={i} variant="secondary"&gt;{t}&lt;/Badge&gt;
                          ))}
                        &lt;/div&gt;
                      &lt;/div&gt;
                      &lt;div&gt;
                        &lt;div className="text-gray-600 mb-1"&gt;Strong Negative&lt;/div&gt;
                        &lt;div className="flex flex-wrap gap-2"&gt;
                          {(co.strong_negative || []).map((t, i) =&gt; (
                            &lt;Badge key={i} className="bg-red-100 text-red-800"&gt;{t}&lt;/Badge&gt;
                          ))}
                        &lt;/div&gt;
                      &lt;/div&gt;
                      &lt;div&gt;
                        &lt;div className="text-gray-600 mb-1"&gt;Insights&lt;/div&gt;
                        &lt;ul className="list-disc pl-5 text-gray-800"&gt;
                          {(co.insights || []).map((t, i) =&gt; (
                            &lt;li key={i}&gt;{t}&lt;/li&gt;
                          ))}
                        &lt;/ul&gt;
                      &lt;/div&gt;
                    &lt;/div&gt;
                  &lt;/div&gt;
                ))}
              &lt;/CardContent&gt;
            &lt;/Card&gt;
          &lt;/div&gt;
        )}
      &lt;/div&gt;
    &lt;/div&gt;
  );
};

export default PatientAnalytics;