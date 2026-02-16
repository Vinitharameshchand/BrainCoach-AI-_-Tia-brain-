from flask import Flask, render_to_view
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

    # Create database tables
    with app.app_context():
        db.create_all()
        # Seed initial data if needed
        # seed_data()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
