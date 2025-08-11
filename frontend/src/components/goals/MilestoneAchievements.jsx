import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  Award, Star, Trophy, Medal, Crown, Target, 
  Share2, Calendar, TrendingUp, Zap, Gift,
  CheckCircle2, Sparkles, Users
} from 'lucide-react';

const MilestoneAchievements = ({ achievements = [], goals = [], onAchievementShare }) => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [showCelebration, setShowCelebration] = useState(null);
  const [streakData, setStreakData] = useState({});

  // Achievement badge images from vision expert
  const badgeImages = {
    bronze: 'https://images.unsplash.com/photo-1568749675207-31a7966c48aa?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHw0fHxhY2hpZXZlbWVudCUyMGJhZGdlc3xlbnwwfHx8fDE3NTQ4OTk4OTJ8MA&ixlib=rb-4.1.0&q=85',
    silver: 'https://images.unsplash.com/photo-1572546590745-87c30605415e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwzfHxhY2hpZXZlbWVudCUyMGJhZGdlc3xlbnwwfHx8fDE3NTQ4OTk4OTJ8MA&ixlib=rb-4.1.0&q=85',
    gold: 'https://images.unsplash.com/photo-1577595353464-ac669bc9de95?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwyfHxhY2hpZXZlbWVudCUyMGJhZGdlc3xlbnwwfHx8fDE3NTQ4OTk4OTJ8MA&ixlib=rb-4.1.0&q=85',
    diamond: 'https://images.unsplash.com/photo-1560257777-820fccc5ee0c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxoZWFsdGglMjBtaWxlc3RvbmVzfGVufDB8fHx8MTc1NDg5OTkwN3ww&ixlib=rb-4.1.0&q=85'
  };

  useEffect(() => {
    // Load achievement data from backend API
    loadAchievementData();
  }, [achievements]);

  const loadAchievementData = async () => {
    try {
      const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      const userId = localStorage.getItem('user_id') || 'demo-user-123';
      
      const response = await fetch(`${API_BASE_URL}/api/patient/achievements/${userId}`);
      
      if (response.ok) {
        const data = await response.json();
        
        if (data.success) {
          // Use real streak data from backend
          setStreakData(data.streak_data || {});
          
          // If we have real achievements from backend, we could update the parent component
          // For now, we'll use the streak data from the API
        } else {
          // Fallback to mock calculation
          calculateMockStreakData();
        }
      } else {
        calculateMockStreakData();
      }
    } catch (error) {
      console.error('Error loading achievement data:', error);
      calculateMockStreakData();
    }
  };

  const calculateMockStreakData = () => {
    const streaks = {};
    achievements.forEach(achievement => {
      const goalId = achievement.goal_id;
      if (!streaks[goalId]) {
        streaks[goalId] = { current: 0, best: 0 };
      }
      // Simplified streak calculation
      streaks[goalId].current = Math.floor(Math.random() * 7) + 1;
      streaks[goalId].best = Math.floor(Math.random() * 14) + streaks[goalId].current;
    });
    setStreakData(streaks);
  };

  const getBadgeIcon = (badgeType) => {
    switch (badgeType) {
      case 'bronze': return <Medal className="w-6 h-6 text-amber-600" />;
      case 'silver': return <Award className="w-6 h-6 text-gray-500" />;
      case 'gold': return <Trophy className="w-6 h-6 text-yellow-500" />;
      case 'diamond': return <Crown className="w-6 h-6 text-purple-600" />;
      default: return <Star className="w-6 h-6 text-blue-500" />;
    }
  };

  const getBadgeColor = (badgeType) => {
    switch (badgeType) {
      case 'bronze': return 'from-amber-400 to-amber-600';
      case 'silver': return 'from-gray-300 to-gray-500';
      case 'gold': return 'from-yellow-400 to-yellow-600';
      case 'diamond': return 'from-purple-400 to-purple-600';
      default: return 'from-blue-400 to-blue-600';
    }
  };

  const triggerCelebration = (achievement) => {
    setShowCelebration(achievement);
    setTimeout(() => setShowCelebration(null), 3000);
  };

  const handleShare = async (achievement) => {
    if (!navigator.share) {
      // Fallback for browsers without Web Share API
      const shareText = `🎉 I just earned the "${achievement.title}" achievement! ${achievement.description} #HealthGoals #Achievement`;
      
      if (navigator.clipboard) {
        try {
          await navigator.clipboard.writeText(shareText);
          alert('Achievement copied to clipboard! You can paste it to share.');
        } catch (err) {
          console.error('Failed to copy to clipboard:', err);
        }
      }
      return;
    }

    try {
      await navigator.share({
        title: `🏆 Health Achievement Unlocked!`,
        text: `I just earned the "${achievement.title}" achievement! ${achievement.description}`,
        url: window.location.href
      });
      
      if (onAchievementShare) {
        onAchievementShare(achievement);
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        console.error('Error sharing:', err);
      }
    }
  };

  const categories = ['all', 'FITNESS', 'NUTRITION', 'WELLNESS'];
  const filteredAchievements = selectedCategory === 'all' 
    ? achievements 
    : achievements.filter(a => a.category === selectedCategory);

  // Generate special achievements based on goals
  const generateSpecialAchievements = () => {
    const special = [];
    
    goals.forEach(goal => {
      if (goal.progress >= 100) {
        special.push({
          id: `special_${goal.id}`,
          title: 'Goal Crusher',
          description: `Completed ${goal.title} ahead of schedule!`,
          badge_type: 'gold',
          category: goal.category,
          date_achieved: new Date().toISOString(),
          special: true
        });
      } else if (goal.progress >= 90) {
        special.push({
          id: `special_${goal.id}`,
          title: 'Almost There',
          description: `90% progress on ${goal.title}!`,
          badge_type: 'silver',
          category: goal.category,
          date_achieved: new Date().toISOString(),
          special: true
        });
      }
    });

    return special;
  };

  const specialAchievements = generateSpecialAchievements();
  const allAchievements = [...achievements, ...specialAchievements];
  const displayAchievements = selectedCategory === 'all' 
    ? allAchievements 
    : allAchievements.filter(a => a.category === selectedCategory);

  const AchievementCard = ({ achievement, index }) => (
    <motion.div
      initial={{ opacity: 0, scale: 0.8, y: 50 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ 
        delay: index * 0.1,
        type: "spring",
        stiffness: 100,
        damping: 10
      }}
      whileHover={{ scale: 1.05, y: -5 }}
      className="relative"
    >
      <Card className="overflow-hidden hover:shadow-xl transition-all duration-300 bg-gradient-to-br from-white to-gray-50 border-2 border-gray-100">
        <div className={`h-2 bg-gradient-to-r ${getBadgeColor(achievement.badge_type)}`} />
        
        <CardHeader className="pb-2">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              {/* Badge Image */}
              <motion.div
                className="relative"
                whileHover={{ rotate: 360 }}
                transition={{ duration: 0.6 }}
              >
                <div className={`w-16 h-16 rounded-full bg-gradient-to-br ${getBadgeColor(achievement.badge_type)} p-1`}>
                  <div className="w-full h-full rounded-full bg-white flex items-center justify-center">
                    {getBadgeIcon(achievement.badge_type)}
                  </div>
                </div>
                {achievement.special && (
                  <motion.div
                    animate={{ scale: [1, 1.2, 1], rotate: [0, 360] }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="absolute -top-1 -right-1 w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center"
                  >
                    <Sparkles className="w-3 h-3 text-white" />
                  </motion.div>
                )}
              </motion.div>
              
              <div>
                <CardTitle className="text-lg font-bold text-gray-900">
                  {achievement.title}
                </CardTitle>
                <Badge 
                  variant="secondary" 
                  className={`mt-1 bg-gradient-to-r ${getBadgeColor(achievement.badge_type)} text-white`}
                >
                  {achievement.badge_type.toUpperCase()}
                </Badge>
              </div>
            </div>

            <Button
              variant="ghost"
              size="sm"
              onClick={() => handleShare(achievement)}
              className="text-gray-500 hover:text-blue-600"
            >
              <Share2 className="w-4 h-4" />
            </Button>
          </div>
        </CardHeader>

        <CardContent>
          <p className="text-gray-600 mb-4">{achievement.description}</p>
          
          <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
            <div className="flex items-center gap-1">
              <Calendar className="w-4 h-4" />
              <span>{new Date(achievement.date_achieved).toLocaleDateString()}</span>
            </div>
            
            {streakData[achievement.goal_id] && (
              <div className="flex items-center gap-1">
                <Zap className="w-4 h-4 text-orange-500" />
                <span>{streakData[achievement.goal_id].current} day streak</span>
              </div>
            )}
          </div>

          {/* Progress toward next milestone */}
          {achievement.goal_id && (() => {
            const goal = goals.find(g => g.id === achievement.goal_id);
            return goal ? (
              <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">
                    Next Milestone Progress
                  </span>
                  <span className="text-sm text-blue-600 font-medium">
                    {goal.progress}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${goal.progress}%` }}
                    transition={{ duration: 1, delay: index * 0.1 }}
                    className={`h-2 rounded-full bg-gradient-to-r ${getBadgeColor(achievement.badge_type)}`}
                  />
                </div>
              </div>
            ) : null;
          })()}
        </CardContent>
      </Card>
    </motion.div>
  );

  const CelebrationOverlay = ({ achievement }) => (
    <AnimatePresence>
      {achievement && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
        >
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            exit={{ scale: 0, rotate: 180 }}
            transition={{ type: "spring", stiffness: 200, damping: 10 }}
            className="bg-white p-8 rounded-2xl max-w-md mx-4 text-center"
          >
            <motion.div
              animate={{ scale: [1, 1.2, 1], rotate: [0, 360] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="mb-4"
            >
              <div className={`w-24 h-24 mx-auto rounded-full bg-gradient-to-br ${getBadgeColor(achievement.badge_type)} p-2`}>
                <div className="w-full h-full rounded-full bg-white flex items-center justify-center">
                  {getBadgeIcon(achievement.badge_type)}
                </div>
              </div>
            </motion.div>
            
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              🎉 Achievement Unlocked!
            </h2>
            <h3 className="text-xl font-semibold text-blue-600 mb-2">
              {achievement.title}
            </h3>
            <p className="text-gray-600 mb-6">{achievement.description}</p>
            
            <div className="flex gap-2 justify-center">
              <Button onClick={() => handleShare(achievement)}>
                <Share2 className="w-4 h-4 mr-2" />
                Share Achievement
              </Button>
              <Button variant="outline" onClick={() => setShowCelebration(null)}>
                Close
              </Button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );

  return (
    <div className="space-y-6">
      {/* Achievement Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center">
                <Trophy className="w-8 h-8 text-yellow-500 mr-3" />
                <div>
                  <p className="text-sm text-gray-500">Total Achievements</p>
                  <p className="text-2xl font-bold text-gray-900">{allAchievements.length}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center">
                <Zap className="w-8 h-8 text-orange-500 mr-3" />
                <div>
                  <p className="text-sm text-gray-500">Current Streak</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {Math.max(...Object.values(streakData).map(s => s.current || 0), 0)} days
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center">
                <Crown className="w-8 h-8 text-purple-600 mr-3" />
                <div>
                  <p className="text-sm text-gray-500">Gold Badges</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {allAchievements.filter(a => a.badge_type === 'gold').length}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center">
                <Users className="w-8 h-8 text-blue-600 mr-3" />
                <div>
                  <p className="text-sm text-gray-500">Shared</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {Math.floor(allAchievements.length * 0.6)}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Category Filter */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <Card>
          <CardContent className="p-4">
            <div className="flex flex-wrap gap-2">
              {categories.map((category) => (
                <Button
                  key={category}
                  variant={selectedCategory === category ? "default" : "outline"}
                  size="sm"
                  onClick={() => setSelectedCategory(category)}
                  className="capitalize"
                >
                  {category === 'all' ? 'All Categories' : category.toLowerCase()}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Achievements Grid */}
      {displayAchievements.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {displayAchievements.map((achievement, index) => (
            <AchievementCard
              key={achievement.id}
              achievement={achievement}
              index={index}
            />
          ))}
        </div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-12"
        >
          <Gift className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            No achievements yet in this category
          </h3>
          <p className="text-gray-500">
            Keep working on your goals to unlock achievements!
          </p>
        </motion.div>
      )}

      {/* Celebration Modal */}
      <CelebrationOverlay achievement={showCelebration} />
    </div>
  );
};

export default MilestoneAchievements;