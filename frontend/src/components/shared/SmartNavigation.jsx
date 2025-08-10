import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useRole } from '../../context/RoleContext';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import RoleSwitcher from './RoleSwitcher';
import DataExport from './DataExport';
import { 
  ArrowLeft, LayoutDashboard, User, Users, Apple, Activity, Target, 
  Stethoscope, BarChart3, BookOpen, FileText, UserPlus, ChefHat, 
  Calendar, Shield, Settings, Plus, Camera, Menu, X, Home, ChevronDown,
  Pill, Timeline, Download
} from 'lucide-react';


// Icon mapping for dynamic icon rendering
const ICON_MAP = {
  LayoutDashboard, User, Users, Apple, Activity, Target, Stethoscope, 
  BarChart3, BookOpen, FileText, UserPlus, ChefHat, Calendar, Shield, 
  Settings, Plus, Camera, Home, Pill, Download
};

const SmartNavigation = ({ breadcrumbs = null, showRoleSwitcher = true }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { currentRole, getRoleConfig, getCurrentTheme } = useRole();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isRoleSwitcherOpen, setIsRoleSwitcherOpen] = useState(false);
  const [isMoreMenuOpen, setIsMoreMenuOpen] = useState(false);
  const [showExportModal, setShowExportModal] = useState(false);
  const moreMenuRef = useRef(null);
  
  const roleConfig = getRoleConfig();
  const theme = getCurrentTheme();

  // Close more menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (moreMenuRef.current && !moreMenuRef.current.contains(event.target)) {
        setIsMoreMenuOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Check if current path matches navigation item
  const isActivePath = (path) => {
    return location.pathname === path;
  };

  // Handle navigation item click
  const handleNavigation = (path) => {
    navigate(path);
    setIsMobileMenuOpen(false);
  };

  // Handle quick action click
  const handleQuickAction = (action) => {
    switch (action) {
      case 'quickLog':
        console.log('Quick log action triggered');
        break;
      case 'newPatient':
        console.log('New patient action triggered');
        break;
      case 'prescriptions':
        console.log('Prescriptions action triggered');
        break;
      case 'addMember':
        console.log('Add member action triggered');
        break;
      case 'planMeals':
        console.log('Plan meals action triggered');
        break;
      case 'logFood':
        console.log('Log food action triggered');
        break;
      case 'setGoal':
        console.log('Set goal action triggered');
        break;
      default:
        console.log(`Unhandled action: ${action}`);
    }
  };

  const NavigationItem = ({ item, isMobile = false }) => {
    const IconComponent = ICON_MAP[item.icon];
    const isActive = isActivePath(item.path);
    
    const getActiveClasses = () => {
      switch (theme.primary) {
        case 'blue':
          return isActive 
            ? 'bg-blue-100 text-blue-900 hover:bg-blue-200' 
            : 'hover:bg-blue-50 text-gray-700 hover:text-gray-900';
        case 'emerald':
          return isActive 
            ? 'bg-emerald-100 text-emerald-900 hover:bg-emerald-200' 
            : 'hover:bg-emerald-50 text-gray-700 hover:text-gray-900';
        case 'amber':
          return isActive 
            ? 'bg-amber-100 text-amber-900 hover:bg-amber-200' 
            : 'hover:bg-amber-50 text-gray-700 hover:text-gray-900';
        case 'purple':
          return isActive 
            ? 'bg-purple-100 text-purple-900 hover:bg-purple-200' 
            : 'hover:bg-purple-50 text-gray-700 hover:text-gray-900';
        default:
          return isActive 
            ? 'bg-gray-100 text-gray-900 hover:bg-gray-200' 
            : 'hover:bg-gray-50 text-gray-700 hover:text-gray-900';
      }
    };
    
    return (
      <Button
        variant={isActive ? "default" : "ghost"}
        onClick={() => handleNavigation(item.path)}
        className={`${isMobile ? 'w-full justify-start' : ''} ${getActiveClasses()}`}
      >
        {IconComponent && <IconComponent className="w-4 h-4 mr-2" />}
        {item.label}
      </Button>
    );
  };

  const QuickActionButton = ({ action, isMobile = false }) => {
    const IconComponent = ICON_MAP[action.icon];
    
    const getGradientClass = () => {
      switch (theme.primary) {
        case 'blue':
          return 'bg-gradient-to-r from-blue-500 to-blue-700';
        case 'emerald':
          return 'bg-gradient-to-r from-emerald-500 to-emerald-700';
        case 'amber':
          return 'bg-gradient-to-r from-amber-500 to-amber-700';
        case 'purple':
          return 'bg-gradient-to-r from-purple-500 to-purple-700';
        default:
          return 'bg-gradient-to-r from-gray-500 to-gray-700';
      }
    };
    
    return (
      <Button
        size="sm"
        onClick={() => handleQuickAction(action.action)}
        className={`${isMobile ? 'w-full justify-start' : ''} ${getGradientClass()} text-white hover:opacity-90`}
      >
        {IconComponent && <IconComponent className="w-4 h-4 mr-2" />}
        {action.label}
      </Button>
    );
  };

  const getThemeClasses = () => {
    switch (theme.primary) {
      case 'blue':
        return {
          gradient: 'from-blue-500 to-blue-700',
          hover: 'hover:bg-blue-50'
        };
      case 'emerald':
        return {
          gradient: 'from-emerald-500 to-emerald-700',
          hover: 'hover:bg-emerald-50'
        };
      case 'amber':
        return {
          gradient: 'from-amber-500 to-amber-700',
          hover: 'hover:bg-amber-50'
        };
      case 'purple':
        return {
          gradient: 'from-purple-500 to-purple-700',
          hover: 'hover:bg-purple-50'
        };
      default:
        return {
          gradient: 'from-gray-500 to-gray-700',
          hover: 'hover:bg-gray-50'
        };
    }
  };

  const themeClasses = getThemeClasses();

  return (
    <nav className="bg-white shadow-sm border-b sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Left Section - Logo and Navigation */}
          <div className="flex items-center space-x-4">
            {/* Back to Home Button */}
            <Button
              variant="ghost"
              onClick={() => navigate('/')}
              className={themeClasses.hover}
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              <span className="hidden sm:inline">Home</span>
            </Button>
            
            <div className="h-6 w-px bg-gray-300" />
            
            {/* Role Title */}
            <div className="flex items-center space-x-3">
              <div className={`bg-gradient-to-r ${themeClasses.gradient} rounded-xl p-2`}>
                <Home className="w-6 h-6 text-white" />
              </div>
              <h1 className="text-xl font-bold text-gray-900 hidden md:block">
                {roleConfig.title}
              </h1>
            </div>

            {/* Desktop Navigation Items */}
            <div className="hidden lg:flex items-center space-x-1 ml-8">
              {roleConfig.navigationItems.slice(0, 4).map((item) => (
                <NavigationItem key={item.path} item={item} />
              ))}
              
              {/* More menu for additional items */}
              {roleConfig.navigationItems.length > 4 && (
                <div className="relative" ref={moreMenuRef}>
                  <Button 
                    variant="ghost" 
                    className={themeClasses.hover}
                    onClick={() => setIsMoreMenuOpen(!isMoreMenuOpen)}
                  >
                    More
                    <ChevronDown className="w-4 h-4 ml-1" />
                  </Button>
                  
                  {/* More dropdown menu */}
                  {isMoreMenuOpen && (
                    <div className="absolute top-full left-0 mt-2 w-48 bg-white border border-gray-200 rounded-md shadow-lg z-50">
                      <div className="py-2">
                        {roleConfig.navigationItems.slice(4).map((item) => (
                          <button
                            key={item.path}
                            onClick={() => {
                              handleNavigation(item.path);
                              setIsMoreMenuOpen(false);
                            }}
                            className="w-full text-left px-4 py-2 hover:bg-gray-50 text-gray-700 hover:text-gray-900 flex items-center"
                          >
                            {ICON_MAP[item.icon] && React.createElement(ICON_MAP[item.icon], { className: "w-4 h-4 mr-2" })}
                            {item.label}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Right Section - Role Switcher and Actions */}
          <div className="flex items-center space-x-4">
            {/* Role Badge and Switcher */}
            {showRoleSwitcher && (
              <div className="flex items-center space-x-2">
                <Badge 
                  variant="secondary" 
                  className={`bg-${theme.primary}-100 text-${theme.primary}-800 cursor-pointer hover:bg-${theme.primary}-200`}
                  onClick={() => setIsRoleSwitcherOpen(true)}
                >
                  {roleConfig.name} Mode
                  <ChevronDown className="w-3 h-3 ml-1" />
                </Badge>
              </div>
            )}

            {/* Quick Actions */}
            <div className="hidden md:flex items-center space-x-2">
              {roleConfig.quickActions.slice(0, 2).map((action, index) => (
                <QuickActionButton key={index} action={action} />
              ))}
            </div>

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              className="lg:hidden"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            >
              {isMobileMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </Button>
          </div>
        </div>

        {/* Breadcrumbs */}
        {breadcrumbs && (
          <div className="pb-4 pt-2">
            {breadcrumbs}
          </div>
        )}
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="lg:hidden border-t bg-white">
          <div className="px-4 py-6 space-y-4">
            {/* Navigation Items */}
            <div className="space-y-2">
              <h3 className="text-sm font-semibold text-gray-900 mb-3">Navigation</h3>
              {roleConfig.navigationItems.map((item) => (
                <NavigationItem key={item.path} item={item} isMobile />
              ))}
            </div>
            
            {/* Quick Actions */}
            <div className="space-y-2 pt-4 border-t">
              <h3 className="text-sm font-semibold text-gray-900 mb-3">Quick Actions</h3>
              {roleConfig.quickActions.map((action, index) => (
                <QuickActionButton key={index} action={action} isMobile />
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Role Switcher Modal */}
      {showRoleSwitcher && (
        <RoleSwitcher 
          isOpen={isRoleSwitcherOpen}
          onClose={() => setIsRoleSwitcherOpen(false)}
        />
      )}
    </nav>
  );
};

export default SmartNavigation;