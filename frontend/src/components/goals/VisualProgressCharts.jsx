import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Slider } from '../ui/slider';
import { Badge } from '../ui/badge';
import { 
  Target, TrendingUp, Calendar, Award, Settings, 
  ChevronUp, ChevronDown, Activity, Timer, CheckCircle2 
} from 'lucide-react';

const VisualProgressCharts = ({ goals = [], onGoalUpdate, viewMode = 'dashboard' }) => {
  const [selectedGoal, setSelectedGoal] = useState(null);
  const [expandedGoals, setExpandedGoals] = useState(new Set());
  const [animationComplete, setAnimationComplete] = useState(false);

  useEffect(() => {
    // Trigger animation completion after initial render
    const timer = setTimeout(() => setAnimationComplete(true), 1000);
    return () => clearTimeout(timer);
  }, []);

  const toggleGoalExpansion = (goalId) => {
    const newExpanded = new Set(expandedGoals);
    if (newExpanded.has(goalId)) {
      newExpanded.delete(goalId);
    } else {
      newExpanded.add(goalId);
    }
    setExpandedGoals(newExpanded);
  };

  const handleProgressUpdate = (goalId, newValue) => {
    const goal = goals.find(g => g.id === goalId);
    if (goal && onGoalUpdate) {
      const newProgress = Math.round((newValue / goal.target_value) * 100);
      onGoalUpdate(goalId, { 
        current_value: newValue, 
        progress: newProgress 
      });
    }
  };

  const getProgressColor = (progress) => {
    if (progress >= 90) return '#10b981'; // green
    if (progress >= 70) return '#f59e0b'; // yellow
    if (progress >= 50) return '#3b82f6'; // blue
    return '#ef4444'; // red
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'FITNESS': return <Activity className="w-5 h-5" />;
      case 'NUTRITION': return <Target className="w-5 h-5" />;
      case 'WELLNESS': return <Award className="w-5 h-5" />;
      default: return <Target className="w-5 h-5" />;
    }
  };

  const generateTrendData = (goal) => {
    // Generate mock trend data - replace with actual historical data
    const days = 7;
    const data = [];
    const increment = goal.current_value / days;
    
    for (let i = 0; i < days; i++) {
      data.push({
        day: `Day ${i + 1}`,
        value: Math.round((increment * (i + 1) + Math.random() * 0.5) * 10) / 10,
        target: goal.target_value
      });
    }
    return data;
  };

  const CircularProgress = ({ goal, size = 120 }) => {
    const radius = size / 2 - 10;
    const circumference = 2 * Math.PI * radius;
    const strokeDasharray = `${circumference} ${circumference}`;
    const strokeDashoffset = circumference - (goal.progress / 100) * circumference;

    return (
      <motion.div 
        className="relative"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2, type: "spring", stiffness: 100 }}
      >
        <svg className="transform -rotate-90" width={size} height={size}>
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#e5e7eb"
            strokeWidth="8"
            fill="transparent"
          />
          {/* Progress circle */}
          <motion.circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={getProgressColor(goal.progress)}
            strokeWidth="8"
            fill="transparent"
            strokeLinecap="round"
            strokeDasharray={strokeDasharray}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: animationComplete ? strokeDashoffset : circumference }}
            transition={{ duration: 1, ease: "easeInOut" }}
          />
        </svg>
        
        {/* Center content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span 
            className="text-2xl font-bold text-gray-900"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            {goal.progress}%
          </motion.span>
          <span className="text-sm text-gray-500">
            {goal.current_value}/{goal.target_value} {goal.unit}
          </span>
        </div>
      </motion.div>
    );
  };

  const GoalCard = ({ goal, index }) => {
    const isExpanded = expandedGoals.has(goal.id);
    const trendData = generateTrendData(goal);

    return (
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: index * 0.1 }}
        className="w-full"
      >
        <Card className="hover:shadow-lg transition-shadow duration-300">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-blue-100 text-blue-600">
                  {getCategoryIcon(goal.category)}
                </div>
                <div>
                  <CardTitle className="text-lg">{goal.title}</CardTitle>
                  <Badge variant="secondary" className="mt-1">
                    {goal.category}
                  </Badge>
                </div>
              </div>
              <Button 
                variant="ghost" 
                size="sm"
                onClick={() => toggleGoalExpansion(goal.id)}
              >
                {isExpanded ? <ChevronUp /> : <ChevronDown />}
              </Button>
            </div>
          </CardHeader>

          <CardContent>
            <div className="flex items-center justify-between mb-6">
              <CircularProgress goal={goal} />
              
              <div className="flex-1 ml-8">
                <div className="mb-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700">Current Progress</span>
                    <span className="text-sm text-gray-500">
                      {Math.ceil((new Date(goal.deadline) - new Date()) / (1000 * 60 * 60 * 24))} days left
                    </span>
                  </div>
                  
                  {viewMode === 'detailed' && (
                    <div className="mb-4">
                      <label className="text-sm text-gray-600 mb-2 block">
                        Adjust Progress: {goal.current_value} {goal.unit}
                      </label>
                      <Slider
                        value={[goal.current_value]}
                        onValueChange={(value) => handleProgressUpdate(goal.id, value[0])}
                        max={goal.target_value}
                        min={0}
                        step={0.1}
                        className="mb-2"
                      />
                    </div>
                  )}
                  
                  {/* Milestones */}
                  <div className="flex items-center gap-2 mb-4">
                    {goal.milestones?.map((milestone, idx) => (
                      <motion.div
                        key={idx}
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.8 + idx * 0.1 }}
                        className={`flex items-center justify-center w-8 h-8 rounded-full text-sm font-medium ${
                          milestone.achieved 
                            ? 'bg-green-500 text-white' 
                            : 'bg-gray-200 text-gray-600'
                        }`}
                      >
                        {milestone.achieved ? (
                          <CheckCircle2 className="w-4 h-4" />
                        ) : (
                          milestone.value
                        )}
                      </motion.div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <AnimatePresence>
              {isExpanded && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="border-t pt-6"
                >
                  {/* Trend Chart */}
                  <div className="mb-6">
                    <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center gap-2">
                      <TrendingUp className="w-4 h-4" />
                      7-Day Progress Trend
                    </h4>
                    <div className="h-48">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={trendData}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="day" />
                          <YAxis />
                          <Tooltip />
                          <Line 
                            type="monotone" 
                            dataKey="value" 
                            stroke={getProgressColor(goal.progress)} 
                            strokeWidth={2}
                            dot={{ fill: getProgressColor(goal.progress), strokeWidth: 2 }}
                          />
                          <Line 
                            type="monotone" 
                            dataKey="target" 
                            stroke="#9ca3af" 
                            strokeDasharray="5 5"
                            strokeWidth={1}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Goal Details */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="flex items-center gap-2">
                      <Calendar className="w-4 h-4 text-gray-500" />
                      <div>
                        <p className="text-xs text-gray-500">Created</p>
                        <p className="text-sm font-medium">
                          {new Date(goal.created_date).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Timer className="w-4 h-4 text-gray-500" />
                      <div>
                        <p className="text-xs text-gray-500">Deadline</p>
                        <p className="text-sm font-medium">
                          {new Date(goal.deadline).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                  </div>

                  {viewMode === 'detailed' && (
                    <div className="mt-4 pt-4 border-t">
                      <Button variant="outline" size="sm" className="mr-2">
                        <Settings className="w-4 h-4 mr-2" />
                        Edit Goal
                      </Button>
                      <Button variant="ghost" size="sm">
                        View History
                      </Button>
                    </div>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </CardContent>
        </Card>
      </motion.div>
    );
  };

  if (!goals || goals.length === 0) {
    return (
      <div className="text-center py-12">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="mb-4"
        >
          <Target className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Goals Yet</h3>
          <p className="text-gray-500 mb-6">Create your first health goal to start tracking progress</p>
          <Button>
            <Target className="w-4 h-4 mr-2" />
            Create Goal
          </Button>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {viewMode === 'dashboard' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {goals.map((goal, index) => (
            <GoalCard key={goal.id} goal={goal} index={index} />
          ))}
        </div>
      )}

      {viewMode === 'detailed' && (
        <div className="space-y-6">
          {goals.map((goal, index) => (
            <GoalCard key={goal.id} goal={goal} index={index} />
          ))}
        </div>
      )}
    </div>
  );
};

export default VisualProgressCharts;