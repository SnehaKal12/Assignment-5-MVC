import os
from flask import Flask
from models.models import db
from flask_login import LoginManager
from auth.auth import auth_bp  # ✅ Ensure authentication is imported
from controllers.event_controller import event_bp  # ✅ Ensure event management is imported
from models.models import User  # ✅ Ensure User model is imported

app = Flask(__name__)

# ✅ Secure Secret Key for Session Management
app.config['SECRET_KEY'] = os.urandom(24)

# ✅ Database Setup
DATABASE_FOLDER = os.path.join(os.getcwd(), "database")
DATABASE_FILE = os.path.join(DATABASE_FOLDER, "events.db")

if not os.path.exists(DATABASE_FOLDER):
    os.makedirs(DATABASE_FOLDER)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_FILE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ✅ Login Manager Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # ✅ Fix incorrect URL reference

# ✅ Register Blueprints with Correct URL Prefixes
app.register_blueprint(auth_bp)  # ✅ Now "/auth/login" and "/auth/register" will work
app.register_blueprint(event_bp, url_prefix='/events')  # ✅ "/events" routes remain functional

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ✅ Initialize Database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
