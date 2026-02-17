# 🧠 BrainCoach AI - Brain Training Platform

An AI-powered brain training platform for children with advanced hand tracking, real-time feedback, and comprehensive analytics for parents.

## 📁 Project Structure

```
braincoach-ai/
│
├── app.py                      # Application entry point
├── config.py                   # Configuration settings
├── models.py                   # Database models
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
│
├── routes/                     # Route blueprints
│   ├── auth.py                # Authentication
│   ├── dashboard.py           # Parent dashboard
│   ├── session.py             # Training sessions
│   ├── student.py             # Student portal
│   └── analytics.py           # Analytics API
│
├── utils/                      # Utility modules
│   ├── advanced_scoring.py    # ML algorithms
│   └── pdf_generator.py       # Report generation
│
├── templates/                  # Jinja2 templates
├── static/                     # CSS, JS, images
├── migrations/                 # Database migrations
├── scripts/                    # Utility scripts
├── tests/                      # Test files
├── docs/                       # Documentation
├── instance/                   # Database & instance files
└── reports/                    # Generated reports
```

## 🚀 Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run application
python app.py

# 4. Open browser
http://localhost:5001
```

## 📖 Documentation

See `docs/` folder for detailed documentation:
- **Quick Start**: `docs/QUICK_START.md`
- **Student System**: `docs/STUDENT_SYSTEM.md`
- **Integration Guide**: `docs/PARENT_STUDENT_INTEGRATION.md`
- **UI Theme**: `docs/UI_IMPROVEMENTS.md`

## ✨ Features

**For Students:**
- Simple 6-digit access code login
- Interactive hand-tracking exercises
- Real-time feedback
- Progress tracking

**For Parents:**
- Create & manage child accounts
- Real-time activity monitoring
- Detailed analytics
- AI-powered recommendations

**🎓 Made with ❤️ for better brain training**
