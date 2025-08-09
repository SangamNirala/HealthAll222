import { useState, useEffect, useCallback } from 'react';
import { debounce } from 'lodash-es';

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
        setSaveError(error.message);
      } finally {
        setIsSaving(false);
      }
    }, delay),
    [saveFunction, delay]
  );

  // Trigger auto-save when data changes
  useEffect(() => {
    if (data && Object.keys(data).length > 0) {
      debouncedSave(data);
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
      setSaveError(error.message);
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