"""
Analytics Blueprint
===================

Provides advanced analytics and scoring endpoints for comprehensive
performance analysis and personalized recommendations.
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import db, Session, Child, Score
from utils.advanced_scoring import (
    AdvancedScoringSystem,
    analyze_session_comprehensive
)
import json

analytics = Blueprint('analytics', __name__)


@analytics.route('/api/analytics/session/<int:session_id>', methods=['GET'])
@login_required
def get_session_analytics(session_id):
    """
    Get comprehensive analytics for a specific session.

    Returns:
        JSON with detailed analysis including:
        - Smoothed accuracy metrics
        - Pattern detection results
        - Session comparison with previous attempts
        - Improvement trend analysis
        - Personalized recommendations
    """
    # Verify session ownership
    session = Session.query.get_or_404(session_id)
    if session.child.parent_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    # Perform comprehensive analysis
    try:
        analysis = analyze_session_comprehensive(session_id, db.session)

        if 'error' in analysis:
            return jsonify({"error": analysis['error']}), 400

        return jsonify(analysis), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analytics.route('/api/analytics/child/<int:child_id>/overview', methods=['GET'])
@login_required
def get_child_overview(child_id):
    """
    Get comprehensive overview analytics for a child.

    Query parameters:
        - limit: Number of recent sessions to analyze (default: 10)
    """
    # Verify child ownership
    child = Child.query.get_or_404(child_id)
    if child.parent_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    limit = request.args.get('limit', 10, type=int)

    # Get recent sessions
    sessions = Session.query.filter_by(
        child_id=child_id,
        result_status='Completed'
    ).filter(
        Session.avg_accuracy.isnot(None)
    ).order_by(
        Session.start_time.desc()
    ).limit(limit).all()

    if not sessions:
        return jsonify({
            "child_id": child_id,
            "message": "No completed sessions found",
            "total_sessions": 0
        }), 200

    # Initialize scoring system
    scorer = AdvancedScoringSystem(child_age=child.age if child.age else 10)

    # Collect session accuracies
    session_accuracies = [s.avg_accuracy for s in sessions]
    session_accuracies.reverse()  # Chronological order

    # Trend analysis
    trend_analysis = scorer.detect_improvement_trend(session_accuracies)

    # Consistency analysis
    consistency = scorer.calculate_consistency_score(session_accuracies)

    # Calculate overall statistics
    avg_accuracy = sum(session_accuracies) / len(session_accuracies)
    max_accuracy = max(session_accuracies)
    min_accuracy = min(session_accuracies)

    # Recent performance (last 3 sessions vs previous 3)
    recent_comparison = {}
    if len(sessions) >= 6:
        recent_3 = [s.avg_accuracy for s in sessions[:3]]
        previous_3 = [s.avg_accuracy for s in sessions[3:6]]
        recent_comparison = scorer.compare_sessions(recent_3, previous_3)

    # Calculate total practice time
    total_duration = sum([
        (s.end_time - s.start_time).total_seconds()
        for s in sessions
        if s.end_time
    ])

    return jsonify({
        "child_id": child_id,
        "child_name": child.name,
        "child_age": child.age,
        "total_sessions": len(sessions),
        "dynamic_threshold": scorer.dynamic_threshold,
        "statistics": {
            "average_accuracy": round(avg_accuracy, 2),
            "max_accuracy": round(max_accuracy, 2),
            "min_accuracy": round(min_accuracy, 2),
            "consistency_score": round(consistency, 2),
            "total_practice_hours": round(total_duration / 3600, 2)
        },
        "trend_analysis": trend_analysis,
        "recent_comparison": recent_comparison,
        "session_history": [
            {
                "session_id": s.id,
                "date": s.start_time.isoformat(),
                "accuracy": s.avg_accuracy,
                "score": s.total_score,
                "exercise_id": s.exercise_id
            }
            for s in reversed(sessions)
        ]
    }), 200


@analytics.route('/api/analytics/child/<int:child_id>/recommendations', methods=['GET'])
@login_required
def get_recommendations(child_id):
    """
    Get personalized recommendations for a child based on their performance history.
    """
    # Verify child ownership
    child = Child.query.get_or_404(child_id)
    if child.parent_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    # Get latest session
    latest_session = Session.query.filter_by(
        child_id=child_id,
        result_status='Completed'
    ).order_by(Session.start_time.desc()).first()

    if not latest_session:
        return jsonify({
            "recommendations": [{
                'category': 'Getting Started',
                'priority': 'High',
                'message': 'Complete your first session to receive personalized recommendations!',
                'action': 'Start a training session'
            }]
        }), 200

    # Analyze latest session
    analysis = analyze_session_comprehensive(latest_session.id, db.session)

    if 'error' in analysis:
        return jsonify({"error": analysis['error']}), 400

    return jsonify({
        "child_id": child_id,
        "recommendations": analysis.get('recommendations', []),
        "based_on_session": latest_session.id,
        "analysis_date": analysis.get('analysis_timestamp')
    }), 200


@analytics.route('/api/analytics/child/<int:child_id>/progress-chart', methods=['GET'])
@login_required
def get_progress_chart(child_id):
    """
    Get data for progress visualization chart.

    Query parameters:
        - days: Number of days to include (default: 30)
        - metric: Metric to chart (accuracy, score, consistency) (default: accuracy)
    """
    # Verify child ownership
    child = Child.query.get_or_404(child_id)
    if child.parent_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    days = request.args.get('days', 30, type=int)
    metric = request.args.get('metric', 'accuracy', type=str)

    # Get sessions within time range
    from datetime import datetime, timedelta
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    sessions = Session.query.filter(
        Session.child_id == child_id,
        Session.result_status == 'Completed',
        Session.start_time >= cutoff_date
    ).order_by(Session.start_time).all()

    if not sessions:
        return jsonify({
            "labels": [],
            "data": [],
            "metric": metric,
            "message": "No data available for this time range"
        }), 200

    # Extract data based on metric
    labels = []
    data = []

    for session in sessions:
        labels.append(session.start_time.strftime('%Y-%m-%d %H:%M'))

        if metric == 'accuracy':
            data.append(session.avg_accuracy if session.avg_accuracy else 0)
        elif metric == 'score':
            data.append(session.total_score if session.total_score else 0)
        else:  # consistency
            # Calculate consistency for this session (would need frame data)
            data.append(0)  # Placeholder

    # Calculate trend line
    scorer = AdvancedScoringSystem(child_age=child.age if child.age else 10)
    trend_analysis = scorer.detect_improvement_trend(data)

    # Generate trend line points
    trend_line = []
    if trend_analysis['trend_available']:
        slope = trend_analysis['slope']
        intercept = trend_analysis['intercept']
        for i in range(len(data)):
            trend_line.append(slope * i + intercept)

    return jsonify({
        "labels": labels,
        "data": data,
        "trend_line": trend_line,
        "metric": metric,
        "trend_analysis": trend_analysis,
        "session_count": len(sessions)
    }), 200


@analytics.route('/api/analytics/compare-children', methods=['POST'])
@login_required
def compare_children():
    """
    Compare performance between multiple children (for parents with multiple children).

    Request body:
        {
            "child_ids": [1, 2, 3],
            "metric": "accuracy" | "score" | "improvement"
        }
    """
    data = request.json
    child_ids = data.get('child_ids', [])
    metric = data.get('metric', 'accuracy')

    if not child_ids or len(child_ids) < 2:
        return jsonify({"error": "At least 2 child IDs required"}), 400

    # Verify all children belong to current user
    children = Child.query.filter(Child.id.in_(child_ids)).all()

    for child in children:
        if child.parent_id != current_user.id:
            return jsonify({"error": "Unauthorized access to child data"}), 403

    comparison_data = []

    for child in children:
        # Get recent sessions
        sessions = Session.query.filter_by(
            child_id=child.id,
            result_status='Completed'
        ).order_by(Session.start_time.desc()).limit(10).all()

        if not sessions:
            comparison_data.append({
                "child_id": child.id,
                "child_name": child.name,
                "data": None,
                "message": "No completed sessions"
            })
            continue

        # Calculate requested metric
        if metric == 'accuracy':
            value = sum(s.avg_accuracy for s in sessions) / len(sessions)
        elif metric == 'score':
            value = sum(s.total_score for s in sessions if s.total_score) / len(sessions)
        elif metric == 'improvement':
            accuracies = [s.avg_accuracy for s in reversed(sessions)]
            scorer = AdvancedScoringSystem(child_age=child.age if child.age else 10)
            trend = scorer.detect_improvement_trend(accuracies)
            value = trend.get('slope', 0) * 10  # Scale for visibility
        else:
            value = 0

        comparison_data.append({
            "child_id": child.id,
            "child_name": child.name,
            "child_age": child.age,
            "metric_value": round(value, 2),
            "session_count": len(sessions)
        })

    return jsonify({
        "metric": metric,
        "comparison": comparison_data,
        "timestamp": datetime.utcnow().isoformat()
    }), 200


@analytics.route('/api/analytics/export/<int:child_id>', methods=['GET'])
@login_required
def export_analytics(child_id):
    """
    Export comprehensive analytics data for a child in JSON format.
    Useful for external analysis or record keeping.
    """
    # Verify child ownership
    child = Child.query.get_or_404(child_id)
    if child.parent_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    # Get all completed sessions
    sessions = Session.query.filter_by(
        child_id=child_id,
        result_status='Completed'
    ).order_by(Session.start_time).all()

    export_data = {
        "export_date": datetime.utcnow().isoformat(),
        "child_info": {
            "id": child.id,
            "name": child.name,
            "age": child.age,
            "grade": child.grade,
            "enrolled_date": child.enrolled_date.isoformat() if child.enrolled_date else None
        },
        "sessions": []
    }

    # Analyze each session
    for session in sessions:
        session_data = {
            "session_id": session.id,
            "exercise_id": session.exercise_id,
            "start_time": session.start_time.isoformat(),
            "end_time": session.end_time.isoformat() if session.end_time else None,
            "duration_seconds": (session.end_time - session.start_time).total_seconds() if session.end_time else 0,
            "avg_accuracy": session.avg_accuracy,
            "total_score": session.total_score
        }

        # Add detailed analysis
        try:
            analysis = analyze_session_comprehensive(session.id, db.session)
            if 'error' not in analysis:
                session_data['detailed_analysis'] = analysis
        except:
            pass

        export_data["sessions"].append(session_data)

    return jsonify(export_data), 200
