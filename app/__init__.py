from flask import Flask
from config import Config
from app.extensions import db, login
from app.models import User, Question, Answer, Tag, Notification

import re
from markupsafe import Markup

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login.init_app(app)
    login.login_view = 'main.login'  

    # Register routes
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # ✅ Register Jinja filter for @mentions
    def highlight_mentions(text):
        pattern = r'@(\w+)'  # matches @username
        return Markup(re.sub(pattern, r'<span class="mention">@\1</span>', text))
    
    app.jinja_env.filters['highlight_mentions'] = highlight_mentions

    return app
