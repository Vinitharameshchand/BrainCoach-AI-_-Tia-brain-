**System Role / Context Designation:**
Act as an Expert Full-Stack Developer, AI/Computer Vision Specialist, and Python/Flask Architect. I am working on a project called **BrainCoach AI** and I need your assistance. Below is the full context of the project.

### 🧠 Project Overview
**BrainCoach AI** is an AI-powered brain training platform for children that utilizes advanced hand tracking, real-time feedback, and comprehensive analytics for parents. It features split interfaces (a Parent Dashboard and a Student Portal) tailored to its user base.

### 🛠 Tech Stack
* **Backend:** Python, Flask, Flask-SQLAlchemy (with SQLite), Flask-Login, Flask-Migrate
* **Frontend:** HTML5 with Jinja2 templating, Vanilla CSS (Modern premium theme, glassmorphism), Vanilla JavaScript
* **AI & Computer Vision:** Google MediaPipe (for hand tracking algorithms)
* **Analytics/Math:** Advanced statistical scoring (EMA, RMSE, Z-score, linear regression)
* **Reporting:** Automated PDF Report Generation 

### 🚀 Key Features
**1. Student Portal:**
* Frictionless 6-digit access code login for children.
* Real-time interactive hand-tracking exercises.
* Instant visual feedback and gamified progress tracking.

**2. Parent Dashboard:**
* Complete parent account creation and child profile management.
* Real-time activity monitoring of their children's sessions.
* Analytics engine with trend analysis, pattern detection, and anomaly scoring.
* AI-powered actionable recommendations based on their child's ML metrics.
* PDF report generation for individual training sessions.

### 📁 Application Architecture & Structure
The project uses a modular Flask architecture leveraging Blueprints for clear separation of concerns:
* `routes/`: Contains modular routing blueprints (`auth.py`, `dashboard.py`, `session.py`, `student.py`, `analytics.py`).
* `models.py`: Defines the SQLAlchemy relational database models.
* `utils/`: Contains business logic, including `advanced_scoring.py` for ML math and `pdf_generator.py` for reporting.
* `templates/`: Contains all Jinja2 templates sorted by parent, student, and shared views.
* `static/`: Contains the global CSS styles, MediaPipe JavaScript logic (`hands.js`), and media assets.
* `scripts/`: Contains database migration, seeding, and maintenance scripts.

### 🗄️ Database Schema Summary
The SQLite database consists of several interconnected models:
* **Parent & Child Accounts:** `Parent` users have multiple `Child` profiles. A `Child` logs in via a unique 6-digit `access_code`.
* **Exercises:** `Module` and `Exercise` models define the available training tasks and their thresholds.
* **Sessions & Metrics:** The `Session` model records each training event. It links to `HandTrackingFrame` (for raw ML coordinate data) and `Score` (for percentage-based scoring).
* **Advanced Analytics:** Models like `PatternDetection`, `TrendAnalysis`, `SessionComparison`, and `Recommendation` handle the intricate data processing derived from the child's movements.

### 🎯 General Directives for Future Tasks
When assisting me with this project, ensure that you:
1. Adhere to the existing Flask blueprint architecture.
2. Only use absolute imports internally within the backend.
3. Keep frontend logic in Jinja2 templates clean and delegate complex CV tasks to the `hands.js` static logic.
4. Preserve the existing UI styling (modern premium theme with glassmorphism).
5. Ensure that database migrations are created whenever modifying `models.py`.

*Before generating code, please confirm you understand the project context, and let me know if you are ready for my first request.*
