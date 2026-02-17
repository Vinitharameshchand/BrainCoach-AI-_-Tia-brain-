-- Migration: Add Advanced Scoring Fields
-- Purpose: Extend database schema to support advanced analytics
-- Date: 2026-02-17

-- Add new columns to Session table for advanced metrics
ALTER TABLE session ADD COLUMN IF NOT EXISTS smoothed_accuracy FLOAT;
ALTER TABLE session ADD COLUMN IF NOT EXISTS consistency_score FLOAT;
ALTER TABLE session ADD COLUMN IF NOT EXISTS improvement_rate FLOAT;
ALTER TABLE session ADD COLUMN IF NOT EXISTS composite_score FLOAT;
ALTER TABLE session ADD COLUMN IF NOT EXISTS performance_grade VARCHAR(2);
ALTER TABLE session ADD COLUMN IF NOT EXISTS pattern_detected BOOLEAN DEFAULT FALSE;

-- Add new columns to Score table for detailed feedback
ALTER TABLE score ADD COLUMN IF NOT EXISTS composite_breakdown TEXT;
ALTER TABLE score ADD COLUMN IF NOT EXISTS recommendations TEXT;
ALTER TABLE score ADD COLUMN IF NOT EXISTS trend_analysis TEXT;
ALTER TABLE score ADD COLUMN IF NOT EXISTS confidence_score FLOAT;

-- Create new table for Pattern Detection results
CREATE TABLE IF NOT EXISTS pattern_detection (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    landmark_index INTEGER NOT NULL,
    error_mean FLOAT,
    error_std FLOAT,
    anomaly_count INTEGER,
    anomaly_percentage FLOAT,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES session(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_pattern_session ON pattern_detection(session_id);
CREATE INDEX IF NOT EXISTS idx_pattern_landmark ON pattern_detection(landmark_index);

-- Create new table for Trend Analysis
CREATE TABLE IF NOT EXISTS trend_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id INTEGER NOT NULL,
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    slope FLOAT,
    intercept FLOAT,
    r_squared FLOAT,
    trend_direction VARCHAR(50),
    confidence_score FLOAT,
    predicted_next FLOAT,
    sessions_analyzed INTEGER,
    FOREIGN KEY (child_id) REFERENCES child(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_trend_child ON trend_analysis(child_id);
CREATE INDEX IF NOT EXISTS idx_trend_date ON trend_analysis(analysis_date);

-- Create new table for Session Comparisons
CREATE TABLE IF NOT EXISTS session_comparison (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    current_session_id INTEGER NOT NULL,
    previous_session_id INTEGER NOT NULL,
    cohens_d FLOAT,
    improvement_percentage FLOAT,
    effect_interpretation VARCHAR(100),
    comparison_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (current_session_id) REFERENCES session(id) ON DELETE CASCADE,
    FOREIGN KEY (previous_session_id) REFERENCES session(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_comparison_current ON session_comparison(current_session_id);
CREATE INDEX IF NOT EXISTS idx_comparison_previous ON session_comparison(previous_session_id);

-- Create new table for Personalized Recommendations
CREATE TABLE IF NOT EXISTS recommendation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id INTEGER NOT NULL,
    session_id INTEGER,
    category VARCHAR(50),
    priority VARCHAR(20),
    message TEXT,
    action_suggestion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (child_id) REFERENCES child(id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES session(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_recommendation_child ON recommendation(child_id);
CREATE INDEX IF NOT EXISTS idx_recommendation_session ON recommendation(session_id);
CREATE INDEX IF NOT EXISTS idx_recommendation_acknowledged ON recommendation(acknowledged);

-- Create view for comprehensive session analytics
CREATE VIEW IF NOT EXISTS session_analytics_view AS
SELECT
    s.id as session_id,
    s.child_id,
    c.name as child_name,
    c.age as child_age,
    s.exercise_id,
    e.title as exercise_title,
    s.start_time,
    s.end_time,
    s.avg_accuracy,
    s.total_score,
    s.smoothed_accuracy,
    s.consistency_score,
    s.composite_score,
    s.performance_grade,
    s.pattern_detected,
    COUNT(DISTINCT pd.landmark_index) as problematic_landmarks_count,
    sc.feedback as score_feedback,
    sc.recommendations as recommendations_json,
    JULIANDAY(s.end_time) - JULIANDAY(s.start_time) as duration_days
FROM session s
LEFT JOIN child c ON s.child_id = c.id
LEFT JOIN exercise e ON s.exercise_id = e.id
LEFT JOIN pattern_detection pd ON s.id = pd.session_id
LEFT JOIN score sc ON s.id = sc.session_id
WHERE s.result_status = 'Completed'
GROUP BY s.id;

-- Create view for child progress tracking
CREATE VIEW IF NOT EXISTS child_progress_view AS
SELECT
    c.id as child_id,
    c.name as child_name,
    c.age,
    c.grade,
    COUNT(DISTINCT s.id) as total_sessions,
    AVG(s.avg_accuracy) as overall_avg_accuracy,
    AVG(s.consistency_score) as overall_consistency,
    AVG(s.composite_score) as overall_composite_score,
    MAX(s.composite_score) as best_score,
    MIN(s.composite_score) as worst_score,
    SUM(CASE WHEN s.pattern_detected THEN 1 ELSE 0 END) as sessions_with_patterns,
    MAX(s.start_time) as last_session_date,
    (
        SELECT trend_direction
        FROM trend_analysis ta
        WHERE ta.child_id = c.id
        ORDER BY ta.analysis_date DESC
        LIMIT 1
    ) as current_trend
FROM child c
LEFT JOIN session s ON c.id = s.child_id AND s.result_status = 'Completed'
GROUP BY c.id;

-- Add comments to tables
-- (SQLite doesn't support COMMENT ON TABLE, but we document here)

-- Table: pattern_detection
-- Purpose: Stores detected patterns in hand movement errors
-- Usage: Identify specific landmarks that consistently show problems

-- Table: trend_analysis
-- Purpose: Stores long-term performance trends using linear regression
-- Usage: Track improvement over time and predict future performance

-- Table: session_comparison
-- Purpose: Stores comparisons between consecutive sessions
-- Usage: Quantify session-to-session improvement using effect sizes

-- Table: recommendation
-- Purpose: Stores personalized AI-generated recommendations
-- Usage: Provide actionable feedback to parents and children

-- Insert sample data for testing (optional)
-- Uncomment to use:

/*
INSERT INTO recommendation (child_id, session_id, category, priority, message, action_suggestion)
VALUES
(1, NULL, 'Getting Started', 'High', 'Complete your first session to receive personalized recommendations!', 'Start a training session');
*/

-- Migration complete
-- Remember to update models.py to include new fields and tables
