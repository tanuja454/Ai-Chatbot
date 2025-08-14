from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Chat API route
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "Please enter a message."}), 400

        # Call Ollama with the smaller llama3.2:1b model
        result = subprocess.run(
            ["ollama", "run", "llama3.2:1b", user_message],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return jsonify({"response": f"Error: {result.stderr}"}), 500

        bot_reply = result.stdout.strip()
        return jsonify({"response": bot_reply})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500


if __name__ == '__main__':
    # Run Flask on 0.0.0.0 so it’s accessible publicly
    app.run(host='0.0.0.0', port=8080, debug=True)

