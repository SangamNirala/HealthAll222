import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { ArrowLeft, UserCheck, Target, Clock } from 'lucide-react';
import FormField from '../shared/FormField';
import ProfileAPI from '../../utils/profileApi';

const GuestProfileSetup = () => {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  // Profile data state
  const [profileData, setProfileData] = useState({
    basic_demographics: {
      age: '',
      gender: '',
      activity_level: ''
    },
    simple_goals: {
      goal_type: '',
      target_amount: '',
      timeframe: ''
    }
  });

  const genderOptions = [
    { value: 'male', label: 'Male' },
    { value: 'female', label: 'Female' },
    { value: 'other', label: 'Other' },
    { value: 'prefer_not_to_say', label: 'Prefer not to say' }
  ];

  const activityLevelOptions = [
    { value: 'SEDENTARY', label: 'Sedentary (Little/no exercise)' },
    { value: 'LIGHTLY_ACTIVE', label: 'Lightly Active (Light exercise 1-3 days/week)' },
    { value: 'MODERATELY_ACTIVE', label: 'Moderately Active (Moderate exercise 3-5 days/week)' },
    { value: 'VERY_ACTIVE', label: 'Very Active (Hard exercise 6-7 days/week)' },
    { value: 'EXTRA_ACTIVE', label: 'Extra Active (Very hard exercise, physical job)' }
  ];

  const goalTypeOptions = [
    { value: 'maintain', label: 'Maintain current weight' },
    { value: 'lose', label: 'Lose weight' },
    { value: 'gain', label: 'Gain weight' }
  ];

  const timeframeOptions = [
    { value: '1_month', label: '1 month' },
    { value: '3_months', label: '3 months' },
    { value: '6_months', label: '6 months' },
    { value: '1_year', label: '1 year' },
    { value: 'no_timeframe', label: 'No specific timeframe' }
  ];

  const handleDemographicsChange = (field, value) => {
    setProfileData(prev => ({
      ...prev,
      basic_demographics: {
        ...prev.basic_demographics,
        [field]: value
      }
    }));
  };

  const handleGoalsChange = (field, value) => {
    setProfileData(prev => ({
      ...prev,
      simple_goals: {
        ...prev.simple_goals,
        [field]: value
      }
    }));
  };

  const isFormValid = () => {
    const { basic_demographics, simple_goals } = profileData;
    return (
      basic_demographics.age && 
      basic_demographics.gender && 
      basic_demographics.activity_level &&
      simple_goals.goal_type
    );
  };

  const handleSubmit = async () => {
    if (!isFormValid()) return;

    setIsSubmitting(true);
    setError(null);

    try {
      // Generate session ID for guest
      const sessionId = `guest_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      
      // Set session expiration to 24 hours from now
      const sessionExpires = new Date();
      sessionExpires.setHours(sessionExpires.getHours() + 24);

      const guestProfilePayload = {
        session_id: sessionId,
        basic_demographics: {
          ...profileData.basic_demographics,
          age: parseInt(profileData.basic_demographics.age)
        },
        simple_goals: {
          ...profileData.simple_goals,
          target_amount: profileData.simple_goals.target_amount ? parseFloat(profileData.simple_goals.target_amount) : null
        },
        session_expires: sessionExpires.toISOString()
      };

      // Create guest profile
      await ProfileAPI.createGuestProfile(guestProfilePayload);

      // Navigate to guest dashboard with session info
      navigate('/guest-dashboard', { 
        state: { 
          sessionId,
          profileCompleted: true,
          message: 'Guest session started successfully!',
          sessionExpires: sessionExpires
        }
      });
    } catch (error) {
      console.error('Failed to create guest profile:', error);
      setError(error.message || 'Failed to create guest profile');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button 
                variant="ghost" 
                onClick={() => navigate('/')}
                className="hover:bg-purple-50"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Back to Home
              </Button>
              <div className="h-6 w-px bg-gray-300" />
              <h1 className="text-2xl font-bold text-gray-900">Quick Guest Setup</h1>
            </div>
            
            {error && (
              <div className="text-red-600 text-sm">
                {error}
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-6 py-8">
        <Card className="shadow-lg">
          <CardHeader className="text-center">
            <div className="mx-auto w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mb-4">
              <UserCheck className="w-8 h-8 text-purple-600" />
            </div>
            <CardTitle className="text-3xl font-bold text-gray-900">
              Start Your Health Journey
            </CardTitle>
            <p className="text-gray-600 mt-2">
              Quick setup to get started with basic nutrition tracking (no account required)
            </p>
          </CardHeader>
          
          <CardContent className="px-8 pb-8 space-y-8">
            {/* Basic Demographics */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <UserCheck className="w-5 h-5 mr-2 text-purple-600" />
                  Basic Information
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <FormField
                    type="number"
                    label="Age"
                    value={profileData.basic_demographics.age}
                    onChange={(value) => handleDemographicsChange('age', value)}
                    placeholder="Enter your age"
                    min="13"
                    max="120"
                    required
                    helpText="We use age to provide appropriate nutrition recommendations"
                  />

                  <FormField
                    type="select"
                    label="Gender"
                    value={profileData.basic_demographics.gender}
                    onChange={(value) => handleDemographicsChange('gender', value)}
                    options={genderOptions}
                    placeholder="Select gender"
                    required
                    helpText="Helps us provide more accurate calorie calculations"
                  />
                </div>

                <FormField
                  type="select"
                  label="Activity Level"
                  value={profileData.basic_demographics.activity_level}
                  onChange={(value) => handleDemographicsChange('activity_level', value)}
                  options={activityLevelOptions}
                  placeholder="Select your typical activity level"
                  required
                  helpText="This helps us estimate your daily calorie needs"
                />
              </CardContent>
            </Card>

            {/* Simple Goals */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Target className="w-5 h-5 mr-2 text-purple-600" />
                  Health Goals
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <FormField
                  type="select"
                  label="Primary Goal"
                  value={profileData.simple_goals.goal_type}
                  onChange={(value) => handleGoalsChange('goal_type', value)}
                  options={goalTypeOptions}
                  placeholder="Select your primary goal"
                  required
                  helpText="What is your main health objective?"
                />

                {profileData.simple_goals.goal_type !== 'maintain' && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <FormField
                      type="number"
                      label={`Target Amount (${profileData.simple_goals.goal_type === 'lose' ? 'lbs to lose' : 'lbs to gain'})`}
                      value={profileData.simple_goals.target_amount}
                      onChange={(value) => handleGoalsChange('target_amount', value)}
                      placeholder="Enter amount"
                      min="1"
                      max="100"
                      helpText="Optional: How much weight would you like to change?"
                    />

                    <FormField
                      type="select"
                      label="Timeframe"
                      value={profileData.simple_goals.timeframe}
                      onChange={(value) => handleGoalsChange('timeframe', value)}
                      options={timeframeOptions}
                      placeholder="Select timeframe"
                      helpText="Optional: When would you like to achieve this goal?"
                    />
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Guest Session Info */}
            <Card>
              <CardContent className="pt-6">
                <div className="bg-purple-50 p-4 rounded-lg">
                  <div className="flex items-start">
                    <Clock className="w-5 h-5 text-purple-600 mt-0.5 mr-3 flex-shrink-0" />
                    <div>
                      <h4 className="font-semibold text-purple-800 mb-2">Guest Session Features:</h4>
                      <ul className="text-sm text-purple-700 space-y-1">
                        <li>• Quick food logging and basic nutrition tracking</li>
                        <li>• Session lasts 24 hours from creation</li>
                        <li>• No account registration required</li>
                        <li>• Data is not permanently saved</li>
                        <li>• Perfect for trying out the platform</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Submit Button */}
            <div className="flex justify-center pt-6">
              <Button
                onClick={handleSubmit}
                disabled={!isFormValid() || isSubmitting}
                className="w-full md:w-auto px-12 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold text-lg"
              >
                {isSubmitting ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Starting Session...
                  </div>
                ) : (
                  <>
                    <UserCheck className="w-5 h-5 mr-2" />
                    Start Guest Session
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default GuestProfileSetup;