# Application factory for creating and configuring the Flask app

from flask import Flask, jsonify
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from db_model import db, User
from config import Config
from routes import bp
from auth import auth_bp

def create_app():
    """Creates and configures a Flask application instance."""
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration settings
    db.init_app(app)  # Initialize the database with the app

    # Initialize Flask-Login and Flask-Bcrypt
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # Redirect unauthorized users to the login page

    bcrypt = Bcrypt(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Flask-Login requires a user loader function to retrieve users from the session
    @login_manager.user_loader
    def load_user(user_id):
        """Loads a user from the database based on their user ID."""
        return User.query.get(int(user_id))
    
    # Handler for unauthorized access
    @login_manager.unauthorized_handler
    def unauthorized():
        """Returns an error response when a user is not authorized."""
        return jsonify({"error": "Unauthorized. Please log in."}), 401
    
    # Register application blueprints
    app.register_blueprint(bp)  # Register routes for cereals
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Register authentication routes under /auth

    return app
