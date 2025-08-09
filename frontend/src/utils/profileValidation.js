// Profile section validation utilities
// These functions check if a profile section has all required fields completed

export const validateBasicInfo = (basicInfo) => {
  if (!basicInfo || typeof basicInfo !== 'object') return false;
  
  const requiredFields = ['full_name', 'age', 'gender', 'location', 'timezone'];
  return requiredFields.every(field => {
    const value = basicInfo[field];
    return value !== null && value !== undefined && value !== '';
  });
};

export const validatePhysicalMetrics = (physicalMetrics) => {
  if (!physicalMetrics || typeof physicalMetrics !== 'object') return false;
  
  const requiredFields = ['height_cm', 'current_weight_kg'];
  return requiredFields.every(field => {
    const value = physicalMetrics[field];
    return value !== null && value !== undefined && value !== '' && !isNaN(value) && value > 0;
  });
};

export const validateActivityProfile = (activityProfile) => {
  if (!activityProfile || typeof activityProfile !== 'object') return false;
  
  // Check required top-level fields
  const requiredFields = ['activity_level', 'exercise_frequency', 'stress_level', 'work_type'];
  const hasRequiredFields = requiredFields.every(field => {
    const value = activityProfile[field];
    return value !== null && value !== undefined && value !== '';
  });
  
  if (!hasRequiredFields) return false;
  
  // Check sleep_schedule sub-object
  const sleepSchedule = activityProfile.sleep_schedule;
  if (!sleepSchedule || typeof sleepSchedule !== 'object') return false;
  
  const sleepRequiredFields = ['bedtime', 'wake_time', 'sleep_quality'];
  return sleepRequiredFields.every(field => {
    const value = sleepSchedule[field];
    return value !== null && value !== undefined && value !== '';
  });
};

export const validateDietaryProfile = (dietaryProfile) => {
  if (!dietaryProfile || typeof dietaryProfile !== 'object') return false;
  
  const requiredFields = ['diet_type', 'meal_timing_preference', 'cooking_skill_level', 'available_cooking_time'];
  return requiredFields.every(field => {
    const value = dietaryProfile[field];
    return value !== null && value !== undefined && value !== '';
  });
};

export const validateHealthHistory = (healthHistory) => {
  // Health history is optional, but we only consider it "complete" if it has some content
  // This prevents auto-save from triggering on empty optional sections
  if (!healthHistory || typeof healthHistory !== 'object') return false;
  
  // Consider it complete if at least one meaningful field has data
  const hasContent = Object.values(healthHistory).some(value => {
    if (Array.isArray(value)) return value.length > 0;
    if (typeof value === 'object' && value !== null) return Object.keys(value).length > 0;
    return value !== null && value !== undefined && value !== '';
  });
  
  return hasContent;
};

export const validateGoalsPreferences = (goalsPreferences) => {
  // Goals and preferences are optional, but we only consider it "complete" if it has some content
  // This prevents auto-save from triggering on empty optional sections
  if (!goalsPreferences || typeof goalsPreferences !== 'object') return false;
  
  // Consider it complete if at least one meaningful field has data
  const hasContent = Object.values(goalsPreferences).some(value => {
    if (Array.isArray(value)) return value.length > 0;
    if (typeof value === 'object' && value !== null) return Object.keys(value).length > 0;
    return value !== null && value !== undefined && value !== '';
  });
  
  return hasContent;
};

// Main function to check if profile data has any complete sections
export const hasCompleteSections = (profileData) => {
  if (!profileData || typeof profileData !== 'object') return false;
  
  const validators = {
    basic_info: validateBasicInfo,
    physical_metrics: validatePhysicalMetrics,
    activity_profile: validateActivityProfile,
    health_history: validateHealthHistory,
    dietary_profile: validateDietaryProfile,
    goals_preferences: validateGoalsPreferences
  };
  
  // Check if at least one section is complete
  const completeSections = Object.entries(profileData).filter(([sectionName, sectionData]) => {
    const validator = validators[sectionName];
    const isComplete = validator && validator(sectionData);
    
    // Debug logging - remove this later
    if (process.env.NODE_ENV === 'development') {
      console.log(`Section ${sectionName}: ${isComplete ? 'COMPLETE' : 'INCOMPLETE'}`, sectionData);
    }
    
    return isComplete;
  });
  
  const hasComplete = completeSections.length > 0;
  
  // Debug logging - remove this later
  if (process.env.NODE_ENV === 'development') {
    console.log(`hasCompleteSections result: ${hasComplete}`, completeSections.map(([name]) => name));
  }
  
  return hasComplete;
};

// Function to get completion status for each section
export const getSectionCompletionStatus = (profileData) => {
  if (!profileData || typeof profileData !== 'object') {
    return {
      basic_info: false,
      physical_metrics: false,
      activity_profile: false,
      health_history: false,
      dietary_profile: false,
      goals_preferences: false
    };
  }
  
  const validators = {
    basic_info: validateBasicInfo,
    physical_metrics: validatePhysicalMetrics,
    activity_profile: validateActivityProfile,
    health_history: validateHealthHistory,
    dietary_profile: validateDietaryProfile,
    goals_preferences: validateGoalsPreferences
  };
  
  const completionStatus = {};
  Object.entries(validators).forEach(([sectionName, validator]) => {
    completionStatus[sectionName] = validator(profileData[sectionName]);
  });
  
  return completionStatus;
};

// Function to get list of missing fields for a section (useful for user feedback)
export const getMissingFields = (sectionName, sectionData) => {
  const missingFields = [];
  
  switch (sectionName) {
    case 'basic_info':
      const basicRequiredFields = ['full_name', 'age', 'gender', 'location', 'timezone'];
      basicRequiredFields.forEach(field => {
        const value = sectionData?.[field];
        if (value === null || value === undefined || value === '') {
          missingFields.push(field);
        }
      });
      break;
      
    case 'physical_metrics':
      const physicalRequiredFields = ['height_cm', 'current_weight_kg'];
      physicalRequiredFields.forEach(field => {
        const value = sectionData?.[field];
        if (value === null || value === undefined || value === '' || isNaN(value) || value <= 0) {
          missingFields.push(field);
        }
      });
      break;
      
    case 'activity_profile':
      const activityRequiredFields = ['activity_level', 'exercise_frequency', 'stress_level', 'work_type'];
      activityRequiredFields.forEach(field => {
        const value = sectionData?.[field];
        if (value === null || value === undefined || value === '') {
          missingFields.push(field);
        }
      });
      
      // Check sleep schedule
      const sleepSchedule = sectionData?.sleep_schedule;
      if (!sleepSchedule) {
        missingFields.push('sleep_schedule');
      } else {
        const sleepRequiredFields = ['bedtime', 'wake_time', 'sleep_quality'];
        sleepRequiredFields.forEach(field => {
          const value = sleepSchedule[field];
          if (value === null || value === undefined || value === '') {
            missingFields.push(`sleep_schedule.${field}`);
          }
        });
      }
      break;
      
    case 'dietary_profile':
      const dietaryRequiredFields = ['diet_type', 'meal_timing_preference', 'cooking_skill_level', 'available_cooking_time'];
      dietaryRequiredFields.forEach(field => {
        const value = sectionData?.[field];
        if (value === null || value === undefined || value === '') {
          missingFields.push(field);
        }
      });
      break;
      
    default:
      // health_history and goals_preferences have no required fields
      break;
  }
  
  return missingFields;
};