from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# Configure application
app = Flask(__name__)

app.config["SECRET_KEY"] = 'b0c0e2a87f5810f740c4425308121def'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


from app import routes
