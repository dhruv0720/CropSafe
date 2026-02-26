"""
Main FastAPI application for CropSafe with Gemini AI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

# Import routes
from api.prediction_routes import router as prediction_router

# Initialize FastAPI
app = FastAPI(
    title="CropSafe API",
    description="AI-Powered Crop Disease Detection System",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(prediction_router)

# Health check endpoints
@app.get("/")
async def root():
    return {
        "message": "🌾 CropSafe AI API is running",
        "version": "2.0.0",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok", 
        "service": "CropSafe AI Backend",
        "ai_model": "Gemini 1.5 Flash",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/test")
async def test():
    return {"message": "API is working", "ai_ready": True}

if __name__ == "__main__":
    print("=" * 50)
    print("🌾 CropSafe AI Backend Starting...")
    print("=" * 50)
    print("\n📡 Available endpoints:")
    print("  - GET  /")
    print("  - GET  /api/health")
    print("  - GET  /api/test")
    print("  - GET  /api/ai/status")
    print("  - POST /api/predict/wheat")
    print("  - POST /api/predict/rice")
    print("\n🚀 Server starting at http://localhost:8000")
    print("=" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=8000,
        reload=True
    )