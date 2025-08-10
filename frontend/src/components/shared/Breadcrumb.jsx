import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useRole } from '../../context/RoleContext';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { ChevronRight, Home, Check, Clock, AlertCircle } from 'lucide-react';

const Breadcrumb = ({ items = [], currentStep = 0, showProgress = true }) => {
  const navigate = useNavigate();
  const { getCurrentTheme } = useRole();
  const theme = getCurrentTheme();

  // Default breadcrumb item structure:
  // {
  //   label: 'Step Name',
  //   path: '/path/to/step', // optional, for navigation
  //   status: 'completed' | 'current' | 'pending' | 'error', // optional
  //   description: 'Step description', // optional
  //   onClick: () => {} // optional custom handler
  // }

  const handleItemClick = (item, index) => {
    if (item.onClick) {
      item.onClick();
    } else if (item.path) {
      navigate(item.path);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <Check className="w-4 h-4 text-green-600" />;
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-600" />;
      case 'current':
        return <Clock className="w-4 h-4 text-blue-600" />;
      default:
        return null;
    }
  };

  const getStatusColor = (status, index) => {
    switch (status) {
      case 'completed':
        return 'text-green-700 bg-green-50 hover:bg-green-100';
      case 'error':
        return 'text-red-700 bg-red-50 hover:bg-red-100';
      case 'current':
        return `text-${theme.primary}-700 bg-${theme.primary}-50 hover:bg-${theme.primary}-100`;
      case 'pending':
        return 'text-gray-500 bg-gray-50 hover:bg-gray-100';
      default:
        // Fallback to index-based status
        if (index < currentStep) return 'text-green-700 bg-green-50 hover:bg-green-100';
        if (index === currentStep) return `text-${theme.primary}-700 bg-${theme.primary}-50 hover:bg-${theme.primary}-100`;
        return 'text-gray-500 bg-gray-50 hover:bg-gray-100';
    }
  };

  const isClickable = (item, index) => {
    // Allow clicking if there's a path, onClick handler, or if it's a completed step
    return item.path || item.onClick || item.status === 'completed' || index < currentStep;
  };

  if (items.length === 0) return null;

  return (
    <nav className="flex flex-col space-y-4" aria-label="Breadcrumb">
      {/* Progress Bar */}
      {showProgress && (
        <div className="w-full">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">
              Progress: Step {currentStep + 1} of {items.length}
            </span>
            <Badge variant="outline" className={`text-${theme.primary}-800 border-${theme.primary}-200`}>
              {Math.round(((currentStep + 1) / items.length) * 100)}% Complete
            </Badge>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className={`bg-gradient-to-r ${theme.gradient} h-2 rounded-full transition-all duration-300`}
              style={{ width: `${((currentStep + 1) / items.length) * 100}%` }}
            />
          </div>
        </div>
      )}

      {/* Breadcrumb Navigation */}
      <div className="flex items-center space-x-2 flex-wrap">
        {/* Home Link */}
        <Button
          variant="ghost"
          size="sm"
          onClick={() => navigate('/')}
          className="text-gray-600 hover:text-gray-900 hover:bg-gray-100"
        >
          <Home className="w-4 h-4" />
          <span className="sr-only">Home</span>
        </Button>

        <ChevronRight className="w-4 h-4 text-gray-400" />

        {/* Breadcrumb Items */}
        {items.map((item, index) => {
          const clickable = isClickable(item, index);
          const statusColor = getStatusColor(item.status, index);
          const statusIcon = getStatusIcon(item.status);
          
          return (
            <React.Fragment key={index}>
              {clickable ? (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleItemClick(item, index)}
                  className={`${statusColor} font-medium transition-colors duration-200`}
                  title={item.description}
                >
                  <div className="flex items-center space-x-2">
                    {statusIcon}
                    <span>{item.label}</span>
                  </div>
                </Button>
              ) : (
                <span 
                  className={`px-3 py-1 rounded-md text-sm ${statusColor} font-medium`}
                  title={item.description}
                >
                  <div className="flex items-center space-x-2">
                    {statusIcon}
                    <span>{item.label}</span>
                  </div>
                </span>
              )}

              {/* Separator */}
              {index < items.length - 1 && (
                <ChevronRight className="w-4 h-4 text-gray-400" />
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Current Step Details */}
      {/* REMOVED: Current step details box per user request */}
    </nav>
  );
};

export default Breadcrumb;