"""
Improved migration: Add access code system for children
Works with SQLite limitations
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
        print("🔄 Starting migration...")

        # Add columns without UNIQUE constraint first
        try:
            from sqlalchemy import text
            with db.engine.connect() as conn:
                try:
                    # Try to add columns
                    conn.execute(text("ALTER TABLE child ADD COLUMN access_code VARCHAR(6)"))
                    conn.execute(text("ALTER TABLE child ADD COLUMN is_active BOOLEAN DEFAULT 1"))
                    conn.execute(text("ALTER TABLE child ADD COLUMN last_access DATETIME"))
                    conn.commit()
                    print("✓ Columns added successfully")
                except Exception as e:
                    if "duplicate column name" in str(e).lower():
                        print("✓ Columns already exist")
                    else:
                        raise
        except Exception as e:
            print(f"Error during column creation: {e}")
            print("Attempting to continue with existing columns...")

        # Generate access codes for children without codes
        try:
            children = Child.query.filter((Child.access_code == None) | (Child.access_code == '')).all()

            if children:
                print(f"\n📝 Generating access codes for {len(children)} children...")
                for child in children:
                    child.access_code = generate_unique_code()
                    if not hasattr(child, 'is_active') or child.is_active is None:
                        child.is_active = True
                    print(f"  • {child.name}: {child.access_code}")

                db.session.commit()
                print(f"\n✅ Generated {len(children)} access codes")
            else:
                print("✓ All children already have access codes")

            # Show summary
            print("\n📋 Access Codes Summary:")
            all_children = Child.query.all()
            for child in all_children:
                status = "🟢 Active" if getattr(child, 'is_active', True) else "🔴 Inactive"
                print(f"  {status} {child.name}: {child.access_code}")

            print(f"\n✅ Migration completed! Total children: {len(all_children)}")

        except Exception as e:
            print(f"❌ Error generating codes: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    migrate()
