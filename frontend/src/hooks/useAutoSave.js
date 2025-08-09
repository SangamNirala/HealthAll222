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
      // Check if data has actual meaningful content, not just empty objects
      const hasContent = Object.values(data).some(section => {
        if (section === null || section === undefined) return false;
        if (Array.isArray(section)) return section.length > 0;
        if (typeof section === 'object') {
          return Object.keys(section).length > 0 && Object.values(section).some(value => 
            value !== null && value !== undefined && value !== ''
          );
        }
        return true;
      });
      
      if (hasContent) {
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