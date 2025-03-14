# Initializes the database (creates tables, clears existing data, and re-imports CSV data)

from app_factory import create_app
from db_model import db
from db_operations import clear_database, import_csv_data, create_admin_user

app = create_app()  # Create app here instead of importing from app.py to avoid circular imports

with app.app_context():  # Use the app context to interact with the database
    db.create_all()  # Ensure that all tables are created
    clear_database()  # Clear the database (remove existing data)
    import_csv_data()  # Re-import the CSV data into the database
    create_admin_user()  # Create an admin user in the database
    print("Database reset, CSV data imported, and admin user created!")
