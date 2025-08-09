import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { ArrowLeft, User, GraduationCap, Building, Settings } from 'lucide-react';
import ProgressIndicator from '../shared/ProgressIndicator';
import WizardNavigation from '../shared/WizardNavigation';
import useAutoSave from '../../hooks/useAutoSave';
import ProfileAPI from '../../utils/profileApi';

// Step Components
import ProfessionalIdentityStep from './provider-steps/ProfessionalIdentityStep';
import CredentialsStep from './provider-steps/CredentialsStep';
import PracticeInfoStep from './provider-steps/PracticeInfoStep';
import PreferencesStep from './provider-steps/PreferencesStep';

const ProviderProfileWizard = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [currentStep, setCurrentStep] = useState(1);
  const [isEditing, setIsEditing] = useState(false);
  const [userId, setUserId] = useState(null);

  // Profile data state
  const [profileData, setProfileData] = useState({
    professional_identity: {},
    credentials: {},
    practice_info: {},
    preferences: {},
  });

  const totalSteps = 4;
  const stepLabels = [
    'Identity',
    'Credentials', 
    'Practice',
    'Preferences'
  ];

  const stepIcons = [
    User,
    GraduationCap,
    Building,
    Settings
  ];

  // Get user ID from location state or generate one
  useEffect(() => {
    const locationUserId = location.state?.userId;
    const existingProfile = location.state?.existingProfile;
    
    if (locationUserId) {
      setUserId(locationUserId);
      if (existingProfile) {
        setProfileData(existingProfile);
        setIsEditing(true);
      }
    } else {
      // Generate a temporary user ID for demo purposes
      const tempUserId = `provider_${Date.now()}`;
      setUserId(tempUserId);
    }
  }, [location.state]);

  // Auto-save functionality
  const saveProfile = async (data) => {
    if (!userId) return;

    const profilePayload = {
      user_id: userId,
      ...data
    };

    try {
      if (isEditing) {
        await ProfileAPI.updateProviderProfile(userId, data);
      } else {
        await ProfileAPI.createProviderProfile(profilePayload);
        setIsEditing(true);
      }
    } catch (error) {
      console.error('Failed to save profile:', error);
      throw error;
    }
  };

  const { isSaving, saveError, saveNow } = useAutoSave(profileData, saveProfile, 2000);

  // Update specific section of profile data
  const updateProfileSection = (section, data) => {
    setProfileData(prev => ({
      ...prev,
      [section]: data
    }));
  };

  // Step navigation
  const goToNextStep = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
    }
  };

  const goToPreviousStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  // Complete profile creation
  const completeProfile = async () => {
    try {
      await saveNow();
      navigate('/provider-dashboard', { 
        state: { 
          userId, 
          profileCompleted: true,
          message: 'Professional profile created successfully!' 
        }
      });
    } catch (error) {
      console.error('Failed to complete profile:', error);
    }
  };

  // Render current step content
  const renderStepContent = () => {
    const StepIcon = stepIcons[currentStep - 1];
    
    switch (currentStep) {
      case 1:
        return (
          <ProfessionalIdentityStep
            data={profileData.professional_identity}
            onChange={(data) => updateProfileSection('professional_identity', data)}
            icon={StepIcon}
          />
        );
      case 2:
        return (
          <CredentialsStep
            data={profileData.credentials}
            onChange={(data) => updateProfileSection('credentials', data)}
            icon={StepIcon}
          />
        );
      case 3:
        return (
          <PracticeInfoStep
            data={profileData.practice_info}
            onChange={(data) => updateProfileSection('practice_info', data)}
            icon={StepIcon}
          />
        );
      case 4:
        return (
          <PreferencesStep
            data={profileData.preferences}
            onChange={(data) => updateProfileSection('preferences', data)}
            icon={StepIcon}
          />
        );
      default:
        return null;
    }
  };

  // Check if current step has required data
  const isCurrentStepValid = () => {
    switch (currentStep) {
      case 1:
        return profileData.professional_identity?.full_name && profileData.professional_identity?.professional_title;
      case 2:
        return profileData.credentials?.education?.length > 0;
      case 3:
        return profileData.practice_info?.workplace && profileData.practice_info?.practice_type;
      case 4:
        return profileData.preferences?.consultation_types?.length > 0;
      default:
        return true;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button 
                variant="ghost" 
                onClick={() => navigate('/')}
                className="hover:bg-emerald-50"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Back to Home
              </Button>
              <div className="h-6 w-px bg-gray-300" />
              <h1 className="text-2xl font-bold text-gray-900">
                {isEditing ? 'Edit Professional Profile' : 'Create Professional Profile'}
              </h1>
            </div>
            
            {saveError && (
              <div className="text-red-600 text-sm">
                Save failed: {saveError}
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-6 py-8">
        <Card className="shadow-lg">
          <CardHeader>
            <ProgressIndicator 
              currentStep={currentStep} 
              totalSteps={totalSteps}
              stepLabels={stepLabels}
            />
          </CardHeader>
          
          <CardContent className="px-8 pb-8">
            {/* Step Content */}
            <div className="min-h-[500px]">
              {renderStepContent()}
            </div>

            {/* Navigation */}
            <WizardNavigation
              currentStep={currentStep}
              totalSteps={totalSteps}
              onPrevious={goToPreviousStep}
              onNext={goToNextStep}
              onSave={completeProfile}
              isNextDisabled={!isCurrentStepValid()}
              isLoading={isSaving}
              showSave={currentStep === totalSteps}
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ProviderProfileWizard;