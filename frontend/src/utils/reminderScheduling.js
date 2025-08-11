/**
 * Smart Reminder Scheduling Utility
 * Handles intelligent medication reminder scheduling with adaptive algorithms
 */

// Meal timing constants
export const MEAL_TIMES = {
  BREAKFAST: { start: '06:00', end: '10:00', optimal: '08:00' },
  LUNCH: { start: '11:00', end: '15:00', optimal: '12:30' },
  DINNER: { start: '17:00', end: '21:00', optimal: '18:30' },
  BEDTIME: { start: '21:00', end: '23:59', optimal: '22:00' }
};

// Reminder intensity levels for escalation
export const REMINDER_INTENSITY = {
  GENTLE: { priority: 1, sound: 'soft', vibration: false },
  NORMAL: { priority: 2, sound: 'medium', vibration: true },
  URGENT: { priority: 3, sound: 'loud', vibration: true },
  EMERGENCY: { priority: 4, sound: 'emergency', vibration: true, emergency_contact: true }
};

// Snooze intelligence patterns
export const SNOOZE_PATTERNS = {
  PROGRESSIVE: [5, 10, 15, 20, 30], // minutes - increases each time
  FIXED: [10, 10, 10, 10, 10], // minutes - same interval
  ADAPTIVE: [5, 15, 10, 20, 15] // minutes - based on user patterns
};

/**
 * Smart Reminder Scheduler Class
 * Handles all intelligent reminder scheduling logic
 */
export class SmartReminderScheduler {
  constructor(userPreferences = {}) {
    this.userPreferences = {
      mealTimes: userPreferences.mealTimes || MEAL_TIMES,
      sleepSchedule: userPreferences.sleepSchedule || { bedtime: '22:00', wakeup: '07:00' },
      activityPatterns: userPreferences.activityPatterns || {},
      snoozePreference: userPreferences.snoozePreference || 'PROGRESSIVE',
      emergencyContacts: userPreferences.emergencyContacts || []
    };
    
    this.adherenceHistory = [];
    this.reminderHistory = [];
    this.snoozeHistory = [];
  }

  /**
   * Optimize reminder timing based on meal requirements
   * @param {Object} medication - Medication object with timing requirements
   * @returns {Array} - Optimized reminder times
   */
  optimizeMealBasedTiming(medication) {
    const { with_food, timing_preference, frequency } = medication;
    const optimizedTimes = [];

    if (with_food) {
      // Schedule around meal times
      switch (frequency) {
        case 'once_daily':
          optimizedTimes.push(this.userPreferences.mealTimes.BREAKFAST.optimal);
          break;
        case 'twice_daily':
          optimizedTimes.push(
            this.userPreferences.mealTimes.BREAKFAST.optimal,
            this.userPreferences.mealTimes.DINNER.optimal
          );
          break;
        case 'three_times_daily':
          optimizedTimes.push(
            this.userPreferences.mealTimes.BREAKFAST.optimal,
            this.userPreferences.mealTimes.LUNCH.optimal,
            this.userPreferences.mealTimes.DINNER.optimal
          );
          break;
        default:
          optimizedTimes.push(this.userPreferences.mealTimes.BREAKFAST.optimal);
      }
    } else {
      // Schedule between meals or based on sleep schedule
      const { bedtime, wakeup } = this.userPreferences.sleepSchedule;
      const wakeupTime = this.timeToMinutes(wakeup);
      const bedtimeTime = this.timeToMinutes(bedtime);
      const activeHours = bedtimeTime - wakeupTime;

      switch (frequency) {
        case 'once_daily':
          // Mid-morning, away from meals
          optimizedTimes.push(this.minutesToTime(wakeupTime + 120)); // 2 hours after wakeup
          break;
        case 'twice_daily':
          const interval = activeHours / 2;
          optimizedTimes.push(
            this.minutesToTime(wakeupTime + 60), // 1 hour after wakeup
            this.minutesToTime(wakeupTime + interval + 60)
          );
          break;
        case 'three_times_daily':
          const threeInterval = activeHours / 3;
          optimizedTimes.push(
            this.minutesToTime(wakeupTime + 60),
            this.minutesToTime(wakeupTime + threeInterval + 30),
            this.minutesToTime(wakeupTime + (threeInterval * 2) + 30)
          );
          break;
        default:
          optimizedTimes.push(this.minutesToTime(wakeupTime + 120));
      }
    }

    return optimizedTimes;
  }

