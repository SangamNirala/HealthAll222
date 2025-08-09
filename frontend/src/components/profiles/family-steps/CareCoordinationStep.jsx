import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Button } from '../../ui/button';
import FormField from '../../shared/FormField';
import { Plus, Trash2, UserCheck, Phone, Shield, Calendar } from 'lucide-react';

const CareCoordinationStep = ({ data, onChange, icon: Icon }) => {
  const [newProvider, setNewProvider] = useState({ member: '', provider: '', contact: '' });
  const [newContact, setNewContact] = useState({ name: '', relationship: '', phone: '', email: '' });

  const handleChange = (field, value) => {
    const updatedData = {
      ...data,
      [field]: value
    };
    onChange(updatedData);
  };

  // Healthcare Providers Management
  const addProvider = () => {
    if (!newProvider.member || !newProvider.provider || !newProvider.contact) return;

    const providers = data?.healthcare_providers || {};
    const updatedProviders = {
      ...providers,
      [newProvider.member]: {
        provider: newProvider.provider,
        contact: newProvider.contact
      }
    };

    handleChange('healthcare_providers', updatedProviders);
    setNewProvider({ member: '', provider: '', contact: '' });
  };

  const removeProvider = (member) => {
    const providers = data?.healthcare_providers || {};
    const { [member]: removed, ...rest } = providers;
    handleChange('healthcare_providers', rest);
  };

  // Emergency Contacts Management
  const addEmergencyContact = () => {
    if (!newContact.name || !newContact.phone) return;

    const contacts = data?.emergency_contacts || [];
    const updatedContacts = [...contacts, { ...newContact, id: `contact_${Date.now()}` }];

    handleChange('emergency_contacts', updatedContacts);
    setNewContact({ name: '', relationship: '', phone: '', email: '' });
  };

  const removeEmergencyContact = (contactId) => {
    const contacts = data?.emergency_contacts || [];
    const updatedContacts = contacts.filter(contact => contact.id !== contactId);
    handleChange('emergency_contacts', updatedContacts);
  };

  // Medication Management
  const handleMedicationChange = (member, medications) => {
    const medicationManagement = data?.medication_management || {};
    const updatedManagement = {
      ...medicationManagement,
      [member]: medications
    };
    handleChange('medication_management', updatedManagement);
  };

  // Health Tracking Preferences
  const handleTrackingPreference = (preference, value) => {
    const preferences = data?.health_tracking_preferences || {};
    const updatedPreferences = {
      ...preferences,
      [preference]: value
    };
    handleChange('health_tracking_preferences', updatedPreferences);
  };

  return (
    <div className="space-y-8">
      {/* Step Header */}
      <div className="text-center">
        <div className="mx-auto w-16 h-16 bg-amber-100 rounded-full flex items-center justify-center mb-4">
          <Icon className="w-8 h-8 text-amber-600" />
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Care Coordination</h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Set up healthcare providers, emergency contacts, and health tracking preferences
        </p>
      </div>

      {/* Healthcare Providers */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <UserCheck className="w-5 h-5 mr-2 text-amber-600" />
            Healthcare Providers
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Current Providers */}
          {data?.healthcare_providers && Object.keys(data.healthcare_providers).length > 0 && (
            <div className="space-y-3">
              <h4 className="font-medium text-gray-900">Current Providers:</h4>
              {Object.entries(data.healthcare_providers).map(([member, details]) => (
                <div key={member} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium">{member}</p>
                    <p className="text-sm text-gray-600">{details.provider} - {details.contact}</p>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => removeProvider(member)}
                    className="text-red-600 hover:text-red-700"
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              ))}
            </div>
          )}

          {/* Add Provider */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <FormField
              type="input"
              label="Family Member"
              value={newProvider.member}
              onChange={(value) => setNewProvider(prev => ({ ...prev, member: value }))}
              placeholder="e.g., Sarah, John"
            />
            <FormField
              type="input"
              label="Provider/Doctor"
              value={newProvider.provider}
              onChange={(value) => setNewProvider(prev => ({ ...prev, provider: value }))}
              placeholder="e.g., Dr. Smith, Pediatrician"
            />
            <FormField
              type="input"
              label="Contact Information"
              value={newProvider.contact}
              onChange={(value) => setNewProvider(prev => ({ ...prev, contact: value }))}
              placeholder="Phone number or clinic"
            />
          </div>
          <Button 
            onClick={addProvider}
            disabled={!newProvider.member || !newProvider.provider || !newProvider.contact}
            className="w-full bg-amber-600 hover:bg-amber-700"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Healthcare Provider
          </Button>
        </CardContent>
      </Card>

      {/* Emergency Contacts */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Shield className="w-5 h-5 mr-2 text-amber-600" />
            Emergency Contacts
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Current Emergency Contacts */}
          {data?.emergency_contacts && data.emergency_contacts.length > 0 && (
            <div className="space-y-3">
              <h4 className="font-medium text-gray-900">Emergency Contacts:</h4>
              {data.emergency_contacts.map((contact) => (
                <div key={contact.id} className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                  <div>
                    <p className="font-medium">{contact.name}</p>
                    <p className="text-sm text-gray-600">
                      {contact.relationship} • {contact.phone}
                      {contact.email && ` • ${contact.email}`}
                    </p>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => removeEmergencyContact(contact.id)}
                    className="text-red-600 hover:text-red-700"
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              ))}
            </div>
          )}

          {/* Add Emergency Contact */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField
              type="input"
              label="Contact Name"
              value={newContact.name}
              onChange={(value) => setNewContact(prev => ({ ...prev, name: value }))}
              placeholder="e.g., Jane Doe"
              required
            />
            <FormField
              type="input"
              label="Relationship"
              value={newContact.relationship}
              onChange={(value) => setNewContact(prev => ({ ...prev, relationship: value }))}
              placeholder="e.g., Sister, Neighbor"
            />
            <FormField
              type="tel"
              label="Phone Number"
              value={newContact.phone}
              onChange={(value) => setNewContact(prev => ({ ...prev, phone: value }))}
              placeholder="e.g., (555) 123-4567"
              required
            />
            <FormField
              type="email"
              label="Email (Optional)"
              value={newContact.email}
              onChange={(value) => setNewContact(prev => ({ ...prev, email: value }))}
              placeholder="e.g., jane@example.com"
            />
          </div>
          <Button 
            onClick={addEmergencyContact}
            disabled={!newContact.name || !newContact.phone}
            className="w-full bg-red-600 hover:bg-red-700"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Emergency Contact
          </Button>
        </CardContent>
      </Card>

      {/* Health Tracking Preferences */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Calendar className="w-5 h-5 mr-2 text-amber-600" />
            Health Tracking Preferences
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField
              type="checkbox"
              label="Track medication schedules for family members"
              value={data?.health_tracking_preferences?.medication_schedules || false}
              onChange={(value) => handleTrackingPreference('medication_schedules', value)}
            />
            <FormField
              type="checkbox"
              label="Set reminders for medical appointments"
              value={data?.health_tracking_preferences?.appointment_reminders || false}
              onChange={(value) => handleTrackingPreference('appointment_reminders', value)}
            />
            <FormField
              type="checkbox"
              label="Monitor family health metrics"
              value={data?.health_tracking_preferences?.health_metrics || false}
              onChange={(value) => handleTrackingPreference('health_metrics', value)}
            />
            <FormField
              type="checkbox"
              label="Track vaccination schedules"
              value={data?.health_tracking_preferences?.vaccination_schedules || false}
              onChange={(value) => handleTrackingPreference('vaccination_schedules', value)}
            />
            <FormField
              type="checkbox"
              label="Share health updates with providers"
              value={data?.health_tracking_preferences?.provider_sharing || false}
              onChange={(value) => handleTrackingPreference('provider_sharing', value)}
            />
            <FormField
              type="checkbox"
              label="Emergency notification system"
              value={data?.health_tracking_preferences?.emergency_notifications || false}
              onChange={(value) => handleTrackingPreference('emergency_notifications', value)}
            />
          </div>
        </CardContent>
      </Card>

      {/* Completion Summary */}
      <Card>
        <CardContent className="pt-6">
          <div className="bg-green-50 p-4 rounded-lg">
            <h4 className="font-semibold text-green-800 mb-2">Care Coordination Setup Complete!</h4>
            <ul className="text-sm text-green-700 space-y-1">
              <li>• Your family's healthcare providers and emergency contacts are organized</li>
              <li>• Health tracking preferences will help coordinate care</li>
              <li>• You can update this information anytime from your family dashboard</li>
              <li>• All family health data will be kept secure and private</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default CareCoordinationStep;