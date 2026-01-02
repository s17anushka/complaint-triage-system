# backend/app/agent.py
import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY missing in .env file")


client = Groq(api_key=GROQ_API_KEY)
print("✅ Groq client initialized")

def ai_agent(text: str) -> dict:
    """
    Analyze complaint using Groq (FREE & SUPER FAST)
    """
    
    prompt = f"""Analyze this customer complaint and return ONLY a valid JSON object.

Required format:
{{
  "category": "technical",
  "priority": "high",
  "summary": "Brief one-line summary",
  "sentiment": "frustrated"
}}

Rules:
- category: technical, billing, service, product, or other
- priority: high, medium, or low
- sentiment: angry, frustrated, neutral, or satisfied
- Return ONLY JSON, no markdown, no explanations

Complaint:
\"\"\"{text}\"\"\"
"""

    try:
        print(f"\n📝 Analyzing with Groq: {text[:50]}...")
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a complaint analysis assistant. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500,
            response_format={"type": "json_object"}  # Forces JSON response
        )
        
        response_text = response.choices[0].message.content.strip()
        print(f"✅ Got response from Groq in {response.usage.total_time:.2f}s")
        
        
        analysis = json.loads(response_text)
        
        
        required_fields = ['category', 'priority', 'summary', 'sentiment']
        if not all(key in analysis for key in required_fields):
            print(f"⚠️  Missing fields: {analysis}")
            raise ValueError("Missing required fields")
        
        print(f"✅ Analysis: {analysis}")
        return analysis
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return get_fallback_response()
        
    except Exception as e:
        print(f"❌ Groq error: {str(e)}")
        import traceback
        traceback.print_exc()
        return get_fallback_response()


def get_fallback_response() -> dict:
    """Fallback response if AI fails"""
    print("⚠️  Using fallback response")
    return {
        "category": "other",
        "priority": "medium",
        "summary": "Complaint received and under review",
        "sentiment": "neutral"
    }