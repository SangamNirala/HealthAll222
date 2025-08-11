// Statistical correlation analysis utilities

/**
 * Calculate Pearson correlation coefficient
 * @param {number[]} x - Array of x values
 * @param {number[]} y - Array of y values
 * @returns {number} Correlation coefficient between -1 and 1
 */
export const pearsonCorrelation = (x, y) => {
  if (x.length !== y.length || x.length < 2) {
    return 0;
  }

  const n = x.length;
  const sumX = x.reduce((sum, val) => sum + val, 0);
  const sumY = y.reduce((sum, val) => sum + val, 0);
  const sumXY = x.reduce((sum, val, i) => sum + val * y[i], 0);
  const sumX2 = x.reduce((sum, val) => sum + val * val, 0);
  const sumY2 = y.reduce((sum, val) => sum + val * val, 0);

  const numerator = n * sumXY - sumX * sumY;
  const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));

  return denominator === 0 ? 0 : numerator / denominator;
};

/**
 * Calculate Spearman rank correlation coefficient
 * @param {number[]} x - Array of x values
 * @param {number[]} y - Array of y values
 * @returns {number} Spearman correlation coefficient
 */
export const spearmanCorrelation = (x, y) => {
  if (x.length !== y.length || x.length < 2) {
    return 0;
  }

  const xRanks = getRanks(x);
  const yRanks = getRanks(y);
  
  return pearsonCorrelation(xRanks, yRanks);
};

/**
 * Get ranks for an array of values
 * @param {number[]} arr - Array of numbers
 * @returns {number[]} Array of ranks
 */
const getRanks = (arr) => {
  const sorted = arr
    .map((val, index) => ({ val, index }))
    .sort((a, b) => a.val - b.val);
  
  const ranks = new Array(arr.length);
  
  for (let i = 0; i < sorted.length; i++) {
    ranks[sorted[i].index] = i + 1;
  }
  
  return ranks;
};

/**
 * Generate correlation matrix for multiple datasets
 * @param {Object} datasets - Object with dataset names as keys and arrays as values
 * @returns {Object} Correlation matrix
 */
export const correlationMatrix = (datasets) => {
  const keys = Object.keys(datasets);
  const matrix = {};
  
  keys.forEach(keyX => {
    matrix[keyX] = {};
    keys.forEach(keyY => {
      if (keyX === keyY) {
        matrix[keyX][keyY] = 1.0;
      } else {
        matrix[keyX][keyY] = pearsonCorrelation(datasets[keyX], datasets[keyY]);
      }
    });
  });
  
  return matrix;
};

/**
 * Analyze eating patterns from food log data
 * @param {Array} foodLogs - Array of food log entries
 * @returns {Object} Pattern analysis results
 */
export const analyzeEatingPatterns = (foodLogs) => {
  if (!foodLogs || foodLogs.length === 0) {
    return {
      mealTiming: {},
      foodPreferences: {},
      goalAdherence: {}
    };
  }

  return {
    mealTiming: analyzeMealTiming(foodLogs),
    foodPreferences: analyzeFoodPreferences(foodLogs),
    goalAdherence: analyzeGoalAdherence(foodLogs)
  };
};

/**
 * Analyze meal timing patterns
 * @param {Array} foodLogs - Food log entries
 * @returns {Object} Meal timing analysis
 */
const analyzeMealTiming = (foodLogs) => {
  const mealTimes = {
    breakfast: [],
    lunch: [],
    dinner: [],
    snacks: []
  };

  foodLogs.forEach(log => {
    if (log.timestamp) {
      const hour = new Date(log.timestamp).getHours();
      const mealType = log.meal_type || categorizeMealByTime(hour);
      
      if (mealTimes[mealType]) {
        mealTimes[mealType].push(hour);
      }
    }
  });

  // Calculate average timing for each meal
  const averageTiming = {};
  Object.keys(mealTimes).forEach(meal => {
    if (mealTimes[meal].length > 0) {
      const sum = mealTimes[meal].reduce((a, b) => a + b, 0);
      averageTiming[meal] = (sum / mealTimes[meal].length).toFixed(1);
    }
  });

  return {
    averageTiming,
    consistency: calculateTimingConsistency(mealTimes),
    patterns: identifyTimingPatterns(mealTimes)
  };
};

