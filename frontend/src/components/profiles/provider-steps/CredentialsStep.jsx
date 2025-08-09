import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import FormField from '../../shared/FormField';
import { GraduationCap, Award, Plus, Trash2 } from 'lucide-react';

const CredentialsStep = ({ data = {}, onChange, icon: Icon }) => {
  const updateField = (field, value) => {
    const updatedData = { ...data, [field]: value };
    onChange(updatedData);
  };

  // Education management
  const addEducation = () => {
    const currentEducation = data.education || [];
    const newEducation = {
      id: Date.now().toString(),
      degree: '',
      institution: '',
      graduation_year: '',
      specialization: ''
    };
    updateField('education', [...currentEducation, newEducation]);
  };

  const updateEducation = (id, field, value) => {
    const updatedEducation = (data.education || []).map(edu =>
      edu.id === id ? { ...edu, [field]: value } : edu
    );
    updateField('education', updatedEducation);
  };

  const removeEducation = (id) => {
    const updatedEducation = (data.education || []).filter(edu => edu.id !== id);
    updateField('education', updatedEducation);
  };

  // Certification management
  const addCertification = () => {
    const currentCertifications = data.certifications || [];
    const newCertification = {
      id: Date.now().toString(),
      name: '',
      organization: '',
      issue_date: '',
      expiration_date: '',
      status: 'ACTIVE'
    };
    updateField('certifications', [...currentCertifications, newCertification]);
  };

  const updateCertification = (id, field, value) => {
    const updatedCertifications = (data.certifications || []).map(cert =>
      cert.id === id ? { ...cert, [field]: value } : cert
    );
    updateField('certifications', updatedCertifications);
  };

  const removeCertification = (id) => {
    const updatedCertifications = (data.certifications || []).filter(cert => cert.id !== id);
    updateField('certifications', updatedCertifications);
  };

  const updateSpecializations = (specialization, checked) => {
    const currentSpecs = data.specializations || [];
    let updatedSpecs;
    
    if (checked) {
      updatedSpecs = [...currentSpecs, specialization];
    } else {
      updatedSpecs = currentSpecs.filter(spec => spec !== specialization);
    }
    
    updateField('specializations', updatedSpecs);
  };

  const degreeOptions = [
    'Bachelor of Science in Nutrition',
    'Master of Science in Nutrition',
    'Master of Science in Clinical Nutrition',
    'Doctor of Medicine (MD)',
    'Doctor of Osteopathic Medicine (DO)',
    'Master of Science in Nursing (MSN)',
    'Doctor of Nursing Practice (DNP)',
    'PhD in Nutrition Science',
    'PhD in Public Health',
    'Master of Public Health (MPH)',
    'Bachelor of Science in Dietetics',
    'Other'
  ];

  const specializationOptions = [
    'Clinical Nutrition',
    'Sports Nutrition',
    'Pediatric Nutrition',
    'Geriatric Nutrition',
    'Cardiac Nutrition',
    'Diabetes Management',
    'Weight Management',
    'Eating Disorders',
    'Renal Nutrition',
    'Oncology Nutrition',
    'Critical Care Nutrition',
    'Community Nutrition',
    'Food Service Management',
    'Research & Development',
    'Nutrigenomics',
    'Plant-Based Nutrition'
  ];

  const certificationStatuses = [
    { value: 'ACTIVE', label: 'Active' },
    { value: 'EXPIRED', label: 'Expired' },
    { value: 'PENDING_RENEWAL', label: 'Pending Renewal' }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-3 mb-6">
        {Icon && <Icon className="w-8 h-8 text-emerald-500" />}
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Education & Certifications</h2>
          <p className="text-gray-600">Your educational background and professional certifications</p>
        </div>
      </div>

      {/* Education */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center">
              <GraduationCap className="w-5 h-5 mr-2" />
              Education
            </div>
            <button
              type="button"
              onClick={addEducation}
              className="text-sm bg-emerald-500 text-white px-3 py-1 rounded hover:bg-emerald-600 flex items-center"
            >
              <Plus className="w-4 h-4 mr-1" />
              Add Education
            </button>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {data.education && data.education.length > 0 ? (
            <div className="space-y-4">
              {data.education.map((education) => (
                <div key={education.id} className="bg-gray-50 p-4 rounded-lg">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <FormField
                      type="select"
                      label="Degree"
                      value={education.degree}
                      onChange={(value) => updateEducation(education.id, 'degree', value)}
                      options={degreeOptions.map(degree => ({ value: degree, label: degree }))}
                      placeholder="Select degree"
                      required
                    />
                    <FormField
                      type="input"
                      label="Institution"
                      value={education.institution}
                      onChange={(value) => updateEducation(education.id, 'institution', value)}
                      placeholder="University Name"
                      required
                    />
                    <FormField
                      type="number"
                      label="Graduation Year"
                      value={education.graduation_year}
                      onChange={(value) => updateEducation(education.id, 'graduation_year', parseInt(value) || '')}
                      placeholder="2020"
                      min="1960"
                      max={new Date().getFullYear() + 10}
                      required
                    />
                    <FormField
                      type="input"
                      label="Specialization/Focus"
                      value={education.specialization}
                      onChange={(value) => updateEducation(education.id, 'specialization', value)}
                      placeholder="e.g., Clinical Nutrition"
                    />
                  </div>
                  <button
                    type="button"
                    onClick={() => removeEducation(education.id)}
                    className="mt-2 text-sm text-red-600 hover:text-red-800 flex items-center"
                  >
                    <Trash2 className="w-4 h-4 mr-1" />
                    Remove Education
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <GraduationCap className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500">No education entries yet.</p>
              <p className="text-sm text-gray-400">Add your educational background to strengthen your profile.</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Certifications */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center">
              <Award className="w-5 h-5 mr-2" />
              Professional Certifications
            </div>
            <button
              type="button"
              onClick={addCertification}
              className="text-sm bg-emerald-500 text-white px-3 py-1 rounded hover:bg-emerald-600 flex items-center"
            >
              <Plus className="w-4 h-4 mr-1" />
              Add Certification
            </button>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {data.certifications && data.certifications.length > 0 ? (
            <div className="space-y-4">
              {data.certifications.map((certification) => (
                <div key={certification.id} className="bg-gray-50 p-4 rounded-lg">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <FormField
                      type="input"
                      label="Certification Name"
                      value={certification.name}
                      onChange={(value) => updateCertification(certification.id, 'name', value)}
                      placeholder="e.g., Certified Diabetes Educator"
                      required
                    />
                    <FormField
                      type="input"
                      label="Issuing Organization"
                      value={certification.organization}
                      onChange={(value) => updateCertification(certification.id, 'organization', value)}
                      placeholder="e.g., CBDCE"
                      required
                    />
                    <FormField
                      type="input"
                      label="Issue Date"
                      value={certification.issue_date}
                      onChange={(value) => updateCertification(certification.id, 'issue_date', value)}
                      placeholder="YYYY-MM-DD"
                      helpText="Format: YYYY-MM-DD"
                    />
                    <FormField
                      type="input"
                      label="Expiration Date"
                      value={certification.expiration_date}
                      onChange={(value) => updateCertification(certification.id, 'expiration_date', value)}
                      placeholder="YYYY-MM-DD"
                      helpText="Format: YYYY-MM-DD"
                    />
                    <FormField
                      type="select"
                      label="Status"
                      value={certification.status}
                      onChange={(value) => updateCertification(certification.id, 'status', value)}
                      options={certificationStatuses}
                      required
                    />
                  </div>
                  <button
                    type="button"
                    onClick={() => removeCertification(certification.id)}
                    className="mt-2 text-sm text-red-600 hover:text-red-800 flex items-center"
                  >
                    <Trash2 className="w-4 h-4 mr-1" />
                    Remove Certification
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <Award className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500">No certifications added yet.</p>
              <p className="text-sm text-gray-400">Add your professional certifications and credentials.</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Specializations */}
      <Card>
        <CardHeader>
          <CardTitle>Areas of Specialization</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              Select your areas of expertise (select all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {specializationOptions.map((specialization) => (
                <FormField
                  key={specialization}
                  type="checkbox"
                  label={specialization}
                  value={data.specializations?.includes(specialization)}
                  onChange={(checked) => updateSpecializations(specialization, checked)}
                />
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Credential Tips */}
      <div className="bg-emerald-50 p-4 rounded-lg">
        <h4 className="font-medium text-emerald-900 mb-2">📚 Building Your Professional Profile</h4>
        <ul className="text-sm text-emerald-800 space-y-1">
          <li>• Include all relevant degrees and certifications to enhance credibility</li>
          <li>• Keep certification status current - expired certifications will be flagged</li>
          <li>• Specializations help patients find the right expertise for their needs</li>
          <li>• All credentials will be verified before your profile goes live</li>
        </ul>
      </div>
    </div>
  );
};

export default CredentialsStep;