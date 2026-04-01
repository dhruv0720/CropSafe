# CropSafe 

CropSafe is an integrated web platform designed to help Indian farmers detect diseases in wheat and rice crops early and receive weather-based early warnings. It combines AI-powered disease detection, real-time severity assessment, and a weather-based early warning system with a bilingual (English/Hindi) voice assistant for accessibility.

The system uses Google Gemini AI for intelligent disease analysis from uploaded or captured images, and the Open-Meteo API for 7‑day weather forecasts. A Web Speech API voice assistant allows low‑literacy farmers to interact naturally in Hindi.

## 🌾 Features
- **Crop Disease Detection:** Upload or capture crop images; Gemini AI identifies diseases with confidence scores and severity assessment (Low/Medium/High/Very High)
- **Early warning system:** Fetches real‑time weather data based on location; calculates 7‑day disease risk using temperature, humidity, and rainfall thresholds; displays color‑coded alerts.
- **Voice Assistant:** Hindi/English speech recognition and synthesis; farmers can ask questions and receive spoken advice.
- **Bilingual Interface:** Switch seamlessly between English and Hindi.

## 🛠️ Technology Stack
### Frontend
- **Framework:** React (TypeScript)
- **UI Components:** Material UI (@mui/material)
- **Mapping:** Leaflet & React-Leaflet
- **HTTP Client:** Axios

### Backend
- **Framework:** FastAPI
- **Language:** Python
- **ASGI server:** Uvicorn
- **Image processing:** Pillow, OpenCV
- **AI Integration:** Google Gemini API 

## 🚀 Getting Started

### Prerequisites
- Node.js (for the frontend)
- Python 3.8+ (for the backend)
- Google Gemini API Key 

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the backend server (ensure API keys are set in `.env` if required):
   ```bash
   python main.py
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend/cropsafe-web
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the React development server:
   ```bash
   npm start
   ```

## 📂 Project Structure
- `/backend`: Contains the Python API, deep learning models (`.h5`, `.keras`), data analysis scripts, and Gemini integration logic.
- `/frontend/cropsafe-web`: Contains the React project for the user interface.
- `/models`: Supplemental model data and training histories.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
