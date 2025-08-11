import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import SmartNavigation from '../shared/SmartNavigation';
import VisualProgressCharts from './VisualProgressCharts';
import MilestoneAchievements from './MilestoneAchievements';
import AdaptiveGoalSuggestions from './AdaptiveGoalSuggestions';
import SocialSharing from './SocialSharing';
import GoalCorrelation from './GoalCorrelation';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Plus, Target, TrendingUp, Users, Brain, BarChart3 } from 'lucide-react';

const AdvancedGoalTracking = () => {
  const [goals, setGoals] = useState([]);
  const [achievements, setAchievements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('dashboard');

  useEffect(() => {
    loadGoalData();
  }, []);

  const loadGoalData = async () => {
    try {
      // Simulate API calls - replace with actual backend endpoints
      const mockGoals = [
        {
          id: 'goal_1',
          title: 'Weekly Exercise Goal',
          category: 'FITNESS',
          target_value: 5,
          current_value: 3,
          unit: 'workouts',
          progress: 60,
          deadline: '2025-01-17',
          status: 'active',
          created_date: '2025-01-10',
          milestones: [
            { value: 1, achieved: true, date: '2025-01-11' },
            { value: 3, achieved: true, date: '2025-01-13' },
            { value: 5, achieved: false, date: null }
          ]
        },
        {
          id: 'goal_2',
          title: 'Daily Water Intake',
          category: 'NUTRITION',
          target_value: 8,
          current_value: 6.5,
          unit: 'glasses',
          progress: 81,
          deadline: '2025-01-17',
          status: 'active',
          created_date: '2025-01-10',
          milestones: [
            { value: 4, achieved: true, date: '2025-01-11' },
            { value: 6, achieved: true, date: '2025-01-13' },
            { value: 8, achieved: false, date: null }
          ]
        },
        {
          id: 'goal_3',
          title: 'Sleep Quality Improvement',
          category: 'WELLNESS',
          target_value: 8,
          current_value: 7.2,
          unit: 'hours',
          progress: 90,
          deadline: '2025-01-30',
          status: 'active',
          created_date: '2025-01-01',
          milestones: [
            { value: 6, achieved: true, date: '2025-01-05' },
            { value: 7, achieved: true, date: '2025-01-10' },
            { value: 8, achieved: false, date: null }
          ]
        }
      ];

      const mockAchievements = [
        {
          id: 'achievement_1',
          goal_id: 'goal_1',
          title: 'First Workout Milestone',
          description: 'Completed your first workout this week!',
          badge_type: 'bronze',
          date_achieved: '2025-01-11',
          category: 'FITNESS'
        },
        {
          id: 'achievement_2',
          goal_id: 'goal_2',
          title: 'Hydration Champion',
          description: 'Maintained daily water intake for 3 days!',
          badge_type: 'silver',
          date_achieved: '2025-01-13',
          category: 'NUTRITION'
        }
      ];

      setGoals(mockGoals);
      setAchievements(mockAchievements);
      setLoading(false);
    } catch (error) {
      console.error('Error loading goal data:', error);
      setLoading(false);
    }
  };

  const handleCreateGoal = () => {
    // Navigate to goal creation form or open modal
    console.log('Create new goal');
  };

  const handleGoalUpdate = (goalId, updates) => {
    setGoals(prevGoals => 
      prevGoals.map(goal => 
        goal.id === goalId ? { ...goal, ...updates } : goal
      )
    );
  };

  const handleAchievementShare = (achievement) => {
    // Trigger social sharing for achievement
    console.log('Share achievement:', achievement);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <SmartNavigation />
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center justify-center h-64">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
              className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full"
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <SmartNavigation />
      
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <div className="flex justify-between items-center mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Advanced Goal Tracking
              </h1>
              <p className="text-gray-600">
                Track your health goals with AI-powered insights and social sharing
              </p>
            </div>
            <Button onClick={handleCreateGoal} className="bg-blue-600 hover:bg-blue-700">
              <Plus className="w-5 h-5 mr-2" />
              New Goal
            </Button>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 }}
            >
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center">
                    <Target className="w-8 h-8 text-blue-600 mr-3" />
                    <div>
                      <p className="text-sm text-gray-500">Active Goals</p>
                      <p className="text-2xl font-bold text-gray-900">{goals.length}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
            >
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center">
                    <TrendingUp className="w-8 h-8 text-green-600 mr-3" />
                    <div>
                      <p className="text-sm text-gray-500">Avg Progress</p>
                      <p className="text-2xl font-bold text-gray-900">
                        {Math.round(goals.reduce((acc, goal) => acc + goal.progress, 0) / goals.length)}%
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3 }}
            >
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center">
                    <Users className="w-8 h-8 text-purple-600 mr-3" />
                    <div>
                      <p className="text-sm text-gray-500">Achievements</p>
                      <p className="text-2xl font-bold text-gray-900">{achievements.length}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.4 }}
            >
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center">
                    <Brain className="w-8 h-8 text-orange-600 mr-3" />
                    <div>
                      <p className="text-sm text-gray-500">AI Insights</p>
                      <p className="text-2xl font-bold text-gray-900">12</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </motion.div>

        {/* Main Content Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-6 mb-8">
            <TabsTrigger value="dashboard" className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4" />
              Dashboard
            </TabsTrigger>
            <TabsTrigger value="progress" className="flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              Progress
            </TabsTrigger>
            <TabsTrigger value="achievements" className="flex items-center gap-2">
              <Target className="w-4 h-4" />
              Achievements
            </TabsTrigger>
            <TabsTrigger value="suggestions" className="flex items-center gap-2">
              <Brain className="w-4 h-4" />
              AI Suggestions
            </TabsTrigger>
            <TabsTrigger value="social" className="flex items-center gap-2">
              <Users className="w-4 h-4" />
              Social
            </TabsTrigger>
            <TabsTrigger value="correlation" className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4" />
              Correlation
            </TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard">
            <VisualProgressCharts 
              goals={goals}
              onGoalUpdate={handleGoalUpdate}
            />
          </TabsContent>

          <TabsContent value="progress">
            <VisualProgressCharts 
              goals={goals}
              onGoalUpdate={handleGoalUpdate}
              viewMode="detailed"
            />
          </TabsContent>

          <TabsContent value="achievements">
            <MilestoneAchievements 
              achievements={achievements}
              goals={goals}
              onAchievementShare={handleAchievementShare}
            />
          </TabsContent>

          <TabsContent value="suggestions">
            <AdaptiveGoalSuggestions 
              goals={goals}
              achievements={achievements}
              onGoalUpdate={handleGoalUpdate}
            />
          </TabsContent>

          <TabsContent value="social">
            <SocialSharing 
              achievements={achievements}
              goals={goals}
            />
          </TabsContent>

          <TabsContent value="correlation">
            <GoalCorrelation 
              goals={goals}
              achievements={achievements}
            />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default AdvancedGoalTracking;