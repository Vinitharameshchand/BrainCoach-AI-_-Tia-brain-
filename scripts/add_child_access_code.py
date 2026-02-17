"""
Migration: Add access code system for children
Adds access_code, is_active, and last_access fields to Child model
"""
from app import create_app
from models import db, Child
import random
import string

def generate_unique_code():
    """Generate unique 6-digit code"""
    while True:
        code = ''.join(random.choices(string.digits, k=6))
        existing = Child.query.filter_by(access_code=code).first()
        if not existing:
            return code

def migrate():
    app = create_app()
    with app.app_context():
        # Add columns if they don't exist
        try:
            # Try to access the columns
            children = Child.query.all()
            for child in children:
                _ = child.access_code
            print("✓ Columns already exist")
        except:
            print("Adding new columns...")
            # Columns don't exist, need to add them
            from sqlalchemy import text
            with db.engine.connect() as conn:
                # Add access_code column
                conn.execute(text(
                    "ALTER TABLE child ADD COLUMN access_code VARCHAR(6) UNIQUE"
                ))
                # Add is_active column
                conn.execute(text(
                    "ALTER TABLE child ADD COLUMN is_active BOOLEAN DEFAULT 1"
                ))
                # Add last_access column
                conn.execute(text(
                    "ALTER TABLE child ADD COLUMN last_access DATETIME"
                ))
                # Create index on access_code
                conn.execute(text(
                    "CREATE INDEX idx_child_access_code ON child(access_code)"
                ))
                conn.commit()
            print("✓ Columns added successfully")

        # Generate access codes for existing children without codes
        children = Child.query.filter_by(access_code=None).all()
        if children:
            print(f"\nGenerating access codes for {len(children)} children...")
            for child in children:
                child.access_code = generate_unique_code()
                child.is_active = True
                print(f"  • {child.name}: {child.access_code}")

            db.session.commit()
            print(f"✓ Generated {len(children)} access codes")
        else:
            print("✓ All children have access codes")

        print("\n✅ Migration completed successfully!")
        print("\n📋 Access Codes Summary:")
        all_children = Child.query.all()
        for child in all_children:
            status = "🟢 Active" if child.is_active else "🔴 Inactive"
            print(f"  {status} {child.name}: {child.access_code}")

if __name__ == '__main__':
    migrate()
