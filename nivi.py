from flask import Flask, render_template
from flask_cors import CORS
from flask_login import LoginManager
from models import db, Parent
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Parent.query.get(int(user_id))

    # Register blueprints
    from routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from routes.dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)

    from routes.session import session as session_blueprint
    app.register_blueprint(session_blueprint)

    from routes.analytics import analytics as analytics_blueprint
    app.register_blueprint(analytics_blueprint, url_prefix='/analytics')

    from routes.student import student as student_blueprint
    app.register_blueprint(student_blueprint)

    @app.route('/')
    def landing():
        return render_template('landing.html')

    @app.route('/seed')
    def run_seed():
        from models import db, Module, Exercise
        try:
            if not Module.query.filter_by(name='Beginner Finger Yoga').first():
                module = Module(name='Beginner Finger Yoga', category='Concentration', difficulty='Easy')
                db.session.add(module)
                db.session.commit()
                
                exercise = Exercise(
                    module_id=module.id,
                    title='Basic Finger Yoga',
                    video_url='https://www.w3schools.com/html/mov_bbb.mp4',
                    accuracy_threshold=80.0,
                    duration_seconds=60
                )
                db.session.add(exercise)
                db.session.commit()
            return "Seed complete! You can now check your dashboard."
        except Exception as e:
            return f"Error: {str(e)}"

    # Create database tables
    with app.app_context():
        db.create_all()
        # Seed initial data if needed
        # seed_data()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
