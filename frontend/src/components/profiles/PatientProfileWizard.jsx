import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useRole } from '../../context/RoleContext';
import SmartNavigation from '../shared/SmartNavigation';
import Breadcrumb from '../shared/Breadcrumb';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { User, Activity, Heart, Target, Utensils, Settings, CheckCircle, Clock } from 'lucide-react';
import ProgressIndicator from '../shared/ProgressIndicator';
import WizardNavigation from '../shared/WizardNavigation';
import useAutoSave from '../../hooks/useAutoSave';
import ProfileAPI from '../../utils/profileApi';
import { getSectionCompletionStatus, getMissingFields } from '../../utils/profileValidation';

// Step Components
import BasicInfoStep from './patient-steps/BasicInfoStep';
import PhysicalMetricsStep from './patient-steps/PhysicalMetricsStep';
import ActivityProfileStep from './patient-steps/ActivityProfileStep';
import HealthHistoryStep from './patient-steps/HealthHistoryStep';
import DietaryProfileStep from './patient-steps/DietaryProfileStep';
import GoalsPreferencesStep from './patient-steps/GoalsPreferencesStep';

const PatientProfileWizard = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [currentStep, setCurrentStep] = useState(1);
  const [isEditing, setIsEditing] = useState(false);
  const [userId, setUserId] = useState(null);
  const [sectionCompletion, setSectionCompletion] = useState({});

  // Profile data state
  const [profileData, setProfileData] = useState({
    basic_info: {},
    physical_metrics: {},
    activity_profile: {},
    health_history: {},
    dietary_profile: {},
    goals_preferences: {},
  });

  const totalSteps = 6;
  const stepLabels = [
    'Basic Info',
    'Physical',
    'Activity',
    'Health',
    'Diet',
    'Goals'
  ];

  const stepIcons = [
    User,
    Activity,
    Heart,
    Target,
    Utensils,
    Settings
  ];

  // Get user ID from localStorage or generate one, and try to load existing profile
  useEffect(() => {
    const initializeProfile = async () => {
      // Check for existing userId in localStorage first
      let storedUserId = localStorage.getItem('patient_user_id');
      
      // Check location state (for navigation with pre-set userId)
      const locationUserId = location.state?.userId;
      const existingProfile = location.state?.existingProfile;
      
      if (locationUserId) {
        // Use userId from location state (takes priority)
        setUserId(locationUserId);
        localStorage.setItem('patient_user_id', locationUserId);
        
        if (existingProfile) {
          setProfileData(existingProfile);
          setSectionCompletion(getSectionCompletionStatus(existingProfile));
          setIsEditing(true);
        }
      } else if (storedUserId) {
        // Use stored userId and try to fetch existing profile
        setUserId(storedUserId);
        
        try {
          const existingProfile = await ProfileAPI.getPatientProfile(storedUserId);
          if (existingProfile) {
            setProfileData(existingProfile);
            setSectionCompletion(getSectionCompletionStatus(existingProfile));
            setIsEditing(true);
          }
        } catch (error) {
          // Profile doesn't exist yet, continue with empty profile
          console.log('No existing profile found, starting fresh');
        }
      } else {
        // Generate a new user ID and store it
        const tempUserId = `patient_${Date.now()}`;
        setUserId(tempUserId);
        localStorage.setItem('patient_user_id', tempUserId);
      }
    };
    
    initializeProfile();
  }, [location.state]);

  // Auto-save functionality
  const saveProfile = async (data) => {
    if (!userId) return;

    // Build a sanitized payload that only includes sections which are actually complete
    const completion = getSectionCompletionStatus(data);
    const sections = ['basic_info', 'physical_metrics', 'activity_profile', 'health_history', 'dietary_profile', 'goals_preferences'];
    const sanitized = sections.reduce((acc, key) => {
      if (completion[key]) {
        acc[key] = data[key];
      }
      return acc;
    }, {});

    // If nothing complete, do not attempt to save
    if (Object.keys(sanitized).length === 0) return;

    try {
      if (isEditing) {
        // Partial update with only valid sections
        await ProfileAPI.updatePatientProfile(userId, sanitized);
      } else {
        const profilePayload = {
          user_id: userId,
          ...sanitized,
        };
        await ProfileAPI.createPatientProfile(profilePayload);
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
    setProfileData(prev => {
      const updated = {
        ...prev,
        [section]: data
      };
      
      // Update section completion status
      setSectionCompletion(getSectionCompletionStatus(updated));
      
      return updated;
    });
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
      navigate('/patient-dashboard', { 
        state: { 
          userId, 
          profileCompleted: true,
          message: 'Profile created successfully!' 
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
          <BasicInfoStep
            data={profileData.basic_info}
            onChange={(data) => updateProfileSection('basic_info', data)}
            icon={StepIcon}
          />
        );
      case 2:
        return (
          <PhysicalMetricsStep
            data={profileData.physical_metrics}
            onChange={(data) => updateProfileSection('physical_metrics', data)}
            icon={StepIcon}
          />
        );
      case 3:
        return (
          <ActivityProfileStep
            data={profileData.activity_profile}
            onChange={(data) => updateProfileSection('activity_profile', data)}
            icon={StepIcon}
          />
        );
      case 4:
        return (
          <HealthHistoryStep
            data={profileData.health_history}
            onChange={(data) => updateProfileSection('health_history', data)}
            icon={StepIcon}
          />
        );
      case 5:
        return (
          <DietaryProfileStep
            data={profileData.dietary_profile}
            onChange={(data) => updateProfileSection('dietary_profile', data)}
            icon={StepIcon}
          />
        );
      case 6:
        return (
          <GoalsPreferencesStep
            data={profileData.goals_preferences}
            onChange={(data) => updateProfileSection('goals_preferences', data)}
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
        return profileData.basic_info?.full_name && profileData.basic_info?.age;
      case 2:
        return profileData.physical_metrics?.height_cm && profileData.physical_metrics?.current_weight_kg;
      case 3:
        return profileData.activity_profile?.activity_level && profileData.activity_profile?.exercise_frequency !== undefined;
      case 4:
        return true; // Health history is optional
      case 5:
        return profileData.dietary_profile?.diet_type;
      case 6:
        return true; // Goals are optional
      default:
        return true;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button 
                variant="ghost" 
                onClick={() => navigate('/')}
                className="hover:bg-blue-50"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Back to Home
              </Button>
              <div className="h-6 w-px bg-gray-300" />
              <h1 className="text-2xl font-bold text-gray-900">
                {isEditing ? 'Edit Health Profile' : 'Create Your Health Profile'}
              </h1>
            </div>
            
            {/* Save Status and Section Completion */}
            <div className="flex items-center space-x-4">
              {Object.values(sectionCompletion).some(complete => complete) && (
                <div className="flex items-center text-green-600 text-sm">
                  <CheckCircle className="w-4 h-4 mr-1" />
                  Auto-save enabled
                </div>
              )}
              
              {saveError && (
                <div className="text-red-600 text-sm max-w-xs">
                  Save failed: {typeof saveError === 'string' ? saveError : 'Please complete required fields before saving'}
                </div>
              )}
            </div>
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
              sectionCompletion={sectionCompletion}
            />
          </CardHeader>
          
          <CardContent className="px-8 pb-8">
            {/* Step Content */}
            <div className="min-h-[500px]">
              {/* Section Completion Hint */}
              {(() => {
                const sectionNames = ['basic_info', 'physical_metrics', 'activity_profile', 'health_history', 'dietary_profile', 'goals_preferences'];
                const currentSectionName = sectionNames[currentStep - 1];
                const isCurrentSectionComplete = sectionCompletion[currentSectionName] || false;
                
                return !isCurrentSectionComplete && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                    <div className="flex items-start">
                      <Clock className="w-5 h-5 text-blue-500 mr-3 mt-0.5" />
                      <div>
                        <h3 className="text-sm font-medium text-blue-900 mb-1">
                          Complete this section to enable auto-save
                        </h3>
                        <p className="text-sm text-blue-700">
                          Fill in all required fields in this step and your progress will be automatically saved.
                        </p>
                      </div>
                    </div>
                  </div>
                );
              })()}
              
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
              isLoading={false}
              showSave={currentStep === totalSteps}
              showAutoSaveIndicator={false}
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default PatientProfileWizard;