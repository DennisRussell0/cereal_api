# Defines the database models (Cereal, User) and manages the database structure

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()  # Create a database instance
bcrypt = Bcrypt()

class Cereal(db.Model):
    """Represents a cereal product in the database."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    mfr = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)
    fat = db.Column(db.Integer, nullable=False)
    sodium = db.Column(db.Integer, nullable=False)
    fiber = db.Column(db.Float, nullable=False)
    carbo = db.Column(db.Float, nullable=False)
    sugars = db.Column(db.Integer, nullable=False)
    potass = db.Column(db.Integer, nullable=False)
    vitamins = db.Column(db.Integer, nullable=False)
    shelf = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    cups = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(200), nullable=True)

class User(db.Model, UserMixin):
    """Represents a user account in the database."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def check_password(self, password):
        """Verifies if the given password matches the stored hashed password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    # Method to hash a password when creating a user
    def set_password(self, password):
        """Hashes and stores the given password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
