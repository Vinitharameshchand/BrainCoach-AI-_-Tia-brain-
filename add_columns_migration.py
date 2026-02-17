"""
Add new columns to existing tables
"""

import sqlite3

def migrate():
    conn = sqlite3.connect('instance/braincoach.db')
    cursor = conn.cursor()

    # Get existing columns in session table
    cursor.execute("PRAGMA table_info(session)")
    existing_columns = [row[1] for row in cursor.fetchall()]

    # Add columns to session table if they don't exist
    session_columns = [
        ('smoothed_accuracy', 'FLOAT'),
        ('consistency_score', 'FLOAT'),
        ('improvement_rate', 'FLOAT'),
        ('composite_score', 'FLOAT'),
        ('performance_grade', 'VARCHAR(2)'),
        ('pattern_detected', 'BOOLEAN DEFAULT 0')
    ]

    print("Adding columns to session table...")
    for col_name, col_type in session_columns:
        if col_name not in existing_columns:
            try:
                cursor.execute(f"ALTER TABLE session ADD COLUMN {col_name} {col_type}")
                print(f"  ✓ Added {col_name}")
            except Exception as e:
                print(f"  ⚠ {col_name} already exists or error: {e}")

    # Get existing columns in score table
    cursor.execute("PRAGMA table_info(score)")
    existing_score_columns = [row[1] for row in cursor.fetchall()]

    # Add columns to score table if they don't exist
    score_columns = [
        ('composite_breakdown', 'TEXT'),
        ('recommendations', 'TEXT'),
        ('trend_analysis', 'TEXT'),
        ('confidence_score', 'FLOAT')
    ]

    print("\nAdding columns to score table...")
    for col_name, col_type in score_columns:
        if col_name not in existing_score_columns:
            try:
                cursor.execute(f"ALTER TABLE score ADD COLUMN {col_name} {col_type}")
                print(f"  ✓ Added {col_name}")
            except Exception as e:
                print(f"  ⚠ {col_name} already exists or error: {e}")

    conn.commit()
    conn.close()
    print("\n✓ Migration completed successfully!")

if __name__ == '__main__':
    migrate()
