import React, { useState, useEffect, useRef } from 'react';
import { 
  BookOpen, 
  MessageSquare, 
  Target, 
  Calendar, 
  Heart, 
  TrendingUp,
  Play,
  Download,
  Star,
  Clock,
  CheckCircle,
  AlertCircle,
  Send,
  Plus,
  Edit3,
  Trash2,
  Filter,
  Search,
  Award,
  Activity,
  Users,
  FileText,
  Video,
  Phone,
  Mail,
  Bell,
  Settings,
  ChevronRight,
  ChevronDown,
  Bookmark,
  ThumbsUp,
  Share2,
  ExternalLink
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts';
import SmartNavigation from '../shared/SmartNavigation';

const PatientEngagementHub = () => {
  // Dashboard States
  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [notifications, setNotifications] = useState([]);
  
  // Educational Content States
  const [educationalContent, setEducationalContent] = useState([]);
  const [contentFilter, setContentFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [favoriteContent, setFavoriteContent] = useState([]);
  const [contentCategories] = useState([
    { id: 'all', label: 'All Content', count: 0 },
    { id: 'nutrition', label: 'Nutrition', count: 0 },
    { id: 'exercise', label: 'Exercise', count: 0 },
    { id: 'mental_health', label: 'Mental Health', count: 0 },
    { id: 'heart_health', label: 'Heart Health', count: 0 },
    { id: 'sleep', label: 'Sleep', count: 0 }
  ]);

  // Progress States
  const [progressData, setProgressData] = useState([]);
  const [progressMetrics, setProgressMetrics] = useState({
    totalGoals: 0,
    completedGoals: 0,
    averageProgress: 0,
    streak: 0
  });

  // Goals States
  const [goals, setGoals] = useState([]);
  const [showGoalForm, setShowGoalForm] = useState(false);
  const [newGoal, setNewGoal] = useState({
    title: '',
    description: '',
    target_value: '',
    current_value: 0,
    unit: '',
    deadline: '',
    category: 'health'
  });
  const [editingGoal, setEditingGoal] = useState(null);

  // Communication States
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [messageRecipients] = useState([
    { id: 'provider-123', name: 'Dr. Sarah Johnson', type: 'provider', online: true },
    { id: 'nutritionist-456', name: 'Lisa Chen, RD', type: 'nutritionist', online: false },
    { id: 'support-789', name: 'Support Team', type: 'support', online: true }
  ]);
  const [selectedRecipient, setSelectedRecipient] = useState('provider-123');

  // Appointment States
  const [appointments, setAppointments] = useState([]);
  const [showAppointmentForm, setShowAppointmentForm] = useState(false);
  const [newAppointment, setNewAppointment] = useState({
    provider_id: 'provider-123',
    scheduled_time: '',
    session_type: 'video',
    notes: '',
    reason: ''
  });

  // Engagement Metrics
  const [engagementMetrics, setEngagementMetrics] = useState({
    engagement_score: 0,
    total_interactions: 0,
    goals_completed: 0,
    appointments_attended: 0,
    messages_sent: 0,
    educational_content_viewed: 0
  });

  // Charts Colors
  const chartColors = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4'];

  // Sample Progress Data for Visualization
  const sampleProgressData = [
    { date: '2025-08-01', weight: 165, steps: 8500, calories: 2100, mood: 8 },
    { date: '2025-08-02', weight: 164.8, steps: 9200, calories: 2050, mood: 7 },
    { date: '2025-08-03', weight: 164.5, steps: 10100, calories: 1980, mood: 9 },
    { date: '2025-08-04', weight: 164.2, steps: 8800, calories: 2150, mood: 8 },
    { date: '2025-08-05', weight: 164.0, steps: 9600, calories: 2000, mood: 8 },
    { date: '2025-08-06', weight: 163.8, steps: 11200, calories: 1950, mood: 9 },
    { date: '2025-08-07', weight: 163.5, steps: 9800, calories: 2080, mood: 7 }
  ];

  // Sample Goals Data
  const sampleGoals = [
    {
      id: '1',
      title: 'Lose 10 pounds',
      description: 'Reach target weight of 155 lbs by end of month',
      target_value: 155,
      current_value: 163.5,
      unit: 'lbs',
      deadline: '2025-08-31',
      category: 'weight',
      progress: 75,
      status: 'active'
    },
    {
      id: '2',
      title: 'Walk 10,000 steps daily',
      description: 'Maintain consistent daily step count',
      target_value: 10000,
      current_value: 9800,
      unit: 'steps',
      deadline: '2025-12-31',
      category: 'fitness',
      progress: 98,
      status: 'active'
    },
    {
      id: '3',
      title: 'Drink 8 glasses of water',
      description: 'Stay properly hydrated throughout the day',
      target_value: 8,
      current_value: 6,
      unit: 'glasses',
      deadline: '2025-08-15',
      category: 'nutrition',
      progress: 75,
      status: 'active'
    }
  ];

  // ===== API FUNCTIONS =====

  const fetchEducationalContent = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/patient-engagement/educational-content`);
      if (response.ok) {
        const data = await response.json();
        setEducationalContent(data.content || []);
        addNotification('Educational content loaded', 'success');
      } else {
        throw new Error('Failed to fetch educational content');
      }
    } catch (error) {
      console.error('Error fetching educational content:', error);
      setError('Failed to load educational content');
    } finally {
      setLoading(false);
    }
  };

  const fetchEngagementData = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/patient-engagement/dashboard/patient-456`);
      if (response.ok) {
        const data = await response.json();
        setEngagementMetrics({
          engagement_score: data.engagement_score || 0,
          total_interactions: data.total_interactions || 0,
          goals_completed: data.goals_completed || 0,
          appointments_attended: data.appointments_attended || 0,
          messages_sent: data.messages_sent || 0,
          educational_content_viewed: data.educational_content_viewed || 0
        });
      }
    } catch (error) {
      console.error('Error fetching engagement data:', error);
    }
  };

  const fetchMessages = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/patient-engagement/messages/patient-456`);
      if (response.ok) {
        const data = await response.json();
        setMessages(data.messages || []);
      }
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const sendMessage = async () => {
    if (!newMessage.trim()) return;

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/patient-engagement/messages`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sender_id: 'patient-456',
          recipient_id: selectedRecipient,
          message: newMessage,
          message_type: 'text'
        })
      });

      if (response.ok) {
        setNewMessage('');
        await fetchMessages();
        await trackEngagement('message_sent');
        addNotification('Message sent successfully', 'success');
      } else {
        throw new Error('Failed to send message');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setError('Failed to send message');
    }
  };

  const trackEngagement = async (activityType, activityData = {}) => {
    try {
      await fetch(`${process.env.REACT_APP_BACKEND_URL}/patient-engagement/engagement-tracking`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_id: 'patient-456',
          activity_type: activityType,
          activity_data: activityData
        })
      });
    } catch (error) {
      console.error('Error tracking engagement:', error);
    }
  };

  const scheduleAppointment = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/virtual-consultation/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...newAppointment,
          patient_id: 'patient-456'
        })
      });

      if (response.ok) {
        const appointment = await response.json();
        setAppointments(prev => [...prev, appointment]);
        setNewAppointment({
          provider_id: 'provider-123',
          scheduled_time: '',
          session_type: 'video',
          notes: '',
          reason: ''
        });
        setShowAppointmentForm(false);
        await trackEngagement('appointment_scheduled');
        addNotification('Appointment scheduled successfully', 'success');
      } else {
        throw new Error('Failed to schedule appointment');
      }
    } catch (error) {
      console.error('Error scheduling appointment:', error);
      setError('Failed to schedule appointment');
    } finally {
      setLoading(false);
    }
  };

  // ===== GOAL MANAGEMENT =====

  const addGoal = () => {
    if (!newGoal.title.trim()) return;

    const goal = {
      id: Date.now().toString(),
      ...newGoal,
      target_value: parseFloat(newGoal.target_value),
      progress: Math.min(100, (newGoal.current_value / parseFloat(newGoal.target_value)) * 100),
      status: 'active',
      created_at: new Date().toISOString()
    };

    setGoals(prev => [...prev, goal]);
    setNewGoal({
      title: '',
      description: '',
      target_value: '',
      current_value: 0,
      unit: '',
      deadline: '',
      category: 'health'
    });
    setShowGoalForm(false);
    addNotification('Goal added successfully', 'success');
  };

  const updateGoal = (goalId, updates) => {
    setGoals(prev => prev.map(goal => {
      if (goal.id === goalId) {
        const updatedGoal = { ...goal, ...updates };
        updatedGoal.progress = Math.min(100, (updatedGoal.current_value / updatedGoal.target_value) * 100);
        return updatedGoal;
      }
      return goal;
    }));
    setEditingGoal(null);
    addNotification('Goal updated successfully', 'success');
  };

  const deleteGoal = (goalId) => {
    setGoals(prev => prev.filter(goal => goal.id !== goalId));
    addNotification('Goal deleted', 'info');
  };

  // ===== CONTENT MANAGEMENT =====

  const toggleFavorite = async (contentId) => {
    const isFavorite = favoriteContent.includes(contentId);
    if (isFavorite) {
      setFavoriteContent(prev => prev.filter(id => id !== contentId));
    } else {
      setFavoriteContent(prev => [...prev, contentId]);
      await trackEngagement('content_favorited', { content_id: contentId });
    }
    addNotification(isFavorite ? 'Removed from favorites' : 'Added to favorites', 'info');
  };

  const viewContent = async (content) => {
    await trackEngagement('content_view', { content_id: content.id, content_title: content.title });
    addNotification(`Viewing: ${content.title}`, 'info');
  };

  // ===== UTILITY FUNCTIONS =====

  const addNotification = (message, type) => {
    const notification = {
      id: Date.now(),
      message,
      type,
      timestamp: new Date()
    };
    setNotifications(prev => [...prev, notification]);
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== notification.id));
    }, 5000);
  };

  const getProgressColor = (progress) => {
    if (progress >= 90) return 'text-emerald-600';
    if (progress >= 70) return 'text-blue-600';
    if (progress >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getGoalStatusColor = (status, progress) => {
    if (progress >= 100) return 'bg-emerald-100 text-emerald-800';
    if (status === 'active') return 'bg-blue-100 text-blue-800';
    return 'bg-gray-100 text-gray-800';
  };

  const filteredContent = educationalContent.filter(content => {
    const matchesFilter = contentFilter === 'all' || content.category === contentFilter;
    const matchesSearch = !searchTerm || 
      content.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      content.description.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  // ===== EFFECTS =====

  useEffect(() => {
    fetchEducationalContent();
    fetchEngagementData();
    fetchMessages();
    
    // Initialize with sample data
    setProgressData(sampleProgressData);
    setGoals(sampleGoals);
    
    // Calculate progress metrics
    const totalGoals = sampleGoals.length;
    const completedGoals = sampleGoals.filter(g => g.progress >= 100).length;
    const averageProgress = sampleGoals.reduce((acc, g) => acc + g.progress, 0) / totalGoals;
    
    setProgressMetrics({
      totalGoals,
      completedGoals,
      averageProgress: Math.round(averageProgress),
      streak: 7
    });
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <SmartNavigation />
      
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Patient Engagement Hub</h1>
              <p className="text-gray-600 mt-2">Your comprehensive health and wellness portal</p>
            </div>
            
            {/* Engagement Score */}
            <div className="flex items-center space-x-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-emerald-600">{engagementMetrics.engagement_score}%</div>
                <p className="text-sm text-gray-600">Engagement Score</p>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{progressMetrics.streak}</div>
                <p className="text-sm text-gray-600">Day Streak</p>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">{progressMetrics.completedGoals}/{progressMetrics.totalGoals}</div>
                <p className="text-sm text-gray-600">Goals Completed</p>
              </div>
            </div>
          </div>
          
          {/* Tab Navigation */}
          <div className="flex space-x-1 mt-6">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: Activity },
              { id: 'education', label: 'Education', icon: BookOpen },
              { id: 'progress', label: 'Progress', icon: TrendingUp },
              { id: 'goals', label: 'Goals', icon: Target },
              { id: 'communication', label: 'Messages', icon: MessageSquare },
              { id: 'appointments', label: 'Appointments', icon: Calendar }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center space-x-2 ${
                    activeTab === tab.id
                      ? 'bg-emerald-100 text-emerald-700 border border-emerald-200'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex items-center">
              <AlertCircle className="w-5 h-5 text-red-600 mr-3" />
              <p className="text-red-800">{error}</p>
              <button
                onClick={() => setError('')}
                className="ml-auto text-red-600 hover:text-red-800"
              >
                ×
              </button>
            </div>
          </div>
        )}

        {/* Notifications */}
        {notifications.length > 0 && (
          <div className="fixed top-4 right-4 z-50 space-y-2">
            {notifications.map((notification) => (
              <div
                key={notification.id}
                className={`p-4 rounded-lg shadow-lg border max-w-sm ${
                  notification.type === 'success' ? 'bg-emerald-50 border-emerald-200 text-emerald-800' :
                  notification.type === 'error' ? 'bg-red-50 border-red-200 text-red-800' :
                  'bg-blue-50 border-blue-200 text-blue-800'
                }`}
              >
                <div className="flex items-center">
                  {notification.type === 'success' && <CheckCircle className="w-5 h-5 mr-3" />}
                  {notification.type === 'error' && <AlertCircle className="w-5 h-5 mr-3" />}
                  {notification.type === 'info' && <AlertCircle className="w-5 h-5 mr-3" />}
                  <p className="text-sm font-medium">{notification.message}</p>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Main Content */}
        {activeTab === 'dashboard' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Quick Stats */}
            <div className="lg:col-span-2 grid grid-cols-2 gap-4">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-emerald-100 rounded-lg">
                    <Target className="w-6 h-6 text-emerald-600" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-gray-900">Active Goals</h3>
                    <p className="text-3xl font-bold text-emerald-600">{goals.filter(g => g.status === 'active').length}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-blue-100 rounded-lg">
                    <MessageSquare className="w-6 h-6 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-gray-900">Messages</h3>
                    <p className="text-3xl font-bold text-blue-600">{messages.length}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-purple-100 rounded-lg">
                    <BookOpen className="w-6 h-6 text-purple-600" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-gray-900">Content Viewed</h3>
                    <p className="text-3xl font-bold text-purple-600">{engagementMetrics.educational_content_viewed}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-yellow-100 rounded-lg">
                    <Calendar className="w-6 h-6 text-yellow-600" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-gray-900">Appointments</h3>
                    <p className="text-3xl font-bold text-yellow-600">{appointments.length}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
              <div className="space-y-4">
                {[
                  { icon: CheckCircle, text: 'Completed daily step goal', time: '2 hours ago', color: 'text-emerald-600' },
                  { icon: BookOpen, text: 'Read nutrition article', time: '4 hours ago', color: 'text-blue-600' },
                  { icon: MessageSquare, text: 'Sent message to provider', time: '1 day ago', color: 'text-purple-600' },
                  { icon: Target, text: 'Updated weight goal', time: '2 days ago', color: 'text-yellow-600' }
                ].map((activity, index) => {
                  const Icon = activity.icon;
                  return (
                    <div key={index} className="flex items-center">
                      <Icon className={`w-4 h-4 ${activity.color} mr-3`} />
                      <div className="flex-1">
                        <p className="text-sm text-gray-900">{activity.text}</p>
                        <p className="text-xs text-gray-500">{activity.time}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Progress Overview Chart */}
            <div className="lg:col-span-3 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Weekly Progress Overview</h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={progressData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="weight" stroke="#10b981" strokeWidth={2} name="Weight (lbs)" />
                    <Line type="monotone" dataKey="steps" stroke="#3b82f6" strokeWidth={2} name="Steps" />
                    <Line type="monotone" dataKey="mood" stroke="#8b5cf6" strokeWidth={2} name="Mood (1-10)" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {/* Educational Content Tab */}
        {activeTab === 'education' && (
          <div className="space-y-6">
            {/* Content Filters */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-gray-900">Educational Content Library</h2>
                <div className="flex items-center space-x-3">
                  <div className="relative">
                    <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
                    <input
                      type="text"
                      placeholder="Search content..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                    />
                  </div>
                </div>
              </div>

              {/* Category Filter */}
              <div className="flex flex-wrap gap-2 mb-6">
                {contentCategories.map((category) => (
                  <button
                    key={category.id}
                    onClick={() => setContentFilter(category.id)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      contentFilter === category.id
                        ? 'bg-emerald-100 text-emerald-700 border border-emerald-200'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100 border border-gray-200'
                    }`}
                  >
                    {category.label}
                  </button>
                ))}
              </div>

              {/* Content Grid */}
              {loading ? (
                <div className="text-center py-12">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600 mx-auto"></div>
                  <p className="text-gray-600 mt-2">Loading content...</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filteredContent.map((content) => (
                    <div key={content.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <h4 className="font-medium text-gray-900 mb-1">{content.title}</h4>
                          <p className="text-sm text-gray-600 mb-2">{content.description}</p>
                          <div className="flex items-center space-x-4 text-xs text-gray-500">
                            <span className="flex items-center">
                              <Clock className="w-3 h-3 mr-1" />
                              {content.estimated_read_time} min
                            </span>
                            <span className={`px-2 py-1 rounded ${
                              content.content_type === 'ARTICLE' ? 'bg-blue-100 text-blue-800' :
                              content.content_type === 'VIDEO' ? 'bg-red-100 text-red-800' :
                              content.content_type === 'QUIZ' ? 'bg-purple-100 text-purple-800' :
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {content.content_type}
                            </span>
                          </div>
                        </div>
                        <button
                          onClick={() => toggleFavorite(content.id)}
                          className={`p-1 rounded ${
                            favoriteContent.includes(content.id) ? 'text-yellow-500' : 'text-gray-400'
                          }`}
                        >
                          <Star className="w-4 h-4" />
                        </button>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <button
                          onClick={() => viewContent(content)}
                          className="bg-emerald-600 text-white px-3 py-1 rounded text-sm hover:bg-emerald-700 flex items-center space-x-1"
                        >
                          <Play className="w-3 h-3" />
                          <span>View</span>
                        </button>
                        <div className="flex items-center space-x-2 text-xs text-gray-500">
                          <ThumbsUp className="w-3 h-3" />
                          <span>{content.rating || 4.5}/5</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {filteredContent.length === 0 && !loading && (
                <div className="text-center py-12">
                  <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">No content found matching your criteria</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Progress Tab */}
        {activeTab === 'progress' && (
          <div className="space-y-6">
            {/* Progress Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {[
                { label: 'Average Progress', value: `${progressMetrics.averageProgress}%`, color: 'bg-emerald-500' },
                { label: 'Total Goals', value: progressMetrics.totalGoals, color: 'bg-blue-500' },
                { label: 'Completed Goals', value: progressMetrics.completedGoals, color: 'bg-purple-500' },
                { label: 'Active Streak', value: `${progressMetrics.streak} days`, color: 'bg-yellow-500' }
              ].map((metric, index) => (
                <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center">
                    <div className={`p-2 rounded-lg ${metric.color}`}>
                      <div className="w-4 h-4 bg-white rounded"></div>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm text-gray-600">{metric.label}</p>
                      <p className="text-2xl font-bold text-gray-900">{metric.value}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Progress Visualization */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Progress Tracking</h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={progressData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="steps" fill="#10b981" name="Steps" />
                    <Bar dataKey="calories" fill="#3b82f6" name="Calories" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Goal Progress */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Goal Progress</h3>
              <div className="space-y-4">
                {goals.map((goal) => (
                  <div key={goal.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium text-gray-900">{goal.title}</h4>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getProgressColor(goal.progress)}`}>
                        {Math.round(goal.progress)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                      <div
                        className="bg-emerald-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${goal.progress}%` }}
                      ></div>
                    </div>
                    <div className="flex items-center justify-between text-sm text-gray-600">
                      <span>{goal.current_value} / {goal.target_value} {goal.unit}</span>
                      <span>Due: {new Date(goal.deadline).toLocaleDateString()}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Goals Tab */}
        {activeTab === 'goals' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">Health Goals</h2>
                <button
                  onClick={() => setShowGoalForm(!showGoalForm)}
                  className="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 flex items-center space-x-2"
                >
                  <Plus className="w-4 h-4" />
                  <span>Add Goal</span>
                </button>
              </div>

              {/* Add Goal Form */}
              {showGoalForm && (
                <div className="bg-gray-50 rounded-lg p-6 mb-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Add New Goal</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Goal Title</label>
                      <input
                        type="text"
                        value={newGoal.title}
                        onChange={(e) => setNewGoal(prev => ({ ...prev, title: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                        placeholder="e.g., Lose 10 pounds"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
                      <select
                        value={newGoal.category}
                        onChange={(e) => setNewGoal(prev => ({ ...prev, category: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                      >
                        <option value="health">General Health</option>
                        <option value="weight">Weight Management</option>
                        <option value="fitness">Fitness & Exercise</option>
                        <option value="nutrition">Nutrition</option>
                        <option value="mental">Mental Health</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Target Value</label>
                      <input
                        type="number"
                        value={newGoal.target_value}
                        onChange={(e) => setNewGoal(prev => ({ ...prev, target_value: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                        placeholder="e.g., 155"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Unit</label>
                      <input
                        type="text"
                        value={newGoal.unit}
                        onChange={(e) => setNewGoal(prev => ({ ...prev, unit: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                        placeholder="e.g., lbs, steps, glasses"
                      />
                    </div>
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                      <textarea
                        value={newGoal.description}
                        onChange={(e) => setNewGoal(prev => ({ ...prev, description: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                        rows={3}
                        placeholder="Describe your goal..."
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Deadline</label>
                      <input
                        type="date"
                        value={newGoal.deadline}
                        onChange={(e) => setNewGoal(prev => ({ ...prev, deadline: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Current Value</label>
                      <input
                        type="number"
                        value={newGoal.current_value}
                        onChange={(e) => setNewGoal(prev => ({ ...prev, current_value: parseFloat(e.target.value) || 0 }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                        placeholder="Current progress"
                      />
                    </div>
                  </div>
                  <div className="flex space-x-3 mt-4">
                    <button
                      onClick={addGoal}
                      disabled={!newGoal.title || !newGoal.target_value}
                      className="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 disabled:opacity-50"
                    >
                      Add Goal
                    </button>
                    <button
                      onClick={() => setShowGoalForm(false)}
                      className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}

              {/* Goals List */}
              <div className="space-y-4">
                {goals.map((goal) => (
                  <div key={goal.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1">
                        <h4 className="font-medium text-gray-900 mb-1">{goal.title}</h4>
                        <p className="text-sm text-gray-600 mb-2">{goal.description}</p>
                        <div className="flex items-center space-x-4 text-sm text-gray-600">
                          <span>Category: {goal.category}</span>
                          <span>Due: {new Date(goal.deadline).toLocaleDateString()}</span>
                        </div>
                      </div>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => setEditingGoal(goal.id)}
                          className="p-1 text-blue-600 hover:text-blue-800"
                        >
                          <Edit3 className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => deleteGoal(goal.id)}
                          className="p-1 text-red-600 hover:text-red-800"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                    
                    <div className="mb-3">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm text-gray-600">
                          Progress: {goal.current_value} / {goal.target_value} {goal.unit}
                        </span>
                        <span className={`text-sm font-medium ${getProgressColor(goal.progress)}`}>
                          {Math.round(goal.progress)}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-emerald-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${goal.progress}%` }}
                        ></div>
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getGoalStatusColor(goal.status, goal.progress)}`}>
                        {goal.progress >= 100 ? 'Completed' : goal.status.charAt(0).toUpperCase() + goal.status.slice(1)}
                      </span>
                      {editingGoal === goal.id && (
                        <div className="flex items-center space-x-2">
                          <input
                            type="number"
                            value={goal.current_value}
                            onChange={(e) => updateGoal(goal.id, { current_value: parseFloat(e.target.value) || 0 })}
                            className="w-20 px-2 py-1 border border-gray-300 rounded text-sm"
                          />
                          <button
                            onClick={() => setEditingGoal(null)}
                            className="text-green-600 hover:text-green-800"
                          >
                            <CheckCircle className="w-4 h-4" />
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {goals.length === 0 && (
                <div className="text-center py-12">
                  <Target className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">No goals set yet</p>
                  <p className="text-sm text-gray-500 mt-2">Create your first health goal to get started</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Communication Tab */}
        {activeTab === 'communication' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Contacts Sidebar */}
            <div className="lg:col-span-1 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Contacts</h3>
              <div className="space-y-3">
                {messageRecipients.map((recipient) => (
                  <div
                    key={recipient.id}
                    onClick={() => setSelectedRecipient(recipient.id)}
                    className={`p-3 rounded-lg cursor-pointer transition-colors ${
                      selectedRecipient === recipient.id ? 'bg-emerald-100 border-emerald-200' : 'hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center">
                      <div className="relative">
                        <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
                          <Users className="w-5 h-5 text-gray-600" />
                        </div>
                        <div className={`absolute -bottom-1 -right-1 w-3 h-3 rounded-full border-2 border-white ${
                          recipient.online ? 'bg-green-500' : 'bg-gray-400'
                        }`}></div>
                      </div>
                      <div className="ml-3">
                        <p className="font-medium text-gray-900">{recipient.name}</p>
                        <p className="text-xs text-gray-500">{recipient.type}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Chat Area */}
            <div className="lg:col-span-2 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">
                  {messageRecipients.find(r => r.id === selectedRecipient)?.name || 'Messages'}
                </h3>
                <div className="flex space-x-2">
                  <button className="p-2 text-gray-600 hover:text-gray-800">
                    <Phone className="w-4 h-4" />
                  </button>
                  <button className="p-2 text-gray-600 hover:text-gray-800">
                    <Video className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Messages */}
              <div className="h-96 overflow-y-auto mb-4 p-3 bg-gray-50 rounded-lg">
                {messages.length === 0 ? (
                  <div className="text-center py-12">
                    <MessageSquare className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600">No messages yet</p>
                    <p className="text-sm text-gray-500 mt-2">Start a conversation with your healthcare team</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {messages.filter(m => 
                      m.sender_id === 'patient-456' || m.recipient_id === selectedRecipient ||
                      m.sender_id === selectedRecipient || m.recipient_id === 'patient-456'
                    ).map((message, index) => (
                      <div
                        key={index}
                        className={`flex ${message.sender_id === 'patient-456' ? 'justify-end' : 'justify-start'}`}
                      >
                        <div
                          className={`max-w-xs px-3 py-2 rounded-lg text-sm ${
                            message.sender_id === 'patient-456'
                              ? 'bg-emerald-600 text-white'
                              : 'bg-white border border-gray-200'
                          }`}
                        >
                          <p>{message.message}</p>
                          <p className={`text-xs mt-1 ${
                            message.sender_id === 'patient-456' ? 'text-emerald-100' : 'text-gray-500'
                          }`}>
                            {new Date(message.timestamp).toLocaleTimeString()}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Message Input */}
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                  placeholder="Type a message..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                />
                <button
                  onClick={sendMessage}
                  disabled={!newMessage.trim()}
                  className="bg-emerald-600 text-white p-2 rounded-lg hover:bg-emerald-700 disabled:opacity-50"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Appointments Tab */}
        {activeTab === 'appointments' && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">Appointments</h2>
              <button
                onClick={() => setShowAppointmentForm(!showAppointmentForm)}
                className="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 flex items-center space-x-2"
              >
                <Calendar className="w-4 h-4" />
                <span>Book Appointment</span>
              </button>
            </div>

            {/* Appointment Form */}
            {showAppointmentForm && (
              <div className="bg-gray-50 rounded-lg p-6 mb-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Book New Appointment</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Provider</label>
                    <select
                      value={newAppointment.provider_id}
                      onChange={(e) => setNewAppointment(prev => ({ ...prev, provider_id: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                    >
                      <option value="provider-123">Dr. Sarah Johnson</option>
                      <option value="provider-456">Dr. Michael Chen</option>
                      <option value="provider-789">Dr. Emily Davis</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Appointment Type</label>
                    <select
                      value={newAppointment.session_type}
                      onChange={(e) => setNewAppointment(prev => ({ ...prev, session_type: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                    >
                      <option value="video">Video Consultation</option>
                      <option value="audio">Phone Call</option>
                      <option value="text">Text Chat</option>
                      <option value="in-person">In-Person</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Date & Time</label>
                    <input
                      type="datetime-local"
                      value={newAppointment.scheduled_time}
                      onChange={(e) => setNewAppointment(prev => ({ ...prev, scheduled_time: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Reason</label>
                    <input
                      type="text"
                      value={newAppointment.reason}
                      onChange={(e) => setNewAppointment(prev => ({ ...prev, reason: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                      placeholder="Reason for appointment"
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Notes</label>
                    <textarea
                      value={newAppointment.notes}
                      onChange={(e) => setNewAppointment(prev => ({ ...prev, notes: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                      rows={3}
                      placeholder="Additional notes..."
                    />
                  </div>
                </div>
                <div className="flex space-x-3 mt-4">
                  <button
                    onClick={scheduleAppointment}
                    disabled={!newAppointment.scheduled_time || loading}
                    className="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 disabled:opacity-50"
                  >
                    {loading ? 'Scheduling...' : 'Book Appointment'}
                  </button>
                  <button
                    onClick={() => setShowAppointmentForm(false)}
                    className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}

            {/* Appointments List */}
            <div className="space-y-4">
              {appointments.length === 0 ? (
                <div className="text-center py-12">
                  <Calendar className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">No appointments scheduled</p>
                  <p className="text-sm text-gray-500 mt-2">Book your first appointment to get started</p>
                </div>
              ) : (
                appointments.map((appointment, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-medium text-gray-900">
                          {appointment.reason || 'General Consultation'}
                        </h4>
                        <p className="text-sm text-gray-600">
                          Provider: {appointment.provider_id}
                        </p>
                        <p className="text-sm text-gray-600">
                          {new Date(appointment.scheduled_time).toLocaleString()}
                        </p>
                        <p className="text-sm text-gray-500 mt-1">
                          Type: {appointment.session_type} | Status: {appointment.status}
                        </p>
                        {appointment.notes && (
                          <p className="text-sm text-gray-600 mt-2">{appointment.notes}</p>
                        )}
                      </div>
                      <div className="flex space-x-2">
                        {appointment.status === 'SCHEDULED' && (
                          <button className="bg-emerald-600 text-white px-3 py-1 rounded text-sm hover:bg-emerald-700">
                            Join
                          </button>
                        )}
                        <button className="bg-gray-600 text-white px-3 py-1 rounded text-sm hover:bg-gray-700">
                          Reschedule
                        </button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PatientEngagementHub;