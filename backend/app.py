import os
import time
import base64
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Optional: Azure AI Integration
try:
    from azure.cognitiveservices.vision.computervision import ComputerVisionClient
    from msrest.authentication import CognitiveServicesCredentials
    AZURE_SUPPORTED = True
except ImportError:
    AZURE_SUPPORTED = False

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Azure Settings
AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")

def get_azure_client():
    if not AZURE_SUPPORTED or not AZURE_KEY or not AZURE_ENDPOINT:
        return None
    return ComputerVisionClient(AZURE_ENDPOINT, CognitiveServicesCredentials(AZURE_KEY))

@app.route('/')
def home():
    return jsonify({
        "status": "BrainCoach AI API is operational", 
        "azure_connected": AZURE_KEY is not None and AZURE_SUPPORTED,
        "mode": "Production" if os.getenv("PORT") else "Development"
    })

@app.route('/analyze', methods=['POST'])
def analyze_frame():
    data = request.json
    image_data = data.get('image')
    exercise_type = data.get('exercise', 'general')

    if not image_data:
        return jsonify({"error": "No image data"}), 400

    try:
        # Save image locally for processing
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Decode base64
        header, encoded = image_data.split(",", 1)
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(encoded))

        # Mock Azure Analysis (or real if keys provided)
        client = get_azure_client()
        concentration_score = 0
        feedback = "Adjust your position"

        if client:
            try:
                # In a real app, you'd send the image to analyze landmarks or objects
                # with open(filepath, "rb") as image_stream:
                #     analysis = client.analyze_image_in_stream(image_stream, visual_features=['Description'])
                concentration_score = 85 # Simulated score
                feedback = "Great focus detected by Azure!"
            except Exception as e:
                print(f"Azure API Error: {e}")
                concentration_score = 70
                feedback = "Local processing fallback active"
        else:
            # Fallback to simple logic/random score for demo purposes
            concentration_score = 75
            feedback = "Focus maintained"

        return jsonify({
            "score": concentration_score,
            "feedback": feedback,
            "timestamp": time.time(),
            "filename": filename
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/report', methods=['GET'])
def get_report():
    return jsonify({
        "total_sessions": 12,
        "avg_concentration": 82,
        "improvement_rate": "18%",
        "recent_exercises": ["Finger Yoga", "Hand Circles", "Pattern Match"]
    })

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