  /**
   * Calculate adaptive reminder timing based on adherence patterns
   * @param {Object} medication - Medication object
   * @param {Array} adherenceData - Historical adherence data
   * @returns {Object} - Adaptive scheduling recommendations
   */
  calculateAdaptiveScheduling(medication, adherenceData) {
    const medicationHistory = adherenceData.filter(
      record => record.medication_id === medication.id
    );

    if (medicationHistory.length < 7) {
      // Not enough data, use standard optimization
      return {
        recommended_times: this.optimizeMealBasedTiming(medication),
        confidence: 'low',
        reason: 'Insufficient data for pattern analysis'
      };
    }

    // Analyze patterns
    const patterns = this.analyzeAdherencePatterns(medicationHistory);
    const adaptedTimes = this.adaptTimingBasedOnPatterns(
      medication,
      patterns
    );

    return {
      recommended_times: adaptedTimes,
      confidence: patterns.confidence,
      reason: patterns.insights,
      patterns: patterns
    };
  }

  /**
   * Analyze adherence patterns to identify optimal timing
   * @param {Array} medicationHistory - Historical data for specific medication
   * @returns {Object} - Pattern analysis results
   */
  analyzeAdherencePatterns(medicationHistory) {
    const timeOfDayData = {};
    const dayOfWeekData = {};
    const successfulTimes = [];
    const missedTimes = [];

    medicationHistory.forEach(record => {
      const date = new Date(record.scheduled_time);
      const hour = date.getHours();
      const dayOfWeek = date.getDay();
      const timeKey = `${hour}:00`;

      // Track time of day patterns
      if (!timeOfDayData[timeKey]) {
        timeOfDayData[timeKey] = { taken: 0, missed: 0 };
      }

      // Track day of week patterns
      if (!dayOfWeekData[dayOfWeek]) {
        dayOfWeekData[dayOfWeek] = { taken: 0, missed: 0 };
      }

      if (record.taken) {
        timeOfDayData[timeKey].taken++;
        dayOfWeekData[dayOfWeek].taken++;
        successfulTimes.push(record.actual_time || record.scheduled_time);
      } else {
        timeOfDayData[timeKey].missed++;
        dayOfWeekData[dayOfWeek].missed++;
        missedTimes.push(record.scheduled_time);
      }
    });

    // Calculate success rates
    const bestTimes = Object.entries(timeOfDayData)
      .map(([time, data]) => ({
        time,
        successRate: data.taken / (data.taken + data.missed),
        total: data.taken + data.missed
      }))
      .filter(item => item.total >= 3) // Minimum 3 occurrences
      .sort((a, b) => b.successRate - a.successRate);

    const bestDays = Object.entries(dayOfWeekData)
      .map(([day, data]) => ({
        day: parseInt(day),
        successRate: data.taken / (data.taken + data.missed),
        total: data.taken + data.missed
      }))
      .sort((a, b) => b.successRate - a.successRate);

    return {
      bestTimes: bestTimes.slice(0, 3),
      bestDays: bestDays.slice(0, 3),
      overallSuccess: medicationHistory.filter(r => r.taken).length / medicationHistory.length,
      confidence: medicationHistory.length >= 14 ? 'high' : 'medium',
      insights: this.generatePatternInsights(bestTimes, bestDays),
      averageDelay: this.calculateAverageDelay(successfulTimes, medicationHistory)
    };
  }

  /**
   * Implement smart snooze logic based on user patterns
   * @param {Object} reminder - Current reminder object
   * @param {Number} snoozeCount - How many times already snoozed
   * @returns {Object} - Snooze recommendation
   */
  calculateSmartSnooze(reminder, snoozeCount = 0) {
    const medication = reminder.medication;
    const currentTime = new Date();
    const scheduledTime = new Date(reminder.scheduled_time);
    const minutesLate = (currentTime - scheduledTime) / (1000 * 60);

    // Determine snooze pattern based on medication criticality and user history
    let snoozePattern = SNOOZE_PATTERNS[this.userPreferences.snoozePreference];
    
    // Adjust for critical medications
    if (medication.critical || medication.condition?.toLowerCase().includes('diabetes')) {
      snoozePattern = SNOOZE_PATTERNS.PROGRESSIVE;
    }

    // Calculate next snooze interval
    const snoozeInterval = snoozeCount < snoozePattern.length 
      ? snoozePattern[snoozeCount] 
      : snoozePattern[snoozePattern.length - 1];

    // Determine intensity escalation
    let intensity = REMINDER_INTENSITY.NORMAL;
    if (minutesLate > 60 || snoozeCount >= 3) {
      intensity = REMINDER_INTENSITY.URGENT;
    }
    if (minutesLate > 120 || snoozeCount >= 5) {
      intensity = REMINDER_INTENSITY.EMERGENCY;
    }

    // Consider meal timing conflicts
    const nextReminderTime = new Date(currentTime.getTime() + snoozeInterval * 60000);
    const mealConflict = this.checkMealConflicts(nextReminderTime, medication);

    if (mealConflict.hasConflict && !medication.with_food) {
      // Adjust timing to avoid meal conflicts for non-food medications
      return {
        snoozeMinutes: mealConflict.suggestedDelay,
        intensity,
        reason: `Adjusted to avoid ${mealConflict.mealType.toLowerCase()} time`,
        nextReminderTime: mealConflict.suggestedTime,
        escalation: snoozeCount >= 3
      };
    }

    return {
      snoozeMinutes: snoozeInterval,
      intensity,
      reason: snoozeCount === 0 ? 'First snooze' : `Snooze #${snoozeCount + 1}`,
      nextReminderTime,
      escalation: minutesLate > 60 || snoozeCount >= 3
    };
  }

