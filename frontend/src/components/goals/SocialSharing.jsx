import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Textarea } from '../ui/textarea';
import { Input } from '../ui/input';
import { 
  Share2, Users, Heart, MessageCircle, ExternalLink, 
  Twitter, Facebook, Instagram, Link2, Copy, 
  CheckCircle2, Camera, Image as ImageIcon, Settings
} from 'lucide-react';

const SocialSharing = ({ achievements = [], goals = [] }) => {
  const [shareHistory, setShareHistory] = useState([]);
  const [selectedAchievement, setSelectedAchievement] = useState(null);
  const [customMessage, setCustomMessage] = useState('');
  const [isSharing, setIsSharing] = useState(false);
  const [shareStats, setShareStats] = useState({
    totalShares: 0,
    platforms: { web: 0, copied: 0 },
    engagement: { likes: 0, comments: 0 }
  });
  const [notificationPermission, setNotificationPermission] = useState('default');

  useEffect(() => {
    // Check notification permission status
    if ('Notification' in window) {
      setNotificationPermission(Notification.permission);
    }

    // Load mock share history
    const mockHistory = [
      {
        id: 'share_1',
        achievement_id: 'achievement_1',
        achievement_title: 'First Workout Milestone',
        platform: 'web',
        shared_at: new Date().toISOString(),
        engagement: { likes: 3, comments: 1 }
      },
      {
        id: 'share_2',
        achievement_id: 'achievement_2',
        achievement_title: 'Hydration Champion',
        platform: 'copied',
        shared_at: new Date(Date.now() - 86400000).toISOString(),
        engagement: { likes: 5, comments: 2 }
      }
    ];

    setShareHistory(mockHistory);
    
    // Calculate share stats
    const stats = {
      totalShares: mockHistory.length,
      platforms: { web: 1, copied: 1 },
      engagement: {
        likes: mockHistory.reduce((acc, share) => acc + share.engagement.likes, 0),
        comments: mockHistory.reduce((acc, share) => acc + share.engagement.comments, 0)
      }
    };
    setShareStats(stats);
  }, []);

  const requestNotificationPermission = async () => {
    if ('Notification' in window) {
      try {
        const permission = await Notification.requestPermission();
        setNotificationPermission(permission);
        
        if (permission === 'granted') {
          new Notification('🔔 Notifications enabled!', {
            body: 'You\'ll now be notified when others engage with your shared achievements.',
            icon: '/favicon.ico',
            badge: '/favicon.ico'
          });
        }
      } catch (error) {
        console.error('Error requesting notification permission:', error);
      }
    }
  };

  const generateShareText = (achievement) => {
    const baseMessages = [
      `🎉 Just unlocked "${achievement.title}"! ${achievement.description}`,
      `🏆 Achievement unlocked: ${achievement.title}! ${achievement.description}`,
      `💪 Milestone reached: ${achievement.title}! ${achievement.description}`,
      `🌟 Celebrating my latest achievement: ${achievement.title}! ${achievement.description}`
    ];

    const randomMessage = baseMessages[Math.floor(Math.random() * baseMessages.length)];
    return customMessage || `${randomMessage} #HealthGoals #Achievement #Progress`;
  };

  const handleWebShare = async (achievement) => {
    if (!navigator.share) {
      alert('Web Share API not supported in this browser. Try copying the link instead!');
      return;
    }

    setIsSharing(true);
    
    try {
      const shareData = {
        title: `🏆 Achievement Unlocked: ${achievement.title}`,
        text: generateShareText(achievement),
        url: `${window.location.origin}/achievements/${achievement.id}`
      };

      await navigator.share(shareData);
      
      // Record the share
      const newShare = {
        id: `share_${Date.now()}`,
        achievement_id: achievement.id,
        achievement_title: achievement.title,
        platform: 'web',
        shared_at: new Date().toISOString(),
        engagement: { likes: 0, comments: 0 }
      };

      setShareHistory(prev => [newShare, ...prev]);
      setShareStats(prev => ({
        ...prev,
        totalShares: prev.totalShares + 1,
        platforms: { ...prev.platforms, web: prev.platforms.web + 1 }
      }));

      // Show success notification if permission granted
      if (notificationPermission === 'granted') {
        new Notification('🎉 Achievement shared!', {
          body: `Your "${achievement.title}" achievement has been shared successfully.`,
          icon: '/favicon.ico'
        });
      }

    } catch (error) {
      if (error.name !== 'AbortError') {
        console.error('Error sharing:', error);
      }
    } finally {
      setIsSharing(false);
    }
  };

  const handleCopyLink = async (achievement) => {
    const shareText = generateShareText(achievement);
    const shareUrl = `${window.location.origin}/achievements/${achievement.id}`;
    const fullText = `${shareText}\n\n${shareUrl}`;

    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(fullText);
      } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = fullText;
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
      }

      // Record the share
      const newShare = {
        id: `share_${Date.now()}`,
        achievement_id: achievement.id,
        achievement_title: achievement.title,
        platform: 'copied',
        shared_at: new Date().toISOString(),
        engagement: { likes: 0, comments: 0 }
      };

      setShareHistory(prev => [newShare, ...prev]);
      setShareStats(prev => ({
        ...prev,
        totalShares: prev.totalShares + 1,
        platforms: { ...prev.platforms, copied: prev.platforms.copied + 1 }
      }));

      alert('Achievement copied to clipboard! You can now paste it anywhere to share.');

    } catch (err) {
      console.error('Failed to copy achievement:', err);
      alert('Failed to copy to clipboard. Please try again.');
    }
  };

  const AchievementShareCard = ({ achievement, index }) => (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      whileHover={{ scale: 1.02 }}
    >
      <Card className="hover:shadow-lg transition-shadow duration-300">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className={`w-12 h-12 rounded-full bg-gradient-to-br ${
                achievement.badge_type === 'gold' ? 'from-yellow-400 to-yellow-600' :
                achievement.badge_type === 'silver' ? 'from-gray-300 to-gray-500' :
                achievement.badge_type === 'diamond' ? 'from-purple-400 to-purple-600' :
                'from-amber-400 to-amber-600'
              } flex items-center justify-center`}>
                <CheckCircle2 className="w-6 h-6 text-white" />
              </div>
              <div>
                <CardTitle className="text-lg">{achievement.title}</CardTitle>
                <Badge variant="secondary" className="mt-1">
                  {achievement.badge_type?.toUpperCase() || 'ACHIEVEMENT'}
                </Badge>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-500">
                {new Date(achievement.date_achieved).toLocaleDateString()}
              </p>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <p className="text-gray-600 mb-4">{achievement.description}</p>
          
          {/* Custom message input */}
          {selectedAchievement?.id === achievement.id && (
            <div className="mb-4 p-4 bg-gray-50 rounded-lg">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Customize your message (optional):
              </label>
              <Textarea
                value={customMessage}
                onChange={(e) => setCustomMessage(e.target.value)}
                placeholder={`Default: "🎉 Just unlocked "${achievement.title}"! ${achievement.description}"`}
                className="mb-2"
                rows={3}
              />
              <p className="text-xs text-gray-500">
                Hashtags #HealthGoals #Achievement #Progress will be added automatically
              </p>
            </div>
          )}
          
          {/* Share Actions */}
          <div className="flex flex-wrap gap-2">
            <Button
              onClick={() => handleWebShare(achievement)}
              disabled={isSharing}
              className="flex-1 min-w-0"
            >
              <Share2 className="w-4 h-4 mr-2" />
              {isSharing ? 'Sharing...' : 'Share'}
            </Button>
            
            <Button
              variant="outline"
              onClick={() => handleCopyLink(achievement)}
              className="flex-1 min-w-0"
            >
              <Copy className="w-4 h-4 mr-2" />
              Copy
            </Button>
            
            <Button
              variant="ghost"
              onClick={() => setSelectedAchievement(
                selectedAchievement?.id === achievement.id ? null : achievement
              )}
            >
              <Settings className="w-4 h-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );

  const ShareHistoryItem = ({ share, index }) => {
    const achievement = achievements.find(a => a.id === share.achievement_id);
    
    return (
      <motion.div
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: index * 0.1 }}
        className="flex items-center justify-between p-4 bg-white rounded-lg border"
      >
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-100 rounded-full">
            {share.platform === 'web' ? (
              <ExternalLink className="w-4 h-4 text-blue-600" />
            ) : (
              <Copy className="w-4 h-4 text-blue-600" />
            )}
          </div>
          <div>
            <h4 className="font-medium text-gray-900">{share.achievement_title}</h4>
            <p className="text-sm text-gray-500">
              Shared via {share.platform === 'web' ? 'Web Share' : 'Clipboard'} • {' '}
              {new Date(share.shared_at).toLocaleDateString()}
            </p>
          </div>
        </div>
        
        <div className="flex items-center gap-4 text-sm text-gray-500">
          <div className="flex items-center gap-1">
            <Heart className="w-4 h-4" />
            <span>{share.engagement.likes}</span>
          </div>
          <div className="flex items-center gap-1">
            <MessageCircle className="w-4 h-4" />
            <span>{share.engagement.comments}</span>
          </div>
        </div>
      </motion.div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Social Sharing Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center">
                <Share2 className="w-8 h-8 text-blue-600 mr-3" />
                <div>
                  <p className="text-sm text-gray-500">Total Shares</p>
                  <p className="text-2xl font-bold text-gray-900">{shareStats.totalShares}</p>
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
                <Users className="w-8 h-8 text-green-600 mr-3" />
                <div>
                  <p className="text-sm text-gray-500">Web Shares</p>
                  <p className="text-2xl font-bold text-gray-900">{shareStats.platforms.web}</p>
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
                <Heart className="w-8 h-8 text-red-600 mr-3" />
                <div>
                  <p className="text-sm text-gray-500">Total Likes</p>
                  <p className="text-2xl font-bold text-gray-900">{shareStats.engagement.likes}</p>
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
                <MessageCircle className="w-8 h-8 text-purple-600 mr-3" />
                <div>
                  <p className="text-sm text-gray-500">Comments</p>
                  <p className="text-2xl font-bold text-gray-900">{shareStats.engagement.comments}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Notification Settings */}
      {notificationPermission !== 'granted' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <Card className="border-orange-200 bg-orange-50">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-orange-100 rounded-full">
                    <Users className="w-5 h-5 text-orange-600" />
                  </div>
                  <div>
                    <h3 className="font-medium text-gray-900">Enable Notifications</h3>
                    <p className="text-sm text-gray-600">
                      Get notified when others engage with your shared achievements
                    </p>
                  </div>
                </div>
                <Button onClick={requestNotificationPermission} variant="outline">
                  Enable
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Shareable Achievements */}
      <div>
        <h2 className="text-xl font-bold text-gray-900 mb-4">Share Your Achievements</h2>
        {achievements.length > 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {achievements.map((achievement, index) => (
              <AchievementShareCard
                key={achievement.id}
                achievement={achievement}
                index={index}
              />
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="p-8 text-center">
              <Share2 className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No achievements to share yet
              </h3>
              <p className="text-gray-500">
                Complete some goals to unlock achievements you can share!
              </p>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Share History */}
      {shareHistory.length > 0 && (
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4">Share History</h2>
          <div className="space-y-3">
            {shareHistory.map((share, index) => (
              <ShareHistoryItem
                key={share.id}
                share={share}
                index={index}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SocialSharing;