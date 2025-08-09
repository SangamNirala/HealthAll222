import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import FormField from '../../shared/FormField';
import { Building, Users, Globe, MapPin } from 'lucide-react';

const PracticeInfoStep = ({ data = {}, onChange, icon: Icon }) => {
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

  const practiceTypes = [
    { 
      value: 'Hospital', 
      label: 'Hospital',
      description: 'Acute care hospital setting'
    },
    { 
      value: 'Outpatient Clinic', 
      label: 'Outpatient Clinic',
      description: 'Ambulatory care clinic'
    },
    { 
      value: 'Private Practice', 
      label: 'Private Practice',
      description: 'Independent practice'
    },
    { 
      value: 'Group Practice', 
      label: 'Group Practice',
      description: 'Multi-provider practice'
    },
    { 
      value: 'Academic Medical Center', 
      label: 'Academic Medical Center',
      description: 'Teaching hospital/university'
    },
    { 
      value: 'Telehealth', 
      label: 'Telehealth',
      description: 'Virtual/remote practice'
    },
    { 
      value: 'Corporate Wellness', 
      label: 'Corporate Wellness',
      description: 'Employee health programs'
    },
    { 
      value: 'Community Health', 
      label: 'Community Health Center',
      description: 'Community-based care'
    }
  ];

  const patientDemographics = [
    'Pediatric (0-17 years)',
    'Young Adults (18-35 years)',
    'Middle Age (36-64 years)',
    'Elderly (65+ years)',
    'Pregnant/Lactating Women',
    'Athletes',
    'Chronic Disease Patients',
    'Post-Surgical Patients',
    'Mental Health Patients',
    'Low-Income Populations',
    'Rural Communities',
    'Urban Populations'
  ];

  const languageOptions = [
    'English',
    'Spanish',
    'French',
    'German',
    'Italian',
    'Portuguese',
    'Chinese (Mandarin)',
    'Chinese (Cantonese)',
    'Japanese',
    'Korean',
    'Arabic',
    'Russian',
    'Hindi',
    'Tagalog',
    'Vietnamese'
  ];

  const expertiseAreas = [
    'Weight Management',
    'Diabetes Management',
    'Heart Disease',
    'Kidney Disease',
    'Gastrointestinal Disorders',
    'Food Allergies/Intolerances',
    'Eating Disorders',
    'Sports Nutrition',
    'Pediatric Nutrition',
    'Geriatric Nutrition',
    'Pregnancy Nutrition',
    'Cancer Nutrition',
    'Mental Health & Nutrition',
    'Plant-Based Diets',
    'Medical Nutrition Therapy',
    'Supplement Counseling'
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-3 mb-6">
        {Icon && <Icon className="w-8 h-8 text-emerald-500" />}
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Practice Information</h2>
          <p className="text-gray-600">Details about your practice and patient population</p>
        </div>
      </div>

      {/* Workplace Details */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Building className="w-5 h-5 mr-2" />
            Workplace Information
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField
              type="input"
              label="Current Workplace"
              value={data.workplace}
              onChange={(value) => updateField('workplace', value)}
              placeholder="Hospital/Clinic Name"
              required
              helpText="Name of your primary workplace"
            />

            <FormField
              type="select"
              label="Practice Type"
              value={data.practice_type}
              onChange={(value) => updateField('practice_type', value)}
              placeholder="Select practice type"
              options={practiceTypes.map(type => ({
                value: type.value,
                label: (
                  <div>
                    <div className="font-medium">{type.label}</div>
                    <div className="text-sm text-gray-500">{type.description}</div>
                  </div>
                )
              }))}
              required
            />

            <FormField
              type="input"
              label="Practice Location"
              value={data.practice_location}
              onChange={(value) => updateField('practice_location', value)}
              placeholder="City, State"
              helpText="Primary practice location"
            />

            <FormField
              type="input"
              label="Department/Unit"
              value={data.department}
              onChange={(value) => updateField('department', value)}
              placeholder="e.g., Clinical Nutrition, Cardiology"
              helpText="Specific department or unit if applicable"
            />
          </div>
        </CardContent>
      </Card>

      {/* Patient Demographics */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Users className="w-5 h-5 mr-2" />
            Patient Demographics
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              Patient populations you typically serve (select all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {patientDemographics.map((demographic) => (
                <FormField
                  key={demographic}
                  type="checkbox"
                  label={demographic}
                  value={data.patient_demographics?.includes(demographic)}
                  onChange={(checked) => updateListField('patient_demographics', demographic, checked)}
                />
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Languages & Communication */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Globe className="w-5 h-5 mr-2" />
            Languages & Communication
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              Languages you speak fluently (select all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {languageOptions.map((language) => (
                <FormField
                  key={language}
                  type="checkbox"
                  label={language}
                  value={data.languages_spoken?.includes(language)}
                  onChange={(checked) => updateListField('languages_spoken', language, checked)}
                />
              ))}
            </div>
          </div>

          <FormField
            type="textarea"
            label="Additional Languages"
            value={data.additional_languages}
            onChange={(value) => updateField('additional_languages', value)}
            placeholder="List any other languages you speak"
            rows={2}
            helpText="Include any languages not listed above"
          />
        </CardContent>
      </Card>

      {/* Areas of Expertise */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <MapPin className="w-5 h-5 mr-2" />
            Clinical Areas of Expertise
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              Your areas of clinical expertise (select all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {expertiseAreas.map((area) => (
                <FormField
                  key={area}
                  type="checkbox"
                  label={area}
                  value={data.areas_of_expertise?.includes(area)}
                  onChange={(checked) => updateListField('areas_of_expertise', area, checked)}
                />
              ))}
            </div>
          </div>

          <FormField
            type="textarea"
            label="Additional Expertise or Special Interests"
            value={data.additional_expertise}
            onChange={(value) => updateField('additional_expertise', value)}
            placeholder="Describe any other areas of expertise or special clinical interests"
            rows={3}
            helpText="Include research interests, special populations, or unique skills"
          />
        </CardContent>
      </Card>

      {/* Practice Philosophy */}
      <Card>
        <CardHeader>
          <CardTitle>Practice Philosophy</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <FormField
            type="textarea"
            label="Your Approach to Patient Care"
            value={data.practice_philosophy}
            onChange={(value) => updateField('practice_philosophy', value)}
            placeholder="Describe your philosophy and approach to patient care and nutrition counseling..."
            rows={4}
            helpText="This helps patients understand your care style and approach"
          />

          <FormField
            type="textarea"
            label="Professional Mission Statement"
            value={data.mission_statement}
            onChange={(value) => updateField('mission_statement', value)}
            placeholder="What drives your work in healthcare and nutrition?"
            rows={3}
            helpText="Optional: Share what motivates you in your professional work"
          />
        </CardContent>
      </Card>

      {/* Practice Building Tips */}
      <div className="bg-emerald-50 p-4 rounded-lg">
        <h4 className="font-medium text-emerald-900 mb-2">🏥 Building Your Practice Profile</h4>
        <ul className="text-sm text-emerald-800 space-y-1">
          <li>• Clear practice information helps patients find the right care</li>
          <li>• Multiple languages increase your accessibility to diverse populations</li>
          <li>• Specific expertise areas help with targeted patient referrals</li>
          <li>• Your practice philosophy helps patients connect with your approach</li>
        </ul>
      </div>
    </div>
  );
};

export default PracticeInfoStep;