import os
from flask import Blueprint, jsonify, request, send_from_directory
from db_model import Cereal, db
from db_operations import import_csv_data
from flask_login import login_required

# Helper function to serialize Cereal objects into dictionaries
def serialize_cereal(cereal):
    return {
        'id': cereal.id,
        'name': cereal.name,
        'mfr': cereal.mfr,
        'type': cereal.type,
        'calories': cereal.calories,
        'protein': cereal.protein,
        'fat': cereal.fat,
        'sodium': cereal.sodium,
        'fiber': cereal.fiber,
        'carbo': cereal.carbo,
        'sugars': cereal.sugars,
        'potass': cereal.potass,
        'vitamins': cereal.vitamins,
        'shelf': cereal.shelf,
        'weight': cereal.weight,
        'cups': cereal.cups,
        'rating': cereal.rating,
    }

bp = Blueprint("main", __name__)

@bp.route('/')
def index():
    """Basic test route to check if the app is running"""
    return "Cereal app is running!"

@bp.route('/cereals', methods=['GET'])
def get_all_cereals():
    """Retrieves all cereals, with optional filtering for exact matches."""
    filterable_fields = {
        "name": str,
        "mfr": str,
        "type": str,
        "calories": int,
        "protein": int,
        "fat": int,
        "sodium": int,
        "fiber": float,
        "carbo": float,
        "sugars": int,
        "potass": int,
        "vitamins": int,
        "shelf": int,
        "weight": float,
        "cups": float,
        "rating": float
    }

    query = Cereal.query
    for field, field_type in filterable_fields.items():
        value = request.args.get(field)
        if value:
            if field_type == str:
                query = query.filter(getattr(Cereal, field).ilike(f"%{value}%"))
            else:
                try:
                    value = field_type(value)
                    query = query.filter(getattr(Cereal, field) == value)
                except ValueError:
                    return jsonify({"error": f"Invalid value for {field}"}), 400

    cereals = query.all()
    return jsonify([serialize_cereal(cereal) for cereal in cereals])

@bp.route('/cereal/<int:id>', methods=['GET'])
def get_cereal(id):
    """Retrieves a specific cereal by ID"""
    cereal = Cereal.query.get(id)
    if cereal:
        return jsonify(serialize_cereal(cereal))
    return jsonify({"message": "Cereal not found!"}), 404

@bp.route('/cereal/<int:id>', methods=['DELETE'])
@login_required  # Only logged-in users allowed
def delete_cereal(id):
    """Deletes a cereal from the database by ID"""
    cereal = Cereal.query.get(id)
    if cereal:
        db.session.delete(cereal)
        db.session.commit()
        return jsonify({"message": "Cereal deleted!"})
    return jsonify({"error": "Cereal not found!"}), 404

@bp.route('/cereal', methods=['POST'])
@login_required  # Only logged-in users allowed
def post_cereal():
    """Creates a new cereal or updates an existing one, depending on the ID."""
    try:
        data = request.json
        cereal_id = data.get("id")  # Try to get ID from request body

        if cereal_id:
            # ID is provided - check if it already exists in the database
            existing_cereal = Cereal.query.get(cereal_id)
            if existing_cereal:
                # Update existing cereal
                for key, value in data.items():
                    if hasattr(existing_cereal, key):  # Ensure the field exists
                        setattr(existing_cereal, key, value)
                db.session.commit()
                return jsonify({"message": "Cereal updated!"}), 200
            else:
                # ID is provided but does not exist - return an error
                return jsonify({"error": "ID must not be chosen manually!"}), 400
        else:
            # Create a new cereal
            new_cereal = Cereal(**data)
            db.session.add(new_cereal)
            db.session.commit()
            return jsonify({"message": "Cereal created!"}), 201

    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 400

@bp.route('/cereal/<int:id>/image', methods=['GET'])
def get_image(id):
    """Retrieves the cereal's image by ID"""
    cereal = Cereal.query.get(id)

    if not cereal:
        return jsonify({"message": "Cereal not found!"}), 404
    
    # Brug image_path direkte fra databasen, ellers brug en standardbillede
    image_path = cereal.image_path or "images/default.jpg"
    image_full_path = os.path.join("static", "images", image_path)
    print(image_full_path)

    # If image exists, send it
    if os.path.exists(image_full_path):
        return send_from_directory(os.path.join("static", "images"), os.path.basename(image_path))
    
    return jsonify({"message": "Image not found!"}), 404
