import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  CheckCircle, AlertTriangle, Lightbulb, Target, 
  TrendingUp, Heart, Star, Zap, Clock, Award,
  ThumbsUp, Brain, Activity, Apple, X
} from 'lucide-react';

const RealTimeFeedback = ({ 
  type, 
  data, 
  onAction, 
  onDismiss,
  autoHide = true,
  position = 'bottom-right'
}) => {
  const [isVisible, setIsVisible] = useState(true);
  const [progress, setProgress] = useState(100);

  useEffect(() => {
    if (autoHide) {
      const duration = getFeedbackDuration(type);
      const interval = setInterval(() => {
        setProgress(prev => {
          const newProgress = prev - (100 / duration * 100);
          if (newProgress <= 0) {
            setIsVisible(false);
            clearInterval(interval);
          }
          return Math.max(newProgress, 0);
        });
      }, 100);

      return () => clearInterval(interval);
    }
  }, [type, autoHide]);

  const getFeedbackDuration = (feedbackType) => {
    switch (feedbackType) {
      case 'instant_success': return 30; // 3 seconds
      case 'tip': return 80; // 8 seconds
      case 'achievement': return 60; // 6 seconds
      case 'warning': return 100; // 10 seconds
      default: return 50; // 5 seconds
    }
  };

  const getFeedbackConfig = () => {
    switch (type) {
      case 'food_logged':
        return {
          icon: CheckCircle,
          iconColor: 'text-green-500',
          bgColor: 'bg-green-50 border-green-200',
          title: 'Food Logged Successfully!',
          message: `${data?.foodName} added to your log`,
          insights: data?.insights || [],
          actions: [
            { label: 'View Nutrition', action: 'view_nutrition' },
            { label: 'Add Another', action: 'add_more' }
          ]
        };

      case 'goal_progress':
        return {
          icon: Target,
          iconColor: 'text-blue-500',
          bgColor: 'bg-blue-50 border-blue-200',
          title: 'Goal Progress Updated!',
          message: `${data?.goalName}: ${data?.current}/${data?.target} ${data?.unit}`,
          progress: data?.progressPercent,
          insights: [
            data?.progressPercent >= 100 ? '🎉 Goal achieved! Great work!' :
            data?.progressPercent >= 75 ? `Almost there! Just ${data?.target - data?.current} more to go.` :
            data?.progressPercent >= 50 ? 'Halfway there! Keep up the momentum!' :
            'Great start! Every step counts toward your goal.'
          ],
          actions: [
            { label: 'Set Next Goal', action: 'next_goal' },
            { label: 'View Analytics', action: 'view_analytics' }
          ]
        };

      case 'streak_achievement':
        return {
          icon: Award,
          iconColor: 'text-yellow-500',
          bgColor: 'bg-yellow-50 border-yellow-200',
          title: '🔥 Streak Achievement!',
          message: `${data?.streakDays} day logging streak!`,
          insights: [
            `You're on fire! ${data?.streakDays} consecutive days of healthy tracking.`,
            'Consistency is key to lasting results. Keep it up!'
          ],
          actions: [
            { label: 'Share Success', action: 'share' },
            { label: 'Set Higher Goal', action: 'level_up' }
          ]
        };

      case 'nutrition_insight':
        return {
          icon: Lightbulb,
          iconColor: 'text-purple-500',
          bgColor: 'bg-purple-50 border-purple-200',
          title: 'Smart Nutrition Insight',
          message: data?.title || 'Personalized recommendation',
          insights: data?.insights || [
            'Based on your recent food choices, we have some suggestions.'
          ],
          actions: [
            { label: 'Learn More', action: 'learn_more' },
            { label: 'Apply Tip', action: 'apply_tip' }
          ]
        };

      case 'hydration_reminder':
        return {
          icon: Activity,
          iconColor: 'text-blue-500',
          bgColor: 'bg-blue-50 border-blue-200',
          title: '💧 Hydration Check',
          message: `You've had ${data?.current || 0} glasses today`,
          insights: [
            data?.current >= 8 ? 'Excellent hydration! You\'re meeting your daily goal.' :
            data?.current >= 6 ? 'Good progress! 2 more glasses to reach your goal.' :
            data?.current >= 4 ? 'Halfway there! Keep sipping throughout the day.' :
            'Time for some water! Your body will thank you.'
          ],
          actions: [
            { label: 'Log Water', action: 'log_water' },
            { label: 'Set Reminder', action: 'set_reminder' }
          ]
        };

      case 'calorie_milestone':
        return {
          icon: TrendingUp,
          iconColor: 'text-green-500',
          bgColor: 'bg-green-50 border-green-200',
          title: '📊 Calorie Milestone',
          message: `${data?.calories} calories logged today`,
          insights: [
            data?.percentOfGoal >= 100 ? 'Perfect! You\'ve reached your daily calorie goal.' :
            data?.percentOfGoal >= 80 ? 'Almost there! You\'re doing great with portion control.' :
            data?.percentOfGoal >= 50 ? 'Good progress! Remember to eat balanced meals.' :
            'Keep logging! Awareness is the first step to better health.'
          ],
          progress: data?.percentOfGoal,
          actions: [
            { label: 'View Breakdown', action: 'view_breakdown' },
            { label: 'Plan Next Meal', action: 'plan_meal' }
          ]
        };

      case 'smart_suggestion':
        return {
          icon: Brain,
          iconColor: 'text-indigo-500',
          bgColor: 'bg-indigo-50 border-indigo-200',
          title: '🤖 AI Suggestion',
          message: data?.title || 'Smart recommendation for you',
          insights: data?.suggestions || [
            'Based on your eating patterns, here\'s a personalized tip.'
          ],
          actions: [
            { label: 'Try This', action: 'try_suggestion' },
            { label: 'More Ideas', action: 'more_suggestions' }
          ]
        };

      case 'health_tip':
        return {
          icon: Heart,
          iconColor: 'text-red-500',
          bgColor: 'bg-red-50 border-red-200',
          title: '❤️ Health Tip',
          message: data?.tip || 'Quick health reminder',
          insights: data?.content ? [data.content] : [
            'Small, consistent changes lead to big health improvements over time.'
          ],
          actions: [
            { label: 'Save Tip', action: 'save_tip' },
            { label: 'Learn More', action: 'learn_more' }
          ]
        };

      default:
        return {
          icon: ThumbsUp,
          iconColor: 'text-gray-500',
          bgColor: 'bg-gray-50 border-gray-200',
          title: 'Great job!',
          message: 'Keep up the healthy habits!',
          insights: ['Every healthy choice matters.'],
          actions: [
            { label: 'Continue', action: 'continue' }
          ]
        };
    }
  };

  const config = getFeedbackConfig();
  const IconComponent = config.icon;

  const handleAction = (actionType) => {
    if (onAction) {
      onAction(actionType, data);
    }
    setIsVisible(false);
  };

  const handleDismiss = () => {
    setIsVisible(false);
    if (onDismiss) {
      onDismiss();
    }
  };

  if (!isVisible) return null;

  const positionClasses = {
    'bottom-right': 'fixed bottom-4 right-4 z-50',
    'bottom-left': 'fixed bottom-4 left-4 z-50',
    'top-right': 'fixed top-20 right-4 z-50',
    'top-left': 'fixed top-20 left-4 z-50',
    'center': 'fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50'
  };

  return (
    <div className={`${positionClasses[position]} animate-in slide-in-from-right duration-300`}>
      <Card className={`w-80 shadow-lg border-2 ${config.bgColor}`}>
        <CardContent className="pt-4 pb-4">
          {/* Progress bar for auto-hide */}
          {autoHide && (
            <div className="absolute top-0 left-0 w-full h-1 bg-gray-200 rounded-t">
              <div 
                className="h-full bg-purple-500 rounded-t transition-all duration-100"
                style={{ width: `${progress}%` }}
              />
            </div>
          )}

          {/* Header */}
          <div className="flex items-start justify-between mb-3">
            <div className="flex items-center space-x-3">
              <div className={`p-2 rounded-full ${config.bgColor}`}>
                <IconComponent className={`w-5 h-5 ${config.iconColor}`} />
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 text-sm">{config.title}</h4>
                <p className="text-xs text-gray-600">{config.message}</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleDismiss}
              className="text-gray-400 hover:text-gray-600 p-1"
            >
              <X className="w-4 h-4" />
            </Button>
          </div>

          {/* Progress bar for goals */}
          {config.progress !== undefined && (
            <div className="mb-3">
              <div className="flex justify-between text-xs text-gray-600 mb-1">
                <span>Progress</span>
                <span>{Math.round(config.progress)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full transition-all duration-500 ${
                    config.progress >= 100 ? 'bg-green-500' : 
                    config.progress >= 75 ? 'bg-blue-500' : 
                    'bg-purple-500'
                  }`}
                  style={{ width: `${Math.min(config.progress, 100)}%` }}
                />
              </div>
            </div>
          )}

          {/* Insights */}
          <div className="mb-4">
            {config.insights.map((insight, index) => (
              <div key={index} className="flex items-start space-x-2 mb-2">
                <Star className="w-3 h-3 text-yellow-500 mt-0.5 flex-shrink-0" />
                <p className="text-xs text-gray-700 leading-relaxed">{insight}</p>
              </div>
            ))}
          </div>

          {/* Actions */}
          <div className="flex space-x-2">
            {config.actions.slice(0, 2).map((action, index) => (
              <Button
                key={index}
                size="sm"
                variant={index === 0 ? "default" : "outline"}
                onClick={() => handleAction(action.action)}
                className={`flex-1 text-xs ${
                  index === 0 ? 'bg-purple-600 hover:bg-purple-700' : 'border-purple-300 text-purple-600'
                }`}
              >
                {action.label}
              </Button>
            ))}
          </div>

          {/* Timer indicator */}
          <div className="flex items-center justify-center mt-3">
            <div className="flex items-center space-x-1">
              <Clock className="w-3 h-3 text-gray-400" />
              <span className="text-xs text-gray-400">
                {autoHide ? 'Auto-dismiss' : 'Manual dismiss'}
              </span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default RealTimeFeedback;