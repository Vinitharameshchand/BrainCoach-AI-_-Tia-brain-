"""
Student Routes - Child device access via access codes
Children can access exercises on their own devices using simple 6-digit codes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, Child, Session, Exercise, Module, HandTrackingFrame, Score
from datetime import datetime
from functools import wraps
import json

student = Blueprint('student', __name__, url_prefix='/student')

def student_login_required(f):
    """Decorator to require student login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'student_id' not in session:
            flash('Please enter your access code first')
            return redirect(url_for('student.login'))
        return f(*args, **kwargs)
    return decorated_function

@student.route('/login', methods=['GET', 'POST'])
def login():
    """Student login - enter 6-digit access code"""
    if request.method == 'POST':
        access_code = request.form.get('access_code', '').strip()

        # Validate code format
        if not access_code or len(access_code) != 6 or not access_code.isdigit():
            flash('Please enter a valid 6-digit access code')
            return redirect(url_for('student.login'))

        # Find child by access code
        child = Child.query.filter_by(access_code=access_code, is_active=True).first()

        if not child:
            flash('Invalid access code. Please check with your parent.')
            return redirect(url_for('student.login'))

        # Update last access time
        child.last_access = datetime.utcnow()
        db.session.commit()

        # Store child ID in session (not using flask-login for students)
        session['student_id'] = child.id
        session['student_name'] = child.name

        return redirect(url_for('student.dashboard'))

    return render_template('student_login.html')

@student.route('/dashboard')
@student_login_required
def dashboard():
    """Student dashboard - simplified view with exercises"""
    student_id = session.get('student_id')

    child = Child.query.get_or_404(student_id)

    # Get modules and exercises
    modules = Module.query.all()
    exercises = Exercise.query.all()

    # Get recent sessions for this child
    recent_sessions = Session.query.filter_by(
        child_id=child.id
    ).order_by(Session.start_time.desc()).limit(3).all()

    # Calculate stats
    total_sessions = Session.query.filter_by(
        child_id=child.id,
        result_status='Completed'
    ).count()

    completed_sessions = Session.query.filter(
        Session.child_id == child.id,
        Session.avg_accuracy != None,
        Session.result_status == 'Completed'
    ).all()

    avg_accuracy = 0
    if completed_sessions:
        avg_accuracy = sum(s.avg_accuracy for s in completed_sessions) / len(completed_sessions)

    return render_template('student_dashboard.html',
                          child=child,
                          modules=modules,
                          exercises=exercises,
                          recent_sessions=recent_sessions,
                          total_sessions=total_sessions,
                          avg_accuracy=round(avg_accuracy, 1) if avg_accuracy else 0)

@student.route('/exercise/<int:exercise_id>/start')
@student_login_required
def start_exercise(exercise_id):
    """Start an exercise directly"""
    student_id = session.get('student_id')
    child = Child.query.get_or_404(student_id)
    exercise = Exercise.query.get_or_404(exercise_id)

    # Create a new session for this exercise
    new_session = Session(
        child_id=child.id,
        exercise_id=exercise.id,
        start_time=datetime.utcnow(),
        result_status='In Progress'
    )
    db.session.add(new_session)
    db.session.commit()

    return redirect(url_for('student.training_session',
                          exercise_id=exercise.id,
                          session_id=new_session.id))

@student.route('/training/<int:exercise_id>/<int:session_id>')
@student_login_required
def training_session(exercise_id, session_id):
    """Student training session page"""
    student_id = session.get('student_id')
    child = Child.query.get_or_404(student_id)
    exercise = Exercise.query.get_or_404(exercise_id)
    training_session = Session.query.get_or_404(session_id)

    # Verify this session belongs to this student
    if training_session.child_id != student_id:
        flash('Unauthorized access')
        return redirect(url_for('student.dashboard'))

    return render_template('student_training.html',
                          child=child,
                          exercise=exercise,
                          session_id=training_session.id)

@student.route('/logout')
def logout():
    """Student logout - clear session"""
    session.pop('student_id', None)
    session.pop('student_name', None)
    flash('You have been logged out. See you next time! 👋')
    return redirect(url_for('student.login'))

