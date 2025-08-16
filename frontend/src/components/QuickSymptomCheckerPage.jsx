import React, { useState } from 'react';
import { ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import QuickSymptomChecker from './QuickSymptomChecker';

const QuickSymptomCheckerPage = () => {
  const navigate = useNavigate();
  const [userId] = useState(`guest_${Date.now()}`);

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/guest-dashboard')}
                className="flex items-center text-gray-600 hover:text-gray-900 transition-colors"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Back to Dashboard
              </button>
              <div className="h-6 w-px bg-gray-300"></div>
              <h1 className="text-2xl font-bold text-gray-900">
                Quick Symptom Checker & Wellness Advisor
              </h1>
            </div>
            <div className="text-sm text-gray-500">
              Feel Better Fast • AI-powered relief in 3 steps
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-2xl shadow-xl border border-green-200">
          <div className="p-8">
            <QuickSymptomChecker userId={userId} />
          </div>
        </div>
      </div>

      {/* Footer Info */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8">
        <div className="bg-white rounded-xl p-6 border border-green-200">
          <div className="grid md:grid-cols-3 gap-6 text-center">
            <div className="p-4">
              <div className="text-2xl font-bold text-green-600 mb-2">3-Step</div>
              <div className="text-sm text-gray-600">
                Simple assessment process for quick results
              </div>
            </div>
            <div className="p-4">
              <div className="text-2xl font-bold text-blue-600 mb-2">AI-Powered</div>
              <div className="text-sm text-gray-600">
                Advanced algorithms for personalized recommendations
              </div>
            </div>
            <div className="p-4">
              <div className="text-2xl font-bold text-purple-600 mb-2">72-Hour</div>
              <div className="text-sm text-gray-600">
                Structured action plans for measurable relief
              </div>
            </div>
          </div>
          
          <div className="mt-6 pt-6 border-t border-gray-200 text-center">
            <div className="text-xs text-gray-500 max-w-2xl mx-auto">
              <strong>Medical Disclaimer:</strong> This tool provides wellness guidance and is not a substitute for professional medical advice, diagnosis, or treatment. 
              Always consult with a qualified healthcare provider for medical concerns. In case of emergency symptoms, contact emergency services immediately.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuickSymptomCheckerPage;