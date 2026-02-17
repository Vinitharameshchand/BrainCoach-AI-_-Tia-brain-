from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models import db, Child, Exercise, Session, HandTrackingFrame, Score
from datetime import datetime
import json

session = Blueprint('session', __name__)

@session.route('/training/<int:child_id>/<int:exercise_id>')
@login_required
def start_training(child_id, exercise_id):
    child = Child.query.get_or_404(child_id)
    exercise = Exercise.query.get_or_404(exercise_id)
    
    # Create a new session record
    new_session = Session(
        child_id=child_id,
        exercise_id=exercise_id,
        start_time=datetime.utcnow(),
        result_status='In Progress'
    )
    db.session.add(new_session)
    db.session.commit()
    
    return render_template('session.html', child=child, exercise=exercise, session_id=new_session.id)

@session.route('/api/session/update', methods=['POST'])
@login_required
def update_session():
    data = request.json
    session_id = data.get('session_id')
    accuracy = data.get('accuracy')
    landmarks = data.get('landmarks')
    frame_number = data.get('frame_number')
    
    # Verify session ownership
    sess = Session.query.get_or_404(session_id)
    if sess.child.parent_id != current_user.id:
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

from utils.pdf_generator import generate_session_report
import os

@session.route('/api/session/complete', methods=['POST'])
@login_required
def complete_session():
    data = request.json
    session_id = data.get('session_id')
    avg_accuracy = data.get('avg_accuracy')
    total_score = data.get('total_score')
    
    sess = Session.query.get_or_404(session_id)
    
    # Verify session ownership
    if sess.child.parent_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    sess.end_time = datetime.utcnow()
    sess.avg_accuracy = avg_accuracy
    sess.total_score = total_score
    sess.result_status = 'Completed'
    
    # Add a score entry
    score_entry = Score(
        session_id=session_id,
        accuracy_percentage=avg_accuracy,
        feedback=f"Session completed with {avg_accuracy:.2f}% accuracy."
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
        # Don't fail the request if PDF generation fails
    
    return jsonify({"status": "success", "redirect": url_for('dashboard.index')})
