import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, Button, Box, ThemeProvider, createTheme } from '@mui/material';

// Import pages
import HomePage from './pages/HomePage';
import PredictPage from './pages/PredictPage';
import EarlyWarningPage from './pages/EarlyWarningPage';
import VoicePage from './pages/VoicePage';  // Make sure this import is correct
// import MapPage from './pages/MapPage';

// Create theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#2E7D32',
    },
    secondary: {
      main: '#FF9800',
    },
  },
});

// Simple placeholder for pages we haven't created yet
const ComingSoonPage = ({ title }: { title: string }) => (
  <Box sx={{ mt: 4, textAlign: 'center' }}>
    <Typography variant="h3" gutterBottom>
      🚧
    </Typography>
    <Typography variant="h4" gutterBottom sx={{ color: '#2E7D32' }}>
      {title}
    </Typography>
    <Typography variant="body1" color="text.secondary" sx={{ mt: 2 }}>
      This feature is coming soon! We're working hard to bring you the best crop disease detection experience.
    </Typography>
    <Button 
      variant="contained" 
      sx={{ mt: 4 }}
      component={Link}
      to="/"
    >
      Back to Home
    </Button>
  </Box>
);

function App() {
  const [language, setLanguage] = useState('en');
  const isHindi = language === 'hi';

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static" color="primary">
            <Toolbar>
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                🌾 CropSafe
              </Typography>
              <Button color="inherit" component={Link} to="/">
                {isHindi ? 'होम' : 'Home'}
              </Button>
              <Button color="inherit" component={Link} to="/predict">
                {isHindi ? 'रोग पहचान' : 'Detect Disease'}
              </Button>
              <Button color="inherit" component={Link} to="/early-warning">
                {isHindi ? 'पूर्व चेतावनी' : 'Early Warning'}
              </Button>
              <Button color="inherit" component={Link} to="/map">
                {isHindi ? 'रोग मानचित्र' : 'Disease Map'}
              </Button>
              <Button color="inherit" component={Link} to="/voice">
                {isHindi ? 'आवाज सहायता' : 'Voice Assistant'}
              </Button>
              
              {/* Language Toggle */}
              <Button 
                color="inherit" 
                onClick={() => setLanguage(isHindi ? 'en' : 'hi')}
                size="small"
                sx={{ ml: 2, border: '1px solid rgba(255,255,255,0.3)' }}
              >
                {isHindi ? '🇬🇧 English' : '🇮🇳 हिन्दी'}
              </Button>
            </Toolbar>
          </AppBar>

          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/predict" element={<PredictPage />} />
              <Route path="/early-warning" element={<EarlyWarningPage />} />
              <Route path="/map" element={<ComingSoonPage title="Disease Map" />} />
              <Route path="/voice" element={<VoicePage />} />  {/* This should now show your real VoicePage */}
            </Routes>
          </Container>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;