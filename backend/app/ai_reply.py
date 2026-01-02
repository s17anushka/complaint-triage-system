# backend/app/ai_reply.py
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY missing in .env file")

client = Groq(api_key=GROQ_API_KEY)
print("✅ Groq client initialized for replies")

def generate_reply(complaint_text: str, category: str, severity: str) -> str:
    """
    Generate AI-powered draft reply using Groq (FREE & FAST)
    """
    
    prompt = f"""You are a professional customer support executive.

Complaint Details:
- Category: {category}
- Severity: {severity}

Customer Complaint:
\"\"\"{complaint_text}\"\"\"

Task: Write a polite, empathetic, and professional response email.

Guidelines:
- Be warm and understanding
- Acknowledge their concern
- Provide helpful next steps
- Keep it 2-3 short paragraphs
- Do NOT promise exact timelines
- Do NOT use placeholders like [NAME] or [TICKET_ID]
- Sound calm and helpful

Generate the response:
"""

    try:
        print(f"\n📝 Generating reply with Groq...")
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a professional customer support agent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )
        
        reply = response.choices[0].message.content.strip()
        print(f"✅ Reply generated in {response.usage.total_time:.2f}s")
        print(f"📄 Reply length: {len(reply)} chars")
        
        return reply
        
    except Exception as e:
        print(f"❌ Groq reply error: {str(e)}")
        import traceback
        traceback.print_exc()
        return get_fallback_reply(category)


def get_fallback_reply(category: str) -> str:
    """Fallback response if AI fails"""
    print("⚠️  Using fallback reply")
    return f"""Thank you for contacting us regarding your {category} concern.

We sincerely apologize for any inconvenience this may have caused. Our team is currently reviewing your case and will work to resolve this matter as quickly as possible.

We appreciate your patience and will keep you updated on the progress."""