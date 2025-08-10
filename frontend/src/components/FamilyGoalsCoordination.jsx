import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Progress } from './ui/progress';
import { 
  Target, Trophy, Star, TrendingUp, Users, Heart, Activity,
  Calendar, Plus, Edit, CheckCircle, Clock, Award, Zap, 
  ChefHat, Apple, Dumbbell, Brain, Moon, Smile
} from 'lucide-react';

const FamilyGoalsCoordination = () => {
  const { switchRole } = useRole();
  const [goalsData, setGoalsData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    switchRole('family');
    fetchGoalsData();
  }, [switchRole]);

  const fetchGoalsData = async () => {
    try {
      const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/family/goals-coordination/demo-family-123`);
      const data = await response.json();
      setGoalsData(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching goals data:', error);
      setLoading(false);
    }
  };

  const updateGoalProgress = async (goalId, member, progress) => {
    try {
      const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;
      await fetch(`${backendUrl}/api/family/goals/${goalId}/update-progress`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ member, progress })
      });
      // Refresh data
      fetchGoalsData();
    } catch (error) {
      console.error('Error updating progress:', error);
    }
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'nutrition': return <Apple className="w-5 h-5 text-green-600" />;
      case 'physical_activity': return <Dumbbell className="w-5 h-5 text-blue-600" />;
      case 'overall_wellness': return <Heart className="w-5 h-5 text-red-600" />;
      default: return <Target className="w-5 h-5 text-gray-600" />;
    }
  };

  const getCategoryColor = (category) => {
    switch (category) {
      case 'nutrition': return 'bg-green-100 text-green-800';
      case 'physical_activity': return 'bg-blue-100 text-blue-800';
      case 'overall_wellness': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getProgressColor = (progress) => {
    if (progress >= 80) return 'bg-green-500';
    if (progress >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
        <SmartNavigation />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center">Loading family goals...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Family Goals Coordination</h1>
          <p className="text-gray-600">Track and achieve health goals together as a family</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-2 border-purple-200 bg-purple-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Target className="w-8 h-8 text-purple-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-purple-600">
                    {goalsData?.active_goals?.length || 0}
                  </div>
                  <p className="text-sm text-gray-600">Active Goals</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-green-200 bg-green-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <TrendingUp className="w-8 h-8 text-green-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-green-600">
                    {goalsData?.goal_analytics?.overall_family_score || 0}%
                  </div>
                  <p className="text-sm text-gray-600">Family Score</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-blue-200 bg-blue-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Trophy className="w-8 h-8 text-blue-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-blue-600">
                    {goalsData?.motivation_system?.individual_rewards?.length || 0}
                  </div>
                  <p className="text-sm text-gray-600">Rewards Earned</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-orange-200 bg-orange-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Users className="w-8 h-8 text-orange-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-orange-600">4</div>
                  <p className="text-sm text-gray-600">Participants</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="active" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="active">Active Goals</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
            <TabsTrigger value="rewards">Rewards</TabsTrigger>
            <TabsTrigger value="routines">Family Routines</TabsTrigger>
          </TabsList>

          {/* Active Goals Tab */}
          <TabsContent value="active" className="space-y-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-semibold text-gray-900">Current Family Goals</h3>
              <Button className="bg-purple-500 hover:bg-purple-600">
                <Plus className="w-4 h-4 mr-2" />
                Create New Goal
              </Button>
            </div>

            <div className="space-y-6">
              {goalsData?.active_goals?.map((goal, index) => (
                <Card key={index} className="overflow-hidden">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-4">
                        {getCategoryIcon(goal.category)}
                        <div>
                          <CardTitle className="text-xl">{goal.title}</CardTitle>
                          <p className="text-gray-600 mt-1">{goal.description}</p>
                          <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                            <span className="flex items-center">
                              <Calendar className="w-4 h-4 mr-1" />
                              {goal.start_date} - {goal.end_date}
                            </span>
                            <Badge className={getCategoryColor(goal.category)}>
                              {goal.category.replace('_', ' ')}
                            </Badge>
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-3xl font-bold text-purple-600">{goal.family_progress}%</div>
                        <div className="text-sm text-gray-500">Family Progress</div>
                      </div>
                    </div>
                  </CardHeader>
                  
                  <CardContent>
                    {/* Overall Progress Bar */}
                    <div className="mb-6">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-700">Overall Family Progress</span>
                        <span className="text-sm text-gray-500">{goal.family_progress}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div 
                          className={`h-3 rounded-full ${getProgressColor(goal.family_progress)}`}
                          style={{ width: `${goal.family_progress}%` }}
                        />
                      </div>
                    </div>

                    {/* Individual Progress */}
                    <div className="mb-6">
                      <h4 className="font-semibold text-gray-900 mb-4">Individual Progress</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {goal.participants?.map((participant, pIndex) => (
                          <div key={pIndex} className="border rounded-lg p-4">
                            <div className="flex items-center justify-between mb-3">
                              <div className="flex items-center space-x-3">
                                <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                                  <Users className="w-5 h-5 text-blue-600" />
                                </div>
                                <div>
                                  <div className="font-medium">{participant.name}</div>
                                  <div className="text-sm text-gray-600">{participant.target}</div>
                                </div>
                              </div>
                              <div className="text-right">
                                <div className="text-lg font-bold text-blue-600">{participant.current_progress}%</div>
                                <div className="text-xs text-gray-500">{participant.streak} day streak</div>
                              </div>
                            </div>
                            <Progress value={participant.current_progress} className="w-full h-2 mb-2" />
                            {participant.favorite_activity && (
                              <div className="text-xs text-gray-500">
                                Favorite: {participant.favorite_activity}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Weekly Activities (for fitness goals) */}
                    {goal.weekly_activities && (
                      <div className="mb-6">
                        <h4 className="font-semibold text-gray-900 mb-4">This Week's Activities</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
                          {goal.weekly_activities.map((activity, aIndex) => (
                            <div key={aIndex} className={`p-3 rounded-lg border-l-4 ${
                              activity.status === 'completed' ? 'border-green-500 bg-green-50' :
                              activity.status === 'scheduled' ? 'border-blue-500 bg-blue-50' :
                              'border-gray-500 bg-gray-50'
                            }`}>
                              <div className="font-medium text-sm">{activity.day}</div>
                              <div className="text-sm text-gray-600">{activity.activity}</div>
                              <div className="text-xs text-gray-500 mt-1">
                                {activity.duration} • {activity.status}
                              </div>
                              {activity.status === 'completed' && (
                                <CheckCircle className="w-4 h-4 text-green-500 mt-1" />
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Milestones */}
                    <div className="mb-4">
                      <h4 className="font-semibold text-gray-900 mb-3">Milestones</h4>
                      <div className="space-y-2">
                        {goal.milestones?.map((milestone, mIndex) => (
                          <div key={mIndex} className={`flex items-center justify-between p-3 rounded-lg ${
                            milestone.achieved ? 'bg-green-50 border-l-4 border-green-500' : 'bg-gray-50 border-l-4 border-gray-300'
                          }`}>
                            <div className="flex items-center space-x-3">
                              {milestone.achieved ? (
                                <CheckCircle className="w-5 h-5 text-green-500" />
                              ) : (
                                <Clock className="w-5 h-5 text-gray-400" />
                              )}
                              <div>
                                <div className="font-medium">Week {milestone.week}</div>
                                <div className="text-sm text-gray-600">{milestone.reward}</div>
                              </div>
                            </div>
                            {milestone.achieved && (
                              <Badge className="bg-green-100 text-green-800">Completed</Badge>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Health Benefits */}
                    {goal.health_benefits && (
                      <div className="p-4 bg-blue-50 rounded-lg border-l-4 border-blue-400">
                        <div className="font-medium text-blue-900 mb-2">Health Benefits</div>
                        <div className="flex flex-wrap gap-2">
                          {goal.health_benefits.map((benefit, bIndex) => (
                            <Badge key={bIndex} className="bg-blue-100 text-blue-800 text-xs">
                              {benefit.replace('_', ' ')}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Actions */}
                    <div className="flex space-x-3 mt-4 pt-4 border-t">
                      <Button variant="outline" size="sm">
                        <Edit className="w-4 h-4 mr-2" />
                        Edit Goal
                      </Button>
                      <Button size="sm" className="bg-purple-500 hover:bg-purple-600">
                        <TrendingUp className="w-4 h-4 mr-2" />
                        Update Progress
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* Analytics Tab */}
          <TabsContent value="analytics" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Overall Family Score */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <TrendingUp className="w-5 h-5 mr-2 text-green-500" />
                    Family Health Score
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center mb-6">
                    <div className="text-5xl font-bold text-green-600 mb-2">
                      {goalsData?.goal_analytics?.overall_family_score}%
                    </div>
                    <div className="text-gray-600">Overall Family Health Score</div>
                  </div>
                  
                  <div className="space-y-4">
                    {goalsData?.goal_analytics?.improvement_trends?.map((trend, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                        <div>
                          <div className="font-medium text-green-900 capitalize">
                            {trend.metric.replace('_', ' ')}
                          </div>
                          <div className="text-sm text-green-700">Last {trend.period.replace('_', ' ')}</div>
                        </div>
                        <div className="text-right">
                          <div className="text-lg font-bold text-green-600">{trend.change}</div>
                          <div className="text-xs text-green-500">improvement</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Challenge Areas */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Target className="w-5 h-5 mr-2 text-orange-500" />
                    Areas for Improvement
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {goalsData?.goal_analytics?.challenge_areas?.map((area, index) => (
                    <div key={index} className="p-4 bg-orange-50 rounded-lg border-l-4 border-orange-400">
                      <div className="font-medium text-orange-900 mb-2 capitalize">
                        {area.area.replace('_', ' ')}
                      </div>
                      <div className="text-sm text-orange-700">{area.improvement_suggestion}</div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Rewards Tab */}
          <TabsContent value="rewards" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Individual Rewards */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Award className="w-5 h-5 mr-2 text-yellow-500" />
                    Individual Rewards
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {goalsData?.motivation_system?.individual_rewards?.map((reward, index) => (
                    <div key={index} className="p-4 bg-yellow-50 rounded-lg border-l-4 border-yellow-400">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-medium text-yellow-900">{reward.member}</div>
                          <div className="text-sm text-yellow-700">{reward.earned}</div>
                          <div className="text-xs text-yellow-600">For: {reward.for}</div>
                        </div>
                        <Trophy className="w-8 h-8 text-yellow-500" />
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              {/* Family Rewards */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Users className="w-5 h-5 mr-2 text-blue-500" />
                    Family Rewards
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {goalsData?.motivation_system?.family_rewards?.map((reward, index) => (
                    <div key={index} className={`p-4 rounded-lg border-l-4 ${
                      reward.earned ? 'border-green-500 bg-green-50' : 'border-blue-500 bg-blue-50'
                    }`}>
                      <div className="flex items-center justify-between">
                        <div>
                          <div className={`font-medium ${reward.earned ? 'text-green-900' : 'text-blue-900'}`}>
                            {reward.earned || reward.pending}
                          </div>
                          <div className={`text-sm ${reward.earned ? 'text-green-700' : 'text-blue-700'}`}>
                            {reward.earned ? `For: ${reward.for}` : `Need: ${reward.requirement}`}
                          </div>
                        </div>
                        {reward.earned ? (
                          <CheckCircle className="w-8 h-8 text-green-500" />
                        ) : (
                          <Clock className="w-8 h-8 text-blue-500" />
                        )}
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>

            {/* Celebration Milestones */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Star className="w-5 h-5 mr-2 text-purple-500" />
                  Celebration Milestones
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {goalsData?.motivation_system?.celebration_milestones?.map((milestone, index) => (
                    <div key={index} className="p-4 bg-purple-50 rounded-lg border-l-4 border-purple-400">
                      <div className="font-medium text-purple-900 mb-2">{milestone.milestone}</div>
                      <div className="text-sm text-purple-700">{milestone.celebration}</div>
                      <div className="mt-3 flex items-center">
                        <Star className="w-5 h-5 text-purple-500 mr-2" />
                        <div className="text-xs text-purple-600">Coming soon!</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Family Routines Tab */}
          <TabsContent value="routines" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Heart className="w-5 h-5 mr-2 text-red-500" />
                    Family Wellness Routines
                  </div>
                  <Button className="bg-red-500 hover:bg-red-600">
                    <Plus className="w-4 h-4 mr-2" />
                    Add Routine
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {/* Find wellness goal */}
                  {goalsData?.active_goals?.find(goal => goal.category === 'overall_wellness')?.family_routines?.map((routine, index) => (
                    <div key={index} className="border rounded-lg p-6">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <div className="text-lg font-semibold text-gray-900">{routine.routine}</div>
                          <div className="text-gray-600 mt-1">{routine.description}</div>
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-bold text-red-600">{routine.compliance}%</div>
                          <div className="text-sm text-gray-500">Compliance</div>
                        </div>
                      </div>

                      {/* Compliance Progress Bar */}
                      <div className="mb-4">
                        <Progress value={routine.compliance} className="w-full h-3" />
                      </div>

                      {/* Benefits */}
                      <div className="p-4 bg-red-50 rounded-lg">
                        <div className="font-medium text-red-900 mb-2">Benefits</div>
                        <div className="flex flex-wrap gap-2">
                          {routine.benefits?.map((benefit, bIndex) => (
                            <Badge key={bIndex} className="bg-red-100 text-red-800 text-xs">
                              {benefit.replace('_', ' ')}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default FamilyGoalsCoordination;