import { useState, useEffect, useCallback } from 'react';
import { debounce } from 'lodash-es';
import { hasCompleteSections } from '../utils/profileValidation';

const useAutoSave = (data, saveFunction, delay = 1000) => {
  const [isSaving, setIsSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState(null);
  const [saveError, setSaveError] = useState(null);

  // Debounced save function
  const debouncedSave = useCallback(
    debounce(async (dataToSave) => {
      // Check if we actually have complete sections before setting saving state
      if (!hasCompleteSections(dataToSave)) {
        return; // Don't save or show saving state if no complete sections
      }
      
      try {
        setIsSaving(true);
        setSaveError(null);
        await saveFunction(dataToSave);
        setLastSaved(new Date());
      } catch (error) {
        console.error('Auto-save failed:', error);
        // Improve error message handling for better user experience
        let errorMessage = 'Please fill in required fields to save your progress';
        
        if (error.message && typeof error.message === 'string') {
          // Check if it's a validation error from backend
          if (error.message.includes('validation error') || error.message.includes('422')) {
            errorMessage = 'Please complete required fields before saving';
          } else if (!error.message.includes('[object Object]')) {
            errorMessage = error.message;
          }
        }
        
        setSaveError(errorMessage);
      } finally {
        setIsSaving(false);
      }
    }, delay),
    [saveFunction, delay]
  );

  // Trigger auto-save when data changes
  useEffect(() => {
    if (data && Object.keys(data).length > 0) {
      // Only auto-save if at least one complete section exists
      if (hasCompleteSections(data)) {
        debouncedSave(data);
      }
    }

    // Cleanup
    return () => {
      debouncedSave.cancel();
    };
  }, [data, debouncedSave]);

  // Manual save function
  const saveNow = useCallback(async () => {
    debouncedSave.cancel(); // Cancel any pending debounced saves
    try {
      setIsSaving(true);
      setSaveError(null);
      await saveFunction(data);
      setLastSaved(new Date());
    } catch (error) {
      console.error('Manual save failed:', error);
      // Improve error message handling for better user experience
      let errorMessage = 'Please fill in required fields to save your progress';
      
      if (error.message && typeof error.message === 'string') {
        // Check if it's a validation error from backend
        if (error.message.includes('validation error') || error.message.includes('422')) {
          errorMessage = 'Please complete required fields before saving';
        } else if (!error.message.includes('[object Object]')) {
          errorMessage = error.message;
        }
      }
      
      setSaveError(errorMessage);
      throw error;
    } finally {
      setIsSaving(false);
    }
  }, [data, saveFunction, debouncedSave]);

  return {
    isSaving,
    lastSaved,
    saveError,
    saveNow
  };
};

export default useAutoSave;