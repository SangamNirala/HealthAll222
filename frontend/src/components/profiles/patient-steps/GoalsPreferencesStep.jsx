import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import FormField from '../../shared/FormField';
import { Target, Bell, Shield, Share2, Calendar } from 'lucide-react';

const GoalsPreferencesStep = ({ data = {}, onChange, icon: Icon }) => {
  const updateField = (field, value) => {
    const updatedData = { ...data, [field]: value };
    onChange(updatedData);
  };

  const updateListField = (field, item, checked) => {
    const currentItems = data[field] || [];
    let updatedItems;
    
    if (checked) {
      updatedItems = [...currentItems, item];
    } else {
      updatedItems = currentItems.filter(i => i !== item);
    }
    
    updateField(field, updatedItems);
  };

  const updateNestedField = (parentField, childField, value) => {
    const updatedData = {
      ...data,
      [parentField]: {
        ...data[parentField],
        [childField]: value
      }
    };
    onChange(updatedData);
  };

  const addHealthTarget = () => {
    const currentTargets = data.health_targets || [];
    const newTarget = {
      id: Date.now().toString(),
      type: '',
      target: '',
      timeframe: '',
      priority: 'medium'
    };
    updateField('health_targets', [...currentTargets, newTarget]);
  };

  const updateHealthTarget = (id, field, value) => {
    const updatedTargets = (data.health_targets || []).map(target =>
      target.id === id ? { ...target, [field]: value } : target
    );
    updateField('health_targets', updatedTargets);
  };

  const removeHealthTarget = (id) => {
    const updatedTargets = (data.health_targets || []).filter(target => target.id !== id);
    updateField('health_targets', updatedTargets);
  };

  const communicationMethods = [
    'Email',
    'SMS/Text Messages',
    'Push Notifications',
    'In-App Messages',
    'Phone Calls',
    'Video Consultations'
  ];

  const targetTypes = [
    { value: 'weight', label: 'Weight Goal' },
    { value: 'exercise', label: 'Exercise/Activity' },
    { value: 'nutrition', label: 'Nutrition Goal' },
    { value: 'sleep', label: 'Sleep Goal' },
    { value: 'stress', label: 'Stress Management' },
    { value: 'health_metric', label: 'Health Metric (BP, glucose, etc.)' },
    { value: 'habit', label: 'Lifestyle Habit' },
    { value: 'medical', label: 'Medical/Clinical Goal' }
  ];

  const timeframes = [
    { value: '1_week', label: '1 Week' },
    { value: '2_weeks', label: '2 Weeks' },
    { value: '1_month', label: '1 Month' },
    { value: '3_months', label: '3 Months' },
    { value: '6_months', label: '6 Months' },
    { value: '1_year', label: '1 Year' },
    { value: 'ongoing', label: 'Ongoing' }
  ];

  const priorities = [
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-3 mb-6">
        {Icon && <Icon className="w-8 h-8 text-blue-500" />}
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Goals & Preferences</h2>
          <p className="text-gray-600">Set your health targets and customize your experience</p>
        </div>
      </div>

      {/* Health Targets */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center">
              <Target className="w-5 h-5 mr-2" />
              Health Targets
            </div>
            <button
              type="button"
              onClick={addHealthTarget}
              className="text-sm bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
            >
              Add Target
            </button>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {data.health_targets && data.health_targets.length > 0 ? (
            <div className="space-y-4">
              {data.health_targets.map((target) => (
                <div key={target.id} className="bg-gray-50 p-4 rounded-lg">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
                    <FormField
                      type="select"
                      label="Target Type"
                      value={target.type}
                      onChange={(value) => updateHealthTarget(target.id, 'type', value)}
                      options={targetTypes}
                      placeholder="Select type"
                    />
                    <FormField
                      type="input"
                      label="Target/Goal"
                      value={target.target}
                      onChange={(value) => updateHealthTarget(target.id, 'target', value)}
                      placeholder="e.g., Lose 10kg, Walk 10,000 steps"
                    />
                    <FormField
                      type="select"
                      label="Timeframe"
                      value={target.timeframe}
                      onChange={(value) => updateHealthTarget(target.id, 'timeframe', value)}
                      options={timeframes}
                      placeholder="Select timeframe"
                    />
                    <FormField
                      type="select"
                      label="Priority"
                      value={target.priority}
                      onChange={(value) => updateHealthTarget(target.id, 'priority', value)}
                      options={priorities}
                      placeholder="Select priority"
                    />
                  </div>
                  <button
                    type="button"
                    onClick={() => removeHealthTarget(target.id)}
                    className="mt-2 text-sm text-red-600 hover:text-red-800"
                  >
                    Remove Target
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <Calendar className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500">No health targets set yet.</p>
              <p className="text-sm text-gray-400">Click "Add Target" to create your first health goal.</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Communication Preferences */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Bell className="w-5 h-5 mr-2" />
            Communication & Notifications
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              Preferred Communication Methods (select all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {communicationMethods.map((method) => (
                <FormField
                  key={method}
                  type="checkbox"
                  label={method}
                  value={data.communication_methods?.includes(method)}
                  onChange={(checked) => updateListField('communication_methods', method, checked)}
                />
              ))}
            </div>
          </div>

          <div className="space-y-3">
            <h4 className="font-medium text-gray-900">Notification Preferences</h4>
            
            <FormField
              type="checkbox"
              label="Daily health reminders"
              value={data.notification_preferences?.daily_reminders}
              onChange={(value) => updateNestedField('notification_preferences', 'daily_reminders', value)}
              helpText="Reminders for meals, medications, and health tracking"
            />

            <FormField
              type="checkbox"
              label="Weekly progress reports"
              value={data.notification_preferences?.weekly_reports}
              onChange={(value) => updateNestedField('notification_preferences', 'weekly_reports', value)}
              helpText="Summary of your health progress and achievements"
            />

            <FormField
              type="checkbox"
              label="Meal planning notifications"
              value={data.notification_preferences?.meal_planning}
              onChange={(value) => updateNestedField('notification_preferences', 'meal_planning', value)}
              helpText="Reminders for meal prep and grocery shopping"
            />

            <FormField
              type="checkbox"
              label="Health tips and education"
              value={data.notification_preferences?.health_tips}
              onChange={(value) => updateNestedField('notification_preferences', 'health_tips', value)}
              helpText="Useful health and nutrition information"
            />

            <FormField
              type="checkbox"
              label="Appointment reminders"
              value={data.notification_preferences?.appointment_reminders}
              onChange={(value) => updateNestedField('notification_preferences', 'appointment_reminders', value)}
              helpText="Reminders for healthcare provider appointments"
            />

            <FormField
              type="checkbox"
              label="Goal achievement celebrations"
              value={data.notification_preferences?.goal_celebrations}
              onChange={(value) => updateNestedField('notification_preferences', 'goal_celebrations', value)}
              helpText="Congratulations when you reach your health goals"
            />
          </div>
        </CardContent>
      </Card>

      {/* Privacy Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Shield className="w-5 h-5 mr-2" />
            Privacy & Security
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <FormField
              type="checkbox"
              label="Share data with healthcare providers"
              value={data.privacy_settings?.share_with_providers}
              onChange={(value) => updateNestedField('privacy_settings', 'share_with_providers', value)}
              helpText="Allow your healthcare team to access your health data"
            />

            <FormField
              type="checkbox"
              label="Participate in anonymous research"
              value={data.privacy_settings?.anonymous_research}
              onChange={(value) => updateNestedField('privacy_settings', 'anonymous_research', value)}
              helpText="Help improve health services through anonymous data analysis"
            />

            <FormField
              type="checkbox"
              label="Allow marketing communications"
              value={data.privacy_settings?.marketing_communications}
              onChange={(value) => updateNestedField('privacy_settings', 'marketing_communications', value)}
              helpText="Receive information about new features and health products"
            />

            <FormField
              type="checkbox"
              label="Public profile visibility"
              value={data.privacy_settings?.public_profile}
              onChange={(value) => updateNestedField('privacy_settings', 'public_profile', value)}
              helpText="Allow other users to see your general progress (no personal data)"
            />
          </div>
        </CardContent>
      </Card>

      {/* Data Sharing */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Share2 className="w-5 h-5 mr-2" />
            Data Sharing Preferences
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <FormField
              type="checkbox"
              label="Share with family members"
              value={data.data_sharing_preferences?.family_access}
              onChange={(value) => updateNestedField('data_sharing_preferences', 'family_access', value)}
              helpText="Allow designated family members to view your health progress"
            />

            <FormField
              type="checkbox"
              label="Emergency medical information sharing"
              value={data.data_sharing_preferences?.emergency_sharing}
              onChange={(value) => updateNestedField('data_sharing_preferences', 'emergency_sharing', value)}
              helpText="Share critical health data with emergency responders if needed"
            />

            <FormField
              type="checkbox"
              label="Third-party app integration"
              value={data.data_sharing_preferences?.third_party_apps}
              onChange={(value) => updateNestedField('data_sharing_preferences', 'third_party_apps', value)}
              helpText="Allow integration with fitness trackers and other health apps"
            />
          </div>
        </CardContent>
      </Card>

      {/* Completion Summary */}
      <div className="bg-blue-50 p-6 rounded-lg">
        <h4 className="font-semibold text-blue-900 mb-3">🎉 Almost Done!</h4>
        <p className="text-blue-800 mb-4">
          You're about to complete your comprehensive health profile. This information will help us:
        </p>
        <ul className="text-sm text-blue-700 space-y-2">
          <li>• Create personalized meal plans based on your preferences and restrictions</li>
          <li>• Provide targeted health recommendations aligned with your goals</li>
          <li>• Send relevant reminders and notifications at the right time</li>
          <li>• Track your progress towards your specific health targets</li>
          <li>• Connect you with appropriate healthcare resources when needed</li>
        </ul>
        <div className="mt-4 p-3 bg-white rounded border-l-4 border-blue-400">
          <p className="text-sm text-gray-700">
            <strong>Remember:</strong> You can always update your profile later as your goals 
            and preferences change. Your privacy and data security are our top priorities.
          </p>
        </div>
      </div>
    </div>
  );
};

export default GoalsPreferencesStep;