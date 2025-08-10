import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useRole } from '../../context/RoleContext';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import RoleSwitcher from './RoleSwitcher';
import { 
  ArrowLeft, LayoutDashboard, User, Users, Apple, Activity, Target, 
  Stethoscope, BarChart3, BookOpen, FileText, UserPlus, ChefHat, 
  Calendar, Shield, Settings, Plus, Camera, Menu, X, Home, ChevronDown
} from 'lucide-react';

// Icon mapping for dynamic icon rendering
const ICON_MAP = {
  LayoutDashboard, User, Users, Apple, Activity, Target, Stethoscope, 
  BarChart3, BookOpen, FileText, UserPlus, ChefHat, Calendar, Shield, 
  Settings, Plus, Camera, Home
};

const SmartNavigation = ({ breadcrumbs = null, showRoleSwitcher = true }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { currentRole, getRoleConfig, getCurrentTheme } = useRole();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isRoleSwitcherOpen, setIsRoleSwitcherOpen] = useState(false);
  
  const roleConfig = getRoleConfig();
  const theme = getCurrentTheme();

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
        // Handle quick food log action
        console.log('Quick log action triggered');
        break;
      case 'photoLog':
        // Handle photo log action
        console.log('Photo log action triggered');
        break;
      case 'newPatient':
        // Handle new patient action
        console.log('New patient action triggered');
        break;
      case 'prescriptions':
        // Handle prescriptions action
        console.log('Prescriptions action triggered');
        break;
      case 'addMember':
        // Handle add family member action
        console.log('Add member action triggered');
        break;
      case 'planMeals':
        // Handle meal planning action
        console.log('Plan meals action triggered');
        break;
      case 'logFood':
        // Handle guest food log action
        console.log('Log food action triggered');
        break;
      case 'setGoal':
        // Handle set goal action
        console.log('Set goal action triggered');
        break;
      default:
        console.log(`Unhandled action: ${action}`);
    }
  };

  const NavigationItem = ({ item, isMobile = false }) => {
    const IconComponent = ICON_MAP[item.icon];
    const isActive = isActivePath(item.path);
    
    return (
      <Button
        variant={isActive ? "default" : "ghost"}
        onClick={() => handleNavigation(item.path)}
        className={`${isMobile ? 'w-full justify-start' : ''} ${
          isActive 
            ? `bg-${theme.primary}-100 text-${theme.primary}-900 hover:bg-${theme.primary}-200` 
            : `${theme.hoverBg} text-gray-700 hover:text-gray-900`
        }`}
      >
        {IconComponent && <IconComponent className="w-4 h-4 mr-2" />}
        {item.label}
      </Button>
    );
  };

  const QuickActionButton = ({ action, isMobile = false }) => {
    const IconComponent = ICON_MAP[action.icon];
    
    return (
      <Button
        size="sm"
        onClick={() => handleQuickAction(action.action)}
        className={`${isMobile ? 'w-full justify-start' : ''} bg-gradient-to-r ${theme.gradient} text-white hover:opacity-90`}
      >
        {IconComponent && <IconComponent className="w-4 h-4 mr-2" />}
        {action.label}
      </Button>
    );
  };

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
              className={theme.hoverBg}
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              <span className="hidden sm:inline">Home</span>
            </Button>
            
            <div className="h-6 w-px bg-gray-300" />
            
            {/* Role Title */}
            <div className="flex items-center space-x-3">
              <div className={`bg-gradient-to-r ${theme.gradient} rounded-xl p-2`}>
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
                <div className="relative">
                  <Button variant="ghost" className={theme.hoverBg}>
                    More
                    <ChevronDown className="w-4 h-4 ml-1" />
                  </Button>
                  {/* Dropdown menu would go here */}
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