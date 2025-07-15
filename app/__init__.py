from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.models import User
import os

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message_category = 'info'

def create_app():
    print("✅ Starting create_app()")
    app = Flask(__name__)
    app.config.from_object('config.Config')
    print("✅ Config loaded")

    # ✅ Handle instance folder creation only if writable
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        print("⚠️ Skipping instance folder creation (read-only file system)")

    # ✅ Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # ✅ Register blueprints
    from app.auth import bp as auth_bp
    from app.main import bp as main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # ✅ Only run this in dev/local environment
    if not os.environ.get("VERCEL"):  # Only do this locally
        with app.app_context():
            db.create_all()
            if not User.query.filter_by(username='GeminiAI').first():
                bot = User(username='GeminiAI', email='gemini@app.bot', is_bot=True)
                db.session.add(bot)
                db.session.commit()
            print("✅ Local DB initialized with GeminiAI user")

    return app
