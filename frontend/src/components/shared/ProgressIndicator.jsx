import React from 'react';
import { Progress } from '../ui/progress';
import { Check, CheckCircle } from 'lucide-react';

const ProgressIndicator = ({ currentStep, totalSteps, stepLabels = [], sectionCompletion = {}, stepToSection }) => {
  const progressPercentage = ((currentStep - 1) / (totalSteps - 1)) * 100;
  
  // Default step-to-section mapping for patient profiles, can be overridden via props
  const defaultStepToSection = {
    1: 'basic_info',
    2: 'physical_metrics', 
    3: 'activity_profile',
    4: 'health_history',
    5: 'dietary_profile',
    6: 'goals_preferences'
  };

  // Use provided stepToSection mapping or fall back to default
  const stepSectionMapping = stepToSection || defaultStepToSection;

  return (
    <div className="w-full mb-8">
      {/* Progress Bar */}
      <div className="mb-4">
        <Progress value={progressPercentage} className="h-2" />
        <div className="flex justify-between mt-2 text-sm text-gray-600">
          <span>Step {currentStep} of {totalSteps}</span>
          <span>{Math.round(progressPercentage)}% Complete</span>
        </div>
      </div>

      {/* Step Indicators */}
      <div className="flex justify-between items-center">
        {Array.from({ length: totalSteps }, (_, index) => {
          const stepNumber = index + 1;
          const isCompleted = stepNumber < currentStep;
          const isCurrent = stepNumber === currentStep;
          const sectionName = stepToSection[stepNumber];
          const isSectionComplete = sectionCompletion[sectionName] || false;

          return (
            <div key={stepNumber} className="flex flex-col items-center relative">
              {/* Section Complete Indicator */}
              {isSectionComplete && (
                <CheckCircle className="w-3 h-3 text-green-500 absolute -top-1 -right-1 bg-white rounded-full" />
              )}
              
              {/* Step Circle */}
              <div
                className={`
                  w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium
                  ${isCompleted 
                    ? 'bg-green-500 text-white' 
                    : isCurrent 
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-500'
                  }
                `}
              >
                {isCompleted ? (
                  <Check className="w-4 h-4" />
                ) : (
                  stepNumber
                )}
              </div>

              {/* Step Label */}
              {stepLabels[index] && (
                <div
                  className={`
                    mt-2 text-xs text-center max-w-20
                    ${isCurrent ? 'text-blue-600 font-medium' : 'text-gray-500'}
                  `}
                >
                  {stepLabels[index]}
                  {isSectionComplete && (
                    <div className="text-green-600 font-medium">✓ Saved</div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ProgressIndicator;