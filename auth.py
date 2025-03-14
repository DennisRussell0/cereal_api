from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from db_model import db, User
from werkzeug.security import check_password_hash

bcrypt = Bcrypt()

# Hash password (for user registration)
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

# Check password (for login)
def check_password(hashed_password, password):
    return bcrypt.check_password_hash(hashed_password, password)

auth_bp = Blueprint("auth", __name__)

# Route for user login (POST) – Public
@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticates a user and logs them in if credentials are correct."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password(user.password_hash, password):
        return jsonify({"message": "Invalid username or password"}), 401

    # Flask-Login login_user
    login_user(user)

    return jsonify({"message": "Login successful"})

# Route for user logout (POST) – Protected
@auth_bp.route('/logout', methods=['POST'])
@login_required  # Only logged-in users allowed
def logout():
    """Logs out the currently authenticated user."""
    logout_user()
    return jsonify({"message": "Logout successful"})
