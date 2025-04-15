from flask import Flask, request
 #function that accepts username/password and, if correct, emits a simple token (containing user
 #role and a random base-64 string).

#app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')



 # function for verifying that the token for a given user is still valid

#app.route('/verify', methods=['POST'])
def verify_token():
    pass
