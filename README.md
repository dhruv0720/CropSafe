# CropSafe 

CropSafe is an AI-powered application designed to detect and identify crop diseases, including specific models for Wheat and Rice crops, as well as providing disease severity analysis using deep learning models. 

## 🌾 Features
- **Crop Disease Detection:** Utilizes advanced Keras and TensorFlow deep learning models (`rice_model.h5`, `wheat_model.h5`) to analyze uploaded images of crops.
- **Disease Severity Analysis:** Evaluates the severity of the identified condition using multiple optimized severity models.
- **LLM Integration:** Built-in generative AI functionalities using Google Gemini for comprehensive insights and real-time guidance.
- **Interactive Dashboard:** A clean, responsive frontend built with React and Material UI, complete with geographic mapping (`react-leaflet`) and drag-and-drop image uploads (`react-dropzone`).

## 🛠️ Technology Stack
### Frontend
- **Framework:** React (TypeScript)
- **UI Components:** Material UI (@mui/material)
- **Mapping:** Leaflet & React-Leaflet
- **HTTP Client:** Axios

### Backend
- **Language:** Python
- **Machine Learning:** TensorFlow / Keras
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
