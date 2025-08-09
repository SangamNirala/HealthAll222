import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import FormField from '../../shared/FormField';

const FamilyStructureStep = ({ data, onChange, icon: Icon }) => {
  const handleChange = (field, value) => {
    const updatedData = {
      ...data,
      [field]: value
    };
    onChange(updatedData);
  };

  const familyRoleOptions = [
    { value: 'parent', label: 'Parent' },
    { value: 'spouse', label: 'Spouse/Partner' },
    { value: 'adult_child', label: 'Adult Child' },
    { value: 'grandparent', label: 'Grandparent' },
    { value: 'guardian', label: 'Guardian' },
    { value: 'caregiver', label: 'Professional Caregiver' },
    { value: 'other', label: 'Other Family Role' }
  ];

  return (
    <div className="space-y-8">
      {/* Step Header */}
      <div className="text-center">
        <div className="mx-auto w-16 h-16 bg-amber-100 rounded-full flex items-center justify-center mb-4">
          <Icon className="w-8 h-8 text-amber-600" />
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Family Structure</h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Tell us about your family structure and your role in managing health and nutrition
        </p>
      </div>

      {/* Family Structure Form */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Icon className="w-5 h-5 mr-2 text-amber-600" />
            Family Information
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Family Role */}
          <FormField
            type="select"
            label="Your Role in the Family"
            value={data?.family_role || ''}
            onChange={(value) => handleChange('family_role', value)}
            options={familyRoleOptions}
            placeholder="Select your family role"
            required
            helpText="Select the role that best describes your position in the family"
          />

          {/* Number of Family Members */}
          <FormField
            type="number"
            label="Total Number of Family Members"
            value={data?.number_of_members || ''}
            onChange={(value) => handleChange('number_of_members', parseInt(value) || 0)}
            placeholder="Enter total family members"
            min="1"
            max="20"
            required
            helpText="Include all family members living in your household"
          />

          {/* Primary Caregiver */}
          <div className="space-y-2">
            <FormField
              type="checkbox"
              label="I am the primary caregiver responsible for family health decisions"
              value={data?.primary_caregiver || false}
              onChange={(value) => handleChange('primary_caregiver', value)}
              helpText="Check this if you are the main person making health and nutrition decisions for the family"
            />
          </div>
        </CardContent>
      </Card>

      {/* Additional Context */}
      <Card>
        <CardHeader>
          <CardTitle>Family Health Management Context</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="bg-amber-50 p-4 rounded-lg">
            <h4 className="font-semibold text-amber-800 mb-2">What to expect next:</h4>
            <ul className="text-sm text-amber-700 space-y-1">
              <li>• Add details for each family member</li>
              <li>• Set up household meal planning and responsibilities</li>
              <li>• Coordinate healthcare providers and emergency contacts</li>
              <li>• Create a comprehensive family health management system</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default FamilyStructureStep;