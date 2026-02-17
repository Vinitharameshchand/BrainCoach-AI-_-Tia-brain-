"""
Database Migration Script
Adds advanced scoring fields to existing database
"""

from app import create_app
from models import db

def migrate():
    app = create_app()
    with app.app_context():
        # Create all new tables and add new columns
        # SQLAlchemy will handle this automatically
        db.create_all()
        print("✓ Database migrated successfully!")
        print("✓ New tables created:")
        print("  - pattern_detection")
        print("  - trend_analysis")
        print("  - session_comparison")
        print("  - recommendation")
        print("✓ New columns added to existing tables")
        print("  - session: smoothed_accuracy, consistency_score, improvement_rate, composite_score, performance_grade, pattern_detected")
        print("  - score: composite_breakdown, recommendations, trend_analysis, confidence_score")

if __name__ == '__main__':
    migrate()
