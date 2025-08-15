import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { 
  BookOpen, Clock, User, Star, Search, Filter, Download, 
  Play, CheckCircle, Award, Calendar, Target, TrendingUp,
  FileText, Users, Brain, Heart, Activity
} from 'lucide-react';

const ProviderEducation = () => {
  const { switchRole } = useRole();
  const [activeTab, setActiveTab] = useState('overview');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [educationData, setEducationData] = useState(null);

  useEffect(() => {
    switchRole('provider');
    
    // Fetch continuing education data
    const fetchEducationData = async () => {
      try {
        const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;
        const response = await fetch(`${backendUrl}/api/provider/continuing-education/provider-123`);
        const data = await response.json();
        setEducationData(data);
      } catch (error) {
        console.error('Error fetching education data:', error);
      }
    };
    
    fetchEducationData();
  }, [switchRole]);

  const handleEnrollCourse = async (courseId) => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/provider/courses/${courseId}/enroll`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify('provider-123')
      });
      
      const result = await response.json();
      console.log('Enrollment result:', result);
      // Refresh education data
      const educationResponse = await fetch(`${backendUrl}/api/provider/continuing-education/provider-123`);
      const updatedData = await educationResponse.json();
      setEducationData(updatedData);
    } catch (error) {
      console.error('Error enrolling in course:', error);
    }
  };

  const getProgressColor = (progress) => {
    if (progress >= 80) return 'bg-green-500';
    if (progress >= 50) return 'bg-yellow-500';
    return 'bg-blue-500';
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'in_progress': return 'bg-blue-100 text-blue-800';
      case 'not_started': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getCategoryIcon = (categoryId) => {
    const icons = {
      diabetes: Brain,
      cardiology: Heart,
      nutrition: Activity,
      mental_health: Users,
      technology: FileText
    };
    return icons[categoryId] || BookOpen;
  };

  if (!educationData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
        <SmartNavigation />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center py-12">
            <BookOpen className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <div className="text-gray-500">Loading continuing education data...</div>
          </div>
        </div>
      </div>
    );
  }

  const filteredCourses = educationData.available_courses?.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         course.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || 
                           educationData.categories.find(cat => 
                             cat.id === selectedCategory && 
                             course.title.toLowerCase().includes(cat.name.toLowerCase().split(' ')[0])
                           );
    return matchesSearch && matchesCategory;
  }) || [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Professional Continuing Education</h1>
          <p className="text-gray-600">Advance your clinical knowledge with evidence-based courses and certifications</p>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('overview')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'overview'
                    ? 'border-emerald-500 text-emerald-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Overview
              </button>
              <button
                onClick={() => setActiveTab('courses')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'courses'
                    ? 'border-emerald-500 text-emerald-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Course Catalog
              </button>
              <button
                onClick={() => setActiveTab('mycourses')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'mycourses'
                    ? 'border-emerald-500 text-emerald-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
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
                Certificates
              </button>
            </nav>
          </div>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <>
            {/* Progress Summary */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <Card className="border-2 border-emerald-200 bg-emerald-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Award className="w-8 h-8 text-emerald-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-emerald-600">
                        {educationData.cme_tracking.total_credits_earned}
                      </div>
                      <p className="text-sm text-gray-600">Credits Earned</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-blue-200 bg-blue-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Target className="w-8 h-8 text-blue-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-blue-600">
                        {Math.round(educationData.education_summary.progress_percentage)}%
                      </div>
                      <p className="text-sm text-gray-600">Progress</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-purple-200 bg-purple-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <BookOpen className="w-8 h-8 text-purple-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-purple-600">
                        {educationData.education_summary.courses_completed}
                      </div>
                      <p className="text-sm text-gray-600">Completed</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-orange-200 bg-orange-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Calendar className="w-8 h-8 text-orange-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-orange-600">
                        {educationData.education_summary.courses_in_progress}
                      </div>
                      <p className="text-sm text-gray-600">In Progress</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Progress Tracking */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
              <div className="lg:col-span-2">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <TrendingUp className="w-5 h-5 mr-2 text-emerald-600" />
                      Credit Progress
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="mb-4">
                      <div className="flex justify-between text-sm font-medium mb-2">
                        <span>Annual Requirement Progress</span>
                        <span>{educationData.education_summary.total_credits_earned} / {educationData.education_summary.credits_required} credits</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div 
                          className="bg-emerald-500 h-3 rounded-full transition-all duration-500"
                          style={{ width: `${educationData.education_summary.progress_percentage}%` }}
                        />
                      </div>
                      <p className="text-sm text-gray-600 mt-2">
                        Deadline: {educationData.education_summary.deadline}
                      </p>
                    </div>
                    
                    {/* Category Progress */}
                    <div className="space-y-3">
                      {educationData.categories.slice(0, 3).map((category) => {
                        const IconComponent = getCategoryIcon(category.id);
                        return (
                          <div key={category.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                            <div className="flex items-center space-x-3">
                              <IconComponent className="w-5 h-5 text-gray-600" />
                              <span className="font-medium text-gray-900">{category.name}</span>
                            </div>
                            <Badge variant="secondary">{category.course_count} courses</Badge>
                          </div>
                        );
                      })}
                    </div>
                  </CardContent>
                </Card>
              </div>

              <div>
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <Calendar className="w-5 h-5 mr-2 text-emerald-600" />
                      Upcoming Deadlines
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {educationData.upcoming_deadlines.map((deadline, index) => (
                        <div key={index} className="p-3 bg-yellow-50 rounded-lg border-l-4 border-yellow-500">
                          <h5 className="font-medium text-yellow-900">{deadline.course}</h5>
                          <div className="text-sm text-yellow-700">Due: {deadline.due_date}</div>
                          <div className="text-sm font-medium text-yellow-800">{deadline.days_left} days left</div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                <Card className="mt-6">
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <Star className="w-5 h-5 mr-2 text-emerald-600" />
                      Featured Courses
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {educationData.featured_courses.slice(0, 2).map((course) => (
                        <div key={course.id} className="p-3 border rounded-lg hover:bg-gray-50">
                          <h5 className="font-medium text-gray-900 mb-1">{course.title}</h5>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-2 text-sm text-gray-600">
                              <Clock className="w-4 h-4" />
                              <span>{course.duration}</span>
                            </div>
                            <Badge className="bg-emerald-100 text-emerald-800">{course.credits} credits</Badge>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </>
        )}

        {/* Course Catalog Tab */}
        {activeTab === 'courses' && (
          <>
            {/* Search and Filters */}
            <div className="flex flex-col md:flex-row gap-4 mb-6">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    placeholder="Search courses..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
              
              <select 
                className="border border-gray-300 rounded-md px-3 py-2 bg-white"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
              >
                <option value="all">All Categories</option>
                {educationData.categories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
              
              <Button variant="outline">
                <Filter className="w-4 h-4 mr-2" />
                More Filters
              </Button>
            </div>

            {/* Course Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredCourses.map((course) => (
                <Card key={course.id} className="hover:shadow-lg transition-shadow duration-200">
                  <CardHeader>
                    <div className="flex justify-between items-start mb-2">
                      <CardTitle className="text-lg leading-tight">{course.title}</CardTitle>
                      <Badge className="bg-emerald-100 text-emerald-800">{course.credits} credits</Badge>
                    </div>
                    <div className="text-sm text-gray-600">{course.provider}</div>
                  </CardHeader>
                  
                  <CardContent>
                    <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                      {course.description}
                    </p>
                    
                    <div className="space-y-2 mb-4">
                      <div className="flex items-center justify-between text-sm">
                        <span className="flex items-center text-gray-600">
                          <Clock className="w-4 h-4 mr-1" />
                          {course.duration}
                        </span>
                        <span className="flex items-center text-gray-600">
                          <Star className="w-4 h-4 mr-1" />
                          {course.rating}
                        </span>
                      </div>
                      
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-600">{course.format}</span>
                        <span className="font-medium text-emerald-600">{course.cost}</span>
                      </div>
                    </div>

                    {course.enrolled ? (
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>Progress</span>
                          <span>{course.progress}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full ${getProgressColor(course.progress)}`}
                            style={{ width: `${course.progress}%` }}
                          />
                        </div>
                        <Button className="w-full bg-blue-600 hover:bg-blue-700">
                          <Play className="w-4 h-4 mr-2" />
                          Continue Course
                        </Button>
                      </div>
                    ) : (
                      <Button 
                        className="w-full bg-emerald-600 hover:bg-emerald-700"
                        onClick={() => handleEnrollCourse(course.id)}
                      >
                        Enroll Now
                      </Button>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          </>
        )}

        {/* My Courses Tab */}
        {activeTab === 'mycourses' && (
          <div className="space-y-6">
            {educationData.my_courses.map((course) => (
              <Card key={course.id}>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900">{course.title}</h3>
                      <div className="flex items-center space-x-4 text-sm text-gray-600 mt-1">
                        <Badge className={getStatusColor(course.status)}>
                          {course.status.replace('_', ' ')}
                        </Badge>
                        <span className="flex items-center">
                          <Award className="w-4 h-4 mr-1" />
                          {course.credits} credits
                        </span>
                        {course.due_date && (
                          <span className="flex items-center">
                            <Calendar className="w-4 h-4 mr-1" />
                            Due: {course.due_date}
                          </span>
                        )}
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-4">
                      {course.status === 'in_progress' && (
                        <div className="text-right">
                          <div className="text-sm text-gray-600">Progress</div>
                          <div className="font-medium text-emerald-600">{course.progress}%</div>
                        </div>
                      )}
                      
                      {course.status === 'completed' ? (
                        <Button variant="outline">
                          <CheckCircle className="w-4 h-4 mr-2 text-green-600" />
                          Completed
                        </Button>
                      ) : (
                        <Button className="bg-blue-600 hover:bg-blue-700">
                          <Play className="w-4 h-4 mr-2" />
                          Continue
                        </Button>
                      )}
                    </div>
                  </div>
                  
                  {course.status === 'in_progress' && (
                    <div className="mt-4">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${getProgressColor(course.progress)}`}
                          style={{ width: `${course.progress}%` }}
                        />
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Certificates Tab */}
        {activeTab === 'certificates' && (
          <>
            <div className="mb-6">
              <div className="flex justify-between items-center">
                <h3 className="text-xl font-semibold text-gray-900">My Certificates</h3>
                <Button variant="outline">
                  <Download className="w-4 h-4 mr-2" />
                  Download All
                </Button>
              </div>
              <p className="text-gray-600 mt-2">
                Total Credits Earned: {educationData.education_summary.total_credits_earned}
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Placeholder for certificates - would be fetched from API */}
              <Card className="border-2 border-emerald-200">
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <Award className="w-8 h-8 text-emerald-600" />
                      <div>
                        <h4 className="font-semibold text-gray-900">Advanced Diabetes Management</h4>
                        <p className="text-sm text-gray-600">4.0 credits • Completed Nov 15, 2023</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-2 mb-4">
                    <div className="text-sm text-gray-600">
                      Certificate Number: ADM-2023-001
                    </div>
                    <div className="text-sm text-gray-600">
                      Verification Code: ADM4B7X9
                    </div>
                  </div>
                  
                  <div className="flex space-x-2">
                    <Button variant="outline" className="flex-1">
                      <Download className="w-4 h-4 mr-2" />
                      Download PDF
                    </Button>
                    <Button variant="outline" className="flex-1">
                      <FileText className="w-4 h-4 mr-2" />
                      Verify
                    </Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-2 border-blue-200">
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <Award className="w-8 h-8 text-blue-600" />
                      <div>
                        <h4 className="font-semibold text-gray-900">Clinical Documentation</h4>
                        <p className="text-sm text-gray-600">3.0 credits • Completed Dec 20, 2023</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-2 mb-4">
                    <div className="text-sm text-gray-600">
                      Certificate Number: CD-2023-002
                    </div>
                    <div className="text-sm text-gray-600">
                      Verification Code: CD8K2M5P
                    </div>
                  </div>
                  
                  <div className="flex space-x-2">
                    <Button variant="outline" className="flex-1">
                      <Download className="w-4 h-4 mr-2" />
                      Download PDF
                    </Button>
                    <Button variant="outline" className="flex-1">
                      <FileText className="w-4 h-4 mr-2" />
                      Verify
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default ProviderEducation;