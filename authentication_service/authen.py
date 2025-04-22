from flask import Flask, request, jsonify, make_response
from base64_random import gen_random_base64
import time
from utils import log_request


app = Flask(__name__)

@app.before_request
def before_request():
    log_request(request)

#dictionary of tokens and its expiration time
tokens_in_use= {}

#hard coded users since we are not using a database, only an in-memory cache
users_db = {
    "admin1": {"password": "password1", "role": "Administrator"},
    "secretary1": {"password": "password1", "role": "Secretary"},
    "agent1": {"password": "password1", "role": "Agent"},
    "admin2": {"password": "password2", "role": "Administrator"},
    "secretary2": {"password": "password2", "role": "Secretary"},
    "agent2": {"password": "password2", "role": "Agent"}
}


#function that accepts username/password and, if correct, emits a simple token (containing user
#role and a random base-64 string).

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users_db and users_db[username]['password'] == password:
        token = create_token(username)
        return jsonify(token=token), 200
    else:
        return jsonify("Incorrect username or password"), 400
        

#basic token creation logic
def create_token(username):
    create_time = time.time()
    expiration_time = create_time + 3600  # valid for an hour
    role = users_db[username]['role']
    string64 = gen_random_base64(10)

    token = f"{role}:{string64}"

    tokens_in_use[token] = expiration_time

    return token


#function for verifying that the token for a given user is still valid

@app.route('/verify', methods=['POST'])
def verify_token():
    token = request.json.get('token')

    if not token:
        return jsonify("Token is missing"), 400
    
    if token in tokens_in_use:
        current_time = time.time()
        expiration_time = tokens_in_use[token]

        if current_time > expiration_time:
            del tokens_in_use[token]
            return jsonify("Token has expired"), 400

        return jsonify("Token is valid"), 200
    else:
        return jsonify("Token is invalid"), 400

if __name__ == '__main__':
    app.run(debug=False, port=5000)