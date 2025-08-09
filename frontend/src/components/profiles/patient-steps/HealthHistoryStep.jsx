import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import FormField from '../../shared/FormField';
import { Heart, Pill, AlertTriangle, Users, Scissors } from 'lucide-react';

const HealthHistoryStep = ({ data = {}, onChange, icon: Icon }) => {
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

  const updateMedicalCondition = (condition, severity) => {
    const updatedConditions = {
      ...data.medical_conditions,
      [condition]: severity
    };
    
    // Remove condition if severity is empty
    if (!severity) {
      delete updatedConditions[condition];
    }
    
    updateField('medical_conditions', updatedConditions);
  };

  const addMedication = () => {
    const currentMeds = data.current_medications || [];
    const newMed = {
      id: Date.now().toString(),
      name: '',
      dosage: '',
      frequency: '',
      purpose: ''
    };
    updateField('current_medications', [...currentMeds, newMed]);
  };

  const updateMedication = (id, field, value) => {
    const updatedMeds = (data.current_medications || []).map(med =>
      med.id === id ? { ...med, [field]: value } : med
    );
    updateField('current_medications', updatedMeds);
  };

  const removeMedication = (id) => {
    const updatedMeds = (data.current_medications || []).filter(med => med.id !== id);
    updateField('current_medications', updatedMeds);
  };

  // Previous surgeries helpers
  const addSurgery = () => {
    const currentSurgeries = data.previous_surgeries || [];
    const newSurgery = {
      id: Date.now().toString(),
      name: '',
      date: '',
      details: ''
    };
    updateField('previous_surgeries', [...currentSurgeries, newSurgery]);
  };

  const updateSurgery = (id, field, value) => {
    const updatedSurgeries = (data.previous_surgeries || []).map(surgery =>
      surgery.id === id ? { ...surgery, [field]: value } : surgery
    );
    updateField('previous_surgeries', updatedSurgeries);
  };

  const removeSurgery = (id) => {
    const updatedSurgeries = (data.previous_surgeries || []).filter(surgery => surgery.id !== id);
    updateField('previous_surgeries', updatedSurgeries);
  };

  const healthGoalOptions = [
    'Weight Loss',
    'Weight Gain', 
    'Muscle Building',
    'Improved Energy',
    'Better Sleep',
    'Stress Reduction',
    'Disease Management',
    'Athletic Performance',
    'General Wellness',
    'Healthy Aging'
  ];

  const commonConditions = [
    'Diabetes Type 1',
    'Diabetes Type 2',
    'Hypertension',
    'High Cholesterol',
    'Heart Disease',
    'Thyroid Disorder',
    'Arthritis',
    'Asthma',
    'COPD',
    'Kidney Disease',
    'Liver Disease',
    'Depression',
    'Anxiety',
    'PCOS',
    'Celiac Disease',
    'IBD/Crohn\'s'
  ];

  const commonAllergies = [
    'Peanuts',
    'Tree Nuts',
    'Shellfish',
    'Fish',
    'Eggs',
    'Milk/Dairy',
    'Soy',
    'Wheat/Gluten',
    'Sesame',
    'Sulfites'
  ];

  const familyHistoryOptions = [
    'Heart Disease',
    'Diabetes',
    'Cancer',
    'High Blood Pressure',
    'Stroke',
    'Obesity',
    'Osteoporosis',
    'Mental Health Conditions',
    'Autoimmune Disorders',
    'Kidney Disease'
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-3 mb-6">
        {Icon && <Icon className="w-8 h-8 text-blue-500" />}
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Health History</h2>
          <p className="text-gray-600">Your medical history helps us provide better recommendations</p>
        </div>
      </div>

      {/* Health Goals */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Heart className="w-5 h-5 mr-2" />
            Primary Health Goals
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              What are your main health goals? (select all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {healthGoalOptions.map((goal) => (
                <FormField
                  key={goal}
                  type="checkbox"
                  label={goal}
                  value={data.primary_health_goals?.includes(goal)}
                  onChange={(checked) => updateListField('primary_health_goals', goal, checked)}
                />
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Medical Conditions */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <AlertTriangle className="w-5 h-5 mr-2" />
            Medical Conditions
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              Current Medical Conditions (check if applicable and specify severity)
            </label>
            <div className="space-y-3">
              {commonConditions.map((condition) => (
                <div key={condition} className="flex items-center space-x-4">
                  <FormField
                    type="checkbox"
                    label={condition}
                    value={!!data.medical_conditions?.[condition]}
                    onChange={(checked) => {
                      if (checked) {
                        updateMedicalCondition(condition, 'mild');
                      } else {
                        updateMedicalCondition(condition, '');
                      }
                    }}
                  />
                  {data.medical_conditions?.[condition] && (
                    <FormField
                      type="select"
                      label=""
                      value={data.medical_conditions[condition]}
                      onChange={(value) => updateMedicalCondition(condition, value)}
                      options={[
                        { value: 'mild', label: 'Mild' },
                        { value: 'moderate', label: 'Moderate' },
                        { value: 'severe', label: 'Severe' }
                      ]}
                      className="w-32"
                    />
                  )}
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Current Medications */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center">
              <Pill className="w-5 h-5 mr-2" />
              Current Medications
            </div>
            <button
              type="button"
              onClick={addMedication}
              className="text-sm bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
            >
              Add Medication
            </button>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {data.current_medications && data.current_medications.length > 0 ? (
            <div className="space-y-4">
              {data.current_medications.map((medication) => (
                <div key={medication.id} className="bg-gray-50 p-4 rounded-lg">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <FormField
                      type="input"
                      label="Medication Name"
                      value={medication.name}
                      onChange={(value) => updateMedication(medication.id, 'name', value)}
                      placeholder="e.g., Metformin"
                    />
                    <FormField
                      type="input"
                      label="Dosage"
                      value={medication.dosage}
                      onChange={(value) => updateMedication(medication.id, 'dosage', value)}
                      placeholder="e.g., 500mg"
                    />
                    <FormField
                      type="input"
                      label="Frequency"
                      value={medication.frequency}
                      onChange={(value) => updateMedication(medication.id, 'frequency', value)}
                      placeholder="e.g., Twice daily"
                    />
                    <FormField
                      type="input"
                      label="Purpose"
                      value={medication.purpose}
                      onChange={(value) => updateMedication(medication.id, 'purpose', value)}
                      placeholder="e.g., Diabetes management"
                    />
                  </div>
                  <button
                    type="button"
                    onClick={() => removeMedication(medication.id)}
                    className="mt-2 text-sm text-red-600 hover:text-red-800"
                  >
                    Remove Medication
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-4">
              No medications added. Click "Add Medication" to include your current medications.
            </p>
          )}
        </CardContent>
      </Card>

      {/* Previous Surgeries */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center">
              <Scissors className="w-5 h-5 mr-2" />
              Previous Surgeries or Procedures
            </div>
            <button
              type="button"
              onClick={addSurgery}
              className="text-sm bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
            >
              Add Surgery/Procedure
            </button>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {data.previous_surgeries && data.previous_surgeries.length > 0 ? (
            <div className="space-y-4">
              {data.previous_surgeries.map((surgery) => (
                <div key={surgery.id} className="bg-gray-50 p-4 rounded-lg">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <FormField
                      type="input"
                      label="Procedure Name"
                      value={surgery.name}
                      onChange={(value) => updateSurgery(surgery.id, 'name', value)}
                      placeholder="e.g., Appendectomy"
                    />
                    <FormField
                      type="input"
                      label="Date"
                      value={surgery.date}
                      onChange={(value) => updateSurgery(surgery.id, 'date', value)}
                      placeholder="YYYY-MM-DD (optional)"
                    />
                  </div>
                  <div className="mt-3">
                    <FormField
                      type="textarea"
                      label="Notes/Details"
                      value={surgery.details}
                      onChange={(value) => updateSurgery(surgery.id, 'details', value)}
                      placeholder="Additional details about the procedure (optional)"
                      rows={2}
                    />
                  </div>
                  <button
                    type="button"
                    onClick={() => removeSurgery(surgery.id)}
                    className="mt-2 text-sm text-red-600 hover:text-red-800"
                  >
                    Remove Surgery/Procedure
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-4">
              No surgeries or procedures added. Click "Add Surgery/Procedure" to include your medical history.
            </p>
          )}
        </CardContent>
      </Card>

      {/* Allergies */}
      <Card>
        <CardHeader>
          <CardTitle>Allergies & Food Intolerances</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              Food Allergies (select all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {commonAllergies.map((allergy) => (
                <FormField
                  key={allergy}
                  type="checkbox"
                  label={allergy}
                  value={data.allergies?.includes(allergy)}
                  onChange={(checked) => updateListField('allergies', allergy, checked)}
                />
              ))}
            </div>
          </div>

          <FormField
            type="textarea"
            label="Food Intolerances or Other Allergies"
            value={data.food_intolerances?.join(', ')}
            onChange={(value) => updateField('food_intolerances', value.split(', ').filter(item => item.trim()))}
            placeholder="List any food intolerances (e.g., lactose intolerance, garlic sensitivity)"
            helpText="Separate multiple items with commas"
          />
        </CardContent>
      </Card>

      {/* Family History */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Users className="w-5 h-5 mr-2" />
            Family Medical History
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              Family History of Medical Conditions (select all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {familyHistoryOptions.map((condition) => (
                <FormField
                  key={condition}
                  type="checkbox"
                  label={condition}
                  value={data.family_medical_history?.includes(condition)}
                  onChange={(checked) => updateListField('family_medical_history', condition, checked)}
                />
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Privacy Notice */}
      <div className="bg-green-50 p-4 rounded-lg">
        <h4 className="font-medium text-green-900 mb-2">🔒 Your Privacy is Protected</h4>
        <p className="text-sm text-green-800">
          All health information is kept strictly confidential and used only to provide 
          personalized nutrition and health recommendations. This data is never shared 
          without your explicit consent.
        </p>
      </div>
    </div>
  );
};

export default HealthHistoryStep;