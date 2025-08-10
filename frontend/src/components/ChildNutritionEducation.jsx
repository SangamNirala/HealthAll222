import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Progress } from './ui/progress';
import { 
  BookOpen, Star, Play, Trophy, Users, Clock, Target,
  Award, ChefHat, Apple, Heart, Brain, Gamepad2, Video,
  Calendar, User, CheckCircle, Lock, Unlock
} from 'lucide-react';

const ChildNutritionEducation = () => {
  const { switchRole } = useRole();
  const [educationData, setEducationData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    switchRole('family');
    fetchEducationData();
  }, [switchRole]);

  const fetchEducationData = async () => {
    try {
      const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/family/child-nutrition-education/demo-family-123`);
      const data = await response.json();
      setEducationData(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching education data:', error);
      setLoading(false);
    }
  };

  const getModuleIcon = (type) => {
    switch (type) {
      case 'interactive_game': return <Gamepad2 className="w-5 h-5 text-purple-600" />;
      case 'tutorial_video': return <Video className="w-5 h-5 text-blue-600" />;
      case 'interactive_workshop': return <Users className="w-5 h-5 text-green-600" />;
      case 'hands_on_cooking': return <ChefHat className="w-5 h-5 text-orange-600" />;
      default: return <BookOpen className="w-5 h-5 text-gray-600" />;
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'interactive_game': return 'bg-purple-100 text-purple-800';
      case 'tutorial_video': return 'bg-blue-100 text-blue-800';
      case 'interactive_workshop': return 'bg-green-100 text-green-800';
      case 'hands_on_cooking': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
        <SmartNavigation />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center">Loading nutrition education...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Child Nutrition Education</h1>
          <p className="text-gray-600">Age-appropriate nutrition learning for healthy kids</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-2 border-purple-200 bg-purple-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <BookOpen className="w-8 h-8 text-purple-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-purple-600">
                    {educationData?.age_specific_content?.reduce((total, age) => 
                      total + age.learning_modules.length, 0) || 0}
                  </div>
                  <p className="text-sm text-gray-600">Learning Modules</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-green-200 bg-green-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Trophy className="w-8 h-8 text-green-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-green-600">
                    {educationData?.family_challenges?.length || 0}
                  </div>
                  <p className="text-sm text-gray-600">Active Challenges</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-blue-200 bg-blue-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Star className="w-8 h-8 text-blue-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-blue-600">
                    {educationData?.age_specific_content?.reduce((total, age) => 
                      total + age.learning_modules.filter(module => module.progress > 0).length, 0) || 0}
                  </div>
                  <p className="text-sm text-gray-600">In Progress</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-orange-200 bg-orange-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Users className="w-8 h-8 text-orange-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-orange-600">
                    {educationData?.expert_resources?.length || 0}
                  </div>
                  <p className="text-sm text-gray-600">Expert Resources</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="learning" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="learning">Learning Modules</TabsTrigger>
            <TabsTrigger value="challenges">Family Challenges</TabsTrigger>
            <TabsTrigger value="experts">Expert Resources</TabsTrigger>
            <TabsTrigger value="progress">Progress Tracking</TabsTrigger>
          </TabsList>

          {/* Learning Modules Tab */}
          <TabsContent value="learning" className="space-y-6">
            {educationData?.age_specific_content?.map((ageGroup, index) => (
              <Card key={index}>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <div className="flex items-center">
                      <User className="w-5 h-5 mr-2 text-amber-500" />
                      {ageGroup.age_group}
                    </div>
                    <Badge className="bg-amber-100 text-amber-800">
                      {ageGroup.learning_modules.length} modules
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Learning Modules */}
                    <div className="space-y-4">
                      <h4 className="font-semibold text-gray-900">Learning Modules</h4>
                      {ageGroup.learning_modules.map((module, moduleIndex) => (
                        <div key={moduleIndex} className="border rounded-lg p-4">
                          <div className="flex items-start justify-between mb-3">
                            <div className="flex items-start space-x-3">
                              {getModuleIcon(module.type)}
                              <div className="flex-1">
                                <div className="font-semibold text-gray-900">{module.title}</div>
                                <div className="text-sm text-gray-600 mt-1">
                                  <span className="inline-flex items-center mr-4">
                                    <Clock className="w-4 h-4 mr-1" />
                                    {module.duration}
                                  </span>
                                  <Badge className={getTypeColor(module.type)} variant="secondary">
                                    {module.type.replace('_', ' ')}
                                  </Badge>
                                </div>
                              </div>
                            </div>
                            <div className="text-right">
                              <div className="text-2xl font-bold text-purple-600">{module.progress}%</div>
                              <div className="text-xs text-gray-500">Complete</div>
                            </div>
                          </div>

                          {/* Progress Bar */}
                          <div className="mb-3">
                            <Progress value={module.progress} className="w-full h-2" />
                          </div>

                          {/* Concepts */}
                          <div className="mb-3">
                            <div className="text-sm font-medium text-gray-700 mb-2">Key Concepts:</div>
                            <div className="flex flex-wrap gap-1">
                              {module.concepts.map((concept, conceptIndex) => (
                                <Badge key={conceptIndex} variant="outline" className="text-xs">
                                  {concept}
                                </Badge>
                              ))}
                            </div>
                          </div>

                          {/* Activities */}
                          <div className="mb-3">
                            <div className="text-sm font-medium text-gray-700 mb-2">Activities:</div>
                            <ul className="text-sm text-gray-600 space-y-1">
                              {module.activities.map((activity, activityIndex) => (
                                <li key={activityIndex} className="flex items-center">
                                  <CheckCircle className="w-4 h-4 mr-2 text-green-500" />
                                  {activity}
                                </li>
                              ))}
                            </ul>
                          </div>

                          {/* Completion Badge */}
                          <div className="flex items-center justify-between pt-3 border-t">
                            <div className="flex items-center">
                              <Award className="w-4 h-4 mr-2 text-yellow-500" />
                              <span className="text-sm font-medium">Badge: {module.completion_badge}</span>
                            </div>
                            <Button 
                              size="sm" 
                              className={module.progress > 0 ? "bg-purple-500 hover:bg-purple-600" : ""}
                              disabled={module.progress === 100}
                            >
                              {module.progress === 0 ? (
                                <>
                                  <Play className="w-4 h-4 mr-2" />
                                  Start Module
                                </>
                              ) : module.progress === 100 ? (
                                <>
                                  <Trophy className="w-4 h-4 mr-2" />
                                  Completed
                                </>
                              ) : (
                                <>
                                  <Play className="w-4 h-4 mr-2" />
                                  Continue
                                </>
                              )}
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* Dietary Considerations & Portions */}
                    <div className="space-y-4">
                      <div>
                        <h4 className="font-semibold text-gray-900 mb-3">Dietary Considerations</h4>
                        <div className="space-y-2">
                          {ageGroup.dietary_considerations.map((consideration, idx) => (
                            <div key={idx} className="p-2 bg-blue-50 rounded border-l-4 border-blue-400">
                              <div className="text-sm text-blue-800 capitalize">
                                {consideration.replace('_', ' ')}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>

                      <div>
                        <h4 className="font-semibold text-gray-900 mb-3">Recommended Daily Portions</h4>
                        <div className="space-y-2">
                          {Object.entries(ageGroup.recommended_portions).map(([food, portion]) => (
                            <div key={food} className="flex items-center justify-between p-2 bg-green-50 rounded">
                              <div className="text-sm font-medium text-green-900 capitalize">
                                {food.replace('_', ' ')}
                              </div>
                              <div className="text-sm text-green-700">{portion}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </TabsContent>

          {/* Family Challenges Tab */}
          <TabsContent value="challenges" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Trophy className="w-5 h-5 mr-2 text-green-500" />
                    Active Family Challenges
                  </div>
                  <Button className="bg-green-500 hover:bg-green-600">
                    <Target className="w-4 h-4 mr-2" />
                    Create Challenge
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {educationData?.family_challenges?.map((challenge, index) => (
                  <div key={index} className="border rounded-lg p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <div className="text-xl font-semibold text-gray-900">{challenge.name}</div>
                        <div className="text-gray-600 mt-1">{challenge.description}</div>
                        <div className="text-sm text-gray-500 mt-2">
                          Duration: {challenge.duration} • {challenge.participants.length} participants
                        </div>
                      </div>
                      <Trophy className="w-8 h-8 text-yellow-500" />
                    </div>

                    {/* Progress for each participant */}
                    <div className="space-y-3 mb-4">
                      <h5 className="font-medium text-gray-900">Participant Progress</h5>
                      {Object.entries(challenge.progress).map(([participant, progress]) => (
                        <div key={participant} className="flex items-center space-x-3">
                          <div className="w-20 text-sm font-medium">{participant}</div>
                          <div className="flex-1">
                            <Progress value={progress} className="w-full h-2" />
                          </div>
                          <div className="w-12 text-sm text-gray-600">{progress}%</div>
                        </div>
                      ))}
                    </div>

                    {/* Rewards */}
                    <div className="p-4 bg-yellow-50 rounded-lg border-l-4 border-yellow-400">
                      <div className="font-medium text-yellow-900 mb-2">Rewards</div>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                        {challenge.rewards.map((reward, rewardIndex) => (
                          <div key={rewardIndex} className="text-sm text-yellow-800 flex items-center">
                            <Star className="w-4 h-4 mr-1" />
                            {reward}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Expert Resources Tab */}
          <TabsContent value="experts" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Users className="w-5 h-5 mr-2 text-blue-500" />
                  Expert Resources & Events
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {educationData?.expert_resources?.map((resource, index) => (
                  <div key={index} className="border rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-4">
                        <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                          {resource.type === 'live_session' ? (
                            <Video className="w-6 h-6 text-blue-600" />
                          ) : (
                            <ChefHat className="w-6 h-6 text-blue-600" />
                          )}
                        </div>
                        <div className="flex-1">
                          <div className="font-semibold text-gray-900">{resource.title}</div>
                          <div className="text-sm text-gray-600 mt-1">
                            <span className="inline-flex items-center mr-4">
                              <Calendar className="w-4 h-4 mr-1" />
                              {resource.date} at {resource.time}
                            </span>
                            {resource.location && (
                              <span className="inline-flex items-center mr-4">
                                <MapPin className="w-4 h-4 mr-1" />
                                {resource.location}
                              </span>
                            )}
                          </div>
                          
                          {/* Expert/Instructor */}
                          <div className="text-sm text-gray-700 mt-2">
                            {resource.expert && `Expert: ${resource.expert}`}
                            {resource.instructor && `Instructor: ${resource.instructor}`}
                          </div>

                          {/* Topics/Focus */}
                          <div className="mt-2">
                            {resource.topics && (
                              <div className="text-sm text-gray-600">
                                <span className="font-medium">Topics: </span>
                                {resource.topics.join(', ')}
                              </div>
                            )}
                            {resource.focus && (
                              <div className="text-sm text-gray-600">
                                <span className="font-medium">Focus: </span>
                                {resource.focus}
                              </div>
                            )}
                            {resource.age_range && (
                              <div className="text-sm text-gray-600">
                                <span className="font-medium">Age Range: </span>
                                {resource.age_range}
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <Badge className={getTypeColor(resource.type)}>
                          {resource.type.replace('_', ' ')}
                        </Badge>
                        <Button size="sm" className="bg-blue-500 hover:bg-blue-600">
                          {resource.registration_required ? 'Register' : 'Join'}
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Progress Tracking Tab */}
          <TabsContent value="progress" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Individual Progress */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <User className="w-5 h-5 mr-2 text-purple-500" />
                    Individual Progress
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {educationData?.age_specific_content?.map((ageGroup, index) => (
                    <div key={index} className="p-4 border rounded-lg">
                      <div className="font-medium text-gray-900 mb-3">{ageGroup.age_group}</div>
                      {ageGroup.learning_modules.map((module, moduleIndex) => (
                        <div key={moduleIndex} className="mb-3 last:mb-0">
                          <div className="flex items-center justify-between mb-1">
                            <div className="text-sm font-medium">{module.title}</div>
                            <div className="text-sm text-gray-600">{module.progress}%</div>
                          </div>
                          <Progress value={module.progress} className="w-full h-2" />
                        </div>
                      ))}
                    </div>
                  ))}
                </CardContent>
              </Card>

              {/* Family Challenge Progress */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Trophy className="w-5 h-5 mr-2 text-green-500" />
                    Challenge Progress
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {educationData?.family_challenges?.map((challenge, index) => (
                    <div key={index} className="p-4 border rounded-lg">
                      <div className="font-medium text-gray-900 mb-3">{challenge.name}</div>
                      <div className="space-y-2">
                        {Object.entries(challenge.progress).map(([participant, progress]) => (
                          <div key={participant}>
                            <div className="flex items-center justify-between mb-1">
                              <div className="text-sm font-medium">{participant}</div>
                              <div className="text-sm text-gray-600">{progress}%</div>
                            </div>
                            <Progress value={progress} className="w-full h-2" />
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default ChildNutritionEducation;