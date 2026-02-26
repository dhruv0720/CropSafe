import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

try:
    print("Attempting to initialize models/gemini-2.5-flash...")
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    print("Success! (Initialization only)")
    
    print("Attempting to generate tiny text...")
    response = model.generate_content("Hi, reply with 'Ready' if you are working.")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
