from flask import Flask
from config import Config
from app.extensions import db, login
from app.models import User, Question, Answer, Tag, Notification

import re
from markupsafe import Markup

def create_app():
    print("✅ Starting create_app()")  # <-- Debug line

    app = Flask(__name__)
    app.config.from_object(Config)
    print("✅ Config loaded")

    db.init_app(app)
    print("✅ DB initialized")

    login.init_app(app)
    login.login_view = 'main.login'
    print("✅ Login initialized")

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    print("✅ Routes registered")

    @app.before_first_request
    def ensure_gemini_user():
        from app.models import User
        from werkzeug.security import generate_password_hash
        if not User.query.filter_by(username='GeminiAI').first():
            user = User(
                username='GeminiAI',
                email='gemini@stackit.com',
                password_hash=generate_password_hash('gemini123'),
                role='ADMIN'
            )
            db.session.add(user)
            db.session.commit()
        print("✅ GeminiAI user ensured")

    def highlight_mentions(text):
        import re
        from markupsafe import Markup
        pattern = r'@(\w+)'
        return Markup(re.sub(pattern, r'<span class=\"mention\">@\1</span>', text))
    
    app.jinja_env.filters['highlight_mentions'] = highlight_mentions
    print("✅ Mention filter registered")

    return app
