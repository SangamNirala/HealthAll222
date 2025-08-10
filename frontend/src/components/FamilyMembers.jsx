import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { User, UserPlus, Edit3, Trash2, Heart, Calendar, Phone } from 'lucide-react';

const FamilyMembers = () => {
  const { switchRole } = useRole();
  const [members, setMembers] = useState([
    {
      id: 1,
      name: 'John Smith',
      relationship: 'Spouse',
      age: 42,
      healthStatus: 'Good',
      conditions: ['Hypertension'],
      lastCheckup: '2024-01-15',
      phone: '(555) 123-4567'
    },
    {
      id: 2,
      name: 'Emma Smith', 
      relationship: 'Daughter',
      age: 16,
      healthStatus: 'Excellent',
      conditions: [],
      lastCheckup: '2023-12-10',
      phone: '(555) 234-5678'
    },
    {
      id: 3,
      name: 'Michael Smith',
      relationship: 'Son',
      age: 12,
      healthStatus: 'Good',
      conditions: ['Asthma'],
      lastCheckup: '2024-01-08',
      phone: ''
    }
  ]);

  const [showAddForm, setShowAddForm] = useState(false);
  const [newMember, setNewMember] = useState({
    name: '',
    relationship: 'Child',
    age: '',
    phone: ''
  });

  useEffect(() => {
    switchRole('family');
  }, [switchRole]);

  const relationships = ['Spouse', 'Child', 'Parent', 'Sibling', 'Other'];

  const getHealthStatusColor = (status) => {
    switch (status) {
      case 'Excellent': return 'bg-green-100 text-green-800';
      case 'Good': return 'bg-blue-100 text-blue-800';
      case 'Fair': return 'bg-yellow-100 text-yellow-800';
      case 'Needs Attention': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const handleAddMember = () => {
    if (newMember.name && newMember.age) {
      const member = {
        id: members.length + 1,
        ...newMember,
        age: parseInt(newMember.age),
        healthStatus: 'Good',
        conditions: [],
        lastCheckup: 'Not scheduled'
      };
      setMembers([...members, member]);
      setNewMember({ name: '', relationship: 'Child', age: '', phone: '' });
      setShowAddForm(false);
    }
  };

  const deleteMember = (id) => {
    setMembers(members.filter(member => member.id !== id));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Family Members</h1>
          <p className="text-gray-600">Manage health information for your family members</p>
        </div>

        {/* Family Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-2 border-amber-200 bg-amber-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <User className="w-8 h-8 text-amber-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-amber-600">{members.length}</div>
                  <p className="text-sm text-gray-600">Family Members</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-green-200 bg-green-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Heart className="w-8 h-8 text-green-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-green-600">
                    {members.filter(m => m.healthStatus === 'Excellent' || m.healthStatus === 'Good').length}
                  </div>
                  <p className="text-sm text-gray-600">Healthy</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-blue-200 bg-blue-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Calendar className="w-8 h-8 text-blue-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-blue-600">
                    {members.filter(m => m.lastCheckup !== 'Not scheduled').length}
                  </div>
                  <p className="text-sm text-gray-600">Recent Checkups</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <div className="w-8 h-8 bg-red-500 rounded-full mr-3 flex items-center justify-center">
                  <span className="text-white font-bold text-sm">!</span>
                </div>
                <div>
                  <div className="text-2xl font-bold text-red-600">
                    {members.reduce((count, m) => count + m.conditions.length, 0)}
                  </div>
                  <p className="text-sm text-gray-600">Health Conditions</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Add Member Button */}
        <div className="mb-8">
          <Button onClick={() => setShowAddForm(true)} className="bg-amber-600 hover:bg-amber-700">
            <UserPlus className="w-4 h-4 mr-2" />
            Add Family Member
          </Button>
        </div>

        {/* Members Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {members.map((member) => (
            <Card key={member.id} className="hover:shadow-lg transition-shadow border-l-4 border-l-amber-500">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="bg-amber-100 p-2 rounded-full">
                      <User className="w-6 h-6 text-amber-600" />
                    </div>
                    <div>
                      <CardTitle className="text-lg leading-tight">{member.name}</CardTitle>
                      <p className="text-sm text-gray-500">{member.relationship} • Age {member.age}</p>
                    </div>
                  </div>
                  <div className="flex space-x-1">
                    <Button variant="ghost" size="sm">
                      <Edit3 className="w-4 h-4" />
                    </Button>
                    <Button 
                      variant="ghost" 
                      size="sm"
                      onClick={() => deleteMember(member.id)}
                      className="text-red-500 hover:text-red-700"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              
              <CardContent className="space-y-4">
                {/* Health Status */}
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Health Status:</span>
                  <Badge className={getHealthStatusColor(member.healthStatus)}>
                    {member.healthStatus}
                  </Badge>
                </div>

                {/* Health Conditions */}
                <div>
                  <span className="text-sm text-gray-600 block mb-2">Conditions:</span>
                  {member.conditions.length > 0 ? (
                    <div className="flex flex-wrap gap-1">
                      {member.conditions.map((condition, index) => (
                        <Badge key={index} variant="secondary" className="text-xs">
                          {condition}
                        </Badge>
                      ))}
                    </div>
                  ) : (
                    <span className="text-sm text-gray-400">None reported</span>
                  )}
                </div>

                {/* Contact Info */}
                {member.phone && (
                  <div className="flex items-center space-x-2">
                    <Phone className="w-4 h-4 text-gray-400" />
                    <span className="text-sm text-gray-600">{member.phone}</span>
                  </div>
                )}

                {/* Last Checkup */}
                <div className="flex items-center justify-between pt-2 border-t">
                  <span className="text-sm text-gray-600">Last Checkup:</span>
                  <span className={`text-sm ${
                    member.lastCheckup === 'Not scheduled' 
                      ? 'text-red-600' 
                      : 'text-gray-900'
                  }`}>
                    {member.lastCheckup}
                  </span>
                </div>

                {/* Actions */}
                <div className="grid grid-cols-2 gap-2 pt-2">
                  <Button variant="outline" size="sm">
                    <Heart className="w-4 h-4 mr-2" />
                    Health
                  </Button>
                  <Button variant="outline" size="sm">
                    <Calendar className="w-4 h-4 mr-2" />
                    Schedule
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Add Member Modal */}
        {showAddForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <Card className="w-full max-w-md mx-4">
              <CardHeader>
                <CardTitle>Add Family Member</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
                  <Input
                    placeholder="Enter full name..."
                    value={newMember.name}
                    onChange={(e) => setNewMember({ ...newMember, name: e.target.value })}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Relationship</label>
                  <select 
                    className="w-full border border-gray-300 rounded-md px-3 py-2"
                    value={newMember.relationship}
                    onChange={(e) => setNewMember({ ...newMember, relationship: e.target.value })}
                  >
                    {relationships.map(rel => (
                      <option key={rel} value={rel}>{rel}</option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Age</label>
                  <Input
                    type="number"
                    placeholder="Age"
                    value={newMember.age}
                    onChange={(e) => setNewMember({ ...newMember, age: e.target.value })}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Phone (Optional)</label>
                  <Input
                    placeholder="(555) 123-4567"
                    value={newMember.phone}
                    onChange={(e) => setNewMember({ ...newMember, phone: e.target.value })}
                  />
                </div>
                
                <div className="flex space-x-3 pt-4">
                  <Button onClick={handleAddMember} className="bg-amber-600 hover:bg-amber-700">
                    Add Member
                  </Button>
                  <Button variant="outline" onClick={() => setShowAddForm(false)}>
                    Cancel
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default FamilyMembers;