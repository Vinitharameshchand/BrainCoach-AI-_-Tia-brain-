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
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    grade = db.Column(db.String(20))
    enrolled_date = db.Column(db.DateTime, default=datetime.utcnow)
    sessions = db.relationship('Session', backref='child', lazy=True)

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
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    avg_accuracy = db.Column(db.Float)
    total_score = db.Column(db.Integer)
    result_status = db.Column(db.String(20)) # e.g., 'Completed', 'Incomplete'
    frames = db.relationship('HandTrackingFrame', backref='session', lazy=True)
    scores = db.relationship('Score', backref='session', lazy=True)
    reports = db.relationship('Report', backref='session', lazy=True)

class HandTrackingFrame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    frame_number = db.Column(db.Integer)
    landmark_data = db.Column(db.Text) # Stored as JSON string
    frame_accuracy = db.Column(db.Float)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    accuracy_percentage = db.Column(db.Float)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False)
    pdf_path = db.Column(db.String(255))
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    emailed_status = db.Column(db.Boolean, default=False)
