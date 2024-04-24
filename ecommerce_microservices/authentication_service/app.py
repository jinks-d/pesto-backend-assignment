# authentication_service/app.py

from flask import Flask, jsonify, request
from flask_security import Security, MongoEngineUserDatastore, RoleMixin
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash

# Initialize Flask app
app = Flask(__name__)


# Secret key for JWT token generation
app.config['SECRET_KEY'] = 'super-secret'


# MongoDB connection URI
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ecommerce'
# Initialize PyMongo for MongoDB connection
mongo = PyMongo(app)


# Define MongoDB Document for User model
class User(mongo.Document):
    # Unique username for each user
    username = mongo.StringField(unique=True)
    # Password hash for user authentication
    password = mongo.StringField()
    # Roles assigned to the user (e.g., admin, customer)
    roles = mongo.ListField(mongo.StringField())


# Initialize Flask-Security for user authentication and authorization
user_datastore = MongoEngineUserDatastore(mongo, User, RoleMixin)
# Initialize Flask-Security extension
security = Security(app, user_datastore)


# Initialize Flask-JWT-Extended for JWT token generation and authentication
jwt = JWTManager(app)


# user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    # Generate password hash for security
    password = generate_password_hash(data['password'])
    # Create a new user with provided username and hashed password
    user_datastore.create_user(username=username, password=password)
    return jsonify({'message': 'User registered successfully'}), 201


# user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    # Find user by username
    user = user_datastore.get_user(username=username)
    # Check if user exists and password is correct
    if user and user_datastore.check_password(user.password, password):
        # Generate JWT token for authenticated user
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


# user logout
@app.route('/logout', methods=['POST'])
@jwt_required()  # User must be logged in (authenticated) to access this
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