/**
 * Categorize meal by time of day
 * @param {number} hour - Hour of the day (0-23)
 * @returns {string} Meal category
 */
const categorizeMealByTime = (hour) => {
  if (hour >= 5 && hour <= 10) return 'breakfast';
  if (hour >= 11 && hour <= 15) return 'lunch';
  if (hour >= 17 && hour <= 22) return 'dinner';
  return 'snacks';
};

/**
 * Calculate timing consistency
 * @param {Object} mealTimes - Meal times by category
 * @returns {Object} Consistency scores
 */
const calculateTimingConsistency = (mealTimes) => {
  const consistency = {};
  
  Object.keys(mealTimes).forEach(meal => {
    const times = mealTimes[meal];
    if (times.length > 1) {
      const mean = times.reduce((a, b) => a + b, 0) / times.length;
      const variance = times.reduce((sum, time) => sum + Math.pow(time - mean, 2), 0) / times.length;
      const standardDeviation = Math.sqrt(variance);
      
      // Lower deviation = higher consistency (scale 0-100)
      consistency[meal] = Math.max(0, 100 - (standardDeviation * 10));
    } else {
      consistency[meal] = 100; // Single meal = perfectly consistent
    }
  });
  
  return consistency;
};

/**
 * Identify timing patterns
 * @param {Object} mealTimes - Meal times by category
 * @returns {Object} Identified patterns
 */
const identifyTimingPatterns = (mealTimes) => {
  const patterns = {};
  
  Object.keys(mealTimes).forEach(meal => {
    const times = mealTimes[meal];
    if (times.length >= 5) {
      // Identify most common time ranges
      const timeRanges = {};
      times.forEach(time => {
        const range = Math.floor(time / 2) * 2; // 2-hour buckets
        timeRanges[range] = (timeRanges[range] || 0) + 1;
      });
      
      const mostCommon = Object.entries(timeRanges)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 2)
        .map(([range, count]) => ({
          timeRange: `${range}:00-${parseInt(range) + 2}:00`,
          frequency: ((count / times.length) * 100).toFixed(1)
        }));
      
      patterns[meal] = mostCommon;
    }
  });
  
  return patterns;
};

/**
 * Analyze food preferences
 * @param {Array} foodLogs - Food log entries
 * @returns {Object} Food preference analysis
 */
const analyzeFoodPreferences = (foodLogs) => {
  const foodCounts = {};
  const categorycounts = {};
  const macroTotals = { protein: 0, carbs: 0, fat: 0 };
  
  foodLogs.forEach(log => {
    // Count individual foods
    if (log.food_name) {
      foodCounts[log.food_name] = (foodCounts[log.food_name] || 0) + 1;
    }
    
    // Count food categories
    if (log.category) {
      categoryCounts[log.category] = (categoryCounts[log.category] || 0) + 1;
    }
    
    // Sum macronutrients
    macroTotals.protein += log.protein || 0;
    macroTotals.carbs += log.carbs || 0;
    macroTotals.fat += log.fat || 0;
  });
  
  // Calculate macro preferences
  const macroTotal = macroTotals.protein + macroTotals.carbs + macroTotals.fat;
  const macroPercentages = {
    protein: macroTotal > 0 ? ((macroTotals.protein / macroTotal) * 100).toFixed(1) : 0,
    carbs: macroTotal > 0 ? ((macroTotals.carbs / macroTotal) * 100).toFixed(1) : 0,
    fat: macroTotal > 0 ? ((macroTotals.fat / macroTotal) * 100).toFixed(1) : 0
  };
  
  return {
    topFoods: Object.entries(foodCounts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10)
      .map(([food, count]) => ({ food, count })),
    topCategories: Object.entries(categoryCounts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 5)
      .map(([category, count]) => ({ category, count })),
    macroPreferences: macroPercentages
  };
};

/**
 * Analyze goal adherence patterns
 * @param {Array} foodLogs - Food log entries
 * @returns {Object} Goal adherence analysis
 */
