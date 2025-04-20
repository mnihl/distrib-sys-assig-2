from flask import Flask, request, jsonify
from db import init_db, get_connection
from auth import token_required, roles_required
from models import add_transaction, update_transaction, get_prediction_result
from utils import log_request

txn_app = Flask(__name__)
init_db()

@txn_app.before_request
def before_request():
    log_request(request)

@txn_app.route("/")
def index():
    return "Welcome to the Transaction Service!"

@txn_app.route('/transaction', methods=['POST'])
@token_required
@roles_required(['agent', 'administrator'])
def create_transaction():
    data = request.json
    result = add_transaction(data)
    return jsonify(result), 201

@txn_app.route('/transaction/<int:transaction_id>', methods=['PUT'])
@token_required
@roles_required(['agent', 'administrator'])
def modify_transaction(transaction_id):
    data = request.json
    result = update_transaction(transaction_id, data)
    return jsonify(result)

@txn_app.route('/result/<int:transaction_id>', methods=['GET'])
@token_required
@roles_required(['agent', 'administrator'])
def get_result(transaction_id):
    result = get_prediction_result(transaction_id)
    return jsonify(result)

#Function to inject test data into the database, as the POST method in transactions does not do that
def add_test_result(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO results (transaction_id, timestamp, is_fraudulent, confidence)
        VALUES (?, ?, ?, ?)
    ''', (transaction_id, '2025-04-20T14:05:00', False, 0.95))
    conn.commit()
    conn.close()

add_test_result(1)  # Use the correct transaction_id

if __name__ == '__main__':
    txn_app.run(debug=False, port = 5001)
