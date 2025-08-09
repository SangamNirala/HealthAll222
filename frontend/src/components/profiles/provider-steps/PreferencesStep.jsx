import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import FormField from '../../shared/FormField';
import { Settings, Clock, Users, Shield, Calendar } from 'lucide-react';

const PreferencesStep = ({ data = {}, onChange, icon: Icon }) => {
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

  const updateWorkingHours = (field, value) => {
    const updatedData = {
      ...data,
      working_hours: {
        ...data.working_hours,
        [field]: value
      }
    };
    onChange(updatedData);
  };

  const updateScheduleDay = (day, timeType, value) => {
    const updatedData = {
      ...data,
      working_hours: {
        ...data.working_hours,
        schedule: {
          ...data.working_hours?.schedule,
          [day]: {
            ...data.working_hours?.schedule?.[day],
            [timeType]: value
          }
        }
      }
    };
    onChange(updatedData);
  };

  const consultationTypes = [
    {
      value: 'IN_PERSON',
      label: 'In-Person Consultations',
      description: 'Face-to-face appointments at your practice'
    },
    {
      value: 'VIDEO',
      label: 'Video Consultations',
      description: 'Video calls via secure platform'
    },
    {
      value: 'PHONE',
      label: 'Phone Consultations',
      description: 'Audio-only consultations'
    },
    {
      value: 'CHAT',
      label: 'Chat/Messaging',
      description: 'Text-based communication'
    }
  ];

  const timezoneOptions = [
    { value: 'America/New_York', label: 'Eastern Time (ET)' },
    { value: 'America/Chicago', label: 'Central Time (CT)' },
    { value: 'America/Denver', label: 'Mountain Time (MT)' },
    { value: 'America/Los_Angeles', label: 'Pacific Time (PT)' },
    { value: 'America/Anchorage', label: 'Alaska Time (AKT)' },
    { value: 'Pacific/Honolulu', label: 'Hawaii Time (HT)' },
  ];

  const specializedConditions = [
    'Type 1 Diabetes',
    'Type 2 Diabetes',
    'Gestational Diabetes',
    'Cardiovascular Disease',
    'Hypertension',
    'Hyperlipidemia',
    'Chronic Kidney Disease',
    'Celiac Disease',
    'Crohn\'s Disease',
    'Ulcerative Colitis',
    'PCOS',
    'Thyroid Disorders',
    'Eating Disorders',
    'Obesity',
    'Malnutrition',
    'Food Allergies'
  ];

  const treatmentPhilosophies = [
    'Evidence-Based Practice',
    'Patient-Centered Care',
    'Holistic Approach',
    'Behavioral Change Focus',
    'Medical Nutrition Therapy',
    'Motivational Interviewing',
    'Mindful Eating',
    'Intuitive Eating',
    'Plant-Based Nutrition',
    'Functional Medicine',
    'Integrative Medicine',
    'Cultural Competency Focus'
  ];

  const daysOfWeek = [
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'
  ];

  const dayLabels = {
    monday: 'Monday',
    tuesday: 'Tuesday', 
    wednesday: 'Wednesday',
    thursday: 'Thursday',
    friday: 'Friday',
    saturday: 'Saturday',
    sunday: 'Sunday'
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-3 mb-6">
        {Icon && <Icon className="w-8 h-8 text-emerald-500" />}
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Practice Preferences</h2>
          <p className="text-gray-600">Configure your availability and practice preferences</p>
        </div>
      </div>

      {/* Consultation Types */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Users className="w-5 h-5 mr-2" />
            Consultation Types
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              How do you prefer to conduct consultations? (select all that apply)
            </label>
            <div className="space-y-3">
              {consultationTypes.map((type) => (
                <div key={type.value} className="flex items-start space-x-3">
                  <FormField
                    type="checkbox"
                    label=""
                    value={data.consultation_types?.includes(type.value)}
                    onChange={(checked) => updateListField('consultation_types', type.value, checked)}
                  />
                  <div className="flex-1">
                    <div className="font-medium text-gray-900">{type.label}</div>
                    <div className="text-sm text-gray-500">{type.description}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Working Hours */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Clock className="w-5 h-5 mr-2" />
            Working Hours & Availability
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <FormField
            type="select"
            label="Timezone"
            value={data.working_hours?.timezone}
            onChange={(value) => updateWorkingHours('timezone', value)}
            placeholder="Select your timezone"
            options={timezoneOptions}
            required
            helpText="Used for scheduling appointments"
          />

          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              Weekly Schedule
            </label>
            <div className="space-y-3">
              {daysOfWeek.map((day) => (
                <div key={day} className="grid grid-cols-3 gap-3 items-center">
                  <div className="font-medium text-gray-900 capitalize">
                    {dayLabels[day]}
                  </div>
                  <FormField
                    type="input"
                    label="Start Time"
                    value={data.working_hours?.schedule?.[day]?.start || ''}
                    onChange={(value) => updateScheduleDay(day, 'start', value)}
                    placeholder="09:00"
                    helpText="24-hour format"
                  />
                  <FormField
                    type="input"
                    label="End Time"
                    value={data.working_hours?.schedule?.[day]?.end || ''}
                    onChange={(value) => updateScheduleDay(day, 'end', value)}
                    placeholder="17:00"
                    helpText="24-hour format"
                  />
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Patient Management */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Calendar className="w-5 h-5 mr-2" />
            Patient Management Preferences
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField
              type="number"
              label="Maximum Patients"
              value={data.max_patients}
              onChange={(value) => updateField('max_patients', parseInt(value) || 0)}
              placeholder="100"
              min="1"
              max="1000"
              required
              helpText="Maximum number of patients in your practice"
            />

            <FormField
              type="select"
              label="Accepting New Patients"
              value={data.accepting_new_patients}
              onChange={(value) => updateField('accepting_new_patients', value === 'true')}
              options={[
                { value: 'true', label: 'Yes - Accepting new patients' },
                { value: 'false', label: 'No - Not accepting new patients' }
              ]}
              required
            />
          </div>

          <FormField
            type="number"
            label="Typical Appointment Duration (minutes)"
            value={data.appointment_duration}
            onChange={(value) => updateField('appointment_duration', parseInt(value) || 0)}
            placeholder="45"
            min="15"
            max="180"
            helpText="Standard length for new patient appointments"
          />

          <FormField
            type="number"
            label="Follow-up Appointment Duration (minutes)"
            value={data.followup_duration}
            onChange={(value) => updateField('followup_duration', parseInt(value) || 0)}
            placeholder="30"
            min="15"
            max="120"
            helpText="Standard length for follow-up appointments"
          />
        </CardContent>
      </Card>

      {/* Specialized Conditions */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Shield className="w-5 h-5 mr-2" />
            Clinical Specializations
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              Specialized conditions you treat (select all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {specializedConditions.map((condition) => (
                <FormField
                  key={condition}
                  type="checkbox"
                  label={condition}
                  value={data.specialized_conditions?.includes(condition)}
                  onChange={(checked) => updateListField('specialized_conditions', condition, checked)}
                />
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Treatment Philosophy */}
      <Card>
        <CardHeader>
          <CardTitle>Treatment Philosophy & Approach</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              Treatment philosophies you follow (select all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {treatmentPhilosophies.map((philosophy) => (
                <FormField
                  key={philosophy}
                  type="checkbox"
                  label={philosophy}
                  value={data.treatment_philosophies?.includes(philosophy)}
                  onChange={(checked) => updateListField('treatment_philosophies', philosophy, checked)}
                />
              ))}
            </div>
          </div>

          <FormField
            type="textarea"
            label="Additional Treatment Approaches"
            value={data.additional_approaches}
            onChange={(value) => updateField('additional_approaches', value)}
            placeholder="Describe any other treatment approaches or methodologies you use"
            rows={3}
            helpText="Include any specialized techniques or unique approaches"
          />
        </CardContent>
      </Card>

      {/* Communication Preferences */}
      <Card>
        <CardHeader>
          <CardTitle>Communication Preferences</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <FormField
            type="select"
            label="Preferred Patient Communication Method"
            value={data.preferred_communication}
            onChange={(value) => updateField('preferred_communication', value)}
            options={[
              { value: 'email', label: 'Email' },
              { value: 'phone', label: 'Phone' },
              { value: 'patient_portal', label: 'Patient Portal' },
              { value: 'secure_messaging', label: 'Secure Messaging Platform' }
            ]}
            helpText="How you prefer to communicate with patients outside appointments"
          />

          <FormField
            type="number"
            label="Response Time (hours)"
            value={data.response_time_hours}
            onChange={(value) => updateField('response_time_hours', parseInt(value) || 0)}
            placeholder="24"
            min="1"
            max="168"
            helpText="Typical response time for patient messages"
          />

          <FormField
            type="checkbox"
            label="Emergency consultations available"
            value={data.emergency_consultations}
            onChange={(value) => updateField('emergency_consultations', value)}
            helpText="Can you provide urgent/emergency nutrition consultations?"
          />
        </CardContent>
      </Card>

      {/* Profile Completion Summary */}
      <div className="bg-emerald-50 p-6 rounded-lg">
        <h4 className="font-semibold text-emerald-900 mb-3">🎉 Professional Profile Complete!</h4>
        <p className="text-emerald-800 mb-4">
          Your professional profile is almost ready! Here's what happens next:
        </p>
        <ul className="text-sm text-emerald-700 space-y-2">
          <li>• <strong>Credential Verification:</strong> We'll verify your licenses and certifications (2-3 business days)</li>
          <li>• <strong>Profile Review:</strong> Our team will review your profile for completeness and accuracy</li>
          <li>• <strong>Platform Access:</strong> You'll receive full access to provider tools and patient management</li>
          <li>• <strong>Patient Discovery:</strong> Patients can find and connect with you based on your specializations</li>
          <li>• <strong>Professional Network:</strong> Connect with other healthcare professionals on the platform</li>
        </ul>
        <div className="mt-4 p-3 bg-white rounded border-l-4 border-emerald-400">
          <p className="text-sm text-gray-700">
            <strong>Note:</strong> You can update your profile, availability, and preferences at any time 
            through your provider dashboard. Patient care and professional standards are our top priorities.
          </p>
        </div>
      </div>
    </div>
  );
};

export default PreferencesStep;