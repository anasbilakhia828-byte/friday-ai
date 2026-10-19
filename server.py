import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Safely get key from Render Environment Variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY is missing from environment variables!")

chat_history = []

SYSTEM_INSTRUCTION = """
You are F.R.I.D.A.Y., a high-tech, witty, and deeply loyal AI companion built for Anas.
Rules:
Keep your answers brief (1 to 2 sentences max).
Never use markdown formatting, code blocks, bullet points, or special symbols.
"""

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    user_query = data.get('prompt', '').lower().strip()
    
    if not user_query:
        return jsonify({"error": "No prompt provided"}), 400
    
    # Custom greeting rule
    if user_query in ["hi", "hello", "hello friday", "hi friday"]:
        ai_response = "Hello Anas, how are you?"
        chat_history.append({"sender": "user", "text": user_query})
        chat_history.append({"sender": "friday", "text": ai_response})
        return jsonify({"response": ai_response})
    
    chat_history.append({"sender": "user", "text": user_query})
    
    try:
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=SYSTEM_INSTRUCTION
        )
        response = model.generate_content(user_query)
        ai_response = response.text.strip()
        
        chat_history.append({"sender": "friday", "text": ai_response})
        return jsonify({"response": ai_response})
        
    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({"response": "I'm having trouble accessing my neural network right now."}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify(chat_history)

@app.route('/api/clear', methods=['POST'])
def clear_history():
    global chat_history
    chat_history = []
    return jsonify({"status": "success"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)