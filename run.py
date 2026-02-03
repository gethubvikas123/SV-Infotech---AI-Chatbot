from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize OpenAI client
client = OpenAI(
    api_key="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",  # Replace with your actual API key
    base_url="https://openrouter.ai/api/v1" # For the free model
)

# Store conversation history for context
conversation_history = []

@app.route('/')
def home():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.json
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Initialize conversation history if empty
        if not conversation_history:
            conversation_history.append({
                "role": "system",
                "content": (
                    "You are a friendly AI assistant like ChatGPT.\n"
                    "Rules:\n"
                    "- Give clean, well-spaced answers\n"
                    "- Use bullet points or tables when useful\n"
                    "- Do NOT use # symbols\n"
                    "- Keep answers clear and readable\n"
                    "- Be concise and helpful\n"
                )
            })
        
        # Add user message to history
        conversation_history.append({"role": "user", "content": user_message})
        
        # Get AI response
        response = client.chat.completions.create(
            model="tngtech/deepseek-r1t2-chimera:free",
            messages=conversation_history,
            temperature=0.7
        )
        
        ai_message = response.choices[0].message.content
        
        # Add AI response to history
        conversation_history.append({"role": "assistant", "content": ai_message})
        
        # Return response with "reply" key to match your JS
        return jsonify({"reply": ai_message})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    try:
        conversation_history.clear()
        return jsonify({"message": "History cleared"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
