import React, { createContext, useContext, useState, useEffect } from 'react';

const RoleContext = createContext();

export const useRole = () => {
  const context = useContext(RoleContext);
  if (!context) {
    throw new Error('useRole must be used within a RoleProvider');
  }
  return context;
};

// Role configuration with themes and navigation options
const ROLE_CONFIG = {
  patient: {
    name: 'Patient',
    title: 'Personal Health Dashboard',
    theme: {
      primary: 'blue',
      gradient: 'from-blue-500 to-blue-700',
      bgGradient: 'from-blue-50 to-indigo-100',
      hoverBg: 'hover:bg-blue-50'
    },
    navigationItems: [
      { label: 'Dashboard', path: '/patient-dashboard', icon: 'LayoutDashboard' },
      { label: 'Profile', path: '/patient-profile', icon: 'User' },
      { label: 'Food Log', path: '/patient-food-log', icon: 'Apple' },
      { label: 'Health Metrics', path: '/patient-metrics', icon: 'Activity' },
      { label: 'Goals', path: '/patient-goals', icon: 'Target' },
      { label: 'Analytics', path: '/patient-analytics', icon: 'BarChart3' },
      { label: 'Medications', path: '/patient-medications', icon: 'Pill' },
      { label: 'Health Timeline', path: '/patient-timeline', icon: 'Calendar' }
    ],
    quickActions: [
      { label: 'Quick Log', icon: 'Plus', action: 'quickLog' }
    ]
  },
  provider: {
    name: 'Provider',
    title: 'Healthcare Provider Portal',
    theme: {
      primary: 'emerald',
      gradient: 'from-emerald-500 to-emerald-700',
      bgGradient: 'from-emerald-50 to-teal-100',
      hoverBg: 'hover:bg-emerald-50'
    },
    navigationItems: [
      { label: 'Dashboard', path: '/provider-dashboard', icon: 'LayoutDashboard' },
      { label: 'Profile', path: '/provider-profile', icon: 'User' },
      { label: 'Patients', path: '/provider-patients', icon: 'Users' },
      { label: 'Clinical Tools', path: '/provider-tools', icon: 'Stethoscope' },
      { label: 'Analytics', path: '/provider-analytics', icon: 'BarChart3' },
      { label: 'Education', path: '/provider-education', icon: 'BookOpen' }
    ],
    quickActions: [
      { label: 'New Patient', icon: 'UserPlus', action: 'newPatient' },
      { label: 'Prescriptions', icon: 'FileText', action: 'prescriptions' }
    ]
  },
  family: {
    name: 'Family',
    title: 'Family Health Management',
    theme: {
      primary: 'amber',
      gradient: 'from-amber-500 to-amber-700',
      bgGradient: 'from-amber-50 to-orange-100',
      hoverBg: 'hover:bg-amber-50'
    },
    navigationItems: [
      { label: 'Dashboard', path: '/family-dashboard', icon: 'LayoutDashboard' },
      { label: 'Profile', path: '/family-profile', icon: 'Users' },
      { label: 'Family Members', path: '/family-members', icon: 'User' },
      { label: 'Meal Planning', path: '/family-meals', icon: 'ChefHat' },
      { label: 'Calendar', path: '/family-calendar', icon: 'Calendar' },
      { label: 'Coordination', path: '/family-coordination', icon: 'Shield' },
      { label: 'Child Education', path: '/child-nutrition-education', icon: 'BookOpen' },
      { label: 'Caregiver Tools', path: '/caregiver-tools', icon: 'Heart' },
      { label: 'Family Goals', path: '/family-goals', icon: 'Target' },
      { label: 'Multi-Profiles', path: '/multi-profile-management', icon: 'Settings' }
    ],
    quickActions: [
      { label: 'Add Member', icon: 'UserPlus', action: 'addMember' },
      { label: 'Plan Meals', icon: 'ChefHat', action: 'planMeals' },
      { label: 'Emergency Info', icon: 'AlertTriangle', action: 'emergencyInfo' },
      { label: 'Health Check', icon: 'Activity', action: 'healthCheck' }
    ]
  },
  guest: {
    name: 'Guest',
    title: 'Quick Health Tracking',
    theme: {
      primary: 'purple',
      gradient: 'from-purple-500 to-purple-700',
      bgGradient: 'from-purple-50 to-violet-100',
      hoverBg: 'hover:bg-purple-50'
    },
    navigationItems: [
      { label: 'Dashboard', path: '/guest-dashboard', icon: 'LayoutDashboard' },
      { label: 'Quick Setup', path: '/guest-setup', icon: 'Settings' },
      { label: 'Food Log', path: '/guest-food-log', icon: 'Apple' },
      { label: 'Goals', path: '/guest-goals', icon: 'Target' },
      { label: 'Health Calculator', path: '/guest-calculator', icon: 'Calculator' },
      { label: 'Nutrition Tips', path: '/guest-tips', icon: 'BookOpen' }
    ],
    quickActions: [
      { label: 'Log Food', icon: 'Plus', action: 'logFood' },
      { label: 'Set Goal', icon: 'Target', action: 'setGoal' }
    ]
  }
};

export const RoleProvider = ({ children }) => {
  const [currentRole, setCurrentRole] = useState(() => {
    // Initialize from localStorage or default to 'patient'
    return localStorage.getItem('currentRole') || 'patient';
  });

  const [roleHistory, setRoleHistory] = useState(() => {
    // Keep track of previously used roles
    const history = localStorage.getItem('roleHistory');
    return history ? JSON.parse(history) : ['patient'];
  });

  // Update localStorage when role changes
  useEffect(() => {
    localStorage.setItem('currentRole', currentRole);
    
    // Update role history
    if (!roleHistory.includes(currentRole)) {
      const newHistory = [...roleHistory, currentRole];
      setRoleHistory(newHistory);
      localStorage.setItem('roleHistory', JSON.stringify(newHistory));
    }
  }, [currentRole, roleHistory]);

  const switchRole = (newRole) => {
    if (ROLE_CONFIG[newRole]) {
      setCurrentRole(newRole);
    }
  };

  const getRoleConfig = (role = currentRole) => {
    return ROLE_CONFIG[role] || ROLE_CONFIG.patient;
  };

  const getCurrentTheme = () => {
    return getRoleConfig().theme;
  };

  const getAvailableRoles = () => {
    return Object.keys(ROLE_CONFIG);
  };

  const value = {
    currentRole,
    roleHistory,
    switchRole,
    getRoleConfig,
    getCurrentTheme,
    getAvailableRoles,
    roleConfig: ROLE_CONFIG
  };

  return (
    <RoleContext.Provider value={value}>
      {children}
    </RoleContext.Provider>
  );
};

export default RoleContext;