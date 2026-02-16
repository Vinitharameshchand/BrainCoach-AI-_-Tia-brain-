# BrainCoach AI – Kids Concentration Training with AI Hand Tracking

## Project Overview
BrainCoach AI is a production-ready web platform designed to help children improve their concentration through interactive hand tracking exercises. Using MediaPipe, the application tracks hand movements in real-time, compares them to target trajectories, and provides instant feedback.

## Tech Stack
- **Frontend**: HTML5, Bootstrap 5, Vanilla JS, Chart.js, Split.js, MediaPipe Hands
- **Backend**: Python Flask 2.3, SQLAlchemy ORM, Flask-Login, Flask-CORS
- **Database**: MySQL 8.0 (Compatible with SQLite for local development)
- **Reporting**: ReportLab (PDF Generation)

## Features
1. **Parent Portal**: Secure authentication and child profile management.
2. **AI Training**: Split-screen interface for guided exercises with real-time hand tracking.
3. **Scoring System**: Accuracy calculation based on Euclidean distance of hand landmarks.
4. **Analytics**: Dashboard with Chart.js showing progress and historical session data.
5. **PDF Reports**: Automated performance summaries with AI-driven recommendations.

## Setup Instructions

### 1. Prerequisities
- Python 3.9+
- MySQL 8.0 (Optional, SQLite is used by default)

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Database Initialization
```bash
python seed.py
```

### 4. Running the App
```bash
python app.py
```
The app will be available at `http://localhost:5001`.

## Deployment
- **Backend (Render)**: Deploy as a Web Service. Ensure environment variables like `SECRET_KEY` and `DATABASE_URL` are set.
- **Frontend**: Served directly by Flask in this architecture.

## AI Scoring Logic
The system normalizes the 21 landmarks provided by MediaPipe and computes the Euclidean distance against a target trajectory. Accuracy is averaged over the session and stored for analytics.