  /**
   * Implement emergency escalation protocols
   * @param {Object} reminder - Reminder that needs escalation
   * @param {Object} adherenceData - Recent adherence data
   * @returns {Object} - Escalation plan
   */
  calculateEmergencyEscalation(reminder, adherenceData) {
    const medication = reminder.medication;
    const missedDoses = this.calculateRecentMissedDoses(medication.id, adherenceData, 7); // Last 7 days
    const criticalMedication = medication.critical || this.isCriticalMedication(medication);
    
    let escalationLevel = 'NONE';
    let actions = [];

    // Determine escalation level
    if (criticalMedication && missedDoses >= 2) {
      escalationLevel = 'HIGH';
    } else if (missedDoses >= 3) {
      escalationLevel = 'MEDIUM';
    } else if (missedDoses >= 5) {
      escalationLevel = 'HIGH';
    }

    // Define escalation actions
    switch (escalationLevel) {
      case 'MEDIUM':
        actions = [
          'Increase reminder frequency',
          'Send daily adherence report',
          'Suggest setting multiple alarms'
        ];
        break;
      case 'HIGH':
        actions = [
          'Notify emergency contacts',
          'Send urgent notifications every 15 minutes',
          'Recommend contacting healthcare provider',
          'Enable location-based reminders'
        ];
        break;
      default:
        actions = ['Monitor adherence closely'];
    }

    return {
      escalationLevel,
      actions,
      emergencyContacts: escalationLevel === 'HIGH' ? this.userPreferences.emergencyContacts : [],
      recommendedInterval: escalationLevel === 'HIGH' ? 15 : 30, // minutes
      requiresImmedateAction: criticalMedication && missedDoses >= 2
    };
  }

  /**
   * Track and analyze adherence patterns
   * @param {String} medicationId - Medication identifier
   * @param {Object} adherenceEvent - Event data (taken/missed)
   */
  trackAdherence(medicationId, adherenceEvent) {
    const record = {
      medication_id: medicationId,
      scheduled_time: adherenceEvent.scheduled_time,
      actual_time: adherenceEvent.actual_time,
      taken: adherenceEvent.taken,
      delay_minutes: adherenceEvent.delay_minutes || 0,
      reason_missed: adherenceEvent.reason_missed,
      timestamp: new Date().toISOString()
    };

    this.adherenceHistory.push(record);
    
    // Keep only last 90 days of data
    const ninetyDaysAgo = new Date();
    ninetyDaysAgo.setDate(ninetyDaysAgo.getDate() - 90);
    
    this.adherenceHistory = this.adherenceHistory.filter(
      record => new Date(record.timestamp) > ninetyDaysAgo
    );

    // Update patterns if significant change
    this.updateLearningPatterns(medicationId);
  }

  // Helper methods
  timeToMinutes(timeString) {
    const [hours, minutes] = timeString.split(':').map(Number);
    return hours * 60 + minutes;
  }

