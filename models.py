from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class Parent(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    children = db.relationship('Child', backref='parent', lazy=True)

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    grade = db.Column(db.String(20))
    enrolled_date = db.Column(db.DateTime, default=datetime.utcnow)
    access_code = db.Column(db.String(6), unique=True, index=True)
    is_active = db.Column(db.Boolean, default=True)
    last_access = db.Column(db.DateTime)
    sessions = db.relationship('Session', backref='child', lazy=True)

    def generate_access_code(self):
        """Generate unique 6-digit access code"""
        import random
        import string
        while True:
            code = ''.join(random.choices(string.digits, k=6))
            existing = Child.query.filter_by(access_code=code).first()
            if not existing:
                self.access_code = code
                return code

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    difficulty = db.Column(db.String(20))
    exercises = db.relationship('Exercise', backref='module', lazy=True)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    video_url = db.Column(db.String(255))
    accuracy_threshold = db.Column(db.Float, default=85.0)
    duration_seconds = db.Column(db.Integer, default=60)
    sessions = db.relationship('Session', backref='exercise', lazy=True)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False, index=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False, index=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    avg_accuracy = db.Column(db.Float)
    total_score = db.Column(db.Integer)
    result_status = db.Column(db.String(20)) # e.g., 'Completed', 'Incomplete'

    # Advanced scoring fields
    smoothed_accuracy = db.Column(db.Float)
    consistency_score = db.Column(db.Float)
    improvement_rate = db.Column(db.Float)
    composite_score = db.Column(db.Float)
    performance_grade = db.Column(db.String(2))
    pattern_detected = db.Column(db.Boolean, default=False)

    frames = db.relationship('HandTrackingFrame', backref='session', lazy=True)
    scores = db.relationship('Score', backref='session', lazy=True)
    reports = db.relationship('Report', backref='session', lazy=True)

class HandTrackingFrame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False, index=True)
    frame_number = db.Column(db.Integer)
    landmark_data = db.Column(db.Text) # Stored as JSON string
    frame_accuracy = db.Column(db.Float)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    accuracy_percentage = db.Column(db.Float)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Advanced scoring fields
    composite_breakdown = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    trend_analysis = db.Column(db.Text)
    confidence_score = db.Column(db.Float)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False)
    pdf_path = db.Column(db.String(255))
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    emailed_status = db.Column(db.Boolean, default=False)

class PatternDetection(db.Model):
    __tablename__ = 'pattern_detection'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False, index=True)
    landmark_index = db.Column(db.Integer)
    error_mean = db.Column(db.Float)
    error_std = db.Column(db.Float)
    anomaly_count = db.Column(db.Integer)
    anomaly_percentage = db.Column(db.Float)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)

class TrendAnalysis(db.Model):
    __tablename__ = 'trend_analysis'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False, index=True)
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    slope = db.Column(db.Float)
    intercept = db.Column(db.Float)
    r_squared = db.Column(db.Float)
    trend_direction = db.Column(db.String(50))
    confidence_score = db.Column(db.Float)
    predicted_next = db.Column(db.Float)
    sessions_analyzed = db.Column(db.Integer)

class SessionComparison(db.Model):
    __tablename__ = 'session_comparison'
    id = db.Column(db.Integer, primary_key=True)
    current_session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    previous_session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    cohens_d = db.Column(db.Float)
    improvement_percentage = db.Column(db.Float)
    effect_interpretation = db.Column(db.String(100))
    comparison_date = db.Column(db.DateTime, default=datetime.utcnow)

class Recommendation(db.Model):
    __tablename__ = 'recommendation'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    category = db.Column(db.String(50))
    priority = db.Column(db.String(20))
    message = db.Column(db.Text)
    action_suggestion = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    acknowledged = db.Column(db.Boolean, default=False)
