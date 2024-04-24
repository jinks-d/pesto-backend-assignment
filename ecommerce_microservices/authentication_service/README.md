# User Authentication Service

This service handles user registration, login, and authentication for the e-commerce application.

### Endpoints:
- `/register` (POST): Register a new user.
- `/login` (POST): Log in an existing user and generate JWT token.
- `/logout` (POST): Log out the user.

### Dependencies:
- Flask
- Flask-Security
- Flask-PyMongo
- Flask-JWT-Extended

### Usage:
1. Install dependencies: `pip install -r requirements.txt`
2. Run the service: `python app.py`

Make sure MongoDB is running locally on port 27017.
