import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { 
  Target, 
  Plus, 
  Edit3, 
  Trash2, 
  CheckCircle, 
  Clock, 
  TrendingUp,
  Zap,
  Brain,
  Calendar,
  Award,
  Activity,
  BarChart3
} from 'lucide-react';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

const PatientGoals = () => {
  const { switchRole } = useRole();
  const [goals, setGoals] = useState([
    {
      id: 1,
      title: 'Lose 5 lbs',
      category: 'Weight Loss',
      target: 5,
      current: 2,
      unit: 'lbs',
      deadline: '2024-03-01',
      status: 'in_progress',
      priority: 'high',
      ai_insights: ['You\'re 40% to your goal!', 'Current pace suggests you\'ll reach target by Feb 25th'],
      milestones: [
        { date: '2024-01-10', value: 1, note: 'First pound lost!' },
        { date: '2024-01-15', value: 2, note: 'Halfway there!' }
      ]
    },
    {
      id: 2,
      title: 'Walk 10,000 steps daily',
      category: 'Activity',
      target: 10000,
      current: 8500,
      unit: 'steps',
      deadline: 'Daily',
      status: 'in_progress',
      priority: 'medium',
      ai_insights: ['85% of daily goal achieved', 'Try a 10-minute evening walk to reach target'],
      streak_days: 12,
      weekly_progress: [8200, 9100, 8500, 9800, 7200, 8500, 8500]
    },
    {
      id: 3,
      title: 'Drink 8 glasses of water',
      category: 'Hydration',
      target: 8,
      current: 8,
      unit: 'glasses',
      deadline: 'Daily',
      status: 'completed',
      priority: 'high',
      ai_insights: ['Perfect hydration today!', 'Consistent water intake improves energy by 15%'],
      completion_rate: 92 // 92% of days this month
    }
  ]);

  const [showAddForm, setShowAddForm] = useState(false);
  const [selectedGoal, setSelectedGoal] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [actionMessage, setActionMessage] = useState('');
  const [newGoal, setNewGoal] = useState({
    title: '',
    category: 'Weight Loss',
    target: '',
    unit: '',
    deadline: '',
    priority: 'medium'
  });

  useEffect(() => {
    switchRole('patient');
  }, [switchRole]);

  const categories = ['Weight Loss', 'Activity', 'Nutrition', 'Hydration', 'Sleep', 'Mental Health'];

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800 border-green-200';
      case 'in_progress': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'overdue': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'border-l-red-500 bg-red-50';
      case 'medium': return 'border-l-yellow-500 bg-yellow-50';
      case 'low': return 'border-l-green-500 bg-green-50';
      default: return 'border-l-gray-500 bg-gray-50';
    }
  };

  const getProgressPercentage = (current, target) => {
    return Math.min((current / target) * 100, 100);
  };

  const getProgressColor = (percentage) => {
    if (percentage >= 100) return 'bg-green-500';
    if (percentage >= 75) return 'bg-blue-500';
    if (percentage >= 50) return 'bg-yellow-500';
    return 'bg-gray-400';
  };

  const handleAddGoal = () => {
    if (newGoal.title && newGoal.target) {
      const goal = {
        id: goals.length + 1,
        ...newGoal,
        current: 0,
        status: 'in_progress',
        target: parseInt(newGoal.target),
        ai_insights: ['New goal created! AI will analyze your progress patterns.'],
        milestones: []
      };
      setGoals([...goals, goal]);
      setNewGoal({ title: '', category: 'Weight Loss', target: '', unit: '', deadline: '', priority: 'medium' });
      setShowAddForm(false);
      setActionMessage('✓ Goal created with AI tracking enabled!');
      setTimeout(() => setActionMessage(''), 3000);
    }
  };

  const completeGoal = (id) => {
    setGoals(goals.map(goal => 
      goal.id === id ? { 
        ...goal, 
        status: 'completed', 
        current: goal.target,
        ai_insights: [...goal.ai_insights, '🎉 Goal completed! Great achievement!']
      } : goal
    ));
    setActionMessage('🎉 Congratulations on completing your goal!');
    setTimeout(() => setActionMessage(''), 3000);
  };

  const deleteGoal = (id) => {
    setGoals(goals.filter(goal => goal.id !== id));
    setActionMessage('Goal deleted');
    setTimeout(() => setActionMessage(''), 2000);
  };

  const updateProgress = (id, newProgress) => {
    setGoals(goals.map(goal => 
      goal.id === id ? { 
        ...goal, 
        current: newProgress,
        ai_insights: [...goal.ai_insights, `Progress updated to ${newProgress} ${goal.unit}`]
      } : goal
    ));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Smart Health Goals</h1>
          <p className="text-gray-600">AI-powered goal tracking with visual progress and smart insights</p>
          {actionMessage && (
            <div className="mt-2 p-3 bg-blue-50 border border-blue-200 text-blue-700 rounded-lg">
              {actionMessage}
            </div>
          )}
        </div>

        {/* Enhanced Goal Summary */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-2 border-blue-200 bg-blue-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Target className="w-8 h-8 text-blue-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-blue-600">{goals.length}</div>
                  <p className="text-sm text-gray-600">Total Goals</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-green-200 bg-green-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <CheckCircle className="w-8 h-8 text-green-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-green-600">
                    {goals.filter(g => g.status === 'completed').length}
                  </div>
                  <p className="text-sm text-gray-600">Completed</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-yellow-200 bg-yellow-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Clock className="w-8 h-8 text-yellow-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-yellow-600">
                    {goals.filter(g => g.status === 'in_progress').length}
                  </div>
                  <p className="text-sm text-gray-600">In Progress</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-purple-200 bg-purple-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <TrendingUp className="w-8 h-8 text-purple-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-purple-600">
                    {Math.round(goals.reduce((acc, goal) => acc + getProgressPercentage(goal.current, goal.target), 0) / goals.length)}%
                  </div>
                  <p className="text-sm text-gray-600">Avg Progress</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Add Goal Button */}
        <div className="mb-8">
          <Button onClick={() => setShowAddForm(true)} className="bg-blue-600 hover:bg-blue-700">
            <Plus className="w-4 h-4 mr-2" />
            Add Smart Goal
          </Button>
        </div>

        {/* Enhanced Goals Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {goals.map((goal) => {
            const progressPercentage = getProgressPercentage(goal.current, goal.target);
            const progressColor = getProgressColor(progressPercentage);
            
            return (
              <Card 
                key={goal.id} 
                className={`border-l-4 ${getPriorityColor(goal.priority)} hover:shadow-xl transition-all duration-300 cursor-pointer`}
                onClick={() => setSelectedGoal(selectedGoal === goal.id ? null : goal.id)}
              >
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-lg leading-tight mb-2">{goal.title}</CardTitle>
                      <div className="flex items-center space-x-2 mb-3">
                        <Badge variant="secondary">{goal.category}</Badge>
                        <Badge className={getStatusColor(goal.status)}>
                          {goal.status.replace('_', ' ')}
                        </Badge>
                        <Badge className="bg-purple-100 text-purple-800">
                          <Zap className="w-3 h-3 mr-1" />
                          AI Tracked
                        </Badge>
                      </div>
                    </div>
                    <div className="flex space-x-1">
                      <Button variant="ghost" size="sm">
                        <Edit3 className="w-4 h-4" />
                      </Button>
                      <Button 
                        variant="ghost" 
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          deleteGoal(goal.id);
                        }}
                        className="text-red-500 hover:text-red-700"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                
                <CardContent>
                  <div className="space-y-4">
                    {/* Enhanced Progress Visualization */}
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-gray-600">Progress</span>
                        <span className="font-semibold">
                          {goal.current} / {goal.target} {goal.unit}
                        </span>
                      </div>
                      <div className="relative">
                        <div className="bg-gray-200 rounded-full h-3 overflow-hidden">
                          <div 
                            className={`${progressColor} h-3 rounded-full transition-all duration-700 relative`}
                            style={{ width: `${progressPercentage}%` }}
                          >
                            {progressPercentage > 20 && (
                              <div className="absolute inset-0 bg-gradient-to-r from-transparent to-white/20"></div>
                            )}
                          </div>
                        </div>
                        <div className="text-xs text-gray-500 mt-1 text-center">
                          {Math.round(progressPercentage)}% complete
                        </div>
                      </div>
                    </div>

                    {/* Goal Details */}
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <div className="text-gray-500 mb-1">Deadline</div>
                        <div className="font-medium flex items-center">
                          <Calendar className="w-4 h-4 mr-1" />
                          {goal.deadline}
                        </div>
                      </div>
                      <div>
                        <div className="text-gray-500 mb-1">Priority</div>
                        <div className="font-medium capitalize">{goal.priority}</div>
                      </div>
                    </div>

                    {/* Streak/Special Stats */}
                    {goal.streak_days && (
                      <div className="p-2 bg-orange-50 rounded-lg flex items-center">
                        <Award className="w-4 h-4 text-orange-600 mr-2" />
                        <span className="text-sm text-orange-800 font-medium">{goal.streak_days} day streak!</span>
                      </div>
                    )}

                    {goal.completion_rate && (
                      <div className="p-2 bg-green-50 rounded-lg flex items-center">
                        <BarChart3 className="w-4 h-4 text-green-600 mr-2" />
                        <span className="text-sm text-green-800 font-medium">{goal.completion_rate}% monthly success rate</span>
                      </div>
                    )}

                    {/* AI Insights */}
                    {goal.ai_insights && goal.ai_insights.length > 0 && (
                      <div className="p-3 bg-purple-50 rounded-lg border-l-4 border-purple-400">
                        <div className="flex items-center mb-2">
                          <Brain className="w-4 h-4 text-purple-600 mr-2" />
                          <span className="text-sm font-semibold text-purple-900">AI Insights</span>
                        </div>
                        <div className="space-y-1">
                          {goal.ai_insights.slice(0, 2).map((insight, idx) => (
                            <div key={idx} className="text-sm text-purple-800">• {insight}</div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Weekly Progress Chart for Step Goal */}
                    {goal.weekly_progress && selectedGoal === goal.id && (
                      <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                        <div className="text-sm font-semibold text-gray-700 mb-2">Weekly Progress</div>
                        <div className="flex items-end justify-between h-16 space-x-1">
                          {goal.weekly_progress.map((steps, idx) => (
                            <div key={idx} className="flex flex-col items-center">
                              <div 
                                className="bg-blue-500 rounded-t w-4 transition-all duration-500"
                                style={{ height: `${(steps / goal.target) * 60}px` }}
                                title={`${steps} steps`}
                              ></div>
                              <div className="text-xs text-gray-500 mt-1">
                                {['M', 'T', 'W', 'T', 'F', 'S', 'S'][idx]}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Milestones */}
                    {goal.milestones && goal.milestones.length > 0 && selectedGoal === goal.id && (
                      <div className="mt-4 p-3 bg-yellow-50 rounded-lg">
                        <div className="text-sm font-semibold text-gray-700 mb-2">Milestones</div>
                        <div className="space-y-2">
                          {goal.milestones.map((milestone, idx) => (
                            <div key={idx} className="flex items-center justify-between text-sm">
                              <div className="flex items-center">
                                <Award className="w-3 h-3 text-yellow-600 mr-2" />
                                <span>{milestone.note}</span>
                              </div>
                              <span className="text-gray-500">{milestone.date}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Action Buttons */}
                    <div className="flex space-x-2 pt-2">
                      {goal.status !== 'completed' && (
                        <>
                          <Button 
                            onClick={(e) => {
                              e.stopPropagation();
                              const newValue = prompt(`Update progress for ${goal.title} (current: ${goal.current}):`, goal.current);
                              if (newValue !== null) {
                                updateProgress(goal.id, parseInt(newValue));
                              }
                            }}
                            className="flex-1 bg-blue-600 hover:bg-blue-700"
                            size="sm"
                          >
                            <Activity className="w-4 h-4 mr-2" />
                            Update Progress
                          </Button>
                          <Button 
                            onClick={(e) => {
                              e.stopPropagation();
                              completeGoal(goal.id);
                            }}
                            className="bg-green-600 hover:bg-green-700"
                            size="sm"
                          >
                            <CheckCircle className="w-4 h-4" />
                          </Button>
                        </>
                      )}
                      {goal.status === 'completed' && (
                        <div className="flex-1 text-center p-2 bg-green-100 rounded-lg text-green-800 text-sm font-medium">
                          🎉 Goal Completed!
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Add Goal Modal */}
        {showAddForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <Card className="w-full max-w-md mx-4">
              <CardHeader>
                <CardTitle>Add New Goal</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Goal Title</label>
                  <Input
                    placeholder="e.g., Lose 10 pounds, Walk daily..."
                    value={newGoal.title}
                    onChange={(e) => setNewGoal({ ...newGoal, title: e.target.value })}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
                  <select 
                    className="w-full border border-gray-300 rounded-md px-3 py-2"
                    value={newGoal.category}
                    onChange={(e) => setNewGoal({ ...newGoal, category: e.target.value })}
                  >
                    {categories.map(cat => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Target</label>
                    <Input
                      type="number"
                      placeholder="10"
                      value={newGoal.target}
                      onChange={(e) => setNewGoal({ ...newGoal, target: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Unit</label>
                    <Input
                      placeholder="lbs, minutes, glasses..."
                      value={newGoal.unit}
                      onChange={(e) => setNewGoal({ ...newGoal, unit: e.target.value })}
                    />
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
                  <select 
                    className="w-full border border-gray-300 rounded-md px-3 py-2"
                    value={newGoal.priority}
                    onChange={(e) => setNewGoal({ ...newGoal, priority: e.target.value })}
                  >
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Deadline</label>
                  <Input
                    type="date"
                    value={newGoal.deadline}
                    onChange={(e) => setNewGoal({ ...newGoal, deadline: e.target.value })}
                  />
                </div>
                
                <div className="flex space-x-3 pt-4">
                  <Button onClick={handleAddGoal} className="bg-blue-600 hover:bg-blue-700">
                    Add Goal
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

export default PatientGoals;