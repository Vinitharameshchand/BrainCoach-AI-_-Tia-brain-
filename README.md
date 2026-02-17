# 🧠 BrainCoach AI - Children's Concentration Training Platform

A premium, AI-powered web application designed to help children improve their concentration and focus through interactive hand-tracking exercises using MediaPipe technology.

## ✨ Features

### For Parents
- 👨‍👩‍👧‍👦 **Multi-Child Management** - Track progress for multiple children
- 📊 **Real-Time Analytics** - View live focus scores and improvement trends
- 📈 **Progress Tracking** - Detailed charts showing concentration improvement over time
- 🏆 **Gamification** - Unlockable badges and level system to motivate children
- 📄 **PDF Reports** - Downloadable session reports for each training session

### For Children
- 🎮 **Interactive Training** - Fun, game-like hand-tracking exercises
- 🎯 **Real-Time Feedback** - Live accuracy meter with visual and audio cues
- ⭐ **Rewards System** - Earn badges and level up with consistent practice
- 🎨 **Child-Friendly UI** - Colorful, engaging interface designed for kids

### Technical Features
- 🤖 **AI Hand Tracking** - Powered by Google MediaPipe
- 🔒 **Secure Authentication** - Flask-Login with password hashing
- 💾 **Database Persistence** - SQLAlchemy ORM with SQLite/MySQL support
- 📱 **Responsive Design** - Works on desktop and tablet devices
- 🎵 **Audio Feedback** - Success and encouragement sounds using Howler.js

## 🚀 Quick Start

### Prerequisites
- Python 3.14+ (or Python 3.10+)
- pip (Python package manager)
- Modern web browser with webcam access

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd BrainCoach-AI-_-Tia-brain-
```

2. **Create and activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize the database**
```bash
source venv/bin/activate
python seed.py
```

5. **Run the application**
```bash
python app.py
```

6. **Access the application**
Open your browser and navigate to: `http://localhost:5001`

## 📁 Project Structure

```
BrainCoach-AI/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── seed.py               # Database seeding script
│
├── routes/               # Route blueprints
│   ├── auth.py          # Authentication routes
│   ├── dashboard.py     # Dashboard routes
│   └── session.py       # Training session routes
│
├── static/              # Static assets
│   ├── css/
│   │   └── style.css    # Premium design system
│   └── js/
│       ├── hands.js     # MediaPipe integration
│       └── scoring.js   # Accuracy scoring system
│
├── templates/           # Jinja2 templates
│   ├── base.html       # Base template
│   ├── login.html      # Login page
│   ├── register.html   # Registration page
│   ├── dashboard.html  # Parent dashboard
│   └── session.html    # Training session interface
│
├── utils/              # Utility modules
│   └── pdf_generator.py # PDF report generation
│
└── reports/            # Generated PDF reports
```

## 🎨 Design System

### Color Palette
- **Primary Blue**: `#3b82f6` - Trust and focus
- **Secondary Green**: `#10b981` - Growth and success
- **Accent Gold**: `#f59e0b` - Achievement
- **Background**: `#f8fafc` - Clean and calm

### Typography
- **Font Family**: 'Outfit' (Google Fonts)
- **Weights**: 300 (Light), 400 (Regular), 600 (Semi-Bold), 700 (Bold)

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///braincoach.db
DEBUG=True
```

### Database Configuration
The application supports both SQLite (development) and MySQL (production):

**SQLite (Default)**:
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///braincoach.db'
```

**MySQL**:
```python
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/braincoach'
```

## 📊 Database Schema

### Models
- **Parent**: User accounts for parents
- **Child**: Child profiles linked to parents
- **Module**: Training module categories
- **Exercise**: Individual training exercises
- **Session**: Training session records
- **HandTrackingFrame**: Frame-by-frame hand tracking data
- **Score**: Session scoring and feedback
- **Report**: Generated PDF reports

## 🔒 Security Features

- ✅ Password hashing using Werkzeug (scrypt)
- ✅ Session ownership verification on all API endpoints
- ✅ CSRF protection via Flask-Login
- ✅ Input validation on all forms
- ✅ Secure session management

## 🐛 Troubleshooting

### Webcam Not Working
- Ensure browser has camera permissions
- Check if another application is using the webcam
- Try refreshing the page

### Database Errors
```bash
# Reset database
rm instance/braincoach.db
python seed.py
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## 📈 Performance Optimizations

- Database indexes on frequently queried columns
- Lazy loading for relationships
- Frame data aggregation (every 60 frames)
- Efficient chart data queries
- Static asset caching

## 🚧 Known Limitations

1. **Frame Storage**: HandTrackingFrame table can grow large with extended use
2. **Browser Compatibility**: Requires modern browser with WebRTC support
3. **Webcam Required**: Training sessions require webcam access
4. **Single Hand Tracking**: Currently tracks one hand at a time

## 🛣️ Roadmap

### Version 2.0
- [ ] Multi-hand tracking support
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Social features (leaderboards)
- [ ] More exercise types
- [ ] Email notifications
- [ ] Data export functionality

### Version 3.0
- [ ] AI-powered exercise recommendations
- [ ] Voice commands
- [ ] Multiplayer mode
- [ ] Integration with educational platforms

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👏 Acknowledgments

- **MediaPipe** - Google's ML framework for hand tracking
- **Flask** - Python web framework
- **Chart.js** - Beautiful charts and graphs
- **Bootstrap 5** - Responsive UI framework
- **Howler.js** - Audio library
- **Split.js** - Resizable split views

## 📧 Support

For support, email support@braincoach-ai.com or open an issue on GitHub.

## 🌟 Show Your Support

Give a ⭐️ if this project helped you!

---

**Made with ❤️ for children's cognitive development**
