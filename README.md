# Project Title

A REST API to manage and retrieve data about various cereal products, with support for CRUD operations, filtering, and user authentication.

## Description

This project implements a REST API for managing breakfast cereal data stored in a local SQLite database. The API supports CRUD operations (Create, Read, Update, Delete) on cereal products, allows filtering based on nutritional information, and ensures secure access via user authentication. Viewing products is accessible for all, while adding, updating and deleting cereal products is limited to authorized users only.

## Getting Started

### Dependencies

* Python
* Flask
* SQLite (built-in database)
* bcrypt for password hashing

### Installing

* Clone the repository to your local machine:
    * git clone https://github.com/dennisrussell0/cereal_api.git
    * cd cereal_api
    
* Install the required dependencies:
    * pip install -r requirements.txt

### Executing program

Once you’ve installed the dependencies, follow these steps to run the program:

* Initialize the database: This step creates the database tables and imports data from the CSV file. If you've already run this before, it will reset the database::
    ```
    python init_db.py
    ```

* Start the Flask application: This command runs the Flask development server:
    ```
    python app.py
    ```

* The application will be running on http://127.0.0.1:5000/. 

    You can now test the following API endpoints using a tool like Postman:

    GET /cereals
    Fetch a list of all cereal products.

    GET /cereal/{id}
    Fetch a specific cereal product by its ID.

    POST /auth/login
    Log in to access restricted endpoints (POST and DELETE). Send raw JSON in the body:
        ```json
        {
            "username": "admin",
            "password": "adminpassword"
        }
        ```

    POST /auth/logout
    Log out.

    POST /cereal
    Add a new cereal product (omit ID for new products) or update an existing product (include the ID). Requires authentication. Example JSON for updating product with ID 1:
        ```json
        {
            "calories": 70,
            "carbo": 5.0,
            "cups": 0.33,
            "fat": 1,
            "fiber": 10.0,
            "id": 1,
            "mfr": "N",
            "name": "100% Brandy",
            "potass": 280,
            "protein": 4,
            "rating": 68402973.0,
            "shelf": 3,
            "sodium": 130,
            "sugars": 6,
            "type": "C",
            "vitamins": 25,
            "weight": 1.0
        }
        ```
    If you want to add a new product, just exclude ID.

    DELETE /cereal/{id}
    Delete a cereal product by its ID. This endpoint also requires authentication.

    GET /cereals?calories=120 (as an example)
    Filter products based on calories (exact match).

    GET /cereals?mfr=k (as an example)
    Filter products based on manufacturer.

    GET /cereals?mfr=k&calories=100 (as an example)
    Filter products based on manufacturer and calories.

    GET /cereal/{id}/image
    Fetch the image for a specific product.

## Author

Dennis Russell
[@DennisRussell0](https://github.com/DennisRussell0)

## Version History

* 0.1
    * Initial Release