from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models import db, Child, Exercise, Session, HandTrackingFrame, Score, PatternDetection, TrendAnalysis, Recommendation
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
from utils.advanced_scoring import analyze_session_comprehensive
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

            # Check for patterns
            patterns = analysis.get('pattern_analysis', {})
            sess.pattern_detected = patterns.get('patterns_detected', False)

            # Store pattern detections if found
            if patterns.get('patterns_detected'):
                for landmark_idx in patterns.get('problematic_landmarks', [])[:10]:  # Limit to 10
                    pattern_entry = PatternDetection(
                        session_id=session_id,
                        landmark_index=int(landmark_idx) if isinstance(landmark_idx, (int, float)) else 0,
                        anomaly_percentage=patterns.get('outlier_percentage', 0)
                    )
                    db.session.add(pattern_entry)

            # Store trend analysis
            trend = analysis.get('trend_analysis', {})
            if trend.get('trend_available'):
                trend_entry = TrendAnalysis(
                    child_id=sess.child_id,
                    slope=trend.get('slope'),
                    intercept=trend.get('intercept'),
                    r_squared=trend.get('r_squared'),
                    trend_direction=trend.get('trend_direction'),
                    confidence_score=trend.get('confidence'),
                    predicted_next=trend.get('predicted_next'),
                    sessions_analyzed=len(analysis.get('smoothed_accuracies', []))
                )
                db.session.add(trend_entry)

            # Store recommendations
            for rec in analysis.get('recommendations', [])[:5]:  # Limit to 5
                rec_entry = Recommendation(
                    child_id=sess.child_id,
                    session_id=session_id,
                    category=rec.get('category'),
                    priority=rec.get('priority'),
                    message=rec.get('message'),
                    action_suggestion=rec.get('action')
                )
                db.session.add(rec_entry)
    except Exception as e:
        print(f"Advanced analysis failed: {e}")
        # Continue with basic scoring if advanced analysis fails

    # Add score entry with detailed feedback
    score_entry = Score(
        session_id=session_id,
        accuracy_percentage=avg_accuracy,
        feedback=f"Session completed with {avg_accuracy:.2f}% accuracy.",
        recommendations=json.dumps(analysis.get('recommendations', [])) if 'error' not in analysis else None,
        composite_breakdown=json.dumps(analysis.get('composite_score', {}).get('breakdown', {})) if 'error' not in analysis else None
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
        "redirect": url_for('dashboard.index'),
        "analysis": analysis if 'error' not in analysis else None
    })
