import React, { useState } from 'react';
import { useRole } from '../../context/RoleContext';
import { Button } from '../ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { 
  Download, FileDown, FileText, Database, Check, X, 
  AlertCircle, Loader2, Shield, Clock, Info 
} from 'lucide-react';
import { exportData, downloadExportedData, generateExportFilename, validateExportData } from '../../utils/dataExport';

const DataExport = ({ userId, className = '', showFullInterface = true }) => {
  const { currentRole, getCurrentTheme } = useRole();
  const [isExporting, setIsExporting] = useState(false);
  const [exportStatus, setExportStatus] = useState(null);
  const [exportProgress, setExportProgress] = useState(0);
  const [selectedFormat, setSelectedFormat] = useState('json');
  
  const theme = getCurrentTheme();

  const handleExport = async (format = 'json') => {
    setIsExporting(true);
    setExportStatus(null);
    setExportProgress(0);

    try {
      // Simulate progress steps
      setExportProgress(20);
      setExportStatus({ type: 'info', message: 'Collecting your data...' });
      
      await new Promise(resolve => setTimeout(resolve, 500));
      setExportProgress(50);
      setExportStatus({ type: 'info', message: 'Processing export...' });
      
      // Get the actual data
      const exportedData = await exportData(currentRole, userId, format);
      
      setExportProgress(80);
      setExportStatus({ type: 'info', message: 'Preparing download...' });
      
      // Validate and download
      validateExportData(exportedData);
      const filename = generateExportFilename(currentRole, userId);
      
      await new Promise(resolve => setTimeout(resolve, 300));
      setExportProgress(100);
      
      downloadExportedData(exportedData, filename, format);
      
      setExportStatus({ 
        type: 'success', 
        message: `Your ${currentRole} data has been exported successfully!` 
      });
      
    } catch (error) {
      setExportStatus({ 
        type: 'error', 
        message: error.message || 'Export failed. Please try again.' 
      });
    } finally {
      setIsExporting(false);
      setTimeout(() => {
        setExportStatus(null);
        setExportProgress(0);
      }, 3000);
    }
  };

  const getThemeClasses = () => {
    switch (theme.primary) {
      case 'blue':
        return {
          gradient: 'from-blue-500 to-blue-700',
          bg: 'bg-blue-50',
          border: 'border-blue-200',
          text: 'text-blue-800'
        };
      case 'emerald':
        return {
          gradient: 'from-emerald-500 to-emerald-700',
          bg: 'bg-emerald-50',
          border: 'border-emerald-200',
          text: 'text-emerald-800'
        };
      case 'amber':
        return {
          gradient: 'from-amber-500 to-amber-700',
          bg: 'bg-amber-50',
          border: 'border-amber-200',
          text: 'text-amber-800'
        };
      case 'purple':
        return {
          gradient: 'from-purple-500 to-purple-700',
          bg: 'bg-purple-50',
          border: 'border-purple-200',
          text: 'text-purple-800'
        };
      default:
        return {
          gradient: 'from-gray-500 to-gray-700',
          bg: 'bg-gray-50',
          border: 'border-gray-200',
          text: 'text-gray-800'
        };
    }
  };

  const themeClasses = getThemeClasses();

  const getExportDescription = () => {
    switch (currentRole) {
      case 'patient':
        return {
          title: 'Export Your Health Data',
          description: 'Download your complete health profile including nutrition logs, health metrics, goals, and AI insights.',
          includes: [
            'Personal profile and health history',
            'Food logs and nutrition tracking',
            'Health metrics and measurements',
            'Goals and progress tracking',
            'AI-powered insights and recommendations'
          ]
        };
      case 'provider':
        return {
          title: 'Export Practice Data',
          description: 'Download your professional profile and practice analytics for records and reporting.',
          includes: [
            'Professional credentials and practice info',
            'Patient overview and analytics',
            'Clinical insights and outcomes',
            'Professional development records',
            'Practice performance metrics'
          ]
        };
      case 'family':
        return {
          title: 'Export Family Health Data',
          description: 'Download comprehensive family health coordination data including all members and activities.',
          includes: [
            'Family structure and member profiles',
            'Meal planning and coordination',
            'Family health goals and progress',
            'Care coordination and schedules',
            'Emergency contacts and medical info'
          ]
        };
      case 'guest':
        return {
          title: 'Export Session Data',
          description: 'Download your current session data before it expires. Perfect for transitioning to a full account.',
          includes: [
            'Current session profile',
            'Food logs and nutrition entries',
            'Simple goals and progress',
            'Basic health calculations',
            'Session insights and tips'
          ]
        };
      default:
        return {
          title: 'Export Data',
          description: 'Download your data',
          includes: []
        };
    }
  };

  const exportInfo = getExportDescription();

  if (!showFullInterface) {
    // Compact version for quick actions
    return (
      <div className={className}>
        <Button
          onClick={() => handleExport('json')}
          disabled={isExporting}
          className={`bg-gradient-to-r ${themeClasses.gradient} text-white hover:opacity-90`}
          size="sm"
        >
          {isExporting ? (
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
          ) : (
            <Download className="w-4 h-4 mr-2" />
          )}
          Export Data
        </Button>
        
        {exportStatus && (
          <div className={`mt-2 p-2 rounded text-sm ${
            exportStatus.type === 'success' ? 'bg-green-100 text-green-800' :
            exportStatus.type === 'error' ? 'bg-red-100 text-red-800' :
            'bg-blue-100 text-blue-800'
          }`}>
            {exportStatus.message}
          </div>
        )}
      </div>
    );
  }

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Database className="w-5 h-5" />
          <span>{exportInfo.title}</span>
          {currentRole === 'guest' && (
            <Badge variant="outline" className="ml-2">
              <Clock className="w-3 h-3 mr-1" />
              Session Data
            </Badge>
          )}
        </CardTitle>
        <p className="text-gray-600 text-sm">{exportInfo.description}</p>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* What's Included */}
        <div className={`p-4 rounded-lg ${themeClasses.bg} ${themeClasses.border} border`}>
          <h4 className={`font-semibold ${themeClasses.text} mb-2`}>What's included in your export:</h4>
          <ul className="space-y-1">
            {exportInfo.includes.map((item, index) => (
              <li key={index} className={`text-sm ${themeClasses.text} flex items-center`}>
                <Check className="w-3 h-3 mr-2 flex-shrink-0" />
                {item}
              </li>
            ))}
          </ul>
        </div>

        {/* Format Selection */}
        <div className="space-y-3">
          <label className="text-sm font-medium text-gray-700">Export Format:</label>
          <div className="flex space-x-3">
            <Button
              variant={selectedFormat === 'json' ? 'default' : 'outline'}
              onClick={() => setSelectedFormat('json')}
              className={selectedFormat === 'json' ? `bg-gradient-to-r ${themeClasses.gradient} text-white` : ''}
            >
              <FileText className="w-4 h-4 mr-2" />
              JSON
            </Button>
            <Button
              variant={selectedFormat === 'csv' ? 'default' : 'outline'}
              onClick={() => setSelectedFormat('csv')}
              className={selectedFormat === 'csv' ? `bg-gradient-to-r ${themeClasses.gradient} text-white` : ''}
            >
              <FileDown className="w-4 h-4 mr-2" />
              CSV
            </Button>
          </div>
        </div>

        {/* Export Progress */}
        {isExporting && (
          <div className="space-y-2">
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className={`bg-gradient-to-r ${themeClasses.gradient} h-2 rounded-full transition-all duration-300`}
                style={{ width: `${exportProgress}%` }}
              />
            </div>
            <p className="text-sm text-gray-600 text-center">
              {exportProgress}% complete
            </p>
          </div>
        )}

        {/* Status Message */}
        {exportStatus && (
          <div className={`p-3 rounded-md flex items-center space-x-2 ${
            exportStatus.type === 'success' ? 'bg-green-100 text-green-800' :
            exportStatus.type === 'error' ? 'bg-red-100 text-red-800' :
            'bg-blue-100 text-blue-800'
          }`}>
            {exportStatus.type === 'success' ? <Check className="w-4 h-4" /> :
             exportStatus.type === 'error' ? <X className="w-4 h-4" /> :
             <Info className="w-4 h-4" />}
            <span className="text-sm">{exportStatus.message}</span>
          </div>
        )}

        {/* Export Button */}
        <Button
          onClick={() => handleExport(selectedFormat)}
          disabled={isExporting}
          className={`w-full bg-gradient-to-r ${themeClasses.gradient} text-white hover:opacity-90`}
        >
          {isExporting ? (
            <Loader2 className="w-5 h-5 mr-2 animate-spin" />
          ) : (
            <Download className="w-5 h-5 mr-2" />
          )}
          {isExporting ? 'Exporting...' : `Export ${selectedFormat.toUpperCase()}`}
        </Button>

        {/* Privacy Notice */}
        <div className="p-3 bg-gray-50 rounded-md border border-gray-200">
          <div className="flex items-start space-x-2">
            <Shield className="w-4 h-4 text-gray-600 mt-0.5 flex-shrink-0" />
            <div className="text-xs text-gray-600">
              <p className="font-medium mb-1">Privacy & Security</p>
              <p>Your exported data is processed securely and downloaded directly to your device. We don't store copies of your exported files on our servers.</p>
              {currentRole === 'guest' && (
                <p className="mt-1 text-amber-700">
                  <strong>Note:</strong> Guest session data will be permanently deleted after 24 hours.
                </p>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default DataExport;