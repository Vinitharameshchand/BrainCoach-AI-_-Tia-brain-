# ✅ Quick Lookup: BrainCoach AI Checklist

Use this document for rapid troubleshooting and command copy-pasting.

## 💻 Terminal Commands (Copy-Paste)

### **Backend Setup**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### **Deployment (Render/Netlify)**
- **Render Build Command:** `pip install -r requirements.txt`
- **Render Start Command:** `gunicorn app:app`
- **Netlify API URL:** In `script.js`, change `http://127.0.0.1:5000` to your Render `.onrender.com` URL.

---

## 📅 Phase Summaries
- **Phase 0:** Azure keys, Folder structure, Venv setup.
- **Phase 1:** Backend API running, Local analysis working.
- **Phase 2:** Frontend split-screen, Real-time camera feed.
- **Phase 3:** Public URLs for Backend and Frontend.
- **Phase 4:** Recorded Demo (.mp4) and Pitch (.mp4).
- **Phase 5:** PDF Pitch Deck (14 slides).
- **Phase 6:** Submission portal complete.

---

## 🔍 Verification Checklist
- [ ] Backend returns `{"status": "..."}` at the root URL.
- [ ] Frontend webcam feed shows up on `dashboard.html`.
- [ ] AI feedback updates when you perform an exercise.
- [ ] Parent dashboard shows at least 3 mock sessions.
- [ ] Videos are audible and under 5 minutes each.
- [ ] Pitch deck saved as PDF.

---

## 🆘 Common Issues + Fixes

**"Webcam not starting"**
- Check browser permissions (top left of address bar).
- Ensure you are using `https://` (Live Server or Netlify).

**"CORS Error on Analysis"**
- Ensure `flask-cors` is installed and `CORS(app)` is in `app.py`.
- Double-check the `API_URL` in `script.js`.

**"Azure API Key Invalid"**
- Check `.env` format: `AZURE_KEY=123...` (no spaces).
- Ensure your endpoint ends with `/`.

---

**WINNING TIP:** Focus on the **Demo Video**. If the live app has a small bug, explain it in the video as "Planned Improvement". The judges care about your VISION and the CORE AI value.
