import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Button } from '../../ui/button';
import FormField from '../../shared/FormField';
import { Plus, Trash2, Users } from 'lucide-react';

const FamilyMembersStep = ({ data, onChange, icon: Icon }) => {
  const [newMember, setNewMember] = useState({
    name: '',
    relationship: '',
    age: '',
    gender: '',
    special_needs: [],
    allergies: [],
    medications: [],
    health_conditions: []
  });

  const members = data || [];

  const relationshipOptions = [
    { value: 'spouse', label: 'Spouse/Partner' },
    { value: 'child', label: 'Child' },
    { value: 'parent', label: 'Parent' },
    { value: 'sibling', label: 'Sibling' },
    { value: 'grandparent', label: 'Grandparent' },
    { value: 'grandchild', label: 'Grandchild' },
    { value: 'other', label: 'Other Relative' }
  ];

  const genderOptions = [
    { value: 'male', label: 'Male' },
    { value: 'female', label: 'Female' },
    { value: 'other', label: 'Other' },
    { value: 'prefer_not_to_say', label: 'Prefer not to say' }
  ];

  const addMember = () => {
    if (!newMember.name || !newMember.relationship || !newMember.age) {
      return;
    }

    const memberWithId = {
      ...newMember,
      id: `member_${Date.now()}`,
      age: parseInt(newMember.age),
      special_needs: newMember.special_needs.filter(need => need.trim()),
      allergies: newMember.allergies.filter(allergy => allergy.trim()),
      medications: newMember.medications.filter(med => med.trim()),
      health_conditions: newMember.health_conditions.filter(condition => condition.trim())
    };

    const updatedMembers = [...members, memberWithId];
    onChange(updatedMembers);

    // Reset form
    setNewMember({
      name: '',
      relationship: '',
      age: '',
      gender: '',
      special_needs: [],
      allergies: [],
      medications: [],
      health_conditions: []
    });
  };

  const removeMember = (memberId) => {
    const updatedMembers = members.filter(member => member.id !== memberId);
    onChange(updatedMembers);
  };

  const updateArrayField = (field, value) => {
    const items = value.split(',').map(item => item.trim()).filter(item => item);
    setNewMember(prev => ({ ...prev, [field]: items }));
  };

  return (
    <div className="space-y-8">
      {/* Step Header */}
      <div className="text-center">
        <div className="mx-auto w-16 h-16 bg-amber-100 rounded-full flex items-center justify-center mb-4">
          <Icon className="w-8 h-8 text-amber-600" />
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Family Members</h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Add details for each family member to create comprehensive health profiles
        </p>
      </div>

      {/* Current Family Members */}
      {members.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Users className="w-5 h-5 mr-2 text-amber-600" />
              Current Family Members ({members.length})
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {members.map((member) => (
              <div key={member.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-900">{member.name}</h4>
                  <p className="text-sm text-gray-600">
                    {member.relationship} • Age {member.age} • {member.gender}
                  </p>
                  {(member.allergies?.length > 0 || member.health_conditions?.length > 0) && (
                    <div className="mt-2 text-xs text-gray-500">
                      {member.allergies?.length > 0 && (
                        <span className="mr-4">Allergies: {member.allergies.join(', ')}</span>
                      )}
                      {member.health_conditions?.length > 0 && (
                        <span>Conditions: {member.health_conditions.join(', ')}</span>
                      )}
                    </div>
                  )}
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => removeMember(member.id)}
                  className="text-red-600 hover:text-red-700 hover:bg-red-50"
                >
                  <Trash2 className="w-4 h-4" />
                </Button>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Add New Member */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Plus className="w-5 h-5 mr-2 text-amber-600" />
            Add Family Member
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Basic Information */}
            <FormField
              type="input"
              label="Full Name"
              value={newMember.name}
              onChange={(value) => setNewMember(prev => ({ ...prev, name: value }))}
              placeholder="Enter full name"
              required
            />

            <FormField
              type="select"
              label="Relationship to You"
              value={newMember.relationship}
              onChange={(value) => setNewMember(prev => ({ ...prev, relationship: value }))}
              options={relationshipOptions}
              placeholder="Select relationship"
              required
            />

            <FormField
              type="number"
              label="Age"
              value={newMember.age}
              onChange={(value) => setNewMember(prev => ({ ...prev, age: value }))}
              placeholder="Enter age"
              min="0"
              max="120"
              required
            />

            <FormField
              type="select"
              label="Gender"
              value={newMember.gender}
              onChange={(value) => setNewMember(prev => ({ ...prev, gender: value }))}
              options={genderOptions}
              placeholder="Select gender"
            />
          </div>

          {/* Health Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <FormField
              type="input"
              label="Allergies"
              value={newMember.allergies.join(', ')}
              onChange={(value) => updateArrayField('allergies', value)}
              placeholder="e.g., Peanuts, Shellfish, Dairy"
              helpText="Separate multiple allergies with commas"
            />

            <FormField
              type="input"
              label="Health Conditions"
              value={newMember.health_conditions.join(', ')}
              onChange={(value) => updateArrayField('health_conditions', value)}
              placeholder="e.g., Diabetes, Hypertension"
              helpText="Separate multiple conditions with commas"
            />

            <FormField
              type="input"
              label="Current Medications"
              value={newMember.medications.join(', ')}
              onChange={(value) => updateArrayField('medications', value)}
              placeholder="e.g., Insulin, Blood pressure medication"
              helpText="Separate multiple medications with commas"
            />

            <FormField
              type="input"
              label="Special Needs"
              value={newMember.special_needs.join(', ')}
              onChange={(value) => updateArrayField('special_needs', value)}
              placeholder="e.g., Mobility assistance, Dietary restrictions"
              helpText="Separate multiple needs with commas"
            />
          </div>

          <Button 
            onClick={addMember}
            disabled={!newMember.name || !newMember.relationship || !newMember.age}
            className="w-full bg-amber-600 hover:bg-amber-700"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Family Member
          </Button>
        </CardContent>
      </Card>

      {/* Help Text */}
      <Card>
        <CardContent className="pt-6">
          <div className="bg-amber-50 p-4 rounded-lg">
            <h4 className="font-semibold text-amber-800 mb-2">Tips for Adding Family Members:</h4>
            <ul className="text-sm text-amber-700 space-y-1">
              <li>• Include all family members who live in your household</li>
              <li>• Add health information to help with meal planning and care coordination</li>
              <li>• You can always edit or update member information later</li>
              <li>• This information helps create personalized health management plans</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default FamilyMembersStep;