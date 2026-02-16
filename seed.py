from app import create_app
from models import db, Module, Exercise

def seed_data():
    app = create_app()
    with app.app_context():
        # Add a default module
        if not Module.query.filter_by(name='Beginner Finger Yoga').first():
            module = Module(name='Beginner Finger Yoga', category='Concentration', difficulty='Easy')
            db.session.add(module)
            db.session.commit()
            
            # Add an exercise
            exercise = Exercise(
                module_id=module.id,
                title='Basic Finger Yoga',
                video_url='https://www.w3schools.com/html/mov_bbb.mp4',
                accuracy_threshold=80.0,
                duration_seconds=60
            )
            db.session.add(exercise)
            db.session.commit()
            print("Seed data created successfully!")

if __name__ == '__main__':
    seed_data()
