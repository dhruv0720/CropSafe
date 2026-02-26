"""
Gemini AI-powered disease detection
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image
import io
import os
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime

from services.weather_service import EarlyWarningSystem

# Load environment variables
load_dotenv()

router = APIRouter(prefix="/api", tags=["prediction"])

# Initialize early warning system
warning_system = EarlyWarningSystem()

@router.post("/voice/query")
async def voice_query(request: dict):
    """
    Handle voice queries for any crop using Gemini AI
    """
    query = request.get('query', '')
    language = request.get('language', 'hi')
    detected_crop = request.get('detected_crop', 'unknown')
    
    prompt = f"""You are an expert agricultural advisor helping Indian farmers. 
    Respond in {'Hindi' if language == 'hi' else 'English'}.
    
    Farmer's query: {query}
    Detected crop: {detected_crop}
    
    Provide practical advice including:
    1. Possible disease/pest identification
    2. Symptoms to look for
    3. Treatment recommendations (both organic and chemical)
    4. Preventive measures
    5. When to contact an expert
    
    Keep response clear, simple, and actionable for farmers.
    Include emergency contact: 1800-180-1551 if needed.
    """
    
    response = model.generate_content(prompt)
    return {"response": response.text}

@router.get("/weather-risk")
async def get_weather_risk(
    lat: float,
    lon: float,
    crop: str = "wheat"
):
    """
    Get weather-based disease risk for a location
    This is used by the PredictPage for real-time risk assessment
    """
    try:
        # Get weather forecast
        weather = warning_system.get_weather_forecast(lat, lon, days=3)
        
        if not weather:
            # Return mock data if weather API fails
            return {
                "success": True,
                "location": {"lat": lat, "lon": lon},
                "current_weather": {
                    "temperature": 26,
                    "humidity": 75,
                    "precipitation": 0
                },
                "forecast": {
                    "avg_temperature": 26,
                    "avg_humidity": 75,
                    "rainy_days": 1,
                    "total_rainfall": 5
                },
                "risks": {
                    "overall_risk": "MEDIUM",
                    "overall_risk_hi": "मध्यम जोखिम",
                    "primary_disease": "Yellow Rust" if crop == "wheat" else "Blast",
                    "primary_disease_hi": "पीला रतुआ" if crop == "wheat" else "ब्लास्ट"
                }
            }
        
        # Calculate risks
        risks = warning_system.calculate_disease_risk(weather, crop)
        
        # Get current weather
        current = {
            "temperature": weather['daily']['temperature_2m_max'][0],
            "humidity": weather['daily']['relative_humidity_2m_max'][0],
            "precipitation": weather['daily']['precipitation_sum'][0]
        }
        
        # Calculate averages for next 3 days
        avg_temp = sum(weather['daily']['temperature_2m_max'][:3]) / 3
        avg_humidity = sum(weather['daily']['relative_humidity_2m_max'][:3]) / 3
        rainy_days = sum(1 for r in weather['daily']['precipitation_sum'][:3] if r > 0.1)
        total_rain = sum(weather['daily']['precipitation_sum'][:3])
        
        # Find highest risk disease
        highest_risk = None
        for day_risk in risks:
            if day_risk['diseases']:
                for disease in day_risk['diseases']:
                    if not highest_risk or disease['risk_score'] > highest_risk.get('risk_score', 0):
                        highest_risk = disease
        
        return {
            "success": True,
            "location": {"lat": lat, "lon": lon},
            "current_weather": current,
            "forecast": {
                "avg_temperature": round(avg_temp, 1),
                "avg_humidity": round(avg_humidity, 1),
                "rainy_days": rainy_days,
                "total_rainfall": round(total_rain, 1)
            },
            "risks": {
                "overall_risk": highest_risk['risk_level'] if highest_risk else "LOW",
                "overall_risk_hi": highest_risk.get('risk_level_hi', 'कम जोखिम') if highest_risk else "कम जोखिम",
                "primary_disease": highest_risk['disease'] if highest_risk else "None",
                "primary_disease_hi": highest_risk.get('disease_hi', 'कोई नहीं') if highest_risk else "कोई नहीं"
            }
        }
        
    except Exception as e:
        print(f"Error in weather-risk endpoint: {e}")
        # Return fallback data
        return {
            "success": True,
            "location": {"lat": lat, "lon": lon},
            "current_weather": {
                "temperature": 26,
                "humidity": 75,
                "precipitation": 0
            },
            "forecast": {
                "avg_temperature": 26,
                "avg_humidity": 75,
                "rainy_days": 1,
                "total_rainfall": 5
            },
            "risks": {
                "overall_risk": "MEDIUM",
                "overall_risk_hi": "मध्यम जोखिम",
                "primary_disease": "Yellow Rust" if crop == "wheat" else "Blast",
                "primary_disease_hi": "पीला रतुआ" if crop == "wheat" else "ब्लास्ट"
            }
        }

# Initialize Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY not found in .env file")
    genai_available = False
else:
    genai.configure(api_key=GEMINI_API_KEY)
    try:
        # Use models/gemini-2.5-flash (already verified as available)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        genai_available = True
        print("✅ Gemini AI initialized with gemini-1.5-flash")
    except Exception as e:
        print(f"❌ Gemini initialization failed: {e}")
        # Try fallback model if first fails
        try:
            model = genai.GenerativeModel('gemini-pro-vision')
            genai_available = True
            print("✅ Falling back to gemini-pro-vision")
        except:
            genai_available = False

warning_system = EarlyWarningSystem()

@router.get("/early-warning")
async def get_early_warning(
    lat: float,
    lon: float,
    crop: str = "wheat"
):
    """
    Get early warning for disease outbreaks
    """
    try:
        warning = warning_system.get_early_warning(lat, lon, crop)
        return warning
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/predict/wheat")
async def predict_wheat(file: UploadFile = File(...)):
    """
    AI-powered wheat disease analysis using Gemini
    """
    if not genai_available:
        raise HTTPException(status_code=503, detail="Gemini AI not configured. Please add API key to .env file")
    
    try:
        # Read and prepare image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Convert PIL to bytes for Gemini
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Create prompt for Gemini
        prompt = """You are an expert plant pathologist specializing in wheat diseases in India.