const analyzeGoalAdherence = (foodLogs) => {
  // Group by date
  const dailyData = {};
  
  foodLogs.forEach(log => {
    const date = log.date || new Date(log.timestamp).toISOString().split('T')[0];
    if (!dailyData[date]) {
      dailyData[date] = { calories: 0, protein: 0, carbs: 0, fat: 0 };
    }
    
    dailyData[date].calories += log.calories || 0;
    dailyData[date].protein += log.protein || 0;
    dailyData[date].carbs += log.carbs || 0;
    dailyData[date].fat += log.fat || 0;
  });
  
  // Analyze against typical goals (these could be user-specific)
  const goals = {
    calories: 2000,
    protein: 150,
    carbs: 250,
    fat: 65
  };
  
  const adherence = {};
  const dates = Object.keys(dailyData);
  
  Object.keys(goals).forEach(nutrient => {
    const adherenceScores = dates.map(date => {
      const actual = dailyData[date][nutrient];
      const target = goals[nutrient];
      const score = Math.min(100, (actual / target) * 100);
      return score;
    });
    
    adherence[nutrient] = {
      average: adherenceScores.length > 0 ? 
        (adherenceScores.reduce((a, b) => a + b, 0) / adherenceScores.length).toFixed(1) : 0,
      consistency: calculateAdherenceConsistency(adherenceScores),
      trend: calculateAdherenceTrend(adherenceScores)
    };
  });
  
  return adherence;
};

/**
 * Calculate adherence consistency
 * @param {number[]} scores - Array of adherence scores
 * @returns {number} Consistency score (0-100)
 */
const calculateAdherenceConsistency = (scores) => {
  if (scores.length < 2) return 100;
  
  const mean = scores.reduce((a, b) => a + b, 0) / scores.length;
  const variance = scores.reduce((sum, score) => sum + Math.pow(score - mean, 2), 0) / scores.length;
  const standardDeviation = Math.sqrt(variance);
  
  // Lower deviation = higher consistency
  return Math.max(0, 100 - standardDeviation);
};

/**
 * Calculate adherence trend
 * @param {number[]} scores - Array of adherence scores
 * @returns {string} Trend direction
 */
const calculateAdherenceTrend = (scores) => {
  if (scores.length < 2) return 'stable';
  
  const firstHalf = scores.slice(0, Math.floor(scores.length / 2));
  const secondHalf = scores.slice(Math.floor(scores.length / 2));
  
  const firstAvg = firstHalf.reduce((a, b) => a + b, 0) / firstHalf.length;
  const secondAvg = secondHalf.reduce((a, b) => a + b, 0) / secondHalf.length;
  
  const difference = secondAvg - firstAvg;
  
  if (difference > 5) return 'improving';
  if (difference < -5) return 'declining';
  return 'stable';
};

/**
 * Calculate moving average for trend analysis
 * @param {number[]} data - Array of numbers
 * @param {number} window - Window size for moving average
 * @returns {number[]} Array of moving averages
 */
export const movingAverage = (data, window = 3) => {
  if (data.length < window) return data;
  
  const result = [];
  for (let i = window - 1; i < data.length; i++) {
    const slice = data.slice(i - window + 1, i + 1);
    const avg = slice.reduce((sum, val) => sum + val, 0) / window;
    result.push(avg);
  }
  
  return result;
};

/**
 * Detect outliers using IQR method
 * @param {number[]} data - Array of numbers
 * @returns {Object} Object with outliers and cleaned data
 */
export const detectOutliers = (data) => {
  if (data.length < 4) return { outliers: [], cleanData: data };
  
  const sorted = [...data].sort((a, b) => a - b);
  const q1Index = Math.floor(sorted.length * 0.25);
  const q3Index = Math.floor(sorted.length * 0.75);
  
  const q1 = sorted[q1Index];
  const q3 = sorted[q3Index];
  const iqr = q3 - q1;
  
  const lowerBound = q1 - 1.5 * iqr;
  const upperBound = q3 + 1.5 * iqr;
  
  const outliers = [];
  const cleanData = [];
  
  data.forEach((value, index) => {
    if (value < lowerBound || value > upperBound) {
      outliers.push({ value, index });
    } else {
      cleanData.push(value);
    }
  });
  
  return { outliers, cleanData };
};