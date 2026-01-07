# 📋 COPY_PASTE_CODE_FILES.md: The Essential Codebase

Copy these contents into the respective files in your project folders.

---

## 🐍 BACKEND: `backend/app.py`

```python
import os
import time
import base64
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Optional: Azure AI Integration
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

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
    if not AZURE_KEY or not AZURE_ENDPOINT:
        return None
    return ComputerVisionClient(AZURE_ENDPOINT, CognitiveServicesCredentials(AZURE_KEY))

@app.route('/')
def home():
    return jsonify({"status": "BrainCoach AI API is operational", "azure_connected": AZURE_KEY is not None})

@app.route('/analyze', methods=['POST'])
def analyze_frame():
    data = request.json
    image_data = data.get('image')
    exercise_type = data.get('exercise', 'general')

    if not image_data:
        return jsonify({"error": "No image data"}), 400

    # Save image locally for processing
    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(image_data.split(',')[1]))

    # Mock Azure Analysis (or real if keys provided)
    client = get_azure_client()
    concentration_score = 0
    feedback = "Adjust your position"

    if client:
        try:
            # Simple placeholder for Azure Computer Vision analysis
            # In a real app, you'd send the image to analyze landmarks or objects
            concentration_score = 85 # Simulated score
            feedback = "Great focus detected!"
        except Exception as e:
            print(f"Azure Error: {e}")
            concentration_score = 70
            feedback = "Local processing fallback active"
    else:
        # Fallback to simple random score for demo purposes if Azure is not setup
        concentration_score = 75
        feedback = "Focus maintained"

    return jsonify({
        "score": concentration_score,
        "feedback": feedback,
        "timestamp": time.time()
    })

@app.route('/report', methods=['GET'])
def get_report():
    # Simple mock report data
    return jsonify({
        "total_sessions": 12,
        "avg_concentration": 82,
        "improvement_rate": "18%",
        "recent_exercises": ["Finger Yoga", "Hand Circles", "Pattern Match"]
    })

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
```

---

## 📦 BACKEND: `backend/requirements.txt`

```text
flask
flask-cors
python-dotenv
azure-cognitiveservices-vision-computervision
msrest
gunicorn
```

---

## 🔑 BACKEND: `backend/.env`

```env
AZURE_KEY=your_azure_api_key_here
AZURE_ENDPOINT=https://your-endpoint.cognitiveservices.azure.com/
PORT=5000
```

---

## 🌐 FRONTEND: `frontend/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BrainCoach AI | Smart Concentration Training</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body class="bg-dark text-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-transparent">
        <div class="container">
            <a class="navbar-brand fw-bold" href="#">🧠 BrainCoach AI</a>
        </div>
    </nav>

    <header class="hero-section text-center py-5">
        <div class="container">
            <h1 class="display-3 fw-bold mb-4">Master Your Focus with <span class="text-primary">AI</span></h1>
            <p class="lead mb-5">Azure-powered concentration training designed for the next generation.</p>
            <div class="d-flex justify-content-center gap-3">
                <a href="dashboard.html" class="btn btn-primary btn-lg px-5">Start Training</a>
                <a href="#features" class="btn btn-outline-light btn-lg px-5">View Analytics</a>
            </div>
            <div class="mt-5">
                <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80" alt="Dashboard Preview" class="img-fluid rounded-4 shadow-lg border border-secondary">
            </div>
        </div>
    </header>

    <section id="features" class="py-5">
        <div class="container">
            <div class="row g-4 text-center">
                <div class="col-md-4">
                    <div class="p-4 border border-secondary rounded-4 h-100">
                        <h3>Split-Screen UI</h3>
                        <p class="text-secondary">Simultaneous training and AI tracking feed.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="p-4 border border-secondary rounded-4 h-100">
                        <h3>Azure AI Tech</h3>
                        <p class="text-secondary">Real-time computer vision analysis.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="p-4 border border-secondary rounded-4 h-100">
                        <h3>Actionable Insights</h3>
                        <p class="text-secondary">Detailed progress reports for parents.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <footer class="py-4 text-center text-secondary">
        <p>© 2026 BrainCoach AI. Built for Microsoft Imagine Cup.</p>
    </footer>
</body>
</html>
```

---

## 🎨 FRONTEND: `frontend/style.css`

```css
:root {
    --primary-color: #0d6efd;
    --dark-bg: #0f172a;
    --card-bg: #1e293b;
}

body {
    font-family: 'Inter', sans-serif;
    background-color: var(--dark-bg);
}

.hero-section {
    padding: 100px 0;
    background: radial-gradient(circle at top center, #1e293b 0%, #0f172a 100%);
}

.rounded-4 { border-radius: 1rem !important; }

#webcam-container {
    position: relative;
    width: 100%;
    max-width: 400px;
    border-radius: 20px;
    overflow: hidden;
    border: 2px solid var(--primary-color);
}

#feedback-overlay {
    position: absolute;
    top: 20px;
    left: 20px;
    background: rgba(0,0,0,0.6);
    padding: 10px 20px;
    border-radius: 10px;
    color: white;
}
```

---

## ⚡ FRONTEND: `frontend/script.js`

```javascript
// BrainCoach AI Frontend Logic
const API_URL = "http://127.0.0.1:5000"; // Update to Render URL for production

async function analyzeHand(imageBlob) {
    try {
        const reader = new FileReader();
        reader.readAsDataURL(imageBlob);
        reader.onloadend = async () => {
            const base64data = reader.result;
            const response = await fetch(`${API_URL}/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: base64data, exercise: 'finger-yoga' })
            });
            const result = await response.json();
            updateUI(result);
        };
    } catch (err) {
        console.error("Analysis Failed:", err);
    }
}

function updateUI(data) {
    const feedbackEl = document.getElementById('ai-feedback');
    const scoreEl = document.getElementById('concentration-score');
    
    if (feedbackEl) feedbackEl.innerText = data.feedback;
    if (scoreEl) scoreEl.innerText = `${data.score}%`;
}

// Webcam integration
async function startWebcam() {
    const video = document.getElementById('webcam-feed');
    if (!video) return;
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        console.error("Webcam access denied", err);
    }
}

window.onload = startWebcam;
```
