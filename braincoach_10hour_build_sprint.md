# 🏃‍♂️ Main Guide: BrainCoach AI 10-Hour Build Sprint

This guide is your step-by-step instruction manual for building BrainCoach AI from scratch to submission.

## 🏁 PHASE 0: Setup (30 Minutes)
*Goal: Prepare your development environment and Azure services.*

1. **Azure Setup:**
   - Go to [Azure Portal](https://portal.azure.com).
   - Create a **Computer Vision** resource (Free F0 tier).
   - Save your **Key 1** and **Endpoint** to a `.env` file in the `backend/` folder.

2. **Project Folders:**
   ```bash
   mkdir backend frontend uploads
   touch backend/.env
   ```

3. **Install Dependencies:**
   ```bash
   cd backend
   pip install flask flask-cors flask-sqlalchemy azure-cognitiveservices-vision-computervision python-dotenv
   ```

---

## ⚙️ PHASE 1: Backend (90 Minutes)
*Goal: Set up the Flask API to process images and handle tracking data.*

1. **Main App (`backend/app.py`):**
   - Copy the code from `COPY_PASTE_CODE_FILES.md`.
   - The backend handles image uploads from the frontend, sends them to Azure AI (or uses local MediaPipe fallback), and returns concentration scores.

2. **Database:**
   - We use SQLite for the local MVP to keep it fast. The code automatically creates `braincoach.db`.

3. **Test the API:**
   ```bash
   python app.py
   # Go to http://127.0.0.1:5000/ - you should see "BrainCoach API Running"
   ```

---

## 🎨 PHASE 2: Frontend (90 Minutes)
*Goal: Create the split-screen training interface.*

1. **Landing Page (`frontend/index.html`):**
   - Modern, high-premium design using Bootstrap 5 and custom CSS.
   - Hero section with a "Start Training" button.

2. **Training Dashboard (`frontend/dashboard.html`):**
   - The heart of the app.
   - Left Side: The "Game" area (Finger Yoga, Patterns).
   - Right Side: Real-time hand tracking webcam feed.

3. **Hand Tracking Logic (`frontend/script.js`):**
   - Uses MediaPipe Hands for instant local feedback.
   - Periodically sends snapshots to the backend for Azure AI deep analysis.

---

## 🚀 PHASE 3: Deploy (30 Minutes)
*Goal: Make your app public for the judges.*

1. **Backend (Render):**
   - Push your code to GitHub.
   - Connect GitHub to [Render.com](https://render.com).
   - Select "Web Service" -> Python environment.

2. **Frontend (Netlify):**
   - Drop the `frontend` folder into [Netlify](https://netlify.com).
   - Update `script.js` with your Render API URL.

---

## 🎬 PHASE 4: Videos (4 Hours)
*Goal: Create the Demo and Pitch videos.*

**1. Demo Video (3-5 min):**
- **0:00-0:30:** The Problem (Kids losing focus).
- **0:30-1:30:** Showing the Training Interface.
- **1:30-2:30:** Real-time AI Tracking in action.
- **2:30-3:00:** The Dashboard/Analytics for parents.

**2. Pitch Video (3-5 min):**
- **0:00-1:00:** Personal Story & Opportunity.
- **1:00-3:00:** Business Model (B2B with schools, B2C via TIA Brain).
- **3:00-5:00:** Vision for the future.

---

## 📊 PHASE 5: Pitch Deck (90 Minutes)
*Goal: Create the 14-slide PDF.*

**The Winning Slide Order:**
1. Title (BrainCoach AI)
2. The Problem (200M kids need this)
3. The Solution (AI tracking + Brain games)
4. Demo Screenshots
5. Tech Stack (Azure AI Core)
6. Customer Validation (50 kids, 18% improvement)
7. Market Size (TAM/SAM/SOM)
8. Business Model
9. Competition (How we are better)
10. Marketing Strategy
11. Roadmap (Next 12 months)
12. The Team (Vinitha + Mentors)
13. Financials (Basic projections)
14. Call to Action/Thank You

---

## ✅ PHASE 6: Submit (30 Minutes)
*Goal: Double-check and hit Send.*

1. **GitHub:** README is polished, code is clean.
2. **URLs:** Live Demo is working on Netlify.
3. **Materials:** MP4s and PDF are under size limits.
4. **Portal:** Fill out the description on [Imagine Cup Portal](https://imaginecup.microsoft.com).

---

**YOU ARE DONE! 🎉 GO CELEBRATE!**
