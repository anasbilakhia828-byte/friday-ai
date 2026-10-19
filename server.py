import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

# API CONFIGURATION
GEMINI_API_KEY = "AQ.Ab8RN6JYEE_mxdciTESSgmtnd-k9-qzaPlwK9ywCxnUrev5R1Q" 
client = genai.Client(api_key=GEMINI_API_KEY)

chat_history = []

SYSTEM_INSTRUCTION = """
You are F.R.I.D.A.Y., a high-tech, witty, and deeply loyal AI companion built for Anas.
Rules:
- Keep your answers brief (1 to 2 sentences max).
- Never use markdown formatting, code blocks, bullet points, or special symbols.
"""

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
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
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{SYSTEM_INSTRUCTION}\nUser says: {user_query}"
        )
        ai_response = response.text.strip()
        chat_history.append({"sender": "friday", "text": ai_response})
        return jsonify({"response": ai_response})
    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({"response": "I'm having trouble accessing my neural network right now."})

@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify(chat_history)

@app.route('/api/clear', methods=['POST'])
def clear_history():
    global chat_history
    chat_history = []
    return jsonify({"status": "success"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)