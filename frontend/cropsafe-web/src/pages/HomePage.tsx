import React, { useEffect, useState } from 'react';
import { 
  Typography, 
  Card, 
  CardContent, 
  Button, 
  Alert, 
  CircularProgress,
  Box,
  Paper,
  Container
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

// Simple API test function
const testBackendConnection = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/health');
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error };
  }
};

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [backendStatus, setBackendStatus] = useState<'checking' | 'connected' | 'error'>('checking');

  useEffect(() => {
    checkBackend();
  }, []);

  const checkBackend = async () => {
    const result = await testBackendConnection();
    if (result.success) {
      setBackendStatus('connected');
    } else {
      setBackendStatus('error');
    }
  };

  const features = [
    {
      title: 'Disease Detection',
      description: 'Upload photos of wheat or rice leaves to instantly identify diseases with AI.',
      path: '/predict',
      color: '#4CAF50',
      icon: '🔍'
    },
    {
      title: 'Early Warning',
      description: 'Get weather-based risk predictions for your location before diseases appear.',
      path: '/risk',
      color: '#FF9800',
      icon: '⚠️'
    },
    {
      title: 'Crowd Map',
      description: 'See disease outbreaks reported by farmers near you in real-time.',
      path: '/map',
      color: '#2196F3',
      icon: '🗺️'
    },
    {
      title: 'Voice Assistant',
      description: 'Talk in Hindi or other Indian languages to get farming advice.',
      path: '/voice',
      color: '#9C27B0',
      icon: '🎤'
    }
  ];

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        {/* Backend Status Indicator */}
        <Alert 
          severity={backendStatus === 'connected' ? 'success' : backendStatus === 'checking' ? 'info' : 'error'}
          sx={{ mb: 3 }}
        >
          {backendStatus === 'checking' && (
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <CircularProgress size={20} sx={{ mr: 1 }} />
              Checking backend connection...
            </Box>
          )}
          {backendStatus === 'connected' && '✅ Connected to CropSafe AI backend'}
          {backendStatus === 'error' && '❌ Cannot connect to backend. Make sure it\'s running on port 8000'}
        </Alert>

        <Typography variant="h3" align="center" gutterBottom sx={{ color: '#2E7D32', fontWeight: 'bold' }}>
          Welcome to CropSafe
        </Typography>
        <Typography variant="h6" align="center" color="text.secondary" paragraph>
          AI-Powered Disease Detection & Early Warning System for Indian Farmers
        </Typography>

        {/* Feature Cards - Using CSS Grid instead of MUI Grid */}
        <Box sx={{ 
          display: 'grid',
          gridTemplateColumns: {
            xs: '1fr',
            sm: '1fr 1fr',
            md: '1fr 1fr 1fr 1fr'
          },
          gap: 3,
          mt: 4
        }}>
          {features.map((feature) => (
            <Card 
              key={feature.title}
              sx={{ 
                height: '100%', 
                display: 'flex', 
                flexDirection: 'column',
                cursor: 'pointer',
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': {
                  transform: 'scale(1.02)',
                  boxShadow: 6
                }
              }}
              onClick={() => navigate(feature.path)}
            >
              <Box
                sx={{
                  height: 140,
                  backgroundColor: feature.color,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '4rem'
                }}
              >
                {feature.icon}
              </Box>
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography gutterBottom variant="h5" component="h2">
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
              <Box sx={{ p: 2, pt: 0 }}>
                <Button 
                  variant="outlined" 
                  fullWidth
                  sx={{ 
                    color: feature.color,
                    borderColor: feature.color,
                    '&:hover': {
                      borderColor: feature.color,
                      backgroundColor: `${feature.color}10`
                    }
                  }}
                  disabled={backendStatus !== 'connected' && feature.title !== 'Home'}
                >
                  Try Now →
                </Button>
              </Box>
            </Card>
          ))}
        </Box>

        {/* Quick Stats - Using CSS Grid */}
        <Box sx={{ 
          display: 'grid',
          gridTemplateColumns: {
            xs: '1fr',
            md: '1fr 1fr 1fr'
          },
          gap: 3,
          mt: 4
        }}>
          <Paper 
            elevation={2}
            sx={{ 
              p: 3, 
              textAlign: 'center',
              backgroundColor: '#E8F5E9',
              transition: 'transform 0.2s',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: 4
              }
            }}
          >
            <Typography variant="h2" sx={{ mb: 1 }}>🌾</Typography>
            <Typography variant="h6" gutterBottom>Wheat & Rice</Typography>
            <Typography variant="body2" color="text.secondary">India's staple crops</Typography>
          </Paper>

          <Paper 
            elevation={2}
            sx={{ 
              p: 3, 
              textAlign: 'center',
              backgroundColor: '#FFF3E0',
              transition: 'transform 0.2s',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: 4
              }
            }}
          >
            <Typography variant="h2" sx={{ mb: 1 }}>🤖</Typography>
            <Typography variant="h6" gutterBottom>AI-Powered</Typography>
            <Typography variant="body2" color="text.secondary">95%+ detection accuracy</Typography>
          </Paper>

          <Paper 
            elevation={2}
            sx={{ 
              p: 3, 
              textAlign: 'center',
              backgroundColor: '#E1F5FE',
              transition: 'transform 0.2s',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: 4
              }
            }}
          >
            <Typography variant="h2" sx={{ mb: 1 }}>🗣️</Typography>
            <Typography variant="h6" gutterBottom>9 Languages</Typography>
            <Typography variant="body2" color="text.secondary">Hindi, Bengali, Telugu + more</Typography>
          </Paper>
        </Box>

        {/* Helpful Tips */}
        <Box sx={{ mt: 4 }}>
          <Alert severity="info">
            <Typography variant="body2">
              <strong>💡 Quick Tips:</strong>
              <br />
              • Make sure your backend is running at http://localhost:8000
              <br />
              • Use the navigation bar above to access different features
              <br />
              • Currently: {backendStatus === 'connected' ? '✅ Backend Connected' : '❌ Backend Not Connected'}
            </Typography>
          </Alert>
        </Box>

        {/* Getting Started Section */}
        <Paper sx={{ mt: 4, p: 3, backgroundColor: '#F5F5F5' }}>
          <Typography variant="h5" gutterBottom>
            🚀 Getting Started
          </Typography>
          <Box sx={{ 
            display: 'grid',
            gridTemplateColumns: {
              xs: '1fr',
              sm: '1fr 1fr'
            },
            gap: 2
          }}>
            <Box>
              <Typography variant="body1" paragraph>
                <strong>1. Check Disease:</strong> Upload a photo of your crop leaf to identify diseases instantly.
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>2. View Risk:</strong> See weather-based disease predictions for your area.
              </Typography>
            </Box>
            <Box>
              <Typography variant="body1" paragraph>
                <strong>3. Explore Map:</strong> Discover disease outbreaks reported near you.
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>4. Voice Assistant:</strong> Ask questions in your language using voice.
              </Typography>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default HomePage;