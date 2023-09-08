from flask import request, jsonify
from pymongo import MongoClient
from passlib.hash import sha256_crypt
from app import app
import logging
from app.auth import authenticate, generate_token
from flask_cors import cross_origin
from bson.objectid import ObjectId
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address


# limiter = Limiter(
#     app,
#     key_func=get_remote_address,
#     default_limits=["5 per minute"]
# )

client = MongoClient(app.config['MONGODB_URI'])
db = client.get_database()

@app.route('/api/login', methods=["POST"])
@cross_origin()
def login():
    # print('We are here')
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')


    if not email or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    user_collection = db['users']
    # app.logger.info(data)
    # app.logger.info(user_collection)

    existing_user = user_collection.find_one({'email': email})

    if existing_user:
        if sha256_crypt.verify(password, existing_user['password']):
            token = generate_token(email)
            return jsonify({'token': token})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    else:
        hashed_password = sha256_crypt.hash(password)
        new_user = {
            'email': email,
            'password': hashed_password
        }
        user_collection.insert_one(new_user)

        token = generate_token(email)
        return jsonify({'token': token})


@app.route('/api/upload', methods=["POST"] )
@cross_origin()
@authenticate
# @limiter.limit("5 per minute")
def upload():

    data = request.get_json()
    image_name = data.get('image_name')
    image_url = data.get('image_url')

    image_collection = db['images']

    data = {
        'image_name':image_name,
        'image_url' : image_url
    }

    response = image_collection.insert_one(data)

    if response.inserted_id:
        inserted_data = {
            '_id': str(response.inserted_id),
            'image_name': image_name,
            'image_url': image_url
    }

    return jsonify(inserted_data)


@app.route('/api/get_image/<string:image_id>', methods=["GET"] )
@cross_origin()
@authenticate
# @limiter.limit("5 per minute")
def getImage(image_id):

    image_collection = db['images']

    try:
        image = image_collection.find_one({'_id': ObjectId(image_id)})
        if image:
            formatted_image = {'_id': str(image['_id']), 'image_url': image['image_url'], 'image_name': image['image_name']}
            return jsonify(formatted_image)
        else:
            return jsonify({'error': 'Image not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500