import os
from flask import Flask
from dotenv import load_dotenv
from models import db
from routes import api

def create_app():
    # Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)

    # Configurations from .env
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.environ.get('SECRET_KEY')

    # Optional: email and redis/celery
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['REDIS_URL'] = os.environ.get('REDIS_URL')

    # Init DB and register blueprints
    db.init_app(app)
    app.register_blueprint(api, url_prefix='/api')

    with app.app_context():
        db.create_all()
        # --- Create default admin if absent ---
        from werkzeug.security import generate_password_hash
        from models import User
        if not User.query.filter_by(role='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('adminpassword', method='scrypt'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()

    return app
