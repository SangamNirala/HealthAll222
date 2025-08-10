import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001/api';

/**
 * Data Export Utility for all roles
 * Handles downloading and formatting exported data
 */

// Export data for different roles
export const exportData = async (role, userId, format = 'json') => {
  try {
    let endpoint;
    
    switch (role) {
      case 'patient':
        endpoint = `/api/patient/export/${userId}`;
        break;
      case 'provider':
        endpoint = `/api/provider/export/${userId}`;
        break;
      case 'family':
        endpoint = `/api/family/export/${userId}`;
        break;
      case 'guest':
        endpoint = `/api/guest/export/${userId}`;
        break;
      default:
        throw new Error(`Unsupported role: ${role}`);
    }

    const response = await axios.get(`${API_BASE_URL}${endpoint}?format=${format}`);
    return response.data;
  } catch (error) {
    if (error.response?.status === 404) {
      throw new Error('Profile not found');
    } else if (error.response?.status === 410) {
      throw new Error('Session expired');
    } else {
      throw new Error(`Export failed: ${error.message}`);
    }
  }
};

// Download exported data as file
export const downloadExportedData = (data, filename, format = 'json') => {
  let content, mimeType;
  
  if (format === 'json') {
    content = JSON.stringify(data, null, 2);
    mimeType = 'application/json';
    filename = `${filename}.json`;
  } else if (format === 'csv') {
    content = convertToCSV(data);
    mimeType = 'text/csv';
    filename = `${filename}.csv`;
  } else {
    throw new Error('Unsupported format');
  }

  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  
  link.href = url;
  link.download = filename;
  link.style.display = 'none';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  
  URL.revokeObjectURL(url);
};

// Convert JSON data to CSV format
const convertToCSV = (data) => {
  let csv = '';
  
  // Add export info
  csv += 'Export Information\n';
  csv += `Role,${data.export_info?.role || 'N/A'}\n`;
  csv += `Exported At,${data.export_info?.exported_at || 'N/A'}\n`;
  csv += `User ID,${data.export_info?.user_id || data.export_info?.family_id || data.export_info?.session_id || 'N/A'}\n\n`;
  
  // Add profile data
  if (data.profile) {
    csv += 'Profile Data\n';
    csv += convertObjectToCSV(data.profile, 'Profile');
    csv += '\n';
  }
  
  // Add role-specific data
  if (data.health_data && data.export_info?.role === 'patient') {
    csv += 'Health Data\n';
    csv += convertObjectToCSV(data.health_data, 'Health');
    csv += '\n';
    
    if (data.food_logs) {
      csv += 'Food Logs\n';
      csv += 'Date,Meal,Food,Calories,Protein\n';
      data.food_logs.forEach(log => {
        Object.entries(log.meals).forEach(([mealType, foods]) => {
          foods.forEach(food => {
            csv += `${log.date},${mealType},${food.food},${food.calories},${food.protein}\n`;
          });
        });
      });
      csv += '\n';
    }
  }
  
  if (data.practice_data && data.export_info?.role === 'provider') {
    csv += 'Practice Data\n';
    csv += convertObjectToCSV(data.practice_data, 'Practice');
    csv += '\n';
  }
  
  if (data.family_health_data && data.export_info?.role === 'family') {
    csv += 'Family Health Data\n';
    csv += convertObjectToCSV(data.family_health_data, 'Family Health');
    csv += '\n';
    
    if (data.meal_planning) {
      csv += 'Meal Planning\n';
      csv += convertObjectToCSV(data.meal_planning, 'Meal Planning');
      csv += '\n';
    }
  }
  
  if (data.session_data && data.export_info?.role === 'guest') {
    csv += 'Session Data\n';
    csv += convertObjectToCSV(data.session_data, 'Session');
    csv += '\n';
  }
  
  return csv;
};

// Helper function to convert nested objects to CSV rows
const convertObjectToCSV = (obj, prefix = '') => {
  let csv = '';
  
  const flattenObject = (obj, parentKey = '') => {
    let items = [];
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        const newKey = parentKey ? `${parentKey}.${key}` : key;
        if (typeof obj[key] === 'object' && !Array.isArray(obj[key]) && obj[key] !== null) {
          items = items.concat(flattenObject(obj[key], newKey));
        } else if (Array.isArray(obj[key])) {
          items.push([newKey, JSON.stringify(obj[key])]);
        } else {
          items.push([newKey, obj[key]]);
        }
      }
    }
    return items;
  };
  
  const flatData = flattenObject(obj);
  csv += 'Field,Value\n';
  flatData.forEach(([key, value]) => {
    csv += `"${key}","${value}"\n`;
  });
  
  return csv;
};

// Generate filename based on role and date
export const generateExportFilename = (role, userId) => {
  const date = new Date().toISOString().split('T')[0];
  const timeStamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[1].split('.')[0];
  
  switch (role) {
    case 'patient':
      return `patient-data-${userId}-${date}-${timeStamp}`;
    case 'provider':
      return `provider-data-${userId}-${date}-${timeStamp}`;
    case 'family':
      return `family-data-${userId}-${date}-${timeStamp}`;
    case 'guest':
      return `guest-data-${userId}-${date}-${timeStamp}`;
    default:
      return `health-data-${userId}-${date}-${timeStamp}`;
  }
};

// Validate export data before download
export const validateExportData = (data) => {
  if (!data || typeof data !== 'object') {
    throw new Error('Invalid export data');
  }
  
  if (!data.export_info) {
    throw new Error('Export metadata missing');
  }
  
  if (!data.profile && !data.session_data) {
    throw new Error('No profile or session data found');
  }
  
  return true;
};