import React from 'react';
import { Button } from '../ui/button';
import { ArrowLeft, ArrowRight, Save } from 'lucide-react';

const WizardNavigation = ({
  currentStep,
  totalSteps,
  onPrevious,
  onNext,
  onSave,
  isNextDisabled = false,
  isLoading = false,
  showSave = false,
  nextButtonText = "Next",
  saveButtonText = "Save Profile",
  showAutoSaveIndicator = true,
}) => {
  const isFirstStep = currentStep === 1;
  const isLastStep = currentStep === totalSteps;

  return (
    <div className="flex justify-between items-center pt-6 border-t border-gray-200">
      {/* Previous Button */}
      <Button
        type="button"
        variant="outline"
        onClick={onPrevious}
        disabled={isFirstStep || isLoading}
        className="flex items-center"
      >
        <ArrowLeft className="w-4 h-4 mr-2" />
        Previous
      </Button>

      {/* Auto-save Indicator */}
      <div className="text-sm text-gray-500">
        {isLoading && (
          <div className="flex items-center">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500 mr-2"></div>
            Auto-saving...
          </div>
        )}
      </div>

      {/* Next/Save Buttons */}
      <div className="flex space-x-3">
        {showSave && (
          <Button
            type="button"
            variant="outline"
            onClick={onSave}
            disabled={isLoading}
            className="flex items-center"
          >
            <Save className="w-4 h-4 mr-2" />
            {saveButtonText}
          </Button>
        )}

        <Button
          type="button"
          onClick={isLastStep ? onSave : onNext}
          disabled={isNextDisabled || isLoading}
          className="flex items-center"
        >
          {isLastStep ? (
            <>
              <Save className="w-4 h-4 mr-2" />
              Complete Profile
            </>
          ) : (
            <>
              {nextButtonText}
              <ArrowRight className="w-4 h-4 ml-2" />
            </>
          )}
        </Button>
      </div>
    </div>
  );
};

export default WizardNavigation;