  minutesToTime(minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}`;
  }

  checkMealConflicts(reminderTime, medication) {
    const hour = reminderTime.getHours();
    const timeString = `${hour.toString().padStart(2, '0')}:00`;
    
    for (const [mealType, mealTime] of Object.entries(this.userPreferences.mealTimes)) {
      const startMinutes = this.timeToMinutes(mealTime.start);
      const endMinutes = this.timeToMinutes(mealTime.end);
      const reminderMinutes = this.timeToMinutes(timeString);
      
      if (reminderMinutes >= startMinutes && reminderMinutes <= endMinutes) {
        if (medication.with_food) {
          return { hasConflict: false }; // Good timing for food-dependent medication
        } else {
          // Suggest timing after meal window
          const suggestedTime = new Date(reminderTime);
          suggestedTime.setHours(Math.floor(endMinutes / 60), endMinutes % 60 + 30);
          
          return {
            hasConflict: true,
            mealType,
            suggestedTime,
            suggestedDelay: 30 + (endMinutes - reminderMinutes)
          };
        }
      }
    }
    
    return { hasConflict: false };
  }

  isCriticalMedication(medication) {
    const criticalConditions = [
      'diabetes', 'heart', 'hypertension', 'seizure', 'epilepsy', 
      'blood pressure', 'insulin', 'warfarin', 'anticoagulant'
    ];
    
    const condition = medication.condition?.toLowerCase() || '';
    const name = medication.name?.toLowerCase() || '';
    
    return criticalConditions.some(critical => 
      condition.includes(critical) || name.includes(critical)
    );
  }

  calculateRecentMissedDoses(medicationId, adherenceData, days) {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);
    
    return adherenceData
      .filter(record => 
        record.medication_id === medicationId &&
        new Date(record.scheduled_time) > cutoffDate &&
        !record.taken
      )
      .length;
  }

  calculateAverageDelay(successfulTimes, medicationHistory) {
    let totalDelay = 0;
    let count = 0;

    medicationHistory.forEach(record => {
      if (record.taken && record.actual_time) {
        const scheduled = new Date(record.scheduled_time);
        const actual = new Date(record.actual_time);
        const delay = (actual - scheduled) / (1000 * 60); // minutes
        
        if (delay > 0) {
          totalDelay += delay;
          count++;
        }
      }
    });

    return count > 0 ? Math.round(totalDelay / count) : 0;
  }

  generatePatternInsights(bestTimes, bestDays) {
    const insights = [];
    
    if (bestTimes.length > 0) {
      const topTime = bestTimes[0];
      insights.push(`Best adherence at ${topTime.time} (${Math.round(topTime.successRate * 100)}% success)`);
    }

    if (bestDays.length > 0) {
      const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
      const topDay = bestDays[0];
      insights.push(`Higher adherence on ${dayNames[topDay.day]}s`);
    }

    return insights.join('; ');
  }

  adaptTimingBasedOnPatterns(medication, patterns) {
    const currentTimes = this.optimizeMealBasedTiming(medication);
    
    if (patterns.bestTimes.length === 0) {
      return currentTimes;
    }

    // Adapt timing based on successful patterns
    const adaptedTimes = patterns.bestTimes
      .slice(0, currentTimes.length)
      .map(pattern => pattern.time);

    return adaptedTimes.length > 0 ? adaptedTimes : currentTimes;
  }

  updateLearningPatterns(medicationId) {
    // Implementation for updating learned patterns
    // This would typically involve more complex ML algorithms
    // For now, we'll keep it simple and just ensure data is current
    const medicationData = this.adherenceHistory.filter(
      record => record.medication_id === medicationId
    );

    if (medicationData.length >= 21) { // 3 weeks of data
      // Trigger pattern recalculation
      const patterns = this.analyzeAdherencePatterns(medicationData);
      // Store updated patterns (would typically go to localStorage or backend)
      console.log(`Updated patterns for medication ${medicationId}:`, patterns);
    }
  }

  // Public API methods for easy integration
  
  /**
   * Get comprehensive reminder schedule for a medication
   * @param {Object} medication - Medication object
   * @param {Array} adherenceData - Historical adherence data
   * @returns {Object} - Complete scheduling recommendation
   */
  getSmartSchedule(medication, adherenceData = []) {
    const mealOptimized = this.optimizeMealBasedTiming(medication);
    const adaptive = this.calculateAdaptiveScheduling(medication, adherenceData);
    const escalation = this.calculateEmergencyEscalation(
      { medication }, 
      adherenceData
    );

    return {
      medication_id: medication.id,
      meal_optimized_times: mealOptimized,
      adaptive_schedule: adaptive,
      emergency_escalation: escalation,
      generated_at: new Date().toISOString(),
      confidence: adaptive.confidence
    };
  }
}

// Export utility functions for direct use
export const createSmartScheduler = (userPreferences) => {
  return new SmartReminderScheduler(userPreferences);
};

export const defaultScheduler = new SmartReminderScheduler();