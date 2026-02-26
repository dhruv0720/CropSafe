import React, { useState, useCallback, useEffect, useRef } from 'react';
import {
  Typography,
  Paper,
  Box,
  Button,
  Card,
  CardContent,
  CardMedia,
  LinearProgress,
  Alert,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import ImageIcon from '@mui/icons-material/Image';
import TranslateIcon from '@mui/icons-material/Translate';
import AgricultureIcon from '@mui/icons-material/Agriculture';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import CloseIcon from '@mui/icons-material/Close';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Language options
const languages = [
  { code: 'en', name: 'English', flag: '🇬🇧' },
  { code: 'hi', name: 'हिन्दी', flag: '🇮🇳' },
];

const PredictPage: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [cropType, setCropType] = useState<'wheat' | 'rice'>('wheat');
  const [language, setLanguage] = useState('hi');
  const [weatherData, setWeatherData] = useState<any>(null);
  const [location, setLocation] = useState<{lat: number, lon: number} | null>(null);
  
  // Camera states
  const [cameraOpen, setCameraOpen] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);

  // Get user's location and fetch weather
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const coords = {
            lat: position.coords.latitude,
            lon: position.coords.longitude
          };
          setLocation(coords);
          fetchWeatherRisk(coords.lat, coords.lon, cropType);
        },
        (error) => {
          console.log("Location error:", error);
          const defaultCoords = { lat: 28.6139, lon: 77.2090 };
          setLocation(defaultCoords);
          fetchWeatherRisk(defaultCoords.lat, defaultCoords.lon, cropType);
        }
      );
    } else {
      const defaultCoords = { lat: 28.6139, lon: 77.2090 };
      setLocation(defaultCoords);
      fetchWeatherRisk(defaultCoords.lat, defaultCoords.lon, cropType);
    }
  }, [cropType]);

  // Cleanup camera stream
  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [stream]);

  const fetchWeatherRisk = async (lat: number, lon: number, crop: string) => {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/weather-risk?lat=${lat}&lon=${lon}&crop=${crop}`
      );
      setWeatherData(response.data);
      console.log("Weather data:", response.data);
    } catch (error) {
      console.error("Failed to fetch weather:", error);
    }
  };

  // Handle file upload (existing)
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setSelectedFile(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    maxFiles: 1
  });

  // Camera functions
  const openCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment' } // Use back camera on phones
      });
      setStream(mediaStream);
      setCameraOpen(true);
      
      // Wait for video to load
      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
          videoRef.current.play();
        }
      }, 100);
    } catch (err) {
      console.error('Camera error:', err);
      alert(isHindi 
        ? 'कैमरा एक्सेस नहीं हो सका। कृपया अनुमति दें।' 
        : 'Could not access camera. Please grant permission.');
    }
  };

  const closeCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    setCameraOpen(false);
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      
      // Set canvas dimensions to match video
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      // Draw video frame to canvas
      const context = canvas.getContext('2d');
      if (context) {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Convert canvas to file
        canvas.toBlob((blob) => {
          if (blob) {
            const file = new File([blob], `camera_capture_${Date.now()}.jpg`, { 
              type: 'image/jpeg' 
            });
            setSelectedFile(file);
            setPreview(URL.createObjectURL(blob));
            setResult(null);
            setError(null);
            closeCamera();
          }
        }, 'image/jpeg', 0.9);
      }
    }
  };

  const handlePredict = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const endpoint = cropType === 'wheat' ? '/api/predict/wheat' : '/api/predict/rice';
      console.log(`Sending request to: ${API_BASE_URL}${endpoint}`);
      
      const response = await axios.post(`${API_BASE_URL}${endpoint}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 60000,
      });
      
      console.log('Response:', response.data);
      
      if (response.data.success) {
        setResult(response.data.prediction);
      } else {
        setError('Failed to analyze image');
      }
    } catch (err) {
      console.error('Error:', err);
      if (axios.isAxiosError(err)) {
        if (err.code === 'ECONNABORTED') {
          setError('Request timeout. Please try a smaller image or try again.');
        } else {
          setError(`Error: ${err.response?.data?.detail || err.message}`);
        }
      } else {
        setError('Failed to predict disease. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const containerStyle = {
    display: 'flex',
    gap: '24px',
    marginTop: '24px',
    flexDirection: { xs: 'column', md: 'row' } as const
  };

  const columnStyle = {
    flex: 1,
    minWidth: 0
  };

  const isHindi = language === 'hi';

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ color: '#2E7D32', fontWeight: 'bold' }}>
        🌾 {isHindi ? 'फसल रोग पहचान - कैमरा सहायता' : 'Crop Disease Detection - Camera Support'}
      </Typography>

      {/* Language Selector */}
      <Paper sx={{ p: 2, mb: 3, display: 'flex', alignItems: 'center', gap: 2, flexWrap: 'wrap' }}>
        <TranslateIcon color="primary" />
        <FormControl component="fieldset">
          <RadioGroup
            row
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
          >
            {languages.map(lang => (
              <FormControlLabel
                key={lang.code}
                value={lang.code}
                control={<Radio />}
                label={`${lang.flag} ${lang.name}`}
              />
            ))}
          </RadioGroup>
        </FormControl>
      </Paper>
      
      {/* Location Info */}
      {location && (
        <Alert severity="info" sx={{ mb: 2 }}>
          📍 {isHindi ? 'आपका स्थान' : 'Your location'}: {location.lat.toFixed(2)}°N, {location.lon.toFixed(2)}°E
        </Alert>
      )}
      
      {/* Two-column layout */}
      <Box sx={containerStyle}>
        {/* Left column - Upload */}
        <Box sx={columnStyle}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <AgricultureIcon /> 
              {isHindi ? 'फसल की फोटो अपलोड करें' : 'Upload Crop Image'}
            </Typography>
            
            {/* Crop selector */}
            <Box sx={{ mb: 3, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              <Button
                variant={cropType === 'wheat' ? 'contained' : 'outlined'}
                onClick={() => setCropType('wheat')}
              >
                🌾 {isHindi ? 'गेहूं' : 'Wheat'}
              </Button>
              <Button
                variant={cropType === 'rice' ? 'contained' : 'outlined'}
                onClick={() => setCropType('rice')}
              >
                🌾 {isHindi ? 'चावल' : 'Rice'}
              </Button>
            </Box>
            
            {/* Upload options */}
            <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
              <Button
                variant="contained"
                startIcon={<CloudUploadIcon />}
                onClick={() => document.getElementById('file-upload')?.click()}
                sx={{ flex: 1 }}
              >
                {isHindi ? 'फोटो चुनें' : 'Choose Photo'}
              </Button>
              <Button
                variant="contained"
                startIcon={<CameraAltIcon />}
                onClick={openCamera}
                sx={{ flex: 1, bgcolor: '#9C27B0' }}
              >
                {isHindi ? 'कैमरा' : 'Camera'}
              </Button>
              <input
                id="file-upload"
                type="file"
                accept="image/*"
                style={{ display: 'none' }}
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) {
                    setSelectedFile(file);
                    setPreview(URL.createObjectURL(file));
                    setResult(null);
                    setError(null);
                  }
                }}
              />
            </Box>
            
            {/* Dropzone */}
            <Box
              {...getRootProps()}
              sx={{
                border: '2px dashed #ccc',
                borderRadius: 2,
                p: 4,
                textAlign: 'center',
                cursor: 'pointer',
                backgroundColor: isDragActive ? '#f0f0f0' : 'transparent',
                '&:hover': {
                  backgroundColor: '#f5f5f5'
                }
              }}
            >
              <input {...getInputProps()} />
              <CloudUploadIcon sx={{ fontSize: 48, color: '#2E7D32', mb: 2 }} />
              {isDragActive ? (
                <Typography>{isHindi ? 'फोटो यहां छोड़ें' : 'Drop the image here...'}</Typography>
              ) : (
                <Typography>
                  {isHindi 
                    ? 'या फोटो यहां खींचकर छोड़ें' 
                    : 'Or drag & drop an image here'}
                </Typography>
              )}
            </Box>

            {/* Preview */}
            {preview && (
              <Box sx={{ mt: 3 }}>
                <Typography variant="subtitle2" gutterBottom>
                  {isHindi ? 'चुनी गई फोटो:' : 'Selected Image:'}
                </Typography>
                <Card>
                  <CardMedia
                    component="img"
                    image={preview}
                    alt="Preview"
                    sx={{ maxHeight: 200, objectFit: 'contain' }}
                  />
                  <CardContent>
                    <Typography variant="body2">
                      {selectedFile?.name || 'Camera photo'}
                      {selectedFile?.size ? ` (${(selectedFile.size / 1024 / 1024).toFixed(2)} MB)` : ''}
                    </Typography>
                  </CardContent>
                </Card>
              </Box>
            )}

            {/* Predict button */}
            {selectedFile && (
              <Button
                variant="contained"
                fullWidth
                size="large"
                onClick={handlePredict}
                disabled={loading}
                sx={{ mt: 3 }}
              >
                {loading 
                  ? (isHindi ? 'विश्लेषण हो रहा है...' : 'Analyzing...')
                  : (isHindi ? 'रोग की पहचान करें' : 'Detect Disease')
                }
              </Button>
            )}

            {error && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {error}
              </Alert>
            )}
          </Paper>
        </Box>

        {/* Right column - Results */}
        <Box sx={columnStyle}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              {isHindi ? 'परिणाम' : 'Detection Results'}
            </Typography>
            
            {loading && (
              <Box sx={{ width: '100%', mt: 4, textAlign: 'center' }}>
                <LinearProgress />
                <Typography variant="body2" sx={{ mt: 2 }}>
                  {isHindi ? 'AI फोटो का विश्लेषण कर रहा है...' : 'AI is analyzing your image...'}
                </Typography>
              </Box>
            )}

            {!loading && !result && (
              <Box sx={{ textAlign: 'center', py: 8, color: 'text.secondary' }}>
                <ImageIcon sx={{ fontSize: 60, mb: 2, opacity: 0.3 }} />
                <Typography>
                  {isHindi 
                    ? 'परिणाम देखने के लिए फोटो अपलोड करें या कैमरे से फोटो लें' 
                    : 'Upload an image or take a photo to see results'}
                </Typography>
              </Box>
            )}

            {result && !loading && (
              <Box>
                {/* Disease Name */}
                <Card sx={{ 
                  bgcolor: result.severity?.level === 'Low' ? '#8BC34A20' : 
                            result.severity?.level === 'Medium' ? '#FFC10720' : 
                            result.severity?.level === 'High' ? '#FF980020' : '#F4433620',
                  borderLeft: `6px solid ${result.severity?.color || '#9E9E9E'}`,
                  mb: 3
                }}>
                  <CardContent>
                    <Typography variant="overline" color="text.secondary">
                      {isHindi ? 'रोग का नाम' : 'Disease Name'}
                    </Typography>
                    <Typography variant="h4" sx={{ color: '#2E7D32', fontWeight: 'bold' }}>
                      {isHindi ? result.disease_name_hi : result.disease_name}
                    </Typography>
                    
                    {/* Confidence */}
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="body2" sx={{ mb: 0.5 }}>
                        {isHindi ? 'विश्वसनीयता' : 'Confidence'}: {result.confidence}%
                      </Typography>
                      <LinearProgress
                        variant="determinate"
                        value={result.confidence}
                        sx={{
                          height: 10,
                          borderRadius: 5,
                          bgcolor: '#e0e0e0',
                          '& .MuiLinearProgress-bar': {
                            bgcolor: result.confidence > 80 ? '#4CAF50' : 
                                    result.confidence > 60 ? '#FFC107' : '#F44336'
                          }
                        }}
                      />
                    </Box>

                    {/* Severity */}
                    {result.severity && (
                      <Chip
                        label={isHindi 
                          ? `गंभीरता: ${result.severity.level_hi} (${result.severity.percentage}%)`
                          : `Severity: ${result.severity.level} (${result.severity.percentage}%)`
                        }
                        sx={{
                          mt: 2,
                          bgcolor: result.severity.color,
                          color: 'white',
                          fontWeight: 'bold'
                        }}
                      />
                    )}
                  </CardContent>
                </Card>

                {/* Symptoms */}
                <Accordion defaultExpanded>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography variant="subtitle1" fontWeight="bold">
                      {isHindi ? '🔍 लक्षण' : '🔍 Symptoms'}
                    </Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Box component="ul" sx={{ pl: 2, m: 0 }}>
                      {(isHindi ? result.symptoms_hi : result.symptoms)?.map((symptom: string, idx: number) => (
                        <Typography component="li" key={idx} variant="body1" sx={{ mb: 1 }}>
                          {symptom}
                        </Typography>
                      ))}
                    </Box>
                  </AccordionDetails>
                </Accordion>

                {/* Remedies */}
                <Accordion defaultExpanded>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography variant="subtitle1" fontWeight="bold">
                      {isHindi ? '💊 उपचार' : '💊 Remedies'}
                    </Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Box component="ul" sx={{ pl: 2, m: 0 }}>
                      {(isHindi ? result.remedies_hi : result.remedies)?.map((remedy: string, idx: number) => (
                        <Typography component="li" key={idx} variant="body1" sx={{ mb: 1 }}>
                          {remedy}
                        </Typography>
                      ))}
                    </Box>
                  </AccordionDetails>
                </Accordion>

                {/* Expert Advice */}
                <Alert severity="info" sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    {isHindi ? '👨‍🌾 विशेषज्ञ सलाह' : '👨‍🌾 Expert Advice'}
                  </Typography>
                  <Typography variant="body2">
                    {isHindi ? result.expert_advice_hi : result.expert_advice}
                  </Typography>
                  {result.emergency_contact && (
                    <Typography variant="body2" sx={{ mt: 1, fontWeight: 'bold' }}>
                      📞 {result.emergency_contact}
                    </Typography>
                  )}
                </Alert>
              </Box>
            )}
          </Paper>
        </Box>
      </Box>

      {/* Camera Dialog */}
      <Dialog
        open={cameraOpen}
        onClose={closeCamera}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h6">
              {isHindi ? '📸 फोटो लें' : '📸 Take Photo'}
            </Typography>
            <IconButton onClick={closeCamera}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
          <Box sx={{ position: 'relative', width: '100%', pt: '56.25%' /* 16:9 aspect ratio */ }}>
            <video
              ref={videoRef}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                borderRadius: '8px'
              }}
              autoPlay
              playsInline
            />
          </Box>
          <canvas ref={canvasRef} style={{ display: 'none' }} />
        </DialogContent>
        <DialogActions sx={{ justifyContent: 'center', pb: 3 }}>
          <Button
            variant="contained"
            color="primary"
            size="large"
            startIcon={<CameraAltIcon />}
            onClick={capturePhoto}
            sx={{ minWidth: 200 }}
          >
            {isHindi ? 'फोटो लें' : 'Capture'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Help Section */}
      <Paper sx={{ mt: 3, p: 2, bgcolor: '#FFF3E0' }}>
        <Typography variant="body2" color="text.secondary" align="center">
          {isHindi 
            ? '🇮🇳 कैमरे से फोटो लें या गैलरी से फोटो चुनें। नियमित फसल निगरानी करें। आपात स्थिति: 1800-180-1551'
            : '🇮🇳 Take photo with camera or choose from gallery. Monitor crops regularly. Emergency: 1800-180-1551'}
        </Typography>
      </Paper>
    </Box>
  );
};

export default PredictPage;