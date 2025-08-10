import React, { useState } from 'react';
import { Card, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  Zap, Crown, Star, Heart, TrendingUp, Shield, 
  CheckCircle, Timer, Gift, Sparkles, Target, X
} from 'lucide-react';

const UpgradePrompt = ({ 
  type = 'general', 
  context = '', 
  onClose, 
  className = '',
  compact = false,
  triggerAction = null
}) => {
  const [isVisible, setIsVisible] = useState(true);

  const handleClose = () => {
    setIsVisible(false);
    if (onClose) onClose();
  };

  const getPromptContent = () => {
    switch (type) {
      case 'goals_limit':
        return {
          icon: Target,
          title: "Want to Set More Goals?",
          subtitle: "Upgrade to create unlimited health goals with progress tracking",
          benefits: [
            "Unlimited custom goals",
            "Advanced progress analytics", 
            "Goal achievement rewards",
            "Weekly progress reports"
          ],
          cta: "Upgrade Now",
          urgency: "Limited Time: 50% Off First Month",
          context: `You've reached the goal limit in guest mode. ${context}`
        };

      case 'data_persistence':
        return {
          icon: Shield,
          title: "Save Your Progress Forever",
          subtitle: "Don't lose your health journey - create a free account",
          benefits: [
            "Permanent data storage",
            "Cross-device synchronization",
            "Backup and restore",
            "Export your data anytime"
          ],
          cta: "Create Free Account",
          urgency: "⏰ Session expires in 24 hours",
          context: `Your guest session will expire soon. ${context}`
        };

      case 'ai_insights':
        return {
          icon: Sparkles,
          title: "Unlock AI-Powered Insights",
          subtitle: "Get personalized nutrition recommendations and meal planning",
          benefits: [
            "AI nutrition analysis",
            "Personalized meal plans",
            "Smart food recommendations",
            "Health trend predictions"
          ],
          cta: "Get AI Insights",
          urgency: "🎯 Exclusive: First week free",
          context: `Advanced AI features available with upgrade. ${context}`
        };

      case 'progress_tracking':
        return {
          icon: TrendingUp,
          title: "See Your Progress Over Time",
          subtitle: "Track trends, patterns, and achievements with detailed analytics",
          benefits: [
            "Historical progress tracking",
            "Trend analysis & insights",
            "Achievement milestones",
            "Weekly/monthly reports"
          ],
          cta: "Start Tracking",
          urgency: "🏆 Build your streak starting today",
          context: `Enhanced analytics help you stay motivated. ${context}`
        };

      case 'calculator_results':
        return {
          icon: Crown,
          title: "Get Deeper Health Analysis",
          subtitle: "Upgrade for body composition tracking and metabolic insights",
          benefits: [
            "Advanced body metrics",
            "Metabolic rate analysis",
            "Health risk assessments",
            "Personalized recommendations"
          ],
          cta: "Upgrade Calculator",
          urgency: "💎 Premium health insights await",
          context: `Your BMI results show great potential for optimization. ${context}`
        };

      case 'food_logging_limit':
        return {
          icon: Star,
          title: "Unlimited Food Logging",
          subtitle: "Log all your meals with advanced nutrition tracking",
          benefits: [
            "Unlimited food entries",
            "Macro/micro tracking",
            "Recipe analysis",
            "Nutrition goal monitoring"
          ],
          cta: "Remove Limits",
          urgency: "🍎 Today only: Free nutrition guide included",
          context: `You're doing great with food logging! ${context}`
        };

      default:
        return {
          icon: Heart,
          title: "Ready to Level Up?",
          subtitle: "Transform your health journey with our premium features",
          benefits: [
            "Unlimited everything",
            "AI-powered insights",
            "Priority support",
            "Advanced analytics"
          ],
          cta: "Start Free Trial",
          urgency: "🎉 Special offer: 7 days free",
          context: `Join thousands of users achieving their health goals. ${context}`
        };
    }
  };

  const content = getPromptContent();
  const IconComponent = content.icon;

  if (!isVisible) return null;

  if (compact) {
    return (
      <div className={`bg-gradient-to-r from-purple-600 to-violet-600 text-white p-3 rounded-lg shadow-lg ${className}`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <IconComponent className="w-5 h-5" />
            <div>
              <div className="font-medium text-sm">{content.title}</div>
              <div className="text-xs opacity-90">{content.urgency}</div>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Button 
              size="sm" 
              className="bg-white text-purple-600 hover:bg-gray-100 text-xs px-3"
              onClick={triggerAction}
            >
              {content.cta}
            </Button>
            {onClose && (
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={handleClose}
                className="text-white hover:bg-white/20 p-1"
              >
                <X className="w-4 h-4" />
              </Button>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <Card className={`border-2 border-purple-200 bg-gradient-to-br from-purple-50 to-violet-100 shadow-lg ${className}`}>
      <CardContent className="pt-6">
        {onClose && (
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={handleClose}
            className="absolute top-2 right-2 text-gray-400 hover:text-gray-600"
          >
            <X className="w-4 h-4" />
          </Button>
        )}

        <div className="text-center mb-6">
          <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-violet-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <IconComponent className="w-8 h-8 text-white" />
          </div>
          
          <h3 className="text-2xl font-bold text-gray-900 mb-2">{content.title}</h3>
          <p className="text-gray-600 mb-4">{content.subtitle}</p>
          
          {content.urgency && (
            <Badge className="bg-orange-100 text-orange-800 border-orange-200">
              {content.urgency}
            </Badge>
          )}
        </div>

        <div className="space-y-3 mb-6">
          {content.benefits.map((benefit, index) => (
            <div key={index} className="flex items-center space-x-3">
              <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
              <span className="text-gray-700">{benefit}</span>
            </div>
          ))}
        </div>

        {content.context && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-6">
            <div className="text-sm text-blue-800">{content.context}</div>
          </div>
        )}

        <div className="flex flex-col sm:flex-row gap-3">
          <Button 
            className="flex-1 bg-gradient-to-r from-purple-600 to-violet-600 hover:from-purple-700 hover:to-violet-700 text-white font-semibold py-3"
            onClick={triggerAction}
          >
            <Zap className="w-4 h-4 mr-2" />
            {content.cta}
          </Button>
          <Button 
            variant="outline" 
            className="border-purple-300 text-purple-600 hover:bg-purple-50"
          >
            <Gift className="w-4 h-4 mr-2" />
            Learn More
          </Button>
        </div>

        <div className="text-center mt-4">
          <p className="text-xs text-gray-500">
            ✨ Join 50,000+ users already transforming their health
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default UpgradePrompt;