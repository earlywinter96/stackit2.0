from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()

# Set the login view route — update if your login route is namespaced
login.login_view = 'main.login'  # 'main' = blueprint name, 'login' = function name
login.login_message_category = 'info'
