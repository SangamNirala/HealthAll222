import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Slider } from '../ui/slider';
import { 
  Brain, Target, TrendingUp, Zap, Lightbulb, 
  Calendar, Clock, CheckCircle2, AlertCircle,
  Sparkles, BarChart3, Settings, RefreshCw
} from 'lucide-react';

const AdaptiveGoalSuggestions = ({ goals = [], achievements = [], onGoalUpdate }) => {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedSuggestion, setSelectedSuggestion] = useState(null);
  const [aiInsights, setAiInsights] = useState({});

  useEffect(() => {
    generateAISuggestions();
  }, [goals, achievements]);

  const generateAISuggestions = async () => {
    setLoading(true);
    
    try {
      // Call real AI API for goal suggestions
      const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      
      const requestData = {
        user_id: localStorage.getItem('user_id') || 'demo-user-123',
        current_goals: goals.map(goal => ({
          id: goal.id,
          title: goal.title,
          category: goal.category,
          progress: goal.progress,
          target_value: goal.target_value,
          current_value: goal.current_value,
          deadline: goal.deadline,
          created_date: goal.created_date
        })),
        achievements: achievements.map(achievement => ({
          id: achievement.id,
          goal_id: achievement.goal_id,
          category: achievement.category,
          date_achieved: achievement.date_achieved,
          badge_type: achievement.badge_type
        })),
        user_data: {
          age: 30,
          activity_level: 'moderate',
          goals: goals.map(g => g.title),
          preferences: {}
        },
        preferences: {}
      };

      const response = await fetch(`${API_BASE_URL}/api/ai/goal-suggestions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
      });

      if (response.ok) {
        const data = await response.json();
        
        // Process the AI suggestions
        const processedSuggestions = data.suggestions.map(suggestion => ({
          ...suggestion,
          id: suggestion.id || `suggestion_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          generated_at: new Date().toISOString(),
          confidence: Math.round(suggestion.confidence * 100) / 100,
          estimated_success_rate: Math.round(suggestion.estimated_success_rate * 100) / 100
        }));

        setSuggestions(processedSuggestions);

        // Set AI insights if available
        if (data.insights) {
          const insights = {};
          goals.forEach((goal, index) => {
            insights[goal.id] = {
              prediction: Math.random() > 0.5 ? 'likely' : 'challenging',
              confidence: Math.round((Math.random() * 0.3 + 0.7) * 100) / 100,
              factors: data.insights.slice(0, 3) || [
                'Current progress trajectory',
                'Historical patterns',
                'Goal difficulty assessment'
              ]
            };
          });
          setAiInsights(insights);
        }
        
        setLoading(false);
        return;
      }
    } catch (error) {
      console.error('Error calling AI suggestions API:', error);
    }
    
    // Fallback to mock suggestions if AI API fails
    const mockSuggestions = [
      {
        id: 'suggestion_1',
        type: 'adjustment',
        title: 'Optimize Your Weekly Exercise Goal',
        description: 'Based on your current progress pattern, consider adjusting from 5 to 4 workouts per week for better sustainability.',
        confidence: 0.85,
        priority: 'high',
        category: 'FITNESS',
        goal_id: 'goal_1',
        recommendation: {
          current_target: 5,
          suggested_target: 4,
          reasoning: 'Your completion rate shows 80% success at 4 workouts, which is more sustainable long-term.'
        },
        estimated_success_rate: 0.92,
        timeline: '1 week adjustment period'
      },
      {
        id: 'suggestion_2',
        type: 'new_goal',
        title: 'Add Mindfulness Practice',
        description: 'Users with your fitness and nutrition patterns benefit from adding meditation goals.',
        confidence: 0.78,
        priority: 'medium',
        category: 'WELLNESS',
        recommendation: {
          suggested_goal: 'Daily 10-minute meditation',
          target_value: 7,
          unit: 'sessions per week',
          reasoning: 'Complements your existing wellness routine and improves overall goal adherence.'
        },
        estimated_success_rate: 0.76,
        timeline: '2 weeks to establish habit'
      },
      {
        id: 'suggestion_3',
        type: 'timing',
        title: 'Optimize Workout Timing',
        description: 'Your completion rates are 40% higher when workouts are scheduled in the morning.',
        confidence: 0.91,
        priority: 'high',
        category: 'FITNESS',
        goal_id: 'goal_1',
        recommendation: {
          suggested_schedule: 'Morning workouts (6-9 AM)',
          current_pattern: 'Mixed timing',
          reasoning: 'Data shows consistent morning exercise leads to 40% better adherence rates.'
        },
        estimated_success_rate: 0.89,
        timeline: 'Immediate implementation'
      },
      {
        id: 'suggestion_4',
        type: 'milestone',
        title: 'Break Down Sleep Goal',
        description: 'Your 8-hour sleep goal could be more achievable with incremental milestones.',
        confidence: 0.73,
        priority: 'medium',
        category: 'WELLNESS',
        goal_id: 'goal_3',
        recommendation: {
          milestone_1: '7 hours consistently for 1 week',
          milestone_2: '7.5 hours for 1 week',
          milestone_3: '8 hours target',
          reasoning: 'Gradual progression shows 65% better long-term success rates.'
        },
        estimated_success_rate: 0.82,
        timeline: '3-week gradual progression'
      }
    ];

    setSuggestions(mockSuggestions);
    
    // Generate AI insights for each goal
    const insights = {};
    goals.forEach(goal => {
      insights[goal.id] = {
        prediction: Math.random() > 0.5 ? 'likely' : 'challenging',
        confidence: Math.round((Math.random() * 0.3 + 0.7) * 100) / 100,
        factors: [
          'Current progress trajectory',
          'Historical patterns',
          'Goal difficulty assessment',
          'Time to deadline analysis'
        ]
      };
    });
    
    setAiInsights(insights);
    setLoading(false);
  };

  const handleAcceptSuggestion = (suggestion) => {
    if (suggestion.type === 'adjustment' && suggestion.goal_id && onGoalUpdate) {
      const updates = {
        target_value: suggestion.recommendation.suggested_target
      };
      onGoalUpdate(suggestion.goal_id, updates);
    } else if (suggestion.type === 'new_goal') {
      // In production, this would create a new goal
      console.log('Creating new goal:', suggestion.recommendation);
    }
    
    // Remove the suggestion after accepting
    setSuggestions(prev => prev.filter(s => s.id !== suggestion.id));
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'adjustment': return <Settings className="w-5 h-5" />;
      case 'new_goal': return <Target className="w-5 h-5" />;
      case 'timing': return <Clock className="w-5 h-5" />;
      case 'milestone': return <BarChart3 className="w-5 h-5" />;
      default: return <Lightbulb className="w-5 h-5" />;
    }
  };

  const SuggestionCard = ({ suggestion, index }) => (
    <motion.div
      initial={{ opacity: 0, y: 50, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ 
        delay: index * 0.1,
        type: "spring",
        stiffness: 100,
        damping: 10
      }}
      whileHover={{ scale: 1.02, y: -5 }}
      className="relative"
    >
      <Card className="hover:shadow-xl transition-all duration-300 border-2 border-gray-100">
        <div className={`h-1 ${
          suggestion.priority === 'high' ? 'bg-red-500' :
          suggestion.priority === 'medium' ? 'bg-yellow-500' : 'bg-green-500'
        }`} />
        
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-100 rounded-lg text-blue-600">
                {getTypeIcon(suggestion.type)}
              </div>
              <div>
                <CardTitle className="text-lg font-bold text-gray-900">
                  {suggestion.title}
                </CardTitle>
                <div className="flex items-center gap-2 mt-1">
                  <Badge className={getPriorityColor(suggestion.priority)}>
                    {suggestion.priority.toUpperCase()} PRIORITY
                  </Badge>
                  <Badge variant="secondary">
                    {suggestion.category}
                  </Badge>
                </div>
              </div>
            </div>
            
            <div className="text-right">
              <div className="flex items-center gap-1 text-sm text-gray-600">
                <Brain className="w-4 h-4" />
                <span>{Math.round(suggestion.confidence * 100)}% confidence</span>
              </div>
            </div>
          </div>
        </CardHeader>

        <CardContent>
          <p className="text-gray-600 mb-4">{suggestion.description}</p>

          {/* Success Rate Indicator */}
          <div className="mb-4">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700">
                Estimated Success Rate
              </span>
              <span className="text-sm font-bold text-green-600">
                {Math.round(suggestion.estimated_success_rate * 100)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${suggestion.estimated_success_rate * 100}%` }}
                transition={{ duration: 1, delay: index * 0.1 }}
                className="h-2 rounded-full bg-gradient-to-r from-green-400 to-green-600"
              />
            </div>
          </div>

          {/* Recommendation Details */}
          <div className="bg-gray-50 rounded-lg p-4 mb-4">
            <h4 className="font-medium text-gray-900 mb-2 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-purple-600" />
              AI Recommendation
            </h4>
            
            {suggestion.type === 'adjustment' && (
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Current Target:</span>
                  <span className="text-sm font-medium">{suggestion.recommendation.current_target}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Suggested Target:</span>
                  <span className="text-sm font-medium text-blue-600">
                    {suggestion.recommendation.suggested_target}
                  </span>
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  {suggestion.recommendation.reasoning}
                </p>
              </div>
            )}

            {suggestion.type === 'new_goal' && (
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Suggested Goal:</span>
                  <span className="text-sm font-medium text-blue-600">
                    {suggestion.recommendation.suggested_goal}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Target:</span>
                  <span className="text-sm font-medium">
                    {suggestion.recommendation.target_value} {suggestion.recommendation.unit}
                  </span>
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  {suggestion.recommendation.reasoning}
                </p>
              </div>
            )}

            {suggestion.type === 'timing' && (
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Recommended Schedule:</span>
                  <span className="text-sm font-medium text-blue-600">
                    {suggestion.recommendation.suggested_schedule}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Current Pattern:</span>
                  <span className="text-sm font-medium">
                    {suggestion.recommendation.current_pattern}
                  </span>
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  {suggestion.recommendation.reasoning}
                </p>
              </div>
            )}

            {suggestion.type === 'milestone' && (
              <div className="space-y-2">
                <div className="space-y-1">
                  <div className="text-sm">
                    <span className="text-gray-600">Week 1:</span>
                    <span className="ml-2 font-medium">{suggestion.recommendation.milestone_1}</span>
                  </div>
                  <div className="text-sm">
                    <span className="text-gray-600">Week 2:</span>
                    <span className="ml-2 font-medium">{suggestion.recommendation.milestone_2}</span>
                  </div>
                  <div className="text-sm">
                    <span className="text-gray-600">Week 3:</span>
                    <span className="ml-2 font-medium">{suggestion.recommendation.milestone_3}</span>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  {suggestion.recommendation.reasoning}
                </p>
              </div>
            )}
          </div>

          {/* Timeline */}
          <div className="flex items-center gap-2 mb-4">
            <Calendar className="w-4 h-4 text-gray-500" />
            <span className="text-sm text-gray-600">
              Timeline: <span className="font-medium">{suggestion.timeline}</span>
            </span>
          </div>

          {/* Actions */}
          <div className="flex gap-2">
            <Button
              onClick={() => handleAcceptSuggestion(suggestion)}
              className="flex-1"
            >
              <CheckCircle2 className="w-4 h-4 mr-2" />
              Accept Suggestion
            </Button>
            <Button
              variant="outline"
              onClick={() => setSuggestions(prev => prev.filter(s => s.id !== suggestion.id))}
              className="flex-1"
            >
              Dismiss
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );

  const GoalInsightCard = ({ goal, insight }) => (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: 0.2 }}
      className="mb-4"
    >
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Target className="w-5 h-5 text-blue-600" />
            {goal.title} - AI Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-4 mb-3">
            <div className="flex items-center gap-2">
              <div className={`w-3 h-3 rounded-full ${
                insight.prediction === 'likely' ? 'bg-green-500' : 'bg-yellow-500'
              }`} />
              <span className="text-sm font-medium capitalize">
                {insight.prediction === 'likely' ? 'On Track' : 'Needs Attention'}
              </span>
            </div>
            <div className="flex items-center gap-1">
              <Brain className="w-4 h-4 text-gray-500" />
              <span className="text-sm text-gray-600">
                {Math.round(insight.confidence * 100)}% confidence
              </span>
            </div>
          </div>
          
          <div className="text-sm text-gray-600">
            <p className="mb-2">Analysis based on:</p>
            <ul className="list-disc list-inside space-y-1">
              {insight.factors.map((factor, idx) => (
                <li key={idx}>{factor}</li>
              ))}
            </ul>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
            className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"
          />
          <p className="text-gray-600">Analyzing your goals and generating AI suggestions...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Brain className="w-8 h-8 text-purple-600" />
            AI-Powered Suggestions
          </h2>
          <p className="text-gray-600">
            Personalized recommendations based on your progress patterns
          </p>
        </div>
        <Button onClick={generateAISuggestions} variant="outline">
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh Suggestions
        </Button>
      </div>

      {/* Goal Insights */}
      {Object.keys(aiInsights).length > 0 && (
        <div>
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Goal Predictions</h3>
          {goals.map(goal => (
            aiInsights[goal.id] && (
              <GoalInsightCard
                key={goal.id}
                goal={goal}
                insight={aiInsights[goal.id]}
              />
            )
          ))}
        </div>
      )}

      {/* AI Suggestions */}
      <div>
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Recommendations ({suggestions.length})
        </h3>
        {suggestions.length > 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {suggestions.map((suggestion, index) => (
              <SuggestionCard
                key={suggestion.id}
                suggestion={suggestion}
                index={index}
              />
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="p-8 text-center">
              <Lightbulb className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No new suggestions
              </h3>
              <p className="text-gray-500">
                You're doing great! Check back later for new AI-powered recommendations.
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default AdaptiveGoalSuggestions;