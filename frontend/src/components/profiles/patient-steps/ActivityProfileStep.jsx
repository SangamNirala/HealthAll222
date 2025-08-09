import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import FormField from '../../shared/FormField';
import { Activity, Moon, Briefcase, Zap } from 'lucide-react';

const ActivityProfileStep = ({ data = {}, onChange, icon: Icon }) => {
  const updateField = (field, value) => {
    const updatedData = { ...data, [field]: value };
    onChange(updatedData);
  };

  const updateSleepSchedule = (field, value) => {
    const updatedData = {
      ...data,
      sleep_schedule: {
        ...data.sleep_schedule,
        [field]: value
      }
    };
    onChange(updatedData);
  };

  const updateExerciseTypes = (type, checked) => {
    const currentTypes = data.exercise_types || [];
    let updatedTypes;
    
    if (checked) {
      updatedTypes = [...currentTypes, type];
    } else {
      updatedTypes = currentTypes.filter(t => t !== type);
    }
    
    updateField('exercise_types', updatedTypes);
  };

  const activityLevels = [
    { 
      value: 'SEDENTARY', 
      label: 'Sedentary',
      description: 'Little or no exercise, desk job'
    },
    { 
      value: 'LIGHTLY_ACTIVE', 
      label: 'Lightly Active',
      description: 'Light exercise 1-3 days/week'
    },
    { 
      value: 'MODERATELY_ACTIVE', 
      label: 'Moderately Active',
      description: 'Moderate exercise 3-5 days/week'
    },
    { 
      value: 'VERY_ACTIVE', 
      label: 'Very Active',
      description: 'Hard exercise 6-7 days/week'
    },
    { 
      value: 'EXTRA_ACTIVE', 
      label: 'Extra Active',
      description: 'Very hard exercise, physical job'
    }
  ];

  const workTypes = [
    { value: 'DESK_JOB', label: 'Desk Job', description: 'Mostly sitting' },
    { value: 'PHYSICAL_WORK', label: 'Physical Work', description: 'Mostly standing/moving' },
    { value: 'MIXED', label: 'Mixed', description: 'Combination of sitting and standing' },
    { value: 'STUDENT', label: 'Student', description: 'Studying/attending classes' },
    { value: 'RETIRED', label: 'Retired', description: 'Not working' }
  ];

  const exerciseTypeOptions = [
    'Cardio (Running, Cycling)',
    'Strength Training',
    'Yoga/Pilates',
    'Swimming',
    'Sports (Team/Individual)',
    'Walking/Hiking',
    'Dancing',
    'Martial Arts',
    'Rock Climbing',
    'Other'
  ];

  const sleepQualityLabels = [
    'Very Poor',
    'Poor', 
    'Fair',
    'Good',
    'Excellent'
  ];

  const stressLevelLabels = [
    'Very Low',
    'Low',
    'Moderate', 
    'High',
    'Very High'
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-3 mb-6">
        {Icon && <Icon className="w-8 h-8 text-blue-500" />}
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Activity & Lifestyle</h2>
          <p className="text-gray-600">Tell us about your daily activity and lifestyle habits</p>
        </div>
      </div>

      {/* Activity Level */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Activity className="w-5 h-5 mr-2" />
            Activity Level
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <FormField
            type="radio"
            label="Overall Activity Level"
            value={data.activity_level}
            onChange={(value) => updateField('activity_level', value)}
            options={activityLevels.map(level => ({
              value: level.value,
              label: (
                <div>
                  <div className="font-medium">{level.label}</div>
                  <div className="text-sm text-gray-500">{level.description}</div>
                </div>
              )
            }))}
            required
          />
        </CardContent>
      </Card>

      {/* Exercise Details */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Zap className="w-5 h-5 mr-2" />
            Exercise Preferences
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <FormField
            type="number"
            label="Exercise Frequency (days per week)"
            value={data.exercise_frequency}
            onChange={(value) => updateField('exercise_frequency', parseInt(value) || 0)}
            placeholder="3"
            min="0"
            max="7"
            required
            helpText="How many days per week do you typically exercise?"
          />

          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              Types of Exercise You Enjoy (select all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {exerciseTypeOptions.map((type) => (
                <FormField
                  key={type}
                  type="checkbox"
                  label={type}
                  value={data.exercise_types?.includes(type)}
                  onChange={(checked) => updateExerciseTypes(type, checked)}
                />
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Sleep Schedule */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Moon className="w-5 h-5 mr-2" />
            Sleep Schedule
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField
              type="input"
              label="Usual Bedtime"
              value={data.sleep_schedule?.bedtime}
              onChange={(value) => updateSleepSchedule('bedtime', value)}
              placeholder="23:00"
              helpText="24-hour format (e.g., 23:00)"
            />

            <FormField
              type="input"
              label="Usual Wake Time"
              value={data.sleep_schedule?.wake_time}
              onChange={(value) => updateSleepSchedule('wake_time', value)}
              placeholder="07:00"
              helpText="24-hour format (e.g., 07:00)"
            />
          </div>

          <FormField
            type="radio"
            label="Sleep Quality"
            value={data.sleep_schedule?.sleep_quality}
            onChange={(value) => updateSleepSchedule('sleep_quality', parseInt(value))}
            options={sleepQualityLabels.map((label, index) => ({
              value: (index + 1).toString(),
              label: `${index + 1} - ${label}`
            }))}
            helpText="Rate your overall sleep quality"
          />
        </CardContent>
      </Card>

      {/* Work & Stress */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Briefcase className="w-5 h-5 mr-2" />
            Work & Stress Levels
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <FormField
            type="radio"
            label="Work Type"
            value={data.work_type}
            onChange={(value) => updateField('work_type', value)}
            options={workTypes.map(work => ({
              value: work.value,
              label: (
                <div>
                  <div className="font-medium">{work.label}</div>
                  <div className="text-sm text-gray-500">{work.description}</div>
                </div>
              )
            }))}
            required
          />

          <FormField
            type="radio"
            label="Stress Level"
            value={data.stress_level}
            onChange={(value) => updateField('stress_level', parseInt(value))}
            options={stressLevelLabels.map((label, index) => ({
              value: (index + 1).toString(),
              label: `${index + 1} - ${label}`
            }))}
            helpText="Rate your typical daily stress level"
          />
        </CardContent>
      </Card>

      {/* Activity Tips */}
      <div className="bg-blue-50 p-4 rounded-lg">
        <h4 className="font-medium text-blue-900 mb-2">Activity & Lifestyle Tips</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Regular physical activity improves metabolism and overall health</li>
          <li>• Quality sleep (7-9 hours) is crucial for recovery and weight management</li>
          <li>• Managing stress helps prevent emotional eating and hormone imbalances</li>
          <li>• Even light activities like walking can make a significant difference</li>
        </ul>
      </div>
    </div>
  );
};

export default ActivityProfileStep;