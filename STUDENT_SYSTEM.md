# Student Authentication & Exercise System

## Overview
BrainCoach AI now has a complete student authentication and exercise system that allows children to access exercises on their own devices using simple 6-digit access codes.

## Features Implemented

### 1. Student Authentication
- **Simple Login**: Students enter a 6-digit numeric code
- **Auto-submit**: Form automatically submits when 6 digits are entered
- **Virtual Keypad**: Optional on-screen keypad for touchscreen devices
- **Session Management**: Secure session handling without requiring complex passwords
- **Last Access Tracking**: Records when students last logged in

### 2. Student Dashboard
- **Personalized Welcome**: Greets student by name
- **Statistics Cards**: Shows total sessions, average accuracy, and recent activities
- **Exercise Grid**: Visual cards for all available exercises with:
  - Exercise icons and titles
  - Duration and difficulty badges
  - One-click start buttons
- **Recent Activity**: Shows the last 3 completed sessions with accuracy badges
- **Mobile-Friendly**: Responsive design works on all devices

### 3. Exercise Training Interface
- **Split View**: Side-by-side comparison of demo video and student's webcam
- **Real-time Hand Tracking**: Uses MediaPipe for hand gesture recognition
- **Accuracy Meter**: Live circular progress indicator showing performance
- **Feedback System**: Emoji feedback based on performance
- **Timer**: Countdown timer for exercise duration
- **Results Modal**: Shows grade, accuracy, and score at completion

### 4. Session History
- **Complete History**: View all completed sessions
- **Detailed Stats**: Accuracy, consistency, composite score for each session
- **Performance Grades**: Visual grade badges (A, B, C, D, F)
- **Pattern Detection**: Alerts when AI detects improvement patterns
- **Progress Bars**: Visual representation of performance metrics

### 5. API Endpoints
All student endpoints are under `/student/`:
- `GET /student/login` - Login page
- `POST /student/login` - Process login
- `GET /student/dashboard` - Main dashboard
- `GET /student/exercise/<id>/start` - Start an exercise
- `GET /student/training/<exercise_id>/<session_id>` - Training interface
- `GET /student/sessions/history` - View session history
- `GET /student/logout` - Logout
- `POST /student/api/session/update` - Update session data (AJAX)
- `POST /student/api/session/complete` - Complete session (AJAX)

## Security Features

### Authentication
- Access codes are unique 6-digit numbers
- Codes are indexed in database for fast lookup
- Active/inactive status check prevents disabled accounts from logging in
- Session-based authentication (no passwords needed)

### Authorization
- Custom `@student_login_required` decorator protects all student routes
- Session verification checks on all API endpoints
- Child ID validation prevents unauthorized access to other students' data
- CSRF protection through Flask's built-in session management

### Session Management
- Student ID stored in Flask session
- Student name cached for UI display
- Session cleared on logout
- Auto-timeout configurable via Flask session settings

## Database Schema

### Child Model Extensions
```python
access_code = db.Column(db.String(6), unique=True, index=True)  # 6-digit code
is_active = db.Column(db.Boolean, default=True)                  # Active status
last_access = db.Column(db.DateTime)                              # Last login time
```

## Setup Instructions

### 1. Register Student Blueprint
Already done in `app.py`:
```python
from routes.student import student as student_blueprint
app.register_blueprint(student_blueprint)
```

### 2. Generate Access Codes
Run the migration script to add access codes to existing children:
```bash
python add_child_access_code.py
```

Or generate codes programmatically:
```python
child = Child.query.get(child_id)
child.generate_access_code()
db.session.commit()
```

### 3. Parent Dashboard Integration
Parents can:
- View their children's access codes in the parent dashboard
- Share codes with their children
- Monitor activity via last_access timestamp
- Deactivate/activate child accounts via is_active flag

## User Flow

### Student Login
1. Student opens `/student/login`
2. Enters 6-digit access code
3. Auto-redirected to dashboard on valid code
4. Invalid code shows error message

### Exercise Session
1. Student selects exercise from dashboard
2. System creates new Session record
3. Student clicks "Start Adventure"
4. Camera initializes, hand tracking begins
5. Real-time accuracy feedback displayed
6. Timer counts down
7. Session auto-completes at timer end or manual stop
8. Results modal shows performance
9. Auto-redirect to dashboard after 10 seconds

### Session Data Flow
```
Student → Webcam → MediaPipe → Landmarks
                                    ↓
                    POST /api/session/update (every 30 frames)
                                    ↓
                    HandTrackingFrame records saved
                                    ↓
                    POST /api/session/complete
                                    ↓
                    Advanced scoring + analysis
                                    ↓
                    Results displayed
```

## Customization Options

### Visual Themes
Edit CSS variables in templates:
```css
:root {
    --primary: #667eea;
    --secondary: #764ba2;
    --success: #10b981;
}
```

### Exercise Duration
Set in Exercise model:
```python
exercise.duration_seconds = 120  # 2 minutes
```

### Accuracy Threshold
Set in Exercise model:
```python
exercise.accuracy_threshold = 85.0  # 85%
```

### Auto-redirect Timer
Change countdown in `student_training.html`:
```javascript
let countdown = 10;  // seconds
```

## Future Enhancements

### Potential Features
- [ ] Gamification (points, badges, levels)
- [ ] Leaderboards (optional, with privacy settings)
- [ ] Daily streaks and rewards
- [ ] Progress charts and graphs
- [ ] Parent-child messaging
- [ ] Exercise recommendations based on performance
- [ ] Multi-language support
- [ ] Accessibility features (screen reader support, high contrast mode)
- [ ] Offline mode with sync
- [ ] Push notifications for reminders

### Security Enhancements
- [ ] Rate limiting on login attempts
- [ ] Account lockout after failed attempts
- [ ] Session timeout warnings
- [ ] Two-factor authentication (optional for older children)
- [ ] Activity logging for parent review

## Troubleshooting

### Access Code Not Working
- Verify code is exactly 6 digits
- Check if account is active (`child.is_active = True`)
- Ensure code exists in database
- Check for typos (code is numeric only)

### Camera Not Starting
- Check browser permissions for webcam access
- Ensure HTTPS connection (required for webcam on modern browsers)
- Verify MediaPipe libraries are loading correctly
- Check console for JavaScript errors

### Session Not Saving
- Verify session_id is being passed correctly
- Check network tab for failed API calls
- Ensure database connection is active
- Check server logs for errors

## Support
For issues or questions, check:
1. Server logs: `flask run --debug`
2. Browser console: F12 → Console tab
3. Network requests: F12 → Network tab
4. Database: Query Session and HandTrackingFrame tables
