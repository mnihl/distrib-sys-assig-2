from flask import Flask
from flask_restx import Api

def create_app():
    auth_app = Flask(__name__)
    auth_api = Api(auth_app, title="Fraud detection system")

    # add individual namespaces
    #auth_api.add_namespace()


    return auth_app

if __name__ == '__main__':
    create_app().run(debug=False, port=5000)
