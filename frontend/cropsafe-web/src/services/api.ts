import axios from 'axios';

// Base URL for your backend API
const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Test function to check backend connection
export const testBackendConnection = async () => {
  try {
    const response = await api.get('/api/health');
    console.log('✅ Backend connected:', response.data);
    return { success: true, data: response.data };
  } catch (error) {
    console.error('❌ Backend connection failed:', error);
    return { success: false, error };
  }
};

// Get disease risk for a location
export const getDiseaseRisk = async (lat: number, lon: number, crop: string = 'wheat') => {
  try {
    const response = await api.get('/api/risk', {
      params: { lat, lon, crop }
    });
    return { success: true, data: response.data };
  } catch (error) {
    console.error('❌ Failed to get risk data:', error);
    return { success: false, error };
  }
};

// Upload image for disease prediction
export const predictDisease = async (file: File, crop: string = 'wheat') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('crop', crop);

  try {
    const response = await api.post('/api/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return { success: true, data: response.data };
  } catch (error) {
    console.error('❌ Prediction failed:', error);
    return { success: false, error };
  }
};

export default api;