from flask import Flask

app = Flask(__name__)
#flask secret key
# generate a secret key in command prompt using this command:
# `python -c 'import os; print(os.urandom(16))'`
app.config['SECRET_KEY'] = b'\xce}2\xac\x05\xbb\x9dM\x81\xad5\xa5\x97]\x8f?'
