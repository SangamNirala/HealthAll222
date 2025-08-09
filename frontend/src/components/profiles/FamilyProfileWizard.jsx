import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { ArrowLeft, Users, UserPlus, Home, Heart } from 'lucide-react';
import ProgressIndicator from '../shared/ProgressIndicator';
import WizardNavigation from '../shared/WizardNavigation';
import useAutoSave from '../../hooks/useAutoSave';
import ProfileAPI from '../../utils/profileApi';
import { getSectionCompletionStatus } from '../../utils/profileValidation';

// Step Components
import FamilyStructureStep from './family-steps/FamilyStructureStep';
import FamilyMembersStep from './family-steps/FamilyMembersStep';
import HouseholdManagementStep from './family-steps/HouseholdManagementStep';
import CareCoordinationStep from './family-steps/CareCoordinationStep';

const FamilyProfileWizard = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [currentStep, setCurrentStep] = useState(1);
  const [isEditing, setIsEditing] = useState(false);
  const [userId, setUserId] = useState(null);

  // Profile data state
  const [profileData, setProfileData] = useState({
    family_structure: {},
    family_members: [],
    household_management: {},
    care_coordination: {},
  });

  const totalSteps = 4;
  const stepLabels = [
    'Structure',
    'Members', 
    'Household',
    'Care'
  ];

  const stepIcons = [
    Users,
    UserPlus,
    Home,
    Heart
  ];

  // Get user ID from localStorage or generate one, and try to load existing profile
  useEffect(() => {
    const initializeProfile = async () => {
      // Check for existing userId in localStorage first
      let storedUserId = localStorage.getItem('family_user_id');
      
      // Check location state (for navigation with pre-set userId)
      const locationUserId = location.state?.userId;
      const existingProfile = location.state?.existingProfile;
      
      if (locationUserId) {
        // Use userId from location state (takes priority)
        setUserId(locationUserId);
        localStorage.setItem('family_user_id', locationUserId);
        
        if (existingProfile) {
          setProfileData(existingProfile);
          setIsEditing(true);
        }
      } else if (storedUserId) {
        // Use stored userId and try to fetch existing profile
        setUserId(storedUserId);
        
        try {
          const existingProfile = await ProfileAPI.getFamilyProfile(storedUserId);
          if (existingProfile) {
            setProfileData(existingProfile);
            setIsEditing(true);
          }
        } catch (error) {
          // Profile doesn't exist yet, continue with empty profile
          console.log('No existing profile found, starting fresh');
        }
      } else {
        // Generate a new user ID and store it
        const tempUserId = `family_${Date.now()}`;
        setUserId(tempUserId);
        localStorage.setItem('family_user_id', tempUserId);
      }
    };
    
    initializeProfile();
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
        await ProfileAPI.updateFamilyProfile(userId, data);
      } else {
        await ProfileAPI.createFamilyProfile(profilePayload);
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
      navigate('/family-dashboard', { 
        state: { 
          userId, 
          profileCompleted: true,
          message: 'Family profile created successfully!' 
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
          <FamilyStructureStep
            data={profileData.family_structure}
            onChange={(data) => updateProfileSection('family_structure', data)}
            icon={StepIcon}
          />
        );
      case 2:
        return (
          <FamilyMembersStep
            data={profileData.family_members}
            onChange={(data) => updateProfileSection('family_members', data)}
            icon={StepIcon}
          />
        );
      case 3:
        return (
          <HouseholdManagementStep
            data={profileData.household_management}
            onChange={(data) => updateProfileSection('household_management', data)}
            icon={StepIcon}
          />
        );
      case 4:
        return (
          <CareCoordinationStep
            data={profileData.care_coordination}
            onChange={(data) => updateProfileSection('care_coordination', data)}
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
        return profileData.family_structure?.family_role && profileData.family_structure?.number_of_members > 0;
      case 2:
        return true; // Family members can be optional
      case 3:
        return true; // Household management is optional
      case 4:
        return true; // Care coordination is optional
      default:
        return true;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button 
                variant="ghost" 
                onClick={() => navigate('/')}
                className="hover:bg-amber-50"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Back to Home
              </Button>
              <div className="h-6 w-px bg-gray-300" />
              <h1 className="text-2xl font-bold text-gray-900">
                {isEditing ? 'Edit Family Profile' : 'Create Family Profile'}
              </h1>
            </div>
            
            {saveError && (
              <div className="text-red-600 text-sm">
                Save failed: {typeof saveError === 'string' ? saveError : 'Please fill in required fields to save your progress'}
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

export default FamilyProfileWizard;