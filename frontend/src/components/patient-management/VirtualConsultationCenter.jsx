import React, { useState, useEffect, useRef, useCallback } from 'react';
import { 
  Video, 
  VideoOff, 
  Mic, 
  MicOff, 
  Phone, 
  PhoneOff, 
  Monitor, 
  MonitorOff,
  MessageCircle,
  Send,
  Settings,
  Users,
  Clock,
  Calendar,
  Play,
  Square,
  Download,
  AlertCircle,
  CheckCircle,
  Wifi,
  WifiOff,
  Camera,
  CameraOff,
  Volume2,
  VolumeX
} from 'lucide-react';
import SmartNavigation from '../shared/SmartNavigation';

const VirtualConsultationCenter = () => {
  // WebRTC and Media States
  const [localVideo, setLocalVideo] = useState(null);
  const [remoteVideo, setRemoteVideo] = useState(null);
  const [localStream, setLocalStream] = useState(null);
  const [remoteStream, setRemoteStream] = useState(null);
  const [peerConnection, setPeerConnection] = useState(null);
  const [isVideoEnabled, setIsVideoEnabled] = useState(true);
  const [isAudioEnabled, setIsAudioEnabled] = useState(true);
  const [isScreenSharing, setIsScreenSharing] = useState(false);
  
  // Session States
  const [currentSession, setCurrentSession] = useState(null);
  const [isInCall, setIsInCall] = useState(false);
  const [callDuration, setCallDuration] = useState(0);
  const [connectionQuality, setConnectionQuality] = useState('good');
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  
  // Recording States
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [recordedChunks, setRecordedChunks] = useState([]);
  const [recordings, setRecordings] = useState([]);
  
  // Chat States
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [webSocket, setWebSocket] = useState(null);
  
  // Appointment States
  const [appointments, setAppointments] = useState([]);
  const [showScheduler, setShowScheduler] = useState(false);
  const [newAppointment, setNewAppointment] = useState({
    patient_id: 'patient-456',
    provider_id: 'provider-123',
    scheduled_time: '',
    session_type: 'video',
    notes: ''
  });
  
  // UI States
  const [activeTab, setActiveTab] = useState('consultation');
  const [showSettings, setShowSettings] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [notifications, setNotifications] = useState([]);
  
  // Refs
  const localVideoRef = useRef(null);
  const remoteVideoRef = useRef(null);
  const chatMessagesRef = useRef(null);
  
  // WebRTC Configuration
  const rtcConfiguration = {
    iceServers: [
      { urls: 'stun:stun.l.google.com:19302' },
      { urls: 'stun:stun1.l.google.com:19302' }
    ]
  };

  // ===== WEBRTC FUNCTIONS =====
  
  const initializeWebRTC = useCallback(async () => {
    try {
      const pc = new RTCPeerConnection(rtcConfiguration);
      
      // Handle remote stream
      pc.ontrack = (event) => {
        console.log('Received remote track:', event);
        setRemoteStream(event.streams[0]);
        if (remoteVideoRef.current) {
          remoteVideoRef.current.srcObject = event.streams[0];
        }
      };
      
      // Handle ICE candidates
      pc.onicecandidate = (event) => {
        if (event.candidate && webSocket) {
          webSocket.send(JSON.stringify({
            type: 'ice_candidate',
            candidate: event.candidate,
            sender_type: 'provider'
          }));
        }
      };
      
      // Monitor connection state
      pc.onconnectionstatechange = () => {
        console.log('Connection state:', pc.connectionState);
        setConnectionStatus(pc.connectionState);
        
        if (pc.connectionState === 'connected') {
          setConnectionStatus('connected');
          startConnectionQualityMonitoring(pc);
        } else if (pc.connectionState === 'disconnected' || pc.connectionState === 'failed') {
          setConnectionStatus('disconnected');
          setConnectionQuality('poor');
        }
      };
      
      setPeerConnection(pc);
      return pc;
    } catch (error) {
      console.error('Error initializing WebRTC:', error);
      setError('Failed to initialize video call');
      return null;
    }
  }, [webSocket]);
  
  const startLocalVideo = async () => {
    try {
      setLoading(true);
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
      });
      
      setLocalStream(stream);
      if (localVideoRef.current) {
        localVideoRef.current.srcObject = stream;
      }
      
      // Add stream to peer connection
      if (peerConnection) {
        stream.getTracks().forEach(track => {
          peerConnection.addTrack(track, stream);
        });
      }
      
      addNotification('Camera and microphone access granted', 'success');
    } catch (error) {
      console.error('Error accessing media devices:', error);
      setError('Could not access camera or microphone');
      addNotification('Failed to access camera/microphone', 'error');
    } finally {
      setLoading(false);
    }
  };
  
  const toggleVideo = () => {
    if (localStream) {
      const videoTrack = localStream.getVideoTracks()[0];
      if (videoTrack) {
        videoTrack.enabled = !videoTrack.enabled;
        setIsVideoEnabled(videoTrack.enabled);
        addNotification(videoTrack.enabled ? 'Camera turned on' : 'Camera turned off', 'info');
      }
    }
  };
  
  const toggleAudio = () => {
    if (localStream) {
      const audioTrack = localStream.getAudioTracks()[0];
      if (audioTrack) {
        audioTrack.enabled = !audioTrack.enabled;
        setIsAudioEnabled(audioTrack.enabled);
        addNotification(audioTrack.enabled ? 'Microphone turned on' : 'Microphone turned off', 'info');
      }
    }
  };
  
  const startScreenShare = async () => {
    try {
      const screenStream = await navigator.mediaDevices.getDisplayMedia({
        video: true,
        audio: false
      });
      
      // Replace video track with screen share
      if (peerConnection && localStream) {
        const videoTrack = localStream.getVideoTracks()[0];
        const screenTrack = screenStream.getVideoTracks()[0];
        
        const sender = peerConnection.getSenders().find(s => 
          s.track && s.track.kind === 'video'
        );
        
        if (sender) {
          await sender.replaceTrack(screenTrack);
        }
        
        // Update local video display
        if (localVideoRef.current) {
          localVideoRef.current.srcObject = screenStream;
        }
        
        setIsScreenSharing(true);
        addNotification('Screen sharing started', 'success');
        
        // Handle screen share end
        screenTrack.onended = () => {
          stopScreenShare();
        };
      }
    } catch (error) {
      console.error('Error starting screen share:', error);
      setError('Could not start screen sharing');
    }
  };
  
  const stopScreenShare = async () => {
    try {
      if (peerConnection && localStream) {
        const videoTrack = localStream.getVideoTracks()[0];
        
        const sender = peerConnection.getSenders().find(s => 
          s.track && s.track.kind === 'video'
        );
        
        if (sender && videoTrack) {
          await sender.replaceTrack(videoTrack);
        }
        
        // Restore local video display
        if (localVideoRef.current) {
          localVideoRef.current.srcObject = localStream;
        }
        
        setIsScreenSharing(false);
        addNotification('Screen sharing stopped', 'info');
      }
    } catch (error) {
      console.error('Error stopping screen share:', error);
    }
  };
  
  // ===== CONNECTION QUALITY MONITORING =====
  
  const startConnectionQualityMonitoring = (pc) => {
    const interval = setInterval(async () => {
      try {
        const stats = await pc.getStats();
        let bytesReceived = 0;
        let bytesSent = 0;
        let packetsLost = 0;
        
        stats.forEach(report => {
          if (report.type === 'inbound-rtp' && report.kind === 'video') {
            bytesReceived = report.bytesReceived || 0;
            packetsLost = report.packetsLost || 0;
          }
          if (report.type === 'outbound-rtp' && report.kind === 'video') {
            bytesSent = report.bytesSent || 0;
          }
        });
        
        // Simple quality calculation
        const quality = packetsLost < 10 ? 'good' : packetsLost < 50 ? 'fair' : 'poor';
        setConnectionQuality(quality);
        
      } catch (error) {
        console.error('Error getting connection stats:', error);
      }
    }, 5000); // Check every 5 seconds
    
    // Clean up interval when call ends
    setTimeout(() => clearInterval(interval), 300000); // Stop after 5 minutes max
  };
  
  // ===== SESSION RECORDING =====
  
  const startRecording = async () => {
    try {
      if (!localStream) {
        setError('No active stream to record');
        return;
      }
      
      const options = { mimeType: 'video/webm;codecs=vp9' };
      const recorder = new MediaRecorder(localStream, options);
      const chunks = [];
      
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunks.push(event.data);
        }
      };
      
      recorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'video/webm' });
        const url = URL.createObjectURL(blob);
        const newRecording = {
          id: Date.now().toString(),
          url,
          name: `Session_${new Date().toISOString().split('T')[0]}_${Date.now()}`,
          size: blob.size,
          duration: callDuration,
          timestamp: new Date().toISOString()
        };
        
        setRecordings(prev => [...prev, newRecording]);
        setRecordedChunks([]);
        addNotification('Recording saved successfully', 'success');
      };
      
      recorder.start();
      setMediaRecorder(recorder);
      setIsRecording(true);
      addNotification('Recording started', 'success');
      
    } catch (error) {
      console.error('Error starting recording:', error);
      setError('Could not start recording');
    }
  };
  
  const stopRecording = () => {
    if (mediaRecorder && isRecording) {
      mediaRecorder.stop();
      setIsRecording(false);
      setMediaRecorder(null);
      addNotification('Recording stopped', 'info');
    }
  };
  
  const downloadRecording = (recording) => {
    const a = document.createElement('a');
    a.href = recording.url;
    a.download = `${recording.name}.webm`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    addNotification(`Downloaded ${recording.name}`, 'success');
  };
  
  // ===== WEBSOCKET CHAT =====
  
  const initializeWebSocket = (sessionId) => {
    try {
      const ws = new WebSocket(`ws://localhost:8001/ws/consultation/${sessionId}/provider-123`);
      
      ws.onopen = () => {
        console.log('WebSocket connected');
        setConnectionStatus('connected');
        addNotification('Connected to consultation', 'success');
      };
      
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          if (data.type === 'chat_message') {
            setMessages(prev => [...prev, {
              ...data.data,
              timestamp: new Date(data.timestamp)
            }]);
          } else if (data.type === 'webrtc_offer') {
            handleWebRTCOffer(data.offer);
          } else if (data.type === 'webrtc_answer') {
            handleWebRTCAnswer(data.answer);
          } else if (data.type === 'ice_candidate') {
            handleICECandidate(data.candidate);
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };
      
      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setConnectionStatus('disconnected');
        addNotification('Disconnected from consultation', 'error');
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setError('Connection error occurred');
      };
      
      setWebSocket(ws);
    } catch (error) {
      console.error('Error initializing WebSocket:', error);
      setError('Could not connect to consultation');
    }
  };
  
  const sendMessage = () => {
    if (newMessage.trim() && webSocket) {
      const message = {
        message: newMessage,
        sender_type: 'provider'
      };
      
      webSocket.send(JSON.stringify(message));
      setNewMessage('');
    }
  };
  
  // ===== WEBRTC SIGNALING =====
  
  const handleWebRTCOffer = async (offer) => {
    try {
      if (peerConnection) {
        await peerConnection.setRemoteDescription(offer);
        const answer = await peerConnection.createAnswer();
        await peerConnection.setLocalDescription(answer);
        
        if (webSocket) {
          webSocket.send(JSON.stringify({
            type: 'webrtc_answer',
            answer: answer,
            sender_type: 'provider'
          }));
        }
      }
    } catch (error) {
      console.error('Error handling WebRTC offer:', error);
    }
  };
  
  const handleWebRTCAnswer = async (answer) => {
    try {
      if (peerConnection) {
        await peerConnection.setRemoteDescription(answer);
      }
    } catch (error) {
      console.error('Error handling WebRTC answer:', error);
    }
  };
  
  const handleICECandidate = async (candidate) => {
    try {
      if (peerConnection) {
        await peerConnection.addIceCandidate(candidate);
      }
    } catch (error) {
      console.error('Error handling ICE candidate:', error);
    }
  };
  
  const createOffer = async () => {
    try {
      if (peerConnection) {
        const offer = await peerConnection.createOffer();
        await peerConnection.setLocalDescription(offer);
        
        if (webSocket) {
          webSocket.send(JSON.stringify({
            type: 'webrtc_offer',
            offer: offer,
            sender_type: 'provider'
          }));
        }
      }
    } catch (error) {
      console.error('Error creating offer:', error);
    }
  };
  
  // ===== SESSION MANAGEMENT =====
  
  const startConsultation = async (sessionId = null) => {
    try {
      setLoading(true);
      
      let session;
      if (sessionId) {
        // Join existing session
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/virtual-consultation/join/${sessionId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_id: 'provider-123',
            user_type: 'provider'
          })
        });
        session = await response.json();
      } else {
        // Create new session
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/virtual-consultation/sessions`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newAppointment)
        });
        session = await response.json();
      }
      
      setCurrentSession(session);
      setIsInCall(true);
      
      // Initialize WebSocket and WebRTC
      const sessionIdToUse = sessionId || session.session_id;
      initializeWebSocket(sessionIdToUse);
      
      const pc = await initializeWebRTC();
      if (pc) {
        await startLocalVideo();
      }
      
      // Start call duration timer
      const startTime = Date.now();
      const timer = setInterval(() => {
        setCallDuration(Math.floor((Date.now() - startTime) / 1000));
      }, 1000);
      
      // Store timer for cleanup
      window.callTimer = timer;
      
      addNotification('Consultation started', 'success');
      
    } catch (error) {
      console.error('Error starting consultation:', error);
      setError('Failed to start consultation');
    } finally {
      setLoading(false);
    }
  };
  
  const endConsultation = async () => {
    try {
      setLoading(true);
      
      // Stop recording if active
      if (isRecording) {
        stopRecording();
      }
      
      // Stop local media
      if (localStream) {
        localStream.getTracks().forEach(track => track.stop());
        setLocalStream(null);
      }
      
      // Close peer connection
      if (peerConnection) {
        peerConnection.close();
        setPeerConnection(null);
      }
      
      // Close WebSocket
      if (webSocket) {
        webSocket.close();
        setWebSocket(null);
      }
      
      // Clear timer
      if (window.callTimer) {
        clearInterval(window.callTimer);
        window.callTimer = null;
      }
      
      // End session on backend
      if (currentSession?.session_id) {
        await fetch(`${process.env.REACT_APP_BACKEND_URL}/virtual-consultation/end/${currentSession.session_id}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            notes: `Call duration: ${formatDuration(callDuration)}`,
            connection_quality: connectionQuality
          })
        });
      }
      
      // Reset states
      setIsInCall(false);
      setCurrentSession(null);
      setCallDuration(0);
      setConnectionStatus('disconnected');
      setMessages([]);
      setIsVideoEnabled(true);
      setIsAudioEnabled(true);
      setIsScreenSharing(false);
      
      addNotification('Consultation ended', 'info');
      
    } catch (error) {
      console.error('Error ending consultation:', error);
      setError('Error ending consultation');
    } finally {
      setLoading(false);
    }
  };
  
  // ===== APPOINTMENT SCHEDULING =====
  
  const scheduleAppointment = async () => {
    try {
      setLoading(true);
      
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/virtual-consultation/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newAppointment)
      });
      
      if (response.ok) {
        const appointment = await response.json();
        setAppointments(prev => [...prev, appointment]);
        setNewAppointment({
          patient_id: 'patient-456',
          provider_id: 'provider-123',
          scheduled_time: '',
          session_type: 'video',
          notes: ''
        });
        setShowScheduler(false);
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
  
  const loadAppointments = async () => {
    try {
      // This would typically load from a backend endpoint
      // For now, we'll simulate with the current session
      const mockAppointments = [];
      if (currentSession) {
        mockAppointments.push(currentSession);
      }
      setAppointments(mockAppointments);
    } catch (error) {
      console.error('Error loading appointments:', error);
    }
  };
  
  // ===== UTILITY FUNCTIONS =====
  
  const formatDuration = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  };
  
  const addNotification = (message, type) => {
    const notification = {
      id: Date.now(),
      message,
      type,
      timestamp: new Date()
    };
    setNotifications(prev => [...prev, notification]);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== notification.id));
    }, 5000);
  };
  
  const getConnectionStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return 'text-emerald-600';
      case 'connecting': return 'text-yellow-600';
      case 'disconnected': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };
  
  const getQualityColor = () => {
    switch (connectionQuality) {
      case 'good': return 'text-emerald-600';
      case 'fair': return 'text-yellow-600';
      case 'poor': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };
  
  // ===== EFFECTS =====
  
  useEffect(() => {
    loadAppointments();
    
    // Cleanup on unmount
    return () => {
      if (localStream) {
        localStream.getTracks().forEach(track => track.stop());
      }
      if (peerConnection) {
        peerConnection.close();
      }
      if (webSocket) {
        webSocket.close();
      }
      if (window.callTimer) {
        clearInterval(window.callTimer);
      }
    };
  }, []);
  
  useEffect(() => {
    if (chatMessagesRef.current) {
      chatMessagesRef.current.scrollTop = chatMessagesRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="min-h-screen bg-gray-50">
      <SmartNavigation />
      
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Virtual Consultation Center</h1>
              <p className="text-gray-600 mt-2">WebRTC-powered video consultations with screen sharing and recording</p>
            </div>
            
            {/* Connection Status */}
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full ${connectionStatus === 'connected' ? 'bg-emerald-500' : connectionStatus === 'connecting' ? 'bg-yellow-500' : 'bg-red-500'}`} />
                <span className={`text-sm font-medium ${getConnectionStatusColor()}`}>
                  {connectionStatus.charAt(0).toUpperCase() + connectionStatus.slice(1)}
                </span>
              </div>
              
              {connectionStatus === 'connected' && (
                <div className="flex items-center space-x-2">
                  <Wifi className={`w-4 h-4 ${getQualityColor()}`} />
                  <span className={`text-sm ${getQualityColor()}`}>
                    {connectionQuality.charAt(0).toUpperCase() + connectionQuality.slice(1)}
                  </span>
                </div>
              )}
              
              {isInCall && (
                <div className="flex items-center space-x-2">
                  <Clock className="w-4 h-4 text-gray-500" />
                  <span className="text-sm text-gray-600">{formatDuration(callDuration)}</span>
                </div>
              )}
            </div>
          </div>
          
          {/* Tab Navigation */}
          <div className="flex space-x-1 mt-6">
            {[
              { id: 'consultation', label: 'Video Call', icon: Video },
              { id: 'appointments', label: 'Appointments', icon: Calendar },
              { id: 'recordings', label: 'Recordings', icon: Play },
              { id: 'settings', label: 'Settings', icon: Settings }
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
        {activeTab === 'consultation' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Video Area */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-gray-900">Video Consultation</h2>
                  {!isInCall ? (
                    <button
                      onClick={() => startConsultation()}
                      disabled={loading}
                      className="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 disabled:opacity-50 flex items-center space-x-2"
                    >
                      <Video className="w-4 h-4" />
                      <span>{loading ? 'Starting...' : 'Start Consultation'}</span>
                    </button>
                  ) : (
                    <button
                      onClick={endConsultation}
                      disabled={loading}
                      className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 disabled:opacity-50 flex items-center space-x-2"
                    >
                      <PhoneOff className="w-4 h-4" />
                      <span>{loading ? 'Ending...' : 'End Call'}</span>
                    </button>
                  )}
                </div>

                {/* Video Containers */}
                <div className="space-y-4">
                  {/* Remote Video */}
                  <div className="relative bg-gray-900 rounded-lg overflow-hidden" style={{ height: '400px' }}>
                    <video
                      ref={remoteVideoRef}
                      autoPlay
                      playsInline
                      className="w-full h-full object-cover"
                    />
                    {!remoteStream && (
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="text-center text-white">
                          <Users className="w-16 h-16 mx-auto mb-4 opacity-50" />
                          <p className="text-lg font-medium">Waiting for participant...</p>
                        </div>
                      </div>
                    )}
                    
                    {/* Local Video (Picture-in-Picture) */}
                    <div className="absolute bottom-4 right-4 w-48 h-36 bg-gray-800 rounded-lg overflow-hidden border-2 border-white">
                      <video
                        ref={localVideoRef}
                        autoPlay
                        playsInline
                        muted
                        className="w-full h-full object-cover"
                      />
                      {!localStream && (
                        <div className="absolute inset-0 flex items-center justify-center">
                          <CameraOff className="w-8 h-8 text-white opacity-50" />
                        </div>
                      )}
                    </div>
                    
                    {/* Recording Indicator */}
                    {isRecording && (
                      <div className="absolute top-4 left-4 bg-red-600 text-white px-3 py-1 rounded-full text-sm font-medium flex items-center space-x-2">
                        <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
                        <span>REC</span>
                      </div>
                    )}
                  </div>

                  {/* Control Panel */}
                  {isInCall && (
                    <div className="flex items-center justify-center space-x-4 p-4 bg-gray-100 rounded-lg">
                      {/* Video Toggle */}
                      <button
                        onClick={toggleVideo}
                        className={`p-3 rounded-full ${isVideoEnabled ? 'bg-emerald-600 text-white' : 'bg-red-600 text-white'}`}
                      >
                        {isVideoEnabled ? <Video className="w-5 h-5" /> : <VideoOff className="w-5 h-5" />}
                      </button>

                      {/* Audio Toggle */}
                      <button
                        onClick={toggleAudio}
                        className={`p-3 rounded-full ${isAudioEnabled ? 'bg-emerald-600 text-white' : 'bg-red-600 text-white'}`}
                      >
                        {isAudioEnabled ? <Mic className="w-5 h-5" /> : <MicOff className="w-5 h-5" />}
                      </button>

                      {/* Screen Share Toggle */}
                      <button
                        onClick={isScreenSharing ? stopScreenShare : startScreenShare}
                        className={`p-3 rounded-full ${isScreenSharing ? 'bg-blue-600 text-white' : 'bg-gray-600 text-white'}`}
                      >
                        {isScreenSharing ? <MonitorOff className="w-5 h-5" /> : <Monitor className="w-5 h-5" />}
                      </button>

                      {/* Recording Toggle */}
                      <button
                        onClick={isRecording ? stopRecording : startRecording}
                        className={`p-3 rounded-full ${isRecording ? 'bg-red-600 text-white' : 'bg-gray-600 text-white'}`}
                      >
                        {isRecording ? <Square className="w-5 h-5" /> : <Play className="w-5 h-5" />}
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Chat Panel */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 h-full">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <MessageCircle className="w-5 h-5 mr-2" />
                  Chat
                </h3>

                {/* Messages */}
                <div
                  ref={chatMessagesRef}
                  className="h-80 overflow-y-auto mb-4 p-3 bg-gray-50 rounded-lg"
                >
                  {messages.length === 0 ? (
                    <p className="text-gray-500 text-center py-8">No messages yet</p>
                  ) : (
                    <div className="space-y-3">
                      {messages.map((message, index) => (
                        <div
                          key={index}
                          className={`flex ${message.sender_type === 'provider' ? 'justify-end' : 'justify-start'}`}
                        >
                          <div
                            className={`max-w-xs px-3 py-2 rounded-lg text-sm ${
                              message.sender_type === 'provider'
                                ? 'bg-emerald-600 text-white'
                                : 'bg-white border border-gray-200'
                            }`}
                          >
                            <p>{message.message}</p>
                            <p className={`text-xs mt-1 ${
                              message.sender_type === 'provider' ? 'text-emerald-100' : 'text-gray-500'
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
                    disabled={!isInCall}
                  />
                  <button
                    onClick={sendMessage}
                    disabled={!newMessage.trim() || !isInCall}
                    className="bg-emerald-600 text-white p-2 rounded-lg hover:bg-emerald-700 disabled:opacity-50"
                  >
                    <Send className="w-4 h-4" />
                  </button>
                </div>
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
                onClick={() => setShowScheduler(!showScheduler)}
                className="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 flex items-center space-x-2"
              >
                <Calendar className="w-4 h-4" />
                <span>Schedule New</span>
              </button>
            </div>

            {/* Scheduler Form */}
            {showScheduler && (
              <div className="bg-gray-50 rounded-lg p-6 mb-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Schedule New Appointment</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Patient ID</label>
                    <input
                      type="text"
                      value={newAppointment.patient_id}
                      onChange={(e) => setNewAppointment(prev => ({ ...prev, patient_id: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Session Type</label>
                    <select
                      value={newAppointment.session_type}
                      onChange={(e) => setNewAppointment(prev => ({ ...prev, session_type: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                    >
                      <option value="video">Video Call</option>
                      <option value="audio">Audio Only</option>
                      <option value="text">Text Chat</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Scheduled Time</label>
                    <input
                      type="datetime-local"
                      value={newAppointment.scheduled_time}
                      onChange={(e) => setNewAppointment(prev => ({ ...prev, scheduled_time: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Notes</label>
                    <input
                      type="text"
                      value={newAppointment.notes}
                      onChange={(e) => setNewAppointment(prev => ({ ...prev, notes: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
                      placeholder="Optional notes..."
                    />
                  </div>
                </div>
                <div className="flex space-x-3 mt-4">
                  <button
                    onClick={scheduleAppointment}
                    disabled={!newAppointment.scheduled_time || loading}
                    className="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 disabled:opacity-50"
                  >
                    {loading ? 'Scheduling...' : 'Schedule'}
                  </button>
                  <button
                    onClick={() => setShowScheduler(false)}
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
                </div>
              ) : (
                appointments.map((appointment, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-medium text-gray-900">
                          Patient: {appointment.patient_id}
                        </h4>
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
                          <button
                            onClick={() => startConsultation(appointment.session_id)}
                            className="bg-emerald-600 text-white px-3 py-1 rounded text-sm hover:bg-emerald-700"
                          >
                            Start
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {/* Recordings Tab */}
        {activeTab === 'recordings' && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Session Recordings</h2>
            
            <div className="space-y-4">
              {recordings.length === 0 ? (
                <div className="text-center py-12">
                  <Play className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">No recordings available</p>
                  <p className="text-sm text-gray-500 mt-2">
                    Recordings will appear here after you record a consultation session
                  </p>
                </div>
              ) : (
                recordings.map((recording) => (
                  <div key={recording.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-medium text-gray-900">{recording.name}</h4>
                        <p className="text-sm text-gray-600">
                          Duration: {formatDuration(recording.duration)} | 
                          Size: {(recording.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                        <p className="text-sm text-gray-500">
                          Recorded: {new Date(recording.timestamp).toLocaleString()}
                        </p>
                      </div>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => downloadRecording(recording)}
                          className="bg-emerald-600 text-white px-3 py-1 rounded text-sm hover:bg-emerald-700 flex items-center space-x-1"
                        >
                          <Download className="w-3 h-3" />
                          <span>Download</span>
                        </button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {/* Settings Tab */}
        {activeTab === 'settings' && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Settings</h2>
            
            <div className="space-y-6">
              {/* Video Settings */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-3">Video Settings</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <label className="text-sm font-medium text-gray-700">Auto-start camera</label>
                    <input type="checkbox" defaultChecked className="rounded" />
                  </div>
                  <div className="flex items-center justify-between">
                    <label className="text-sm font-medium text-gray-700">Auto-start microphone</label>
                    <input type="checkbox" defaultChecked className="rounded" />
                  </div>
                  <div className="flex items-center justify-between">
                    <label className="text-sm font-medium text-gray-700">HD video quality</label>
                    <input type="checkbox" defaultChecked className="rounded" />
                  </div>
                </div>
              </div>

              {/* Recording Settings */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-3">Recording Settings</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <label className="text-sm font-medium text-gray-700">Auto-record sessions</label>
                    <input type="checkbox" className="rounded" />
                  </div>
                  <div className="flex items-center justify-between">
                    <label className="text-sm font-medium text-gray-700">Include audio in recordings</label>
                    <input type="checkbox" defaultChecked className="rounded" />
                  </div>
                </div>
              </div>

              {/* Notification Settings */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-3">Notifications</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <label className="text-sm font-medium text-gray-700">Connection status alerts</label>
                    <input type="checkbox" defaultChecked className="rounded" />
                  </div>
                  <div className="flex items-center justify-between">
                    <label className="text-sm font-medium text-gray-700">Chat message sounds</label>
                    <input type="checkbox" defaultChecked className="rounded" />
                  </div>
                  <div className="flex items-center justify-between">
                    <label className="text-sm font-medium text-gray-700">Appointment reminders</label>
                    <input type="checkbox" defaultChecked className="rounded" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default VirtualConsultationCenter;