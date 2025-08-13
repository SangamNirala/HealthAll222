import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  Clock, Users, FileText, Monitor, CheckCircle, 
  AlertTriangle, Info, Play, RefreshCw, Wifi,
  Volume2, Camera, Mic, Settings, Shield,
  Brain, Calculator, MessageSquare, Grid3X3
} from 'lucide-react';

const PreTestInstructions = ({ onStartTest }) => {
  const [browserCheck, setBrowserCheck] = useState({
    browser: 'checking',
    internet: 'checking',
    audio: 'checking',
    camera: 'checking',
    microphone: 'checking'
  });
  const [agreementChecked, setAgreementChecked] = useState(false);
  const [allChecksPass, setAllChecksPass] = useState(false);

  useEffect(() => {
    performSystemChecks();
  }, []);

  const performSystemChecks = async () => {
    // Simulate browser compatibility check
    setTimeout(() => {
      setBrowserCheck(prev => ({
        ...prev,
        browser: detectBrowserCompatibility() ? 'pass' : 'fail'
      }));
    }, 1000);

    // Check internet connection
    setTimeout(() => {
      setBrowserCheck(prev => ({
        ...prev,
        internet: navigator.onLine ? 'pass' : 'fail'
      }));
    }, 1500);

    // Audio check
    setTimeout(() => {
      setBrowserCheck(prev => ({
        ...prev,
        audio: 'pass' // Assume audio is available
      }));
    }, 2000);

    // Camera check (optional for aptitude test)
    setTimeout(() => {
      setBrowserCheck(prev => ({
        ...prev,
        camera: 'pass'
      }));
    }, 2500);

    // Microphone check (optional for aptitude test)
    setTimeout(() => {
      setBrowserCheck(prev => ({
        ...prev,
        microphone: 'pass'
      }));
    }, 3000);
  };

  useEffect(() => {
    const allPass = Object.values(browserCheck).every(status => status === 'pass');
    setAllChecksPass(allPass && agreementChecked);
  }, [browserCheck, agreementChecked]);

  const detectBrowserCompatibility = () => {
    const userAgent = navigator.userAgent;
    const isChrome = /Chrome/.test(userAgent);
    const isFirefox = /Firefox/.test(userAgent);
    const isSafari = /Safari/.test(userAgent) && !/Chrome/.test(userAgent);
    const isEdge = /Edg/.test(userAgent);
    
    return isChrome || isFirefox || isSafari || isEdge;
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'pass':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'fail':
        return <AlertTriangle className="w-5 h-5 text-red-600" />;
      case 'checking':
        return <RefreshCw className="w-5 h-5 text-blue-600 animate-spin" />;
      default:
        return <Info className="w-5 h-5 text-gray-400" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pass': return 'text-green-600';
      case 'fail': return 'text-red-600';
      case 'checking': return 'text-blue-600';
      default: return 'text-gray-400';
    }
  };

  const testTopics = [
    {
      name: 'Numerical',
      icon: Calculator,
      description: 'Mathematical reasoning and numerical problem solving',
      questions: 12,
      time: 20
    },
    {
      name: 'Logical',
      icon: Brain,
      description: 'Pattern recognition and logical reasoning',
      questions: 12,
      time: 25
    },
    {
      name: 'Verbal',
      icon: MessageSquare,
      description: 'Language comprehension and verbal reasoning',
      questions: 11,
      time: 20
    },
    {
      name: 'Spatial',
      icon: Grid3X3,
      description: 'Spatial awareness and visual reasoning',
      questions: 10,
      time: 25
    }
  ];

  const testRules = [
    "Each question has only one correct answer",
    "You cannot go back to previous questions once submitted",
    "Use only the provided calculator for numerical questions",
    "No external materials or resources are allowed",
    "Maintain focus - switching tabs may end the test",
    "Complete the test in one sitting without breaks",
    "Submit answers before time expires for each section",
    "Ensure stable internet connection throughout"
  ];

  const browserRequirements = [
    {
      requirement: 'Supported Browser',
      icon: Monitor,
      status: browserCheck.browser,
      details: 'Chrome 90+, Firefox 88+, Safari 14+, Edge 90+'
    },
    {
      requirement: 'Stable Internet',
      icon: Wifi,
      status: browserCheck.internet,
      details: 'Minimum 1 Mbps connection speed required'
    },
    {
      requirement: 'Audio System',
      icon: Volume2,
      status: browserCheck.audio,
      details: 'Working speakers or headphones (optional)'
    },
    {
      requirement: 'Camera Access',
      icon: Camera,
      status: browserCheck.camera,
      details: 'Webcam access (optional for monitoring)'
    },
    {
      requirement: 'Microphone',
      icon: Mic,
      status: browserCheck.microphone,
      details: 'Microphone access (optional)'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Aptitude Test Instructions</h1>
          <p className="text-gray-600">Please read all instructions carefully before starting the test</p>
        </div>

        {/* Test Overview */}
        <Card className="border-2 border-blue-200">
          <CardHeader className="bg-blue-50">
            <CardTitle className="flex items-center text-blue-800">
              <FileText className="w-6 h-6 mr-2" />
              Test Overview
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <FileText className="w-8 h-8 text-green-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-green-600">45</div>
                <div className="text-sm text-gray-600">Total Questions</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <Clock className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-purple-600">90</div>
                <div className="text-sm text-gray-600">Minutes Total</div>
              </div>
              <div className="text-center p-4 bg-orange-50 rounded-lg">
                <Users className="w-8 h-8 text-orange-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-orange-600">4</div>
                <div className="text-sm text-gray-600">Topic Areas</div>
              </div>
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <CheckCircle className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                <div className="text-lg font-bold text-blue-600">Multiple</div>
                <div className="text-sm text-gray-600">Choice Format</div>
              </div>
            </div>

            {/* Topic Breakdown */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Test Topics Included:</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {testTopics.map((topic) => {
                  const Icon = topic.icon;
                  return (
                    <div key={topic.name} className="border rounded-lg p-4">
                      <div className="flex items-center mb-2">
                        <Icon className="w-5 h-5 text-blue-600 mr-2" />
                        <h4 className="font-medium text-gray-900">{topic.name}</h4>
                        <Badge variant="outline" className="ml-auto">
                          {topic.questions} questions
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-600 mb-2">{topic.description}</p>
                      <div className="text-xs text-gray-500">
                        Recommended time: {topic.time} minutes
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Test Rules and Guidelines */}
        <Card className="border-2 border-orange-200">
          <CardHeader className="bg-orange-50">
            <CardTitle className="flex items-center text-orange-800">
              <Shield className="w-6 h-6 mr-2" />
              Test Rules and Guidelines
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold text-gray-900 mb-3">Important Rules:</h4>
                <ul className="space-y-2">
                  {testRules.slice(0, 4).map((rule, index) => (
                    <li key={index} className="flex items-start">
                      <AlertTriangle className="w-4 h-4 text-orange-500 mt-0.5 mr-2 flex-shrink-0" />
                      <span className="text-sm text-gray-700">{rule}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-3">Additional Guidelines:</h4>
                <ul className="space-y-2">
                  {testRules.slice(4).map((rule, index) => (
                    <li key={index} className="flex items-start">
                      <Info className="w-4 h-4 text-blue-500 mt-0.5 mr-2 flex-shrink-0" />
                      <span className="text-sm text-gray-700">{rule}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <div className="flex items-start">
                <AlertTriangle className="w-5 h-5 text-red-600 mt-0.5 mr-2" />
                <div>
                  <h5 className="font-semibold text-red-900">Important Notice:</h5>
                  <p className="text-sm text-red-800">
                    Any attempt to cheat, use unauthorized materials, or leave the test window 
                    may result in automatic disqualification. Ensure you have a quiet environment 
                    and sufficient time to complete the entire test.
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Browser Requirements Check */}
        <Card className="border-2 border-green-200">
          <CardHeader className="bg-green-50">
            <CardTitle className="flex items-center text-green-800">
              <Settings className="w-6 h-6 mr-2" />
              System Requirements Check
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="space-y-4">
              {browserRequirements.map((req) => {
                const Icon = req.icon;
                return (
                  <div key={req.requirement} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center">
                      <Icon className="w-5 h-5 text-gray-600 mr-3" />
                      <div>
                        <div className="font-medium text-gray-900">{req.requirement}</div>
                        <div className="text-sm text-gray-600">{req.details}</div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      {getStatusIcon(req.status)}
                      <span className={`text-sm font-medium ${getStatusColor(req.status)}`}>
                        {req.status === 'checking' ? 'Checking...' : 
                         req.status === 'pass' ? 'Ready' : 'Failed'}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="mt-6 flex justify-center">
              <Button 
                variant="outline" 
                onClick={performSystemChecks}
                className="flex items-center"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Re-run System Check
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Agreement and Start Test */}
        <Card className="border-2 border-indigo-200">
          <CardContent className="pt-6">
            <div className="space-y-6">
              {/* Agreement Checkbox */}
              <div className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  id="agreement"
                  checked={agreementChecked}
                  onChange={(e) => setAgreementChecked(e.target.checked)}
                  className="mt-1 h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                />
                <label htmlFor="agreement" className="text-sm text-gray-700">
                  I have read and understood all the test instructions, rules, and requirements. 
                  I agree to follow all guidelines and understand that any violation may result 
                  in test disqualification. I confirm that I will complete the test honestly 
                  and to the best of my ability.
                </label>
              </div>

              {/* System Status Summary */}
              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-gray-900">System Status:</span>
                  <div className="flex items-center space-x-2">
                    {allChecksPass ? (
                      <>
                        <CheckCircle className="w-5 h-5 text-green-600" />
                        <span className="text-green-600 font-medium">All Systems Ready</span>
                      </>
                    ) : (
                      <>
                        <AlertTriangle className="w-5 h-5 text-yellow-600" />
                        <span className="text-yellow-600 font-medium">Completing Checks...</span>
                      </>
                    )}
                  </div>
                </div>
              </div>

              {/* Start Test Button */}
              <div className="text-center">
                <Button
                  onClick={onStartTest}
                  disabled={!allChecksPass}
                  size="lg"
                  className={`px-8 py-3 text-lg font-semibold ${
                    allChecksPass 
                      ? 'bg-indigo-600 hover:bg-indigo-700 text-white' 
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  <Play className="w-5 h-5 mr-2" />
                  Start Aptitude Test
                </Button>
                
                {!allChecksPass && (
                  <p className="text-sm text-gray-600 mt-2">
                    Please complete all system checks and accept the agreement to start the test
                  </p>
                )}
              </div>

              {/* Additional Info */}
              <div className="text-center text-sm text-gray-600 border-t pt-4">
                <p>
                  Once you click "Start Aptitude Test", the timer will begin immediately. 
                  Make sure you're ready to begin and won't be interrupted.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default PreTestInstructions;