@student.route('/sessions/history')
@student_login_required
def sessions_history():
    """View session history"""
    student_id = session.get('student_id')

    child = Child.query.get_or_404(student_id)

    # Get all completed sessions
    sessions = Session.query.filter_by(
        child_id=child.id,
        result_status='Completed'
    ).order_by(Session.start_time.desc()).all()

    return render_template('student_sessions.html',
                          child=child,
                          sessions=sessions)

@student.route('/api/session/update', methods=['POST'])
@student_login_required
def api_update_session():
    """API endpoint for students to update session data"""
    student_id = session.get('student_id')
    data = request.json
    session_id = data.get('session_id')
    accuracy = data.get('accuracy')
    landmarks = data.get('landmarks')
    frame_number = data.get('frame_number')

    # Verify session ownership
    sess = Session.query.get_or_404(session_id)
    if sess.child_id != student_id:
        return jsonify({"error": "Unauthorized"}), 403

    # Save frame data
    frame = HandTrackingFrame(
        session_id=session_id,
        frame_number=frame_number,
        landmark_data=json.dumps(landmarks),
        frame_accuracy=accuracy
    )
    db.session.add(frame)
    db.session.commit()

    return jsonify({"status": "success"})

@student.route('/api/session/complete', methods=['POST'])
@student_login_required
def api_complete_session():
    """API endpoint for students to complete session"""
    from utils.advanced_scoring import analyze_session_comprehensive
    from utils.pdf_generator import generate_session_report
    import os

    student_id = session.get('student_id')
    data = request.json
    session_id = data.get('session_id')
    avg_accuracy = data.get('avg_accuracy')
    total_score = data.get('total_score')

    sess = Session.query.get_or_404(session_id)

    # Verify session ownership
    if sess.child_id != student_id:
        return jsonify({"error": "Unauthorized"}), 403

    sess.end_time = datetime.utcnow()
    sess.avg_accuracy = avg_accuracy
    sess.total_score = total_score
    sess.result_status = 'Completed'

    # Perform advanced analysis
    analysis = {}
    try:
        analysis = analyze_session_comprehensive(session_id, db.session)

        if 'error' not in analysis:
            # Store advanced metrics
            sess.smoothed_accuracy = analysis.get('average_accuracy')
            sess.consistency_score = analysis.get('consistency_score')
            composite = analysis.get('composite_score', {})
            sess.composite_score = composite.get('composite_score')
            sess.performance_grade = composite.get('grade')
    except Exception as e:
        print(f"Advanced analysis failed: {e}")

    # Add score entry
    score_entry = Score(
        session_id=session_id,
        accuracy_percentage=avg_accuracy,
        feedback=f"Great job! You completed this exercise with {avg_accuracy:.2f}% accuracy.",
    )
    db.session.add(score_entry)
    db.session.commit()

    # Trigger PDF generation
    try:
        pdf_dir = os.path.join('reports', f'child_{sess.child_id}')
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        pdf_path = os.path.join(pdf_dir, f'session_{session_id}.pdf')
        generate_session_report(sess, pdf_path)
    except Exception as e:
        print(f"PDF generation failed: {e}")

    return jsonify({
        "status": "success",
        "redirect": url_for('student.dashboard'),
        "avg_accuracy": avg_accuracy,
        "grade": sess.performance_grade
    })

@student.route('/sessions/download/<int:session_id>')
@student_login_required
def download_report(session_id):
    from flask import send_file
    from utils.pdf_generator import generate_session_report
    import os
    
    student_id = session.get('student_id')
    sess = Session.query.get_or_404(session_id)
    
    # Verify session ownership
    if sess.child_id != student_id:
        return jsonify({"error": "Unauthorized"}), 403
    
    pdf_dir = os.path.join('reports', f'child_{sess.child_id}')
    pdf_path = os.path.join(pdf_dir, f'session_{session_id}.pdf')
    
    if not os.path.exists(pdf_path):
        os.makedirs(pdf_dir, exist_ok=True)
        try:
            generate_session_report(sess, pdf_path)
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return jsonify({"error": f"Failed to generate report: {e}"}), 500

    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    return jsonify({"error": "Report not found"}), 404
