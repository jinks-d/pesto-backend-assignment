# product_management_service/app.py

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ecommerce'

mongo = PyMongo(app)


# creating a new product
@app.route('/products', methods=['POST'])
@jwt_required()  # Requires authentication to access this endpoint
def create_product():
    data = request.get_json()
    name = data['name']
    price = data['price']
    # Retrieve current user's identity from JWT token
    user_id = get_jwt_identity()
    # Insert new product into MongoDB
    product_id = mongo.db.products.insert_one({
        'name': name,
        'price': price,
        'created_by': ObjectId(user_id)
    }).inserted_id
    return jsonify({'message': 'Product created successfully',
                    'product_id': str(product_id)}), 201


# retrieving all products
@app.route('/products', methods=['GET'])
def get_products():
    products = list(mongo.db.products.find({}, {'created_by': 0}))
    return jsonify(products), 200


if __name__ == '__main__':
    app.run(debug=True)
