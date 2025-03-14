# Handles database operations such as clearing and importing CSV data

import csv
import os
import re
from db_model import Cereal, db, User

def create_admin_user():
    """Creates an admin user if it does not already exist."""
    admin = User.query.filter_by(username='admin').first()  # Check if admin user exists
    if not admin:
        admin = User(username='admin')  # Create admin user
        admin.set_password('adminpassword')  # Set a default password
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")
    else:
        print("Admin user already exists.")

def clear_database():
    """Deletes all records from the Cereal table."""
    db.session.query(Cereal).delete()
    db.session.commit()
    db.session.close()  # Close session to free up resources
    print("Database cleared!")

def import_csv_data():
    """Reads data from the CSV file and inserts it into the database."""
    try:
        with open('data/Cereal.csv', mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter=';')
            
            # Skip the first two rows (headers + data types)
            next(csv_reader)
            next(csv_reader)
            
            for row in csv_reader:
                try:
                    cereal_name = row[0].strip()
                    image_path = find_image_for_cereal(cereal_name)  # Find matching image
                    
                    # Create a new Cereal object and add it to the database
                    cereal = Cereal(
                        name=cereal_name,
                        mfr=row[1].strip(),
                        type=row[2].strip(),
                        calories=int(row[3]),
                        protein=int(row[4]),
                        fat=int(row[5]),
                        sodium=int(row[6]),
                        fiber=float(row[7]),
                        carbo=float(row[8]),
                        sugars=int(row[9]),
                        potass=int(row[10]),
                        vitamins=int(row[11]),
                        shelf=int(row[12]),
                        weight=float(row[13]),
                        cups=float(row[14]),
                        rating=float(row[15].replace('.', '')),
                        image_path=image_path  # Store image path in the database
                    )
                    db.session.add(cereal)
                except (IndexError, ValueError) as e:
                    print(f"Skipping row due to error: {e}")

            db.session.commit()  # Commit the changes to the database
            db.session.close()  # Close session to avoid leaks
            print("CSV data imported successfully!")

    except FileNotFoundError:
        print("Error: CSV file not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")

def normalize_name(name):
    """Removes spaces, special characters, and converts to lowercase to match file names."""
    name = name.lower()  # Convert to lowercase
    name = re.sub(r'[^a-z0-9]', '', name)  # Remove non-alphanumeric characters
    return name

def find_image_for_cereal(cereal_name):
    """Finds the best matching image file based on the product name."""
    image_folder = "static\images"
    
    # Ensure the image folder exists
    if not os.path.exists(image_folder):
        print(f"Warning: Image folder '{image_folder}' not found.")
        return None

    normalized_cereal_name = normalize_name(cereal_name)

    # Iterate through all files in static/images/
    for filename in os.listdir(image_folder):
        normalized_filename = normalize_name(os.path.splitext(filename)[0])  # Remove file extension (.jpg, .png)

        if normalized_cereal_name == normalized_filename:  # Compare normalized names
            return (filename)  # Return full path to the image

    return None  # No match found
