import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure with your API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ No API key found in .env file")
    exit(1)

genai.configure(api_key=api_key)

print("📋 Available Gemini Models:")
print("=" * 50)

try:
    for model in genai.list_models():
        print(f"📌 {model.name}")
        print(f"   Supported methods: {model.supported_generation_methods}")
        print()
except Exception as e:
    print(f"❌ Error listing models: {e}")