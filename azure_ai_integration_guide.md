# 🤖 Azure AI Integration Guide: BrainCoach AI

This guide covers how BrainCoach AI leverages Azure Cognitive Services to provide high-level concentration analysis.

## 🛠️ Azure Setup (10 Minutes)
1. **Create Resource:**
   - Search for **Computer Vision** in the Azure Portal.
   - Select the Free (F0) tier if available, otherwise Standard (S1).
2. **Retrieve Keys:**
   - Go to **Keys and Endpoint** in the resource menu.
   - Key 1: `COPY_THIS`
   - Endpoint: `https://YOUR_NAME.cognitiveservices.azure.com/`

---

## 💻 Code Implementation

### **Backend Integration (`app.py`)**
We use the `azure-cognitiveservices-vision-computervision` SDK.

```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# Initialize Client
client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# Example: Analysis of Hand Gestures / Body Language
def analyze_attention(image_stream):
    analysis = client.analyze_image_in_stream(image_stream, visual_features=['Description', 'Objects'])
    # logic to parse objects and determine focus
    return "Focused" if "child" in analysis.description.tags else "Distracted"
```

---

## 🧪 Testing Instructions
1. Put your Azure Key and Endpoint into the `.env` file.
2. Restart the Flask server.
3. Open the Dashboard and perform an exercise.
4. Check the Flask console for logs: `Azure Analysis Success: ...`

---

## 💰 Pricing Info (Free Tier)
- **Computer Vision (F0):** 5,000 transactions per month.
- **Cost for this project:** $0.
- **Why it matters:** Judges love to see "Azure AI CORE" used efficiently at scale.

---

**PRO TIP:** If the API feels slow, use **MediaPipe (Local)** for the 30fps frames (instant feedback) and **Azure AI** for one "Deep Check" every 5 seconds. This creates a smooth experience while leveraging cloud power.
