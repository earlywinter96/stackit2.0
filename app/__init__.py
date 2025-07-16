from flask import Flask
from app.extensions import db, login
from flask_migrate import Migrate
import os

migrate = Migrate()
login.login_view = 'auth.login'

def create_app():
    print("✅ Starting create_app()")

    if os.environ.get("VERCEL"):
        instance_path = "/tmp/instance"
    else:
        instance_path = None

    app = Flask(__name__, instance_path=instance_path)
    app.config.from_object('config.Config')
    print("✅ Config loaded")

    # ✅ Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # ✅ Register blueprints
    from app.auth import bp as auth_bp
    from app.main.routes import bp as main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # ✅ Always run DB setup (local + Vercel)
    with app.app_context():
        from app.models import User, Tag  # Make sure Tag is imported
        db.create_all()
        if not User.query.filter_by(username='GeminiAI').first():
            bot = User(username='GeminiAI', email='gemini@app.bot', is_bot=True)
            db.session.add(bot)
            db.session.commit()
        print("✅ DB initialized with GeminiAI user")

    return app
