
import google.generativeai as genai

genai.configure(api_key="AIzaSyDrS6I5qjWivYeiKjPt0kt-Rf1QU7oS7vU")

model = genai.GenerativeModel("gemini-2.5-flash")

def get_ai_reply(message: str) -> str:
    try:
        prompt = f"""
You are an expert AI assistant. Answer the user's question clearly, in plain English, and in a well-organized and paragraph-based format.
Avoid using markdown symbols like asterisks (*) or hashtags (#). Do not use bullet points unless the user specifically asks.
Be concise, yet informative and professional.

User's message:
{message}
"""

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.85,
                top_k=40,
            )
        )
        if response.text:
            return response.text.strip()
        else:
            return "The AI could not generate a response."
    except Exception as e:
        return f"Error: {str(e)}"