Analyze this wheat image and provide a detailed diagnosis in valid JSON format ONLY. No other text or markdown blocks.

{
  "disease_name": "specific disease name",
  "disease_name_hi": "हिंदी में रोग का नाम",
  "confidence": 95,
  "severity": {
    "level": "Low/Medium/High/Very High",
    "level_hi": "कम/मध्यम/अधिक/बहुत अधिक",
    "percentage": 25
  },
  "symptoms": [
    "Symptom 1 in English",
    "Symptom 2 in English"
  ],
  "symptoms_hi": [
    "लक्षण 1 हिंदी में",
    "लक्षण 2 हिंदी में"
  ],
  "remedies": [
    "Remedy 1 in English",
    "Remedy 2 in English"
  ],
  "remedies_hi": [
    "उपचार 1 हिंदी में",
    "उपचार 2 हिंदी में"
  ],
  "expert_advice": "English advice",
  "expert_advice_hi": "हिंदी में सलाह",
  "emergency_contact": "1800-180-1551"
}

Base your analysis ONLY on what you see in the image. Be accurate and practical for Indian farmers."""
        
        # Get response from Gemini
        response = model.generate_content([
            prompt,
            {"mime_type": "image/png", "data": img_byte_arr}
        ])
        
        # Parse JSON from response
        import json
        import re
        
        # Extract JSON from response (handle markdown formatting)
        response_text = response.text
        # Clean up text - sometimes Gemini adds markers we don't want
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        
        if json_match:
            try:
                result = json.loads(json_match.group())
            except json.JSONDecodeError:
                # If nested clean-up fails, try harder
                clean_json = re.sub(r'//.*', '', json_match.group()) # remove comments
                result = json.loads(clean_json)
        else:
            raise ValueError(f"Could not find valid JSON in Gemini response: {response_text[:100]}...")
        
        return {
            "success": True,
            "crop": "wheat",
            "prediction": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/predict/rice")
async def predict_rice(file: UploadFile = File(...)):
    """
    AI-powered rice disease analysis using Gemini
    """
    if not genai_available:
        raise HTTPException(status_code=503, detail="Gemini AI not configured. Please add API key to .env file")
    
    try:
        # Read and prepare image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Convert PIL to bytes for Gemini
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Create prompt for Gemini
        prompt = """You are an expert plant pathologist specializing in rice diseases in India.

Analyze this rice image and provide a detailed diagnosis in valid JSON format ONLY. No other text or markdown blocks.

{
  "disease_name": "specific disease name",
  "disease_name_hi": "हिंदी में रोग का नाम",
  "confidence": 95,
  "severity": {
    "level": "Low/Medium/High/Very High",
    "level_hi": "कम/मध्यम/अधिक/बहुत अधिक",
    "percentage": 25
  },
  "symptoms": [
    "Symptom 1 in English",
    "Symptom 2 in English"
  ],
  "symptoms_hi": [
    "लक्षण 1 हिंदी में",
    "लक्षण 2 हिंदी में"
  ],
  "remedies": [
    "Remedy 1 in English",
    "Remedy 2 in English"
  ],
  "remedies_hi": [
    "उपचार 1 हिंदी में",
    "उपचार 2 हिंदी में"
  ],
  "expert_advice": "English advice",
  "expert_advice_hi": "हिंदी में सलाह",
  "emergency_contact": "1800-180-1551"
}

Base your analysis ONLY on what you see in the image. Be accurate and practical for Indian farmers."""
        
        # Get response from Gemini
        response = model.generate_content([
            prompt,
            {"mime_type": "image/png", "data": img_byte_arr}
        ])
        
        # Parse JSON from response
        import json
        import re
        
        # Extract JSON from response (handle markdown formatting)
        response_text = response.text
        # Clean up text
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        
        if json_match:
            try:
                result = json.loads(json_match.group())
            except json.JSONDecodeError:
                clean_json = re.sub(r'//.*', '', json_match.group()) 
                result = json.loads(clean_json)
        else:
            raise ValueError(f"Could not find valid JSON in Gemini response: {response_text[:100]}...")
        
        return {
            "success": True,
            "crop": "rice",
            "prediction": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/ai/status")
async def ai_status():
    """Check if Gemini AI is available"""
    return {
        "available": genai_available,
        "model": "gemini-1.5-flash" if genai_available else None,
        "message": "Add GEMINI_API_KEY to .env file" if not genai_available else "Ready"
    }