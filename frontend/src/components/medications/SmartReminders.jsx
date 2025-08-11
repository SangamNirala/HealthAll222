import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  Brain,
  Clock,
  Zap,
  AlertTriangle,
  TrendingUp,
  Settings,
  Bell,
  BellOff,
  Calendar,
  Utensils,
  Moon,
  Sun,
  Activity,
  CheckCircle,
  XCircle,
  Target,
  RefreshCw
} from 'lucide-react';

import { 
  SmartReminderScheduler, 
  REMINDER_INTENSITY,
  MEAL_TIMES 
} from '../../utils/reminderScheduling';

const SmartReminders = ({ 
  medications = [], 
  adherenceData = [], 
  userPreferences = {},
  onReminderUpdate,
  onScheduleChange 
}) => {
  const [scheduler, setScheduler] = useState(null);
  const [smartSchedules, setSmartSchedules] = useState({});
  const [activeReminders, setActiveReminders] = useState([]);
  const [snoozeStates, setSnoozeStates] = useState({});
  const [escalationStates, setEscalationStates] = useState({});
  const [isEnabled, setIsEnabled] = useState(true);
  const [loading, setLoading] = useState(false);

  // Initialize scheduler with user preferences
  useEffect(() => {
    const smartScheduler = new SmartReminderScheduler(userPreferences);
    setScheduler(smartScheduler);
  }, [userPreferences]);

  // Generate smart schedules for all medications
  const generateSmartSchedules = useCallback(async () => {
    if (!scheduler || !medications.length) return;

    setLoading(true);
    const schedules = {};
    
    for (const medication of medications) {
      if (medication.status === 'active') {
        const smartSchedule = scheduler.getSmartSchedule(medication, adherenceData);
        schedules[medication.id] = smartSchedule;
      }
    }
    
    setSmartSchedules(schedules);
    setLoading(false);

    // Notify parent component of schedule changes
    if (onScheduleChange) {
      onScheduleChange(schedules);
    }
  }, [scheduler, medications, adherenceData, onScheduleChange]);

  // Generate schedules when data changes
  useEffect(() => {
    generateSmartSchedules();
  }, [generateSmartSchedules]);

  // Handle smart snooze
  const handleSmartSnooze = (reminderId, medicationId) => {
    if (!scheduler) return;

    const medication = medications.find(m => m.id === medicationId);
    const currentSnoozeCount = snoozeStates[reminderId] || 0;
    
    const reminder = {
      id: reminderId,
      medication,
      scheduled_time: new Date().toISOString() // Current time for demo
    };

    const snoozeRecommendation = scheduler.calculateSmartSnooze(reminder, currentSnoozeCount);
    
    // Update snooze state
    setSnoozeStates(prev => ({
      ...prev,
      [reminderId]: currentSnoozeCount + 1
    }));

    // Update active reminders with new timing
    setActiveReminders(prev => prev.map(r => 
      r.id === reminderId 
        ? { 
            ...r, 
            next_reminder: snoozeRecommendation.nextReminderTime,
            intensity: snoozeRecommendation.intensity,
            snooze_count: currentSnoozeCount + 1,
            snooze_reason: snoozeRecommendation.reason
          }
        : r
    ));

    // Handle escalation if needed
    if (snoozeRecommendation.escalation) {
      handleEscalation(medicationId, 'SNOOZE_ESCALATION');
    }

    if (onReminderUpdate) {
      onReminderUpdate({
        type: 'SNOOZE',
        reminderId,
        medicationId,
        snoozeData: snoozeRecommendation
      });
    }
  };

  // Handle emergency escalation
  const handleEscalation = (medicationId, reason) => {
    if (!scheduler) return;

    const medication = medications.find(m => m.id === medicationId);
    const reminder = { medication };
    
    const escalationPlan = scheduler.calculateEmergencyEscalation(reminder, adherenceData);
    
    setEscalationStates(prev => ({
      ...prev,
      [medicationId]: {
        level: escalationPlan.escalationLevel,
        actions: escalationPlan.actions,
        triggered_at: new Date().toISOString(),
        reason
      }
    }));

    if (onReminderUpdate) {
      onReminderUpdate({
        type: 'ESCALATION',
        medicationId,
        escalationData: escalationPlan
      });
    }
  };

  // Track adherence event
  const trackAdherenceEvent = (medicationId, eventData) => {
    if (!scheduler) return;

    scheduler.trackAdherence(medicationId, eventData);
    
    // Regenerate schedules with new data
    setTimeout(() => {
      generateSmartSchedules();
    }, 1000);
  };

  // Get intensity indicator color
  const getIntensityColor = (intensity) => {
    switch (intensity?.priority) {
      case 1: return 'bg-blue-100 text-blue-800';
      case 2: return 'bg-green-100 text-green-800';
      case 3: return 'bg-yellow-100 text-yellow-800';
      case 4: return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getConfidenceIcon = (confidence) => {
    switch (confidence) {
      case 'high': return <Target className="w-4 h-4 text-green-600" />;
      case 'medium': return <TrendingUp className="w-4 h-4 text-yellow-600" />;
      case 'low': return <RefreshCw className="w-4 h-4 text-gray-600" />;
      default: return <RefreshCw className="w-4 h-4 text-gray-600" />;
    }
  };

  const formatTime = (time) => {
    return new Date(`2000-01-01T${time}:00`).toLocaleTimeString([], { 
      hour: 'numeric', 
      minute: '2-digit' 
    });
  };

  if (!scheduler) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="text-center text-gray-500">
            <Brain className="w-12 h-12 mx-auto mb-2 text-gray-400" />
            <div>Initializing Smart Reminder System...</div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Smart Reminders Header */}
      <Card className="border-2 border-purple-200 bg-gradient-to-r from-purple-50 to-blue-50">
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span className="flex items-center">
              <Brain className="w-6 h-6 mr-3 text-purple-600" />
              Smart Reminder System
              {!isEnabled && <Badge variant="secondary" className="ml-2">Disabled</Badge>}
            </span>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsEnabled(!isEnabled)}
                className={isEnabled ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}
              >
                {isEnabled ? <Bell className="w-4 h-4" /> : <BellOff className="w-4 h-4" />}
                {isEnabled ? 'Enabled' : 'Disabled'}
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={generateSmartSchedules}
                disabled={loading}
              >
                {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <RefreshCw className="w-4 h-4" />}
                Optimize
              </Button>
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-sm text-gray-600 mb-4">
            AI-powered medication reminders that adapt to your meal times, sleep schedule, and adherence patterns.
          </div>
          
          {/* Quick Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-3 bg-white rounded-lg border">
              <Clock className="w-6 h-6 mx-auto mb-1 text-blue-600" />
              <div className="text-sm font-semibold">{Object.keys(smartSchedules).length}</div>
              <div className="text-xs text-gray-500">Optimized</div>
            </div>
            <div className="text-center p-3 bg-white rounded-lg border">
              <Utensils className="w-6 h-6 mx-auto mb-1 text-green-600" />
              <div className="text-sm font-semibold">
                {medications.filter(m => m.with_food).length}
              </div>
              <div className="text-xs text-gray-500">Meal-Based</div>
            </div>
            <div className="text-center p-3 bg-white rounded-lg border">
              <AlertTriangle className="w-6 h-6 mx-auto mb-1 text-orange-600" />
              <div className="text-sm font-semibold">
                {Object.keys(escalationStates).length}
              </div>
              <div className="text-xs text-gray-500">Escalated</div>
            </div>
            <div className="text-center p-3 bg-white rounded-lg border">
              <Activity className="w-6 h-6 mx-auto mb-1 text-purple-600" />
              <div className="text-sm font-semibold">
                {adherenceData.filter(d => d.taken).length || 0}
              </div>
              <div className="text-xs text-gray-500">Learned</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Smart Schedules Display */}
      {isEnabled && (
        <div className="space-y-4">
          {Object.entries(smartSchedules).map(([medicationId, schedule]) => {
            const medication = medications.find(m => m.id === medicationId);
            const escalation = escalationStates[medicationId];
            
            return (
              <Card key={medicationId} className="border-l-4 border-l-blue-500">
                <CardHeader className="pb-3">
                  <CardTitle className="flex items-center justify-between text-lg">
                    <span className="flex items-center">
                      <div className="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
                      {medication?.name}
                      <Badge variant="secondary" className="ml-2 text-xs">
                        {medication?.dosage}
                      </Badge>
                    </span>
                    <div className="flex items-center space-x-2">
                      {getConfidenceIcon(schedule.confidence)}
                      <Badge className={getIntensityColor(REMINDER_INTENSITY.NORMAL)}>
                        Smart Optimized
                      </Badge>
                    </div>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Meal-Optimized Times */}
                  <div>
                    <div className="flex items-center mb-2">
                      <Utensils className="w-4 h-4 mr-2 text-green-600" />
                      <span className="text-sm font-medium">
                        {medication?.with_food ? 'Meal-Based Schedule' : 'Between-Meal Schedule'}
                      </span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {schedule.meal_optimized_times?.map((time, idx) => (
                        <Badge key={idx} variant="outline" className="bg-green-50">
                          {formatTime(time)}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  {/* Adaptive Schedule */}
                  {schedule.adaptive_schedule && (
                    <div>
                      <div className="flex items-center mb-2">
                        <Brain className="w-4 h-4 mr-2 text-purple-600" />
                        <span className="text-sm font-medium">AI-Adapted Schedule</span>
                        <Badge variant="secondary" className="ml-2 text-xs">
                          {schedule.adaptive_schedule.confidence}
                        </Badge>
                      </div>
                      <div className="flex flex-wrap gap-2 mb-2">
                        {schedule.adaptive_schedule.recommended_times?.map((time, idx) => (
                          <Badge key={idx} variant="outline" className="bg-purple-50">
                            {formatTime(time)}
                          </Badge>
                        ))}
                      </div>
                      {schedule.adaptive_schedule.reason && (
                        <div className="text-xs text-gray-600 italic">
                          {schedule.adaptive_schedule.reason}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Emergency Escalation Status */}
                  {escalation && (
                    <div className="bg-red-50 border border-red-200 rounded-md p-3">
                      <div className="flex items-center mb-2">
                        <AlertTriangle className="w-4 h-4 mr-2 text-red-600" />
                        <span className="text-sm font-medium text-red-800">
                          Escalation Active: {escalation.level}
                        </span>
                      </div>
                      <div className="text-xs text-red-700">
                        Triggered: {new Date(escalation.triggered_at).toLocaleString()}
                      </div>
                      <div className="text-xs text-red-600 mt-1">
                        Reason: {escalation.reason}
                      </div>
                    </div>
                  )}

                  {/* Actions */}
                  <div className="flex items-center space-x-2 pt-2 border-t">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleSmartSnooze(`reminder_${medicationId}`, medicationId)}
                      className="text-xs"
                    >
                      <Clock className="w-3 h-3 mr-1" />
                      Smart Snooze
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => trackAdherenceEvent(medicationId, {
                        scheduled_time: new Date().toISOString(),
                        actual_time: new Date().toISOString(),
                        taken: true
                      })}
                      className="text-xs bg-green-50 border-green-200"
                    >
                      <CheckCircle className="w-3 h-3 mr-1" />
                      Mark Taken
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => trackAdherenceEvent(medicationId, {
                        scheduled_time: new Date().toISOString(),
                        taken: false,
                        reason_missed: 'User reported'
                      })}
                      className="text-xs bg-red-50 border-red-200"
                    >
                      <XCircle className="w-3 h-3 mr-1" />
                      Mark Missed
                    </Button>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}

      {/* Configuration Panel */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Settings className="w-5 h-5 mr-2 text-gray-600" />
            Smart Reminder Configuration
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Meal Times Display */}
            <div>
              <h4 className="text-sm font-medium mb-2 flex items-center">
                <Utensils className="w-4 h-4 mr-2 text-green-600" />
                Meal Time Preferences
              </h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Breakfast:</span>
                  <span className="text-gray-600">
                    {formatTime(userPreferences.mealTimes?.BREAKFAST?.optimal || MEAL_TIMES.BREAKFAST.optimal)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Lunch:</span>
                  <span className="text-gray-600">
                    {formatTime(userPreferences.mealTimes?.LUNCH?.optimal || MEAL_TIMES.LUNCH.optimal)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Dinner:</span>
                  <span className="text-gray-600">
                    {formatTime(userPreferences.mealTimes?.DINNER?.optimal || MEAL_TIMES.DINNER.optimal)}
                  </span>
                </div>
              </div>
            </div>

            {/* Sleep Schedule Display */}
            <div>
              <h4 className="text-sm font-medium mb-2 flex items-center">
                <Moon className="w-4 h-4 mr-2 text-indigo-600" />
                Sleep Schedule
              </h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Wake up:</span>
                  <span className="text-gray-600">
                    {formatTime(userPreferences.sleepSchedule?.wakeup || '07:00')}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Bedtime:</span>
                  <span className="text-gray-600">
                    {formatTime(userPreferences.sleepSchedule?.bedtime || '22:00')}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-4 p-3 bg-blue-50 rounded-md border-l-4 border-blue-400">
            <div className="text-sm text-blue-900">
              <strong>Smart Features Active:</strong>
              <ul className="mt-1 list-disc list-inside text-xs space-y-1">
                <li>Meal-based timing optimization for food-dependent medications</li>
                <li>Adaptive scheduling based on your adherence patterns</li>
                <li>Progressive snooze intelligence to prevent missed doses</li>
                <li>Emergency escalation for critical medications</li>
                <li>Continuous learning from your behavior patterns</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SmartReminders;