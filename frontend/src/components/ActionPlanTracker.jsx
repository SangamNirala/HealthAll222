import React, { useState, useEffect } from 'react';
import {
  Calendar,
  Clock,
  Target,
  CheckCircle,
  Circle,
  TrendingUp,
  AlertCircle,
  Star,
  Activity,
  Moon,
  Sun,
  Sunset,
  ArrowRight,
  Award,
  BarChart3,
  RefreshCw,
  Heart
} from 'lucide-react';

const ActionPlanTracker = ({ actionPlan, assessmentId, userId }) => {
  const [currentDay, setCurrentDay] = useState(1);
  const [completedTasks, setCompletedTasks] = useState(new Set());
  const [progress, setProgress] = useState({});
  const [symptomRatings, setSymptomRatings] = useState({});
  const [loading, setLoading] = useState(false);

  const timeIcons = {
    morning: Sun,
    midday: Sunset,
    evening: Moon
  };

  const timeLabels = {
    morning: 'Morning Routine',
    midday: 'Midday Check-in', 
    evening: 'Evening Care'
  };

  useEffect(() => {
    // Load saved progress from localStorage for guest users
    const savedProgress = localStorage.getItem(`actionPlan_${assessmentId}`);
    if (savedProgress) {
      try {
        const parsed = JSON.parse(savedProgress);
        setCompletedTasks(new Set(parsed.completedTasks || []));
        setProgress(parsed.progress || {});
        setSymptomRatings(parsed.symptomRatings || {});
        setCurrentDay(parsed.currentDay || 1);
      } catch (error) {
        console.error('Error loading saved progress:', error);
      }
    }
  }, [assessmentId]);

  const saveProgress = () => {
    const progressData = {
      completedTasks: Array.from(completedTasks),
      progress,
      symptomRatings,
      currentDay,
      lastUpdated: new Date().toISOString()
    };
    localStorage.setItem(`actionPlan_${assessmentId}`, JSON.stringify(progressData));
  };

  const updateProgress = async (dayData) => {
    setLoading(true);
    
    try {
      // For guest users, we'll store locally and optionally sync with backend
      const response = await fetch(`${import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL}/api/symptom-checker/progress-update`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          plan_id: actionPlan?.plan_id || assessmentId,
          user_id: userId || 'guest',
          day: currentDay,
          time_of_day: dayData.time_of_day || 'evening',
          symptom_ratings: symptomRatings,
          interventions_used: Array.from(completedTasks),
          overall_improvement: dayData.overall_improvement || 5,
          quality_of_life_impact: dayData.quality_of_life_impact || 5,
          sleep_quality: dayData.sleep_quality || 5,
          energy_level: dayData.energy_level || 5,
          notes: dayData.notes || ''
        })
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Progress updated:', result);
      }
    } catch (error) {
      console.error('Error updating progress:', error);
      // Continue with local storage even if API fails
    } finally {
      setLoading(false);
      saveProgress();
    }
  };

  const toggleTask = (taskId) => {
    const newCompleted = new Set(completedTasks);
    if (newCompleted.has(taskId)) {
      newCompleted.delete(taskId);
    } else {
      newCompleted.add(taskId);
    }
    setCompletedTasks(newCompleted);
    
    // Auto-save progress
    setTimeout(() => {
      saveProgress();
    }, 100);
  };

  const updateSymptomRating = (symptom, rating) => {
    setSymptomRatings(prev => ({
      ...prev,
      [symptom]: rating
    }));
  };

  const calculateDayProgress = (day) => {
    if (!actionPlan?.daily_plans?.[`day_${day}`]) return 0;
    
    const dayPlan = actionPlan.daily_plans[`day_${day}`];
    const allTasks = [
      ...(dayPlan.morning_routine || []),
      ...(dayPlan.midday_checkpoints || []),
      ...(dayPlan.evening_routine || [])
    ];
    
    const completedCount = allTasks.filter(task => 
      completedTasks.has(`day${day}_${task}`)
    ).length;
    
    return allTasks.length > 0 ? (completedCount / allTasks.length) * 100 : 0;
  };

  const renderDaySelector = () => (
    <div className="flex justify-center mb-6">
      <div className="inline-flex bg-gray-100 rounded-lg p-1">
        {[1, 2, 3].map((day) => (
          <button
            key={day}
            onClick={() => setCurrentDay(day)}
            className={`px-6 py-3 rounded-md font-medium transition-all duration-200 ${
              currentDay === day
                ? 'bg-white text-blue-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Day {day}
            <div className="text-xs mt-1">
              {Math.round(calculateDayProgress(day))}% complete
            </div>
          </button>
        ))}
      </div>
    </div>
  );

  const renderDayPlan = () => {
    if (!actionPlan?.daily_plans?.[`day_${currentDay}`]) {
      return (
        <div className="text-center py-8 text-gray-500">
          <Calendar className="w-12 h-12 mx-auto mb-3 text-gray-400" />
          <p>No plan available for Day {currentDay}</p>
        </div>
      );
    }

    const dayPlan = actionPlan.daily_plans[`day_${currentDay}`];
    const timeSlots = ['morning_routine', 'midday_checkpoints', 'evening_routine'];

    return (
      <div className="space-y-6">
        {/* Day Focus */}
        {dayPlan.day_focus && (
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-xl p-5">
            <h3 className="font-semibold text-gray-900 mb-2 flex items-center">
              <Target className="w-5 h-5 text-blue-600 mr-2" />
              Day {currentDay} Focus
            </h3>
            <p className="text-gray-700">{dayPlan.day_focus}</p>
          </div>
        )}

        {/* Time-based Tasks */}
        {timeSlots.map((slot) => {
          const tasks = dayPlan[slot] || [];
          const SlotIcon = timeIcons[slot.split('_')[0]] || Clock;
          
          if (tasks.length === 0) return null;

          return (
            <div key={slot} className="bg-white border border-gray-200 rounded-xl p-5">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <SlotIcon className="w-5 h-5 text-blue-600" />
                </div>
                <h4 className="font-semibold text-gray-900">
                  {timeLabels[slot.split('_')[0]] || slot.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </h4>
              </div>
              
              <div className="space-y-3">
                {tasks.map((task, index) => {
                  const taskId = `day${currentDay}_${task}`;
                  const isCompleted = completedTasks.has(taskId);
                  
                  return (
                    <div
                      key={index}
                      className={`flex items-start space-x-3 p-3 rounded-lg cursor-pointer transition-all duration-200 ${
                        isCompleted
                          ? 'bg-green-50 border border-green-200'
                          : 'bg-gray-50 hover:bg-gray-100 border border-gray-200'
                      }`}
                      onClick={() => toggleTask(taskId)}
                    >
                      <button className="mt-1">
                        {isCompleted ? (
                          <CheckCircle className="w-5 h-5 text-green-600" />
                        ) : (
                          <Circle className="w-5 h-5 text-gray-400" />
                        )}
                      </button>
                      <span className={`flex-1 text-sm ${
                        isCompleted ? 'text-green-800 line-through' : 'text-gray-800'
                      }`}>
                        {task}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}

        {/* Tracking Requirements */}
        {dayPlan.tracking_requirements && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-5">
            <h4 className="font-semibold text-yellow-900 mb-3 flex items-center">
              <BarChart3 className="w-5 h-5 text-yellow-600 mr-2" />
              Today's Tracking
            </h4>
            <div className="grid gap-3">
              {Object.entries(dayPlan.tracking_requirements).map(([key, requirement]) => (
                <div key={key} className="text-sm">
                  <span className="font-medium text-yellow-800 capitalize">
                    {key.replace('_', ' ')}:
                  </span>
                  <span className="ml-2 text-yellow-700">{requirement}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderSymptomTracker = () => {
    const primarySymptoms = actionPlan?.symptom_profile?.primary_symptoms || 
                            ['Overall Wellness', 'Energy Level', 'Sleep Quality'];
    
    return (
      <div className="bg-white border border-gray-200 rounded-xl p-5">
        <h3 className="font-semibold text-gray-900 mb-4 flex items-center">
          <Activity className="w-5 h-5 text-blue-600 mr-2" />
          Symptom Intensity Check (Day {currentDay})
        </h3>
        
        <div className="space-y-4">
          {primarySymptoms.map((symptom) => (
            <div key={symptom} className="space-y-2">
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-700 capitalize">
                  {symptom.replace('_', ' ')}
                </label>
                <span className="text-sm text-gray-500">
                  {symptomRatings[symptom] || 5}/10
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="10"
                value={symptomRatings[symptom] || 5}
                onChange={(e) => updateSymptomRating(symptom, parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                style={{
                  background: `linear-gradient(to right, #ef4444 0%, #f59e0b 50%, #10b981 100%)`
                }}
              />
              <div className="flex justify-between text-xs text-gray-500">
                <span>Better</span>
                <span>Same</span>
                <span>Worse</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderMilestones = () => {
    const milestones = actionPlan?.progress_milestones || [];
    
    return (
      <div className="bg-white border border-gray-200 rounded-xl p-5">
        <h3 className="font-semibold text-gray-900 mb-4 flex items-center">
          <Award className="w-5 h-5 text-purple-600 mr-2" />
          Progress Milestones
        </h3>
        
        <div className="space-y-3">
          {milestones.map((milestone, index) => {
            const isUpcoming = index + 1 === currentDay;
            const isPast = index + 1 < currentDay;
            
            return (
              <div
                key={index}
                className={`p-4 rounded-lg border-2 ${
                  isPast
                    ? 'border-green-200 bg-green-50'
                    : isUpcoming
                    ? 'border-blue-200 bg-blue-50'
                    : 'border-gray-200 bg-gray-50'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center font-semibold text-sm ${
                    isPast
                      ? 'bg-green-500 text-white'
                      : isUpcoming
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-300 text-gray-600'
                  }`}>
                    {isPast ? <CheckCircle className="w-4 h-4" /> : index + 1}
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">{milestone.milestone}</h4>
                    <p className="text-sm text-gray-600">{milestone.target_time}</p>
                    <p className="text-xs text-gray-500">{milestone.success_criteria}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const renderProgressSummary = () => {
    const overallProgress = [1, 2, 3].reduce((sum, day) => sum + calculateDayProgress(day), 0) / 3;
    
    return (
      <div className="bg-gradient-to-br from-blue-50 to-purple-50 border border-blue-200 rounded-xl p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-gray-900 flex items-center">
            <TrendingUp className="w-5 h-5 text-blue-600 mr-2" />
            3-Day Progress Summary
          </h3>
          <span className="text-2xl font-bold text-blue-600">
            {Math.round(overallProgress)}%
          </span>
        </div>
        
        <div className="grid grid-cols-3 gap-4 mb-4">
          {[1, 2, 3].map((day) => {
            const progress = calculateDayProgress(day);
            return (
              <div key={day} className="text-center">
                <div className="text-sm font-medium text-gray-700">Day {day}</div>
                <div className="text-lg font-bold text-blue-600">{Math.round(progress)}%</div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
              </div>
            );
          })}
        </div>
        
        <div className="text-center">
          <button
            onClick={() => updateProgress({ time_of_day: 'evening', overall_improvement: 6 })}
            disabled={loading}
            className="flex items-center justify-center w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                Saving Progress...
              </>
            ) : (
              <>
                <Heart className="w-4 h-4 mr-2" />
                Update Progress
              </>
            )}
          </button>
        </div>
      </div>
    );
  };

  if (!actionPlan) {
    return (
      <div className="bg-white border border-gray-200 rounded-xl p-8 text-center">
        <Calendar className="w-12 h-12 mx-auto mb-3 text-gray-400" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Action Plan Available</h3>
        <p className="text-gray-600">Complete a symptom assessment to get your personalized 3-day action plan.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          3-Day Action Plan Tracker
        </h2>
        <p className="text-gray-600">
          {actionPlan.title || 'Your Personalized Wellness Plan'}
        </p>
      </div>

      {/* Day Selector */}
      {renderDaySelector()}

      {/* Two Column Layout */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left Column - Day Plan */}
        <div className="lg:col-span-2 space-y-6">
          {renderDayPlan()}
        </div>
        
        {/* Right Column - Tracking */}
        <div className="space-y-6">
          {renderSymptomTracker()}
          {renderMilestones()}
          {renderProgressSummary()}
        </div>
      </div>

      {/* Success Metrics */}
      {actionPlan.success_metrics && (
        <div className="bg-white border border-gray-200 rounded-xl p-5">
          <h3 className="font-semibold text-gray-900 mb-3 flex items-center">
            <Star className="w-5 h-5 text-yellow-600 mr-2" />
            Success Goals
          </h3>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-700">Primary Goal:</span>
              <div className="text-gray-600">{actionPlan.success_metrics.target_improvement}</div>
            </div>
            <div>
              <span className="font-medium text-gray-700">Minimum Success:</span>
              <div className="text-gray-600">{actionPlan.success_metrics.minimum_acceptable}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ActionPlanTracker;