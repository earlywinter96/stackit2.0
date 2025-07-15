from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    existing = User.query.filter_by(username='GeminiAI').first()
    if not existing:
        dummy_password = generate_password_hash("bot_secret_password")
        gemini_user = User(
            username='GeminiAI',
            email='gemini@ai.com',
            password_hash=dummy_password,
            role='BOT'
        )
        db.session.add(gemini_user)
        db.session.commit()
        print("✅ GeminiAI user created.")
    else:
        print("ℹ️ GeminiAI user already exists.")
