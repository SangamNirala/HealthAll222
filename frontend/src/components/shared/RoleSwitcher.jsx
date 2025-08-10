import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useRole } from '../../context/RoleContext';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  X, User, Stethoscope, Users, UserCheck, ArrowRight, 
  Check, Clock, Star, Shield
} from 'lucide-react';

const RoleSwitcher = ({ isOpen, onClose }) => {
  const navigate = useNavigate();
  const { currentRole, roleHistory, switchRole, getAvailableRoles, getRoleConfig } = useRole();
  const [selectedRole, setSelectedRole] = useState(currentRole);

  if (!isOpen) return null;

  const roleIcons = {
    patient: User,
    provider: Stethoscope, 
    family: Users,
    guest: UserCheck
  };

  const roleDescriptions = {
    patient: {
      title: 'Personal Health Tracking',
      description: 'Track your nutrition, monitor health metrics, get AI-powered meal recommendations',
      benefits: ['Food logging with AI', 'Health metrics tracking', 'Personalized meal plans']
    },
    provider: {
      title: 'Professional Healthcare Portal',
      description: 'Monitor patients, create diet prescriptions, access clinical decision support',
      benefits: ['Patient management', 'Clinical analytics', 'Evidence-based tools']
    },
    family: {
      title: 'Family Health Management',
      description: 'Manage family member\'s health, coordinate care, track multiple profiles',
      benefits: ['Multiple profile management', 'Family meal planning', 'Care coordination']
    },
    guest: {
      title: 'Quick Health Tracking',
      description: 'Basic nutrition tracking and health monitoring without account creation',
      benefits: ['Simple food logging', 'Basic nutrition info', 'No account needed']
    }
  };

  const handleRoleSwitch = () => {
    if (selectedRole !== currentRole) {
      switchRole(selectedRole);
      
      // Navigate to the selected role's dashboard
      const dashboardRoutes = {
        patient: '/patient-dashboard',
        provider: '/provider-dashboard',
        family: '/family-dashboard',
        guest: '/guest-dashboard'
      };
      
      navigate(dashboardRoutes[selectedRole]);
    }
    onClose();
  };

  const RoleCard = ({ role }) => {
    const IconComponent = roleIcons[role];
    const config = getRoleConfig(role);
    const description = roleDescriptions[role];
    const isSelected = selectedRole === role;
    const isCurrent = currentRole === role;
    const wasUsedBefore = roleHistory.includes(role);

    return (
      <Card 
        className={`cursor-pointer transition-all duration-200 hover:shadow-md ${
          isSelected 
            ? `ring-2 ring-${config.theme.primary}-500 bg-${config.theme.primary}-50` 
            : 'hover:bg-gray-50'
        }`}
        onClick={() => setSelectedRole(role)}
      >
        <CardContent className="p-6">
          <div className="flex items-start space-x-4">
            {/* Role Icon */}
            <div className={`rounded-full p-3 bg-gradient-to-r ${config.theme.gradient} flex-shrink-0`}>
              <IconComponent className="w-6 h-6 text-white" />
            </div>
            
            {/* Role Info */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-2 mb-2">
                <h3 className="text-lg font-semibold text-gray-900">
                  {description.title}
                </h3>
                
                {/* Status Badges */}
                <div className="flex items-center space-x-1">
                  {isCurrent && (
                    <Badge variant="secondary" className="text-xs bg-green-100 text-green-800">
                      <Check className="w-3 h-3 mr-1" />
                      Current
                    </Badge>
                  )}
                  
                  {wasUsedBefore && !isCurrent && (
                    <Badge variant="outline" className="text-xs">
                      <Clock className="w-3 h-3 mr-1" />
                      Recent
                    </Badge>
                  )}
                  
                  {role === 'provider' && (
                    <Badge variant="outline" className="text-xs">
                      <Shield className="w-3 h-3 mr-1" />
                      Professional
                    </Badge>
                  )}
                  
                  {role === 'guest' && (
                    <Badge variant="outline" className="text-xs">
                      <Star className="w-3 h-3 mr-1" />
                      No Signup
                    </Badge>
                  )}
                </div>
              </div>
              
              <p className="text-gray-600 text-sm mb-3 leading-relaxed">
                {description.description}
              </p>
              
              {/* Benefits List */}
              <div className="space-y-1">
                {description.benefits.map((benefit, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <div className={`w-1.5 h-1.5 rounded-full bg-gradient-to-r ${config.theme.gradient}`} />
                    <span className="text-xs text-gray-700">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
            
            {/* Selection Indicator */}
            {isSelected && (
              <div className={`rounded-full p-1 bg-${config.theme.primary}-500`}>
                <Check className="w-4 h-4 text-white" />
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Switch Role</h2>
            <p className="text-gray-600 mt-1">Choose how you want to use the platform</p>
          </div>
          <Button variant="ghost" onClick={onClose} className="hover:bg-gray-100">
            <X className="w-5 h-5" />
          </Button>
        </div>
        
        {/* Role Selection Grid */}
        <div className="p-6 overflow-y-auto max-h-[60vh]">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {getAvailableRoles().map((role) => (
              <RoleCard key={role} role={role} />
            ))}
          </div>
        </div>
        
        {/* Footer */}
        <div className="flex items-center justify-between p-6 border-t bg-gray-50">
          <div className="text-sm text-gray-600">
            {selectedRole !== currentRole ? (
              <span>Switching to <strong>{getRoleConfig(selectedRole).name}</strong> mode</span>
            ) : (
              <span>Currently in <strong>{getRoleConfig(selectedRole).name}</strong> mode</span>
            )}
          </div>
          
          <div className="flex items-center space-x-3">
            <Button variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button 
              onClick={handleRoleSwitch}
              disabled={selectedRole === currentRole}
              className={`bg-gradient-to-r ${getRoleConfig(selectedRole).theme.gradient} text-white hover:opacity-90 disabled:opacity-50`}
            >
              {selectedRole === currentRole ? 'Current Role' : (
                <>
                  Switch Role
                  <ArrowRight className="w-4 h-4 ml-2" />
                </>
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RoleSwitcher;