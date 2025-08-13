import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  GraduationCap, BookOpen, Calendar, Clock, 
  Star, Play, Download, Award, Search, Filter,
  TrendingUp, Users, CheckCircle, AlertTriangle, Target
} from 'lucide-react';

const ProfessionalContinuingEducation = () => {
  const [educationData, setEducationData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');

  const providerId = 'provider-123';

  useEffect(() => {
    fetchEducationData();
  }, []);

  const fetchEducationData = async () => {
    try {
      setLoading(true);
      const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/provider/continuing-education/${providerId}`);
      const data = await response.json();
      setEducationData(data);
    } catch (error) {
      console.error('Error fetching education data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEnrollment = async (courseId) => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/provider/courses/${courseId}/enroll`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ provider_id: providerId })
      });
      
      const result = await response.json();
      if (result.enrollment_status === 'success') {
        // Refresh education data
        fetchEducationData();
      }
    } catch (error) {
      console.error('Error enrolling in course:', error);
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getProgressColor = (progress) => {
    if (progress >= 80) return 'bg-green-500';
    if (progress >= 50) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'in_progress': return 'bg-blue-100 text-blue-800';
      case 'not_started': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <Card>
          <CardContent className="pt-6">
            <div className="animate-pulse space-y-4">
              <div className="h-4 bg-gray-200 rounded w-1/4"></div>
              <div className="grid grid-cols-3 gap-4">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="h-20 bg-gray-200 rounded"></div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'dashboard'
                ? 'border-emerald-500 text-emerald-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <GraduationCap className="w-4 h-4 inline mr-2" />
            CME Dashboard
          </button>
          <button
            onClick={() => setActiveTab('courses')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'courses'
                ? 'border-emerald-500 text-emerald-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <BookOpen className="w-4 h-4 inline mr-2" />
            Available Courses
          </button>
          <button
            onClick={() => setActiveTab('mycourses')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'mycourses'
                ? 'border-emerald-500 text-emerald-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <CheckCircle className="w-4 h-4 inline mr-2" />
            My Courses
          </button>
          <button
            onClick={() => setActiveTab('certificates')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'certificates'
                ? 'border-emerald-500 text-emerald-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <Award className="w-4 h-4 inline mr-2" />
            Certificates
          </button>
        </nav>
      </div>

      {/* CME Dashboard Tab */}
      {activeTab === 'dashboard' && (
        <div className="space-y-6">
          {/* Progress Overview */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Target className="w-5 h-5 mr-2 text-emerald-600" />
                CME Progress Overview
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
                <div className="text-center p-6 bg-emerald-50 rounded-lg">
                  <div className="text-3xl font-bold text-emerald-600">
                    {educationData?.education_summary?.total_credits_earned || 0}
                  </div>
                  <div className="text-sm text-gray-600">Credits Earned</div>
                </div>
                <div className="text-center p-6 bg-blue-50 rounded-lg">
                  <div className="text-3xl font-bold text-blue-600">
                    {educationData?.education_summary?.credits_required || 50}
                  </div>
                  <div className="text-sm text-gray-600">Credits Required</div>
                </div>
                <div className="text-center p-6 bg-purple-50 rounded-lg">
                  <div className="text-3xl font-bold text-purple-600">
                    {Math.round(educationData?.education_summary?.progress_percentage || 0)}%
                  </div>
                  <div className="text-sm text-gray-600">Progress</div>
                </div>
                <div className="text-center p-6 bg-orange-50 rounded-lg">
                  <div className="text-3xl font-bold text-orange-600">
                    {educationData?.education_summary?.courses_completed || 0}
                  </div>
                  <div className="text-sm text-gray-600">Completed</div>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="mb-4">
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                  <span>CME Progress</span>
                  <span>{educationData?.education_summary?.progress_percentage || 0}% Complete</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div 
                    className="bg-emerald-500 h-3 rounded-full"
                    style={{ width: `${educationData?.education_summary?.progress_percentage || 0}%` }}
                  />
                </div>
              </div>

              {/* Deadline Alert */}
              <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="flex items-center">
                  <AlertTriangle className="w-5 h-5 text-yellow-600 mr-2" />
                  <div>
                    <div className="font-medium text-yellow-900">
                      CME Deadline: {educationData?.education_summary?.deadline || 'Dec 31, 2024'}
                    </div>
                    <div className="text-sm text-yellow-800">
                      {(educationData?.education_summary?.credits_required || 50) - 
                       (educationData?.education_summary?.total_credits_earned || 0)} 
                      credits remaining
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Upcoming Deadlines */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Calendar className="w-5 h-5 mr-2 text-orange-600" />
                Upcoming Deadlines
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {educationData?.upcoming_deadlines?.map((deadline, index) => (
                  <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <div className="font-medium text-gray-900">{deadline.course}</div>
                      <div className="text-sm text-gray-600">Due: {deadline.due_date}</div>
                    </div>
                    <Badge className={deadline.days_left <= 7 ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}>
                      {deadline.days_left} days left
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Available Courses Tab */}
      {activeTab === 'courses' && (
        <div className="space-y-6">
          {/* Search and Filter */}
          <Card>
            <CardContent className="pt-6">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                    <input
                      type="text"
                      placeholder="Search courses..."
                      className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                    />
                  </div>
                </div>
                <select 
                  className="border border-gray-300 rounded-md px-3 py-2 bg-white"
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                >
                  <option value="">All Categories</option>
                  {educationData?.categories?.map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.name} ({category.course_count})
                    </option>
                  ))}
                </select>
                <Button variant="outline">
                  <Filter className="w-4 h-4 mr-2" />
                  Advanced Filters
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Featured Courses */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Star className="w-5 h-5 mr-2 text-emerald-600" />
                Featured Courses
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {educationData?.featured_courses?.map((course) => (
                  <div key={course.id} className="border rounded-lg p-6">
                    <div className="flex justify-between items-start mb-3">
                      <h4 className="font-semibold text-gray-900">{course.title}</h4>
                      <Badge className={getDifficultyColor(course.difficulty)}>
                        {course.difficulty}
                      </Badge>
                    </div>
                    
                    <div className="text-sm text-gray-600 mb-2">{course.provider}</div>
                    <p className="text-sm text-gray-700 mb-4">{course.description}</p>
                    
                    <div className="grid grid-cols-2 gap-4 text-sm mb-4">
                      <div className="flex items-center">
                        <Award className="w-4 h-4 text-emerald-600 mr-1" />
                        {course.credits} Credits
                      </div>
                      <div className="flex items-center">
                        <Clock className="w-4 h-4 text-blue-600 mr-1" />
                        {course.duration}
                      </div>
                      <div className="flex items-center">
                        <Star className="w-4 h-4 text-yellow-600 mr-1" />
                        {course.rating}/5
                      </div>
                      <div className="flex items-center">
                        <Users className="w-4 h-4 text-purple-600 mr-1" />
                        {course.format}
                      </div>
                    </div>
                    
                    {course.learning_objectives && (
                      <div className="mb-4">
                        <h6 className="font-medium text-gray-700 mb-2">Learning Objectives:</h6>
                        <ul className="text-sm text-gray-600 space-y-1">
                          {course.learning_objectives.map((obj, i) => (
                            <li key={i} className="flex items-start">
                              <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                              {obj}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    <div className="flex justify-between items-center">
                      <span className="font-semibold text-emerald-600">{course.cost}</span>
                      {course.enrolled ? (
                        <Badge className="bg-blue-100 text-blue-800">Enrolled</Badge>
                      ) : (
                        <Button 
                          size="sm"
                          onClick={() => handleEnrollment(course.id)}
                          className="bg-emerald-600 hover:bg-emerald-700"
                        >
                          Enroll Now
                        </Button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* My Courses Tab */}
      {activeTab === 'mycourses' && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <BookOpen className="w-5 h-5 mr-2 text-emerald-600" />
              My Enrolled Courses
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {educationData?.my_courses?.map((course) => (
                <div key={course.id} className="border rounded-lg p-4">
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex-1">
                      <h5 className="font-semibold text-gray-900">{course.title}</h5>
                      <div className="text-sm text-gray-600">
                        {course.credits} Credits • Last accessed: {course.last_accessed}
                      </div>
                    </div>
                    <Badge className={getStatusColor(course.status)}>
                      {course.status.replace('_', ' ')}
                    </Badge>
                  </div>
                  
                  {course.status === 'in_progress' && (
                    <div className="mb-3">
                      <div className="flex justify-between text-sm text-gray-600 mb-1">
                        <span>Progress</span>
                        <span>{course.progress}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${getProgressColor(course.progress)}`}
                          style={{ width: `${course.progress}%` }}
                        />
                      </div>
                    </div>
                  )}
                  
                  <div className="flex justify-between items-center">
                    {course.due_date && (
                      <div className="text-sm text-gray-600">
                        Due: {course.due_date}
                      </div>
                    )}
                    <div className="flex space-x-2">
                      {course.status === 'in_progress' && (
                        <Button size="sm" className="bg-emerald-600 hover:bg-emerald-700">
                          <Play className="w-4 h-4 mr-1" />
                          Continue
                        </Button>
                      )}
                      {course.status === 'completed' && course.certificate_url && (
                        <Button size="sm" variant="outline">
                          <Download className="w-4 h-4 mr-1" />
                          Certificate
                        </Button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Certificates Tab */}
      {activeTab === 'certificates' && (
        <Card>
          <CardHeader>
            <div className="flex justify-between items-center">
              <CardTitle className="flex items-center">
                <Award className="w-5 h-5 mr-2 text-emerald-600" />
                My Certificates
              </CardTitle>
              <Button variant="outline">
                <Download className="w-4 h-4 mr-2" />
                Download All
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-center py-12">
              <Award className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <div className="text-gray-500 mb-2">Your Earned Certificates</div>
              <p className="text-sm text-gray-400">
                Completed courses will appear here with downloadable certificates
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ProfessionalContinuingEducation;